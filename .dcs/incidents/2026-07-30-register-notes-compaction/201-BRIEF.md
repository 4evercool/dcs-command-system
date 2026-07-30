# 201 — Incident Brief

**Incident:** register-notes-compaction
**Opened:** 2026-07-30
**Type:** 3

## Symptom

REGISTER.md's Notes section (56,320 B, 54.1% of the 104,187-byte file) has absorbed all 30,418 bytes of growth since the 2026-07-28 retroactive Territory/Outcome/Intake compaction — which deliberately never touched Notes. Every `/dcs-esg` sweep and `/dcs-status --campaign` reads the full file, including 16 historical per-session prose entries that serve no operational purpose during a portfolio scan. The token-economy incident already shipped the pointer-not-copy pattern for Territory/Outcome/Intake columns; the Notes section is the remaining uncompacted bulk and the largest single-source token drain in the ESG read path.

## Evidence

- REGISTER.md total size: 104,187 B (`wc -c`); Notes section: 56,320 B starting at line 145 — 54.1% of the file — source: `wc -c` + awk measurement, 2026-07-30
- 16 discrete Notes entries: 9 ESG session accounts (Fifth through Thirteenth), 6 incident-opening notes, plus a `/dcs-deploy` session note. Top 3 by size: Territory lock (13,038 B / 215 lines), Ninth ESG (5,138 B / 79 lines), Fifth ESG (4,446 B / 72 lines) — source: per-`###` section breakdown
- Post-compaction baseline (2026-07-28, after retroactive Territory/Outcome/Intake collapse): 73,769 B. Growth since then: +30,418 B — all attributable to Notes additions — source: REGISTER.md retroactive compaction note, lines 1024-1065
- 10 of 10 DCS workflow files read `REGISTER.md` (close, deploy, esg, execute, init, loop, new, plan, run, status) — none include a scoping instruction to skip or limit the Notes section — source: `grep -nl 'REGISTER\.md\|\.dcs/esg/' dcs/workflows/*.md`
- token-economy's retroactive compaction explicitly excluded Notes: "does not attempt" to touch Notes, scoped to 11 DEPLOYED rows' Territory/Outcome/Intake only — source: `.dcs/esg/REGISTER.md` lines 1024-1065; AAR.md criterion 8 scoped close-time compaction to "this project's own live REGISTER.md/STRATEGY.md using S4's mechanism," S4's mechanism addressed only table columns — source: token-economy IAP.md criterion 8, 204-TASKING/S4.md lines 56-61
- The register row `register-notes-compaction` (QUEUED, rank 6) already names the fix shape: route historical Notes to `vault/Meta/ESG-sessions/` with one-line pointers — source: `.dcs/esg/REGISTER.md` row 142
- STRATEGY.md ranks this at 6: "Largest remaining single-source token drain in the ESG read path" — source: `.dcs/esg/STRATEGY.md` lines 187-192
- No agent charter (safety-officer, planning-chief, commander) references REGISTER.md directly — source: `grep 'REGISTER.md\|register' agents/dcs-*.md` returns zero hits for the register file
- Target directory `vault/Meta/ESG-sessions/` does not exist yet — source: `glob` on `C:/dcs/vault/Meta/` returns only `building-dcs-lessons.md`
- REGISTER.md has no backup (unlike STRATEGY.md which has `.bak-pre-compaction-2026-07-28`) — source: file listing of `.dcs/esg/`
- `.dcs/esg/` is gitignored; `vault/**` is unguarded by the gate and excluded from npm publish — source: `CLAUDE.md` vault rule, `package.json` files whitelist

## Reproduction path

Not a runtime defect — a structural size/reading-cost concern. Reproduce the measurement:
1. `wc -c .dcs/esg/REGISTER.md` — returns ~104,187 B
2. Compute Notes section share: `python -c "t=open('.dcs/esg/REGISTER.md',encoding='utf-8').read(); n=t.find('## Notes'); print(f'Notes: {len(t)-n} B, Total: {len(t)} B, Share: {(len(t)-n)*100/len(t):.1f}%')"` — Notes ~56,320 B, share ~54.1%
3. Count session sub-sections: `grep -c '^### ' .dcs/esg/REGISTER.md` — returns 16
4. Confirm blast radius: `grep -nl 'REGISTER\.md\|\.dcs/esg/' dcs/workflows/*.md` — returns 10 files, none scope to exclude Notes
5. Regenerate growth trajectory: 73,769 B post-compaction (2026-07-28) → 104,187 B now (+30,418 B)

## Blast radius (best guess at intake)

- `.dcs/esg/REGISTER.md` — the primary target: move historical Notes entries out, replace with one-line pointers
- `vault/Meta/ESG-sessions/` — destination directory for moved Notes (to be created)
- `dcs/templates/REGISTER.md` — possible template-level Notes scoping policy (add a convention line like the two-state Territory rule)
- 10 workflow files reading REGISTER.md (consumers, not targets — no workflow logic changes needed; the pointer-in-register pattern is already established by token-economy)

## Prior art

- **token-economy** (Type 1, DEPLOYED 2026-07-28): shipped the pointer-not-copy mechanism for Territory/Outcome/Intake source columns — collapsing each from multi-line prose to a one-line pointer (e.g. "see IAP.md partition table") when a row reaches a terminal state. The retroactive compaction saved ~45,186 B (118,955 B → 73,769 B). Did NOT touch the Notes section by design — the IAP's criterion 8 scoped close-time compaction to "this project's own live REGISTER.md/STRATEGY.md using S4's mechanism," and S4's mechanism only addressed the table columns. This incident applies that identical pattern to the one column left behind.
- **esg-artifact-bloat** (KILLED, folded into token-economy): precursor defect that measured REGISTER.md+STRATEGY.md growth across three consecutive ESG sessions and identified the pointer-not-copy pattern as the fix. Its own intake cell documented the bloat trajectory before fold.
- **Declined SQLite migration** (`vault/Decisions/sqlite-migration-register.md`, 2026-07-28): the Owner proposed migrating REGISTER.md to a database; the case against it noted that the Notes section's bloat is a content-bound problem, not a storage-format problem — "the fix for unbounded prose is a content bound, independent of storage engine."
- **strategy-compaction-loses-history** (QUEUED, rank 15): a related but separate concern — STRATEGY.md's retroactive compaction dropped decline-history texture with no git backing. The lesson for this incident: moved Notes must be preserved in `vault/Meta/ESG-sessions/` before replacing with pointers, not deleted.

## Type + rationale

**Proposed type:** 3
**Rationale:** Notes compaction follows the established pointer-not-copy pattern from token-economy (Type 1), touches only unguarded files (`.dcs/esg/REGISTER.md` + `vault/Meta/`), requires no enforcement mechanism, installer, or architectural changes — a bounded well-scoped task matching Type 3 criteria per typing.md: well-scoped bug/feature touching a bounded set of files with a clear fix pattern. Type 1 is unwarranted (no enforcement mechanism impact, no schema migration, no deploy-ordering decision); Type 5 is insufficient (16 historical entries to route, template-level policy to add, register row to update — more than one file and one act).
**Owner confirmation:** confirmed as proposed

## Intake source

Thirteenth `/dcs-esg` sweep, 2026-07-30 — register row `register-notes-compaction` (QUEUED, rank 6, M)
