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
   IAP.md's sha256. ACTIVE's first field resolves to the incident dir by
   exact name, or tolerantly to the UNIQUE dir ending in "-<slug>" (the
   date-prefixed form; ambiguity denies -- see resolve_incident_dir). Editing IAP.md after approval changes its hash and
   silently revokes the marker -- this is deliberate: an edited plan is no
   longer the plan the Owner approved (deviation doctrine, principle 8).
6. Active incident, phase=planning (pre-approval) -> only paths matching
   config.json's unguarded_paths (scratch/docs/.dcs/** by default) may be
   touched. Everything else is denied until /dcs-plan produces an approved
   IAP.
7. Any internal error -> fail OPEN (exit 0). Never brick the session over
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
import sys
from pathlib import Path

DEFAULT_GUARDED = ["**/*"]
DEFAULT_UNGUARDED = [".dcs/**", "tasks/**", "*.md", ".claude/**"]


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


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


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
        return bool(stored_hash) and stored_hash == sha256_of(iap)
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
