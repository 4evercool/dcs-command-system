# IAP — Incident Action Plan

**Incident:** release-provenance-guard
**Type:** 3
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `204-TASKING/S1.md` · `204-TASKING/S2.md`
(`203-ORG.md` skipped this period — default Type 3 activation: IC +
Planning Chief + 2 specialists = 2 taskings, plain parallel)

## Objectives (summary of 202)

**Goal:** A version cannot be published to npm unless the commit being
published already carries a matching git tag and a truthful
`CHANGELOG.md` entry for that version — checked automatically at publish
time, never left to operator discipline. Enforcement shape chosen by the
Owner at command point 1: a blocking prepublish gate, with `npm test`
staying network-free. Structural consequence: tagging currently happens
at `docs/publishing.md` step 8, *after* `npm publish` at step 6 — a
prepublish tag-gate can never pass on a version's first publish attempt
under that order, so tagging must move ahead of publishing.

**Acceptance criteria:**

1. A new standalone script (`tests/release_provenance_check.py`, not
   `test_`-prefixed, not in `npm test`) checks, for `V` = `package.json`'s
   version: a **precondition** that `dcs/VERSION` equals `V` (unequal or
   unreadable → exit `2`, mirroring `payload_check.py`'s "cannot check"
   class); past that, exits `1` if no tag `vV` exists, OR that tag's
   commit ≠ `HEAD`, OR `CHANGELOG.md` has no entry for `V`; exits `0` when
   all hold. `CHANGELOG.md`'s real heading convention is `## <version> —
   <date>` with a literal U+2014 em dash (verified `CHANGELOG.md:28`), not
   ASCII `--` — the check is anchored to this exact convention.
2. `package.json`'s `scripts.prepublishOnly` invokes that script, so
   `npm publish` fails before any registry contact when provenance is
   incomplete. Verified this period: `prepublishOnly` fires on `npm
   publish --dry-run` (before any network activity) and does **not** fire
   on `npm pack` or `npm pack --dry-run` at all.
3. `npm test`'s script list and file count are unchanged.
4. `docs/publishing.md`'s numbered release steps are reordered so tag
   creation precedes `npm publish`, with every internal by-number
   cross-reference repaired.
5. `npm test` still passes in full; no existing test's assertions about
   `package.json` break.

Full text, including the amendment history and Chief feedback:
`202-OBJECTIVES.md`.

## Tactics (from the Planning Chief)

- Pattern the gate script on `tests/payload_check.py`'s conventions: no
  `test_` prefix, a docstring explaining why, `argparse --repo`, stdlib
  only, offline, and the exit-code discipline mirrored exactly (`0` holds,
  `1` incomplete/real failure, `2` cannot check).
- Four checks, not three: precondition `dcs/VERSION == package.json`
  version (unequal/unreadable → `2`); then for `V` = `package.json`'s
  version: tag `vV` exists; `git rev-parse vV^{commit} == git rev-parse
  HEAD`; `CHANGELOG.md` has a heading for `V`. Any of these three failing
  → `1`.
- CHANGELOG heading contract corrected to the real convention: `##
  <version> — <date>` with a single U+2014 em dash (verified
  `CHANGELOG.md:28`), regex anchored so `0.7.1` never matches `0.7.10`;
  read with `encoding="utf-8"` explicitly (the platform default mis-decodes
  the em dash's bytes, `E2 80 94`).
- Wire `package.json` `scripts.prepublishOnly = "python
  tests/release_provenance_check.py"`; `scripts.test` untouched.
- Six fixtures in scratch `git init` repos, never in this incident's
  worktree (it shares `refs/tags` with the canonical `C:\DCS` repo).
  Anti-drift rule: both clean fixtures' `CHANGELOG.md` is a byte-verbatim
  copy of the worktree's real `CHANGELOG.md` (`cp`/`shutil`, never
  PowerShell `Set-Content`/`Out-File` — BOM has twice broken hash
  comparisons in this repo), proven by matching sha256. The worktree
  itself is used read-only as one live red case: tag `v0.7.2` = `3d559ce`,
  `HEAD` = `998bcd4`, versions in sync at `0.7.2` → expected exit exactly
  `1`.
- Reorder `docs/publishing.md`: move the tag-and-push step (current step
  8) ahead of `npm publish` (current step 6); the GitHub Release step
  stays post-publish; renumber; repair every internal by-number citation
  (currently at lines 47, 73, 78); rewrite the two passages the reorder
  falsifies — the 0.7.1 bullet's now-false narrative, and the tag step's
  "someone tagged ahead of the publish" caveat, which inverts under
  tag-first ordering.
- Interface freeze so S1 and S2 can run in parallel without reading each
  other's diffs: the frozen strings are the filename
  `tests/release_provenance_check.py`, the trigger `prepublishOnly`, and
  the invocation `python tests/release_provenance_check.py`. The Safety
  Officer verifies the three-way match (docs prose == shipped filename ==
  `package.json` value) as a named check, not by relay.

## File-territory partition

| Specialist | Territory | Forbidden |
|---|---|---|
| S1 | `tests/release_provenance_check.py`, `package.json` | `docs/**`, `tests/test_*.py`, `tests/payload_check.py`, `CHANGELOG.md`, `dcs/**`, `agents/**`, `skills/**`, `bin/**`, `install.*`, `README.md` |
| S2 | `docs/publishing.md` | `tests/**`, `package.json`, `CHANGELOG.md`, `dcs/**`, `agents/**`, `skills/**`, `bin/**`, `install.*`, `README.md`, every other file under `docs/` |

**Partition status:** disjoint — parallel execution. Verified independently
three times this period (Planning Chief, IC via `fnmatch` script, and
`dcs-commander` at both `iap_review` passes): `S1`'s and `S2`'s territory
sets share no path and each side's forbidden list covers the other's
territory.

## Risks

- Interface coupling without file overlap: S2's prose names S1's script
  path and trigger before S1 has built it. Mitigated by the frozen
  interface strings above and closed by the Safety Officer's named
  three-way check (see Verification plan), not relay alone.
- Worktree ref pollution: this incident's worktree
  (`C:\DCS-wt\release-provenance-guard`) shares `refs/tags` with the
  canonical repo `C:\DCS`. Any `git tag` run in the worktree would create
  a real tag in the canonical repo. Both taskings treat fixtures-only
  (separate scratch `git init` repos) as a hard constraint.
- **Tag-audit baseline, recorded at IAP issuance per `dcs-commander`'s
  explicit requirement:** `git tag --list` in the worktree returns
  **exactly 33 tags, newest `v0.7.2`**, measured 2026-08-01 during
  planning and re-confirmed identical during the plan revision. Any
  delta at Safety review means a fixture tag leaked into the shared ref
  store — a halt-worthy finding, not a warning.
- The new script itself ships: `tests/` is in `package.json`'s `files:`
  whitelist, so `tests/release_provenance_check.py` and the reordered
  `docs/publishing.md` both enter the published tarball — same treatment
  `payload_check.py` already gets. Sequencing note for the sibling
  incident `shipped-set-defined-three-times`, which owns the shipped-set
  definitions; nothing here is absorbed into it, since
  `payload_check.py`'s walked roots (`dcs/`, `agents/dcs-*.md`,
  `skills/dcs-*/`) never include `tests/` regardless.
- npm-version dependence is probe-only: `prepublishOnly` firing on `npm
  publish --dry-run` was confirmed this period on this machine's npm;
  real `npm publish` runs `prepublishOnly` on every supported npm major,
  so enforcement does not hinge on the dry-run nuance — only the
  verification probe does. `npm --version` is recorded alongside.
- Bare `python` in `prepublishOnly` mirrors `scripts.test`'s existing
  convention. On a machine exposing only `python3`, the gate fails
  closed — it blocks publish with an interpreter error rather than
  silently passing. Acceptable failure direction for a guard.
- The gate is *correctly* red in this worktree right now (tag behind
  `HEAD`, no version bump yet) — that is designed behavior: the fix at
  real release time is bump + changelog + tag, in the reordered runbook
  order, never moving an existing tag.
- Em-dash encoding trap: reading `CHANGELOG.md` without explicit
  `encoding="utf-8"` mis-decodes the heading separator on some platform
  defaults; writing fixtures via PowerShell `Set-Content`/`Out-File`
  BOM-stamps them. The byte-verbatim clean-fixture rule is the designed
  tripwire against both — either mistake turns a clean fixture red
  instead of silently passing.
- Criterion 5 needs no edit to `tests/test_doctrine_integrity.py` —
  verified, not assumed: its only `package.json` checks are version-sync
  (`:255-257`) and size-under-8kB (`:415-416`); nothing in the suite pins
  `scripts`' shape (`grep` for `scripts` across the suite: zero matches).
  If a specialist finds an assertion missed here, that is a deviation to
  report — `tests/test_doctrine_integrity.py` stays out of this
  incident's territory.

## Verification plan

Safety Officer independently re-runs, not reads from either specialist's
report:

1. `npm test` from the repo root — each suite's own `N/M passed`; `git
   diff package.json` shows exactly one addition (`scripts.prepublishOnly`)
   with `scripts.test` byte-identical (criteria 3, 5).
2. The six-fixture matrix, re-executed: lightweight-clean and
   annotated-clean → `0`; no-tag, tag-not-HEAD, no-changelog-entry → `1`;
   version-mismatch → `2` — the `2`-vs-`1` distinctness is itself checked,
   not assumed. Both clean fixtures' `CHANGELOG.md` sha256-verified
   against this worktree's real `CHANGELOG.md` (criterion 1).
3. Criterion-2 probe, re-run in a fresh scratch fixture: `npm publish
   --dry-run` exits non-zero citing the script's message, before any
   registry contact; `npm pack --dry-run` in the same fixture still exits
   `0`. `--dry-run` only — a bare `npm publish` is never run by anyone but
   the Owner.
4. The live red case, re-run in this incident's worktree with no
   arguments: exits exactly `1` (tag `v0.7.2` = `3d559ce`, `HEAD` =
   `998bcd4`, versions in sync at `0.7.2` — so `1` via tag-not-HEAD, not
   `2`).
5. `docs/publishing.md`: tagging now precedes `npm publish`; every
   internal "step N" citation resolves to the correct renumbered step
   (cross-check `grep -nE "^[0-9]+\."` against `grep -noE "step [0-9]+"`);
   neither the 0.7.1 bullet nor the tag step's caveat still claims tagging
   happens after publishing.
6. **Named interface check:** the script path and trigger named in
   `docs/publishing.md`'s prose equal, character-for-character, the
   shipped filename `tests/release_provenance_check.py` and
   `package.json`'s `scripts.prepublishOnly` value
   (`python tests/release_provenance_check.py`) — a three-way string
   equality, checked directly, never taken on either specialist's word.
7. Territory audit: `git status` / `git diff --name-only` shows exactly
   three paths touched — `tests/release_provenance_check.py`,
   `package.json`, `docs/publishing.md` — and nothing else.
8. Tag-audit: `git tag --list` in the worktree returns exactly the 33-tag,
   `v0.7.2`-newest baseline recorded above under Risks. Any delta is
   halt-worthy.

## Deviation history (this period)

None — this is period 1's first (and, after two `iap_review` passes at
command point 2, only) IAP for this period. The two rejections that
shaped this document happened *before* IAP.md existed (command point 2,
still inside step 4) and are recorded in `214-LOG.md`, not here — this
section is for deviations discovered during execution that force a
return to planning, which has not yet happened this period.
