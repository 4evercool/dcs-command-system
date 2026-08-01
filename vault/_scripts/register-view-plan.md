# Plan: sortable HTML view of the register (`register_view.py`)

Implementation plan for a session to execute in `C:\DCS`. Self-contained
— read this fully before writing any code. The plan's author reviewed
the register's actual format; the edge cases listed here are real, not
hypothetical.

## What is being built, in one paragraph

A read-only, stdlib-only Python generator at
`vault/_scripts/register_view.py` that parses the incident-portfolio
table in `.dcs/esg/REGISTER.md` and writes one fully self-contained
HTML file to `vault/register-view.html` with click-to-sort columns and
a text filter. It is a *view*: it never modifies the register, and the
generated HTML is never committed. Precedent constraint: the Owner
already declined migrating the register to SQLite
(`vault/Decisions/sqlite-migration-register.md`) — the markdown file
stays the single source of truth, and this tool must not become a
second writable copy.

## Hard constraints (violating any of these fails the task)

1. **Never write to `.dcs/esg/`** — the script opens `REGISTER.md`
   read-only. Do not create, take, or touch `.dcs/esg/REGISTER-LOCK`
   (the lock protects read-modify-write; a pure read needs no lock).
2. **stdlib only** — `re`, `html`, `pathlib`, `argparse`, `datetime`,
   `sys`. No pip installs, no third-party imports.
3. **Self-contained output** — inline CSS and JS only. The generated
   HTML must contain no `<script src=`, no `href="http`, no external
   fonts, no CDN anything.
4. **No BOM** — the script writes its output with
   `open(path, "w", encoding="utf-8", newline="\n")`. When you (the
   implementing session) create files, use the Write/Edit tools, never
   PowerShell `Set-Content`/`Out-File` (they emit a UTF-8 BOM; this has
   broken parses in this repo twice).
5. **English throughout** — code, comments, HTML labels.
6. **Do not commit the generated HTML** — add `vault/register-view.html`
   to `.gitignore` (see step 5).
7. **Fail soft, never silently drop** — a row that does not parse into
   exactly 12 cells is not discarded and does not crash the script; it
   is rendered raw in a visible "Unparsed rows" section at the bottom
   and counted in the console summary.

## Source format facts (verified against the live file)

- The table lives in `.dcs/esg/REGISTER.md`. Header line starts with
  `| ID | Title |` and has 12 columns:
  `ID | Title | Type | Priority | State | Worktree | Branch | Territory | Intake source | Opened | Closed | Outcome`.
- Above the table are large HTML comments (`<!-- ... -->`) containing
  lines that start with `|`-like text — do NOT parse anything before
  the header line. Below the table is a blank line, then `## Notes`.
  Data rows are the contiguous lines starting with `|` after the
  separator line (`|---|...`) and before the first non-`|` line.
- **Cells contain markdown**: `**bold**`, `` `code spans` ``, em-dashes,
  parenthetical qualifiers.
- **Trap: cells can contain `|` inside backtick spans** (e.g. a title
  quoting the state enum `` `QUEUED | ACTIVE | ...` ``). A naive
  `line.split('|')` mis-splits those rows. Required approach: a
  character-walk splitter that toggles an `in_code` flag on each
  backtick and only splits on `|` when `in_code` is false. Strip the
  leading and trailing empty fields produced by the outer pipes.
- Empty-value cells contain an em-dash `—`, sometimes with a qualifier:
  `— (removed)`, `— (deleted)`.
- Priority cells look like `**H (rank 1)**`, `**M (rank 6, fourteenth
  /dcs-esg, 2026-07-31)**`, `**H (unranked — Owner-directed queue
  2026-08-01, ...)**`, or plain `H`. Extract: priority letter = first
  standalone `H`/`M`/`L`; rank = `rank\s+(\d+)` if present, else none.
- State cells look like `QUEUED`, `**DEPLOYED**`, `ACTIVE`,
  `**DEPLOYED** (out-of-band: ...)`, `RESOLVED (field repair)`,
  `**KILLED**`. Extract the first ALL-CAPS token after stripping `**`;
  keep the full cell for display.
- Type cells: `3`, `**1**`, `? (at its stem — likely 5, ...)`. Extract
  first `1`/`3`/`5` digit if the cell doesn't start with `?`; else `?`.
- Opened/Closed cells: `2026-07-30` or `—`.

## Step 1 — the script skeleton

`vault/_scripts/register_view.py`. Structure:

```
#!/usr/bin/env python3
"""Generate a sortable read-only HTML view of .dcs/esg/REGISTER.md.

Regenerate with:  python vault/_scripts/register_view.py
Output:           vault/register-view.html   (gitignored, never committed)
Read-only over .dcs/esg/ -- never writes there, never takes the lock.
"""
```

- Resolve repo root as `Path(__file__).resolve().parents[2]` (script
  sits at `<root>/vault/_scripts/`).
- `argparse`: `--source` (default `<root>/.dcs/esg/REGISTER.md`) and
  `--out` (default `<root>/vault/register-view.html`) — needed for the
  fixture test in step 4.
- Exit non-zero with a clear message if the source file is missing.

## Step 2 — parsing

1. Read source with `encoding="utf-8"`. Iterate lines; find the first
   line matching `^\| ID \| Title \|` — that is the header. The next
   line is the separator (starts `|---`). Every following line starting
   with `|` is a data row; stop at the first line that doesn't.
2. Split each row with the backtick-aware splitter described above.
3. If a row yields exactly 12 cells → parsed row. Otherwise → append
   `(line_number, raw_text)` to `unparsed`.
4. For each parsed row compute sort keys:
   - `state_key`: index in `[ACTIVE, QUEUED, MERGED, PARKED, DEPLOYED,
     RESOLVED, KILLED]` (working-states-first order); unknown state →
     99 (and the row still renders).
   - `pri_key`: H→0, M→1, L→2, none→9.
   - `rank_key`: int, or 9999 when unranked.
   - `type_key`: 1/3/5 as int, `?`→9.
   - `opened_key`/`closed_key`: ISO date string as-is (sorts
     lexicographically), `—`→empty string (JS sorts empties last).

## Step 3 — HTML generation

- Escape every cell with `html.escape` FIRST, then apply two inline
  renderings, in this order: `` `...` `` → `<code>...</code>`, then
  `**...**` → `<strong>...</strong>`. No link rendering (relative repo
  links wouldn't resolve from the HTML file) — leave link syntax as
  literal text.
- Page layout:
  - Header: title, generation timestamp, source path + its mtime, row
    counts by state (e.g. `QUEUED 12 · ACTIVE 1 · DEPLOYED 30 ...`),
    and the regeneration command verbatim (this repo's principle 15:
    every derived artifact names the command that regenerates it).
  - A single text `<input>` that filters rows by case-insensitive
    substring over the row's full text (`row.textContent`).
  - The table with 8 visible columns: ID, Title, Type, Pri, Rank,
    State, Opened, Closed. The four long-prose cells (Worktree, Branch,
    Territory, Intake source, Outcome — five, in fact) render inside a
    `<details>` element in a second `<tr>` spanning all columns,
    toggled by clicking the row's ID cell or a `▸` control. Default
    collapsed.
  - "Unparsed rows" section at the bottom (only when non-empty), raw
    text in a `<pre>`, with line numbers.
- Sorting: each `<td>` of a sortable column carries the pre-computed
  key in a `data-k` attribute; the JS is deliberately dumb — on header
  click, read `data-k` of that column for each row-pair, compare
  numerically when both parse as numbers else as strings, toggle
  asc/desc, re-append rows (keeping each row's detail `<tr>` glued to
  it — sort by pairs, not single rows). Show `▲`/`▼` in the active
  header. ~50 lines of vanilla JS.
- Style: system font stack; `@media (prefers-color-scheme: dark)`
  support; sticky `<thead>`; `max-width` + ellipsis on Title with full
  title in the details row. No frameworks.

## Step 4 — verification (all mechanical; run every one)

1. `python vault/_scripts/register_view.py` → exit 0; console prints
   `parsed N rows, M unparsed, wrote <path>`.
2. Row-count cross-check (self-computing, no hardcoded numbers):
   `N + M + 1` must equal the count of lines matching `^\|` from the
   header line to the end of the table block. Easiest: have the script
   print both numbers and compare; or grep manually:
   `grep -c '^| ' .dcs/esg/REGISTER.md` counts header + data rows
   (the `|---` separator has no space after the pipe, so it's excluded)
   — expect `N + M + 1`.
3. `M` must be 0 against the live register today. If it is not, the
   splitter is broken — the likely culprit is the pipes-in-backticks
   trap; fix the splitter, do not "fix" the register.
4. Fixture test for the trap: write a 3-row fixture file in the system
   temp dir (NOT in the repo) where one row's Title cell contains
   `` `A | B | C` `` inside backticks; run with `--source <fixture>
   --out <tempdir>/t.html`; assert the row parses (script reports
   3 parsed, 0 unparsed).
5. BOM check: first 3 bytes of the output are not `EF BB BF`
   (`python -c "print(open(r'vault/register-view.html','rb').read(3))"`).
6. Self-containment: `grep -c 'src="http\|href="http\|<script src'
   vault/register-view.html` → 0 matches.
7. Open `vault/register-view.html` in a browser (or the preview pane if
   available) and verify: clicking State sorts; clicking again
   reverses; the filter box narrows rows; a details row expands; dark
   mode renders legibly. If no browser is available, at minimum
   verify the JS has no syntax errors by pasting it through
   `node --check` if node exists, else state plainly in the report that
   in-browser behavior was not verified — do not claim it works.
8. `git status --porcelain` shows ONLY: the new script, the plan file
   (already present), the `.gitignore` edit, the navigation edit —
   and `vault/register-view.html` must NOT appear (proving the
   gitignore line works).

## Step 5 — repo integration

1. Append to `.gitignore` (top-level), with a one-line comment:
   ```
   # generated register view (regenerate: python vault/_scripts/register_view.py)
   vault/register-view.html
   ```
2. Add one line to `vault/00-Navigation.md`'s Map list:
   `- register view — sortable HTML over .dcs/esg/REGISTER.md; regenerate with python vault/_scripts/register_view.py (output gitignored)`
   (plain text, not a wikilink — the output is gitignored so there is
   no note to link to).
3. Commit the script + `.gitignore` + navigation edit in ONE commit.
   Write the commit message to a temp file with the Write tool and use
   `git commit -F <file>` — do not pass multi-line messages inline (a
   recent operator corrupted 22 commit messages that way). Message
   subject: `vault: add sortable HTML register view (read-only generator)`.
   Do NOT commit `vault/register-view.html`.

## Out of scope — do not do these even if they seem like improvements

- Any write to `.dcs/esg/**`, including "fixing" register formatting
  the parser dislikes. Parser adapts to register, never the reverse.
- Adding a register row for this work (the Owner/Chief of Staff handles
  register bookkeeping; your task ends at the commit).
- Parsing `vault/Backlog.md` or `.dcs/incidents/` (a possible v2, not
  now).
- Publishing the HTML anywhere (artifact hosting, gist, etc.) —
  `.dcs/esg/` is deliberately untracked and local; the view stays on
  this machine.
- Editing capability in the HTML (the SQLite-decline precedent).
- Running `install.ps1` or touching `~/.claude/` (unrelated to this
  task, and forbidden mid-incident repo-wide).

## Final report shape

State: rows parsed / unparsed against the live register, each
verification step's actual result (including step 7 honestly), the
commit sha, and the exact regeneration command.
