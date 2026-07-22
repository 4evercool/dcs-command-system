# DCS v0.3 — Parallel incidents: worktree isolation + deploy train

**Status: DRAFT — awaiting Owner review.** Implements multi-incident
operation. Supersedes the v0.1 "one incident active at a time" constraint
and the v0.2 non-goal "no multi-active-incident execution."

## Context

The pain: parallel dev sessions share one working tree, and the project's
deploy ships the whole tree — so no session can deploy until every other
session's work is done, and a deploy performed carelessly ships someone's
WIP. DCS v0.2 formalizes the serialization (single `.dcs/ACTIVE`) instead
of fixing it; worse, two sessions on one checkout would have their edits
judged against each other's incident phase by the gate.

The fix has three parts: **(1)** each incident gets its own git worktree +
branch, so parallel work is physically isolated; **(2)** terrain
partitioning (doctrine principle 6) is lifted to the portfolio level, so
concurrent incidents hold disjoint file territories and merge cleanly;
**(3)** deploys become a serialized **deploy train** that runs only from
the always-clean main checkout, shipping exactly the set of merged,
Safety-passed incidents.

A standing Owner pain this spec MUST kill: **forgotten worktrees** that
never get merged and rot. See "No dangling worktrees" — the design makes
merging part of `/dcs-close` (not a separate chore anyone can forget) and
makes every DCS surface inventory and age anything living outside that
lifecycle.

## Layout and state split

- **Main checkout** (e.g. `C:\bread_bot`) — the "base camp": ESG state,
  merges, deploys, Type 5 express fixes, non-DCS work. Nobody develops
  Type 3/1 incidents here.
- **Incident worktrees** — `git worktree add <repo-parent>\<repo>-wt\<slug>
  -b dcs/<slug>` (container dir `<repo>-wt\` as a sibling of the repo).
  One incident per worktree; the incident's session works there.

State split (the load-bearing decision):

| State | Location | Tracked in git? |
|---|---|---|
| `.dcs/incidents/<slug>/` | authored in the incident's worktree | **yes** — rides the branch, arrives in main via the merge (the archive merges itself) |
| `.dcs/ACTIVE` | per-worktree | **no — .gitignore** (a tracked ACTIVE would merge into main and wedge the gate) |
| `.dcs/CLOSED` | per-worktree zombie marker (see gate) | **no — .gitignore** |
| `.dcs/esg/` (STRATEGY, DELEGATION, REGISTER, SITREPS, DEPLOY-LOCK) | **main checkout only** | **no — .gitignore** (operational state; branch copies would diverge) |
| `.dcs/config.json` | repo root | yes (unchanged) |

**`esg_root` resolution rule:** every workflow that touches ESG state
resolves the main checkout first — `git worktree list --porcelain`, first
entry — and reads/writes `.dcs/esg/` THERE, never in the current worktree.
Migration note for already-onboarded projects: `git rm -r --cached
.dcs/esg` (if previously tracked) + add the three .gitignore entries.

## Register: the portfolio lock table

`REGISTER.md` rows gain columns: `state`, `worktree`, `branch`,
`territory` (globs), plus existing id/title/type/priority/dates.

States: `QUEUED → ACTIVE → MERGED (deploy pending) → DEPLOYED`, with
`PARKED` / `KILLED` as side exits. `ACTIVE` now means "has a live
worktree"; multiple rows may be ACTIVE concurrently. The per-worktree
`.dcs/ACTIVE` file keeps its v0.1 role — the gate's input — while the
register holds the cross-incident view.

**Cross-incident terrain partition (principle 6, portfolio level):**
`/dcs-new` (and `/dcs-esg` when queueing) records the incident's territory
globs in its register row (initial = the 201 blast radius; refined to the
IAP partition's union after `/dcs-plan`). Opening an incident whose
territory overlaps any ACTIVE row's territory is **refused by default** —
the new incident is QUEUED behind the conflicting one, and the Owner is
told why. Owner may override (accept merge-conflict risk); the override is
recorded in both rows. Disjoint territories across incidents are what make
the merges below trivially clean — same reason they make parallel
specialists safe within one incident.

Register mutations from parallel sessions: create-exclusive
`.dcs/esg/REGISTER-LOCK` (holder + timestamp) around read-modify-write;
treat a lock older than 10 minutes as stale (note the takeover in the
file). Human-paced contention; this is a courtesy lock, not a database.

## Lifecycle changes

**`/dcs-new` (Type 3/1):** after typing confirmation — check territory vs
register (above) → create branch + worktree → write the incident dir and
`ACTIVE` **in the worktree** → register row ACTIVE with worktree/branch →
tell the Owner where the incident lives. The recommended pattern is one
session per worktree (start the next session in the worktree directory);
same-session continuation is supported (see gate fix). Type 5 express is
unchanged: runs wherever it is, commits immediately, no worktree.

**`/dcs-plan`, `/dcs-execute`:** unchanged internally — they already
operate on "the project root," which is now the worktree. Specialists
spawned from a worktree session inherit it naturally (their edits are
absolute paths under the worktree). The IAP partition governs *within* the
incident as before; after IAP integration, `/dcs-plan` updates the
register row's territory to the partition's union (via `esg_root`).

**`/dcs-close` — the anti-rot core.** New step between the AAR and gate
release, in this order, all inside the close (an incident is NOT closed
until every one succeeds):

1. All close-out writes that belong to the repo (AAR, memory-routing
   lessons per the project's own protocol) happen **in the worktree** and
   are committed on the branch — so they ride the merge.
2. **Merge to main:** from the main checkout, `git merge --no-ff
   dcs/<slug>`. Disjoint territories ⇒ clean merge. A conflict means the
   territory promise was violated somewhere — treat as escalation trigger
   (a): stop, 209 sitrep, Owner decides. Never resolve a conflict silently.
3. Register row → `MERGED (deploy pending)`.
4. `git worktree remove <path>` (the branch is KEPT until the deploy train
   confirms it shipped — rollback reference). If removal fails (locked
   files, session still inside it): write `.dcs/CLOSED` into the worktree
   and tell the Owner it needs manual removal — the gate makes a zombie
   worktree unusable (below), so it can't quietly become a second life.
5. Only now: delete the worktree's role in the story — final sitrep names
   the merge commit and the deploy-pending state.

**`/dcs-deploy` — new command (the deploy train).** Owner-triggered, never
called by `/dcs-loop` (hard rule 2 unchanged). Process: take
`DEPLOY-LOCK` (create-exclusive; stale >30 min may be taken over with a
note) → worktree audit (below) → verify main checkout is clean (the
project's own preflight hook keeps working — main never carries WIP now)
→ list `MERGED` rows about to ship + warn about any unmerged `dcs/*`
branches → Owner confirms → run the project's documented deploy command
(discovered from the project's CLAUDE.md — never invented) → verify the
project's deployed-version marker actually advanced (facts-only rule) →
rows → `DEPLOYED`, delete their `dcs/*` branches → release the lock.
Intake-closure linkage (v0.2 close.md rule) keys off DEPLOYED, not MERGED.

## No dangling worktrees (the Owner's standing pain)

The design answer: **the human is never responsible for remembering the
merge — the close workflow is.** You cannot close without merging (it is a
close step, not a suggestion), and you cannot silently not-close, because:

- **Worktree audit** — a shared checklist run by `/dcs-status --campaign`,
  `/dcs-esg` step 1, `/dcs-loop` preconditions, and `/dcs-deploy`:
  cross-reference `git worktree list` + `git branch --list 'dcs/*'
  --no-merged main` against the register. Flag, with ages: worktrees with
  no ACTIVE register row (orphans), ACTIVE incidents older than
  `esg.max_incident_age_days` (config, default 7), MERGED rows waiting on
  a deploy, `dcs/*` branches unmerged with no live incident. Nothing in
  this list is auto-deleted — it is surfaced loudly, every time, with the
  exact cleanup command.
- **ESG agenda item (f) — worktree/branch hygiene:** the audit's findings
  become Owner decisions at every session: finish / park (worktree
  removed, branch kept, row PARKED) / kill (worktree removed, branch
  deleted, row KILLED with reason). Parking an incident ALWAYS removes its
  worktree — a parked incident is a register row and a branch, never a
  directory quietly aging on disk.
- **Doctrine principle 10 amended:** "no dangling incidents" becomes "no
  dangling incidents **or worktrees** — a worktree exists only while its
  incident is ACTIVE; close, park, and kill all remove it."
- **Gate zombie rule** (`dcs_gate.py`): if `.dcs/CLOSED` exists in the
  resolved project root → **deny all guarded edits** with "this incident
  is closed and merged; this worktree is awaiting removal — do not work
  here" (fail-closed is correct here, unlike elsewhere: the merge already
  happened, edits here are guaranteed lost work).

## Gate hook changes (`dcs_gate.py`)

1. **Root resolution from the TARGET, not the session:** currently
   `CLAUDE_PROJECT_DIR`/cwd-walk — wrong tree when a session rooted in
   main edits a file inside a worktree (env var wins, main has no ACTIVE
   → everything allowed: a real hole once worktrees exist). Fix: walk up
   **from the target file's own path** looking for `.dcs/`; fall back to
   env/cwd only for relative paths. Add lifecycle-test cases: main-rooted
   session editing worktree file (denied per the worktree's phase),
   worktree file with valid marker (allowed), `.dcs/CLOSED` zombie
   (denied).
2. `.dcs/CLOSED` zombie rule (above).
3. No other changes — per-worktree `ACTIVE` already gives per-incident
   gating via the root walk.

## Doctrine amendments

- v0.1 constraints section: single-incident becomes **single incident per
  worktree**; the portfolio constraint moves to the register (territory
  partition). Note the ergonomic recommendation: one session per worktree.
- Principle 6: add the portfolio-level sentence.
- Principle 10: amended per above.
- New short section "Parallel operation" summarizing: worktree = division
  of the fire line; main = staging area; deploy train = demobilization to
  the line only from staging; the three audits that keep worktrees from
  rotting.
- Automation layers: `/dcs-loop` may run incidents in parallel worktrees
  in future — **explicitly out of scope for v0.3** (loop stays serial, one
  incident at a time; parallelism is for human-driven parallel sessions).

## Non-goals (v0.3)

- No auto-rebase/sync of long-lived incident branches against main — the
  territory partition makes it unnecessary for the intended short-lived
  incidents; an incident old enough to need a rebase should be hitting the
  age audit and an ESG decision instead.
- No parallel `/dcs-loop` (see above). No cross-machine coordination. No
  CI integration. No automatic conflict resolution, ever.
- Deploy stays project-defined and Owner-gated; DCS orchestrates, the
  project's own deploy script does the work.

## Migration (bread_bot)

`.gitignore` += `.dcs/ACTIVE`, `.dcs/CLOSED`, `.dcs/esg/`; `git rm -r
--cached .dcs/esg` if tracked by then; create `C:\bread_bot-wt\` on first
use (automatic); everything else (deploy.sh, preflight hook, vault
protocol) is untouched — deploys just always find a clean tree now.

## Verification

1. Scratch repo: open two incidents with disjoint territories in two
   worktrees; run both to close; both merges clean; `/dcs-deploy` (mock
   deploy command) ships both rows; branches deleted.
2. Territory overlap: third incident overlapping an ACTIVE one → refused
   and QUEUED with the conflict named; Owner override path recorded.
3. Forgotten-worktree simulation: close a session mid-incident, wait, run
   `/dcs-status --campaign` and `/dcs-esg` → audit flags the worktree with
   age both times; ESG park decision removes it and keeps the branch.
4. Gate: main-rooted session editing a worktree file is judged against the
   WORKTREE's phase (target-path resolution); `.dcs/CLOSED` denies; full
   existing 14-case suite still passes plus the new cases.
5. bread_bot live: nan-guard-style Type 3 run entirely in a worktree while
   a second session dirties main with unrelated WIP; deploy train ships
   the merged incident without waiting on, or shipping, the WIP.
