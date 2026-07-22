---
name: dcs-loop
description: "DCS unattended queue sweep: cycles /dcs-run --next over .dcs/esg/REGISTER.md's queued incidents, Owner involved only at real decisions. Never runs a Type 1 unattended, never deploys, and ends the turn (no self-approval, no busy-wait) at any Owner gate the Delegation doesn't cover. Use for hands-off processing of a queued incident backlog under an active Delegation of Authority."
argument-hint: "[notes]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
  - AskUserQuestion
---

<objective>
Sweep `.dcs/esg/REGISTER.md`'s `QUEUED` items one at a time, running each
through the full `/dcs-run` lifecycle, stopping cleanly when the queue is
empty. Enforces three non-negotiable hard rules regardless of Delegation
bounds: never run a Type 1 incident unattended (park it, "awaits Owner"),
never deploy from the loop (each incident stops at committed +
safety-passed, register row notes "deploy pending"), and never busy-wait
or self-approve past an Owner gate the Delegation doesn't cover (notify if
possible, confirm the pause state is on disk, end the turn). Requires an
active `.dcs/esg/` — states plainly if `auto_approve_type3` is off, since
that means every incident will still pause at IAP approval.
</objective>

<execution_context>
@$HOME/.claude/dcs/workflows/loop.md
</execution_context>

<context>
$ARGUMENTS
</context>
