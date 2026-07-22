# DCS — Development Command System

Source-of-truth repository for **ICC (Incident Command for Code)** — an
installable Claude Code skill package that adapts the ICS (Incident Command
System) **Planning P** to the software development cycle.

> **This repo is canonical.** The installed copy lives in `~/.claude/`
> (payload `~/.claude/icc/`, agents `~/.claude/agents/icc-*.md`, skills
> `~/.claude/skills/icc-*/`). Edit HERE, commit, then run `install.ps1` —
> never patch the installed copy in place (same discipline the gate itself
> enforces for source code).

## What ICC is

Every unit of work — feature, bug, audit finding — is an **incident** with
a typed response level (5 / 3 / 1). A repeating planning cycle (the P-loop)
runs: objectives → tactics → integrated action plan (IAP) → Owner approval
→ **gated** execution → adversarial verification → assess → next period or
close. The core mechanic: **no source edit until an approved IAP exists**,
enforced mechanically by a PreToolUse hook (`icc/hooks/icc_gate.py`) with a
hash-bound approval marker — editing the plan after approval voids the
approval automatically.

Chain of command (phases, not nesting — subagents can't spawn subagents):

| Role | Seat | Model |
|---|---|---|
| Owner | human | — |
| Incident Commander | main session if it runs Fable, else the `icc-commander` agent (transfer of command) | Fable |
| Dispatcher | main session, any model | any |
| Section Chiefs (Planning / Logistics) | subagents | Opus |
| Safety Officer (binding halt) | subagent | Opus |
| Ops Specialists (≤4, disjoint file territories) | subagents | Sonnet |

Full constitution: [icc/references/doctrine.md](icc/references/doctrine.md).
Design history: [docs/design-v0.1.md](docs/design-v0.1.md).
Roadmap: [docs/spec-v0.2-esg.md](docs/spec-v0.2-esg.md) — the ESG strategic
layer (Delegation of Authority, incident register, escalation triggers).

## Layout

```
icc/          package payload  -> installs to ~/.claude/icc/
  workflows/    orchestration bodies (@-included by skills)
  references/   doctrine, schemas, forms, typing guide
  templates/    201/202/203/204/IAP/214/AAR + config.json
  hooks/        icc_gate.py (the PreToolUse gate)
agents/       subagent charters -> installs to ~/.claude/agents/
skills/       slash commands    -> installs to ~/.claude/skills/
docs/         design docs and version specs
tests/        gate lifecycle test (14 cases)
install.ps1   copy repo -> ~/.claude (the only sanctioned install path)
```

## Commands (once installed)

`/icc-init` (onboard a project + wire the gate) · `/icc-new` (stem: intake
→ 201 → typing) · `/icc-plan` (202 → chiefs → IAP → approval) ·
`/icc-execute` (gated fan-out + Safety Officer) · `/icc-close` (AAR +
release) · `/icc-status` (sitrep / resume).

## Testing

```bash
python tests/test_icc_gate.py
```

14 lifecycle cases against the gate hook (deny pre-approval, hash-void
after IAP edit, fail-open on errors, BOM tolerance, cwd-walk discovery).
