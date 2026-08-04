<!--
IAP.md -- the Integrated Action Plan, written by the IC during /dcs-plan.
This is the ONLY document specialists execute against once approved -- the
single source of truth doctrine principle 3 insists on. Editing this file
after approval voids IAP-APPROVED automatically (hash mismatch) -- that is
deliberate, not a bug to route around.
-->

# IAP — Incident Action Plan

**Incident:** field-lesson-guard-bare-date-weakening
**Type:** 3
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · 203 skipped (default Type 3 activation, logged) · `204-TASKING/S1.md` `S2.md` `S3.md`

## Objectives (summary of 202)

**Goal:** an unverifiable (slugless, versionless, non-predates)
field-lesson claim becomes mechanically unrepresentable in shipped prose
again — check 20a stops accepting a bare same-line date as sufficient
identification while keeping the multi-line citation shape; the fourth
mechanically-parsed sentinel (`RECORD-CORRECTION:`) becomes visible to
check 12's census and is documented in shipped prose; both guards'
descriptions match exactly what they enforce. Rides the parent's held
deploy train.

1. Check 20a flags a same-line bare-date-only field-lesson claim; proven
   by new fixture `tests/fixtures/field-lesson-guard/bare-date-claim.md`
   + self-test. (S1)
2. Existing self-tests over `multiline-claim.md` (accepted) and
   `undated-claim.md` (flagged) pass with behaviour unchanged. (S1)
3. Every shipped citation site satisfies the strict rule, enumerated by
   the guard's own loop going green — the 3 intake-known sites reworded
   to strict forms. (S2, regex by S1)
4. Check 20a's docstring describes exactly the enforced rule. (S1)
5. The parent's identifier-stuffing removed — the invariant is "every
   identifier `bcf9468` inserted into non-claim prose is gone",
   enumerated by `git show bcf9468 -- dcs/references/doctrine-appendix.md`
   (4 sites at intake: :1, :11, :13, :669). (S2)
6. `_SENTINEL_TOKENS` names `RECORD-CORRECTION:` (S1); check 12 fully
   green: doctrine.md carries the literal token in running prose,
   convention documented in forms.md, token never inside a fenced block
   in `dcs/**/*.md` (S3).
7. Hot-path budget green — doctrine.md+schemas.md within 37 KB; any
   addition funded by a trim in the same files (166 B slack at plan
   time, it moves). (S3)
8. All three suites green in the worktree: `test_doctrine_integrity.py`,
   `test_dcs_gate.py`, `test_dcs_intake.py` (plan-time baselines
   266/266, 100/100, 18/18 — read each run's own N/M). (all + IC
   integrated run)

## Tactics (from the Planning Chief)

- **T1 — Strict identifier, broad entry filter, unchanged lookahead.**
  Drop only the `|\d{4}-\d{2}-\d{2}` alternative from `_FL_ID_RE`,
  restoring the `stash@{0}` prior-art form; keep `_FL_LINE_RE` broad and
  the one-line lookahead verbatim. Measured against the current tree
  this flags exactly 4 lines (3 sites): `doctrine-appendix.md:414`,
  `plan.md:57`+`:58`, `execute.md:231`. The multi-line shape survives.
- **T2 — Reword the citation sites; do NOT teach the grammar a W-entry
  form.** A `W\d` label indexes a section that renumbers — a paragraph
  pointer, not an incident identifier; adding it would be a new
  acceptance branch of exactly the kind under repair. All three sites
  cite W-entries already marked `predates self-hosting`, so a strict
  form exists for each.
- **T3 — Exempt non-claim mentions by NAMED LINE, never by shape.**
  `_FL_NON_CLAIM_PREFIXES`: two ASCII prefixes in
  `doctrine-appendix.md` (`# DCS Doctrine`,
  `### Field-lesson citation convention`), plus a staleness case so a
  stale exemption goes red. Strictly tighter than the shipped file-level
  doctrine.md exclusion; no shape hole.
- **T4 — One implementation, not a mirror.** The live `_FL_FILES` loop
  calls `_fl_check_file`; the self-test helper stops being a drifting
  duplicate.
- **T5 — Check 12 tuple widening is safe today, measured why.** Zero new
  population members; zero fenced occurrences of the token in `dcs/**`;
  sub-check (f) satisfied by S3's doctrine.md clause.
- **T6 — Document the fourth sentinel truthfully.** forms.md states the
  asymmetry as it is: parsed by `record_integrity.py` via
  `ENTRY_PREFIX`, NOT classified by `sentinel_of()`, not writable via
  `dcs_log.py --sentinel`.
- **T7 — Fund the doctrine.md addition in the same act.** 166 B slack at
  plan time; trim redundant prose in doctrine.md/schemas.md, report
  bytes before/after.
- **T8 — Verbatim-quoted constants are untouchable.** `GRAMMAR_LINE`,
  `ROLLBACK_BODY`, `FORMAT_LINE`/`INVOCATION` quotes: whitespace reflow
  safe, rewording not. No tasking edits `dcs/hooks/**` or
  `dcs/tools/**`.

## File-territory partition

| Specialist | Territory | Forbidden (summary — full lists in 204s) |
|---|---|---|
| S1 | `tests/test_doctrine_integrity.py`, `tests/fixtures/field-lesson-guard/**` | all of `dcs/**`, other test files, other fixture dirs, `package.json`, `.dcs/**`, `vault/**` |
| S2 | `dcs/references/doctrine-appendix.md`, `dcs/workflows/plan.md`, `dcs/workflows/execute.md` | `tests/**`, all other `dcs/references/**` and `dcs/workflows/**`, `dcs/hooks/**`, `dcs/tools/**`, `dcs/templates/**` |
| S3 | `dcs/references/forms.md`, `dcs/references/doctrine.md`, `dcs/references/schemas.md` | `tests/**`, `dcs/references/doctrine-appendix.md`, `dcs/workflows/**`, `dcs/hooks/**`, `dcs/tools/**`, `dcs/templates/**` |

**Partition status:** disjoint — parallel execution.

## Risks

1. Green is only reachable jointly: S1's strict regex reds S2's
   not-yet-reworded sites; S1's widened tuple reds sub-check (f) until
   S3's doctrine.md token lands. Each tasking carries a scoped
   self-contained command proving ITS half; each specialist names a
   peer-caused red rather than crossing territory. The authoritative
   green is the integrated run.
2. Two exact strings couple S1 and S2 without sharing a file: the
   allowlisted line-openings. A drift fails loudly via S1's staleness
   case; Safety runs `grep -c` on both as the one-line integration
   check.
3. The non-claim allowlist is itself an acceptance branch — defensible
   only while (a) keyed by named line, (b) two entries, enumerated in
   the docstring with reasons, (c) staleness-checked. Wanting a third
   entry or a pattern key is a deviation.
4. Criterion 3's command can be satisfied by re-weakening; the defences
   are criterion 1's fixture plus the Safety Officer reading the shipped
   `_FL_ID_RE` source line directly (both in the verification plan).
5. Check 12's population is discovered — a token mention in a
   `dcs/**/*.md` outside the seven-file plan-time population drags that
   file under sub-check (c); doing so is a deviation, not a judgment
   call.
6. Line budgets: plan.md 243/250, execute.md 238/250 — S2 re-measures
   with `wc -l`; a breach is a merge-time red.
7. Hot-path slack (166 B) moves; if negative after S3's addition, deepen
   the trim, never shrink the clause below truthfulness.
8. `_TERM_CENSUS` :546 'one of the three sentinels' — S1 scopes it to
   `sentinel_of()`; if a reviewer still reads it as an honesty defect,
   it is a one-line follow-up, not scope.
9. Deploy stays HELD: nothing runs `install.ps1`, touches `~/.claude/**`,
   bumps a version, or prepares a release.

## Verification plan

1. **The defect shape is unrepresentable again.**
   `python tests/test_doctrine_integrity.py 2>&1 | grep -i 'field-lesson'`:
   `bare-date-claim.md` case PASS (fixture IS flagged), `undated-claim.md`
   PASS (flagged), `multiline-claim.md` PASS (accepted), live sweep PASS.
   Then read the source, not the suite:
   `grep -n '_FL_ID_RE' -A2 tests/test_doctrine_integrity.py` must show
   three alternatives — slug, version, `predates self-hosting` — and no
   date alternative. The pairing closes criterion 3's self-referential
   loop.
2. **The 201's repro is dead.** The brief's demonstration line
   (`Field lesson 2026-07-23: ...`, no identifier either line) is now
   reported by the guard's own helper; `bare-date-claim.md` is exactly
   this shape — confirm its content matches the demonstration, not a
   weaker one.
3. **The guards describe what they do.** Read check 20a's docstring and
   check 12's comments/labels as prose: no promised strictness the regex
   doesn't keep, both named exemptions stated with reasons, the stale
   multiline comment rewritten, no surviving 'three sentinels' label
   where the code enumerates four (except explicitly `sentinel_of()`-
   scoped ones). This is a judgment check performed by reading — the
   check the parent's PASS did not perform.
4. **The stuffing is gone and did not migrate.**
   `git show bcf9468 -- dcs/references/doctrine-appendix.md` lists the
   insertions; the stuffing grep returns nothing; the four rewritten
   passages read as English with no new regex-food parentheticals;
   `grep -c '^# DCS Doctrine'` and
   `grep -c '^### Field-lesson citation convention'` both print 1.
5. **The fourth sentinel is visible and documented.** All check 12 cases
   green; population unchanged (seven files); doctrine.md carries the
   literal token; S3's fence audit prints CLEAN; forms.md's prose
   matches `record_integrity.py:419` and does NOT claim `sentinel_of()`
   recognises the token; `git diff --name-only main -- dcs/hooks/` is
   empty.
6. **Budgets hold.** Hot-path bytes non-negative slack (regenerating
   command in S3's 204), corroborated by the suite's hot-path case;
   `wc -l dcs/workflows/*.md` — plan.md and execute.md ≤ 250.
7. **All three suites green** (criterion 8): read each run's own N/M;
   the first suite should rise by the new field-lesson and
   exemption-staleness cases and by nothing else unexplained — an
   unexplained count move is itself a finding.
8. **Scope discipline.** `git diff --name-only main` lists only:
   `tests/test_doctrine_integrity.py`,
   `tests/fixtures/field-lesson-guard/bare-date-claim.md`,
   `dcs/references/doctrine-appendix.md`, `dcs/references/forms.md`,
   `dcs/references/doctrine.md`, `dcs/references/schemas.md`,
   `dcs/workflows/plan.md`, `dcs/workflows/execute.md` — no
   `dcs/hooks/**`, no `package.json`, no `dcs/VERSION`, no install
   performed.

## Deviation history (this period)

none
