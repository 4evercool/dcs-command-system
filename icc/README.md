# ICC — Incident Command for Code

v0.1.0

Adapts the ICS (Incident Command System) Planning P to software
development. Core mechanic: **no source edit until an approved IAP
(Incident Action Plan) exists** — enforced by a PreToolUse hook, not by
discipline.

Chain of command is realized as phases, not nesting (subagents can't spawn
subagents): the IC (main session) spawns Opus chiefs to plan, gets Owner
(human) approval, spawns Sonnet specialists to execute, then an Opus
Safety Officer to adversarially verify. All state lives on disk in a
project's `.icc/` directory because subagents start blank and context
windows are perishable — "operational period = context window."

## Full doctrine

`references/doctrine.md` is the constitution — concept, hierarchy, the 11
working principles, incident typing, the lifecycle. Read it before reading
anything else in this package; `workflows/*.md` and `agents/*.md` quote it
rather than restate it.

## Layout

```
icc/                      # this payload — shared, read-only source material
├── VERSION
├── README.md             # this file
├── workflows/            # orchestration bodies, @-included by the skills
│   ├── init.md   new.md   plan.md   execute.md   close.md   status.md
├── references/
│   ├── doctrine.md        # the constitution
│   ├── schemas.md         # every structured-return JSON schema
│   ├── forms.md           # what each ICS-numbered file contains, who writes it
│   └── typing.md          # Type 5/3/1 decision guide
├── templates/             # skeletons the workflows fill in per incident
│   ├── 201-BRIEF.md  202-OBJECTIVES.md  203-ORG.md  204-TASKING.md
│   ├── IAP.md  214-LOG.md  AAR.md  config.json
└── hooks/
    └── icc_gate.py         # the PreToolUse gate, copied per-project by /icc-init

agents/icc-*.md             # flat files, alongside any other installed agents
skills/icc-*/SKILL.md        # one skill per command, thin @-include wrappers
```

Project-side state, created by `/icc-init`, lives in `<project>/.icc/` —
`config.json`, `ACTIVE` (present only while an incident is open — its
absence *is* the gate's open state), and `incidents/<date>-<slug>/` per
incident. See `references/doctrine.md` for the full incident-directory
layout.

## Commands

| Command | Does |
|---|---|
| `/icc-init` | Onboard a project: `.icc/` + config, copy the gate hook, ask before wiring `settings.json` |
| `/icc-new <description>` | Stem: intake → analysts → 201 brief → typing → Type 5 express lane, or open a gated incident |
| `/icc-plan` | Objectives → chiefs' tactics/partition → integrated IAP → Owner approval (hash-stamped marker) |
| `/icc-execute` | Verify marker → fan out specialists → handle deviations → binding Safety Officer verdict |
| `/icc-close` | Require green Safety verdict → AAR → lessons to project memory → release the gate |
| `/icc-status` | Read-only sitrep from disk; states exactly which command resumes the P |

## v0.1 constraints

One incident active at a time. No manifest, no updater, no multi-project
registry — each project gets its own `.icc/` via `/icc-init`; this payload
under `~/.claude/icc/` is shared, read-only source material every
project's workflows and agents `@`-include from.
