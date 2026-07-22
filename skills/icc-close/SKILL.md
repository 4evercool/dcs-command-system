---
name: icc-close
description: "ICC close-out: requires a green Safety verdict, writes the AAR, routes lessons to the project's own memory system if one is documented, flags the intake source, and releases the gate. Use when an ICC incident has passed Safety review and is ready to close."
argument-hint: "[notes]"
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
Close the active incident: require the current period's Safety Officer
verdict to be `pass`, write `AAR.md`, route lessons to the project's own
memory system per its own documented protocol (skip gracefully if none is
documented), flag the intake source for the Owner rather than touching it
directly, remove `.icc/ACTIVE` to release the gate, and deliver a final
sitrep.
</objective>

<execution_context>
@$HOME/.claude/icc/workflows/close.md
</execution_context>

<context>
$ARGUMENTS
</context>
