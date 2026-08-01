"""Preservation-map checker for `dcs/workflows/plan.md`'s `## 6c.`
bounded-amendment path.

Why this exists (incident revision-preservation-map, 202-OBJECTIVES.md):
`register-field-repair-path` (2026-07-27) took a narrow `## 6c.` amendment
that edited one criterion's content while silently dropping a different,
already-satisfied criterion's section from `IAP.md`. Nothing mechanical
checked that the untouched criteria still held in the artifact as it stood
before the marker was re-stamped -- only a bare assertion of coverage
(doctrine principle 15's exact target).

This module is that mechanical check. It reads a `## 6c.` amendment's
preservation map -- a JSON block appended to `214-LOG.md` naming, for
every 202 acceptance criterion the amendment itself does not touch, the
artifact section and exact anchor text that proves it still holds -- and
RE-DERIVES the proof from the artifact's current bytes every time. The
map's own self-reported `output` field is NEVER trusted as the proof (the
AAR.md:82-89 false-fidelity defect this closes): `verify()` always reads
the artifact from disk and recomputes what it finds there.

Stdlib-only, Python 3. `main()` sits behind `if __name__ == "__main__"`,
so importing this module (as `tests/test_doctrine_integrity.py` does, via
the `importlib.util.spec_from_file_location` idiom already used for
`dcs_gate.py`) has no side effects.

Invocation (for a human, or a session, running this by hand against a
real incident directory):

    python "$HOME/.claude/dcs/tools/preservation_map.py" <incident_dir>

Exit codes (tests/payload_check.py's convention):
    0   clean -- every criterion the amendment does not name is proven
        present, by content, in a screened artifact
    1   one or more findings (each printed, one per line)
    2   environment error -- missing incident dir, or missing/unreadable
        `202-OBJECTIVES.md` / `214-LOG.md`
"""
import fnmatch
import json
import re
import sys
from pathlib import Path

# The exact invocation string, shared verbatim with dcs/workflows/plan.md's
# `## 6c.` step (S2's territory) -- do not paraphrase either copy; a test
# (tests/test_doctrine_integrity.py's carrier case) reads this constant
# and confirms plan.md quotes it, whitespace-collapsed, rather than typing
# a second literal that could drift.
INVOCATION = 'python "$HOME/.claude/dcs/tools/preservation_map.py" <incident_dir>'

# The top-level JSON key a 214-LOG.md preservation-map block is keyed
# under. find_map() looks for a fenced JSON block whose parse is a dict
# carrying this key; verify() reads the value at this key as the map body
# ({"amended_criteria": [...], "preserved": [...]}).
MAP_KEY = "preservation_map"

# `## 6c.` boundary condition 1's screened artifact set: the only three
# shapes a `preserved` entry's `artifact` field may name. `204-TASKING/*.md`
# is a pattern (any file directly under that directory); the other two are
# exact incident-relative paths.
_SCREENED_ARTIFACT_PATTERNS = ("IAP.md", "203-ORG.md", "204-TASKING/*.md")

# 202-OBJECTIVES.md's acceptance-criteria heading, and the next heading of
# any level -- criteria() reads only the numbered lines between the two.
_ACCEPTANCE_HEADING_RE = re.compile(r"^#{1,6}\s*Acceptance criteria\b", re.IGNORECASE)
_HEADING_RE = re.compile(r"^#{1,6}\s")
_NUMBERED_ITEM_RE = re.compile(r"^(\d+)\.\s")

# prefix_coverage()'s scope-limiting tags -- lint 4a check 6's own three
# (a criterion tagged with one of these is exempt from needing a tasking).
_SCOPE_TAGS = ("[IC]", "[Owner]", "[deploy period]")

# A "criteria"/"criterion" mention followed by the numbers it scopes --
# prefix_coverage()'s (pre-fix) notion of "maps to a tasking id": any
# 204-TASKING/*.md file naming a criterion number near that word.
_CRITERIA_MENTION_RE = re.compile(
    r"criteri(?:on|a)\b(.{0,120}?)(?=[.\n]|$)", re.IGNORECASE | re.DOTALL
)


def _ws_norm(s):
    """Collapse any run of whitespace to one space -- the map's
    self-reported `output` and the artifact's own line are compared this
    way so a markdown hard-wrap or trailing space is never a false
    disagreement; anything ELSE differing (words, punctuation, case) still
    counts as a real one."""
    return re.sub(r"\s+", " ", s).strip()


def criteria(objectives_text):
    """The numbered acceptance criteria parsed out of a 202-OBJECTIVES.md:
    every `N. ...` line under its "Acceptance criteria" heading, up to the
    next heading of any level. A `[IC]`/`[Owner]`/`[deploy period]` tag on
    a line does not exclude that criterion -- tags only matter to
    prefix_coverage()'s pre-fix comparator, never here. Returns a sorted
    list of unique ints; empty if the heading or its list is absent."""
    nums = []
    in_section = False
    for line in objectives_text.splitlines():
        if _ACCEPTANCE_HEADING_RE.match(line):
            in_section = True
            continue
        if in_section and _HEADING_RE.match(line):
            break
        if in_section:
            m = _NUMBERED_ITEM_RE.match(line)
            if m:
                nums.append(int(m.group(1)))
    return sorted(set(nums))


def _fenced_blocks_text(text):
    """Every fenced (``` / ```) code block's raw body text, in file order.
    A line opening or closing a fence is itself never part of a block's
    body -- mirrors tests/test_doctrine_integrity.py's own _fenced_blocks
    idiom, reimplemented here (not imported) because this module must
    stay import-clean and side-effect-free on its own, with no dependency
    on the test suite."""
    blocks = []
    in_block = False
    cur = []
    for line in text.splitlines():
        if line.strip().startswith("```"):
            if in_block:
                blocks.append("\n".join(cur))
                cur = []
            in_block = not in_block
        elif in_block:
            cur.append(line)
    return blocks


def find_map(log_text):
    """The last fenced JSON block in a 214-LOG.md whose parse is a dict
    carrying MAP_KEY -- i.e. the most recent `## 6c.` amendment's
    preservation map, so a later amendment's map always supersedes an
    earlier one. Returns that block's own parsed dict (callers read the
    map body at `result[MAP_KEY]`), or None if no such block exists. A
    block that fails to parse as JSON, or parses to something other than
    a MAP_KEY-carrying dict, is silently skipped -- it is not this
    function's job to validate shape, only to find the right block;
    verify() is what turns a malformed map into a finding."""
    result = None
    for block_text in _fenced_blocks_text(log_text):
        try:
            parsed = json.loads(block_text)
        except (json.JSONDecodeError, ValueError):
            continue
        if isinstance(parsed, dict) and MAP_KEY in parsed:
            result = parsed
    return result


def _artifact_valid(incident_dir, artifact_rel):
    """True + the resolved Path iff `artifact_rel` is BOTH inside
    `incident_dir` and shaped like one of `## 6c.` boundary condition 1's
    three screened artifacts. A single check covers both halves of the
    one finding this guards ("outside the incident directory OR not a
    screened artifact") because either failure means the same thing here:
    this is not a citation verify() may trust."""
    if not artifact_rel or not isinstance(artifact_rel, str):
        return False, None
    normalized = artifact_rel.replace("\\", "/").strip()
    if not any(fnmatch.fnmatch(normalized, pat) for pat in _SCREENED_ARTIFACT_PATTERNS):
        return False, None
    try:
        incident_resolved = incident_dir.resolve()
        candidate = (incident_dir / normalized).resolve()
        candidate.relative_to(incident_resolved)
    except (ValueError, OSError):
        return False, None
    return True, candidate


def preserved_findings(entry, artifact_text, artifact_label=None):
    """Findings against ONE `preserved` map entry, given the CURRENT text
    of the artifact it names -- never touches disk itself. This is the
    comparator verify() calls after reading the artifact from disk; it is
    also, deliberately, reusable standalone (idiom of
    tests/test_doctrine_integrity.py's in-memory forgery proofs -- see the
    section-22 negative-proof cases, `grep -n '^# --- [0-9]'
    tests/test_doctrine_integrity.py` for the current label since
    citations by section number in that file have a known expiry):
    handing it a hand-edited copy of an artifact's text proves the SAME
    function reads content, rather than passing whatever it is handed,
    without touching any file on disk.

    Two independent findings, both re-derived from `artifact_text` alone:
      - the entry's `anchor` does not occur in the artifact's current
        bytes at all (the section it once named may have been dropped, or
        never existed);
      - the entry's self-reported `output` disagrees with the actual
        (whitespace-normalised) line the anchor is found on -- `output` is
        NEVER the proof (AAR.md:82-89's false-fidelity defect): a
        "plausible" self-reported value that no longer matches the
        artifact is exactly the shape this guards against.
    """
    n = entry.get("criterion") if isinstance(entry, dict) else None
    label = artifact_label or (entry.get("artifact") if isinstance(entry, dict) else None)
    anchor = entry.get("anchor", "") if isinstance(entry, dict) else ""
    findings = []
    if not anchor or anchor not in artifact_text:
        findings.append(
            f"criterion {n}: preserved anchor does not occur in "
            f"{label}'s current bytes"
        )
        return findings
    found_line = ""
    for ln in artifact_text.splitlines():
        if anchor in ln:
            found_line = ln.strip()
            break
    reported = str(entry.get("output", ""))
    if _ws_norm(found_line) != _ws_norm(reported):
        findings.append(
            f"criterion {n}: preserved output disagrees with {label}'s "
            f"actual content at the anchor (reported {reported!r}, "
            f"found {found_line!r})"
        )
    return findings


def verify(incident_dir):
    """The findings list for one incident directory's CURRENT preservation
    map (the last one find_map() locates in 214-LOG.md) -- EMPTY means
    admissible. Reports, each as its own finding string naming the
    criterion number:
      - a 202 criterion in neither the map's `amended_criteria` nor its
        `preserved` list;
      - a `preserved` entry whose `artifact` is outside the incident
        directory or is not one of `## 6c.` boundary condition 1's three
        screened artifacts;
      - a `preserved` entry whose `anchor` does not occur in that
        artifact's current bytes;
      - a `preserved` entry whose self-reported `output` disagrees with
        what this function itself finds there.
    `output` is NEVER the proof -- every claim is re-derived from the
    artifact's bytes on disk, every call, never cached and never taken on
    the map's own word.

    Raises FileNotFoundError (environment error, never a finding) if
    `incident_dir` does not exist, or `202-OBJECTIVES.md` / `214-LOG.md`
    under it is missing -- main() turns that into exit code 2.
    """
    incident_dir = Path(incident_dir)
    if not incident_dir.is_dir():
        raise FileNotFoundError(f"no such incident directory: {incident_dir}")

    objectives_path = incident_dir / "202-OBJECTIVES.md"
    if not objectives_path.is_file():
        raise FileNotFoundError(f"missing 202-OBJECTIVES.md under {incident_dir}")
    objectives_text = objectives_path.read_text(encoding="utf-8")

    log_path = incident_dir / "214-LOG.md"
    if not log_path.is_file():
        raise FileNotFoundError(f"missing 214-LOG.md under {incident_dir}")
    log_text = log_path.read_text(encoding="utf-8")

    crit_nums = criteria(objectives_text)

    block = find_map(log_text)
    if block is None:
        return [
            f"no {MAP_KEY} JSON block found in {log_path} -- a "
            "## 6c. amendment must carry one before its marker re-stamps"
        ]

    pm = block.get(MAP_KEY)
    if not isinstance(pm, dict):
        return [f"the {MAP_KEY} block in {log_path} did not parse to an object"]

    amended = set()
    for a in (pm.get("amended_criteria") or []):
        try:
            amended.add(int(a))
        except (TypeError, ValueError):
            pass

    preserved = pm.get("preserved") or []

    preserved_nums = set()
    for entry in preserved:
        if not isinstance(entry, dict):
            continue
        try:
            preserved_nums.add(int(entry.get("criterion")))
        except (TypeError, ValueError):
            continue

    findings = []

    for c in crit_nums:
        if c not in amended and c not in preserved_nums:
            findings.append(
                f"criterion {c}: named by neither the amendment's "
                "amended_criteria nor the preservation map's preserved list"
            )

    for entry in preserved:
        if not isinstance(entry, dict):
            findings.append(f"preserved entry is not an object: {entry!r}")
            continue
        n = entry.get("criterion")
        artifact_rel = entry.get("artifact")
        ok, resolved = _artifact_valid(incident_dir, artifact_rel)
        if not ok:
            findings.append(
                f"criterion {n}: preserved artifact {artifact_rel!r} is "
                "outside the incident directory or is not one of the "
                "screened artifacts (IAP.md, 203-ORG.md, 204-TASKING/*.md)"
            )
            continue
        try:
            artifact_text = resolved.read_text(encoding="utf-8")
        except OSError:
            findings.append(
                f"criterion {n}: preserved artifact {artifact_rel!r} "
                "could not be read"
            )
            continue
        findings.extend(preserved_findings(entry, artifact_text, artifact_rel))

    return findings


def _numbers_in_context(s):
    """Every integer literal in `s`, with an `N-M` range expanded to every
    integer it spans (`,`/`and`/`&` between numbers need no special case:
    the plain \\d+ scan already finds each one)."""
    nums = set()
    for tok in re.findall(r"\d+\s*-\s*\d+|\d+", s):
        tok = tok.replace(" ", "")
        if "-" in tok:
            a, b = tok.split("-", 1)
            nums.update(range(int(a), int(b) + 1))
        else:
            nums.add(int(tok))
    return nums


def prefix_coverage(incident_dir):
    """The PRE-FIX comparator: the 202 criteria that fail lint 4a check
    6's rule -- a criterion mapping to no `204-TASKING/*.md` tasking id
    and carrying no `[IC]`/`[Owner]`/`[deploy period]` tag -- with NO
    regard to whether any artifact's CONTENT still proves it. Preserved,
    named and importable, purely so criterion 4's contrast is provable
    in-suite: `register-field-repair-path`'s defect shape (dropped-criterion
    fixture) passes this pre-fix check cleanly (every criterion still maps
    to a tasking id) while verify() on the very same fixture reports the
    drop -- proving this comparator's blindness is real, not asserted.
    """
    incident_dir = Path(incident_dir)
    objectives_text = (incident_dir / "202-OBJECTIVES.md").read_text(encoding="utf-8")
    crit_nums = criteria(objectives_text)

    tagged = set()
    in_section = False
    for line in objectives_text.splitlines():
        if _ACCEPTANCE_HEADING_RE.match(line):
            in_section = True
            continue
        if in_section and _HEADING_RE.match(line):
            break
        if in_section:
            m = _NUMBERED_ITEM_RE.match(line)
            if m and any(tag in line for tag in _SCOPE_TAGS):
                tagged.add(int(m.group(1)))

    mapped = set()
    tasking_dir = incident_dir / "204-TASKING"
    if tasking_dir.is_dir():
        for p in sorted(tasking_dir.glob("*.md")):
            text = p.read_text(encoding="utf-8")
            for m in _CRITERIA_MENTION_RE.finditer(text):
                mapped |= _numbers_in_context(m.group(1))

    return sorted(c for c in crit_nums if c not in mapped and c not in tagged)


def main():
    if len(sys.argv) != 2:
        print(f"usage: {INVOCATION}")
        sys.exit(2)

    try:
        findings = verify(sys.argv[1])
    except OSError as exc:
        print(f"ERROR: {exc}")
        sys.exit(2)

    if findings:
        for f in findings:
            print(f)
        sys.exit(1)

    print(
        "preservation map: clean -- every criterion the amendment does "
        "not name is proven present, by content, in a screened artifact"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
