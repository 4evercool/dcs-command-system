"""Independent lifecycle test of dcs_gate.py — fabricated project states, real subprocess calls."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HOOK = str(Path(__file__).resolve().parent.parent / "dcs" / "hooks" / "dcs_gate.py")
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


root = Path(tempfile.mkdtemp(prefix="dcs_test_"))
try:
    # --- Project WITHOUT .dcs ---
    bare = root / "bare"
    (bare / "src").mkdir(parents=True)
    check("no .dcs anywhere -> allow", run_gate(bare, bare / "src" / "app.py"), "allow")

    # --- DCS project, Type 3, phase=planning ---
    proj = root / "proj"
    inc = proj / ".dcs" / "incidents" / "2026-07-22-test-incident"
    inc.mkdir(parents=True)
    (proj / "src").mkdir()
    (proj / "src" / "app.py").write_text("x = 1\n")
    (proj / "rootfile.py").write_text("y = 2\n")
    (proj / ".dcs" / "config.json").write_text(json.dumps({
        "incidents_dir": ".dcs/incidents",
        "guarded_paths": ["**/*"],
        "unguarded_paths": [".dcs/**", "tasks/**", "*.md", ".claude/**"],
    }))
    active = proj / ".dcs" / "ACTIVE"
    active.write_text("2026-07-22-test-incident|3|planning")

    check("planning: guarded src file -> deny", run_gate(proj, proj / "src" / "app.py"), "deny")
    check("planning: ROOT-level .py (fnmatch fix) -> deny", run_gate(proj, proj / "rootfile.py"), "deny")
    check("planning: .dcs bookkeeping -> allow", run_gate(proj, inc / "202-OBJECTIVES.md"), "allow")
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

    # --- v0.3: root resolution from the TARGET's own path, not env/cwd ---
    # Two sibling .dcs projects: a session rooted (cwd + CLAUDE_PROJECT_DIR)
    # in A edits a file that physically lives in B (the worktree case).
    # A is deliberately type=5 (which the gate always allows regardless of
    # phase) so a wrong resolution against A would read "allow" -- if these
    # checks instead see B's real state, the old bug is proven fixed.
    projA = root / "parallel" / "projA"
    projB = root / "parallel" / "projB"
    (projA / ".dcs").mkdir(parents=True)
    (projA / ".dcs" / "ACTIVE").write_text("a-incident|5|planning")

    incB = projB / ".dcs" / "incidents" / "b-incident"
    incB.mkdir(parents=True)
    (projB / "src").mkdir()
    (projB / "src" / "app.py").write_text("z = 1\n")
    (projB / ".dcs" / "config.json").write_text(json.dumps({
        "incidents_dir": ".dcs/incidents",
        "guarded_paths": ["**/*"],
        "unguarded_paths": [".dcs/**", "tasks/**", "*.md", ".claude/**"],
    }))
    (projB / ".dcs" / "ACTIVE").write_text("b-incident|3|planning")

    def run_gate_cross(target, project_dir_env, cwd):
        payload = json.dumps({"tool_name": "Edit", "tool_input": {"file_path": str(target)}})
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project_dir_env))
        p = subprocess.run([sys.executable, HOOK], input=payload, capture_output=True,
                           text=True, cwd=str(cwd), env=env, timeout=30)
        out = p.stdout.strip()
        if not out:
            return "allow"
        try:
            return json.loads(out)["hookSpecificOutput"]["permissionDecision"]
        except Exception:
            return f"unparseable: {out[:120]}"

    check(
        "v0.3(a): env=A, target lives in B (planning) -> judged against B, deny",
        run_gate_cross(projB / "src" / "app.py", projA, projA), "deny",
    )

    iapB = incB / "IAP.md"
    iapB.write_text("# IAP\nobjectives...\n")
    digestB = hashlib.sha256(iapB.read_bytes()).hexdigest()
    (incB / "IAP-APPROVED").write_text(f"{digestB}\napproved_by: owner\n")
    (projB / ".dcs" / "ACTIVE").write_text("b-incident|3|execution")
    check(
        "v0.3(b): env=A, target lives in B (execution, valid marker) -> allow",
        run_gate_cross(projB / "src" / "app.py", projA, projA), "allow",
    )

    (projB / ".dcs" / "CLOSED").write_text("merged into main 2026-07-22\n")
    check(
        "v0.3(c): .dcs/CLOSED zombie marker in B -> deny even with valid IAP marker",
        run_gate_cross(projB / "src" / "app.py", projA, projA), "deny",
    )
    (projB / ".dcs" / "CLOSED").unlink()

    outside_file = root / "parallel" / "elsewhere.py"
    outside_file.write_text("q = 1\n")
    check(
        "v0.3(d): target outside any .dcs project, env points elsewhere -> allow",
        run_gate_cross(outside_file, projA, projA), "allow",
    )

    # --- v0.3.1: ACTIVE slug vs date-prefixed incident dir (field defect
    # 2026-07-22: a session wrote the bare slug into ACTIVE while the dir
    # was <date>-<slug>; the exact-join lookup missed a VALID approval and
    # denied every territory edit with a misleading hash-mismatch message).
    projC = root / "parallel" / "projC"
    incC = projC / ".dcs" / "incidents" / "2026-07-22-slug-mismatch"
    incC.mkdir(parents=True)
    (projC / "src").mkdir()
    (projC / "src" / "app.py").write_text("q = 1\n")
    iapC = incC / "IAP.md"
    iapC.write_text("# IAP C\n")
    dC = hashlib.sha256(iapC.read_bytes()).hexdigest()
    (incC / "IAP-APPROVED").write_text(f"{dC}\napproved_by: owner\n")
    (projC / ".dcs" / "ACTIVE").write_text("slug-mismatch|1|execution")
    check(
        "v0.3.1(a): bare-slug ACTIVE, date-prefixed dir, valid marker -> allow",
        run_gate(projC, projC / "src" / "app.py"), "allow",
    )
    iapC.write_text("# IAP C edited after approval\n")
    check(
        "v0.3.1(b): bare-slug ACTIVE resolves, but hash void -> deny",
        run_gate(projC, projC / "src" / "app.py"), "deny",
    )
    iapC.write_text("# IAP C\n")  # restore the valid marker state
    (projC / ".dcs" / "incidents" / "2026-07-23-slug-mismatch").mkdir()
    check(
        "v0.3.1(c): ambiguous suffix match (two dirs) -> deny, never guess",
        run_gate(projC, projC / "src" / "app.py"), "deny",
    )

    failed = [r for r in results if not r[0]]
    print(f"\n{len(results) - len(failed)}/{len(results)} passed")
    sys.exit(1 if failed else 0)
finally:
    shutil.rmtree(root, ignore_errors=True)
