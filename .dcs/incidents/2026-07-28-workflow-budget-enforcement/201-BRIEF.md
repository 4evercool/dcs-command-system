# 201 — Incident Brief

**Incident:** workflow-budget-enforcement
**Opened:** 2026-07-28
**Type:** 1

## Symptom

CLAUDE.md documents a coding rule — "File size: workflows ≤ ~250 lines" — that no automated check enforces anywhere in this repository: neither the merge-time guard (`tests/test_doctrine_integrity.py`, invoked by `/dcs-close` step 1a via CLAUDE.md's "Merge-time guard" section) nor the runtime PreToolUse gate (`dcs_gate.py`) measures a `dcs/workflows/*.md` file's line count. The rule exists as prose only. Fresh measurement shows 4 of the repository's 10 workflow files already over budget — `plan.md` 666 lines (2.7× budget), `execute.md` 424, `deploy.md` 282, `close.md` 273 — and the gap has already forced at least two prior incidents into ad hoc, undocumented IC rulings just to hold a line, because no mechanical check exists to hold it for them.

## Evidence

- `wc -l dcs/workflows/*.md` (fresh, independently reproduced by two analysts, 2026-07-28): plan.md 666, execute.md 424, deploy.md 282, close.md 273 over budget; esg.md 152, init.md 215, loop.md 161, new.md 242, run.md 184, status.md 120 under. new.md has only 8 lines of headroom left and has already needed a hand-written per-tasking ceiling once (`direct-resolution-lane`) to stay under — source: situation analyst 1 (reproduction), independently corroborated by analyst 2.
- `tests/test_doctrine_integrity.py` read in full (1228 lines, 16 numbered checks): only check 7 (`HOT_PATH_BUDGET_KB = 37`, line 142; measured at lines 263-272) touches file size, and it budgets `doctrine.md` + `schemas.md` combined by normalised byte count — never `dcs/workflows/*.md`, never a line count. A `workflows()` enumerator already exists (lines 175-176, `sorted((REPO/"dcs"/"workflows").glob("*.md"))`) and is reused by 4 other (purely textual-reference) checks, but no check measures size with it. Repo-wide grep for the literal string "250" across every `*.py` file returns zero hits — source: situation analyst 1.
- `dcs/hooks/dcs_gate.py` (the runtime PreToolUse hook, distinct from the merge-time suite) has no size/budget logic either — the gap is unenforced at both layers — source: situation analyst 1.
- `vault/Backlog.md` item 18 (this row's origin, registered at `deploy-marker-blind`'s close, 2026-07-27): "Nothing checks it — `tests/test_doctrine_integrity.py`'s size budget covers doctrine.md + schemas.md only," closing with the open design question: "Decide whether the budget becomes a check (with a per-file ratchet like the hot path's) or is retired as advice. Either is defensible; the current state — a rule enforced only by whoever remembers to measure — is the one that is not." — source: situation analyst 2.
- `deploy-marker-blind` (2026-07-27) needed at least two ad hoc IC rulings on `deploy.md`'s length within that one incident (a 265-line ceiling, then a pre-authorised band to 275 — `.dcs/incidents/2026-07-27-deploy-marker-blind/IAP.md:122-129`, `AAR.md:104-108`). `deploy.md` has since drifted past even that ruling, to 282 today — the very next commit to touch it (`token-economy`'s `807edb8`) grew it 275→282 unflagged, because nothing measures it — source: situation analyst 2.
- `criterion-unmeasured-fact`'s Safety Officer (2026-07-28) independently hit the identical gap on `plan.md` (403→422, IAP-bounded at ≤425, held) and reached this same conclusion on the record: "a written budget nothing measures is itself a principle-15 defect" (`SAFETY.md:24-25`) — source: situation analyst 2.
- The only existing size-budget precedent in this codebase, the `HOT_PATH_BUDGET_KB` check, was itself hardened once already against representation-dependent measurement (`hot-path-budget-eol-sensitivity`, 2026-07-25 — raw byte counts drifted with CRLF/LF, and a merged tree with mixed line endings had no stable definition at all). Empirically re-checked against the live tree for this new incident: that specific hazard does NOT carry over to a line-count check — `bytes.count(b'\n')` (what `wc -l` measures) is identical to `wc -l`'s own output on all four over-budget files regardless of representation, and `git ls-files --eol` confirms all four already sit at `w/lf` under the repo's `.gitattributes` policy (the EOL incident's own deliverable) with zero CRLF pairs and zero lone CRs. A narrower, smaller-magnitude residual risk remains (a lone CR, or a missing trailing newline, would each be invisible to naive `\n`-counting) and is worth defending against by house idiom (normalise before counting) even though not currently triggered — source: situation analyst 2.
- The Owner declined this item twice before promoting it to rank 1 (recovered from `.dcs/esg/STRATEGY.md.bak-pre-compaction-2026-07-28`, since the live `STRATEGY.md` was retroactively compacted 2026-07-28 and lost this texture — now separately registered as its own row, `strategy-compaction-loses-history`, out of this incident's territory). 5th ESG (2026-07-27): 4 files already over budget, still didn't carry. 6th ESG (same day): declined a second time; `new.md`'s 234→242 growth survived only because a Planning Chief hand-wrote the ceiling into that incident's own tasking — "precisely the item's own complaint, observed once more without being acted on." Promoted to rank 1 at the ninth ESG (2026-07-28) once `plan.md` hit 666 and 4 files sat over budget — source: situation analyst 2.

## Reproduction path

1. From C:\DCS, run `wc -l dcs/workflows/*.md` — observe plan.md 666, execute.md 424, deploy.md 282, close.md 273, all over the ~250-line budget CLAUDE.md states.
2. Run `python tests/test_doctrine_integrity.py` — 85/85 checks pass; none reference this budget.
3. Grep every `*.py` file in the repo for the literal `250` — zero hits, confirming no other script enforces it either.

Net effect: the gap reproduces on every run, deterministically, not intermittently.

## Blast radius (best guess at intake)

- `tests/test_doctrine_integrity.py` — add the enforcement check itself; likely reuses the existing `workflows()` enumerator (lines 175-176).
- `CLAUDE.md` — the rule's own wording; analyst 1 separately flagged that "see the guard" at CLAUDE.md:133 currently reads ambiguously (grammatically attached to the doctrine.md exception clause only, but readable as if the workflow-line rule is already guarded, which it is not).
- Possibly `dcs/workflows/plan.md`, `execute.md`, `deploy.md`, `close.md` — ONLY if tactics decides the fix requires trimming and/or a per-file ratchet baseline rather than a check that starts from a grandfathered baseline for already-over-budget files. This is an open design question for objectives/tactics, not resolved at intake — the register's own territory estimate agrees ("tests/test_doctrine_integrity.py, CLAUDE.md (estimate — refine at its own stem)").

## Prior art

`vault/Backlog.md` item 18 (origin, 2026-07-27, open design question quoted above); `deploy-marker-blind` AAR.md/IAP.md (two ad hoc IC rulings on deploy.md, since drifted past); `criterion-unmeasured-fact` SAFETY.md advisory 3 (plan.md, same conclusion independently reached); the existing `HOT_PATH_BUDGET_KB` check and its own hardening incident `hot-path-budget-eol-sensitivity` (closest architectural precedent, byte-based not line-based, EOL-hazard empirically shown not to carry over to a line-count design); `.dcs/esg/STRATEGY.md.bak-pre-compaction-2026-07-28` (recovered decline history — Owner declined this item twice, now separately registered as `strategy-compaction-loses-history`). Two related-but-out-of-territory findings surfaced during analyst research and were kept OUT of this incident's scope per the one-incident-one-defect rule: (1) `STRATEGY.md`'s compaction losing decline-history texture — now its own QUEUED register row, `strategy-compaction-loses-history`; (2) a small arithmetic inconsistency in `token-economy`'s own closed `214-LOG.md` (a specialist self-report miscounting 2 of 3 files as "under budget" when they were already over) — a closed incident's historical record, nothing live to fix, noted for the Owner's awareness only.

## Type + rationale

**Proposed type:** 1
**Rationale:** The deliverable is a new merge-blocking check inside `tests/test_doctrine_integrity.py` — the enforcement mechanism itself under CLAUDE.md's carve-out rationale, and the exact shape `schema-citation-guard` ran as Type 1 while no-new-check `schemas-md-trim` ran as Type 3 — where the unresolved grandfather-vs-trim design reaches up to six files (4 of 10 workflows verified over budget, `plan.md` at 666) and carries both guard failure modes (false red blocks every close; false green grandfathers forever), in a repo whose only prior size check needed its own Type 1 hardening incident after shipping with a measurement defect. (IC=dcs-commander, fable)
**Owner confirmation:** confirmed as proposed (Type 1)

## Intake source (for /dcs-close to route back to)

`.dcs/esg/REGISTER.md` row `workflow-budget-enforcement` (rank 1, ninth `/dcs-esg`, 2026-07-28); originally `vault/Backlog.md` item 18, registered at `deploy-marker-blind`'s close, 2026-07-27.
