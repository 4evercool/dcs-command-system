# DCS — Development Command System

Run your development the way emergencies are run: every feature, bug, or
audit finding is an **incident** with a typed response level, a written
action plan, an approval gate that is **mechanically enforced**, and an
adversarial verifier with veto power. DCS adapts the Incident Command
System's **Planning P** to the software development cycle, as an
installable [Claude Code](https://claude.com/claude-code) skill package.

## Install

```bash
npm i -g dcs-command-system     # auto-installs into ~/.claude
```

or one-shot, no global install:

```bash
npx dcs-command-system install
```

Then, inside a Claude Code session in your project:

```
/dcs-init        # onboard the project: creates .dcs/, wires the approval gate
/dcs-run <describe a bug or feature>
```

Requirements: Node ≥ 16.7 for the installer; Python 3.8+ on PATH for the
approval-gate hook. `dcs doctor` checks both. The auto-install skips
politely in CI or when `~/.claude` doesn't exist
(`DCS_SKIP_POSTINSTALL=1` opts out).

## What you get

- **No code before an approved plan — enforced, not promised.** A
  PreToolUse hook blocks source edits while an incident lacks an approved
  IAP (Incident Action Plan). The approval marker is hash-bound: editing
  the plan after approval voids the approval automatically.
- **A chain of command mapped to model tiers.** You are the **Owner**
  (ultimate authority). An **Incident Commander** (strongest available
  model) holds command judgment at four defined command points. **Section
  Chiefs** (Opus) plan; **Ops Specialists** (Sonnet, ≤4, disjoint file
  territories) execute; an independent **Safety Officer** (Opus)
  adversarially verifies the real diff and runs the tests itself — its
  halt is binding. Any model can drive the session: command judgment
  transfers to a dedicated commander agent when needed, never to the
  session's own voice.
- **Typed, scalable ceremony.** Type 5 (trivial) = one specialist, no
  ceremony. Type 3 (well-scoped) = the standard gated loop. Type 1
  (architectural) = full activation with mandatory Owner sign-off.
  Ceremony is proportional to risk, decided per incident.
- **Everything on paper.** Incidents live on disk (`.dcs/incidents/…`,
  ICS-style forms: 201 brief, 202 objectives, 204 taskings, 214 log,
  AAR). Any session — any model, any day — resumes an incident losslessly
  from its files.
- **A strategic layer when you want one.** `/dcs-esg` holds a standing
  session: incident register, ranked strategy, and a written **Delegation
  of Authority** that lets routine in-bounds work auto-approve on your
  behalf — logged, never silent. `/dcs-run` chains a whole incident with
  you only at real decisions; `/dcs-loop` sweeps the queue unattended
  under the Delegation (never runs architectural work unattended, never
  deploys).
- **Parallel sessions without deploy contention** (v0.3). Each incident
  gets its own git worktree and branch; concurrent incidents hold
  disjoint file territories; merging is a mandatory step of closing (a
  worktree cannot rot forgotten — every DCS surface audits and ages
  strays); deploys run from an always-clean main via `/dcs-deploy`.

## Commands

| Command | What it does |
|---|---|
| `/dcs-init` | Onboard a project: `.dcs/` state + the approval-gate hook |
| `/dcs-run <intake>` | Drive a full incident: stem → plan → execute → close, pausing only at Owner gates (`--next` pulls the top queued register item) |
| `/dcs-new` / `/dcs-plan` / `/dcs-execute` / `/dcs-close` | The individual phases, for stepwise use or resuming |
| `/dcs-status` | Sitrep; `--campaign` for the whole portfolio |
| `/dcs-esg` | Strategy session: register, priorities, Delegation of Authority |
| `/dcs-loop` | Unattended sweep of the queued register under the Delegation |
| `/dcs-deploy` | The deploy train: ship all merged incidents from clean main |

CLI (this npm package): `dcs install` · `dcs uninstall` · `dcs doctor` ·
`dcs version`.

## How it holds up

The doctrine was hardened by running it on a real production project from
day one: every failure mode observed in the field (dispatchers skipping
command points, self-reported "done" without artifacts, verification
staged before commits existed, forgotten worktrees) became a mechanical
check — entry gates that audit the command chain at every phase boundary,
a facts-only rule for close-out reports, hash-bound approvals, and a
14+-case test suite for the gate hook. The full constitution is in
[dcs/references/doctrine.md](dcs/references/doctrine.md) — workflows and
agents quote it; if they ever disagree, doctrine wins.

DCS ships none of its authors' project facts: project-specific behavior
(memory systems, intake trackers, deploy commands) is discovered from
YOUR project's `CLAUDE.md` at runtime, never assumed.

## For maintainers of this repo

This repo is canonical; `~/.claude` is the installed copy. Edit here,
commit, then install — `install.ps1` (Windows) / `install.sh` (POSIX) /
`node bin/dcs.js install` all perform the same flat copy. Never patch the
installed copy in place. Version-sync rule: `package.json` and
`dcs/VERSION` bump together (see
[docs/publishing.md](docs/publishing.md)). Tests:
`python tests/test_dcs_gate.py`. Design history:
[docs/design-v0.1.md](docs/design-v0.1.md) ·
[docs/spec-v0.2-esg.md](docs/spec-v0.2-esg.md) ·
[docs/spec-v0.3-parallel.md](docs/spec-v0.3-parallel.md).

## License

MIT
