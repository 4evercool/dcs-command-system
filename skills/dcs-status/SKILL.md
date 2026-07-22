---
name: dcs-status
description: "DCS sitrep: reads .dcs/ACTIVE and the incident directory (no writes, no subagents) and states exactly which command resumes the Planning P. Use to check DCS state, especially after a context reset."
argument-hint: "[project-path]"
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

<objective>
Report the active incident's slug, type, phase, operational period, open
taskings, and Safety Officer state purely by reading files on disk — then
state exactly which command resumes the Planning P. Read-only: no writes,
no subagent spawns.
</objective>

<execution_context>
@$HOME/.claude/dcs/workflows/status.md
</execution_context>

<context>
$ARGUMENTS
</context>
