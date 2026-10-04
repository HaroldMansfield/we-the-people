# Setup Guide

We The People works in any AI agent platform that supports skills. Claude Code, Codex, Hermes Agent, and other Anthropic-compatible tools can use the same basic skill format. The instructions below cover common options.

You need two things to get started:

1. **The skill files** dropped into your platform's skills folder
2. **A free API key from api.data.gov** (one minute to get)

Total setup time: under 5 minutes.

---

## Part 1: Get your free API key

The U.S. government runs a single sign-up service at **api.data.gov** that gives you one key for ~40 federal APIs, including the two this skill uses (FEC and Congress.gov).

### Steps

1. Open **https://api.data.gov/signup/** in your browser.
2. Fill in your name and email. That's the entire form. No payment, no waiting list.
3. Your API key is emailed to you immediately. It looks like a long string of letters and numbers, around 40 characters.
4. Copy the key. Keep the email open in case you need it again.

### Why one key?

`api.data.gov` is a unified gateway. The same key authenticates to:
- `api.congress.gov`. bills, sponsors, votes, committees
- `api.open.fec.gov`. candidates, committees, contributions

You don't need separate keys for each.

### Rate limits

The default is 1,000 requests per hour. A typical lookup uses 1, 10 requests, so you're nowhere near the limit unless you're running automation. If you do hit it, you'll see HTTP 429. Wait an hour and resume.

---

## Part 2: Install the skill

Pick the section that matches your platform.

### Option A: Claude-compatible platforms

1. **Install the skill files:**
 - Open Claude-compatible platforms settings > **Skills** > **Add skill**.
 - Either upload the `we-the-people` folder, or paste the GitHub URL: `https://github.com/HaroldMansfield/we-the-people`.
2. **Add the API key to your platform's environment:**
 - Open Claude-compatible platforms settings > **Environment variables** (or **Secrets**).
 - Add two entries with the same value:
 ```
 FEC_API_KEY=<your-api-data-gov-key>
 CONGRESS_API_KEY=<your-api-data-gov-key>
 ```
3. **Restart your session.** The skill is ready to use.

### Option B: Local skill folders

Some agent tools read skills from a local folder. If yours does, copy the skill folder there:

 Mac/Linux:
 ```bash
 cp -r we-the-people /path/to/skills/
 ```

 Windows (PowerShell):
 ```powershell
 Copy-Item -Recurse we-the-people "C:\path\to\skills\we-the-people"
 ```

2. **Run the setup script:**
 ```bash
 cd /path/to/skills/we-the-people
 chmod +x setup.sh scripts/*.py
 ./setup.sh
 ```
 Paste your API key when prompted. The script validates it against both APIs and writes a `.env` file.

3. **Make the env vars available to your agent platform.** Add this line to your shell profile (`~/.bashrc`, `~/.zshrc`, or equivalent):
 ```bash
 source /path/to/skills/we-the-people/.env
 ```
4. **Start a new agent platforms session.**

### Option C: Claude Code

1. Place the `we-the-people` folder somewhere your Claude Code project can see. typically `./skills/we-the-people` inside your project.
2. Run setup:
 ```bash
 cd ./skills/we-the-people
 chmod +x setup.sh scripts/*.py
 ./setup.sh
 ```
3. Either:
 - Add `source ./skills/we-the-people/.env` to your shell profile, OR
 - Reference the env file in your project's launch config.
4. Reference the skill in your conversation. Claude will read `SKILL.md` and follow it.

### Option D: Codex / other Anthropic-compatible platforms

The skill format is the standard Anthropic skills layout: `SKILL.md` at the root with frontmatter, supporting reference files in `references/`, helper scripts in `scripts/`. Drop the folder wherever your platform reads skills from, set the two environment variables, and start a session.

### Option E: Just running the helpers manually

If you're not using an agent and just want the helper scripts:

```bash
cd we-the-people
chmod +x setup.sh scripts/*.py
./setup.sh
source .env

python3 scripts/congress_lookup.py bill --congress 119 --type hr --number 22
python3 scripts/fec_lookup.py candidate --name "Roy, Chip" --state TX
```

---

## Part 3: Verify it's working

Ask the agent something like:

> "Look up H.R. 22 in the 119th Congress and tell me who sponsored it."

The agent should pull the bill metadata, name the sponsor, and cite Congress.gov as the source.

If you see something like `ERROR: CONGRESS_API_KEY environment variable not set`, the env vars aren't being passed through. Re-check the install steps for your platform.

---

## Troubleshooting

### `ERROR: CONGRESS_API_KEY environment variable not set` (or `FEC_API_KEY`)

The skill can't see your keys. Check:

- **Claude-compatible platforms:** Are the variables saved in the environment settings UI? Restart the session after adding them.
- **agent platforms / Claude Code:** Did you `source` the `.env` file in the same shell that's running the agent? Run `echo $CONGRESS_API_KEY` to verify.

### `Congress.gov API error: 403 Forbidden`

Your key isn't being accepted. Most common causes:
- Key got truncated when pasting (real keys are ~40 chars; check with `echo -n "$CONGRESS_API_KEY" | wc -c`)
- Whitespace or newlines snuck into the value
- Key was revoked at api.data.gov

Re-run `./setup.sh` to validate and rewrite.

### `Congress.gov API error: 429 Too Many Requests`

You've hit the 1,000/hour rate limit. Wait an hour, or request a higher limit through api.data.gov support.

### The skill loads but doesn't actually do anything

Most platforms (Claude-compatible platforms, Claude Code, agent platforms) auto-load reference files when the skill is invoked. If yours doesn't, explicitly tell the agent:

> "Read references/sources.md and references/search-operators.md, then look up [your question]."

### `setup.sh` says "permission denied"

Make scripts executable:
```bash
chmod +x setup.sh scripts/*.py
```

### I'm not sure my key is right

Run setup.sh again. It will re-validate against both APIs and tell you if the key is good. The validation hits the live endpoints, so if both pass, your key works.

---

## What's in this skill

```
we-the-people/
├── SKILL.md ← agent reads this first
├── README.md ← project overview
├── SETUP.md ← this file
├── LICENSE ← free permitted use with attribution, commercial use by permission
├── AGENTS.md ← agent platforms compatibility shim
├── setup.sh ← interactive API key configuration
├── .env.example ← key template
├── .gitignore ← protects .env from being committed
├── references/
│ ├── sources.md ← every primary data source
│ ├── search-operators.md ← Google operators for legislative work
│ └── output-formats.md ← file format rules for saved outputs
└── scripts/
 ├── congress_lookup.py ← Congress.gov API helper
 └── fec_lookup.py ← FEC API helper
```
