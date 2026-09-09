# Changelog

All notable changes to **We The People** are documented in this file.

This project follows [Semantic Versioning](https://semver.org/):
**MAJOR.MINOR.PATCH**. major for breaking changes, minor for new features, patch for fixes.

---

## [1.2]: 2026-05-10

### Added
- **Prompt-injection defenses.** The skill now treats all fetched web content as untrusted data and refuses to follow instructions found inside web pages, alt text, HTML comments, or hidden CSS. Protects against malicious sites attempting to manipulate the agent's behavior or output.
- **Source allowlist enforcement.** Web fetches are restricted to the curated source list in `references/sources.md`. Fetches to domains outside the list require explicit user confirmation.
- **Site blacklist mechanism.** When the skill detects a manipulation attempt, it flags the URL to the user and offers three options: skip the source, blacklist for the session, or blacklist permanently. Permanent blacklist entries are stored in a new `blacklist.txt` file at the skill root and read on every run.
- **`blacklist.txt`** (new file) at repo root. Empty by default; users or the agent can append domains to it.

### Changed
- **SKILL.md** has a new `## Security: Untrusted Web Content` section documenting the agent's behavior under prompt-injection conditions.
- **README.md** has a new user-facing `## Security` section explaining the protections in plain language.

---

## [1.1]: 2026-05-06

### Added
- **Hermes Agent support.** The skill now installs natively in Hermes Agent (Nous Research) via `hermes skills install SamaritanOC/We-The-People` or the `/skills install` slash command. No manual file copying required.
- **`required_environment_variables` block in SKILL.md frontmatter.** Hermes Agent uses this to securely prompt users for their `api.data.gov` key on first use of the skill, then automatically pass it through to the helper scripts. Other platforms (Cowork, OpenClaw, Claude Code, Codex) ignore the field, so this change is fully backward-compatible.
- **Hermes Agent install section in README.md** with step-by-step instructions for the Hermes-specific install flow.
- **Header image and tagline quote** on README.

### Changed
- **License tightened to non-commercial use only.** Previous license language allowed commercial use with a donation request. New license explicitly prohibits commercial use, resale, and repackaging. Commercial license inquiries should go to `hm@smbconsultants.ai`.
- **OpenClaw install instructions** rewritten to use the Mission Control dashboard UI (the easy path) rather than command-line copy operations.
- **README "Works with…" tagline** updated to include Hermes Agent and reference the [agentskills.io](https://agentskills.io) standard.

### Fixed
- Several typos in README.md (`thier` > `their`, `represpentatives` > `representatives`, `areactually` > `are actually`, `globalskills` > `global skills`, `it's development` > `its development`).

---

## [1.0]: 2026-05-04

### Added
- Initial public release.
- Bill and legislation lookup capabilities. bills, sponsors, co-sponsors, campaign finance, financial disclosures, lobbying, court records, news, polling.
- Helper scripts for the Congress.gov and FEC OpenFEC APIs.
- Reference files: `sources.md`, `search-operators.md`, `output-formats.md`.
- Interactive `setup.sh` script for API key configuration with live validation against both APIs.
- Installation instructions for Cowork, OpenClaw, Claude Code, and Codex.
- Custom non-commercial license (later tightened in 1.1).

[1.2]: https://github.com/HaroldMansfield/we-the-people/releases/tag/v1.2
[1.1]: https://github.com/HaroldMansfield/we-the-people/releases/tag/v1.1
[1.0]: https://github.com/HaroldMansfield/we-the-people/releases/tag/v1.0
