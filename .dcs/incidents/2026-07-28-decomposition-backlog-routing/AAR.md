<!--
AAR.md -- After Action Report, written by the IC during /dcs-close. Requires
a green (pass) Safety Officer verdict to exist before this file is written
-- close.md enforces this, do not write an AAR to paper over a halt.
-->

# AAR — After Action Report

**Incident:** decomposition-backlog-routing
**Type:** 3
**Opened:** 2026-07-28
**Closed:** 2026-07-29
**Operational periods:** 1

## Outcome

All four period-1 acceptance criteria were met, verified independently by
the Safety Officer (zero refutations) and re-checked by the IC at command
point 4 against the actual diff and fresh suite runs, not accepted on
report:

1. `dcs/workflows/new.md` step 4a now proposes a Priority (`H`/`M`/`L`)
   for every decomposed defect and routes `L`-tier defects to the
   project's own `CLAUDE.md`-documented lightweight surface instead of a
   `REGISTER.md` row — a project documenting none keeps today's
   unconditional behavior. Met.
2. `dcs/workflows/esg.md` step 2's cluster (b) gained the mirror
   disposition, offered as one of step 3's `AskUserQuestion` options. Met.
3. `dcs/references/doctrine.md` principle 4 states the bar as a standing
   rule (`(v0.6.13)` parenthetical), amended in place — no new principle,
   numbering/count unchanged (verified: `python
   tests/test_doctrine_integrity.py` principle-numbering checks all
   PASS). Met.
4. All three suites green: `test_doctrine_integrity.py` 86/86,
   `test_dcs_gate.py` 100/100, `test_dcs_intake.py` 10/10 (run
   independently by the Safety Officer and again by the IC after
   integration). Met.

**Owner-UAT:** not applicable this period — every criterion was
agent-verifiable (workflow-prose reading, byte/line counts, test suite
runs); no browser/manual observation was required by the IAP's
verification plan.

**Deploy status:** not deployed. This close merges to `main`; the
register row lands `MERGED (deploy pending)`. `/dcs-deploy` is a separate,
later, Owner-batched act.

## What worked

- **Keying the bar on the register template's own lowest priority tier
  (`L`) rather than a Type/shape test.** The Planning Chief tested the
  shape-based alternative against this incident's own evidence before
  committing to a design: the three live `QUEUED` rows the 201 cited as
  the symptom were all Type 3 at priority `L` — a "Type-5-shaped only"
  bar would have caught none of them. Deciding by measurement against
  real data, before writing any prose, is what kept this from becoming a
  second under-specified bar layered over the first.
- **Central, single-author wording for the shared bar.** The Planning
  Chief fixed the exact tier name and condition once and handed identical
  text to both specialists, rather than letting each invent its own
  phrasing. The Safety Officer's side-by-side read of all three hunks
  found the tier, condition, and fallback identical across
  `doctrine.md`/`new.md`/`esg.md` — the one place they diverged (the
  "harm is never `L`" clause, present only in `new.md`) is recorded as
  advisory 2, not a defect that slipped through.
- **Runtime CLAUDE.md discovery instead of a hardcoded path.** Both
  taskings carried the "ship no project facts" constraint as a hard
  constraint with its own evidence requirement (a grep that must return
  empty), not a suggestion — the Safety Officer's own independent
  per-token grep over the added diff lines confirmed zero hits for
  `vault`, `Backlog.md`, or any project-specific path.
- **Budget-aware tasking.** Both near-ceiling files (`new.md` at
  242/250 lines, the hot path at 37,458/37,888 bytes going in) had
  explicit net-delta caps in their own taskings, measured with the merge
  guard's own counting method rather than `wc -l`. Both specialists
  landed inside their caps on the first attempt — zero deviations, zero
  Safety halts, one operational period.
- **Splitting the incidental Record-bullet finding at the stem instead of
  folding it in.** A situation analyst found `esg.md` step 4's Record
  bullet never writes back a row for cluster (b) — a real, adjacent gap
  in the same file this incident needed to touch. Registering it
  separately (`esg-intake-writeback-gap`) rather than absorbing it kept
  this incident's own scope to the one bar it was about, honoring the
  very principle (`decompose, don't accrete`) its own fix implements.

## Lessons

- **A priority-keyed bar beats a shape-keyed one when the live data says
  so — test the alternative against real rows before writing the rule,
  not after.** The obvious-sounding "trivial-shaped defects only" framing
  from the original intake would have shipped a bar that caught none of
  this incident's own three cited symptom rows. Reusable pattern: before
  committing prose for any bar/threshold, run it mentally (or literally)
  against the concrete instances that motivated writing it.
- **When two files must state one rule identically and the constitution
  wins on conflict, fix the wording once, centrally, and hand it to every
  tasking verbatim — don't let per-specialist judgment reconstruct it.**
  This incident did that by design (Planning Chief's tactic T6) and the
  Safety Officer's side-by-side check found only the one clause that
  wasn't centrally mandated (the "harm is never `L`" guard) actually
  diverged. The mechanism, not the discipline, is what held.
- **A worktree inherits only committed state — an uncommitted edit
  sitting in the main checkout when a worktree opens is invisible to
  that worktree, and collides silently at merge time if both sides touch
  the same file.** Found live during this close: the main checkout held
  an uncommitted ninth-`/dcs-esg`-session edit to `vault/Backlog.md`
  (and other vault files) from *before* this incident's worktree was
  created; this incident's own close also needed to edit `Backlog.md`.
  Resolved by committing the pre-existing main-checkout edit as its own
  standalone commit (`6ecb136`) before merging, so the merge became a
  clean 3-way merge over disjoint hunks instead of a collision between
  one committed side and one uncommitted side. Reusable pattern: `git
  status` in the **primary checkout**, not just the worktree, before a
  close's merge step whenever the close itself needs to touch a file
  (`vault/**` especially) that an ESG session might independently be
  mid-edit on.

## Deviations this incident

None — executed as planned, per `214-LOG.md` (source of this claim, not
memory): zero `status: "deviation"` returns, zero `SAFETY-HALT:` entries,
one stamped IAP, one operational period, disposed `close` at command
point 4 on the first Safety pass.

## Memory routing

- **`dcs/references/doctrine-appendix.md`** (ships, never `@`-included):
  +1 entry under the existing "Principle 4" cluster — the provenance
  story for the `(v0.6.13)` bar (third-party review, the priority-vs-
  triviality split and fold, why the tier was measured rather than
  assumed). This is a rule change (principle 4 amendment, already in the
  shipped `doctrine.md`), so its story is the appendix's job per this
  project's own `CLAUDE.md` routing rule.
- **`vault/Backlog.md`** (repo-local, never shipped): +1 section,
  "Follow-up registered at `decomposition-backlog-routing`'s close" —
  the three Safety advisories deliberately not folded into the period's
  integration commit (the all-`L` edge case in `new.md`'s bullet 1, the
  "harm is never `L`" clause missing from two of the three hunks, and a
  minor wording overstatement about the register template's Priority
  vocabulary), each with the officer's own candidate fix, plus the live
  budget headroom fact with its regenerating command.
- **`.dcs/esg/REGISTER.md`**: `esg-intake-writeback-gap`'s row (the
  separately-registered, independent-root-cause sibling finding) had its
  scope note widened at the Safety verdict (advisory 3) to record that
  cluster (b) now carries two outcomes needing write-back, not one —
  direct bookkeeping, not a lesson file.
- No `vault/Meta/building-dcs-lessons.md` entry was written. The budget-
  headroom finding (both touched files now near their ceilings) directly
  corroborates that file's very recent lesson #24 (`workflow-budget-
  enforcement`, closed hours earlier) rather than adding a new pattern;
  recording it a second time as a fresh numbered lesson would be exactly
  the register-style accretion this incident's own fix exists to slow
  down. It is recorded once, with its regenerating command, in the
  `vault/Backlog.md` addition above.

## Intake source closure

Intake source is this project's own `.dcs/esg/REGISTER.md` row
(`decomposition-backlog-routing`, rank 8) — not an external system.
Closure is this close's own step 5a.3 (`ACTIVE` → `MERGED (deploy
pending)`), not a separate flag-for-Owner action.

## Safety Officer's final verdict (verbatim, from SAFETY.md)

```json
{
  "verdict": "pass",
  "refutations": [],
  "advisories": [
    {
      "finding": "new.md:81-86 — the all-`L` corner case is under-specified. Bullet 1 now reads \"Register every defect at `H`/`M` ... then open **one** — the one on the critical path\"; the pre-change text read \"Register every defect ... then open **one** of them\", where \"them\" was every defect. Dropping \"of them\" re-scopes the open-one instruction to the H/M set. If a stem decomposes into defects that are ALL `L` and the project documents a surface, no row is written and no set is named to open the incident from — /dcs-new could produce nothing. Not an AC1 failure: the routing bar itself stays decidable in all four cases the IAP plan named (H+surface, H-none, L+surface, L-none), and bullet 4's \"say plainly ... where they went\" makes a silent drop visible to the Owner.",
      "fix": "One clause at close: \"...then open **one** — the one on the critical path; where every defect is `L`, open the one the Owner came for and route the rest.\""
    },
    {
      "finding": "\"Harm is never `L`.\" (new.md:91-92) exists in only one of the three hunks. The doctrine.md:55 amendment and the esg.md:68-75 mirror both omit it, so the constitution — which wins on conflict in this project — is silent on the guard that stops a harm-causing defect being demoted below the bar. Risk is bounded on the esg side because routing is offered as an option inside step 3's `AskUserQuestion` round (esg.md:105), i.e. Owner-decided. Not a divergence in the three elements the IAP plan named: tier (`L`), condition (project's own `CLAUDE.md` documents a lightweight backlog-style surface) and fallback (unconditional row) agree verbatim across all three.",
      "fix": "Carry the harm clause into doctrine principle 4's parenthetical at close, or record in the AAR that the guard is deliberately stem-only."
    },
    {
      "finding": "The new cluster-(b) option widens the separately-registered `esg-intake-writeback-gap` rather than leaving it flat. I confirmed \"(b)\" appears exactly once in the whole of esg.md (line 67, the cluster definition) and that step 4's Record bullet enumerates only (a)/(c)/(e)/(f) — so cluster (b) now carries TWO decision outcomes with no write-back instruction where it previously carried one, and the new outcome's target is a file esg.md never names again. The text itself is untouched and not worsened (steps 3/4/5 byte-identical to HEAD), and the 202's out-of-scope constraint to avoid step 4's Record lines was honoured in full.",
      "fix": "At close, amend the `esg-intake-writeback-gap` register row's scope to name both branches (queue → REGISTER.md, and route → the project-documented surface), so its eventual fix does not land half-done."
    },
    {
      "finding": "Both files this incident enlarged are now close to their ceilings, and the next edit to either goes red: hot path 37,735 / 37,888 bytes (153 left), new.md 248 / 250 lines (2 left). esg.md is comfortable at 159 / 250. Regenerate with the guard's own method, not `wc -l` — CRLF→LF-normalised byte count over `dcs/references/doctrine.md` + `dcs/references/schemas.md` for the hot path, and `_workflow_line_count` in `tests/test_doctrine_integrity.py:1273` for lines (it adds 1 for content after the last LF, where `wc -l` under-counts by exactly one).",
      "fix": "Note the measured headroom plus its regenerating command in the AAR; treat doctrine.md and new.md as budget-blocked for the next incident until a trim."
    },
    {
      "finding": "`(v0.6.13)` appears exactly three times, one per touched file (doctrine.md:55, new.md:87, esg.md:68), while `dcs/VERSION` and `package.json` both read `0.6.12`. This was ruled in-scope at command point 2 (`214-LOG.md:29`), so it is not a defect — but nothing mechanical will catch a missed bump: the merge guard's version-sync check compares `dcs/VERSION` against `package.json` only, and never compares either against a prose version label.",
      "fix": "Close must bump both files in the same commit (CLAUDE.md: \"Version sync is atomic\"). Manual step — no test covers it."
    },
    {
      "finding": "new.md:81-82 calls `H`/`M`/`L` \"the register template's vocabulary\"; `dcs/templates/REGISTER.md:150`'s Priority placeholder is actually `{{H\\|M\\|L or rank}}`. The branch stays total because the step mandates the stem propose one of H/M/L, and this project's live register writes both (`**L (rank 12)**`), so nothing is un-followable — but the parenthetical slightly overstates what the referenced file says.",
      "fix": "Optional: \"(`H`/`M`/`L`, the register template's letter tiers)\"."
    }
  ],
  "checked": ["see SAFETY.md for the full 16-item checked[] list -- not repeated here to keep this AAR from re-growing the same duplicate-copy problem this incident's own fix targets; SAFETY.md is this file's permanent neighbor in the same incident directory"]
}
```

Full verdict with the complete `checked[]` list: `SAFETY.md` (this
directory). The five-item resolution of each advisory above (three
fixed/routed now, three folded into this AAR/Backlog) is recorded there
under "IC resolution of each advisory."
