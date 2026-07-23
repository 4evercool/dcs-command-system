# DCS Doctrine — Appendix (provenance, field lessons, background)

This file is commentary, not constitution. `doctrine.md` is the normative
core — every MUST/NEVER/definition/threshold lives there and stands on its
own. This appendix exists for humans (and the ESG) who want the *why*:
which incident taught a rule, the ICS analogy behind a mechanism, the
longer version of a rationale that doctrine only gives one clause of.
Nothing here is `@`-included by any workflow or agent — if a rule matters
to how an agent behaves, it is already in the core.

Headings below mirror the core's section names so you can jump from a
core rule straight to its story.

## Why phases, not nesting

The deeper reason DCS reaches for ICS at all: in a real incident, the
first unit on scene doesn't wait for a fully-staffed command post before
acting, and a large incident doesn't collapse into one person doing
everything either — it activates only the sections the scale demands
(this is where DCS's "scalable activation" principle comes from). ICS
solves the same problem software agent orchestration has: how do you get
disciplined division of labor without a live, ever-present supervisor.
Claude's inability to nest subagents is what forces the ICS chain of
command into a **temporal** shape instead of a live one — chiefs don't
supervise specialists in real time, they hand off a tasking and read a
report later, the same way a shift's day-chief hands off to the
night-chief through a logbook, not a phone call.

## Transfer of command

The ICS original: the person who first reports "I see fire on that
distillation tower" is never required to be the incident commander — the
first unit on scene takes the report and runs initial actions, and
command transfers to the qualified IC when they arrive. This matters
because it is the whole justification for why DCS doesn't insist the main
session itself be the smartest available model: exactly as a report can
come from whoever's on shift, a Dispatcher on any model tier can take the
initial report and run the mechanics, while the actual command judgment
transfers to a qualified seat (Fable, or the strongest tier that's
actually available) the moment a real decision is needed. The prohibition
on the Dispatcher ever quietly deciding for itself exists because that is
precisely the shortcut a tired shift-lead is tempted to take in real ICS
too — "I'll just make the call myself, no need to loop in the IC for
this one" — and it is exactly how authority erodes in both domains.

## The 14 working principles

**Principle 14 — goal drift (field lesson 2026-07-22, v0.3.2).** The
original incident that motivated this trigger: a multi-period incident's
202 objectives, redrafted at the start of period 3, had quietly grown
acceptance criteria that traced to nothing in the 201's original Symptom
section — a plausible-sounding feature had been folded in because it was
adjacent to the code being touched, not because the incident was ever
supposed to deliver it. Nobody involved thought they were doing anything
wrong in the moment; each individual 202 revision looked like a reasonable
next step from the previous one. The lesson: an incident is supposed to
*converge* on its original goal, not *accrete* new ones period over
period, and the only reliable tripwire for that drift is comparing each
new 202 against the 201 verbatim, not against the previous period's 202
(which is exactly the document that's already drifted).

## Relationship to project-specific protocols

The core rule ("DCS agents honor a project's own pre-flight protocols
inside their DCS role") was written against three concrete examples worth
keeping on record as illustrations of the pattern, not because DCS itself
knows anything about these specific protocols:

- A project that documents "query the vault before a non-trivial fix" —
  a `dcs-planning-chief` planning tactics on that project reads the
  relevant vault domain pages before proposing tactics, the same way any
  agent working in that codebase would.
- A project that documents "query the action_log before debugging" — a
  `dcs-situation-analyst` doing stem-phase intel queries it as part of
  gathering evidence for the 201, rather than reconstructing history from
  code alone.
- A project that documents "query the codegraph before a cross-file
  edit" — an ops specialist about to touch a function other code calls
  checks callers/callees first, per that project's own rule, before
  writing its 214 return.

In every case DCS discovers the protocol the same way a new human
contributor would: by reading the target project's `CLAUDE.md`. DCS never
ships assumptions about what a given project's memory system, evidence
trail, or call-graph tooling looks like.

## Automation layers

The rationale for why deploy delegation (`auto_after_close`, v0.4) is
allowed to exist at all: it is aimed specifically at an Owner who has
already watched enough routine, in-bounds ships go out correctly that
requiring their explicit go/no-go on each one has stopped teaching them
anything and started being pure latency. The safeguard that makes this
non-reckless is that delegation only ever narrows *prompts*, never
*evidence* — every ship still produces the exact same append-only log,
hash-bound approval, and register row it would have if the Owner had
typed "yes" themselves; delegation removes a keystroke, not a record.

The broader point the whole automation-layers design leans on: unattended
operation is legitimate specifically *because* the Delegation of Authority
is a written, Owner-signed artifact reviewed at a standing ESG session —
`/dcs-loop` is not DCS deciding for itself what counts as routine, it is
DCS mechanically enforcing a definition of "routine" the Owner already
wrote down. Strip away the Delegation and `/dcs-loop` degrades gracefully
to "pause at every approval," which is the honest behavior for "nothing
has been delegated yet," not a bug.

## Parallel operation

**Field lesson 2026-07-23 (worktree audit scoping, v0.4.2).** A worktree
audit run against a real project found four worktrees beyond the incident
ones the audit was designed to check: three belonging to the agent
harness itself (created under `.claude/worktrees/`, detached HEAD, names
that look generated rather than chosen) and one belonging to the deploy
script's own temporary checkout. The pre-v0.4.2 version of the audit had
no notion of "foreign" — it treated every worktree on disk as DCS's to
account for, so all four were flagged as orphans with a proposed
`git worktree remove` command. Deleting the harness's own worktrees out
from under it, or a deploy script's worktree mid-flight, would have been
actively destructive, not merely a false positive. The fix was to give
the audit a scoping test (DCS-owned = under the DCS container, or has a
`dcs/*` branch checked out; everything else is foreign) and make foreign
worktrees categorically un-flaggable, un-removable-by-DCS, mentioned at
most as a one-line footnote. The general lesson carried forward: a tool
that walks "everything on disk" needs an explicit ownership boundary
before it's safe to point cleanup suggestions at what it finds, because
disk state is shared with things that aren't the tool's business.

**Why "one worktree per division of the fire line" as the framing.** The
ICS image is literal: a wildfire's divisions are physically separate
ground, each worked by its own crew without micromanaging every other
division's moves, because the incident's overall plan already assigned
disjoint terrain. A DCS worktree is the same idea applied to a
filesystem: once the portfolio-level territory partition (principle 6)
has assigned disjoint file globs to concurrent incidents, each incident's
worktree can be worked without coordinating every edit with the others,
because the plan already guarantees they can't collide. "Main checkout as
staging area" and "deploy train as demobilization" follow the same
literal-ICS-image habit: staging is where resources marshal *before* being
released back to general availability (shipped), and demobilization is
the formal, accounted-for act of standing resources down — never an
ad hoc walk-off.

**Why three separate surfaces catch a stray worktree, not one.** The
worktree audit is detection, not correction — by design it never deletes
anything, because an automated cleanup routine that's wrong once destroys
someone's in-progress work with no recovery path. Correction is deliberately
routed through a slower, human-gated surface (the ESG's finish/park/kill
decision) specifically so that "this looks stale" and "this is safe to
delete" are never the same judgment call. The gate's `.dcs/CLOSED` zombie
rule is the last line of defense for the case where both of the first two
surfaces get skipped — a worktree that nobody audited and nobody parked
still can't be quietly reused for source edits, because the gate denies
unconditionally the moment `.dcs/CLOSED` exists in that root, IAP marker
or not. This is doctrine's only deliberately fail-closed exception to
"the gate only reads the approval marker" (principle 11) — a closed
incident's directory should never accidentally become a live one again.
