# 201 — Incident Brief

**Incident:** deviation-path-proportionality
**Opened:** 2026-07-28T08:40:46+11:00
**Type:** 3

## Symptom

DCS's deviation-arbitration command point (`dcs/workflows/execute.md` step
6, `dcs/references/schemas.md` #6) offers three dispositions for a
specialist's `status: "deviation"` return — `replan`, `amend_tasking`,
`escalate_owner` — but all three converge on the identical action: edit
the plan, then run a full `/dcs-plan` pass to produce a fresh
`IAP-APPROVED` stamp, because doctrine principle 8 makes any `IAP.md`
content change void the hash unconditionally, regardless of edit size.
`amend_tasking` is a distinct label with no distinct cost — "the scale of
the response is not derived from the scale of the finding" (`vault/
Backlog.md` item 11). The same collapse reaches beyond command point 3: a
Safety-verdict fix-tasking (command point 4) that touches `IAP.md` pays
the identical full re-stamp cost, confirmed by a second, independent
field measurement below.

**Folded in by explicit Owner decision at command point 1 confirmation
(2026-07-28, `AskUserQuestion`):** this incident also carries backlog
recommendation 2 — "stop prose transcription between seats: facts move by
file reference and regenerating command; the Dispatcher copies bytes or
cites paths, never re-types values" (`vault/Decisions/
fable-review-roadmap.md`, ranked recommendation 2, and its own text:
"rides with whichever incident touches `schemas.md` first"). This
incident's territory already includes `schemas.md`, so the Owner chose to
ride it along rather than defer it. Rec 2 has no concrete, testable shape
yet in this repo — 202 must give it one, scoped to what this incident's
territory can actually carry (see "Open questions," resolved, below).

## Evidence

- `dcs/workflows/execute.md:153-173` (step 6, COMMAND POINT 3): every
  deviation disposition ends in the same instruction — "Tell the Owner to
  run `/dcs-plan` again." Lines 168-170 confirm no disposition-based
  exception: "This edit to the plan changes IAP.md's content in the next
  /dcs-plan pass — its hash will differ from IAP-APPROVED, which
  mechanically voids the current approval; that's the deviation doctrine
  working as intended."
- `agents/dcs-commander.md:55-58`: the literal disposition enum documents
  `amend_tasking` as "mechanical correction, one 204 fixed, no premise
  change — still voids the IAP hash, which is correct." The voiding is
  deliberate; only the ceremony required to produce a new valid stamp is
  disproportionate.
- `dcs/references/doctrine.md:59` (principle 8): "Editing the IAP after
  approval invalidates it automatically" — no disposition-based exception
  in doctrine text.
- `dcs/templates/IAP.md` (read directly): the IAP is self-contained by
  design — the file-territory partition table (with globs), tactics,
  objectives summary, and verification plan are embedded inline, not
  referenced by pointer. Since `plan.md` step 5 fully regenerates
  `IAP.md` on every replan pass, any tasking amendment that reaches it
  changes the hash — confirming the hash check itself is not the
  disproportion; the ceremony required to responsibly produce a new valid
  `IAP.md` (fresh Planning Chief spawn per principle 9b, full tasking
  lint 4a, command point 2, Owner approval 6b unless delegated) is.
- `dcs/hooks/dcs_gate.py`: exactly one code-level counter exists —
  `halt_cycles()` (lines 399-477, exposed via `--halt-count`), scoped to
  Safety halts only. The attempt/stamp count doctrine principle 13
  trigger (c) depends on has no code-level equivalent — it is counted
  only by the IC/Dispatcher reading `214-LOG.md` prose
  (`execute.md:83-98`), the identical "a count performed by reading prose
  is not a count" defect class `vault/Meta/building-dcs-lessons.md` §10
  documents (and which `halt_cycles()` itself was built to fix — for
  halts only, never generalized to attempts/stamps). Verified directly by
  `dcs-commander` at command point 1: `marker_valid()`
  (`dcs_gate.py:515-528`) is a pure content-hash membership check against
  `approval_digests(IAP.md)` (`:326-368`) — it cannot see how much
  ceremony produced the stamp, and trigger (c)'s tally is defined
  entirely in workflow prose over the already-published sentinel
  grammar — so a "cheap but still-counted" route is buildable at the
  workflow/doctrine layer alone, no gate-code change required.
- **Field measurement 1** —
  `.dcs/incidents/2026-07-25-halt-loop-unbounded/214-LOG.md:96-127`
  (2026-07-26T11:50–13:00): specialist S3 returns a `deviation` touching
  zero files; disposition `amend_tasking`. Full cost: IC arbitration
  spawn, transcription pass, full `/dcs-plan` run, tasking lint, second
  IC spawn (acceptance), IAP rewrite, 209 sitrep, two Owner questions,
  re-stamp — for a fix the AAR itself describes as "one derived regex...
  and reword one bullet." The Owner's own contemporaneous framing is
  logged verbatim at line 126-127: "у DCS ровно один путь для отклонения,
  и он стоит полного цикла планирования независимо от размера находки...
  Пропорциональности... нет" (DCS has exactly one path for a deviation,
  costing a full planning cycle regardless of finding size — no
  proportionality).
- **Field measurement 2** —
  `.dcs/incidents/2026-07-27-register-field-repair-path/214-LOG.md:31-44`
  (2026-07-27T20:43–22:46): Safety Halt 2 (command point 4, disposition
  `fix_taskings` — a different command point than measurement 1, same
  underlying mechanism) required a one-paragraph, IC-authored,
  `.dcs/**`-only fix — still paid a full re-stamp. Worse: minutes later,
  fixing unrelated Safety advisories inside `IAP.md` forced a second,
  unrelated re-stamp, because `dcs_gate.py`'s `marker_valid()` denies all
  non-`.dcs/**` edits (including the incident's own mandatory close-time
  `vault/` memory-routing write) the instant the marker goes stale —
  regardless of `config.json`'s `unguarded_paths`. This generalizes the
  defect: the tax is a property of `IAP.md` content changing at all,
  under any disposition, not specific to `amend_tasking`.
- **Rec 2 evidence** (`vault/Decisions/fable-review-roadmap.md`, "review
  in one paragraph"): "the dominant defect source is one seat — the
  Dispatcher re-typing facts between artifacts (9 of `prod-tools-drift`'s
  10 halts were not about the code)." A situation analyst additionally
  found 5 in-repo instances of a related, narrower drift
  (`schemas.md`-undeclared field names appearing in prompts/returns, e.g.
  `checks_run`) during this very stem's own research — cited as
  corroborating motivation, not this incident's fix surface (that
  drift is register row `prompt-vs-schema-drift`, rank 6, explicitly
  separate).

## Reproduction path

Not reproducible as a runtime crash — this is a process/ceremony defect,
not a code bug. Trace-the-logic path: (1) `execute.md` step 6 — confirm
identical end-state regardless of disposition; (2) `doctrine.md`
principle 8 — confirm no disposition-based exception; (3) `dcs_gate.py`'s
`marker_valid()`/`approval_digests()` — confirm the check is whole-file,
ceremony-blind. The two field measurements above are the actual
reproduction evidence: timestamped, first-hand `214-LOG.md` entries of
the mechanism firing live, not paraphrase.

## Blast radius (best guess at intake)

**In territory:** `dcs/workflows/execute.md`, `dcs/workflows/plan.md`,
`dcs/references/schemas.md`, `dcs/references/doctrine.md`,
`dcs/references/doctrine-appendix.md` (provenance landing site, per this
project's hot-path-diet convention), `agents/dcs-commander.md`
(disposition enum + rationale), `dcs/references/forms.md` (IAP-APPROVED
description), `dcs/templates/214-LOG.md` (only if a new sentinel grammar
is needed), `CHANGELOG.md`, `dcs/VERSION` + `package.json` (minor version
bump prep only — per `CLAUDE.md`, `npm publish` is Owner-only with a 2FA
OTP, never attempted by a session). Rec 2's fold-in is not expected to add
new files beyond this set — it lands in the same schemas.md/doctrine
layer already in scope.

**Explicitly flagged, NOT presumed in territory:** `dcs/hooks/dcs_gate.py`
+ `tests/test_dcs_gate.py`. `CLAUDE.md` rules changes to the gate hook
Type 1 by definition ("they are the enforcement mechanism itself"), and
`IAP.md`'s self-contained template structure means a design that keeps
producing a fresh stamp — just with less ceremony around producing it —
needs no gate-code change. **Standing constraint carried into planning**
(dcs-commander, command point 1): any IAP whose territory or tactics
reach `dcs/hooks/dcs_gate.py` or `tests/test_dcs_gate.py` is rejected at
command point 2 and bounced to re-typing as Type 1, never quietly
absorbed under Type 3 ceremony.

## Prior art

Register row `deviation-path-proportionality` already exists
(`.dcs/esg/REGISTER.md` line 90): Type 3, priority "H (rank 4)" (stale —
predates `criterion-unmeasured-fact`'s sweep closing 2026-07-28; not
authoritative, a fresh `/dcs-esg` would re-rank), State QUEUED, territory
matches this brief's core four files exactly — this incident transitions
that row rather than minting a new one. `vault/Backlog.md` item 11
(primary source, lines 323-350) and item 19 (lines 707-751,
`revision-preservation-map` — related, explicitly flagged by the backlog
itself as a different, disjoint candidate fix, NOT this incident's
scope). `vault/Decisions/fable-review-roadmap.md` (Owner-approved
2026-07-27 reform roadmap): this item is "Phase 2a," "cheap, ships
first," Channel 1 (workflows/doctrine only, auto-propagates via
`npm i -g`), "minor version," plus Rec 2's fold-in clause. Two AARs cited
above. `vault/Meta/building-dcs-lessons.md` §10 (prose-count defect
class — design guidance for the Planning Chief: any new counting
mechanism must be field-position-anchored like `STAMP_RE`/`halt_cycles()`,
never substring-grep) and §18.

## Open questions (surfaced by situation analysts; resolved at command
point 1 confirmation, 2026-07-28)

(a) **Resolved — Owner chose to fold in.** The roadmap doc states (twice)
"Rec 2 (transcription by reference) rides with whichever incident touches
`schemas.md` first" — and this incident's territory includes
`schemas.md`. Analysts had flagged tension with the roadmap's own claim
that Rec 2 "already landed" via `criterion-unmeasured-fact" (a reading
found narrower than Rec 2's stated scope) and recommended leaving it out
pending a fresh measurement. Presented to the Owner via `AskUserQuestion`
alongside the typing confirmation; **Owner explicitly chose "fold it in
now."** 202 must give Rec 2 concrete, testable acceptance criteria scoped
to what this incident's territory can carry — not the full breadth of
"the Dispatcher never re-types values anywhere in DCS," which is
unmeasured and would itself violate one-incident-one-defect if treated as
open-ended.

(b) **Resolved — excluded.** The roadmap's Phase 2a text also cites "a
one-line export crossing `max_files` cost a sitrep and an Owner decision
at 00:40" as supporting evidence. A situation analyst could not trace
this to any artifact in this repo — it describes a structurally different
control path (Delegation-bound crossing → escalation trigger (d) → 209
sitrep → Owner) than this incident's deviation-arbitration path, and
likely originates from the sister project (bread_bot) the roadmap's own
header names. Decomposition check result: the deviation-arbitration
defect itself is ONE defect (backlog item 11's own two in-repo AAR
measurements both trace to the identical doctrine-principle-8 /
`marker_valid()` mechanism) — the un-sourced roadmap example stays
excluded from scope.

## Type + rationale

**Proposed type:** 3

**Rationale (dcs-commander, IC seat, command point 1):** "Type 3 with a
standing constraint: verified firsthand that `marker_valid()`
(`dcs_gate.py:515-528`) is a pure content-hash check that cannot see
ceremony and that trigger (c)'s attempt tally is defined entirely in
workflow prose over the already-published `IAP-APPROVED` sentinel grammar
(`execute.md:83-98`), so the 'cheap but still-counted' route backlog item
11 names is fully buildable in the workflow/doctrine layer the
Owner-approved roadmap already scoped this to (Phase 2a, Channel 1,
'workflows/doctrine only') — making a `dcs_gate.py` touch a foreseeable
temptation rather than a foreseeable need, fenced thus: any IAP whose
territory or tactics reach `dcs/hooks/dcs_gate.py` or
`tests/test_dcs_gate.py` is rejected at command point 2 and bounced to
re-typing as Type 1, never absorbed."

**Owner confirmation:** confirmed as proposed (Type 3), via
`AskUserQuestion`, 2026-07-28. In the same gate, Owner also resolved open
question (a) above: fold Rec 2 in now, rather than leave it out.

**dcs-commander's two follow-on notes for the next `/dcs-esg`** (not this
incident's scope, recorded so they aren't lost): (1) Owner to weigh
whether a remainder of Rec 2 beyond what this incident's territory can
carry should be measured and queued as its own row; (2) generalizing
`halt_cycles()` into a code-level attempt/stamp counter
(`vault/Meta/building-dcs-lessons.md` §10) is explicitly out of this
incident's scope and is Type 1 by `CLAUDE.md` whenever done, since it
touches `dcs/hooks/dcs_gate.py` and `tests/test_dcs_gate.py`.

## Intake source (for /dcs-close to route back to)

`vault/Backlog.md` item 11, register row `deviation-path-proportionality`
(pre-existing QUEUED row to transition to ACTIVE, not a fresh row) —
queued at the 2026-07-27 ESG per the roadmap decision doc.
