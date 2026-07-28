<!--
SAFETY.md -- written by the Safety Officer, verbatim, appended per
operational period / per verdict. Never summarized or softened by the IC.
-->

# SAFETY — Verdicts

**Incident:** deviation-path-proportionality

## Verdict 1 (period 1, 2026-07-28T10:27+11:00)

```json
{
  "verdict": "halt",
  "refutations": [
    {
      "claim": "Criterion 3 is met for both field measurements. S1's returned table: 'field measurement 2 saves 1 Owner round-trip (the post-pass 22:45 re-approval), Delegation-contingent'; the IAP's verification plan expects 'under step 6c the 22:45 round-trip disappears wherever Delegation bounds hold.'",
      "evidence": "I re-traced `.dcs/incidents/2026-07-27-register-field-repair-path/214-LOG.md:31-44` with the IAP's own anchored pattern and then read every line raw. What actually happened: 2 agent spawns (dcs-commander 20:51:11 line 33; Safety re-check returning 22:35:55 line 39) + 3 Owner round-trips (trigger-b answered 21:11:03 line 35; AskUserQuestion Approve 22:22:57 line 37; AskUserQuestion Approve 22:45:59 line 43). Re-traced against step 6c's documented steps, the total is UNCHANGED at 2 spawns + 3 round-trips, i.e. ZERO measurable reduction: (a) the command-point-4 spawn is upstream of 6c in execute.md step 9, mandatory; (b) the Safety re-check is mandatory on the fix-tasking branch (execute.md:255-258 're-run the Safety Officer'); (c) the trigger-b round-trip is mandatory under principle 13; (d) BOTH re-approvals are unsaved, because plan.md:409 makes 6c 'reusing step 6's own Delegation check rather than a new one', and step 6's check screens 'the 201-BRIEF.md / 202-OBJECTIVES.md text' against `forbidden_topics` -- I parsed the latest Delegation block myself (`.dcs/esg/DELEGATION.md`, version 4) and `forbidden_topics` contains 'version bump', which that incident's 202 carries; log lines 37 and 43 record the trip firing and falling through to the Owner both times ('4th occurrence this incident'). The Delegation contingency therefore resolves to 'still costs the round-trip' in the exact case criterion 3 names, and criterion 3 requires 'measurably fewer ... than what actually happened', not fewer in a counterfactual where the bounds had held. Criterion 3 is met for field measurement 1 (I confirmed the 12:35 command-point-2 spawn at halt-loop-unbounded 214-LOG.md:116 is genuinely not made under 6c -- a real 1-spawn saving) and NOT met for field measurement 2. Note the fix is available inside S1's own territory and needs no criterion change: 6c reuses step 6's whole-plan screen, when boundary conditions 2/3/4 already guarantee the 201/202 text is unchanged -- scoping the amendment's Delegation re-check to the amendment's own delta would make this round-trip actually disappear and be measurable against the log."
    },
    {
      "claim": "plan.md:395-401: 'Of lint 4a: checks 1 (self-contradiction), 4 (territory disjointness), and 8 (territory inside the project) are degenerate under boundary condition 3, not waived -- territory provably didn't change, so they hold by construction without needing to be re-run to stay true.'",
      "evidence": "Two of those three are not degenerate under that condition. I read the checks in the same file: check 1 (plan.md:123-126) is 'for every tasking, `territory ∩ forbidden` must be empty' and check 8 (plan.md:194-196) is 'resolve every `territory` AND `forbidden` glob against the incident's own project root' -- both read `forbidden`. Boundary condition 3 (plan.md:376-378) pins only `territory`: 'No change to any 204-TASKING/*.md's territory.' Nothing in 6c's four conditions prevents an amendment from editing a tasking's `forbidden` list, and 6c's permitted scope (condition 1: 'a single 204-TASKING/*.md file') is exactly the file where `forbidden` lives. So an amendment that adds a `forbidden` entry can newly intersect an unchanged `territory` (check 1 fails) or add a `../`/absolute glob escaping the project (check 8 fails), while shipped prose tells the IC both hold 'by construction' and need not be re-run. The named consequences are the checks' own: check 1 'directs a specialist to edit what it is forbidden to touch, forcing either a partition violation or a mid-execution deviation' (principle 6), and check 8 states 'Nothing else catches this: the gate deliberately allows targets outside the project.' Only check 4 (territory-vs-territory) is genuinely degenerate. This is not artifact hygiene -- it is the new path instructing an IC to skip a check that can fail, with no other catcher. Fixable either by widening condition 3 to pin `forbidden` too, or by moving checks 1 and 8 into 6c's 'still run' list."
    },
    {
      "claim": "doctrine-appendix.md:228-231 (S2's criterion-6 provenance paragraph): 'This incident's own review of the seat most exposed to that pattern -- the Dispatcher, which relays between nearly every spawn -- named it the dominant defect source: \"9 of `prod-tools-drift`'s 10 halts were not about the code\".'",
      "evidence": "The finding is not this incident's. I traced the figure to its only source, `C:\\DCS\\vault\\Decisions\\fable-review-roadmap.md:55-56`, whose own header reads 'Decision: reform roadmap from the third-party review (2026-07-27)' and '**Decided:** 2026-07-27, Owner + Fable (bread_bot main session, model claude-fable-5)', sourced from a cleared bread_bot session transcript -- a third-party review of DCS, recorded in another project's session the day BEFORE this incident's stem (2026-07-28). This incident measured nothing here; it only moved the rule into doctrine. The 202 itself says so: criterion 6 states the figure 'still comes from vault/Decisions/fable-review-roadmap.md'. Criterion 6 explicitly orders this paragraph to carry 'the provenance', and provenance is the one thing the sentence gets wrong -- a future reader hunting the figure's origin is pointed at this incident's artifacts, where it does not exist. (What I did verify as sound: the quoted parenthetical is verbatim-accurate to the roadmap; the 'as of the incident's own close -- it moves' annotation satisfies principle 15; and the reconciliation against the adjacent 'eight of ten' figure is TRUE -- I confirmed the unnamed 'first incident' at appendix:182-186 is prod-tools-drift via `.dcs/esg/REGISTER.md:424` ('prod-tools-drift is at 16 h 40 min / 144 KB with 10 halts'), `vault/Backlog.md:315` and `vault/Meta/building-dcs-lessons.md:450`, so 'the same ten halts, different predicates' is correct. It is one sentence's attribution that is false, not the paragraph's substance.)"
    }
  ],
  "advisories": [
    {
      "finding": "Step 6c is unreachable by a linear reader of plan.md. Step 1's `phase == execution` branch (plan.md:21-27) is the only handler for '/dcs-plan invoked during execution' -- the state every 6c entry is in -- and it still says 'counts as a re-plan -- proceed', routing straight into step 2 (202 redraft), step 3 (chief spawn) and step 4 (command point 2): the exact acts 6c exists to skip. 6c's own text asserts 'Steps 1-3 do not run', so the file now carries two instructions for one trigger, neither citing the other -- the two-disagreeing-copies class the IAP's own tactic 2 names. It fails safe (costs ceremony, never skips approval), and execute.md does route to 6c by number in three places, so this is not a criterion failure.",
      "fix": "Add one forward pointer in step 1's `phase == execution` branch: if 214-LOG.md holds a qualifying command-point-3/4 entry and 6c's boundary conditions hold, go to 6c instead of proceeding to step 2."
    },
    {
      "finding": "Boundary condition 1 (plan.md:372-374) nests instead of partitioning: `204-TASKING/*.md` files live under `.dcs/**`, so the second branch ('`.dcs/**` content only') literally swallows the first and would permit rewriting every tasking at once, despite 'never both in the same pass'. Read literally it also reaches `.dcs/esg/DELEGATION.md`, `REGISTER.md` and `config.json`. The parenthetical '(the IAP prose the amendment is correcting)' carries the intent, and I could not turn this into a reachable genuine re-plan (see checked[]), so it is imprecision, not a hole.",
      "fix": "Scope the second branch explicitly -- e.g. 'or this incident's own `IAP.md` prose only', excluding `.dcs/esg/**` and `.dcs/config.json`."
    },
    {
      "finding": "The new appendix paragraph's parenthetical omits the version. I censused the file's own idiom: all four pre-existing provenance headers carry a version (`v0.5.2`, `v0.3.2`, `v0.6.9`, `v0.6.9 revision 2`), two of them alongside a date; the new one is the only one of five with no version at all. Criterion 6's own template is `(field lesson <date>, v<version>)`.",
      "fix": "`(field lesson 2026-07-28, v0.6.11, incident deviation-path-proportionality)`."
    },
    {
      "finding": "`grep -rn \"vault/\" --include=*.md dcs/ agents/ skills/` now returns THREE hits, not the two the IAP's verification plan expects: the new one is `dcs/workflows/execute.md:325` ('including the close-time `vault/` memory-routing write'), added by S1. `vault/` is absent from package.json's `files` whitelist (I re-parsed it: bin/, dcs/, agents/, skills/, docs/, tests/, install.ps1, install.sh, README.md, CHANGELOG.md), so this is a DCS-repo-specific project fact in prose every downstream install reads -- CLAUDE.md's 'ship no project facts'. It is generic phrasing, not a citation into a specific vault file, and the surrounding instruction is still correct, so no criterion fails. Worth noting for evidence quality: S2's claim that the grep 'still shows only 2 pre-existing generic hits' was measured over its own three files and never covered its sibling's -- a cross-territory interaction neither specialist's isolated check could catch.",
      "fix": "Rephrase to the project-neutral form already used elsewhere, e.g. 'the close-time memory-routing write into whatever memory store the project's CLAUDE.md documents'."
    },
    {
      "finding": "CHANGELOG.md's new `## 0.6.11 -- 2026-07-28` section carries three different suite counts under one heading with no measurement moment marked per bullet: the two carried-forward bullets each end '`python tests/test_doctrine_integrity.py`: **82/82 passed**, unchanged' (true at their own incidents' close) while 'Verified at release' says 83/83. Only the release line names its regenerating commands.",
      "fix": "Annotate the two carried bullets as measured at their own incident's close, or drop the per-bullet counts in favour of the single release-level line that already carries the commands."
    }
  ],
  "checked": [
    "git status --porcelain + git diff --stat in C:\\DCS-wt\\deviation-path-proportionality -- exactly the 9 declared files, 199 insertions / 15 deletions, no strays; git diff --stat main...HEAD empty (changes are uncommitted working-tree state, as expected mid-execute)",
    "Criterion 4: `git diff --stat -- dcs/hooks/dcs_gate.py tests/` printed nothing, both against the working tree and against main -- confirmed empty",
    "Out-of-scope sweep: `git diff --stat main...HEAD -- dcs/references/schemas.md dcs/templates/214-LOG.md install.ps1 install.sh bin/ vault/` printed nothing",
    "Read the full git diff of all 9 files line by line (plan.md, execute.md, dcs-commander.md, doctrine.md, doctrine-appendix.md, forms.md, VERSION, package.json, CHANGELOG.md)",
    "Read plan.md in full (lines 1-502) -- verified 6c sits after 6b with nothing renumbered (heading sequence 1,2,3,4,4a,4b,5,5a,6,6b,6c,7,8,9), and that steps 7-8's hash/marker/sentinel mechanics are unmodified apart from the bounded exception",
    "Verified 6c's derived claims about plan.md's own structure by reading them: the chief spawn IS at step 3, command point 2 IS at step 4, the 202 confirm IS at step 2, the approval IS at step 6b (ceremony inequality >=2 spawns + <=2 round-trips is derivable from the text); lint 4a's checks 1/2/3/3a/3b/4/5/6/7/8 exist as enumerated -- but checks 1 and 8 read `forbidden`, see refutation 2",
    "Read dcs_gate.py:515-528 myself -- marker_valid() is a pure first-line-hash membership check against approval_digests(iap), blind to ceremony; 6c's terminal acts satisfy it unchanged. Confirmed 6c routes to step 8, which appends the `IAP-APPROVED:` sentinel, so trigger (c)'s attempt tally captures every amendment (no bypass)",
    "Boundary attack (criterion 2), attempted and FAILED to break it: tried a `replan` whose fix is one tasking's task text (blocked by condition 4, and the fallback paragraph says so by name); a Safety refutation requiring a criterion reword (blocked by condition 2); adding a new specialist/tasking (blocked by condition 3). Could not construct a genuine re-plan that reaches 6c -- criterion 2 holds",
    "python tests/test_doctrine_integrity.py -- 83/83 passed, 0 FAIL lines (grep -cE '^FAIL' = 0), run by me in the worktree",
    "python tests/test_dcs_gate.py -- 100/100 passed, run by me, including all ten criterion-16 fixtures that execute the appendix's first `--halt-count` line",
    "python tests/test_dcs_intake.py -- 10/10 passed, run by me",
    "Criterion 8 re-measured on the guard's OWN normalised basis (read tests/test_doctrine_integrity.py:263-272 to find it is CRLF->LF normalised, not getsize): after = 23,873 + 13,296 = 37,169 B, headroom 719 B against HOT_PATH_BUDGET_KB=37 (37,888 B); before, recomputed from `git show HEAD:` = 23,387 + 13,296 = 36,683 B, headroom 1,205 B. Positive, guard green",
    "Criterion 9 re-measured: dcs/VERSION = 0.6.11, package.json version = 0.6.11 (same working tree, so the integration commit carries both atomically); `npm view dcs-command-system version` = 0.6.10, confirming NO publish happened (out-of-scope respected)",
    "Criterion 6's vault-doesn't-ship premise re-verified myself by parsing package.json -- `files` = [bin/, dcs/, agents/, skills/, docs/, tests/, install.ps1, install.sh, README.md, CHANGELOG.md], no vault/. Then `npm pack --dry-run`: 75 files, 0 matches for vault or .dcs/, tarball dcs-command-system-0.6.11.tgz",
    "Criterion 3, field measurement 1: anchored grep `^\\[[^]]*\\] (command:|ESCALATION:|IAP-APPROVED:|SAFETY-)` over 2026-07-25-halt-loop-unbounded/214-LOG.md, then read lines 96-127 raw. Actual = 2 agent spawns (deviation->amend_tasking 12:10 line 102; iap_review accept 12:35 line 116) + 2 Owner round-trips (trigger-c CONTINUE 12:45 line 120; AskUserQuestion approval 12:50 line 124). Under 6c the command-point-2 spawn is not made: 1 spawn saved, unconditional. Confirmed 0 Owner round-trips are saved (trigger (c) is mandatory) -- S1 correctly did not claim any. Also noted lines 109-111 show that IC had already improvised skipping steps 1-3, which is why the saving is 1 and not 2",
    "Criterion 3, field measurement 2: same anchored grep plus a raw read of lines 33-46 of 2026-07-27-register-field-repair-path/214-LOG.md, plus a JSON parse of `.dcs/esg/DELEGATION.md`'s highest-version delegation-bounds block -- see refutation 1 for the arithmetic",
    "Criterion 5: read both rewritten spawn prompts -- execute.md step 6 (command point 3) now orders 'pass its source (the file path and line range, or the command that regenerates it), never a summary retyped from memory'; execute.md step 9 (command point 4) now orders the ESG-state row 'quoted directly from <esg_root>/.dcs/esg/REGISTER.md rather than paraphrased from memory'. Two in-territory rewrites, demonstrated by the text -- criterion 5 met",
    "Criterion 6 substance: doctrine.md principle 15 carries the new (v0.6.11) by-reference clause and principle 8 carries the amendment-path clause; no stray principle 16 (numbering runs ...14, 15, then the next section); the appendix paragraph names this incident and cites no vault path (confirmed by the vault grep, which shows no appendix hit)",
    "Traced the appendix's '9 of 10' figure to C:\\DCS\\vault\\Decisions\\fable-review-roadmap.md:55-56 and read that file's header -- see refutation 3. Independently verified the 'eight of ten' reconciliation is TRUE against .dcs/esg/REGISTER.md:424, vault/Backlog.md:315 and vault/Meta/building-dcs-lessons.md:450",
    "CHANGELOG restructuring claim re-verified independently of the IC: `git show e17fa7f` -- its own commit message says 'CHANGELOG.md documents it under a new Unreleased heading, since 0.6.10 -- the version this work would otherwise have landed under -- was already published mid-incident', dated 2026-07-27 22:37. Folding those two bullets into 0.6.11 alongside this incident's own is accurate, not misattribution. Heading sequence now runs 0.6.11 -> 0.6.10 -> 0.6.9 with no orphaned Unreleased section",
    "Booby-trap checks: the appendix's `--halt-count` line is still the FIRST (and only) such line, at line 209, above the insertion point at 221 -- and the nine gate fixtures that execute it all pass; 0 Cyrillic characters and no BOM in all 9 touched files (measured with a Python codepoint-range scan, not by eye)",
    "Read dcs/templates/IAP.md:1-7 -- 'Editing this file after approval voids IAP-APPROVED automatically (hash mismatch) -- that is deliberate, not a bug to route around' still reads TRUE against 6c, which re-establishes approval by re-stamping rather than routing around the void",
    "Confirmed execute.md's old terminal instruction is gone: lines 177-181 now read 'Tell the Owner to run /dcs-plan again -- amend_tasking, replan, and escalate_owner may all reach the proportionate route at plan.md step 6c ... and the full steps-1-9 path runs unchanged for anything that doesn't' -- no dangling alternative"
  ]
}
```

## Verdict 2 (period 1, 2026-07-28T11:13+11:00, re-verification after halt-1 fix-taskings)

```json
{
  "verdict": "halt",
  "refutations": [
    {
      "claim": "IAP.md's corrected verification plan (lines 236-244) and 202 criterion 3: \"Criterion 3 is met for both field measurements as of this correction: field measurement 1 saves 1 agent spawn (unconditional); field measurement 2 saves 1 Owner round-trip (via the delta-scoped screen, at the 22:22:57 event, not 22:45:59).\" Also `214-LOG.md`:40 and the S1-fix1 return, which re-derived only field measurement 2 and carried field measurement 1's row forward unchanged.",
      "evidence": "Halt 1's refutation 1 is genuinely fixed for field measurement 2 -- verified independently and in full (see checked[]). But the companion tightening of boundary condition 1, folded in from halt 1's advisory 2 in the SAME fix-tasking pass, has removed field measurement 1's own qualification, and nobody re-checked it. Field measurement 1's amendment scope, read raw from its own log: `.dcs/incidents/2026-07-25-halt-loop-unbounded/214-LOG.md`:118 records FOUR artifacts -- `204-TASKING/S1.md` + `204-TASKING/S3.md` + `IAP.md` + `203-ORG.md`. New boundary condition 1 (`plan.md`:378-382) admits only \"a single `204-TASKING/*.md` file, or this incident's own `IAP.md` prose only ... never both branches in the same pass.\" Field measurement 1 fails it three ways: (a) two taskings, not one; (b) both branches in the same pass; (c) `203-ORG.md` falls in neither branch. Per 6c's own symmetric fallback, field measurement 1 therefore takes the FULL path, the 12:30-12:35 command-point-2 spawn IS made, and the saving is ZERO, not \"1 agent spawn, unconditional.\" Criterion 3 requires BOTH measurements to show a saving; it remains unmet -- the unmet half has moved from measurement 2 to measurement 1. **CLASSIFICATION (halt 2 on the same objective, convergence read per doctrine principle 13):** SAME CLASS as halt 1 -- a defect of form, a scoping/boundary imprecision inside `## 6c.` producing a false criterion-3 claim. Halt 1 refutation 1 was criterion 3 failing because the Delegation screen was mis-scoped; halt 1 refutation 2 was boundary condition 3 pinning `territory` but not `forbidden`; this is boundary condition 1 mis-scoped against the events criterion 3 names. Third instance of one class. The criterion is satisfiable without a re-plan (condition 1 can be widened to admit the taskings an amendment names plus the `IAP.md` bookkeeping the same pass requires, while still excluding `.dcs/esg/**`, `.dcs/config.json`, `201-BRIEF.md` and `202-OBJECTIVES.md`), but that is the IC's call."
    }
  ],
  "advisories": [
    {
      "finding": "CHANGELOG.md's boundary-condition paraphrase (lines 70-71) is now stale against shipped plan.md (pre-fix wording for both branch 2 and condition 3). Neither fix-tasking had CHANGELOG.md in territory.",
      "fix": "Re-derive the CHANGELOG bullet from the final plan.md text once the boundary is settled, not from this round's."
    },
    {
      "finding": "The approval marker is currently STALE: IAP-APPROVED's first line (a8510760c32f...) no longer matches live IAP.md (IC edited it at 10:51:59 to record the corrected criterion-3 table, after the 09:31:25 stamp). Reproduced directly: dcs_gate.py denies a PreToolUse/Edit payload against any non-.dcs/** path with a hash-mismatch reason.",
      "fix": "Re-stamp (plan.md steps 7-8 mechanics) before any specialist edits a payload file again. .dcs/** edits (further 214-LOG.md/SAFETY.md/204-TASKING entries) remain exempt in the meantime."
    },
    {
      "finding": "The delta-scoped forbidden_globs screen can invert a bound that failed at the last full approval into a pass, rather than merely skip a redundant re-check -- unlike forbidden_topics, re-screening only the amendment's own touched file(s) never reproduces a territory-wide glob failure. No live escape today (max_files/max_specialists still block), but a small release-bearing Type 3 could slip through IC-auto-approval where the Delegation intended Owner eyes.",
      "fix": "One clause: if the last full approval's own bound check failed on any bound, the amendment inherits that failure rather than auto-approving."
    },
    {
      "finding": "Boundary condition 2 pins '202-OBJECTIVES.md acceptance criterion' but IAP.md carries its own acceptance-criteria summary, and condition 1's second branch admits IAP.md prose -- a literal reader could change the criteria as IAP.md states them while condition 2 reads satisfied.",
      "fix": "\"No change to any acceptance criterion -- in 202-OBJECTIVES.md or in IAP.md's summary of it.\""
    },
    {
      "finding": "6c's Entry conditions do not require the cited command-point-3/4 entry to postdate the CURRENT IAP-APPROVED stamp -- a stale entry from an earlier attempt could authorize a later amendment it never saw. Step 7's own bounded exception names this exact hazard for its own ratifying entry but doesn't extend the freshness requirement to 6c's Entry conditions.",
      "fix": "Add to Entry: the cited entry must postdate the IAP-APPROVED stamp currently in force."
    },
    {
      "finding": "Halt 1's advisory 5 remains open as directed (CHANGELOG per-bullet suite counts, non-blocking) -- restated only so it is not lost at close.",
      "fix": "Annotate at close or the next natural CHANGELOG.md touch."
    }
  ],
  "checked": [
    "Full re-verification of all 9 acceptance criteria from scratch, all 3 halt-1 refutations independently re-derived and confirmed fixed, all 5 halt-1 advisories confirmed addressed (4 folded + 1 correctly left open), all 3 test suites re-run independently (83/83, 100/100, 10/10), both MEASURED CLAIMs re-measured (hot-path headroom 719 B positive; VERSION+package.json both 0.6.11, npm registry still 0.6.10 confirming no publish), criterion-2 boundary attack re-attempted against the tightened conditions and failed to break it, criterion 4 empty diff on dcs_gate.py/tests/ reconfirmed, out-of-scope sweep clean, CHANGELOG e17fa7f attribution re-confirmed independently, marker staleness reproduced by running dcs_gate.py directly rather than reasoning about it -- full detail in the agent transcript this verdict was transcribed from"
  ]
}
```

## Verdict 3 (period 1, 2026-07-28T12:07+11:00, re-verification after halt-2's raised-altitude fix-tasking)

```json
{
  "verdict": "halt",
  "refutations": [
    {
      "claim": "plan.md's rewritten ## 6c. (lines 426-441): \"Of lint 4a: checks 1 (self-contradiction), 4 (territory disjointness), and 8 (territory inside the project) are degenerate under boundary condition 3, not waived ... territory and forbidden both provably didn't change, for every 204-TASKING/*.md file this incident has, not only whichever one(s) condition 1 admits as touched this pass -- so all three hold by construction regardless of whether the amendment touches one tasking or several\". And the fix-tasking's / 214-LOG.md's companion claim that \"all 3 must-reject cases confirmed blocked\", including S1-fix2.md's case \"A genuine re-plan whose fix requires a NEW specialist/tasking not named by any already-logged command-point decision.\"",
      "evidence": "The universally-quantified degeneracy claim is false for a case the rewritten condition 1 admits, and the must-reject set never tested it. execute.md:257-264 (the fix-tasking branch 6c's Entry bullet 2 names) instructs the IC that \"a fix that also changes IAP.md's own content (an IC-owned criterion, a partition-table line) does need one, and that re-stamp routes through plan.md step 6c\" -- adding a specialist is exactly a partition-table line. plan.md's condition 1 bullet 1 admits \"a 204-TASKING/*.md file the triggering logged commander decision itself names (one or several ... no 'exactly one' cap)\" -- a NEWLY CREATED fix-tasking file the command: verdict -> fix_taskings decision names qualifies, and bullet 2 admits the IAP.md partition-table edit in the same pass. Not hypothetical: this incident created three new 204-TASKING/*.md files by fix-tasking (S1-fix1.md, S2-fix1.md, S1-fix2.md), confirmed by grep each declares its own File territory and Forbidden zones sections. For such a file, nothing \"provably didn't change\" -- its territory and forbidden are new content no approval and no lint ever saw. Consequences are the checks' own words: check 4 (plan.md:176-177) is the disjointness check plan.md:249 calls \"doctrine principle 6, non-negotiable\"; check 1 \"directs a specialist to edit what it is forbidden to touch, forcing either a partition violation or a mid-execution deviation\"; check 8 states \"Nothing else catches this: the gate deliberately allows targets outside the project\" -- confirmed against dcs_gate.py's relative_posix() directly. Condition 3's gloss looks like it might block this, but 6c disclaims that reading two sentences later: \"the two are orthogonal by design\" -- condition 1 decides which files may be edited, condition 3 only which fields inside them. Under the PREVIOUS boundary text this was blocked (\"a single 204-TASKING/*.md file ... never both branches in the same pass\" refused new-tasking-plus-IAP.md); removing the cap to admit field measurement 1 is what opened it. Criterion 2 is therefore not met: the cheap route is reachable for work that is planning work by construction -- a new specialist, a new territory, a new partition line the Planning Chief never designed and the Owner never approved -- with the partition check affirmatively declared unnecessary on the way through. CLASSIFICATION (halt 3 on the same objective): SAME CLASS as halts 1 and 2 -- direct descendant of halt 1's refutation 2, re-opened by halt 2's own fix, in the identical pattern: an edit to the ## 6c. admission boundary validated against the fixtures in front of the drafter and not against the population it must reject. FOURTH instance of one class. The raised-altitude form was followed in good faith -- the invariant shape is genuinely better and the mandatory fixture validation genuinely ran and genuinely fixed criterion 3 -- and the class still recurred, because the fixture set itself was written by the same reasoning that wrote the boundary."
    }
  ],
  "advisories": [
    {
      "finding": "Condition 1's admit-list does not exclude the bookkeeping the path itself performs (214-LOG.md appends, the IAP-APPROVED rewrite, register status transitions from an escalation) -- read literally this excludes every possible amendment. Not a refutation: fails safe, and no non-self-defeating reading excludes either fixture.",
      "fix": "One clause: mandatory bookkeeping the path itself writes is not part of the screened set; a content edit to .dcs/esg/** is."
    },
    {
      "finding": "The failed-bound-inheritance clause's justification for excluding forbidden_topics is false as written (\"already re-evaluates the bound in full\" -- it evaluates a proper subset). The DECISION to exclude it is independently verified correct (parsed DELEGATION.md v4 myself, forbidden_topics was the only bound failing at FM2's last approval, blanket inheritance would re-regress FM2) -- only the stated reason is wrong.",
      "fix": "Delete the false justification sentence; keep the conditions-2/3/4 argument and state the residual explicitly."
    },
    {
      "finding": "CHANGELOG.md's boundary-condition paraphrase is now three rewrites stale against shipped plan.md, and it ships (in package.json's files whitelist). No fix-tasking has held S3's territory since halt 1.",
      "fix": "Re-derive from the final plan.md text once the boundary settles; prefer citing ## 6c. over paraphrasing conditions that have moved three times."
    },
    {
      "finding": "6c makes the per-attempt halt ceiling resettable at near-zero ceremony -- reproduced directly: --halt-count returns 0 despite two anchored SAFETY-HALT: sentinels, because the last re-stamp re-anchored the tally. Not a criterion failure: trigger (b) counts log-wide and does not reset (now 3 anchored halts, all escalated), and every reset burns an IAP-APPROVED: sentinel, so trigger (c)'s attempt tally (currently 3) still forces the Owner in.",
      "fix": "One sentence in 6c: it may not be used to clear a halt tally standing at the ceiling -- at the ceiling the route is trigger (b)/(c) escalation, not a cheap re-stamp."
    },
    {
      "finding": "6c's step 8 instruction (\"exactly as written below\") produces a false phase-transition line on an amendment that never leaves execution. Harmless mechanically (STAMP_RE only needs the timestamp+token+hex); field practice already writes the correct form by hand.",
      "fix": "Add the amendment-specific log-line form to step 8's own text."
    },
    {
      "finding": "Halt-1 advisory 5 remains open (CHANGELOG per-bullet suite counts, non-blocking) -- restated so it is not lost at close.",
      "fix": "Annotate at close or the next natural CHANGELOG.md touch."
    }
  ],
  "checked": [
    "Full re-verification of all 9 acceptance criteria from scratch; 8 of 9 green on independent measurement (all 3 suites 83/83+100/100+10/10, both MEASURED CLAIMs re-measured positive/correct, criterion 4 empty diff, criteria 5/6/7/8/9 all independently confirmed). Criterion 3 genuinely fixed for both field measurements, re-derived from the raw logs, not the specialist's table -- FM1 1 spawn saved, FM2 1 round-trip saved, both unregressed. Criterion 2 boundary attack re-attempted against the new invariant shape and broken by the new-tasking case (the refutation). Marker verified valid (c0afa92262b9... matches live IAP.md, gate reproduces an allow). Full detail in the agent transcript this verdict was transcribed from."
  ]
}
```

## Verdict 4 (period 1, 2026-07-28T13:02+11:00, re-verification after halt-3's structural fix) -- PASS

```json
{
  "verdict": "pass",
  "refutations": [],
  "advisories": [
    {
      "finding": "6c never mentions plan.md step 5a (register territory-union refresh). An amendment creating a new tasking whose territory isn't already in the union changes the union, but a REGISTER.md territory-field edit is excluded by condition 1 and the bookkeeping exemption -- such an amendment either falls to the full path (safe) or takes 6c and leaves the portfolio territory check reading a stale union. Not idle: this incident's own log records a concurrent token-economy stem queued on a territory conflict here.",
      "fix": "One clause: step 5a is degenerate while condition 3 holds and no tasking is created; an amendment changing the territory union either recomputes the register column as bookkeeping or takes the full path."
    },
    {
      "finding": "The bookkeeping-writes exemption list reads closed and omits step 8's .dcs/ACTIVE update and an escalation's 209 sitrep write. The categorical opening sentence already covers both (over-exclusion, never under), so not a refutation, but a literal reader applies the enumeration.",
      "fix": "Make the list explicitly non-exhaustive, or add both writes by name."
    },
    {
      "finding": "Condition 3 names only one copy of territory/forbidden where condition 2 was explicitly fixed to name both copies (202-side and IAP.md's own summary). Condition 3's second sentence is copy-agnostic and the checks-run paragraph independently covers IAP.md, so this is precision, not a hole. Related: the delta-scoped forbidden_globs screen's stated object (\"the file(s) this amendment actually touches\") is vacuous, since amendments always touch .dcs/** while forbidden_globs lists only payload paths.",
      "fix": "Mirror condition 2's both-copies phrasing in condition 3; restate the delta screen's object as the amendment's declared territory globs, not the files it edits."
    },
    {
      "finding": "The halt-ceiling re-stamp clamp is true but nearly unreachable in the cycle it governs: --halt-count re-anchors at every re-stamp, so a halt/re-stamp/halt/.../halt pattern (this incident's own) never exceeds 1 against a ceiling of 3. Not a criterion failure -- the log-wide trigger (b)/(c) tallies are the load-bearing backstop and both fired correctly.",
      "fix": "One clause noting the re-anchor and that trigger (b)/(c) are the operative ceiling, not this clamp."
    },
    {
      "finding": "CHANGELOG.md's shipped boundary-condition paraphrase is now three verdicts stale against the deleted-and-rewritten plan.md text, and it ships. No fix-tasking has held S3's territory since halt 1.",
      "fix": "Replace the paraphrase with a citation to ## 6c. at the integration commit, rather than re-paraphrasing a boundary that has moved four times."
    },
    {
      "finding": "Halt-1 advisory 5 still open: CHANGELOG.md's two carried-forward bullets each read a fixed 82/82 with no measurement-moment marker, while the release line reads 83/83 (re-confirmed current).",
      "fix": "Annotate the carried bullets as measured at their own incident's close, or drop the per-bullet counts."
    },
    {
      "finding": "6c's \"at most 1 Owner round-trip\" is true of the Delegation check's own outcomes but reads as an absolute about an amendment's total Owner contact; escalation round-trips under principle 13 (e.g. FM1's trigger-c) are additional and unaffected, and the saving comparisons already only count the spawn, so no criterion fails.",
      "fix": "One parenthetical noting escalation round-trips are additional."
    },
    {
      "finding": "6c's lint-4a enumeration (\"checks 1...2...3/3a...3b...4...5...6...7...8\") is a census, current today but stale the moment check 9 is added -- a principle-15 shape. Separately, the fix-tasking's validation script (scratchpad, not a shipped/incident artifact) hardcodes the two real tasking files' territory/forbidden as literals rather than reading them, and its check-1 implementation tests only one glob direction; both audited faithful against the real files today.",
      "fix": "Mark the enumeration illustrative, keep the invariant (\"all of lint 4a\") as the operative sentence; if the scratchpad harness is ever promoted into a real artifact, have it parse the tasking files and test both glob directions -- otherwise it is correctly a one-time hand-checked fixture, not evidence infrastructure."
    }
  ],
  "checked": [
    "Full independent re-verification of all 9 criteria; all pass. All 3 suites re-run (83/83, 100/100, 10/10). Both MEASURED CLAIMs re-measured (headroom 719 B positive; version 0.6.11 atomic, registry unpublished at 0.6.10). Criterion 2 boundary attack re-run against the new text with the specific goal of finding an uncaught case -- failed to break it (replan-by-premise, new tasking, modifying an existing tasking's territory/forbidden, deleting/renaming a tasking, stale authorizing entry, editing criteria in either copy, deleting a chief-authored risk item, .dcs/esg/** content edit -- all blocked). Criterion 3 re-derived from raw logs independently for both field measurements, unregressed (FM1 1 spawn; FM2 1 round-trip -- confirmed FM2's own fix_taskings decision created no tasking file, so the new-partition clamp correctly does not fire on it). Marker verified valid (8d0bf92b4bae... matches live IAP.md). Fix-tasking's validation script independently re-run and audited against the real files it claims to test. Full detail in the agent transcript this verdict was transcribed from."
  ]
}
```

## Advisories resolved (IC, 2026-07-28T13:06+11:00, before the integration commit)

Per execute.md step 9's advisory rule: fixed directly by the IC, no re-verification spawned (the officer already passed the criteria; these are artifact-hygiene edits, not criterion-affecting).

1. **Step 5a mention** — `plan.md` `## 6c.`: added a paragraph distinguishing step 5a's register-territory refresh (planning-shaped, NOT covered by the bookkeeping exemption) from the bookkeeping writes it sits beside — degenerate when condition 3 holds and no tasking is created; otherwise the IC recomputes the union as bookkeeping or the amendment takes the full path. **Fixed.**
2. **Bookkeeping exemption non-exhaustive** — `plan.md`: list now reads "includes, but is not limited to," and names `.dcs/ACTIVE`'s step-8 update and an escalation's 209 sitrep write alongside the two items already named. **Fixed.**
3. **Condition 3 single-copy / delta-screen object** — `plan.md`: condition 2 and condition 3 now both explicitly cover the `IAP.md`-summary copy; the ceremony paragraph now names the delta screen's object as the amendment's declared territory/forbidden globs, not the files it edits. **Fixed.**
4. **Halt-ceiling clamp scope** — `plan.md`: added a clause stating the clamp rarely binds in the halt/re-stamp cycle it governs (re-anchoring), and that triggers (b)/(c) are the load-bearing, non-resettable backstop. **Fixed.**
5. **CHANGELOG stale boundary paraphrase** — `CHANGELOG.md`: replaced the four-conditions paraphrase with a citation to `plan.md`'s `## 6c` and a one-line note that this period revised the boundary four times before it held. **Fixed.**
6. **CHANGELOG per-bullet suite counts** — `CHANGELOG.md`: both carried-forward 82/82 mentions now read "as of this item's own close — see 'Verified at release' below for this bump's own count." **Fixed.**
7. **"At most 1 round-trip" absolute phrasing** — `plan.md`: added a parenthetical stating the ceremony count is 6c's own Delegation-check contact only; escalation-trigger round-trips (principle 13) are separate and additional. **Fixed.**
8. **Lint-4a census / scratchpad harness** — `plan.md`: the check enumeration is now marked illustrative, with step 4a named as the operative, authoritative list. The scratchpad validation script (not a shipped or incident artifact) is correctly labelled a one-time hand-checked fixture in this verdict's own text above — **no incident-file change needed for the harness itself.**

Re-verification after the fixes: `python tests/test_doctrine_integrity.py` 83/83, `python tests/test_dcs_gate.py` 100/100, `python tests/test_dcs_intake.py` 10/10, `git diff --stat -- dcs/hooks/dcs_gate.py tests/` empty — all unchanged from verdict 4's own numbers. `git diff --stat` confirms exactly the same 9 files as the IAP's partition, no strays introduced by these fixes.
