#!/usr/bin/env python3
"""Canonical, timestamp-honest appender for one DCS incident's own
214-LOG.md -- the only programmatic writer of phase-transition entries
this package ships (incident log-append-helper, 202-OBJECTIVES.md
criteria 1-3).

Why this exists: every 214-LOG.md entry across the incident portfolio
was, until this tool, hand-typed by whichever session happened to be at
a phase transition. Two defect classes followed, both confirmed on disk
at this incident's intake (201-BRIEF.md): backfilled batches sharing one
identical, stale timestamp, and at least five distinct timestamp-bracket
shapes in use portfolio-wide, sometimes mixed inside a single incident's
own log. dcs_gate.py's entry grammar (ENTRY_PREFIX) is content-agnostic
inside the brackets, so none of this defeats the mechanical halt-ceiling
counter -- it defeats only auditability, which is exactly the gap this
tool closes: one writer, one real-clock timestamp source, one place
operator identity is recorded, or the append is refused outright.

IMPORT, NEVER RE-DERIVE (criterion 2). This module imports
dcs/hooks/dcs_gate.py dynamically, via the same
importlib.util.spec_from_file_location idiom record_integrity.py
already uses (record_integrity.py:152-179) -- never a package-relative
`import`, since this file must run standalone from either the repo or
the installed copy, with no `dcs` package on sys.path either way. Only
four names are ever used from the imported module: render_entry() (the
one place an entry's "[<timestamp>] <body>" shape is assembled),
sentinel_of() (the one classifier of 'halt'/'pass'/'stamp'/None),
find_project_root(), and resolve_incident_dir(). No regex, no f-string
entry template, and no literal '.dcs/incidents' path is typed anywhere
in this file -- a second, drifting copy of dcs_gate.py's grammar is
exactly the defect class this incident's own reuse pattern (and
record_integrity.py before it) exists to prevent. A failed import is a
hard error, printed to stderr, exit 2 -- never a fallback to a locally
re-derived regex.

CONTAINMENT (command point 2 ruling; both probes made explicit
requirements). (1) A slug carrying a path separator ('/' or '\\') or a
literal '..' path component is rejected before ANY resolution is
attempted -- never sanitized and continued. Also rejected, for the same
underlying reason, are an empty slug and a literal '.': verified that
Path(base) / '' and Path(base) / '.' both collapse onto `base` itself,
so resolve_incident_dir()'s own `exact = base / slug` would silently
resolve to the incidents directory ITSELF rather than any single
incident -- the tasking names only '..' explicitly, but the same
silent-collapse hazard applies to these two related component values,
so this module closes all three the same way, before any filesystem
call is made. (2) `append` refuses (non-zero exit) when the resolved
incident directory, or its 214-LOG.md, does not already exist -- this
tool appends to an existing artifact, it never creates one (`new.md`
alone creates 214-LOG.md, from the template, at incident open).

PINNED FORMAT (tasking D1/D2 -- not this file's to vary; a variance is
a deviation, not a judgement call). The timestamp is always
`datetime.now().astimezone().isoformat(timespec="microseconds")` --
full precision, at whatever sub-second resolution the platform's clock
actually returns, never truncated or rounded to whole seconds --
computed fresh at call time and passed EXPLICITLY as render_entry()'s
second argument (that function's own default is naive and offset-less,
dcs_gate.py:166-168 -- never relied on here). The explicit
timespec="microseconds" argument (not bare .isoformat()) matters
because Python's own default timespec, "auto", OMITS the
fractional-seconds field entirely on the rare call where microsecond
lands on exactly 0 -- a real, if rare, flake against a sibling test
(tests/test_dcs_log.py) that asserts a fixed, six-digit fractional
field on every appended bracket; timespec="microseconds" makes that
field unconditionally present, zero-padded to six digits, with no
change to the actual precision recorded -- never a rounding, never an
invented digit. No flag, environment variable, or config file can
override it (criterion 1) -- this module reads no such input
anywhere; grep this file for 'environ' or 'getenv' and find nothing.
The rendered line is
`render_entry(body, timestamp) + OPERATOR_SEP + operator`: the operator
identity is always appended LAST, after the whole body, via the fixed
literal OPERATOR_SEP, and never sits between the bracket and a sentinel
token -- any other placement would defeat sentinel_of()
(dcs_gate.py:140-155), which classifies a line from its own start.

SELF-VALIDATION BEFORE WRITE. After rendering the complete line (body,
any sentinel prefix, and the operator suffix), this module calls the
imported sentinel_of() on that exact finished line and refuses to
append unless the classification equals what was requested
(--sentinel's kind, or None if omitted). Because sentinel_of()'s
patterns are anchored only at the line's start (re.match, no trailing
`$`), the appended OPERATOR_SEP suffix never changes the classification
-- this check genuinely validates the same bytes that will land in the
file. `--sentinel stamp` therefore requires the body to LEAD with 8 or
more hex characters (STAMP_RE, dcs_gate.py:109) -- a feature: it
enforces plan.md step 8's own stamp shape, not an accidental
restriction. Free text that happens to classify as a sentinel without
--sentinel being requested is refused, not silently written.

NEWLINE SAFETY. If 214-LOG.md's existing bytes do not already end in a
newline, one is prepended before the new entry -- the exact reasoning
dcs_gate.py's own rollback_act() already documents
(dcs_gate.py:188-200): without it, the new entry glues onto the tail of
whatever entry is currently last, and the glued line classifies as THAT
entry's kind, never its own. All file I/O here is binary, UTF-8, no BOM
(CLAUDE.md's Set-Content/Out-File BOM rule) -- never a text-mode open
that could translate a newline or smuggle one in.

FAIL CLOSED -- a deliberate, argued exception to this project's default
(CLAUDE.md: "every hook fails open on error"). Every failure path in
this module exits non-zero with a stderr message; there is no path that
swallows an error and proceeds anyway. This is not the situation
CLAUDE.md's default is written for: that default protects a PreToolUse
HOOK sitting silently in every edit's path, where failing closed would
brick an entire session over a bug unrelated to the edit at hand. This
module is not that -- it is invoked directly, by an operator or agent
already standing at the point of wanting one specific line appended to
a permanent, append-only historical record, and "failing open" has no
coherent meaning here: there is no safe default action other than
writing the line correctly or not writing it at all. A silently wrong,
silently skipped, or silently re-derived-grammar append would corrupt
or thin the very audit trail this incident exists to make honest --
worse than a refusal. The precedent for this kind of documented
exception already ships in the package: dcs_gate.py's own .dcs/CLOSED
zombie rule (dcs_gate.py:66-74, 627-640) fails CLOSED for the same
class of reason -- by the time that rule fires, the harm of silently
permitting the edit outweighs the harm of blocking it, so that module
deliberately inverts its own general fail-open default for that one
path. This module inverts it for all of its paths, because appending a
false or malformed audit line is the harm this whole incident exists to
stop, not an edge case of it.

CONCURRENCY -- the read-then-write critical section is now one atomic
unit, cross-process. Until this fix, _append_entry() read 214-LOG.md's
existing bytes to compute the NEWLINE SAFETY prefix, then opened the
file "ab" to append, as two UNLOCKED steps -- and on Windows "ab" is a
seek-to-end-then-write emulation, not a true atomic append. Two
concurrent invocations racing that pair could both read the same
"existing" bytes and both append based on it, interleaving writes and
landing fewer distinct entries than invocations made -- proven live,
8 concurrent invocations against one fixture log landed only 6 entries,
every process exiting 0 with empty stderr. That was the one genuine
hole in the FAIL CLOSED claim above: not a path that swallowed a raised
error, but a path with no error at all around a non-atomic critical
section -- data silently lost with nothing to catch it. Fixed by
_append_entry() acquiring an exclusive, cross-process lock BEFORE the
read and releasing it only after the write (see _append_entry() and
_acquire_lock() below for the exact mechanism and the bounded-timeout
refusal). That refusal path is itself FAIL CLOSED, not an exception to
it: a bounded wait-then-refuse -- exit 1, a stderr message naming the
lock file, nothing written -- is an honest, attributable failure; only
an unbounded wait or a silent proceed-anyway would violate this
module's own guarantee. One accepted, documented limitation: a lock
holder killed hard enough to skip its `finally` (SIGKILL, power loss --
ordinary exceptions and this module's own _fail()/sys.exit() do NOT
skip it) leaves a stale lock file behind, and every later caller then
waits the full timeout before refusing -- a hung append, not a silent
one, and not something this module auto-clears, since guessing a
lock's "safe to steal" age is its own race.

Stdlib-only, Python 3. main() sits behind `if __name__ == "__main__"`,
so importing this module has no side effects.

Invocation:

    python "$HOME/.claude/dcs/tools/dcs_log.py" append <slug> --by
        <operator> [--sentinel {halt,pass,stamp}] "<text>"

Exit codes:
    0   the entry was appended.
    1   the request was refused: an unsafe slug, a missing or empty
        --by, a slug that does not resolve to a unique incident
        directory, a resolved incident directory with no 214-LOG.md, a
        rendered entry whose sentinel_of() classification does not
        match the requested --sentinel (or None, if omitted), or the
        cross-process append lock could not be acquired within the
        bounded timeout (see FAIL CLOSED, CONCURRENCY).
    2   environment error: dcs_gate.py could not be imported, or no DCS
        project (a directory with .dcs/) was found above the current
        working directory.
"""
import argparse
import importlib.util
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# The exact invocation string -- pinned by this incident's IAP and S1's
# own tasking, quoted verbatim by S3's template/forms.md work and read
# by S4's tests. Do not paraphrase; a drifted second literal is exactly
# the class of defect this whole incident exists to close.
INVOCATION = 'python "$HOME/.claude/dcs/tools/dcs_log.py" append <slug> --by <operator> "<text>"'

# The fixed literal that always separates a rendered entry's body from
# the operator identity -- appended LAST, after the whole body,
# never between the bracket and a sentinel token (see module docstring,
# PINNED FORMAT).
OPERATOR_SEP = " -- op: "

# The three sentinel tokens dcs_gate.py's sentinel_of() recognizes,
# keyed by the --sentinel CLI value that selects each one. Values are
# quoted byte-for-byte from dcs_gate.py's own HALT_RE/PASS_RE/STAMP_RE
# (dcs_gate.py:107-109), never retyped from memory.
SENTINELS = {"halt": "SAFETY-HALT:", "pass": "SAFETY-PASS:", "stamp": "IAP-APPROVED:"}

# The canonical format, in prose, published for verbatim quotation --
# exactly as dcs_gate.py's own GRAMMAR_LINE is (dcs_gate.py:128-137).
# ONE ASCII line, no backticks.
FORMAT_LINE = (
    "One line: a bracketed real-clock timestamp, then the body -- an "
    "optional sentinel token (SAFETY-HALT:, SAFETY-PASS:, or "
    "IAP-APPROVED:) immediately after the bracket, followed by free "
    "text -- then the operator identity, appended last via the fixed "
    "separator ' -- op: ', which never sits between the bracket and "
    "the sentinel."
)

# Where dcs_gate.py lives, relative to THIS file, in both the repo
# layout (dcs/tools/dcs_log.py + dcs/hooks/dcs_gate.py, siblings under
# dcs/) and the installed layout (~/.claude/dcs/tools/... +
# ~/.claude/dcs/hooks/...) -- the same relative shape either way, so
# one path expression covers both without knowing which copy is
# running. Copied from record_integrity.py:157's own _DCS_GATE_PATH,
# which lives in this same directory.
_DCS_GATE_PATH = Path(__file__).resolve().parent.parent / "hooks" / "dcs_gate.py"


def _load_dcs_gate():
    """Import dcs_gate.py from _DCS_GATE_PATH via the
    spec_from_file_location idiom record_integrity.py already uses
    (record_integrity.py:164-179) -- never a package-relative `import`,
    since this file must run standalone from either the repo or the
    installed copy, with no `dcs` package on sys.path either way.
    Raises on any failure; main() is the only caller, and turns that
    into exit 2 with a clear stderr message rather than falling back to
    a locally re-derived regex."""
    spec = importlib.util.spec_from_file_location("dcs_gate", str(_DCS_GATE_PATH))
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot build an import spec for {_DCS_GATE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _fail(message, code):
    """The one place this module ends a run early: a stderr message and
    a non-zero exit (FAIL CLOSED, see module docstring). Every failure
    path in this tool goes through here -- there is no silent skip and
    no fallback to locally re-derived logic anywhere in this file."""
    print(f"dcs_log.py: {message}", file=sys.stderr)
    sys.exit(code)


def _validate_slug(slug):
    """CONTAINMENT probe 1: True iff `slug` is safe to resolve at all.
    Rejects any slug carrying a path separator ('/' or '\\') -- the
    tasking's own wording -- and, since a separator's absence means the
    whole string is necessarily ONE path component, rejects that one
    component being '..' (the tasking's named case), or '.' or '' (the
    same silent-collapse hazard: Path(base) / '' and Path(base) / '.'
    both resolve to `base` itself, verified, which would otherwise let
    resolve_incident_dir() silently return the whole incidents
    directory instead of refusing). Pure -- no filesystem access, so
    this can run, and refuse, before ANY resolution is attempted."""
    if "/" in slug or "\\" in slug:
        return False
    if slug in ("", ".", ".."):
        return False
    return True


def _compose_body(text, sentinel_kind):
    """The entry body: `text` as given, or -- iff --sentinel <kind> was
    supplied -- SENTINELS[kind] + ' ' prepended to it. The operator
    identity is never part of this: it is appended after the WHOLE
    rendered entry (see main()), via OPERATOR_SEP, so it can never land
    between the bracket and a sentinel token -- the one placement that
    would defeat dcs_gate.sentinel_of()."""
    if sentinel_kind is None:
        return text
    return SENTINELS[sentinel_kind] + " " + text


# Cross-process serialization for _append_entry()'s critical section (see
# module docstring, CONCURRENCY). A portable sidecar lock file, not
# msvcrt.locking(): msvcrt is Windows-only stdlib, and every other tool
# in dcs/ -- and this package's own install.sh -- is platform-neutral,
# so a msvcrt-only lock would simply not exist as a module on POSIX.
# os.O_CREAT | os.O_EXCL is an atomic create-or-fail on both Windows and
# POSIX; the lock file's mere presence on disk IS the lock, so nothing
# about the fd needs to stay open once it is created.
_LOCK_TIMEOUT_SECONDS = 5.0
_LOCK_RETRY_INITIAL_SECONDS = 0.02
_LOCK_RETRY_MAX_SECONDS = 0.25


def _acquire_lock(lock_path, timeout_seconds=_LOCK_TIMEOUT_SECONDS):
    """Create `lock_path` exclusively (os.O_CREAT | os.O_EXCL), retrying
    with a short exponential backoff (_LOCK_RETRY_INITIAL_SECONDS up to
    _LOCK_RETRY_MAX_SECONDS between attempts) until either it succeeds --
    returns the open fd, which the caller closes immediately, since the
    file's existence on disk is what holds the lock, not the fd -- or
    `timeout_seconds` elapses without success, in which case this
    returns None and the caller refuses (FAIL CLOSED: a bounded
    wait-then-refuse, never an unbounded wait). Only FileExistsError
    (errno EEXIST -- another writer currently holds the lock) is
    retried; any other OSError (e.g. an unwritable directory) propagates
    immediately, since retrying that for the full timeout would only
    delay an unrelated failure, never a real lock holder."""
    deadline = time.monotonic() + timeout_seconds
    delay = _LOCK_RETRY_INITIAL_SECONDS
    while True:
        try:
            return os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return None
            time.sleep(min(delay, remaining))
            delay = min(delay * 2, _LOCK_RETRY_MAX_SECONDS)


def _append_entry(log_path, rendered_line):
    """Append `rendered_line` (no trailing newline of its own) to
    `log_path`, guaranteeing it starts at column zero even if the
    file's existing bytes do not currently end in a newline --
    dcs_gate.py's own rollback_act() reasoning, dcs_gate.py:188-200: an
    entry glued onto the tail of the previous line classifies as THAT
    line's kind, never its own. Binary I/O throughout, UTF-8, no BOM,
    '\\n' only -- never PowerShell Set-Content/Out-File, never a
    text-mode newline translation that could smuggle one in.

    CONCURRENCY (module docstring has the full argument): the read of
    `log_path`'s existing bytes (to compute the newline prefix) and the
    append write are ONE atomic unit, serialized cross-process by an
    exclusive sidecar lock file (`<log_path>.lock`, via _acquire_lock())
    held across both steps -- acquired before the read, released
    (fd already closed; the lock file itself removed) only after the
    write completes or fails. Without this, two concurrent callers could
    both read the same "existing" bytes and both open "ab" -- on Windows
    "ab" is a seek-to-end-then-write emulation, not a true atomic append
    -- and interleave, silently landing fewer entries than invocations
    (proven live: 8 concurrent invocations landed only 6 entries, every
    process exiting 0 with empty stderr). Failing to acquire the lock
    within _LOCK_TIMEOUT_SECONDS is itself a FAIL CLOSED refusal: exit 1,
    a stderr message naming the lock file, and nothing written."""
    lock_path = log_path.with_name(log_path.name + ".lock")
    lock_fd = _acquire_lock(lock_path)
    if lock_fd is None:
        _fail(
            f"REFUSED: could not acquire the append lock ({lock_path}) "
            f"within {_LOCK_TIMEOUT_SECONDS:g}s -- another writer appears "
            "to hold it; refusing to append rather than race the "
            "read-then-write critical section (see module docstring, "
            "CONCURRENCY). If no writer process is actually running, "
            "this lock is stale -- delete it and retry.",
            1,
        )
    os.close(lock_fd)
    try:
        try:
            existing = log_path.read_bytes()
        except OSError as exc:
            _fail(f"REFUSED: could not read {log_path} to append: {exc}", 1)
        prefix = b"" if (not existing or existing.endswith(b"\n")) else b"\n"
        try:
            with open(log_path, "ab") as f:
                f.write(prefix + rendered_line.encode("utf-8") + b"\n")
        except OSError as exc:
            _fail(f"REFUSED: could not write to {log_path}: {exc}", 1)
    finally:
        try:
            os.remove(str(lock_path))
        except OSError:
            pass


def _build_arg_parser():
    parser = argparse.ArgumentParser(
        prog="dcs_log.py",
        description="Canonical, timestamp-honest appender for one DCS "
        "incident's 214-LOG.md.",
        epilog=(
            f"Invocation: {INVOCATION}\n\n"
            f"Format: {FORMAT_LINE}\n\n"
            "Exit codes:\n"
            "  0   the entry was appended\n"
            "  1   the request was refused -- an unsafe slug, a "
            "missing or empty\n"
            "      --by, a slug that does not resolve to a unique "
            "incident directory,\n"
            "      a resolved incident directory with no 214-LOG.md, "
            "or a rendered\n"
            "      entry whose sentinel_of() classification does not "
            "match --sentinel,\n"
            "      or the cross-process append lock could not be "
            "acquired within the\n"
            "      bounded timeout\n"
            "  2   environment error -- dcs_gate.py could not be "
            "imported, or no DCS\n"
            "      project (.dcs/) was found above the current "
            "directory"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    append_parser = subparsers.add_parser(
        "append", help="append one entry to <slug>'s 214-LOG.md"
    )
    append_parser.add_argument(
        "slug",
        help="the incident directory's slug, or its exact directory "
        "name, under .dcs/incidents/ -- never a path; no separator and "
        "no '..' component is accepted",
    )
    append_parser.add_argument(
        "--by",
        required=True,
        metavar="OPERATOR",
        help="the operator identity to record -- mandatory, must be "
        "non-empty after stripping whitespace",
    )
    append_parser.add_argument(
        "--sentinel",
        choices=sorted(SENTINELS),
        default=None,
        help="prepend the matching sentinel token to the body "
        "(SENTINELS[kind] + ' '); omit for an ordinary entry",
    )
    append_parser.add_argument("text", help="the entry body's free text")
    return parser


def main():
    args = _build_arg_parser().parse_args()

    # CONTAINMENT probe 1 -- rejected before any resolution is
    # attempted, and before --by is even inspected: never
    # sanitized-and-continued.
    if not _validate_slug(args.slug):
        _fail(
            f"REFUSED: slug {args.slug!r} contains a path separator or "
            "is a '..' (or '.', or empty) path component -- rejected "
            "before any resolution is attempted",
            1,
        )

    operator = (args.by or "").strip()
    if not operator:
        _fail(
            "REFUSED: --by must be a non-empty operator identity "
            "(after stripping whitespace) -- refusing to append an "
            "entry with no attributable operator",
            1,
        )

    try:
        dcs_gate = _load_dcs_gate()
    except Exception as exc:
        _fail(f"ERROR: could not import dcs_gate.py from {_DCS_GATE_PATH}: {exc}", 2)
        return  # unreachable (_fail exits), keeps linters happy

    # NB: a relative target ('.') deliberately takes find_project_root's
    # env/cwd branch (dcs_gate.py:296-309), which walks from cwd
    # INCLUSIVE -- the same call shape dcs_gate.py's own main() uses for
    # its SendMessage handling (dcs_gate.py:601).
    project_root = dcs_gate.find_project_root(".", os.getcwd())
    if project_root is None:
        _fail(
            "ERROR: no DCS project found -- no .dcs/ directory above "
            f"the current working directory ({os.getcwd()})",
            2,
        )
        return  # unreachable

    incident_dir = dcs_gate.resolve_incident_dir(project_root, args.slug)
    if incident_dir is None:
        _fail(
            f"REFUSED: no unique incident directory found for slug "
            f"{args.slug!r} under {project_root} -- dcs_log.py never "
            "creates one",
            1,
        )
        return  # unreachable

    # CONTAINMENT probe 2, second half: refuse if 214-LOG.md itself does
    # not already exist. There is no other candidate write target
    # anywhere in this file -- no path argument is ever accepted, and
    # this is the ONLY expression that builds a target path, so "the
    # resolved target is exactly this file" holds by construction.
    log_path = incident_dir / "214-LOG.md"
    if not log_path.is_file():
        _fail(
            f"REFUSED: {log_path} does not already exist -- dcs_log.py "
            "appends to an existing 214-LOG.md, it never creates one",
            1,
        )
        return  # unreachable

    # PINNED FORMAT: real-clock, offset-aware, full (sub-second)
    # precision -- never truncated or rounded to whole seconds --
    # passed EXPLICITLY -- render_entry()'s own default is naive and
    # offset-less and is never relied on here. No flag, environment
    # variable, or config value is consulted for this value.
    # timespec="microseconds" (not bare .isoformat()) keeps the
    # fractional field unconditionally present at a fixed six digits --
    # Python's default "auto" timespec silently omits it when
    # microsecond == 0 (see module docstring, PINNED FORMAT).
    timestamp = datetime.now().astimezone().isoformat(timespec="microseconds")
    body = _compose_body(args.text, args.sentinel)
    rendered = dcs_gate.render_entry(body, timestamp) + OPERATOR_SEP + operator

    # SELF-VALIDATION BEFORE WRITE: classify the exact bytes that will
    # be appended, not merely the body -- OPERATOR_SEP's suffix cannot
    # change this, since sentinel_of()'s patterns anchor only at the
    # line's start.
    classification = dcs_gate.sentinel_of(rendered)
    if classification != args.sentinel:
        if args.sentinel is None:
            _fail(
                "REFUSED: no --sentinel was requested, but the "
                f"rendered entry classifies as {classification!r} "
                "under dcs_gate.sentinel_of() -- free text that "
                "happens to open with a sentinel-shaped token must be "
                "passed through --sentinel explicitly, or reworded",
                1,
            )
        hint = (
            " -- a 'stamp' entry's body must LEAD with 8 or more hex "
            "characters immediately after 'IAP-APPROVED: ' "
            "(dcs_gate.STAMP_RE)"
            if args.sentinel == "stamp"
            else ""
        )
        _fail(
            f"REFUSED: --sentinel {args.sentinel} was requested, but "
            f"the rendered entry classifies as {classification!r} "
            f"under dcs_gate.sentinel_of() instead{hint}",
            1,
        )
        return  # unreachable

    _append_entry(log_path, rendered)
    print(f"dcs_log.py: appended to {log_path}: {rendered}")
    sys.exit(0)


if __name__ == "__main__":
    main()
