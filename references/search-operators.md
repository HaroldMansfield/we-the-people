# Search Operators for Legislative Lookup

Google search operators tailored for legislative work. Use these instead of plain keyword searches. operators turn 10,000 noisy results into 10 useful ones.

---

## Operator quick reference

| Operator | What it does | Track |
|---|---|---|
| `site:` | Restrict to a domain | 1 |
| `inurl:` | URL must contain term | 1 |
| `intitle:` | Page title must contain term | 1 |
| `intext:` | Page body must contain term | 1 |
| `filetype:` / `ext:` | File type filter | 1 |
| `"exact phrase"` | Exact string match | 1 |
| `-term` | Exclude term or site | 1 |
| `OR` / `\|` | Boolean OR | 1 |
| `*` | Wildcard | 1 |
| `cache:` | Cached page version | 2 only |
| `related:` | Find similar sites | 2 only |
| `AROUND(n)` | Words within N of each other | 2 only |
| `before:` / `after:` | Date range filter | 2 only |

**Track 1** = web_search tool. Most operators work.
**Track 2** = browser > Google. Required for `cache:`, `related:`, `AROUND()`, `before:`, `after:`.

---

## Bill identification

```
"H.R. 22" site:congress.gov
"H.R. 22" site:govtrack.us
"[act name]" site:congress.gov
"[act name]" site:govtrack.us

"HB 100" "[state name]" site:legiscan.com
"HB 100" site:ballotpedia.org
"SB 1047" site:legiscan.com

"[act name]" (introduced OR sponsor OR cosponsor) site:congress.gov
"[bill number]" filetype:pdf site:congress.gov
```

## Prior versions of a bill

```
"[act name]" site:congress.gov (prior OR previous OR session)
"[act name]" site:govtrack.us
"[act name]" "introduced"

# Track 2 only: date range to find earlier introductions
"[act name]" site:congress.gov before:2024-01-01
```

## Sponsor biographical lookup

```
"FirstName LastName" site:votesmart.org
"FirstName LastName" site:ballotpedia.org
"FirstName LastName" site:congress.gov
"FirstName LastName" (bio OR biography OR background) filetype:pdf
"FirstName LastName" site:linkedin.com
```

## Sponsor social media

```
"FirstName LastName" site:twitter.com OR site:x.com
"FirstName LastName" site:facebook.com
"FirstName LastName" site:instagram.com
"FirstName LastName" site:youtube.com

# Combined sweep
"FirstName LastName" (site:twitter.com OR site:x.com OR site:facebook.com OR site:instagram.com OR site:youtube.com)

# Official accounts only
"FirstName LastName" "U.S. Senator" site:twitter.com
"FirstName LastName" "Representative" site:twitter.com
```

## Sponsor statements about a bill

```
"FirstName LastName" "[bill name OR act name]"
"FirstName LastName" "[act name]" site:youtube.com
"FirstName LastName" "[act name]" (interview OR speech OR statement OR op-ed)
"FirstName LastName" "[act name]" site:c-span.org
"FirstName LastName" "[act name]" site:medium.com OR site:substack.com
```

## Floor speeches and Congressional Record

```
"FirstName LastName" site:congress.gov/congressional-record
"FirstName LastName" "[bill name]" site:c-span.org
"FirstName LastName" "floor speech" site:youtube.com
"FirstName LastName" (committee OR subcommittee) hearing site:youtube.com
"FirstName LastName" testimony site:c-span.org
```

## Campaign finance

```
"FirstName LastName" site:opensecrets.org
"FirstName LastName" site:fec.gov
"FirstName LastName" site:followthemoney.org
"FirstName LastName" (donor OR contribution OR PAC) site:opensecrets.org

# Industry analysis
"FirstName LastName" "top industries" site:opensecrets.org
"FirstName LastName" "top contributors" site:opensecrets.org
```

## Financial disclosures and stock trades

```
"FirstName LastName" site:unusualwhales.com
"FirstName LastName" site:disclosures.house.gov
"FirstName LastName" (stock trade OR PTR OR "periodic transaction") filetype:pdf
"FirstName LastName" "financial disclosure" filetype:pdf
"FirstName LastName" (insider OR conflict OR holdings) "[Company Name]"
```

## Lobbying disclosures

```
"[bill name OR act name]" site:lobbyingdisclosure.senate.gov
"[bill name OR act name]" site:opensecrets.org/lobby
"[Company Name]" "lobbying" site:opensecrets.org
"[bill name]" lobbying filetype:pdf
"[issue area]" lobbying disclosure filetype:pdf
```

## News coverage of a bill

```
"[bill name OR act name]" (site:apnews.com OR site:reuters.com)
"[bill name]" (site:politico.com OR site:thehill.com OR site:rollcall.com)
"[bill name]" (site:nytimes.com OR site:washingtonpost.com)
"[bill name]" site:propublica.org
"[bill name]" site:axios.com

# Local coverage in sponsor's home district
"[district city]" "[bill name]"
```

## Polling

```
"[bill name OR act name]" (poll OR polling OR survey OR approval)
"[issue area]" site:pewresearch.org
"[issue area]" site:news.gallup.com
"[issue area]" site:today.yougov.com
"[bill name]" site:projects.fivethirtyeight.com/polls
"[bill name]" site:realclearpolitics.com/epolls
```

## Podcasts

```
"FirstName LastName" site:listennotes.com
"FirstName LastName" site:podchaser.com
"FirstName LastName" site:podcasts.apple.com
"[bill name]" site:listennotes.com
"FirstName LastName" (guest OR interviewed OR featured) (podcast OR show OR episode)
```

## Court records: challenges to similar laws

```
"[act name OR similar bill]" site:courtlistener.com
"[act name]" (lawsuit OR "struck down" OR unconstitutional)
"[Company Name]" site:courtlistener.com
"[Company Name]" (lawsuit OR settlement OR consent decree)
```

## Beneficiary corporate research

```
"Company Name" site:opencorporates.com
"Company Name" site:sec.gov
"Company Name" site:opensecrets.org (donor OR contribution OR lobbying)
"Company Name" site:followthemoney.org
"Company Name" 990 filetype:pdf
"Company Name" site:propublica.org/nonprofits
```

## Government documents

```
"[bill name OR act name]" filetype:pdf site:gov
"[bill name]" site:govinfo.gov
"[bill name]" site:federalregister.gov
"FirstName LastName" filetype:pdf site:congress.gov
"FirstName LastName" filetype:pdf site:senate.gov OR site:house.gov
```

---

## Combo sweeps for fast lookups

### Full sponsor sweep
```
"FirstName LastName" (site:congress.gov OR site:votesmart.org OR site:opensecrets.org OR site:fec.gov OR site:unusualwhales.com)
```

### Full bill sweep
```
"[act name]" (site:congress.gov OR site:govtrack.us OR site:propublica.org OR site:politico.com OR site:thehill.com)
```

### Donor-to-beneficiary check
```
"Company Name" "FirstName LastName" (donor OR contribution OR PAC OR lobbying)
"Company Name" "FirstName LastName" site:opensecrets.org
```

---

## Operator pitfalls

- **Brave Search (web_search) does not support `cache:`, `related:`, `AROUND()`, `before:`, or `after:`.** Escalate to Track 2 (browser > Google) for those.
- **Quotes matter.** `"H.R. 22"` is different from `H.R. 22`. Google's tokenizer chops `H.R.` without quotes.
- **OR is case-sensitive.** Lowercase `or` is treated as a search term.
- **`site:` is greedy.** Combine with `inurl:` to scope tighter.
- **Long operator strings sometimes get silently truncated.** If a 7-operator query returns junk, split it into two 3-operator queries.

## Track 1 > Track 2 escalation rule

If Track 1 returns fewer than 3 useful results, switch to Track 2. Open a browser, navigate to https://www.google.com, and run the operator string there. Don't treat Track 1 failure as a dead end.
