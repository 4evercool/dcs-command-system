# Fifteenth `/dcs-esg`, 2026-08-01 — the period review lands

Chair: Owner. Chief of Staff: main session (Fable). The session's whole
agenda was shaped by the external period review
(`vault/Post-mortems/deepseek-period-review.md`, DeepSeek-driven,
Owner-commissioned, covering 2026-07-29 → 07-31) and the ten rows the
Owner queued from it on 2026-08-01.

## Portfolio at close of session

29 DEPLOYED (4 out-of-band-qualified), 15 QUEUED (ranked 1–15,
contiguous), 1 PARKED (`halt-binding-status`), 10 KILLED, 3 RESOLVED
(`at-risk-records-preservation` this session), nothing ACTIVE, nothing
deploy-pending, no pending sitreps. Regenerate from the State column
itself, not a cell-boundary grep — qualified cells (`**DEPLOYED**
(out-of-band: ...)`) escape the anchored pattern:
`awk -F'|' '/^\| [a-z][a-z0-9-]* \|/ {s=$6; gsub(/^ +| +$/,"",s); print s}' .dcs/esg/REGISTER.md | sort | uniq -c`.
Note `QUEUED` cells are unbolded (one row, `type5-express-lane-tuning`,
had a stray bolded state cell — normalized this session).

## Decisions (all four put via one AskUserQuestion round)

1. **`revision-preservation-map` — restart** (over resume and kill).
   Grounds: the abandoned execution's paper trail belongs to the same
   +03:00 cluster whose logs the review found backfilled, and a safe
   resume depends on exactly that paper. Executed: all artifacts plus the
   three partially-executed payload edits committed as evidence on the
   kept branch (`dcs/revision-preservation-map` @ `497dcd4`, message
   marks it NOT a mergeable state), `.dcs/CLOSED` written, worktree
   removed, row → QUEUED at rank 3. The removal itself first failed with
   `Permission denied` from a shell cwd inside the worktree —
   live-reproducing the `close-md-lock-diagnostic-inert` scenario (rank
   5) — and succeeded from outside; logged here as one more field
   measurement for that row.
2. **At-risk records — rescued inline now** (over waiting for a ranked
   incident); row `at-risk-records-preservation` → RESOLVED. Rescue
   commit `064bd5b`: sole-copy `vault/Meta/ESG-sessions/` (18 files) +
   the post-mortem committed; `provisioning-script-upstreaming`'s 8
   untracked artifacts committed; four closed incidents' 214-LOG
   close-out tails committed; `status-md-enum-drift/AAR.md` restored from
   `5e09979`; Backlog items 27–28 extracted from `stash@{0}` and landed
   (**the stash itself is deliberately kept** — it also holds an
   identifier-based check-20 draft, prior art for
   `field-lesson-guard-vacuity`'s stem, rank 4, and applying its
   test-file hunk outside an incident would edit guarded territory);
   both `C:temp_s1_*.patch` root-debris files deleted (content already
   in `bf21a1f` per the review).
3. **Delegation amended v4 → v5: `auto_approve_type3` suspended
   (true→false).** Principle 12's grant presumes IC approvals are
   honestly logged; review §D found backfilled logs, a fabricated merge
   commit in a FACTS-ONLY 214-LOG, and closes missing mandatory
   artifacts — in that machinery. Reinstatement condition written into
   the v5 block: restore on `record-integrity-corrections` closing with
   a green Safety verdict. The `deploy` object untouched (its witness is
   content-based and does not depend on log honesty).
4. **Ranking accepted as proposed.** Rank 1
   `trim-content-loss-restoration` (H — the workflow trim dropped the
   no-Delegation fallback's `guarded_paths` condition from the shipped
   package, among other §B losses). Then: 2
   `doctor-silent-pass-and-bump-defects`, 3 `revision-preservation-map`
   (restarted), 4 `field-lesson-guard-vacuity`, 5
   `close-md-lock-diagnostic-inert`, 6 `shipped-project-facts-sweep`, 7
   `record-integrity-corrections`, 8 `russian-artifacts-translation`, 9
   `run-md-markup-corruption`, 10 `metrics-pass-counter-blind`, 11
   `halt-ceiling-re-anchor`, 12 `independent-fixture-authorship`, 13
   `type5-express-lane-tuning`, 14 `register-writer-map-completeness`,
   15 `strategy-compaction-loses-history`.

## Sequencing note

Rank 1 is the widest row (plan.md, execute.md, doctrine+appendix,
loop.md, the trim-damaged test comment chain) and collides with ranks 3,
4, 11, 12 — open it first and alone in that set. Ranks 7 and 8 share the
`.dcs/incidents/**` archives; ranks 6 and 14 share
`dcs/templates/REGISTER.md` (weigh folding at rank 6's stem).

## Worktree audit

Clean after this session's own acts: one worktree (main checkout), zero
unmerged `dcs/*` branches (`dcs/revision-preservation-map` holds only the
evidence commit and is kept deliberately), no orphans, no husks — the
`token-economy` husk and its holder PID 40876 disappeared between
sessions (machine restart), consistent with the orphaned-process
hypothesis recorded in `vault/Decisions/orphan-worktree-husk.md`.
