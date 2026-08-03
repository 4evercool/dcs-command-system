# DCS — Development Command System

v0.1.0

Adapts the ICS (Incident Command System) Planning P to software
development. Core mechanic: **no source edit until an approved IAP
(Incident Action Plan) exists** — enforced by a PreToolUse hook, not by
discipline.

Chain of command is realized as phases, not nesting (subagents can't spawn
subagents): the IC (main session) spawns Opus chiefs to plan, gets Owner
(human) approval, spawns Sonnet specialists to execute, then an Opus
Safety Officer to adversarially verify. All state lives on disk in a
project's `.dcs/` directory because subagents start blank and context
windows are perishable — "operational period = context window."

## Full doctrine

`references/doctrine.md` is the constitution — concept, hierarchy, the 11
working principles, incident typing, the lifecycle. Read it before reading
anything else in this package; `workflows/*.md` and `agents/*.md` quote it
rather than restate it.

## Layout

```
dcs/                      # this payload — shared, read-only source material
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
├── esg/
│   └── register_view.py   # sortable HTML view of REGISTER.md, copied
│                           # per-project by /dcs-init to .dcs/ (tracked --
│                           # not .dcs/esg/, which is gitignored wholesale);
│                           # regenerate: python .dcs/register_view.py
├── hooks/
│   ├── dcs_gate.py         # the PreToolUse gate, copied per-project by /dcs-init
│   └── register_view_regen.py  # PostToolUse: regenerates the register
│                              # view whenever REGISTER.md is edited
└── tools/
    ├── preservation_map.py # ## 6c. bounded-amendment preservation-map
    │                        # checker -- run standalone (see its own
    │                        # module docstring for the invocation) or
    │                        # imported by tests/test_doctrine_integrity.py
    └── record_integrity.py # close-time record-integrity check --
                             # commit-citation existence, artifact-set
                             # completeness, SAFETY.md schema, clean tree,
                             # non-degenerate commit messages -- run
                             # standalone (see its own module docstring) or
                             # invoked unconditionally by dcs/workflows/close.md

agents/dcs-*.md             # flat files, alongside any other installed agents
skills/dcs-*/SKILL.md        # one skill per command, thin @-include wrappers
```

Project-side state, created by `/dcs-init`, lives in `<project>/.dcs/` —
`config.json`, `ACTIVE` (present only while an incident is open — its
absence *is* the gate's open state), and `incidents/<date>-<slug>/` per
incident. See `references/doctrine.md` for the full incident-directory
layout.

## Commands

| Command | Does |
|---|---|
| `/dcs-init` | Onboard a project: `.dcs/` + config, copy the gate hook, ask before wiring `settings.json` |
| `/dcs-new <description>` | Stem: intake → analysts → 201 brief → typing → Type 5 express lane, or open a gated incident |
| `/dcs-plan` | Objectives → chiefs' tactics/partition → integrated IAP → Owner approval (hash-stamped marker) |
| `/dcs-execute` | Verify marker → fan out specialists → handle deviations → binding Safety Officer verdict |
| `/dcs-close` | Require green Safety verdict → AAR → lessons to project memory → release the gate |
| `/dcs-status` | Read-only sitrep from disk; states exactly which command resumes the P |

## v0.1 constraints

One incident active at a time. No manifest, no updater, no multi-project
registry — each project gets its own `.dcs/` via `/dcs-init`; this payload
under `~/.claude/dcs/` is shared, read-only source material every
project's workflows and agents `@`-include from.
