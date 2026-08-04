<!--
201-BRIEF.md — written by the IC from dcs-situation-analyst findings, once,
at the stem (/dcs-new). Never edited after typing is confirmed except to
append a note if a later period's assessment reveals the original blast
radius was wrong (append, don't rewrite — 214-LOG.md is the append-only
one, but this file's Symptom/Evidence should stay a true record of what was
known at intake).
-->

# 201 — Incident Brief

**Incident:** field-lesson-guard-vacuity
**Opened:** 2026-08-04
**Type:** 1

## Symptom

Check 20 in `tests/test_doctrine_integrity.py` (the "field-lesson citation guard," shipped by incident `field-lesson-citations` at commit `710cf52`) is structurally vacuous for the defect class it was written to catch. The line filter `_FL_LINE_RE` (line 2048) requires a YYYY-MM-DD date on the same physical line as "field lesson" — every undated mention passes by inspection because it is never matched. The historic v0.5.10 false-lesson defect was an undated claim: the guard is blind to its own motivating case. Additionally: the file list `_FL_FILES` is a hard-coded 6-file enumeration that omits known field-lesson sites (`dcs/workflows/execute.md`, `dcs/workflows/plan.md`); two sections share the number `--- 20.` (lines 1975 and 2032); and the guard's multi-line follow-up check (lines 2060–2068) is reachable only after `_FL_LINE_RE` already matched — for the cited multi-line case (`202-OBJECTIVES.md:33-34` where "field lesson" and date are on different lines), it never fires.

## Evidence

- `_FL_LINE_RE` at `tests/test_doctrine_integrity.py:2048` — `re.compile(r'[Ff]ield lesson.*\d{4}-\d{2}-\d{2}', re.I)` requires a date on the same physical line; any "field lesson" mention without a date on that line never enters the guard at all (source: code inspection, both analysts).
- `doctrine-appendix.md:1` — "Provenance, field lessons, background": undated, never checked (source: grep for "field lesson" in doctrine-appendix.md, analyst 1).
- `dcs/workflows/plan.md:57-58` — "field lesson 2026-07-23" — this file is NOT in `_FL_FILES` at all (the list contains `new.md`, `close.md`, `deploy.md` but omits `plan.md` and `execute.md`) (source: code inspection, analyst 1).
- `dcs/workflows/execute.md:231` — "field lesson 2026-07-24" — also omitted from `_FL_FILES` (source: code inspection, analyst 1).
- `dcs/templates/202-OBJECTIVES.md:33-34` — "field lesson," on line 33 (no date), "2026-07-22, predates self-hosting" on line 34 (no "field lesson" phrase). Neither line matches `_FL_LINE_RE`. The multi-line check at lines 2062–2068 fires only after `_FL_LINE_RE` already matched, so this pair is never inspected. The comment at lines 2060–2061 explicitly cites this case as the multi-line form the guard handles — but the guard cannot reach it (source: code inspection, both analysts).
- `tests/test_doctrine_integrity.py:1975` and `:2032` — two sections both numbered `--- 20.`: the inbound field-presence guard and the field-lesson citation guard share the same section number (source: code inspection, both analysts).
- `_FL_FILES` at lines 2037–2044 — a hard-coded 6-file enumeration: `doctrine-appendix.md`, `deploy.md`, `new.md`, `close.md`, `202-OBJECTIVES.md`, `REGISTER.md`. All six exist; all currently-caught lines carry valid identifiers, so check 20 passes vacuously — not because the guard would catch a new undated violation, but because no current line triggers the vacuity path (source: code inspection, analyst 2).
- `vault/Post-mortems/deepseek-period-review.md` §A.2 (lines 40-43) — external review of the 2026-07-29 → 07-31 period confirmed: "Check 20 (field-lesson citation guard) is largely vacuous … every undated claim — the shape of the historic v0.5.10 false-lesson defect — is never inspected. The multi-line form its own comment cites (`dcs/templates/202-OBJECTIVES.md:33-34`) is unreachable by the code. Also two sections both numbered `--- 20.` in that file." (source: vault post-mortem, both analysts).
- `.dcs/esg/REGISTER.md` line 152 — incident already queued as `field-lesson-guard-vacuity`, rank 4, priority M, status QUEUED, with prior art noted: "stash@{0} holds an identifier-based check-20 draft, kept intact" (source: register, both analysts).
- `vault/Decisions/non-anthropic-hardening.md` — broader principle: "Every rule enforced by a mechanism held … Every rule that lived only in doctrine prose broke." No mechanism validates doctrine field-lesson claims against actual guard coverage (source: vault decision record, analyst 1).

## Reproduction path

1. Open `C:\DCS\tests\test_doctrine_integrity.py` at lines 2048–2068.
2. Observe that `_FL_LINE_RE` requires both "field lesson" AND a YYYY-MM-DD date **on the same physical line**.
3. Observe that the next-line check (lines 2060–2068) is inside the branch gated by `_FL_LINE_RE` matching the current line — a multi-line citation where "field lesson" is on line N and the date on line N+1 never enters this branch.
4. Confirm the guard cannot catch the v0.5.10 false-lesson defect class: undated "field lesson" claims are invisible.
5. Run `python tests/test_doctrine_integrity.py` — check 20 passes because all currently-inspected lines happen to carry valid identifiers, not because the guard would catch a new undated violation.
6. Observe two sections both numbered `--- 20.` at lines 1975 and 2032.

## Blast radius (best guess at intake)

- `C:\DCS\tests\test_doctrine_integrity.py` — lines 2032–2073 (check 20, the field-lesson citation guard) and lines 1975–2030 (check 20's inbound field-presence sibling, sharing the same section number). Line 2226 (comment noting section numbers will shift when this defect is fixed).
- `C:\DCS\dcs\references\doctrine-appendix.md` — field-lesson mentions without dates on the same line that pass uninspected (lines 1, 13, 669, 731).
- `C:\DCS\dcs\workflows\plan.md` — field-lesson mentions not covered by `_FL_FILES` (lines 57–58).
- `C:\DCS\dcs\workflows\execute.md` — field-lesson mention not covered by `_FL_FILES` (line 231).
- `C:\DCS\dcs\templates\202-OBJECTIVES.md` — multi-line forms unreachable by the current guard (lines 33–34, 44–46).

## Prior art

- Original discovery: `vault/Post-mortems/deepseek-period-review.md` §A.2 (2026-08-01) — external review of the 2026-07-29 → 07-31 period found check 20 vacuous.
- Queued as register row `field-lesson-guard-vacuity` (rank 4, QUEUED) at the same act (`vault/Meta/ESG-sessions/period-review-queue-2026-08-01.md`).
- Prior art stash: the period-review working tree contained an unlanded check-20 draft in `stash@{0}` that used identifier-based matching instead of date-proximity; rescued and committed at the fifteenth `/dcs-esg` (commit `064bd5b`) as an explicit prior-art reference rather than applied, per REGISTER.md Notes entry.
- The incident `field-lesson-citations` itself (commit `710cf52`, 2026-07-31, AAR at `.dcs/incidents/2026-07-31-field-lesson-citations/AAR.md`) shipped check 20 as part of a broader effort to make field-lesson citations verifiable — the vacuity was a latent defect in the guard's design, not a degradation after the fact.
- Related meta-lesson: `doctrine-appendix.md`, Principle 16 — "a mechanism that checks itself is not a check" (from incident `close-integrity-guard-bundle`, 2026-08-02/03), directly applicable to check 20's own lack of a self-test.

## Type + rationale

**Proposed type:** 1
**Rationale:** Change to the merge-time enforcement mechanism itself (`tests/test_doctrine_integrity.py` check 20) with a verified 5-file blast radius and a guard-redesign whose wrong fix re-ships the vacuity defect class — Type 1 per the project's enforcement-mechanism rule (CLAUDE.md: "dcs/hooks/dcs_gate.py, the tests that guard it, or the installer are Type 1 — they are the enforcement mechanism itself") and type-up guidance.
**Owner confirmation:** confirmed as proposed (Type 1)

## Intake source (for /dcs-close to route back to)

`.dcs/esg/REGISTER.md` row `field-lesson-guard-vacuity` (rank 4, QUEUED, priority M), opened from the `deepseek-period-review.md` §A.2 finding.
