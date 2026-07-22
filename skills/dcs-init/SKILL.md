---
name: dcs-init
description: "Onboard a project into DCS: create .dcs/ state + config, copy the gate hook, and (only on explicit yes) wire it into .claude/settings.json. Use when a project needs its first DCS incident directory and PreToolUse gate."
argument-hint: "[project-path]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
---

<objective>
Onboard the target project (or the current directory) into DCS: create
`.dcs/` state, copy `dcs_gate.py` into `.claude/hooks/`, and — only after
explicit Owner consent in chat — wire the PreToolUse hook into
`.claude/settings.json` without disturbing any existing hooks there.
</objective>

<execution_context>
@$HOME/.claude/dcs/workflows/init.md
</execution_context>

<context>
$ARGUMENTS
</context>
