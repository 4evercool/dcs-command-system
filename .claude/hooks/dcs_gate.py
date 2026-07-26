#!/usr/bin/env python3
"""PreToolUse hook: mechanical enforcement of the DCS IAP-approval gate.

DCS ("Development Command System") adapts the ICS Planning P to software
work: no source edit happens until an Incident Action Plan (IAP) exists and
has been approved by the Owner. Doctrine says the rule is "mechanical, not
behavioral" (references/doctrine.md, principle 11) -- this hook is that
mechanism, speaking the standard PreToolUse stdin-JSON /
stdout-JSON deny pattern.

Fires on PreToolUse for Edit|Write|NotebookEdit (wired by /dcs-init into the
project's .claude/settings.json, appended alongside any existing
PreToolUse hooks -- never replacing them). Logic:

1. Resolve the project root FROM THE TARGET FILE'S OWN PATH (v0.3), not
   the session's cwd or CLAUDE_PROJECT_DIR -- see find_project_root()'s
   docstring for why. No root found -> allow (not a DCS-onboarded tree).
2. `.dcs/CLOSED` present in that root -> deny ALL guarded edits
   unconditionally (the zombie rule, v0.3) -- see the deny message and
   find_project_root() callers for rationale. This check runs before
   anything else, including the .dcs/** bookkeeping exemption below.
3. No active incident (<project>/.dcs/ACTIVE absent) -> allow. Zero
   overhead for projects/sessions doing non-DCS work.
4. Active incident, type=5 or phase=closed -> allow. Type 5's express lane
   never sets ACTIVE in the first place; a "closed" phase label (defensive
   handling -- /dcs-close normally deletes ACTIVE outright rather than
   transitioning through a closed state) has nothing left to enforce.
5. Active incident, phase=execution -> the gate is open IF the approval
   marker (.dcs/incidents/<dir>/IAP-APPROVED) still matches the current
   IAP.md's content, modulo line-ending representation (not its exact
   bytes -- see approval_digests()). ACTIVE's first field resolves to the
   incident dir by exact name, or tolerantly to the UNIQUE dir ending in
   "-<slug>" (the date-prefixed form; ambiguity denies -- see
   resolve_incident_dir). Editing IAP.md after approval changes its
   content and silently revokes the marker -- this is deliberate: an
   edited plan is no longer the plan the Owner approved (deviation
   doctrine, principle 8).
6. Active incident, phase=planning (pre-approval) -> only paths matching
   config.json's unguarded_paths (scratch/docs/.dcs/** by default) may be
   touched. Everything else is denied until /dcs-plan produces an approved
   IAP.
7. Active incident, phase=execution, valid marker -> before allowing, also
   check the halt ceiling, UNLESS the target path is itself exempt under
   config.json (unguarded, or simply not in the guarded set -- the same
   two checks the planning branch already applies below, so one rule
   governs both surfaces). Otherwise: count the sentinel lines
   sentinel_of() classifies 'halt' in the incident's 214-LOG.md since the
   last reset anchor (the last line sentinel_of() classifies 'pass', or
   the last it classifies 'stamp' whose captured hex prefix case-
   insensitively prefixes the incident's own IAP-APPROVED marker -- the
   marker is the authority, the log line only fixes its position in time)
   and compare against config.json's `esg.max_halts_per_attempt` (default
   3, validated: only a plain positive int is accepted, see max_halts()).
   At or above the ceiling -> deny, even though the hash marker is valid.
   Sentinels are recognized only through this module's own published
   grammar -- ENTRY_PREFIX and GRAMMAR_LINE, one definition, no second
   unpublished structural requirement layered on top (see sentinel_of()
   and halt_cycles()). This whole path (the config-exemption check, the
   count, the threshold read, the comparison, and the deny() call itself)
   lives in its OWN inner try/except that degrades to "no ceiling" on any
   failure -- see halt_cycles()'s and max_halts()'s docstrings for why
   that guard must not be merely present but total.
8. Any internal error -> fail OPEN (exit 0). Never brick the session over
   a hook bug.

No escape-hatch environment variable --
the one sanctioned emergency release is the Owner deleting .dcs/ACTIVE, an
explicit, visible act (doctrine principle 11). The `.dcs/CLOSED` zombie
rule (step 2) is the one deliberate exception to "fail open when in
doubt": it fails CLOSED, because by the time CLOSED exists the incident's
work has already been merged into main (close.md's anti-rot core, v0.3) --
any edit made here from this point on is guaranteed-lost work in a
worktree that's just waiting to be `git worktree remove`d, not a case
where under-enforcing is the safe default.
"""
import fnmatch
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_GUARDED = ["**/*"]
DEFAULT_UNGUARDED = [".dcs/**", "tasks/**", "*.md", ".claude/**"]
DEFAULT_MAX_HALTS = 3

# Sentinel grammar -- ONE published definition (halt-loop-unbounded period
# 1 revision 3; revision 2's fatal defect was exactly this existing in TWO
# places, an "optional timestamp" prose next to code that required one). A
# 214-LOG.md entry begins ONLY at column zero with a MANDATORY bracketed
# timestamp: ENTRY_PREFIX is that one definition, and HALT_RE / PASS_RE /
# STAMP_RE are built from it by concatenation, never re-typed. A line
# lacking the bracketed prefix at column zero is a continuation of the
# entry above it and never a sentinel, even if it happens to open with a
# sentinel-shaped token (a multi-line SAFETY-HALT: summary quoting a reset
# token in its own body must neither count nor reset) -- and an indented
# quotation of a WHOLE prior entry, its own timestamp included, is
# likewise never a sentinel, because indentation alone moves it off column
# zero. There is no second, unpublished structural requirement on top of
# these three patterns: GRAMMAR_LINE states the same boundary rule in
# prose, for the one prose surface that needs it, instead of a second
# author reconstructing it from these patterns by eye. Case-sensitive by
# construction (no re.I flag).
ENTRY_PREFIX = r"^\[[^\]]*\]\s+"
HALT_RE = re.compile(ENTRY_PREFIX + r"SAFETY-HALT:")
PASS_RE = re.compile(ENTRY_PREFIX + r"SAFETY-PASS:")
STAMP_RE = re.compile(ENTRY_PREFIX + r"IAP-APPROVED:\s*([0-9a-fA-F]{8,})")

# Published POSITIONAL form of the stamp sentinel (halt-loop-unbounded
# period 1 revision 3 amendment, command point 3): entry boundary plus the
# IAP-APPROVED: token, with NO requirement on the argument that follows.
# STAMP_RE remains the ONLY authority halt_cycles() and sentinel_of() use
# to recognize a reset anchor -- this pattern never anchors anything. Its
# sole purpose is validating PROSE that quotes the stamp shape with a
# placeholder where a real hex digest would sit (e.g.
# dcs/workflows/plan.md's step-8 template line): such a line is correct
# AT THE BOUNDARY (STAMP_ENTRY_RE matches it) while correctly failing to
# anchor (STAMP_RE does not), and that distinction is exactly what a
# second author needs a published, positional check for, instead of
# reconstructing "boundary minus hex requirement" by eye. Built by
# concatenation from the SAME ENTRY_PREFIX as the other three patterns, so
# every line STAMP_RE matches is, by construction, also matched by this
# one -- there is no way to compose the two patterns that diverges.
STAMP_ENTRY_RE = re.compile(ENTRY_PREFIX + r"IAP-APPROVED:")

# The one prose statement of the boundary rule ENTRY_PREFIX encodes,
# published so nothing else -- doctrine, a docstring, a deny message --
# ever has to paraphrase it and risk drifting out of sync with the code.
# ASCII, no backticks, one line: quoted verbatim by anything that needs to
# describe the grammar in prose.
GRAMMAR_LINE = (
    "An entry begins at column zero with a mandatory bracketed timestamp; "
    "any other line is a continuation, never a sentinel, and quoting a "
    "whole prior entry inside a body requires indenting it off column zero."
)


def sentinel_of(line):
    """Classify one physical line as 'halt', 'pass', 'stamp', or None. The
    ONLY classifier halt_cycles() uses -- see ENTRY_PREFIX / GRAMMAR_LINE
    above for the boundary rule this depends on: a line that does not open
    at column zero with a bracketed timestamp cannot match any of the
    three patterns and always returns None here, with no separate
    entry-start check anywhere else in this module. The three patterns
    share one prefix (concatenated above, never re-typed), so at most one
    can ever match a given line."""
    if HALT_RE.match(line):
        return 'halt'
    if PASS_RE.match(line):
        return 'pass'
    if STAMP_RE.match(line):
        return 'stamp'
    return None


def render_entry(body, timestamp=None):
    """Render one complete 214-LOG.md entry: "[<timestamp>] <body>". This
    is the ONLY place in the module that assembles that shape -- anything
    that needs a ready-to-append entry (the emergency rollback act below
    included) calls this, rather than hand-building a matching string that
    could drift out of sync with ENTRY_PREFIX. `timestamp` defaults to the
    current local time in ISO 8601; a caller with a real historical
    timestamp to reproduce (e.g. a test) may pass one explicitly."""
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    return f"[{timestamp}] {body}"


# The Owner's one-line emergency release at the halt wall: rendered
# through render_entry() like any other entry, so sentinel_of() accepting
# it back is a fact about the SAME code that parses 214-LOG.md, not a
# second literal an author keeps in sync by eye (criterion 1(i)). No hash
# or period number inside it, so the body is fixed across every incident.
ROLLBACK_BODY = "SAFETY-PASS: Owner rollback at the halt ceiling"


def rollback_entry(timestamp=None):
    """The rollback act's own single sentinel line, exactly as
    sentinel_of() will read it back: sentinel_of(rollback_entry()) ==
    'pass' always, by construction -- the module's own circular proof
    that its emergency act is one its own parser accepts (criterion
    1(i))."""
    return render_entry(ROLLBACK_BODY, timestamp)


def rollback_act(timestamp=None):
    """The exact bytes a session must APPEND to 214-LOG.md to perform the
    rollback -- distinct from rollback_entry() itself: this is
    rollback_entry() prefixed with one leading newline, which is delivery
    framing, not sentinel grammar. That leading newline guarantees the
    appended text always begins a fresh physical line, whether or not
    214-LOG.md already ends in one (L0-d, IC addendum 4) -- without it, a
    log lacking a trailing newline would glue the act onto the tail of
    whatever entry is already last, and the glued line would classify as
    THAT entry's kind, never 'pass'. See ROLLBACK_ACT_BEGIN / END below
    for how a deny message bounds this block so it can be extracted
    mechanically instead of guessed at."""
    return "\n" + rollback_entry(timestamp)


# Machine-extractable boundary around rollback_act()'s bytes in the deny
# message below (criterion 6 / L0-d): ROLLBACK_ACT_END carries its OWN
# leading newline as part of the literal, so
# ROLLBACK_ACT_BEGIN + rollback_act(...) + ROLLBACK_ACT_END reproduces
# rollback_act()'s bytes exactly between the two markers, with nothing
# added or stripped either side -- splitting on these two literals, in
# order, recovers them without depending on "the last line of the
# message" or any other heuristic.
ROLLBACK_ACT_BEGIN = "----BEGIN DCS ROLLBACK ACT (copy exactly, byte for byte)----"
ROLLBACK_ACT_END = "\n----END DCS ROLLBACK ACT----"

# Published specimens of this grammar (criterion 1, S2's test surface):
# every line here is classified by sentinel_of() alone, no other function,
# and both this module's own tests and S2's independent ones cite these
# same pairs rather than inventing their own.
SPECIMENS = (
    # A valid entry of each of the three kinds -- the ordinary case.
    ("[2026-01-01T00:03:00+0000] SAFETY-HALT: attempt 1 failed verification", 'halt'),
    ("[2026-01-01T00:20:00+0000] SAFETY-PASS: Owner rollback at the halt ceiling", 'pass'),
    ("[2026-01-01T00:01:00+0000] IAP-APPROVED: 68304eb79661 -- phase: planning -> execution (period 1)", 'stamp'),
    # The rollback body, dictated verbatim but with the mandatory timestamp
    # left off (as if a second author had merely quoted the OLD, pre-v0.6.9
    # deny message word for word): no bracket at column zero, so it never
    # matches -- this is the level-0 refutation IC addendum 4 named, and
    # the reason the timestamp became mandatory in this revision.
    ("SAFETY-PASS: Owner rollback at the halt ceiling", None),
    # A continuation line that itself opens with a sentinel-shaped token,
    # quoting a real anchor mid-summary (verbatim, per
    # multiline-halt-continuation/214-LOG.md) -- not a bracketed timestamp
    # at column zero, so it is a continuation, never a sentinel.
    ("IAP-APPROVED: 68304eb79661 -- this is body text of the halt entry above", None),
    # An INDENTED, verbatim quotation of a whole anchor entry, timestamp
    # and token included -- indentation alone moves the bracket off column
    # zero, so this never anchors even though every character after the
    # leading spaces is a real, valid entry.
    ("    [2026-01-01T00:01:00+0000] IAP-APPROVED: 68304eb79661 -- phase: planning -> execution (period 1)", None),
    # A genuine halt entry that quotes the anchor MID-LINE, in its own
    # body -- the bracket at column zero belongs to THIS entry's own
    # timestamp, so it counts as 'halt', exactly like
    # multiline-halt-continuation/214-LOG.md's first physical line.
    ("[2026-01-01T00:02:00+0000] SAFETY-HALT: refutation detail below, quoted for context -- IAP-APPROVED: 68304eb79661 -- phase: planning -> execution (period 1)", 'halt'),
    # dcs/workflows/plan.md step 8's own verbatim template line, UNFILLED
    # (period 1 revision 3 amendment, command point 3): the placeholder
    # text sits exactly where a real hex digest would go. Correct AT THE
    # BOUNDARY -- STAMP_ENTRY_RE matches it, since the entry prefix and
    # the IAP-APPROVED: token are both present -- but the placeholder is
    # not hex, so STAMP_RE never matches and this line cannot anchor.
    # Publishing this distinction, rather than hiding it, is the whole
    # point of the amendment: an unresolved anchor means counting from the
    # top of the file, which is always earlier, never later, than the
    # true ceiling.
    ("[<timestamp>] IAP-APPROVED: <first 12 hex chars of IAP.md's sha256> -- phase: planning -> execution (period <N>)", None),
)


def deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def find_project_root(target, cwd):
    """Resolve the project root from the TARGET file's own path (v0.3),
    not the session's cwd/env. Before worktrees, a session rooted anywhere
    always meant "the one project" -- CLAUDE_PROJECT_DIR or a cwd-walk was
    an adequate proxy for "which .dcs/ governs this edit." Once a project
    can have several git worktrees (each its own .dcs/ACTIVE, its own
    phase) sharing one machine, that proxy breaks: a session rooted in the
    main checkout editing a file that physically lives inside a worktree
    would resolve against main's .dcs/ (often gate-open, nothing active)
    instead of the worktree's -- a real hole, not a corner case, once
    parallel incidents exist.

    Fix: walk up from the TARGET's own absolute path looking for .dcs/.
    This is what "judged against the tree the file actually lives in"
    means mechanically. CLAUDE_PROJECT_DIR / cwd are consulted ONLY as a
    fallback for a relative target path (needed just to make it absolute
    before the walk can start) -- they are never allowed to override what
    an absolute target path's own walk finds, and they contribute nothing
    once the target is already absolute (the common case: Claude Code's
    Edit/Write tools always pass absolute file_path).
    """
    target_path = Path(target)
    if target_path.is_absolute():
        for candidate in [target_path.parent, *target_path.parent.parents]:
            if (candidate / ".dcs").is_dir():
                return candidate.resolve()
        return None  # absolute target, no .dcs/ anywhere above it -- allow

    # Relative target: fall back to env/cwd to make it absolute-ish first,
    # matching pre-v0.3 behavior exactly (env wins if it has .dcs/, else
    # cwd-walk).
    env_root = os.environ.get("CLAUDE_PROJECT_DIR")
    if env_root:
        candidate = Path(env_root)
        if (candidate / ".dcs").is_dir():
            return candidate.resolve()
    cur = Path(cwd).resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / ".dcs").is_dir():
            return candidate
    return None


def load_config(project_root):
    cfg_path = project_root / ".dcs" / "config.json"
    guarded = DEFAULT_GUARDED
    unguarded = DEFAULT_UNGUARDED
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        guarded = cfg.get("guarded_paths", DEFAULT_GUARDED)
        unguarded = cfg.get("unguarded_paths", DEFAULT_UNGUARDED)
    except (OSError, ValueError, TypeError):
        pass
    return guarded, unguarded


def approval_digests(path):
    """sha256 hex digests of the IAP's accepted byte forms, deduped.

    A byte-exact hash of IAP.md is representation-dependent: git may check
    the file out as LF or CRLF depending on core.autocrlf / .gitattributes,
    and an approval stamp computed against one representation would then
    fail to verify against the other checkout of the SAME commit -- a real
    field failure (2026-07-25), not a hypothetical.

    Widen the accepted set to exactly the equivalence class git's own
    text-conversion declares -- \\r\\n <-> \\n -- and not one byte more:

      raw  -- the file as-is
      lf   -- raw with every \\r\\n folded to \\n
      crlf -- lf with every \\n expanded to \\r\\n (derived from lf, NEVER
              from raw, or an already-CRLF file would double into \\r\\r\\n)

    A lone \\r (old Mac-style, or a real embedded CR) is deliberately left
    untouched in all three forms: it is not part of git's \\r\\n<->\\n
    conversion, so two files differing only by a real CR still hash apart.
    Folding it in would widen the equivalence class beyond what the policy
    declares.

    One exception, found by exhaustive search during the incident that wrote
    this (2026-07-25) and recorded rather than smoothed over: a CR that
    IMMEDIATELY PRECEDES a CRLF is not distinguished, because lf() folds
    "X\\r\\r\\n" and "X\\r\\n" to the same bytes. The asymmetry is one-way --
    a stamp for "X\\r\\n" accepts a disk file "X\\r\\r\\n", not the reverse --
    and it is git's own fold that is lossy there, not this function. The same
    search confirmed the bound: over 1.19 million text pairs, no genuinely
    different logical content is ever accepted, and every ordinary lone-CR
    difference still denies.
    """
    with open(path, "rb") as f:
        raw = f.read()
    lf = raw.replace(b"\r\n", b"\n")
    crlf = lf.replace(b"\n", b"\r\n")
    digests = []
    for form in (raw, lf, crlf):
        d = hashlib.sha256(form).hexdigest()
        if d not in digests:
            digests.append(d)
    return digests


def resolve_incident_dir(project_root, slug):
    """ACTIVE's first field should be the incident directory's EXACT name,
    but that convention was ambiguous before v0.3.1 and sessions wrote the
    bare slug without the YYYY-MM-DD- prefix (field defect, 2026-07-22: a
    real, valid approval became invisible to the exact-join lookup and
    every territory edit was denied with a misleading hash-mismatch
    message). Resolution order:
      1. exact directory match;
      2. otherwise the UNIQUE directory whose name ends with "-<slug>"
         (the date-prefixed form).
    Two or more candidates -> None (deny, naming them): guessing between
    incidents would be worse than blocking."""
    base = project_root / ".dcs" / "incidents"
    exact = base / slug
    if exact.is_dir():
        return exact
    try:
        candidates = [
            d for d in base.iterdir()
            if d.is_dir() and d.name.endswith("-" + slug)
        ]
    except OSError:
        return None
    if len(candidates) == 1:
        return candidates[0]
    return None


def halt_cycles(incident_dir):
    """Pure function: number of lines sentinel_of() classifies 'halt' in
    `<incident_dir>/214-LOG.md`, counted since the LAST valid reset anchor.

    Sentinels are classified with sentinel_of() -- the ONLY classifier
    this function uses, built from this module's ONE published boundary
    definition (see ENTRY_PREFIX / GRAMMAR_LINE): a physical line lacking
    the mandatory bracketed timestamp at column zero classifies as None
    from sentinel_of() alone, with no separate entry-start check anywhere
    in this function. This is what keeps a multi-line SAFETY-HALT: summary
    that quotes a reset token in its own body from either double-counting
    or silently resetting the tally.

    Exactly two things can anchor (reset the tally to zero, then count
    resumes from the next entry onward):
      - the LAST line sentinel_of() classifies 'pass' -- unconditional,
        not hash-bound. There is no verified artifact to bind a Safety
        verdict to, and removing this anchor would brick the close of
        every incident the ceiling ever caught (doctrine-appendix.md
        records why this is a deliberate trade, not an oversight);
      - the LAST line sentinel_of() classifies 'stamp' whose captured hex
        prefix (>= 8 chars, via this module's own STAMP_RE) case-
        insensitively PREFIXES the first line of
        `<incident_dir>/IAP-APPROVED` on disk. The stamped marker is the
        authority; the log line only fixes the marker's position in time
        -- a 'stamp' line whose hex does NOT match the current marker
        (stale, or simply invented) never anchors.
    Whichever of the two comes LAST in the file wins -- not the first
    found scanning backward, and not both compared against each other.

    No anchor matches at all -> count from the top of the file. For any
    log that predates this sentinel grammar, that is always zero, because
    `SAFETY-HALT:` itself is new (v0.6.9) -- a pre-existing incident is
    never walled on first contact with the upgraded hook.

    A missing or unreadable log, or a missing or unreadable
    `IAP-APPROVED` marker, reads as zero halts (or as "no valid 'stamp'
    anchor is possible", respectively) -- NEVER as an exception. This
    function's own contract, independent of any caller. main()
    additionally wraps its caller in another try/except (see that
    function's comments) precisely because a defect here must degrade to
    "no ceiling", never propagate to the outer fail-open clause that
    would disable the entire gate.
    """
    incident_dir = Path(incident_dir)
    log_path = incident_dir / "214-LOG.md"
    try:
        text = log_path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError, ValueError):
        return 0

    marker_prefix = None
    try:
        with open(incident_dir / "IAP-APPROVED", "r", encoding="utf-8-sig") as f:
            first_line = f.readline().strip().lower()
        marker_prefix = first_line or None
    except OSError:
        marker_prefix = None

    lines = text.splitlines()

    anchor = None  # index into `lines` of the last valid reset anchor
    for i, line in enumerate(lines):
        kind = sentinel_of(line)
        if kind == 'pass':
            anchor = i
        elif kind == 'stamp':
            m = STAMP_RE.match(line)
            if m and marker_prefix and marker_prefix.startswith(m.group(1).lower()):
                anchor = i

    start = 0 if anchor is None else anchor + 1
    count = 0
    for i, line in enumerate(lines):
        if i < start:
            continue
        if sentinel_of(line) == 'halt':
            count += 1
    return count


def max_halts(project_root):
    """The halt ceiling: config.json's esg.max_halts_per_attempt, or the
    compiled-in default DEFAULT_MAX_HALTS if the file, the "esg" key, the
    "max_halts_per_attempt" subkey, or a validly-typed value, is absent.

    Every lookup goes through .get(...) with a default, never indexing --
    an old .dcs/config.json predating this key must fall back to the
    default rather than raise. Malformed JSON, missing file, or the
    wrong types all fall back the same way.

    Validated: accepted only when `isinstance(v, int) and not
    isinstance(v, bool) and v >= 1`. `bool` is excluded on purpose even
    though it IS an `int` in Python -- `True` would silently set a
    ceiling of 1, and a project author writing `"max_halts_per_attempt":
    true` almost certainly meant "on" (the default), not "one". `'three'`,
    `0`, `-1`, `3.0`, `None`, or a list all fall back to
    DEFAULT_MAX_HALTS the same way a missing key would. No upper bound is
    enforced: a very large ceiling is a legitimate Owner-level release
    lever (a permissive project may simply choose a high number), not a
    misconfiguration to reject."""
    cfg_path = project_root / ".dcs" / "config.json"
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except (OSError, ValueError, TypeError):
        return DEFAULT_MAX_HALTS
    esg = cfg.get("esg")
    if not isinstance(esg, dict):
        return DEFAULT_MAX_HALTS
    v = esg.get("max_halts_per_attempt", DEFAULT_MAX_HALTS)
    if isinstance(v, bool) or not isinstance(v, int) or v < 1:
        return DEFAULT_MAX_HALTS
    return v


def marker_valid(incident_dir):
    approved = incident_dir / "IAP-APPROVED"
    iap = incident_dir / "IAP.md"
    if not approved.is_file() or not iap.is_file():
        return False
    try:
        # utf-8-sig: tolerate a BOM -- PowerShell 5.1's `Set-Content
        # -Encoding utf8` writes one, and a BOM-prefixed hash silently
        # fails a plain-utf-8 comparison (found in the field 2026-07-22).
        with open(approved, "r", encoding="utf-8-sig") as f:
            stored_hash = f.readline().strip()
        return bool(stored_hash) and stored_hash in approval_digests(iap)
    except OSError:
        return False


def relative_posix(path, project_root):
    """Path relative to the project root, forward-slashed, or None if the
    target lives outside the project entirely (always allowed)."""
    try:
        candidate = Path(path)
        if not candidate.is_absolute():
            candidate = Path(os.getcwd()) / candidate
        rel = candidate.resolve().relative_to(project_root)
    except ValueError:
        return None
    return rel.as_posix()


def path_matches(rel_path, patterns):
    """fnmatch requires a literal '/' in the pattern to have one in the
    string too -- a leading '**/' (glob convention for "any depth,
    including the project root") otherwise fails to match root-level
    files, silently under-matching config.json's default guarded_paths:
    ["**/*"] for anything not inside a subdirectory. For any pattern
    starting with '**/', also try it with that prefix stripped so a
    root-level file matches the zero-directories case."""
    normalized = rel_path.replace("\\", "/")
    for pat in patterns:
        if fnmatch.fnmatch(normalized, pat):
            return True
        if pat.startswith("**/") and fnmatch.fnmatch(normalized, pat[3:]):
            return True
    return False


def main():
    # argv parsing happens STRICTLY BEFORE reading stdin, so this mode
    # never touches the PreToolUse stdin-JSON path below (criterion 2):
    # `--halt-count <incident_dir>` prints halt_cycles() and exits, for a
    # human (or a test) to run by hand against a real incident directory,
    # independent of any PreToolUse invocation.
    if len(sys.argv) >= 3 and sys.argv[1] == "--halt-count":
        print(halt_cycles(sys.argv[2]))
        sys.exit(0)

    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    try:
        tool_input = payload.get("tool_input") or {}
        tool_name = payload.get("tool_name") or ""

        if tool_name == "SendMessage":
            # Single-shot agents (v0.5.8). Every DCS agent -- chief,
            # specialist, Safety Officer, commander, analyst -- is spawned
            # with its inputs, returns once, and is done; nothing in the
            # architecture continues an agent conversationally. Resuming
            # one instead of re-spawning is harmful twice over: the
            # agent's reasoning lives in a transcript no incident artifact
            # records (principle 5 -- the incident directory is the only
            # channel that survives a reset), and a resumed SPECIALIST
            # still carries its OLD tasking, so an amended territory can
            # be edited against the stale one -- a partition violation
            # this hook cannot see because each individual edit looks
            # in-bounds for the tasking the agent remembers.
            #
            # Prose said this twice (plan.md step 3, v0.5.5) and did not
            # hold in the field, which is the whole argument for putting
            # it here instead.
            # NB: a relative target deliberately takes find_project_root's
            # env/cwd branch, which walks from cwd INCLUSIVE. Passing an
            # absolute cwd instead would start at cwd's PARENT and miss a
            # project root that is cwd itself.
            root = find_project_root(".", os.getcwd())
            if root is None:
                sys.exit(0)
            active = root / ".dcs" / "ACTIVE"
            if not active.is_file():
                sys.exit(0)  # no active incident -- not our business
            deny(
                "DCS: agents are single-shot -- resuming one instead of "
                "re-spawning is a doctrine violation while an incident is "
                "active. Spawn a NEW agent (Task) carrying its inputs plus "
                "the corrections verbatim: 201+202 for a chief, the amended "
                "204 for a specialist. A resumed agent's reasoning is in a "
                "transcript no artifact records, and a resumed specialist "
                "still holds its OLD tasking. If this SendMessage is "
                "genuinely unrelated to the incident, the Owner can release "
                "the gate by deleting .dcs/ACTIVE."
            )

        target = tool_input.get("file_path") or tool_input.get("notebook_path")
        if not target:
            sys.exit(0)

        project_root = find_project_root(target, os.getcwd())
        if project_root is None:
            sys.exit(0)  # not a DCS-onboarded project -- nothing to do

        if (project_root / ".dcs" / "CLOSED").is_file():
            # Zombie rule (v0.3, close.md's anti-rot core): this worktree's
            # incident already merged into main and the worktree removal
            # either hasn't run yet or failed (locked files, a session
            # still inside it). Deliberately fail CLOSED here -- see the
            # module docstring for why this is the one exception to
            # "fail open when uncertain."
            deny(
                "DCS gate: this incident is closed and merged; this "
                "worktree is awaiting removal -- do not work here. If you "
                "need to keep working, open a fresh incident "
                "(`/dcs-new`) in a new worktree instead."
            )
            return  # unreachable (deny() exits), keeps linters happy

        active_path = project_root / ".dcs" / "ACTIVE"
        if not active_path.is_file():
            sys.exit(0)  # gate open -- no active incident

        raw = active_path.read_text(encoding="utf-8-sig").strip()
        parts = raw.split("|")
        if len(parts) != 3:
            sys.exit(0)  # malformed ACTIVE -- fail open, don't guess

        slug, inc_type, phase = (p.strip() for p in parts)

        rel_path = relative_posix(target, project_root)
        if rel_path is None:
            sys.exit(0)  # target outside the project -- always allow

        if rel_path == ".dcs" or rel_path.startswith(".dcs/"):
            sys.exit(0)  # incident bookkeeping itself is always writable

        if inc_type == "5" or phase == "closed":
            sys.exit(0)  # express lane / closed incident -- nothing to enforce

        if phase == "execution":
            incident_dir = resolve_incident_dir(project_root, slug)
            if incident_dir is None:
                deny(
                    f"DCS gate: ACTIVE names incident '{slug}' but no "
                    "unique matching directory exists under "
                    ".dcs/incidents/ (none, or several ending in "
                    f"'-{slug}'). Fix .dcs/ACTIVE's first field to the "
                    "EXACT incident directory name, then retry."
                )
            if marker_valid(incident_dir):
                # Halt ceiling check. This entire path -- the config
                # exemption check, count, threshold read, comparison, and
                # the deny call itself -- lives in its OWN inner
                # try/except that returns to the surrounding code on ANY
                # failure. This is deliberate and load-bearing (see the
                # module docstring, step 7): main()'s own outer `except
                # Exception: sys.exit(0)` at the bottom of this function
                # is the fail-open clause for the WHOLE gate -- hash
                # validation, territory globs, the zombie rule included. A
                # defect in the ceiling logic (a missing config key, an
                # unreadable log, a bad incident dir) must degrade to "no
                # ceiling", i.e. fall through to the existing "approved
                # IAP still matches -- gate open" behavior below, and must
                # NEVER be allowed to propagate up to that outer handler,
                # where it would silently disable hash validation and
                # every other check too. deny() itself raises SystemExit,
                # not Exception, so a genuine ceiling breach still exits
                # through here even though the call sits inside this try
                # block.
                try:
                    # Same two checks the planning branch below already
                    # applies to guarded/unguarded_paths, so one rule
                    # governs both surfaces: a path this project's own
                    # config exempts from the gate is exempt from the
                    # ceiling too. This call was previously missing
                    # entirely on the execution path, which is why the
                    # ceiling used to fire on e.g. docs/notes.md
                    # regardless of what config.json declared. The
                    # unconditional .dcs/** exemption above this whole
                    # branch remains the floor either way.
                    guarded, unguarded = load_config(project_root)
                    if path_matches(rel_path, unguarded) or not path_matches(rel_path, guarded):
                        sys.exit(0)  # this path isn't subject to the gate at all
                    count = halt_cycles(incident_dir)
                    ceiling = max_halts(project_root)
                    if count >= ceiling:
                        deny(
                            f"DCS gate: halt ceiling reached for incident "
                            f"{slug} -- {count} SAFETY-HALT: entries since "
                            f"the last reset, ceiling is {ceiling} "
                            "(config.json esg.max_halts_per_attempt). "
                            "Answering \"continue\" on an escalation does "
                            "NOT reset this counter -- a \"continue\" is a "
                            "decision, not a reset. The wall lifts only two "
                            "ways: (1) a fresh stamped and Owner-approved "
                            "IAP via /dcs-plan, which writes both "
                            "IAP-APPROVED and its own IAP-APPROVED: log "
                            "line, or (2) a logged Safety Officer PASS "
                            "verdict. .dcs/** bookkeeping and this "
                            "project's own unguarded paths (config.json "
                            "unguarded_paths) remain writable while this "
                            "wall is up.\n\n"
                            "Emergency rollback -- OWNER ACT ONLY: append "
                            "the exact bytes between the two markers below "
                            "to 214-LOG.md, byte for byte. The act's FIRST "
                            "byte is a newline and it sits INSIDE the "
                            "markers: copy from the end of the BEGIN marker "
                            "line through the end of the entry line. That "
                            "leading newline is part of the act -- it "
                            "guarantees a fresh entry whether or not "
                            "214-LOG.md currently ends in one, and a copy "
                            "that starts at the visible text instead will "
                            "silently fail against a log with no trailing "
                            "newline. Doing "
                            "this without a genuine Safety Officer pass "
                            "verdict behind it is not a routine action -- "
                            "it is a session forging an Owner-level "
                            "rollback decision. Copy it exactly, as the "
                            f"Owner:\n{ROLLBACK_ACT_BEGIN}"
                            f"{rollback_act()}{ROLLBACK_ACT_END}"
                        )
                except Exception:
                    pass
                sys.exit(0)  # approved IAP still matches -- gate open
            deny(
                f"DCS gate: incident {slug} (Type {inc_type}) has no valid "
                f"IAP approval in {incident_dir.name} -- IAP-APPROVED is "
                "missing, or IAP.md was edited after approval (hash "
                "mismatch). Re-approve via /dcs-plan before editing "
                "source. Emergency release: Owner deletes .dcs/ACTIVE."
            )
            return  # unreachable (deny() exits), keeps linters happy

        # phase == "planning" (or any other pre-approval label): only
        # explicitly unguarded paths may be touched.
        guarded, unguarded = load_config(project_root)
        if path_matches(rel_path, unguarded):
            sys.exit(0)
        if not path_matches(rel_path, guarded):
            sys.exit(0)  # not in the guarded set at all -- nothing to enforce

        deny(
            f"DCS gate: incident {slug} (Type {inc_type}) has no approved "
            "IAP. Complete /dcs-plan and get Owner approval. Emergency "
            "release: Owner deletes .dcs/ACTIVE."
        )
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)  # fail open -- never brick the session over a hook bug


if __name__ == "__main__":
    main()
