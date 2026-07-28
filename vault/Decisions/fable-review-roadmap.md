---
tags: [dcs, decision, roadmap]
updated: 2026-07-27
---

# Decision: reform roadmap from the third-party review (2026-07-27)

**Decided:** 2026-07-27, Owner + Fable (bread_bot main session, model
`claude-fable-5`)
**Source:** session transcript
`~/.claude/projects/c--bread-bot/3df3e401-1e42-4ecd-8be1-3a0b077303ba.jsonl`
— the session itself was cleared by accident on 2026-07-27; this file is
the recovered record, written so the roadmap cannot be lost again.
**Status:** Phase 0 done (bread_bot commits `a661b916`, `4ae52377`).
Phase 1 was split at its own stem (IC ruling, principle 4: the pack's
root cause is a model, not a defect): `direct-resolution-lane` shipped
manifestation (a) only — the `RESOLVED` terminal state + `new.md` 7a
register write, commit `13f557d`, Safety pass with zero refutations,
Owner-UAT approved — while (b) and (c) became rows
`register-field-repair-path` and `trivial-work-inline-lane` (QUEUED,
unranked, owed to the sixth `/dcs-esg` along with `status-md-enum-drift`
and the STRATEGY objective for "the register's contract for
sub-lifecycle resolution"). The incident closed and DEPLOYED on
2026-07-27 (its register row carries the full account); `npm view
dcs-command-system versions` → 0.6.10 published (measured 2026-07-28 at
the `criterion-unmeasured-fact` close — the original sentence here said
"remains unpublished" with only in-tree regeneration commands beside it,
and was found stale by that incident's Safety Officer: the fourth field
instance of the class, `vault/Meta/building-dcs-lessons.md` §19).
**Phase 1 completed 2026-07-28:** (b) `register-field-repair-path`
closed (merge `506052c`); (c) `trivial-work-inline-lane` KILLED (folded)
into `decomposition-backlog-routing` (rank 9) — the seventh sweep ruled
triviality-bar and priority-bar are two readings of one missing bar in
`new.md` step 4a, so Phase 1(c) and Phase 2a's decomposition threshold
travel as one incident. Recommendation 2 also landed as mechanism, not
prose: `criterion-unmeasured-fact` closed (merge `35c3507`; plan lint 4a
check 3b — a criterion's claim about state outside the tree must carry
and run its establishing command). Next per this roadmap: Phase 2a
(`deviation-path-proportionality`, then `decomposition-backlog-routing`
carrying the fold), then 2b, then Phase 3. Regenerate the register half
from the rows' State cells; the registry half only from `npm view
dcs-command-system versions`.

## The review in one paragraph

Three reader agents swept six days of bread_bot's DCS history (15 closed
incidents, 58 register rows at the time). Verdict: **keep the gate and
the adversarial verifier — they are the invention; gut the prose-copying
coordination layer and give trivial work a door that costs what trivial
work costs.** The three framing measurements: intake outruns delivery
3–4×; ceremony is roughly constant per incident so small changes pay a
6–30× paper-to-code tax (`nan-guard`: 52 LOC / 11 artifacts;
`cost-dynamics-labor-toggle`: 147 LOC / 915 lines of paper, code written
*before* the incident existed); and the dominant defect source is one
seat — the Dispatcher re-typing facts between artifacts (9 of
`prod-tools-drift`'s 10 halts were not about the code).

## The nine recommendations, ranked

1. **Two proportionality lanes** — inline-fix recommendation at stem +
   field-repair registration; actually use Type 5.
2. **Stop prose transcription between seats** — facts move by file
   reference and regenerating command; the Dispatcher copies bytes or
   cites paths, never re-types values.
3. **Make the register structured data** (see below — the SQLite/JSONL
   decision).
4. **Cap decomposition** — below a priority bar, decomposed defects go
   to the backlog surface, not the register.
5. **Cheap deviation route** — pull `deviation-path-proportionality`
   forward.
6. **Provision worktrees** — `.env`, `node_modules`, `dist`, test DB; a
   ~20-line setup script at worktree creation.
7. **Wire the phantom halt ceiling; fix the upgrade path** — docs
   describing an enforcement the project doesn't have is the worst
   configuration state.
8. **Aggregate telemetry already in the 214-LOGs** — wall-clock, spawns,
   halts, code-vs-paper LOC per incident.
9. **Re-align the queue with the objective** — money rows vs.
   self-generated governance rows; ESG decision.

## Decision: split by change-kind, not by venue

Not everything through DCS (self-absorption trap: register rows about
the register), not everything outside (two evidence-backed reasons: the
adversarial verify has repeatedly refuted "obvious" designs —
`migration-number-allocation`, `external-copies` — and unrecorded
outside edits to the enforcement layer break the audit chain that lets a
session distinguish Owner-approved reform from drift). **Mechanical
repairs with no design ambiguity run outside, recorded post-hoc; design
changes with failure modes run through the process with a Safety pass.**

## Decision: the register becomes structured data (SQLite or JSONL)

Recommendation 3 verbatim, recovered: bread_bot's `REGISTER.md` at 291
KB / 803 lines / 58 data rows with multi-paragraph table cells, re-read
every cycle, **"is a database pretending to be a document."** JSONL or
SQLite **with a generated markdown view** kills, in one move:

- the size tax (291 KB re-read every cycle);
- the format breakage (broke three days running; each catch was manual —
  and after a session reported "0 malformed," two more appeared);
- the manual re-rank gap (rows invisible to `--next` for a week:
  `tools-action-log-trail`, `voice-assistant-dead-receipt-ref` never
  ranked once);
- the silent-decay class (`cancel-leaves-receipt-attach-mode` sat at
  priority 3–4 after its surface was demolished; delivered work was
  invisible to the portfolio three times).

Plus: **archive DEPLOYED/KILLED rows out of the hot file.** A later
argument discovered during Phase 0: bread_bot's `.dcs/esg/` is
gitignored, so field-repair rows currently have **no history at all** —
a structured store with its own history fixes that too.

**npm consequence (this is why it moved to late Phase 2):** with
external users, a register format change requires a converter command
(existing markdown register → new format), a format-version marker in
the file so workflows can detect what they are reading, and arguably a
semver major. That is a genuine Type 1 by DCS's own typing rules —
schema-migration territory, Owner-mandatory.

## Decision: decouple the deviation route from the structured register

Both were rank 5 and rank 8 in this repo's own register; the original
plan shipped them together. The npm reality split them: the deviation
route is channel 1 (workflows/doctrine only, auto-propagates on
`npm i -g`) and cheap; the structured register is a data migration.
**The deviation route ships first, alone.** The
transcription-by-reference doctrine change (rec 2) rides with whichever
incident touches `schemas.md` first.

## Decision: the author never verifies the author's designs

Fable's own caveat, kept as a standing rule for this roadmap: the
Phase 1–2 incidents spawn the Safety seat even though the proposer wrote
the designs — *because* the proposer wrote them. The record shows
officers overturning the IC; that feature is pointed at this roadmap's
own work.

---

# The phases, in full (final, npm-aware form)

Three delivery channels frame everything, and each phase names its
channel: **(1)** `npm i -g` refreshes `~/.claude/dcs/` only — workflows,
doctrine, skills arrive downstream automatically; **(2)** project hooks
arrive only via re-running `/dcs-init`; **(3)** `.dcs/config.json` keys
never reach an existing project automatically.

## Phase 0 — field repairs, outside DCS, recorded post-hoc — DONE

Mechanical, no design ambiguity; deliberately doubled as the first live
specimens of the field-repair convention Phase 1 proposes.

1. **Wire the phantom halt ceiling in bread_bot.** Copy
   `.claude/hooks/dcs_gate.py` from the *installed* package (not the
   `C:\DCS` dev tree — that would create a project running hook code
   matching no published version); add `esg.max_halts_per_attempt: 3` by
   hand (channel 3 never propagates). Verified: `grep -c halt_cycles` →
   8 (was 0), `py_compile` clean, parity diff empty, smoke of
   `--halt-count` prints the expected 0 on the old-grammar log. Commit
   `a661b916`.
2. **Worktree provisioning script** `.dcs/provision-worktree.ps1` —
   idempotent: `.env`, local DB without WAL sidecars, `node_modules`
   junction guarded by a package-lock comparison, `dist` copy. Live
   smoke on a throwaway worktree, all four targets, `[skip]` on re-run.
   Stays bread_bot-local, register row marked **LOCAL — candidate for
   upstreaming**. Commit `4ae52377`.
3. **Post-hoc register rows** `dcs-gate-halt-ceiling-wired` and
   `dcs-worktree-provisioning-local` — Type 5, DEPLOYED under the
   "deploy not applicable" convention, facts with regenerating commands.

Deviation handled on the way: the whole-table format check caught a
pre-existing 13-field row (line 73, missing trailing pipe) — third
recurrence of the format class in three days, logged as evidence for the
structured register.

## Phase 1 — the proportionality pack, one incident in `C:\DCS`

Now register row **`direct-resolution-lane`** (the stem decomposed item
4 into its own row — see Phase 2a). Scope, per the 201:

1. **Type 5 register-write gap** — `new.md` step 7a's five substeps
   never touch `REGISTER.md`; the only register write lives in the
   Type 3/1 branch (7b/4a). Two-layered: the state enum
   (`QUEUED|ACTIVE|MERGED|DEPLOYED|PARKED|KILLED`) also has no terminal
   state fitting "resolved via Type 5, no worktree ever existed." A
   Type 5 pulled off the queue leaves its row QUEUED forever.
2. **Field-repair convention** — Owner-authorized fixes applied outside
   the lifecycle get one post-hoc register row (state, one-line outcome,
   diff reference; optionally one retroactive Safety look). No incident
   directory, no 201/IAP/AAR. Zero existing carrier anywhere in
   doctrine/templates/workflows; the two bread_bot rows are the live
   specimens.
3. **Inline-fix recommendation at stem** — when `/dcs-new` or an ESG
   sweep sizes work as trivial, output the recommended diff for outside
   application plus a post-hoc row, instead of a QUEUED row awaiting a
   full lifecycle.

**Why first: it is the multiplier — everything after it gets cheaper,
including its own successors.**

Ship shape (the npm revision): this is a release, not a doc edit.
Acceptance criteria include a safe version bump (the PowerShell mojibake
hazard is live until `version-bump-command` closes — use the Edit tool
path), CHANGELOG entry, `npm publish`, and **post-publish verification
against the registry itself** (`npm view` version + tarball checksum,
not the local tree — the exact check that would have caught the 0.6.9
double-publish). Channel 1 only, so downstream projects need no
`/dcs-init` re-run. Semver: minor. Registry context at decision time:
npm holds 0.6.9, tree is 0.6.10 unpublished.

Register reconciliation, settled at the stem: `type5-express-lane-tuning`
stays PARKED (it is about typing conservatism, not this mechanical gap);
`deviation-path-proportionality` is disjoint territory — leave it alone;
`esg-artifact-bloat` is related (fix 4 shrinks its growth) but a
different root — flag, don't fold.

Resume command: `/dcs-run --next` in a `C:\DCS` session.

## Phase 2 — two decoupled incidents in `C:\DCS`

**2a — cheap, ships first:**
- **Deviation route** (`deviation-path-proportionality`, was rank 5): a
  one-line tasking amendment currently costs a full re-plan because any
  edit voids the IAP hash; a one-line export crossing `max_files` cost a
  sitrep and an Owner decision at 00:40. Build the cheap-but-still-
  counted route the backlog already names. Channel 1, minor version.
- **Decomposition threshold** (`decomposition-backlog-routing`, rank 9,
  split from this pack's stem): below a priority bar, decomposed defects
  land in the project's backlog/tech-debt surface, not the register.
  Evidence: 35 of 58 bread_bot rows were minted by four Type 1
  decompositions; 13 of 60 rows cite stem decomposition as their intake.
- Rec 2 (transcription by reference) rides with whichever incident
  touches `schemas.md` first.

**2b — the hard one, later or with a migration:**
- **Structured register** (SQLite/JSONL + generated markdown view, per
  the decision above) with converter, format-version marker, archive of
  terminal rows out of the hot file. Type 1, Owner-mandatory, arguably
  semver major.

## Phase 3 — not code

- **Queue-vs-objective re-alignment** — an ESG session decision in
  bread_bot by construction; no fixer, inside or outside, can make it
  for the Owner. Either the money rows move up or the objective changes.
- **Telemetry table** (rec 8) — can be a field repair once the
  halt-grammar row is fixed; one generated table per incident
  (wall-clock, spawns, halts, code LOC vs paper LOC) would have made
  every observation in this review visible weeks earlier.
- **`dcs doctor`-style upgrade check** — installed package version vs.
  project hook version vs. config keys present. Named in the review as
  probably the highest-value small feature npm distribution creates: the
  Phase 0 phantom-ceiling fix will recur in every external user's
  project on every hook-touching release (channels 2 and 3 never
  propagate). Register row `doctor-version-only-check` suggests part
  exists and is known to be shallow.

## Reopen / amendment conditions

- If Phase 1's incident refutes the field-repair design at Safety, the
  phase split itself stands — only the mechanism re-plans.
- If external npm users materialize before Phase 2b, the migration
  requirements harden from "arguably major" to "major, with a tested
  converter."
- Phase 3's ESG item does not expire: STRATEGY.md records the
  queue-vs-objective tension as "open, not raised for reconsideration" —
  this file exists so it *is* raised.

## Links

- [[Backlog]] — items 5 (version bump) and 6 (Type 5 under-use) predate
  this review and are absorbed by Phases 1–2
- [[Decisions/cross-project-register-view]] — earlier register-shape
  decision this roadmap does not disturb
- [[Metrics/incident-metrics]] — where rec 8's table belongs when built
