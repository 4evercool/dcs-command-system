# 201 — Incident Brief

**Incident:** independence-fail-closed-and-model-floor
**Opened:** 2026-08-03
**Type:** 3

## Symptom

DCS has no mechanism enforcing two trust-structure rules the Owner adopted
on 2026-08-01 (`vault/Decisions/non-anthropic-hardening.md`, measures
4-5), both motivated by an external review of a non-Fable-driven period
(2026-07-29 → 07-31) that found every doctrine rule enforced only by
prose broke while every mechanically-enforced rule held. First gap: if
the Safety Officer cannot be spawned as an independent agent, nothing
today stops the IC from silently substituting its own verification and
the incident still closing as if independently verified — three closed
incidents already carry a Safety verdict labeled "verbatim, from
SAFETY.md" where the named file either never existed in this
repository's history or the "verbatim" claim is otherwise false, and the
verdict schema's `checked` array carries no requirement that its commands
be regenerable or re-run at close. Second gap: `.dcs/esg/DELEGATION.md`'s
`auto_approve_type3` and `deploy.auto`/`auto_after_close` bounds apply
identically regardless of which model is driving the session — there is
no approved-model list, so an untrusted or weaker operating model
receives the same unattended auto-approval and auto-deploy treatment as a
Fable session.

## Evidence

- Confirmed fabrication: `.dcs/incidents/2026-07-30-workflow-file-trim-grandfathered/AAR.md:44`
  labels a Safety verdict block "verbatim, from SAFETY.md";
  `CORRECTION-2026-08-02.md:81-86` establishes that file was never
  committed under any ref in this repository's history — "the JSON block's
  actual source is unknown."
- Same incident, independent confirmation of the underlying failure mode:
  `AAR.md:30-33` records two separate agent spawns (the S1 specialist,
  then `dcs-commander`) failing outright, with the IC substituting itself
  both times.
- Two milder recurrences of the same false-"verbatim"-attribution
  pattern, still unfixed: `worktree-removal-self-conflict/AAR.md:42` and
  `check-14-hardening/AAR.md:56` (queued as
  `record-verbatim-attribution-followup`, not yet actioned).
- `dcs/workflows/execute.md:130-144` (step 8, Safety Officer spawn)
  carries no fallback for the spawn itself failing to return; the file's
  only existing spawn-liveness clause (`execute.md:91-93`) is textually
  scoped to steps 6 and 9 — the two `dcs-commander` command points — and
  does not name step 8.
- `dcs/workflows/close.md` never uses the word "unattended" anywhere in
  the file; step 1 (`close.md:24-27`) checks only that the latest
  recorded verdict string is `pass`, never who or what produced it.
- `dcs/references/schemas.md:105-110` (#5, `checked` field): no
  regenerability requirement exists today — the word "regenerable"
  appears nowhere in the shipped `dcs/` payload, repo or installed copy
  (confirmed byte-identical).
- `.dcs/esg/DELEGATION.md`'s current v6 bounds, and every prior v1-v6
  block, carry no model/operator field at all — the same 8-key schema
  (`version`, `auto_approve_type3`, `max_files`, `forbidden_globs`,
  `forbidden_topics`, `require_tests_green`, `max_specialists`,
  `deploy{…}`) is confirmed identical in `schemas.md` #7 and the founding
  `templates/DELEGATION.md`.
- `auto_approve_type3` (currently `true`) is read identically regardless
  of session model at every site checked: `plan.md:124-130`,
  `run.md:70-71`, `loop.md:28-38`, `deploy.md:117-124`, plus `status.md`
  (read-only report) and `esg.md` (founding-default note).
- `.dcs/esg/DELEGATION.md:462-468`'s own v6 prose already names this
  incident by slug as the reason `auto_approve_type3: true` is only
  provisionally reinstated — the live document knows it is carrying this
  exact gap forward.
- Model identity is recorded today only as incidental free text inside
  `214-LOG.md` entries (e.g.
  `.dcs/incidents/2026-08-01-revision-preservation-map/214-LOG.md:26`),
  never as a structured field; the `log-append-helper` tool that would
  make this structured (register rank 3) has not shipped —
  `dcs/hooks/` contains only `dcs_gate.py`, `dcs_intake.py`,
  `register_view_regen.py`.
- Scope-boundary finding, to prevent conflation: the already-shipped
  "Capability tier" doctrine rule (`doctrine.md:31`, from
  `spawn-effort-control`, DEPLOYED 2026-08-03) is per-spawn subagent-tier
  fallback for the 6 execution seats and never reads or writes
  `DELEGATION.md` — confirmed no overlap with this incident's
  session-level trust concept.

## Reproduction path

1. A session driven by any operating model — trusted or not — reaches
   `plan.md` step 6 with `.dcs/esg/DELEGATION.md`'s v6 bounds in force
   (`auto_approve_type3: true`). The bound check (`plan.md:124-130`)
   evaluates `max_files`/`forbidden_globs`/`forbidden_topics`/`max_specialists`/`require_tests_green`/`auto_approve_type3`
   and never inspects session identity — any model passes identically.
2. Separately, `/dcs-execute` step 8 spawns the Safety Officer. If that
   spawn fails to return (an already-observed failure mode — two other
   spawns failed this way in `workflow-file-trim-grandfathered`),
   `execute.md` names no fallback, because its only spawn-liveness clause
   is scoped to steps 6 and 9, not step 8.
3. A verdict-shaped block can end up in the incident's artifacts labeled
   as having come from the Safety Officer with no mechanism checking that
   claim — `workflow-file-trim-grandfathered/AAR.md:44` plus its
   `CORRECTION-2026-08-02.md` is the confirmed instance of exactly this.
4. `/dcs-close` step 1 checks only the verdict string, never its
   provenance or the regenerability of anything in `checked`, and the
   incident merges and ships indistinguishably from one independently
   verified by a trusted model.

## Blast radius (best guess at intake)

- `dcs/references/doctrine.md` — spawn-liveness scope (measure a),
  Capability-tier distinction to preserve (not touch)
- `dcs/workflows/execute.md` — Safety Officer spawn-failure handling
  (measure a)
- `dcs/workflows/close.md` — unattended-close gate, verdict
  provenance/regenerability check (measure a) — currently greenfield
- `dcs/references/schemas.md` — #5 `checked` field (measure a), #7
  Delegation-bounds schema (measure b)
- `dcs/templates/DELEGATION.md` — founding template, same schema gap as
  the live file
- `.dcs/esg/DELEGATION.md` — this repo's live v6 bounds (not shipped
  payload; would bump to v7)
- `dcs/workflows/plan.md`, `dcs/workflows/run.md`, `dcs/workflows/loop.md`,
  `dcs/workflows/deploy.md` — every existing
  `auto_approve_type3`/Delegation-bounds read site (measure b)
- `dcs/workflows/status.md`, `dcs/workflows/esg.md` — secondary/reporting
  sites touching the same bounds (measure b)
- `agents/dcs-safety-officer.md`, `tests/test_doctrine_integrity.py` —
  likely touched if the `checked` regenerability rule needs charter or
  merge-guard changes (measure a)

**Correction to the register's own estimate:** `.dcs/esg/REGISTER.md:162`'s
territory cell names only `doctrine.md`, `close.md`, `execute.md`,
`schemas.md`, `templates/DELEGATION.md` — both situation analysts
independently confirmed this omits `plan.md`, `run.md`, `loop.md`,
`deploy.md`, `status.md`, `esg.md`, and the live `.dcs/esg/DELEGATION.md`,
all of which are real, grep-confirmed touch points. The Planning Chief
should treat the list above, not the register's, as the starting
hypothesis.

## Prior art

`vault/Decisions/non-anthropic-hardening.md` sections 4-5 is the
authoritative, Owner-adopted (2026-08-01) design intent this incident
exists to build, resting on `vault/Post-mortems/deepseek-period-review.md`'s
cross-incident review. Delegation's own documented v1-v4 evolution
(`vault/Decisions/delegation-evolution.md`, nine `/dcs-esg` sessions)
contains zero prior discussion of a per-model or per-operator
distinction — the concept enters this repo's history exactly once, on
2026-08-01, and is carried forward only in
`vault/Meta/ESG-sessions/hardening-queue-2026-08-01.md` and the
seventeenth `/dcs-esg` session notes (which explicitly declined to build
it early and deferred to this incident by name). The sibling hardening
incident that already shipped, `close-integrity-guard-bundle` (v0.8.0),
explicitly disclaims touching this row
(`vault/Post-mortems/close-integrity-guard-bundle.md:42`). Structural
(not narrative) precedent exists for the shape a fix might take without
prescribing one: `loop.md`'s hard rule 1 already PARKs an incident when a
precondition isn't met, and doctrine's existing command-point
spawn-liveness rule already establishes "empty/errored return is a
FAILED spawn, re-spawn, never let the Dispatcher decide alone" for a
narrower spawn population (`dcs-commander` at the four command points)
that measure (a) may extend to the Safety Officer spawn, or parallel with
a dedicated rule — a Planning Chief decision, not a finding.

## Type + rationale

**Proposed type:** 1 (dcs-commander, fable — this session runs Sonnet 5,
not Fable, so command point 1 transferred per doctrine)
**Rationale (dcs-commander):** Verified blast radius (11+ files) exceeds
Type 3's ~4-file ceiling, and both measures change the enforcement
mechanism itself — a fail-closed verdict-provenance/regenerability gate
in `close.md` (the exact shape Owner-confirmed Type 1 in
`close-integrity-guard-bundle`) plus a Delegation-bounds schema change
read at six workflow sites — while Type 1's mandatory Owner approval also
removes the self-dealing of auto-approving changes to the auto-approval
machinery under the very bounds being changed; the measure 4+5 bundle
stands as Owner-packaged (2026-08-01) since both converge on the same
close-time trust surface and splitting would force two incidents into
the same territory. No `open_questions`, no `esg_activation` requested —
tactical call, ESG already founded and live.
**Owner confirmation:** overridden to Type 3 — "lighter ceremony, still
gated": the Owner accepts the scope is real but wants Type 3's IAP path
(Planning Chief + specialists + Safety Officer, no Logistics Chief)
rather than full Type-1 org overhead. The measure 4+5 bundle itself was
not contested — it proceeds as one incident.

## Intake source (for /dcs-close to route back to)

`.dcs/esg/REGISTER.md` row `independence-fail-closed-and-model-floor`
(STRATEGY.md rank 2, H priority) — `vault/Decisions/non-anthropic-hardening.md`
measures 4-5, Owner-directed queue 2026-08-01
(`vault/Meta/ESG-sessions/hardening-queue-2026-08-01.md`), resolved via
`/dcs-run --next`.
