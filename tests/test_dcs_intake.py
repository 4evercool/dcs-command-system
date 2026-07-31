"""Behavioural tests for dcs_intake.py (UserPromptSubmit session nudge).

Verifies core intake-nudge behaviour: silent outside DCS projects, one
nudge per session when no incident is active, active-incident reporting,
once-per-session deduplication — plus telemetry logging (both branches,
append, field validation, and fail-open).
"""
import json
import os
import re
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


def run_raw(cwd, session_id):
    """Run hook and return the full CompletedProcess for return-code checks."""
    payload = json.dumps({"session_id": session_id, "prompt": "fix the thing",
                          "cwd": str(cwd)})
    env = dict(os.environ)
    env.pop("CLAUDE_PROJECT_DIR", None)
    return subprocess.run([sys.executable, HOOK], input=payload,
                          capture_output=True, text=True, cwd=str(cwd),
                          env=env, timeout=30)


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

    # ---- Telemetry tests (intake-nudge-telemetry, criterion 5) ----

    def _tel(path):
        """Read telemetry log, return list of record dicts ([] if missing)."""
        if not path.is_file():
            return []
        return [json.loads(l) for l in
                path.read_text(encoding="utf-8").strip().split("\n") if l.strip()]

    # (a) No-active-incident -> nudge_offered
    proj_ta = root / "proj_tel_nudge"
    (proj_ta / ".dcs" / "incidents").mkdir(parents=True)
    run(proj_ta, uuid.uuid4().hex)
    recs_ta = _tel(proj_ta / ".dcs" / "esg" / "intake-telemetry.log")
    check("telemetry: nudge_offered log written with correct event_type",
          len(recs_ta) == 1 and recs_ta[0].get("event_type") == "nudge_offered")

    # (b) Active-incident -> active_reported
    proj_tb = root / "proj_tel_active"
    (proj_tb / ".dcs" / "incidents").mkdir(parents=True)
    (proj_tb / ".dcs" / "ACTIVE").write_text("2026-07-31-test|3|execution")
    run(proj_tb, uuid.uuid4().hex)
    recs_tb = _tel(proj_tb / ".dcs" / "esg" / "intake-telemetry.log")
    check("telemetry: active_reported log written with correct event_type",
          len(recs_tb) == 1 and recs_tb[0].get("event_type") == "active_reported")

    # (c) Append (not overwrite) across successive invocations
    proj_tc = root / "proj_tel_append"
    (proj_tc / ".dcs" / "incidents").mkdir(parents=True)
    run(proj_tc, uuid.uuid4().hex)
    log_tc = proj_tc / ".dcs" / "esg" / "intake-telemetry.log"
    before = len(_tel(log_tc))
    run(proj_tc, uuid.uuid4().hex)
    after = len(_tel(log_tc))
    # If S1 wrote nudge_offered telemetry, we expect: before==1, after==2
    check("telemetry: log appends across invocations (before=1 after=2)",
          before == 1 and after == 2)

    # (d) Field validation on all collected records
    iso_pat = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}')
    sid_pat = re.compile(r'^[0-9a-f]{12}$')
    valid_events = {"nudge_offered", "active_reported"}
    all_tel = []
    for src_path, proj_path in [(proj_ta / ".dcs" / "esg" / "intake-telemetry.log", proj_ta),
                                 (proj_tb / ".dcs" / "esg" / "intake-telemetry.log", proj_tb),
                                 (log_tc, proj_tc)]:
        for rec in _tel(src_path):
            all_tel.append((rec, str(proj_path.resolve())))
    for i, (rec, expect_root) in enumerate(all_tel):
        ts_ok = bool(iso_pat.match(rec.get("timestamp", "")))
        sid_ok = bool(sid_pat.match(rec.get("session_id", "")))
        ev_ok = rec.get("event_type") in valid_events
        pr_ok = rec.get("project_root") == expect_root
        check(f"telemetry: record {i} has valid JSON fields (ts={ts_ok} sid={sid_ok} ev={ev_ok} pr={pr_ok})",
              ts_ok and sid_ok and ev_ok and pr_ok)

    # (e) Fail-open: directory at log path must not crash the hook
    proj_te = root / "proj_tel_failopen"
    (proj_te / ".dcs" / "incidents").mkdir(parents=True)
    (proj_te / ".dcs" / "esg").mkdir(parents=True, exist_ok=True)
    (proj_te / ".dcs" / "esg" / "intake-telemetry.log").mkdir()
    res = run_raw(proj_te, uuid.uuid4().hex)
    check("telemetry: fail-open emits advisory despite directory at log path",
          res.returncode == 0 and "/dcs-run" in res.stdout)

    failed = [r for r in results if not r[0]]
    print(f"\n{len(results) - len(failed)}/{len(results)} passed")
    sys.exit(1 if failed else 0)
finally:
    shutil.rmtree(root, ignore_errors=True)
