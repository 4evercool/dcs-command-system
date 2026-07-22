#!/usr/bin/env python3
"""PreToolUse hook: mechanical enforcement of the ICC IAP-approval gate.

ICC ("Incident Command for Code") adapts the ICS Planning P to software
work: no source edit happens until an Incident Action Plan (IAP) exists and
has been approved by the Owner. Doctrine says the rule is "mechanical, not
behavioral" (references/doctrine.md, principle 11) -- this hook is that
mechanism, modeled directly on bread_bot's bash_guard.py stdin-JSON /
stdout-JSON deny pattern.

Fires on PreToolUse for Edit|Write|NotebookEdit (wired by /icc-init into the
project's .claude/settings.json, appended alongside any existing
PreToolUse hooks -- never replacing them). Logic:

1. No active incident (<project>/.icc/ACTIVE absent) -> allow. Zero
   overhead for projects/sessions doing non-ICC work.
2. Active incident, type=5 or phase=closed -> allow. Type 5's express lane
   never sets ACTIVE in the first place; a "closed" phase label (defensive
   handling -- /icc-close normally deletes ACTIVE outright rather than
   transitioning through a closed state) has nothing left to enforce.
3. Active incident, phase=execution -> the gate is open IF the approval
   marker (.icc/incidents/<slug>/IAP-APPROVED) still matches the current
   IAP.md's sha256. Editing IAP.md after approval changes its hash and
   silently revokes the marker -- this is deliberate: an edited plan is no
   longer the plan the Owner approved (deviation doctrine, principle 8).
4. Active incident, phase=planning (pre-approval) -> only paths matching
   config.json's unguarded_paths (scratch/docs/.icc/** by default) may be
   touched. Everything else is denied until /icc-plan produces an approved
   IAP.
5. Any internal error -> fail OPEN (exit 0). Never brick the session over
   a hook bug.

No escape-hatch environment variable, unlike bash_guard.py's GUARD_OK=1 --
the one sanctioned emergency release is the Owner deleting .icc/ACTIVE, an
explicit, visible act (doctrine principle 11).
"""
import fnmatch
import hashlib
import json
import os
import sys
from pathlib import Path

DEFAULT_GUARDED = ["**/*"]
DEFAULT_UNGUARDED = [".icc/**", "tasks/**", "*.md", ".claude/**"]


def deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def find_project_root(start):
    """CLAUDE_PROJECT_DIR if it has .icc/, else walk up from cwd looking
    for a directory containing .icc/. Returns None if neither finds one --
    that means this isn't an ICC-onboarded project and the hook has
    nothing to do."""
    env_root = os.environ.get("CLAUDE_PROJECT_DIR")
    if env_root:
        candidate = Path(env_root)
        if (candidate / ".icc").is_dir():
            return candidate.resolve()
    cur = Path(start).resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / ".icc").is_dir():
            return candidate
    return None


def load_config(project_root):
    cfg_path = project_root / ".icc" / "config.json"
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
        target = tool_input.get("file_path") or tool_input.get("notebook_path")
        if not target:
            sys.exit(0)

        project_root = find_project_root(os.getcwd())
        if project_root is None:
            sys.exit(0)  # not an ICC-onboarded project -- nothing to do

        active_path = project_root / ".icc" / "ACTIVE"
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

        if rel_path == ".icc" or rel_path.startswith(".icc/"):
            sys.exit(0)  # incident bookkeeping itself is always writable

        if inc_type == "5" or phase == "closed":
            sys.exit(0)  # express lane / closed incident -- nothing to enforce

        if phase == "execution":
            incident_dir = project_root / ".icc" / "incidents" / slug
            if marker_valid(incident_dir):
                sys.exit(0)  # approved IAP still matches -- gate open
            deny(
                f"ICC gate: incident {slug} (Type {inc_type}) has no valid "
                "IAP approval -- IAP.md was edited after approval (hash "
                "mismatch) or IAP-APPROVED is missing. Re-approve via "
                "/icc-plan before editing source. Emergency release: Owner "
                "deletes .icc/ACTIVE."
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
            f"ICC gate: incident {slug} (Type {inc_type}) has no approved "
            "IAP. Complete /icc-plan and get Owner approval. Emergency "
            "release: Owner deletes .icc/ACTIVE."
        )
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)  # fail open -- never brick the session over a hook bug


if __name__ == "__main__":
    main()
