<!--
201-BRIEF.md — written by the IC from dcs-situation-analyst findings, once,
at the stem (/dcs-new). Never edited after typing is confirmed except to
append a note if a later period's assessment reveals the original blast
radius was wrong (append, don't rewrite — 214-LOG.md is the append-only
one, but this file's Symptom/Evidence should stay a true record of what was
known at intake).
-->

# 201 — Incident Brief

**Incident:** field-lesson-guard-bare-date-weakening
**Opened:** 2026-08-04
**Type:** 3

## Symptom

The `field-lesson-guard-vacuity` repair (commit `bcf9468`, MERGED via
`8f6b1ea`/`64a4a01`, deploy HELD by Owner direction on this very defect)
silently widened check 20a's identifier grammar `_FL_ID_RE`
(`tests/test_doctrine_integrity.py:2057-2058`) to accept a bare same-line
`YYYY-MM-DD` date as a sufficient field-lesson identifier. A
dated-but-slugless claim ("Field lesson 2026-09-01: X happened") is now
green where the pre-repair check went red — the unverifiable-claim shape
the guard was built to catch (the v0.5.10 false-lesson defect) is
representable again. The guard's own docstring
(`tests/test_doctrine_integrity.py:2033-2036`) still promises the strict
slug/version/predates rule, so the check no longer does what it says.
The widening was undisclosed in the parent's commit message, AAR, and
SAFETY.md alike (PASS, 0 refutations), and its self-tests never covered
the same-line bare-date-only case; it was found only by an
Owner-directed post-close review on 2026-08-04. **Folded in by explicit
ESG decision (eighteenth `/dcs-esg`, 2026-08-04, rank 1):**
`vault/Backlog.md` item 31 — `RECORD-CORRECTION:` is a fourth
mechanically-parsed sentinel (`dcs/tools/record_integrity.py:419`)
invisible to check 12's census (`_SENTINEL_TOKENS`,
`tests/test_doctrine_integrity.py:728`, still names only three tokens)
and undocumented in shipped prose. Same file, same held deploy train.
Two defects ride together here by Owner-chaired ESG decision, not by
stem oversight — decomposition was considered and rejected there.

## Evidence

- `tests/test_doctrine_integrity.py:2057-2058` — current regex:
  `` _FL_ID_RE = re.compile(r"incident `[a-z0-9-]+`|v\d+\.\d+\.\d+|predates self-hosting|\d{4}-\d{2}-\d{2}", re.I) `` —
  the `\d{4}-\d{2}-\d{2}` alternative accepts any bare date, no slug
  required (source: analyst A, file read).
- Live regex demonstration (analyst A, python one-liner): for
  `line = 'Field lesson 2026-07-23: users reported a crash on save.'`,
  `_FL_LINE_RE.search(line)` and `_FL_ID_RE.search(line)` are both
  truthy via the bare date alone — check 20a would not flag the line
  despite it carrying no slug, version, or predates-note.
- `git show bcf9468 -- tests/test_doctrine_integrity.py` — the same
  commit broadened `_FL_LINE_RE` (from requiring a same-line date to
  bare `[Ff]ield[- ]lesson`) and added the `|\d{4}-\d{2}-\d{2}`
  alternative to `_FL_ID_RE` (source: analyst A, git history).
- `git stash show -p stash@{0}` — a pre-existing strict draft with
  `_FL_LINE_RE` broadened identically but `_FL_ID_RE` left strict (no
  bare-date branch): the non-weakening alternative was drafted and
  available, not taken (source: analyst A; kept intact as prior art per
  the register row).
- 3-site measurement (analyst A, re-running check 20a's loop with the
  strict `_FL_ID_RE` over the shipped `_FL_FILES`; regenerate with the
  strict-variant script named in the register row's Intake source):
  exactly 3 real citation sites pass today only via the bare-date
  allowance — `doctrine-appendix.md:414`, `plan.md:57-58`,
  `execute.md:231` — each already carrying a section-name/W-entry
  cross-reference. The parent AAR's "false-positive storm" justification
  measures to these 3 sites, not a storm.
- The bare-date acceptance IS needed for the *next-line* lookahead
  (multi-line citations, fixture
  `tests/fixtures/field-lesson-guard/multiline-claim.md`) — the fix must
  keep it there while dropping same-line sufficiency, or reword the 3
  sites to strict forms (source: register row + analyst A fixture read).
- Companion defects named by the register row, same act:
  the docstring falsehood (`tests/test_doctrine_integrity.py:2033-2036`),
  and identifier-stuffing the broadened entry filter forced into
  convention prose (`doctrine-appendix.md:11,13,669` — "(v0.5.0)"/
  "(v0.6.9)" jammed mid-sentence into non-claims the old date-filter
  deliberately excluded).
- `python tests/test_doctrine_integrity.py` (analyst A run, main
  checkout): exits 0 — the weakening is live and silently accepted; the
  suite's own pass count is a moving fact, read from the run, not from
  this brief (principle 15).
- **Item 31 half:** `tests/test_doctrine_integrity.py:728` —
  `_SENTINEL_TOKENS = ("SAFETY-HALT:", "SAFETY-PASS:", "IAP-APPROVED:")`;
  `dcs/tools/record_integrity.py:419` —
  `correction_re = re.compile(dcs_gate.ENTRY_PREFIX + r"RECORD-CORRECTION:")`
  (source: analyst B, file reads).
- A naive tuple-only widening fails on arrival: check 12 sub-check (f)
  (`tests/test_doctrine_integrity.py:816-817`) requires every token in
  `_SENTINEL_TOKENS` to appear literally in `doctrine.md`, which has
  zero `RECORD-CORRECTION:` hits today; sub-check (d) (`:790-806`)
  validates fenced sentinel-shaped lines via `dcs_gate.py`'s
  `sentinel_of()`, which has no `RECORD-CORRECTION:` recognizer at all
  (source: analyst B, code read + grep).
- The three original sentinels' convention is documented twice in
  `dcs/references/forms.md:52-81`; `RECORD-CORRECTION:` is absent from
  both passages and from `doctrine.md` entirely; its only shipped-prose
  mention is narrative (`doctrine-appendix.md:797`) (source: analyst B,
  grep).
- No existing artifact is newly swept in by the census widening: check
  12's population walk is `(REPO / "dcs").rglob("*.md")` only
  (`tests/test_doctrine_integrity.py:759-763`) — all real
  `RECORD-CORRECTION:` entries live under `.dcs/incidents/**`, outside
  the scan (source: analyst B, code read + grep).
- Hot-path budget pressure: `doctrine.md` + `schemas.md` measured at
  37,722 B against the 37 KB ceiling (`HOT_PATH_BUDGET_KB = 37`,
  `tests/test_doctrine_integrity.py:212`) — 166 B of slack as of
  `efc3244`; it moves — regenerate with
  `python -c "import os;print(os.path.getsize('dcs/references/doctrine.md')+os.path.getsize('dcs/references/schemas.md'))"`.
  Any doctrine.md sentence for item 31 must fit or be funded by a trim
  (source: analyst B, measurement).
- Check 12 has no fixture-based self-test scaffold today (unlike check
  20's `tests/fixtures/field-lesson-guard/`) — whether to add one is a
  Planning Chief decision (source: analyst B, fixture glob).

## Reproduction path

1. Open `tests/test_doctrine_integrity.py`, confirm `_FL_ID_RE` at
   :2057-2058 includes the `\d{4}-\d{2}-\d{2}` alternative.
2. In a Python shell, compile the shipped `_FL_LINE_RE`/`_FL_ID_RE` and
   evaluate them against
   `'Field lesson 2026-07-23: an entire IAP review cycle was consumed.'` —
   both match; a slugless, versionless, non-predates line is treated as
   adequately cited.
3. Run `python tests/test_doctrine_integrity.py` from the repo root —
   exits 0 with the weakening live; re-run the check-20a loop with the
   strict regex (no bare-date branch, per `stash@{0}`'s draft) to see
   the 3 sites that pass only via the allowance.
4. Item 31 half: `grep -rn RECORD-CORRECTION dcs/ tests/test_doctrine_integrity.py` —
   present in shipped code and appendix narrative, absent from
   `_SENTINEL_TOKENS` and from `forms.md`/`doctrine.md`'s convention
   passages; no test fails on this today.

## Blast radius (best guess at intake)

- `tests/test_doctrine_integrity.py` — check 20a `_FL_ID_RE` + docstring;
  check 12 `_SENTINEL_TOKENS` (+ sub-checks (d)/(f) interactions)
- `tests/fixtures/field-lesson-guard/**` — new same-line bare-date-only
  fixture; existing fixtures must keep passing
- `dcs/references/doctrine-appendix.md` — citation site :414; the
  identifier-stuffing sites :11,13,669
- `dcs/workflows/plan.md` — citation site :57-58
- `dcs/workflows/execute.md` — citation site :231
- `dcs/references/forms.md` and/or `dcs/references/doctrine.md` —
  documenting `RECORD-CORRECTION:` as the fourth sentinel (doctrine.md
  needs the literal token if `_SENTINEL_TOKENS` widens, per sub-check (f);
  hot-path budget applies)
- possibly `dcs/hooks/dcs_gate.py` — only if the chosen design gives
  `sentinel_of()` a `RECORD-CORRECTION:` recognizer rather than
  documenting the fenced-line landmine around it (Planning Chief
  decision; touching the hook would revisit typing — see rationale)

## Prior art

Direct incident chain: v0.5.10 shipped a false field-lesson claim
(commit `0798fb1`, corrected v0.5.11; provenance in
`.dcs/incidents/2026-07-31-field-lesson-citations/201-BRIEF.md`) →
incident `field-lesson-citations` built check 20 to make recurrence
mechanically detectable → incident `field-lesson-guard-vacuity`
(2026-08-04, MERGED, deploy HELD) found check 20 vacuous and repaired it,
but the repair reintroduced the v0.5.10 shape via the bare-date branch —
this incident. The strict alternative sits drafted in `stash@{0}` (keep
intact — it is prior art, and the register row's measurement script
derives from it). Item 31 traces to incident
`close-integrity-guard-bundle` (merge `779773b`), which introduced the
fourth sentinel in code without updating check 12 or shipped prose — an
unassigned follow-up the `record-integrity-corrections` register row
owed, discharged by this fold. Same defect class (a prose/grammar guard
drifting from its own enforcement code) recurs across the repo:
`schema-citation-guard`, `check-14-hardening` (`vault/Backlog.md` items
15-16). ESG scoping: `vault/Meta/ESG-sessions/eighteenth-dcs-esg-2026-08-04.md`;
register row: `.dcs/esg/REGISTER.md` (id `field-lesson-guard-bare-date-weakening`).

## Type + rationale

**Proposed type:** 1
**Rationale (as proposed):** Edits the merge-time enforcement mechanism
itself (`tests/test_doctrine_integrity.py` checks 20 and 12) plus
doctrine/forms prose against a measured 166 B hot-path margin; CLAUDE.md's
enforcement-mechanism rule and the parent incident's Owner-confirmed
Type 1 in the same file both pointed to Type 1.
**Owner confirmation:** overridden to Type 3 — Owner's call at the typing
gate (2026-08-04, `AskUserQuestion`): Type 3 ceremony (IC + Planning
Chief + specialists + Safety Officer, no Logistics Chief), still fully
gated with Owner IAP approval unless the Delegation covers it. Recorded
without re-litigation per the IC-proposes/Owner-decides rule. If
planning discovers the fix must touch `dcs/hooks/dcs_gate.py` itself
(the `sentinel_of()` option in the blast radius), that is a scope change
warranting a fresh typing look, not a silent continuation.

## Intake source (for /dcs-close to route back to)

Register row `field-lesson-guard-bare-date-weakening`
(`.dcs/esg/REGISTER.md`, rank 1, H, eighteenth `/dcs-esg` 2026-08-04),
itself from the Owner-directed post-close review of
`field-lesson-guard-vacuity` (2026-08-04); carries `vault/Backlog.md`
item 31 folded in (fold recorded in the Backlog entry and the ESG
session note). Gates the held deploy of its parent — fix rides the same
train.
