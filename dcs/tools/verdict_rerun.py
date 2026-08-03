"""Verdict-rerun checker: containment-based re-run of one `checked[]`
entry from a DCS incident's current-period Safety-officer verdict.

Why this exists (incident independence-fail-closed-and-model-floor,
202-OBJECTIVES.md criteria 4/8(a)): a `SAFETY.md` verdict fence's
`checked[]` array is a Safety Officer's own CLAIM that a command was run
and produced some observation -- nothing before this tool ever re-ran any
of those commands again, closer to close time, to confirm the claim still
holds by the time the incident is about to merge. This module is that
check, run once per incident directory, immediately before `close.md`'s
merge step (`close.md` step 1c).

What it does, in full:
  1. Reads `<incident_dir>/SAFETY.md` and finds the CURRENT period's
     verdict fence -- the LAST genuine (```-delimited, JSON-parsing)
     fenced block whose parsed body is an object carrying a `verdict`
     key (find_current_verdict()). `execute.md` step 9 only ever
     writes/appends SAFETY.md on a `pass` verdict (a `halt` verdict is
     recorded in `214-LOG.md` only), so the LAST verdict-shaped fence is
     always the most recent period's, the same "last one wins"
     convention `dcs/tools/preservation_map.py`'s `find_map()` already
     established for a sibling artifact -- one module, one instance of
     that idiom, not a re-derivation.
  2. Reads that verdict's `checked` array and SELECTS exactly one entry
     (select_entry()) by a deterministic, printed rule: the first entry,
     in array order, that (a) splits on the FIRST em dash (U+2014) into
     a non-empty (command, observation) pair, (b) is not a bare
     working-tree `git diff` (no commit-ish argument) -- `execute.md`
     step 7 has the Safety Officer verify exactly that shape of diff,
     which step 9b then commits, so by the time this tool runs at close
     time the diff no longer exists to reproduce -- and (c) tokenises as
     a real, allowlisted command, never prose describing what a human
     did ("repro of 201 path" is not a command this tool may shell out
     to). "No stable entry found" is ITSELF a finding (exit 1), never a
     silent pass -- the whole mechanism is vacuous the moment a verdict
     lists only diffs, and this is the one branch that catches that.
  3. Re-runs the selected command from the REPO ROOT, `shell=False`
     (the tokenised argv list only -- never a shell string), bounded by
     RERUN_TIMEOUT_SECONDS.
  4. Asserts the recorded observation is CONTAINED in the fresh combined
     stdout+stderr -- NEVER byte equality: pytest emits timings and
     paths that differ every run, so "5 passed" must be found as a
     substring of "5 passed in 1.23s", not compared equal to it.

Fence discovery (find_current_verdict() / _fenced_json_blocks()) mirrors
`dcs/tools/record_integrity.py`'s own `_fenced_json_blocks` REIMPLEMENTED
locally (not imported -- this module stays import-clean and
side-effect-free on its own, with no dependency on a sibling tool, same
discipline record_integrity.py itself documents for its own reasons): a
fence delimiter is recognised only when a physical line's STRIPPED
content starts with three backticks -- never a substring search anywhere
else in the line. This is load-bearing, not stylistic:
`record_integrity.py:683-692` documents the live counterexample in this
repository's own history
(`.dcs/incidents/2026-08-02-record-integrity-corrections/SAFETY.md:33`
contains the literal text "```json" inside a single-backtick INLINE-code
span, in prose about the ABSENCE of a fence in some other files) -- a
substring search would misfire on that exact line; a line-start check
does not, because that line's own stripped content does not begin with
three backticks.

Re-running arbitrary text out of an artifact is CODE EXECUTION, so this
module treats it that way: `looks_like_command()` refuses to shell out to
anything that does not tokenise (shlex, balanced quotes) to a first token
naming one of ALLOWED_COMMAND_EXES, and the actual re-run always passes
the tokenised argv list to `subprocess.run` with `shell=False` and a
bounded `timeout`. Nothing here ever executes a string through a shell.

Stdlib-only, Python 3. `main()` sits behind `if __name__ == "__main__"`,
so importing this module (as `tests/test_doctrine_integrity.py` does, via
the same `importlib.util.spec_from_file_location` idiom already used for
`dcs_gate.py`, `preservation_map.py` and `record_integrity.py`) has no
side effects.

Invocation:

    python "$HOME/.claude/dcs/tools/verdict_rerun.py" <incident_dir>

Exit codes (tests/payload_check.py's convention, matching
record_integrity.py's / preservation_map.py's):
    0   clean -- the selected checked[] entry was re-run and its
        recorded observation is contained in the fresh output
    1   one or more findings: no genuine verdict fence, no stable
        re-runnable entry found (design point (iii) -- never a silent
        pass), or the selected entry's recorded observation is NOT
        contained in the fresh output (treat as a halt through the
        existing halt-handling machinery, never a silent pass-through)
    2   environment error -- missing incident directory, git is not on
        PATH, or `<incident_dir>` is not inside a git work tree
"""
import argparse
import json
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

# The exact invocation string, quoted verbatim by dcs/workflows/close.md's
# step 1c (S3's territory) and re-read by a test (S4's own territory) --
# do not paraphrase either copy; a drifted second literal is exactly the
# class of defect this whole incident exists to close.
INVOCATION = 'python "$HOME/.claude/dcs/tools/verdict_rerun.py" <incident_dir>'

# The FIRST em dash (U+2014) is the split point between a checked[]
# entry's command half and its observation half -- schemas.md #5's own
# worked examples use exactly this separator ("pytest ... -x — 5
# passed"), never U+2013 EN DASH or a bare hyphen in separator position.
EM_DASH = "—"

# Bounded re-run timeout. A `checked[]` entry can legitimately be a full
# suite run (this repository's own test_doctrine_integrity.py takes a
# few seconds; a project's own suite could take longer) -- generous
# enough not to false-positive a slow-but-honest re-run, bounded enough
# that a genuinely hung command cannot stall a close indefinitely.
RERUN_TIMEOUT_SECONDS = 120

# The allowlist gate looks_like_command() enforces -- the same small
# vocabulary this repository's own merge-time guard already treats as
# "a regenerating command" (tests/test_doctrine_integrity.py's
# _REGEN_CMD_RE: grep/python/git/wc/find/awk/sed/jq), widened with the
# two executables schemas.md #5's OWN worked examples actually use
# (pytest, and python's cross-platform python3 spelling) plus npm/node
# for a project whose own test command is JS-based. Re-running arbitrary
# artifact text is code execution (this module's own docstring) --
# refusing anything outside this list is deliberate and conservative,
# not an oversight: a `checked[]` entry written as prose ("repro of 201
# path", "manual repro of the symptom") is refused BEFORE
# subprocess.run ever sees it, never merely left to fail at OS-exec time.
ALLOWED_COMMAND_EXES = frozenset({
    "git", "python", "python3", "pytest", "grep", "wc", "find", "sed",
    "awk", "jq", "npm", "node",
})

# Design point (ii)'s ONE named stability rule: a `git diff` with no
# commit-ish argument (a bare `HEAD`, a 7-40 hex sha, or a `..`/`...`
# range token) is a working-tree diff against the index -- exactly the
# shape `execute.md` step 7 has the Safety Officer verify, which step 9b
# then commits. By the time this tool runs at close time, that diff no
# longer exists to reproduce, so the selection rule must SKIP such an
# entry rather than let it fail the whole close. `git diff --stat <sha>`
# or `git diff <sha1>..<sha2>` DO carry a commit-ish token and are NOT
# skipped by this rule -- those genuinely can reproduce.
_GIT_DIFF_RE = re.compile(r"\bgit\s+diff\b")
_COMMIT_ISH_RE = re.compile(r"\bHEAD\b|[0-9a-fA-F]{7,40}\b|\.\.")


def _fenced_json_blocks(text):
    """Every fenced (``` / ```) code block in `text` whose body parses as
    JSON, as (open_line, parsed_object) pairs in file order. Line-based:
    a fence delimiter is recognised only when a physical line's STRIPPED
    content starts with three backticks -- never a substring search
    anywhere else in the line. Deliberately reimplemented here rather
    than imported from record_integrity.py (this module's own docstring
    explains why), but IDENTICAL in shape to that module's own
    `_fenced_json_blocks` -- see record_integrity.py:672-716 for the
    fuller rationale and the exact counterexample this line-start
    discipline exists to defeat."""
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


def find_current_verdict(text):
    """The LAST fenced JSON block in `text` that parses to a dict
    carrying a `verdict` key -- the CURRENT period's verdict.
    `execute.md` step 9 only ever writes/appends SAFETY.md on a `pass`
    verdict (a `halt` verdict is recorded in 214-LOG.md only, never
    written to SAFETY.md), so across however many periods SAFETY.md has
    accumulated, the most recently appended verdict-shaped fence is
    always the current period's -- the same "last one wins" convention
    `preservation_map.py`'s `find_map()` already established for a
    sibling artifact (a later `## 6c.` amendment's map supersedes an
    earlier one there; here, a later period's verdict supersedes an
    earlier period's). Returns (open_line, obj), or None if no
    verdict-shaped fence exists at all."""
    result = None
    for open_line, obj in _fenced_json_blocks(text):
        if isinstance(obj, dict) and "verdict" in obj:
            result = (open_line, obj)
    return result


def split_checked_entry(entry):
    """(command, observation) -- `entry` split on the FIRST em dash
    (U+2014) into a command half and an observation half, both
    whitespace-stripped. Returns (None, None) if `entry` is not a
    string, carries no em dash at all, or either half is empty after
    stripping -- callers treat that as "not a candidate", never a
    degenerate empty-observation containment check (an empty string is
    trivially "contained" in any output at all, which would be exactly
    the silent pass design point (i)/(iii) forbid)."""
    if not isinstance(entry, str) or EM_DASH not in entry:
        return None, None
    command, _, observation = entry.partition(EM_DASH)
    command = command.strip()
    observation = observation.strip()
    if not command or not observation:
        return None, None
    return command, observation


def is_working_tree_diff(command):
    """True iff `command` invokes `git diff` with no commit-ish token
    (`HEAD`, a 7-40 hex sha, or a `..`-shaped range) -- see this
    module's _GIT_DIFF_RE/_COMMIT_ISH_RE comment for the full rationale.
    A SKIP rule, not a failure: such an entry is simply never eligible
    for selection, exactly design point (ii)."""
    if not _GIT_DIFF_RE.search(command):
        return False
    return not _COMMIT_ISH_RE.search(command)


def looks_like_command(command):
    """A conservative allowlist gate: True iff `command` tokenises with
    shlex (an unbalanced quote is refused outright, never fed to a
    shell) AND its first token, lower-cased, names one of
    ALLOWED_COMMAND_EXES. See this module's docstring / the
    ALLOWED_COMMAND_EXES comment for why this exists and how the list
    was chosen."""
    try:
        tokens = shlex.split(command)
    except ValueError:
        return False
    if not tokens:
        return False
    return tokens[0].lower() in ALLOWED_COMMAND_EXES


def select_entry(checked):
    """The first schemas.md #5 `checked[]` entry, in array order, that
    is BOTH: (a) splittable into a non-degenerate (command, observation)
    pair (split_checked_entry), (b) not a working-tree git-diff entry
    (is_working_tree_diff -- the ONE stability rule this criterion names
    explicitly), and (c) a real, allowlisted command (looks_like_command),
    never prose. Returns (index, command, observation, reasons) where
    `reasons` names, in order, why every earlier (or, on total failure,
    every) entry was not selected -- the selection rule's own reasoning
    is meant to be printed, not merely asserted. Returns
    (None, None, None, reasons) if nothing in `checked` qualifies --
    design point (iii): the caller turns this into a FINDING, never a
    silent pass."""
    reasons = []
    if not isinstance(checked, list):
        return None, None, None, [f"'checked' is not a list: {checked!r}"]
    for i, entry in enumerate(checked):
        command, observation = split_checked_entry(entry)
        if command is None:
            reasons.append(
                f"[{i}] {entry!r}: no FIRST em dash (—) split into a "
                "non-empty (command, observation) pair -- not a candidate"
            )
            continue
        if is_working_tree_diff(command):
            reasons.append(
                f"[{i}] command {command!r}: a working-tree `git diff` "
                "with no commit-ish argument -- cannot reproduce once "
                "execute.md step 9b has committed it (the stability "
                "rule, design point (ii)) -- skipped"
            )
            continue
        if not looks_like_command(command):
            reasons.append(
                f"[{i}] command {command!r}: does not tokenise to an "
                f"allowlisted command ({sorted(ALLOWED_COMMAND_EXES)}) "
                "-- refusing to shell out to what looks like prose, not "
                "a command -- skipped"
            )
            continue
        reasons.append(
            f"[{i}] command {command!r}: SELECTED -- splits into a "
            "non-empty (command, observation) pair, is not a "
            "working-tree git-diff, and tokenises to an allowlisted "
            "command"
        )
        return i, command, observation, reasons
    return None, None, None, reasons


def rerun_containment_findings(text, repo_root, timeout=RERUN_TIMEOUT_SECONDS):
    """Criterion 4 in full, minus the top-level file IO (SAFETY.md is
    already read into `text` by the caller): finds the current verdict
    fence, selects an entry per select_entry()'s stability rule, re-runs
    the selected command from `repo_root` with a bounded timeout, and
    checks CONTAINMENT (never byte equality -- design point (i): pytest
    emits timings and paths that differ every run) of the recorded
    observation in the fresh combined stdout+stderr. Returns a findings
    list (empty means admissible) -- also prints the selection reasoning
    and the fresh output's length so a reader sees the tool's own
    reasoning, not just its verdict. Pure aside from the ONE
    subprocess.run of the SELECTED command -- no other filesystem or git
    access happens here."""
    findings = []
    current = find_current_verdict(text)
    if current is None:
        findings.append(
            "verdict-rerun: FINDING: no genuine verdict-shaped JSON "
            "fence (a ```-delimited block whose body parses as a JSON "
            "object carrying a 'verdict' key) found in SAFETY.md -- "
            "nothing to re-run"
        )
        return findings
    open_line, verdict_obj = current
    print(f"verdict-rerun: current verdict fence found at SAFETY.md:{open_line}")

    checked = verdict_obj.get("checked")
    if not checked:
        findings.append(
            f"verdict-rerun: FINDING: the verdict fence at SAFETY.md:"
            f"{open_line} has a missing or empty 'checked' field -- no "
            "stable, re-runnable checked[] entry found"
        )
        return findings

    idx, command, observation, reasons = select_entry(checked)
    for r in reasons:
        print(f"verdict-rerun: selection: {r}")

    if command is None:
        findings.append(
            "verdict-rerun: FINDING: no stable, re-runnable checked[] "
            f"entry found in the verdict fence at SAFETY.md:{open_line} "
            "-- every entry was either unparseable, a working-tree "
            "git-diff entry, or not an allowlisted command; see the "
            "selection reasoning printed above"
        )
        return findings

    print(f"verdict-rerun: selected checked[{idx}]: command={command!r}")
    print(f"verdict-rerun: recorded observation: {observation!r}")

    tokens = shlex.split(command)
    timed_out = False
    try:
        proc = subprocess.run(
            tokens, cwd=str(repo_root), capture_output=True, text=True,
            timeout=timeout, encoding="utf-8", errors="replace",
        )
        fresh_output = (proc.stdout or "") + (proc.stderr or "")
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        fresh_output = (
            (exc.stdout or "") if isinstance(exc.stdout, str) else ""
        ) + ((exc.stderr or "") if isinstance(exc.stderr, str) else "")
    except OSError as exc:
        findings.append(
            f"verdict-rerun: FINDING: checked[{idx}] command {command!r} "
            f"could not be run from {repo_root}: {exc}"
        )
        return findings

    if timed_out:
        findings.append(
            f"verdict-rerun: FINDING: checked[{idx}] command {command!r} "
            f"did not complete within {timeout}s -- cannot confirm the "
            "recorded observation reproduces"
        )
        return findings

    print(f"verdict-rerun: fresh combined stdout+stderr ({len(fresh_output)} chars)")

    if observation not in fresh_output:
        findings.append(
            f"verdict-rerun: FINDING: checked[{idx}] command {command!r} "
            f"re-ran, but the recorded observation {observation!r} is "
            "NOT contained in the fresh combined stdout+stderr -- treat "
            "as a halt through the existing halt-handling machinery "
            "(close.md step 1's PARK / AskUserQuestion refusal), never a "
            "silent pass-through"
        )
        return findings

    print(
        f"verdict-rerun: recorded observation {observation!r} IS "
        f"contained in the fresh output -- checked[{idx}] reproduces"
    )
    return findings


def _git_repo_root(path):
    """The git work tree root containing `path`, or None if git itself
    is unavailable, the invocation fails, or `path` is not inside a git
    work tree at all -- main() turns any of those into exit 2, with a
    distinct message per condition. Mirrors record_integrity.py's own
    `_git_repo_root` (not imported, per this module's own
    import-clean/side-effect-free discipline)."""
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
        description="Re-run one containment-verifiable checked[] entry "
        "from a DCS incident's current-period Safety-officer verdict, "
        "immediately before close.md's merge step.",
        epilog=(
            f"Invocation: {INVOCATION}\n\n"
            "Exit codes:\n"
            "  0   clean -- the selected checked[] entry was re-run and "
            "its recorded\n"
            "      observation is contained in the fresh output\n"
            "  1   one or more findings -- no genuine verdict fence, no "
            "stable\n"
            "      re-runnable entry found, or the selected entry's "
            "recorded\n"
            "      observation is NOT contained in the fresh output\n"
            "  2   environment error -- missing incident directory, git "
            "is not on\n"
            "      PATH, or <incident_dir> is not inside a git work tree"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("incident_dir", help="the one incident directory to check")
    return parser


def main():
    # A checked[] entry is free-form text a Safety Officer wrote and may
    # legitimately carry any Unicode character (an arrow, an em dash, a
    # quote) -- this tool prints that text verbatim (the selection
    # reasoning, the command, the recorded observation) so a reader can
    # see its own logic, not just its verdict. On a Windows console
    # whose active codepage is not UTF-8 (observed: cp1251), a bare
    # print() of such a character raises UnicodeEncodeError and crashes
    # the tool outright -- reconfigure stdout/stderr to replace an
    # unencodable character with '?' rather than crash. `errors`-only
    # (never forcing `encoding=`) leaves whatever real encoding the
    # environment already chose untouched. Guarded: a stream that
    # predates Python 3.7's TextIOWrapper.reconfigure (e.g. one already
    # replaced by a test harness) simply keeps its current behaviour.
    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(errors="replace")
        except AttributeError:
            pass

    args = _build_arg_parser().parse_args()

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

    print(f"verdict-rerun check: {incident_dir} (repo root {repo_root})")

    safety_path = incident_dir / "SAFETY.md"
    if not safety_path.is_file():
        print(f"verdict-rerun: FINDING: {safety_path.as_posix()} is missing")
        sys.exit(1)
    text = safety_path.read_text(encoding="utf-8")

    findings = rerun_containment_findings(text, repo_root)

    if findings:
        for f in findings:
            print(f)
        sys.exit(1)

    print(
        "verdict-rerun: clean -- the selected checked[] entry re-ran and "
        "its recorded observation is contained in the fresh output"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
