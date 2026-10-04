# We The People

> A civic lookup skill for turning public legislative records into sourced answers.

**A bill and legislation lookup skill for AI agents.**

Ask your AI agent about a bill, a senator, a campaign donor, or a lobbying disclosure. We The People returns the answer with sources cited. Built for civic engagement, journalism, advocacy, and anyone who wants to know what the U.S. government and their elected representatives are actually doing.

Works with **Hermes Agent**, **Claude Code**, **Codex**, and other agent platforms that support Anthropic-style skills.

---

## What it does

Give a command to look up a bill:

> *"Do a We The People search on HR22"*

Ask questions like:

> *"What does H.R. 22 actually do?"*<br>
> *"Who are the top donors to Senator Elizabeth Warren?"*<br>
> *"Has Chip Roy traded any stocks in defense companies?"*<br>
> *"Who's lobbying for the SAFE Banking Act?"*<br>
> *"Has this immigration bill been introduced before?"*<br>
> *"What did Bernie Sanders say about the Inflation Reduction Act on the Senate floor?"*

We The People helps pull answers from public sources such as Congress.gov, the FEC, OpenSecrets, Unusual Whales, Senate lobbying disclosures, C-SPAN, and more, then gives you links you can verify yourself.

It's a **lookup tool**. You ask, it helps retrieve sourced public information, and you decide what to do with it.

---

## Installation

You need three things to get started:

1. **A free API key** from https://api.data.gov/signup/ (one-minute email signup, no payment and no waiting list)
2. **The skill files** dropped into your platform's skills folder
3. **The two env vars set** with your API key

Pick the section below that matches your platform.

### Claude-compatible platforms

1. **Install the skill files:**
 - Open Claude-compatible platforms settings > **Skills** > **Add skill**.
 - Either upload the `we-the-people` folder, or paste this repo URL: `https://github.com/HaroldMansfield/we-the-people`.
2. **Add the API key:**
 - Open Claude-compatible platforms settings > **Environment variables** (or **Secrets**).
 - Add two entries with the same value:
 ```
 FEC_API_KEY=<your-api-data-gov-key>
 CONGRESS_API_KEY=<your-api-data-gov-key>
 ```
3. **Restart your Claude-compatible platforms session.** The skill is ready to use.

### agent platforms

1. **Open agent platforms Mission Control** (the dashboard).
2. Go to the **Skills** section.
3. Click **Add Skill** (or **Install Skill**).
4. Either upload the `we-the-people` folder, or paste this repo URL:
 `https://github.com/HaroldMansfield/we-the-people`
5. Once installed, open the **Settings** or **Environment Variables** section in Mission Control.
6. Add these two variables, both set to your `api.data.gov` key:
 ```
 FEC_API_KEY=<your-api-data-gov-key>
 CONGRESS_API_KEY=<your-api-data-gov-key>
 ```
7. Save and restart your agent platforms session.

### Claude Code

1. **Place the skill folder where Claude Code can see it.** Either inside your project (recommended) or in a global skills location:
 ```bash
 # Inside a project
 mkdir -p ./skills && cp -r we-the-people ./skills/

 # Or globally for all projects
 mkdir -p ~/.claude/skills && cp -r we-the-people ~/.claude/skills/
 ```

2. **Run the interactive setup script:**
 ```bash
 cd ./skills/we-the-people
 chmod +x setup.sh scripts/*.py
 ./setup.sh
 ```

3. **Make the env vars available.** Either:
 - Add `source ./skills/we-the-people/.env` to your shell profile, OR
 - Add the env vars to your project's `.env` and reference it in your Claude Code config

4. **Reference the skill in your conversation.** Claude Code will read `SKILL.md` and follow it.

### Codex

1. **Drop the skill folder into your Codex skills directory:**
 ```bash
 cp -r we-the-people ~/.codex/skills/
 ```

2. **Run the interactive setup script:**
 ```bash
 cd ~/.codex/skills/we-the-people
 chmod +x setup.sh scripts/*.py
 ./setup.sh
 ```

3. **Make the env vars available to Codex.** Add to your shell profile:
 ```bash
 source ~/.codex/skills/we-the-people/.env
 ```

4. **Start a new Codex session.**

### Hermes Agent

Hermes Agent (by Nous Research) supports installing skills directly from a GitHub repo, with no manual file copying.

1. **Install Hermes Agent** if you haven't already. one-line install at https://hermes-agent.nousresearch.com.

2. **Install the skill.** From inside a Hermes chat session:
 ```
 /skills install HaroldMansfield/we-the-people
 ```
 Or from your terminal:
 ```bash
 hermes skills install HaroldMansfield/we-the-people
 ```

3. **First time the skill loads, Hermes will prompt you for your `api.data.gov` key.** Get a free one at https://api.data.gov/signup/ if you don't have one. Hermes stores it securely and passes it to the skill automatically. No manual `.env` editing needed.

4. **Use the skill** by asking naturally in any Hermes chat (the agent loads it when it's relevant), or invoke explicitly:
 ```
 /we-the-people who sponsored H.R. 22?
 ```

Hermes works on the desktop CLI plus messaging platforms (Telegram, Discord, Slack, WhatsApp, Signal, Email), so you can query We The People from anywhere your Hermes is connected.

### Other Anthropic-compatible platforms

The skill format is the standard Anthropic skills layout: `SKILL.md` at the root with frontmatter, supporting reference files in `references/`, helper scripts in `scripts/`. Drop the folder wherever your platform reads skills from, set the two environment variables (`FEC_API_KEY` and `CONGRESS_API_KEY`), and start a session.

### Just running the helpers manually

If you're not using an agent platform and just want the API helpers:

```bash
cd we-the-people
chmod +x setup.sh scripts/*.py
./setup.sh
source .env

python3 scripts/congress_lookup.py bill --congress 119 --type hr --number 22
python3 scripts/fec_lookup.py candidate --name "Roy, Chip" --state TX
```

### Verify it's working

Ask the agent something like:

> "Look up H.R. 22 in the 119th Congress and tell me who sponsored it."

The agent should pull the bill metadata, name the sponsor, and cite Congress.gov as the source.

For troubleshooting, see [`SETUP.md`](SETUP.md).

---

## Example interactions

**You:** *"Pull up H.R. 22 and tell me who sponsored it."*

**Agent:** Pulls bill metadata from the Congress.gov API, names the sponsor (Chip Roy, R-TX-21), summarizes what the bill does in plain language, links to the full text. Around 30 seconds.

---

**You:** *"Top donors to Roy in 2024."*

**Agent:** Hits the FEC API for Roy's principal campaign committee, returns the top 20 contributing employers with totals, links to OpenSecrets for the donor profile. Optionally: *"Save it as a spreadsheet."* > produces an `.xlsx` file you can open in Excel.

---

**You:** *"Has Roy traded any stocks while H.R. 22 was active?"*

**Agent:** Checks Unusual Whales and the House disclosure portal, summarizes any trades in the relevant window, flags any companies that benefit from the bill.

---

## Where the data comes from

| Question | Source |
|---|---|
| Federal bill text, sponsors, votes | Congress.gov |
| Federal bill summaries, plain-language | GovTrack |
| State bills | LegiScan, Ballotpedia, Open States |
| Campaign finance (federal) | OpenSecrets, FEC.gov |
| Campaign finance (state) | FollowTheMoney |
| Stock trades by legislators | Unusual Whales, House/Senate disclosure portals |
| Lobbying | Senate LDA, OpenSecrets Lobbying |
| Floor speeches, hearings | C-SPAN, Congressional Record |
| News coverage | AP, Reuters, Politico, The Hill, ProPublica |
| Polling | Gallup, Pew, YouGov, FiveThirtyEight |

Full source list with URLs in [`references/sources.md`](references/sources.md).

**Important:** the included helper scripts support Congress.gov and the FEC. Other sources listed in this repository are used through normal web lookup by the agent.


---

## What you need

- An AI agent platform that supports skills (Claude-compatible platforms, agent platforms, Hermes Agent, Claude Code, Codex, or compatible)
- A free **api.data.gov** API key (covers both Congress.gov and FEC)
- Python 3 and `bash` (for the helper scripts and setup)

That's it. Everything is free. Everything is public-record. No paid services, no data brokers. Use it for public civic research, not targeting or harassment.

---

## Security

The skill treats all fetched web content as untrusted data and will not follow instructions it finds on websites. This protects against prompt injection, where a page attempts to manipulate the agent by telling it to change its answer, ignore your question, recommend a different bill, or send data somewhere. If a page tries any of that, the skill stops and tells you.

The skill only fetches from a curated list of authoritative sources: Congress.gov, the FEC, OpenSecrets, Unusual Whales, Senate lobbying disclosures, and other official or widely-recognized outlets listed in `references/sources.md`. If you ask it to fetch from a domain outside that list, it will confirm with you before proceeding.

If the skill detects a manipulation attempt while processing a page, it stops immediately, tells you the URL and a plain-language description of what looked suspicious, and offers you three options: skip that source and continue with others, block the site for the rest of this session, or blacklist it permanently.

Permanently blacklisted domains are stored in `blacklist.txt` at the skill root. You can also edit that file manually at any time to pre-block sites you know you don't want the skill to access.

---

## What's in this repo

```
we-the-people/
├── SKILL.md <- agent reads this first
├── README.md <- you are here
├── SETUP.md <- detailed install for every platform
├── LICENSE <- license terms
├── AGENTS.md <- agent platforms compatibility entry point
├── blacklist.txt <- domains the skill will skip
├── setup.sh <- interactive API key configuration
├── .env.example <- key template
├── references/
│ ├── sources.md <- every primary data source
│ ├── search-operators.md <- Google operators for legislative work
│ └── output-formats.md <- file format rules for saved outputs
└── scripts/
 ├── congress_lookup.py <- Congress.gov API helper
 └── fec_lookup.py <- FEC API helper
```

---

## Release Information

Current version: `1.3.0`

Release notes are tracked in [CHANGELOG.md](CHANGELOG.md). The release process and safety review checklist are documented in [RELEASES.md](RELEASES.md).

---

## License

Free to use and modify for personal, internal, educational, research, journalism, nonprofit, civic, and public-interest work. Redistribution requires credit to the original source and Seeker One. Commercial use requires separate written permission when the skill is a material part of a paid product, paid service, client deliverable, subscription, or commercial offering.

Full terms are in [`LICENSE`](./LICENSE).

---

## Lawful use

This skill uses publicly available, indexed information from government data portals, news archives, and public-record databases. No non-public data sources or data brokers are used.

Use it for journalism, civic research, academic work, advocacy, or just understanding what your representatives are actually doing.

Do not use it to target individuals. That use is explicitly prohibited by the license.

---

## Support and contributions

Built by [Harold Mansfield](https://www.linkedin.com/in/haroldmansfield/), founder and researcher at [Seeker One](https://seeker.one).

Questions, bug reports, and feature requests: https://github.com/HaroldMansfield/we-the-people/issues
