"""Independent lifecycle test of dcs_log.py -- the canonical 214-LOG.md
append tool (incident log-append-helper). Same house style as
test_dcs_gate.py: stdlib-only, subprocess-driven against real fixture
directories, its own check()/counter, prints its own "N/M passed" as the
last line, non-zero exit on failure.

dcs_log.py is imported via the SAME guarded importlib.util.spec_from_file_
location pattern test_doctrine_integrity.py's check 23 uses for
record_integrity.py (test_doctrine_integrity.py:2355-2364): this incident
runs four specialists in parallel and S1's module (dcs/tools/dcs_log.py) is
a read dependency this file does not control the landing order of, so a
missing or broken module degrades every import-dependent case to a NAMED
RED finding instead of crashing this script before its own "N/M passed"
line ever prints. The CLI-level (subprocess) cases below need no separate
guard: subprocess.run does not raise merely because dcs_log.py does not
exist yet -- Python's own launcher reports that on stderr with a non-zero
exit, which every case below already treats as an ordinary, named FAIL
(mirrors test_doctrine_integrity.py:2384-2397's own comment on this same
point for record_integrity.py's _ri_run()).

dcs_gate.py (dcs/hooks/dcs_gate.py) is NOT part of this incident's
parallel-landing set -- 202-OBJECTIVES.md criterion 2 requires no edit to
it, and no specialist's territory includes it -- so it is imported
directly, unguarded, matching this repo's own test_dcs_gate.py precedent
at the top of that file.

A first, early run of this suite (before S1 landed dcs/tools/dcs_log.py)
is this file's own required non-vacuity control-run evidence for
criterion 8: every import-dependent case below reported a NAMED red
finding rather than aborting the script, and the CLI-level cases reported
plain, named failures (dcs_log.py not found) rather than raising. See this
tasking's return for that recorded control-run output.
"""
import concurrent.futures
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DCS_LOG_PATH = REPO / "dcs" / "tools" / "dcs_log.py"
DCS_GATE_PATH = REPO / "dcs" / "hooks" / "dcs_gate.py"

# Tolerance around a "does this timestamp look like real now()" window.
# dcs_log.py's own pinned format is datetime.now().astimezone().isoformat()
# -- full, UNTRUNCATED sub-second precision, never rounded to whole
# seconds (the earlier .replace(microsecond=0) truncation was removed;
# see the timestamp-resolution checks below) -- so this padding exists
# only to absorb ordinary process-launch/clock skew between this test's
# own datetime.now() capture and the subprocess's internal clock read,
# never any truncation in the tool itself (there is none). 2 seconds is
# generous for that skew without weakening the check's ability to catch
# a wildly wrong value (a fixed epoch, a hardcoded past date, an
# env-var override).
_WINDOW_PAD = timedelta(seconds=2)

results = []


def check(name, got, want):
    ok = got == want
    results.append((ok, name, want, got))
    print(f"{'PASS' if ok else 'FAIL'}  {name}: want={want} got={got}")


def extract_bracket(line):
    """The raw "[...]" substring (delimiters stripped) at the start of
    `line`, or None -- mirrors record_integrity.py's own bracket-peeling
    (record_integrity.py:1330-1331), not a re-derivation of ENTRY_PREFIX
    itself (classification stays gate.sentinel_of()'s job everywhere in
    this file)."""
    m = re.match(r"^\[([^\]]*)\]", line)
    return m.group(1) if m else None


def make_fixture_project(root, dirname, slug, initial_log_text):
    """A minimal DCS project holding exactly one incident directory named
    EXACTLY `slug` (so resolve_incident_dir()'s exact-match branch
    applies, dcs_gate.py:384-386), with `initial_log_text` written as
    214-LOG.md's starting bytes. No config.json/ACTIVE/IAP-APPROVED --
    dcs_log.py's own CLI needs neither (only find_project_root()'s
    '.dcs/' marker and resolve_incident_dir()'s <incidents_dir>/<slug>
    directory), unlike dcs_gate.py's PreToolUse gate path. Returns
    (project_root, incident_dir)."""
    proj = root / dirname
    inc = proj / ".dcs" / "incidents" / slug
    inc.mkdir(parents=True)
    (inc / "214-LOG.md").write_bytes(initial_log_text.encode("utf-8"))
    return proj, inc


def run_dcs_log(args, cwd, extra_env=None):
    """Subprocess CLI invocation -- the ONLY interface this file relies on
    for dcs_log.py's behaviour (204-TASKING/S1.md's documented `append
    <slug> --by <operator> [--sentinel ...] "<text>"` contract), never an
    internal function name S1's tasking does not guarantee. cwd is set to
    the fixture project root itself, which dcs_log.py's own
    find_project_root(".", os.getcwd()) call resolves via the relative-
    target/cwd-walk branch (dcs_gate.py:296-309) -- CLAUDE_PROJECT_DIR is
    also set to the same root, belt-and-suspenders, matching
    test_dcs_gate.py's own run_gate() convention. Never raises merely
    because dcs_log.py does not exist yet -- see module docstring."""
    env = dict(os.environ)
    env.pop("DCS_TIMESTAMP", None)
    env.pop("SOURCE_DATE_EPOCH", None)
    if extra_env:
        env.update(extra_env)
    env["CLAUDE_PROJECT_DIR"] = str(cwd)
    proc = subprocess.run(
        [sys.executable, str(DCS_LOG_PATH)] + list(args),
        cwd=str(cwd), capture_output=True, text=True,
        encoding="utf-8", errors="replace", env=env, timeout=30,
    )
    return proc.returncode, proc.stdout, proc.stderr


def gate_halt_count(incident_dir):
    proc = subprocess.run(
        [sys.executable, str(DCS_GATE_PATH), "--halt-count", str(incident_dir)],
        capture_output=True, text=True, timeout=30,
    )
    return proc.stdout.strip()


INITIAL_LOG = (
    "# 214 -- Operational Log\n"
    "\n"
    "**Incident:** test-incident\n"
    "\n"
    "[2026-08-01T09:00:00+00:00] incident opened, type 3, phase=planning\n"
)

# --- 1. criterion 1's own stated proof: stdlib-only imports ----------------
if not DCS_LOG_PATH.is_file():
    check(f"dcs_log.py stdlib-only imports (file not found -- S1 has not "
          f"landed yet at {DCS_LOG_PATH})", False, True)
else:
    _src = DCS_LOG_PATH.read_text(encoding="utf-8")
    _stdlib = getattr(sys, "stdlib_module_names", None)
    if _stdlib is None:
        # Fallback for Python < 3.10 (this worktree measures 3.10.0rc2,
        # so the branch above is the one actually exercised here).
        _stdlib = frozenset(sys.builtin_module_names) | {
            "argparse", "datetime", "importlib", "json", "os", "pathlib",
            "re", "sys", "subprocess", "shutil", "hashlib", "tempfile",
            "io", "fnmatch", "shlex", "collections", "contextlib",
        }
    _bad_imports = [
        m.group(0) for m in re.finditer(
            r"^(?:import|from)\s+([A-Za-z_][A-Za-z0-9_.]*)", _src, re.M)
        if m.group(1).split(".")[0] not in _stdlib
    ]
    check(f"dcs_log.py: every top-level import is stdlib-only (checked "
          f"against sys.stdlib_module_names); offending lines: {_bad_imports}",
          not _bad_imports, True)

# --- 2. guarded import + PINNED FORMAT (D1/D2) contract equality -----------
# dcs_gate.py is pre-existing, outside every specialist's territory this
# incident -- unguarded, matching test_dcs_gate.py's own top-of-file import.
_gate_spec = importlib.util.spec_from_file_location("dcs_gate", str(DCS_GATE_PATH))
gate = importlib.util.module_from_spec(_gate_spec)
_gate_spec.loader.exec_module(gate)

_dl_import_error = None
try:
    _dl_spec = importlib.util.spec_from_file_location("dcs_log", str(DCS_LOG_PATH))
    dl = importlib.util.module_from_spec(_dl_spec)
    _dl_spec.loader.exec_module(dl)
except Exception as _dl_exc:  # noqa: broad on purpose -- see module docstring
    dl = None
    _dl_import_error = _dl_exc

check(f"dcs_log.py imports cleanly via the guarded spec_from_file_location "
      f"pattern (S1's territory: {DCS_LOG_PATH}); import error if any: "
      f"{_dl_import_error!r}",
      dl is not None, True)

if dl is None:
    for _name in ("INVOCATION", "OPERATOR_SEP", "SENTINELS", "FORMAT_LINE"):
        check(f"dcs_log.py exports {_name} (guarded: module not importable)",
              False, True)
else:
    # Pinned INDEPENDENTLY here, from 204-TASKING/S1.md's "PINNED FORMAT
    # (D1/D2)" section and the IAP, never read back from `dl` itself --
    # the whole point of this permanent regression test is to catch S1's
    # own module drifting from the plan, which reading the answer key
    # from the code under test could never do.
    _PINNED_INVOCATION = ('python "$HOME/.claude/dcs/tools/dcs_log.py" '
                           'append <slug> --by <operator> "<text>"')
    _PINNED_OPERATOR_SEP = " -- op: "
    _PINNED_SENTINELS = {"halt": "SAFETY-HALT:", "pass": "SAFETY-PASS:",
                          "stamp": "IAP-APPROVED:"}
    check("dcs_log.py: INVOCATION matches the pinned contract (not S1's "
          "to vary; a variance here is a deviation, not a judgement call)",
          getattr(dl, "INVOCATION", None), _PINNED_INVOCATION)
    check("dcs_log.py: OPERATOR_SEP matches the pinned contract",
          getattr(dl, "OPERATOR_SEP", None), _PINNED_OPERATOR_SEP)
    check("dcs_log.py: SENTINELS matches the pinned contract",
          getattr(dl, "SENTINELS", None), _PINNED_SENTINELS)
    _fl = getattr(dl, "FORMAT_LINE", "")
    check("dcs_log.py: FORMAT_LINE is a non-empty, single-line, ASCII, "
          f"backtick-free string (204-TASKING/S1.md's own requirement; "
          f"value: {_fl!r})",
          bool(_fl) and "\n" not in _fl and "`" not in _fl
          and all(ord(c) < 128 for c in _fl),
          True)

# ============================================================================
# Everything below needs real fixture directories -- one shared tempdir,
# removed in `finally` even if a case above already went red.
# ============================================================================
root = Path(tempfile.mkdtemp(prefix="dcs_log_test_"))
try:
    # --- 3. round-trip through the imported dcs_gate.sentinel_of() ---------
    # All three sentinel kinds and the no-sentinel case (202 criterion 2's
    # own stated proof, exercised through this file's own CLI contract).
    _RT_CASES = (
        ("no-sentinel", None,
         "plain body text for the no-sentinel round trip", None),
        ("halt", "halt", "halt body for the round trip", "halt"),
        ("pass", "pass", "pass body for the round trip", "pass"),
        ("stamp", "stamp",
         "deadbeef01 -- phase: planning -> execution (period 1)", "stamp"),
    )
    for _case_name, _sentinel_flag, _text, _expect_kind in _RT_CASES:
        _proj, _inc = make_fixture_project(
            root, f"rt_{_case_name}", "rt-incident", INITIAL_LOG)
        _args = ["append", "rt-incident", "--by", "S4 tester"]
        if _sentinel_flag:
            _args += ["--sentinel", _sentinel_flag]
        _args.append(_text)
        _rc, _out, _err = run_dcs_log(_args, cwd=_proj)
        check(f"round-trip {_case_name}: append exits 0 "
              f"(stdout={_out.strip()!r} stderr={_err.strip()!r})", _rc, 0)
        _lines = (_inc / "214-LOG.md").read_text(encoding="utf-8").splitlines()
        _last_line = _lines[-1] if _lines else ""
        _classification = gate.sentinel_of(_last_line) if _rc == 0 else "<append failed>"
        check(f"round-trip {_case_name}: dcs_gate.sentinel_of(appended line) "
              f"== {_expect_kind!r} (appended line: {_last_line!r})",
              _classification, _expect_kind)

    # --- 4. timestamp: offset-aware, second-resolution, moves between calls
    _ts_proj, _ts_inc = make_fixture_project(root, "ts_test", "ts-incident", INITIAL_LOG)

    _before1 = datetime.now(timezone.utc)
    _rc1, _out1, _err1 = run_dcs_log(
        ["append", "ts-incident", "--by", "S4 tester", "first timestamp call"],
        cwd=_ts_proj)
    _after1 = datetime.now(timezone.utc)
    check(f"timestamp call 1: append exits 0 (stderr={_err1.strip()!r})", _rc1, 0)
    _line1 = (_ts_inc / "214-LOG.md").read_text(encoding="utf-8").splitlines()[-1]

    time.sleep(1.5)

    _before2 = datetime.now(timezone.utc)
    _rc2, _out2, _err2 = run_dcs_log(
        ["append", "ts-incident", "--by", "S4 tester", "second timestamp call"],
        cwd=_ts_proj)
    _after2 = datetime.now(timezone.utc)
    check(f"timestamp call 2: append exits 0 (stderr={_err2.strip()!r})", _rc2, 0)
    _line2 = (_ts_inc / "214-LOG.md").read_text(encoding="utf-8").splitlines()[-1]

    _bracket1, _bracket2 = extract_bracket(_line1), extract_bracket(_line2)
    # Sub-second (fractional-seconds) resolution is the whole point of S1's
    # precision fix -- this must now assert the OPPOSITE of what it used to:
    # not "no fractional seconds" but "fractional seconds present, exactly
    # 6 digits". CONFIRMED against S1's now-final dcs_log.py (re-read
    # 2026-08-04, second fix-tasking): the call is
    # datetime.now().astimezone().isoformat(timespec="microseconds") --
    # the EXPLICIT timespec="microseconds" argument (not bare .isoformat(),
    # which defaults to timespec="auto") is what makes this UNCONDITIONAL
    # rather than merely likely: "auto" omits the fractional field entirely
    # whenever microsecond happens to land on exactly 0, which
    # timespec="microseconds" never does -- it always zero-pads to 6
    # digits. So this assertion holds on every call, not just the
    # astronomically-likely-but-not-guaranteed case a bare .isoformat()
    # would have left it as. Never truncated or rounded (dcs_log.py's own
    # PINNED FORMAT section) -- this regex itself needed no change from
    # the first fix-tasking round, only this confirmation.
    _SUBSECOND_RE = re.compile(
        r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}[+-]\d{2}:\d{2}$")
    check(f"timestamp: bracket 1 ({_bracket1!r}) is sub-second-resolution, "
          "offset-aware ISO shape (fractional seconds present, per the "
          "pinned datetime.now().astimezone().isoformat() format -- never "
          "truncated or rounded to whole seconds)",
          bool(_bracket1 and _SUBSECOND_RE.match(_bracket1)), True)
    check(f"timestamp: bracket 2 ({_bracket2!r}) is sub-second-resolution, "
          "offset-aware ISO shape",
          bool(_bracket2 and _SUBSECOND_RE.match(_bracket2)), True)

    _parsed1 = datetime.fromisoformat(_bracket1) if _bracket1 else None
    _parsed2 = datetime.fromisoformat(_bracket2) if _bracket2 else None
    check("timestamp: bracket 1 parses offset-aware (tzinfo is not None)",
          _parsed1 is not None and _parsed1.tzinfo is not None, True)
    check("timestamp: bracket 2 parses offset-aware (tzinfo is not None)",
          _parsed2 is not None and _parsed2.tzinfo is not None, True)
    check(f"timestamp: moves between two calls ~1.5s apart "
          f"(bracket1={_bracket1!r} bracket2={_bracket2!r})",
          bool(_parsed1 and _parsed2 and _parsed1 != _parsed2), True)

    if _parsed1 is not None:
        _u1 = _parsed1.astimezone(timezone.utc)
        check(f"timestamp: bracket 1 ({_u1.isoformat()}) falls within the "
              f"real call window [{_before1.isoformat()}, {_after1.isoformat()}] "
              f"(padded {_WINDOW_PAD})",
              _before1 - _WINDOW_PAD <= _u1 <= _after1 + _WINDOW_PAD, True)
    if _parsed2 is not None:
        _u2 = _parsed2.astimezone(timezone.utc)
        check(f"timestamp: bracket 2 ({_u2.isoformat()}) falls within the "
              f"real call window [{_before2.isoformat()}, {_after2.isoformat()}] "
              f"(padded {_WINDOW_PAD})",
              _before2 - _WINDOW_PAD <= _u2 <= _after2 + _WINDOW_PAD, True)

    # --- 5. no flag or environment variable can set the timestamp ----------
    _env_proj, _env_inc = make_fixture_project(root, "env_test", "env-incident", INITIAL_LOG)
    _junk_env = {
        "DCS_TIMESTAMP": "1999-01-01T00:00:00+00:00",
        "SOURCE_DATE_EPOCH": "0",
        "TZ": "Junk/Nonexistent_Zone_12345",
    }
    _before_e = datetime.now(timezone.utc)
    _rc_e, _out_e, _err_e = run_dcs_log(
        ["append", "env-incident", "--by", "S4 tester", "env override probe"],
        cwd=_env_proj, extra_env=_junk_env)
    _after_e = datetime.now(timezone.utc)
    check(f"no-env-override: append with junk DCS_TIMESTAMP/SOURCE_DATE_EPOCH/"
          f"TZ still exits 0 (stdout={_out_e.strip()!r} stderr={_err_e.strip()!r})",
          _rc_e, 0)
    _line_e = (_env_inc / "214-LOG.md").read_text(encoding="utf-8").splitlines()[-1]
    _bracket_e = extract_bracket(_line_e)
    _parsed_e = datetime.fromisoformat(_bracket_e) if _bracket_e else None
    check(f"no-env-override: appended bracket ({_bracket_e!r}) is offset-aware "
          "(never the naive junk DCS_TIMESTAMP value)",
          _parsed_e is not None and _parsed_e.tzinfo is not None, True)
    if _parsed_e is not None:
        _u_e = _parsed_e.astimezone(timezone.utc)
        check(f"no-env-override: appended bracket ({_u_e.isoformat()}) falls "
              "within the real call window, not 1999-01-01 or epoch 0",
              _before_e - _WINDOW_PAD <= _u_e <= _after_e + _WINDOW_PAD, True)

    if DCS_LOG_PATH.is_file():
        _src2 = DCS_LOG_PATH.read_text(encoding="utf-8")
        _env_hits = re.findall(r"\b(?:environ|getenv)\b[^\n]*", _src2)
        _suspicious = [h for h in _env_hits if re.search(r"time|stamp|epoch|clock", h, re.I)]
        check(f"no-env-override: no environ/getenv reference in dcs_log.py's "
              f"source mentions a timestamp-shaped name (all hits: {_env_hits})",
              not _suspicious, True)

    # --- 6. refusals: --sentinel stamp non-hex body; missing/empty --by ----
    _ref_proj, _ref_inc = make_fixture_project(root, "refusal_test", "ref-incident", INITIAL_LOG)
    _ref_log = _ref_inc / "214-LOG.md"
    _ref_lines_before = _ref_log.read_text(encoding="utf-8").splitlines()

    _rc, _out, _err = run_dcs_log(
        ["append", "ref-incident", "--by", "S4 tester", "--sentinel", "stamp",
         "nothexvalue -- phase: planning -> execution (period 1)"],
        cwd=_ref_proj)
    check(f"refusal: --sentinel stamp with a non-hex body is refused "
          f"(exit={_rc}, stderr={_err.strip()!r})", _rc != 0, True)

    _rc, _out, _err = run_dcs_log(
        ["append", "ref-incident", "--by", "", "empty-by body text"],
        cwd=_ref_proj)
    check(f"refusal: empty --by '' is refused (exit={_rc}, stderr={_err.strip()!r})",
          _rc != 0, True)

    _rc, _out, _err = run_dcs_log(
        ["append", "ref-incident", "missing-by-flag-entirely body text"],
        cwd=_ref_proj)
    check(f"refusal: --by omitted entirely is refused "
          f"(exit={_rc}, stderr={_err.strip()!r})", _rc != 0, True)

    _ref_lines_after = _ref_log.read_text(encoding="utf-8").splitlines()
    check(f"refusal: none of the three refused calls appended a line "
          f"(before={len(_ref_lines_before)} lines, after={len(_ref_lines_after)} lines)",
          len(_ref_lines_after), len(_ref_lines_before))

    # --- 7. a file with no trailing newline still gets an entry at column 0
    _noeol_proj, _noeol_inc = make_fixture_project(
        root, "noeol_test", "noeol-incident", INITIAL_LOG)
    _noeol_log = _noeol_inc / "214-LOG.md"
    _noeol_bytes = _noeol_log.read_bytes().rstrip(b"\n")
    check("no-trailing-newline setup: fixture log deliberately stripped of "
          "its final newline", _noeol_bytes.endswith(b"\n"), False)
    _noeol_log.write_bytes(_noeol_bytes)
    _original_last_line = _noeol_bytes.decode("utf-8").splitlines()[-1]

    _count_before = gate_halt_count(_noeol_inc)
    _rc, _out, _err = run_dcs_log(
        ["append", "noeol-incident", "--by", "S4 tester", "--sentinel", "halt",
         "no-trailing-newline probe"],
        cwd=_noeol_proj)
    check(f"no-trailing-newline: append exits 0 (stderr={_err.strip()!r})", _rc, 0)

    _new_lines = _noeol_log.read_bytes().decode("utf-8").splitlines()
    check("no-trailing-newline: the file's original last line is unchanged, "
          f"not glued to (original: {_original_last_line!r}, now at index -2: "
          f"{_new_lines[-2] if len(_new_lines) >= 2 else None!r})",
          _new_lines[-2] if len(_new_lines) >= 2 else None, _original_last_line)
    check(f"no-trailing-newline: the new entry starts at column zero on its "
          f"own line (new last line: {_new_lines[-1]!r})",
          _new_lines[-1].startswith("["), True)

    _count_after = gate_halt_count(_noeol_inc)
    check("no-trailing-newline: dcs_gate.py --halt-count confirms the new "
          f"entry counts (before={_count_before!r}, after={_count_after!r})",
          (_count_before, _count_after), ("0", "1"))

    # --- 8. permanent regression test: counted identically to a hand-written
    # entry of equivalent content -----------------------------------------
    _eq_proj_a, _eq_inc_a = make_fixture_project(root, "halteq_a", "halteq-incident", INITIAL_LOG)
    _eq_proj_b, _eq_inc_b = make_fixture_project(root, "halteq_b", "halteq-incident", INITIAL_LOG)

    _rc, _out, _err = run_dcs_log(
        ["append", "halteq-incident", "--by", "S4 tester", "--sentinel", "halt",
         "equivalence probe body"],
        cwd=_eq_proj_a)
    check(f"halt-count equivalence: tool-appended halt entry, append exits 0 "
          f"(stderr={_err.strip()!r})", _rc, 0)

    # Hand-built using the PINNED contract, deliberately NOT read back from
    # `dl` -- this permanent regression test exists to catch dcs_log.py
    # drifting from the pinned SAFETY-HALT:/OPERATOR_SEP shape, which
    # reading the answer key from the code under test could never do.
    _PINNED_HALT_TOKEN = "SAFETY-HALT:"
    _PINNED_OP_SEP = " -- op: "
    _hand_body = f"{_PINNED_HALT_TOKEN} equivalence probe body"
    _hand_line = gate.render_entry(_hand_body, "2026-08-01T10:00:00+00:00") + _PINNED_OP_SEP + "S4 tester"
    with open(_eq_inc_b / "214-LOG.md", "a", encoding="utf-8", newline="\n") as _f:
        _f.write(_hand_line + "\n")
    check(f"halt-count equivalence: the hand-written entry itself classifies "
          f"as 'halt' (sanity check: {_hand_line!r})",
          gate.sentinel_of(_hand_line), "halt")

    _count_a = gate_halt_count(_eq_inc_a)
    _count_b = gate_halt_count(_eq_inc_b)
    check("halt-count equivalence (permanent regression test): dcs_gate.py "
          f"--halt-count counts the tool-appended entry ({_count_a!r}) "
          f"identically to a hand-written entry of equivalent content "
          f"({_count_b!r})", _count_a, _count_b)
    check("halt-count equivalence: both counts are exactly 1, not vacuously "
          "equal at 0", _count_a, "1")

    # --- 9. containment, two explicit permanent regression tests -----------
    _cont_proj, _cont_inc = make_fixture_project(
        root, "containment_test", "containment-incident", INITIAL_LOG)
    _cont_incidents_dir = _cont_proj / ".dcs" / "incidents"

    for _bad_slug in ("../containment-incident", "..\\containment-incident",
                       "sub/slug", "sub\\slug", ".."):
        _before_dirs = {p.name for p in _cont_incidents_dir.iterdir()}
        _rc, _out, _err = run_dcs_log(
            ["append", _bad_slug, "--by", "S4 tester", "containment probe"],
            cwd=_cont_proj)
        _after_dirs = {p.name for p in _cont_incidents_dir.iterdir()}
        check(f"containment (permanent regression test): slug {_bad_slug!r} "
              "(path separator or '..' component) is REJECTED before "
              f"resolution -- exit != 0 (exit={_rc}, stderr={_err.strip()!r})",
              _rc != 0, True)
        check(f"containment: slug {_bad_slug!r} refusal created no new "
              f"directory under .dcs/incidents/ (before={sorted(_before_dirs)}, "
              f"after={sorted(_after_dirs)})",
              _after_dirs, _before_dirs)

    _unknown_slug = "no-such-incident-anywhere"
    _before_dirs2 = {p.name for p in _cont_incidents_dir.iterdir()}
    _rc, _out, _err = run_dcs_log(
        ["append", _unknown_slug, "--by", "S4 tester", "unknown slug probe"],
        cwd=_cont_proj)
    _after_dirs2 = {p.name for p in _cont_incidents_dir.iterdir()}
    check("containment (permanent regression test): append REFUSES when the "
          f"resolved incident directory does not already exist -- exit != 0 "
          f"(slug={_unknown_slug!r}, exit={_rc}, stderr={_err.strip()!r})",
          _rc != 0, True)
    check(f"containment: unknown-slug refusal created no new directory "
          f"(before={sorted(_before_dirs2)}, after={sorted(_after_dirs2)})",
          _after_dirs2, _before_dirs2)

    _nolog_proj = root / "nolog_test"
    _nolog_inc = _nolog_proj / ".dcs" / "incidents" / "nolog-incident"
    _nolog_inc.mkdir(parents=True)
    _rc, _out, _err = run_dcs_log(
        ["append", "nolog-incident", "--by", "S4 tester", "missing-log probe"],
        cwd=_nolog_proj)
    check("containment (permanent regression test): append REFUSES when the "
          "resolved incident directory exists but its 214-LOG.md does not -- "
          f"exit != 0 (exit={_rc}, stderr={_err.strip()!r})", _rc != 0, True)
    check("containment: the missing-log refusal did not create a 214-LOG.md",
          (_nolog_inc / "214-LOG.md").exists(), False)

    # --- 10. concurrency stress test (log-append-helper, second fix-------
    # tasking): N simultaneous dcs_log.py append invocations against ONE
    # fixture log -- every entry must land exactly once, and no invocation
    # may report success (exit 0) for bytes that did not actually survive
    # to disk. This is the permanent test that makes S1's lock fix
    # "enforced by a test, not asserted by prose" (this tasking's own
    # wording). S1's dcs_log.py docstring (CONCURRENCY section, read fresh
    # for this fix-tasking) documents the pre-fix failure this guards
    # against: "proven live, 8 concurrent invocations against one fixture
    # log landed only 6 entries, every process exiting 0 with empty
    # stderr" -- fixed by _append_entry() acquiring an exclusive,
    # cross-process os.O_CREAT|os.O_EXCL sidecar lock file
    # (<log_path>.lock) before the read and releasing it only after the
    # write, with a 5.0s bounded-retry timeout that refuses (exit 1, FAIL
    # CLOSED) rather than proceeding unsafely.
    _CONC_N = 10  # "8 or more simultaneous invocations" (fix-tasking)
    _conc_proj, _conc_inc = make_fixture_project(
        root, "concurrency_test", "conc-incident", INITIAL_LOG)
    _conc_log = _conc_inc / "214-LOG.md"
    _conc_lines_before = len([
        ln for ln in _conc_log.read_text(encoding="utf-8").splitlines()
        if ln.startswith("[")
    ])

    def _conc_worker(i):
        marker = f"concurrent-append-marker-{i:03d}"
        rc, out, err = run_dcs_log(
            ["append", "conc-incident", "--by", f"S4 concurrency worker {i}", marker],
            cwd=_conc_proj)
        return i, marker, rc, out, err

    with concurrent.futures.ThreadPoolExecutor(max_workers=_CONC_N) as _conc_ex:
        # All N tasks submitted in one tight loop, max_workers == N, so
        # every worker's subprocess.run() call is in flight at once --
        # subprocess.run() blocks only the calling THREAD while the child
        # process runs; the GIL is released for that wait, so the N child
        # processes genuinely execute concurrently, racing the SAME
        # fixture log and the SAME sidecar lock file.
        _conc_futures = [_conc_ex.submit(_conc_worker, i) for i in range(_CONC_N)]
        _conc_results = [f.result() for f in _conc_futures]

    _conc_final_text = _conc_log.read_text(encoding="utf-8")
    _conc_final_bracket_lines = [
        ln for ln in _conc_final_text.splitlines() if ln.startswith("[")
    ]

    _conc_successes = [(i, marker) for i, marker, rc, out, err in _conc_results if rc == 0]
    _conc_failures = [(i, rc, err.strip()) for i, marker, rc, out, err in _conc_results if rc != 0]
    check(f"concurrency stress: all {_CONC_N} simultaneous dcs_log.py "
          f"append invocations against ONE fixture log exit 0 "
          f"(failures: {_conc_failures})",
          len(_conc_successes), _CONC_N)

    # Every entry lands exactly once: each successful invocation's unique
    # marker must appear on disk EXACTLY once -- zero occurrences is a
    # FALSE SUCCESS (exit 0 reported for bytes that never survived to
    # disk); more than one is an impossible duplicate/interleave.
    _conc_marker_counts = {
        marker: _conc_final_text.count(marker) for _i, marker in _conc_successes
    }
    _conc_lost = sorted(m for m, c in _conc_marker_counts.items() if c == 0)
    _conc_dup = {m: c for m, c in _conc_marker_counts.items() if c > 1}
    check("concurrency stress: no invocation reported success (exit 0) for "
          f"bytes that did not actually survive to disk (lost markers: "
          f"{_conc_lost})",
          _conc_lost, [])
    check("concurrency stress: every marker landed EXACTLY once -- no "
          f"duplicate/interleaved write (markers appearing more than "
          f"once: {_conc_dup})",
          _conc_dup, {})

    # Aggregate count: exactly len(successes) NEW bracketed lines landed --
    # S1's own documented pre-fix failure was "8 concurrent invocations
    # landed only 6 entries, every process exiting 0"; this is the
    # permanent regression test for exactly that count-level symptom.
    _conc_new_line_count = len(_conc_final_bracket_lines) - _conc_lines_before
    check(f"concurrency stress: exactly {len(_conc_successes)} new entries "
          f"landed on disk (before={_conc_lines_before} bracket lines, "
          f"after={len(_conc_final_bracket_lines)}) -- S1's own documented "
          "pre-fix failure was 8 invocations landing only 6 lines, every "
          "process exiting 0",
          _conc_new_line_count, len(_conc_successes))

    # No glued/interleaved garbage: every one of the NEW lines starts at
    # column zero with a bracket (NEWLINE SAFETY) -- a marker-substring
    # count alone could theoretically miss two entries glued onto one
    # physical line.
    _conc_new_bracket_lines = _conc_final_bracket_lines[_conc_lines_before:]
    check("concurrency stress: every newly-landed line is well-formed -- "
          "starts at column zero with a bracket, none glued/interleaved "
          f"(new bracket-line count: {len(_conc_new_bracket_lines)})",
          len(_conc_new_bracket_lines), len(_conc_successes))

    # No stray lock file left behind: _acquire_lock()'s own contract is
    # that the lock file's mere presence on disk IS the lock, removed in
    # _append_entry()'s own `finally` on every exit path (ordinary or
    # refused).
    _conc_lock_path = _conc_log.with_name(_conc_log.name + ".lock")
    check("concurrency stress: no stray .lock sidecar file left behind "
          f"after all {_CONC_N} invocations completed ({_conc_lock_path})",
          _conc_lock_path.exists(), False)

finally:
    shutil.rmtree(root, ignore_errors=True)

failed = [r for r in results if not r[0]]
print(f"\n{len(results) - len(failed)}/{len(results)} passed")
sys.exit(1 if failed else 0)
