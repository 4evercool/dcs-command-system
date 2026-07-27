# 204 — Tasking S1-CONTRACT (revision 2)

**Incident:** deploy-marker-blind · **Period:** 1 · **Revision:** 2
**Specialist:** dcs-ops-specialist (S1-CONTRACT) — fresh spawn
**Runs FIRST.** S2-GUARD and S3-RECORD both depend on your finished text.

## Task

Satisfy criteria **5, 5a and 10**, and fold in every still-open advisory
that touches prose.

### A. Establish the contract shape

Not styling — this is what makes criterion 11's guard implementable.

1. **`dcs/workflows/deploy.md`'s step 7 section is the SINGLE SOURCE.** It
   states the shape branches and, per shape, the disposition (`DEPLOYED` /
   stop). Nothing else in the package states a disposition.
2. **Every other declaring paragraph** — anywhere in `dcs/`, `agents/`,
   `skills/`, `CLAUDE.md` — cites it in exactly this form, verbatim:
   `` `dcs/workflows/deploy.md` step 7 ``. Same shape as the citation
   contract check 14 already enforces for the Safety Officer charter.
3. **At most ONE declaring paragraph per file outside `deploy.md`.** A
   *declaring paragraph* is a blank-line-delimited paragraph containing
   `DEPLOYED` together with proof language (verified / read / confirmed /
   proof / ancestor / witness / evidence). Where a file has two today,
   **merge or demote** — the second becomes disposition-free prose that
   cites, never a restatement.

   > **IC DIRECTIVE (iii), binding: rule 3 holds TREE-WIDE.** `CLAUDE.md`'s
   > Deploy table row and the paragraph beneath it collapse to **one**
   > statement; `skills/dcs-deploy/SKILL.md`'s frontmatter description and
   > `<objective>` carry dispositions in only one place;
   > `docs/spec-v0.3-parallel.md` is made **non-declaring** (a supersession
   > annotation, or quoted as history), **never path-exempted.** The
   > chief offered a fallback scoping rule 3 to `dcs/` and `skills/` only;
   > the IC rejected it, because that drops `CLAUDE.md` — both a halt-1
   > refutation site and where the flawed contract was normatively stated.

### B. The two known criterion-10 instances

1. **`dcs/templates/REGISTER.md`** — the `DEPLOYED` definition (~39-46) is
   the file's one declaring paragraph and gains the citation. The
   facts-only block (~55-61) must **stop restating the `DEPLOYED`
   condition**: delete *"DEPLOYED only after the project's deployed marker
   was read and the merge commit confirmed an ancestor of it"* and the
   *"naming the deployed sha"* clause that presumes the commit-ish route,
   replacing them with a pointer to the definition above plus the
   facts-only discipline itself (a row states what was **verified**).
   **Keep the branch-deleted / worktree-removed clauses and the 2026-07-23
   field lesson intact** — those are a different rule.
2. **`dcs/workflows/deploy.md`'s step 4 out-of-band paragraph** (currently
   ~117-121): it moves rows to `DEPLOYED` *"naming the sha or witness
   result"* and cites the facts-only rule as authority for a phrase that
   rule forbade. Once B.1 lands, make the citation accurate — cite
   `` `dcs/workflows/deploy.md` step 7 `` for the disposition, and the
   facts-only rule only for the facts-only discipline.

### C. Walk criterion 5's enumerator end to end

Re-run it. **Every hit is either changed or named in your return with a
stated reason it is deliberately correct as written.** An unannotated hit
is an incomplete tasking. Known hits needing work, all as **population
members** rather than one-offs:

- `skills/dcs-deploy/SKILL.md` — frontmatter description and `<objective>`
  are witness-specific for what is now shape-dependent. Make them
  shape-neutral; leave exactly one declaring paragraph, or none plus a
  citation. **Keep the frontmatter valid** — integrity checks read it.
- `dcs/workflows/close.md:64-67` — the AAR facts-only artifact list still
  names *"a deployed version marker compared"* as the exemplar deploy
  artifact. Revision 1 fixed lines 75-79 of this same block and missed
  line 66.
- `CLAUDE.md:30`'s table row **plus** the paragraph below it — two
  declaring statements in one file today; collapse under A.3.
- `docs/spec-v0.3-parallel.md:127` — a dated v0.3 design spec reading in
  the present tense. Add a one-clause *"superseded in 0.6.10 — see
  `dcs/workflows/deploy.md` step 7"* marker so it stops reading as a live
  second statement. **It is a historical record: the marker is the fix, not
  a rewrite.**

### D. The three open step-7 advisories

1. The content-witness branch prescribes a **before** run with no stated
   disposition. State it: what the before run is for, and that a **red**
   before run is expected input to the ship, never a stop — it is the
   reason the deploy is happening.
2. *"Why the checkout stands in for what was merged"* rests on step 3,
   which ran **before** step 6. State the caveat and its remedy: a deploy
   command that writes into the repo's own payload paths breaks the
   equivalence, so re-confirm step 3's scoped cleanliness after step 6
   before the after run is trusted.
3. The *"readable but neither"* branch is a permanent stop with no remedy.
   Give it the shape step 6's harness-refusal path already has — rows stay
   `MERGED (deploy pending)`, and the Owner is told the remedy is to
   document a deploy-evidence witness in the project's own `CLAUDE.md` and
   re-run. **Never an override, never a substituted check:** that
   trained-to-override behaviour is the defect this incident opened over.

## Binding constraints

1. **IC DIRECTIVE (ii) — the line ceiling.** `deploy.md` is at exactly
   **265** lines. Pay for D's additions by compressing step 4's shape
   branches into citations of step 7 where the disposition is genuinely
   the same — that compression *is* the one-statement-per-file fix, not a
   tax. **If honest compression cannot fit them, you are pre-authorised to
   overrun to AT MOST 275 lines, every line past 265 inside step 7's
   disposition section**, with the final count and the justification in
   your return. **The deliberate step-4 / step-7 asymmetry for the "cannot
   check" case is a PROTECTED element** — step 4 treats an unreadable
   marker as "unshipped, include it", step 7 stops, and step 7 says
   plainly that this is deliberately stricter. Any pressure to delete it,
   or any need beyond 275 lines, is a **deviation to the IC**, never your
   judgment call.
2. **`deploy.md` stays project-agnostic** — it never names
   `tests/payload_check.py`, `~/.claude`, or `dcs/VERSION`. This-repo
   specifics live in `CLAUDE.md` only.
3. **Encoding** — the merge guard's check 8 walks the whole repo for BOM
   and U+FFFD, checks 9 and 10 scope to `SHIPPED_DIRS`. Use the Write/Edit
   tools, never PowerShell `Set-Content`/`Out-File`; a BOM has broken a
   hash comparison in this repo twice.
4. **IC open question, carried verbatim:** if your role-shaped walk finds
   the contract needs a statement in `dcs/references/doctrine.md` or
   `schemas.md` (the hot path, **1,205 B** of spare against the 37 kB
   ratchet), that is **a scope change to escalate at proposal time, not an
   edit.** Raise it as a deviation.

## File territory (may edit ONLY these)

`dcs/workflows/deploy.md` · `dcs/workflows/close.md` ·
`dcs/templates/REGISTER.md` · `skills/dcs-deploy/SKILL.md` · `CLAUDE.md` ·
`docs/spec-v0.3-parallel.md`

## Forbidden zones

`tests/**` · `CHANGELOG.md` · `install.ps1` · `install.sh` ·
`package.json` · `dcs/VERSION` · `bin/**` · `dcs/references/**` ·
`agents/**` · `.dcs/**`

**Do NOT run `install.ps1` / `install.sh`, no deploy** — `CLAUDE.md`
forbids installing while an incident is active.

## Evidence required in the return

1. **Criterion 5, the full walk.** Paste the complete output of the
   enumerator at **end state**, with **every** hit annotated `changed` or
   `deliberately correct as written because <reason>`.
2. **Criterion 5a, the negative control.** Run **both** enumerators at end
   state; paste both outputs and `| wc -l` for each. The new one must
   return `dcs/templates/REGISTER.md`'s facts-only region and the old must
   not. Baseline at plan time: old **4**, new **18 in 6 files**.
3. **Criterion 10, per-file census.** For **every** file in your
   territory, paste each declaring paragraph in full. Outside `deploy.md`
   there must be **at most one per file**, each containing the literal
   citation `` `dcs/workflows/deploy.md` step 7 ``.
4. ``grep -rn '`dcs/workflows/deploy.md` step' dcs/ skills/ CLAUDE.md docs/``
   — the citation census S2-GUARD's population must match.
5. `wc -l dcs/workflows/deploy.md` — ≤ 265, or ≤ 275 with justification.
6. `grep -nE 'payload_check|~/\.claude|dcs/VERSION' dcs/workflows/deploy.md`
   — must return nothing.
7. `python tests/test_doctrine_integrity.py` — the final `N/M passed` line
   **and the exit code** (73/73 at plan time; checks 4, 5, 6, 13 and 14 all
   read files you are editing). The module `sys.exit()`s at file scope with
   no runner, so an exception mid-file prints accumulated PASS lines then a
   traceback — **the count and the exit code together, never a list of PASS
   lines.**
8. `python tests/test_dcs_gate.py` and `python tests/test_dcs_intake.py` —
   each suite's own `N/M passed` line.
9. `git diff --stat` and `git status --short` at end state, proving nothing
   outside territory moved.

## On discovering the plan doesn't fit reality

STOP. Return `status: "deviation"` per `schemas.md` #4 with `found`,
`why_plan_wrong`, `proposal`.
