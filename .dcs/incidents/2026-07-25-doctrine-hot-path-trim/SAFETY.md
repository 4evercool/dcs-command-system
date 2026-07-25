# SAFETY — Operational Period 1

**Incident:** doctrine-hot-path-trim
**Period:** 1
**Verifications this period:** 3 (halt, halt, pass) — each a fresh
`dcs-safety-officer` spawn per principle 9b. Both halts were against the routing
ledger (criterion 6's bookkeeping artifact); **neither was ever against the trim.**

---

## Verdict (third verification) — verbatim

**`verdict: pass`**
**`refutations: []`**

### checks_run — verbatim

- Extracted all 21 backtick-quoted commands from the CORRECTION 2 block of `214-LOG.md` programmatically (not retyped by hand) and executed all 19 anchor commands verbatim through bash, each twice: once as written (`grep -n -F`) and once as `grep -c -F`. Result: **19/19 returned exactly 1 hit. Zero returned 0, zero returned >1.**
- Confirmed every anchor sits within a single physical line: each `grep -F` match is a single numbered output line, so no anchor spans a markdown hard wrap. Independently confirmed the entry's own hard-wrap anecdote by running `git show 51dd073:dcs/references/doctrine-appendix.md | grep -c -F "three times in one incident"` => 0 (the phrase wraps between 51dd073 lines 52 and 53).
- Read the full `git diff -U2 dcs/references/doctrine.md` (8 hunks, at old lines 15/29/55/102/112/118/137/147) and mapped every hunk to ledger rows; all 8 hunks accounted for.
- **ROW 17 (the halt-2 row), all three clauses traced** against the diff and both anchored paragraphs. Cut text: "— neither changes who holds command judgment or what counts as approval, they only remove the Owner's need to type each phase command by hand." Clause 1 (command judgment) -> anchor `not DCS deciding for itself what counts as routine` = 51dd073:131. Clause 2 (what counts as approval) -> anchor `keystroke, not a record` = 51dd073:126, in "every ship still produces the exact same append-only log, hash-bound approval, and register row it would have if the Owner had typed 'yes' themselves." Clause 3 (removes only the keystroke) -> same sentence, and its specific content additionally survives in delivered core. **All three homed. The halt-2 refutation is genuinely resolved.**
- Rows 11, 12, 18, 19, 20, 21 substance re-checked against 51dd073 source text, **not against prior officers' findings**: row 11 TRAVEL -> 51dd073:52; row 11 ROT -> 51dd073:64; row 12 -> 51dd073:53 and :61; row 18 -> 51dd073:131 (near-verbatim); row 19 -> 51dd073:158, paragraph covers all three ICS analogies incl. staging and demobilization; row 20 -> 51dd073:139, and I confirmed the entry's own annotation is honest — the paragraph names the harness's worktrees and the deploy script's, and never "a human's personal one"; row 21 -> 51dd073:31.
- All 9 destination anchors resolved in the delivered tree and their paragraph **content** read, not just their lead-ins: 46 model-availability rationale AND the row-3 announce-rule sentence; 62 quota-vs-transcript field lesson; 120 principle 4's over-scope cost; 131 principle 6; 147 principle 9b's two structural reasons; 161 principle 13's four-revisions/31-hour lesson; 175 the test-inversion text verbatim from the cut; 184 the new lifecycle section; 221 the charter-defect field lesson. Every anchor line equals the exact start line of the range CORRECTION 1 cited, so the anchors target the same already-verified text.
- Rows 6 and 22 **re-judged independently from the diff** rather than carried from halt 1. Row 6 dropped only `**(v0.5.10)** Two rules, both about making the pause legible instead of ambiguous:` — both rules survive verbatim as the two bullets under the unchanged `### A command point is never a silent wait` heading. Row 22 dropped only the consequence clause "which fails and confuses the Owner"; the operative prohibition ("Never put a slash command inside a `bash`-fenced code block") is intact. **No rule lost in either.**
- Audited CORRECTION 2 for a third instance of the class by testing its own prose claims against its own stated commands: `git diff --numstat dcs/references/doctrine-appendix.md` => `114 0` (matches "114 lines"); `git diff -U0 dcs/references/doctrine-appendix.md | grep "^@@"` => first hunk `@@ -45,0 +46,29 @@` (matches the off-by-one correction exactly).
- Traced the supersession chain for orphaned citations: enumerated every citation in the original ledger and in CORRECTION 1, and confirmed each has a CORRECTION 2 counterpart. **No citation is orphaned between the three entries.**
- Scope (b): `git diff --numstat` => exactly 5 files, dcs/VERSION 1/1, dcs/references/doctrine-appendix.md 114/0, dcs/references/doctrine.md 18/20, package.json 1/1, tests/test_doctrine_integrity.py 9/4. `git status --porcelain --untracked-files=all` shows nothing untracked outside `.dcs/incidents/`.
- Re-measured the hot path myself => doctrine 22121, schemas 14596, **total 36717 B**. Matches the claim to the byte, 147 B under the 36,864 B target.
- Re-ran all three suites independently: `test_doctrine_integrity.py` => 12/12 including "hot-path budget: doctrine+schemas <= 37 kB"; `test_dcs_gate.py` => 25/25; `test_dcs_intake.py` => 10/10.
- Verified atomic version sync: `dcs/VERSION` = 0.6.5 and `package.json` 0.6.4 -> 0.6.5 in the same working change; the guard's version-sync check passes.
- Read `git diff tests/test_doctrine_integrity.py` — the ratchet edit is `HOT_PATH_BUDGET_KB` 42 -> 37 plus comment; the `hot = os.path.getsize(...)` check logic is untouched, **no forbidden-zone crossing into guard logic**.

### observations — verbatim, and all of these are for the Owner's criterion-10 read

- **ROW 16 IS ABSENT FROM CORRECTION 2's ACCOUNTING.** The entry cites rows 1-5, 7-15, 17-21 and explicitly excuses rows 6 and 22. Row 16 appears in neither list. **NOT a refutation**: row 16 was a compression-in-core, so no citation is owed; I verified the substance survives at delivered `doctrine.md:118` AND is independently carried at delivered `appendix:226`. The original ledger, which amended ruling B carries into the AAR alongside CORRECTION 2, describes row 16 in full. Nothing is unaccounted — the entry's list of citation-free rows is just short by one, and it cannot rot (the population is 22 frozen rows in an append-only file).
- **"ROWS 17 AND 18 GENUINELY HAVE DIFFERENT HOMES" IS IMPRECISE.** Row 18's single anchor is byte-identical to row 17's first anchor; row 17's home set is a strict **superset**, not a different set. The causal diagnosis is also loose — the halt-2 gap was caused by `128-135` under-covering, not by rows 17 and 18 sharing a range. **NOT a refutation**: I verified both rows' citations are individually complete and correct. Row 18 is not under-cited.
- **"THE DEFECT CLASS ... STOPS BEING REPRESENTABLE" OVERCLAIMS BY HALF.** Anchors genuinely eliminate **ROT** — a stale anchor returns 0 loudly rather than resolving to wrong text silently — but they do **not** eliminate **UNDER-COVERAGE**: a row can still name too few anchors, which is exactly what halt 2 was. What the scheme actually bought is different and, in my judgment, sufficient: **the population is now enumerable and each member is a one-command binary check**, which is why I could exercise all 19 in a single script rather than the one-instance-per-cycle grind the convergence read described. I closed the under-coverage question by hand for all 22 rows this session and found no gap.
- **ROW 17 CLAUSE 3's HOME IS GENERALIZED, NOT LITERAL.** The cut clause says the two commands remove the need to type each *phase command*; the anchored appendix sentence is about *deploy delegation* removing the approval "yes" keystroke. Same proposition at a higher generality. **NOT a refutation**, because the literal content also survives in delivered core, which still describes `/dcs-run` as "the full lifecycle ... in one command" and retains the load-bearing constraint "without eliminating its gates."
- **ONE PRINCIPLE-15 RESIDUE IN SHIPPED CODE, TWICE-PASSED, NOTED NOT REFUTED.** The new `HOT_PATH_BUDGET_KB` comment says CRLF makes the pair "~319 B larger" than the LF main checkout, without a command beside that specific number. It is hedged with `~`, the derivation with both commands is recorded at `214-LOG.md` line 25, and the operative number (36,717 -> 37) carries its own runnable regenerating command. Criterion 8 was ruled MET under two prior independent re-checks; recorded only because the checklist requires naming every durable claim this period added to shipped files.
- **COST NOTE FOR THE IC AND OWNER.** Every observation above is a precision defect in CORRECTION 2's *commentary*, not in its *citations*. The artifact's actual job — proving every byte cut from `doctrine.md` either relocated (and is cited) or was already redundant (and is cited) — I verified end to end this session, including the row that halted twice. A third halt would buy prose polish at the cost of another full IC-write plus Safety-verify cycle, on an incident whose substantive work has now passed three independent verifications unchanged.

### The officer's own summary of why this is a pass — verbatim

> I went looking for the fourth instance of the class and did not find one. [...]
> Every one of the 19 anchors returns exactly one hit — I extracted the commands
> programmatically [...] rather than retyping them, so a transcription
> normalization on my side could not mask a broken anchor. [...] Row 17 is
> genuinely fixed. All three clauses are homed, and the second anchor
> `keystroke, not a record` resolves to `51dd073:126` — the exact sentence halt 2
> said CORRECTION 1 had wrongly excluded. [...] The observations are real and I
> would not have written them if they were not, but each one is a sentence in the
> entry's prose reasoning that is looser than the citation it accompanies. None of
> them leaves a cut byte unaccounted, none of them can rot, and none of them would
> mislead a later seat into a wrong measurement — which is the harm principle 15
> exists to prevent.

---

## Criteria state at pass

| # | Criterion | State |
|---|---|---|
| 1 | Hot path ≤ 36,864 B | **MET** — 22,121 + 14,596 = 36,717 B, 147 B headroom, re-measured at every verification |
| 2 | No field-lesson narrative in core | **MET** |
| 3 | 28 principle labels unchanged incl. `9b` | **MET** |
| 4 | 12 `##` headings unchanged (+ the `###` sub-heading) | **MET** |
| 5 | Guard green | **MET** — 12/12 against the new 37 kB budget |
| 6 | Nothing deleted without a home | **MET** — coverage half (all 22 rows, 100 % of deletions, no orphan) and citation half (19/19 anchors unique and substantively correct) |
| 7 | Command-point lesson in the appendix | **MET** — verified under `## Transfer of command` |
| 8 | Ratchet re-seated | **MET** — 37, derivation in the comment |
| 9 | Every named rule survives as a rule | **MET** — 13 rule greps, read in context, across three verifications |
| 10 | **[Owner]** end-to-end read | **Pending — the close gate** |
| 11 | Version bump atomic to 0.6.5 | **MET** |
| 12 | **[deploy period]** marker advances | Not verifiable this period |
