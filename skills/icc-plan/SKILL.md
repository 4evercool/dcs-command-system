---
name: icc-plan
description: "ICC planning arc: objectives (202) → chiefs' tactics → integrated IAP → Owner approval (hash-stamped). Use when an active ICC incident needs its operational-period plan."
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
Draft this operational period's objectives, spawn the Planning Chief (and
Logistics Chief for Type 1) to produce tactics and a file-territory-
partitioned tasking set, integrate it all into `IAP.md`, get Owner
approval via `AskUserQuestion`, and stamp the hash-bound approval marker
that opens the gate.
</objective>

<execution_context>
@$HOME/.claude/icc/workflows/plan.md
</execution_context>

<context>
$ARGUMENTS
</context>
