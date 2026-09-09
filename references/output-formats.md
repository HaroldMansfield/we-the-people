# Output Formats

What format to use when the user asks for a saved file.

This skill is a lookup tool. most answers come back as text in chat. But when the user wants something they can save, share, or open later, use these rules.

---

## Default: `.docx` for written output

If the user asks for a "report", "summary", "writeup", "briefing", "doc", or anything they're going to read or share, default to **`.docx`**.

Most people don't know what a `.md` file is or how to open one. A `.docx` opens in Word, Pages, Google Docs, LibreOffice, and every email preview pane. It's the right answer 95% of the time.

When generating a `.docx`, use the `docx` skill if it's available. It produces properly formatted documents with headings, tables, and styling. not just dumped text.

## Tabular data: `.xlsx` (default) or `.csv` (when asked)

For donor lists, cosponsor lists, stock trades, vote breakdowns, contribution rosters. anything with rows and columns. use **`.xlsx`** by default.

Use **`.csv`** instead only when:
- The user specifically asks for CSV
- The user wants to import the data into another tool (analytics, Sheets, a database)
- The dataset is so simple that a spreadsheet's formatting features don't add value

Use the `xlsx` skill for `.xlsx` generation. It produces real spreadsheets with column headers, frozen panes, and number formatting. not CSV-with-an-xlsx-extension.

## Other allowed formats

| Format | Use for |
|---|---|
| `.docx` | **Default for reports, summaries, writeups, briefings** |
| `.xlsx` | **Default for tabular data. donors, cosponsors, trades, etc.** |
| `.csv` | Tabular data when the user explicitly requests it for re-import |
| `.pdf` | Downloaded official filings, government documents, PDFs the user wants to keep as-is |
| `.png` / `.jpg` | Screenshots of pages, charts, or content the user can't get any other way |
| `.txt` | Raw transcripts, plain text captures the user explicitly asked for |

## Avoid as user-facing output

| Format | Why | What to do instead |
|---|---|---|
| `.json` | Not human-readable | Convert to `.xlsx` or `.csv` |
| `.yaml` / `.yml` | Not human-readable | Convert to `.xlsx` or `.csv` |
| `.xml` | Not human-readable | Extract to `.xlsx`, or summarize in `.docx` |
| `.zip` | Hides contents, requires unzipping | Deliver the contents directly |
| `.gz` / `.tar` | Same as zip | Decompress, deliver contents |
| `.md` | Most users don't know how to open it | Use `.docx` for written content |
| `.html` | Looks broken outside a browser | Use `.docx` or `.pdf` |

If a source returns data in one of these formats (FEC bulk data is `.txt`, Congress.gov gives `.xml`, APIs return `.json`), convert before delivering. Pull the relevant fields into a spreadsheet or write a `.docx` summary.

## Naming files

Use descriptive filenames. The user should be able to tell what's in a file from its name.

**Pattern:** `[source]-[descriptor]-[scope-or-date].[ext]`

**Good:**
```
opensecrets-roy-2024-top-donors.xlsx
hr22-summary.docx
hr22-cosponsors.xlsx
unusualwhales-roy-trades-2025.png
congress-gov-bill-text-HR22-119th.pdf
```

**Bad:**
```
output.csv
data.json
results.txt
file.pdf
download (1).pdf
```

Never deliver a file with a generic or system-default filename.

## When you have to deliver multiple files

Deliver them as separate files, not as a `.zip`. The chat interface or skill platform handles multi-file delivery natively. A zipped folder hides what's inside and adds a step for the user.

If you have many related files (say, individual donor records for a long roster), consolidate them into one `.xlsx` with multiple sheets rather than many small files.

## What "saved" means

The user has to explicitly ask for a saved file. If they just ask a question, answer in chat with sources cited inline. Don't generate files unsolicited.

Triggers for file generation:
- "Can you save that as a [doc / spreadsheet / file]?"
- "Give me a write-up I can share"
- "Export the donor list"
- "Make me a brief on this bill"
- "Put together a summary I can send to..."

If the request is ambiguous ("can I get this in a doc?"), assume `.docx`.
