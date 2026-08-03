# IAP — Incident Action Plan

**Incident:** spawn-effort-control
**Type:** 1
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `203-ORG.md` · `204-TASKING/S1.md` · logistics plan below

## Objectives (summary of 202)

**Goal:** The IC's choice of which tier answers a spawn tracks that
spawn's actual complexity every time, not a value fixed once when the
seat was defined — using the mechanism that genuinely works today (the
Agent tool's existing per-call `model` override, since no per-call effort
parameter exists), phrased so it never assumes a specific provider's
effort vocabulary is universal.

**Acceptance criteria:**

1. `dcs/references/doctrine.md` states a rule for selecting a spawn's
   capability tier by that spawn's own complexity, grounded in the real
   per-call `model` override — not an unverified `effort:` parameter.
2. That rule and the existing availability-fallback rule are ONE
   mechanism, not two separate/competing principles.
3. The rule's vocabulary is provider-agnostic — never mandating Claude's
   low/medium/high/xhigh/max scale as the only shape a tier can take.
4. The existing Fable availability-fallback behavior for the four command
   points is unchanged in substance.
5. `python tests/test_doctrine_integrity.py` passes in full, including
   the hot-path budget check (ceiling stays fixed at 37 KB, no increase).
6. `python tests/test_dcs_gate.py` and `python tests/test_dcs_intake.py`
   stay green.
7. `dcs/references/doctrine-appendix.md` gains a field-lesson entry
   recording the platform-capability finding and why tier-substitution
   was chosen.
8. The rule ships with at least 2 concrete worked examples distinguishing
   a default-tier spawn from a deliberately stronger-tier spawn.

**Out of scope this period:** new per-tier charter file variants;
changing the six charters' existing static `model:` defaults; algorithmic
complexity scoring; actually spawning any DCS seat on a non-Claude
provider; waiting on a native per-call effort parameter.

## Tactics (from the Planning Chief)

- Rewrite in place, do not add. Criterion 2's "exactly one place" is
  satisfied most cheaply and most provably by generalising doctrine.md's
  EXISTING "Model availability:" paragraph (inside "Transfer of command")
  into one rule spanning both axes — availability and complexity —
  rather than adding a 17th principle or a new section. A new principle
  would cost bytes the tree does not have (17 free) and would itself be
  the second competing rule criterion 2 forbids.
- Split the rule by seat class, because criterion 1 and criterion 4
  otherwise contradict each other. The four command points must keep the
  availability rule EXACTLY as it is — preferred tier first every time,
  re-tested per spawn, never cached — so complexity-driven selection may
  never DOWNGRADE a command-point spawn; it governs the other six spawn
  classes (Planning Chief, Logistics Chief, Ops Specialists, Safety
  Officer, situation analysts) and may move those in either direction
  from their charter default.
- Ground the rule in the per-call `model` override, and name it. The
  interactive Agent tool has no per-invocation effort parameter, only
  `model`. The rule therefore describes tier substitution — the
  charter's `model:` frontmatter is the DEFAULT the per-call override
  starts from, never a ceiling or a floor — and never mentions an
  `effort:` key. Inversion-proof: `grep -ri effort agents/` must still
  return zero after this incident.
- Phrase provider-agnostically by construction, not by disclaimer. "the
  strongest tier the work warrants, from what is available for that
  seat's provider" names no vendor scale at all.
- FREEZE schemas.md, and the budget becomes one number. No 202 criterion
  requires a schema change, and adding a field to schemas.md #6 would
  cascade into agents/dcs-commander.md through the merge guard's field
  guard — a three-file ripple no criterion asks for. With schemas.md
  frozen at 13962 B, criterion 5 reduces to the single checkable fact
  `doctrine.md <= 23926 bytes, LF-normalised`.
- Change no workflow and no charter. doctrine.md is `@`-included by all
  four workflows that hold the ten spawn call-sites (new.md, plan.md,
  execute.md, esg.md), so the rule binds at every spawn with zero
  workflow edits. Measured line counts: plan.md 249/250, execute.md
  248/250, new.md 263/270 — the workflow line budget is a hard merge-guard
  ceiling. An empty diff over `dcs/workflows/` and `agents/` is the
  strongest possible form of criterion 4.
- Fund by RELOCATION, never by deletion, using the appendix convention
  that already exists. If in-paragraph compression cannot free the needed
  bytes, any prose leaving doctrine.md moves verbatim into
  doctrine-appendix.md as a new `### D5:` entry in the established D1-D4
  shape. Deleting hot-path prose without routing it to the appendix is
  the exact failure `trim-content-loss-restoration` (2026-08-01) existed
  to repair.
- Defend the trim with content anchors, not with review. Five fragments
  carry the availability guarantee and each occurs exactly once in
  doctrine.md today; all five must survive the rewrite verbatim, each
  proved by its own `grep -n -F`.
- Put the field lesson and the worked examples in doctrine-appendix.md,
  and give doctrine.md one explicit pointer to them. The appendix is
  never `@`-included so it is unbudgeted, and criterion 8 explicitly
  permits "a paired reference it points to."
- One tasking, deliberately. The funding trim's only lawful sink
  (doctrine-appendix.md) is the same file criteria 7 and 8 write to, so a
  two-way split would put a deletion from doctrine.md in one specialist's
  territory and its receipt in another's — reconstructing the precise
  content-loss mode this repo has already had an incident about.

## File-territory partition

| Specialist | Territory | Forbidden |
|---|---|---|
| S1 | `dcs/references/doctrine.md`, `dcs/references/doctrine-appendix.md` | `dcs/references/schemas.md`, `dcs/references/typing.md`, `dcs/references/forms.md`, `dcs/workflows/**`, `agents/**`, `skills/**`, `dcs/templates/**`, `dcs/hooks/**`, `dcs/tools/**`, `tests/**`, `bin/**`, `install.ps1`, `install.sh`, `package.json`, `dcs/VERSION`, `CHANGELOG.md`, `CLAUDE.md`, `README.md`, `docs/**`, `vault/**`, `.dcs/**` |

**Partition status:** disjoint — parallel execution (trivially, one
tasking; deliberately not split further — see Risks).

## Deploy / environment plan (Type 1 only, from the Logistics Chief)

**Deploy path:** `powershell -ExecutionPolicy Bypass -File C:\DCS\install.ps1`
(POSIX: `./install.sh`) — FULL payload deploy, run only via `/dcs-deploy`
from the canonical checkout `C:\DCS` after `/dcs-close` merges. No scoped
deploy exists: `install.ps1` copies the whole `dcs/` tree plus
`agents/dcs-*.md` plus `skills/dcs-*/`, so a two-file territory does not
produce a two-file ship. This incident does **not** ship alone — it joins
a deploy train already carrying two `MERGED (deploy pending)` rows
(`record-integrity-corrections`, merge `a62ffad`; `close-integrity-guard-bundle`,
merge `779773b`).

**Environment/dependency changes:**
- No new env vars. DCS defines none at all.
- No new package dependencies — guard and witness are stdlib-only Python;
  `package.json` engines stays `node>=16.7.0`.
- **No version bump, and this is a decision, not an omission.** The
  registry is at 0.7.2, the repo is already at 0.8.0,
  `CHANGELOG.md` already carries a `## 0.8.0` section, and no `v0.8.0`
  git tag exists. 0.8.0 is prepared-but-unpublished, so this change ships
  **inside** the existing unpublished 0.8.0 — `dcs/VERSION` and
  `package.json` stay untouched.
- `CHANGELOG.md`/`vault/` edits need no territory grant — neither is in
  `.dcs/config.json`'s `guarded_paths`, so the gate treats them as
  exempt; this is IC-level bookkeeping, not a specialist tasking.
- No config, frontmatter, or installer changes.

**Migration ordering:** No schema migration, no runtime service, no
restart. The real ordering constraint is CLAUDE.md's hard rule: never run
`install.ps1` while an incident is active (it swaps the workflows the
running session reads, mid-incident). Strict order: (1) merge-time guard
green in the worktree; (2) `/dcs-close` merges to main, row →
`MERGED (deploy pending)`, branch NOT deleted yet; (3) `/dcs-deploy` takes
`DEPLOY-LOCK`, runs `payload_check.py` before install; (4) `install.ps1`;
(5) `payload_check.py` again, disposition per `deploy.md` step 7; (6)
only then does the row move to `DEPLOYED` and the branch get deleted.
**This incident's own close runs under the OLD installed `close.md`
(v0.7.2)** — the new `close-integrity-guard-bundle` enforcement is merged
but not yet installed, so it will not fire on this incident's own close.

**Rollback plan:** No down-migration needed — this is a stated
conclusion, not an empty field. The change is prose in two files (one
rewritten in place, one appended), with no data, no schema, no persisted
state, and no new payload file. If it must be undone: `git revert` the
merge commit on main, re-run `install.ps1` (idempotent, overwrites
installed files with repo versions), confirm via
`python tests/payload_check.py --repo C:\DCS` expecting exit 0. Keep
branch `dcs/spawn-effort-control` alive until `deploy.md` step 7 confirms
the ship — do not delete it at close.

## Risks

**From the Planning Chief:**
- Partition trivially disjoint (one tasking). A two-specialist split
  would separate a deletion from its appendix receipt — the exact
  failure mode of `trim-content-loss-restoration` (2026-08-01).
- The 201's byte figure was stale (50 claimed, 17 live, since re-verified
  live by the IC at command point 2) because `close-integrity-guard-bundle`
  merged after the 201 was written.
- The merge guard cannot see semantic loss — it checks byte
  budgets/numbering/headings/encoding, nothing would go red if the
  rewrite silently dropped a guarantee while staying under budget. The 5
  verbatim anchors are the only mechanical defence; the Safety Officer
  must re-run them independently.
- Four merge-guard traps sit directly in this territory: the
  field-lesson-date-needs-identifier check (cost `trim-content-loss-restoration`
  two IAP rejects before), by-name section references from
  workflows/charters, principle 13's verbatim `GRAMMAR_LINE` quote
  requirement, and the appendix bare-census-without-regenerating-command
  check.
- Host encoding traps in evidence commands (not DCS defects, but they
  have produced false deviations before): `awk length()` counts bytes not
  characters on this host given dense em-dash usage; Python
  subprocess text-mode decodes as cp1251 here, not UTF-8. All evidence
  commands use `read_bytes()` with explicit CRLF normalisation.
- Residual, not fixed this period: criterion 2 is enforced by prose
  review only — nothing mechanical stops a future incident adding a
  second competing tier rule. Recommend registering as a follow-up.
- Residual: the rule reaches all 10 spawn call-sites only via doctrine.md's
  existing `@`-inclusion; no workflow spawn instruction cites the rule by
  name. Not affordable to fix this period — workflow line budgets have
  1-2 lines of slack against a hard 250-line ceiling.

**From the Logistics Chief:**
- Hot-path budget (17 bytes slack) is the deploy's single largest gating
  risk and fires at merge time, blocking deploy entirely if red.
- UTF-8 BOM would fail the guard's encoding check and
  `payload_check.py`'s sha256 comparison — Write/Edit tools only, never
  PowerShell `Set-Content`/`Out-File`.
- The pre-deploy witness is already red (44 identical / 6 differing / 1
  repo-only, exit 1) from prior merged-but-unshipped work — expected
  input for the coming deploy, not this incident's failure.
- The train is wider than this incident (also ships a rewritten
  `close.md` and new `record_integrity.py` from other rows) — attribute
  any post-install witness diff by filename, never assume this incident
  caused it.
- Section-rename risk: doctrine-appendix.md line 63 refers to the
  paragraph being rewritten as "Model availability rationale" — an
  unpropagated rename would break that by-name reference.
- Installing mid-incident must not happen — install is strictly after
  `/dcs-close`.
- Do not delete the branch at close — that's `deploy.md` step 8's act,
  after step 7 confirms.
- `npm publish` must not be improvised by a session — Owner-only,
  requires a 2FA OTP.

## Verification plan

The integrated picture, for the Safety Officer to check against —
re-derive everything, treat S1's numbers as claims, never as facts.

1. **Baseline comparison:** re-run all three suites from the worktree
   root and read each tool's own final line —
   `python tests/test_doctrine_integrity.py` (was 156/156 at
   `5e17284e56c85c599ae75efbd35fa7f258a74459`),
   `python tests/test_dcs_gate.py` (was 100/100),
   `python tests/test_dcs_intake.py` (was 18/18). Any FAIL is a
   refutation; criteria 5 and 6 both live here.
2. **Independent budget derivation:** do not accept S1's byte figures —
   re-run the `read_bytes`/CRLF-normalised one-liner and confirm sum
   <= 37888 with schemas.md at exactly 13962. Confirm
   `HOT_PATH_BUDGET_KB` in `tests/test_doctrine_integrity.py` is still
   37; a ceiling raise is a refutation regardless of what else passes,
   per the Owner's command-point-1 ruling.
3. **Read the rule, do not grep it:** open the rewritten paragraph in
   `dcs/references/doctrine.md` and judge criteria 1, 2 and 3 by reading
   — does it name the per-call `model` override as the mechanism it
   relies on (criterion 1); is there exactly ONE imperative rule
   governing how a spawn's tier is chosen, with the Hierarchy table and
   charter frontmatter left as defaults rather than competing rules
   (criterion 2); does its vocabulary select "the strongest tier the
   complexity warrants, from what is available" without asserting any
   vendor's scale as universal (criterion 3). Then read the WHOLE
   "## Transfer of command" section top to bottom to confirm no
   duplicate or conflicting tier rule was added elsewhere.
4. **The guarantee anchors:** re-run all five `grep -n -F` commands from
   S1's evidence contract. Each returned exactly one hit before the
   incident; each must still hit. A missing anchor is a criterion-4
   refutation even if every test is green — the guard cannot see this.
5. **The empty diffs:**
   `git diff --name-only 5e17284e56c85c599ae75efbd35fa7f258a74459 -- dcs/workflows/ agents/ dcs/templates/ tests/`
   must print nothing, and the same over
   `dcs/references/schemas.md`. This is criterion 4's mechanical half.
6. **The appendix entries:** resolve criteria 7 and 8 by content anchor,
   never by line number — a line-range citation is correct when written
   and wrong when read (`doctrine-hot-path-trim`, 2026-07-25). Confirm
   the field lesson records the platform-capability finding AND cites how
   it was verified, that its citation satisfies the field-lesson
   identifier rule, that at least two worked examples exist and are
   concrete, and that doctrine.md carries a specific pointer to them.
7. **Relocation integrity:** if S1 reports that prose left doctrine.md,
   confirm by anchor that the identical passage is now in
   doctrine-appendix.md and that its D-entry follows the D1-D4 shape. If
   S1 reports no relocation, diff doctrine.md and confirm no shipped rule
   was silently compressed away.
8. **The 201's gap, closed end to end:** read doctrine.md as a spawning
   workflow receives it (it is `@`-included by new.md, plan.md,
   execute.md and esg.md, which between them hold all ten spawn
   call-sites) and confirm an IC now has one stated, applicable rule at
   every one of them, and that the four command points' guarantee is
   intact. Run `grep -ri effort agents/` — it must still return zero.
9. **Manual check no test covers:** read the worked examples against
   CLAUDE.md's "ship no project facts" rule. Examples in
   `dcs/references/doctrine.md` must be neutral; inside
   `doctrine-appendix.md` an incident slug is admissible under that
   file's existing convention. A shipped payload file naming this repo's
   own paths is an advisory at minimum and a refutation if it lands in
   doctrine.md itself.

## Deviation history (this period)

none — first IAP this period.
