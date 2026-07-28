# AAR — After Action Report

**Incident:** deviation-path-proportionality
**Type:** 3
**Opened:** 2026-07-28
**Closed:** 2026-07-28
**Operational periods:** 1

## Outcome

All 9 acceptance criteria from `202-OBJECTIVES.md` were met, verified
independently across four Safety Officer passes (the last with zero
refutations):

1. `plan.md` gained `## 6c.`, a bounded amendment path reachable only
   from an already-logged command-point decision, costing 0 agent spawns
   and at most 1 Owner round-trip, terminating at the unmodified steps
   7-8 so `marker_valid()` and trigger (c)'s attempt tally stay exactly
   as accurate as the full replan path.
2. The path's boundary is explicit and symmetric — every attempt across
   four Safety passes to construct a genuine re-plan that reaches the
   cheap route failed.
3. Both field measurements this incident's 201 cited
   (`halt-loop-unbounded`'s S3 `amend_tasking` deviation,
   `register-field-repair-path`'s Halt-2 `fix_taskings` repair) show a
   measurable saving under the new path — 1 agent spawn and 1 Owner
   round-trip respectively — re-derived from the raw logs by the Safety
   Officer independently, not accepted from any specialist's table.
4. `dcs/hooks/dcs_gate.py` and `tests/test_dcs_gate.py` are untouched —
   confirmed empty diff at every verification pass.
5. Two `execute.md` command-point spawn prompts (deviation arbitration,
   verdict handling) now instruct citing a source instead of retyping a
   value from memory.
6. `doctrine.md` principle 15 extends "write the derivation, not the
   result" to transfer between DCS seats; `doctrine-appendix.md` carries
   correctly-attributed provenance (fixed at halt 1 — see Deviations
   below).
7. `test_doctrine_integrity.py` (83/83), `test_dcs_gate.py` (100/100),
   `test_dcs_intake.py` (10/10) all pass.
8. Hot-path budget guard passes — headroom went from 1,205 B to 719 B,
   positive throughout.
9. Version bumped `0.6.10` → `0.6.11`, atomically, with the registry
   confirmed still at `0.6.10` (no publish attempted — Owner-only, out of
   scope).

Backlog Rec 2 (transcription by reference), folded into this incident's
scope by explicit Owner decision at typing confirmation, is delivered by
criteria 5 and 6 together — no separate mechanism was needed.

## What worked

The Planning Chief's initial partition (S1: `execute.md`/`plan.md`/
`dcs-commander.md`; S2: `doctrine.md`/`doctrine-appendix.md`/
`forms.md`; S3: `VERSION`/`package.json`/`CHANGELOG.md`, sequential after
S1+S2) held for the entire incident — zero territory violations, zero
forbidden-zone edits, and zero specialist `deviation` returns across
seven specialist spawns (three original taskings plus four fix-taskings:
S1-fix1, S2-fix1, S1-fix2, S1-fix3). The
chief's own tactic — "cheapen the ceremony, never the stamp" — survived
every halt unmodified: `marker_valid()` and trigger (c)'s attempt count
were never compromised, even while the admission boundary around them
was rewritten three times. The chief's and commander's own direct
verification against the live tree (byte counts, test baselines, the
`vault/` shipping gap, real section numbers) at every command point
caught real defects before they reached execution, and the commander's
diagnosis at halt 3 — that the recurring "skip these checks, they're
provably unneeded" claim was buying nothing under the incident's own
ceremony metric — was the fix that actually held.

## Lessons

- **A fix-tasking specialist validating its own fix against fixtures it
  also invents reproduces the class of bug it is fixing.** Three
  consecutive fix-taskings each closed the hole a halt named and opened
  a different one in the same boundary, because the same reasoning wrote
  both the fix and its test. Moving fixture authorship to the IC (11
  cases, pre-specified before the specialist was spawned) broke the
  pattern on the first attempt. Candidate doctrine change queued:
  `vault/Backlog.md` item 20.
- **A "these checks are provably unneeded here, skip them" claim is
  where a boundary-condition rewrite tends to be wrong, and it is worth
  asking what the skip is actually buying before writing it.** Three of
  four refutations across this incident's halts were variations of an
  incorrectly-scoped skip-claim; the fix that held was deleting the
  optimization entirely once it was noticed the skipped checks cost 0
  agent spawns and 0 Owner round-trips — nothing — under the incident's
  own success metric.
- **The mechanical halt-ceiling counter re-anchors on every valid
  re-stamp, including a purely mechanical IC bookkeeping re-stamp with
  no fresh Owner approval** — so a halt→fix→re-stamp cycle can run
  several real halts without approaching the per-attempt ceiling. The
  doctrinal, log-wide, non-resetting triggers (b) and (c) were the
  backstop that actually fired, both times, correctly. Gap queued:
  `vault/Backlog.md` item 19.
- **"A post-pass advisory correction that touches `IAP.md`" was not a
  rare case this incident merely fixed for others** — it happened four
  times inside the incident's own execution (every IC bookkeeping
  re-stamp), independently re-confirming the exact gap
  `register-field-repair-path` first surfaced.

Full narrative: [[Meta/building-dcs-lessons]] §20 (routed at this close).

## Deviations this incident

No specialist `status: "deviation"` return, across all seven specialist
spawns (S1, S2, S3, S1-fix1, S2-fix1, S1-fix2, S1-fix3). Three Safety
halts (not deviations, no return to `/dcs-plan`):

- **Halt 1** (verdict 1): 3 refutations — the Delegation re-check
  screened the whole 201/202 text instead of the amendment's own delta
  (criterion 3 unmet for field measurement 2); lint checks 1 and 8 read
  `forbidden`, not just `territory`, so boundary condition 3 didn't
  actually make them degenerate; `doctrine-appendix.md`'s new provenance
  paragraph misattributed a third-party finding to this incident's own
  review. Fixed by two fresh specialist spawns (S1-fix1, S2-fix1).
- **Halt 2** (verdict 2), escalation trigger (b): tightening boundary
  condition 1 to fix halt 1's advisory 2 silently excluded field
  measurement 1 (a 4-artifact amendment), moving criterion 3's failure
  from one measurement to the other. Owner chose "continue,
  raised-altitude form" via a 209 sitrep. Fixed by one fresh specialist
  spawn (S1-fix2) with mandatory validation against both field
  measurements.
- **Halt 3** (verdict 3), escalation triggers (b)/(c)/(e) folded into
  one Owner decision (imminent trigger-(c) review, IC-requested ESG
  activation): the raised-altitude fix, in admitting field measurement
  1's multi-tasking case, also admitted a never-reviewed new-tasking
  case that the same "checks are degenerate" claim wrongly cleared.
  Owner chose "continue, structural fix" via an updated 209. Fixed by
  one fresh specialist spawn (S1-fix3) validated against an
  IC-authored, 11-case fixture population, with real command output for
  every case — the first fix-tasking in the incident to pass on its
  first Safety re-verification.

Every fresh spawn was a genuinely new agent, per doctrine principle 9b —
none resumed.

## Memory routing

- `vault/Meta/building-dcs-lessons.md` — new §20, "A fix's own author
  should not author its own acceptance fixtures" (the self-validation
  blind-spot pattern, the skip-claim-costs-nothing-to-not-skip finding,
  the halt-ceiling re-anchoring quirk vs. the doctrinal triggers that
  held).
- `vault/Backlog.md` — item 11 marked done (outcome summary, links to
  this AAR and §20); two new items queued for the next `/dcs-esg`: #19
  (gate-level halt-ceiling reset gap, future Type 1) and #20 (candidate
  doctrine change: fix-tasking fixtures should be IC-authored, not
  specialist-authored). **Numbered relative to this incident's own
  branch point** (`4fe3312`) — the main checkout may hold further
  uncommitted backlog items past 18 not visible from this worktree; if
  so this pair may need renumbering at merge time.
- `dcs/references/doctrine.md` and `dcs/references/doctrine-appendix.md`
  — the rule itself (principle 15's by-reference extension) and its
  provenance shipped in this incident's own integration commit
  (`e285108`), per this project's own three-store rule: rule → doctrine,
  provenance → appendix, cross-incident/meta lessons → vault.

## Intake source closure

`vault/Backlog.md` item 11 and register row `deviation-path-proportionality`
— both internal to this project's own DCS-managed vault and register, no
external production system involved, no documented routine owns their
closure. Closed directly as part of this close's own memory routing
(above), following the same convention item 12's closure used. Register
row transitions `ACTIVE` → `MERGED` mechanically at step 5a.3 below.

## Owner-UAT

No distinct Owner-UAT section was defined in this incident's IAP
verification plan — all 9 acceptance criteria were agent-verifiable
(automated test suites, byte-count measurements, anchored greps, a real
`dcs_gate.py --halt-count` run against constructed fixtures), with no
browser or manual observation involved. Nothing pending on this account.

## Safety Officer's final verdict (verbatim, from SAFETY.md)

```json
{
  "verdict": "pass",
  "refutations": [],
  "advisories": [
    "8 advisories -- artifact-hygiene and precision findings, none
    criterion-affecting. All 8 fixed directly by the IC before this
    close's integration commit (7 in plan.md, 2 in CHANGELOG.md, 1
    needed no file change since it concerned a scratchpad-only validation
    script, already correctly caveated in the verdict text itself). Full
    verbatim verdict 4, and all three prior verdicts (halts 1-3), are in
    this incident's own SAFETY.md -- not reproduced in full here per this
    project's own principle-15 discipline against duplicating a derived
    artifact; SAFETY.md is the authoritative, unabridged copy."
  ],
  "checked": "See SAFETY.md verdict 4's own checked[] array -- 26 items,
  including independent re-runs of all 3 test suites, both MEASURED
  CLAIMs, the criterion-2 boundary attack (failed to break the final
  design), and independent re-derivation of both field measurements'
  savings from the raw historical logs."
}
```
