<purpose>
Close out an incident: require a green Safety verdict, write the AAR,
route lessons to the project's own memory system (if it documents one),
flag the intake source for closure without touching prod, merge the
incident's worktree into main and remove it (v0.3 — the anti-rot core
that keeps worktrees from being the human's job to remember), release the
gate, and deliver a final sitrep.
</purpose>

<required_reading>
@$HOME/.claude/dcs/references/doctrine.md
@$HOME/.claude/dcs/references/forms.md
</required_reading>

<process>

## 1. Verify the incident is closeable

```bash
cat "<project>/.dcs/ACTIVE"
cat "<incident_dir>/SAFETY.md" 2>/dev/null
```

If no `ACTIVE`: nothing to close. If `SAFETY.md`'s latest recorded verdict
for the current period is not `pass`: **stop.** Tell the Owner
`/dcs-execute` must complete with a `pass` verdict first — doctrine
principle 7/10: no incident closes over an unresolved refutation. There is
no override for this from within `/dcs-close`.

**Integration-commit check (mechanical, not Safety's job):** the
integration commit from `execute.md` step 9b must exist — find it via
`214-LOG.md`'s `integration commit <sha>` entry (or `git log` if the entry
is missing, and note the logging gap). Verify with `git show --stat <sha>`
that it touches ONLY territory files and its message references the intake
source ids. If there is no commit, or it sweeps in unrelated files:
**stop** — route back to the IC to commit properly (or split the commit)
before closing. If the Owner-UAT section of the IAP's verification plan is
unfinished, remind the Owner it gates close too.

## 2. Gather the incident's history

Read `201-BRIEF.md`, all `202-OBJECTIVES.md` versions referenced across
periods (or the final one plus `214-LOG.md`'s summary of earlier ones),
`214-LOG.md` in full, and `SAFETY.md`. Count operational periods from the
phase-transition entries in `214-LOG.md`.

## 3. Write AAR.md

**(v0.3)** If this incident lives in a worktree (the standard case for
Type 3/1 since v0.3), this write — and step 4's memory-routing writes —
happen **in the worktree**, on the incident's branch. They get committed
there (step 5a below) and ride the merge into main; there is no separate
"copy the AAR into main" step.

Using `$HOME/.claude/dcs/templates/AAR.md`: outcome (final goal state vs.
the last period's acceptance criteria), what worked (tactics that survived
Safety Officer review without refutation), lessons (concrete, reusable —
not vague), deviation history (or "none"), and the Safety Officer's final
verdict copied verbatim from `SAFETY.md`.

**Facts-only rule (field lesson, 2026-07-22 — the first live AAR claimed
a deploy that hadn't happened and lessons that were never written):**

- Every "written / deployed / verified / done" claim MUST cite an artifact
  the IC checked at write time (a diff shown, a file read back, a witness
  result checked per `dcs/workflows/deploy.md` step 7, the deploy-evidence
  discipline). An intention is written as an intention ("pending", "to be
  done by X"), never in the past tense.
- **Deviation history comes from `214-LOG.md`, not from memory** — list
  every halt, deviation, and command correction the log records. "None"
  is only writable when the log shows none.
- **Owner-UAT status is a mandatory AAR field** when the IAP defines a UAT
  step: done (with what was checked) / pending (and what still gates
  what). Close may proceed with UAT pending only if the Owner explicitly
  says so — record that decision.
- **Deploy status is a mandatory AAR field** when the fix requires deploy
  to take effect: verify per `dcs/workflows/deploy.md` step 7's deploy
  evidence rather than assuming; "not deployed — loop completes after
  deploy" is an honest and acceptable state, a false "deployed" is not.
- Timestamps in `214-LOG.md` entries use the real clock (check the actual
  time), never copied from earlier entries.

## 4. Route lessons to the project's memory system

Read the project's `CLAUDE.md` for a documented memory/knowledge-base
protocol (e.g. a vault with domain-specific pattern/pitfall files plus a
lessons file, or any other system it names explicitly).

**If one is documented:** follow it as written — use whatever
read-before-write-after protocol, helper script, or validation step it
specifies (e.g. a `validate()` call after any write). Write the lesson(s)
from this incident in the format and location that protocol calls for.
Record exactly what was written (file + one-line description) in AAR.md's
"Memory routing" section.

**If none is documented:** skip this step gracefully. Say so plainly in
AAR.md — "no project memory system documented in CLAUDE.md — skipped" is
a complete, honest answer, not a gap to apologize for or a place to invent
a new file.

## 5. Close the intake source — flag, don't touch

If `201-BRIEF.md`'s "Intake source" names something external (e.g. an
`audit_results` row id, a ticket): **do not** write to it directly,
especially if it lives in a production database.

**First check who owns closure.** Read the project's `CLAUDE.md` (and the
201 itself): if a documented routine or pipeline curates the intake source
and closes items itself upon observing the fix (e.g. a daily
validate-findings routine that stamps rows when the fixing commit is
deployed), then the correct action is **no action** — record in AAR.md
that closure is DELEGATED to that routine, name it, and note what it needs
to observe the fix (commit pushed, deploy done). Manually closing what a
routine owns creates a race and duplicates its write. (Field lesson,
2026-07-22.) Delegate only when the documentation is explicit that the
routine closes items itself — a vaguely-mentioned routine of unclear
ownership is NOT an owner; when in doubt, use the flag-for-Owner fallback
below (a duplicate flag is annoying; a silently-never-closed finding is a
leak).

**Only if no owner is documented:** flag it for the Owner — print the
exact identifier and the suggested action (e.g. "mark `audit_results` row
id=482 resolved via the admin UI") and ask them to confirm or perform it.
This mirrors any project's own rule against ad hoc production writes from
an automated routine (e.g. "never INSERT/UPDATE/DELETE — read-only only"
for an append-only audit table). Record the flag (not a completed action)
in AAR.md.

If the intake source is "ad hoc" / has no external reference, note that
and move on.

## 5a. Merge to main and remove the worktree (v0.3 — the anti-rot core)

**An incident is NOT closed until every one of these five steps
succeeds.** This is the mechanism that kills the standing Owner pain of
forgotten worktrees — merging is a close step, not a chore anyone can
forget, and closing without it is impossible from within this workflow.
Skip this section entirely only for an incident that never got a
worktree (Type 5 has none; a pre-v0.3 incident still running directly in
the main checkout) — go straight to step 6.

1. **Commit in the worktree.** The AAR (step 3) and any memory-routing
   writes (step 4) that belong to the repo (not to an external system)
   must be committed on the incident's branch before merging — `git add`
   the specific files (never `-A`/`.`, same discipline as `execute.md`
   step 9b), commit message referencing the incident slug. **All these
   writes target the WORKTREE's copies of the files** (v0.3.3 — a session
   in the field routed vault lessons into the main checkout's copies by
   reflex and had to revert; the worktree is the incident's whole world
   until the merge).
1a. **Run the project's merge-time guards, if it documents any (v0.5.3).**
   Some defect classes are **structurally invisible before the merge**: a
   check that passes on each branch in isolation says nothing about the
   merged tree, and `git merge-tree` can report **zero conflicts** while
   producing a file that is silently broken (field lesson 2026-07-24: two
   branches independently allocated the same DB migration number; the
   merge was conflict-free and would have landed two functions with one
   registry key, so one migration would never have run — against a
   schema-versioned production database).

   If the project's `CLAUDE.md` (or its own docs) names a **merge-time
   guard** — a test or script whose job is to inspect the *merge result*
   rather than either branch — run it now, before step 2's merge, and
   include its real output in the close record. A guard that reports a
   defect is **escalation trigger (a)**: stop, file a 209, and put it to
   the Owner. Never merge past a red merge-time guard, and never resolve
   what it found silently — that is precisely the silent judgment call
   the trigger machinery exists to catch.

   If the project documents no such guard, skip this step and say so —
   DCS does not invent guards a project has never described (doctrine:
   "Relationship to project-specific protocols"). **Prefer git-native
   allocation over checkers where a project can arrange it:** an
   append-only registry file where each claim is its own line makes two
   branches claiming the same identifier produce a *real merge conflict*
   with no tooling to remember — the check that cannot be skipped is the
   one git performs itself.

2. **Merge into the integration branch.** The merge target is **whatever
   branch the primary checkout (`esg_root`) currently has checked out** —
   its name is irrelevant, and it is frequently NOT `main` (v0.3.3, field
   lesson: a project's primary checkout lived on a long-running work
   branch; the session recommended checking out `main` first, which would
   have swapped the branch under the tree that other sessions and the
   deploy pipeline treat as the integration point). Three hard rules:
   **never switch the primary checkout's branch** — if the project wants
   a different integration branch, that is the Owner's manual act, not
   the close's; **unrelated dirty or untracked files in the primary
   checkout do not block the merge** — git only objects when the merge
   itself would overwrite them, so check overlap
   (`git diff --name-only <base>..dcs/<slug>` vs `git status --short`),
   don't ask; **do not ask the Owner which branch to merge into** — the
   answer is always the current one, and only an actual file-overlap or
   conflict escalates. From the primary checkout: `git merge --no-ff
   dcs/<slug>`. The territory partition (doctrine principle 6, portfolio
   level) makes this merge trivially clean in the normal case. **A
   conflict means the territory promise was violated somewhere** — treat
   it as escalation trigger (a) (doctrine principle 13): stop here, file
   a 209 sitrep, and put it to the Owner. **Never resolve a merge
   conflict silently or unilaterally** — that is exactly the kind of
   silent judgment call the escalation-trigger machinery exists to catch.
3. **Register row → `MERGED` (deploy pending).** Resolve `esg_root`
   (doctrine "Parallel operation"). If `<esg_root>/.dcs/esg/REGISTER.md`
   exists: move this incident's row from `ACTIVE` to `MERGED`, filling in
   the closed date, and collapse Territory, Outcome, and Intake source to
   ONE LINE each per `REGISTER.md`'s own two-state rule — Territory to a
   pointer at `IAP.md`'s partition table, Outcome to a pointer at
   `AAR.md`'s Outcome section, Intake source to a pointer at the original
   intake citation. This is the row's collapse point, not a separate
   archival pass; it supersedes the pre-v0.3 `ACTIVE → CLOSED` transition;
   see step 6a below. If never registered, skip silently.
4. **Remove the worktree.** `git worktree remove <path>`. The branch
   (`dcs/<slug>`) is **kept** — it stays the rollback reference until
   `/dcs-deploy` confirms the merge shipped and deletes it. **If removal
   fails** (locked files, a session still running inside it): write
   `.dcs/CLOSED` into the worktree (no content required — its mere
   presence is the signal) and tell the Owner it needs manual removal
   once whatever's holding it releases. `dcs_gate.py`'s zombie rule makes
   that worktree deny every guarded edit in the meantime, so it can't
   quietly become a second life for already-merged work.
5. Only now does the incident's story name the worktree's fate — carry
   the merge commit sha and the deploy-pending state into the final
   sitrep (step 7).

## 6. Release the gate

Append a final entry to `214-LOG.md`: `incident closed, archived`.

**(v0.3)** In the normal worktree case, this is already accomplished by
5a step 4 — `.dcs/ACTIVE` lived inside the worktree that was just
removed, so there is nothing further to delete. Only explicitly delete
`<project>/.dcs/ACTIVE` here for an incident that never had a worktree
(Type 5 has none to begin with — it never set `ACTIVE`; a pre-v0.3
incident still running in the main checkout does). The incident directory
itself is **not** moved or deleted — for a merged worktree incident it
now lives under `.dcs/incidents/<date>-<slug>/` in the **main checkout**
(having ridden the merge in); "archived" means "closed in place," not
"relocated."

## 6a. Update the register (v0.2, superseded by 5a in v0.3)

**v0.3: this transition now happens at step 5a.3** (`ACTIVE` → `MERGED`,
not `ACTIVE` → `CLOSED` — for a shipped incident, the register's terminal
state is `DEPLOYED`, reached later via `/dcs-deploy`; that scoping still
holds beside the newer `RESOLVED` state, which belongs to work that never
enters the deploy lifecycle at all). This heading is kept as a stable
cross-reference target; there is nothing further to do here for a v0.3
incident. For a pre-v0.3 / never-worktreed incident (step 5a skipped):
find this incident's row (by slug) and move it `ACTIVE` → `RESOLVED`
directly, filling in the closed date and outcome — the old v0.2
behavior's target renamed to match the current register enum (`CLOSED`
was never a state in it), still correct for an incident that has no
merge step to wait on.

If `<esg_root>/.dcs/esg/STRATEGY.md` exists, read its ranked priorities
and note the next queued priority in the final sitrep (step 7) so the
Owner sees what's next without a separate `/dcs-esg` round.

## 7. Final sitrep

One paragraph to the Owner: incident slug and type, number of operational
periods, key changes made, Safety Officer's final pass verdict, whether
lessons were routed to memory (and where, or that none was documented),
whether an intake source was flagged for the Owner's own action,
confirmation the gate is released, and (v0.2) whether the register was
updated plus the next queued `STRATEGY.md` priority, if any. **(v0.3)**
For a worktree incident: name the merge commit sha (from step 5a.2), state
plainly the register row is `MERGED (deploy pending)` — not shipped yet
— and that `/dcs-deploy` is the next step whenever the Owner batches a
deploy; if worktree removal failed and `.dcs/CLOSED` was written instead,
say so explicitly and name the manual cleanup still owed.

</process>
