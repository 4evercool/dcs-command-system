<!--
201-BRIEF.md — written by the IC from dcs-situation-analyst findings, once,
at the stem (/dcs-new). Never edited after typing is confirmed except to
append a note if a later period's assessment reveals the original blast
radius was wrong (append, don't rewrite — 214-LOG.md is the append-only
one, but this file's Symptom/Evidence should stay a true record of what was
known at intake).
-->

# 201 — Incident Brief

**Incident:** decomposition-backlog-routing
**Opened:** 2026-07-28
**Type:** 3

## Symptom

`new.md` step 4a's decomposition check and `esg.md` step 2's intake-sweep
decision clusters both funnel every defect they touch into
`.dcs/esg/REGISTER.md` as a first-class `QUEUED` row, with no bar keyed on
priority or triviality that would instead route a low-value item to the
project's existing lightweight surface (`vault/Backlog.md`). The register
consequently mixes L-priority cosmetic items with H-priority architectural
work in the same portfolio table, and nothing in either workflow ever
offers an alternative disposition.

## Evidence

- `new.md:81-82` (step 4a) instructs "Register every defect as its own row
  in REGISTER.md (QUEUED)" with no size/priority/triviality condition
  anywhere in the step; grep for "backlog"/"vault" across the file: 0
  matches. — source: dcs-situation-analyst, current-state read
- `esg.md` step 2's decision clusters (a)-(g), lines 65-94, contain no
  "route to backlog instead of a register row" option; cluster (b) (line
  67, "New intake found this sweep, each with a proposed type +
  priority") records priority but never uses it as a threshold. — source:
  dcs-situation-analyst, current-state read
- `doctrine.md` principle 4 (v0.5.12) itself codifies the unconditional
  form — "A stem that finds several registers each of them" — so a bar
  added only to workflow prose would contradict the constitution, which
  wins on conflict; principle 14 is a mid-incident IC→ESG escalation
  mechanism, unrelated to stem-time intake triage. — source:
  dcs-situation-analyst + dcs-commander, current-state read
- `tests/test_doctrine_integrity.py`: zero matches for
  priority|backlog|decompos|trivial, confirmed against a working control
  pattern in the same file — no mechanical check exists for this gap. —
  source: dcs-situation-analyst, current-state read
- `vault/Backlog.md` already exists and is documented (this project's own
  `CLAUDE.md` three-store rule) as exactly the lighter-weight surface this
  bar would route into — but **the shipped package must not hardcode it**
  (`CLAUDE.md`: "Ship no project facts" — DCS discovers a project's
  protocols from that project's own `CLAUDE.md` at runtime). — source:
  dcs-situation-analyst (surface exists) + dcs-commander (packaging
  constraint)
- The symptom is not hypothetical: `.dcs/esg/REGISTER.md` currently
  carries `json-examples-unparsed` (L, rank 12), `intake-nudge-telemetry`
  (L, rank 16) and `status-md-enum-drift` (L, rank 15) as full `QUEUED`
  rows in the same table as H-rank Type 1 items. — source:
  dcs-situation-analyst, current-state read, REGISTER.md:106,112,129
- This exact defect was already decomposed once, at
  `direct-resolution-lane`'s stem (2026-07-27), into a triviality-axis row
  (`trivial-work-inline-lane`) and this priority-axis row; the two were
  folded at the sixth `/dcs-esg` (2026-07-27) on the finding that both
  edit the same two sites for the same complaint. — source:
  dcs-situation-analyst, prior-art read, REGISTER.md:124,127 and Notes at
  368-376
- Concrete precedent that the gap already fires in production:
  `halt-loop-unbounded`'s AAR records three defects split at its stem
  going straight to `QUEUED` with no bar, two days before this row was
  even filed. — source: dcs-situation-analyst, prior-art read,
  `.dcs/incidents/2026-07-25-halt-loop-unbounded/AAR.md:236`
- Neither incident that later touched adjacent territory actually edited
  the mechanism this incident must change: `direct-resolution-lane`
  excluded `esg.md` entirely and edited `new.md` step 7a, not 4a;
  `token-economy` edited `esg.md` step 4's park/kill handling, not step
  2's decision clusters — a tree-wide search for "decision cluster" /
  "esg.md step 2" across every prior incident returns zero hits. —
  source: dcs-situation-analyst, prior-art read
- Correction to the original intake framing: this row is not sourced from
  `vault/Backlog.md` (an exhaustive search of its current 24 items found
  no trace of it) — its actual intake is the third-party
  `direct-resolution-lane` stem review, as the register row's own Intake
  source field already states. — source: dcs-situation-analyst, prior-art
  read

## Reproduction path

1. A stem's Symptom decomposes into 2+ independent defects at `new.md`
   step 4a, at least one of them trivial or low-priority.
2. Step 4a's literal text routes every non-critical-path defect to its
   own `QUEUED` row in `REGISTER.md`, unconditionally — no branch checks
   size, priority, or triviality first.
3. At the next `/dcs-esg` sweep, `esg.md` step 2 surfaces new intake under
   cluster (b) with a proposed type + priority, but none of clusters
   (a)-(g) ever offers "send this to `vault/Backlog.md` instead" — the
   row's only path forward is to stay `QUEUED`, indefinitely.
4. The row now competes for attention in the same table as H-priority
   architectural rows — already observed today (see Evidence).

## Blast radius (best guess at intake)

- `dcs/workflows/new.md` (step 4a's decomposition check)
- `dcs/workflows/esg.md` (step 2's decision clusters, and possibly step
  4's Record instructions for whatever disposition is added)
- `dcs/references/doctrine.md` principle 4 — its current wording mandates
  the unconditional form; if a bar ships, this sentence needs amending in
  the same IAP or the workflow and the constitution will contradict
  (constitution wins per this project's own stated precedence)
- Not in scope, split out separately at this stem: `esg.md` step 4's
  Record bullet omitting cluster (b) from its `REGISTER.md` write-back
  instructions entirely — independent root cause, registered as
  `esg-intake-writeback-gap` (QUEUED). Note for planning: that row's
  territory overlaps this incident's own edits to `esg.md`, so check
  whether this incident's tactics touch the same lines before that row is
  separately planned.
- Open design question carried from typing (dcs-commander): the fix must
  route to "a project-documented lightweight surface, discovered at
  runtime" with an explicit fallback to today's behavior (register
  unconditionally) when a project documents none — not a hardcoded
  `vault/Backlog.md` path. This is a 202-objectives-level decision, not
  pre-decided here.

## Prior art

This is a reassembled fold, not a fresh finding. Split at the
`direct-resolution-lane` stem (2026-07-27, third-party bread_bot review)
alongside a triviality-axis sibling (`trivial-work-inline-lane`), later
folded into this row at the sixth `/dcs-esg` (2026-07-27) — see
`.dcs/esg/REGISTER.md` rows 124/127 and their Notes, and
`vault/Meta/building-dcs-lessons.md` §15 (the seam-failure lesson the fold
cites). Structural precedent for the fix direction already exists in this
project: `vault/Backlog.md` already functions as a "candidates for
/dcs-esg to queue, not a register" surface (`CLAUDE.md`'s three-store
rule) — the fix wires the stem and the ESG sweep into an existing surface
pattern, it does not invent one. Inherited, not re-derived: 13 of 60 rows
in a different project's (bread_bot) register cite stem decomposition as
their intake source (regenerate: parse `C:/bread_bot/.dcs/esg/REGISTER.md`
rows, split on pipe, test cell 8 for «Декомпозиция»/4a).

## Type + rationale

**Proposed type:** 3
**Rationale:** Verified to the line: `new.md` step 4a's unconditional
register-every-defect instruction and `esg.md` step 2's clusters (a)-(g)
lacking any backlog disposition are a precisely located prose gap whose
remediation spans the 2-3 known files the register row already names
(`new.md`, `esg.md`, conditionally `doctrine.md`), follows an existing
documented surface pattern, and touches nothing in the
enforcement-mechanism set (gate, guarding tests, installer) that would
make this Type 1 in this project's own convention. (IC=dcs-commander,
fable, command point 1.)
**Owner confirmation:** confirmed as proposed (Type 3).

## Intake source (for /dcs-close to route back to)

`.dcs/esg/REGISTER.md` row `decomposition-backlog-routing` (rank 8),
itself decomposed at the `direct-resolution-lane` stem, 2026-07-27, from
third-party review (bread_bot main session, Fable).
