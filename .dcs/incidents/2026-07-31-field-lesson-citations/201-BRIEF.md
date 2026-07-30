# 201 — Incident Brief

**Incident:** field-lesson-citations
**Opened:** 2026-07-31
**Type:** 3

## Symptom

Field lessons shipped in DCS doctrine and workflows carry no verifiable provenance. Of 11 explicitly labeled "field lesson" citations in `doctrine-appendix.md`, only 3 name an incident slug; the other 8 cite only a date and/or version. Four workflow files (`deploy.md`, `new.md`, `close.md`) and two templates (`202-OBJECTIVES.md`, `REGISTER.md`) embed field lesson mentions with zero incident identifiers. No mechanical check in `test_doctrine_integrity.py` verifies field lesson truth — the test suite checks structure (numbering, references, includes, size) but cannot detect a fabricated claim. One false lesson already shipped in v0.5.10, corrected in v0.5.11 four minutes later — the exact failure mode this incident exists to prevent.

## Evidence

- `doctrine-appendix.md`: 11 field-lesson paragraphs; 3 carry an incident slug (`decomposition-backlog-routing`, `deviation-path-proportionality`, `safety-halt-functional-scope`); the other 8 name only a date and/or version — analyst 2 (repro+logs), items 1-11
- `deploy.md`: four field lesson mentions (lines 48, 77, 148, 169), none with an incident slug — analyst 1 (codegraph+prior-art), item 4
- `new.md` lines 108-118: one field lesson narrative ("the incident this rule exists for"), never naming the slug — analyst 1, item 5
- `close.md`: two field lesson mentions (lines 61, 143), dates only — analyst 1, item 6
- `202-OBJECTIVES.md` lines 33, 58: two field lesson mentions, date only — analyst 1, items 7-8 (analyst 2 confirmed line 33 in addition to 58)
- `REGISTER.md` line 77: one field lesson, date only — analyst 1, item 8 (analyst 2 notes this may be a rendering artifact; verify at the stem)
- v0.5.10 commit `0798fb1`: shipped a false field lesson claiming a command-point spawn "left the session idle with a zero-byte agent transcript" when the agent had already returned a complete reject verdict — analyst 2, item 12
- v0.5.11 commit `d53adc1`: corrected the false lesson four minutes later — analyst 2, item 12
- `test_doctrine_integrity.py`: 19+ checks, zero on field lesson truth or citation format; check 14's appendix rule only checks quoted census figures — analyst 1, items 1-2
- Safety Officer charter (`agents/dcs-safety-officer.md`): zero mentions of field-lesson verification; verification scope is bound to current operational period's diff/tests — analyst 2, item 14
- 7 of 11 field lessons predate the self-hosting incident directory (earliest `.dcs/incidents/` entry is 2026-07-25), so their dates cannot be resolved to an artifact path — analyst 2, item 15

## Reproduction path

Not a runtime symptom. To reproduce the structural gap: (1) grep for "[Ff]ield lesson" across `dcs/`; (2) for each match, attempt to identify the incident slug and artifact that would let a human verify the claim in one lookup; (3) observe that only 3 of 11 appendix entries and 0 of ~8 workflow/template entries carry a slug. The v0.5.10 incident demonstrates the consequence: a false claim shipped and passed every mechanical check.

## Blast radius (best guess at intake)

`dcs/references/doctrine-appendix.md` (11 field lesson entries), `dcs/references/doctrine.md` (compressed field-lesson text, if any remains after hot-path trim), `dcs/workflows/deploy.md` (4 mentions), `dcs/workflows/new.md` (1 mention), `dcs/workflows/close.md` (2 mentions), `dcs/templates/202-OBJECTIVES.md` (2 mentions), `dcs/templates/REGISTER.md` (1 mention), `agents/dcs-safety-officer.md` (optional: add verification duty), `tests/test_doctrine_integrity.py` (optional: add citation-format check).

## Prior art

- `vault/Backlog.md` item 2: explicitly documents the gap — "Field-lesson citations are unverifiable" — and proposes two options: require incident slug+artifact per field lesson, or make verification a Safety Officer charter duty. Leaning toward the first.
- `vault/Decisions/distribution-and-scheduling.md` lines 57-61: records the deliberate decision that self-hosting does not buy verification of meaning, and that Safety Officer evidence-reading is the check that would have caught v0.5.10.
- Two appendix entries already carry incident slugs (principle 4 — `decomposition-backlog-routing`, principle 15 — `deviation-path-proportionality`, principle 15 — `safety-halt-functional-scope`), demonstrating the format is viable and already partially adopted.
- `CHANGELOG.md` line 705: the v0.5.10 defect specifics — a doctrine section referenced as a heading that was only a bolded paragraph.

## Type + rationale

**Proposed type:** 3 (dcs-commander, fable)
**Rationale:** Bounded mechanical change to 6-8 known files following an already-proven format (two appendix entries already carry incident slugs); root cause fully understood, scope limited to adding identifier metadata to existing text with an optional additive regex check in the existing test suite — no structural consequences, no shared infrastructure risk.
**Owner confirmation:** confirmed as proposed, Type 3

## Intake source

`vault/Backlog.md` item 2; queued in `.dcs/esg/REGISTER.md` at rank 10 (M), thirteenth `/dcs-esg`, 2026-07-30
