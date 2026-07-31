# 201 — Incident Brief

**Incident:** intake-nudge-telemetry
**Opened:** 2026-07-31
**Type:** 3

## Symptom

The DCS intake nudge (`dcs/hooks/dcs_intake.py`) — a UserPromptSubmit hook that fires once per session per project, advising the session to offer `/dcs-run` when no incident is active (or reporting the active incident's slug/type/phase when one is) — has zero telemetry. Nothing records whether the nudge was accepted, declined, or ignored. The only disk state it writes is a transient `1`-byte marker file in the system temp directory, used solely to enforce the once-per-session rule; those markers are reaped after 12 hours. This gap means the nudge's effectiveness can only be assessed by impression — which is exactly what DCS principle 15 warns against ("write the derivation, not the result").

## Evidence

- `dcs/hooks/dcs_intake.py` lines 55-82: `already_seen()` writes a `1`-byte marker to temp dir — the ONLY disk write in the hook. No telemetry record is written anywhere. Source: file read at `C:\dcs\dcs\hooks\dcs_intake.py`.
- `dcs/hooks/dcs_intake.py` lines 97-141: `main()`'s two branches (active-incident at lines 113-125, no-incident at lines 127-137) both call `emit()` with advisory text and `sys.exit(0)` — no logging, no append to any file. Source: file read at `C:\dcs\dcs\hooks\dcs_intake.py`.
- `tests/test_dcs_intake.py`: all 10 tests verify behavioural output only (silent, nudge text, active-incident report, once-per-session); none assert telemetry or log output. Source: file read at `C:\dcs\tests\test_dcs_intake.py`.
- `vault/Backlog.md` lines 73-79, item 4: explicitly documents the gap — "Intake nudge has no telemetry. … A single line appended to a local (gitignored) log would be enough." Source: file read at `C:\dcs\vault\Backlog.md`.
- `.dcs/esg/REGISTER.md` line 112: row `intake-nudge-telemetry` — Type 3, priority L (rank 14), state QUEUED, territory `dcs/hooks/dcs_intake.py, tests/test_dcs_intake.py, .gitignore`. Source: file read at `C:\DCS\.dcs\esg\REGISTER.md`.
- `.dcs/esg/STRATEGY.md` lines 211-214: rank 11 listing notes "tuning the intake nudge by impression is exactly what principle 15 warns against." Source: grep of `C:\DCS\.dcs\esg\STRATEGY.md`.
- `vault/Meta/ESG-sessions/territory-lock-cost-cluster-2026-07-26.md` lines 165-170: ESG session confirmed disjoint territory for this row and noted `dcs/hooks/**` is a Delegation `forbidden_glob`. Source: file read.
- `dcs/hooks/dcs_gate.py` (777 lines): the sibling hook also has no telemetry — DCS has no telemetry infrastructure at all; this gap is a missing instrumentation point, not a missing integration. Source: file read.
- `dcs/workflows/init.md` lines 62-78: documents the hook's role and copies it to onboarded projects — any change to the hook surface must update this workflow's description. Source: file read.
- `install.ps1` line 19: warns that per-project hook copies are stale until `/dcs-init` re-runs. Source: file read.

## Reproduction path

1. Verify the hook has no telemetry: `grep -n 'open\|write\|log\|append\|record' dcs/hooks/dcs_intake.py` — only `already_seen()`'s temp-marker at lines 62-67; no append-write anywhere.
2. Run the test suite: `python tests/test_dcs_intake.py` — all 10 pass, none assert telemetry output.
3. Inspect the register: `grep 'intake-nudge-telemetry' .dcs/esg/REGISTER.md` — state QUEUED, confirming no incident has ever been opened.
4. Read the backlog: item 4 at `vault/Backlog.md:73-79` — gap documented with proposed fix shape.

## Blast radius (best guess at intake)

- `dcs/hooks/dcs_intake.py` — the hook itself (add telemetry output)
- `tests/test_dcs_intake.py` — tests must verify telemetry output
- `.gitignore` — telemetry log file must be gitignored
- `dcs/workflows/init.md` — hook description may need updating
- `.claude/settings.json` (per-project) — if a log path needs configuration
- `~/.claude/dcs/hooks/dcs_intake.py` (installed copy) — updated by `install.ps1`

## Prior art

Backlog item 4 at `vault/Backlog.md:73-79`, filed by the Owner. Registered as QUEUED row `intake-nudge-telemetry` (Type 3, priority L, rank 14) in `.dcs/esg/REGISTER.md`. Ranked at the first `/dcs-esg` session that assigned ranks (2026-07-26, documented in `vault/Meta/ESG-sessions/territory-lock-cost-cluster-2026-07-26.md`). Territory includes `dcs/hooks/**` which is a Delegation `forbidden_glob`, so this incident can never auto-approve. The backlog item proposes a specific fix shape: "a single line appended to a local (gitignored) log would be enough."

`vault/Decisions/v0.7-scope.md` lines 98-99 classifies telemetry as a rider, not a leader, and notes that the broader per-incident telemetry table gates behind `halt-enumeration-grammar-drift` (now DEPLOYED), but the intake-nudge-specific log has no grammatical dependency on that fix.

## Type + rationale

**Proposed type:** 3
**Rationale:** Bounded 2-3 file change with a known fix pattern (add a log line to an existing hook), no schema/shared-infrastructure/architectural change — the gap is a missing instrumentation point, not missing telemetry infrastructure. Territory includes `dcs/hooks/**` (Delegation `forbidden_glob`), so Owner approval is already mandatory regardless of type. Type 5 is disqualified by file count (>1). Type 1 is unnecessary — no migration, no architectural pattern change, no deploy-ordering decision.
**Owner confirmation:** confirmed as proposed (Type 3)

## Intake source (for /dcs-close to route back to)

`.dcs/esg/REGISTER.md` row `intake-nudge-telemetry` (QUEUED), originating from `vault/Backlog.md` item 4
