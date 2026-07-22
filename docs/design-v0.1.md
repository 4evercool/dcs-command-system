# ICC — Incident Command for Code (installable skill package)

## Context

Per-feature development keeps jumping to code before the goal is nailed down. We adapt the ICS **Planning P** into a subagent-based workflow where the chain of command is realized as **phases, not nesting** (subagents can't spawn subagents), with a **hook-enforced gate**: no source edits until an approved IAP exists. Package mirrors GSD's installable anatomy (explored: `skills/*/SKILL.md` thin wrappers → `workflows/*.md` orchestration → flat `agents/*.md`, state in a project dot-dir, Python PreToolUse hooks denying via stdout JSON like `bash_guard.py`).

Design was agreed in conversation, including the review amendments: Safety Officer with veto, file-based IAP as the only context channel (ops period = context window), file-territory partitioning, deviation doctrine, hook gate, intake/AAR wiring, Type-5 economics, structured returns.

---

## Part 1 — The ICC doctrine (goes into `references/doctrine.md`, summarized here as the spec)

### Concept

ICC treats every unit of work — feature, bug, audit finding — as an **incident** with a typed response level. A single command authority (the **IC**, the main Fable session) runs a repeating planning cycle (the P-loop): objectives → tactics → integrated plan (IAP) → owner approval → gated execution → assessment → next period or close. Work products live **on disk** in the incident directory; conversation context is treated as perishable.

### Hierarchy (chain of command)

| Role | Seat | Model | Authority |
|---|---|---|---|
| **Owner** | Human user | — | Ultimate authority. Approves IAPs, decides scope changes, receives sitreps. |
| **Incident Commander (IC)** | Main session | Fable | Sets objectives, types the incident, spawns all agents, arbitrates deviations, reports to Owner. Writes no code (delegates even trivia). |
| **Section Chiefs** | Subagents | Opus | Planning Chief authors the IAP; Logistics Chief (Type 1 only) plans deploy/env. Command specialists **through the tasking they author and later review**, not live links. |
| **Safety Officer** | Subagent | Opus | Outside sections; reports to IC. Adversarial verification of "done"; **binding halt** — no incident closes over an unresolved refutation. |
| **Specialists** | Subagents | Sonnet | ≤4 per section per period. Execute one 204 tasking each, inside a declared file territory, return structured reports. |

### Working principles

1. **Phases, not nesting** — chiefs plan (phase A), IC approves, specialists execute (phase B), chiefs review (phase C). The temporal pipeline *is* the chain of command.
2. **Objectives before tactics before plan** — 202 before 204 before IAP; each a separate artifact with a gate.
3. **One IAP per operational period** — a single approved document; everyone works off it.
4. **Scalable activation** — activate only what the incident type demands (see typing table). Positions stay merged into the IC until complexity forces a split.
5. **Paper-based handoffs** — subagents start blank; the incident directory is the only context channel. **Ops period = context window**; the files are the shift-change briefing, so any new session resumes losslessly.
6. **Terrain partitioning** — the IAP must declare disjoint file territories per specialist; overlap ⇒ sequential stages or worktree isolation. IC rejects IAPs without a partition.
7. **Independent safety authority** — verification is never done by the section that produced the work.
8. **Deviation doctrine** — plans meet reality; specialists report deviations in their structured return, never improvise. Deviation ⇒ IC re-enters the P at Tactics. IAP edits invalidate approval automatically (hash-bound marker).
9. **Common terminology** — all agent returns follow fixed JSON schemas (`references/schemas.md`); prose reports from four specialists are how an IC gets snowed.
10. **Mandatory AAR** — every incident closes with lessons written to the project's memory system and the incident archived. No dangling incidents.
11. **Gate is mechanical, not behavioral** — a PreToolUse hook blocks source edits while an active incident lacks a valid approval marker.

### Incident typing (decided at the stem, recorded in 201)

| Type | Trigger | Activation | Approval |
|---|---|---|---|
| **5** | Trivial, obvious, ≤1 file | IC + 1 specialist; no sections, no gate; auto-close w/ one-line AAR | none (IC verifies) |
| **3** | Well-scoped feature/bug | IC + Planning Chief + 1–4 specialists + Safety Officer | Owner approves IAP (config `auto_approve_type3` can delegate later) |
| **1** | Architectural / multi-file / schema / migration | Full org: + Logistics Chief; optional deterministic Workflow-script execution | Owner approval **mandatory**, plus sign-off at scope changes |

### The lifecycle (Planning P mapped)

```
STEM (once):  intake → initial response (situation analysts: repro, logs, impact)
              → 201 brief → typing decision → [Type 5: express lane, done]
P-LOOP:       202 objectives+acceptance criteria → chiefs plan (tactics+204 partition)
              → IAP integration → OWNER APPROVAL (hash-stamped marker)
              → gate opens → specialists execute → Safety Officer verify
              → assess: done? deviation? → next period (back to 202) or CLOSE
CLOSE:        AAR → lessons to memory → archive → clear ACTIVE (gate released)
```

---

## Part 2 — Package layout (mirrors GSD conventions found on this machine)

```
C:\Users\4ever\.claude\
├── icc\                              # payload
│   ├── VERSION                       # "0.1.0"
│   ├── workflows\                    # orchestration bodies, @-included by skills
│   │   ├── init.md  new.md  plan.md  execute.md  close.md  status.md
│   ├── references\
│   │   ├── doctrine.md               # Part 1 above, full prose
│   │   ├── schemas.md                # all structured-return JSON schemas
│   │   ├── forms.md                  # what each ICS-numbered file contains
│   │   └── typing.md                 # Type 5/3/1 decision guide + activation table
│   ├── templates\                    # 201-BRIEF.md, 202-OBJECTIVES.md, 203-ORG.md,
│   │   │                             # 204-TASKING.md, IAP.md, 214-LOG.md, AAR.md,
│   │   └── config.json               # per-project defaults
│   └── hooks\
│       └── icc_gate.py               # the PreToolUse gate (copied per-project by /icc-init)
├── agents\
│   ├── icc-planning-chief.md         # model: opus
│   ├── icc-logistics-chief.md        # model: opus
│   ├── icc-safety-officer.md         # model: opus
│   ├── icc-ops-specialist.md         # model: sonnet
│   └── icc-situation-analyst.md      # model: sonnet, read-only tools
└── skills\
    ├── icc-init\SKILL.md   icc-new\SKILL.md   icc-plan\SKILL.md
    ├── icc-execute\SKILL.md  icc-close\SKILL.md  icc-status\SKILL.md
```

Frontmatter formats copied from GSD exemplars: agents get `name/description/tools/model/color`; skills get `name/description/argument-hint/allowed-tools` and a body that `@`-includes `$HOME/.claude/icc/workflows/<name>.md`. No manifest/updater in v0.1 (over-engineering for one user).

### Project-side state (created by `/icc-init`)

```
<project>/.icc/
├── config.json          # incidents_dir (default ".icc/incidents"), guarded_paths globs,
│                        # auto_approve_type3: false, language: "auto"
├── ACTIVE               # slug + type + phase of the active incident (absent = gate open)
└── incidents\<YYYY-MM-DD>-<slug>\
    ├── 201-BRIEF.md         # symptom, evidence (action-log/codegraph findings), blast radius, TYPE + rationale
    ├── 202-OBJECTIVES.md    # goal + measurable acceptance criteria (the DoD)
    ├── 203-ORG.md           # activated positions this period
    ├── 204-TASKING\S1.md…   # one per specialist: task, file territory, forbidden zones, evidence required
    ├── IAP.md               # integrated: links 202+203+204, partition table, risks, verification plan
    ├── IAP-APPROVED         # sha256 of IAP.md at approval — hash mismatch = approval void
    ├── 214-LOG.md           # append-only phase-transition log (the shift-change record)
    ├── SAFETY.md            # Safety Officer verdicts per period
    └── AAR.md               # close-out: what worked, lessons, links to memory writes
```

One incident active at a time (v0.1 constraint — matches solo operation; noted in doctrine).

---

## Part 3 — Commands (skills)

- **`/icc-init`** — onboard a project: create `.icc/` + config, copy `icc_gate.py` into `<project>/.claude/hooks/`, and **show the user** the exact `settings.json` hooks block to add (Edit\|Write\|NotebookEdit matcher) — wire it only on explicit yes (settings edits are config changes). Detects bread_bot-style existing hooks and appends alongside them.
- **`/icc-new <description>`** — the stem. IC gathers intake (user report, `audit_results` `needs_fix` row, bug), spawns 1–2 `icc-situation-analyst` (read-only: repro path, logs/action-log, codegraph impact, vault/pitfall check per project protocols), writes `201-BRIEF.md`, proposes a Type via `references/typing.md`, confirms typing with Owner via AskUserQuestion. **Type 5 express lane**: spawn one `icc-ops-specialist` with an inline micro-tasking, verify, one-line AAR, auto-close — no gate, no ceremony. Type 3/1: create incident dir, set `ACTIVE` (gate now closed), hand to `/icc-plan`.
- **`/icc-plan`** — the planning arc. IC drafts `202-OBJECTIVES.md` (acceptance criteria = the DoD), spawns `icc-planning-chief` (and `icc-logistics-chief` for Type 1) which returns tactics + a 204 tasking set **with a file-territory partition**; IC integrates into `IAP.md`, rejects partition-less plans, then presents the IAP to the Owner via **AskUserQuestion** (not plan mode — avoids colliding with the global ExitPlanMode handoff hook). On approval: write `IAP-APPROVED` with the IAP's sha256. Gate opens.
- **`/icc-execute`** — verifies marker validity (exists + hash matches), fans out ≤4 `icc-ops-specialist` per the 204s (parallel only when territories are disjoint; else sequential; `isolation: worktree` as declared in the IAP), collects structured returns, spawns `icc-safety-officer` on the combined diff vs. acceptance criteria. Refuted ⇒ fix-tasking or back to `/icc-plan` (deviation doctrine). Deviation in any return ⇒ IC updates 202/204 → IAP hash changes → re-approval forced automatically. Passed ⇒ assess against 202 → next period or `/icc-close`. For **Type 1**, offers the deterministic variant: IC emits a Workflow script (schema-enforced returns, phases Execute/Verify) instead of Agent-tool fan-out.
- **`/icc-close`** — Safety verdict must be green. AAR written; lessons routed to the project's memory (for bread_bot: vault patterns/pitfalls + `tasks/lessons.md` per its own protocol; generic projects: whatever `config.json` names); intake source closed (e.g. flag the `audit_results` row); incident archived; `ACTIVE` removed (gate released). 
- **`/icc-status`** — sitrep from files: active incident, phase, period count, open taskings, safety state. Also the resume entry after a context reset: reads `214-LOG.md` tail and tells the IC where the P left off.

## Part 4 — Agents (charters, abbreviated — full text in the .md files)

- **icc-planning-chief** (opus): consumes 201+202 only. Runs project pre-flight protocols (vault domains, codegraph callers/impact — per the project's CLAUDE.md if present). Produces tactics + 204 set + partition + risks + verification plan as structured JSON. Forbidden: writing source code.
- **icc-ops-specialist** (sonnet): consumes exactly one 204 + IAP excerpt. Edits only inside its territory. Returns `{status: done|blocked|deviation, files_touched[], tests_run, evidence, deviation?: {found, why_plan_wrong, proposal}}`. Forbidden: touching files outside territory, improvising on deviation.
- **icc-safety-officer** (opus): consumes IAP acceptance criteria + the real diff + test output; never the specialists' self-reports as evidence. Charter: *attempt to refute* completion; default to refuted when uncertain. Returns `{verdict: pass|halt, refutations[]}`. Its halt is binding on the IC.
- **icc-logistics-chief** (opus, Type 1 only): deploy path, env/deps, migration ordering, rollback plan → feeds the IAP.
- **icc-situation-analyst** (sonnet, tools: Read/Grep/Glob/Bash-readonly + codegraph): stem-phase intel; returns structured findings for the 201.

## Part 5 — The gate hook (`icc_gate.py`)

Modeled directly on `bash_guard.py` (stdin JSON → stdout `permissionDecision: "deny"`, exit 0):
- Fires on PreToolUse `Edit|Write|NotebookEdit`. Reads `<project>/.icc/ACTIVE`; absent ⇒ allow (zero overhead for non-ICC work).
- If active incident is Type 3/1 and phase is pre-execution: allow writes to `.icc/**`, plan/scratch paths; **deny** writes matching `config.json → guarded_paths` (default: everything except `.icc/`, `tasks/`, docs) with a reason naming the missing/void `IAP-APPROVED`.
- Marker validity = file exists **and** stored sha256 equals current `IAP.md` hash — editing the plan voids approval mechanically.
- Escape hatch mirroring house style: none for the core rule; emergencies = Owner deletes `ACTIVE` (explicit, visible act).

## Implementation order

1. `references/` (doctrine, schemas, forms, typing) — the constitution everything else quotes.
2. `templates/` + `agents/` (5 files).
3. `workflows/` + `skills/` (6 pairs; skills are thin `@`-include wrappers per GSD pattern).
4. `hooks/icc_gate.py` + `/icc-init` wiring logic.
5. `VERSION`, and a short `README.md` in `~/.claude/icc/`.

All new files; no existing files modified except — on explicit later approval during `/icc-init` — a project's `.claude/settings.json`.

## Verification

1. Fresh session: skill list shows `icc-*`; `/icc-init` on a scratch project creates `.icc/` and prints the hooks block.
2. Wire the hook in the scratch project; create a dummy Type 3 incident; confirm an `Edit` to a guarded file is **denied** pre-approval, allowed after `IAP-APPROVED`, denied again after touching `IAP.md` (hash void).
3. End-to-end dry run on bread_bot with a real `needs_fix` audit finding as intake: `/icc-new` → `/icc-plan` (IAP with partition) → approve → `/icc-execute` (1–2 specialists + Safety Officer) → `/icc-close` (lessons land in vault + `tasks/lessons.md`, finding flagged).
4. Resume test: kill the session mid-P, new session `/icc-status` picks up the correct phase from files alone.
