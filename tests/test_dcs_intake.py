"""Behavioural tests for dcs_intake.py (UserPromptSubmit session nudge).

Verifies the four things that matter: it stays silent outside DCS
projects, it nudges once when no incident is active, it reports an active
incident instead, and it never fires twice in one session.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

HOOK = str(Path(__file__).resolve().parent.parent / "dcs" / "hooks" / "dcs_intake.py")
results = []


def run(cwd, session_id):
    payload = json.dumps({"session_id": session_id, "prompt": "fix the thing",
                          "cwd": str(cwd)})
    env = dict(os.environ)
    env.pop("CLAUDE_PROJECT_DIR", None)
    p = subprocess.run([sys.executable, HOOK], input=payload, capture_output=True,
                       text=True, cwd=str(cwd), env=env, timeout=30)
    out = p.stdout.strip()
    if not out:
        return ""
    try:
        return json.loads(out)["hookSpecificOutput"]["additionalContext"]
    except Exception:
        return "UNPARSEABLE: " + out[:120]


def check(name, ok):
    results.append((ok, name))
    print(f"{'PASS' if ok else 'FAIL'}  {name}")


root = Path(tempfile.mkdtemp(prefix="dcs_intake_test_"))
try:
    bare = root / "bare"
    (bare / "src").mkdir(parents=True)
    check("outside a DCS project -> silent", run(bare, uuid.uuid4().hex) == "")

    proj = root / "proj"
    (proj / ".dcs" / "incidents").mkdir(parents=True)
    (proj / "src").mkdir()

    sid = uuid.uuid4().hex
    ctx = run(proj, sid)
    check("no active incident -> nudge mentions /dcs-run",
          "/dcs-run" in ctx and "no incident" in ctx.lower())
    check("nudge tells the session to ASK rather than to open unilaterally",
          "ASK" in ctx or "ask" in ctx.lower())
    check("nudge exempts questions/trivial work", "trivial" in ctx.lower())

    check("same session again -> silent (once per session)", run(proj, sid) == "")

    sid2 = uuid.uuid4().hex
    (proj / ".dcs" / "ACTIVE").write_text("2026-07-25-some-slug|3|execution")
    ctx2 = run(proj, sid2)
    check("active incident -> reports slug", "2026-07-25-some-slug" in ctx2)
    check("active incident -> reports type and phase",
          "Type 3" in ctx2 and "execution" in ctx2)
    check("active incident -> points at /dcs-status", "/dcs-status" in ctx2)

    # a different project in the same session must still get its own note
    proj2 = root / "proj2"
    (proj2 / ".dcs").mkdir(parents=True)
    check("different project, same session -> still notified", run(proj2, sid2) != "")

    p = subprocess.run([sys.executable, HOOK], input="not json at all",
                       capture_output=True, text=True, cwd=str(proj), timeout=30)
    check("malformed stdin -> silent, exit 0", p.stdout.strip() == "" and p.returncode == 0)

    failed = [r for r in results if not r[0]]
    print(f"\n{len(results) - len(failed)}/{len(results)} passed")
    sys.exit(1 if failed else 0)
finally:
    shutil.rmtree(root, ignore_errors=True)
