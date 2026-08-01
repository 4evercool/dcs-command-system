# 201 — Incident Brief

**Incident:** revision-preservation-map
**Opened:** 2026-08-01
**Type:** 1

## Symptom

`dcs/workflows/plan.md`'s bounded-amendment path (`## 6c.`, lines 165-220)
and the gate's hash-stamp mechanism (`dcs_gate.py`'s `marker_valid()` /
`approval_digests()`) protect only `IAP.md`'s own bytes and confirm that
every 202 acceptance criterion is still claimed by *some* tasking id (lint
4a check 6). Neither re-verifies that a criterion's actual satisfying
content survives a narrow revision aimed at a *different* named criterion.
This is not hypothetical: it already caused a real silent regression in
`register-field-repair-path` (2026-07-27) — fixing a criterion-6 halt
silently dropped an already-Safety-verified criterion-5 answer, caught only
by the Safety Officer's full manual re-read, not by any required check —
plus a compounding false-fidelity claim in the same repair (an IC's "restored
verbatim" claim was itself unverified and proved to be a reconstruction).
This is a restart: a prior attempt at this exact incident (2026-07-31,
branch `dcs/revision-preservation-map` @ `497dcd4`) was abandoned
mid-execution with an unreliable, backfilled log and no clean handover, and
per the Owner's 2026-08-01 restart decision its artifacts are prior art
only — nothing from it has landed on `main` (`grep` for "preservation"
across the three affected files returns zero hits at HEAD). The abandoned
branch has been renamed (not deleted) to
`dcs/revision-preservation-map-abandoned-2026-07-31` to preserve evidence
commit `497dcd4` while freeing the branch name for this restart.

## Evidence

- AAR.md:67-72 (`register-field-repair-path`): "A pinned-hash (or any
  payload-file-scoped) protection mechanism cannot reach `.dcs/**` prose...
  When the IC rewrote `IAP.md` to fix the criterion-6 halt, it silently
  dropped the unrelated 'Criterion 5, answered' section."
- AAR.md:82-89 (same incident): the "restored verbatim" claim "is a
  faithful reconstruction, re-verified on its own merits, not a verbatim
  recovery" — same defect shape one level up (unverified fidelity claim).
- `vault/Meta/building-dcs-lessons.md` §18 (lines 631-684), transferable
  rule verbatim (676-680): "A revision scoped to one criterion must still
  prove it preserved every other criterion's already-satisfied content —
  map each one to the section that carries it, in the file as it now
  stands, before re-stamping."
- `dcs/hooks/dcs_gate.py:515-528` (`marker_valid()`) and `:326`
  (`approval_digests()`) hash only `IAP.md`'s bytes — no other `.dcs/**`
  artifact is hash-protected at all.
- `dcs/workflows/plan.md:165-180` (`## 6c.` boundary condition 1) explicitly
  excludes mandatory bookkeeping (`214-LOG.md` appends, `IAP-APPROVED`
  rewrite, `.dcs/ACTIVE`, register transitions, 209 sitreps) from the
  screened per-artifact invariant — narrower than it first appears.
- `dcs/workflows/plan.md:67` (lint 4a check 6, "criterion coverage, both
  directions") only requires a criterion to map to *some* tasking id or
  carry a tag — never that the mapped content still satisfies it after an
  edit.
- `dcs/references/schemas.md` #2 (chief plan, lines 23-48): no field on the
  tasking object or chief-plan return is shaped to carry a
  criterion-to-artifact-section pairing — a preservation map needs either a
  new field or a deliberate decision not to add one.
- `dcs/references/doctrine.md:67` (principle 15): a preservation map is
  itself a derived, durable claim and cannot ship as a bare assertion — it
  needs the regenerating check beside it, exactly the trap the abandoned
  branch's own check 23 fell into (verified below).
- `git show 497dcd4 -- dcs/workflows/plan.md`: the abandoned attempt added
  only a step-7 prose instruction ("the IC must produce a preservation
  map... and log it in `214-LOG.md`") — discipline, not a mechanical check.
- `git show 497dcd4 -- tests/test_doctrine_integrity.py`: the abandoned
  check 23 only greps `plan.md`'s own text for the phrase "preservation
  map", a `214-LOG.md` mention, and a provenance-pointer string — it never
  checks that any real incident produced or verified an actual map.
- `git show 497dcd4` commit message, self-flagged: "NOT verified work — the
  branch is evidence for the restarted incident's stem, not a mergeable
  state."
- `vault/Post-mortems/deepseek-period-review.md:149-153` (§E), independent
  confirmation of the abandonment: "`.dcs/ACTIVE` says execution, three
  payload files modified, all artifacts... untracked, branch has zero
  commits, log backfilled with no handover note."
- `ls C:\DCS-wt`: the old worktree no longer existed on disk at stem time —
  no live resumable state remained, only the branch snapshot.
- `grep -n "preservation" dcs/workflows/plan.md tests/test_doctrine_integrity.py dcs/references/doctrine-appendix.md`
  at HEAD: zero hits in all three — the gap is current and unaddressed.
- `tests/test_doctrine_integrity.py` currently has a genuine, pre-existing,
  **independent** defect: two sections both headed `# --- 20.` (lines 1690,
  1747) with the outbound guard mislabeled `# --- 21.` (line 1790) instead
  of 22. This is **already registered separately** as
  `field-lesson-guard-vacuity` (REGISTER.md rank 4, its own row explicitly
  tasked with this fix) — noted here only because it shares this incident's
  territory file and the abandoned branch's S3 tasking had (incorrectly)
  coupled the two together; this incident does not re-open or absorb it.

## Reproduction path

not reproducible as a runtime bug: this is a missing-guard/structural gap,
no test currently fails and no code path throws today. Demonstrated by
tracing the mechanism: (1) approve an `IAP.md`, note its hash in
`IAP-APPROVED`; (2) take the `## 6c.` amendment path to fix one named
criterion, touching only the tasking(s) the triggering entry names; (3)
observe lint 4a check 6 passes as long as every criterion still maps to a
tasking id, with no check reading whether the untouched taskings' or
`IAP.md`'s content for other criteria is unchanged; (4) observe
`dcs_gate.py`'s `marker_valid()` only re-validates the new `IAP.md` hash.
The 2026-07-27 incident (`register-field-repair-path`) is the one live
field instance where this exact absence let a verified criterion's content
silently vanish, caught only by a Safety Officer's manual re-read, not by
any required check.

## Blast radius (best guess at intake)

- `dcs/workflows/plan.md` (`## 6c.` boundary conditions; step 7 pre-stamp
  checklist; lint 4a check 6) — the amendment path itself
- `dcs/references/doctrine.md` (principle 8 citation point; principle 15
  compliance for the map itself, if doctrine text needs a pointer)
- `dcs/references/doctrine-appendix.md` (provenance entry — none currently
  merged; the abandoned branch's draft section is prior art only)
- `dcs/references/schemas.md` (#2 chief-plan/tasking-object schema — a new
  field, or an explicit decision not to add one)
- `tests/test_doctrine_integrity.py` (new check — **territory collision**
  with `field-lesson-guard-vacuity` (rank 4, the duplicate-20 fix) and
  `semantic-content-loss-guard` (unranked); REGISTER.md itself defers
  sequencing among these three to the next `/dcs-esg` — the Planning Chief
  should treat this as a live constraint, not re-derive it)
- `dcs/hooks/dcs_gate.py` — confirmed **not** touched by the fix as
  currently scoped (its hash covers `IAP.md` only); flagged for the
  Planning Chief in case widening gate-level hashing is preferred over a
  doctrine/test-level check
- `agents/dcs-commander.md`, `agents/dcs-safety-officer.md` — possible,
  unconfirmed, only if the amendment-disposition mechanic or Safety's scope
  needs to formally reference the map

## Prior art

Single field origin: `register-field-repair-path` (2026-07-27, integration
commit `e17fa7f`) — full account in
`.dcs/incidents/2026-07-27-register-field-repair-path/AAR.md` (Lessons
section) and its `SAFETY.md` verdict 3 (halt 2); generalized lesson in
`vault/Meta/building-dcs-lessons.md` §18 (lines 631-684). This incident
itself was already attempted once and abandoned: branch
`dcs/revision-preservation-map-abandoned-2026-07-31` @ `497dcd4`
(2026-07-31) holds a complete, IAP-approved, partially-executed draft
(201/202/IAP/three taskings) that never merged and per the Owner's
2026-08-01 restart decision is prior art only, not resumable state — its
own step-7 prose-only fix and its check 23 (which validated wording, not
truth) are lessons in what *not* to repeat, not a sketch to resume. Full
abandonment account: `vault/Post-mortems/deepseek-period-review.md` §E.

## Type + rationale

**Proposed type:** 1
**Rationale:** Five-plus files across the amendment path, doctrine, and the
merge-time guard itself, plus a `schemas.md` #2 field decision (schema
trigger) and a prior failed attempt proving the naive fix is wrong — shared
enforcement infrastructure, expensive to reverse, mandatory Owner approval.
Decided by `dcs-commander` (model fable) at command point 1.
**Owner confirmation:** confirmed as proposed.

## Intake source (for /dcs-close to route back to)

`.dcs/esg/REGISTER.md` row `revision-preservation-map` — `vault/Backlog.md`
item 19, queued at the eighth `/dcs-esg` (2026-07-27), restarted at the
fifteenth `/dcs-esg` (2026-08-01) by Owner decision after the prior
attempt's abandonment.
