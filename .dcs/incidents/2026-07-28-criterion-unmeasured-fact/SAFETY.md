# SAFETY — Safety Officer verdicts

## Period 1 — verdict 1 (final), 2026-07-28

Verdict returned verbatim (schemas.md #5); IC resolutions for each
advisory appended after the block.

```json
{
  "verdict": "pass",
  "refutations": [],
  "advisories": [
    {
      "finding": "Stale unmeasured registry claim in the maintainer vault, outside this period's territory but exactly the defect class this incident codifies. C:\\DCS\\vault\\Decisions\\fable-review-roadmap.md:24-25 states \"0.6.10 remains unpublished (registry at 0.6.9)\" and offers as its regeneration command \"read the row's State cell and `git log main..dcs/direct-resolution-lane`\" -- an in-tree command paired with an out-of-tree claim, so it can never establish the fact. I measured it: `npm view dcs-command-system versions` returns [... '0.6.9', '0.6.10'], i.e. 0.6.10 IS published. (Line 194's \"npm holds 0.6.9, tree is 0.6.10 unpublished\" is explicitly labelled \"at decision time\" and is provenance, not a live claim -- leave it.)",
      "fix": "Rewrite lines 24-25 as the command's result and name the command: \"`npm view dcs-command-system versions` -> 0.6.10 published (measured 2026-07-28)\". File is untracked in C:\\DCS and absent from this worktree, so it is not this period's diff -- fold in at close or queue it.",
      "severity": "low"
    },
    {
      "finding": "Repo is accumulating shipped-payload changes under an already-published version number. dcs/VERSION = 0.6.10 and `npm view dcs-command-system versions` shows 0.6.10 published; this period adds payload content (plan.md, dcs/templates/202-OBJECTIVES.md, agents/dcs-planning-chief.md) under the open `## Unreleased` heading. That is the \"one version, two contents\" shape the 3b field lesson describes. It is NOT a refutation: criterion 4 explicitly forbids a bump this period, the prior Unreleased entry did the same, and vault/Backlog.md:393-396 already tracks the underlying gap.",
      "fix": "Nothing this period. The next release must bump before publish; the pending `version-bump-command` work is the right home.",
      "severity": "low"
    },
    {
      "finding": "dcs/workflows/plan.md is now 422 lines (was 403). CLAUDE.md's coding rules state \"workflows <= ~250 lines\" with doctrine.md as the only exception, and no test enforces it -- tests/test_doctrine_integrity.py's only size check is the doctrine+schemas 37 kB hot-path budget. The breach is pre-existing (403 before this diff), and the IAP bounded this period at <= 425, which held.",
      "fix": "Either correct CLAUDE.md's stated budget to the real one or queue a plan.md split; a written budget nothing measures is itself a principle-15 defect.",
      "severity": "low"
    },
    {
      "finding": "The \"75 minutes\" figure now appears in three surfaces added this period (dcs/workflows/plan.md check 3b, dcs/templates/202-OBJECTIVES.md MEASURED CLAIM, CHANGELOG.md) with no regenerating command beside it. I traced the provenance and it holds -- .dcs/incidents/2026-07-26-schemas-md-trim/AAR.md:250 records the publish at 03:33:16Z = 14:33 +1100 and vault/Backlog.md:454-455,500 the timeline -- and it is a frozen historical event, not a census over a moving tree, so it matches the precedent set by check 3a's \"four Safety halts\".",
      "fix": "None required. Noted only so the figure's provenance is on the record with the verdict rather than in memory.",
      "severity": "informational"
    },
    {
      "finding": "agents/dcs-planning-chief.md:58 uses an ASCII double hyphen (\"You read the 202 before any lint does -- plan.md lint 4a check 3b\") in a file that uses the em dash 12 times and nowhere else uses \" -- \". Cosmetic only; no test covers it.",
      "fix": "Swap `--` for an em dash at the integration commit.",
      "severity": "informational"
    }
  ],
  "checked": [
    "Read the full uncommitted diff myself: `git diff` on all four files in C:\\DCS-wt\\criterion-unmeasured-fact. `git diff --numstat` = CHANGELOG.md 17/0, agents/dcs-planning-chief.md 6/1, dcs/templates/202-OBJECTIVES.md 15/1, dcs/workflows/plan.md 20/1. No file additions, deletions or renames.",
    "CRITERION 1 -- read the landed check 3b at dcs/workflows/plan.md:153-171. Trigger is state outside the tree (\"asserting anything the working tree does not contain (a registry version, whether something is published, an installed or deployed copy, another repository, a remote ref, a live service)\"), and it explicitly extends to \"a waiver inside one\". Requirements mirror 3a: (i) \"the 202 names the command that establishes the fact\", (ii) \"phrased as that command's result ... never as a bare assertion\", (iii) \"you run it yourself now and record the actual output in `214-LOG.md`\". Carve-out for in-tree facts present. MET.",
    "CRITERION 1 numbering -- `grep -c \"^3b\\.\" dcs/workflows/plan.md` = 1. `grep -n \"^[0-9]\\+[a-z]\\?\\. \\*\\*\"` returns 1(123), 2(127), 3(132), 3a(137), 3b(153), 4(172), 5(174), 6(177), 7(187), 8(194) -- exact expected sequence, no renumbering of 1-8. `grep -rn \"lint 4a\"` confirms the one external reference (template:42, \"plan.md lint 4a check 6\") still resolves to the unchanged check 6.",
    "CRITERION 1 fidelity -- diffed the approved verbatim draft in 204-TASKING/S1.md against the landed paragraph with a Python difflib script. The ONLY delta is the disclosed compression in the final sentence (\"nothing was required to look, and\" dropped). Trigger sentence and (i)(ii)(iii) are byte-identical to the draft. S1's claim survives.",
    "CRITERION 2 -- read the historical text MYSELF from the worktree copy, .dcs/incidents/2026-07-26-schemas-md-trim/202-OBJECTIVES.md:115-118, and derived independently without S1's reasoning. Criterion 10's third sentence, \"Версия не бампится, если план не назовёт причину: 0.6.9 не опубликована\", is a waiver whose justification asserts an npm-registry publication state. Tokens that catch it under the new trigger: \"a waiver inside one\", \"a registry version\", \"whether something is published\". It fails (i) -- the criterion names `grep -ril \"bread_bot\" dcs/ tests/ agents/ skills/` for its in-tree half and nothing for the publication half; fails (ii) -- bare assertion, not a command result; fails (iii) -- SAFETY.md:61 records only the grep and the VERSION/package.json sync, no registry reading. Would now be a lint defect. MET.",
    "CRITERION 2 corroborated empirically -- ran `npm view dcs-command-system versions`, exit 0, output includes '0.6.9'. The historical assertion was not merely unmeasured, it was false.",
    "FALSE-POSITIVE TEST -- applied the 3b trigger myself to all five of this incident's own acceptance criteria. Criterion 1 (read plan.md diff), 3 (read template), 5 (run suites in-tree) settle from this project's own files/harness -- 3b's own carve-out excludes them. Criterion 4 uses `grep`/`git diff` on this repo -- in-tree, and it carries its command regardless. Criterion 2 references .dcs/incidents/2026-07-26-schemas-md-trim/202-OBJECTIVES.md, which I confirmed is git-TRACKED (`git ls-files .dcs`) and physically present in this worktree, so it is an in-tree read, not another-repository state. ZERO of five trigger, under the IAP's bound of at most one. Wording is not over-broad.",
    "CRITERION 3 -- read dcs/templates/202-OBJECTIVES.md:20-70. MEASURED CLAIM block sits at line 48, inside the SAME HTML comment that opens at line 24 (single `-->` now at line 60, none stray in between), immediately after the OWNERSHIP TAG paragraph, same genre (all-caps label + rule + worked phrasing + dated field lesson). It requires the establishing command inside the criterion, requires result-phrasing, and cites \"plan.md lint 4a check 3b\", which I confirmed resolves. MET.",
    "CRITERION 4 -- `grep -n \"^## Unreleased\" CHANGELOG.md` = line 26 (pre-existing; the new bullet is at 42-58, under it and under `### Added`, before the closing `---`). `git diff -- CHANGELOG.md | grep -c \"^+## \"` = 0. `git diff --stat -- dcs/VERSION package.json` = empty output, no version bump. MET.",
    "CRITERION 5 -- ran both suites myself from the worktree root. `python tests/test_doctrine_integrity.py` -> 82/82 passed, exit 0. `npm test` -> 100/100 passed (gate), 10/10 passed (intake), 82/82 passed (integrity), exit 0. Counts read from the runs' own output, identical to the recorded baseline, no drop. MET.",
    "BOUNDARIES -- `git status --short` shows exactly four modified tracked files (CHANGELOG.md, agents/dcs-planning-chief.md, dcs/templates/202-OBJECTIVES.md, dcs/workflows/plan.md) plus the untracked incident directory .dcs/incidents/2026-07-28-criterion-unmeasured-fact/ (IC artifacts, expected). No forbidden path touched: nothing under dcs/hooks/, tests/, skills/, bin/, dcs/references/, no install.*, no package.json.",
    "TERRITORY vs TASKINGS -- read both 204-TASKING files. S1 territory = dcs/workflows/plan.md only, forbidden dcs/templates/**, agents/**, CHANGELOG.md, dcs/references/**, dcs/hooks/**. S2 territory = the other three files, forbidden dcs/workflows/**, dcs/references/**, dcs/hooks/**, tests/**, skills/**. Each specialist's actual diff lies wholly inside its own territory; neither entered the other's. Non-overlap confirmed at file granularity and by content -- plan.md's diff contains no MEASURED CLAIM/template/charter/CHANGELOG text, and the other three diffs contain no plan.md edit.",
    "ADJACENT-INCIDENT ZONE -- `git diff -- dcs/workflows/plan.md | grep -c \"Pre-stamp checklist\"` = 0; the two hunks are @@ -113,7 and @@ -150,6 only, both inside the 4a zone. Lines 331-340 untouched.",
    "PACKAGE HYGIENE -- Python byte-level check on all four files: BOM False, CRLF False, Cyrillic False on each. `wc -l dcs/workflows/plan.md` = 422 (<= 425 bound; was 403 at HEAD).",
    "PRINCIPLE-15 AUDIT of claims this period added -- \"These five checks\" -> \"These checks\" removes a stale count that was already false (nine items); `grep -rniE \"(five|six|seven|eight|nine|[0-9]+) checks\" dcs/ agents/ skills/` confirms no other copy of that census survives anywhere in the payload. CHANGELOG's \"82/82 passed\" carries its regenerating command and I re-measured it as 82/82. The \"75 minutes\" figure traced to AAR.md:250 (publish 03:33:16Z = 14:33 +1100) and vault/Backlog.md:454-455,500. The registry claims the diff makes about 0.6.9 verified against a live `npm view`."
  ]
}
```

## IC resolutions of the advisories (period 1)

1. **Vault stale registry claim** — fixed at close in the main checkout
   (`vault/Decisions/fable-review-roadmap.md:24-25` rewritten as the
   command's result with the command named; vault is unguarded, outside
   this period's diff by design). Also a **fourth field measurement** of
   this incident's own defect class — recorded in the AAR.
2. **Payload accumulating under a published 0.6.10** — no action this
   period (criterion 4 forbids the bump); the release act bumps first.
   Tracked by `version-bump-command` (register, rank 11).
3. **plan.md 422 lines vs CLAUDE.md's unenforced ~250 budget** — queued
   at close as a Backlog note under item 18 (the budget-no-suite-enforces
   entry); not this incident's territory.
4. **"75 minutes" provenance** — no action required; provenance now on
   the record here.
5. **ASCII `--` at agents/dcs-planning-chief.md:58** — fixed by the IC
   before the integration commit (em dash, matching the file's own
   convention).
