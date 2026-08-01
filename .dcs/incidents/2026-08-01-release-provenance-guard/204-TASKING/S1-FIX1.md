# 204 — Tasking S1-FIX1

**Incident:** release-provenance-guard
**Period:** 1 (fix-tasking after SAFETY-HALT, same period, no re-stamp — this
tasking is new, `IAP.md`'s content and `202-OBJECTIVES.md`'s criteria are
unchanged)
**Specialist:** dcs-ops-specialist (S1-FIX1)

## Why this exists

The Safety Officer halted period 1 on a real, independently-reproduced
refutation in the file you just wrote. Criterion 1's text is correct and
unchanged; the **implementation** falsified it.

## Task

**The refutation (fix this first):** `check_tag_at_head` in
`tests/release_provenance_check.py:148` resolves the tag with an
**unqualified refname**:

```python
tag_commit = _git_rev_parse(repo_root, tag + "^{commit}")
```

`git rev-parse` walks the full disambiguation order (`refs/tags/`, then
`refs/heads/`, then `refs/remotes/`), so a **branch** (or remote ref) named
`vV` satisfies this call even when **zero tags exist**. Verified
independently three times (Safety Officer, IC, and by reading the code):
a fixture with no tags at all, plus a branch named `v0.7.2` at `HEAD`,
made the shipped script print `PROVENANCE OK` and exit `0`. This falsifies
criterion 1's own text ("exit 1 when no git tag vV exists") and the
incident's goal.

**Fix:** qualify the ref to `refs/tags/` and use `--verify`, so only an
actual tag can satisfy the check — `refs/tags/<tag>^{commit}`, `git
rev-parse --verify`. The `HEAD` resolution call is unaffected; add
`--verify` there too only if it does not change its existing behavior
(it should not — `HEAD` always resolves). Keep the existing failure
message (`"no git tag %s exists"`) and the `^{commit}` peel logic itself —
the Safety Officer confirmed the peel is sound, only the ref namespace was
wrong.

**Add a seventh fixture:** zero tags, a branch named `vV` at `HEAD`,
otherwise-complete provenance (synced versions, real em-dash `CHANGELOG.md`
entry) — must exit `1` citing the no-tag message, not `0`.

**Then fold in these four advisories, confirmed by the Safety Officer
against the same file you are already re-editing:**

1. **Changelog regex crosses lines.** `changelog_has_entry`'s pattern uses
   `\s+` on both sides of the em dash, and `\s` matches `\n` — a *dateless*
   `## <V>` heading followed by any em-dash-leading line later in the file
   counts as a match. Change both `\s+` occurrences immediately around
   `EM_DASH` to `[ \t]+` so the heading must be a single physical line.
   Add a fixture: a bare `## <V>` heading (no date) with an unrelated
   em-dash-leading line elsewhere in the file — must exit `1` (no valid
   entry for `V`), not `0`.
2. **Undecodable files traceback instead of failing per their documented
   exit class.** `read_dcs_version` catches `OSError` only;
   `read_package_version` already catches `(OSError, ValueError)` — make
   `read_dcs_version` match it. `changelog_has_entry`'s file read has the
   same gap — wrap it the same way. Add two fixtures: `dcs/VERSION`
   written in a non-UTF-8 encoding (e.g. UTF-16LE) must exit `2` with the
   "cannot check" message, not traceback; an undecodable `CHANGELOG.md`
   must exit `1` via the no-entry failure, not traceback. Both must fail
   *closed* either way — verify the exit code and the printed message, not
   just "does it crash".
3. **Two hard-coded, perishable citations.** The module docstring (near
   the `CHANGELOG.md` convention description) and the `EM_DASH` comment
   both cite `"verified at CHANGELOG.md:28"` — a line number that will
   point at a different heading the moment the next release prepends an
   entry. Replace both with the regenerating command instead of the fixed
   number, e.g. `` grep -n "^## " CHANGELOG.md | head -1 ``, keeping the
   substantive claim (the real convention uses U+2014, not ASCII `--`).

**Do not touch `docs/publishing.md`** — its one remaining advisory
(qualifying the `npm pack`-is-unaffected claim with a measured npm version)
is S2's file and follows the normal integration-commit path, not this
fix-tasking.

## File territory (may edit only within these globs)

- `tests/release_provenance_check.py`

## Forbidden zones (explicitly, even if it seems related)

- `docs/**`
- `package.json`
- `tests/test_*.py`
- `tests/payload_check.py`
- `CHANGELOG.md`
- `dcs/**`
- `agents/**`
- `skills/**`
- `bin/**`
- `install.*`
- `README.md`

## Worktree root

`C:\DCS-wt\release-provenance-guard`

## Evidence required in the return

- The exact diff hunk fixing `check_tag_at_head`'s ref qualification —
  quote it verbatim.
- Fixture 7 (zero tags, branch named `vV` at `HEAD`) run and reported:
  must now exit `1`, quote the message.
- The full expanded fixture matrix re-run — all **nine** fixtures now
  (the original six, unchanged in expected outcome, plus the three new
  ones: branch-not-tag → `1`, dateless-heading → `1`,
  undecodable-dcs-VERSION → `2`, undecodable-CHANGELOG → `1` — that is
  four new fixtures, not three; count them explicitly in your return) —
  each with its numeric exit code.
- The live no-args run in this worktree, re-confirmed still exits `1`
  with the same tag-not-HEAD message as before (this fix must not change
  that outcome, only close the branch-masquerading-as-tag hole).
- `npm test` from the repo root — full pass, confirming the fix didn't
  regress anything criteria 3/5 already covered.
- Quote the two rewritten citation lines (advisory 3) verbatim, showing
  the regenerating command in place of the old fixed line number.

## On discovering the plan doesn't fit reality

STOP. Do not improvise a different fix. Return `status: "deviation"` per
`references/schemas.md` #4 (ops-specialist return), with `found`,
`why_plan_wrong`, and a `proposal` (a recommendation, not an action). The
IC will re-enter planning around your finding.
