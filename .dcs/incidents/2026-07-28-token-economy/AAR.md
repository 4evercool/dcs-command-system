<!--
AAR.md -- After Action Report, written by the IC during /dcs-close.
Requires a green (pass) Safety Officer verdict to exist before this file
is written -- close.md enforces this, do not write an AAR to paper over
a halt.
-->

# AAR — After Action Report

**Incident:** 2026-07-28-token-economy
**Type:** 1
**Opened:** 2026-07-28
**Closed:** 2026-07-28
**Operational periods:** 1

## Outcome

Five of the six independently-caused token-waste mechanisms 201-BRIEF.md
identified are fixed and Safety-passed (verdict: pass, 0 refutations,
verified: `.dcs/incidents/2026-07-28-token-economy/SAFETY.md`). The
sixth (criterion 5, `doctrine.md`'s per-phase reread frequency) was
formally dropped this period via its own pre-authorized escape hatch —
no tool available can safely distinguish "same session, continuing" from
"fresh spawn, possibly post-reset," and forcing a fix would have traded
principle 5's context-reset resilience guarantee for a token saving. The
Owner was told this explicitly at IAP approval and accepted the drop as
part of that approval, not silently.

Delivered, integration commit `807edb8` (15 files, `git show --stat
807edb8` confirms exactly this set):

1. `dcs/workflows/run.md`/`loop.md` no longer eagerly `@`-include all
   four phase workflows; each phase's material loads only where the
   process body reads it on entry (S1).
2. Five previously-unbounded `214-LOG.md` read sites (`plan.md:38`,
   `plan.md:573`, `execute.md:25`, `agents/dcs-commander.md:63`,
   `agents/dcs-safety-officer.md`, which had none before) are now bounded
   checks (S1/S2/S3).
3. `dcs/templates/REGISTER.md`/`STRATEGY.md` gained a pointer-not-copy
   mechanism: `Territory` stays bare globs while a row is `ACTIVE`
   (`new.md` step 7b's O(1) scan needs it), collapsing to a one-line
   pointer for `Territory`/`Outcome`/`Intake source` once terminal;
   `STRATEGY.md`'s Sessions log capped at 5 lines, in project-agnostic
   shipped language (S4). Applying this mechanism to this project's own
   live register happened during this same close (see below) — not part
   of the integration commit, per this incident's own criterion text.
4. A repeat Safety Officer spawn within one period may cite a prior,
   independently-reconfirmed finding by reference instead of restating
   it — wired end to end across `execute.md`'s spawn inputs and the
   officer's own charter (S2/S3), verified by a dry run against a past
   incident's `SAFETY.md`.
5. `dcs/references/schemas.md`'s evidence-bearing fields and three agent
   charters gained an explicit brevity rule, matching the existing
   `summary`/`rationale` convention (S2).

## What worked

- **The chiefs' independent verification of the Dispatcher's own draft.**
  The Planning Chief caught three real defects in the 202 objectives
  before any tasking was cut: an enumerator that missed 3 of its own
  population, a stated cap that was never actually stated, and a
  shipped-package rule violation (`vault/Decisions/` named literally in
  text meant to ship). All three were confirmed independently rather
  than taken on the chief's word, and all three held up.
- **Independent re-derivation at every command point, not trust.**
  `dcs-commander` re-verified the chiefs' partition claim itself at
  command point 2, and re-verified the Safety Officer's verdict itself
  at command point 4 — catching a real factual error in `SAFETY.md`'s
  own `checked[]` list in the process (see Lessons).
- **Parallel execution with a genuinely disjoint partition.** Four
  specialists, zero deviations, zero territory violations, verified by
  file-list inspection at three separate points (Dispatcher, Safety
  Officer, commander) with the same result each time.
- **The Safety Officer's adversarial posture, exercised for real.** Six
  named attack attempts against the work, not a checklist walk-through;
  all six failed to find a refutation, and the officer said so plainly
  rather than manufacturing one to seem thorough.

## Lessons

- **A criterion's own verification command can be wrong, and the fix is
  to run it, not to trust it.** The Dispatcher's original 202 draft
  stated an enumerator for criterion 2 that missed 3 real sites (a
  line-wrap in the regex, and one file never checked at all) and a
  criterion-3 expectation ("`grep -rni vault` returns nothing") that
  was never actually measured before being written down — both caught
  by independent re-derivation, not by review. See
  [[Backlog#21|vault/Backlog.md item 21]] for the doctrine-appendix
  analogue.
- **The verifier's own written record is not exempt from the rule it
  just wrote.** This period built criterion 4's by-reference citation
  mechanism, and in the same period, `SAFETY.md`'s own `checked[]` list
  contained a false claim ("plan.md absent from git status" — it was
  not). Caught by `dcs-commander` applying the same "verify, don't
  accept" discipline one level up. Full account:
  [[Meta/building-dcs-lessons]] §21. **The false clause must never be
  cited by reference in a future verdict** — flagged here so it is not
  rediscovered the hard way.
- **A tool-surface limitation is a legitimate reason to drop a criterion
  formally, not a failure to route around.** Criterion 5 could not be
  satisfied safely with the tools available (the harness resolves
  `@`-includes before the model sees the prompt; a disk marker or a
  model self-report both fail for reasons the 202 itself anticipated).
  The right response was the escape hatch the 202 pre-authorized, not a
  workaround that would have quietly traded resilience for savings. See
  [[Backlog#21|vault/Backlog.md item 21]].
- **State criterion expectations as deltas against a measured baseline,
  never as unmeasured absolutes.** Criterion 3(c)'s "returns nothing"
  was wrong (4 pre-existing hits); the underlying property it was
  protecting held regardless, once measured against a baseline rather
  than an assumption. Safety advisory 1, `SAFETY.md`.
- **A transient test-count discrepancy across parallel specialists is
  not four different real states — it is snapshots at different points
  in one shared, moving tree.** Each of S1/S2/S3/S4 read
  `test_doctrine_integrity.py` at a different moment during ~13-20
  minutes of concurrent execution and got a different number (83/83
  through 84/85); the authoritative reading is the one taken once,
  after all specialists return, which is what the Dispatcher and the
  Safety Officer both did independently (85/85, matching).

## Deviations this incident

None — all four specialists returned `status: "done"` on their first
spawn, no `deviation` or `blocked` returns, no fix-tasking cycle, no
Safety halt. One Dispatcher-side bookkeeping defect occurred (a
`214-LOG.md` append landed two entries out of chronological order,
timestamps unaffected) — caught and corrected before any scoped read
relied on the wrong order; recorded plainly in `214-LOG.md` rather than
silently fixed.

## Deploy status

**Deployed** 2026-07-28 by `/dcs-deploy`, under Delegation v4 deploy
authority (1 row, 0 `forbidden_globs` hits, within `max_rows_per_train`
— announced, not asked, per doctrine principle 12). Content witness
`python tests/payload_check.py`: before install exit 1 (32 identical, 15
differing — exactly this incident's own 15 payload files, the expected
red-before-ship signal, not a discrepancy); after install exit 0 (47
identical, 0 differing, 0 repo-only, 0 installed-only). Integration-branch
sha `202e00a` pinned unchanged across both runs. Version marker
`~/.claude/dcs/VERSION` stayed `0.6.11` — no bump needed or made, a
legitimate same-version content ship per `deploy-marker-blind`'s own
lesson (the witness is the proof, not the version string moving). Branch
`dcs/token-economy` deleted — the witness confirmed the ship, so its
rollback job was done.

## Memory routing

This project's `CLAUDE.md` documents `vault/` (Obsidian, repo-local,
never shipped) as its memory system. Written this close:

- `vault/Meta/building-dcs-lessons.md` §21 — the by-reference
  verification-record lesson (see Lessons above).
- `vault/Backlog.md` item 21 — criterion 5's infeasibility, with the
  tested mechanism and the reopen condition.
- `vault/Backlog.md`, "Follow-up registered at token-economy's close" —
  the four remaining advisory fixes, cross-referenced to the register
  row below.
- `.dcs/esg/REGISTER.md` — new `QUEUED` row `token-economy-advisory-fixes`
  (unranked, pending the next `/dcs-esg`), territory: `dcs/workflows/run.md`,
  `dcs/templates/204-TASKING.md`, `agents/dcs-safety-officer.md`,
  `dcs/templates/STRATEGY.md`.

## Intake source closure

None — ad hoc intake (Owner chat via `/dcs-new`), no external ticket or
row to close.

## Safety Officer's final verdict (verbatim, from SAFETY.md)

```json
{
  "verdict": "pass",
  "refutations": [],
  "advisories": [
    {
      "finding": "202-OBJECTIVES.md criterion 3(c) asserts `grep -rni vault <5 files>` \"returns nothing, confirming no project-specific path was shipped.\" It returns 4 hits. I confirmed all 4 are pre-existing and byte-identical to baseline (diffed stashed vs current sweep output; only REGISTER.md's line number moved, 114->150, the token `vault tech-debt` itself untouched), and none is a project-fact leak: REGISTER.md:150 and close.md:86 are generic illustrations, close.md:148 is a field-lesson narrative, deploy.md:98 lists `vault/` as a payload-inert dir. The substantive requirement is met -- the new text says \"the project's own decision-rationale store ... only if that project's own `CLAUDE.md` documents one\", naming no literal path. The expected grep result was written into the criterion without ever being measured (principle 15).",
      "fix": "Restate 3(c) as \"returns no hit not present at baseline\", with the regenerating command beside it (stash-diff of the sweep), rather than \"returns nothing\"."
    },
    {
      "finding": "dcs/templates/204-TASKING.md contradicts itself two lines apart. The comment now ends `Cite the decisive excerpt or file:line, never a full unabridged transcript.` (line 35); the example immediately below is still `{{e.g. \"pytest tests/test_inventory_repo.py -x -- full output\"}}` (line 37). Since that example is the pattern a Planning Chief copies when filling `evidence_required`, it propagates the instruction the new rule exists to stop. Criterion 6 is still met -- the rule text is present in all five locations.",
      "fix": "Change the example's trailing `-- full output` to `-- cite the failing assertion`."
    },
    {
      "finding": "run.md step 3's new doctrine.md carve-out reads: \"re-read it only where there is real doubt it is still in context (a long gap, or a resumed session).\" That is a model self-report about its own context -- precisely the mechanism criterion 5 was dropped for, per 202 criterion 5's own words (\"silently wrong across an auto-compaction\"). It is not a regression (baseline run.md instructed no per-phase doctrine re-read either) and doctrine.md is in no diff, so criterion 5's check passes; but it narrows the new generic instruction using a judgment the same period ruled unsafe to make.",
      "fix": "Replace the judgment clause with the unconditional fact: doctrine.md is @-included at run.md's top, so it is loaded for this invocation -- drop \"real doubt\" and let the phase workflows' own boundaries handle a fresh spawn."
    },
    {
      "finding": "agents/dcs-safety-officer.md's new by-reference exception permits citing a prior verdict's `checked[]` entry for \"a subject you have yourself just established is unchanged with a named command you ran (a scoped `git diff` returning empty, or equivalent).\" For a *derived* subject -- e.g. \"I re-ran the suite, 85/85\" -- an empty diff on the test file does not establish the result is unchanged, because its inputs live in other files. The `never for anything in the fix-tasking's files_touched` bar catches the common case, so criterion 4 is met.",
      "fix": "Add: for a derived subject (a test result, a byte budget, a count), \"unchanged\" requires its INPUTS unchanged, not just the file that produced it."
    },
    {
      "finding": "The live-ESG figure in 202 criterion 3 / IAP step 8 (118,525 + 59,711 = 178,236 B) is stale. I re-measured at esg_root=C:/DCS: 119,428 + 59,711 = 179,139 B, matching S4 exactly. This is already principle-15-compliant by construction -- the 202 carries `wc -c` beside the number and explicitly says \"don't trust this session's own ... reading\" -- so it is noted only so the IC uses a fresh measurement, not this one, at close.",
      "fix": "Re-run `wc -c` at the moment of the close-time compaction; do not carry 178,236 forward."
    },
    {
      "finding": "dcs/templates/STRATEGY.md's cap comment says \"CAP: <= 5 LINES total per entry\" then enumerates four items (\"Nothing beyond these four fits inside the cap\"), leaving the fifth line unexplained; and the template's own optional-pointer placeholder wraps across 3 physical lines, so the shipped example reads as 6 lines until filled in. The cap number matches the 202's own \"5 lines or fewer\" verbatim, so criterion 3 is met.",
      "fix": "Either state the cap as 4, or name what the 5th line is for; unwrap the placeholder to one physical line."
    }
  ]
}
```

Full `checked[]` list (22 items) and the officer's rationale: `SAFETY.md`
in this directory, copied in verbatim per forms.md's single-writer rule.

**Command point 4 correction, recorded here per doctrine principle 15:**
`dcs-commander` found `SAFETY.md`'s `checked[]` item 12 contains a false
clause ("confirmed new.md and plan.md are absent from git status" —
`plan.md` was one of the 15 modified files). The commander independently
re-verified the invariant that clause was defending (criterion 3's
territory-glob-writing logic in `plan.md` step 5a, untouched by the
period's actual edits at unrelated line numbers) and ruled the pass
stands on that independent check, not on the false sentence. **This
`SAFETY.md` entry must never be cited by reference in a future
verdict.**
