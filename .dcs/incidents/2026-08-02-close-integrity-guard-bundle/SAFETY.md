<!--
SAFETY.md -- the Safety Officer's verdict, copied in as returned, not
summarized or softened by the IC (forms.md). Accumulates every verdict
for this operational period, in order -- a multi-attempt period holds
more than one. Period 1 currently holds one verdict (attempt 1's halt);
attempt 2's verdict is appended here once returned.
-->

# SAFETY — Verdict Record

**Incident:** close-integrity-guard-bundle
**Period:** 1

## Attempt 1 verdict — HALT (2026-08-03T08:53:59+11:00)

```json
{
  "verdict": "halt",
  "refutations": [
    {
      "claim": "S2: 'load-bearing-term census added with its own banner' — satisfying criterion 6's requirement that the census cover 'the shipped payload's current content', and IAP verification plan item 4's 'non-vacuity everywhere a mechanism could pass untested: ... the term census's empty-list guard'.",
      "evidence": "The census check is a tautology: it can never go red. `tests/test_doctrine_integrity.py:364` sets `SHIPPED_DIRS = [\"dcs\", \"agents\", \"skills\", \"bin\", \"docs\", \"tests\"]` and `:226` sets `EXCLUDED_DIRS = {\".git\", \"node_modules\", \"__pycache__\"}`, so `candidates` includes `tests/test_doctrine_integrity.py` itself. `_term_census_texts` (:553-562) is built from that same `candidates` list, and `_TERM_CENSUS` (:521-549) stores every term as a literal string inside that very file. Therefore `if not any(term in t for t in _term_census_texts)` (:565-568) is never true. Measured by me: all 9/9 census terms are satisfied by `tests/test_doctrine_integrity.py`'s own text alone, so `_term_missing` is provably always `[]` — the check passes even if every other file in the package were emptied. This is not merely theoretical: across the entire scanned population, `WORKFLOW_BUDGET_LINES` and `HOT_PATH_BUDGET_KB` occur in exactly ONE file (that same file, others=0), so for 2 of 9 terms the census is today measuring nothing but its own list entry. Compounding it, both those entries' mandatory reason reads 'CLAUDE.md's coding-rules section cites it by this exact name' — but `CLAUDE.md` is absent from `SHIPPED_FILES` (:365) and is never scanned, so the check cannot observe the relationship its own rationale asserts. The delivered `bool(_TERM_CENSUS)` degeneracy guard (:551-553) guards only against an empty list; it does not address this. This is precisely the refutation the incident's own IAP names at verification plan item 9: 'any of those six properties enforced only by a case that would pass with the mechanism deleted.'"
    },
    {
      "claim": "IAP verification plan item 9's definition of done — 'a close in any project shipping DCS 0.8.0 runs an unconditional, fail-closed check' — together with criterion 14's self-application (plan item 8 invites me to 'note if you see anything that would make it fail').",
      "evidence": "I ran `python dcs/tools/record_integrity.py .dcs/incidents/2026-08-02-close-integrity-guard-bundle`. It exits 1 on: `criterion 1: FINDING: .../214-LOG.md:30: token '3df43fc8' (keyword 'sha') does not resolve to a git object`. That token sits in the Planning Chief re-spawn entry, which quotes `\"sha 3df43fc8\" is a file-content digest, not a commit`. Neither suppression can reach it: the entry's first line is not a stamp, and its body does not carry the literal `RECORD-CORRECTION:` (line 31's text is `RECORD CORRECTION`, no hyphen and no colon, and is a different entry regardless). `214-LOG.md` is append-only by its own header ('Never edit or delete a past entry'), and suppression (b) is entry-scoped — `_entry_containing()` then `\"RECORD-CORRECTION:\" in body` at `dcs/tools/record_integrity.py:306-314` — so appending a new correction entry cannot suppress a token in an earlier one. The finding is permanent and unremediable. `dcs/workflows/close.md` step 5a.1b is unconditional and fail-closed with no override ('exit 1 (findings) or 2 (environment error) is fail-closed — stop, do not merge'), so this incident cannot close through the gate it ships. Criterion 1's tool behaviour is per spec here — the `sha` false-positive class was ratified at command point 2 — so what fails is the end-to-end close, not the tool; but the same trap ships to every installing project with no documented operator remedy for an already-written append-only log."
    }
  ],
  "advisories": [
    {
      "finding": "Date-pin boundary is one day later than both criteria's prose describes, and no test covers the boundary. `dcs/tools/record_integrity.py:515` sets `SAFETY_FENCE_EFFECTIVE_DATE = \"2026-08-03\"` and `:653` treats `dir_date <= pin` as out of scope, so the real in-scope set is 'dated 2026-08-04 or later'. Criterion 3 says 'strictly after 2026-08-02' and criterion 6 says 'post-2026-08-02'. The 202's fuller text and both taskings explicitly ratify the 2026-08-03 value with the exclusive comparison, so this is not a deviation from tasking — but an incident directory dated exactly 2026-08-03 (today) silently escapes BOTH new date-scoped checks, and the only in-scope fixture is dated 2026-08-10, so nothing tests the edge. Separately, `_ne_dir_in_scope`'s docstring says it 'mirrors `_PM_EFFECTIVE_DATE`'s precedent in check 22', but check 22 uses `>= _PM_EFFECTIVE_DATE` (inclusive of the pin) while this uses `> pin` (exclusive) — opposite conventions under the same `EFFECTIVE_DATE` name.",
      "fix": "Either move both constants to \"2026-08-02\" and keep the exclusive comparison (which then literally matches 'strictly after 2026-08-02' and matches check 22's semantics), or keep 2026-08-03 and rename the constants to say what they mean (e.g. `LAST_OUT_OF_SCOPE_DATE`). Either way add a boundary fixture dated exactly one day after the pin, and correct the docstring's 'mirrors check 22's precedent' claim."
    },
    {
      "finding": "IAP verification plan item 3 describes the fence trap as 'checked as a PAIR', implying the real `record-integrity-corrections/SAFETY.md` half proves trap-resistance. It does not: that run prints `criterion 3: ... on or before SAFETY_FENCE_EFFECTIVE_DATE 2026-08-03 -- SAFETY.md check out of scope` and returns before `SAFETY.md` is ever opened. Trap-resistance is genuinely proven by the `prose-fence` fixture alone.",
      "fix": "In the AAR, state the real half as an exit-0 regression guard and credit trap-resistance to the `prose-fence` fixture only."
    },
    {
      "finding": "`safety_fence_findings()` validates EVERY JSON fence in `SAFETY.md` against schemas.md #5, not only the verdict fence, including 'unrecognized key' findings. 2 real corpus SAFETY.md files already carry more than one JSON fence, and one carries the non-#5 key `checks_run`. All pre-pin so out of scope today, but a post-pin SAFETY.md that quotes any other JSON block would fail-close the merge on an unrecognized key.",
      "fix": "Scope the schema check to fences that look like a verdict (e.g. those carrying `verdict`), or downgrade 'unrecognized key' on non-verdict fences to a printed note."
    }
  ],
  "checked": [
    "Read `dcs/tools/record_integrity.py` in full (934 lines) and this incident's own `214-LOG.md` in full as primary sources.",
    "Ran all three suites myself, twice, from a clean tree: `test_dcs_gate.py` 100/100; `test_dcs_intake.py` 18/18; `test_doctrine_integrity.py` 152/152.",
    "Ran `release_provenance_check.py`: fails only on 'no git tag v0.8.0 exists', expected pre-publish state.",
    "Ran the original 201 repro pair against real corpus incidents (halt-enumeration-grammar-drift, record-integrity-corrections) with correct results on both.",
    "Re-measured every corpus figure in the tool's docstring with its own published command; all reproduced exactly.",
    "Ran the tool against this incident's own directory (criterion 14 sanity check) -- exit 1, permanent finding.",
    "Verified close.md step 5a.1a and step 5a.4 byte-identical to merge-base; verified no renumbering; verified all four external step-number citations unchanged.",
    "Regenerated both budgets with the guard's own methods; verified the relocated doctrine paragraph verbatim; verified principle numbering contiguous 1-16.",
    "Verified test-file section structure; verified check 10's CRLF candidates list unmodified; verified suppression (a) genuinely fixture-reached.",
    "Verified the fence-trap pair's real behavior; verified fixtures immutable; verified ship-no-project-facts; verified criterion 9's cross-file agreement; verified criterion 12's version/changelog.",
    "Cross-checked every touched file against the four declared territories -- zero forbidden-zone violations.",
    "Proved refutation 1 mechanically by extracting the real constants and computing per-term occurrence counts across the real scanned population."
  ]
}
```

**Disposition:** `dcs-commander` ruled `verdict_disposition: replan` at command point 4 (full ruling: `214-LOG.md`). 202-OBJECTIVES.md revised (attempt 2); both refutations addressed with a redesigned suppression mechanism and a corrected census scope, not a narrow patch. Advisories folded into the same revision (date-pin exact values, fence-field scoping) or deferred to the AAR (the "pair" framing correction).

## Attempt 2 verdict — PASS (2026-08-03T13:24:29+11:00)

```json
{
  "verdict": "pass",
  "refutations": [],
  "advisories": [
    {
      "finding": "The `suppressed-correction/` fixture does not exercise required behavior (i), despite two artifacts claiming it does. `tests/fixtures/record-integrity/suppressed-correction/uncorrected/214-LOG.md`'s header states both halves carry a mid-line mention \"to prove a mention alone (the discarded old design's trigger) suppresses nothing either way\", and `tests/test_doctrine_integrity.py:2452-2456`'s check text asserts \"the different entry's mid-line RECORD-CORRECTION: mention (not entry-initial) suppresses nothing (zero SUPPRESSED lines)\". Measured: mutating `correction_named_targets` to a body-anywhere test (defect (i) restored) and re-running both halves gives IDENTICAL results to the delivered design. The mention entry names no token in citation position, so it can authorize nothing under either rule. Behavior (i) IS correctly implemented (8 grammar probes) and discriminated by the real corpus, but nothing in the suite pins it.",
      "fix": "Add a citation-position token to the mention entry in BOTH halves, e.g. naming sha cafef00d1. A body-anywhere mutation would then suppress it in `uncorrected/`, reddening that case's zero-SUPPRESSED conjunct."
    },
    {
      "finding": "Two criterion-3 cases (prose-fence, boundary-pin) assert on conjuncts satisfied by unrelated noise: `_ri_rc != 0 and \"SAFETY.md\" in _ri_out` also holds because every fixture is untracked and criterion 2 always fires. prose-fence's case is vacuous for the fence check specifically; boundary-pin survives on its third conjunct only (verified: reverting the pin makes the suite's own predicate False).",
      "fix": "Filter to `criterion 3: FINDING` lines specifically, the same criterion-scoped filtering case (iv) already does."
    },
    {
      "finding": "Attempt 1's date-pin advisory was half-fixed: the boundary fixture was added, but the docstring at `tests/test_doctrine_integrity.py:416` still says the pin \"mirrors `_PM_EFFECTIVE_DATE`'s precedent in check 22\" while the comparison is deliberately the opposite sense (exclusive vs. check 22's inclusive) -- invites a future maintainer to 'align' them and reintroduce the off-by-one.",
      "fix": "State which property is mirrored (the unparseable-date disposition) and which is deliberately not (the comparison sense)."
    },
    {
      "finding": "S2's return claims the fixture pair 'differs by exactly one appended entry' -- true only of `214-LOG.md`; 8 other files differ in self-identifying labels, plus one IAP-APPROVED hash. Behaviorally sound, none of the other deltas touch criterion 1, but the phrasing is looser than the evidence.",
      "fix": "State it precisely in the AAR: 214-LOG.md byte-identical plus one appended entry; other files differ only in self-identifying labels."
    },
    {
      "finding": "202-OBJECTIVES.md criterion 1's '5 of 8 historical sha-keyword tokens are genuine commit citations across 4 incidents' claim has no regenerating command beside it (principle 15) -- re-measured and confirmed accurate, but un-regenerable as written.",
      "fix": "Append the command, or cite record_integrity.py's own docstring corpus block which already carries one."
    },
    {
      "finding": "Two informational notes for the queued RECORD-CORRECTION documentation follow-up (not a defect -- the IAP already declares this gap): (a) suppression is authorized by any hex token a correction entry names in citation position, so a correction entry that incidentally opens a new sentence with a genuine commit's hex would also clear that token file-wide -- a false-negative risk, explicitly inside criterion 1(b)'s 'distinguishing true from false corrections is out of scope by design' clause; (b) hot-path headroom is 17 bytes after this incident -- the next doctrine edit of any size reds the merge guard.",
      "fix": "When documenting the convention: instruct operators to name only the bad token in citation position, write any correct commit outside citation position. Track hot-path headroom as debt for the next doctrine-touching incident."
    }
  ],
  "checked": ["Full independent re-verification, all mutation-tested rather than inspected: both prior refutations resolved (real-corpus witnesses invert correctly, token-scoping bound holds); census fix structural (path-identity, not name-matching); date pin fix verified both directions with regression guards; verdict/non-verdict fence scoping verified both directions with live schema parsing; all three suites green from one post-both-specialists-write run (100/100, 18/18, 156/156); S3/S4's attempt-1 work re-derived from scratch (not cited by reference, since HEAD has no attempt-1 baseline commit to diff against) -- byte-identical close.md steps except the new 1b, doctrine principle 16 intact, forms.md's 9-count, README/CHANGELOG/VERSION all correct; zero forbidden-zone violations across the full attempt-2 touched-file set; disclosed prompt-injection incident independently verified as causing no actual tampering (corrected/214-LOG.md content confirmed intact, not blanked)."]
}
```

**Disposition:** Pass, no refutations -- period 1 complete. Advisories 1, 2, 3 (fixture/test precision) and 5 (202 regenerating command) folded into the integration commit by the IC directly, per `execute.md`'s advisory-handling clause (artifact edits inside already-granted territory, no fix-tasking needed). Advisories 4 and 6 carried into the AAR and the queued follow-up incident respectively -- both are documentation-precision notes, not code changes.
