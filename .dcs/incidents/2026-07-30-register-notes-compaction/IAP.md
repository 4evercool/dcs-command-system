# IAP — Incident Action Plan

**Incident:** register-notes-compaction
**Period:** 1
**Type:** 3

## Artifacts

- [202 — Objectives](./202-OBJECTIVES.md)
- 203 skipped (default Type 3 activation: IC + Planning Chief + 1 specialist matching 204 tasking count, plain parallel execution)
- [204-TASKING/S1](./204-TASKING/S1.md)

## Goals and criteria summary

**Goal:** REGISTER.md reads no longer load historical Notes prose — 16 historical per-session entries moved to `vault/Meta/ESG-sessions/`, replaced with one-line pointers.

| Criterion | Owner | Summary |
|---|---|---|
| 1 | S1 | `grep -c '^### ' REGISTER.md` → 0 |
| 2 | S1 | Every entry replaced with `see vault/Meta/ESG-sessions/<file>.md — <summary>`, all pointers valid |
| 3 | S1 | `vault/Meta/ESG-sessions/README.md` exists, states read-only historical record purpose |
| 4 | S1 | Table section (before `## Notes`) byte-identical to pre-edit snapshot |
| 5 | S1 | `git diff --stat dcs/workflows/` shows no changes |
| 6 | S1 | Notes section < 10,000 B |
| 7 | IC | `dcs/templates/REGISTER.md` Notes cell: add routing convention line |
| 8 | IC | 214-LOG.md: compaction summary with before/after counts and regenerating command |

## Partition

| Tasking | Territory | Forbidden |
|---|---|---|
| S1 | `C:/DCS/.dcs/esg/REGISTER.md`, `C:/DCS/vault/Meta/ESG-sessions/**` | `C:/DCS/dcs/workflows/**`, `C:/DCS/dcs/templates/**`, `C:/DCS/.dcs/esg/STRATEGY.md`, `C:/DCS/.dcs/esg/REGISTER-LOCK` |

**Disjointness:** Single-specialist plan — trivially disjoint.

## Risks

1. **Single-specialist plan** — no parallel-execution risk. Territory trivially disjoint.
2. **REGISTER.md lives in main checkout** (C:/DCS/.dcs/esg/), not worktree — specialist must use absolute paths to the esg_root copy.
3. **REGISTER-LOCK protocol** — specialist must create-exclusive lock before RMW of REGISTER.md, delete when done.
4. **Pointer-filename consistency** — 16 filenames must exactly match between vault files and pointer lines. Criterion 2's verification loop catches mismatches.
5. **Table-section preservation** — lines 1-144 must not gain or lose a single byte. Diff against pre-edit snapshot is definitive.
6. **No rollback** — REGISTER.md is gitignored with no backup. Pre-edit table snapshot is the only recovery artifact for the table; moved sections exist in vault files and could be manually reassembled.
7. **Criteria 7 and 8 are IC-executed** — specialist must not touch `dcs/templates/**` or incident directory.
8. **vault/Meta/ESG-sessions/ does not exist yet** — must be created before writing files.

## Verification plan

End-to-end: all S1 evidence commands verified (grep for `###` → 0, pointer count → 16, every pointer file exists, README correct, table diff empty, workflow diff empty, Notes < 10,000 B). IC executes criteria 7 (template routing convention) and 8 (compaction summary in 214-LOG.md). Safety Officer independently re-runs pointer-existence loop and table-section diff, then confirms 201 repro_path measurements.
