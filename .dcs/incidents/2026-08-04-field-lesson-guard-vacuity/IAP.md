<!--
IAP.md -- the Integrated Action Plan, written by the IC during /dcs-plan.
This is the ONLY document specialists execute against once approved -- the
single source of truth doctrine principle 3 insists on. Editing this file
after approval voids IAP-APPROVED automatically (hash mismatch) -- that is
deliberate, not a bug to route around.
-->

# IAP — Incident Action Plan

**Incident:** field-lesson-guard-vacuity
**Type:** 1
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `203-ORG.md` · `204-TASKING/S1.md` · `204-TASKING/S2.md` · logistics plan below

## Objectives (summary of 202)

**Goal:** Check 20 in `tests/test_doctrine_integrity.py` catches every shipped "field lesson" mention that lacks a verifiable identifier — regardless of whether the date is on the same physical line, on the next line, or absent — and the guard's own vacuity defect class cannot recur because a self-test exercises the undated-claim path.

1. An undated "field lesson" claim (the v0.5.10 defect shape) causes check 20 to fail. Verified by: a test fixture containing a deliberately undated claim, and `python tests/test_doctrine_integrity.py` exits non-zero when that fixture is present.
2. A multi-line field-lesson citation where "field lesson" is on line N and the date on line N+1 enters the guard and is checked. Verified by: a test fixture exercising the split-line form, and the check processes it rather than skipping it.
3. `_FL_FILES` covers all shipped `dcs/` files containing "field lesson" mentions. Verified by: `grep -rl "[Ff]ield[ -]lesson" dcs/ --include='*.md' --include='*.py'` returns no shipped file outside the enumeration. At minimum, `dcs/workflows/plan.md` and `dcs/workflows/execute.md` are added.
4. No two check sections share the same number. The duplicate `--- 20.` (inbound field-presence guard at line 1975 and field-lesson citation guard at line 2032) is resolved — field-lesson guard renumbered to `20a`.
5. The guard includes a self-test: a deliberately invalid field-lesson claim in a test fixture causes `test_doctrine_integrity.py` to exit non-zero, confirming the guard would catch a new undated violation.
6. All existing tests pass: `python tests/test_dcs_gate.py`, `python tests/test_dcs_intake.py`, `python tests/test_doctrine_integrity.py` exit 0 with no regressions.
7. [IC] `doctrine-appendix.md` field-lesson mentions that would trip the repaired guard are brought into compliance — each currently-undated mention gains a date or verifiable identifier on the same line.

## Tactics (from the Planning Chief)

- Replace `_FL_LINE_RE` with a broad match (no date requirement) so every "field lesson" / "field-lesson" / "field lessons" mention enters the guard regardless of line layout
- Add bare YYYY-MM-DD dates to `_FL_ID_RE` so multi-line citations (plan.md:57-58, execute.md:231-232, 202-OBJECTIVES.md:33-34) are recognised when the date is on the next line
- Expand `_FL_FILES` to all shipped `dcs/` files containing field-lesson claims: add `dcs/workflows/plan.md` and `dcs/workflows/execute.md`
- Renumber the duplicate `--- 20.` section (field-lesson citation guard) to `20a`, leaving all subsequent section numbers undisturbed
- Add a permanent test fixture (undated claim) and a self-test assertion that the guard catches it
- Add a permanent test fixture for the multi-line form and a self-test that the guard processes it
- Bring `doctrine-appendix.md` into compliance: every "field lesson" / "field-lesson" mention on a line with no identifier gains one on the same line

## File-territory partition

| Specialist | Territory | Forbidden |
|---|---|---|
| S1 | `tests/test_doctrine_integrity.py`, `tests/fixtures/field-lesson-guard/**` | `dcs/**`, `agents/**`, `skills/**` |
| S2 | `dcs/references/doctrine-appendix.md` | `tests/**`, `dcs/workflows/**`, `dcs/templates/**`, `dcs/references/doctrine.md`, `dcs/references/schemas.md` |

**Partition status:** disjoint — parallel execution. S1 works exclusively in `tests/`; S2 works exclusively in `dcs/references/doctrine-appendix.md`. No shared files.

## Deploy / environment plan (Type 1, from the Logistics Chief)

- **Deploy path:** Standard DCS installer (`install.ps1` / `install.sh`). The test change (`tests/test_doctrine_integrity.py`) is merge-time only and does not ship; the compliance fixes in `dcs/references/doctrine-appendix.md`, `dcs/workflows/plan.md`, and `dcs/workflows/execute.md` ship with the `dcs/` payload copy.
- **Env deps:** No new env vars, no new package dependencies, no config changes. Pure test-logic and prose-compliance change.
- **Migration ordering:** None — no schema, no data, no service restart ordering.
- **Rollback plan:** Revert the merge commit and re-install. The test change is merge-time only (never deployed); prose changes are additive compliance annotations — reverting restores prior state without data loss.

## Risks

- **Sequencing: S2's identifiers must survive S1's repaired guard.** S1 changes the entry filter (`_FL_LINE_RE`) and the identifier recogniser (`_FL_ID_RE`), but `_FL_ID_RE` only grows (adds bare dates), never shrinks — any identifier S2 adds in the existing recognised forms (date, slug, version, "predates self-hosting") will survive the repair. S1 and S2 edit disjoint files and execute in parallel.
- **Blockquote content** in `doctrine-appendix.md` lines 666-668 and 733-750 contains "field lesson" mentions in quoted historical prose. These may be flagged by the broadened guard. S2 must handle them: quoted historical claims inside `>` blocks still carry the identifier of the quoting context, or S2 may add inline identifiers within the blockquote.
- **Broadened `_FL_ID_RE` false-negative:** adding bare YYYY-MM-DD dates creates a theoretical false-negative — a "field lesson" mention co-occurring with an unrelated date elsewhere on the same line would pass. No such line exists in the current codebase.
- **`doctrine-appendix.md` line 414** ("unverifiable, per the field lesson below") is a cross-reference, not a standalone claim. The broadened guard flags it. S2 resolves by adding the referenced lesson's date inline.
- **Guard becomes stricter:** adding `plan.md` and `execute.md` to `_FL_FILES` means any undated "field lesson" mention in those files that the prose fixes missed will block future merges at check 20. The prose-compliance fixes must be comprehensive — re-run `python tests/test_doctrine_integrity.py` before close to confirm check 20a is green.

## Verification plan

1. Run `python tests/test_doctrine_integrity.py`: the guard check (now 20a) passes on the real codebase (all shipped field-lesson claims carry identifiers); the two self-tests both pass (undated fixture is caught, multi-line fixture is processed).
2. Run `python tests/test_dcs_gate.py` and `python tests/test_dcs_intake.py`: both exit 0.
3. Run the 202 criterion 3 verification: `grep -rli '[Ff]ield[ -]lesson' dcs/ --include='*.md' --include='*.py'` returns only files present in `_FL_FILES`.
4. The original 201 repro: search for "field lesson" in any shipped file; every claim-shaped mention (not a heading, not a routing directive, not a guard comment) carries an identifier on the same or adjacent line.

## Deviation history (this period)

None — first IAP for this period.
