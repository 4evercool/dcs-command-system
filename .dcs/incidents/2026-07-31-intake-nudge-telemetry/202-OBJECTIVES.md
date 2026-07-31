# 202 — Objectives (Operational Period 1)

**Incident:** intake-nudge-telemetry
**Period:** 1

## Goal

The intake nudge records its outcome so its effectiveness can be measured rather than guessed — a principle-15 fix: replace "tuning by impression" with evidence.

## Acceptance criteria (the Definition of Done)

1. `dcs/hooks/dcs_intake.py` appends a one-line JSON record to a project-local, gitignored telemetry log on each first-session invocation, before calling `emit()`
2. The record captures: ISO8601 timestamp, a session-id prefix (first 12 chars of the SHA-256 hash already computed for `already_seen()`), event type (`nudge_offered` for the no-active-incident branch, `active_reported` for the active-incident branch), and the project root path
3. The telemetry log path is `.dcs/esg/intake-telemetry.log` — the `.dcs/esg/` directory is already in `.gitignore`, so no `.gitignore` change is needed
4. The telemetry append fails open: an `OSError` during log write does not prevent the hook's advisory `emit()` — the nudge itself must never break a turn
5. `tests/test_dcs_intake.py` verifies that a telemetry line is written for both branches (no-incident and active-incident), with the correct event type, and that the log is appended to (not overwritten) across successive invocations
6. [IC] Update `dcs/workflows/init.md` if the hook's documented behaviour description needs amendment to reflect the new telemetry output

## Out of scope this period

- A broader DCS telemetry framework or per-incident telemetry table (that's `halt-enumeration-grammar-drift`'s territory, now DEPLOYED, and the v0.7-scope decision's "telemetry rides, never leads" directive)
- Aggregation, analysis, or dashboarding of telemetry data
- Telemetry for any hook other than `dcs_intake.py`

## Chief feedback (filled in after /dcs-plan spawns the Planning Chief)

