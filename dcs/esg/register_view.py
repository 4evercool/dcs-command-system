#!/usr/bin/env python3
"""Generate a sortable read-only HTML view of .dcs/esg/REGISTER.md.

Regenerate with:  python .dcs/esg/register_view.py
Output:           .dcs/esg/register-view.html   (already gitignored --
                  .dcs/esg/ is wholesale-ignored by every /dcs-init'd
                  project -- never committed)
Read-only over REGISTER.md itself -- never writes there, never takes the
REGISTER-LOCK.

Shipped from dcs/esg/register_view.py (package source, installed to
~/.claude/dcs/esg/ by install.ps1); each onboarded project holds its own
copy at <project>/.dcs/esg/register_view.py, same convention as
dcs/hooks/dcs_gate.py.
"""
import argparse
import html
import re
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = REPO_ROOT / ".dcs" / "esg" / "REGISTER.md"
DEFAULT_OUT = REPO_ROOT / ".dcs" / "esg" / "register-view.html"
REGEN_CMD = "python .dcs/esg/register_view.py"

STATE_ORDER = ["ACTIVE", "QUEUED", "MERGED", "PARKED", "DEPLOYED", "RESOLVED", "KILLED"]
STATE_INDEX = {name: i for i, name in enumerate(STATE_ORDER)}
PRIORITY_INDEX = {"H": 0, "M": 1, "L": 2}
VISIBLE_HEADERS = ["ID", "Title", "Type", "Pri", "Rank", "State", "Opened", "Closed"]


def split_row(line):
    """Split one table row on '|', ignoring pipes inside backtick code
    spans -- a cell can quote something like `QUEUED | ACTIVE | ...` and a
    plain str.split('|') would mis-split it. Strips the empty leading and
    trailing fields the row's own delimiting pipes produce; a row missing
    its closing pipe simply keeps its last cell unstripped (real content,
    not a delimiter artifact)."""
    fields = []
    current = []
    in_code = False
    for ch in line:
        if ch == "`":
            in_code = not in_code
            current.append(ch)
        elif ch == "|" and not in_code:
            fields.append("".join(current))
            current = []
        else:
            current.append(ch)
    fields.append("".join(current))
    if fields and fields[0] == "":
        fields = fields[1:]
    if fields and fields[-1] == "":
        fields = fields[:-1]
    return [f.strip() for f in fields]


def find_table(lines):
    """Locate the header line and the contiguous run of '|'-prefixed data
    lines right after the separator. Everything above the header
    (including the large HTML comments) is ignored by construction, since
    we only start scanning from the header match onward."""
    header_idx = None
    for i, line in enumerate(lines):
        if line.startswith("| ID | Title |"):
            header_idx = i
            break
    if header_idx is None:
        return None, []
    data_indices = []
    i = header_idx + 2  # header line, then the |--- separator line
    while i < len(lines) and lines[i].startswith("|"):
        data_indices.append(i)
        i += 1
    return header_idx, data_indices


def extract_priority(cell):
    letter_m = re.search(r"\b([HML])\b", cell)
    rank_m = re.search(r"rank\s+(\d+)", cell)
    letter = letter_m.group(1) if letter_m else None
    rank = int(rank_m.group(1)) if rank_m else None
    return letter, rank


def extract_state(cell):
    stripped = cell.replace("**", "")
    m = re.search(r"[A-Z]+", stripped)
    return m.group(0) if m else None


def extract_type(cell):
    stripped = cell.replace("**", "").strip()
    if stripped.startswith("?"):
        return "?"
    m = re.search(r"[135]", stripped)
    return m.group(0) if m else None


def date_key(cell):
    c = cell.strip()
    return "" if c == "—" else c


def build_row(cells, line_no):
    (id_, title, type_c, pri_c, state_c, worktree, branch,
     territory, intake, opened, closed, outcome) = cells
    letter, rank = extract_priority(pri_c)
    state_tok = extract_state(state_c)
    type_tok = extract_type(type_c)
    return {
        "line_no": line_no,
        "id": id_, "title": title, "type_raw": type_c,
        "state_raw": state_c, "worktree": worktree, "branch": branch,
        "territory": territory, "intake": intake, "opened": opened,
        "closed": closed, "outcome": outcome,
        "type_tok": type_tok, "pri_letter": letter, "pri_rank": rank,
        "state_tok": state_tok,
        "keys": {
            "id": id_,
            "title": title,
            "type": type_tok if type_tok in ("1", "3", "5") else 9,
            "pri": PRIORITY_INDEX.get(letter, 9),
            "rank": rank if rank is not None else 9999,
            "state": STATE_INDEX.get(state_tok, 99),
            "opened": date_key(opened),
            "closed": date_key(closed),
        },
    }


def parse_register(text):
    lines = text.splitlines()
    header_idx, data_indices = find_table(lines)
    if header_idx is None:
        return None, [], []
    rows = []
    unparsed = []
    for i in data_indices:
        raw = lines[i]
        cells = split_row(raw)
        if len(cells) == 12:
            rows.append(build_row(cells, i + 1))
        else:
            unparsed.append((i + 1, raw))
    return header_idx, rows, unparsed


def render_inline(raw):
    """Escape, then apply the two supported inline renderings in order:
    code spans first, then bold -- so a literal '**' inside a code span
    (e.g. a shell snippet) is never re-touched by the bold pass."""
    escaped = html.escape(raw, quote=True)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def attr(value):
    return html.escape(str(value), quote=True)


def count_by_state(rows):
    counts = {}
    for r in rows:
        key = r["state_tok"] or "UNKNOWN"
        counts[key] = counts.get(key, 0) + 1
    ordered = [s for s in STATE_ORDER if s in counts]
    ordered += sorted(k for k in counts if k not in STATE_INDEX)
    return [(s, counts[s]) for s in ordered]


CSS_TEXT = """
:root {
  color-scheme: light dark;
  --bg: #ffffff;
  --fg: #1a1a1a;
  --muted: #666666;
  --border: #d5d5d5;
  --header-bg: #f2f2f2;
  --row-alt: #fafafa;
  --code-bg: #eef0f2;
  --accent: #0b5fff;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1a1a1a;
    --fg: #e4e4e4;
    --muted: #a0a0a0;
    --border: #444444;
    --header-bg: #262626;
    --row-alt: #202020;
    --code-bg: #2d2d2d;
    --accent: #7aa2ff;
  }
}
* { box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background: var(--bg);
  color: var(--fg);
  margin: 0;
  padding: 1.25rem 1.5rem 3rem;
}
header.page-header { margin-bottom: 1rem; }
h1 { font-size: 1.3rem; margin: 0 0 0.4rem; }
.meta { color: var(--muted); font-size: 0.85rem; line-height: 1.5; }
.meta code { background: var(--code-bg); padding: 0.05rem 0.3rem; border-radius: 3px; }
#filter {
  width: 100%;
  max-width: 420px;
  padding: 0.4rem 0.6rem;
  margin: 0.75rem 0 1rem;
  font-size: 0.95rem;
  background: var(--bg);
  color: var(--fg);
  border: 1px solid var(--border);
  border-radius: 4px;
}
table { border-collapse: collapse; width: 100%; font-size: 0.88rem; }
thead { position: sticky; top: 0; background: var(--header-bg); z-index: 1; }
th, td { border: 1px solid var(--border); padding: 0.35rem 0.55rem; text-align: left; vertical-align: top; }
th { cursor: pointer; user-select: none; white-space: nowrap; }
th[data-sort="asc"]::after { content: " \\25B2"; }
th[data-sort="desc"]::after { content: " \\25BC"; }
tr.main-row:nth-of-type(4n+1) { background: var(--row-alt); }
td.id-cell { cursor: pointer; white-space: nowrap; }
td.title-cell { max-width: 380px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
tr.detail-row > td { border-top: none; padding: 0 0.55rem 0.5rem; }
tr.detail-row summary { cursor: pointer; color: var(--muted); font-size: 0.85rem; padding: 0.2rem 0; }
.detail-grid { display: grid; gap: 0.3rem; margin-top: 0.3rem; font-size: 0.85rem; }
.detail-label { color: var(--muted); font-weight: 600; }
code { background: var(--code-bg); padding: 0.05rem 0.25rem; border-radius: 3px; }
#unparsed { margin-top: 2rem; }
#unparsed pre {
  white-space: pre-wrap;
  word-break: break-word;
  background: var(--code-bg);
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 0.8rem;
}
"""

JS_TEXT = """
(function () {
  "use strict";
  var table = document.getElementById("reg-table");
  if (!table) return;
  var tbody = table.tBodies[0];
  var headers = Array.prototype.slice.call(table.tHead.rows[0].cells);
  var sortState = { col: -1, dir: 1 };

  function rowPairs() {
    var pairs = [];
    var trs = Array.prototype.slice.call(tbody.children);
    for (var i = 0; i < trs.length; i++) {
      if (trs[i].classList.contains("main-row")) {
        var next = trs[i].nextElementSibling;
        var detail = next && next.classList.contains("detail-row") ? next : null;
        pairs.push({ main: trs[i], detail: detail });
      }
    }
    return pairs;
  }

  function compareKeys(av, bv) {
    var aEmpty = av === "";
    var bEmpty = bv === "";
    if (aEmpty && bEmpty) return 0;
    if (aEmpty) return 1;
    if (bEmpty) return -1;
    var an = Number(av), bn = Number(bv);
    if (!isNaN(an) && !isNaN(bn)) return an - bn;
    if (av < bv) return -1;
    if (av > bv) return 1;
    return 0;
  }

  headers.forEach(function (th, colIndex) {
    th.addEventListener("click", function () {
      var dir = sortState.col === colIndex ? -sortState.dir : 1;
      sortState = { col: colIndex, dir: dir };
      headers.forEach(function (h) { h.removeAttribute("data-sort"); });
      th.setAttribute("data-sort", dir === 1 ? "asc" : "desc");

      var pairs = rowPairs();
      pairs.sort(function (a, b) {
        var av = a.main.children[colIndex].getAttribute("data-k") || "";
        var bv = b.main.children[colIndex].getAttribute("data-k") || "";
        return dir * compareKeys(av, bv);
      });
      pairs.forEach(function (p) {
        tbody.appendChild(p.main);
        if (p.detail) tbody.appendChild(p.detail);
      });
    });
  });

  tbody.addEventListener("click", function (ev) {
    var cell = ev.target.closest(".id-cell");
    if (!cell) return;
    var detail = cell.closest("tr").nextElementSibling;
    if (detail && detail.classList.contains("detail-row")) {
      var det = detail.querySelector("details");
      if (det) det.open = !det.open;
    }
  });

  var filterInput = document.getElementById("filter");
  filterInput.addEventListener("input", function () {
    var needle = filterInput.value.toLowerCase();
    rowPairs().forEach(function (p) {
      var text = p.main.textContent + " " + (p.detail ? p.detail.textContent : "");
      var show = text.toLowerCase().indexOf(needle) !== -1;
      p.main.style.display = show ? "" : "none";
      if (p.detail) p.detail.style.display = show ? "" : "none";
    });
  });
})();
"""


def render_html(rows, unparsed, source_path):
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    source_mtime = datetime.fromtimestamp(source_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    state_counts = count_by_state(rows)
    summary = " · ".join("{0} {1}".format(s, n) for s, n in state_counts)
    if not summary:
        summary = "no parsed rows"

    thead = "".join(
        '<th data-col="{0}">{1}</th>'.format(i, html.escape(c))
        for i, c in enumerate(VISIBLE_HEADERS)
    )

    body_parts = []
    for r in rows:
        k = r["keys"]
        pri_display = r["pri_letter"] or "—"
        rank_display = str(r["pri_rank"]) if r["pri_rank"] is not None else "—"
        if r["type_tok"] is not None:
            type_display = r["type_tok"]
        else:
            type_display = r["type_raw"].strip() or "—"

        main_cells = [
            '<td class="id-cell" data-k="{0}">{1}</td>'.format(attr(k["id"]), render_inline(r["id"])),
            '<td class="title-cell" data-k="{0}">{1}</td>'.format(attr(k["title"]), render_inline(r["title"])),
            '<td data-k="{0}">{1}</td>'.format(attr(k["type"]), html.escape(type_display)),
            '<td data-k="{0}">{1}</td>'.format(attr(k["pri"]), html.escape(pri_display)),
            '<td data-k="{0}">{1}</td>'.format(attr(k["rank"]), html.escape(rank_display)),
            '<td data-k="{0}">{1}</td>'.format(attr(k["state"]), render_inline(r["state_raw"])),
            '<td data-k="{0}">{1}</td>'.format(attr(k["opened"]), render_inline(r["opened"])),
            '<td data-k="{0}">{1}</td>'.format(attr(k["closed"]), render_inline(r["closed"])),
        ]
        body_parts.append('<tr class="main-row">{0}</tr>'.format("".join(main_cells)))

        detail_fields = [
            ("Title (full)", r["title"]),
            ("Worktree", r["worktree"]),
            ("Branch", r["branch"]),
            ("Territory", r["territory"]),
            ("Intake source", r["intake"]),
            ("Outcome", r["outcome"]),
        ]
        detail_html = "".join(
            '<div class="detail-field"><span class="detail-label">{0}:</span> '
            '<span class="detail-value">{1}</span></div>'.format(html.escape(label), render_inline(value))
            for label, value in detail_fields
        )
        body_parts.append(
            '<tr class="detail-row"><td colspan="{0}">'
            '<details><summary>▸ details</summary>'
            '<div class="detail-grid">{1}</div></details>'
            "</td></tr>".format(len(VISIBLE_HEADERS), detail_html)
        )

    unparsed_section = ""
    if unparsed:
        lines_html = "\n".join(
            "Line {0}: {1}".format(n, html.escape(raw)) for n, raw in unparsed
        )
        unparsed_section = (
            '<section id="unparsed"><h2>Unparsed rows ({0})</h2>'
            "<p>These lines sit inside the table block but did not split into "
            "exactly 12 cells, so they are rendered raw here instead of being "
            "silently dropped:</p>"
            "<pre>{1}</pre></section>"
        ).format(len(unparsed), lines_html)

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>DCS Register View</title>
<style>{css}</style>
</head>
<body>
<header class="page-header">
<h1>DCS Register View</h1>
<div class="meta">
Generated {generated_at} from <code>{source}</code> (modified {source_mtime})<br>
{row_count} parsed, {unparsed_count} unparsed &middot; {summary}<br>
Regenerate: <code>{regen_cmd}</code>
</div>
</header>
<input type="text" id="filter" placeholder="Filter rows...">
<table id="reg-table">
<thead><tr>{thead}</tr></thead>
<tbody>{tbody}</tbody>
</table>
{unparsed_section}
<script>{js}</script>
</body>
</html>
""".format(
        css=CSS_TEXT,
        generated_at=html.escape(generated_at),
        source=html.escape(str(source_path)),
        source_mtime=html.escape(source_mtime),
        row_count=len(rows),
        unparsed_count=len(unparsed),
        summary=html.escape(summary),
        regen_cmd=html.escape(REGEN_CMD),
        thead=thead,
        tbody="".join(body_parts),
        unparsed_section=unparsed_section,
        js=JS_TEXT,
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a sortable read-only HTML view of REGISTER.md."
    )
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE,
                         help="path to REGISTER.md (default: %(default)s)")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                         help="path to write the HTML view (default: %(default)s)")
    return parser.parse_args()


def main():
    args = parse_args()
    source = args.source
    out = args.out

    if not source.is_file():
        print("error: source file not found: {0}".format(source), file=sys.stderr)
        return 1

    text = source.read_text(encoding="utf-8")
    header_idx, rows, unparsed = parse_register(text)
    if header_idx is None:
        print(
            "error: could not find the '| ID | Title |' table header in {0}".format(source),
            file=sys.stderr,
        )
        return 1

    doc = render_html(rows, unparsed, source)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(doc)

    print("parsed {0} rows, {1} unparsed, wrote {2}".format(len(rows), len(unparsed), out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
