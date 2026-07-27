# 201 — Incident Brief

**Incident:** register-field-repair-path
**Opened:** 2026-07-27
**Type:** 3

## Symptom

Owner-authorized fixes are sometimes applied entirely outside the DCS
incident lifecycle -- committed directly to a project's main checkout with
no 201, no typing decision, no worktree, no IAP, and no Safety review -- and
DCS has no documented registration path for recording such a fix
afterward. Two live specimens exist in the bread_bot project's register
(currently rows 95-96 -- row numbers have drifted from the 89-90 cited when
this incident was queued, itself evidence that a row *number* is an unstable
reference and row *id* is the only durable one) -- ids
`dcs-gate-halt-ceiling-wired` and `dcs-worktree-provisioning-local` -- each
improvising its own undocumented state annotation ("DEPLOYED" qualified by
hand-written prose meaning "deploy not applicable") because no convention
exists to reuse. This repo independently hit the identical shape once, with
a THIRD, different ad hoc label (`package-json-description-corruption`,
`KILLED` + an "out-of-band" outcome note) -- evidence the gap is structural
to DCS, not specific to one project.

## Evidence

- bread_bot `.dcs/esg/REGISTER.md` rows 95-96 (read directly): State
  "**DEPLOYED** по конвенции «деплой не применяется» (см. Outcome)", Worktree
  "-- (field repair done in the main checkout, no worktree of its own)",
  Branch "-- (commit straight to main, no branch)", Outcome ending "Field
  repair outside the incident lifecycle, recorded in the register
  retroactively in this same session." -- source: situation analyst A, direct
  read of C:\bread_bot\.dcs\esg\REGISTER.md.
- Grep for `field repair|post-hoc` (case-insensitive) across
  `dcs/workflows/*.md`, `dcs/references/doctrine.md`,
  `dcs/references/doctrine-appendix.md`, and separately across `esg.md`:
  zero hits, confirming the register row's own claimed grep result -- source:
  both situation analysts, independently re-run.
- `dcs/references/doctrine.md`'s STEM diagram (lines 92-96) and "Parallel
  operation" section (137-139): every path, including Type 5, passes through
  a 201 and a typing decision; a field repair has neither -- source: analyst
  B, direct read.
- `dcs/templates/REGISTER.md`'s `RESOLVED` state (lines 55-59, shipped by
  `direct-resolution-lane`, commit `13f557d`) is scenario-neutral at the text
  level ("no worktree was ever opened, and it never enters the deploy
  lifecycle") and does not mechanically contradict a field repair, but it
  presupposes "an incident" that was typed and completed inline (Type 5) --
  a field repair never enters DCS's process at all. No field exists for a
  diff/commit reference either. -- source: both analysts.
- This repo's own independent precedent: `package-json-description-corruption`
  (`REGISTER.md` row, `KILLED` + "Fixed out-of-band by `0428ac4`... Never
  worked as a DCS incident") -- same shape, third distinct label, not
  previously cited for this incident -- source: analyst A,
  `vault/Backlog.md` item 9.
- `vault/Decisions/fable-review-roadmap.md` (a recovered decision record from
  a third-party bread_bot/Fable review) already specifies the target shape
  for this exact gap, Phase 1 item 2: "Owner-authorized fixes applied outside
  the lifecycle get one post-hoc register row (state, one-line outcome, diff
  reference; optionally one retroactive Safety look). No incident directory,
  no 201/IAP/AAR." Phase 0 (done) produced the two bread_bot rows above as
  "the first live specimens of the field-repair convention Phase 1
  proposes." -- source: analyst A, direct read of the vault file.
- Dependency cleared: `direct-resolution-lane`'s register row now reads
  **DEPLOYED** (merge `05d63b0`, deployed via `/dcs-deploy`, content witness
  clean) -- this incident's stated "do not open until the parent closes" gate
  is satisfied -- source: both analysts, `REGISTER.md` row + `git show
  13f557d`.
- Correction to this incident's own register-row framing: the claim that
  bread_bot's Worktree/Branch cells were "invented placeholders" does not
  hold -- those cells reuse the template's pre-existing "--" convention
  correctly; what is actually undocumented anywhere is the **state-gloss
  text itself**. The row also cites the specimen path as
  `C:read_bot\.dcs\esg\REGISTER.md`, a corrupted rendering of
  `C:\bread_bot\...` -- ids and row count are otherwise correct. -- source:
  analyst A.
- `direct-resolution-lane`'s own commit (`13f557d`) deliberately did NOT
  touch `doctrine.md` or `esg.md` -- ruled forbidden at that incident's IAP
  because "no doctrine rule changes here"; its 5-file diff was
  `CHANGELOG.md`, `dcs/references/forms.md`, `dcs/templates/REGISTER.md`,
  `dcs/workflows/close.md`, `dcs/workflows/new.md`. Worth weighing at plan
  time whether this incident follows the same narrow pattern (register
  template + close-time consumers) rather than the wider estimate below. --
  source: analyst B, `git show 13f557d`.
- Distinctness check against a same-file sibling: `register-writer-map-
  completeness` (rank 14, QUEUED) is a documentation-sync gap against
  writers that already exist and function (`/dcs-loop` writing `PARKED`
  undocumented, no named `KILLED` writer). This incident is a no-writer-
  exists-at-all gap for a scenario that never runs through any DCS workflow.
  Both analysts independently concluded these are genuinely different
  defects that happen to share `dcs/templates/REGISTER.md` as territory
  (already tracked in `STRATEGY.md`'s cluster note; they cannot run `ACTIVE`
  in parallel, but are not one incident).
- Minor drift noted, likely out of this incident's territory: this repo's
  own operational `.dcs/esg/REGISTER.md` header comment (lines 25-26) still
  lists the pre-`RESOLVED` six-state enum even though rows below already use
  `RESOLVED` -- `.dcs/esg/` is unguarded/gitignored so this is a hygiene
  note, not a shipped-package defect. -- source: analyst B.
- Unrelated, pre-existing observation made while opening this incident: the
  main checkout carries an uncommitted `CHANGELOG.md` working-tree edit
  (backfilling 0.6.0-0.6.4 release notes) not authored by this incident and
  not touched by it -- flagged to the Owner at stem time, noted here so a
  later merge does not mistake it for this incident's own change.

## Reproduction path

Not reproducible: this is a documentation/convention gap, not a runtime
defect. Demonstrated by direct search (grep zero hits across
doctrine/workflows/templates for any existing carrier) plus the two live
bread_bot specimens that had to invent their own convention in its absence.

## Blast radius (best guess at intake)

- `dcs/templates/REGISTER.md` -- primary: writer-map + a documented
  field-repair row shape (state text, required Outcome content).
- `dcs/workflows/esg.md` -- possible: the sweep/record step currently only
  says "update REGISTER.md rows," which presumes a pre-existing row; may
  need a branch for "Owner reports a field repair -> post-hoc row." Refine
  at plan time -- the sibling incident found the equivalent file (`new.md`)
  unnecessary for its own narrower change.
- `dcs/references/doctrine.md` -- conditional, refine at plan time. The
  direct precedent (`direct-resolution-lane`) deliberately excluded this
  file ("no doctrine rule changes"); the Planning Chief should decide
  whether documenting a convention for work that bypasses DCS entirely is
  itself a doctrine-level statement or purely a template/workflow matter.
- `dcs/workflows/close.md`, `dcs/references/forms.md`, `CHANGELOG.md` --
  possible consumers, by analogy with the sibling incident's own diff shape.
- Explicitly NOT `dcs/workflows/new.md` -- a field repair by definition
  never runs through `/dcs-new`.

## Prior art

`direct-resolution-lane` (merged `05d63b0`, deployed 2026-07-27) is the
direct dependency and closest prior art: it added `REGISTER.md`'s `RESOLVED`
terminal state for Type-5-off-the-queue work, across exactly 5 files, and
explicitly split this incident out at its own stem (principle 4) because the
scenario differs at the root -- that work was always a typed, triaged
incident; a field repair never is.

`vault/Decisions/fable-review-roadmap.md` is a recovered decision record
(third-party review, bread_bot main session running Fable, 2026-07-27) that
already designed this exact convention in detail (Phase 1 item 2) and
produced its first two live specimens as Phase 0. It frames the convention
as: mechanical repairs with no design ambiguity run outside DCS's process,
recorded post-hoc; design changes with failure modes still run through the
full process with a Safety pass. It also proposes an eventual move to a
structured (SQLite/JSONL) register as a separate, later, Type-1
Owner-mandatory migration (Phase 2b) -- explicitly out of scope here.

This repo's own `package-json-description-corruption` row (`KILLED` +
"fixed out-of-band") is a third, independent precedent for the identical
underlying shape, not previously cited in the register row that queued this
incident.

## Decomposition check (new.md 4a)

One defect: no documented registration path exists for Owner-authorized
fixes applied outside the DCS lifecycle. This is already the product of a
prior decomposition (`direct-resolution-lane`'s stem split one asserted root
cause into three rows under principle 4); this row is manifestation (b)
alone. No further splitting found necessary -- the brief describes a single,
bounded documentation/convention change, not a model or a bundle of
independent defects.

## Type + rationale

**Proposed type:** 3
**Rationale:** The Type-1 surface already shipped: `direct-resolution-lane`
(`13f557d`, verified 5-file `--stat`) created the `RESOLVED` state under a
Safety-verified scenario-neutrality bound so this row consumes it unchanged;
what remains is a bounded prose convention across ~2-5 known template/workflow
files whose target shape is pre-designed in
`vault/Decisions/fable-review-roadmap.md` Phase 1 item 2, touching none of
the enforcement surface (`dcs/hooks`, gate tests, installer) that
`C:\DCS\CLAUDE.md` reserves for Type 1 -- `typing.md`'s "follows existing
patterns" Type-3 trigger, with the genuinely architectural piece (structured
register migration, Phase 2b) explicitly out of scope. Not Type 5: multi-file,
an open design decision at plan time (doctrine in or out, the state-gloss
wording, the `esg.md` branch), and the wording defines the boundary of
legitimate process bypass, which needs a Safety Officer to refute against.
**Owner confirmation:** confirmed as proposed.

## Intake source (for /dcs-close to route back to)

`/dcs-run --next` resolving `.dcs/esg/REGISTER.md`'s rank-1 `QUEUED` row
`register-field-repair-path` (`STRATEGY.md` seventh `/dcs-esg` session,
2026-07-27). That row was itself split from `direct-resolution-lane` at its
stem (`new.md` step 4a, command point 1, IC=dcs-commander/fable), tracing
back to a third-party DCS review recorded in
`vault/Decisions/fable-review-roadmap.md`.
