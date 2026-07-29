<!--
201-BRIEF.md — written by the IC from dcs-situation-analyst findings, once,
at the stem (/dcs-new). Never edited after typing is confirmed except to
append a note if a later period's assessment reveals the original blast
radius was wrong (append, don't rewrite — 214-LOG.md is the append-only
one, but this file's Symptom/Evidence should stay a true record of what was
known at intake).
-->

# 201 — Incident Brief

**Incident:** token-economy-advisory-fixes
**Opened:** 2026-07-30
**Type:** 3

## Symptom

Four one-line package-text defects flagged as advisories by the Safety Officer during `token-economy` (period 1, verdict 1, 2026-07-28) remain unfixed in the shipped package. The IC at that incident's command point 4 deliberately excluded them from integration commit `807edb8`, ruling that "an unverified edit to a guarded workflow file riding the merge with no Safety pass of its own costs more auditability than any one sentence is worth." The defects are: (1) `dcs/templates/204-TASKING.md` line 37 example says `-- full output` three lines after line 34's rule says "never a full unabridged transcript"; (2) `dcs/workflows/run.md` lines 52-53 contain "re-read it only where there is real doubt it is still in context" — a model self-report about its own context, the exact mechanism criterion 5 was dropped for in the same incident; (3) `agents/dcs-safety-officer.md` lines 57-60 define a by-reference exception for "unchanged" subjects but lack the caveat that derived subjects (test results, byte budgets, counts) require their inputs unchanged, not just the file that produced them; (4) `dcs/templates/STRATEGY.md` line 41 states "CAP: <= 5 LINES total per entry" but enumerates four items with the fifth unexplained, and the placeholder wraps across 3 physical lines.

## Evidence

- SAFETY.md advisory 2: `C:\dcs\dcs\templates\204-TASKING.md` lines 34-35 read 'Cite the decisive excerpt or file:line, never a full unabridged transcript' but line 37 reads `{{e.g. "pytest tests/test_inventory_repo.py -x -- full output"}}` — the example two lines below the rule contradicts it.
- SAFETY.md advisory 3: `C:\dcs\dcs\workflows\run.md` lines 51-53 read 're-read it only where there is real doubt it is still in context (a long gap, or a resumed session).' — model self-report about its own context.
- SAFETY.md advisory 4: `C:\dcs\agents\dcs-safety-officer.md` lines 57-59 define the by-reference exception for 'a subject you have yourself just established is unchanged with a named command you ran (a scoped git diff returning empty, or equivalent)' — no mention that for a derived subject, unchanged inputs are required.
- SAFETY.md advisory 6: `C:\dcs\dcs\templates\STRATEGY.md` line 41 states 'CAP: <= 5 LINES total per entry' but lines 42-52 enumerate four items; the placeholder wraps across 3 physical lines.
- Deferral ruling: `C:\dcs\.dcs\esg\REGISTER.md` row `token-economy-advisory-fixes` records the `dcs-commander`'s command-point-4 rationale.
- No intervening changes: `git log --oneline -- dcs/workflows/run.md dcs/templates/204-TASKING.md agents/dcs-safety-officer.md dcs/templates/STRATEGY.md` since `807edb8` shows zero commits.
- No ACTIVE incidents at open — territory check clean.

## Reproduction path

Not reproducible in the runtime sense — these are package-text defects. Each advisory describes a contradiction or ambiguity in prose, not in behavior:
1. Open `dcs/templates/204-TASKING.md` at line 34 — read the comment rule, then line 37's example; they contradict.
2. Open `dcs/workflows/run.md` at line 52 — read the "real doubt" clause; it asks the model to self-report about its own context.
3. Open `agents/dcs-safety-officer.md` at lines 57-59 — read the by-reference exception; it lacks the derived-subject caveat.
4. Open `dcs/templates/STRATEGY.md` at line 41 — count enumerated items (four) against stated cap (five); observe the placeholder wrapping.

## Blast radius (best guess at intake)

- `dcs/workflows/run.md`
- `dcs/templates/204-TASKING.md`
- `agents/dcs-safety-officer.md`
- `dcs/templates/STRATEGY.md`

## Prior art

Two DCS precedents for deferred advisories:
1. `register-field-repair-path` (2026-07-27) — advisory 4 deferred by IC at command point 4 into its own register row `register-writer-map-completeness` (now QUEUED, rank 12), with documented rationale: "fixing only the /dcs-close entry would be a partial repair of a pre-existing, out-of-scope defect."
2. `decomposition-backlog-routing` (2026-07-29) — advisories 1/2/6 deferred to vault/Backlog.md (not a register row).

## Type + rationale

**Proposed type:** 3
**Rationale:** Four well-isolated one-line text corrections to package documentation with no behavioral, schema, or architectural change — fits the Type 3 trigger exactly (1-4 files, clear root cause, no investigation needed) and exceeds the Type 5 single-file threshold.
**Owner confirmation:** confirmed as proposed — Type 3

## Intake source

`token-economy`'s own SAFETY.md (period 1 verdict, advisories 2/3/4/6) and AAR.md — self-generated at close, not an external ticket.
