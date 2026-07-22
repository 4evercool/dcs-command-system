# DCS — Development Command System

Source-of-truth repository for **DCS (Development Command System)** — an
installable Claude Code skill package that adapts the ICS (Incident Command
System) **Planning P** to the software development cycle.

> **This repo is canonical.** The installed copy lives in `~/.claude/`
> (payload `~/.claude/dcs/`, agents `~/.claude/agents/dcs-*.md`, skills
> `~/.claude/skills/dcs-*/`). Edit HERE, commit, then run `install.ps1` —
> never patch the installed copy in place (same discipline the gate itself
> enforces for source code).

## What DCS is

Every unit of work — feature, bug, audit finding — is an **incident** with
a typed response level (5 / 3 / 1). A repeating planning cycle (the P-loop)
runs: objectives → tactics → integrated action plan (IAP) → Owner approval
→ **gated** execution → adversarial verification → assess → next period or
close. The core mechanic: **no source edit until an approved IAP exists**,
enforced mechanically by a PreToolUse hook (`dcs/hooks/dcs_gate.py`) with a
hash-bound approval marker — editing the plan after approval voids the
approval automatically.

**v0.2 adds the ESG strategic layer** above the P-loop: a standing session
(`/dcs-esg`) where the Owner chairs and the main session acts as Chief of
Staff, managing an incident portfolio (`.dcs/esg/REGISTER.md`), a ranked
`STRATEGY.md`, and a versioned `DELEGATION.md` — the Owner's written grant
of authority letting the IC auto-approve routine (Type 3, in-bounds) IAPs
on their behalf instead of a click-through every time. Two driver commands
build on it: `/dcs-run` chains stem → plan → execute → close for one
incident attended (Owner answers gates only), and `/dcs-loop` sweeps the
register's queue unattended under the Delegation, never running a Type 1
or deploying without the Owner. See
[docs/spec-v0.2-esg.md](docs/spec-v0.2-esg.md) for the full spec.

**v0.3 adds parallel operation**: each Type 3/1 incident gets its own git
worktree + branch, so multiple incidents can be developed at once without
sharing a working tree — the portfolio-level territory partition
(`REGISTER.md`'s `territory` column) is what keeps their eventual merges
clean. `/dcs-close` now merges the incident's branch into main and removes
its worktree as part of closing (never a separate chore anyone can
forget), and a new `/dcs-deploy` command runs a serialized, Owner-gated
deploy train that ships exactly the set of merged, Safety-passed
incidents from the always-clean main checkout. See
[docs/spec-v0.3-parallel.md](docs/spec-v0.3-parallel.md) for the full
spec.

Chain of command (phases, not nesting — subagents can't spawn subagents):

| Role | Seat | Model |
|---|---|---|
| Owner | human | — |
| Incident Commander | main session if it runs Fable, else the `dcs-commander` agent (transfer of command) | Fable |
| Dispatcher | main session, any model | any |
| Section Chiefs (Planning / Logistics) | subagents | Opus |
| Safety Officer (binding halt) | subagent | Opus |
| Ops Specialists (≤4, disjoint file territories) | subagents | Sonnet |

Full constitution: [dcs/references/doctrine.md](dcs/references/doctrine.md).
Design history: [docs/design-v0.1.md](docs/design-v0.1.md).
ESG spec (implemented in v0.2): [docs/spec-v0.2-esg.md](docs/spec-v0.2-esg.md)
— the strategic layer (Delegation of Authority, incident register,
escalation triggers).

## Layout

```
dcs/          package payload  -> installs to ~/.claude/dcs/
  workflows/    orchestration bodies (@-included by skills)
  references/   doctrine, schemas, forms, typing guide
  templates/    201/202/203/204/IAP/214/AAR + config.json
  hooks/        dcs_gate.py (the PreToolUse gate)
agents/       subagent charters -> installs to ~/.claude/agents/
skills/       slash commands    -> installs to ~/.claude/skills/
docs/         design docs and version specs
tests/        gate lifecycle test (18 cases)
install.ps1   copy repo -> ~/.claude (Windows; the only sanctioned install path)
install.sh    same, for macOS/Linux
```

**Per onboarded project (v0.3):** a sibling `<repo>-wt\` directory holds
one subdirectory per active incident worktree (`git worktree add
<repo>-wt\<slug> -b dcs/<slug>`), created automatically the first time a
Type 3/1 incident opens. The repo itself stays the "main checkout" — the
only place `.dcs/esg/` state, merges, and deploys live; see doctrine's
"Parallel operation" section.

**Portability notes for new installers:** the gate hook needs `python` on
PATH (stdlib only, 3.8+). The IC tier degrades gracefully — if your plan
has no Fable access, `dcs-commander` falls back to the strongest available
model (doctrine → "Model availability"). Project-specific behaviors
(memory routing, intake-source closure) are discovered from YOUR project's
CLAUDE.md at runtime — DCS ships none of its authors' project facts.

## Commands (once installed)

`/dcs-init` (onboard a project + wire the gate) · `/dcs-new` (stem: intake
→ 201 → typing) · `/dcs-plan` (202 → chiefs → IAP → approval) ·
`/dcs-execute` (gated fan-out + Safety Officer) · `/dcs-close` (AAR,
merge worktree to main, release) · `/dcs-status` (sitrep / resume,
`--campaign` for the portfolio) · `/dcs-esg` (v0.2: standing strategy
session — priorities, register, Delegation of Authority) · `/dcs-run`
(v0.2: attended auto-chain of the full lifecycle, pausing only at Owner
gates) · `/dcs-loop` (v0.2: unattended queue sweep over the register,
under the Delegation) · `/dcs-deploy` (v0.3: serialized, Owner-gated
deploy train — ships merged incidents from the main checkout, Owner-
triggered only, never called by `/dcs-loop`).

## Testing

```bash
python tests/test_dcs_gate.py
```

18 lifecycle cases against the gate hook (deny pre-approval, hash-void
after IAP edit, fail-open on errors, BOM tolerance, cwd-walk discovery,
and v0.3's target-path root resolution + `.dcs/CLOSED` zombie rule).
