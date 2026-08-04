<!--
AAR.md -- After Action Report, written by the IC during /dcs-close. Requires
a green (pass) Safety Officer verdict to exist before this file is written
-- close.md enforces this, do not write an AAR to paper over a halt.
-->

# AAR — After Action Report

**Incident:** log-append-helper
**Type:** 1
**Opened:** 2026-08-03
**Closed:** 2026-08-04
**Operational periods:** 1

## Outcome

All 10 acceptance criteria from `202-OBJECTIVES.md` period 1 met, verified by the Safety Officer's third pass (0 refutations) and independently re-confirmed by the IC. `dcs/tools/dcs_log.py` exists — stdlib-only, imports `dcs_gate.py`'s grammar dynamically, stamps a real offset-aware sub-second timestamp with no override channel, records operator identity, self-validates its own output, fails closed under concurrent invocation via a cross-process lock. All 22 real hand-written `214-LOG.md` append sites across the six writer workflows now invoke it. A new close-time criterion in `dcs/tools/record_integrity.py` flags 3-or-more identical timestamps or out-of-order entries, date-scoped, parse-safe over the portfolio's own legacy shapes. A permanent merge-guard check (`tests/test_doctrine_integrity.py`) enforces the migration mechanically. `CHANGELOG.md` carries the entry under the existing unpublished `0.8.0` heading. Integration commit `1894d89` (`git show 1894d89 --stat`), 20 files, staged explicitly by path. Register row `MERGED` as of this close (see 5a below) — deploy pending, `/dcs-deploy` is next.

## What worked

- **Import, never re-derive.** `dcs_log.py` and the new `record_integrity.py` criterion both reused `dcs_gate.py`'s existing grammar (`ENTRY_PREFIX`, `sentinel_of()`, `render_entry()`) via dynamic import rather than re-implementing the entry format — this is why the whole incident needed zero edits to `dcs_gate.py` itself, confirmed unchanged at every Safety Officer pass.
- **Self-validation before write.** The tool classifies its own rendered output through the real `sentinel_of()` before appending, so a future grammar drift breaks it loudly at call time rather than silently at audit time.
- **Sequenced specialists when a fix genuinely depends on another's landed change**, parallel otherwise. Both fix-tasking cycles after a halt ran the dependent specialist (S1, the root cause) alone first, then the dependent work (S2 and/or S4) once real code existed to build and test against — avoided both wasted rework and unverifiable claims about not-yet-existing behavior.
- **Real concurrent-process stress testing, not threads**, caught a genuine non-atomic-file-append race that no sequential test had or could have surfaced — and every non-vacuity claim throughout this incident (the merge-guard's sensitivity, the concurrency fix, the criterion's parse-safety) was proven with a control: the same test run against a deliberately broken or reverted version, confirmed to fail.
- **The Safety Officer's third pass replayed the exact prior falsifying mutations from scratch**, rather than trusting a green suite — this is what actually confirmed the recurring defect class was closed, not just narrowed a third time. See `vault/Meta/building-dcs-lessons.md` §32.

## Lessons

- A merge-guard check that derives its population from the same text it guards will keep losing to narrower and narrower surface-form attacks (§14's shape); pinning the population *outside* the guarded text (an explicit, hand-maintained manifest) plus an independent negative scan is what finally held, verified across three adversarial Safety Officer passes. `vault/Meta/building-dcs-lessons.md` §32.
- Two components can each be correct against their own stated contract and still be wrong together when one's implementation detail (here: a clock's precision) is silently load-bearing for a sibling's stated justification (here: a duplicate-timestamp threshold) — no isolated unit test sees the seam; only a cross-component test running one's real output through the other's real logic does. `vault/Meta/building-dcs-lessons.md` §33.
- A second, deeper adversarial pass can and did find a genuinely new defect class (the concurrency race) that a first, real, non-trivial pass had no reason to look for — escalation trigger (b)'s mandatory convergence read is what forced an honest classification (same-class vs. different-class) instead of treating both refutations as one undifferentiated "still broken."

## Deviations this incident

No specialist ever reported `status: "deviation"` — every one of the 4 original taskings and every fix-tasking respawn returned `"done"`. The incident's real course-correction came through the Safety Officer / command-point-4 mechanism instead: **two halts, both period 1, no re-plan (one operational period throughout, one IAP stamp).** Halt 1 (both refutations): criterion 4's merge-guard check required a same-line token 17 of 22 real sites lacked; the close-time criterion's duplicate-timestamp threshold justification was falsified by the tool's then-second-resolution clock. Fixed: S1 alone (precision), then S2+S4 in parallel. Halt 2 (escalation trigger (b) fired — second halt on the same objective, 209 sitrep filed, Owner chose continue via `AskUserQuestion`): the halt-1 merge-guard fix was same-class recurrence (narrowed, not closed) per the mandatory convergence read; a new, different-class concurrency race in the tool's own file-append was found on the deeper pass. Fixed at a structurally higher altitude (S1 alone: cross-process lock; then S4: check rebuilt with an external population manifest + independent negative scan + the four falsifying mutations encoded as permanent self-tests). Third Safety Officer pass: clean, 0 refutations, 6 advisories (all forward-hardening against not-yet-existing future hand-written sites), folded into the same integration commit via one more parallel S1+S4 round. Halt count ended at 2 of 3 (`max_halts_per_attempt`) — the incident closed before the ceiling, never needed the `replan` backstop dcs-commander named as its own stated condition.

## Memory routing

`vault/Meta/building-dcs-lessons.md` +2 sections (§32: population-pinned-outside-the-guarded-text, extending §14's shape with a working resolution; §33: cross-component precision interaction invisible to isolated unit tests). No `dcs/references/doctrine.md` or `doctrine-appendix.md` entry — neither lesson changes a doctrine rule or explains one's provenance; both are meta-lessons about building DCS's own guards, which is exactly `vault/Meta/`'s documented scope per `CLAUDE.md`'s routing test.

## Intake source closure

`.dcs/esg/REGISTER.md` row `log-append-helper` — DCS's own register, not an external system. Closure is this incident's own act: the row moves `ACTIVE` → `MERGED` at step 5a.3 below, filling in the closed date and collapsing Territory/Outcome/Intake source to one line each, pointing at `IAP.md`'s partition table and this file's Outcome section. No external ticket or `audit_results` row to flag — the originating decision (`vault/Decisions/non-anthropic-hardening.md` measure 1 + packaging item 2) is a vault document, not a system with its own closure state; nothing further to touch there.

## Safety Officer's final verdict (verbatim, from SAFETY.md)

All 6 advisories below were fixed and folded into integration commit `1894d89` before this close (see `214-LOG.md`'s advisory-fold-in entries for the S1/S4 spawns that did it).

```json
{
  "verdict": "pass",
  "refutations": [],
  "advisories": [
    {
      "finding": "The workflow append-site check walks only the six files in _WAC_WRITER_FILES (tests/test_doctrine_integrity.py:3636), while 202 criterion 4's enforcement clause says it 'walks dcs/workflows/*.md'. Proven live: appending 'Append the deploy outcome to `214-LOG.md` with the operator name.' to dcs/workflows/deploy.md leaves the suite fully green (242/242, zero WAC-family failures). Not a present-state defect -- deploy.md/esg.md/init.md/status.md measured at zero '214-LOG' mentions each, so the criterion's binding population is fully covered today -- but the guard is blind to a future append site added in those four files.",
      "fix": "Iterate the negative scan over every dcs/workflows/*.md rather than _WAC_WRITER_FILES, keeping the count-manifest bound to the six writers; or add an explicit assertion that the four non-writer workflows contain zero '214-LOG' append-shaped lines, so the file set itself is pinned rather than assumed."
    },
    {
      "finding": "_wac_negative_scan()'s continuation branch (tests/test_doctrine_integrity.py:3697-3700) looks back exactly one physical line, so a hand-written instruction wrapped across three lines evades both signals. Proven live: appending a three-line hand-written instruction to execute.md leaves the suite green (242/242). The two-line form of the same instruction IS caught, so the boundary is exactly at a two-line gap.",
      "fix": "Widen the look-back to the enclosing markdown paragraph (scan backward to the last blank line) instead of a fixed single line, while keeping the same-line-only rule for the dcs_log.py compliance test that the second rebuild deliberately narrowed."
    },
    {
      "finding": "The compliance shortcut `if \"dcs_log.py\" in line: continue` (tests/test_doctrine_integrity.py:3703) still marks an ENTIRE line compliant, so a hand-written clause appended onto a line that already invokes the tool is invisible. Proven live: rewriting execute.md:222 to add a second, hand-written append clause on the same line leaves the suite green. This is the same mechanism that killed the first rebuild, but its blast radius is now much smaller -- it can only hide an ADDED clause, never undo an existing conversion, because the count-manifest pins all 22 sites externally (confirmed by mutations m1-m4 all going red).",
      "fix": "Scan every '214-LOG' occurrence on a line rather than only the first, and require the dcs_log.py mention to fall within the same sentence as the matched keyword rather than merely somewhere on the line."
    },
    {
      "finding": "The two published exclusions match as unanchored, case-folded substrings over the whole line (tests/test_doctrine_integrity.py:3705), so any future new.md line containing the word 'template', or any plan.md line containing 'preservation', is silently exempt. Proven live: a fabricated new.md line using the word 'template' incidentally is wrongly exempted; the identical line with 'standard' in place of 'template' IS caught. new.md is dense with template prose, so this is a realistic future collision.",
      "fix": "Anchor each exclusion to its actual published site -- match on the specific invariant phrase (new.md's 'Initialize `214-LOG.md` from the template', plan.md's preservation-map fence) or pin it by line content hash, rather than a bare keyword anywhere on the line."
    },
    {
      "finding": "A reverted site can be hidden by editing _WAC_EXPECTED_SITE_COUNTS down in the same commit. Proven live: reverting plan.md:224 to hand-written shape AND changing the manifest's plan.md count from 8 to 7 leaves the suite green, because the negative scan independently misses that particular line (it carries an earlier, benign '214-LOG.md' mention, and the first-occurrence-only scan doesn't reach the real one). The manifest comment already frames manual updates as a feature ('forces conscious attention'), and the edit is visible in code review -- but the second signal does not currently back-stop it here.",
      "fix": "Folds into the same fix as advisory 3 (scan all occurrences on a line) -- that would make the negative scan catch this line independently of the manifest, restoring the intended two-independent-signals property for it."
    },
    {
      "finding": "dcs_log.py's accepted limitation -- a hard-killed process leaves <log>.md.lock behind, after which every later caller waits the full 5s and refuses -- is documented in the module docstring and reproduced exactly (exit 1 after ~5.3s, log byte-identical). The stderr names the lock file path but gives the operator no recovery instruction, so a hung append at a command point reads as an unexplained refusal.",
      "fix": "Add one clause to the refusal message naming the recovery, e.g. 'if no writer is actually running, delete <path> and retry' -- no behaviour change, no auto-stealing by age (which the docstring correctly rejects as its own race)."
    }
  ],
  "checked": [
    "python tests/test_doctrine_integrity.py -> 242/242 passed",
    "python tests/test_dcs_gate.py -> 100/100 passed",
    "python tests/test_dcs_intake.py -> 18/18 passed",
    "python tests/test_dcs_log.py -> 60/60 passed",
    "git diff --stat main -- dcs/hooks/dcs_gate.py dcs/references/doctrine.md -> empty (both forbidden zones unchanged)",
    "grep -c 'dcs_log.py' dcs/workflows/{new,plan,execute,close,run,loop}.md -> 1/8/9/2/1/1, sum 22, matching _WAC_EXPECTED_SITE_COUNTS exactly",
    "independent census: grep -n '214-LOG' dcs/workflows/*.md | grep -v dcs_log.py -> 25 lines, every one a read/count/grep or one of the two published exclusions",
    "mutation m1 (prior falsifying #1, strip all dcs_log.py from new.md) -> RED: count mismatch, manifest expects 1, found 0",
    "mutation m2 (prior falsifying #2, strip all dcs_log.py from plan.md) -> RED: count mismatch, manifest expects 8, found 0",
    "mutation m3 (prior falsifying #3, revert one plan.md site) -> RED on both signals: count mismatch AND negative-scan hit, plan.md:71",
    "mutation m4 (prior falsifying #4, revert one execute.md site) -> RED on both signals: count mismatch AND negative-scan hit, execute.md:222",
    "own mutation B2 (new standalone hand-written line in execute.md) -> RED, named",
    "own mutation E2/E3 (same instruction wrapped across two vs three lines) -> two-line RED, three-line GREEN (advisory 2)",
    "own mutation C (new hand-written line in deploy.md, a non-writer file) -> GREEN (advisory 1)",
    "own mutation G (hand-written clause appended onto an already-compliant line) -> GREEN (advisory 3)",
    "own mutation X1/X3 (exclusion-keyword collision test) -> GREEN then RED, confirming over-broad exclusion match (advisory 4)",
    "own mutation A (revert + manifest count edited down in the same change) -> GREEN (advisory 5)",
    "concurrency: 16 real simultaneous processes via subprocess.Popen against one fixture log, 3 rounds -> every round 16/16 exit 0, zero missing, zero duplicate",
    "concurrency non-vacuity control: same harness with the lock short-circuited, 4 rounds -> lost 1-3 entries per round, confirming the harness detects the defect the lock fixes",
    "fail-closed timeout: pre-touch the lock file, then append -> exit 1 after ~5.3s (bounded, not infinite), stderr names the lock path, log sha256 identical before and after",
    "criterion 1: grep imports -> all stdlib; no --timestamp/--at/--date/--now flag accepted",
    "criterion 3: empty/whitespace/missing --by all refused, log unchanged",
    "containment: slug with '..', '/', or unknown value all refused before resolution",
    "criterion 2: tool-written log and hand-written log with equivalent content both give halt_cycles()==2",
    "IAP verification plan A: date-scope-bypassed real logs (status-md-enum-drift, worktree-path-propagation) -> finds the 11-entry run exactly as the 201 states, reports colon-less offsets as notes, no crash",
    "IAP verification plan R4: corpus dry run over all 37 real .dcs/incidents/* dirs -> 0 in scope, 0 findings, 0 crashes",
    "criterion 7: collect_log_order_findings defined at record_integrity.py:1303, called at :1457 as the sixth findings.extend(...)",
    "criterion 5: all 7 population files quote GRAMMAR_LINE verbatim, sole stamp witness survives, dcs_log carrier (INVOCATION/FORMAT_LINE) bound in both forms.md and templates/214-LOG.md",
    "IAP verification plan D: wc -l all six workflow files at or under ceiling, new.md 264/270 grandfathered, WORKFLOW_GRANDFATHERED_LINES untouched by S4",
    "IAP verification plan E: every changed path (tracked + untracked) maps to exactly one specialist's declared territory",
    "principle 15: re-ran the corpus run-length census embedded beside DUPLICATE_TIMESTAMP_THRESHOLD -> matches the comment exactly except bucket 1, which the comment itself predicts will drift",
    "principle 15: re-measured the stem's '48 214-LOG mentions across 7 files' claim against main -> 48 exactly",
    "renumbering: grep for duplicate section numbers -> only a pre-existing '20.' duplicate on main, unrelated to this incident; this incident's 28-31 are unique with an accurate old-to-new map",
    "git status clean at session end -- only the scratchpad copy was mutated for adversarial testing, never the real worktree"
  ]
}
```
