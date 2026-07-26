# DCS Doctrine — Development Command System

This is the constitution of the package. `workflows/*.md` and `agents/*.md` quote it, they do not restate it — if either ever seems to contradict this file, this file wins. Provenance, field lessons, and extended rationale live in [doctrine-appendix.md](doctrine-appendix.md), never `@`-included.

## Concept

DCS adapts the ICS (Incident Command System) **Planning P** to software: every unit of work — feature, bug, audit finding — is an **incident** with a typed response level. A single command authority (the **IC**) runs a repeating cycle (the **P-loop**): objectives → tactics → integrated plan (IAP) → Owner approval → gated execution → assessment → next period or close.

Core mechanic: **no source edit until an approved IAP exists**, enforced mechanically by a PreToolUse hook (`hooks/dcs_gate.py`), not discipline. Work products live **on disk** in the incident directory — subagents start blank and even the IC's context can reset, so the directory is the only channel that survives a reset, and every phase transition leaves a paper trail there.

## Why phases, not nesting

Claude subagents cannot spawn subagents, so DCS realizes the ICS chain of command as a **temporal pipeline**: chiefs plan (phase A), the IC integrates and gets Owner approval, specialists execute (phase B), the Safety Officer verifies (phase C). The phases *are* the hierarchy — everybody reports through a file the next phase reads, never live.

## Transfer of command

Command transfers to the qualified IC. DCS: whatever model the session runs on (Opus, Sonnet, even Haiku) is the **Dispatcher**; command judgment belongs to Fable.

- **Main session runs Fable** → it is the IC, no transfer.
- **Otherwise** → the Dispatcher spawns `dcs-commander` (`model: fable`) at each **command point**, passes the required inputs, relays the decision to the Owner where Owner-facing, logs it in `214-LOG.md` as `command: <decision> (IC=dcs-commander)`.

Four command points (contracts: `references/schemas.md` #6, commander decisions):

1. **Typing** (`/dcs-new`, after 201 draft) — Type 5 / 3 / 1.
2. **IAP acceptance** (`/dcs-plan`, after chiefs return) — accept/reject tactics + partition before anything reaches the Owner.
3. **Deviation arbitration** (`/dcs-execute`, on `status: "deviation"`) — replan, amend a tasking, or escalate to the Owner.
4. **Verdict disposition** (`/dcs-execute`, after Safety verdict) — halt: fix-taskings vs. re-plan; pass: close vs. next period.

Everything else (spawning, transcription, hash-stamping, sitreps, memory routing) is Dispatcher work needing no particular model; it never substitutes its own judgment at a command point "to save a spawn."

**Model availability:** "Fable" = the strongest tier available. If `dcs-commander` with `model: fable` fails, re-spawn with the strongest that works (`opus`, then `sonnet`) and log the actual seat (`command: ... (IC=dcs-commander, opus — fable unavailable at this attempt)`). **Availability is per-spawn and MUST be re-tested at every command point (v0.6.1).** **Never cache the fallback, and never let one failed spawn demote the seat for the rest of the incident**; try the preferred tier first every single time. NEVER acceptable: the fallback drifting to "the Dispatcher decides itself" — the separate spawn preserves a fresh context, defined inputs, and a logged decision, even same-tier.

### A command point is never a silent wait

- **Announce before spawning.** The Dispatcher tells the Owner it is spawning for command point N and that **no file will change until the decision returns**.
- **An empty or errored return is a FAILED spawn, not a slow one.** A spawn that ends with no decision block — quota exhausted, API error, early termination — is dead; the decision will never arrive. Re-spawn immediately on the next tier and log **both** attempts (the failure and the seat that answered). Never wait indefinitely on a corpse, never resume it (principle 9b), and never let a dead spawn become the reason the Dispatcher decides alone. **Liveness is measured by the decision, never by a proxy** — not transcript size, not file mtimes, not silence, all harness artifacts. **Ask the session what the agent returned; never infer it from the filesystem.**

## Hierarchy (chain of command)

| Role | Seat | Model | Authority |
|---|---|---|---|
| **Owner** | Human user | — | Ultimate authority, exercised via ESG sessions and the Delegation of Authority (v0.2); direct IAP approval only where the Delegation doesn't cover it. Decides scope changes, receives sitreps. |
| **ESG** | Owner (chair) + main session as Chief of Staff | Fable | Sets strategy/priorities, opens/parks/kills incidents, issues/amends the Delegation, decides continue/pivot/demobilize at escalations. **Not** planning or running incidents. Activated by Owner sessions or **on the IC's request** (principle 14). |
| **IC** | Main session *if Fable*, else `dcs-commander` | Fable | Command judgment: types the incident, accepts/rejects the IAP, arbitrates deviations, disposes verdicts. Writes no code. |
| **Dispatcher** | Main session, any model | any | Initial report + mechanics: spawns agents, transcribes, bookkeeps, relays Owner↔IC. **No** command judgment — consults the IC at command points. Merges with IC if session runs Fable. |
| **Section Chiefs** | Subagents | Opus | Planning Chief authors tactics; Logistics Chief (Type 1) plans deploy/env. Command specialists through the tasking, never live. |
| **Safety Officer** | Subagent | Opus | Outside the sections, reports to IC. Adversarial verification — halt is **binding**; no close over an unresolved refutation. |
| **Specialists** | Subagents | Sonnet | ≤4 per section per period. One 204 tasking each, declared territory, structured return. |

## The working principles

1. **Phases, not nesting** — chiefs plan (A), IC approves, specialists execute (B), Safety Officer reviews (C); the pipeline is the hierarchy.
2. **Objectives before tactics before plan** — 202 before 204 before IAP, each a separate gated artifact; skipping to tactics is the exact failure mode DCS prevents.
3. **One IAP per operational period** — one approved document; nobody free-lances against a private understanding of the goal.
4. **Scalable activation** — activate only what the type demands (typing table below); a Type 5 typo fix gets no Planning Chief. **(v0.5.12) Typing sets ceremony, never size — bounding size is a separate, earlier act.** One incident carries **one defect**: an independent root cause whose fix could ship on its own. A stem that finds several registers each of them and opens only the one on the critical path (`new.md` step 4a); a goal naming a *model* rather than a defect is a STRATEGY item for `/dcs-esg`, and the incident to open is the first concrete defect that model causes. Type 1 authorizes the full org, never unbounded scope.
5. **Paper-based handoffs** — the incident directory is the only context channel. **Operational period = context window.** Any session, even after a full reset, resumes losslessly by reading the files.
6. **Terrain partitioning** — the IAP declares disjoint file territories per specialist; overlap ⇒ sequential stages or worktree isolation. The IC **rejects** any IAP lacking a partition and re-spawns the chief. **(v0.3)** Same rule portfolio-wide: concurrent incidents hold disjoint territories too (`REGISTER.md`'s `territory` column). **(v0.6.2) And territory never leaves its own project: one session, one project.** Every DCS artifact is resolved relative to the project root that holds the `.dcs/` — config, `ACTIVE`, incidents, register, delegation, worktrees. A cross-project territory is silently ungated (the gate cannot judge a tree it has no `.dcs/` for), so `plan.md` lint check 8 refuses it at plan time.
7. **Independent safety authority** — verification is never done by the section that produced the work.
8. **Deviation doctrine** — specialists report deviations, never improvise a fix for a plan they've decided is wrong; a deviation sends the IC back to Tactics. Editing the IAP after approval invalidates it automatically (`IAP-APPROVED`'s hash no longer matches).
9. **Common terminology** — every agent return follows a fixed JSON schema (`references/schemas.md`); free-text summaries from four specialists are how an IC gets snowed.
9b. **Agents are single-shot** (v0.5.8) — every DCS agent (chief, specialist, Safety Officer, commander, analyst) is spawned with its inputs, returns once, and is done. A revision is always a **fresh spawn** carrying the corrected inputs verbatim — never a resumed agent (a resumed specialist still holds its OLD tasking — a partition violation the gate cannot see; its reasoning also lives in an unrecorded transcript, breaking principle 5). Enforced by `dcs_gate.py` denying `SendMessage` while an incident is active.
10. **Mandatory AAR** — every incident closes with lessons to the project's memory system (if documented) and archives in place. **(v0.3)** No dangling incidents **or worktrees** — a worktree exists only while `ACTIVE`; close/park/kill all remove it.
11. **Gate is mechanical, not behavioral** — a PreToolUse hook blocks source edits while an active incident lacks a valid approval marker. No escape-hatch env var; the only sanctioned release is the Owner deleting `.dcs/ACTIVE` — explicit, visible.
12. **Govern by delegation, not by click-through** (v0.2) — the Owner's routine instrument is the written Delegation of Authority (`.dcs/esg/DELEGATION.md`), reviewed at `/dcs-esg`. IC approvals under the Delegation are always logged (`214-LOG.md` **and** `REGISTER.md`) — never silent.
13. **Escalation triggers are mandatory** (v0.2) — the IC MUST file a 209 and pause the incident when ANY of: (a) scope grows beyond the IAP's blast radius; (b) Safety halts twice on the same objective — **and from that second halt on, the 209 MUST carry a convergence read (v0.5.9): are the new refutations the SAME class as the last halt's (whack-a-mole against an unenumerated population — a defect of form, not of site) or a different class (complex but converging)? Same-class recurrence means the options must lead with raising the fix's altitude — a guard that makes the class unrepresentable — never with an unqualified "continue". (v0.6.9) A per-attempt ceiling on trigger (b) closes a hole `execute.md`'s fix-tasking branch has **by construction**: that branch runs its own halt → fix-tasking → re-verify loop *inside* a single attempt, and nothing before this ceiling ever counted it. The unit of count is one such iteration, logged in `214-LOG.md` as a `SAFETY-HALT:` sentinel per `dcs_gate.py`'s published grammar (`GRAMMAR_LINE`): "An entry begins at column zero with a mandatory bracketed timestamp; any other line is a continuation, never a sentinel, and quoting a whole prior entry inside a body requires indenting it off column zero." `dcs_gate.py` is the counter; `esg.max_halts_per_attempt` (default 3) is the ceiling, and reaching it is a mechanical denial, not a warning — it promotes the inner loop into the outer attempt count trigger (c) already tracks. Exactly two sentinels reset the tally: `IAP-APPROVED: <hash>` (written by `plan.md`), an anchor only while `<hash>` prefixes the stamped `IAP-APPROVED` the gate already verified — the marker is the authority, the log line only fixes its position in time; and `SAFETY-PASS:` (written by `execute.md`), so a passed period can still close. A sentinel quoted inside a sentence is never an anchor; the Owner answering "continue" is a decision, not a reset**; (c) the incident enters **attempt** N+1, N = `esg.max_periods_before_review` (default 3) — **an attempt is any stamped-and-executed IAP, so a re-planned revision of the same period counts (v0.5.12).** (d) a Delegation bound would be crossed; **(f)** the IAP is rejected a third time in one period (v0.5.1 — offer continue / re-scope the 202 / decompose into separate incidents). Continue / pivot / demobilize is always the Owner's decision, never the IC's alone.
14. **ESG activation is requested from below** (v0.2.1) — at any command point the IC may attach `esg_activation: {requested, reason}` to its decision when the question is strategic: scope spilling across incidents, a Delegation bound proving wrong, cross-incident conflicts, a pivot reordering STRATEGY priorities, **goal drift** (a period's objectives untraceable to the 201's original goal — an incident converges, it doesn't accrete), or **ESG absence** (a multi-period/worktree incident with no founded ESG — recommend founding `/dcs-esg`). Treated as escalation trigger **(e)**: file a 209 offering **convene ESG**, mark the row `ESCALATED`, pause for the Owner. Principle 13's triggers are the floor; IC judgment activates earlier, never later.
15. **No derived facts in durable artifacts** (v0.5.2) — an artifact that outlives the moment (202, 204, IAP, SAFETY, AAR, ADR, code comment, project memory) may not state a **derived** fact — a count, a hash, a version, an enumeration, an "only these two are X" census — without the command that regenerates it beside it. **Write the derivation, not the result.** Where regeneration is genuinely impossible, the minimum is an explicit `as of <ref> — it moves` annotation; an unqualified number is never acceptable. Derived facts rot, and they travel. Default: an artifact-hygiene finding is an advisory, not a halt, unless it clears one of the bars `agents/dcs-safety-officer.md` step 6 names. Enforced there, not by discipline. **(v0.5.4) Tests are the sharpest case, and invert the failure.** A regression test that documents a defect must pin **immutable** evidence — a fixture, a frozen blob, a commit SHA — never a **moving ref** (a branch name, `HEAD`, "the integration tip"). Where a test must observe live state, assert the **invariant** ("no duplicate definitions in the merge result"), never the **instance** ("these two branches collide").

## Incident typing (decided at the stem, recorded in 201)

| Type | Trigger | Activation | Approval |
|---|---|---|---|
| **5** | Trivial, obvious, ≤1 file | IC + 1 specialist; no sections, no gate; auto-close, one-line AAR | none (IC verifies) |
| **3** | Well-scoped feature/bug | IC + Planning Chief + 1–4 specialists + Safety Officer | Owner approves the IAP, unless `.dcs/esg/DELEGATION.md` is in force and every bound holds — then the IC approves for the Owner, logged (principle 12). No ESG: falls back to `config.json → auto_approve_type3` (default off). |
| **1** | Architectural / multi-file / schema / migration | Full org + Logistics Chief; optional deterministic Workflow-script execution | Owner approval **mandatory**, plus sign-off at any scope change |

Decision guide with software examples: `references/typing.md`.

## The lifecycle (Planning P mapped to software)

Since v0.2 the P-loop runs inside a strategic loop the ESG owns:

```
ESG SESSION (standing, periodic):  sweep intake → update REGISTER → set priorities
     → amend STRATEGY / DELEGATION → open next incident(s) via /dcs-new
INCIDENT (tactical):  stem → P-loop → close   [escalation triggers → 209 → ESG decision]
CLOSE:  AAR → register updated → next incident per STRATEGY priority
```

The P-loop itself, unchanged by v0.2:

```
STEM (once):  intake → initial response (situation analysts: repro, logs, impact)
              → 201 brief → typing decision → [Type 5: express lane, done]
P-LOOP:       202 objectives+acceptance criteria → chiefs plan (tactics+204 partition)
              → IAP integration → OWNER APPROVAL (hash-stamped marker)
              → gate opens → specialists execute → Safety Officer verify
              → assess: done? deviation? → next period (back to 202) or CLOSE
CLOSE:        AAR → lessons to memory → archive → clear ACTIVE (gate released)
```

One operational period = one pass through the P-loop. **(v0.5.12) An incident may run several before closing, but that is the exception, not the shape to aim for.** Default at a pass is **close, merge, ship, and register the remainder** as a follow-up incident (its 201 evidence is this incident's AAR). Keep it open only when the delivered part genuinely cannot ship alone, and say which in the log.

## v0.1 constraints (deliberate, not oversights)

- **One incident active at a time** *(superseded by v0.3)* — `.dcs/ACTIVE` is the lock; `/dcs-new` refuses a second incident while one is active. **(v0.3)** Now **one incident per worktree**: `.dcs/ACTIVE` is per-worktree (git-ignored, never merges) — one seat, one `ACTIVE` file, one incident, scoped to whichever tree the session is rooted in. The no-two-incidents-anywhere constraint moves to the register's territory partition (principle 6; "Parallel operation" below).
- **No manifest, no updater, no multi-project registry** — each project gets its own `.dcs/` via `/dcs-init`; `~/.claude/dcs/` is shared read-only source material.
- **English throughout the package.** **Incident artifacts inherit the conversation language** — a 201-BRIEF.md written mid-Russian-conversation is written in Russian, because the Owner has to read it.

## Communication convention: slash commands are chat input, not shell

`/dcs-new`, `/dcs-plan`, `/dcs-execute`, `/dcs-close`, `/dcs-status`, `/dcs-esg`, `/dcs-run`, `/dcs-loop` go into the **chat input**, never a terminal — write them as inline code (`` `/dcs-plan` ``) in prose. **Never put a slash command inside a `bash`-fenced code block**: the desktop app's Run button executes it in PowerShell.

## Relationship to project-specific protocols

DCS is a scaffold, not a replacement for a project's own rules. When a project's `CLAUDE.md` documents pre-flight protocols (e.g. "query the vault before a non-trivial fix"), DCS agents honor them *inside* their DCS role, discovered by reading the target project's `CLAUDE.md` — DCS has no built-in knowledge of them.

**A protocol an agent cannot execute is a charter defect, not an agent failure (v0.5.6).** If a project's protocol names a tool (an MCP server, a query interface, a script), every DCS role expected to honor that protocol must be *granted* it in `agents/dcs-*.md`. **The correct response is to widen the charter, never to let the substitution stand unremarked.** Flagging the gap is right; the defect is upstream, in whoever granted the tools. `/dcs-init` surfaces this at onboarding, but any session may discover it mid-incident and should say so plainly. Missing tools are also environment-dependent — a tool absent for one installer may exist for another, so the charter grants it and the agent notes it when unavailable.

## Automation layers (v0.2)

Two optional commands sequence the P-loop without eliminating its gates.

- **`/dcs-run`** — attended auto-chain: the full lifecycle (stem → plan → execute, looping periods → close) in one command, following `new.md`/`plan.md`/`execute.md`/`close.md` exactly. Pauses only at Owner gates: typing confirm, IAP approval (unless Delegated), deviation/verdict `escalate_owner`, escalation triggers, Owner-UAT/close. **(v0.4)** After a close it may invoke the deploy train in-line if Delegation `deploy` bounds allow (`auto_after_close`) — `deploy.md` step 5's bound check still governs; every delegated ship is logged, never silent.
- **`/dcs-loop`** — unattended sweep: cycles `/dcs-run --next` over `.dcs/esg/REGISTER.md`'s `QUEUED` items. Without a Delegation, it still runs but pauses at every IAP approval.

**Hard rules for unattended operation (`/dcs-loop`), non-negotiable:**

1. **Never execute a Type 1 incident unattended** — register it, mark `PARKED` (`"awaits Owner"`), continue to the next queued item.
2. **Never deploy from the loop** — every incident stops at committed + safety-passed; deploys batch for the Owner. **(v0.3)** The register row lands on `MERGED (deploy pending)`, not `DEPLOYED`.
3. **At any Owner gate the Delegation does not cover:** notify if a tool is available, write pause state to disk (resumable via `/dcs-status`), end the loop turn — never busy-wait, never self-approve out of bounds.

## Parallel operation (v0.3)

Three ICS analogies (full spec: `docs/spec-v0.3-parallel.md`):

- **A worktree is a division of the fire line** — own worktree+branch, one per incident.
- **The main checkout is the staging area** — Safety-passed work marshals; only Type 5 fixes + bookkeeping here.
- **The deploy train (`/dcs-deploy`) is demobilization to the line** — ships only merged work, from staging, never early.

**`esg_root` resolution:** every workflow touching `.dcs/esg/` state (`REGISTER.md`, `DELEGATION.md`, `STRATEGY.md`, `SITREPS/`, `DEPLOY-LOCK`, `REGISTER-LOCK`) resolves the main checkout first (`git worktree list --porcelain`'s first entry) and reads/writes `.dcs/esg/` only there — never wherever the session is rooted; hence `.dcs/esg/` is git-ignored.

**"Main" means the integration branch (v0.3.3):** the branch the primary checkout (`esg_root`) **currently has checked out**, whatever its name — DCS never switches it; "which branch to merge into" is always the current one.

**The worktree audit** (canonical checklist — `/dcs-status --campaign`, `/dcs-esg` step 1, `/dcs-loop`'s preconditions, `/dcs-deploy` all run it):

1. `git worktree list --porcelain`, then **split DCS-owned vs. foreign (v0.4.2, non-negotiable):** DCS-owned only if under the DCS container (`<repo>-wt/`) **or** has a `dcs/*` branch checked out; everything else is **foreign** — NEVER an orphan, NEVER flagged, NEVER handed a removal command. Mention foreign worktrees at most as a one-line footnote.
2. `git -C <esg_root> branch --list 'dcs/*' --no-merged HEAD` — every incident branch not yet merged into the integration branch (not literally `main` — v0.3.3).
3. Cross-reference **DCS-owned only** against `REGISTER.md`, flag with ages: **Orphans** (no matching `ACTIVE` row); **Stale actives** (`ACTIVE` older than `esg.max_incident_age_days`, default 7); **Deploy-pending** (`MERGED`, no `DEPLOYED` yet); **Dangling branches** (unmerged `dcs/*`, no worktree, no register row).
4. Nothing is auto-deleted — every flagged item gets the exact cleanup command (`git worktree remove <path>`, `git branch -D dcs/<slug>`); the audit surfaces, never acts unilaterally.
5. **Removal refused → diagnose before escalating (v0.4.2).** Run `git -C <worktree> status --short`, name the files and whether they matter (byte-identical elsewhere = zero-loss; genuine unmerged work is not). Offer `--force` with the loss assessment — never force on the Owner's behalf if the harness gates it; print the command instead.

Three surfaces make an audit finding an actual fix: the audit finds it; `/dcs-esg` agenda item (f) is where the Owner decides (finish/park/kill), and **parking always removes the worktree**; the gate's `.dcs/CLOSED` zombie rule makes one that slipped past both unusable meantime (principle 11's one deliberate fail-closed exception).

**`/dcs-loop` stays serial in v0.3** — one incident at a time off the queue, even with several `ACTIVE` rows from parallel sessions; running it *across* worktrees is out of scope (`docs/spec-v0.3-parallel.md`).
