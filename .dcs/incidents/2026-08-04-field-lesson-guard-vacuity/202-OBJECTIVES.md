<!--
202-OBJECTIVES.md -- written by the IC together with the Owner, at the
start of EACH operational period (/dcs-plan). Re-drafted (new file content,
same filename) each time the incident re-enters the P-loop for another
period -- the prior period's 202 is preserved in 214-LOG.md's phase-
transition history and, once complete, in AAR.md's summary, not in this
file itself.
-->

# 202 — Objectives (Operational Period 1)

**Incident:** field-lesson-guard-vacuity
**Period:** 1

## Goal

Check 20 in `tests/test_doctrine_integrity.py` catches every shipped "field lesson" mention that lacks a verifiable identifier — regardless of whether the date is on the same physical line, on the next line, or absent — and the guard's own vacuity defect class cannot recur because a self-test exercises the undated-claim path.

## Acceptance criteria (the Definition of Done)

1. An undated "field lesson" claim (the v0.5.10 defect shape — "field lesson" with no YYYY-MM-DD date on the same line) causes check 20 to fail. Verified by: a test fixture containing a deliberately undated claim, and `python tests/test_doctrine_integrity.py` exits non-zero when that fixture is present.
2. A multi-line field-lesson citation where "field lesson" is on line N and the date on line N+1 (the `202-OBJECTIVES.md:33-34` shape) enters the guard and is checked. Verified by: a test fixture exercising the split-line form, and the check processes it rather than skipping it.
3. `_FL_FILES` covers all shipped files containing "field lesson" mentions. Verified by: `grep -rl "[Ff]ield lesson" dcs/ tests/ agents/ skills/ --include='*.md' --include='*.py'` returns no shipped file outside the enumeration. At minimum, `dcs/workflows/plan.md` and `dcs/workflows/execute.md` are added.
4. No two check sections in `tests/test_doctrine_integrity.py` share the same number. The duplicate `--- 20.` (inbound field-presence guard at line 1975 and field-lesson citation guard at line 2032) is resolved — one section renumbered.
5. The guard includes a self-test: a deliberately invalid field-lesson claim in a test fixture causes `test_doctrine_integrity.py` to exit non-zero, confirming the guard would catch a new undated violation. The self-test must be part of the test suite, not a one-off manual check.
6. All existing tests pass: `python tests/test_dcs_gate.py`, `python tests/test_dcs_intake.py`, and `python tests/test_doctrine_integrity.py` exit 0 with no regressions.
7. [IC] `doctrine-appendix.md` field-lesson mentions that would trip the repaired guard are brought into compliance — each currently-undated mention (lines 1, 13, 669, 731 at HEAD) gains a date or verifiable identifier on the same line, so the repaired check 20 passes on the real codebase. The line numbers are a census (lint check 3a) — re-derive the population at execution time with `grep -n "[Ff]ield lesson" dcs/references/doctrine-appendix.md`.

## Out of scope this period

- The broader question of a general "prose-without-mechanism" guard (register row `semantic-content-loss-guard`, rank 5) — this incident fixes one specific vacuous guard, not the class of all unguarded prose claims.
- Replacing the entire check-20 architecture with a different approach (e.g., the identifier-based draft in `stash@{0}`) — this incident fixes the three specific defects in the existing guard: the line filter, the file list, and the section number. The `stash@{0}` draft is prior art, not a binding design.

## Chief feedback (filled in after /dcs-plan spawns the Planning Chief)

Criterion 3's verification command (`grep -rl "[Ff]ield lesson" dcs/ tests/ agents/ skills/`) includes `tests/test_doctrine_integrity.py` (self-referential guard comments) and `dcs/references/doctrine.md` (routing directive, not a claim). Neither belongs in `_FL_FILES`. Verification scoped to `dcs/` only; the routing-mention file (`doctrine.md:3`) is excluded by explicit rationale — it directs readers to the appendix, it does not make a field-lesson claim.

Criterion 7's line census (1, 13, 669, 731) is approximate — line 731 already carries an incident slug. S2's tasking re-derives the full population at execution time with `grep -n '[Ff]ield[ -]lesson' dcs/references/doctrine-appendix.md`.

Also noted by Chief: `_FL_ID_RE` must be broadened to recognise bare YYYY-MM-DD dates — the current regex recognises slugs, versions, and "predates self-hosting" but NOT bare dates. This is the second silent defect: once `_FL_LINE_RE` stops requiring a date on the same line, multi-line citations enter the guard but `_FL_ID_RE` cannot recognise the dates on the next line and falsely flags them. The fix is covered by S1's scope.
