# IAP — Incident Action Plan

**Incident:** record-integrity-corrections
**Type:** 3
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `204-TASKING/S1.md` · `204-TASKING/S2.md` (`203-ORG.md` skipped — default Type 3 activation, see `214-LOG.md`)

## Objectives (summary of 202)

**Goal:** Every record-integrity failure the sixteenth `/dcs-esg` session named is corrected honestly, by appending new, clearly-labelled correction material — never by editing or deleting what a closed incident's own artifacts already say.

**Acceptance criteria:**
1. Append a correction to `halt-enumeration-grammar-drift/214-LOG.md` naming the fabricated `b4af6e4` and the real merges `f7e0cc9`/`838adea`; original line 37 untouched.
2. Append a correction addressing `workflow-file-trim-grandfathered/AAR.md`'s false verbatim-SAFETY.md attribution; `AAR.md` untouched.
3. Each of the three artifact-sparse incidents gets a new annotation file listing present/missing artifacts and confirming missing ones are irrecoverable; no existing file edited.
4. **[IC]** Fix `REGISTER.md`'s `token-economy-advisory-fixes` Branch cell.
5. **[IC]** Verify (no write) that `CHANGELOG.md`'s 0.7.1 entry already exists.
6. **[IC]** Zero pre-existing lines removed or modified anywhere in the four touched incident directories — the Safety Officer's primary check.

Full text, including verification commands and out-of-scope boundaries: `202-OBJECTIVES.md`.

## Tactics (from the Planning Chief)

- **T1 — The "closed-record correction" convention (five rules), designed for this incident since none existed:** (a) never edit or delete a pre-existing byte; (b) placement follows the artifact's own shape — `214-LOG.md` already has an append-only entry grammar, so its correction is a new entry in that grammar; every other touched artifact is a finished document with no entry grammar, so its correction goes in a new sibling file (`CORRECTION-2026-08-02.md`) rather than appended prose a reader could mistake for original content; (c) one fixed filename across every corrected directory, so `ls .dcs/incidents/*/CORRECTION-*.md` enumerates them; (d) one literal token, `RECORD-CORRECTION`, in every correction whether log entry or file, so `grep -rn "RECORD-CORRECTION" .dcs/incidents/` finds all of them; (e) every factual claim carries its regenerating command and that command's real output.
- **T2 — The anti-W4 rule:** a correction never claims a restoration it cannot show. Missing material is described as "confirmed never committed to this repository under any ref present at the time of the check; irrecoverable" — never as "restored verbatim". (`doctrine-appendix.md:658-670`, field lesson W4, `register-field-repair-path` — the same false-restoration shape this incident must not repeat one level up.)
- **T3 — Fixed head-matter** for every sibling correction file: H1, corrects/issued-by line, a bold "nothing edited or deleted" line, then per-claim sections (claim as recorded / what is actually true / regenerating command and output).
- **T4 — Criterion 1's pinned facts**, independently verified by the Chief: `b4af6e4` is not a git object and appears nowhere in `git log --all`; `48ea59a` (named at `214-LOG.md:36`) is a single-parent, non-merge commit; `f7e0cc9` and `838adea` are the two real merge commits that actually integrated this incident's work, both ancestors of main.
- **T5 — Guard interactions:** the appended entry must not place a `IAP-APPROVED:`/`SAFETY-HALT:`/`SAFETY-PASS:` sentinel token right after its timestamp; must not contain the literal string `re-stamp` (today, 2026-08-02, is `test_doctrine_integrity.py`'s `_PM_EFFECTIVE_DATE`, so that string would misfile the entry as a preservation-map re-stamp); any quoted prior entry is indented off column zero; no correction re-pastes the fabricated JSON verdict inside a ` ```json ` fence (check 21 parses every fenced JSON block in `SAFETY.md`/`AAR.md`/`214-LOG.md` — a sibling `CORRECTION-*.md` sits outside that walk, reinforcing T1(b)'s placement choice).
- **T6 — Census method:** both the per-artifact `git log --all --full-history` command criterion 3 names, and a whole-history slug sweep (`git log --all --full-history --pretty=format: --name-only -- "*<slug>*" | sort -u`) as decisive evidence ruling out a same-content rename. The Chief ran this sweep at planning time; it returned exactly the files present on disk for all three sparse incidents.
- **T7 — Two specialists, partitioned by directory**, sitting exactly at Delegation v5's `max_specialists: 2` and `max_files: 4`. S2 single-authors all three census files for cross-file consistency, since the convention is brand new and its value depends on the three files matching.
- **T8 — English only.** Does not translate or touch the Russian-language `worktree-removal-self-conflict/AAR.md` (separately registered as `russian-artifacts-translation`). Write/Edit tools only, never PowerShell `Set-Content`/`Out-File` (BOM risk).

## File-territory partition

| Specialist | Territory | Forbidden |
|---|---|---|
| S1 | `.dcs/incidents/2026-07-30-halt-enumeration-grammar-drift/214-LOG.md` | every other file in that directory; the other three touched directories; this incident's own directory; `.dcs/esg/**`; `CHANGELOG.md`; `dcs/**`; `tests/**`; `agents/**`; `skills/**`; `bin/**`; `install.ps1`; `install.sh`; `package.json`; `vault/**` |
| S2 | `.dcs/incidents/2026-07-30-workflow-file-trim-grandfathered/CORRECTION-2026-08-02.md`, `.dcs/incidents/2026-07-29-check-14-hardening/CORRECTION-2026-08-02.md`, `.dcs/incidents/2026-07-29-worktree-removal-self-conflict/CORRECTION-2026-08-02.md` | the 5 pre-existing AAR.md/SAFETY.md files in those 3 directories (named individually); `halt-enumeration-grammar-drift/**`; this incident's own directory; `.dcs/esg/**`; `CHANGELOG.md`; `dcs/**`; `tests/**`; `agents/**`; `skills/**`; `bin/**`; `install.ps1`; `install.sh`; `package.json`; `vault/**` |

**Partition status:** disjoint — parallel execution. Verified mechanically by both the Planning Chief and `dcs-commander` (command point 2, accept): four literal file paths in four distinct directories, no globs to collide, each cross-listed in the other's `forbidden`, this incident's own directory excluded from both.

Criterion 4 (`REGISTER.md`'s Branch cell) is **deliberately untasked** — `.dcs/esg/` is git-ignored and exists only in the main checkout (`esg_root`), unreachable by any worktree-spawned specialist. The IC performs this edit directly, outside the partition, under the `REGISTER-LOCK` protocol — see Verification plan, part 6.

## Risks

- **Bounds sit exactly at the ceiling.** Delegation v5: `max_specialists: 2` (2 used), `max_files: 4` (1 modified + 3 created). Any addition — e.g. a symmetry file in `halt-enumeration-grammar-drift` — breaches `max_files` and needs a fresh bounds decision, not a quiet add. `auto_approve_type3` is `false` regardless, so Owner approval is required either way.
- **Second-order fabrication is the primary threat to this incident's own value.** Correcting a false citation with a differently-false one would repeat the exact `register-field-repair-path` W4 defect shape one level up. Mitigated by pinning independently-verified ancestry facts in tactic T4, requiring a regenerating command for every claim, and instructing S1 explicitly: if evidence disagrees with the entry's wording, the entry changes, not the evidence.
- **Guard couplings on S1's single line:** `vault/_scripts/incident_metrics.py`'s `collect()` walks every incident directory; `dcs_gate.py`'s `ENTRY_PREFIX` grammar and `test_doctrine_integrity.py`'s `_PM_EFFECTIVE_DATE` (today) both react to specific tokens/strings. Addressed by explicit prohibitions in S1's tasking plus mechanical grep proofs in its evidence.
- **`git diff --numstat HEAD` is blind to untracked files** — must be paired with `git status --porcelain` or criterion 6 passes vacuously. After the IC's integration commit, re-run rebased to `git diff --numstat 86fb74d..HEAD` (`86fb74d` = this worktree's pre-incident base commit).
- **The Russian AAR next door:** `worktree-removal-self-conflict/AAR.md` is Russian-language and belongs to the separate `russian-artifacts-translation` row. S2 must write an English correction beside it without translating, rewriting, or extensively quoting it.
- **Prior provenance:** `halt-enumeration-grammar-drift/214-LOG.md` already carries two commits (`dc570c7` original archive, `064bd5b` a fifteenth-`/dcs-esg` rescue-commit touch) — not a conflict, but "the original record" S1's byte-identity check diffs against is `064bd5b`'s version, i.e. current HEAD.
- **Outbound-field-guard count:** do not hardcode an expected finding count in evidence gathering — `dcs-commander` flagged that the suite prints per-check lines, not a fixed summary number; anchor on the actual printout each time.

## Verification plan

Baseline, measured at worktree HEAD `86fb74d` before any specialist runs: `python tests/test_doctrine_integrity.py` → `133/133 passed`; preservation-map field guard `0 ... in scope`.

**End-to-end "done" has six parts:**

1. **Criterion 6 (primary Safety check).** `git diff --numstat HEAD -- <4 incident dirs>` — expect exactly one row (S1's file) with `0` in the deletions column, **paired with** `git status --porcelain -- <4 dirs>` (expect exactly three `??` + one ` M`, nothing else — the numstat check alone is blind to new untracked files). After the IC's integration commit, rebase to `git diff --numstat 86fb74d..HEAD -- <4 dirs>` (now four rows, all `0` deletions); strongest single form: `git diff 86fb74d..HEAD -- <4 dirs> | grep -c '^-[^-]'` must print `0`.
2. **Criterion 1.** Re-verify independently of S1's self-report: `git cat-file -t b4af6e4` still fails; `git log --all --oneline | grep -c b4af6e4` still `0`; `git cat-file -t f7e0cc9`/`838adea` both `commit`; `git log -1 --format` on both matches the entry's wording; `git merge-base --is-ancestor 48ea59a f7e0cc9` holds; byte-identity (`sha256sum` of `HEAD:<log>` vs. `head -n 37 <log>`) matches; grammar proof (sentinels only at pre-existing lines 32/35, `grep -c "re-stamp"` is `0`).
3. **Criterion 2.** `git log --all --full-history -- "**/workflow-file-trim-grandfathered/SAFETY.md"` still empty; correction text present; `AAR.md` unchanged (proven by part 1); `grep -n '```json' .dcs/incidents/*/CORRECTION-2026-08-02.md` returns nothing.
4. **Criterion 3.** All three `CORRECTION-2026-08-02.md` files exist. The Safety Officer re-derives the census itself via the whole-history slug sweep rather than trusting the files; confirms irrecoverability is stated as annotation, never restoration (the W4 bound); confirms structural uniformity across all three.
5. **Criterion 5 [IC].** `grep -n "^## 0.7.1" CHANGELOG.md` → `117:## 0.7.1 — 2026-07-30`; `git diff HEAD -- CHANGELOG.md` empty.
6. **Criterion 4 [IC], outside the worktree.** In `esg_root` (`C:\DCS`), under the `REGISTER-LOCK` protocol: confirm the branch is gone (`git branch -a --list "*token-economy*"`), edit the Branch cell to `— (deleted)`, release the lock, regenerate `register-view.html`, and paste the read-back (`grep -n "token-economy-advisory-fixes" REGISTER.md`) into `214-LOG.md` — the only durable evidence this edit happened, since it rides no commit and appears in no diff.

**Whole-suite gate**, run once at the end from the worktree: `python tests/test_dcs_gate.py`, `python tests/test_dcs_intake.py`, `python tests/test_doctrine_integrity.py` — read each suite's own printed `N/M passed` rather than any count written down anywhere.

**Manual check:** open each of the four touched directories the way a future auditor would and confirm the goal literally holds — the original flawed record is visible and intact, a clearly dated correction sits beside it, and no reader could mistake which is which. Then confirm the convention is discoverable: `grep -rn "RECORD-CORRECTION" .dcs/incidents/` must find every correction this incident made, in both its forms, in one command.

## Deviation history (this period)

none — first IAP of period 1.
