"""Independent lifecycle test of dcs_gate.py — fabricated project states, real subprocess calls."""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HOOK = str(Path(__file__).resolve().parent.parent / "dcs" / "hooks" / "dcs_gate.py")
results = []

# Import the hook module itself (stdlib only; main() sits behind
# `if __name__ == "__main__"`, so importing it has no side effects) --
# same importlib.util technique tests/test_doctrine_integrity.py already
# uses. This test cites the module's OWN sentinel grammar (ENTRY_PREFIX,
# HALT_RE/PASS_RE/STAMP_RE, sentinel_of, render_entry, rollback_entry,
# rollback_act, ROLLBACK_ACT_BEGIN/END, SPECIMENS) rather than re-deriving
# any of it here -- a duplicate is exactly how revision 2's circular test
# drifted from the code it was meant to check.
_gate_spec = importlib.util.spec_from_file_location("dcs_gate", HOOK)
gate = importlib.util.module_from_spec(_gate_spec)
_gate_spec.loader.exec_module(gate)


def extract_rollback_act(reason):
    """Extract the exact bytes of the rollback act from a deny message, by
    the ONE boundary dcs_gate.py itself publishes (ROLLBACK_ACT_BEGIN /
    ROLLBACK_ACT_END) -- never a "last line" heuristic. Returns None if
    either marker is absent from `reason`; a caller getting None back must
    treat that as a hard test failure (a deviation to S1, per
    204-TASKING/S2.md), never as a license to fall back to guessing at the
    message's shape."""
    if gate.ROLLBACK_ACT_BEGIN not in reason or gate.ROLLBACK_ACT_END not in reason:
        return None
    after_begin = reason.split(gate.ROLLBACK_ACT_BEGIN, 1)[1]
    if gate.ROLLBACK_ACT_END not in after_begin:
        return None
    extracted, _, _ = after_begin.partition(gate.ROLLBACK_ACT_END)
    return extracted


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


def run_gate_reason(project, target, cwd=None):
    """Like run_gate, but returns the full permissionDecisionReason text
    on a deny (or None on allow) -- used by the criterion-5a/level-0
    circular test to extract the copy-ready rollback line from the deny
    message ITSELF, never from a hardcoded duplicate of it."""
    payload = json.dumps({"tool_name": "Edit", "tool_input": {"file_path": str(target)}})
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project))
    p = subprocess.run([sys.executable, HOOK], input=payload, capture_output=True,
                       text=True, cwd=str(cwd or project), env=env, timeout=30)
    out = p.stdout.strip()
    if not out:
        return None
    return json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]


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

    # --- v0.5.8: SendMessage (agent resume) denied while an incident is
    # active. Every DCS agent is single-shot; a resumed specialist still
    # carries its OLD tasking, so an amended territory can be edited
    # against the stale one -- invisible to the per-edit check above.
    def run_sendmessage(project, cwd):
        payload = json.dumps({"tool_name": "SendMessage",
                              "tool_input": {"to": "abc123", "message": "revise"}})
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project))
        p = subprocess.run([sys.executable, HOOK], input=payload, capture_output=True,
                           text=True, cwd=str(cwd), env=env, timeout=30)
        out = p.stdout.strip()
        if not out:
            return "allow"
        try:
            return json.loads(out)["hookSpecificOutput"]["permissionDecision"]
        except Exception:
            return f"unparseable: {out[:120]}"

    active.write_text("2026-07-22-test-incident|3|execution")
    check("v0.5.8(a): SendMessage during active incident -> deny",
          run_sendmessage(proj, proj), "deny")
    check("v0.5.8(b): SendMessage in a planning-phase incident -> deny",
          run_sendmessage(proj, proj), "deny")
    active.unlink()
    check("v0.5.8(c): SendMessage with no active incident -> allow",
          run_sendmessage(proj, proj), "allow")
    check("v0.5.8(d): SendMessage outside any DCS project -> allow",
          run_sendmessage(bare, bare), "allow")
    active.write_text("2026-07-22-test-incident|3|execution")

    # --- EOL sensitivity (202 criterion 4): the gate's verdict must not
    # depend on line-ending representation -- git may check IAP.md out as
    # LF or CRLF (core.autocrlf / .gitattributes), and a legacy approval
    # stamp may have been computed against either representation. Content
    # built with write_bytes throughout -- write_text would normalize
    # newlines and make every fixture self-consistent by construction,
    # which is exactly why no earlier test caught this.
    eol_base_lf = b"# IAP\nobjectives...\n"
    eol_base_crlf = eol_base_lf.replace(b"\n", b"\r\n")
    eol_edited_lf = b"# IAP\nobjectives... EDITED AFTER APPROVAL\n"
    eol_edited_crlf = eol_edited_lf.replace(b"\n", b"\r\n")

    def make_eol_project(name, stamp_bytes, disk_bytes):
        proj = root / name
        inc = proj / ".dcs" / "incidents" / "eol-incident"
        inc.mkdir(parents=True)
        (proj / "src").mkdir()
        (proj / "src" / "app.py").write_bytes(b"x = 1\n")
        (proj / ".dcs" / "ACTIVE").write_text("eol-incident|3|execution")
        iap = inc / "IAP.md"
        iap.write_bytes(disk_bytes)
        digest = hashlib.sha256(stamp_bytes).hexdigest()
        (inc / "IAP-APPROVED").write_bytes(f"{digest}\napproved_by: owner\n".encode("ascii"))
        return proj

    p_lf_lf = make_eol_project("eol_lf_lf", eol_base_lf, eol_base_lf)
    check("eol: stamp=LF disk=LF -> allow",
          run_gate(p_lf_lf, p_lf_lf / "src" / "app.py"), "allow")

    p_lf_crlf = make_eol_project("eol_lf_crlf", eol_base_lf, eol_base_crlf)
    check("eol: stamp=LF disk=CRLF -> allow",
          run_gate(p_lf_crlf, p_lf_crlf / "src" / "app.py"), "allow")

    p_crlf_lf = make_eol_project("eol_crlf_lf", eol_base_crlf, eol_base_lf)
    check("eol: stamp=CRLF disk=LF -> allow",
          run_gate(p_crlf_lf, p_crlf_lf / "src" / "app.py"), "allow")

    p_crlf_crlf = make_eol_project("eol_crlf_crlf", eol_base_crlf, eol_base_crlf)
    check("eol: stamp=CRLF disk=CRLF -> allow",
          run_gate(p_crlf_crlf, p_crlf_crlf / "src" / "app.py"), "allow")

    # Negative controls: genuinely edited content post-approval must still
    # deny, in both disk representations -- without these a gate that
    # simply always allows would pass the four rows above too.
    p_neg_lf = make_eol_project("eol_neg_lf", eol_base_lf, eol_edited_lf)
    check("eol: negative control, LF disk genuinely edited -> deny",
          run_gate(p_neg_lf, p_neg_lf / "src" / "app.py"), "deny")

    p_neg_crlf = make_eol_project("eol_neg_crlf", eol_base_lf, eol_edited_crlf)
    check("eol: negative control, CRLF disk genuinely edited -> deny",
          run_gate(p_neg_crlf, p_neg_crlf / "src" / "app.py"), "deny")

    # --- IC directive: dcs/hooks/dcs_gate.py and .claude/hooks/dcs_gate.py
    # must be byte-identical -- closes the detection hole (a copy
    # divergence shipping unnoticed) rather than merely registering it.
    live_hook = Path(__file__).resolve().parent.parent / ".claude" / "hooks" / "dcs_gate.py"
    check(
        "dcs/hooks/dcs_gate.py and .claude/hooks/dcs_gate.py are byte-identical",
        Path(HOOK).read_bytes() == live_hook.read_bytes(),
        True,
    )

    # --- halt ceiling (202 criteria 1, 2, 3, 4, 5): the loop is COUNTED
    # (not merely detected), the count is MECHANICAL (a test fails if the
    # code computing it is removed), breaching the ceiling DENIES
    # automatically, and the count survives a session boundary -- two
    # independent invocations of the same fixture agree.
    FIXTURES = Path(__file__).resolve().parent / "fixtures" / "halt-ceiling"

    def halt_count_cli(incident_dir):
        p = subprocess.run(
            [sys.executable, HOOK, "--halt-count", str(incident_dir)],
            capture_output=True, text=True, timeout=30,
        )
        return p.stdout.strip()

    ten = FIXTURES / "ten-halts"
    check("halt-count: fixture (a), 10 SAFETY-HALT: entries -> 10, not 1",
          halt_count_cli(ten), "10")
    check("halt-count: fixture (a), second call -> identical count (criterion 4)",
          halt_count_cli(ten), "10")
    check("halt-count: fixture (b), below default ceiling -> 2",
          halt_count_cli(FIXTURES / "below-threshold"), "2")
    check("halt-count: fixture (c), continue does not reset -> 4",
          halt_count_cli(FIXTURES / "after-continue"), "4")
    check("halt-count: fixture (d), fresh IAP-APPROVED: stamp resets -> 0",
          halt_count_cli(FIXTURES / "fresh-stamp"), "0")
    check("halt-count: missing incident dir -> 0, not an error",
          halt_count_cli(root / "does-not-exist"), "0")

    # --- v0.6.9: field-position sentinel grammar (criteria 1-5, 5a, 5b, 5c) ---
    check("halt-count: legacy pre-sentinel grammar (criterion 5c) -> 0, not 10",
          halt_count_cli(FIXTURES / "legacy-no-sentinel"), "0")
    check("halt-count: narrative resilience (criterion 5b) -> 4, narration never counts or resets",
          halt_count_cli(FIXTURES / "narrative-resilience"), "4")
    check("halt-count: multi-line halt entry (IC addendum 4) -> 2, continuation line neither counts nor resets",
          halt_count_cli(FIXTURES / "multiline-halt-continuation"), "2")

    # --- new fixtures for revision 3 (204-TASKING/S2.md steps 4, 5): both
    # opponents of halt 2 in the new, timestamp-mandatory grammar.
    check("halt-count: quoted-entry-continuation (criterion 5 / 5b(b)) -> 3, "
          "not 0 -- an indented whole-entry quotation never anchors",
          halt_count_cli(FIXTURES / "quoted-entry-continuation"), "3")
    check("halt-count: bare-pass-no-timestamp (criterion 5b(a)) -> 4, "
          "not reset -- a bare SAFETY-PASS: line with no bracketed "
          "timestamp is a continuation, never a sentinel",
          halt_count_cli(FIXTURES / "bare-pass-no-timestamp"), "4")

    # --- criterion 1 acceptance (204-TASKING/S2.md revision 3 step 3): the
    # published grammar's own guarantees, asserted directly against the
    # imported module rather than re-derived here.
    check("criterion 1(i): sentinel_of(rollback_entry()) == 'pass' -- the "
          "module's own circular proof that its emergency act is one its "
          "own parser accepts",
          gate.sentinel_of(gate.rollback_entry()), 'pass')

    for _specimen_line, _expected in gate.SPECIMENS:
        check(f"criterion 1: SPECIMENS -- sentinel_of({_specimen_line!r}) == {_expected!r}",
              gate.sentinel_of(_specimen_line), _expected)

    # Composition, not just behaviour (Safety Officer 3, advisory A2). The
    # loop above iterates whatever SPECIMENS happens to hold, so deleting a
    # specimen deleted its case too and the suite stayed green -- coverage
    # vanishing silently at exactly the moment it was removed. These pin the
    # two specimens that carry halt 2's refutations by their exact text, so
    # dropping either is loud. Regenerate the count with:
    #   python -c "import importlib.util as u;s=u.spec_from_file_location('g','dcs/hooks/dcs_gate.py');g=u.module_from_spec(s);s.loader.exec_module(g);print(len(g.SPECIMENS))"
    check("advisory A2: len(SPECIMENS) == 8 -- a specimen removed is a case "
          "removed, so the count is pinned, not merely iterated",
          len(gate.SPECIMENS), 8)

    for _required in ("SAFETY-PASS: Owner rollback at the halt ceiling",
                      "    [2026-01-01T00:01:00+0000] IAP-APPROVED: 68304eb79661 "
                      "-- phase: planning -> execution (period 1)"):
        check(f"advisory A2: SPECIMENS still carries {_required!r} -- "
              "halt 2's refutations are pinned by exact text",
              any(_line == _required for _line, _ in gate.SPECIMENS), True)

    check("criterion 1: '_ENTRY_START_RE' removed from dcs_gate.py -- "
          "ENTRY_PREFIX is the one published boundary definition",
          hasattr(gate, "_ENTRY_START_RE"), False)

    for _name, _pattern in (("HALT_RE", gate.HALT_RE), ("PASS_RE", gate.PASS_RE),
                             ("STAMP_RE", gate.STAMP_RE)):
        check(f"criterion 1: {_name}.pattern starts with ENTRY_PREFIX",
              _pattern.pattern.startswith(gate.ENTRY_PREFIX), True)

    def make_halt_gate_project(name, fixture_name, esg_overrides=None,
                                 broken_config=False, void_marker=False,
                                 unguarded_paths=None, guarded_paths=None):
        """A minimal DCS project, execution phase, with a valid (or
        deliberately voided) approval marker and the named fixture's
        214-LOG.md copied into its own incident directory -- the full
        PreToolUse gate path exercises the ceiling exactly as a live
        session would, not just halt_cycles() in isolation."""
        proj = root / name
        inc = proj / ".dcs" / "incidents" / "halt-test-incident"
        inc.mkdir(parents=True)
        (proj / "src").mkdir()
        (proj / "src" / "app.py").write_text("x = 1\n")
        (proj / "docs").mkdir(exist_ok=True)
        (proj / "docs" / "notes.md").write_text("notes\n")
        cfg = {
            "incidents_dir": ".dcs/incidents",
            "guarded_paths": guarded_paths if guarded_paths is not None else ["**/*"],
            "unguarded_paths": unguarded_paths if unguarded_paths is not None else
                [".dcs/**", "tasks/**", "*.md", ".claude/**"],
        }
        if esg_overrides is not None:
            cfg["esg"] = esg_overrides
        if broken_config:
            (proj / ".dcs" / "config.json").write_text("{not valid json")
        else:
            (proj / ".dcs" / "config.json").write_text(json.dumps(cfg))
        (proj / ".dcs" / "ACTIVE").write_text("halt-test-incident|1|execution")
        iap = inc / "IAP.md"
        iap.write_text("# IAP\nobjectives...\n")
        digest = hashlib.sha256(iap.read_bytes()).hexdigest()
        (inc / "IAP-APPROVED").write_text(f"{digest}\napproved_by: owner\n")
        if void_marker:
            # Edit IAP.md AFTER the marker was stamped against the original
            # bytes -- the stored hash no longer matches (hash-mismatch
            # deny), independent of anything the ceiling logic does.
            iap.write_text("# IAP\nobjectives... EDITED AFTER APPROVAL\n")
        if fixture_name is not None:
            log_src = FIXTURES / fixture_name / "214-LOG.md"
            if log_src.is_file():
                (inc / "214-LOG.md").write_bytes(log_src.read_bytes())
            else:
                # 204-TASKING/S2.md step 8: a missing/renamed fixture
                # directory must COLOR the suite -- a bare
                # FileNotFoundError here would abort the whole script
                # before it ever prints its own "N/M passed" line, hiding
                # every case that runs after this one instead of failing
                # them. Record a named FAIL and continue: the project ends
                # up with no 214-LOG.md at all, which downstream checks
                # (expecting this fixture's real halt count) will then
                # also fail cleanly, rather than never running.
                check(f"fixture setup: {fixture_name}/214-LOG.md exists "
                      "(missing fixture directory must fail loudly, not "
                      "crash the whole run)", False, True)
        return proj, inc

    proj_below, _ = make_halt_gate_project("halt_below", "below-threshold")
    check("ceiling: below default threshold (fixture b) -> allow",
          run_gate(proj_below, proj_below / "src" / "app.py"), "allow")

    proj_ten, inc_ten = make_halt_gate_project("halt_ten", "ten-halts")
    check("ceiling: 10 halts >= default threshold 3 (fixture a) -> deny",
          run_gate(proj_ten, proj_ten / "src" / "app.py"), "deny")
    check("ceiling: .dcs/** bookkeeping stays writable even over the ceiling",
          run_gate(proj_ten, inc_ten / "209-post-incident.md"), "allow")

    proj_continue, _ = make_halt_gate_project("halt_continue", "after-continue")
    check("ceiling: over threshold, Owner answered continue (fixture c) -> still deny",
          run_gate(proj_continue, proj_continue / "src" / "app.py"), "deny")

    # Built from "after-continue" (4 halts, no reset) plus a genuine fresh
    # IAP-APPROVED: line appended here, rather than reusing the static
    # fresh-stamp/ fixture directly: that fixture's trailing stamp hex is
    # only valid against ITS OWN companion IAP-APPROVED file (see its
    # header), and this harness stamps every project against its own
    # dynamically-computed digest of IAP.md -- text-mode writes translate
    # newlines per-platform (the EOL-sensitivity lesson this repo already
    # paid for once), so a hardcoded hex baked into a fixture would silently
    # stop matching on a platform whose write_text() behaves differently.
    # Deriving the appended stamp's hex from the project's OWN marker file
    # at test-run time is what a real /dcs-plan run would do too.
    proj_fresh, inc_fresh = make_halt_gate_project("halt_fresh", "after-continue")
    stamp_hash = (inc_fresh / "IAP-APPROVED").read_text(encoding="utf-8-sig").splitlines()[0].strip()
    with open(inc_fresh / "214-LOG.md", "a", encoding="utf-8") as f:
        f.write(
            "\n[2026-01-01T00:08:00+0000] period 2: new IAP drafted, addressing the root cause\n"
            f"[2026-01-01T00:09:00+0000] IAP-APPROVED: {stamp_hash[:12]} -- phase: planning -> execution (period 2)\n"
        )
    check("ceiling: over threshold but a fresh IAP-APPROVED: stamp followed -> allow",
          run_gate(proj_fresh, proj_fresh / "src" / "app.py"), "allow")

    proj_custom, _ = make_halt_gate_project(
        "halt_custom_threshold", "ten-halts",
        esg_overrides={"max_halts_per_attempt": 20},
    )
    check("ceiling: custom esg.max_halts_per_attempt from config.json honored -> allow",
          run_gate(proj_custom, proj_custom / "src" / "app.py"), "allow")

    proj_nolog, _ = make_halt_gate_project("halt_nolog", None)
    check("ceiling: no 214-LOG.md at all -> allow, not deny",
          run_gate(proj_nolog, proj_nolog / "src" / "app.py"), "allow")

    proj_badlog, inc_badlog = make_halt_gate_project("halt_badlog", None)
    (inc_badlog / "214-LOG.md").write_bytes(b"\xff\xfe\x00undecodable garbage bytes\xff")
    check("ceiling: unreadable/corrupt 214-LOG.md -> allow, not deny",
          run_gate(proj_badlog, proj_badlog / "src" / "app.py"), "allow")

    # --- fail-soft (202 criterion 5 / tasking point 5): a malformed
    # config.json must not let an exception escape the ceiling's own inner
    # try/except and reach main()'s outer `except Exception: sys.exit(0)`,
    # which would silently disable the WHOLE gate -- including hash
    # enforcement -- rather than just the ceiling. Proven here with the
    # marker deliberately voided (hash mismatch): if the ceiling code were
    # ever moved ahead of marker_valid, or its guard were not total, a
    # config-triggered exception here would flip this "deny" into a false
    # "allow" and this case would catch it.
    proj_brokencfg, _ = make_halt_gate_project(
        "halt_broken_config", "ten-halts", broken_config=True, void_marker=True,
    )
    check(
        "fail-soft: malformed config.json + voided marker -> hash gate still denies",
        run_gate(proj_brokencfg, proj_brokencfg / "src" / "app.py"), "deny",
    )

    # --- 204-TASKING/S2.md step 2, criterion 14a: unguarded_paths must
    # govern the ceiling too, not just the planning branch -- load_config()
    # was never called on the execution path before this, so the ceiling
    # was the only thing that could deny, and it denied on docs/notes.md
    # regardless of what config.json declared. "*.md" is deliberately left
    # OUT of both configs below (fnmatch's "*" matches "/" too, so the
    # stock default unguarded_paths already covers docs/notes.md via
    # "*.md" and would confound this contrast) -- the only variable is
    # whether "docs/**" is declared.
    proj_docs_allowed, _ = make_halt_gate_project(
        "halt_docs_allowed", "ten-halts",
        unguarded_paths=[".dcs/**", "tasks/**", ".claude/**", "docs/**"],
    )
    check(
        "unguarded_paths: docs/notes.md over the ceiling, docs/** declared -> allow",
        run_gate(proj_docs_allowed, proj_docs_allowed / "docs" / "notes.md"), "allow",
    )

    proj_docs_denied, _ = make_halt_gate_project(
        "halt_docs_denied", "ten-halts",
        unguarded_paths=[".dcs/**", "tasks/**", ".claude/**"],
    )
    check(
        "unguarded_paths: docs/notes.md over the ceiling, docs/** NOT declared -> deny",
        run_gate(proj_docs_denied, proj_docs_denied / "docs" / "notes.md"), "deny",
    )

    # --- criterion 14a floor: .dcs/** stays writable over the ceiling even
    # when config.json's unguarded_paths doesn't mention it at all -- the
    # hardcoded exemption in main() runs before the phase branch is ever
    # reached, independent of config.
    proj_dcs_floor, inc_dcs_floor = make_halt_gate_project(
        "halt_dcs_floor", "ten-halts",
        unguarded_paths=["tasks/**", ".claude/**"],
    )
    check(
        "unguarded_paths: .dcs/** writable over the ceiling even when config doesn't declare it",
        run_gate(proj_dcs_floor, inc_dcs_floor / "209-note.md"), "allow",
    )

    # --- 204-TASKING/S2.md step 2, criterion 14b: max_halts() validation.
    # ten-halts (count=10) makes the contrast legible without inspecting
    # max_halts() directly: a REJECTED value falls back to the compiled
    # default 3, and 10 >= 3 always denies; a genuinely ACCEPTED value (20)
    # is honored, and 10 < 20 allows.
    for bad_value in ["three", 0, -1, True, 3.0]:
        proj_bad, _ = make_halt_gate_project(
            f"halt_maxhalts_{str(bad_value).replace('.', '_').replace('-', 'neg')}",
            "ten-halts", esg_overrides={"max_halts_per_attempt": bad_value},
        )
        check(
            f"max_halts validation: {bad_value!r} rejected, falls back to default 3 -> deny (10 >= 3)",
            run_gate(proj_bad, proj_bad / "src" / "app.py"), "deny",
        )

    proj_valid20, _ = make_halt_gate_project(
        "halt_maxhalts_20", "ten-halts", esg_overrides={"max_halts_per_attempt": 20},
    )
    check(
        "max_halts validation: 20 accepted -> allow (10 < 20)",
        run_gate(proj_valid20, proj_valid20 / "src" / "app.py"), "allow",
    )

    # --- criterion 5c end to end: a project whose 214-LOG.md predates the
    # sentinel grammar entirely reads as zero halts through the FULL gate
    # path, not just through halt_cycles() in isolation.
    proj_legacy, _ = make_halt_gate_project("halt_legacy", "legacy-no-sentinel")
    check(
        "criterion 5c: pre-sentinel-grammar log -> 0 halts -> allow",
        run_gate(proj_legacy, proj_legacy / "src" / "app.py"), "allow",
    )

    # --- criterion 5 / 5b: the two new fixtures through the FULL gate path
    # (204-TASKING/S2.md revision 3 step 6), not merely through
    # `--halt-count`, so the ceiling's own deny branch is exercised end to
    # end exactly as a live session would hit it.
    proj_quoted, _ = make_halt_gate_project("halt_quoted_entry", "quoted-entry-continuation")
    check(
        "ceiling: quoted-entry-continuation, indented whole-entry quote "
        "never anchors (3 >= 3) -> deny",
        run_gate(proj_quoted, proj_quoted / "src" / "app.py"), "deny",
    )

    proj_barepass, _ = make_halt_gate_project("halt_bare_pass", "bare-pass-no-timestamp")
    check(
        "ceiling: bare-pass-no-timestamp, no bracketed timestamp so it "
        "never resets (4 >= 3) -> deny",
        run_gate(proj_barepass, proj_barepass / "src" / "app.py"), "deny",
    )

    # --- criterion 5a / Tier-0 circular test (IC addendum 2, 204-TASKING/
    # S2.md revision 3 step 1): extract the copy-ready rollback ACT from the
    # DENY MESSAGE ITSELF, by the exact byte boundary dcs_gate.py itself
    # publishes (ROLLBACK_ACT_BEGIN / ROLLBACK_ACT_END) -- never a
    # hardcoded duplicate and never a "last line" heuristic. Append EXACTLY
    # those bytes and nothing else, and prove the SAME edit that was
    # denied is now allowed. No f-string anywhere below adds a field to
    # `extracted` -- revision 2's defect was exactly a test that extracted
    # a bare literal and then supplied the mandatory timestamp field
    # itself, masking the very drift this round trip exists to catch.
    proj_rollback, inc_rollback = make_halt_gate_project("halt_rollback", "after-continue")
    log_rollback = inc_rollback / "214-LOG.md"
    rollback_before = log_rollback.read_bytes()
    reason = run_gate_reason(proj_rollback, proj_rollback / "src" / "app.py")
    check("rollback: the halt ceiling denies before any rollback act", reason is not None, True)

    extracted = extract_rollback_act(reason or "")
    check(
        "rollback: deny message carries an extractable rollback act bounded "
        "by dcs_gate.py's own ROLLBACK_ACT_BEGIN / ROLLBACK_ACT_END markers",
        extracted is not None, True,
    )

    if extracted is None:
        # 204-TASKING/S2.md's named-in-advance special case: failure to
        # extract by S1's declared boundary is a deviation TO S1, not a
        # license to fall back to a "last line" heuristic -- recorded here
        # as a FAILED case (never silently dropped from the denominator),
        # which is the exact defect the IC found in revision 2's harness.
        check("rollback: performing the exact named act lifts the wall -> allow",
              False, True)
    else:
        with open(log_rollback, "ab") as f:
            f.write(extracted.encode("utf-8"))
        rollback_after = log_rollback.read_bytes()
        check(
            "rollback: appended bytes are EXACTLY the extracted act, "
            "nothing added, nothing stripped",
            rollback_after == rollback_before + extracted.encode("utf-8"), True,
        )
        # The two closing assertions of the circle (204-TASKING/S2.md step
        # 1's own words): sentinel_of(extracted) == 'pass', and appending
        # lifts the wall. Never an equality against a FRESH
        # rollback_entry() call -- the timestamp is generated per call, so
        # that equality would be false-fragile by construction.
        extracted_entry_line = extracted.split("\n", 1)[1]
        check(
            "rollback: sentinel_of() classifies the extracted act's own "
            "entry line as 'pass'",
            gate.sentinel_of(extracted_entry_line), 'pass',
        )
        check(
            "rollback: performing the exact named act lifts the wall -> allow",
            run_gate(proj_rollback, proj_rollback / "src" / "app.py"), "allow",
        )

    # --- L0-d (IC addendum 4, 204-TASKING/S2.md revision 3 step 2): a
    # 214-LOG.md that does NOT end in a trailing newline must still accept
    # the rollback act as a fresh, correctly-classified entry. Without
    # rollback_act()'s own leading newline, the appended sentinel would
    # glue onto the tail of whatever entry is already last and classify as
    # THAT entry's kind, never 'pass' -- reproducing halt 2's invisible
    # failure a third way. Built by copying "after-continue" and then
    # stripping its trailing newline (never constructed as a fresh string
    # by hand), so this exercises the same round trip as the check above,
    # just against a log lacking a final newline.
    proj_noeol, inc_noeol = make_halt_gate_project("halt_rollback_noeol", "after-continue")
    log_noeol = inc_noeol / "214-LOG.md"
    noeol_bytes = log_noeol.read_bytes().rstrip(b"\n")
    check("L0-d setup: fixture log deliberately stripped of its trailing newline",
          noeol_bytes.endswith(b"\n"), False)
    log_noeol.write_bytes(noeol_bytes)

    noeol_before = log_noeol.read_bytes()
    reason_noeol = run_gate_reason(proj_noeol, proj_noeol / "src" / "app.py")
    check(
        "L0-d: the halt ceiling denies before any rollback act, log has no "
        "trailing newline",
        reason_noeol is not None, True,
    )
    extracted_noeol = extract_rollback_act(reason_noeol or "")
    check("L0-d: deny message still carries an extractable rollback act",
          extracted_noeol is not None, True)

    if extracted_noeol is None:
        check(
            "L0-d: performing the exact named act lifts the wall even "
            "without a trailing newline -> allow",
            False, True,
        )
    else:
        with open(log_noeol, "ab") as f:
            f.write(extracted_noeol.encode("utf-8"))
        noeol_after = log_noeol.read_bytes()
        check(
            "L0-d: appended bytes are EXACTLY the extracted act, nothing "
            "added, nothing stripped",
            noeol_after == noeol_before + extracted_noeol.encode("utf-8"), True,
        )
        check(
            "L0-d: performing the exact named act lifts the wall even "
            "without a trailing newline -> allow",
            run_gate(proj_noeol, proj_noeol / "src" / "app.py"), "allow",
        )

    # --- criterion 16 (204-TASKING/S2.md revision 3 step 7): the
    # regeneration command doctrine-appendix.md publishes must produce the
    # SAME number halt_cycles() computes, on EVERY fixture (the seven old
    # ones plus the two new). Extracted by searching for the line
    # containing "--halt-count" -- the canonical string both this tasking
    # and S3's is:
    #   python .claude/hooks/dcs_gate.py --halt-count <incident-dir>
    # The only substitutions performed are the ones 204-TASKING/S2.md names
    # explicitly: the script-path token (the installed copy,
    # .claude/hooks/dcs_gate.py) for this repo's own canonical copy
    # (dcs/hooks/dcs_gate.py), the <incident-dir> placeholder for each
    # fixture's real path, and the interpreter invoked via sys.executable
    # rather than a bare "python" that may not resolve on every machine --
    # nothing else in the command line is rewritten. Failing to find the
    # line is itself a FAILED case for every fixture, never a silently
    # skipped one -- this criterion's own tasking says so in as many
    # words, and it is exactly the failure mode risk 6 names in advance:
    # this test reads doctrine-appendix.md, which S3 edits in parallel,
    # and until S3 has written the line this whole block is expected red
    # with a known owner, not a deviation.
    appendix_path = Path(__file__).resolve().parent.parent / "dcs" / "references" / "doctrine-appendix.md"
    appendix_text = appendix_path.read_text(encoding="utf-8")
    regen_line = None
    for _line in appendix_text.splitlines():
        if "--halt-count" in _line:
            regen_line = _line.strip().strip("`")
            break

    check("criterion 16: dcs/references/doctrine-appendix.md has a "
          "--halt-count regeneration line", regen_line is not None, True)

    ALL_HALT_FIXTURES = [
        "ten-halts", "below-threshold", "after-continue", "fresh-stamp",
        "legacy-no-sentinel", "narrative-resilience", "multiline-halt-continuation",
        "quoted-entry-continuation", "bare-pass-no-timestamp",
    ]

    if regen_line is None:
        for _fname in ALL_HALT_FIXTURES:
            check(f"criterion 16: {_fname} -- appendix regeneration command "
                  "vs halt_cycles() agree", False, True)
    else:
        _tokens = regen_line.split()
        for _fname in ALL_HALT_FIXTURES:
            _fixture_dir = FIXTURES / _fname
            _cmd = []
            for _tok in _tokens:
                if _tok.replace("\\", "/").endswith("dcs_gate.py"):
                    _cmd.append(HOOK)
                elif _tok == "<incident-dir>":
                    _cmd.append(str(_fixture_dir))
                else:
                    _cmd.append(_tok)
            if _cmd:
                _cmd[0] = sys.executable
            _p = subprocess.run(_cmd, capture_output=True, text=True, timeout=30)
            _appendix_count = _p.stdout.strip()
            _expected_count = str(gate.halt_cycles(str(_fixture_dir)))
            check(
                f"criterion 16: {_fname} -- appendix command ({_appendix_count!r}) "
                f"== halt_cycles() ({_expected_count!r})",
                _appendix_count, _expected_count,
            )

    failed = [r for r in results if not r[0]]
    print(f"\n{len(results) - len(failed)}/{len(results)} passed")
    sys.exit(1 if failed else 0)
finally:
    shutil.rmtree(root, ignore_errors=True)
