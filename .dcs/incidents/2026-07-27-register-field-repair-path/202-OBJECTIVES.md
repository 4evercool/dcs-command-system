# 202 — Objectives (Operational Period 1)

**Incident:** register-field-repair-path
**Period:** 1 (revision 2 -- criterion 6 only, after the period-1 Safety
halt; criteria 1-5 unchanged and already Safety-verified, see 214-LOG.md)

## Goal

An Owner-authorized fix applied entirely outside the DCS incident lifecycle
(no 201, no worktree, no IAP, no Safety review) has one documented,
mechanical way to be recorded in the register afterward -- a fixed,
quotable label plus a required Outcome-content shape -- instead of each
occurrence inventing its own ad hoc prose the way bread_bot's two
specimens and this repo's own `package-json-description-corruption` row
each did independently. Consistent with this incident's own Type-3 typing
(command point 1: "no new architectural pattern" -- the `RESOLVED` state's
addition already spent that ceremony in `direct-resolution-lane`), this
documents a convention for annotating an existing register state, not for
adding an eighth state token to the enum.

## Acceptance criteria (the Definition of Done)

1. `dcs/templates/REGISTER.md` defines an exact, quotable label/phrase for
   a field-repair row (reusing an existing terminal state, not a new enum
   value) and specifies what its Worktree/Branch/Opened/Closed cells must
   read (confirming the existing "—" convention already used correctly by
   the bread_bot specimens) and what its Outcome cell must minimally
   contain: a one-line description of the fix, a diff/commit reference,
   and whether a retroactive Safety look was done.
2. The template's writer-map (or equivalent header guidance) names who may
   write a field-repair row and when, distinguishing it from every
   existing writer -- none of which today originates a row with no prior
   `QUEUED`/`ACTIVE` phase.
3. `grep` for the new convention's defining phrase across the shipped
   payload (`dcs/`, `agents/`) returns exactly one declaring site -- run
   the command yourself and record its output, consistent with check 15's
   existing rule-C shape (at most one declaring paragraph per file) rather
   than asserting the count.
4. `python tests/test_doctrine_integrity.py` passes at its own reported
   N/N after the change (cite the count from the suite's own output, per
   principle 15 -- never write the number here from memory).
5. The plan states explicitly, with a one-line reason in the IAP, whether
   `dcs/workflows/esg.md` and/or `dcs/references/doctrine.md` need a
   textual carrier for this convention -- following or deliberately
   departing from the `direct-resolution-lane` precedent, which excluded
   both on "no doctrine rule changes here" -- rather than leaving the
   question implicit in whichever files happen to get touched. [IC]
6. **(Revision 2, replacing the refuted original)** `CHANGELOG.md` records
   the change under a new `## Unreleased` heading (inserted directly above
   `## 0.6.10 — 2026-07-26`), not inside the `0.6.10` section -- re-measured
   this revision, not inherited: `npm view dcs-command-system version` and
   `npm view dcs-command-system time --json` both confirm `0.6.10` is
   already published (as of 2026-07-27T05:39:23Z), so there is no "current
   open" version section to write into. The `## 0.6.10` section must return
   to byte-for-byte equality with the published tarball's `CHANGELOG.md`
   (`npm pack dcs-command-system@0.6.10`, diff against it) -- i.e. S2's
   period-1 addition to that section is reverted, not merely supplemented.
   No version bump, no edit to `dcs/VERSION` or `package.json` (still out of
   scope). At the next real version bump, `## Unreleased` becomes that
   version's heading mechanically -- this incident does not perform that
   bump itself.

   **Original criterion 6 (period 1, revision 1) — refuted, kept for the
   record, not restored:** "`CHANGELOG.md` records the change in the
   current open (unpublished) version's section, matching every prior
   shipped change's own pattern." Refuted by the Safety Officer 2026-07-27:
   the premise was inherited from `direct-resolution-lane`'s AAR, true when
   written, stale by the time this incident used it -- 0.6.10 published 49
   minutes before this incident's own 201-BRIEF was drafted.

## Out of scope this period

- Touching bread_bot's own register, specimens, or row text in any way --
  different project; doctrine principle 6, "one session, one project."
- The structured (SQLite/JSONL) register migration -- roadmap Phase 2b,
  Type 1, Owner-mandatory, explicitly later.
- `register-writer-map-completeness`'s own scope (documenting EXISTING
  writers -- `/dcs-loop`'s `PARKED`, the missing `KILLED` writer) -- a
  distinct, already-registered incident (rank 14) that shares this file as
  territory but is not this incident's job; it cannot run `ACTIVE` in
  parallel with this one and should stay `QUEUED` until this closes.
- Retroactively reconciling or relabeling this repo's own
  `package-json-description-corruption` row.
- Adding an eighth register state token to the enum -- this incident's own
  Type-3 typing rationale rests on there being no new architectural
  surface; a proposal that expands the enum would retroactively contradict
  that call and belongs in a re-typed (likely Type 1) incident instead.
- Any change to `dcs/hooks/**`, `tests/test_dcs_gate.py`, the installer, or
  `package.json`/`bin/**` -- Delegation v4 `forbidden_globs` and
  `CLAUDE.md`'s Type-1 reservations.
- Version bump / `npm publish` -- `CLAUDE.md`: Owner-only, requires a 2FA
  OTP, never attempted by a session; `direct-resolution-lane` set the
  precedent of leaving the version unbumped in the open `CHANGELOG.md`
  section, which criterion 6 above follows.

## Chief feedback (filled in after /dcs-plan spawns the Planning Chief)

(pending)
