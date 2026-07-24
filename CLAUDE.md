# CLAUDE.md — DCS (Development Command System)

This repo is the **source of truth** for the DCS package. It is also
**self-hosted**: changes to DCS are made as DCS incidents.

---

## Source of truth, and the isolation that makes self-hosting safe

`C:\DCS` is canonical. `~/.claude/` holds the **installed copy** —
`~/.claude/dcs/` (payload), `~/.claude/agents/dcs-*.md`,
`~/.claude/skills/dcs-*/`.

A running session reads its workflows and doctrine from the **installed
copy**, while an incident edits the **repo**. That gap is what makes
self-hosting safe: a specialist rewriting `dcs/workflows/plan.md` cannot
change the plan.md the session is currently following.

**Never patch `~/.claude/dcs/*` in place** — edit here, then install.

> **HARD RULE: never run `install.ps1` while a DCS incident is active.**
> Installing swaps the workflows the running session reads, mid-incident.
> Install *is* the deploy step and belongs after `/dcs-close`.

## Deploy

| | |
|---|---|
| **Deploy command** | `powershell -ExecutionPolicy Bypass -File C:\DCS\install.ps1` (POSIX: `./install.sh`) |
| **Deployed-version marker** | `~/.claude/dcs/VERSION` — must equal `dcs/VERSION` after deploy |
| **Release (registry)** | `npm publish` — **Owner only**, requires a 2FA OTP; never attempted by a session |
| **Registry marker** | `npm view dcs-command-system version` |

`/dcs-deploy` runs the deploy command and verifies the marker advanced.
An `npm publish` is a separate, Owner-performed act; a session prepares
the release (version sync, `npm pack --dry-run` review) and stops there.

## Merge-time guard

`/dcs-close` step 1a runs this before merging, and a red result blocks
the merge (escalation trigger (a)):

```bash
python tests/test_doctrine_integrity.py
```

It checks what is mechanically checkable about prose: version sync,
principle numbering (unique, contiguous, matching any stated count),
`@`-include resolution, agent/template references, doctrine sections
referenced by name, the hot-path size budget, and encoding. Every check
in it exists because that defect shipped at least once.

## Verification suite

```bash
python tests/test_dcs_gate.py           # 25 cases — the approval gate
python tests/test_dcs_intake.py         # 10 cases — the session intake nudge
python tests/test_doctrine_integrity.py # 12 checks — package structure
```

`npm test` runs the first two. Run all three before any close.

## Where lessons go — three stores, one rule each

DCS's memory is layered, and putting a lesson in the wrong layer is how
knowledge bases rot. On `/dcs-close`, route by **who needs it**:

| Store | Takes | Ships? |
|---|---|---|
| `dcs/references/doctrine.md` | a change to a **rule** — how DCS behaves | yes, **hot path** |
| `dcs/references/doctrine-appendix.md` | the **provenance** of a rule: the field lesson, the story | yes, never `@`-included |
| **`vault/`** (Obsidian) | what only a **maintainer of DCS** needs: cross-incident analysis, metrics over time, decisions that did not become doctrine, meta-lessons about building DCS, the backlog | **no** |

**Test:** if it changes how DCS *behaves* → doctrine. If it explains why
a rule exists → appendix. If it would only ever be read while improving
DCS itself → vault.

Keep the rule in the core and the story in the appendix — that split is
the whole point of the v0.5.0 diet, and the core is read on every
invocation and every command-point spawn.

## The vault (`vault/`)

An Obsidian vault, **repo-local and never shipped** (absent from
`package.json`'s `files` whitelist, so `npm pack` excludes it). Entry
point: `vault/00-Navigation.md`.

- `Post-mortems/` — cross-incident analysis with citations to the
  incident artifacts, not to memory
- `Metrics/` — numbers **plus the command that regenerates them**
  (principle 15 applied to the vault itself; `vault/_scripts/`)
- `Decisions/` — choices deliberately kept out of doctrine, so they are
  not silently relitigated
- `Meta/` — patterns in *building* DCS, distinct from the rules DCS enforces
- `Backlog.md` — known gaps with evidence; candidates for `/dcs-esg` to
  queue, **not** a register

Read it before non-trivial DCS work; write to it after. It is unguarded
by the gate (like `docs/`) so a close can write lessons without holding
territory, and it costs zero runtime latency because nothing
`@`-includes it.

## Coding rules

- **Hooks are stdlib-only Python** (`dcs/hooks/*.py`). They run from a
  project's own `.claude/hooks/`, with no venv and no dependencies.
  Every hook **fails open** on error — except `dcs_gate.py`'s
  `.dcs/CLOSED` zombie rule, which is deliberately fail-closed.
- **Write files with the Write/Edit tools, never PowerShell
  `Set-Content`/`Out-File`** — those emit a UTF-8 BOM, which has twice
  broken a hash comparison and a parse here.
- **English throughout the package.** Incident artifacts inherit the
  conversation's language; the shipped package does not.
- **Ship no project facts.** DCS discovers a project's protocols from
  *that* project's `CLAUDE.md` at runtime. Worked examples in
  `schemas.md` use a neutral fiction (`src/`, `docs/`), never a real
  repo's paths. `tests/test_doctrine_integrity.py` has no dependency on
  any project outside this one.
- **Version sync is atomic**: `dcs/VERSION` and `package.json` change in
  the same commit. The guard fails otherwise.
- **File size**: workflows ≤ ~250 lines. `doctrine.md` is the exception
  (it is the constitution) but is budgeted — see the guard.

## Self-hosting notes for incidents in this repo

- **Worktrees**: `C:\DCS-wt\<slug>`, branch `dcs/<slug>` (doctrine,
  "Parallel operation"). Integration branch is whatever `C:\DCS` has
  checked out — currently `main`.
- **One session, one project.** Run DCS incidents from a session rooted
  in `C:\DCS`. A session rooted elsewhere that edits this repo produces
  an incident in the *wrong* portfolio, and the gate cannot catch it —
  `plan.md` lint check 8 refuses such a territory at plan time.
- **`.dcs/config.json` must not exempt `*.md`.** The gate matches with
  `fnmatch`, where `*` also matches `/`, so a blanket `*.md` in
  `unguarded_paths` exempts **every markdown file at any depth** — which
  in this repo is doctrine, every workflow, every agent charter and every
  template: 48 of ~57 tracked files. The guarded set here is explicit
  (`dcs/**`, `agents/**`, `skills/**`, `tests/**`, `bin/**`,
  `install.*`, `package.json`); `docs/**`, `README.md`, `CLAUDE.md` and
  `.dcs/**` are deliberately unguarded.
- **Typical incident type**: doctrine and workflow changes are Type 3.
  Changes to `dcs/hooks/dcs_gate.py`, the tests that guard it, or the
  installer are Type 1 — they are the enforcement mechanism itself.
