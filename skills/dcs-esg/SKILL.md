---
name: dcs-esg
description: "DCS strategic layer: standing ESG session (Owner chairs, main session is Chief of Staff) that sweeps the incident register and intake, sets priorities, and issues/amends the Delegation of Authority. Use for periodic portfolio review, or when the Owner wants to decide what DCS works on next rather than approving one incident's plan."
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
Run a standing strategic session above the P-loop: create or read
`.dcs/esg/{STRATEGY,DELEGATION,REGISTER}.md`, sweep the register's queued
items plus any project-documented intake sources, present a portfolio
agenda (active/queued/parked, new intake, stale items, pending sitreps,
proposed Delegation amendments), record the Owner's decisions, and hand
off to `/dcs-new` (or `/dcs-run`) for whatever gets opened. Never plans or
runs an incident itself.
</objective>

<execution_context>
@$HOME/.claude/dcs/workflows/esg.md
</execution_context>

<context>
$ARGUMENTS
</context>
