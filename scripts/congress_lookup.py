#!/usr/bin/env python3
"""
Congress.gov API helper for We The People.

Reads CONGRESS_API_KEY from the environment. Get a free key at:
  https://api.data.gov/signup/

Usage:
  python3 congress_lookup.py bill --congress 119 --type hr --number 22
  python3 congress_lookup.py cosponsors --congress 119 --type hr --number 22
  python3 congress_lookup.py text --congress 119 --type hr --number 22
  python3 congress_lookup.py member --bioguide-id R000614
  python3 congress_lookup.py sponsored --bioguide-id R000614

Bill types: hr, hres, hjres, hconres, s, sres, sjres, sconres
Congress numbers: 117 (2021-2022), 118 (2023-2024), 119 (2025-2026), etc.

All output is CSV-friendly (printed to stdout). Pipe to a file:
  python3 congress_lookup.py cosponsors --congress 119 --type hr --number 22 \\
    > cosponsors-HR22.csv
"""

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://api.congress.gov/v3"


def get_api_key():
    key = os.environ.get("CONGRESS_API_KEY")
    if not key:
        print(
            "ERROR: CONGRESS_API_KEY environment variable not set.\n"
            "Get a free key at https://api.data.gov/signup/ and set it:\n"
            "  export CONGRESS_API_KEY=<your-api-data-gov-key>",
            file=sys.stderr,
        )
        sys.exit(2)
    return key


def api_get(endpoint, params=None):
    if params is None:
        params = {}
    params["api_key"] = get_api_key()
    params["format"] = "json"
    qs = urllib.parse.urlencode(params, doseq=True)
    url = f"{API_BASE}{endpoint}?{qs}"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"Congress.gov API error: {e.code} {e.reason} - {url}", file=sys.stderr)
        sys.exit(3)
    except urllib.error.URLError as e:
        print(f"Network error: {e}", file=sys.stderr)
        sys.exit(3)


def cmd_bill(args):
    """Get bill metadata: title, sponsor, status, latest action."""
    data = api_get(f"/bill/{args.congress}/{args.type}/{args.number}")
    bill = data.get("bill", {})
    fields = [
        ("congress", bill.get("congress")),
        ("type", bill.get("type")),
        ("number", bill.get("number")),
        ("title", bill.get("title")),
        ("introduced_date", bill.get("introducedDate")),
        ("origin_chamber", bill.get("originChamber")),
        ("policy_area", (bill.get("policyArea") or {}).get("name")),
        ("latest_action_date", (bill.get("latestAction") or {}).get("actionDate")),
        ("latest_action", (bill.get("latestAction") or {}).get("text")),
        ("sponsor_name", _first_sponsor_field(bill, "fullName")),
        ("sponsor_bioguide", _first_sponsor_field(bill, "bioguideId")),
        ("sponsor_party", _first_sponsor_field(bill, "party")),
        ("sponsor_state", _first_sponsor_field(bill, "state")),
        ("cosponsor_count", (bill.get("cosponsors") or {}).get("count")),
        ("congress_gov_url", bill.get("url")),
    ]
    for k, v in fields:
        print(f"{k}: {v if v is not None else ''}")


def _first_sponsor_field(bill, field):
    sponsors = bill.get("sponsors") or [{}]
    return sponsors[0].get(field) if sponsors else None


def cmd_cosponsors(args):
    """List all cosponsors for a bill."""
    all_results = []
    offset = 0
    limit = 250
    while True:
        data = api_get(
            f"/bill/{args.congress}/{args.type}/{args.number}/cosponsors",
            {"limit": limit, "offset": offset},
        )
        results = data.get("cosponsors", [])
        if not results:
            break
        all_results.extend(results)
        if len(results) < limit:
            break
        offset += limit

    writer = csv.writer(sys.stdout)
    writer.writerow(["bioguide_id", "full_name", "party", "state", "district",
                     "sponsorship_date", "is_original", "withdrawn"])
    for r in all_results:
        writer.writerow([
            r.get("bioguideId"),
            r.get("fullName"),
            r.get("party"),
            r.get("state"),
            r.get("district"),
            r.get("sponsorshipDate"),
            r.get("isOriginalCosponsor"),
            r.get("sponsorshipWithdrawnDate") or "",
        ])


def cmd_text(args):
    """Get URLs for bill text in various formats (PDF, XML, HTML)."""
    data = api_get(f"/bill/{args.congress}/{args.type}/{args.number}/text")
    versions = data.get("textVersions", [])
    print(f"# Found {len(versions)} text version(s) for "
          f"{args.type.upper()}{args.number} ({args.congress}th Congress)\n")
    for v in versions:
        print(f"Version: {v.get('type')} (date: {v.get('date')})")
        for fmt in v.get("formats", []):
            print(f"  {fmt.get('type')}: {fmt.get('url')}")
        print()


def cmd_member(args):
    """Get member metadata by bioguide ID."""
    data = api_get(f"/member/{args.bioguide_id}")
    member = data.get("member", {})
    fields = [
        ("bioguide_id", member.get("bioguideId")),
        ("full_name", member.get("directOrderName") or member.get("invertedOrderName")),
        ("party", _current_party(member)),
        ("state", member.get("state")),
        ("district", member.get("district")),
        ("birth_year", member.get("birthYear")),
        ("served_terms", _term_summary(member)),
        ("congress_gov_url", member.get("url")),
    ]
    for k, v in fields:
        print(f"{k}: {v if v is not None else ''}")


def _current_party(member):
    history = member.get("partyHistory") or []
    return history[-1].get("partyName") if history else None


def _term_summary(member):
    terms = member.get("terms") or []
    return "; ".join(
        f"{t.get('chamber','?')}:{t.get('startYear','?')}-{t.get('endYear','present')}"
        for t in terms
    )


def cmd_sponsored(args):
    """List bills sponsored by a member."""
    all_results = []
    offset = 0
    limit = 250
    while True:
        data = api_get(
            f"/member/{args.bioguide_id}/sponsored-legislation",
            {"limit": limit, "offset": offset},
        )
        results = data.get("sponsoredLegislation", [])
        if not results:
            break
        all_results.extend(results)
        if len(results) < limit or offset >= args.max:
            break
        offset += limit

    writer = csv.writer(sys.stdout)
    writer.writerow(["congress", "type", "number", "title", "introduced_date",
                     "policy_area", "latest_action"])
    for r in all_results:
        writer.writerow([
            r.get("congress"),
            r.get("type"),
            r.get("number"),
            r.get("title"),
            r.get("introducedDate"),
            (r.get("policyArea") or {}).get("name"),
            (r.get("latestAction") or {}).get("text"),
        ])


def main():
    parser = argparse.ArgumentParser(description="Congress.gov API helper for We The People.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_bill = sub.add_parser("bill", help="Get bill metadata")
    p_bill.add_argument("--congress", type=int, required=True, help="e.g. 119")
    p_bill.add_argument("--type", required=True, help="hr, hres, hjres, hconres, s, sres, sjres, sconres")
    p_bill.add_argument("--number", type=int, required=True)
    p_bill.set_defaults(func=cmd_bill)

    p_co = sub.add_parser("cosponsors", help="List cosponsors of a bill")
    p_co.add_argument("--congress", type=int, required=True)
    p_co.add_argument("--type", required=True)
    p_co.add_argument("--number", type=int, required=True)
    p_co.set_defaults(func=cmd_cosponsors)

    p_text = sub.add_parser("text", help="Get bill text URLs")
    p_text.add_argument("--congress", type=int, required=True)
    p_text.add_argument("--type", required=True)
    p_text.add_argument("--number", type=int, required=True)
    p_text.set_defaults(func=cmd_text)

    p_mem = sub.add_parser("member", help="Get member metadata")
    p_mem.add_argument("--bioguide-id", required=True)
    p_mem.set_defaults(func=cmd_member)

    p_sp = sub.add_parser("sponsored", help="List bills sponsored by a member")
    p_sp.add_argument("--bioguide-id", required=True)
    p_sp.add_argument("--max", type=int, default=1000, help="Max results to fetch")
    p_sp.set_defaults(func=cmd_sponsored)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
