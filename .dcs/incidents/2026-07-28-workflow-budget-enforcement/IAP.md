# IAP — Incident Action Plan

**Incident:** workflow-budget-enforcement
**Type:** 1
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `203-ORG.md` · `204-TASKING/*.md` · logistics plan below

## Objectives (summary of 202)

**Goal:** A `dcs/workflows/*.md` file exceeding its allowed line-count ceiling is caught mechanically at merge time, every time — not only when someone remembers to run `wc -l` by hand or an IC improvises a ruling mid-incident. The four files already over CLAUDE.md's ~250-line policy (`plan.md`, `execute.md`, `deploy.md`, `close.md`) get a deliberate, documented, finite grandfather ceiling instead of either silently passing forever or immediately reddening the merge-time guard on day one; the six currently-compliant files hold the policy ceiling itself.

**Acceptance criteria:**
1. `tests/test_doctrine_integrity.py` gains a new check enumerating `dcs/workflows/*.md` (reusing `workflows()`, lines 175-176) that fails the suite if any file exceeds its per-file ceiling.
2. All ceilings set so the suite is green (exit 0) against the tree as this incident leaves it — command + verbatim output as evidence.
3. Six compliant files hold the plain ~250-line ceiling; the four over-budget files get an explicit grandfather ceiling at their own current line count, with a derivation comment (principle 15).
4. The measurement normalises line-ending representation before counting, matching the `HOT_PATH_BUDGET_KB` idiom, defending the lone-CR / missing-trailing-newline hazard.
5. `CLAUDE.md`'s "File size" rule is corrected so "see the guard" unambiguously names the new check, and states the four files' grandfather status plainly.
6. No previously-passing check regresses — baseline 85/85, exit 0, plus exactly the one new check.
7. `AAR.md` records, or explicitly declines with reasoning, a follow-up register row for trimming the four grandfathered files. **[IC]**
8. `dcs/VERSION` + `package.json` bumped together (0.6.11 → 0.6.12), `CHANGELOG.md` gains an entry. Added after chief planning surfaced that this incident's shipped payload (`tests/`, which npm's `files` whitelist ships) would otherwise sit under an already-published version label.

Full text with rationale: `202-OBJECTIVES.md`.

## Tactics (from the Planning Chief)

- Land the enforcement as ONE new check (17) at the tail of `tests/test_doctrine_integrity.py`, reusing the existing `workflows()` enumerator — one `check()` call whose name states every condition in its conjunction (house idiom: a PASS line must not claim more than its condition delivers).
- Two named constants: `WORKFLOW_BUDGET_LINES = 250` (the policy ceiling) and `WORKFLOW_GRANDFATHERED_LINES` (a dict of the four over-budget files). Effective ceiling = grandfather entry if present, else the policy constant — any workflow file added in future defaults to 250, no inherited exemption.
- Grandfather ceilings set **exactly** at current counts (zero headroom): `close.md` 273, `deploy.md` 282, `execute.md` 424, `plan.md` 666. Headroom is the mechanism that failed before — `deploy.md` drifted 265 → 275 → 282 through two ad hoc ceilings each leaving slack. Nothing in this period's own taskings touches a workflow file, so a zero-headroom ceiling cannot be tripped by this incident's own work. **IC ratifies this as the deliberate design choice**, not a default — it directly targets this incident's own root cause.
- Extend the hot-path normalisation idiom (byte-level CRLF/lone-CR collapse) to line counting, plus a trailing-newline correction (deliberately divergent from raw `wc -l`, documented as such).
- Fold three staleness tripwires into the same check's boolean: a grandfather entry naming a file that no longer exists, a grandfather entry now slack (file has fallen to ≤250 — the entry must be deleted, not left as a dead exemption), and an empty population. Same degeneracy-guard idiom as checks 13/15. Keeps the case count at 86, matching criterion 6's literal reading.
- Record the derivation, not just the number, beside each grandfather value — `plan.md`'s comment must show the 422 basis (as recently as `623582f`, same-day growth to 666 via `e285108`/`807edb8`), so the entry reads as recording a same-day regression, not blessing a stable state.
- Bind prose to mechanism by identifier: `CLAUDE.md`'s corrected rule names the literal constants, so a grep across both files is the proof of criterion 5, not a reviewer's opinion.
- Version bump (criterion 8) and CHANGELOG entry are their own tasking (S3), disjoint from S1/S2, because dcs/VERSION and package.json are guarded paths outside both chiefs' existing territories, and doctrine's hierarchy table bars the IC itself from writing code ("IC ... Writes no code").

## File-territory partition

| Specialist | Territory | Forbidden |
|---|---|---|
| S1 | `tests/test_doctrine_integrity.py` | `CLAUDE.md`, `dcs/**`, `tests/payload_check.py`, `tests/test_dcs_gate.py`, `tests/test_dcs_intake.py`, `tests/fixtures/**`, `agents/**`, `skills/**`, `package.json`, `install.ps1`, `install.sh`, `vault/**` |
| S2 | `CLAUDE.md` | `tests/**`, `dcs/**`, `agents/**`, `skills/**`, `bin/**`, `package.json`, `install.ps1`, `install.sh`, `vault/**`, `README.md` |
| S3 | `dcs/VERSION`, `package.json`, `CHANGELOG.md` | `tests/**`, `CLAUDE.md`, `dcs/workflows/**`, `dcs/references/**`, `dcs/hooks/**`, `dcs/templates/**`, `agents/**`, `skills/**`, `bin/**`, `install.ps1`, `install.sh`, `vault/**`, `README.md` |

**Partition status:** disjoint — parallel execution. All three territories verified non-overlapping (tasking lint 4a check 4). S2's evidence items 2-3 have a soft data dependency on S1 (cross-grepping S1's constant names) — handled by instructing S2 to report a missing hit verbatim and stop rather than guess, not by a partition change.

## Deploy / environment plan (Type 1 only, from the Logistics Chief)

**Deploy path:** Full install, post-close only, from `C:\DCS` — never from the worktree (`install.ps1` takes `$PSScriptRoot` as its source; running it from the worktree would install the branch). Standard `/dcs-deploy` sequence: `tests/payload_check.py` (before) → `install.ps1` → `tests/payload_check.py` (after) → `deploy.md` step 7 disposition. This incident's effective payload delta is small: neither `tests/test_doctrine_integrity.py` nor `CLAUDE.md` is in the installed payload (`install.ps1` copies only `dcs/`, `agents/dcs-*.md`, `skills/dcs-*/`) — only `dcs/VERSION` (via S3) is. Payload-check baseline measured 2026-07-28 at `C:\DCS`: exit 0, 47 identical.

**Env/dependency changes:** None. No new env var, no new package dependency (the check is stdlib-only Python, matching CLAUDE.md's hooks rule), no new `.dcs/config.json` key. Version files move together in S3 per CLAUDE.md's atomic-sync rule.

**Migration ordering:** None (no schema, no data store, no service restart). The one ordering decision is the version bump itself: `npm view dcs-command-system version` = 0.6.11 = `dcs/VERSION` (measured live) — landing this change under an already-published label would repeat the exact "published twice with different contents" defect `0.6.10`'s own CHANGELOG entry records. Bump lands in S3, in the same commit as the rest of this period's integration, before merge.

**Rollback plan:** Revert-and-reinstall — nothing here is destructive or stateful, no down-migration needed. Rollback reference: branch `dcs/workflow-budget-enforcement`, kept until `/dcs-deploy` confirms the ship. Before deploy: `git revert -m 1 <merge sha>` on `main` at `C:\DCS` alone suffices (installed copy never received the change pre-deploy). After deploy: same revert, then re-run the install command from `C:\DCS`; `payload_check.py` should return to exit 0. Blast radius is bounded by construction — the new check is merge-time only, lives in `tests/`, is never installed to `~/.claude/`, and is read by no running session/hook/workflow, so a bad ceiling blocks a merge but cannot break a live session. The one irreversible step, `npm publish`, stays Owner-only and last, per CLAUDE.md.

## Risks

- **Merge-result drift (highest risk, documented precedent in this exact file).** Criterion 3 pins ceilings to the integration commit, but S1 measures the branch. `test_doctrine_integrity.py:108-116` records `HOT_PATH_BUDGET_KB` getting this exact scenario wrong once (budget derived on a branch, `schemas.md` grew on `main` underneath it, would have landed red at merge). Exposure right now is zero (`git log main..HEAD` / `HEAD..main` both empty, single worktree, no other incident open — verified, not assumed) but zero-headroom ceilings mean ANY workflow growth landing on `main` before merge turns `close.md` step 1a red. **Mitigation, binding on the IC at close:** re-measure the ceilings against the merge result immediately before merging (verification plan step 5 below), not once at plan time. If red, re-derive from the merged tree — never widen pre-emptively.
- `plan.md`'s grandfather ceiling of 666 records a same-day 244-line regression (422 at `623582f` → 663 at `e285108` → 666 at `807edb8`, all 2026-07-28), not a settled state. Strengthens the case for criterion 7's follow-up row; S1's required comment must carry the 422 basis so the debt's true size is visible.
- `new.md` at 242 has 8 lines of headroom against a ceiling that stops being advisory the moment this lands — the first future incident to edit it meets a red merge guard. Correct behavior, but a surprise with a cost; S2 is tasked to say the ceiling is now hard, not advisory.
- **Green proves nothing about red.** A budget check only ever observed passing is indistinguishable from an inverted comparator or a dict-key typo. This suite has paid for that twice already (check 15 Rule B removed at halt 3 for over-claiming; check 13 built with a forged-mapping case for the same reason). S1's two red-path demonstrations are load-bearing evidence — a return omitting them is incomplete, not merely light on ceremony.
- Criterion 6's count language (86/86 aggregate vs. 95/95 per-file) is ambiguous; IC ratifies the aggregate reading (one `check()` call, all four conditions in its name) as binding — see Chief feedback in `202-OBJECTIVES.md`.
- Check 16 couples S1's file to `tests/payload_check.py` (`EXCLUDED_DIRS`/`BYTECODE_SUFFIXES` must stay textually identical); handled by forbidding `payload_check.py` outright in S1's territory and naming the constants explicitly in its task text.
- S2's evidence items 2-3 are inconclusive if S2 finishes before S1 lands — handled by instructing S2 to report a missing hit verbatim and stop, not guess (this is a convenience ordering issue, not a partition problem).
- Neither `tests/test_doctrine_integrity.py` nor `CLAUDE.md` is in the installed payload, so the deploy-time content witness will read identical on those two files regardless of this incident; only `dcs/VERSION` (via S3) is payload-visible. Whether this incident's merge alone warrants a version bump is answered by the atomic-sync rule (yes — matches this project's consistent per-incident bump convention) rather than being a formality.

## Verification plan

1. Re-run the 201's own three commands, expecting an inversion of the gap: `wc -l dcs/workflows/*.md` UNCHANGED (trimming is out of scope — `close.md` 273, `deploy.md` 282, `execute.md` 424, `plan.md` 666 still numerically over 250, now under their own explicit ceiling instead); `python tests/test_doctrine_integrity.py` green with the new check named in its output; `grep -rn '250' --include='*.py' .` — zero hits at intake, must now return hits (S1's own constant). This third command flipping from empty to non-empty is the most direct demonstration the gap closed.
2. All three suites green per CLAUDE.md's "Run all three before any close": `test_dcs_gate.py`, `test_dcs_intake.py`, `test_doctrine_integrity.py`, each read from its own printed `N/M` line.
3. Review S1's two red-path demonstrations (budget-rule FAIL via `close.md` 273→272, tripwire FAIL via a phantom dict entry) — each must show a FAIL line, non-zero exit, and a proven revert. A green-only return does not satisfy criterion 1.
4. Cross-surface consistency: `CLAUDE.md`'s stated ceilings equal `WORKFLOW_GRANDFATHERED_LINES` exactly; `CLAUDE.md` carries the check's literal identifiers so a grep hits both files.
5. **The criterion-3 re-measure S1 structurally cannot perform itself:** at `close.md` step 1a, run `python tests/test_doctrine_integrity.py` against the **merge result**, not either branch. If a workflow file grew on `main` while this incident was open, the ceiling is stale — re-derive it from the merged tree, never widen pre-emptively.
6. Manual read: each grandfather ceiling's inline comment states its derivation, not only its value — `plan.md`'s must show the 422 basis.
7. Scope discipline: `git diff --name-only main..HEAD` lists exactly `tests/test_doctrine_integrity.py`, `CLAUDE.md`, `dcs/VERSION`, `package.json`, `CHANGELOG.md`, and the incident directory — any other `dcs/workflows/*` or `dcs/**` file appearing means the out-of-scope line was crossed.
8. Criterion 8: `git diff dcs/VERSION package.json` shows the atomic bump; `CHANGELOG.md` carries the new entry above `0.6.11`; `npm view dcs-command-system version` re-confirmed at 0.6.11 (unpublished still — this incident does not publish) so the bump is a repo-local prep step, not a claimed ship.

## Deviation history (this period)

none — first IAP for period 1
