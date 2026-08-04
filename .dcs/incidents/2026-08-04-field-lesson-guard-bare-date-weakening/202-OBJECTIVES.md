<!--
202-OBJECTIVES.md -- written by the IC together with the Owner, at the
start of EACH operational period (/dcs-plan). Re-drafted (new file content,
same filename) each time the incident re-enters the P-loop for another
period -- the prior period's 202 is preserved in 214-LOG.md's phase-
transition history and, once complete, in AAR.md's summary, not in this
file itself.
-->

# 202 — Objectives (Operational Period 1)

**Incident:** field-lesson-guard-bare-date-weakening
**Period:** 1

## Goal

An unverifiable (slugless, versionless, non-predates) field-lesson claim
becomes mechanically unrepresentable in shipped prose again — check 20a
stops accepting a bare same-line date as sufficient identification while
keeping the multi-line citation shape the parent repair legitimately
enabled; the fourth mechanically-parsed sentinel (`RECORD-CORRECTION:`)
becomes visible to check 12's census and is documented in shipped prose;
and both guards' own descriptions match exactly what they enforce. The
fix rides the same held deploy train as its parent
(`field-lesson-guard-vacuity`).

## Acceptance criteria (the Definition of Done)

1. Check 20a flags a same-line bare-date-only field-lesson claim (a line
   whose only identifier is `YYYY-MM-DD`, with no incident slug, version,
   or "predates self-hosting" note on that line or the lookahead line).
   Proven by a new fixture
   `tests/fixtures/field-lesson-guard/bare-date-claim.md` and a self-test
   asserting check 20a flags it.
2. Check 20a still accepts the multi-line citation shape and still flags
   the no-identifier shape: the existing self-tests over
   `tests/fixtures/field-lesson-guard/multiline-claim.md` (accepted) and
   `undated-claim.md` (flagged) pass unchanged in behaviour.
3. Every shipped field-lesson citation site satisfies the strict rule,
   enumerated by the guard's own loop: `python
   tests/test_doctrine_integrity.py` exits 0 with the strict check 20a
   sweeping `_FL_FILES` — no site passes via same-line bare-date
   sufficiency. (The 3 sites known at intake — `doctrine-appendix.md:414`,
   `plan.md:57-58`, `execute.md:231`, as recorded in the 201 — are
   reworded to strict identifier forms, or the grammar is taught the
   W-entry citation form, per the Planning Chief's design; the criterion
   is the command going green, not the intake-time census.)
4. Check 20a's docstring (`tests/test_doctrine_integrity.py:2033-2036` at
   intake) describes exactly the rule the code enforces — no promised
   strictness the regex doesn't keep, no undocumented acceptance branch.
5. The identifier-stuffing the parent's broadened entry filter forced
   into convention prose (`doctrine-appendix.md:11,13,669` at intake —
   "(v0.5.0)"/"(v0.6.9)" jammed mid-sentence into non-claims) is
   removed, with check 20a still green over those passages.
6. `_SENTINEL_TOKENS` (`tests/test_doctrine_integrity.py:728` at intake)
   names `RECORD-CORRECTION:`, and check 12 is fully green: `doctrine.md`
   carries the literal token (sub-check (f)); the fourth sentinel's
   convention is documented in `forms.md`'s sentinel-convention
   passage(s) in running prose, placed so sub-check (d)'s fenced-line
   validation cannot misfire on it (`sentinel_of()` in `dcs/hooks/`
   remains untouched — see Out of scope).
7. The hot-path budget check stays green: `doctrine.md` + `schemas.md`
   within `HOT_PATH_BUDGET_KB` (166 B of slack measured at intake as of
   `efc3244`; regenerate with
   `python -c "import os;print(os.path.getsize('dcs/references/doctrine.md')+os.path.getsize('dcs/references/schemas.md'))"`)
   — any addition is funded by a trim in the same files.
8. All three suites green in the worktree: `python
   tests/test_doctrine_integrity.py`, `python tests/test_dcs_gate.py`,
   `python tests/test_dcs_intake.py` — each reporting its own N/M
   passed, read from the run.

## Out of scope this period

- Any edit under `dcs/hooks/**` (e.g. teaching `sentinel_of()` the
  fourth token): the 201's re-typing tripwire — reaching it is a
  deviation, never a silent widening. Check 12's documentation must
  route around it instead (criterion 6).
- Version bump / `package.json`: a deploy-train decision, not needed for
  version-sync (no bump keeps sync); the fix rides the parent's held
  train.
- The QUEUED collisions on the same test file
  (`semantic-content-loss-guard`, `shipped-set-defined-three-times`):
  their defects stay untouched here.
- `npm publish` / registry state: Owner-only, never a session act.

## Chief feedback (filled in after /dcs-plan spawns the Planning Chief)

All 8 criteria judged mechanically verifiable; no revision requested.
Four notes, adopted by the IC (logged at command point 2):
1. Criterion 3 is self-referential as written (satisfiable by
   re-weakening) — closed by criterion 1's fixture plus a Safety Officer
   duty to read the shipped `_FL_ID_RE` source line directly.
2. Criterion 5 is read as the invariant "every identifier `bcf9468`
   inserted into non-claim prose is removed", enumerated by
   `git show bcf9468 -- dcs/references/doctrine-appendix.md` — 4 sites,
   not the 3 intake line numbers (the title line :1 is the fourth).
3. Criterion 2's fixtures keep their outcomes, but the stale comment
   claiming `multiline-claim.md` is accepted via the bare date must be
   rewritten (its identifier is `predates self-hosting`) — criterion 4
   work, not a criterion 2 violation. Corollary: the parent's claim that
   the bare-date branch was *needed* for the multi-line fixture never
   held.
4. Criterion 6's forms.md prose documents the fourth sentinel's
   asymmetry truthfully (parsed by `record_integrity.py`, NOT classified
   by `sentinel_of()`, not writable via `dcs_log.py --sentinel`) —
   claiming uniformity would require `dcs/hooks/**`, which is out of
   scope.
