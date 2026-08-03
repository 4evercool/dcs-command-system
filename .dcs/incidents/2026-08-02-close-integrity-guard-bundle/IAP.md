<!--
IAP.md -- the Integrated Action Plan, written by the IC during /dcs-plan.
This is the ONLY document specialists execute against once approved.
Editing this file after approval voids IAP-APPROVED automatically (hash
mismatch) -- deliberate, not a bug to route around. RE-ISSUED for period
1, attempt 2, after a Safety Officer halt routed to replan (not a
pre-execution command-point reject like the prior revision) -- see
"Deviation history" below.
-->

# IAP — Incident Action Plan

**Incident:** close-integrity-guard-bundle
**Type:** 1
**Operational period:** 1 (attempt 2)
**Links:** `202-OBJECTIVES.md` · `203-ORG.md` · `204-TASKING/*.md` · logistics plan below (attempt 1, unaffected)

## Objectives (summary of 202)

**Goal:** DCS's close-time process mechanically enforces, for every project shipping DCS, the universal record-integrity properties of an incident's own artifacts — commit-SHA existence, artifact-set completeness, `SAFETY.md` schema conformance, a clean tree after the archive commit, non-degenerate commit messages — running unconditionally, not opt-in, **with a real, append-only-compatible remedy for a legitimate record about the mechanism itself** (added this attempt — the gap the halt found). Separately, DCS's own package content stays English-only and retains its load-bearing operative terms, enforced as this repo's own policy, never forced onto downstream projects.

**What changed this attempt** (full criteria text: `202-OBJECTIVES.md`): criterion 1(b) — suppression redesigned as a real, grammar-recognized, target-naming `RECORD-CORRECTION:` entry mechanism (fixes both halt defects: a mid-line mention no longer suppresses; a named correction clears every occurrence of that token in the file, not just its own restatement). Criterion 3 — date pin corrected to the literal value `"2026-08-02"` with strict-greater-than (fixes an off-by-one-day bug), and `SAFETY.md` fence-field validation scoped to verdict-shaped fences only. Criterion 6 — the load-bearing-term census excludes its own defining file from the population it checks and adds `CLAUDE.md` as a real citing site (fixes the tautology). Criterion 13 — a new fixture pair proves the corrected suppression works both ways. Criterion 14 — the IC's self-application procedure now has a real remedy step (append a correction, rerun, confirm genuine exit 0) instead of discovering an unfixable block.

**Unchanged, already satisfied, not re-tasked:** criteria 2, 4, 5, 7, 8 (S1's original work, untouched by this attempt's fixes); criteria 9, 10, 11, 12, 15 (S3/S4's attempt-1 work — doctrine principle 16, forms.md's artifact count, close.md's step 5a.1b wiring, the 0.8.0 version bump, the register territory refinement).

## Tactics (from the Planning Chief, attempt-2 return)

- **T1** — Recognize the correction sentinel exactly as `dcs_gate.py` recognizes its own three (built by concatenation from the imported `ENTRY_PREFIX`, matched only against an entry's first line — never re-derived, never a body-anywhere test).
- **T2** — Suppression (b) becomes a two-pass, file-scoped rule: pass 1 collects every genuine correction entry's named target tokens; pass 2 screens citations against that set. This is what makes "clears every occurrence in the file" a one-line consequence rather than a redesign.
- **T3** — Split criterion 3's fence-field validation into a pure comparator + IO collector, mirroring criteria 4/5's existing split — the only way "non-verdict fence = printed note" is testable, since no real file on disk has one.
- **T4** — The finding text itself must state the `RECORD-CORRECTION:` remedy and its required shape — the practical fix for the undocumented-convention gap the halt exposed, delivered on the one surface a blocked operator actually sees, inside S1's own territory (no `forms.md` reopening).
- **T5** — Prove both fixed defects on immutable REAL corpus data, not only fixtures: `halt-enumeration-grammar-drift/214-LOG.md:37-38` for the "corrected original stays flagged" defect (must invert to 0 findings, both suppressed); this incident's own `214-LOG.md:39` for the "mid-line mention suppresses" defect (must invert to a genuine finding).
- **T6** — Kill the census tautology by PATH-IDENTITY exclusion of the census's own defining file (not name-matching, which one refactor could re-break), then add `CLAUDE.md`, then prove non-vacuity, then curate the term list honestly against measurement.
- **T7** — Regenerate every derived fact this change invalidates (the tool's docstring "measured facts" block, the "suppression fires once" claim, the "drop `sha`" remedy suggestion) — principle 15, write the derivation beside the new numbers.

## File-territory partition (attempt 2 — 2 specialists)

| Specialist | Territory | Forbidden |
|---|---|---|
| S1 | `dcs/tools/record_integrity.py` | `tests/**`, `dcs/hooks/**`, `dcs/references/**`, `dcs/workflows/**`, `dcs/templates/**`, `dcs/README.md`, `dcs/VERSION`, `agents/**`, `skills/**`, `docs/**`, `bin/**`, `install.ps1`, `install.sh`, `package.json`, `CHANGELOG.md`, `README.md`, `CLAUDE.md`, `vault/**`, `.dcs/**` |
| S2 | `tests/test_doctrine_integrity.py`, `tests/fixtures/record-integrity/**` | `dcs/**`, other test files, `agents/**`, `skills/**`, `docs/**`, `bin/**`, installers, `package.json`, `CHANGELOG.md`, `README.md`, `CLAUDE.md`, `vault/**`, `.dcs/**` |

**Partition status:** disjoint — but **sequential execution**: S1 runs first and its return is validated before S2 is spawned (S2 hard-reads S1's finding/suppression-line output formats; this shared worktree already produced one real concurrent-snapshot confusion in attempt 1). S3 and S4 are not re-tasked this attempt.

## Deploy / environment plan (Type 1, from the Logistics Chief — attempt 1, unaffected, not re-solicited)

Unchanged from attempt 1: full payload install via `install.ps1`/`install.sh` after `/dcs-close`, never during. Stdlib-only, no new deps, no env vars, no `.dcs/config.json` opt-out. No migration. Simple-revert rollback, no kill-switch (reasoned from doctrine principle 11's own shape). Version 0.8.0 already bumped (S4, attempt 1). Verified at this attempt's command point 2 that neither fixed defect touches deploy path, env/deps, migration ordering, or rollback — no re-solicitation needed.

## Risks

- S2 has a hard read-dependency on S1's finding-line/suppression-line output formats — not a partition violation, but the reason for sequential (not parallel) execution this attempt.
- Shared, non-isolated worktree: a test run taken mid-write by either specialist can show a snapshot that is neither the old nor new behavior — the Safety Officer's integrated re-run is the authority.
- The corrected term census goes red unless `HOT_PATH_BUDGET_KB` is re-curated (S2's own territory: replace with `WORKFLOW_GRANDFATHERED_LINES`, genuinely cited by `CLAUDE.md`, or drop) — re-verified independently at command point 2.
- Deliberate widening of criterion 1(b)(ii) from "anywhere earlier" to "anywhere in the file" — ratified at command point 2 as a strict superset with an unchanged trust model; bound for the Safety Officer: suppression must stay token-scoped to a correction's named targets, never sweep in an unrelated genuine citation on the same line pattern (probe: `halt-enumeration-grammar-drift/214-LOG.md:36`'s separate `integration commit 48ea59a` must still resolve as a commit).
- Criterion 14 cannot reach a genuine exit 0 before the close-time artifact-set commit (criteria 2/4 legitimately fire on the still-untracked incident directory) — sequence the IC's hand-run after that commit, not before.
- `AAR.md` has no suppression path by design (not append-only, unlike `214-LOG.md`) — any future `sha <hex>`-shaped false positive there is fixable only by rewording.
- The boundary fixture (dated `2026-08-03`) must live under `tests/fixtures/record-integrity/`, never `.dcs/incidents/`, or it would silently pollute check 9's and section 23's other measured counts.
- Stale derived facts in the shipped docstring are the exact defect class this incident exists to close — S1 must regenerate them with the command beside the numbers (principle 15).
- The `RECORD-CORRECTION:` convention remains undocumented in shipped prose (`forms.md`) — ruled a follow-up to register at close, not a third tasking, since T4 already puts the remedy where an operator actually encounters it.

## Verification plan

Four things holding at once, checked by the Safety Officer in this order:

1. **The original 201 repro path, inverted on real data.** `halt-enumeration-grammar-drift` must go from 1 finding to 0 findings (both `:37` and `:38` suppressed, naming each other). This incident's own `214-LOG.md:39` must go from suppressed-by-accident to a genuine finding. `record-integrity-corrections` must still exit 0.
2. **All three suites green together, from one run taken after both specialists' last write** — not either specialist's own snapshot.
3. **Non-vacuity of every new/changed check, demonstrated in the failing direction** — the term census must flag a synthetic absent term; the fixture pair must show the uncorrected half red and the corrected half clean on criterion 1; the boundary fixture must be in-scope and flagged while the pin date itself stays out; the non-verdict fence comparator must return findings only for a bad verdict-shaped object, nothing for a non-verdict one.
4. **The pins and populations did not move silently.** Both date constants read literally `"2026-08-02"` with strict greater-than scoping; the printed in-scope/excluded counts are identical before and after (a measured no-op today).

**Manual check for the IC, not the specialists (criterion 14):** after appending the `RECORD-CORRECTION:` entry naming `3df43fc8` and after the close-time artifact-set commit, run the tool by hand against this incident's own directory and confirm a genuine exit 0. The incident does not close over a recorded exit 1 from its own gate.

**Declared gap, not hidden:** nothing in this plan documents the `RECORD-CORRECTION:` convention in shipped prose — the remedy lives only in the tool's own finding text (T4). Queued as a follow-up register row at close.

## Deviation history (this period)

**Attempt 1 → attempt 2, halt-routed replan (not a pre-execution reject):** period 1 was fully planned, approved, and executed (S1-S4 all `status: "done"`). The Safety Officer halted on two refutations — see `SAFETY.md` (attempt 1's verdict) and `214-LOG.md`'s `SAFETY-HALT:` entry for full detail. `dcs-commander` ruled `replan` at `verdict_disposition` (not `fix_taskings`), since the fix revises Owner-facing 202 content. The Owner confirmed the revised `202-OBJECTIVES.md`. A re-spawned Planning Chief produced this attempt's 2-tasking plan (S1, S2 only — S3/S4's attempt-1 work confirmed unaffected and not re-tasked), accepted at a second command-point-2 pass. Full chronology: `214-LOG.md`.
