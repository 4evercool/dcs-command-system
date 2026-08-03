# 201 — Incident Brief

**Incident:** spawn-effort-control
**Opened:** 2026-08-03 (typed and Owner-confirmed at the stem; QUEUED on a territory conflict, not yet opened — see Type + rationale)
**Type:** 1

## Symptom

DCS has no mechanism for varying reasoning/thinking effort per subagent
spawn. Every one of the six `agents/dcs-*.md` charters pins exactly one
static `model:` value in frontmatter and sets no `effort:` key at all
(confirmed: `grep -ri effort agents/` returns zero matches, and none of
`schemas.md`'s nine structured contracts or `dcs/templates/204-TASKING.md`
carries a model or effort field). The one existing per-spawn dynamic
behavior in the package — doctrine.md's "Model availability" tier-fallback
rule (line 31) — reacts to whether Fable is currently reachable, not to how
complex the work is, and is scoped to the `dcs-commander`/IC seat at its 4
command points only; it never touches the other five seats (chiefs,
specialists, Safety Officer, analysts), which account for the large
majority of spawns in any incident (Specialists alone run up to 4 per
section per period — doctrine.md:48). The Owner wants the IC to be able to
decide, per spawn, how hard a given piece of work deserves to be thought
about — a routine typo fix and a multi-file architectural tactic
shouldn't cost the same reasoning budget — and wants that decision built
so it doesn't assume every future spawnable tier speaks Claude's
low/medium/high/xhigh/max vocabulary.

## Evidence

- All six charters set only `model:`, never `effort:` — verified by
  reading every charter's frontmatter and by `grep -ri effort agents/`
  (zero hits). `agents/dcs-ops-specialist.md:5`,
  `agents/dcs-situation-analyst.md:5` (`model: sonnet`);
  `agents/dcs-planning-chief.md:5`, `agents/dcs-logistics-chief.md:5`,
  `agents/dcs-safety-officer.md:5` (`model: opus`);
  `agents/dcs-commander.md:5` (`model: fable`) — restated in
  `doctrine.md:40-48`'s Hierarchy table.
- `doctrine.md:31` (exact text): "**Model availability:** \"Fable\" = the
  strongest tier available. If `dcs-commander` with `model: fable` fails,
  re-spawn with the strongest tier that works and log the actual seat.
  **Availability is per-spawn and MUST be re-tested at every command
  point (v0.6.1).** **Never cache the fallback — try the preferred tier
  first every single time.**" Scope is bounded by `doctrine.md:17`
  ("Command transfers to the qualified IC") — the 4 command points named
  at `doctrine.md:24-27`, not every spawn.
- `schemas.md` #6 (Commander decisions, lines 112-137) is keyed to exactly
  those 4 command points (`typing`, `iap_review`, `deviation`,
  `verdict_disposition`); its one cross-cutting field, `esg_activation`
  (`Command point = "any"`), still only rides on a `dcs-commander`
  decision at one of those points — no field or point exists today for a
  decision fired at ordinary chief/specialist/analyst spawn time.
- Full-file grep of `schemas.md` (187 lines, all 9 contracts) and
  `dcs/templates/204-TASKING.md` (49 lines — the literal content a
  spawned specialist receives) for "model": zero matches in either.
- Ten actual spawn call-sites exist across four workflow files:
  `new.md:55,127,151`; `plan.md:35,89`; `execute.md:68,106,132,157`;
  `esg.md:49`. `close.md`, `deploy.md`, `run.md`, `loop.md`, `status.md`,
  `init.md` spawn no `dcs-*.md` agents of their own.
- **Hot-path budget is nearly exhausted, and this is load-bearing for
  scope.** Live measurement this session: `doctrine.md` + `schemas.md` =
  37,838 of the 37,888-byte ceiling (`HOT_PATH_BUDGET_KB = 37`,
  `tests/test_doctrine_integrity.py:212`) — **50 bytes of slack.** Both
  files this design would extend have each already needed a dedicated
  trim incident before (`2026-07-25-doctrine-hot-path-trim`,
  `2026-07-26-schemas-md-trim`,
  `2026-07-30-hot-path-budget-emergency-trim`), and one incident exists
  specifically because a trim lost content
  (`2026-08-01-trim-content-loss-restoration`) — any new principle/schema
  text this incident adds will not fit without an offsetting trim
  elsewhere, and that trim itself is a known failure mode in this
  project's own history, not a hypothetical risk. **Owner ruling
  (command point 1 gate, 2026-08-03): the design must fit inside the
  existing 37 KB ceiling — trims fund the addition; no
  `HOT_PATH_BUDGET_KB` increase.** Planning must treat the ceiling as
  fixed.
- Workflow line-count margins (guard-exact, all files LF-terminated —
  `tests/test_doctrine_integrity.py`'s `WORKFLOW_BUDGET_LINES = 250`,
  `WORKFLOW_GRANDFATHERED_LINES = {"new.md": 270}`): `new.md` 263/270 (7
  slack), `plan.md` 249/250 (1 slack), `execute.md` 248/250 (2 slack),
  `deploy.md` 245/250 (5 slack), `close.md` 244/250 (6 slack), `init.md`
  exactly 250/250 (0 slack, though `init.md` spawns nothing here). This
  corroborates the Owner's own scouted note: effort-decision prose has
  nowhere to go in the 3 workflow files that actually spawn agents
  (`new.md`, `plan.md`, `execute.md`) — it has to live in
  `doctrine.md`/`schemas.md`, competing for the same 50 bytes above.
- **Correction to the Owner's second citation.** `deepseek-v4-pro`
  (`vault/Meta/building-dcs-lessons.md:1016-1056`, incident
  `token-economy-advisory-fixes`) is documented as *"the Agent tool's
  safety classifier"* — infrastructure belonging to the Task/Agent tool
  itself (verified word-for-word against the primary source,
  `.dcs/incidents/2026-07-30-token-economy-advisory-fixes/AAR.md:36`). It
  never appears as a `model:` value in any charter or as a row in
  doctrine's Hierarchy table. It is evidence that a non-Claude model
  already sits somewhere in the operating stack and can gate spawns when
  unavailable — it is **not** evidence that DCS itself has ever assigned
  incident work to a non-Claude seat tier, and it carries no effort
  vocabulary of its own. Requirement 2 (provider-agnostic effort
  vocabulary) is therefore new ground this design has to originate, not
  an existing pattern it can extend — noted as an open question below,
  not a blocker to typing.
- `vault/Backlog.md` item 25 (lines 1133-1176, confirmed accurate)
  concerns which single static Claude-family tier (Fable vs. Opus) should
  staff the ESG Chief-of-Staff seat — decided once per ESG session, not a
  per-spawn dial. Genuinely adjacent, not a duplicate, as the Owner
  framed it; no other Backlog item or vault Decision/Post-mortem touches
  effort, reasoning tiers, or per-spawn model tuning
  (`vault/Decisions/non-anthropic-hardening.md`'s "Delegation model
  floor," lines 83-92, is the next-closest adjacent mechanism and gates
  the *operator's* session model for whole-incident trust, a different
  axis again).
- **Territory conflict found at new.md step 7b (v0.3 check), before any
  worktree was created.** `REGISTER.md`'s only `ACTIVE` row,
  `close-integrity-guard-bundle` (Type 1, refined territory as of
  `/dcs-plan` step 5a, 2026-08-03), claims
  `dcs/references/doctrine.md`, `dcs/references/doctrine-appendix.md`,
  and `tests/test_doctrine_integrity.py` — all three inside this
  incident's own estimated blast radius. That incident is deep into
  execution (period 1, attempt 2 after one replan; `SAFETY-PASS` logged
  2026-08-03T13:24:29+11:00, one command point from close) — concurrent
  edits to the same constitution file by two worktrees is exactly the
  risk principle 6 exists to prevent, and this repo has a documented
  history of doctrine.md trims losing content
  (`2026-08-01-trim-content-loss-restoration`). Refused by default per
  `new.md` step 7b; this incident is QUEUED, not opened.

## Appended note (2026-08-03, at 202 drafting — blast radius/premise correction, not a rewrite)

**Platform-capability finding, verified via `claude-code-guide`, load-bearing
for what "dynamic per-spawn effort" can mean:** subagent frontmatter does
support a static `effort:` key (confirming the Owner's premise), but the
interactive Agent/Task tool that every DCS workflow actually spawns
subagents through — the one with `subagent_type`/`prompt`/`model` — has
**no per-invocation effort override parameter**, only `model`. The
Workflow tool's scripted `agent()` function has an `opts.effort` claimed
in its own tool description, but independent research found it unconfirmed
as shipping (a duplicate-marked feature request exists for it, and a
frontmatter `effort:` key was observed to have no effect inside a
workflow run). **Net: today, no DCS spawn path — interactive Agent tool or
Workflow-script — has a verified, working per-call effort dial.** The one
lever that verifiably IS per-call today is the `model` override parameter,
which already exists precisely because doctrine's Fable
availability-fallback rule uses it. This reframes both Owner requirements
around what's real: requirement 1 ("decided dynamically, per spawn")
is achievable today only through **tier substitution** (spawning the same
seat on a stronger or weaker model for this specific piece of work),
which is a natural, small extension of the *existing* tier-fallback
mechanism rather than a wholly new one — good news against the 50-byte
hot-path constraint. Requirement 2 (provider-agnostic vocabulary) still
holds and is now easier to satisfy honestly: a rule phrased as "select the
tier the complexity warrants, from what's available" never has to name
Claude's specific low/medium/high/xhigh/max scale at all, and upgrades
transparently if/when a real per-call effort parameter ships. This does
not change the incident's Type or blast radius — the affected-files list
above stands — but it is likely to change 202's acceptance criteria and
the shape of the eventual doctrine text, so it is recorded here rather
than only in 202, per this file's own "append a note" allowance.

## Reproduction path

Current-state gap (feature request, not a bug):

1. Any of the six `agents/dcs-*.md` charters spawns today with exactly
   the reasoning effort Claude Code applies by default for that
   charter's pinned `model:` — no DCS workflow or agent ever passes an
   effort override, static or dynamic.
2. `doctrine.md:31`'s only per-spawn dynamic-tier rule is
   availability-driven ("is Fable reachable right now"), not
   complexity-driven, and is scoped to the IC's 4 command points only.
3. `schemas.md` #6 has no field and no command-point value for a
   decision issued at ordinary spawn time, so even if the IC judged "this
   tasking needs more effort," there is no schema slot to record that
   judgment and no workflow instruction telling any seat to pass it
   through to the spawn.
4. Net effect: no seat — IC included — has a mechanism, static or
   dynamic, to vary reasoning effort by task complexity for any of the
   ~90%+ of spawns that never touch `dcs-commander`.

## Blast radius (best guess at intake)

- `dcs/references/doctrine.md` — constitution; likely site for a new
  effort-availability principle mirroring the Fable tier-fallback rule
  **(collides with `close-integrity-guard-bundle`'s ACTIVE territory)**
- `dcs/references/schemas.md` — #6 Commander decisions likely needs a new
  field/shape for a per-spawn effort decision
- `dcs/references/doctrine-appendix.md` — provenance/field-lesson home,
  never hot-path budgeted **(collides with `close-integrity-guard-bundle`'s
  ACTIVE territory)**
- `agents/dcs-commander.md`, `dcs-logistics-chief.md`,
  `dcs-ops-specialist.md`, `dcs-planning-chief.md`,
  `dcs-safety-officer.md`, `dcs-situation-analyst.md` — all 6 charters,
  if effort selection is expressed per-seat
- `dcs/workflows/new.md`, `plan.md`, `execute.md`, `esg.md` — the 4 files
  holding all 10 spawn call-sites; at minimum need a pointer to the new
  doctrine rule, budget permitting
- `dcs/templates/204-TASKING.md` — specialist tasking template, if a
  tasking should carry a recorded effort decision
- `tests/test_doctrine_integrity.py` — enforces the hot-path/line budgets
  this design must fit inside; no logic change expected, but every
  addition is checked against it **(collides with
  `close-integrity-guard-bundle`'s ACTIVE territory)**

Planning Chief refines this into an actual disjoint territory partition;
this is a starting hypothesis, already past Type 3's ~4-file bound on its
own.

## Prior art

`vault/Meta/building-dcs-lessons.md` §25 and `vault/Backlog.md` item 25
are both accurately cited by the Owner but are weaker prior art than the
intake implies (see Evidence above): §25's `deepseek-v4-pro` is Agent-tool
infrastructure, not a DCS-assigned seat tier, and carries no effort
vocabulary; Backlog item 25 is a single static per-seat tier choice, not a
per-spawn dial. `doctrine.md:31`'s Fable availability-fallback rule is the
closest true structural precedent — same "re-test per spawn, never cache"
shape the Owner's own brief points at — but it has never before been
asked to carry a second axis (effort, not just which tier) or a
non-Claude vocabulary. No prior incident or vault entry addresses
reasoning-effort control itself. `.dcs/esg/QUEUED-201/` itself (this
file's location) follows the precedent `release-provenance-guard` and
`tag-refname-disambiguation-hole` set for a stem refused at step 7b on a
territory conflict.

## Type + rationale

**Proposed type:** 1
**Rationale (dcs-commander, Fable, command point 1, verified live against
the repo before deciding):** "Verified live: a new cross-cutting
per-spawn mechanism touching ~13 files across constitution, contracts,
all six charters and four workflows, with schema-shape changes and only
50 bytes of hot-path slack forcing compensating trims of
doctrine.md/schemas.md — a maneuver this repo has documented losing
content from before — meets Type 1's new-architectural-pattern and
shared-infrastructure triggers and far exceeds Type 3's ~4-file bound."
**Owner confirmation:** confirmed as proposed (Type 1), via
`AskUserQuestion`, 2026-08-03. Same gate also settled the commander's
flagged open question: the hot-path ceiling stays fixed at 37 KB — see
Evidence above.

## Intake source (for /dcs-close to route back to)

Owner chat report, via `/dcs-run` direct intake description (not from the
register).
