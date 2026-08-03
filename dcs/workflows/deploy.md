<purpose>
The deploy train (v0.3): a serialized, Owner-gated ship of every incident
merged to main but not yet shipped. Runs only from the clean main
checkout, verifies the deployed payload matches what was merged, and is
the only place `REGISTER.md` rows reach `DEPLOYED`.
Never called by `/dcs-loop` (doctrine's automation-layer hard rule 2).
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

"Clean" means: **no dirty tracked files among the paths the deploy
command actually ships** — discover the payload from the project's
`CLAUDE.md` / deploy script (e.g. a deploy that ships `src/` doesn't
care about `.claude/` hook churn). Field lesson 2026-07-22, v0.3.4: a whole-tree
check stopped a deploy over `.claude/` files the deploy would never
ship, asking a question the payload scoping already answers.

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

If the project documents its own pre-deploy checks, this step does not
replace them — the project's deploy command (step 6) still runs its own
preflight; this step is DCS's tree-cleanliness check, scoped to what
DCS added (the worktree/merge model), not a substitute for project
gates.

## 4. List what's about to ship — reconcile against prod FIRST (v0.4.1)

**DCS is not the only thing that ships.** Other sessions, people, and CI
can deploy the integration branch any time, carrying every merged
incident underneath it — so a `MERGED` row may already be live without
DCS ever having shipped it (field lesson 2026-07-23, v0.4.1: an unrelated hotfix
deploy transitively shipped a whole incident; the register still claimed
it pending).

Before listing anything, reconcile every `MERGED` row against the
project's deployed-state check, using the same shapes step 7 classifies
a marker into — see step 7 for what each shape IS; this step runs
**before** step 6 and differs in what it DOES with the result:

- **Commit-ish marker:** ancestor of the marker sha → already live,
  reconciles away below; not an ancestor → include it.
- **Content witness:** run it once against this checkout, the
  integration-branch tip C (`esg_root`). Identical or installed-only
  only reconciles every row whose merge commit is an ancestor of C,
  same as an ancestor commit-ish marker (a payload-inert merge —
  `vault/`, `.dcs/`, docs only — counts as already shipped). Differing
  or repo-only attests to **bytes**, not to which merge introduced them,
  so the difference **cannot be attributed to individual rows**: treat
  **every** `MERGED` row as unshipped, include them all, and name the
  differing/missing files. A witness environment error folds into
  "unreadable" below.
- **Readable-but-neither, or unreadable:** skip reconciliation, say so
  plainly, and treat every `MERGED` row as unshipped — flag that this
  train may re-ship already-live work. (Step 7 gives these same two
  shapes different post-deploy dispositions.)
- **Every row reconciles away:** report "nothing to ship — all merged
  rows already live (shipped out-of-band)", release the lock, and stop.

Rows that reconcile away move to `DEPLOYED` per step 7's disposition,
noting they shipped **out-of-band** (naming the sha or witness result
that carried them), delete their `dcs/*` branch, and are EXCLUDED from
this train — never re-ship what's already deployed.

Then list the remaining `MERGED` rows — what this deploy will ship.
Separately warn about any `dcs/*` branch from the audit (step 2) that
ISN'T backed by a `MERGED` row — these **will not** ship (they were
never merged) and the warning exists so the Owner isn't surprised.

## 5. Owner confirms — Delegation-aware (v0.4, Owner-requested)

**Deploy-delegation check first:** read the latest `delegation-bounds` block from `<esg_root>/.dcs/esg/DELEGATION.md`. If it has a `deploy` object with `auto: true` AND the session's current operating model appears in that block's `approved_models` (model floor — `approved_models` empty or absent means no model is approved), evaluate EVERY row about to ship against its bounds (schemas.md #7, delegation bounds): territory vs `frontend_only` and the deploy `forbidden_globs` (migration-bearing rows are never routine), row count vs `max_rows_per_train`. **All rows in-bounds:** the go/no-go prompt is covered by the Owner's standing authorization — announce in one visible line ("shipping N rows under Delegation v<X> deploy authority: <ids>"), log it against each register row, and continue to step 6. Never silent (principle 12); the Owner sees every delegated ship.

**Any row out of bounds, no `deploy` block, `auto: false`, or the model floor fails (unlisted model, or `approved_models` empty or absent — no model approved):** use `AskUserQuestion` — full v0.1 behavior — present the `MERGED` rows about to ship (id, title, merge commit sha), name the failed bound if any (the model floor counts as one), and ask for a go/no-go. On "no": release the lock (step 9) and stop. On "go": continue.

## 6. Run the project's documented deploy command

Discover it from the project's own `CLAUDE.md` — **never invented, never
guessed**. Run exactly that command with exactly the flags the project's
docs specify. If `CLAUDE.md` documents no deploy command at all: **stop**
and tell the Owner — DCS orchestrates the train, it does not invent a
way to ship (doctrine: "Relationship to project-specific protocols").

**If the harness refuses to run the deploy command** (a permission
prompt denied, a safety classifier blocking the call — a deploy script
that pushes to prod and restarts services is exactly the kind of action
a harness may gate independently of DCS): this is a **first-class path,
not a failure** — the block is a deliberate boundary, not an obstacle
to route around. **Never** substitute, split, or wrap the command
(field lesson 2026-07-23 (predates self-hosting): a session hit this and correctly refused).
Instead:

1. Print the **exact** command in its own shell-tagged block for the
   Owner to run in their own terminal.
2. Record that the train stopped here — rows stay `MERGED (deploy
   pending)`, NOT marked deployed on the strength of an unrun command.
3. Release the lock (step 9) and tell the Owner to re-run
   `/dcs-deploy`: step 4's reconciliation will detect the now-shipped
   rows by ancestry and close them out, including deleting their
   branches.

That turns a hard block into a loop the Owner closes.

## 7. Verify the deployed content actually matches what was merged

**This step is the single source of every disposition in this
workflow** (`DEPLOYED` / stop / stays `MERGED (deploy pending)`, by
shape) — nothing else in the package states one; every other declaring
statement cites this step by name.

Facts-only rule (same discipline as `close.md`'s AAR rule, field lesson 2026-07-22 (predates self-hosting)): **do not** report success because the deploy command
exited 0. Read what the project documents for checking deployed state
(the same discovery step 4 used from `CLAUDE.md`), and verify **after**
step 6, by the same shape step 4 already sorted it into:

- **Commit-ish marker** (e.g. a sha in `.deployed_sha`): read the
  marker's sha after step 6 and run `git merge-base --is-ancestor <row
  merge commit> <deployed marker sha>` for every row about to ship. All
  ancestors → `DEPLOYED`. Any row not an ancestor → **stop**; name the
  row(s) the marker doesn't yet reflect, and do not proceed to step 8.
- **Content witness** (discovered from `CLAUDE.md`, same discipline as
  step 6): run it **before** step 6 to capture the deployed starting
  state — **a red before run is expected input, never a stop: it's
  the reason this deploy is happening.** Run it again **after** step
  6, recording the integration-branch sha each time. **Why the
  checkout stands in for "what was merged":** the witness compares
  deployed against this checkout — step 3 confirmed its payload paths
  are clean, and the sha pins exactly which commit that clean checkout
  equals. **That holds only if nothing wrote into payload paths between
  step 3 and this after run** — re-confirm step 3's cleanliness before
  trusting what follows. The **after** run decides:
  - **Identical** → `DEPLOYED`. A marker (version string or otherwise)
    that didn't move is explicitly **not** a stop condition —
    before-green/after-green is a legitimate no-op ship, not a
    discrepancy.
  - **Differing or repo-only** → **stop**. Name the files from the
    witness's own report and do **not** proceed to step 8 — never mark
    anything `DEPLOYED` on the strength of step 6's exit code alone.
  - **Installed-only only** → `DEPLOYED`, **with a mandatory flag
    naming the stale files** (step 10) so the Owner can delete them —
    the merged payload is fully live, the extras are pre-existing
    installer debris. **IC ruling, binding:** stop is reserved for
    differing/repo-only above.
- **Readable, but neither a commit-ish nor a content witness** (e.g. a
  bare version string): give it **step 6's harness-refusal shape** —
  rows stay `MERGED (deploy pending)`, Owner told to document a
  deploy-evidence witness in `CLAUDE.md` and re-run `/dcs-deploy`.
  **Never an override, never a substituted check.**
- **Marker unreadable** (no SSH, no documented marker, or content
  witness environment error): report and **stop** — deliberately stricter
  than step 4's "cannot check": before deploy, treating rows as unshipped
  is safe; after deploy, recording unproven `DEPLOYED` is not.

## 8. Update rows and delete shipped branches

For every `MERGED` row confirmed shipped in step 7: move it to
`DEPLOYED` in `REGISTER.md`. Territory, Outcome, and Intake source stay
collapsed to the ONE LINE each `close.md` step 5a.3 already wrote per
`REGISTER.md`'s two-state rule — this step never restates them. If any
of the three somehow reached `MERGED` uncollapsed (a row older than this
rule), collapse it now instead: Territory to a pointer at `IAP.md`'s
partition table, Outcome to a pointer at `AAR.md`'s Outcome section,
Intake source to a pointer at the original intake citation. Then
`git branch -D dcs/<slug>` — the branch was kept exactly until this
point as the rollback reference (`close.md` step 5a.4); once step 7
confirms it shipped, it has no further job to do.

**Intake-closure linkage:** `close.md` step 5's intake-source-closure
rule keys off **`DEPLOYED`**, not `MERGED` — a merged-but-undeployed
fix hasn't reached production, so intake sources stay unresolved until
this step confirms the deploy. If `close.md` already flagged an intake
source at close time, this is when that flag becomes actionable; note
it in the final report (step 10).

## 9. Release DEPLOY-LOCK

Delete `<esg_root>/.dcs/esg/DEPLOY-LOCK` — even on a stop-and-abort
path, release the lock so a future `/dcs-deploy` isn't blocked.

## 10. Report

Summarize: which rows shipped (id, title, merge commit, step 7's
verification evidence and any stale-extras flag), which `dcs/*` branches
deleted, any worktree-audit findings from step 2, and any intake sources
now actionable per step 8's linkage note.

</process>
