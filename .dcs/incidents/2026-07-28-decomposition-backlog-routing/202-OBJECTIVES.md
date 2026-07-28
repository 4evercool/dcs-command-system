<!--
202-OBJECTIVES.md -- written by the IC together with the Owner, at the
start of EACH operational period (/dcs-plan). Re-drafted (new file content,
same filename) each time the incident re-enters the P-loop for another
period -- the prior period's 202 is preserved in 214-LOG.md's phase-
transition history and, once complete, in AAR.md's summary, not in this
file itself.
-->

# 202 — Objectives (Operational Period 1)

**Incident:** decomposition-backlog-routing
**Period:** 1

## Goal

A defect a stem decomposes, or new intake an ESG sweep finds, that falls
below a concrete, mechanically-followable priority/triviality bar is
routed to a lighter-weight, project-documented surface instead of
automatically becoming a first-class `REGISTER.md` row. A project whose
`CLAUDE.md` documents no such surface keeps today's unconditional
behavior unchanged — this incident adds a routing option, it does not
remove the fallback.

## Acceptance criteria (the Definition of Done)

1. `dcs/workflows/new.md` step 4a's decomposition check states a
   concrete, mechanically-followable bar (e.g. a named priority tier, or
   an explicit shape test) that a split-out defect must clear before the
   step still writes it to `REGISTER.md` as `QUEUED`. Below the bar, and
   only when the project's own `CLAUDE.md` documents a lightweight
   backlog-style surface, the step routes there instead. A project whose
   `CLAUDE.md` documents none keeps the current unconditional behavior —
   no project loses portfolio visibility by omission, and the step never
   hardcodes this project's own `vault/Backlog.md` path (this project
   ships no project facts, per its own `CLAUDE.md` coding rule).
2. `dcs/workflows/esg.md` step 2's decision clusters gain the mirror
   disposition for cluster (b) (new intake found this sweep): below the
   bar, with a documented surface available, routing there is offered as
   one of the `AskUserQuestion` options; otherwise unchanged from today.
3. `dcs/references/doctrine.md` principle 4's existing text is amended in
   place — a parenthetical version note, matching this file's own
   established convention — to state the bar as a standing rule, so the
   workflow prose and the constitution agree. This is an amendment to an
   existing principle, not a new top-level one: principle numbering and
   count are unchanged.
4. `python tests/test_doctrine_integrity.py`, `python
   tests/test_dcs_gate.py`, and `python tests/test_dcs_intake.py` each
   still report a fully green run (their own `N/M passed` line, per this
   project's own `CLAUDE.md`: read that count fresh rather than restating
   one here).

## Out of scope this period

- Retroactively migrating existing `QUEUED` low-priority rows
  (`json-examples-unparsed`, `intake-nudge-telemetry`,
  `status-md-enum-drift`) to whatever lighter-weight surface this
  incident wires in — a future `/dcs-esg` sweep's decision, not this
  incident's.
- Fixing `esg-intake-writeback-gap` (`.dcs/esg/REGISTER.md`, QUEUED) —
  the separately-registered, independent-root-cause gap in `esg.md` step
  4's Record bullet (cluster (b) decisions are never written back to
  `REGISTER.md`). **Constraint carried into tactics:** the specialist
  touching `esg.md` should avoid step 4's Record-bullet lines where
  possible; if wiring this incident's new disposition genuinely requires
  touching them, say so explicitly in `214-LOG.md`/`AAR.md` so the
  sibling row can be closed as incidentally-resolved or re-scoped rather
  than silently duplicating work.
- Any change to `esg.md` step 4's park/kill handling, `new.md` step 7a's
  Type-5 express lane, or any workflow step outside step 4a / step 2's
  decision clusters.
- Renumbering or restructuring `doctrine.md`'s principle list — criterion
  3 is an amendment to principle 4's own text, not a new principle.

## Chief feedback (filled in after /dcs-plan spawns the Planning Chief)

(pending)
