# 204 — Fix-tasking S1-fix2 (repair of Safety Halt 2, raised-altitude)

**Incident:** deviation-path-proportionality
**Period:** 1
**Specialist:** dcs-ops-specialist (fresh spawn — do not resume any
prior S1 agent, per doctrine principle 9b)
**Triggered by:** `SAFETY.md` verdict 2 (halt), refutation 1; command
point 4 disposition `fix_taskings` (dcs-commander, convergence read: SAME
CLASS as halt 1 — a boundary edited and verified against only the single
case that prompted it, three instances now); escalation trigger (b), 209
sitrep `.dcs/esg/SITREPS/deviation-path-proportionality-p1.md`, Owner
decision: **continue, raised-altitude form**, 2026-07-28T11:22:44+11:00.

## Why this tasking is shaped differently from the first two fix-taskings

Halt 1 fixed two narrow scoping defects in `## 6c.`'s boundary
condition 1/3. One of those fixes (tightening condition 1) then broke a
THIRD thing — field measurement 1, which criterion 3 requires to show a
saving — because it was verified only against the complaint that
prompted it (condition 1's over-broad second branch), never against the
full set of cases the boundary has to admit and reject correctly at the
same time. **Do not repeat that pattern.** This tasking requires you to
validate your rewritten boundary against the ENTIRE fixture set below
BEFORE you may report `status: "done"` — not just the one case this
halt's refutation named.

## Task

**(1) Rewrite boundary condition 1 as ONE per-artifact invariant**, not
an enumerated branch list. Replace the current two-branch condition with
a single test evaluated over the amendment's WHOLE real artifact set (all
files the amendment actually touches, from the triggering command-point
entry through to any `IAP.md`/`203-ORG.md` bookkeeping it necessitates):

An amendment is admissible on this axis **iff every touched artifact is
one of**:
- a `204-TASKING/*.md` file the triggering logged commander decision
  itself names (one or several — a single deviation/verdict decision may
  legitimately touch more than one tasking; do not re-impose an
  arbitrary "exactly one" cap that field measurement 1 already falsifies)
- this incident's own `IAP.md`
- this incident's own `203-ORG.md`, where the tasking-count or
  execution-mode change makes its bookkeeping a consequence of the same
  amendment

**and none of**:
- `.dcs/esg/**` (any file)
- `.dcs/config.json`
- `201-BRIEF.md`
- `202-OBJECTIVES.md`
- any acceptance-criterion text, whether in `202-OBJECTIVES.md` or in
  `IAP.md`'s own summary of it (this closes halt-2 verdict's advisory 4
  in the same pass — do not treat "criterion" as meaning only the
  202-side copy)

**(2) Fold three more boundary-text advisories from `SAFETY.md` verdict
2 into this SAME redesign pass** (do not patch them separately — they
touch the same clauses fix (1) is already rewriting):

- **Advisory 3 (failed-bound inheritance):** the delta-scoped Delegation
  re-check (from halt 1's fix) must NOT be able to turn a bound that
  failed at the last full approval into a pass. Add one clause: if the
  last full approval's own bound check failed on any bound
  (`max_files`/`max_specialists`/`forbidden_globs`/`forbidden_topics`/
  `require_tests_green`), the amendment inherits that failure and takes
  the lightweight approve/reject path (at most 1 Owner round-trip)
  rather than silently auto-approving.
- **Advisory 5 (stale ratifying entry):** `## 6c.`'s Entry conditions
  currently accept "an already-logged command-point-3/4 entry, cited by
  its timestamp" with no freshness requirement. Add: the cited entry
  must postdate the `IAP-APPROVED` stamp currently in force — an entry
  from an earlier attempt or revision ratifies nothing here, for the
  same reason step 7's own bounded exception already refuses the
  period's first-pass `command: iap_review` entry as a stand-in for a
  fresh one.

(Advisory 4 is folded into fix (1) above, not separate.)

## MANDATORY pre-return validation — do this before writing `status:
"done"`, not after

Run every check below yourself, with real commands, and report the real
output. If ANY must-admit case fails to admit, or ANY must-reject case
fails to reject, your rewrite is wrong — revise it and re-validate
before returning, do not report `done` with a known gap and a note.

**MUST-ADMIT (both, with their real savings re-derived):**

- Field measurement 1 (`.dcs/incidents/2026-07-25-halt-loop-unbounded/214-LOG.md:96-127`,
  amendment scope per line 118: `204-TASKING/S1.md` + `204-TASKING/S3.md`
  + `IAP.md` + `203-ORG.md`, four artifacts in one pass). Confirm your
  new condition 1 admits this set. Re-derive the saving with the anchored
  pattern (`grep -nE '^\[[^]]*\] (command:|ESCALATION:|IAP-APPROVED:|SAFETY-)' .dcs/incidents/2026-07-25-halt-loop-unbounded/214-LOG.md`,
  then read the matched lines raw): expect the command-point-2 spawn
  (12:30-12:35) to be skippable under your new path — 1 agent spawn
  saved.
- Field measurement 2 (`.dcs/incidents/2026-07-27-register-field-repair-path/214-LOG.md:31-44`,
  the 22:22:57 event, `IAP.md`-only scope). Confirm your new condition 1
  still admits it (it should — this event's scope is a strict subset of
  field measurement 1's admitted set). Re-derive the saving the same way:
  expect 1 Owner round-trip saved, via the delta-scoped Delegation screen
  from halt 1's fix (unchanged by this round) — do not let this
  re-derivation regress just because you touched the neighboring clause.

**MUST-REJECT (all three — confirm your new condition 1, plus the
existing conditions 2/3/4, still block each):**

- A genuine re-plan whose fix requires a NEW specialist/tasking not
  named by any already-logged command-point decision.
- An edit reaching `.dcs/esg/DELEGATION.md`, `.dcs/esg/REGISTER.md`, or
  `.dcs/config.json`.
- An edit changing an acceptance criterion's substance, whether the edit
  lands in `202-OBJECTIVES.md` or in `IAP.md`'s own summary of it.

**MUST-HOLD (re-derive from what each check actually reads, do not
assume the halt-1 fix's claim still holds after this round's edit):**

- Lint 4a checks 1, 4, and 8 are correctly degenerate under your new,
  single condition 1 (re-read `plan.md`'s check 1 at ~lines 127-130,
  check 4 at ~lines 176-177, check 8 at ~lines 198-210, and confirm each
  one's actual inputs are pinned by your rewritten condition — do not
  just restate halt 1's claim).

## File territory (may edit only within these globs — unchanged from
your prior taskings)

- `dcs/workflows/execute.md`
- `dcs/workflows/plan.md`
- `agents/dcs-commander.md`

(This round's edits are expected to land entirely in `plan.md`'s
`## 6c.` section — do not touch `execute.md` or `dcs-commander.md`
unless your validation above reveals a genuine consequential need, and
if so, name exactly why in your return.)

## Forbidden zones (unchanged)

- `dcs/hooks/**`
- `tests/**`
- `dcs/references/**`
- `dcs/templates/**`
- every other `dcs/workflows/*.md`
- every other `agents/dcs-*.md`
- `skills/**`
- `dcs/VERSION`
- `package.json`
- `CHANGELOG.md`
- `.dcs/**`
- `vault/**`

## Evidence required in the return

- `python tests/test_doctrine_integrity.py` — full tail + every FAIL
  line. Current baseline: 83/83.
- `python tests/test_dcs_gate.py` — baseline 100/100. `python
  tests/test_dcs_intake.py` — baseline 10/10.
- `git diff --stat -- dcs/hooks/dcs_gate.py tests/` — must print nothing.
- Both MUST-ADMIT re-derivations, with real anchored-grep output pasted.
- All three MUST-REJECT confirmations, stated explicitly (not just "still
  holds" — show which clause blocks each).
- The MUST-HOLD re-derivation for checks 1, 4, 8.
- Confirm `git diff --stat` shows only `plan.md` (or name the
  consequential exception).

## On discovering the plan doesn't fit reality

STOP. Do not improvise a different fix. Return `status: "deviation"` per
`references/schemas.md` #4 (ops-specialist return), with `found`,
`why_plan_wrong`, and a `proposal`. The IC will re-enter planning around
your finding. Given this is already halt-count 2 of 3, a `deviation`
return here is itself significant — say so plainly, don't soften it.
