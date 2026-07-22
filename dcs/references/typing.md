# DCS Incident Typing Guide

Decided once, at the stem (`/dcs-new`), before any planning happens.
Recorded in `201-BRIEF.md` with rationale. The Owner confirms the proposed
type via `AskUserQuestion` — the IC proposes, the Owner decides.

**The rule when in doubt: type up, not down.** A Type 3 incident run with
Type-1 ceremony wastes an operational period. A Type 1 incident run with
Type-3 (or worse, Type-5) informality risks exactly the failure DCS exists
to prevent — jumping to code before the goal, the blast radius, or the
rollback plan is nailed down. The cost of over-typing is a wasted Chief
spawn; the cost of under-typing is an unreviewed architectural change.

## Type 5 — Trivial, obvious, ≤1 file

**Trigger:** The fix is so small and unambiguous that writing a 202/204/IAP
would cost more context than the fix itself.

**Concrete software examples:**
- Fixing a typo in a log message or a docstring
- Correcting an off-by-one in a single, already-tested function
- Updating a hardcoded string/constant that's clearly wrong (e.g. a stale
  version number, a wrong URL in a comment)
- A one-line null-check guard where the fix is unambiguous and the
  surrounding function is already covered by a test

**Not Type 5 if:** the "obvious" fix touches more than one file, changes a
public function signature, touches anything security- or money-adjacent
(auth, payments, SQL construction), or you find yourself writing more than
one sentence to describe it.

**Activation:** IC + 1 `dcs-ops-specialist`. No chiefs, no Safety Officer,
no incident directory, no gate.

**Approval:** None from the Owner — the IC verifies the result itself
(reads the diff, runs the relevant test if one exists) and reports a
one-line AAR-equivalent in chat.

## Type 3 — Well-scoped feature or bug

**Trigger:** The problem is understood, the fix touches a bounded, known
set of files, and a competent developer could estimate the work without
further investigation — but it's not something to wave through without a
plan.

**Concrete software examples:**
- A well-scoped bug fix touching 1-4 files with a clear root cause
- A small feature addition that follows existing patterns (new endpoint on
  an existing resource, new field on an existing model with its migration)
- A plugin-level fix (e.g. a notification-heuristic change) that doesn't touch
  shared core modules
- An audit finding (`needs_fix` row) with a concrete, describable remediation

**Not Type 3 if:** the fix requires a schema migration touching multiple
tables, spans more than ~4 files, or the root cause is still genuinely
unknown (that's more investigation before typing, not a bigger type).

**Activation:** IC + Planning Chief + 1-4 `dcs-ops-specialist` + Safety
Officer.

**Approval:** Owner approves the IAP via `AskUserQuestion` — unless (v0.2)
`.dcs/esg/DELEGATION.md` is in force and every bound holds, in which case
the IC approves on the Owner's behalf, logged per doctrine principle 12
(`plan.md` step 6). Projects without an ESG fall back to the older
`config.json → auto_approve_type3` (default `false`).

## Type 1 — Architectural, multi-file, schema, or migration

**Trigger:** The change has long-term structural consequences, touches
shared infrastructure, or is expensive/risky to reverse.

**Concrete software examples:**
- A database schema migration (new tables, altered columns with data
  backfill, changed constraints)
- A multi-file refactor that changes a widely-called function's contract
  (mixin reordering, plugin ABC changes, shared DB facade changes)
- Introducing a new architectural pattern (a new plugin category, a new
  cross-cutting concern like the DCS gate hook itself)
- Anything requiring a deploy-ordering decision (migrate-then-restart vs.
  restart-then-migrate) or a rollback plan

**Activation:** Full org — IC + Planning Chief + Logistics Chief +
specialists + Safety Officer. Optional deterministic Workflow-script
execution instead of Agent-tool fan-out (offered by `/dcs-execute`) when
the taskings are mechanical enough to script rather than delegate to a
subagent's judgment.

**Approval:** Owner approval is **mandatory** — no `auto_approve` escape
valve exists for Type 1, ever — plus a fresh sign-off at any scope change
mid-incident (a Type 1 that discovers it needs to touch an unplanned file
is a deviation, and deviations force re-approval mechanically anyway via
the IAP hash).

## Activation table (quick reference)

| Type | Planning Chief | Logistics Chief | Specialists | Safety Officer | Owner approval |
|---|---|---|---|---|---|
| 5 | no | no | 1 (inline) | no | none (IC verifies) |
| 3 | yes | no | 1-4 | yes | yes (delegable later) |
| 1 | yes | yes | 1-4 (or Workflow script) | yes | yes, mandatory, always |
