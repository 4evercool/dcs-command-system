# IAP — Incident Action Plan

**Incident:** register-field-repair-path
**Type:** 3
**Operational period:** 1 (revision 2, repaired -- criterion 6 fixed and
twice Safety-verified; criterion 5's answer restored to this file after a
second halt found it had been silently dropped from the revision-2
rewrite, see "Criterion 5, answered" below and Deviation history;
criteria 1-4 Safety-verified twice, not reopened)
**Links:** `202-OBJECTIVES.md` · `204-TASKING/S3.md` (203-ORG.md skipped:
default Type 3 activation, single specialist)

**Supersedes:** this repair's own prior stamp (revision 2's `IAP-APPROVED`,
hash `123657f4c460...`), voided by the criterion-5 restoration edit itself
-- the IAP-edit-voids-approval mechanism working as intended, not a bug.
That stamp had already superseded revision 1's (`a6e93fbf0de6...`, voided
by the criterion-6 rewrite). Revision 1's `204-TASKING/S1.md` and `S2.md`
remain the true record of that revision's Safety-verified work and are not
superseded by any of this.

## Objectives (summary of 202, revision 2)

**Goal (unchanged):** An Owner-authorized fix applied entirely outside the
DCS incident lifecycle has one documented, mechanical way to be recorded
in the register afterward -- reusing `RESOLVED`, qualified, not an eighth
enum token.

**Acceptance criteria 1-4: unchanged from revision 1, already Safety-
verified twice (revision 1 and this revision's re-check: zero refutations
both times).** Not reopened; their delivered content lives entirely in
`dcs/templates/REGISTER.md` and `dcs/workflows/esg.md`, protected by the
pinned-hash evidence requirement in `204-TASKING/S3.md`
(`b2450322f3a1bb848c474bab1285ea772cf1a65cc0e2608a935f31ffb5e81f8a`) --
**this pin covers criteria 1-4 only.**

**Criterion 5 [IC]: restored below** ("Criterion 5, answered"), after
Safety halt #2 (2026-07-27T20:43:41+11:00) found this section missing from
the revision-2 rewrite of this file. Its deliverable is IAP prose, not
payload-file content, so the criteria-1-4 pin above **cannot and does not
protect it** -- that claim, as it read before this correction, was itself
part of what the officer refuted. **Correction (Safety verdict 3):** the
text below is a **reconstruction**, not a verbatim recovery -- neither
`214-LOG.md`'s 2026-07-27T17:55:39+11:00 entries nor
`.dcs/esg/REGISTER.md` line 94's (differently-worded, partial) quotation
contain this section's actual prose; a tree-wide grep for its distinctive
phrasing finds no on-disk source but this file. It is re-verified on its
merits instead -- against `dcs/workflows/esg.md` steps 1 and 4,
`dcs/templates/REGISTER.md`'s header, `package.json`'s `files` whitelist,
and the roadmap -- by the Safety Officer at the repair re-check, and holds.

**Criterion 6 (revision 2, replacing the refuted original):** `CHANGELOG.md`
records the change under a new `## Unreleased` heading (inserted directly
above `## 0.6.10 — 2026-07-26`), not inside the `0.6.10` section --
re-measured this revision, not inherited: `npm view dcs-command-system
version` and `npm view dcs-command-system time --json` both confirm
`0.6.10` is already published (as of 2026-07-27T05:39:23Z), so there is no
"current open" version section to write into. The `## 0.6.10` section
must return to byte-for-byte equality with the published tarball's
`CHANGELOG.md` -- i.e. revision 1's addition to that section is reverted,
not merely supplemented. No version bump, no edit to `dcs/VERSION` or
`package.json`.

**Original criterion 6 (revision 1) — refuted 2026-07-27 by the Safety
Officer:** "`CHANGELOG.md` records the change in the current open
(unpublished) version's section..." -- the premise was inherited from
`direct-resolution-lane`'s AAR, true when written, stale by the time this
incident used it. 0.6.10 published 49 minutes before this incident's own
201-BRIEF was drafted.

**Why the revert is safe (measured, not assumed):** the npm publish
(2026-07-27T05:39:23.099Z = 16:39:23+11) happened AFTER
`direct-resolution-lane`'s merge `05d63b0` (2026-07-27T16:03:14+11:00 =
05:03:14Z per `git log`), so the published tarball already contains that
sibling incident's own `RESOLVED` bullet. The revert therefore deletes
nothing that hasn't already shipped. Confirmed: `git show
HEAD:CHANGELOG.md` and the packed `dcs-command-system@0.6.10` tarball's
`CHANGELOG.md` are byte-identical, both sha256
`9ae04cccee1304ca9d5181e6742a177b0788004c425e7598723f053f9ce46c82`.

## Criterion 5, answered (recording vs. routing)

**`dcs/workflows/esg.md`: IN.** The Chief of Staff at `/dcs-esg` is the
register's owner and the only seat that could originate this row; its step
1 sweeps only `QUEUED` rows and step 4's Record bullet presumes a row
already exists, so the writer the template names has no live moment to act
in today. `esg.md` also ships on channel 1 (`npm i -g`) and so reaches
every EXISTING project, whereas the template reaches only newly founded
registers.

**`dcs/references/doctrine.md`: OUT.** This incident documents how to
RECORD work that already happened, not WHEN work may legitimately bypass
DCS's lifecycle -- that routing question is the roadmap's Phase 1 item 3,
whose live owner is `decomposition-backlog-routing` (rank 9) -- **not**
`trivial-work-inline-lane`, which is `KILLED` (folded into
`decomposition-backlog-routing` at the sixth `/dcs-esg`; corrected here per
Safety verdict 3, which also found `REGISTER.md` line 94 citing the same
stale name; regenerate with `grep -n "trivial-work-inline-lane"
.dcs/esg/REGISTER.md`). It is the incident that will owe a doctrine rule if
any. Follows `direct-resolution-lane`'s "no doctrine rule changes here"
precedent rather than departing from it. Secondary: the hot path
(doctrine.md + schemas.md) has 1,205 B of slack against a 37 kB ratchet
that must not move without cause.

## Tactics (from the Planning Chief, revision 2)

1. Revert by git, not by hand: `git checkout HEAD -- CHANGELOG.md` reaches
   the byte-for-byte target exactly (proven equal above), with no risk of
   an off-by-one deletion and no risk of touching the sibling incident's
   bullet in the same section.
2. Insert `## Unreleased` following the file's own section-boundary
   convention (blank / `---` / blank between every existing section,
   verified at the 0.6.10/0.6.9 boundary) -- strictly above the `0.6.10`
   heading, never retyping that heading line.
3. Move the bullet verbatim except one sentence that becomes false in the
   new position: "the same qualifier shape as `MERGED (deploy pending)`
   above" -- both referents (lines 119, 133 of the reverted HEAD file --
   IC-corrected from an earlier draft's pre-revert coordinates 131/145,
   which are offset by the 12-line insertion) sit in `0.6.10`'s `###
   Changed`, now BELOW the new section. Required correction, not left to
   the specialist's eye.
4. Re-run the integrity suite and cite its own output rather than carry
   revision 1's number forward (principle 15); `CHANGELOG.md` is
   deliberately outside check 14/15's walked population
   (`tests/test_doctrine_integrity.py` lines 947-964), so no
   declaring-site constraint applies here unlike revision 1's `esg.md`
   work.
5. Pin the Safety-verified criteria 1-4 work with a pre-registered hash:
   `git diff -- dcs/templates/REGISTER.md dcs/workflows/esg.md |
   sha256sum` = `b2450322f3a1bb848c474bab1285ea772cf1a65cc0e2608a935f31ffb5e81f8a`
   (full paths, run from the worktree root -- IC-verified this reproduces;
   a bare-name pathspec hashes an empty diff and must not be used). This
   is the real enforcement since `CHANGELOG.md` matches neither
   `guarded_paths` nor `unguarded_paths` in `.dcs/config.json`, so
   `dcs_gate.py` does not mechanically defend this tasking's forbidden
   zones.

## File-territory partition

| Specialist | Territory | Forbidden |
|---|---|---|
| S3 | `CHANGELOG.md` | `dcs/templates/**`, `dcs/workflows/**`, `dcs/references/**`, `dcs/hooks/**`, `dcs/VERSION`, `tests/**`, `agents/**`, `skills/**`, `package.json`, `bin/**`, `install.*`, `.dcs/**`, `vault/**`, `docs/**`, `README.md`, `CLAUDE.md` |

**Partition status:** trivially disjoint (single tasking). Delegation v4:
1 file <= max_files 4, 1 specialist <= max_specialists 2, no forbidden
glob hit, verification plan names a concrete test run
(`require_tests_green` satisfied) -- **but the topic screen DOES trip**:
202 revision 2 contains the forbidden_topics string "version bump" verbatim
(criterion 6's "No version bump..." and the out-of-scope line), same as
revision 1. `auto_approve_type3` therefore does NOT cover this IAP;
approval routes to the Owner via `AskUserQuestion` exactly as revision 1's
did -- do not stamp on delegation authority.

## Risks

1. A verbatim copy of the bullet ships a false statement if the `MERGED
   (deploy pending)` sentence isn't corrected -- mitigated: required step,
   not left to judgment.
2. `git checkout HEAD -- CHANGELOG.md` is destructive of ALL working-tree
   changes to that file -- safe because the diff is confirmed single-hunk,
   zero-deletions at plan time (IC-verified); the tasking orders
   save-then-confirm-then-revert.
3. Collateral risk to criteria-1-4 work sharing this worktree -- mitigated
   by forbidden zones plus the pinned sha256 (the real enforcement, since
   the gate exempts `CHANGELOG.md` entirely). Criterion 5 lives in this
   file, not in that worktree content, and is not protected by this pin --
   see "Criterion 5, answered" above and Deviation history below.
4. Line-ending risk (v0.6.8 was a line-ending-policy release) -- caught by
   the `git diff HEAD` and BOM/CRLF evidence requirements.
5. `## Unreleased` ships as an undocumented convention (zero prior
   `unreleased` hits tracked outside `.dcs/`; `CHANGELOG.md` is in
   `package.json`'s `files` whitelist). **Accepted gap this revision** --
   not an expansion of this Owner-mandated narrow replan. Dispatcher will
   register a follow-up candidate for the next `/dcs-esg` sweep (document
   the rename-at-next-bump rule wherever the release procedure lives).
6. Network dependency: criterion 6's verification needs the npm registry
   twice (`npm view`, `npm pack`); declared fallback to `git show
   HEAD:CHANGELOG.md` comparison (with the plan-time equality hash cited)
   if the registry is unreachable at execution time.

## Verification plan

1. Premise re-measured live in the return, not cited from 202.
2. `## 0.6.10` section byte-identical to a freshly-packed tarball from
   that heading onward (empty diff, exit 0) AND `git diff HEAD` shows zero
   deletions / no change at-or-below that heading.
3. Territory discipline: `git diff --stat` shows the same three files at
   the same line counts as at plan time (`REGISTER.md` 38+/1-, `esg.md`
   9+/0-, unchanged); the pinned-hash command reproduces
   `b2450322f3a1bb848c474bab1285ea772cf1a65cc0e2608a935f31ffb5e81f8a`
   exactly; `dcs/VERSION` and `package.json` appear in no diff.
4. `python tests/test_doctrine_integrity.py` green at its own reported
   N/N (>= 82); any count written inside the CHANGELOG bullet matches that
   output.
5. Manual: the new `## Unreleased` section reads as a peer of the dated
   sections -- `---` separators both sides, no date on the heading, no
   "Shipped by incident" line claiming a ship that hasn't happened, and
   the `MERGED (deploy pending)` sentence no longer pointing "above" at
   something now below it.

Criteria 1-4 are **not** re-verified again by this repair; item 3 above is
what protects that prior `pass`-on-those-criteria verdict. Criterion 5 IS
being re-verified this repair (its answer above, restored) -- the scoped
Safety re-check should confirm the restored text is present, coherent, and
that criteria 1-4/6 remain untouched (the preservation map in `214-LOG.md`
covers the latter).

## Deviation history (this period)

**Revision 1 → 2:** Safety halt on criterion 6 (stale "unpublished"
premise), disposed by dcs-commander as `replan, narrow` (command point 4,
2026-07-27T18:50:05+11:00). Escalation trigger (e) fired alongside (IC
requested ESG activation for two queued strategy items this halt evidences);
Owner chose `continue` (2026-07-27T18:55:28+11:00) -- see
`.dcs/esg/SITREPS/register-field-repair-path-p1.md` for the full 209.
Criteria 1-5 carried forward unchanged; only criterion 6 and its tasking
were rewritten.

**Revision 2, repair (halt 2):** the revision-1→2 rewrite above silently
dropped the "Criterion 5, answered" section while rewriting this file for
criterion 6 -- found by the Safety Officer's period-end re-check
(2026-07-27T20:43:51+11:00), the incident's second `SAFETY-HALT:` sentinel
for the same 202 goal (trigger (b), mandatory). dcs-commander's convergence
read: **different class** from halt 1 (that was an unmeasured external
fact; this is content lost during a doc rewrite) -- converging, disposed as
`fix_taskings`: an IC-authored `.dcs/**`-only restoration, no Planning
Chief re-spawn, no ops-specialist tasking. Escalation trigger (b) filed its
own 209 (`.dcs/esg/SITREPS/register-field-repair-path-p1-halt2.md`); Owner
chose `continue` (2026-07-27T21:11:03+11:00). This edit restores the
section verbatim and corrects the pinned-hash claim's scope (criteria 1-4
only, never 5) -- see the preservation map in `214-LOG.md` confirming
nothing else was lost in the process.
