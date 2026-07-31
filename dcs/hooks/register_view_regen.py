#!/usr/bin/env python3
"""PostToolUse hook: regenerate the register view whenever REGISTER.md is
edited, so vault/register-view.html's predecessor problem -- a derived
artifact that only updates when someone remembers to re-run the generator
-- never recurs for register-view.html itself.

Fires on PostToolUse for Edit|Write (wired into .claude/settings.json by
/dcs-init, alongside the PreToolUse gate). Logic:

1. Resolve the project root FROM THE TARGET FILE'S OWN PATH, exactly like
   dcs_gate.py's find_project_root() -- a session rooted elsewhere editing
   a file inside a worktree must regenerate THAT worktree's view, not
   main's. No root found -> not a DCS-onboarded tree, nothing to do.
2. Target isn't <project_root>/.dcs/esg/REGISTER.md -> nothing to do. Any
   other edit is none of this hook's business.
3. Otherwise, run <project_root>/.dcs/register_view.py -- the per-project
   installed copy, tracked in the project's own git history (unlike
   REGISTER.md itself, this is a static tool, not per-worktree data, so
   it lives outside .dcs/esg/ rather than beside the file it reads) --
   and report its result via additionalContext.

This hook never writes to .dcs/esg/REGISTER.md or REGISTER-LOCK itself --
it only ever invokes register_view.py, which is documented there as
opening REGISTER.md read-only and writing solely to the sibling,
already-gitignored register-view.html.

Fails open on every error, like every other DCS hook: a hook bug must
never block the edit that already happened, and never bricks the session.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

SUBPROCESS_TIMEOUT = 15  # seconds; register_view.py parses one small file


def find_project_root(target, cwd):
    """Same resolution dcs_gate.py uses: walk up from the TARGET's own
    absolute path looking for .dcs/. CLAUDE_PROJECT_DIR/cwd are consulted
    only as a fallback to make a relative target absolute first -- Claude
    Code's Edit/Write tools always pass an absolute file_path, so that
    fallback is the uncommon path here, not the load-bearing one."""
    target_path = Path(target)
    if target_path.is_absolute():
        for candidate in [target_path.parent, *target_path.parent.parents]:
            if (candidate / ".dcs").is_dir():
                return candidate.resolve()
        return None

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


def emit(context):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": context,
        }
    }))


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    try:
        tool_input = payload.get("tool_input") or {}
        target = tool_input.get("file_path")
        if not target:
            sys.exit(0)

        project_root = find_project_root(target, payload.get("cwd") or os.getcwd())
        if project_root is None:
            sys.exit(0)  # not a DCS-onboarded tree -- nothing to do

        register = (project_root / ".dcs" / "esg" / "REGISTER.md").resolve()
        try:
            target_resolved = Path(target).resolve()
        except OSError:
            sys.exit(0)

        if os.path.normcase(str(target_resolved)) != os.path.normcase(str(register)):
            sys.exit(0)  # not the register -- not our business

        script = project_root / ".dcs" / "register_view.py"
        if not script.is_file():
            sys.exit(0)  # this project hasn't installed the view generator

        try:
            result = subprocess.run(
                [sys.executable, str(script)],
                cwd=str(project_root),
                capture_output=True,
                text=True,
                timeout=SUBPROCESS_TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            emit(
                "[register-view] regeneration timed out after {0}s following "
                "a REGISTER.md edit -- view may be stale, "
                "re-run python .dcs/register_view.py by hand.".format(SUBPROCESS_TIMEOUT)
            )
            sys.exit(0)

        if result.returncode == 0:
            emit("[register-view] regenerated: " + result.stdout.strip())
        else:
            emit(
                "[register-view] regeneration FAILED after REGISTER.md edit "
                "(exit {0}): {1}".format(
                    result.returncode, (result.stderr or result.stdout).strip()[:500]
                )
            )
    except SystemExit:
        raise
    except Exception:
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()
