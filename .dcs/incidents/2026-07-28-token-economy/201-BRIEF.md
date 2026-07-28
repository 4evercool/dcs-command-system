# 201 — Incident Brief

**Incident:** token-economy
**Opened:** 2026-07-28
**Type:** 1

## Symptom

DCS spends more of its own token budget than it needs to, across six
independent mechanisms with six independent root causes. **This brief
deliberately covers all six** — doctrine principle 4 (one incident, one
defect) and this stem's own decomposition check (`new.md` step 4a) would
otherwise have split them into separate incidents, and the stem did
originally propose opening only the first. The Owner explicitly directed
combining them into one Type 1 incident, overriding that default; the
override and its reasoning are recorded in `.dcs/esg/REGISTER.md`'s
`token-economy` row and Notes section, and repeated here so this file
alone remains sufficient after a context reset (principle 5).

1. **Automation-layer eager reading.** `dcs/workflows/run.md` and
   `dcs/workflows/loop.md` each `@`-include the full text of every phase
   workflow file they may invoke, rather than the slice needed for the
   phase actually about to run. `run.md`'s block front-loads at least
   111,725 B before its own `<process>` begins (see Evidence — this
   number grew 18% since the stem opened, from an unrelated incident's
   growth of one nested file). Since `/dcs-loop` cycles `/dcs-run --next`
   unattended over every `QUEUED` register row, this repeats on every
   incident the sweep touches.

2. **Incomplete `214-LOG.md` read-scoping.** No per-entry length guard
   exists anywhere (371-entry sample across 7 closed incidents: median
   413 chars, p90 951, max 2,318). The one scoping convention that exists
   (v0.5.1, "current period + last ~20 lines") is wired into a single
   call site (`execute.md`'s `verdict_disposition` commander spawn)
   while other documented and observed read paths — `plan.md`'s and
   `execute.md`'s own command-chain checks, the Safety Officer's own
   read, and "a fresh session reads it in full to resume" per the
   template's own header — are not scoped by it.

3. **ESG artifact bloat.** `REGISTER.md` + `STRATEGY.md`, read in full at
   brief-authoring time and every territory check, now total 177,654 B
   (117,943 + 59,711) — **past** the 167 KB (170,988 B) benchmark from a
   sister project that motivated this item, up from 99.2% three days ago.
   Honest caveat: roughly 8 KB of the current `REGISTER.md` figure is
   this very stem's own bookkeeping (the `token-economy` row itself, the
   territory-conflict note, three fold notes) — the file was 169,571 B
   immediately before this stem began writing to it. The underlying
   growth trend predates and is independent of that, and three prior ESG
   sessions already deferred acting on it while watching the same number
   climb.

4. **Redundant full Safety re-verification.** Every fresh Safety Officer
   spawn re-derives all acceptance criteria and re-runs the full
   verification suite from scratch, even when a prior spawn in the same
   period just did so (doctrine principle 9b requires the fresh spawn;
   nothing requires the full re-derivation). A live, byte-measured
   instance: `register-field-repair-path`'s `SAFETY.md` reached 21,415 B
   from 3 Safety Officer spawns in one period.

5. **`doctrine.md` reloaded once per phase within a single incident.**
   Across one ordinary lifecycle (stem→plan→execute→close as four
   separate command invocations), the four phase workflows' own
   `required_reading` blocks sum to 152,064 B, of which `doctrine.md`
   alone contributes 95,492 B (62.8%), reloaded four times with no
   documented convention for a later phase to treat it as already loaded.
   **Named caveat, carried from `vault/Backlog.md` item 20 and not
   resolved by opening this incident:** the repeated read may be
   load-bearing for doctrine principle 5's context-reset resilience
   guarantee ("any session, even after a full reset, resumes losslessly
   by reading the files"). A fix here must prove it distinguishes "same
   session, no reset occurred" from "fresh spawn, possibly post-reset" —
   or it trades resilience for token savings rather than removing genuine
   waste. The Planning Chief inherits this as a hard verification
   requirement, not a suggestion.

6. **Unbounded verbatim-evidence fields.** `dcs/references/schemas.md`
   fields explicitly required to carry real/unparaphrased output
   (`evidence` #4, `checked`/`refutations`/`advisories` #5,
   `evidence_required` #2 on the tasking object) have no stated ceiling
   anywhere — schemas.md, the three governing charters
   (`dcs-ops-specialist.md`, `dcs-safety-officer.md`,
   `dcs-planning-chief.md`), and `dcs/templates/204-TASKING.md` all model
   "full output" as the default with no trimmed alternative offered. By
   contrast every field at genuine risk of brevity already carries an
   explicit bound (`summary`: "one paragraph"; `rationale`: "one line").
   Sampling found this asymmetry real but **not**, on the evidence
   gathered, currently producing much actual waste — agents already tend
   to cite only the decisive excerpt rather than pasting full transcripts
   (see Evidence) — so the fix is closing a structural gap pre-emptively,
   not correcting an observed pattern of abuse.

## Evidence

**Item 1 — automation-layer eager reading:**
- `dcs/workflows/run.md:13-17` `<required_reading>`: `doctrine.md` (23,873)
  + `new.md` (12,561) + `plan.md` (37,634) + `execute.md` (22,883) +
  `close.md` (14,774) = **111,725 B**. Re-measured 2026-07-28 post-merge
  of `deviation-path-proportionality`; was 94,566 B at stem open three
  days earlier — the 18% growth is entirely `plan.md`'s (22,996 → 37,634
  B, +64%, from that unrelated incident adding `## 6c.`, a 216-line
  section), illustrating the risk directly: `run.md`'s up-front cost
  moves whenever *any* nested file changes, for reasons unrelated to
  `run.md` itself. (`wc -c` on each file, 2026-07-28)
- `dcs/workflows/loop.md:10-11` `<required_reading>`: `doctrine.md`
  (23,873) + `run.md` (8,616) = **32,489 B** single-level; larger if
  `@`-resolution is recursive (open question, unresolved — see Type +
  rationale).
- `grep -rn required_reading agents/` → no matches (0 of 6 agent
  charters); `grep -rn "@\$HOME|@dcs/references" agents/` → no matches
  either — the eager-load pattern is confined to the automation layer,
  not a general "every spawn reads doctrine" design this item would cut
  against.
- `dcs/workflows/close.md` spawns no subagents (`grep -in
  'via Task|spawn' close.md` → no matches) — confirms territory here is
  the two automation-layer files only.

**Item 2 — `214-LOG.md` read-scoping:**
- 371-entry distribution across 7 closed incidents (min 52, p25 254,
  median 413, p75 610, p90 951, max 2,318 chars) — new max
  `.dcs/incidents/2026-07-27-register-field-repair-path/214-LOG.md:39`.
- `dcs/workflows/execute.md`'s `verdict_disposition` spawn is the one
  scoped call site ("scoped, v0.5.1: entries for the CURRENT period plus
  the last ~20 lines — never the whole file"); `plan.md`'s and
  `execute.md`'s own command-chain-check reads carry no such bound.
- `.dcs/incidents/2026-07-27-register-field-repair-path/SAFETY.md:141`:
  a Safety Officer verdict's `checked[]` states "Read 214-LOG.md in full
  — both 17:55:39 entries inspected" — a live, direct instance of the
  unbounded path, independent of and in addition to the bounded
  `/dcs-status` tail.

**Item 3 — ESG artifact bloat:**
- `wc -c .dcs/esg/REGISTER.md .dcs/esg/STRATEGY.md` → 117,943 + 59,711 =
  **177,654 B**, 2026-07-28, post-stem-bookkeeping. 167 KB benchmark =
  170,988 B — now exceeded. Pre-stem-bookkeeping figure (measured at stem
  open, before this incident's own register edits): 109,860 + 59,711 =
  169,571 B, 99.2%. Growth history per `.dcs/esg/STRATEGY.md`'s Ranked
  priorities §8: 77% → 95% → 99.2% → (now) 103.9%, deferred three
  consecutive `/dcs-esg` sessions.

**Item 4 — redundant Safety re-verification:**
- `.dcs/incidents/2026-07-27-register-field-repair-path/SAFETY.md`:
  21,415 B, 3 verdict blocks (2 halt + 1 pass) in one period, each
  independently re-running the full 3-suite verification and full `git
  diff` read — the row's own header names the cause.

**Item 5 — `doctrine.md` per-phase reread:**
- Fresh 2026-07-28 sums (post-merge): `new.md` required_reading =
  doctrine (23,873) + typing (4,774) + schemas (13,296) = 41,943 B;
  `plan.md` = doctrine + schemas + forms (5,955) = 43,124 B; `execute.md`
  = doctrine + schemas = 37,169 B; `close.md` = doctrine + forms =
  29,828 B. Sum = **152,064 B**, `doctrine.md`'s share = 23,873 × 4 =
  95,492 B (**62.8%**).
- Hot path itself remains healthy and mechanically guarded: doctrine +
  schemas = 37,169 B against the 37 KB (37,888 B) ratchet in
  `tests/test_doctrine_integrity.py` (`HOT_PATH_BUDGET_KB = 37`) — 719 B
  slack, down from 1,205 B three days ago, still positive. This item is
  about re-read *frequency*, not size; size has its own working guard
  and is explicitly not broken.

**Item 6 — unbounded verbatim-evidence fields:**
- `dcs/references/schemas.md` line 75 (`evidence`, #4): "Real output, not
  a paraphrase"; line 102 (`checked`, #5): "Everything the Safety Officer
  actually did"; `dcs/templates/204-TASKING.md` `evidence_required` (#2):
  "Concrete command(s) whose real output the specialist must include" —
  none states a maximum. Contrast: `summary` (#1, line 17) "One
  paragraph, no hedging"; `rationale`/`directives` (#6, lines 124-125)
  "One line" / "Concrete, one line each."
- Ground-truth check against the actual practice: `python
  tests/test_doctrine_integrity.py` produces 8,202 characters / 84 lines
  of real output; every sampled `checked[]`/`evidence` citation of this
  exact command quotes only its 13-character final summary line or 2-3
  named PASS lines — no sampled artifact pastes the full transcript. The
  restraint already happens by convention; the gap is that no rule
  requires it, so nothing prevents the opposite.

## Reproduction path

Not a behavioral bug across all six items — measured static-loading and
schema-completeness patterns. Regenerate per item:

1. Item 1: `wc -c` the five files `run.md` nests, sum; same for `loop.md`.
2. Item 2: the sampling script and method are recorded in the prior
   situation-analyst return (this incident's own 214-LOG will cite it at
   the relevant tasking).
3. Item 3: `wc -c .dcs/esg/REGISTER.md .dcs/esg/STRATEGY.md`.
4. Item 4: `wc -c` any closed incident's `SAFETY.md`; count `"verdict":`
   occurrences for spawn count.
5. Item 5: `wc -c` each phase workflow's own named `@`-includes, sum per
   phase, then across the four-phase lifecycle.
6. Item 6: `grep -niE "verbos|concise|terse|paraphrase|paste|full output|
   unabridged|one line|one paragraph" agents/dcs-*.md
   dcs/references/schemas.md`.

## Blast radius (best guess at intake)

**Estimate, union of six items — not yet territory-checked against an IAP
partition, refined at `/dcs-plan`:**

- `dcs/workflows/run.md`, `dcs/workflows/loop.md` (item 1)
- `dcs/templates/214-LOG.md`, `dcs/workflows/plan.md`,
  `dcs/workflows/execute.md`, `agents/dcs-safety-officer.md` (item 2)
- `dcs/workflows/esg.md`, `dcs/templates/REGISTER.md`,
  `dcs/templates/STRATEGY.md` (item 3)
- `agents/dcs-safety-officer.md`, `dcs/workflows/execute.md`,
  `dcs/references/doctrine.md` (item 4)
- `dcs/workflows/new.md`, `dcs/workflows/plan.md`,
  `dcs/workflows/execute.md`, `dcs/workflows/close.md`,
  `dcs/references/doctrine.md` (item 5)
- `dcs/references/schemas.md`, `agents/dcs-ops-specialist.md`,
  `agents/dcs-safety-officer.md`, `agents/dcs-planning-chief.md`,
  `dcs/templates/204-TASKING.md` (item 6)

Deduplicated union: `dcs/workflows/{run,loop,new,plan,execute,close,esg}.md`,
`dcs/templates/{214-LOG,204-TASKING,REGISTER,STRATEGY}.md`,
`agents/dcs-{safety-officer,ops-specialist,planning-chief}.md`,
`dcs/references/{doctrine,schemas}.md` — **15 files.** The Planning Chief
partitions this into disjoint per-specialist territory; six items sharing
15 files means the partition is the load-bearing design decision for this
incident's safety, not an afterthought (doctrine principle 6).

Explicitly **not** touched by any item: `dcs/hooks/dcs_gate.py`,
`tests/test_dcs_gate.py`, `install.ps1`, `install.sh`, `package.json`,
`dcs/VERSION` — no item's fix requires the enforcement mechanism or the
release surface.

## Prior art

**This intake decomposed into six independent items at this stem
(`new.md` step 4a).** The stem originally proposed opening only item 1
(`automation-layer-eager-reading`) as a narrow Type 3, with items 3 and 4
staying in the register as already-queued rows (`esg-artifact-bloat` rank
8, `safety-officer-incremental-verify` rank 7), item 5 filed to
`vault/Backlog.md` item 20 without queueing (principle-5 tension), and
item 2 (`log-read-scoping-incomplete`) newly split out and queued
separately. `dcs-commander` (fable) endorsed that narrower framing at
command point 1, Type 3.

**The Owner then explicitly overrode both decisions**: combine all
token-economy items into one incident (overriding principle 4's default),
and Type 1 instead of the commander's proposed Type 3. A second recon
pass (situation analyst) supplied item 6, which had no prior register or
backlog presence. Items 2, 3 and 4's register rows were folded into this
one (`KILLED`, "not abandoned — evidence moves with it", matching the
package's existing fold convention, e.g. `charter-schema-agreement` →
`schemas-contract-format`).

**A territory conflict then deferred opening for one operational period.**
This incident's estimated territory overlapped `doctrine.md`, `plan.md`
and `execute.md` with the then-`ACTIVE` `deviation-path-proportionality`,
which was mid-execution (one Safety halt already spent, fix-tasking just
returned). Doctrine's v0.3 territory-partition rule refused a worktree by
default; the Owner chose to wait rather than override or narrow.
`deviation-path-proportionality` has since closed and deployed (merge
`f62938b`, `/dcs-deploy` verified) — this incident opens now that the
conflict is gone, per that same decision.

**No prior incident examined any of these six mechanisms directly.** The
closest, `doctrine-hot-path-trim`, addressed `doctrine.md`'s absolute
size, not read frequency (item 5) or nesting (item 1); its AAR and
`doctrine-appendix.md` grepped for `run.md|loop.md` return no matches.

Source for all figures: direct `wc -c`/`grep` measurement, 2026-07-28,
post-merge of `deviation-path-proportionality` — cited inline per item
above rather than collected here, per doctrine principle 15.

## Type + rationale

**Proposed type:** 1
**Rationale:** Six independent root causes bundled by explicit Owner
override of doctrine principle 4's one-incident-one-defect default (see
Prior art). `dcs-commander` (fable) had proposed Type 3 for the
originally-scoped single item; the Owner's combine-and-elevate decision
was not re-submitted to a fresh commander typing pass, since typing.md
reserves the Owner's confirmation as final ("the IC proposes, the Owner
decides") and a materially wider scope only strengthens the case for
Type 1's ceremony, never weakens it. Full org activation (Planning Chief
+ Logistics Chief + up to 4 specialists + Safety Officer) is warranted by
the territory alone: 15 files, three of them (`doctrine.md`, `plan.md`,
`execute.md`) touching DCS's own enforcement-adjacent core, six
independent tactics to partition without collision.
**Owner confirmation:** Confirmed via `AskUserQuestion`, 2026-07-28 —
Type 1 selected directly as an override, not proposed-then-accepted.

**Carried forward for `/dcs-plan`, not yet resolved:**
1. Whether `@`-include resolution is single-level or recursive (affects
   item 1's `loop.md` magnitude, not its direction or type).
2. Item 1 and item 5 both require the verification plan to prove
   deferred/reduced reading does not become *omitted* reading — each
   phase's required material must demonstrably still be read at its
   boundary. Item 5 specifically must show it does not weaken principle
   5's context-reset resilience guarantee; if no tactic can prove that,
   the Planning Chief's `objectives_feedback` should say so and drop item
   5 from this period rather than force a fix that trades safety for
   savings.
3. Six items over 15 files, three files shared by three or more items
   (`doctrine.md`: items 3⁺/4/5; `execute.md`: items 2/4/5;
   `agents/dcs-safety-officer.md`: items 2/4) — the Planning Chief's
   `partition_ok` determination and any sequential-staging decision is
   this incident's central safety question, not routine bookkeeping.

## Intake source (for /dcs-close to route back to)

Owner chat via `/dcs-new`: "need to minimize (reasonably, without harming
the system effectiveness) token consumption for DCS." Expanded by
explicit Owner direction (combine six items, Type 1) in the same
conversation. Opening deferred one operational period on a territory
conflict with `deviation-path-proportionality`, resolved 2026-07-28 when
that incident closed and deployed.
