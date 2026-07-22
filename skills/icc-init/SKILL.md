---
name: icc-init
description: "Onboard a project into ICC: create .icc/ state + config, copy the gate hook, and (only on explicit yes) wire it into .claude/settings.json. Use when a project needs its first ICC incident directory and PreToolUse gate."
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
Onboard the target project (or the current directory) into ICC: create
`.icc/` state, copy `icc_gate.py` into `.claude/hooks/`, and — only after
explicit Owner consent in chat — wire the PreToolUse hook into
`.claude/settings.json` without disturbing any existing hooks there.
</objective>

<execution_context>
@$HOME/.claude/icc/workflows/init.md
</execution_context>

<context>
$ARGUMENTS
</context>
