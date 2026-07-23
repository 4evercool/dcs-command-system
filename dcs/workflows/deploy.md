<purpose>
The deploy train (v0.3): a serialized, Owner-gated ship of every incident
that has merged to main but not yet shipped. Runs only from the always-
clean main checkout, verifies the project's own deployed-version marker
actually advanced before declaring victory, and is the only place
`REGISTER.md` rows reach `DEPLOYED` — nothing else in DCS ships code.
Never called by `/dcs-loop` (doctrine's automation-layer hard rule 2 is
unchanged by this command's existence).
</purpose>

<required_reading>
@$HOME/.claude/dcs/references/doctrine.md
</required_reading>

<process>

## 1. Resolve esg_root and take DEPLOY-LOCK

Resolve `esg_root` (doctrine "Parallel operation": `git worktree list
--porcelain`, first entry — always the main checkout). All state below
lives at `<esg_root>/.dcs/esg/`.

Create-exclusive `<esg_root>/.dcs/esg/DEPLOY-LOCK` (contents: holder +
ISO8601 timestamp). If it already exists and is younger than 30 minutes:
**stop** — report who holds it and since when; a deploy is already in
flight or a prior one didn't clean up yet, and two deploy trains running
at once is exactly the hazard this lock exists to prevent. If older than
30 minutes: may be taken over — note the takeover (who, when, why) in the
lock file itself before proceeding. This is a courtesy lock, same
convention as `REGISTER-LOCK` (doctrine "Parallel operation" /
`templates/REGISTER.md`'s header comment) — human-paced contention, not a
database transaction.

## 2. Run the worktree audit

Follow doctrine's canonical worktree-audit checklist ("Parallel
operation" section) in full: `git worktree list --porcelain`, `git
branch --list 'dcs/*' --no-merged main`, cross-referenced against
`REGISTER.md`. Present the findings (orphans, stale actives, deploy-
pending, dangling branches) to the Owner as context before the ship
decision in step 5 — a deploy is a natural moment to also surface
portfolio hygiene, even though this workflow doesn't act on the findings
itself (that's `/dcs-esg` agenda item (f)'s job).

## 3. Verify the deploy payload is clean (v0.3.4 — scoped, not whole-tree)

"Clean" means: **no dirty tracked files among the paths the project's
documented deploy command actually ships** — discover the payload from
the project's CLAUDE.md / deploy script (e.g. a deploy that ships `src/`
and a built frontend does not care about `.claude/` hook churn or local
settings files). Field lesson 2026-07-22: a whole-tree check stopped a
deploy over three `.claude/` infrastructure files that the deploy would
never ship, and asked the Owner a question the payload scoping already
answers.

- **Payload-dirty (tracked, modified, inside what ships): stop.** Report
  exactly which files, and let the Owner commit or set them aside before
  re-running `/dcs-deploy`. Never stash, discard, or commit on the
  Owner's behalf (and never suggest `git stash` as the remedy — some
  projects forbid it outright; "commit or set aside" is the language).
- **Non-payload dirt and untracked files: never a blocker, never a
  question.** List them as a one-line warning inside the step-5 Owner
  confirmation summary instead — dirty main is still a *signal* under
  v0.3 (stray WIP, an incident that skipped the worktree flow), it just
  isn't this command's tripwire unless it ships.
- **Payload unknowable** (project documents no deploy command paths and
  the script can't be read): fall back to the strict whole-tree check —
  when you can't scope, blocking is safer than guessing.

If the project documents its own pre-deploy checks (a preflight hook, a
lint/test gate in its `CLAUDE.md` or deploy script itself), this step
does not replace them — the project's own deploy command (step 6) still
runs its own preflight; this step is DCS's own tree-cleanliness check,
scoped to what DCS added (the worktree/merge model), not a substitute for
project-specific gates.

## 4. List what's about to ship — reconcile against prod FIRST (v0.4.1)

**DCS is not the only thing that ships.** Other sessions, other people,
and CI can deploy the integration branch at any time, and any such deploy
carries every merged incident underneath it — so a `MERGED` row may
already be live without DCS ever having shipped it (field lesson
2026-07-23: an unrelated hotfix deploy transitively shipped a whole
incident; the register still claimed it pending).

Before listing anything, read the project's deployed-version marker
(step 7's mechanism — e.g. `.deployed_sha` over SSH) and, for **every**
`MERGED` row, check whether its merge commit is already an ancestor of
what's deployed:

```bash
git merge-base --is-ancestor <row merge commit> <deployed marker sha>
```

- **Ancestor (already live):** move the row to `DEPLOYED` with a note
  saying it shipped **out-of-band** (naming the deployed sha that carried
  it), delete its `dcs/*` branch, and EXCLUDE it from this train. Never
  re-ship what is already deployed, and never record it as if DCS shipped
  it — that is the facts-only rule applied to the register.
- **Not an ancestor:** it genuinely needs shipping; include it.
- **Marker unreadable** (no SSH, no documented marker): skip the
  reconciliation, say so plainly, and treat every `MERGED` row as
  unshipped — but flag that this train may re-ship already-live work.
- **Every row reconciles away:** report "nothing to ship — all merged
  rows already live (shipped out-of-band)", release the lock, and stop.

Then list the remaining `MERGED` rows — these are what this deploy will
ship. Separately warn about any `dcs/*` branch from
`git branch --list 'dcs/*' --no-merged main` that ISN'T backed by a
`MERGED` row (a dangling branch from the audit, step 2) — these will
**not** ship (they were never merged) and the warning exists so the Owner
isn't surprised their existence didn't affect the deploy scope.

## 5. Owner confirms — Delegation-aware (v0.4, Owner-requested)

**Deploy-delegation check first:** read the latest `delegation-bounds`
block from `<esg_root>/.dcs/esg/DELEGATION.md`. If it has a `deploy`
object with `auto: true`, evaluate EVERY row about to ship against its
bounds (schemas.md #7): territory vs `frontend_only` and the deploy
`forbidden_globs` (migration-bearing rows are never routine), row count
vs `max_rows_per_train`. **All rows in-bounds:** the go/no-go prompt is
covered by the Owner's standing, signed authorization — announce in one
visible line ("shipping N rows under Delegation v<X> deploy authority:
<ids>"), log `deployed under Delegation v<X>` against each register row,
and continue to step 6. Never silent (principle 12); the Owner sees
every delegated ship, they just don't have to click it.

**Any row out of bounds, no `deploy` block, or `auto: false`:** use
`AskUserQuestion` — present the exact list of `MERGED` rows about to
ship (id, title, merge commit sha), name the specific failed bound if a
delegation check was attempted, and ask for an explicit go/no-go. This
follows the same "explicit permission required" discipline as any other
irreversible action — a deploy ships real code to production. On "no":
release the lock (step 9) and stop; nothing changed. On "go": continue.

## 6. Run the project's documented deploy command

Discover it from the project's own `CLAUDE.md` — **never invented, never
guessed**. Most projects document one canonical deploy entry point (e.g.
a `deploy.sh`, a CI trigger, a platform CLI command); run exactly that,
with exactly the flags the project's own docs specify for a full deploy.
If the project's `CLAUDE.md` documents no deploy command at all: **stop**
here and tell the Owner — DCS orchestrates the train, it does not invent
a way to ship code a project has never described (doctrine: "Relationship
to project-specific protocols").

**If the harness refuses to run the deploy command** (a permission
prompt denied, a safety classifier blocking the call — a deploy script
that pushes to prod and restarts services is exactly the kind of action
a harness may gate independently of DCS): this is a **first-class path,
not a failure**, and it is emphatically **not** an invitation to get the
same effect another way. **Never** substitute an equivalent script, split
the command into pieces, wrap it in another shell, or run its steps by
hand — the block is a deliberate boundary, and routing around it would
be exactly the kind of silent judgment call this whole system exists to
prevent (field lesson 2026-07-23: a session hit this and correctly
refused; that refusal is the standard). Instead:

1. Print the **exact** command, in its own shell-tagged block, for the
   Owner to run in their own terminal.
2. Record in the register/notes that the train stopped here awaiting an
   Owner-run deploy — the rows stay `MERGED (deploy pending)`, and are
   NOT marked deployed on the strength of a command nobody ran.
3. Release the lock (step 9) so the tree isn't left locked while the
   Owner works, and tell them to re-run `/dcs-deploy` afterwards: step
   4's reconciliation will detect the now-shipped rows by ancestry and
   close them out correctly, including deleting their branches.

That turns a hard block into a loop the Owner closes, with DCS still
doing every part it is allowed to do.

## 7. Verify the deployed-version marker actually advanced

Facts-only rule (same discipline as `close.md`'s AAR facts-only rule,
field lesson 2026-07-22): **do not** report success because the deploy
command exited 0. Check the project's own deployed-version marker (e.g. a
`.deployed_sha` file, a `/version` endpoint, whatever the project
documents) **before and after** running the deploy command in step 6, and
confirm it actually advanced to (or past) the merge commit(s) from step
4. If it didn't advance, or advanced to something unexpected: **stop**,
report the discrepancy exactly as observed, and do **not** proceed to
step 8 — do not mark anything `DEPLOYED` on the strength of an exit code
alone.

## 8. Update rows and delete shipped branches

For every `MERGED` row confirmed shipped in step 7: move it to
`DEPLOYED` in `REGISTER.md`, then `git branch -D dcs/<slug>` — the branch
was kept exactly until this point as the rollback reference (`close.md`
step 5a.4); once the deployed-version marker confirms it shipped, it has
no further job to do.

**Intake-closure linkage:** `close.md` step 5's intake-source-closure
rule (flag for the Owner, or delegate to a project-documented routine
that closes items itself) keys off **`DEPLOYED`**, not `MERGED` — a
merged-but-undeployed fix hasn't actually reached production yet, so any
intake source (an `audit_results` row, a ticket) should not be reported
as resolved until this step confirms the deploy. If `close.md` already
flagged an intake source for the Owner at close time, this is the moment
that flag becomes actionable; note it in the final report (step 10).

## 9. Release DEPLOY-LOCK

Delete `<esg_root>/.dcs/esg/DEPLOY-LOCK`. Always run this step — even on
a step 3/5/7 stop-and-abort path above, release the lock before ending
the turn so a future `/dcs-deploy` isn't blocked by this run's own lock.

## 10. Report

Summarize: which rows shipped (id, title, merge commit, confirmed
deployed-version marker value), which `dcs/*` branches were deleted, any
worktree-audit findings from step 2 still needing an `/dcs-esg` decision,
and any intake sources now actionable per step 8's linkage note.

</process>
