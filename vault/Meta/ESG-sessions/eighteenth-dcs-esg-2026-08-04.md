# Eighteenth `/dcs-esg`, 2026-08-04 — ranking around a held deploy

Chair: Owner. Chief of Staff: main session (Fable).

## Portfolio at close of session

37 DEPLOYED, 1 MERGED (deploy **held** — `field-lesson-guard-vacuity`,
branch kept as rollback ref), 19 QUEUED (ranked 1–19, contiguous),
1 PARKED (`halt-binding-status`), 10 KILLED, 4 RESOLVED, nothing ACTIVE,
no pending sitreps (all Decision fields filled). Regenerate from the
State column:
`awk -F'|' '/^\| [a-z][a-z0-9-]* \|/ {s=$6; gsub(/^ +| +$/,"",s); sub(/ \(.*/,"",s); print s}' .dcs/esg/REGISTER.md | sort | uniq -c`.

Since the seventeenth session: the 2026-08-03 train shipped
`record-integrity-corrections`, `close-integrity-guard-bundle` and the
out-of-queue `spawn-effort-control` (witness 51 identical / 0 differing);
`independence-fail-closed-and-model-floor` and `log-append-helper`
followed — **the entire hardening arc from
`vault/Decisions/non-anthropic-hardening.md` is now delivered.**
`field-lesson-guard-vacuity` ran as this repo's first deliberately
DeepSeek-operated incident (a hardening probe); its post-close review
produced the held deploy, one `RECORD-CORRECTION:` entry in its own log,
one new row, and evidence routed to two existing rows.

## Decisions

1. **Rank 1 = `field-lesson-guard-bare-date-weakening`** — it gates the
   held deploy: the parent's repair widened `_FL_ID_RE` to accept a bare
   same-line date as an identifier (unverifiable, the v0.5.10 shape),
   and the Owner held the train so the fix ships with the parent.
2. **Backlog item 31 folded into rank 1** (over own-row and
   leave-in-backlog): the `RECORD-CORRECTION:` sentinel is invisible to
   check 12's `_SENTINEL_TOKENS` census and undocumented in shipped
   prose; the fix is a tuple addition plus a prose paragraph in the same
   file rank 1 already edits, riding the same train. This also
   discharges the disposition the register's
   `record-integrity-corrections` row owed "at next /dcs-esg".
3. **Ranking accepted:** rank 2 `verdict-rerun-em-dash-gap` (H — the
   em-dash `checked[]` split `verdict_rerun.py` requires is not reliably
   produced by Safety Officers, undermining the independence mechanism
   at its first real exercise); prior ranks 5–20 shifted to 3–18
   unchanged; `spawn-effort-control-d5-corrections` at 19, adjacent to
   its correction-convention sibling (18).

## Delegation

v6 unchanged. The model floor shipped inside
`independence-fail-closed-and-model-floor`'s own IAP; whether it
supersedes the blanket `auto_approve_type3` switch in the bounds schema
is that mechanism's own documented behavior now — no ESG amendment
needed this session, and no new evidence against any bound.

## Hygiene

Worktree audit clean: one worktree (main checkout), no orphans, no
husks. Two `dcs/*` branches, both accounted for:
`dcs/field-lesson-guard-vacuity` (rollback ref while its deploy is held)
and `dcs/revision-preservation-map-abandoned-2026-07-31` (kept by the
sixteenth session's standing decision). The held train ships when rank 1
merges — Owner-invoked, not started here.
