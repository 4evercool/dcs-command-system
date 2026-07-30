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

- Every "written / deployed / verified / done" claim MUST cite an
  artifact checked at write time. Intentions stay in future tense
  ("pending", "to be done by X").
- **Deviation history comes from `214-LOG.md`, not from memory** — list
  every halt, deviation, and command correction the log records. "None"
  is only writable when the log shows none.
- **Owner-UAT status is a mandatory AAR field** when the IAP defines a
  UAT step: done (with what was checked) / pending (what gates what).
  Close may proceed with UAT pending only if the Owner explicitly says
  so — record that decision.
- **Deploy status is a mandatory AAR field** when the fix requires
  deploy: verify per `dcs/workflows/deploy.md` step 7; "not deployed —
  loop completes after deploy" is honest, a false "deployed" is not.
- Timestamps in `214-LOG.md` use the real clock, never copied from
  earlier entries.

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
`audit_results` row id, a ticket): **do not** write to it directly.

**First check who owns closure.** Read the project's `CLAUDE.md` and the
201: if a documented routine closes items itself upon observing the fix
(e.g. a daily validate-findings routine that stamps rows when the fixing
commit is deployed), then the correct action is **no action** — record in
AAR.md that closure is DELEGATED, name the routine, and note what it
needs to observe the fix. Manually closing what a routine owns creates a
race and duplicates its write. Delegate only when the documentation is
explicit — a vaguely-mentioned routine is NOT an owner; when in doubt,
use the flag-for-Owner fallback (a duplicate flag is annoying; a
silently-never-closed finding is a leak).

**Only if no owner is documented:** flag it for the Owner — print the
exact identifier and suggested action (e.g. "mark `audit_results` row
id=482 resolved via the admin UI") and ask them to confirm. Record the
flag (not a completed action) in AAR.md.

If the intake source is "ad hoc" / has no external reference, note that
and move on.

## 5a. Merge to main and remove the worktree (v0.3 — the anti-rot core)

**An incident is NOT closed until every one of these five steps
succeeds** — merging is a close step, not a chore anyone can forget.
Skip this section only for an incident that never got a worktree (Type 5
has none; a pre-v0.3 incident still in the main checkout) — go straight
to step 6.

1. **Commit in the worktree.** The AAR (step 3) and any memory-routing
   writes (step 4) that belong to the repo must be committed on the
   incident's branch before merging — `git add` the specific files
   (never `-A`/`.`, same discipline as `execute.md` step 9b), commit
   message referencing the incident slug. **All writes target the
   WORKTREE's copies of the files** — the worktree is the incident's
   whole world until the merge (v0.3.3: a session routed vault lessons
   into the main checkout by reflex and had to revert).
1a. **Run the project's merge-time guards, if it documents any (v0.5.3).**
   Some defect classes are **structurally invisible before the merge**:
   each branch may pass in isolation while the merged tree is silently
   broken — `git merge-tree` can report zero conflicts on a merge that
   would, e.g., land two branches with the same DB migration number under
   one registry key, silently dropping one (field lesson 2026-07-24).

   If the project's `CLAUDE.md` names a **merge-time guard** — a test or
   script that inspects the *merge result* rather than either branch —
   run it now (before step 2's merge) and include its real output in the
   close record. A red guard is **escalation trigger (a)**: stop, file a
   209, and put it to the Owner. Never merge past a red guard or resolve
   what it found silently.

   If the project documents no such guard, skip and say so — DCS does
   not invent guards a project has never described. **Prefer git-native
   allocation:** an append-only registry where each claim is its own line
   makes two branches claiming the same identifier produce a *real merge
   conflict* — the check that cannot be skipped is the one git performs
   itself.

2. **Merge into the integration branch.** The merge target is **whatever
   branch the primary checkout (`esg_root`) currently has checked out** —
   its name is irrelevant (v0.3.3: a session once recommended checking
   out `main`, which would have swapped the integration point out from
   under other sessions). Three hard rules: **never switch the primary
   checkout's branch** — changing the integration branch is the Owner's
   manual act; **unrelated dirty or untracked files do not block the
   merge** — git only objects on real overlap, so check
   (`git diff --name-only <base>..dcs/<slug>` vs `git status --short`)
   and only escalate on actual file-overlap; **do not ask which branch
   to merge into** — the answer is always the current one. From the
   primary checkout: `git merge --no-ff dcs/<slug>`. The territory
   partition (doctrine principle 6) makes this merge trivially clean in
   the normal case. **A conflict means the territory promise was
   violated somewhere** — treat it as escalation trigger (a) (doctrine
   principle 13): stop here, file a 209 sitrep, and put it to the
   Owner. **Never resolve a merge conflict silently or unilaterally.**
3. **Register row → `MERGED` (deploy pending).** If
   `<esg_root>/.dcs/esg/REGISTER.md` exists: move this incident's row
   from `ACTIVE` to `MERGED`, filling in the closed date, and collapse
   Territory, Outcome, and Intake source to ONE LINE each per
   `REGISTER.md`'s two-state rule — pointers at `IAP.md`'s partition
   table, `AAR.md`'s Outcome section, and the original intake citation.
   This is the row's collapse point; it supersedes the pre-v0.3
   `ACTIVE → CLOSED` transition (see step 6a). If never registered,
   skip silently.
4. **Remove the worktree.** If `pwd` shows you are inside the worktree
   path: `cd` to `<esg_root>` first — `git worktree remove` of the
   directory you stand in fails with a cryptic error indistinguishable
   from a real lock holder (cwd self-conflict). Then `git worktree
   remove <path>`. The branch (`dcs/<slug>`) is **kept** as the rollback
   reference until `/dcs-deploy` deletes it. **If removal still fails**
   (locked files, a session still running inside): diagnose the lock
   holder — POSIX: `lsof +D <path>` or `fuser -v <path>`; Windows:
   `powershell "Get-Process | Where-Object { $_.Path -like '*<path>*'
   }"` (or Sysinternals `handle <path>` if installed) — then write
   `.dcs/CLOSED` into the worktree (mere presence is the signal), tell
   the Owner manual removal is needed, and include the diagnostic output
   in 214-LOG.md. `dcs_gate.py`'s zombie rule denies every guarded edit
   on that worktree in the meantime, so it can't quietly become a second
   life for already-merged work.
5. Only now does the incident's story name the worktree's fate — carry
   the merge commit sha and the deploy-pending state into the final
   sitrep (step 7).

## 6. Release the gate

Append a final entry to `214-LOG.md`: `incident closed, archived`.

**(v0.3)** In the normal worktree case, this is already accomplished by
5a step 4 — `.dcs/ACTIVE` lived inside the removed worktree, so there is
nothing further to delete. Only explicitly delete
`<project>/.dcs/ACTIVE` here for a pre-v0.3 incident still running in
the main checkout (Type 5 never set `ACTIVE` to begin with). The incident
directory itself is **not** moved or deleted — for a merged worktree
incident it now lives under `.dcs/incidents/<date>-<slug>/` in the main
checkout (having ridden the merge in); "archived" means "closed in
place," not "relocated."

## 6a. Update the register (v0.2, superseded by 5a in v0.3)

**v0.3: this transition now happens at step 5a.3** (`ACTIVE` → `MERGED`,
not `ACTIVE` → `CLOSED`). This heading is kept as a stable cross-reference
target; there is nothing further to do here for a v0.3 incident. For a
pre-v0.3 / never-worktreed incident (step 5a skipped): find this
incident's row (by slug) and move it `ACTIVE` → `RESOLVED` directly,
filling in the closed date and outcome — correct for an incident that has
no merge step to wait on.

If `<esg_root>/.dcs/esg/STRATEGY.md` exists, read its ranked priorities
and note the next queued priority in the final sitrep (step 7).

## 7. Final sitrep

One paragraph to the Owner: slug, type, period count, key changes, final
Safety verdict, memory-routing destination (or that none was documented),
intake-source flag if any, gate-released confirmation. **(v0.3)** For a
worktree incident: name the merge commit sha (step 5a.2), state the
register row is `MERGED (deploy pending)` — not shipped — and that
`/dcs-deploy` is next; if worktree removal failed and `.dcs/CLOSED` was
written, say so and name the manual cleanup owed. If `STRATEGY.md` exists,
cite the next queued priority so the Owner sees what's next without a
separate round.

</process>
