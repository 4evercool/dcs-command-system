"""Record-integrity checker for a DCS incident directory's own artifacts.

Why this exists (incident close-integrity-guard-bundle, 202-OBJECTIVES.md):
an external period review found that several already-closed incidents'
own historical records carried false or missing factual claims about
themselves -- a fabricated merge-commit citation quoted as real, a
"verbatim" quote attributed to a file that never existed, and several
incidents nearly devoid of their standard artifact set. Every one of
those defects was, in hindsight, mechanically detectable: a cited commit
either exists in the repository or it does not; the canonical nine-file
artifact set is either present and tracked or it is not; a verdict file
either carries a real, schema-conformant fence or it does not. Nothing
before this tool checked any of that at close time -- each defect was
found later, by a human-directed review, not by the process that
produced the record in the first place.

This module is that mechanical check, run once per incident directory.
It is deliberately NARROW: it re-derives six specific, universal
properties of ONE incident's own artifacts -- never a portfolio-wide
historical sweep (see SCOPE below) -- from the artifacts and the git
history currently on disk, every time, the same discipline
`preservation_map.py` already established for a different mechanism:
nothing here is ever trusted from a prior run or from the artifact's own
prose.

What it RE-DERIVES, and from where:
  1. CITATION EXISTENCE -- every commit/merge/sha-keyword citation in
     `<incident_dir>/214-LOG.md` and `<incident_dir>/AAR.md` names an
     object that genuinely exists in the repository (`git cat-file -t`),
     with two narrow, always-printed suppressions for the two
     conventions that legitimately quote a hex string which is not a
     commit claim (see CITATION_KEYWORDS below for the false-positive
     class this deliberately still accepts).
  2. ARTIFACT-SET COMPLETENESS -- the canonical nine-entry artifact set
     (ARTIFACT_SET) is present on disk AND tracked by git, with the one
     documented conditional member (`203-ORG.md` under a compliant
     Type-3 skip -- Type 1 requires it unconditionally).
  3. SAFETY.md SCHEMA CONFORMANCE -- for incidents dated after
     SAFETY_FENCE_EFFECTIVE_DATE, a genuine (```-delimited, JSON-parsing)
     verdict fence in `SAFETY.md` carries the keys
     `references/schemas.md` #5 declares.
  4. CLEAN TREE -- `git status --short` reports nothing dirty for the
     incident directory, and for any additional `--also-clean` path a
     caller names.
  5. NON-DEGENERATE COMMIT MESSAGES -- no commit touching the incident
     directory (or the `--commit-range` a caller names instead) carries
     a bare `@`-only line in its message body -- the shape a botched
     mail-merge or templated commit leaves behind.
  6. LOG ORDER -- for incidents dated after LOG_ORDER_EFFECTIVE_DATE, no
     DUPLICATE_TIMESTAMP_THRESHOLD-or-more `214-LOG.md` entries share one
     identical bracketed timestamp, and no two chronologically-comparable
     adjacent entries run backward; historical logs are never
     retroactively broken (see LOG_ORDER_EFFECTIVE_DATE below).

SCOPE (criterion 7): every check above is scoped to the ONE incident
directory named on the command line. This module never walks
`.dcs/incidents/` itself and never compares across incidents -- a
repository-wide historical sweep is a different, explicitly out-of-scope
tool.

It imports `dcs/hooks/dcs_gate.py` (a sibling file in both the repo and
the installed copy -- see _DCS_GATE_PATH) for the 214-LOG.md entry
grammar: ENTRY_PREFIX to split entries, STAMP_RE/sentinel_of() to
classify a sentinel line -- rather than re-deriving any of it. A second,
drifted copy of that grammar is exactly the defect class GRAMMAR_LINE
exists to prevent. If that import fails for any reason, this module
exits 2 with a clear message rather than silently falling back to a
local regex.

Stdlib-only, Python 3. `main()` sits behind `if __name__ == "__main__"`,
so importing this module (as `tests/test_doctrine_integrity.py` does, via
the same `importlib.util.spec_from_file_location` idiom already used for
`dcs_gate.py` and `preservation_map.py`) has no side effects.

Invocation:

    python "$HOME/.claude/dcs/tools/record_integrity.py" <incident_dir>
        [--also-clean <path> [--also-clean <path> ...]]
        [--commit-range <range>]

`--also-clean <path>` (repeatable, criterion 4) adds one more path to the
clean-tree check beyond `<incident_dir>` itself. `--commit-range <range>`
(criterion 5) replaces the default commit-message scope (every commit
`git log` finds touching `<incident_dir>`) with an explicit range/pathspec
of the caller's choosing -- the default is measured to under-cover a
merge commit that never itself touches the incident directory's own
files (see collect_commit_messages()'s docstring).

Exit codes (tests/payload_check.py's convention, matching
preservation_map.py's):
    0   clean -- every criterion that is in scope for this incident
        directory is satisfied; each out-of-scope criterion says so
    1   one or more findings (each printed, one per line)
    2   environment error -- missing incident directory, the
        dcs_gate.py import failed, git is not on PATH, or
        `<incident_dir>` is not inside a git work tree

Measured facts, recorded here with their commands rather than merely
asserted (principle 15 -- a derived fact is only as good as the command
that regenerates it). Re-run against THIS module's finished attempt-2
redesign (criteria 1(b) and 3) -- not carried over from attempt 1's own
now-superseded numbers, a staleness this same incident exists to close:

    for d in .dcs/incidents/*/; do python dcs/tools/record_integrity.py
    "$d"; done > /tmp/corpus_run.txt 2>&1

  - Over the 34 incident directories on disk at measurement time:
    `grep -c "resolves to" /tmp/corpus_run.txt` -> 72, all 72 reading
    `resolves to 'commit'` (`grep -c "resolves to 'commit'"` also 72, so
    0 resolve to `tree`/`blob`); `grep -c "does not resolve to a git
    object"` -> 3 -- the documented `sha`-keyword false positive
    (CITATION_KEYWORDS above; token 3df43fc8) at its original citation,
    hot-path-budget-eol-sensitivity/214-LOG.md:43, plus two citations of
    that same token inside this incident's own growing 214-LOG.md
    (lines 30 and 39 at measurement time -- the second a mid-line
    mention inside a SAFETY-HALT: entry, correctly a finding under this
    redesign since no genuine correction entry in that file names it).
    `grep -c "criterion 1:.*token '"` -> 77 total citation-position
    tokens (72 resolved + 3 findings + 2 suppressed below), matching the
    count CITATION_RE's alternation was corpus-tested against.
  - Suppression (a) (a citation inside a `stamp`-classified entry):
    `grep -c "suppression (a)"` -> 0, fixture-verified only -- a fixture
    that genuinely reaches this branch lives under
    `tests/fixtures/record-integrity/`, a different tasking's territory,
    not this module's.
  - Suppression (b), this incident's redesigned two-pass, file-scoped
    mechanism: `grep -c "suppression (b)"` -> 2, both in
    halt-enumeration-grammar-drift/214-LOG.md, whose own line-38
    RECORD-CORRECTION: entry names token b4af6e4. The widened scope
    (required behavior (ii)) means this ONE correction entry now
    suppresses BOTH the original fabricated citation it corrects (line
    37) and its own restatement of that same token (line 38), where the
    prior per-entry design only ever suppressed the latter. The same run
    independently confirms the one bound the Safety Officer checks:
    line 36's unrelated, genuine `integration commit 48ea59a` citation
    is untouched -- `.../214-LOG.md:36: token '48ea59a' ... resolves to
    'commit'` appears in the run unchanged, never swept into
    suppression (b).
"""
import argparse
import importlib.util
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# The exact invocation string, quoted verbatim by dcs/workflows/close.md's
# new fail-closed step (S4's territory) and re-read by a test (S2's
# territory) -- do not paraphrase either copy; a drifted second literal
# is exactly the class of defect this whole incident exists to close.
INVOCATION = 'python "$HOME/.claude/dcs/tools/record_integrity.py" <incident_dir>'

# Where dcs_gate.py lives, relative to THIS file, in both the repo layout
# (dcs/tools/record_integrity.py + dcs/hooks/dcs_gate.py, siblings under
# dcs/) and the installed layout (~/.claude/dcs/tools/... +
# ~/.claude/dcs/hooks/...) -- the same relative shape either way, so one
# path expression covers both without knowing which copy is running.
_DCS_GATE_PATH = Path(__file__).resolve().parent.parent / "hooks" / "dcs_gate.py"

# schemas.md's location, relative to this file, same two-layout logic as
# _DCS_GATE_PATH above.
_SCHEMAS_PATH = Path(__file__).resolve().parent.parent / "references" / "schemas.md"


def _load_dcs_gate():
    """Import dcs_gate.py from _DCS_GATE_PATH via the
    spec_from_file_location idiom (the same one dcs_gate.py itself
    documents as the way `tests/test_doctrine_integrity.py` imports
    `preservation_map.py`) -- never a package-relative `import`, since
    this file must run standalone from either the repo or the installed
    copy, with no `dcs` package on sys.path either way. Raises on any
    failure; main() is the only caller, and turns that into exit 2 with
    a clear message rather than falling back to a locally re-derived
    regex, per this incident's explicit tactic T2."""
    spec = importlib.util.spec_from_file_location("dcs_gate", str(_DCS_GATE_PATH))
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot build an import spec for {_DCS_GATE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------
# Criterion 1 -- citation-position sha check
# ---------------------------------------------------------------------

# Matched as whole words (via the mandatory `\s+` immediately after the
# keyword in CITATION_RE below -- "commits," or "commit-ish" never
# matches, only "commit <hex>"). `sha` stays in this tuple -- KEPT, not
# dropped -- on corpus evidence re-verified at command point 2 of this
# incident's replanned (attempt 2) period: of the 8 historical
# sha-keyword citation-position tokens on disk, 5 are TRUE commit
# citations across 4 separate incidents (ba6019e, 202e00a -- named
# twice, in two separate citations -- c73e498, 6766bbc); dropping the
# keyword to dodge the one false positive below would have silently
# stopped checking those 5 real ones too. The one documented false
# positive is
# .dcs/incidents/2026-07-25-hot-path-budget-eol-sensitivity/214-LOG.md:43,
# "...both copies byte-identical at sha 3df43fc8..." -- a file-content
# digest and a true statement, not a commit claim. Its remedy is NOT a
# keyword change: it is the same RECORD-CORRECTION: entry mechanism
# criterion 1(b) implements below (citation_findings() +
# correction_named_targets()) -- an operator appends a correction entry
# naming the token, and every occurrence of that token anywhere in the
# same 214-LOG.md is suppressed, printed as such, exactly like a
# genuine fabricated citation is cleared. Rewording future digests as
# "sha256 of <file>: <hex>" (so the keyword never sits immediately
# before the hex run) remains a valid style choice but is no longer the
# ONLY escape available -- the correction entry is.
CITATION_KEYWORDS = ("integration commit", "commit", "merge", "sha")

# Verified working pattern (IC ruling, command point 2; re-verified at
# this incident's own attempt-2 command point 2 against the redesigned
# criteria 1(b)/3): tested over all 34 incident directories present in
# this repository at measurement time -- 77 citation-position tokens
# total, 72 resolve to `commit`, 0 resolve to tree/blob (see the module
# docstring's "Measured facts" section for the fuller record, including
# the 3 that do not resolve and the 2 suppression (b) fires).
# Kept byte-for-byte as tested rather than re-derived from
# CITATION_KEYWORDS by string-joining, so nothing here can silently drift
# from the pattern that was actually corpus-verified; citation_tokens()
# below recovers the matched keyword from the match span instead of a
# second capturing group, for the same reason.
CITATION_RE = re.compile(
    r"\b(?:integration\s+commit|commit|merge|sha)\s+`?([0-9a-fA-F]{7,40})`?\b",
    re.I,
)


def citation_tokens(text):
    """(line_no, token, matched_keyword) for every hex run of 7-40 chars
    immediately preceded, on the same physical line, by one of
    CITATION_KEYWORDS. Pure -- no filesystem or git access, and no
    knowledge of 214-LOG.md's entry grammar (that is layered on top, by
    citation_findings() below, only for the one file where suppression
    applies). `line_no` is 1-indexed against `text`'s own lines.
    `matched_keyword` is recovered from the match span (the text between
    the full match's start and the captured token's start, stripped of
    the pattern's own optional backtick and whitespace) rather than a
    second capturing group, so CITATION_RE stays exactly the pattern
    that was corpus-tested."""
    tokens = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for m in CITATION_RE.finditer(line):
            token = m.group(1)
            prefix = line[m.start():m.start(1)]
            keyword = re.sub(r"\s+", " ", prefix.rstrip("` \t")).strip().lower()
            tokens.append((line_no, token, keyword))
    return tokens


def split_log_entries(text, entry_prefix_re):
    """214-LOG.md's own entry grammar, applied structurally: a list of
    (start_line, end_line, entry_text) tuples, 1-indexed and inclusive,
    in file order. An entry begins at any line `entry_prefix_re` matches
    (dcs_gate.py's own ENTRY_PREFIX, imported and never re-derived) and
    continues through every following line that does NOT itself match --
    exactly GRAMMAR_LINE's boundary rule, applied to the whole file
    rather than to one sentinel lookup. Lines before the first
    entry-start (this file's leading HTML-comment header) belong to no
    entry and are never returned here; citation_findings() treats a
    token found there as ungoverned by either suppression."""
    lines = text.splitlines()
    entries = []
    start = None
    buf = []
    for line_no, line in enumerate(lines, start=1):
        if entry_prefix_re.match(line):
            if start is not None:
                entries.append((start, line_no - 1, "\n".join(buf)))
            start = line_no
            buf = [line]
        elif start is not None:
            buf.append(line)
    if start is not None:
        entries.append((start, len(lines), "\n".join(buf)))
    return entries


def _entry_containing(entries, line_no):
    """The (start, end, body) entry that `line_no` falls inside, or None
    if it precedes the first entry (or `entries` is empty)."""
    for start, end, body in entries:
        if start <= line_no <= end:
            return start, end, body
    return None


def correction_named_targets(entries, correction_re):
    """{token: [start_line, start_line, ...]} for every hex token a
    genuine RECORD-CORRECTION: entry NAMES in its own body -- pass 1 of
    criterion 1(b)'s two-pass suppression (IAP tactic T2). An entry
    counts as a correction entry only when `correction_re` (built by the
    caller from dcs_gate.ENTRY_PREFIX by concatenation, never re-derived
    here -- IAP tactic T1) matches its FIRST line; a mid-line,
    non-entry-initial mention of the literal "RECORD-CORRECTION:"
    string -- e.g. a later entry quoting or discussing the convention in
    prose -- never qualifies, no matter where the substring sits in its
    body. This is what makes required behavior (i) hold: suppression
    (b) can only ever be authorized by a genuine entry, never a passing
    mention.

    NAMING RULE (documented here, the one place it lives, per this
    incident's tasking): "names" is deliberately the SAME test
    citation_tokens() applies everywhere else in this module, run over
    the correction entry's own body -- a hex run of CITATION_RE's own
    captured shape (7-40 hex chars, word-bounded) immediately preceded
    by one of CITATION_KEYWORDS. It is deliberately NOT "any 7-40 char
    hex run anywhere in the body": a correction entry's prose routinely
    mentions OTHER, unrelated, genuinely valid citations while
    explaining itself -- e.g. halt-enumeration-grammar-drift/
    214-LOG.md:38's own correction entry also says "48ea59a, named on
    the preceding line 36, is the integration commit...", a true
    citation on a nearby line, not the token this entry corrects.
    Because "48ea59a" there is never immediately preceded by one of
    CITATION_KEYWORDS within that sentence (it opens a new sentence),
    citation_tokens() does not capture it as named, and it is never
    swept into the suppression set -- exactly the bound the Safety
    Officer checks for this incident.

    Multiple correction entries naming the same token accumulate their
    start lines in file order (a list, not a set): pass 2 in
    citation_findings() below can then report every authorizing entry a
    suppressed citation names, not just one."""
    targets = {}
    for start, end, body in entries:
        body_lines = body.splitlines()
        first_line = body_lines[0] if body_lines else ""
        if not correction_re.match(first_line):
            continue
        named_here = {token for _line_no, token, _keyword in citation_tokens(body)}
        for token in named_here:
            targets.setdefault(token, []).append(start)
    return targets


def _resolve_citation(repo_root, path, line_no, token, keyword):
    """git cat-file -t <token>, run with the incident's repo as context.
    Returns a one-element (or empty) findings list: a non-zero exit is
    the ONLY thing that counts as a finding here. A zero exit is never a
    finding by itself -- it is printed (the resolved type, whatever it
    is) so a `commit`-keyword citation that actually resolves to a
    `tree` or `blob` is visible to a reader rather than silently accepted
    as though it were a commit, per this criterion's own instruction;
    the measured corpus fact above (module docstring, regenerated by the
    corpus command it names) records where this repository's real
    citations resolve, without a second, separately-drifting copy of
    that count repeated here.

    The FINDING text for a non-resolving token carries the
    RECORD-CORRECTION: remedy inline and states its required shape --
    this incident's own requirement: a blocked operator sees this one
    line and nothing else, since no shipped prose in doctrine.md,
    forms.md or close.md documents the convention today (measured: zero
    hits package-wide; the IC queued documenting it as a separate
    follow-up rather than fixing it here). The remedy names the same
    three things correction_named_targets() itself requires to
    recognize an entry: a column-zero bracketed timestamp, the literal
    sentinel 'RECORD-CORRECTION:' immediately after it, and this token
    named in the entry's own body immediately after one of
    CITATION_KEYWORDS."""
    proc = subprocess.run(
        ["git", "-C", str(repo_root), "cat-file", "-t", token],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        remedy = (
            "Remedy: append a new 214-LOG.md entry beginning at column "
            "zero with a bracketed timestamp, carrying the literal "
            "sentinel 'RECORD-CORRECTION:' immediately after it, that "
            f"names token '{token}' in its own body immediately after "
            f"one of this check's own citation keywords (e.g. \"commit "
            f"{token}\" or \"sha {token}\") -- that is the only shape "
            "this check recognizes to suppress a corrected citation, "
            "anywhere in this same file, on every future run."
        )
        return [
            f"criterion 1: FINDING: {path.as_posix()}:{line_no}: token '{token}' "
            f"(keyword '{keyword}') does not resolve to a git object "
            f"(git cat-file -t exit {proc.returncode}: {proc.stderr.strip()}). "
            f"{remedy}"
        ]
    resolved_type = proc.stdout.strip()
    print(
        f"criterion 1: {path.as_posix()}:{line_no}: token '{token}' "
        f"(keyword '{keyword}') resolves to '{resolved_type}'"
    )
    return []


def citation_findings(incident_dir, repo_root, dcs_gate):
    """Criterion 1 in full: citation_tokens() over `214-LOG.md` and
    `AAR.md`, with 214-LOG.md's tokens additionally screened against two
    entry-scoped suppressions (never applied to AAR.md, which has no
    entry grammar at all). Both suppressions are printed when they fire,
    naming what was suppressed, why, and (suppression (b)) the line
    number of the correction entry that authorized it -- never silent.

    Suppression (b) is a two-pass, file-scoped mechanism (IAP tactic T2,
    this incident's redesign of what was a per-entry body-anywhere
    substring test): pass 1, correction_named_targets(), walks every
    entry split_log_entries() finds and collects the set of tokens a
    genuine RECORD-CORRECTION: entry (first line only, per IAP tactic
    T1 -- never a body-anywhere test) names in its own body; pass 2, the
    loop below, suppresses a citation-position token iff its value is in
    that file-wide set. This is deliberately wider than "anywhere
    earlier" (a strict superset, ratified at command point 2): a
    correction entry anywhere in the file clears every occurrence of its
    named token anywhere in the same 214-LOG.md, including occurrences
    that precede the correction entry itself -- required behavior (ii)."""
    findings = []
    incident_dir = Path(incident_dir)
    entry_prefix_re = re.compile(dcs_gate.ENTRY_PREFIX)
    correction_re = re.compile(dcs_gate.ENTRY_PREFIX + r"RECORD-CORRECTION:")

    log_path = incident_dir / "214-LOG.md"
    if log_path.is_file():
        text = log_path.read_text(encoding="utf-8")
        entries = split_log_entries(text, entry_prefix_re)
        named_targets = correction_named_targets(entries, correction_re)
        for line_no, token, keyword in citation_tokens(text):
            entry = _entry_containing(entries, line_no)
            suppression = None
            authorizing_lines = None
            if entry is not None:
                _, _, body = entry
                body_lines = body.splitlines()
                first_line = body_lines[0] if body_lines else ""
                if dcs_gate.sentinel_of(first_line) == "stamp":
                    suppression = "a"
                elif token in named_targets:
                    suppression = "b"
                    authorizing_lines = named_targets[token]
            if suppression == "a":
                print(
                    f"criterion 1: SUPPRESSED {log_path.as_posix()}:{line_no}: "
                    f"token '{token}' (keyword '{keyword}') -- suppression (a): "
                    "this entry's own sentinel line classifies as 'stamp' "
                    "(dcs_gate.sentinel_of) -- a sha256 digest of an approved "
                    "IAP.md, not a commit claim"
                )
                continue
            if suppression == "b":
                lines_desc = ", ".join(str(n) for n in authorizing_lines)
                plural = len(authorizing_lines) != 1
                print(
                    f"criterion 1: SUPPRESSED {log_path.as_posix()}:{line_no}: "
                    f"token '{token}' (keyword '{keyword}') -- suppression (b): "
                    f"named as a corrected target by the RECORD-CORRECTION: "
                    f"entr{'ies' if plural else 'y'} at line{'s' if plural else ''} "
                    f"{lines_desc} of this same file -- that convention exists "
                    "to name a bad token, anywhere in the file, while "
                    "correcting the record that cited it"
                )
                continue
            findings.extend(
                _resolve_citation(repo_root, log_path, line_no, token, keyword)
            )

    aar_path = incident_dir / "AAR.md"
    if aar_path.is_file():
        text = aar_path.read_text(encoding="utf-8")
        for line_no, token, keyword in citation_tokens(text):
            findings.extend(
                _resolve_citation(repo_root, aar_path, line_no, token, keyword)
            )

    return findings


# ---------------------------------------------------------------------
# Criterion 2 -- artifact-set completeness
# ---------------------------------------------------------------------

# The canonical nine-entry artifact set, in this exact order. Stable,
# importable module-level name: S2's carrier cases (tests/
# test_doctrine_integrity.py) read this tuple directly rather than
# retyping its members, so that forms.md's own prose list and this
# tuple cannot silently drift apart. "204-TASKING" names the directory
# as ONE entry regardless of how many specialist files it holds --
# never expanded into a per-specialist member.
ARTIFACT_SET = (
    "201-BRIEF.md",
    "202-OBJECTIVES.md",
    "203-ORG.md",
    "204-TASKING",
    "IAP.md",
    "IAP-APPROVED",
    "214-LOG.md",
    "SAFETY.md",
    "AAR.md",
)

TYPE_RE = re.compile(r"^\*\*Type:\*\*\s*(\d+)", re.M)
SKIP_RE = re.compile(r"\b203(?:-ORG\.md)?\s+skipped\b.*?default\s+Type\s*3\s+activation", re.I)


def _relposix(path, root):
    """`path` relative to `root`, forward-slashed. Falls back to
    os.path.relpath if Path.relative_to raises (observed on Windows when
    the two absolute forms disagree only in case or in an extended-length
    \\\\?\\ prefix that git's own rev-parse --show-toplevel does not
    emit) -- either way the result is the same logical relative path."""
    p = Path(path).resolve()
    r = Path(root).resolve()
    try:
        rel = p.relative_to(r)
    except ValueError:
        rel = Path(os.path.relpath(str(p), str(r)))
    return rel.as_posix()


def _read_optional(path):
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def _tracked_files_under(repo_root, incident_dir):
    """Repo-relative POSIX paths `git ls-files` reports as tracked under
    `incident_dir`, scoped with `-- <incident_dir>` so this is always a
    check of the ONE incident currently closing, never a repo-wide sweep
    (criterion 7). Empty set (never an exception) if the git invocation
    itself fails."""
    proc = subprocess.run(
        ["git", "-C", str(repo_root), "ls-files", "--", str(incident_dir)],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        return set()
    return set(proc.stdout.splitlines())


def artifact_set_findings(incident_dir, repo_root):
    """Criterion 2 in full: every ARTIFACT_SET entry present on disk AND
    tracked, with 203-ORG.md's one documented conditional exemption
    (present iff the incident's own 201-BRIEF.md types it Type 3 AND its
    214-LOG.md carries a compliant skip note -- Type 1 requires it
    unconditionally, skip note or not). Always prints one honest
    disposition line; never claims "9/9" when a file is legitimately
    absent under the compliant skip."""
    findings = []
    incident_dir = Path(incident_dir)
    incident_rel = _relposix(incident_dir, repo_root)
    tracked = _tracked_files_under(repo_root, incident_dir)

    statuses = []
    for entry in ARTIFACT_SET:
        target = incident_dir / entry
        if entry == "204-TASKING":
            on_disk = target.is_dir() and any(target.iterdir())
            prefix = f"{incident_rel}/{entry}/"
            is_tracked = any(p.startswith(prefix) for p in tracked)
        else:
            on_disk = target.is_file()
            rel = f"{incident_rel}/{entry}"
            is_tracked = rel in tracked
        statuses.append((entry, on_disk, is_tracked))

    missing = [e for e, disk, _ in statuses if not disk]
    untracked = [e for e, disk, trk in statuses if disk and not trk]
    n_ok = len([e for e, disk, trk in statuses if disk and trk])

    for e in untracked:
        findings.append(
            f"criterion 2: FINDING: {incident_rel}/{e} is present on disk "
            "but not tracked by git"
        )

    org_missing = "203-ORG.md" in missing
    other_missing = [e for e in missing if e != "203-ORG.md"]
    for e in other_missing:
        findings.append(
            f"criterion 2: FINDING: {incident_rel}/{e} is missing from the "
            "canonical 9-artifact set"
        )

    org_compliant = False
    skip_line_no = None
    type_num = None
    if org_missing:
        brief_text = _read_optional(incident_dir / "201-BRIEF.md")
        log_text = _read_optional(incident_dir / "214-LOG.md")
        if brief_text is not None:
            m = TYPE_RE.search(brief_text)
            if m:
                type_num = int(m.group(1))
        if log_text is not None:
            for i, line in enumerate(log_text.splitlines(), start=1):
                if SKIP_RE.search(line):
                    skip_line_no = i
                    break
        org_compliant = type_num == 3 and skip_line_no is not None
        if not org_compliant:
            findings.append(
                "criterion 2: FINDING: "
                f"{incident_rel}/203-ORG.md is missing without a compliant "
                f"Type-3 skip (201-BRIEF.md Type={type_num!r}, 214-LOG.md "
                f"skip note found={skip_line_no is not None}) -- Type 1 "
                "requires 203-ORG.md unconditionally, and a Type-3 skip "
                "requires a logged skip note"
            )

    if not other_missing and not untracked and (not org_missing or org_compliant):
        if org_missing:
            print(
                f"criterion 2: {n_ok} present and tracked, plus one "
                f"compliant 203-ORG.md skip (Type 3, skip note at "
                f"214-LOG.md:{skip_line_no})"
            )
        else:
            print(f"criterion 2: {n_ok} present and tracked")
    else:
        print(
            f"criterion 2: {n_ok} present and tracked, out of "
            f"{len(ARTIFACT_SET)} canonical artifacts -- see findings above "
            "for the rest"
        )

    return findings


# ---------------------------------------------------------------------
# Criterion 3 -- SAFETY.md verdict-fence schema check
# ---------------------------------------------------------------------

# Dirs dated on or before this pin are OUT OF SCOPE for criterion 3 --
# this is a NEW convention (a JSON verdict fence in SAFETY.md) that no
# incident before this one was ever asked to follow, so scoping it to
# "strictly after" rather than checking history is what keeps criterion
# 7's scope boundary real (see the module docstring's SCOPE section).
# The comparison below (dir_date <= SAFETY_FENCE_EFFECTIVE_DATE ->
# out of scope) is plain ISO-8601 string comparison, which sorts
# correctly because every incident directory name's leading date is
# zero-padded YYYY-MM-DD; this incident's own fix changed only the
# pinned value below, never that comparison's sense, which was already
# correct STRICT-GREATER-THAN scoping (a directory dated strictly after
# the pin is in scope, the pin date itself is out). Pinned to this
# incident's own opening date, 2026-08-02: this incident's own directory
# (2026-08-02-close-integrity-guard-bundle) and every incident before
# it -- including 2026-08-02-record-integrity-corrections, dated the
# same day -- stay out of scope; only a directory dated strictly after
# this day enters scope. `_NE_EFFECTIVE_DATE` in
# tests/test_doctrine_integrity.py (S2's territory) shares this same
# value today but remains a SEPARATE constant on purpose, never
# asserted equal to this one anywhere: this one ships and is universal
# to every installing project; that one pins only this repository's own
# English-only mandate. The two sharing a value is incidental to both
# being dated from this incident's own opening day, not a coupling
# either constant's owner may rely on.
SAFETY_FENCE_EFFECTIVE_DATE = "2026-08-02"

_DIR_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-")

# The built-in fallback field set (name -> required?), used only when
# schemas.md itself cannot be read or its #5 table cannot be parsed --
# always printed when it fires, never a silent substitution. Mirrors
# references/schemas.md #5 (Safety-officer verdict) as of this module's
# writing: verdict/refutations/checked required, advisories optional.
_SAFETY_FIELDS_FALLBACK = {
    "verdict": True,
    "refutations": True,
    "advisories": False,
    "checked": True,
}

_SCHEMAS_SAFETY_HEADING_RE = re.compile(r"^##\s*5\.\s*Safety-officer verdict", re.IGNORECASE)
_SCHEMAS_ANY_HEADING_RE = re.compile(r"^##\s")
_SCHEMAS_FIELD_ROW_RE = re.compile(r"^\|\s*`([A-Za-z_]+)`\s*\|(.*)$")


def _fenced_json_blocks(text):
    """Every fenced (``` / ```) code block in `text` whose body parses as
    JSON, as (open_line, parsed_object) pairs in file order. Reimplements
    dcs/tools/preservation_map.py's `_fenced_blocks_text` idiom LOCALLY
    (line-based: a fence delimiter is recognised only when a physical
    line's STRIPPED content starts with three backticks -- never a
    substring search anywhere else in the line) rather than importing
    it, so this module stays import-clean and side-effect-free on its
    own, with no dependency on a sibling tool -- and extends it with
    line tracking, which that function's own caller never needed.

    This distinction is load-bearing, not stylistic: this incident's own
    predecessor's SAFETY.md (record-integrity-corrections/SAFETY.md:33)
    contains the literal text "```json" inside a single-backtick
    INLINE-code span, in prose about the ABSENCE of a fence in some other
    files. A substring search (`"```json" in text`, or `re.search`
    without anchoring to line start) would misfire on that exact line.
    This function does not, because that line's own stripped content
    begins with "11.", never with three backticks -- only a line-start
    check is safe here, which is exactly what this reimplementation is
    provably doing.
    """
    blocks = []
    in_block = False
    open_line = None
    cur = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith("```"):
            if in_block:
                body = "\n".join(cur)
                try:
                    parsed = json.loads(body)
                except (json.JSONDecodeError, ValueError):
                    parsed = None
                if parsed is not None:
                    blocks.append((open_line, parsed))
                cur = []
                in_block = False
                open_line = None
            else:
                in_block = True
                open_line = line_no
        elif in_block:
            cur.append(line)
    return blocks


def _parse_safety_fields(schemas_text):
    """{field_name: required_bool} for schemas.md #5's field table, read
    from the section between the "## 5. Safety-officer verdict" heading
    and the next "## " heading. A table row's Type/Notes columns are not
    split precisely (one of them, `verdict`'s, contains a markdown-
    escaped literal pipe that would defeat a naive column split) --
    instead, everything after the field-name cell is scanned as one
    string for the substring "optional", which is exactly how
    schemas.md marks an optional field (`advisories` | object[],
    optional |) and appears nowhere else in this table's Notes prose.
    Returns {} if the heading or the table is not found -- callers
    treat that as "unparseable" and fall back to _SAFETY_FIELDS_FALLBACK,
    always printing that they did."""
    fields = {}
    in_section = False
    for line in schemas_text.splitlines():
        if _SCHEMAS_SAFETY_HEADING_RE.match(line):
            in_section = True
            continue
        if in_section and _SCHEMAS_ANY_HEADING_RE.match(line):
            break
        if in_section:
            m = _SCHEMAS_FIELD_ROW_RE.match(line)
            if m:
                name, rest = m.group(1), m.group(2)
                fields[name] = "optional" not in rest.lower()
    return fields


def _safety_schema_fields():
    """The field set to validate a genuine verdict fence against --
    parsed from _SCHEMAS_PATH at run time (never hardcoded) unless that
    file is unreachable or unparseable, in which case
    _SAFETY_FIELDS_FALLBACK is used and that disposition is printed,
    never silently substituted."""
    text = _read_optional(_SCHEMAS_PATH)
    if text is None:
        print(
            f"criterion 3: {_SCHEMAS_PATH} unreachable -- falling back to "
            f"the built-in SAFETY.md field set {sorted(_SAFETY_FIELDS_FALLBACK)}"
        )
        return dict(_SAFETY_FIELDS_FALLBACK)
    fields = _parse_safety_fields(text)
    if not fields:
        print(
            f"criterion 3: could not parse a field table from "
            f"{_SCHEMAS_PATH} -- falling back to the built-in SAFETY.md "
            f"field set {sorted(_SAFETY_FIELDS_FALLBACK)}"
        )
        return dict(_SAFETY_FIELDS_FALLBACK)
    return fields


def safety_verdict_fence_findings(fences, fields, safety_path):
    """Pure comparator: given `fences` (_fenced_json_blocks()'s own
    (open_line, obj) pairs, already parsed -- no filesystem or git
    access here) and `fields` (_safety_schema_fields()'s {name:
    required_bool} spec), validate ONLY the fences that carry a
    `verdict` key -- criterion 3's genuine verdict-fence schema check,
    rescoped this way by this incident's redesign (IAP tactic T3) so a
    SAFETY.md that happens to also contain some OTHER JSON fence (an
    example, a different tool's output) is never fail-closed against
    the verdict schema merely for existing. A fence that does not even
    parse to a JSON object -- so it cannot carry any key at all -- is
    non-verdict for the same reason. Mirrors
    clean_tree_findings()/degenerate_message_findings()'s own
    pure-comparator shape: takes already-collected data, touches
    nothing, so this half of criterion 3 is testable on a fixture's
    already-parsed fence list without a real SAFETY.md on disk.

    Returns (findings, verdict_fences, non_verdict_fences). The caller
    (safety_fence_findings() below, the IO-collector half of this
    split) decides what an EMPTY verdict_fences list means (no genuine
    verdict fence anywhere, even if non-verdict fences exist) and
    prints one note per non_verdict_fences entry -- a non-verdict fence
    is information, never a finding on its own."""
    findings = []
    verdict_fences = []
    non_verdict_fences = []
    required = sorted(k for k, req in fields.items() if req)
    for open_line, obj in fences:
        if not isinstance(obj, dict) or "verdict" not in obj:
            non_verdict_fences.append((open_line, obj))
            continue
        verdict_fences.append((open_line, obj))
        for k in required:
            if k not in obj:
                findings.append(
                    f"criterion 3: FINDING: {safety_path.as_posix()}:{open_line} "
                    f"verdict fence missing required key '{k}'"
                )
        for k in obj.keys():
            if k not in fields:
                findings.append(
                    f"criterion 3: FINDING: {safety_path.as_posix()}:{open_line} "
                    f"verdict fence has unrecognized key '{k}' (not in "
                    "schemas.md #5's field table)"
                )
    return findings, verdict_fences, non_verdict_fences


def safety_fence_findings(incident_dir):
    """Criterion 3 in full, the IO-collector half of this incident's
    pure-comparator/IO-collector split (IAP tactic T3): date-scope the
    incident directory by its own name first (always printed, never a
    silent skip); only if in scope, read SAFETY.md, find its genuine
    JSON fence(s) via _fenced_json_blocks, then hand them to
    safety_verdict_fence_findings() (the pure comparator above) for the
    actual field-schema check. A non-verdict-shaped fence -- one that
    parses as JSON but carries no `verdict` key, or does not even parse
    to an object -- is printed as a note, never a finding; an in-scope
    SAFETY.md whose fences are ALL non-verdict-shaped (including the
    zero-fences case) still produces the one "no genuine verdict fence"
    finding, since criterion 3 requires at least one real verdict fence
    to exist, not merely some JSON somewhere in the file."""
    findings = []
    incident_dir = Path(incident_dir)
    dir_name = incident_dir.name

    m = _DIR_DATE_RE.match(dir_name)
    if not m:
        print(
            f"criterion 3: {dir_name} carries no parseable leading "
            "YYYY-MM-DD date -- SAFETY.md check out of scope"
        )
        return findings
    dir_date = m.group(1)
    if dir_date <= SAFETY_FENCE_EFFECTIVE_DATE:
        print(
            f"criterion 3: {dir_name} dated {dir_date} is on or before "
            f"SAFETY_FENCE_EFFECTIVE_DATE {SAFETY_FENCE_EFFECTIVE_DATE} -- "
            "SAFETY.md check out of scope"
        )
        return findings
    print(
        f"criterion 3: {dir_name} dated {dir_date} is after "
        f"SAFETY_FENCE_EFFECTIVE_DATE {SAFETY_FENCE_EFFECTIVE_DATE} -- "
        "SAFETY.md check in scope"
    )

    safety_path = incident_dir / "SAFETY.md"
    if not safety_path.is_file():
        findings.append(
            f"criterion 3: FINDING: {safety_path.as_posix()} is missing "
            "(in scope, required)"
        )
        return findings

    text = safety_path.read_text(encoding="utf-8")
    fences = _fenced_json_blocks(text)

    fields = dict(_SAFETY_FIELDS_FALLBACK)
    if fences:
        fields = _safety_schema_fields()

    field_findings, verdict_fences, non_verdict_fences = safety_verdict_fence_findings(
        fences, fields, safety_path
    )
    for open_line, obj in non_verdict_fences:
        obj_desc = (
            "a JSON object with no 'verdict' key" if isinstance(obj, dict)
            else f"valid JSON but not an object ({type(obj).__name__})"
        )
        print(
            f"criterion 3: {safety_path.as_posix()}:{open_line} fenced JSON "
            f"block is {obj_desc} -- not a verdict fence, not validated "
            "against the verdict schema"
        )

    if not verdict_fences:
        findings.append(
            f"criterion 3: FINDING: {safety_path.as_posix()} has no genuine "
            "verdict-shaped JSON fence (a ```-delimited block whose body "
            "parses as a JSON object carrying a 'verdict' key) -- required "
            "for incidents in scope"
        )
        return findings

    findings.extend(field_findings)
    return findings


# ---------------------------------------------------------------------
# Criterion 4 -- clean-tree check
# ---------------------------------------------------------------------

def clean_tree_findings(porcelain_text, label):
    """Pure comparator: one finding per non-empty line of `porcelain_text`
    (a `git status --short` run's stdout), each naming `label` so several
    checked paths stay distinguishable in output. Takes text, touches
    nothing -- this is what makes criterion 4 testable at all without a
    real dirty working tree (a fixture cannot carry an untracked file;
    git itself stores no such thing)."""
    findings = []
    for line in porcelain_text.splitlines():
        if line.strip():
            findings.append(f"criterion 4: FINDING: clean-tree ({label}): {line}")
    return findings


def collect_clean_tree_findings(repo_root, incident_dir, also_clean):
    """Criterion 4's git-invoking collector: `git status --short` against
    the incident directory, plus one run per repeatable `--also-clean`
    path. NEVER hardcodes any path beyond the incident directory itself
    -- every extra path comes from the caller. Prints every path actually
    checked, always."""
    findings = []
    checks = [("incident directory", str(incident_dir))]
    checks += [("--also-clean", p) for p in also_clean]
    for label, path in checks:
        print(f"criterion 4: checking clean tree for {label}: {path}")
        proc = subprocess.run(
            ["git", "-C", str(repo_root), "status", "--short", "--", path],
            capture_output=True, text=True,
        )
        if proc.returncode != 0:
            findings.append(
                f"criterion 4: FINDING: git status --short -- {path} could "
                f"not run (exit {proc.returncode}): {proc.stderr.strip()}"
            )
            continue
        findings.extend(clean_tree_findings(proc.stdout, f"{label} {path}"))
    return findings


# ---------------------------------------------------------------------
# Criterion 5 -- degenerate commit-message check
# ---------------------------------------------------------------------

_RECORD_SEP = "\x1e"
_UNIT_SEP = "\x1f"


def degenerate_message_findings(messages):
    """Pure comparator: one finding per (commit_ref, message_text) pair
    in `messages` whose message body contains a bare `@`-only line (a
    line that, stripped, is exactly "@" -- the shape a botched mail-merge
    or templated commit leaves behind). Takes text, touches nothing --
    this is what makes criterion 5 testable at all without a real commit
    carrying a corrupt message (git stores no such fixture-friendly
    handle; a fixture directory cannot carry a commit)."""
    findings = []
    for commit_ref, message_text in messages:
        for line in message_text.splitlines():
            if line.strip() == "@":
                findings.append(
                    "criterion 5: FINDING: commit "
                    f"{commit_ref} has a degenerate message -- a bare "
                    "'@'-only line in its body"
                )
                break
    return findings


def collect_commit_messages(repo_root, incident_dir, commit_range):
    """Criterion 5's git-invoking collector. Default scope is every
    commit `git log` finds touching `incident_dir`; `--commit-range`
    overrides that scope entirely with the caller's own range/pathspec
    expression (shlex-split, so a multi-token range like "HEAD~5..HEAD --
    src/" works). PRINTS the scope actually used, always -- the default
    is measured to under-cover: a merge commit that integrates an
    incident's territory files without itself touching the incident
    directory (e.g. this repository's own record-integrity-corrections
    incident, whose integration commit 7fcab05 touches only the four
    corrected artifact directories, never its own not-yet-created
    directory) is invisible to the default scope.

    Returns (messages, error): `messages` is a list of (commit_ref,
    message_text) pairs ready for degenerate_message_findings(); `error`
    is None on success or a stderr string if the git invocation itself
    failed (main() turns that into its own finding, never a silent
    empty scan)."""
    if commit_range:
        range_args = shlex.split(commit_range)
        scope_desc = f"git log {commit_range} (--commit-range override)"
    else:
        range_args = ["--", str(incident_dir)]
        scope_desc = (
            f"git log -- {incident_dir} (default scope; known to "
            "under-cover a merge commit that integrates the incident's "
            "territory without itself touching the incident directory)"
        )
    print(f"criterion 5: commit-message scope = {scope_desc}")

    proc = subprocess.run(
        ["git", "-C", str(repo_root), "log", f"--format=%H{_UNIT_SEP}%B{_RECORD_SEP}"]
        + range_args,
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        return [], proc.stderr.strip()

    messages = []
    for record in proc.stdout.split(_RECORD_SEP):
        record = record.strip("\n")
        if not record or _UNIT_SEP not in record:
            continue
        ref, _, body = record.partition(_UNIT_SEP)
        messages.append((ref, body))
    return messages, None


def commit_message_findings(repo_root, incident_dir, commit_range):
    """Criterion 5 in full: collect_commit_messages() then
    degenerate_message_findings() over the result; a failed collection
    is itself one finding rather than a silent empty pass."""
    messages, error = collect_commit_messages(repo_root, incident_dir, commit_range)
    if error is not None:
        return [f"criterion 5: FINDING: git log could not run: {error}"]
    return degenerate_message_findings(messages)


# ---------------------------------------------------------------------
# Criterion 6 -- 214-LOG.md duplicate/out-of-order timestamp check
# ---------------------------------------------------------------------

# Dirs dated on or before this pin are OUT OF SCOPE for criterion 6 -- the
# same "new convention, strictly-after scoping" rationale
# SAFETY_FENCE_EFFECTIVE_DATE documents above (record_integrity.py:633-657):
# a canonical, timestamp-honest append tool is a NEW convention no
# incident before it ships was ever asked to follow, so history is never
# retroactively broken. Pinned to the day the tool lands, 2026-08-04 --
# NOT this incident's own opening day, which is one day earlier (see
# below, same comment, for that one-day gap and why it is load-bearing).
# The comparison below (dir_date <=
# LOG_ORDER_EFFECTIVE_DATE -> out of scope) is the same plain ISO-8601
# STRING comparison criterion 3 already established, correct because
# every incident directory name's leading date is zero-padded YYYY-MM-DD.
#
# The scope test reads the INCIDENT DIRECTORY's own leading date, NEVER an
# individual 214-LOG.md entry's own bracketed timestamp --
# collect_log_order_findings() below scopes on `incident_dir.name` alone,
# exactly like safety_fence_findings() does for criterion 3. This
# distinction is load-bearing for THIS incident's own directory
# (2026-08-03-log-append-helper, opened 2026-08-03, one day before the
# pin): real wall-clock time crosses 2026-08-04 while this incident is
# still open, so several of this very file's own entries carry an 08-04
# bracket -- that must never, by itself, pull this log into scope. Only
# the directory's OWN opening date decides.
LOG_ORDER_EFFECTIVE_DATE = "2026-08-04"

# The smallest identical-bracket run length treated as a finding rather
# than a plausible honest collision. Once dcs_log.py is the one true
# writer of every entry in scope (LOG_ORDER_EFFECTIVE_DATE above), 3
# rests on dcs_log.py's own SUB-SECOND precision -- NOT on a same-SECOND
# collision argument. An earlier version of this comment argued the
# latter ("2 is reachable that way, 3 is not"), and the Safety Officer
# falsified it (incident log-append-helper's own fix-tasking cycle): 6
# real sequential appends through the tool, at its THEN-current
# whole-second-only precision (a `.replace(microsecond=0)` truncation,
# since removed), produced a 5-entry identical-bracket run, honestly,
# with no backfilling -- proof that a same-second collision reaches well
# past 2 once a TOOL, not a human, is appending rapidly, so a
# same-second argument was never sound here, at any run length.
#
# dcs_log.py now stamps every entry with
# `datetime.now().astimezone().isoformat()` at call time
# (dcs_log.py:384), full sub-second precision, never truncated or
# rounded. That removes the collision surface the old argument depended
# on, rather than merely narrowing it: two honest, independent appends
# sharing an identical timestamp down to the microsecond is not a
# plausible clock reading, and a THIRD sharing it too, from the same
# tool, is a legitimate backfill/tampering signal, not a corpus-tuned
# guess.
#
# Verified, not merely asserted (principle 15), against dcs_log.py as it
# ships today -- run against a disposable scratch incident directory,
# never against a real one in this repository (outside this module's own
# file territory): 12 honest, sequential CLI appends (`python
# dcs/tools/dcs_log.py append <slug> --by <operator> "<text>"`, run back
# to back with no delay beyond Python's own process-startup cost)
# produced 12 distinct timestamps, none sharing even their microsecond
# field -- `2026-08-04T09:23:41.300219+11:00` through
# `2026-08-04T09:23:42.951810+11:00`, ~150ms apart (process-spawn-bound,
# not clock-bound). Zero collisions of any length, let alone 3.
#
# The historical corpus measurement below (using this same module's own
# split_log_entries() + dcs_gate.ENTRY_PREFIX, counting MAXIMAL
# CONSECUTIVE runs of an identical raw bracket string -- never runs
# split across non-adjacent entries, exactly what log_order_findings()
# below itself checks) predates this rationale and is kept only as
# background on PRE-TOOL, hand-typed/copy-pasted logs -- every directory
# it covers is out of scope by construction (dated on or before
# LOG_ORDER_EFFECTIVE_DATE), so it is neither evidence for nor against 3
# as a threshold for entries THIS tool writes; the sub-second
# measurement above carries that weight now. Re-run the command below
# against THIS repository's own .dcs/incidents/*/214-LOG.md (never a
# fixture) to regenerate the figures -- the low end (run-length 1, i.e.
# no duplicate at all) is expected to keep climbing as this incident's
# own still-open log keeps growing while it is worked (315 at first
# measurement, 322 as of this rewrite, both already superseded by the
# time this incident closes), while every OTHER bucket (2 and up) has
# stayed identical across both measurements, because entries in an
# actively-worked, precision-timestamped log are (near) always
# singletons:
#
#   python -c "
#   import importlib.util, re
#   from pathlib import Path
#   from collections import Counter
#   def load(n, p):
#       s = importlib.util.spec_from_file_location(n, p)
#       m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
#       return m
#   gate = load('g', 'dcs/hooks/dcs_gate.py')
#   ri = load('r', 'dcs/tools/record_integrity.py')
#   pre = re.compile(gate.ENTRY_PREFIX)
#   runs = Counter()
#   for p in sorted(Path('.dcs/incidents').glob('*/214-LOG.md')):
#       stamps = []
#       for start, end, body in ri.split_log_entries(p.read_text(encoding='utf-8'), pre):
#           fl = body.splitlines()[0] if body.splitlines() else ''
#           if fl.startswith('[') and ']' in fl:
#               stamps.append(fl[:fl.index(']')+1])
#       i = 0
#       while i < len(stamps):
#           j = i
#           while j+1 < len(stamps) and stamps[j+1] == stamps[i]:
#               j += 1
#           runs[j-i+1] += 1
#           i = j+1
#   print(sorted(runs.items()))
#   "
#
# Over the 34 214-LOG.md files found on disk as of this rewrite (37
# incident directories exist; the same 3 -- check-14-hardening,
# worktree-removal-self-conflict, workflow-file-trim-grandfathered --
# carry no 214-LOG.md at all and contribute nothing to a per-file
# run-length count): run-length distribution (length: number of runs) is
# 1:322, 2:116, 3:42, 4:25, 5:11, 6:10, 7:3, 8:1, 9:1, 10:1, 11:2, 12:2,
# 75:2 -- every bucket unchanged from the first measurement except the
# low end (315 -> 322, see above), confirming this incident's own two
# headline "observed corpus defects", 11 and 75, each appearing exactly
# twice (both length-75 runs are the bare-date `[2026-07-25]` convention
# repeated across a whole file, in hot-path-budget-eol-sensitivity and
# doctrine-hot-path-trim; both length-11 runs are full timestamps, in
# status-md-enum-drift and schemas-md-trim). Every run in this corpus,
# like those two headline ones, comes from hand-typed or copy-pasted
# entries in incidents that predate this tool and this criterion's own
# effective date, so every measured directory is out of scope by
# construction and none of this measured history ever becomes a finding
# -- it says nothing, either way, about how a TOOL-written log behaves,
# which is what the sub-second measurement above establishes instead.
DUPLICATE_TIMESTAMP_THRESHOLD = 3


def log_order_findings(stamps):
    """Criterion 6's pure comparator half (mirrors the criterion-3 split
    at safety_verdict_fence_findings() / safety_fence_findings() above,
    record_integrity.py:826-839): `stamps` is an ordered list of
    (start_line, bracket_text) pairs the IO-collector below
    (collect_log_order_findings()) has already derived, in file order --
    `bracket_text` is the RAW "[...]" substring exactly as it appears on
    an entry's first line, delimiters included, never parsed for the
    duplicate half of this check. Returns a list of finding strings.

    PURE in the sense this incident's tasking requires: no filesystem, no
    git, no dcs_gate import -- so this is the function a test exercises
    directly against a synthetic stamps list, with no real 214-LOG.md on
    disk. Unlike safety_verdict_fence_findings() above, this function's
    own return type is constrained to a flat findings list (no second
    tuple element for a caller to print from), so the informational,
    never-a-finding notes below (an unparseable bracket, a naive/aware
    pair) are printed here directly -- print() touches none of the three
    things this function's purity bar names, and threading that same
    information back out through a second return channel just for the
    caller to print verbatim would be the drifting-copy risk this whole
    incident exists to avoid, not a way to prevent one.

    Two independent sub-checks, both scoped to `stamps` alone:

      (a) DUPLICATE run -- a maximal run of CONSECUTIVE stamps sharing
          the identical raw bracket_text, length >=
          DUPLICATE_TIMESTAMP_THRESHOLD, is one finding naming the
          bracket, the run's length, and its first and last line numbers.
          Consecutive on purpose, not "anywhere in the file":
          DUPLICATE_TIMESTAMP_THRESHOLD's own justification above is
          about a tool that fails to advance the clock across successive
          appends, which is a contiguous shape, and is the exact run
          definition this incident's own corpus measurement used.

      (b) OUT-OF-ORDER adjacent pair -- each bracket_text is parsed once
          (`datetime.fromisoformat` on the text between the brackets); a
          bracket that fails to parse is printed as a note (never a
          finding, never a crash) and drops out of every pairwise
          comparison it would have touched. Remaining ADJACENT pairs (in
          `stamps`' own order) are compared only when both parsed AND are
          mutually comparable -- classified EXPLICITLY by each side's own
          `tzinfo` presence before any comparison is attempted, never by
          a bare try/except swallowing the whole loop: a naive/aware pair
          is printed as a note (never a finding) and skipped, exactly
          like an unparseable bracket. A comparable pair whose SECOND
          entry's timestamp is strictly earlier than its predecessor's is
          one finding naming both line numbers; equal timestamps are
          never a finding here -- that is sub-check (a)'s job, at
          DUPLICATE_TIMESTAMP_THRESHOLD or more -- and a later-or-equal
          timestamp is the expected case, silently fine.
    """
    findings = []

    # -- (a) duplicate consecutive-run check: raw string, no parsing ----
    i = 0
    n = len(stamps)
    while i < n:
        j = i
        while j + 1 < n and stamps[j + 1][1] == stamps[i][1]:
            j += 1
        run_len = j - i + 1
        if run_len >= DUPLICATE_TIMESTAMP_THRESHOLD:
            first_line, bracket_text = stamps[i]
            last_line = stamps[j][0]
            findings.append(
                "criterion 6: FINDING: 214-LOG.md has "
                f"{run_len} consecutive entries sharing the identical "
                f"bracketed timestamp {bracket_text} (>= "
                f"DUPLICATE_TIMESTAMP_THRESHOLD={DUPLICATE_TIMESTAMP_THRESHOLD}), "
                f"lines {first_line}-{last_line}"
            )
        i = j + 1

    # -- (b) out-of-order adjacent-pair check: parsed, classified --------
    parsed = []
    for start_line, bracket_text in stamps:
        inner = bracket_text
        if inner.startswith("[") and inner.endswith("]"):
            inner = inner[1:-1]
        try:
            dt = datetime.fromisoformat(inner)
        except ValueError:
            dt = None
            print(
                f"criterion 6: 214-LOG.md:{start_line}: bracket "
                f"{bracket_text} does not parse as an ISO-8601 timestamp "
                "-- order check skipped for this entry"
            )
        parsed.append((start_line, bracket_text, dt))

    for idx in range(len(parsed) - 1):
        start_a, bracket_a, dt_a = parsed[idx]
        start_b, bracket_b, dt_b = parsed[idx + 1]
        if dt_a is None or dt_b is None:
            continue  # already printed as a note above; never a finding
        aware_a = dt_a.tzinfo is not None
        aware_b = dt_b.tzinfo is not None
        if aware_a != aware_b:
            print(
                "criterion 6: 214-LOG.md lines "
                f"{start_a} and {start_b}: bracket {bracket_a} and "
                f"{bracket_b} are not mutually comparable (one naive, one "
                "offset-aware) -- order check skipped for this pair"
            )
            continue
        try:
            out_of_order = dt_b < dt_a
        except TypeError:
            # Defensive backstop only: the explicit tzinfo check just
            # above already classifies the one comparability failure this
            # module has ever measured (naive vs aware, dcs_gate.py:220-
            # 222's own SPECIMENS on Python 3.10.0rc2). Never reached in
            # practice; never a crash if it somehow still is.
            print(
                "criterion 6: 214-LOG.md lines "
                f"{start_a} and {start_b}: bracket {bracket_a} and "
                f"{bracket_b} raised TypeError on comparison -- order "
                "check skipped for this pair"
            )
            continue
        if out_of_order:
            findings.append(
                "criterion 6: FINDING: 214-LOG.md lines "
                f"{start_a} and {start_b} are out of chronological order "
                f"-- {bracket_b} at line {start_b} is earlier than "
                f"{bracket_a} at line {start_a}"
            )

    return findings


def collect_log_order_findings(incident_dir, dcs_gate):
    """Criterion 6's IO-collector half (mirrors safety_fence_findings()
    above, record_integrity.py:826-839): date-scope the incident
    directory by its own name FIRST -- reusing _DIR_DATE_RE and
    reproducing criterion 3's three ALWAYS-PRINTED dispositions verbatim
    in shape (no parseable date -> out of scope; date on or before
    LOG_ORDER_EFFECTIVE_DATE -> out of scope; else in scope) -- never a
    silent skip. Reads the INCIDENT DIRECTORY's own leading date, never an
    individual 214-LOG.md entry's own bracketed timestamp (see
    LOG_ORDER_EFFECTIVE_DATE's own comment above for why that distinction
    is load-bearing for this incident's own still-open directory).

    Only if in scope: read 214-LOG.md, split it into entries via the
    EXISTING split_log_entries() + dcs_gate.ENTRY_PREFIX (never a
    re-derived entry regex -- dcs_gate.py is the one published grammar),
    take each entry's raw "[...]" bracket (delimiters included) off its
    own first line as `bracket_text`, and delegate the whole
    (start_line, bracket_text) list, in file order, to
    log_order_findings() -- the pure comparator above -- for the actual
    duplicate/out-of-order check. A missing 214-LOG.md is printed, not a
    finding, here: criterion 2 (artifact_set_findings()) already owns
    "214-LOG.md must exist" as part of ARTIFACT_SET, and duplicating that
    as a second, criterion-6-flavored finding would itself be a behaviour
    change to an unrelated criterion -- exactly what this incident's own
    tasking forbids."""
    findings = []
    incident_dir = Path(incident_dir)
    dir_name = incident_dir.name

    m = _DIR_DATE_RE.match(dir_name)
    if not m:
        print(
            f"criterion 6: {dir_name} carries no parseable leading "
            "YYYY-MM-DD date -- 214-LOG.md order check out of scope"
        )
        return findings
    dir_date = m.group(1)
    if dir_date <= LOG_ORDER_EFFECTIVE_DATE:
        print(
            f"criterion 6: {dir_name} dated {dir_date} is on or before "
            f"LOG_ORDER_EFFECTIVE_DATE {LOG_ORDER_EFFECTIVE_DATE} -- "
            "214-LOG.md order check out of scope"
        )
        return findings
    print(
        f"criterion 6: {dir_name} dated {dir_date} is after "
        f"LOG_ORDER_EFFECTIVE_DATE {LOG_ORDER_EFFECTIVE_DATE} -- "
        "214-LOG.md order check in scope"
    )

    log_path = incident_dir / "214-LOG.md"
    if not log_path.is_file():
        print(
            f"criterion 6: {log_path.as_posix()} is missing -- nothing "
            "for this check to read (criterion 2 already reports a "
            "missing 214-LOG.md as its own finding)"
        )
        return findings

    text = log_path.read_text(encoding="utf-8")
    entry_prefix_re = re.compile(dcs_gate.ENTRY_PREFIX)
    entries = split_log_entries(text, entry_prefix_re)

    stamps = []
    for start, _end, body in entries:
        body_lines = body.splitlines()
        first_line = body_lines[0] if body_lines else ""
        if first_line.startswith("[") and "]" in first_line:
            bracket_text = first_line[: first_line.index("]") + 1]
            stamps.append((start, bracket_text))

    return log_order_findings(stamps)


# ---------------------------------------------------------------------
# Environment checks + CLI
# ---------------------------------------------------------------------

def _git_repo_root(path):
    """The git work tree root containing `path`, or None if git itself
    is unavailable, the invocation fails, or `path` is not inside a git
    work tree at all -- main() turns any of those into exit 2, with a
    distinct message per condition."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True,
        )
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    top = proc.stdout.strip()
    return Path(top) if top else None


def _build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Mechanically re-derive six record-integrity properties "
        "of one DCS incident directory's own artifacts.",
        epilog=f"Invocation: {INVOCATION}",
    )
    parser.add_argument("incident_dir", help="the one incident directory to check")
    parser.add_argument(
        "--also-clean",
        action="append",
        default=[],
        metavar="PATH",
        help="an additional path for criterion 4's clean-tree check "
        "(repeatable)",
    )
    parser.add_argument(
        "--commit-range",
        default=None,
        metavar="RANGE",
        help="override criterion 5's default commit-message scope",
    )
    return parser


def main():
    args = _build_arg_parser().parse_args()

    try:
        dcs_gate = _load_dcs_gate()
    except Exception as exc:
        print(f"ERROR: could not import dcs_gate.py from {_DCS_GATE_PATH}: {exc}")
        sys.exit(2)

    incident_dir = Path(args.incident_dir)
    if not incident_dir.is_dir():
        print(f"ERROR: no such incident directory: {incident_dir}")
        sys.exit(2)

    if shutil.which("git") is None:
        print("ERROR: git is not available on PATH")
        sys.exit(2)

    repo_root = _git_repo_root(incident_dir)
    if repo_root is None:
        print(
            f"ERROR: {incident_dir} is not inside a git work tree "
            "(git rev-parse --show-toplevel failed)"
        )
        sys.exit(2)

    print(f"record-integrity check: {incident_dir} (repo root {repo_root})")

    findings = []
    findings.extend(citation_findings(incident_dir, repo_root, dcs_gate))
    findings.extend(artifact_set_findings(incident_dir, repo_root))
    findings.extend(safety_fence_findings(incident_dir))
    findings.extend(collect_clean_tree_findings(repo_root, incident_dir, args.also_clean))
    findings.extend(commit_message_findings(repo_root, incident_dir, args.commit_range))
    findings.extend(collect_log_order_findings(incident_dir, dcs_gate))

    if findings:
        for f in findings:
            print(f)
        sys.exit(1)

    print(
        "record-integrity check: clean -- criteria 1-6 all satisfied (or "
        "out of scope, as printed above) for this incident directory"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
