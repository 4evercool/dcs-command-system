# IAP — Incident Action Plan

**Incident:** field-lesson-citations
**Type:** 3
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `204-TASKING/*.md` (203 skipped — default Type 3 activation: IC + Planning Chief + 3 specialists, parallel execution)

## Objectives (summary of 202)

**Goal:** Every shipped field lesson is verifiable in one lookup — a reader can identify the originating incident from the citation itself.

1. Population census of all field lesson mentions across 6 target files (grep, output to 214-LOG.md)
2. Every appendix field lesson names its incident — grep returns zero undocumented lines
3. Every workflow field lesson (deploy.md, new.md, close.md) names its incident
4. Every template field lesson (202-OBJECTIVES.md, REGISTER.md) names its incident
5. The citation convention is documented in doctrine-appendix.md
6. Pre-self-hosting lessons carry best-available identifier (version, or "predates self-hosting" note)
7. [IC] test_doctrine_integrity.py gains a mechanical check flagging field lesson mentions without incident identifiers

## Tactics (from the Planning Chief)

1. Census and pattern definition — enumerate every field lesson line with file/line/identifier status, output to 214-LOG.md as period-start baseline
2. Fix the appendix — add missing identifiers to 8 field lesson citations, add convention paragraph per criterion 5
3. Fix the workflows — add "(predates self-hosting)" annotations and version numbers to 7 workflow field lesson mentions
4. Fix the templates — add identifiers to 3 template mentions; the post-self-hosting lesson (2026-07-26) needs a real incident slug
5. [IC] Mechanical check — add check to test_doctrine_integrity.py

## File-territory partition

| Specialist | Territory | Forbidden |
|---|---|---|
| S1 | `dcs/references/doctrine-appendix.md` | `dcs/workflows/**`, `dcs/templates/**`, `tests/**` |
| S2 | `dcs/workflows/deploy.md`, `dcs/workflows/new.md`, `dcs/workflows/close.md` | `dcs/references/**`, `dcs/templates/**`, `tests/**` |
| S3 | `dcs/templates/202-OBJECTIVES.md`, `dcs/templates/REGISTER.md` | `dcs/references/**`, `dcs/workflows/**`, `tests/**` |

**Partition status:** disjoint — parallel execution (S1 runs census first, then S1/S2/S3 edit in parallel)

## Risks

1. **No partition risk:** `dcs/references/` vs `dcs/workflows/` vs `dcs/templates/` are disjoint directory trees with no overlap.
2. **S1 census is read-only** across all 6 files before S2/S3 edit — serial dependency: S1 completes census first, then S2+S3 proceed in parallel.
3. **The post-self-hosting lesson in `202-OBJECTIVES.md` (2026-07-26)** may not have a directly matching incident in `.dcs/incidents/`. S3 is instructed to search and flag a deviation if unfindable — do NOT fall back to "(predates self-hosting)" for a post-2026-07-25 date; that would be factually wrong (commander flagged this at IAP review).
4. **CHANGELOG.md** has a field lesson mention outside the 6-file census scope (commander noted at IAP review). The 202 deliberately scoped to 6 files; CHANGELOG.md is a known omission this period. Recorded here so the Safety Officer is not surprised.

## Verification plan

1. Baseline census in 214-LOG.md shows N field lesson mentions across 6 files, with which carry identifiers and which do not
2. For all 3 territory groups, confirming grep per file returns zero lines lacking an identifier
3. Convention paragraph is present at top of doctrine-appendix.md
4. [IC] test_doctrine_integrity.py gains check that mechanically validates the same invariant at merge time
5. `python tests/test_doctrine_integrity.py` passes clean
6. Manual IC spot-check: each identifier is honest — slugs refer to real incidents in `.dcs/incidents/`, "(predates self-hosting)" annotations are truthfully applied to pre-2026-07-25 material

## Deviation history (this period)

None — period 1, first IAP.
