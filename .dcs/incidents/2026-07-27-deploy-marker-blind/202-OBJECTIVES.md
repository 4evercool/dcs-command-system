# 202 — Objectives (Operational Period 1, **revision 2** / attempt 2)

**Incident:** deploy-marker-blind
**Period:** 1 · **Revision:** 2, after Safety halt 2 and escalation trigger (b)

> **Revision 1 is superseded by this file, not deleted from the record** —
> its text and the two halts that produced this revision are in
> `214-LOG.md`, and the escalation is in
> `<esg_root>/.dcs/esg/SITREPS/deploy-marker-blind-p1.md`.

## Why this revision exists

Two Safety halts, and the convergence read came out **same class**: three
refutations of one form — *two statements of one contract, disagreeing*
(`deploy.md` step 4 vs step 7; `CLAUDE.md:40` vs step 7; `REGISTER.md`'s
`DEPLOYED` definition vs `REGISTER.md`'s facts-only rule thirteen lines
below it).

**The mechanism of the recurrence was measured, not guessed, and it was
revision 1's own criterion 5.** That criterion defined its population by
**vocabulary**; the defect is defined by **role**. The line that halted the
period reads *"deployed marker was read"* and matched none of the four
patterns, so criterion 5 was **met at both halts** while the class kept
shipping. That is whack-a-mole against an unenumerated population, and per
doctrine principle 13 (v0.5.9) the answer is to raise the altitude of the
fix rather than close one more site. The Owner chose that at the first
offer, so the rotation stopped at two halts instead of four.

## Goal (unchanged from revision 1)

`/dcs-deploy` can tell a shipped payload from an unshipped one using
evidence that changes when the **content** changes, so that a correct ship
which deliberately did not bump the version verifies as shipped instead of
tripping step 7's stop condition; an unshipped `MERGED` row is never
recorded live by step 4's reconciliation; and the witness that has done
this job by hand three times exists as a runnable command **in the repo**.

**Extended by this revision:** and every site in the package that states
that contract says the *same* thing, held there by a mechanism rather than
by a criterion in one incident's 202.

## Acceptance criteria

### Carried unchanged — already met on the Safety Officer's own evidence

Criteria 1-4 and 6-8 are **not re-litigated**. Both officers verified them
independently; the second ran 14 perturbation scenarios itself, proved the
payload set derived by injecting three files the script had never seen, and
traced both marker shapes through step 7. They are restated so this file
stays self-contained, and a fresh officer will re-derive them anyway.

1. **A payload-witness command exists in the repo and runs** — per-file
   sha256 against the installed tree, reporting identical / differing /
   repo-only / installed-only, non-zero exit when anything differs. Payload
   set **derived** by walking the way the installer does, **never a
   hardcoded list** (principle 15).
   **[already delivered — no tasking, deliberately]**
2. **The witness is proven to go RED**, not only green — perturbed
   **scratch copy**, non-zero exit naming the altered file. **No install
   performed.**
   **[already delivered — no tasking, deliberately]**

   > **Ownership note for criteria 1 and 2 (lint check 6).** These map to
   > **no tasking in this revision, and that is correct rather than an
   > omission.** `tests/payload_check.py` is Safety-proven against both —
   > the second officer ran 14 perturbation scenarios itself and proved the
   > payload set derived by injecting three files the script had never seen
   > — and it is **forbidden to every tasking** this revision, so nothing
   > can quietly re-open it. Criterion 12 asks for a check that its
   > exclusion constants *stay* aligned with the suite's, **not** for an
   > edit to the file. A fresh Safety Officer will re-derive 1 and 2 as
   > regression, which is the only work they generate.
3. **`deploy.md` step 7's stop condition is content-shaped** — never "the
   version string is unchanged".
4. **`deploy.md` step 4 has defined behaviour for a marker that is readable
   but not a commit-ish.**
6. **`CLAUDE.md`'s Deploy table states the contract step 7 actually
   enforces** — all four exit classes.
7. **A CHANGELOG entry in the existing, unpublished 0.6.10 section.**
   Re-measure `npm view dcs-command-system version` rather than trusting
   this sentence; it read `0.6.9` at both plan times and it moves.
8. **All three suites green**, read from each suite's own `N/M passed`
   line.

### Revised

5. **No surviving site in the population presents the version marker as
   sufficient proof of a ship — where the population is defined by ROLE,
   not by vocabulary.** The binding enumerator is now:

   ```bash
   grep -rniE 'deployed[- ]?(version )?marker|deployed_sha|marker (actually )?advanc|VERSION.*after deploy|DEPLOYED only after|deploy(ed|-)?[ -]evidence|deployed[- ]content|content witness|payload witness' dcs/ agents/ skills/ CLAUDE.md README.md docs/
   ```

   Measured at this revision's plan time, 2026-07-27, from the worktree
   root: **18 hits in 6 files** — `deploy.md` **10**,
   `dcs/templates/REGISTER.md` 3, `skills/dcs-deploy/SKILL.md` 2,
   `dcs/workflows/close.md` 1, `CLAUDE.md` 1,
   `docs/spec-v0.3-parallel.md` 1. *(The first draft of this line said
   `deploy.md` 9; the Planning Chief caught it and it was re-measured at
   lint. The total and the file count were right, the breakdown was not —
   which is why the criterion binds to the command's live output and not
   to this list.)* Met when that output is walked end to end and every hit
   is either
   changed or **named in the owning tasking with a stated reason for being
   deliberately correct as written**. Re-run it to regenerate; the counts
   move with the tree.

   `bin/**` remains outside the population and is **not** a refutation —
   carried as register row `doctor-version-only-check`.

5a. **NEGATIVE CONTROL — the new population must be shown to reach further
   than the old one, not merely to be worded differently.** Evidence
   required: run **both** enumerators and show that the new one returns
   the sentence *"DEPLOYED only after the project's deployed marker was
   read and the merge commit confirmed an ancestor of it"* in
   `dcs/templates/REGISTER.md`, and the old one does not. That single
   sentence is the whole reason this revision exists.

   > **Cite the sentence, not a line range** — corrected at the halt-4 fix
   > round on officer 4's advisory. The first draft said
   > `REGISTER.md:59-60` without naming the tree it was measured against,
   > while instructing a measurement on `ba6019e`, where the same text
   > sits at **55-56**. A line number is a derived fact about one specific
   > tree (principle 15), and this one silently pointed at the attempt-1
   > worktree. **This incident has already shipped one thing that
   looked like new capability and was a relabel; a population definition
   that cannot demonstrate new reach is the same mistake at a higher
   altitude.**

### New

10. **No file states the deploy-evidence contract two ways.** This is
    halt 2 at class level rather than as a `REGISTER.md` special case. Two
    known instances, both to be fixed as hits of criterion 5's population
    rather than as one-offs:
    - `dcs/templates/REGISTER.md` — the `DEPLOYED` definition admits two
      routes (commit-ish ancestry **or** a green / stale-extras-only
      witness run) while the facts-only block below states the commit-ish
      route as a **necessary** condition, making the witness route
      unreachable.
    - `dcs/workflows/deploy.md:121` cites that facts-only rule as the
      authority for *"naming the sha **or witness result**"* — an
      instruction the rule as written forbids.

    Verified by reading, and by criterion 11's check going green.

> **CRITERION 11 WAS NARROWED BY THE OWNER AT THE THIRD-HALT ESCALATION,
> 2026-07-27 — judge against this, not against the original text below.**
>
> Officer 3 refuted the guard as first built: its disposition comparator
> (rule B) was defeated by markup and contributed **zero binding** on the
> live tree, and four forged contradictions stayed green. The Owner's
> decision was **"narrow the guard's claim to what it demonstrably
> enforces"**, on the reasoning that *the actual harm is a green PASS line
> asserting something the check cannot see* — **a guard that under-claims
> truthfully is worth more than one that over-claims greenly.**
>
> **Criterion 11 is therefore met when the guard enforces, and claims,
> exactly:**
> - **Rule A** — every declaring paragraph outside the source carries a
>   `` `dcs/workflows/deploy.md` step N `` citation whose N equals the
>   **live parsed** step number.
> - **Rule C** — at most one declaring paragraph per non-source file,
>   tree-wide. *This is the rule that catches halt 2, and it is proven:
>   the halt-2 reintroduction reds on structure alone.*
> - The **structural degeneracy guard** and the anti-erasure floor —
>   erasure must not buy green.
> - **Every PASS-line string literally true of what the check does.**
>
> **Explicitly NOT required, and explicitly not to be claimed:**
> disposition-content agreement (rule B, removed — F2 proved it
> unrepairable: a contradiction can cite step 7 correctly while naming
> none of its classes, in superseded vocabulary), and coverage of
> `CLAUDE.md` (which contains **zero** `DEPLOYED` tokens, so no predicate
> keyed on that token reaches it — a finding to carry forward, not a
> defect to force).
>
> IC directive (iii)'s aspiration to hold rule C over `CLAUDE.md` is
> **recorded as unmet** rather than quietly dropped.

11. **A durable guard holds contract-declaring sites to `deploy.md` step
    7's own live text** — the pattern `tests/test_doctrine_integrity.py`
    already establishes twice: check 13 binds `schemas.md #N` citations to
    the section's real title, and check 14 binds the Safety bar's citing
    prose to the charter's own live step number and bar count. This is what
    "raise the altitude" means concretely: a fourth instance becomes
    **unrepresentable**, not merely unlikely.

    Requirements, taken from what makes checks 13 and 14 work:
    - It **derives its population by walking the tree**, and the only file
      literal in its body is the path of the source of truth (`deploy.md`).
      No hand-written list of sites, no exit-class token hardcoded — parse
      them out of step 7 at run time.
    - **A structural-degeneracy guard**: if the population collapses to
      empty, or step 7 stops parsing, the check goes **red**, never
      vacuously green.
    - **Behavioural proof, not a claim** (the bar both prior checks met):
      forge a disagreement — flip one exit-class disposition in a citing
      site — and show the suite goes red **naming the file and the
      mismatch**; then run the identical forgery against
      `git archive ba6019e` (the pre-incident tree) and show it stays
      green. That is what distinguishes new capability from a relabel.

12. **The two copies of one exclusion rule are held together.**
    `tests/payload_check.py` and `tests/test_doctrine_integrity.py` each
    carry `EXCLUDED_DIRS` / `BYTECODE_SUFFIXES`; they are byte-identical
    today and nothing keeps them so. Assert textual equality by reading
    source text, **not by import** — importing `test_doctrine_integrity.py`
    runs its checks and calls `sys.exit()` at module scope.

    *(This was directed by the IC at command point 4 and held by the
    Dispatcher because it needed a file outside the then-approved
    partition. Criterion 11 brings that file into territory, so it lands
    here rather than as a follow-up.)*

9. **[Owner]** UAT. Unchanged, and still not the Safety Officer's to close:
   the Owner authorised the substituted check by hand on three deploys, so
   whether this is the shape they were reaching for is theirs to say.

## Out of scope this period (unchanged, plus one)

- **`bin/dcs.js`'s `doctor()`** — register row `doctor-version-only-check`.
- **Running an actual deploy, and `npm publish`.**
- **A version bump.** Re-measure at close.
- **Backlog item 12's candidate fix (3)**, and **fix (1)**, the
  installer-written hash marker — rejected with reasons recorded in the
  IAP; `install.ps1` and `install.sh` stay untouched.
- **(new) Re-opening criteria 1-4 and 6-8.** They are met on two officers'
  independent evidence. A fresh officer will re-derive them, but this
  revision does not re-plan them.

## Chief feedback (filled in after the Planning Chief returns)

{{objectives_feedback — pending}}
