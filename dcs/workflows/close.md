<purpose>
Close out an incident: require a green Safety verdict, write the AAR,
route lessons to the project's own memory system (if it documents one),
flag the intake source for closure without touching prod, release the
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

Using `$HOME/.claude/dcs/templates/AAR.md`: outcome (final goal state vs.
the last period's acceptance criteria), what worked (tactics that survived
Safety Officer review without refutation), lessons (concrete, reusable —
not vague), deviation history (or "none"), and the Safety Officer's final
verdict copied verbatim from `SAFETY.md`.

**Facts-only rule (field lesson, 2026-07-22 — the first live AAR claimed
a deploy that hadn't happened and lessons that were never written):**

- Every "written / deployed / verified / done" claim MUST cite an artifact
  the IC checked at write time (a diff shown, a file read back, a deployed
  version marker compared). An intention is written as an intention
  ("pending", "to be done by X"), never in the past tense.
- **Deviation history comes from `214-LOG.md`, not from memory** — list
  every halt, deviation, and command correction the log records. "None"
  is only writable when the log shows none.
- **Owner-UAT status is a mandatory AAR field** when the IAP defines a UAT
  step: done (with what was checked) / pending (and what still gates
  what). Close may proceed with UAT pending only if the Owner explicitly
  says so — record that decision.
- **Deploy status is a mandatory AAR field** when the fix requires deploy
  to take effect: verify the project's deployed-version marker (e.g. a
  `.deployed_sha`) rather than assuming; "not deployed — loop completes
  after deploy" is an honest and acceptable state, a false "deployed" is
  not.
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

## 6. Release the gate

Append a final entry to `214-LOG.md`: `incident closed, archived`.

Delete `<project>/.dcs/ACTIVE`. The incident directory itself is **not**
moved or deleted — it remains under `.dcs/incidents/<date>-<slug>/`
permanently as the archived record; "archived" means "closed in place",
not "relocated".

## 6a. Update the register (v0.2)

If `<project>/.dcs/esg/REGISTER.md` exists: find this incident's row (by
slug) and move it `ACTIVE` → `CLOSED`, filling in the closed date and a
one-line outcome (from `AAR.md`'s Outcome section). If the incident was
never registered (no ESG in use on this project, or it was opened before
the founding `/dcs-esg` session), skip silently — `REGISTER.md` is
optional infrastructure, not a close-blocking requirement.

If `<project>/.dcs/esg/STRATEGY.md` exists, read its ranked priorities and
note the next queued priority in the final sitrep (step 7) so the Owner
sees what's next without a separate `/dcs-esg` round.

## 7. Final sitrep

One paragraph to the Owner: incident slug and type, number of operational
periods, key changes made, Safety Officer's final pass verdict, whether
lessons were routed to memory (and where, or that none was documented),
whether an intake source was flagged for the Owner's own action,
confirmation the gate is released (`.dcs/ACTIVE` removed — the project is
free to open a new incident with `/dcs-new`), and (v0.2) whether the
register was updated plus the next queued `STRATEGY.md` priority, if any.

</process>
