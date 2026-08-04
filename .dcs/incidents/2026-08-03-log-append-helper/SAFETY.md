<!--
SAFETY.md -- written by the Safety Officer, verbatim, transcribed by the IC.
Not summarized or softened. This period's verdict is the third pass (two
prior SAFETY-HALT: entries in 214-LOG.md record the halted attempts and
their fix cycles) -- this file holds the verdict that let the period close.
-->

# SAFETY — Verdict (Operational Period 1)

**Incident:** log-append-helper
**Verdict:** pass (third pass this period; two prior halts, see `214-LOG.md`)

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
