<purpose>
The stem of the Planning P: turn an intake report into a typed incident.
Gathers intel via dcs-situation-analyst subagents, writes 201-BRIEF.md,
proposes and confirms a Type, then either runs the Type 5 express lane to
completion inline or opens a gated incident directory and hands off to
/dcs-plan.
</purpose>

<required_reading>
@$HOME/.claude/dcs/references/doctrine.md
@$HOME/.claude/dcs/references/typing.md
@$HOME/.claude/dcs/references/schemas.md
</required_reading>

<process>

## 1. Intake

`$ARGUMENTS` is the intake description — a user report, a bug, or a
reference to an `audit_results` `needs_fix` row. If it's a bare reference
(e.g. a row id) rather than a description, read enough to understand what
it's asking for before proceeding (e.g. query the row itself if the
project documents how).

**(v0.2)** Intake may also simply be `"next from the register"`. If so,
read `<project>/.dcs/esg/REGISTER.md`'s `QUEUED` rows (topmost by the
order `STRATEGY.md`'s ranked priorities implies, or table order if
`STRATEGY.md` doesn't exist) and use that row's title as the intake
description. If `REGISTER.md` doesn't exist, or exists with no `QUEUED`
rows, stop and tell the Owner there's nothing queued — run `/dcs-esg`
first, or pass a concrete intake description instead.

Determine the project root. Verify `<project>/.dcs/` exists — if not, stop
and tell the Owner to run `/dcs-init` first.

## 2. Check for an already-active incident

```bash
cat "<project>/.dcs/ACTIVE" 2>/dev/null
```

Here `<project>` is wherever this session is rooted — the main checkout,
or (v0.3) an incident worktree if the session was started there. If
present: **stop.** Report the active incident (slug, type, phase) and
tell the Owner to finish it (`/dcs-plan`, `/dcs-execute`, or `/dcs-close`
as appropriate — see `/dcs-status` for exactly which) or explicitly close
it before opening a new one. This is single-incident-per-tree by design
(doctrine's v0.1 constraints, rescoped by v0.3) — not negotiable from
within this workflow. It is **not** the portfolio-wide check — a second
incident can be perfectly legitimate in a different worktree; that's
what the territory check in step 7b guards, not this one.

## 3. Spawn situation analysts

Spawn 1-2 `dcs-situation-analyst` subagents via the Task tool (in parallel,
both in one message, if using two). Give each: the intake description
verbatim, the project root, and the path to the project's `CLAUDE.md` if
it exists. If spawning two, split the angle (e.g. one on
reproduction+logs, one on codegraph impact+prior art) rather than having
both do identical work.

Each must return a JSON block per schemas.md #1 (situation-analyst
findings): required fields `summary` (string), `evidence` (string[]),
`affected_files` (string[]), `repro_path` (string), `prior_art` (string).

Validate each return: confirm a JSON block is present, all required fields
per schemas.md #1 (situation-analyst findings): `summary`, `evidence`, `affected_files`, `repro_path`,
`prior_art`) are present, and no fields outside the schema appear. Missing
required field or structural non-JSON = deviation — re-spawn that analyst.
Collect the findings. If the two disagree on something material (e.g. one
finds a repro path the other calls unreproducible), note the disagreement
rather than silently picking one — it belongs in the 201 as an open
question.

## 4. Draft 201-BRIEF.md

Use `$HOME/.claude/dcs/templates/201-BRIEF.md`. Fill in Symptom, Evidence
(one bullet per finding, citation intact), Reproduction path, Blast radius,
Prior art, and Intake source. Leave Type + rationale for the next step.

## 4a. Decomposition check — ONE incident, ONE defect (v0.5.12)

**This is the cheapest place in the whole system to prevent a runaway
incident, and the only place that is free.** Read the Symptom you just
wrote and count the *independent* defects in it. Independent means: it
has its own root cause, and fixing it could ship on its own.

- **More than one → decompose now.** Give each a proposed Priority
  (`H`/`M`/`L`, the register template's vocabulary). Register every
  defect at `H`/`M` as its own row in `<esg_root>/.dcs/esg/REGISTER.md`
  (`QUEUED`), then open **one** — the one on the critical path, usually
  the one actively causing harm. The others are follow-ups with the
  evidence already gathered; each can ship the day it is fixed.
- **(v0.6.13) `L` is below the bar.** It goes to the project's own
  lightweight backlog-style surface instead of a register row, if its
  `CLAUDE.md` documents one (doctrine's "Relationship to
  project-specific protocols"); documenting none, the row is written as
  before, so no portfolio loses visibility by omission. Harm is never
  `L`.
- **A "rework" / "rethink" / "redesign" goal is a program, not an
  incident.** If the goal names a *model* rather than a *defect*
  ("rethink how X is accounted"), the incident to open is the first
  concrete defect that model causes; the redesign is a STRATEGY item for
  `/dcs-esg`.
- Say plainly in the report which defects were split out and where they
  went — the Owner should see the decomposition, not discover it.

**Field lesson 2026-07-23/24 (the incident this rule exists for):** a
201 opened with "the energy model is wrong" **and** noted three
accompanying defects, one of them actively corrupting production data.
All four were absorbed into a single Type 1. It ran **31 hours, 3
periods, 4 revisions of period 1, 10 Safety halts, 3 escalations, a
285 KB log, 54 files and 11,000 lines**, and spawned its own blocker
incident mid-flight. Every *individual* mechanism behaved correctly
throughout — the halts were right, the rejects were right, the blocker
was real. The cost came from scope that was admitted at intake and never
bounded afterwards. Nothing downstream can undo an over-scoped 201;
typing sets *ceremony*, it has never set *size*.

**Sanity check (a smell, not a gate):** DCS briefs for well-scoped
incidents run ~7–11 KB. If yours is two or three times that, it is
probably describing more than one incident — reread it before typing.

## 5. Propose a Type — COMMAND POINT 1 (typing)

This is a command point (doctrine: "Transfer of command"). **If this
session is not running Fable**: spawn `dcs-commander` via Task (model
`fable`), passing the draft 201-BRIEF.md text in full; take its `typing`
decision (schemas.md #6, commander decisions) as the proposal and record it in the eventual
214-LOG.md as `command: typed <N> (IC=dcs-commander)`. **If this session
is Fable**, you are the IC — decide yourself using `references/typing.md`'s
triggers and concrete examples: Type 5, 3, or 1 with a one-sentence
rationale grounded in what the analysts actually found (file count, whether
the fix is obvious, whether it touches schema/architecture/shared
infrastructure). Either way, the Dispatcher never substitutes its own
typing judgment to save a spawn.

## 6. Confirm typing with the Owner

Use `AskUserQuestion`: present the proposed type + rationale, with options
to accept it or override to a different type (with the Owner's own
reason). Write the final type + rationale + confirmation outcome into
201's "Type + rationale" section.

## 7a. Type 5 — express lane

No incident directory, no `ACTIVE` file, no gate involvement at all.

1. Assemble a micro-tasking inline (not written to disk) describing the
   one-file fix directly from the 201 findings.
2. Spawn **one** `dcs-ops-specialist` via Task with that inline tasking —
   frame its territory as the single implicated file, forbidden as
   everything else, evidence required as whatever test covers it (or "run
   the repro manually" if none exists).
3. When it returns, the IC verifies the result itself: read the diff,
   run the relevant test/repro if one exists. Do not simply trust a
   `status: "done"` return without looking — Type 5 skips the Safety
   Officer specifically because the IC is expected to do this check
   personally, given the small scope.
4. Report a one-line AAR-equivalent to the Owner in chat: what was
   wrong, what changed, what was verified. This is not written to any
   file — Type 5 explicitly has no incident directory per doctrine's
   typing table.
5. **Update the register, if one already knows this incident.** Resolve
   `esg_root` as step 7b substep 4a does. If
   `<esg_root>/.dcs/esg/REGISTER.md` exists and holds a row for this
   incident, set that row's state to `RESOLVED`, fill Closed and
   Outcome, and leave Worktree and Branch as the em-dash the row
   template already prescribes for an incident that never opened one.
   Otherwise — no register, or no matching row — do nothing and report
   nothing.
6. Done. No `/dcs-plan`, no `/dcs-execute`, no `/dcs-close` — the
   incident never opened a gate to begin with.

## 7b. Type 3 / Type 1 — open a gated incident

**(v0.3) Territory check against the register — before anything else.**
Resolve `esg_root` (doctrine "Parallel operation": `git worktree list
--porcelain`, first entry is always the main checkout). If
`<esg_root>/.dcs/esg/REGISTER.md` exists, compute this incident's initial
territory as glob(s) from the situation analysts' `affected_files` (the
201's blast radius), and compare it against every `ACTIVE` row's
`territory` column. If any overlap: **refuse by default** — do not create
a worktree yet. Tell the Owner which `ACTIVE` incident conflicts and why,
add this incident as a `QUEUED` row in the register (territory recorded,
no worktree/branch yet), and stop — it opens once the conflicting
incident closes, or is parked/killed. The Owner may explicitly override
(accept merge-conflict risk); if so, record the override in **both**
rows' Notes (this incident's and the conflicting one's) and continue
below. If `REGISTER.md` doesn't exist, skip this check — no portfolio to
conflict with yet.

**(v0.3) Create the branch and worktree** (Type 5 never gets one — see
step 7a). From the main checkout:

```bash
git worktree add "<repo-parent>\<repo>-wt\<slug>" -b "dcs/<slug>"
```

(`<repo>-wt\` is a sibling directory of the repo, created automatically
the first time any incident needs one).

**(v0.7.1)** After the worktree is created, check whether
`<project_root>/.dcs/provision` exists. If it does, run it with the new
worktree path as the first argument and the main checkout root as the
second. Non-zero exit: warn the Owner and proceed. Absent file: skip
silently.

Everything below — the incident
directory, `201-BRIEF.md`, `214-LOG.md`, `ACTIVE` — is written **inside
this worktree**, never in the main checkout.

1. Create `<worktree>/.dcs/incidents/<YYYY-MM-DD>-<slug>/` (slug: the same
   short kebab-case description used for the branch and worktree above).
2. Write the finished `201-BRIEF.md` into that directory.
3. Initialize `214-LOG.md` from the template, with the incident's slug and
   first entry (`incident opened, type {N}, phase=planning`), followed
   immediately by the command point 1 entry from step 5
   (`command: typed {N} -- <rationale> (IC=<dcs-commander|this Fable
   session>)`) — `/dcs-plan`'s pre-stamp checklist will refuse to stamp an
   approval if this entry is missing.
4. Write `<worktree>/.dcs/ACTIVE` with content:
   `<incident-directory-name>|<type>|planning` — the first field is the
   **EXACT directory name** under `.dcs/incidents/`, i.e. the full
   `<YYYY-MM-DD>-<slug>` including the date prefix, NOT the bare slug
   (field defect 2026-07-22: a bare slug made a valid approval invisible
   to the gate's lookup and every territory edit was denied; the hook now
   tolerates the bare form when it's unambiguous, but the exact name is
   the contract). Exact pipe-delimited format — the gate hook parses this
   literally. **(v0.3)** `.dcs/ACTIVE` is per-worktree and git-ignored —
   it never rides the branch into main.
4a. **(v0.2, amended v0.3)** Resolve `esg_root` as above. If
   `<esg_root>/.dcs/esg/REGISTER.md` exists: add or update this incident's
   row — id (slug), title, type, priority, intake source, opened date,
   **worktree** (the path from `git worktree add` above), **branch**
   (`dcs/<slug>`), **territory** (the same globs checked above) — and set
   its state `QUEUED` → `ACTIVE` (or insert a new `ACTIVE` row if it
   wasn't already queued; not every incident originates from the
   register). If `REGISTER.md` doesn't exist: **warn the Owner loudly
   before proceeding** (v0.3.2) — a worktree incident with no register
   runs with zero portfolio visibility: cross-incident territory
   partitioning cannot be enforced (nothing stops a second incident
   claiming the same files), the `MERGED (deploy pending)` state at close
   has nowhere to live, and the forgotten-worktree audits have nothing to
   audit. Recommend founding the ESG now (`/dcs-esg` in the main
   checkout, ~2 minutes); proceed without it only on the Owner's explicit
   acknowledgment, and record that acknowledgment in `214-LOG.md`. The
   register remains optional for non-worktree work.
5. Tell the Owner the incident is open, its worktree path, and that the
   next step is `/dcs-plan`. Recommended pattern: start the next session
   rooted in the worktree directory; same-session continuation from here
   also works (the gate now judges by the target file's own path, not
   session cwd — see `dcs_gate.py`'s v0.3 root resolution), just be
   deliberate about writing into the worktree path, not the main
   checkout's.

## 8. Report

Summarize what was found, the confirmed type, and (for Type 3/1) the
incident's slug and directory path, or (for Type 5) the completed fix and
verification.

</process>
