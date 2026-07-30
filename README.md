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

## Upgrading

**Updating the package is not enough to update a project.** The payload in
`~/.claude/` (workflows, doctrine, agents, skills) is shared; the pieces
that actually *enforce* anything live inside each onboarded project and
are never written by an install. After every upgrade that changes a hook,
do all three of these, **in this order**, in each project:

**1. Update the package.** This refreshes `~/.claude/dcs/` only.

```bash
npm i -g dcs-command-system@latest
```

**2. Re-run `/dcs-init` in the project.** This is what copies the current
hooks into `<project>/.claude/hooks/`. It must come *after* step 1 —
`/dcs-init` copies from `~/.claude/dcs/hooks/`, so running it first just
reinstalls the old hook. Never run it while an incident is active.

Check that it took:

```bash
grep -c halt_cycles .claude/hooks/dcs_gate.py
```

`0` means the project has the new documentation and the old enforcer —
the worst of both, because the docs now describe a ceiling the project
does not have. Anything above `0` means the hook is current.

**3. Add any new `.dcs/config.json` keys by hand.** `/dcs-init` copies the
config template **only when the file does not exist**, so it will never
add a key to a config you already have — not on the first re-run, not on
the tenth. New keys are listed per release in
[CHANGELOG.md](CHANGELOG.md); the full set with defaults is below.

### `.dcs/config.json`

Every key is optional and falls back to a safe default, so an older config
keeps working — it just silently keeps the defaults.

| Key | Default | What it does |
|---|---|---|
| `incidents_dir` | `.dcs/incidents` | Where incident directories live |
| `guarded_paths` | `["**/*"]` | Globs the approval gate protects |
| `unguarded_paths` | `[".dcs/**", "tasks/**", "*.md", ".claude/**"]` | Globs it exempts. **Careful:** matching is `fnmatch`, where `*` also crosses `/`, so a bare `*.md` exempts every markdown file at any depth |
| `auto_approve_type3` | `false` | Fallback delegation for projects with no ESG |
| `language` | `"auto"` | Language of incident artifacts |
| `esg.max_periods_before_review` | `3` | Stamped attempts before an incident must escalate to the Owner |
| `esg.max_incident_age_days` | `7` | Age at which an incident is flagged as stale |
| `esg.max_halts_per_attempt` | `3` | **New in 0.6.9.** Safety Officer halts inside one attempt before the gate closes and refuses further edits. Answering "continue" does not reset it |

**Optional tools.** The agent charters grant `mcp__codegraph__*` (a
call-graph MCP) to the roles that plan, edit, and verify code. **It is
entirely optional** — an MCP pattern that matches no installed server
grants nothing and errors nothing, so DCS works unchanged without it and
those agents simply use `grep`/`Read` for impact analysis. Grant more if
your project needs it: if your `CLAUDE.md` makes some tool mandatory
before an edit, add its glob to the relevant charter's `tools:` line —
`/dcs-init` audits this at onboarding and reports any role that is
expected to honor a protocol it lacks the tool to execute.

## What you get

- **No code before an approved plan — enforced, not promised.** A
  PreToolUse hook blocks source edits while an incident lacks an approved
  IAP (Incident Action Plan). The approval marker is hash-bound: editing
  the plan after approval voids the approval automatically.
- **It offers itself, so you never have to remember it.** On the first
  prompt of each session in an onboarded project, a second (advisory,
  never blocking) hook asks whether a bug or feature should be opened as
  an incident — and if one is already mid-flight in that tree, reports
  its slug, type and phase instead. Questions, explorations and trivial
  changes are explicitly exempt: DCS stays opt-in per task.
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
- **An audit trail regulators would recognize.** Every incident leaves an
  append-only decision log, hash-bound human approvals with attribution,
  versioned delegations of authority, adversarial verification records,
  and escalation sitreps with recorded human decisions — the evidence
  EU AI Act Articles 12/14, ISO/IEC 42001 and the NIST AI RMF ask for,
  produced as a by-product rather than a report. See
  [Audit trail and human oversight](#audit-trail-and-human-oversight).
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

CLI (this npm package):

| Command | What it does |
|---|---|
| `dcs install` | Copy the payload into `~/.claude` |
| `dcs uninstall` | Remove the payload from `~/.claude` |
| `dcs doctor` | Content-aware payload comparison (sha256 of every file, via `tests/payload_check.py`) + Python-on-PATH check |
| `dcs bump <version>` | Atomically update `dcs/VERSION` and `package.json` → `version` to the same value |
| `dcs version` | Print the package version |

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

## Audit trail and human oversight

Most agentic development frameworks produce **plans**. DCS produces
**provenance** — and it does so as a by-product of how it works, not as a
reporting feature bolted on afterwards.

This matters beyond tidiness. Three regimes now converge on the same
demand — that human oversight of AI systems be *demonstrable*, not
asserted: the **EU AI Act**
([Article 14, human oversight](https://artificialintelligenceact.eu/article/14/)
and [Article 12, record-keeping](https://artificialintelligenceact.eu/article/12/)),
**ISO/IEC 42001** (AI management systems: documented lifecycle processes,
defined roles and responsibilities, verification and validation, and
records that survive an audit), and the **NIST AI RMF** (Govern / Map /
Measure / Manage). Article 12 in particular requires logging that permits
**post-hoc reconstruction of individual AI-assisted decisions** — which is
precisely what an agentic coding workflow normally destroys, because its
reasoning lives in a chat transcript nobody keeps.

**What DCS leaves behind, per incident, without anyone opting in:**

| Artifact | What it evidences |
|---|---|
| `214-LOG.md` | Append-only operational log: every phase transition, command decision (with which seat decided), escalation, and verdict — decision reconstruction, in order |
| `IAP-APPROVED` | Human approval with attribution and timestamp, **hash-bound to the approved plan** — editing the plan voids the approval mechanically, so approvals cannot be silently outgrown |
| `DELEGATION.md` | Versioned, human-signed grants of authority with explicit machine-checked bounds; every amendment retained — *what was delegated, by whom, when, and under what limits* |
| `SITREPS/*.md` | Escalations with the options presented and the human's recorded decision |
| `SAFETY.md` | Independent adversarial verification, verbatim verdicts, binding halts |
| `AAR.md` | Close-out under a facts-only rule: claims must cite artifacts actually checked |
| `REGISTER.md` | Portfolio state — what ran, what shipped, what was verified against production |

**Three properties that make this oversight rather than paperwork:**

1. **The gate is preventive, not advisory.** Article 14 asks that overseers
   be able to *intervene*. DCS inverts the default: a PreToolUse hook
   denies source edits until an approved plan exists, so human approval is
   a **precondition of action**, not an interruption of it. Nothing has to
   be caught in time.
2. **Oversight is proportionate to risk.** Article 14 requires measures
   "commensurate with the risks, level of autonomy and context of use."
   DCS types every unit of work (5 / 3 / 1) and activates ceremony
   accordingly — trivial work stays cheap, architectural and
   migration-bearing work is mandatorily human-approved, and delegated
   authority explicitly excludes the irreversible.
3. **It is built against automation bias** — the failure mode Article 14
   names outright. The Safety Officer is chartered to *refute* completion,
   is forbidden from accepting agent self-reports as evidence, must re-run
   checks itself, and its halt is binding. The facts-only rule forbids
   past-tense claims that cite no artifact. Both exist because
   self-reported success drifts, and both were written after watching it
   happen.

**What this is not.** DCS does not make an organization compliant with
anything, is not a certification, and is not legal advice. Compliance is
achieved by a management system, an assessment, and people — not by a
package. What DCS does is make the *evidence* a by-product of doing the
work: if your organization has to demonstrate human oversight of
AI-assisted software changes, DCS means that evidence already exists, in
your repository, generated at the moment each decision was actually made.

## For maintainers of this repo

This repo is canonical; `~/.claude` is the installed copy. Edit here,
commit, then install — `install.ps1` (Windows) / `install.sh` (POSIX) /
`node bin/dcs.js install` all perform the same flat copy. Never patch the
installed copy in place. Version-sync rule: `package.json` and
`dcs/VERSION` bump together (see
[docs/publishing.md](docs/publishing.md)). Tests:
`npm test` (gate + intake) plus `python tests/test_doctrine_integrity.py`
(package structure — also the merge-time guard, see
[CLAUDE.md](CLAUDE.md)). DCS is self-hosted: changes to it are made as
DCS incidents from a session rooted in this repo. Design history:
[docs/design-v0.1.md](docs/design-v0.1.md) ·
[docs/spec-v0.2-esg.md](docs/spec-v0.2-esg.md) ·
[docs/spec-v0.3-parallel.md](docs/spec-v0.3-parallel.md) ·
[dcs/references/doctrine-appendix.md](dcs/references/doctrine-appendix.md)
(provenance and field lessons for the doctrine core).

## License

MIT
