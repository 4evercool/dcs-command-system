"""Regression tests for bin/dcs.js's `doctor` and `bump` commands.

Covers four defects introduced in f3af8f5 and shipped without any test
coverage until an external review caught them:

  1. doctor's silent-pass fallback -- when payload_check.py exits 2
     (environment error) or is missing, doctor used to print nothing at
     all if the version strings happened to match, indistinguishable
     from a genuine content-verified pass.
  2. bump's double-new-version log -- `pkgJson.version = version` ran
     before the final log line, so both sides of "old -> new" read the
     new value.
  3. bump's unguarded rollback write -- the rollback write to
     package.json (on a dcs/VERSION write failure) had no try/catch, so
     a failure during rollback crashed with an uncaught exception
     instead of a clear diagnostic.
  4. bump's unanchored version regex -- `/^\\d+\\.\\d+\\.\\d+/` has no end
     anchor, so garbage like "9.9.9-garbage-not-semver!!!" passed.

All fixtures live under a per-test temp directory and are pointed to via
DCS_PKG_ROOT / DCS_CLAUDE_DIR (bin/dcs.js's own testing hooks, see its
top-of-file comment) -- the real repo's package.json / dcs/VERSION are
never touched.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BIN = str(Path(__file__).resolve().parent.parent / "bin" / "dcs.js")
results = []


def check(name, ok, detail=""):
    results.append((ok, name, detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail and not ok else ""))


def make_pkg_root(root, version="1.2.3", payload_check=None):
    """payload_check: None (no tests/ dir at all), 'exit2' (a script that
    always exits 2), or 'exit0' (always exits 0)."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "package.json").write_text(
        json.dumps({"name": "dcs-test-fixture", "version": version}, indent=2) + "\n",
        encoding="utf8",
    )
    (root / "dcs").mkdir(parents=True, exist_ok=True)
    (root / "dcs" / "VERSION").write_text(version + "\n", encoding="utf8")
    if payload_check is not None:
        (root / "tests").mkdir(parents=True, exist_ok=True)
        code = {"exit2": "import sys\nsys.exit(2)\n",
                "exit0": "import sys\nsys.exit(0)\n"}[payload_check]
        (root / "tests" / "payload_check.py").write_text(code, encoding="utf8")
    return root


def make_claude_dir(root, version="1.2.3"):
    root.mkdir(parents=True, exist_ok=True)
    (root / "dcs").mkdir(parents=True, exist_ok=True)
    (root / "dcs" / "VERSION").write_text(version + "\n", encoding="utf8")
    return root


def run_dcs(args, pkg_root, claude_dir, extra_env=None):
    env = dict(os.environ)
    env["DCS_PKG_ROOT"] = str(pkg_root)
    env["DCS_CLAUDE_DIR"] = str(claude_dir)
    if extra_env:
        env.update(extra_env)
    return subprocess.run(["node", BIN] + args, capture_output=True, text=True,
                           env=env, timeout=30)


root = Path(tempfile.mkdtemp(prefix="dcs_cli_test_"))
try:
    # ---------------------------------------------------------------
    # Defect 1: doctor's silent-pass fallback must never be silent,
    # even when installed == package version.
    # ---------------------------------------------------------------

    # 1a. payload_check.py missing entirely, versions MATCH.
    pkg1 = make_pkg_root(root / "d1a_pkg", version="1.2.3", payload_check=None)
    claude1 = make_claude_dir(root / "d1a_claude", version="1.2.3")
    p = run_dcs(["doctor"], pkg1, claude1)
    check(
        "doctor: missing payload_check.py + version match -> explicit "
        "'not performed' signal (not silent)",
        "content check: NOT performed (payload_check.py not found)" in p.stdout,
        p.stdout,
    )

    # 1b. payload_check.py exits 2 (environment error), versions MATCH.
    pkg1b = make_pkg_root(root / "d1b_pkg", version="4.5.6", payload_check="exit2")
    claude1b = make_claude_dir(root / "d1b_claude", version="4.5.6")
    p = run_dcs(["doctor"], pkg1b, claude1b)
    check(
        "doctor: payload_check.py exit 2 + version match -> explicit "
        "'not performed' signal (not silent)",
        "content check: NOT performed (payload_check.py exited with "
        "environment error, status 2)" in p.stdout,
        p.stdout,
    )

    # 1c. sanity: a real pass (exit 0) still reports "identical", so the
    # fix didn't turn genuine passes into false warnings.
    pkg1c = make_pkg_root(root / "d1c_pkg", version="7.7.7", payload_check="exit0")
    claude1c = make_claude_dir(root / "d1c_claude", version="7.7.7")
    p = run_dcs(["doctor"], pkg1c, claude1c)
    check(
        "doctor: payload_check.py exit 0 -> 'content check: identical' "
        "(genuine pass unaffected)",
        "content check: identical" in p.stdout
        and "NOT performed" not in p.stdout,
        p.stdout,
    )

    # ---------------------------------------------------------------
    # Defect 2: bump must log the OLD version, not the new one, on the
    # left side of "old -> new".
    # ---------------------------------------------------------------
    pkg2 = make_pkg_root(root / "d2_pkg", version="0.1.0")
    p = run_dcs(["bump", "9.9.9"], pkg2, root / "d2_claude_unused")
    check(
        "bump: logs 'old -> new', not 'new -> new'",
        "version bumped: 0.1.0 -> 9.9.9" in p.stdout
        and "version bumped: 9.9.9 -> 9.9.9" not in p.stdout,
        p.stdout + p.stderr,
    )
    new_pkg_json = json.loads((pkg2 / "package.json").read_text(encoding="utf8"))
    new_version_file = (pkg2 / "dcs" / "VERSION").read_text(encoding="utf8").strip()
    check(
        "bump: package.json and dcs/VERSION both actually updated to 9.9.9",
        new_pkg_json["version"] == "9.9.9" and new_version_file == "9.9.9",
        f"package.json={new_pkg_json['version']!r} VERSION={new_version_file!r}",
    )

    # ---------------------------------------------------------------
    # Defect 4: version regex must be anchored at both ends.
    # ---------------------------------------------------------------
    pkg4 = make_pkg_root(root / "d4_pkg", version="0.1.0")
    p = run_dcs(["bump", "9.9.9-garbage-not-semver!!!"], pkg4, root / "d4_claude_unused")
    check(
        "bump: rejects unanchored garbage ('9.9.9-garbage-not-semver!!!')",
        p.returncode != 0 and "error: version must be semver-like" in p.stderr,
        f"returncode={p.returncode} stderr={p.stderr}",
    )
    unchanged = json.loads((pkg4 / "package.json").read_text(encoding="utf8"))
    check(
        "bump: rejected garbage version leaves package.json untouched",
        unchanged["version"] == "0.1.0",
        unchanged["version"],
    )

    pkg4b = make_pkg_root(root / "d4b_pkg", version="0.1.0")
    p = run_dcs(["bump", "1.2.3 "], pkg4b, root / "d4b_claude_unused")
    check(
        "bump: rejects trailing-whitespace garbage ('1.2.3 ')",
        p.returncode != 0 and "error: version must be semver-like" in p.stderr,
        f"returncode={p.returncode} stderr={p.stderr}",
    )

    pkg4c = make_pkg_root(root / "d4c_pkg", version="0.1.0")
    p = run_dcs(["bump", "1.2.3-alpha.1"], pkg4c, root / "d4c_claude_unused")
    check(
        "bump: still accepts a valid semver pre-release ('1.2.3-alpha.1')",
        p.returncode == 0 and "version bumped: 0.1.0 -> 1.2.3-alpha.1" in p.stdout,
        f"returncode={p.returncode} stdout={p.stdout} stderr={p.stderr}",
    )

    pkg4d = make_pkg_root(root / "d4d_pkg", version="0.1.0")
    p = run_dcs(["bump", "1.2.3"], pkg4d, root / "d4d_claude_unused")
    check(
        "bump: still accepts a bare N.N.N ('1.2.3')",
        p.returncode == 0 and "version bumped: 0.1.0 -> 1.2.3" in p.stdout,
        f"returncode={p.returncode} stdout={p.stdout} stderr={p.stderr}",
    )

    # ---------------------------------------------------------------
    # Defect 3: a failure during the rollback write must produce a
    # clear diagnostic naming both files and both versions -- never an
    # uncaught exception. Simulated by monkey-patching fs.writeFileSync
    # inside the SAME node process that requires bin/dcs.js, so the
    # patched fs module (Node's module cache is shared) is the one
    # bin/dcs.js's own `require("fs")` sees: 1st call (package.json,
    # new version) succeeds for real, 2nd call (dcs/VERSION) is made to
    # throw, 3rd call (the rollback write of package.json) is ALSO made
    # to throw, forcing exactly the double-failure path.
    # ---------------------------------------------------------------
    pkg3 = make_pkg_root(root / "d3_pkg", version="0.1.0")
    bin_path_js = BIN.replace("\\", "\\\\")
    harness = f"""
const fs = require('fs');
const real = fs.writeFileSync;
let n = 0;
fs.writeFileSync = function(...args) {{
  n++;
  if (n === 1) return real.apply(fs, args);
  throw new Error('SIMULATED_WRITE_FAIL_' + n);
}};
process.argv[2] = 'bump';
process.argv[3] = '9.9.9';
require('{bin_path_js}');
"""
    env = dict(os.environ)
    env["DCS_PKG_ROOT"] = str(pkg3)
    env["DCS_CLAUDE_DIR"] = str(root / "d3_claude_unused")
    p = subprocess.run(["node", "-e", harness], capture_output=True, text=True,
                        env=env, timeout=30)
    expected_pkg_file = str(pkg3 / "package.json")
    expected_version_file = str(pkg3 / "dcs" / "VERSION")
    check(
        "bump: double-write-failure exits 1 (not an uncaught-exception crash)",
        p.returncode == 1,
        f"returncode={p.returncode} stderr={p.stderr}",
    )
    check(
        "bump: double-write-failure names package.json and dcs/VERSION and both versions",
        "INCONSISTENT" in p.stderr
        and expected_pkg_file in p.stderr
        and expected_version_file in p.stderr
        and "0.1.0" in p.stderr
        and "9.9.9" in p.stderr,
        p.stderr,
    )
    check(
        "bump: double-write-failure reports the rollback failure explicitly",
        "rollback of package.json also failed" in p.stderr,
        p.stderr,
    )
    # Must NOT look like a raw, unhandled JS stack trace escaping our
    # own diagnostic (i.e. no "at Object.writeFileSync" internal frame
    # printed as the FIRST thing before our own error: lines).
    check(
        "bump: double-write-failure prints our diagnostic, not a bare uncaught-exception trace",
        p.stderr.strip().startswith("error:"),
        p.stderr,
    )

    failed = [r for r in results if not r[0]]
    print(f"\n{len(results) - len(failed)}/{len(results)} passed")
    sys.exit(1 if failed else 0)
finally:
    shutil.rmtree(root, ignore_errors=True)
