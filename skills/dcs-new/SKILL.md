---
name: dcs-new
description: "DCS stem: gather intake, spawn situation analysts, write the 201 brief, type the incident (5/3/1), and either resolve it inline (Type 5) or open a gated incident directory for /dcs-plan. Use when a new bug/feature/finding needs to enter the Planning P."
argument-hint: "<description or intake reference>"
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Task
  - AskUserQuestion
---

<objective>
Turn an intake report into a typed DCS incident: reconnaissance via
`dcs-situation-analyst` subagents, a written `201-BRIEF.md`, an Owner-
confirmed Type, and either a completed Type 5 fix or a newly opened,
gated incident directory ready for `/dcs-plan`.
</objective>

<execution_context>
@$HOME/.claude/dcs/workflows/new.md
</execution_context>

<context>
$ARGUMENTS
</context>
