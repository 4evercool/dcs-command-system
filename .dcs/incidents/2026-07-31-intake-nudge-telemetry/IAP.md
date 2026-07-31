# IAP — Incident Action Plan

**Incident:** intake-nudge-telemetry
**Type:** 3
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `204-TASKING/S1.md` · `204-TASKING/S2.md`

## Objectives (summary of 202)

**Goal:** The intake nudge records its outcome so its effectiveness can be measured rather than guessed — a principle-15 fix: replace "tuning by impression" with evidence.

1. `dcs/hooks/dcs_intake.py` appends a one-line JSON record to a project-local, gitignored telemetry log on each first-session invocation, before calling `emit()`
2. The record captures: ISO8601 timestamp, a session-id prefix (first 12 chars of the SHA-256 hash already computed for `already_seen()`), event type (`nudge_offered` for the no-active-incident branch, `active_reported` for the active-incident branch), and the project root path
3. The telemetry log path is `.dcs/esg/intake-telemetry.log` — the `.dcs/esg/` directory is already in `.gitignore`, so no `.gitignore` change is needed
4. The telemetry append fails open: an `OSError` during log write does not prevent the hook's advisory `emit()` — the nudge itself must never break a turn
5. `tests/test_dcs_intake.py` verifies that a telemetry line is written for both branches (no-incident and active-incident), with the correct event type, and that the log is appended to (not overwritten) across successive invocations
6. [IC] Update `dcs/workflows/init.md` if the hook's documented behaviour description needs amendment to reflect the new telemetry output

## Tactics (from the Planning Chief)

- Add a `record_telemetry(event_type, project_root, session_id)` function in `dcs_intake.py` that appends a one-line JSON record (ISO8601 timestamp, first-12-chars session-id prefix from the same SHA-256 hash `already_seen()` computes, event_type string, project_root path) to `.dcs/esg/intake-telemetry.log`. The function catches `OSError` and returns silently — the nudge must never break a turn (criterion 4).
- Call `record_telemetry()` before `emit()` in both branches of `main()`: pass `"nudge_offered"` for the no-active-incident branch, `"active_reported"` for the active-incident branch.
- Extend `test_dcs_intake.py` to assert: a telemetry line is written for each branch with the correct event_type (criterion 5), the log appends rather than overwrites, each record has parseable JSON with all four required fields, and a simulated write failure does not prevent `emit()` output.

## File-territory partition

| Specialist | Territory | Forbidden |
|---|---|---|
| S1 | `dcs/hooks/dcs_intake.py` | `tests/**`, `dcs/workflows/**`, `dcs/references/**`, `agents/**`, `bin/**`, `skills/**`, `vault/**` |
| S2 | `tests/test_dcs_intake.py` | `dcs/**`, `agents/**`, `bin/**`, `skills/**`, `vault/**` |

**Partition status:** disjoint — parallel execution

## Risks

- `.dcs/esg/` is gitignored per the existing `.gitignore` entry (verified with `git check-ignore`). No `.gitignore` change is needed — the 202 criterion 3 path is correct after IC resolution.
- `dcs/hooks/**` is a Delegation v4 `forbidden_glob` — Owner approval is mandatory at IAP stage; Delegation auto-approval cannot cover this incident.
- The test for fail-open (criterion 4, S2 test (e)) creates a directory at the log path inside a tempdir. The test must handle cleanup correctly — the directory exists inside the test's own temp project, not at the worktree level.
- S2's test for append behaviour (criterion 5) requires running the hook twice with different session_ids in the same test project. The current test structure uses `mkdtemp` and cleans up with `rmtree` — the new test must preserve the project directory between two hook invocations.

## Verification plan

Integrated end-to-end verification, run from the worktree root `C:\DCS-wt\intake-nudge-telemetry`:
1. `python tests/test_dcs_intake.py` — all tests pass, including the new telemetry tests (both branches + append + field validation + fail-open), minimum 14 passed total
2. Manual spot-check: run the hook against a scratch project with no ACTIVE file, inspect `.dcs/esg/intake-telemetry.log` — it must contain exactly one line of valid JSON with `event_type` `"nudge_offered"`, a parseable ISO8601 timestamp, a 12-char hex `session_id`, and the correct `project_root`. Run again with an ACTIVE file present — the log must have grown by one line with `event_type` `"active_reported"`
3. Original 201 repro path: `grep -n 'record_telemetry' dcs/hooks/dcs_intake.py` must now show hits beyond the temp-marker write
4. The hook must still pass the existing 10 behavioural tests unchanged (S2's edits are additions only)

## Deviation history (this period)

None — first IAP for period 1.
