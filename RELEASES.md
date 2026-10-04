# Release Process

This file documents how We The People releases are tracked.

## Current release

Current version: `1.3.0`

Release notes are maintained in [CHANGELOG.md](CHANGELOG.md). GitHub releases should use the same notes so visitors can see what changed without reading commit history.

## Versioning

We The People uses simple semantic versioning.

### Major versions

Use a major version when the skill changes in a way that may break existing usage, such as:

- Renaming core files
- Changing the expected skill folder structure
- Reworking the operator reference format
- Removing helper script commands
- Changing required environment variables

### Minor versions

Use a minor version when adding or changing public functionality, such as:

- New helper commands
- New public source categories
- New output formats
- New platform compatibility notes
- License, branding, or public release changes
- Expanded safety guidance

### Patch versions

Use a patch version for maintenance updates, such as:

- Typo fixes
- Broken link fixes
- Formatting cleanup
- Small documentation clarifications
- Non-breaking script fixes

## Release checklist

Before publishing a release:

1. Update `VERSION.md`.
2. Update `CHANGELOG.md`.
3. Confirm `SKILL.md` starts with valid YAML frontmatter.
4. Confirm required environment variables are still documented.
5. Confirm `.env.example` contains placeholders only, never real keys.
6. Confirm helper scripts do not print API keys in errors.
7. Confirm no secrets, credentials, private data, or sensitive targets are included.
8. Confirm no old project branding remains.
9. Confirm there are no em dashes or en dashes in public Markdown files.
10. Compile the Python helper scripts.
11. Commit the changes.
12. Tag the release, for example `v1.3.0`.
13. Create a GitHub release using the matching changelog notes.

## Safety review checklist

Before each release, confirm the project remains focused on public civic records and does not enable:

- Credential discovery or exposed secret searches
- Doxxing, stalking, harassment, intimidation, or invasive profiling
- Private personal information lookup
- Unauthorized access, exploitation, evasion, or bypassing access controls
- Unverified claims without source links
