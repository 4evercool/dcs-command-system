<purpose>
The stem of the Planning P: turn an intake report into a typed incident.
Gathers intel via dcs-situation-analyst subagents, writes 201-BRIEF.md,
proposes and confirms a Type, then either runs the Type 5 express lane to
completion inline or opens a gated incident directory and hands off to
/dcs-plan.
</purpose>

<required_reading>
@$HOME/.claude/dcs/references/doctrine.md
@$HOME/.claude/dcs/references/typing.md
@$HOME/.claude/dcs/references/schemas.md
</required_reading>

<process>

## 1. Intake

`$ARGUMENTS` is the intake description — a user report, a bug, or a
reference to an `audit_results` `needs_fix` row. If it's a bare reference
(e.g. a row id) rather than a description, read enough to understand what
it's asking for before proceeding (e.g. query the row itself if the
project documents how).

**(v0.2)** Intake may also simply be `"next from the register"`. If so,
read `<project>/.dcs/esg/REGISTER.md`'s `QUEUED` rows (topmost by the
order `STRATEGY.md`'s ranked priorities implies, or table order if
`STRATEGY.md` doesn't exist) and use that row's title as the intake
description. If `REGISTER.md` doesn't exist, or exists with no `QUEUED`
rows, stop and tell the Owner there's nothing queued — run `/dcs-esg`
first, or pass a concrete intake description instead.

Determine the project root. Verify `<project>/.dcs/` exists — if not, stop
and tell the Owner to run `/dcs-init` first.

## 2. Check for an already-active incident

```bash
cat "<project>/.dcs/ACTIVE" 2>/dev/null
```

If present: **stop.** Report the active incident (slug, type, phase) and
tell the Owner to finish it (`/dcs-plan`, `/dcs-execute`, or `/dcs-close`
as appropriate — see `/dcs-status` for exactly which) or explicitly close
it before opening a new one. v0.1 is single-incident by design (doctrine's
v0.1 constraints) — this is not negotiable from within this workflow.

## 3. Spawn situation analysts

Spawn 1-2 `dcs-situation-analyst` subagents via the Task tool (in parallel,
both in one message, if using two). Give each: the intake description
verbatim, the project root, and the path to the project's `CLAUDE.md` if
it exists. If spawning two, split the angle (e.g. one on
reproduction+logs, one on codegraph impact+prior art) rather than having
both do identical work.

Collect their structured findings (`references/schemas.md` #1). If the two
disagree on something material (e.g. one finds a repro path the other
calls unreproducible), note the disagreement rather than silently picking
one — it belongs in the 201 as an open question.

## 4. Draft 201-BRIEF.md

Use `$HOME/.claude/dcs/templates/201-BRIEF.md`. Fill in Symptom, Evidence
(one bullet per finding, citation intact), Reproduction path, Blast radius,
Prior art, and Intake source. Leave Type + rationale for the next step.

## 5. Propose a Type — COMMAND POINT 1 (typing)

This is a command point (doctrine: "Transfer of command"). **If this
session is not running Fable**: spawn `dcs-commander` via Task (model
`fable`), passing the draft 201-BRIEF.md text in full; take its `typing`
decision (schemas.md #6) as the proposal and record it in the eventual
214-LOG.md as `command: typed <N> (IC=dcs-commander)`. **If this session
is Fable**, you are the IC — decide yourself using `references/typing.md`'s
triggers and concrete examples: Type 5, 3, or 1 with a one-sentence
rationale grounded in what the analysts actually found (file count, whether
the fix is obvious, whether it touches schema/architecture/shared
infrastructure). Either way, the Dispatcher never substitutes its own
typing judgment to save a spawn.

## 6. Confirm typing with the Owner

Use `AskUserQuestion`: present the proposed type + rationale, with options
to accept it or override to a different type (with the Owner's own
reason). Write the final type + rationale + confirmation outcome into
201's "Type + rationale" section.

## 7a. Type 5 — express lane

No incident directory, no `ACTIVE` file, no gate involvement at all.

1. Assemble a micro-tasking inline (not written to disk) describing the
   one-file fix directly from the 201 findings.
2. Spawn **one** `dcs-ops-specialist` via Task with that inline tasking —
   frame its territory as the single implicated file, forbidden as
   everything else, evidence required as whatever test covers it (or "run
   the repro manually" if none exists).
3. When it returns, the IC verifies the result itself: read the diff,
   run the relevant test/repro if one exists. Do not simply trust a
   `status: "done"` return without looking — Type 5 skips the Safety
   Officer specifically because the IC is expected to do this check
   personally, given the small scope.
4. Report a one-line AAR-equivalent to the Owner in chat: what was
   wrong, what changed, what was verified. This is not written to any
   file — Type 5 explicitly has no incident directory per doctrine's
   typing table.
5. Done. No `/dcs-plan`, no `/dcs-execute`, no `/dcs-close` — the
   incident never opened a gate to begin with.

## 7b. Type 3 / Type 1 — open a gated incident

1. Create `<project>/.dcs/incidents/<YYYY-MM-DD>-<slug>/` (slug: a short
   kebab-case description derived from the symptom).
2. Write the finished `201-BRIEF.md` into that directory.
3. Initialize `214-LOG.md` from the template, with the incident's slug and
   first entry (`incident opened, type {N}, phase=planning`), followed
   immediately by the command point 1 entry from step 5
   (`command: typed {N} -- <rationale> (IC=<dcs-commander|this Fable
   session>)`) — `/dcs-plan`'s pre-stamp checklist will refuse to stamp an
   approval if this entry is missing.
4. Write `<project>/.dcs/ACTIVE` with content: `<slug>|<type>|planning`
   (exact pipe-delimited format — the gate hook parses this literally).
4a. **(v0.2)** If `<project>/.dcs/esg/REGISTER.md` exists: add or update
   this incident's row — id (slug), title, type, priority, intake source,
   opened date — and set its status `QUEUED` → `ACTIVE` (or insert a new
   `ACTIVE` row if it wasn't already queued; not every incident originates
   from the register). If `REGISTER.md` doesn't exist, skip this
   sub-step — the register is optional infrastructure, not required to
   open an incident.
5. Tell the Owner the incident is open and the next step is `/dcs-plan`.

## 8. Report

Summarize what was found, the confirmed type, and (for Type 3/1) the
incident's slug and directory path, or (for Type 5) the completed fix and
verification.

</process>
