<!--
IAP.md -- the Integrated Action Plan, written by the IC during /dcs-plan.
This is the ONLY document specialists execute against once approved -- the
single source of truth doctrine principle 3 insists on. Editing this file
after approval voids IAP-APPROVED automatically (hash mismatch) -- that is
deliberate, not a bug to route around.
-->

# IAP — Incident Action Plan

**Incident:** decomposition-backlog-routing
**Type:** 3
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `204-TASKING/S1.md` · `204-TASKING/S2.md`
(`203-ORG.md` skipped — default Type 3 activation: 2 specialists match 2
taskings, plain parallel execution, no Logistics Chief)

## Objectives (summary of 202)

**Goal:** A defect a stem decomposes, or new intake an ESG sweep finds,
that falls below a concrete, mechanically-followable priority/triviality
bar is routed to a lighter-weight, project-documented surface instead of
automatically becoming a first-class `REGISTER.md` row. A project whose
`CLAUDE.md` documents no such surface keeps today's unconditional
behavior unchanged.

**Acceptance criteria:**

1. `new.md` step 4a states a concrete, mechanically-followable bar; below
   it, and only when the project's `CLAUDE.md` documents a lightweight
   surface, route there instead of a register row; otherwise unchanged,
   and the surface is never hardcoded.
2. `esg.md` step 2's decision clusters gain the mirror disposition for
   cluster (b), same bar, same fallback.
3. `doctrine.md` principle 4 is amended in place (parenthetical version
   note) to state the bar as a standing rule — an amendment, not a new
   principle; numbering/count unchanged.
4. `test_doctrine_integrity.py`, `test_dcs_gate.py`, and
   `test_dcs_intake.py` each still report a fully green run.

## Tactics (from the Planning Chief)

- **T1:** Key the bar on the register template's own lowest priority tier
  (`L`), not a type/shape test — verified against the incident's own
  three live-symptom rows, all priority `L` at Type 3/unset, so a
  shape-based bar would have caught none of them. `L` is package
  vocabulary (`dcs/templates/REGISTER.md`), not a project fact.
- **T2:** Have `new.md` step 4a assign a proposed Priority (`H`/`M`/`L`)
  before applying the bar — neither `new.md` nor `esg.md` currently makes
  this assignment explicit at the stem; without it the bar is
  unfollowable.
- **T3:** Cite the project-surface lookup using this repo's established
  citation shape (`doctrine's "Relationship to project-specific
  protocols"`), matching `esg.md`'s own existing precedent (line 41) and
  verified against the integrity suite's citation-resolution check.
- **T4:** Treat both edits as budget-constrained: `new.md` capped at +7
  lines (242/250, not grandfathered), `doctrine.md` capped at +350 bytes
  of the hot-path's 430-byte headroom (37,458/37,888 joint with
  `schemas.md`), measured by the guard's own counting method.
- **T5:** Confine the `esg.md` edit to step 2 cluster (b) only — step 3
  is already generic over clusters, and step 4's Record bullets belong to
  the separately-registered `esg-intake-writeback-gap`.
- **T6:** Fix the exact bar wording and tier name once, centrally, so
  both specialists carry identical prose — divergence would leave the
  constitution (which wins on conflict) disagreeing with the workflows.

## File-territory partition

| Specialist | Territory | Forbidden |
|---|---|---|
| S1 | `dcs/references/doctrine.md`, `dcs/workflows/new.md` | `dcs/workflows/esg.md`, `dcs/references/schemas.md`, `dcs/references/doctrine-appendix.md`, `dcs/VERSION`, `package.json`, `tests/**`, `dcs/templates/**`, `dcs/hooks/**`, `agents/**`, `skills/**`, `vault/**`, `.dcs/**`, `install.ps1`, `install.sh`, `C:/Users/4ever/.claude/**` |
| S2 | `dcs/workflows/esg.md` | `dcs/workflows/new.md`, `dcs/references/doctrine.md`, `dcs/references/schemas.md`, `dcs/VERSION`, `package.json`, `tests/**`, `dcs/templates/**`, `dcs/hooks/**`, `agents/**`, `skills/**`, `vault/**`, `.dcs/**`, `install.ps1`, `install.sh`, `C:/Users/4ever/.claude/**` |

**Partition status:** disjoint — parallel execution. Verified at both
specialist level (no shared file, each forbids the other's territory)
and portfolio level (this incident is the only `ACTIVE` register row; the
`QUEUED` `esg-intake-writeback-gap` row shares `esg.md` but does not
lock, and its lines — step 4's Record bullet, `esg.md:106` — sit outside
S2's confinement to step 2 cluster (b) at `esg.md:67`).

## Risks

- **Hot-path byte budget (tightest):** `doctrine.md` + `schemas.md`
  stand at 37,458 of 37,888 normalised bytes — 430 bytes of headroom for
  the whole incident. Mitigated by capping S1 at +350 bytes and requiring
  the measured number in evidence. If the bar genuinely cannot fit, the
  correct move is a deviation, not trimming `schemas.md` or the appendix.
- **`new.md` line budget (second-tightest):** 242 of 250, not
  grandfathered. Draft is +6; cap is +7. Compressing prose inside step
  4a's first bullet is authorised; compressing anything else in `new.md`
  is out of scope and must be a deviation.
- **Wording divergence across three files:** because the constitution
  wins on conflict, a bar stated one way in `doctrine.md` and another in
  `esg.md` is worse than no bar. Mitigated centrally (T6); the Safety
  Officer should read the three hunks side by side.
- **Version-label forward reference:** `(v0.6.13)` is written while
  `dcs/VERSION`/`package.json` say `0.6.12`; the bump happens at close,
  outside every territory here. Nothing mechanical binds it. **IC ruling
  (command point 2):** confirmed as the correct label given the
  one-patch-bump-per-incident pattern and no other incident active;
  close must sync `VERSION`/`package.json` to exactly `0.6.13`, or
  correct the label in the same pre-merge act if the Owner directs a
  different version.
- **Known, deliberate incompleteness:** `esg.md` step 4's Record bullet
  still won't write back a register row for cluster (b) after this
  incident — that is `esg-intake-writeback-gap`, separately registered
  and explicitly out of scope. The Safety Officer should not halt on
  this pre-existing, out-of-scope gap.
- **Bar only bites where a priority is assigned:** T2's assignment clause
  in S1 is mandatory, not optional trim — dropping it for line budget
  would make the bar unfollowable even though the file still compiles.
- **Numeric-rank registers:** a project whose register ranks numerically
  rather than `H`/`M`/`L` has no literal `L` to match; it falls back to
  today's unconditional behavior by construction — safe, flagged rather
  than fixed, worth a Backlog row at close rather than hot-path prose now.
- **Restoring "defects" in `doctrine.md` principle 4 (line 55) alongside
  the amendment:** a pre-existing missing-object defect in the exact
  sentence being amended. **IC ruling (command point 2):** in scope — it
  sits inside the sentence criterion 3 already rewrites, was carried into
  planning by the stem's own command-point-1 directive, and is declared
  here rather than smuggled in.

## Verification plan

1. Re-walk the 201 repro path on the amended text for a synthetic `H`
   defect and a synthetic `L` defect, both with and without a documented
   project surface — the outcome must be decidable from the text alone,
   no reader judgment call.
2. Repeat for the `esg.md` sweep side (cluster (b) plus step 3).
3. Read all three hunks side by side: identical tier (`L`), identical
   condition (`CLAUDE.md` documents a surface), identical fallback
   (unconditional row). Divergent wording is a defect even if tests pass.
4. Full suite, fresh: `python tests/test_doctrine_integrity.py`
   (baseline 86/86), `python tests/test_dcs_gate.py`, `python
   tests/test_dcs_intake.py`.
5. Budgets, measured not assumed: hot-path bytes <= 37,888 (baseline
   37,458); `new.md` <= 250 (baseline 242); `esg.md` <= 250 (baseline
   152) — counted with the guard's own method, not `wc -l`.
6. Ship-no-project-facts audit across the whole diff: `git diff --
   dcs/ | grep -i "vault\|backlog.md\|C:\\DCS"` must return nothing.
7. Constitution integrity: principle count/numbering unchanged (check 2
   PASS), no principle added, principle 4 still principle 4.
8. Scope containment on `esg.md`: hunk headers confirm no edit to step 3
   or step 4, so `esg-intake-writeback-gap`'s lines are untouched.
9. Not part of verification: running `install.ps1` or `payload_check.py`
   — installing mid-incident is a HARD RULE violation; deploy is a
   post-close act.

## Deviation history (this period)

none
