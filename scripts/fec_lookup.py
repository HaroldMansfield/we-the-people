#!/usr/bin/env python3
"""
FEC OpenFEC API helper for We The People.

Reads FEC_API_KEY from the environment. Get a free key at:
  https://api.data.gov/signup/

Usage:
  python3 fec_lookup.py candidate --name "Roy, Chip"
  python3 fec_lookup.py candidate --name "Roy" --state TX
  python3 fec_lookup.py top_donors --candidate-id H8TX21000 --cycle 2024
  python3 fec_lookup.py committees --candidate-id H8TX21000

All output is CSV-friendly (printed to stdout). Pipe to a file:
  python3 fec_lookup.py top_donors --candidate-id H8TX21000 --cycle 2024 \\
    > roy-2024-top-donors.csv
"""

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://api.open.fec.gov/v1"


def get_api_key():
    key = os.environ.get("FEC_API_KEY")
    if not key:
        print(
            "ERROR: FEC_API_KEY environment variable not set.\n"
            "Get a free key at https://api.data.gov/signup/ and set it:\n"
            "  export FEC_API_KEY=<your-api-data-gov-key>",
            file=sys.stderr,
        )
        sys.exit(2)
    return key


def api_get(endpoint, params):
    params["api_key"] = get_api_key()
    qs = urllib.parse.urlencode(params, doseq=True)
    url = f"{API_BASE}{endpoint}?{qs}"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"FEC API error: {e.code} {e.reason} - {url}", file=sys.stderr)
        sys.exit(3)
    except urllib.error.URLError as e:
        print(f"Network error: {e}", file=sys.stderr)
        sys.exit(3)


def cmd_candidate(args):
    """Find candidates by name."""
    params = {"q": args.name, "per_page": 50}
    if args.state:
        params["state"] = args.state
    if args.office:
        params["office"] = args.office
    data = api_get("/candidates/search/", params)

    writer = csv.writer(sys.stdout)
    writer.writerow(["candidate_id", "name", "party", "office", "state",
                     "district", "incumbent_challenge"])
    for r in data.get("results", []):
        writer.writerow([
            r.get("candidate_id"),
            r.get("name"),
            r.get("party"),
            r.get("office"),
            r.get("state"),
            r.get("district"),
            r.get("incumbent_challenge_full"),
        ])


def cmd_committees(args):
    """List committees affiliated with a candidate."""
    data = api_get(f"/candidate/{args.candidate_id}/committees/", {"per_page": 50})
    writer = csv.writer(sys.stdout)
    writer.writerow(["committee_id", "name", "designation", "type", "state"])
    for r in data.get("results", []):
        writer.writerow([
            r.get("committee_id"),
            r.get("name"),
            r.get("designation_full"),
            r.get("committee_type_full"),
            r.get("state"),
        ])


def cmd_top_donors(args):
    """Top contributing employers to a candidate's principal committee."""
    cand_data = api_get(f"/candidate/{args.candidate_id}/committees/", {"per_page": 50})
    principal = None
    for r in cand_data.get("results", []):
        if r.get("designation") == "P":
            principal = r.get("committee_id")
            break
    if not principal:
        print(f"No principal committee found for {args.candidate_id}", file=sys.stderr)
        sys.exit(4)

    params = {
        "committee_id": principal,
        "cycle": args.cycle,
        "per_page": args.limit,
        "sort": "-total",
    }
    data = api_get("/schedules/schedule_a/by_employer/", params)

    writer = csv.writer(sys.stdout)
    writer.writerow(["employer", "total", "count", "cycle", "committee_id"])
    for r in data.get("results", []):
        writer.writerow([
            r.get("employer"),
            r.get("total"),
            r.get("count"),
            r.get("cycle"),
            principal,
        ])


def cmd_pac_contributions(args):
    """Individual contributions to a candidate."""
    cand_data = api_get(f"/candidate/{args.candidate_id}/committees/", {"per_page": 50})
    principal = None
    for r in cand_data.get("results", []):
        if r.get("designation") == "P":
            principal = r.get("committee_id")
            break
    if not principal:
        print(f"No principal committee found for {args.candidate_id}", file=sys.stderr)
        sys.exit(4)

    params = {
        "committee_id": principal,
        "two_year_transaction_period": args.cycle,
        "per_page": args.limit,
        "sort": "-contribution_receipt_amount",
    }
    data = api_get("/schedules/schedule_a/", params)

    writer = csv.writer(sys.stdout)
    writer.writerow(["contributor_name", "amount", "date",
                     "contributor_employer", "contributor_occupation"])
    for r in data.get("results", []):
        writer.writerow([
            r.get("contributor_name"),
            r.get("contribution_receipt_amount"),
            r.get("contribution_receipt_date"),
            r.get("contributor_employer"),
            r.get("contributor_occupation"),
        ])


def main():
    parser = argparse.ArgumentParser(description="FEC OpenFEC API helper for We The People.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_cand = sub.add_parser("candidate", help="Search candidates by name")
    p_cand.add_argument("--name", required=True, help='Lastname or "Lastname, Firstname"')
    p_cand.add_argument("--state", help="Two-letter state code")
    p_cand.add_argument("--office", help="H (House), S (Senate), or P (President)")
    p_cand.set_defaults(func=cmd_candidate)

    p_com = sub.add_parser("committees", help="List committees for a candidate")
    p_com.add_argument("--candidate-id", required=True)
    p_com.set_defaults(func=cmd_committees)

    p_td = sub.add_parser("top_donors", help="Top contributing employers to a candidate")
    p_td.add_argument("--candidate-id", required=True)
    p_td.add_argument("--cycle", type=int, required=True, help="Election cycle (e.g. 2024)")
    p_td.add_argument("--limit", type=int, default=50)
    p_td.set_defaults(func=cmd_top_donors)

    p_pac = sub.add_parser("pac_contributions", help="Individual contributions to a candidate")
    p_pac.add_argument("--candidate-id", required=True)
    p_pac.add_argument("--cycle", type=int, required=True)
    p_pac.add_argument("--limit", type=int, default=100)
    p_pac.set_defaults(func=cmd_pac_contributions)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
