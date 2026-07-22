---
name: dcs-execute
description: "DCS gated execution: verify the IAP approval marker, fan out Ops Specialists per their 204 taskings, handle deviations by returning to planning, and get a binding Safety Officer verdict. Use when a DCS incident has an approved IAP ready to execute."
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
Execute the current operational period's approved IAP: confirm the
approval marker is still valid, fan out up to 4 `dcs-ops-specialist`
subagents against disjoint (or IAP-declared sequential/worktree) file
territories, route any deviation back to planning, and spawn
`dcs-safety-officer` for an adversarial, binding verdict before the period
counts as complete.
</objective>

<execution_context>
@$HOME/.claude/dcs/workflows/execute.md
</execution_context>

<context>
$ARGUMENTS
</context>
