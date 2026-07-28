<!--
IAP.md -- the Integrated Action Plan, written by the IC during /dcs-plan.
This is the ONLY document specialists execute against once approved -- the
single source of truth doctrine principle 3 insists on. Editing this file
after approval voids IAP-APPROVED automatically (hash mismatch) -- that is
deliberate, not a bug to route around.
-->

# IAP — Incident Action Plan

**Incident:** deviation-path-proportionality
**Type:** 3
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `203-ORG.md` · `204-TASKING/S1.md`,
`204-TASKING/S2.md`, `204-TASKING/S3.md`

## Objectives (summary of 202)

**Goal:** A narrow, no-premise-change amendment to an approved plan —
reached via any of the three deviation dispositions (`replan` /
`amend_tasking` / `escalate_owner`), a Safety-verdict fix-tasking, or a
post-pass advisory correction that touches `IAP.md` content — costs
ceremony proportional to its own size instead of a full replanning
cycle, while remaining fully counted by the existing attempt/halt
machinery; and a fact a prior DCS seat already established moves into a
later artifact by reference to its source, not by the Dispatcher
retyping it from memory.

**Acceptance criteria:**

1. `execute.md`/`plan.md` define ≥1 amendment path (any of the three
   deviation dispositions, a Safety fix-tasking, or a post-pass advisory
   correction) whose ceremony is documented as strictly less than a full
   `plan.md` steps-1-9 pass, while still producing a stamp that satisfies
   `marker_valid()` unchanged and that trigger (c)'s attempt count still
   captures, no bypass.
2. The new path's boundary is explicit: stated applicability conditions,
   and a symmetric fallback to the full path outside them.
3. Both field measurements (`halt-loop-unbounded` S3,
   `register-field-repair-path` Halt-2) re-traced against the new path
   show measurably fewer spawns and/or Owner round-trips. [S1 derives the
   count as evidence via anchored grep; IC records the finished table
   here — see Verification plan below]
4. `dcs/hooks/dcs_gate.py` and `tests/test_dcs_gate.py` untouched
   (`git diff --stat` empty). [IC]
5. ≥2 in-territory command-point spawn instructions rewritten to cite
   sources instead of retyping them.
6. `doctrine.md` states the by-reference-not-retype principle generally;
   `doctrine-appendix.md` carries provenance in its own idiom, naming
   this incident, not a `vault/` path.
7. `test_doctrine_integrity.py`, `test_dcs_gate.py`, `test_dcs_intake.py`
   all still pass.
8. Hot-path budget guard still passes. MEASURED CLAIM: before/after byte
   counts recorded as evidence, not carried forward.
9. MEASURED CLAIM: `npm view dcs-command-system version` → `0.6.10`
   (confirmed at stem and independently at plan time, both `0.6.10`,
   tree and registry in sync). `dcs/VERSION` + `package.json` bumped
   atomically to `0.6.11`, `CHANGELOG.md` entry added.

**Out of scope this period:** actually running `npm publish`;
`revision-preservation-map` (register rank 5); any change to
`dcs/hooks/dcs_gate.py` / `tests/test_dcs_gate.py`; the roadmap's
un-sourced "max_files export" example / Delegation-bound-crossing
proportionality; the full breadth of Rec 2 beyond this incident's
in-territory spawn instructions; `decomposition-backlog-routing`
(register rank 9). Full text: `202-OBJECTIVES.md`.

## Tactics (from the Planning Chief)

1. **Cheapen the ceremony, never the stamp.** `marker_valid()`
   (`dcs_gate.py:515-528`) is a pure content-hash membership check —
   it cannot see how much ceremony produced the stamp. The amendment
   path performs the identical terminal acts (recompute sha256, rewrite
   `IAP-APPROVED`'s first line, append the sentinel per `plan.md` step
   8) and cuts only the acts upstream of them, so trigger (c)'s attempt
   count stays fully accurate by construction.
2. **One declaring site, everywhere else a citation.** The amendment
   path is declared once, as new `## 6c.` in `plan.md` (its mechanics
   ARE `plan.md`'s: the Delegation check is step 6, the hash/marker/
   sentinel are steps 7-8); `execute.md` steps 6 and 9 cite it by number
   rather than restating it, to avoid the exact two-disagreeing-copies
   defect class `check-15`/field measurement 2 already caught this
   project on.
3. **Ratify by the decision already made, not by a second one.** Step
   6c takes the already-logged command-point-3/4 decision (cited by
   timestamp) as its ratifying authority; `plan.md` step 7's pre-stamp
   checklist gains a bounded exception naming that entry in place of a
   fresh `command: iap_review` — explicit, because the checklist as
   written would otherwise be satisfied by the period's *first* pass's
   entry and ratify nothing new.
4. **State the ceremony inequality as a count derived from the workflow
   text.** Full `plan.md` steps-1-9 pass: ≥2 agent spawns (chief,
   command point 2) + up to 2 Owner round-trips (202 confirm, 6b
   approval). Step 6c: 0 agent spawns + at most 1 Owner round-trip. 0 < 2
   is derivable by counting spawn instructions in the two paths,
   independent of any incident's history.
5. **Reuse existing disposition tokens; add no schema surface.** No new
   enum value, no new sentinel grammar — `schemas.md` and
   `dcs/templates/214-LOG.md` stay untouched, preserving the 1,205 B hot-
   path headroom entirely for criterion 6, and keeping check 13's anchors
   and the commander's enum stable.
6. **Additive-only numbering.** `6c` is appended after the existing `6b`
   (`plan.md`'s heading sequence: 1,2,3,4,4a,4b,5,5a,6,6b,7,8,9); nothing
   renumbered — 7 external citations to `plan.md`/`execute.md` step
   numbers live outside every territory in this plan (`typing.md`,
   `202-OBJECTIVES.md` template, `close.md`, `run.md`) and must not
   break.
7. **Principle-15 clause, not a new principle 16, unless it doesn't
   fit.** Principle 15 already is this rule ("write the derivation, not
   the result") applied to durable artifacts; Rec 2 is the same rule
   applied to transfer between seats. A new principle 16 is the fallback
   only if the clause distorts 15, and only after re-measuring the
   budget.
8. **Provenance in the appendix's own idiom, census annotated.** Name
   the incident, not an unshipped `vault/` path; annotate the "9 of 10"
   figure as moving, exactly as the file's existing historical figures
   already are, and reconcile with the adjacent pre-existing "eight of
   ten" figure.
9. **The release tasking runs last and verifies its own citations by
   command.** S3's `CHANGELOG.md` entry names labels S1/S2 create; its
   evidence is a grep proving each exists before the sentence is
   written — Rec 2 applied to this incident's own paperwork.

## File-territory partition

| Specialist | Territory | Forbidden |
|---|---|---|
| S1 | `dcs/workflows/execute.md`, `dcs/workflows/plan.md`, `agents/dcs-commander.md` | `dcs/hooks/**`, `tests/**`, `dcs/references/**`, `dcs/templates/**`, every other `dcs/workflows/*.md`, every other `agents/dcs-*.md`, `skills/**`, `dcs/VERSION`, `package.json`, `CHANGELOG.md`, `.dcs/**`, `vault/**` |
| S2 | `dcs/references/doctrine.md`, `dcs/references/doctrine-appendix.md`, `dcs/references/forms.md` | `dcs/references/schemas.md`, `dcs/references/typing.md`, `dcs/workflows/**`, `agents/**`, `skills/**`, `dcs/hooks/**`, `tests/**`, `dcs/templates/**`, `dcs/VERSION`, `package.json`, `CHANGELOG.md`, `.dcs/**`, `vault/**` |
| S3 | `dcs/VERSION`, `package.json`, `CHANGELOG.md` | `dcs/references/**`, `dcs/workflows/**`, `dcs/templates/**`, `dcs/hooks/**`, `agents/**`, `skills/**`, `tests/**`, `bin/**`, `install.ps1`, `install.sh`, `.dcs/**`, `vault/**` |

**Partition status:** disjoint — verified by direct inspection (9 literal
paths, zero overlap), not merely trusted from `partition_ok: true`.
**Execution mode:** staged (see `203-ORG.md`) — S1 ∥ S2 in parallel
(mutually independent: S2 renames no heading S1 cites, does not touch
`schemas.md` which S1's citation checks depend on); **S3 sequential,
after both S1 and S2 return `done`** — its `CHANGELOG.md` entry cites
their output and its evidence is a grep proving those labels exist.

## Risks

1. Execution mode is staged, not fully parallel, though S1/S2's
   territories are disjoint (see partition table) — an execution-mode
   note, not an overlap needing justification.
2. **Measured contradiction S1 must resolve:** `execute.md` step 9's
   advisories paragraph (lines 289-302) orders the IC to fix advisories
   "itself, now," folding them into the integration commit — but if that
   fix touches `IAP.md`, the marker goes stale and `dcs_gate.py` denies
   every non-`.dcs/**` edit, including the incident's own mandatory
   close-time `vault/` memory-routing write. Logged verbatim in field
   measurement 2 at 2026-07-27T22:44:52. Step 6c is the resolution; S1's
   edit to that paragraph must make the route explicit.
3. **Rec 2 has a legitimate exception.** `plan.md` step 3 mandates
   passing the Planning Chief the full 201+202 text INLINE, "not file
   paths" — a deliberate information-diet constraint (principle 5), not
   a retyping habit. Criterion 5's safe targets are `execute.md`'s two
   summarizing spawn prompts (steps 6, 9), not `plan.md` step 3.
4. **Hot-path budget (1,205 B) is the most likely halt cause.** If
   criterion 6's mandatory clause doesn't fit, the correct outcome is
   dropping the optional principle-8 pointer and, if still short,
   reporting a deviation (tighter wording, or a ratchet change — which
   is a separate incident) — never trimming unrelated doctrine prose to
   fund a new one.
5. **Three booby-traps**, each named to its owning tasking: (i)
   `tests/test_dcs_gate.py` executes the FIRST `--halt-count` line it
   finds in `doctrine-appendix.md` (currently line 209) across nine
   fixtures — a second such line above it hijacks the test, and
   criterion 4 forbids repairing the test; (ii) `agents/dcs-commander.md`
   is check 13's degeneracy-guard population member; (iii) five files
   carry a verbatim `GRAMMAR_LINE` quotation checked by check 12.
6. **Cyrillic trap sits exactly where criterion 6 points.** Field
   measurement 1's log, including the Owner's own framing, is in
   Russian; quoting it verbatim in a shipped file trips check 9 ("no
   Cyrillic anywhere in the shipped package"). S2 is forbidden from
   doing so — English only in `doctrine-appendix.md`.
7. **Criterion 3's savings are asymmetric and partly
   Delegation-contingent.** Field measurement 1's saving is
   unconditional — one agent spawn (command point 2 not spawned; the
   trigger-(c) escalation round-trip is NOT saved and must not be
   claimed, it is mandatory under principle 13 regardless). Field
   measurement 2's saving is one Owner round-trip (the post-pass advisory
   re-approval), and holds only where Delegation bounds hold. Do not
   average the two into one headline number.
8. **Two surfaces deliberately left unowned**, checked rather than
   overlooked: `dcs/templates/IAP.md`'s "not a bug to route around" line
   stays true (step 6c re-stamps properly, doesn't route around the
   void); `schemas.md:142`'s "voids" sentence is about `forbidden_globs`
   auto-approval, unrelated to the IAP hash, and doesn't go stale.
   `dcs/workflows/run.md`'s pause list is a plausible follow-up home for
   the new path but is out of every territory — registered as a
   follow-up, not absorbed.
9. **Auto-approval will fail its bound check as expected** —
   `package.json` is in territory (`forbidden_globs`) and criterion 9
   necessarily discusses a version bump (`forbidden_topics`). This
   IAP goes to a real Owner `AskUserQuestion` at step 6b; not a defect
   in the plan.

## Verification plan

Five parts, for the Safety Officer:

1. **Re-trace both field-measurement logs** against the new step 6c
   using an anchored pattern (`grep -nE '^\[[^]]*\] (command:|ESCALATION:|IAP-APPROVED:|SAFETY-)' <log>`
   — never a bare substring count, which over-counts on narrative
   lines). Expected, to be checked against S1's returned table rather
   than accepted from it: **field measurement 1**
   (`.dcs/incidents/2026-07-25-halt-loop-unbounded/214-LOG.md:96-127`)
   actually paid 2 agent spawns (command point 3 at 12:10, command point
   2 at 12:30-12:35, both `dcs-commander`) + 2 Owner round-trips
   (trigger-(c) escalation 12:45, IAP approval 12:50), plus a full lint
   4a re-run and an `IAP.md` + `203-ORG.md` rewrite, for a fix its own
   AAR calls "one derived pattern and one reworded bullet"; under step
   6c the command-point-2 spawn is not made — 1 agent spawn, an
   unconditional saving of one. **Field measurement 2**
   (`.dcs/incidents/2026-07-27-register-field-repair-path/214-LOG.md:31-44`)
   actually paid 2 agent spawns (command point 4 at 20:51, Safety
   re-check at 22:35, both mandatory) + 3 Owner round-trips (trigger-(b)
   escalation 21:11, re-approval 22:22, post-pass advisory re-approval
   22:45), across two re-stamps.

   **Corrected after Safety Halt 1 (see `SAFETY.md` verdict 1,
   refutation 1, and the halt-1 fix-tasking return):** the ORIGINAL
   claim — that the 22:45 post-pass advisory round-trip disappears
   "wherever Delegation bounds hold" — was refuted: step 6c's first-pass
   design re-screened the WHOLE 201/202 text against
   `forbidden_topics` on every amendment, and that text contains
   "version bump," so the screen re-trips unconditionally — zero
   measurable saving, not a contingent one. The fix-tasking rescoped
   6c's Delegation re-check to the amendment's own delta only (not the
   unchanged 201/202 body) and, separately, tightened boundary condition
   1 so `## 6c.`'s cheap path excludes an amendment whose real scope
   spans more than `IAP.md` alone (e.g. touching `REGISTER.md` too).
   Re-derived with the same anchored grep: the 22:45:59 re-stamp's real
   historical scope touched `IAP.md` **and** `REGISTER.md`, so it is
   correctly EXCLUDED from `## 6c.` by the tightened boundary — not a
   saving. The genuinely `.dcs/**`-only, single-artifact event is the
   **22:22:57** re-stamp (the `fix_taskings` repair itself), which the
   delta-scoped screen now measurably saves: **1 Owner round-trip
   saved** — same headline number as the original claim, but a
   different mechanism and a different named event. Criterion 3 is met
   for both field measurements as of this correction: field measurement
   1 saves 1 agent spawn (unconditional); field measurement 2 saves 1
   Owner round-trip (via the delta-scoped screen, at the 22:22:57 event,
   not 22:45:59).

   **Corrected AGAIN after Safety Halt 2 (see `SAFETY.md` verdict 2,
   refutation 1, and the halt-2 fix-tasking return — same class as halt
   1: a boundary edited and verified against only the single case that
   prompted it).** The paragraph immediately above was itself wrong for
   field measurement 1: tightening boundary condition 1 to exclude the
   22:45:59 event (correct) also excluded field measurement 1's own
   4-artifact amendment (`204-TASKING/S1.md` + `S3.md` + `IAP.md` +
   `203-ORG.md`, `.dcs/incidents/2026-07-25-halt-loop-unbounded/214-LOG.md:118`)
   — unchecked, because the fix was validated only against the
   complaint that prompted it. Boundary condition 1 was rewritten a
   second time, this time as ONE per-artifact invariant over an
   amendment's WHOLE touched-artifact set (admissible iff every artifact
   is a `204-TASKING/*.md` the triggering logged decision names, this
   incident's own `IAP.md`, or this incident's own `203-ORG.md` where
   the amendment makes its bookkeeping consequent — and none of
   `.dcs/esg/**`, `.dcs/config.json`, `201-BRIEF.md`,
   `202-OBJECTIVES.md`, or any acceptance-criterion text in either
   `202-OBJECTIVES.md` or `IAP.md`'s own summary), **with mandatory
   validation against both field measurements before the fix-tasking was
   allowed to report done** — both re-derived by anchored grep and
   confirmed admitted, with their savings intact: field measurement 1's
   4-artifact set is now admitted (1 agent spawn saved, the 12:30-12:35
   command-point-2 spawn skipped, the 12:45 trigger-(c) round-trip still
   correctly NOT claimed as saved — it is mandatory under principle 13
   regardless of path); field measurement 2's 1-artifact set remains
   admitted as a strict subset (1 Owner round-trip saved, unregressed).
   **Criterion 3 is met for both field measurements, doubly verified.**
   One disclosed implementation judgment call from the fix-tasking, for
   the Safety Officer's independent assessment: the "failed-bound
   inheritance" clause (verdict-2 advisory 3) was scoped to `max_files`/
   `max_specialists`/`forbidden_globs`/`require_tests_green` and
   deliberately excludes `forbidden_topics`, because `forbidden_topics`
   is the one bound the delta-scoped screen (halt 1's fix) already
   re-derives in full — blind inheritance of `forbidden_topics` would
   have re-regressed field measurement 2 (whose only failed bound at its
   last full approval was `forbidden_topics`, the "version bump" trip).

   **Corrected a THIRD time after Safety Halt 3 (see `SAFETY.md` verdict
   3; Owner-sanctioned "continue, structural fix," 209 sitrep, folding
   escalation triggers b/c/e).** The paragraph above was itself wrong
   again: admitting field measurement 1's multi-tasking amendment also
   admitted a case nobody had reviewed — a brand-new `204-TASKING/*.md`
   file, for which `## 6c.`'s old claim that lint checks 1/4/8 are
   "degenerate" is vacuously false (nothing was ever proven about a
   partition line that didn't exist at the last approval). Root cause,
   named by the Safety Officer and concurred by dcs-commander: three
   consecutive fix-taskings each validated their own rewrite only against
   the case that prompted it, because the same agent authored both the
   fix and its test. **Structural fix, removing the class by
   construction rather than patching wording a fourth time:** the
   "skip checks 1/4/8" optimization is deleted outright — those checks
   now always run against the amendment's complete post-amendment
   tasking set (costing 0 additional spawns/round-trips, since the
   session already runs lint itself); any amendment touching a
   newly-created tasking file now always takes the lightweight Owner
   round-trip, never auto-approves; and the validation fixture set was
   IC-authored (11 must-admit/must-reject/must-catch-by-execution cases)
   rather than left to the fix-tasking specialist to invent, specifically
   to break the same-reasoning-writes-both-the-fix-and-its-test pattern.
   **All 11 fixtures validated with real, reproducible command output**
   (an actual Python script exercising checks 1/4/8 against this
   incident's own real fix-tasking files and four constructed bad cases,
   plus a real `dcs_gate.py --halt-count` run against a constructed
   at-ceiling fixture) — not asserted, executed. Criterion 3 remains met
   for both field measurements (savings unchanged: FM1 1 spawn, FM2 1
   round-trip), and criterion 2's boundary is now closed against the
   specific case that broke it (new, unnamed, or ceiling-adjacent
   tasking files) by mechanism (checks that execute), not by an
   enumerated exception that the next case could slip past.
2. **The path must be cheap without being a bypass.** Confirm
   `dcs_gate.py:515-528`'s `marker_valid()` is still satisfied unchanged,
   and that step 6c still routes through `plan.md` step 8 so an
   `IAP-APPROVED:` sentinel is appended and trigger (c)'s tally captures
   the amendment. Then attack the boundary from the other side: try to
   construct a genuine re-plan that reaches step 6c anyway. Criterion 2
   is met only if the fallback is symmetric and explicit, not implied by
   omission.
3. **All three suites, run independently**, not read from a specialist's
   return: `python tests/test_doctrine_integrity.py`, `python
   tests/test_dcs_gate.py`, `python tests/test_dcs_intake.py`. Baselines
   measured before any edit, 2026-07-28: 82/82, 100/100, 10/10, all
   green. The doctrine-integrity total may legitimately grow (checks
   12(c)/13(d)/14(d) emit one named case per discovered population
   file) — only a named FAIL is a defect.
4. **Both MEASURED CLAIMs, re-measured, not carried forward.** Criterion
   8: the byte-count one-liner in `204-TASKING/S2.md`'s evidence — before
   was 23,387 + 13,296 = 36,683 with 1,205 B headroom; confirm the after
   and that the remainder is not negative. Criterion 9: `npm view
   dcs-command-system version`, then `dcs/VERSION` and `package.json`'s
   version field, both must read `0.6.11` in the same commit.
5. **The standing constraint and the scope floor.** Criterion 4: `git
   diff --stat -- dcs/hooks/dcs_gate.py tests/` must print nothing — any
   output at all is escalation, not a fix-tasking. Confirm the change is
   complete, not merely green: `grep -rn "run \`/dcs-plan\` again"
   --include=*.md dcs/ agents/` should no longer show `execute.md:173`
   as a terminal instruction with no alternative, and `grep -rn "vault/"
   --include=*.md dcs/ agents/ skills/` must still return only its two
   pre-existing generic hits — a third would mean an unshipped path was
   cited from shipped prose. Manual check: read `dcs/templates/IAP.md:5`
   and confirm it still reads true against the new path.

## Deviation history (this period)

None — first pass, period 1.
