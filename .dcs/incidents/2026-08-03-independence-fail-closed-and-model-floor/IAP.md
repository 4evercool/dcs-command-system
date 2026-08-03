# IAP — Incident Action Plan

**Incident:** independence-fail-closed-and-model-floor
**Type:** 3
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `204-TASKING/S1.md` · `204-TASKING/S2.md`
· `204-TASKING/S3.md` · `204-TASKING/S4.md` (`203-ORG.md` skipped —
default Type 3 activation, logged in `214-LOG.md`)

## Objectives (summary of 202)

**Goal:** DCS's close-time and Delegation-approval machinery stop
treating every operating model and every Safety-Officer-spawn outcome
identically. An unattended close is refused whenever this period's
Safety verdict either lacks proof of independent-agent origin or
contains `checked` commands that do not reproduce — refusal means PARK
or an Owner `AskUserQuestion` gate, never a silent close. Separately,
`.dcs/esg/DELEGATION.md` gains an approved-model list, and
unattended/auto-approval bounds (`auto_approve_type3`, `deploy.auto`,
`deploy.auto_after_close`) apply only when the session's operating model
is on that list — every other model gets full v0.1
every-gate-is-an-Owner-gate behavior at every site that currently reads
those bounds.

**Acceptance criteria** (full text with `Verified:` clauses —
`202-OBJECTIVES.md` is the canonical copy; criteria 1 and 7 below carry
`[CORRECTED at /dcs-plan lint 3a]` markers from two arithmetic fixes
applied before either command-point spawn, per doctrine's "a failure is
yours to fix, never a reason to spend a command point"):

1. **[Corrected]** `execute.md` step 8 gains an explicit spawn-liveness
   fallback in its own body — a spawn that never returns a decision is
   never silently treated as "Safety verification happened."
2. `close.md` refuses an unattended close when independent Safety spawn
   could not be established — PARK or Owner `AskUserQuestion`, before
   the merge, never a silent pass-through.
3. `schemas.md` #5's `checked` field states each entry must be a
   **regenerable** command.
4. `close.md` re-runs at least one `checked[]` command before the
   merge; a non-reproducing entry is treated as a halt through the
   existing halt-handling machinery (see command-point-2 ratification
   below — this means PARK/`AskUserQuestion`, not a new sentinel).
5. `doctrine.md` states the new rule, funded within the hot-path budget
   (37834/37888 bytes measured at plan time — 54 B headroom; funded by
   compressing doctrine.md/schemas.md prose and relocating it verbatim to
   a new `doctrine-appendix.md` `### D6` anchor, never by trimming the
   appendix itself).
6. `.dcs/esg/DELEGATION.md`'s schema (`schemas.md` #7) and the founding
   `dcs/templates/DELEGATION.md` both gain an `approved_models` field;
   absent/empty means no model approved (fail-closed).
7. **[Corrected — 9 real sites across 6 files]** every
   `auto_approve_type3`/`deploy.auto`/`deploy.auto_after_close` read
   site — `plan.md:31`+`124-130`, `run.md:70-71`+`154-158`,
   `loop.md:28-38`+`71`, `deploy.md:117-124`, `status.md:106`,
   `esg.md:33` — is model-gated. Known out-of-scope gap:
   `plan.md:130`'s config.json fallback branch has no model floor
   (reported to Owner below, not silently absorbed).
8. Fixture/coverage proof both mechanisms actually gate: (a) fixtures
   for criterion 4's re-run tool; (b) a merge-guard coverage check for
   criterion 7, built around two independently-provable phrasing classes
   (literal bound keys vs. `deploy.md`'s non-literal "`auto: true`"
   form) — see Tactics T7-T11 below for why a single-class check would
   ship the hardest site uncovered.
9. All three test suites stay green (156/156, 100/100, 18/18 baseline);
   new structural checks added for criteria 3/6.
10. **[Owner]** `.dcs/esg/DELEGATION.md` amended to v7 with
    `approved_models` populated (`fable` at minimum) — Owner's call
    alone, via `AskUserQuestion`; witness-command output (`grep -n
    "approved_models"` and `grep -n '"version": 7'` against
    `<esg_root>/.dcs/esg/DELEGATION.md`) must be pasted into
    `214-LOG.md`, since this file is git-ignored and unwitnessable from
    this worktree.
11. **[IC]** Register territory cell refined to the actual 204 partition
    union at step 5a; same out-of-tree-witness treatment as criterion 10.

Full `Out of scope this period` list and `Chief feedback` (5 items,
IC-resolved) are in `202-OBJECTIVES.md` — not restated here.

## Tactics (from the Planning Chief, second/accepted pass)

- **T1:** fund criterion 5 by compressing doctrine.md/schemas.md prose in
  place and relocating verbatim originals to a new doctrine-appendix.md
  `### D6` anchor (the `### D5` convention `spawn-effort-control` already
  established). Appendix edits free zero hot-path bytes and are never
  funding. Invariant: `bytes_removed_from(doctrine+schemas) >=
  bytes_added_to(doctrine+schemas) - 54`.
- **T2:** measured funding menu with existing appendix anchors —
  `Parallel operation` 3068 B / anchor L507, `The lifecycle` 1482 B /
  L440, `Automation layers` 1448 B / L486, `Relationship to
  project-specific protocols` 1094 B / L452; schemas.md `#2 Chief plan`
  2491 B, `#6 Commander decisions` 1810 B / anchor L590.
- **T3:** guard-pinned strings S1 must not touch — verbatim
  `GRAMMAR_LINE` quote (check 12c), three sentinel tokens (12f), any
  heading cited by name from a workflow/charter (check 6), principle
  numbering contiguity (check 2).
- **T4:** satisfy criterion 3 by amending schemas.md #5's EXISTING
  `checked` row, never adding a new field (checks 18/20 would force a
  cross-territory edit into execute.md/safety-officer.md).
- **T5:** fix schemas.md:102's non-conforming halt example in the same
  tasking as criterion 3.
- **T6:** criterion 4's comparison is containment, not byte equality;
  the tool selects a re-runnable entry by an explicit stability rule
  that skips working-tree-diff entries; "no stable entry found" is a
  reported finding, never a silent pass.
- **T7:** criterion 7's coverage check must derive its population from
  TWO named phrasing classes — 8 of 9 sites carry a literal bound key,
  `deploy.md`'s site phrases the same bound as "a `deploy` object with
  `auto: true`", zero hits under any literal-key pattern.
- **T8:** each phrasing class's population must be asserted non-empty as
  its own named case, so an empty class is a failure, not a silently
  skipped loop.
- **T9:** the check must print a per-class runtime inventory (class
  name, matched-site count, file:line) so evidence discloses which
  classes actually matched.
- **T10:** a non-vacuity case must prove class B is load-bearing:
  `deploy.md`'s actual sentence returns True under the class-B matcher
  and False under class-A.
- **T11:** do not freeze "9 sites" into the guard itself — assert the
  invariant (every discovered site gated, both classes non-empty), never
  the instance (principle 15); the count 9 stays in the 202 with its
  regenerating command.
- **T12:** route criterion 4's close-time failure through the existing
  PARK/`AskUserQuestion` disposition (criterion 2's own machinery)
  rather than emitting a literal `SAFETY-HALT:` token — close.md has
  zero sentinel tokens today and would trip check 12(c)'s
  verbatim-grammar-quote requirement (205 B) at only 2 lines of
  headroom, and a close-time `SAFETY-HALT:` would also consume a
  principle-13 halt-ceiling slot via `dcs_gate.py`'s `halt_cycles()`, a
  behavioral change with `dcs/hooks/**` explicitly out of scope this
  period.
- **T13:** workflow line ceilings are a hard co-constraint on S2/S3
  (plan.md 249/250, execute.md 248/250, close.md 248/250, deploy.md
  245/250) — funding is in-file compression, mandatory, same tasking.

## File-territory partition

Verified genuinely disjoint independently by both the IC (twice — tasking
lint, both passes) and `dcs-commander` (twice — both `iap_review`
passes), file-by-file, not trusted from `partition_ok: true` alone.

| Specialist | Territory | Forbidden (highlights — full lists in 204-TASKING/*.md) |
|---|---|---|
| S1 | `dcs/references/doctrine.md`, `schemas.md`, `doctrine-appendix.md`, `typing.md`; `dcs/templates/DELEGATION.md`; `agents/dcs-safety-officer.md` | `dcs/workflows/**`, `dcs/tools/**`, `tests/**`, `dcs/hooks/**`, other `agents/*.md`, `.dcs/**`, `vault/**` |
| S2 | `dcs/workflows/plan.md`, `run.md`, `loop.md`, `deploy.md`, `status.md`, `esg.md` | `dcs/workflows/execute.md`, `close.md`, `new.md`, `init.md`; `dcs/references/**`, `dcs/templates/**`, `dcs/tools/**`, `dcs/hooks/**`, `tests/**`, `agents/**` |
| S3 | `dcs/workflows/execute.md`, `close.md` | `dcs/workflows/plan.md`, `run.md`, `loop.md`, `deploy.md`, `status.md`, `esg.md`, `new.md`, `init.md`; `dcs/references/**`, `dcs/templates/**`, `dcs/tools/**`, `dcs/hooks/**`, `tests/**`, `agents/**` |
| S4 | `dcs/tools/verdict_rerun.py` (new), `tests/fixtures/verdict-rerun/**` (new), `tests/test_doctrine_integrity.py` | `dcs/workflows/**`, `dcs/references/**`, `dcs/templates/**`, `dcs/hooks/**`, `dcs/tools/record_integrity.py`, `dcs/tools/preservation_map.py`, other `tests/*.py`, other `tests/fixtures/**` |

**Partition status:** disjoint — parallel execution. No sequential
staging or worktree isolation needed.

## Risks

- Partition genuinely disjoint (re-verified four times across two
  planning passes) — no file in two territories.
- **Highest risk of the period:** hot-path funding is ~1 kB against 54 B
  of headroom, on prose already trimmed twice (appendix D1-D5). The byte
  ledger balances identically whether a sentence was compressed with its
  meaning preserved or simply destroyed, and no mechanical guard can
  tell the two apart — mitigated by S1's mandatory per-passage
  verbatim-preservation proof (pre-edit text must be a
  whitespace-normalised substring of the post-edit appendix), which the
  Safety Officer independently spot-checks.
- Cross-territory trap avoided by design: a new field in schemas.md #5
  would force an edit into execute.md/safety-officer.md via checks
  18/20 — S1 is forbidden from adding a field; a deviation, not a
  cross-territory edit, if unavoidable.
- Close.md would trip check 12(c)'s grammar-quote requirement if
  criterion 4 emitted a literal `SAFETY-HALT:` token at 2 lines of
  headroom — resolved by command-point-2's ratification (see below):
  S3 reuses the existing PARK/`AskUserQuestion` disposition instead.
- Workflow line ceilings nearly exhausted with no appendix to relocate
  into — plan.md/execute.md/close.md/deploy.md all carry mandatory
  in-file compression as an explicit tasking obligation.
- S4's coverage check lands in the same file S1/S2/S3 all run as
  evidence — ordering hazard (S4's work-in-progress red cases vs.
  genuine defects), mitigated by requiring named red cases in every
  specialist's evidence.
- Criterion 7's model floor is fail-closed by design — between merge and
  the Owner writing DELEGATION.md v7 (criterion 10), **this project's
  own future sessions get v0.1 every-gate behavior.** Flagged here for
  the Owner's awareness at approval, not left to be discovered later.
- Criteria 10/11 are not witnessable from this worktree at all
  (`.dcs/esg/DELEGATION.md` is git-ignored, main-checkout-only) —
  witness-command output must be pasted into `214-LOG.md`, never left as
  a bare assertion.
- No version bump tasked, deliberately — a close-time/deploy-time
  single-writer act, not this period's job.
- Criterion 2 ships verified by structure (word-presence plus
  co-location case), not by behavior — no runtime exists to execute
  close.md's unattended branch against; this is the architecture's
  ceiling, stated plainly rather than papered over.
- Non-blocking observations from `dcs-commander`'s second-pass review:
  (a) criterion 3's "(zero matches anywhere in the shipped payload
  today)" aside is imprecise — "un-regenerable" occurs at
  `agents/dcs-safety-officer.md:83`/`109` — but the operative `Verified:`
  command is scoped to `schemas.md`, where the baseline genuinely is 0,
  so the check still discriminates correctly; S1 should know the aside
  overclaims even though the check is sound. (b) S4's coverage-walker
  corpus must stay scoped to `dcs/workflows/*.md` — a broader corpus
  would self-announce red on definitional class-A matches inside
  `schemas.md`'s own JSON example and `templates/DELEGATION.md`; any
  such red is fixed by narrowing the corpus, never by weakening a class.

**Command-point-2 ratification (binding on the Safety Officer):**
criterion 4's parenthetical mention of a `SAFETY-HALT:` sentinel is
superseded by this IAP's own Goal text ("refusal means PARK or an Owner
`AskUserQuestion` gate, never a silent close") for the
non-reproducing-`checked`-entry case. `dcs-commander` ratified this on
the record at the second `iap_review` pass rather than forcing a third
chief re-spawn over a parenthetical the Goal already overrides — a
literal reading of the superseded parenthetical is not itself a valid
Safety Officer refutation ground. Full ratification text:
`214-LOG.md`, entry timestamped `2026-08-03T17:31:21+11:00`.

## Verification plan

End to end, for the Safety Officer — every command re-run independently
against the assembled tree, never accepted from a specialist's return.

1. **Suites:** `test_doctrine_integrity.py`, `test_dcs_gate.py`,
   `test_dcs_intake.py` each report `N/N`; baselines 156/156, 100/100,
   18/18 — the first should have grown by S4's new cases.
2. **Hot-path ledger**, re-derived not accepted: regen command at
   `test_doctrine_integrity.py:211`, confirm sum <= 37888, confirm S1's
   funding ledger reconciles against the 23872/13962/37834 baseline, and
   confirm no ledger row claims an appendix deletion as funding
   (`doctrine-appendix.md` must have grown). Independently spot-check at
   least two moved passages via the verbatim-preservation proof.
3. **Criterion greps**, run fresh: criterion 3 `regenerable` inside #5;
   criterion 6 `approved_models` in schemas.md #7 + templates/DELEGATION.md
   (payload before-count was zero); criterion 7 `approved_models` count
   across the six workflows (plan/run/loop each >= 2); criterion 2
   `unattended` in close.md (before-count 0). Criterion 1: do NOT use
   the original 202 command (10 matches pre-change, proves nothing) —
   use the corrected `sed`-scoped check confirming the fallback sits
   inside step 8's own body.
4. **Model-floor coverage liveness — one revert PER phrasing class, not
   one revert total:** (a) deploy-object class, MANDATORY target
   `deploy.md` step 5 — remove its model gate, confirm the guard goes
   RED naming `deploy.md` and the deploy-object class, restore, confirm
   green (if the guard stays green with deploy.md's gate removed, that
   is a refutation); (b) literal-bound-key class, target any site
   outside deploy.md — same remove/red/restore/green cycle; (c)
   class-floor liveness — neuter one class's matcher, confirm that
   class's own non-empty case reds; (d) read the restored tree's
   per-class runtime inventory, confirm both classes non-zero with
   `deploy.md` under the deploy-object class.
5. **Verdict re-run tool:** run the three fixtures (reproducing -> 0,
   non-reproducing -> 1 named, all-non-reproducible-by-design -> a
   finding, never 0), then run it for real against this incident's own
   eventual `SAFETY.md`.
6. **Criterion 2 desk-check:** walk close.md's unattended branch,
   confirm both dispositions reachable and both sit before the merge,
   confirm S4(d)'s co-location case actually covers it.
7. **201 repro path**, the original symptom: trace that a
   never-returning Safety Officer spawn cannot reach a completed close,
   and that an unlisted-model session gets full v0.1 behavior at all
   nine sites including deploy.md's.
8. **Structural hygiene:** checks 2, 6, 7, 12, 17, 18, 19, 20 green by
   name; all workflow line counts within ceiling; version sync
   unaffected (no bump tasked); schemas.md fenced blocks all parse.
9. **Manual checks with no command:** read close.md's new gate end to
   end confirming no branch falls through to an unhandled merge; confirm
   absent/empty `approved_models` denies (not permits) at every S2 site;
   confirm doctrine's new text doesn't overclaim the
   self-reported-identity guarantee (the model floor demotes an honest
   unlisted operator, does nothing against a dishonest one — the
   Owner-adopted design, stated not papered over).
10. **[Owner/IC, outside the worktree]** Criteria 10/11's witness-command
    output pasted into `214-LOG.md` — cannot be verified from this
    branch at all.

## Deviation history (this period)

None — this is period 1's first (and, after one `iap_review` reject at
command point 2, second) IAP for this period. The reject was resolved
entirely within planning (a fresh Planning Chief spawn per doctrine
principle 9b); no specialist had been dispatched yet, so this is not a
deviation in the `execute.md`-triggered sense. Full history:
`214-LOG.md`, entries `17:04:58` (reject) through `17:31:21` (accept).
