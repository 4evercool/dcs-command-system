# SAFETY — Period 1 Verdict

**Incident:** revision-preservation-map
**Period:** 1

```json
{
  "verdict": "pass",
  "refutations": [],
  "advisories": [
    {
      "finding": "dcs/tools/preservation_map.py:4 — the module docstring cites 'incident revision-preservation-path'; the actual slug is 'revision-preservation-map'. I grepped the whole repo: this is the only occurrence of that string, so it resolves to no incident directory, no branch and no register row. The field-lesson citation guard passes it because it only checks that a slug-shaped identifier is present, not that it resolves.",
      "fix": "s/revision-preservation-path/revision-preservation-map/ in the docstring at line 4. Fold into the integration commit."
    },
    {
      "finding": "The incident's 214-LOG.md carries no specialist return entries at all. Its last line is '[2026-08-01T13:40:00+11:00] execute.md step 3.5: Owner chose standard Agent-tool fan-out...' — all three S1/S2/S3 returns that my tasking says are logged there are absent. My prompt pointed me at that file for 'full specialist evidence blocks'; they do not exist. (No verification depended on them — I re-derived everything from the repo — but the log is what a fresh session reads to resume losslessly.)",
      "fix": "IC appends the three specialist return entries (and the command-point-3 verdict entry) before close, per execute.md's logging steps."
    },
    {
      "finding": "preservation_map.py's output-disagreement branch (lines 210-216) — the false-fidelity defect the module docstring twice claims to close, citing AAR.md:82-89 — has no named test case. Section 22's in-memory forgery proof deletes the anchor line, exercising only the anchor-missing branch (199-204). I exercised the output branch by hand and it behaves correctly: a map whose anchor is present but whose self-reported `output` misdescribes the line is caught, as is an empty `output`. So the capability is real, just uncovered.",
      "fix": "Add one more forgery case in section 22 mutating the victim entry's `output` rather than the artifact text — same preserved_findings() comparator, no new fixture, ~6 lines."
    },
    {
      "finding": "preservation_map.py:180 and tests/test_doctrine_integrity.py:1939-1940 both cite 'check 18(f)' as the borrowed idiom. Check numbers in that file are the very thing the queued field-lesson-guard-vacuity incident will renumber (it owns the duplicate-20/mislabeled-21 fix), so these citations have a known expiry and carry no regenerating command beside them.",
      "fix": "Cite the idiom by its test name ('field guard negative proof') rather than by section number, or add `grep -n '^# --- [0-9]' tests/test_doctrine_integrity.py` beside the citation."
    },
    {
      "finding": "Hot-path headroom is now 50 B, not the 402 B the IAP planned against. I re-derived CRLF-normalized doctrine.md + schemas.md = 37838 B against the guard's own HOT_PATH_BUDGET_KB=37 (37888 B ceiling). In band, so criterion 6 is met — but S3 spent 352 of the 402 B, and the next hot-path sentence anyone adds breaches the budget.",
      "fix": "No action this period. Worth a note in the close/AAR so the next incident touching doctrine.md or schemas.md knows it must fund its own trim from the first byte."
    }
  ],
  "checked": [
    "git status --porcelain -uall and git diff --stat in C:\\DCS-wt\\revision-preservation-map — 5 modified files (dcs/README.md, doctrine-appendix.md, schemas.md, plan.md, test_doctrine_integrity.py) plus untracked dcs/tools/, tests/fixtures/preservation-map/, and the incident artifacts. Every path maps to exactly one specialist's IAP territory; no forbidden-zone violation found.",
    "Forbidden-zone sweep: git diff --name-only | grep -i gate empty, no agents/** in git status, no dcs/VERSION or package.json in the diff, git diff --stat dcs/references/doctrine.md empty — S3's 'doctrine.md untouched' claim independently confirmed, not accepted.",
    "CRITERION 1 — read dcs/workflows/plan.md:215-221 directly: the Preservation-map duty is pre-stamp, requires a literal anchor plus the command output per pairing (not a bare assertion), specifies the indented-fence 214-LOG.md placement against dcs_gate.py's grammar, and makes a non-zero exit a hard stop.",
    "CRITERION 1 trim ledger, THE CHECK THE IAP CALLED MOST IMPORTANT — ran git diff --word-diff=plain --word-diff-regex='\\S+' dcs/workflows/plan.md. Output contains ZERO removed-word runs; every change is either a pure addition or a line rejoin. S2's 'zero words changed, zero content removed' claim is literally true at word granularity. plan.md is 249 lines against the 250 ceiling.",
    "CRITERION 2 — ran criterion 2's own named command grep -n \"preservation\" dcs/references/schemas.md: matches at lines 171 and 174 describing and exemplifying the shape. Heading at line 167 is byte-exact '## 9. Preservation map (6c amendment pre-stamp proof)'. Grepped section 9's body (lines 167-200) for 'Returned by' — 0 occurrences, so it correctly stays out of checks 18/20's contract population.",
    "CRITERION 3 — compared grep -n '^# --- [0-9]' against HEAD and working tree: every pre-existing label sits at an identical line number, both '# --- 20.' headings and the mislabeled '# --- 21.' present unchanged, exactly one new label 22 added.",
    "CRITERION 3, stronger than the grep — proved insert-only in Python by splitting both versions on newlines: old[:1874] == new[:1874] is True AND old[1874:] == new[1874+152:] is True. Everything outside the 152-line insert is byte-identical, so the duplicate-20/mislabeled-21 defect is provably untouched. git diff -U0 shows a single hunk, @@ -1874,0 +1875,152 @@, zero deletions.",
    "CRITERION 4 — ran python dcs/tools/preservation_map.py against all three fixtures myself: clean -> exit 0, dropped-criterion -> exit 1 printing 'criterion 5: preserved anchor does not occur in IAP.md's current bytes', no-map -> exit 1 printing the missing-block finding. All three discriminate as claimed.",
    "CRITERION 4 dual reading — imported the module and called both comparators on the same fixture: prefix_coverage('dropped-criterion') == [] (pre-fix blindness) while verify('dropped-criterion') names criterion 5. Confirmed in the suite output that these are two SEPARATELY NAMED cases, not one aggregate assertion.",
    "CRITERION 4 frozen-fixture requirement (principle 15) — grepped all three fixture trees for git refs, HEAD, commit, branch, origin/ and 7-40 char hex. The only hex hits are fixture-internal fake stamps (aaaa1111bbbb, cccc2222dddd) that reference nothing in this repo's history. No moving ref anywhere. Also confirmed no 'schemas.md' citation inside any fixture, per the IAP's neutral-fiction risk.",
    "CRITERION 5 — verified BOTH of W4's line-range citations by reading the cited source. .dcs/incidents/2026-07-27-register-field-repair-path/AAR.md:67-72 is exactly the pinned-hash-cannot-reach-.dcs/** passage about silently dropping 'Criterion 5, answered'; AAR.md:82-89 is exactly the 'unverified claim of fidelity' passage. vault/Meta/building-dcs-lessons.md:631 is '## 18. A revision that fixes one criterion can silently unfix another'. All three resolve.",
    "CRITERION 5, extra — verified the appendix's abandoned-branch claim: git rev-parse dcs/revision-preservation-map-abandoned-2026-07-31 returns 497dcd47a12795a6..., so the cited '@ 497dcd4' is genuinely that branch's tip, not a stale hash.",
    "CRITERION 6 — re-derived the hot path myself in Python with CRLF normalization (the guard's own check-7 method, not a bare wc -c): doctrine.md 23876 + schemas.md 13962 = 37838 B, inside the 36865-37888 band, against HOT_PATH_BUDGET_KB=37 read from tests/test_doctrine_integrity.py:212. S3's reported 37838 B matches my own measurement.",
    "CRITERION 7 — ran every suite myself: test_dcs_gate.py 100/100, test_dcs_intake.py 18/18, test_doctrine_integrity.py 132/132 (exit 0), and the extra tests/test_dcs_cli.py 14/14 (exit 0). Read package.json's test script to confirm npm test really does run all three. The claimed 132/100/18 numbers had not drifted.",
    "SCHEMAS.MD COMPRESSION AUDIT (S3's trim ledger, the second half of the IAP's manual check) — 98 removed-word runs, so I reviewed the word-diff line by line across all 35 affected lines. Every removal is verbosity, example detail, or redundancy; I found no rule whose normative content disappeared. Two cells drop a bare 'must be' ('must be disjoint' -> 'disjoint'; 'Must be a subset' -> 'A subset') but each retains its enforcing clause, so the rule still stands.",
    "SCHEMAS.MD structural loss check — the failure mode compression could hide that no guard catches: a deleted field-table row. Parsed both versions and compared rows per section. Sections 1-7 all identical counts and identical field names (5/11/5/5/4/10/8); section 9 adds 9 new rows. Zero rows lost.",
    "SCHEMAS.MD pure-deletion check — computed +/- per hunk on git diff -U0. Of 25 hunks, 24 are balanced replacements and the single net-deletion hunk (@@ -3,3 +3 @@) is the intro reflowing 3 lines to 1 with all clauses retained. No paragraph or sentence was dropped outright.",
    "MECHANISM SPOT-CHECK (the tasking told me not to trust a passing test) — read dcs/tools/preservation_map.py in full. verify() reads 202-OBJECTIVES.md and 214-LOG.md from disk, resolves each preserved entry's artifact through _artifact_valid() (screened-set fnmatch plus a relative_to() containment check against path escape), reads the artifact's current bytes, and only then calls preserved_findings(). The map's self-reported output is never the proof; it is compared against the line the anchor is actually found on. T2 is genuinely implemented, not asserted.",
    "ADVERSARIAL PROBE of the false-fidelity branch — hand-built three entries against an in-memory artifact: honest output -> [], lying output with the anchor still present -> correctly reports 'preserved output disagrees ... (reported ..., found ...)', empty output -> also caught. The capability the docstring claims is real; it is simply untested (advisory 3).",
    "INVOCATION literal trap — imported the module and asserted pm.INVOCATION in plan_text: True. The literal python \"$HOME/.claude/dcs/tools/preservation_map.py\" <incident_dir> sits unbroken on plan.md:218, and the test's carrier case reads the constant from the module rather than retyping it, so the two copies cannot drift.",
    "OPERATIONAL-HARM CHECK on the new documented command — plan.md now instructs running $HOME/.claude/dcs/tools/preservation_map.py, so I verified it will actually exist there: install.ps1:7 robocopies dcs/ with /E, install.sh:10-11 rsyncs dcs/ recursively, and package.json's files whitelist includes 'dcs/'. The command resolves post-install; this is not a rollback-card-class defect.",
    "INTERACTION CHECK between S1's new import and the deploy witness — importing preservation_map.py creates dcs/tools/__pycache__ in the repo tree. Read tests/payload_check.py:96-110: EXCLUDED_DIRS includes __pycache__ and iter_files() filters .pyc/.pyo unconditionally on both sides, and package.json excludes '!**/__pycache__'. No false repo-only finding will result.",
    "ENCODING/BOM sweep on all six touched files in Python: zero CRLF, zero BOM, all decode as UTF-8 — the CLAUDE.md Set-Content hazard did not bite.",
    "Read 202-OBJECTIVES.md and IAP.md in full rather than working from the summary in my tasking; confirmed the acceptance criteria I verified are the ones actually written, including the out-of-scope list.",
    "Read the incident's 214-LOG.md in full (37 lines) — which is how I found that the specialist return entries my tasking referred to are absent (advisory 2). Confirmed no SAFETY.md exists in the incident directory, so this is a first verdict, not a fix-tasking re-verification; nothing was cited by reference."
  ]
}
```

**Post-verdict disposition (command point 4, dcs-commander, model fable): close.**
Rationale: pass with zero refutations; all 8 criteria independently
re-verified; the 201's goal is fully delivered and ships standalone; no
proposed next objectives exist. Advisories 1, 3, and 4 folded into the
integration commit (docstring typo fixed, a false-fidelity forgery case
added to section 22, section-number citations replaced with
name/regenerating-command citations); all four suites re-run green
afterward (133/133 integrity, up one for the new case; 100/100 gate;
18/18 intake; 14/14 cli). Advisory 2 (log hygiene) resolved by this
entry and the specialist-return entries appended to `214-LOG.md`.
Advisory 5 (50 B hot-path headroom) recorded in the AAR and
`vault/Backlog.md`, not actioned this period.
