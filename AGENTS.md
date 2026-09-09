## Agent: We The People
- Purpose: legislative lookup tool. bills, sponsors, campaign finance, lobbying, financial disclosures, and historical context for federal, state, and local legislation
- Scope: information gathering only (not case-building system)
- Routing: default

## Required Reference Files

The following skill files contain the information sources, search operators,
and output format rules. Read them when relevant to the user's question:

- `SKILL.md`. agent identity, when to trigger, default behavior
- `references/sources.md`: primary data sources with URLs and use cases
- `references/search-operators.md`: search operators for legislative research
- `references/output-formats.md`: file format rules when the user requests saved output

## API requirements

This skill uses two free U.S. government APIs:

- `CONGRESS_API_KEY`: for the Congress.gov API
- `FEC_API_KEY`: for the FEC OpenFEC API

Both can be the same value. they're both gated through api.data.gov.

If keys are missing, the skill falls back to web search of the same data on
the public sites. slower, but works. See `SETUP.md` for installation and key
configuration.
