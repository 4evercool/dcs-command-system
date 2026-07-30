# 202 — Objectives (Operational Period 1)

**Incident:** register-notes-compaction
**Period:** 1

## Goal

REGISTER.md reads no longer load historical Notes prose. Every historical per-session Notes entry (the 16 `###`-headed sections currently occupying 56,320 B) is preserved in `vault/Meta/ESG-sessions/` and replaced with a one-line pointer — the same pointer-not-copy pattern token-economy shipped for Territory/Outcome/Intake source.

## Acceptance criteria (the Definition of Done)

1. Every `###`-headed section in REGISTER.md's Notes (below `## Notes`, line 145) is moved to its own file in `vault/Meta/ESG-sessions/` — verify with: `grep -c '^### ' .dcs/esg/REGISTER.md` returns 0
2. Each moved entry is replaced with a one-line pointer: `see vault/Meta/ESG-sessions/<filename>.md — <one-line summary>` — verify with: `grep -c 'see vault/Meta/ESG-sessions/' .dcs/esg/REGISTER.md` equals the number of moved entries, and every pointer line names a file that exists
3. `vault/Meta/ESG-sessions/README.md` exists and clearly explains that these files are read-only historical records of past ESG and incident-stem sessions, not to be edited — verify with: file exists at the path and its first paragraph states the read-only historical record purpose
4. The REGISTER.md table section (everything before `## Notes`) is byte-identical to its pre-compaction state — verify with: diff of the table header + body against a pre-edit copy
5. No workflow file (`dcs/workflows/*.md`) is edited — verify with: `git diff --stat dcs/workflows/` shows no changes
6. REGISTER.md Notes section after compaction is under 10,000 B — verify with: `python -c "t=open('.dcs/esg/REGISTER.md',encoding='utf-8').read(); n=t.find('## Notes'); print(len(t)-n)"` returns a value < 10000
7. [IC] `dcs/templates/REGISTER.md` Notes template cell gets a one-line scoping convention appended: prose carries the convention that historical per-session accounts route to `vault/Meta/ESG-sessions/` with a pointer, keeping the Notes section scoped to operational notes
8. [IC] 214-LOG.md appended with compaction summary: byte counts before/after, entry count, and a regenerating measurement command

## Out of scope this period

- Compacting STRATEGY.md's Sessions log (separate incident: `strategy-compaction-loses-history`, QUEUED rank 15)
- Adding a Notes length guard or structured bound to REGISTER.md (a content-bound is independent of storage engine per `vault/Decisions/sqlite-migration-register.md`; this incident applies the pointer pattern, it does not add enforcement)
- Editing any workflow file to add Notes-scoping instructions — the pointer pattern is already established and workflow consumers already handle it
