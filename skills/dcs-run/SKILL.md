---
name: dcs-run
description: "DCS attended auto-chain: drives the full incident lifecycle (stem → plan → execute → close, looping operational periods as needed) from one command, pausing only at Owner AskUserQuestion gates. Use to run an incident end to end without typing each phase command by hand; pass --next to pull the top queued register item."
argument-hint: "<intake description> | --next"
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
Run the entire Planning P — `/dcs-new`'s stem, `/dcs-plan`'s planning arc,
`/dcs-execute`'s execution (looping operational periods as needed), and
`/dcs-close`'s close-out — for one incident, in sequence, by reading and
following each phase workflow's own `<process>` exactly as written.
Deviations and safety-halt-with-replan loop back into planning
automatically instead of stopping to ask the Owner to retype a command.
Every genuine Owner gate still pauses the chain: typing confirm, IAP
approval (unless the Delegation of Authority covers it), deviation/verdict
escalation to the Owner, escalation-trigger sitreps, and Owner-UAT/close.
A safety valve halts and escalates after 3 operational periods without a
close. `--next` pulls the top `QUEUED` item from `.dcs/esg/REGISTER.md`
instead of a typed intake description.
</objective>

<execution_context>
@$HOME/.claude/dcs/workflows/run.md
</execution_context>

<context>
$ARGUMENTS
</context>
