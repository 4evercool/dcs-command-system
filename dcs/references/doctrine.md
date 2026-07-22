# DCS Doctrine — Development Command System

This is the constitution of the package. `workflows/*.md` and `agents/*.md`
quote it; they do not restate it. If a workflow or agent charter ever seems
to contradict this file, this file wins.

## Concept

Per-feature development keeps jumping to code before the goal is nailed
down. DCS adapts the ICS (Incident Command System) **Planning P** to
software work: every unit of work — feature, bug, audit finding — is an
**incident** with a typed response level. A single command authority (the
**IC**) runs a repeating planning cycle (the **P-loop**): objectives →
tactics → integrated plan (IAP) → Owner approval → gated execution →
assessment → next operational period or close.

The core mechanic: **no source edit until an approved IAP exists.** This is
enforced mechanically by a PreToolUse hook (`hooks/dcs_gate.py`), not by
discipline or a system-prompt reminder. Discipline forgets under pressure;
a hook does not.

Work products live **on disk**, in the incident directory. Conversation
context is treated as perishable — subagents start blank, and even the IC's
own context window can reset. The incident directory is the only channel
that survives a reset. This is why the lifecycle below insists on a paper
trail for every phase transition, not just the final artifacts.

## Why phases, not nesting

Claude subagents cannot spawn subagents — there is no live nested chain of
command available. DCS realizes the ICS chain of command as a **temporal
pipeline** instead: chiefs plan in one phase, the IC integrates and gets
Owner approval, specialists execute in a later phase, the Safety Officer
verifies in a phase after that. The phases *are* the hierarchy. Nobody
reports "live" to anybody; everybody reports through a file that the next
phase reads.

## Transfer of command

In ICS, the person who reports the fire ("I see fire on that distillation
tower") is never required to be the incident commander — the first unit on
scene takes the report and runs initial actions, and **command transfers to
the qualified IC** when they arrive. DCS works the same way, because a
skill cannot switch the main session's model: whatever model the session
runs on (Opus, Sonnet, even Haiku) serves as the **Dispatcher**, and
command judgment belongs to Fable regardless.

- **If the main session runs Fable**, it is the IC. No transfer — it makes
  the command-point decisions itself.
- **If it doesn't**, the Dispatcher spawns the `dcs-commander` agent
  (`model: fable`) at each **command point**, passes the inputs that
  command point requires (file contents, structured returns), relays the
  decision to the Owner where Owner-facing, and records it in `214-LOG.md`
  as `command: <decision> (IC=dcs-commander)`.

The four command points (decision contracts in `references/schemas.md` #6):

1. **Typing** — after the 201 draft (`/dcs-new`): Type 5 / 3 / 1.
2. **IAP acceptance** — after the chiefs return (`/dcs-plan`): accept or
   reject the tactics + partition before anything is presented to the Owner.
3. **Deviation arbitration** — on any `status: "deviation"`
   (`/dcs-execute`): replan, amend a tasking, or escalate to the Owner.
4. **Verdict disposition** — after the Safety Officer's verdict
   (`/dcs-execute`): on `halt`, fix-taskings vs. re-plan; on `pass`, close
   vs. next period.

Everything else — spawning, transcription, hash-stamping, sitreps, memory
routing — is Dispatcher work and needs no particular model. The Dispatcher
never substitutes its own judgment at a command point "to save a spawn";
that is precisely the drift the transfer exists to prevent.

**Model availability (portability rule):** "Fable" here means "the
strongest model tier available in this environment." Not every user or
plan has Fable access. If spawning `dcs-commander` with `model: fable`
fails because the model is unavailable, re-spawn with the strongest tier
that works (`opus`, then `sonnet` as last resort) and record the actual
seat in `214-LOG.md` (e.g. `command: ... (IC=dcs-commander, opus —
fable unavailable)`). What is NEVER acceptable is the fallback drifting
to "the Dispatcher decides itself": even when the commander runs on the
same tier as the Dispatcher, the separate spawn preserves the structural
value — a fresh context, the defined inputs, and a logged decision
against the schema, none of which the Dispatcher mid-conversation can
guarantee about itself.

## Hierarchy (chain of command)

| Role | Seat | Model | Authority |
|---|---|---|---|
| **Owner** | Human user | — | Ultimate authority, exercised primarily through ESG sessions and the Delegation of Authority (v0.2); direct IAP approval only where the Delegation doesn't cover it. Decides scope changes, receives sitreps. |
| **ESG** | Standing body: Owner (chair) + main session as Chief of Staff | Fable | Sets strategy and priorities across incidents, opens/parks/kills incidents, issues and amends the Delegation of Authority, decides continue/pivot/demobilize at escalations. Does **not** plan or run incidents. Activated two ways: the Owner's standing sessions, or **on the IC's request** (principle 14). |
| **Incident Commander (IC)** | Main session *when it runs Fable*; otherwise the `dcs-commander` agent (transfer of command, below) | Fable | Holds command judgment: types the incident, accepts/rejects the IAP, arbitrates deviations, disposes of Safety verdicts. Writes no code — delegates even trivia. |
| **Dispatcher** | Main session, any model (Opus, Sonnet, even Haiku) | any | Takes the initial report, runs the mechanics: spawns agents, transcribes artifacts, does bookkeeping, relays between Owner and IC. Holds **no** command judgment — at command points it must consult the IC. When the main session runs Fable, IC and Dispatcher merge into one seat. |
| **Section Chiefs** | Subagents | Opus | Planning Chief authors the IAP's tactics; Logistics Chief (Type 1 only) plans deploy/env. Command specialists **through the tasking they author and later review**, never through a live link. |
| **Safety Officer** | Subagent | Opus | Outside the sections; reports to the IC. Adversarial verification of "done" — its halt is **binding**. No incident closes over an unresolved refutation. |
| **Specialists** | Subagents | Sonnet | ≤4 per section per operational period. Execute one 204 tasking each, inside a declared file territory, return a structured report. |

## The 13 working principles

1. **Phases, not nesting** — chiefs plan (phase A), IC approves, specialists
   execute (phase B), the Safety Officer reviews (phase C). The temporal
   pipeline *is* the chain of command.
2. **Objectives before tactics before plan** — 202 before 204 before IAP;
   each is a separate artifact with its own gate. Skipping straight to
   tactics is the exact failure mode DCS exists to prevent.
3. **One IAP per operational period** — a single approved document; every
   specialist works off it, nobody free-lances against a private
   understanding of the goal.
4. **Scalable activation** — activate only what the incident type demands
   (see the typing table below). Positions stay merged into the IC until
   complexity forces a split. A Type 5 typo fix does not get a Planning
   Chief.
5. **Paper-based handoffs** — subagents start blank; the incident directory
   is the only context channel. **Operational period = context window.**
   The files are the shift-change briefing: any new session — even after a
   full context reset — can resume losslessly by reading them.
6. **Terrain partitioning** — the IAP must declare disjoint file
   territories per specialist. Overlap ⇒ sequential stages or worktree
   isolation. The IC **rejects** any IAP without a partition and re-spawns
   the Planning Chief. **(v0.3)** The same principle applies one level up,
   across the whole portfolio: concurrent incidents hold disjoint file
   territories too (`REGISTER.md`'s `territory` column), which is what
   lets their eventual `git merge --no-ff` into main stay trivially
   clean — same reasoning, just scaled from "specialists inside one
   incident" to "incidents inside one portfolio."
7. **Independent safety authority** — verification is never done by the
   section that produced the work. The Safety Officer is not a section
   chief's rubber stamp.
8. **Deviation doctrine** — plans meet reality. Specialists report
   deviations in their structured return; they never improvise a fix for a
   plan they've decided is wrong. A deviation sends the IC back to Tactics
   (`/dcs-plan`). Editing the IAP after approval invalidates the approval
   automatically — the hash-bound marker (`IAP-APPROVED`) no longer matches.
9. **Common terminology** — every agent return follows a fixed JSON schema
   (`references/schemas.md`). Prose reports from four specialists are how
   an IC gets snowed: free-text summaries hide exactly the disagreement
   between "I did the task" and "I did *a* task."
10. **Mandatory AAR** — every incident closes with lessons written to the
    project's own memory system (if it documents one) and the incident
    archived in place. **(v0.3)** No dangling incidents **or worktrees** —
    a worktree exists only while its incident is `ACTIVE`; close, park,
    and kill all remove it. `/dcs-close` is not optional ceremony, it's
    how the gate gets released for the next incident AND how the worktree
    stops being the human's job to remember to clean up (see "Parallel
    operation" below).
11. **Gate is mechanical, not behavioral** — a PreToolUse hook blocks
    source edits while an active incident lacks a valid approval marker.
    There is no escape-hatch environment variable for this rule: the only
    sanctioned emergency
    release is the Owner deleting `.dcs/ACTIVE` — an explicit, visible act
    that leaves a trace in the directory's absence.
12. **Govern by delegation, not by click-through** (v0.2) — the Owner's
    routine control instrument is the written Delegation of Authority
    (`.dcs/esg/DELEGATION.md`), reviewed and amended at ESG sessions
    (`/dcs-esg`). IC approvals made on the Owner's behalf under the
    Delegation are always logged — `214-LOG.md` **and** `REGISTER.md` —
    never silent.
13. **Escalation triggers are mandatory** (v0.2) — the IC MUST file a 209
    sitrep and convene the Owner (pause the incident) when ANY of: (a)
    scope grows beyond the approved IAP's stated blast radius; (b) the
    Safety Officer halts twice on the same objective; (c) the incident
    enters operational period N+1, where N = `esg.max_periods_before_review`
    (default 3); (d) a Delegation bound would be crossed. Continue / pivot
    / demobilize is the Owner's decision, recorded in the sitrep — never
    the IC's to decide alone, Delegation or not.
14. **ESG activation is requested from below** (v0.2.1) — in ICS the
    EOC/ESG stands up when an incident outgrows incident-level management,
    and the request comes **from the IC**. Same here: at any command point,
    the IC may attach `esg_activation: {requested: true, reason}` to its
    decision (schemas.md #6) when the question at hand is strategic, not
    tactical — scope spilling across incidents, Delegation bounds proving
    wrong in practice, cross-incident conflicts, a pivot that would reorder
    STRATEGY priorities, **goal drift** (a period proposing objectives
    untraceable to the 201's ORIGINAL goal — an incident is supposed to
    converge, not accrete features; field lesson 2026-07-22, v0.3.2), or
    **ESG absence** (a multi-period or worktree incident running with no
    founded ESG at all — the activation request then means: recommend the
    founding `/dcs-esg` session; principle 14's other cues presuppose a
    portfolio that must first exist). The Dispatcher treats it as escalation trigger
    **(e)**: file a 209 whose options include **convene ESG**, mark the
    incident's `REGISTER.md` row `ESCALATED`, and pause for the Owner —
    who may convene `/dcs-esg` (its agenda takes IC-requested activations
    first) or decide inline, recording in the sitrep why a session wasn't
    needed. The mechanical triggers of principle 13 are the floor; IC
    judgment activates earlier, never later.

## Incident typing (decided at the stem, recorded in 201)

| Type | Trigger | Activation | Approval |
|---|---|---|---|
| **5** | Trivial, obvious, ≤1 file | IC + 1 specialist; no sections, no gate; auto-close with a one-line AAR | none (IC verifies) |
| **3** | Well-scoped feature/bug | IC + Planning Chief + 1–4 specialists + Safety Officer | Owner approves the IAP, unless `.dcs/esg/DELEGATION.md` (v0.2) is in force and every bound holds — then the IC approves on the Owner's behalf, logged (principle 12). Projects without an ESG fall back to `config.json → auto_approve_type3` (default off). |
| **1** | Architectural / multi-file / schema / migration | Full org: + Logistics Chief; optional deterministic Workflow-script execution | Owner approval **mandatory**, plus sign-off at any scope change |

Full decision guide with concrete software examples: `references/typing.md`.

## The lifecycle (Planning P mapped to software)

Since v0.2, the P-loop runs inside a larger strategic loop the ESG owns:

```
ESG SESSION (standing, periodic):  sweep intake → update REGISTER → set priorities
     → amend STRATEGY / DELEGATION → open next incident(s) via /dcs-new
INCIDENT (tactical):  stem → P-loop → close   [escalation triggers → 209 → ESG decision]
CLOSE:  AAR → register updated → next incident per STRATEGY priority
```

The P-loop itself is unchanged by v0.2:

```
STEM (once):  intake → initial response (situation analysts: repro, logs, impact)
              → 201 brief → typing decision → [Type 5: express lane, done]
P-LOOP:       202 objectives+acceptance criteria → chiefs plan (tactics+204 partition)
              → IAP integration → OWNER APPROVAL (hash-stamped marker)
              → gate opens → specialists execute → Safety Officer verify
              → assess: done? deviation? → next period (back to 202) or CLOSE
CLOSE:        AAR → lessons to memory → archive → clear ACTIVE (gate released)
```

One operational period = one pass through the P-loop. An incident may run
several periods (each a fresh 202→IAP→execute→verify cycle) before closing.

## v0.1 constraints (deliberate, not oversights)

- **One incident active at a time** *(superseded by v0.3 — see below)*,
  matching solo operation. `.dcs/ACTIVE` presence is the lock; `/dcs-new`
  refuses to open a second incident while one is active.
  **(v0.3)** This becomes **one incident per worktree**: `.dcs/ACTIVE` is
  now per-worktree state (git-ignored, never merges), so the lock still
  holds exactly as written — one Fable/dcs-commander seat, one `ACTIVE`
  file, one incident — just scoped to whichever tree (main checkout or an
  incident worktree) the session is rooted in, instead of to the whole
  project. The portfolio-level constraint this used to also imply (no two
  incidents running *anywhere* in the project) moves to the register: see
  "Parallel operation" below for the territory partition that replaces it.
- **No manifest, no updater, no multi-project registry.** Over-engineering
  for one user. Each project gets its own `.dcs/` via `/dcs-init`; the
  payload under `~/.claude/dcs/` is shared read-only source material.
- **English throughout the package** — doctrine, workflows, agent charters,
  schemas, templates. **Incident artifacts inherit the conversation
  language** — a 201-BRIEF.md written during a Russian conversation is
  written in Russian, because the Owner has to actually read it.

## Communication convention: slash commands are chat input, not shell

`/dcs-new`, `/dcs-plan`, `/dcs-execute`, `/dcs-close`, `/dcs-status`,
`/dcs-esg`, `/dcs-run`, `/dcs-loop` are Claude Code slash commands — the
Owner types them into the **chat input**,
never into a terminal. When a workflow's report step says "tell the Owner
the next step is /dcs-plan", write the command as inline code
(`` `/dcs-plan` ``) in plain prose. **Never put a slash command inside a
`bash`-fenced code block** — the desktop app attaches a Run button to
shell-tagged blocks, and clicking it executes the text in PowerShell,
which fails with CommandNotFoundException and confuses the Owner. Fenced
`bash` blocks are reserved for commands genuinely meant for the shell.

## Relationship to project-specific protocols

DCS is a scaffold, not a replacement for a project's own rules. When a
project's `CLAUDE.md` documents pre-flight protocols (e.g. "query the vault
before a non-trivial fix", "query the action_log before debugging", "query
the codegraph before a cross-file edit"), DCS agents honor them *inside*
their DCS role — a `dcs-situation-analyst` doing stem-phase intel on a
project with an action_log protocol queries it as part of gathering
evidence for the 201; a `dcs-planning-chief` planning tactics on a project
with a vault protocol reads the relevant domain pages before proposing
tactics. DCS does not know these protocols itself — it discovers them by
reading the target project's `CLAUDE.md`, the same way any agent would.

## Automation layers (v0.2)

Two optional commands sequence the P-loop without eliminating its gates —
neither changes who holds command judgment (see "Transfer of command"
above) or what counts as approval; they only remove the need for the
Owner to type each phase command by hand.

- **`/dcs-run`** — attended auto-chain. Runs the full incident lifecycle
  (stem → plan → execute, looping operational periods as needed → close)
  in one command, reading and following `workflows/new.md`, `plan.md`,
  `execute.md`, `close.md` exactly as written. Pauses only at the Owner's
  own gates: typing confirm, IAP approval (unless the Delegation covers
  it), deviation `escalate_owner`, verdict `escalate_owner`, escalation
  triggers, Owner-UAT/close. **(v0.4)** After a close, an attended run
  may invoke the deploy train in-line when the Delegation's `deploy`
  bounds say so (`auto_after_close`) — `deploy.md` step 5's bound check
  still governs, out-of-bounds and migration-bearing rows still ask, and
  every delegated ship is announced and logged, never silent
  (principle 12). Deploy delegation exists for the Owner who has watched
  routine ships long enough to sign them off in writing; it is a
  narrowing of prompts, never of evidence.
- **`/dcs-loop`** — unattended queue sweep. Cycles `/dcs-run --next` over
  `.dcs/esg/REGISTER.md`'s `QUEUED` items, with the Owner involved only at
  real decisions. Legitimate only *because* the ESG's Delegation of
  Authority (principle 12) defines what "routine" means in writing —
  without an active delegation, `/dcs-loop` still runs, but pauses at
  every IAP approval; that is the honest degenerate case of "nothing has
  been delegated yet," not a bug to route around.

**Hard rules for unattended operation (`/dcs-loop`), non-negotiable:**

1. **Never execute a Type 1 incident unattended** — register it, mark
   `PARKED` with reason `"awaits Owner"`, continue to the next queued item.
2. **Never deploy from the loop** — every incident it drives stops at
   committed + safety-passed; deploys are batched for the Owner. **(v0.3)**
   Concretely, this is `close.md`'s anti-rot core running its merge step
   but never `/dcs-deploy`: the register row lands on `MERGED (deploy
   pending)`, not `DEPLOYED` — the loop closes and merges incidents, it
   never ships them.
3. **At any Owner gate the Delegation does not cover:** send one
   notification if a push/notification tool is available in the session,
   write the pause state to disk (the incident stays mid-phase, resumable
   by any future session via `/dcs-status`), and end the loop turn —
   never busy-wait, never self-approve outside Delegation bounds.

ESG and the Delegation are what make unattended operation legitimate
rather than reckless: `/dcs-loop` never invents its own authority to act
— it only exercises what the Owner already signed off on in
`DELEGATION.md`, in writing, at an `/dcs-esg` session, and stops cleanly
at the edge of that grant.

## Parallel operation (v0.3)

Three ICS analogies keep the mental model straight, full spec:
`docs/spec-v0.3-parallel.md`.

- **A worktree is a division of the fire line** — physically separate
  ground (its own git worktree + branch), worked without coordinating
  every move with other divisions, because the portfolio-level territory
  partition (principle 6) already keeps the ground disjoint. One incident
  per worktree (v0.1's constraint, rescoped — see above).
- **The main checkout is the staging area** — where merged, Safety-passed
  work marshals before shipping. Nobody develops a Type 3/1 incident in
  staging; only Type 5 express fixes and portfolio bookkeeping (ESG
  sessions, the register, deploys) happen there.
- **The deploy train (`/dcs-deploy`) is demobilization to the line** —
  it only ships resources already IN staging (merged to main) and only
  runs from staging itself; it never reaches into a worktree early.

**`esg_root` resolution rule:** every workflow that touches `.dcs/esg/`
state (`REGISTER.md`, `DELEGATION.md`, `STRATEGY.md`, `SITREPS/`,
`DEPLOY-LOCK`, `REGISTER-LOCK`) resolves the main checkout first —
`git worktree list --porcelain`'s first listed entry is always the main
checkout — and reads/writes `.dcs/esg/` there, never wherever the current
session happens to be rooted. This is why `.dcs/esg/` is git-ignored (a
tracked copy would diverge across every incident branch) and why an
incident's own worktree never carries a copy of the register it has a row
in.

**"Main" means the integration branch (v0.3.3).** Wherever this doctrine
says "merge to main" / "merged into main", it means the branch the
primary checkout (`esg_root`) **currently has checked out** — whatever
its name. Many projects' primary checkouts live on long-running work
branches, and the deploy pipeline ships that checkout's HEAD, not a
branch literally named `main`. DCS never switches the primary checkout's
branch; asking the Owner "which branch should I merge into?" is a
question the doctrine already answers: the current one.

**The worktree audit** — the canonical checklist. `/dcs-status
--campaign`, `/dcs-esg` step 1, `/dcs-loop`'s preconditions, and
`/dcs-deploy` all run this exact check rather than each restating their
own version of it:

1. `git worktree list --porcelain` — every worktree actually on disk.
2. `git -C <esg_root> branch --list 'dcs/*' --no-merged HEAD` — every
   incident branch not yet merged into the integration branch (HEAD of
   the primary checkout, NOT a branch literally named `main` — v0.3.3).
3. Cross-reference both against `REGISTER.md`, and flag, with ages (days
   since the relevant date):
   - **Orphans** — a worktree on disk with no matching `ACTIVE` row.
   - **Stale actives** — an `ACTIVE` row older than `config.json`'s
     `esg.max_incident_age_days` (default 7).
   - **Deploy-pending** — a `MERGED` row with no later `DEPLOYED`
     transition yet.
   - **Dangling branches** — a `dcs/*` branch, unmerged, with no live
     worktree and no `ACTIVE`/`QUEUED` row referencing it.
4. Nothing found by the audit is auto-deleted. Every flagged item is
   surfaced loudly with the exact cleanup command (`git worktree remove
   <path>`, `git branch -D dcs/<slug>`) — the audit's job is to make
   forgetting impossible, never to act unilaterally on the Owner's behalf.

Three surfaces turn an audit finding into an actual fix, none of them
optional: the audit itself (above) finds it; `/dcs-esg` agenda item (f)
— worktree/branch hygiene — is where the Owner decides (finish / park /
kill) at a standing session, and **parking an incident always removes its
worktree** (a parked incident is a register row and a kept branch, never
a directory quietly aging on disk); the gate's `.dcs/CLOSED` zombie rule
(`dcs_gate.py`) makes a worktree that slipped past both unusable in the
meantime, so it can never quietly become a second life for stale, already-
merged work (principle 11's one deliberate fail-closed exception).

**Automation layers note:** `/dcs-loop` (v0.2) stays serial in v0.3 — it
still runs exactly one incident at a time off the register queue, even
though that queue may now hold several `ACTIVE` rows opened by human-
driven parallel sessions. Running `/dcs-loop` itself *across* parallel
worktrees is explicitly out of scope for v0.3 (`docs/spec-v0.3-parallel.md`'s
non-goals): parallelism in this version is for human-driven parallel
sessions — one worktree, one session — not for the unattended loop to fan
out on its own.
