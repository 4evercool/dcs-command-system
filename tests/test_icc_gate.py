"""Independent lifecycle test of icc_gate.py — fabricated project states, real subprocess calls."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HOOK = r"C:\Users\4ever\.claude\icc\hooks\icc_gate.py"
results = []


def run_gate(project, target, cwd=None):
    payload = json.dumps({"tool_name": "Edit", "tool_input": {"file_path": str(target)}})
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project))
    p = subprocess.run([sys.executable, HOOK], input=payload, capture_output=True,
                       text=True, cwd=str(cwd or project), env=env, timeout=30)
    out = p.stdout.strip()
    if not out:
        return "allow"
    try:
        decision = json.loads(out)["hookSpecificOutput"]["permissionDecision"]
        return decision  # "deny"
    except Exception:
        return f"unparseable: {out[:120]}"


def check(name, got, want):
    ok = got == want
    results.append((ok, name, want, got))
    print(f"{'PASS' if ok else 'FAIL'}  {name}: want={want} got={got}")


root = Path(tempfile.mkdtemp(prefix="icc_test_"))
try:
    # --- Project WITHOUT .icc ---
    bare = root / "bare"
    (bare / "src").mkdir(parents=True)
    check("no .icc anywhere -> allow", run_gate(bare, bare / "src" / "app.py"), "allow")

    # --- ICC project, Type 3, phase=planning ---
    proj = root / "proj"
    inc = proj / ".icc" / "incidents" / "2026-07-22-test-incident"
    inc.mkdir(parents=True)
    (proj / "src").mkdir()
    (proj / "src" / "app.py").write_text("x = 1\n")
    (proj / "rootfile.py").write_text("y = 2\n")
    (proj / ".icc" / "config.json").write_text(json.dumps({
        "incidents_dir": ".icc/incidents",
        "guarded_paths": ["**/*"],
        "unguarded_paths": [".icc/**", "tasks/**", "*.md", ".claude/**"],
    }))
    active = proj / ".icc" / "ACTIVE"
    active.write_text("2026-07-22-test-incident|3|planning")

    check("planning: guarded src file -> deny", run_gate(proj, proj / "src" / "app.py"), "deny")
    check("planning: ROOT-level .py (fnmatch fix) -> deny", run_gate(proj, proj / "rootfile.py"), "deny")
    check("planning: .icc bookkeeping -> allow", run_gate(proj, inc / "202-OBJECTIVES.md"), "allow")
    check("planning: tasks/** -> allow", run_gate(proj, proj / "tasks" / "todo.md"), "allow")
    check("planning: root *.md -> allow", run_gate(proj, proj / "NOTES.md"), "allow")
    check("planning: relative path resolution -> deny", run_gate(proj, "src/app.py"), "deny")
    check("planning: file OUTSIDE project -> allow", run_gate(proj, root / "elsewhere.py"), "allow")

    # --- phase=execution, no marker ---
    active.write_text("2026-07-22-test-incident|3|execution")
    check("execution: no IAP-APPROVED -> deny", run_gate(proj, proj / "src" / "app.py"), "deny")

    # --- valid marker ---
    iap = inc / "IAP.md"
    iap.write_text("# IAP\nobjectives...\n")
    digest = hashlib.sha256(iap.read_bytes()).hexdigest()
    (inc / "IAP-APPROVED").write_text(f"{digest}\napproved_by: owner\n")
    check("execution: valid hash marker -> allow", run_gate(proj, proj / "src" / "app.py"), "allow")

    # --- IAP edited post-approval -> hash void ---
    iap.write_text("# IAP\nobjectives... EDITED AFTER APPROVAL\n")
    check("execution: IAP edited (hash void) -> deny", run_gate(proj, proj / "src" / "app.py"), "deny")

    # --- Type 5 / malformed ACTIVE / cwd-walk discovery ---
    active.write_text("2026-07-22-test-incident|5|planning")
    check("type 5 -> allow", run_gate(proj, proj / "src" / "app.py"), "allow")
    active.write_text("garbage-no-pipes")
    check("malformed ACTIVE -> fail open (allow)", run_gate(proj, proj / "src" / "app.py"), "allow")
    active.write_text("2026-07-22-test-incident|3|planning")
    env_less = dict(os.environ)
    env_less.pop("CLAUDE_PROJECT_DIR", None)
    p = subprocess.run([sys.executable, HOOK],
                       input=json.dumps({"tool_name": "Edit", "tool_input": {"file_path": str(proj / "src" / "app.py")}}),
                       capture_output=True, text=True, cwd=str(proj / "src"), env=env_less, timeout=30)
    got = "deny" if '"deny"' in p.stdout else "allow"
    check("no env var, cwd-walk finds root -> deny", got, "deny")

    failed = [r for r in results if not r[0]]
    print(f"\n{len(results) - len(failed)}/{len(results)} passed")
    sys.exit(1 if failed else 0)
finally:
    shutil.rmtree(root, ignore_errors=True)
