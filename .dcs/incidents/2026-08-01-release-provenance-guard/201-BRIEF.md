<!--
201-BRIEF.md for a QUEUED incident. Written at the /dcs-new stem on
2026-08-01, which typed the incident and got Owner confirmation but
REFUSED to open a worktree on a territory conflict (new.md 7b). It lives
here, not in .dcs/incidents/, because no incident directory exists yet.

Move this file to <worktree>/.dcs/incidents/<date>-release-provenance-guard/201-BRIEF.md
when the incident actually opens, and initialize 214-LOG.md with the
command-point-1 entry recorded under "Type + rationale" below —
/dcs-plan's pre-stamp checklist refuses to stamp an approval without it.

NOTE: .dcs/esg/ is gitignored by design, so this file is NOT under version
control. It is the only copy of two analysts' work.
-->

# 201 — Incident Brief

**Incident:** release-provenance-guard
**Opened:** not yet — QUEUED at the stem, 2026-08-01 (repo commits are +11:00)
**Type:** 3 (confirmed)

## Symptom

Nothing mechanically verifies that a published npm version has complete,
truthful provenance: that a git tag exists for it, that the tag points at
the commit actually published, and that `CHANGELOG.md` describes it. Three
releases have now shipped with defective provenance and nothing complained
— `npm test` was green for all three, because the only version-aware check
in the suite compares `dcs/VERSION` to `package.json` as strings and cannot
see which commit was shipped.

**The intake's framing was wrong and is corrected here.** It asked for a
guard that fails when "a published tarball and the tag that describes it
disagree". Neither measured instance is that defect, and a byte-comparison
guard passes both:

- **0.7.1** — the tarball matches commit `aa9b00b` exactly. There was no
  tag to disagree with: the `v0.7.1` tag and its GitHub release were both
  created retroactively on 2026-08-01, a day after the 2026-07-30 publish.
  The defect is *absent* provenance, not mismatched provenance.
- **0.7.2** — the tarball is byte-identical to its tag `v0.7.2` (3d559ce),
  75 of 75 files. The publish was faithful to the tip of `main` **at that
  moment**: `3d559ce` was committed 00:42:24Z, published 00:45:48Z, and the
  corrective commit `33c2dd4` did not exist until 00:51:51Z — six minutes
  *after* the publish. What shipped wrong was the content of the tip's own
  `CHANGELOG.md`, which claimed a defect was unfixed that the same release
  had in fact fixed. No tag/tarball comparison can detect this.

That correction matters for the fix: the "publish-from-the-pushed-tip" rule
added to `docs/publishing.md` at `91aec02` **would not have prevented
0.7.2**, because the tip is exactly what was published. That commit's
narrative is wrong on this point and is in scope to correct.

## Evidence

- 0.7.2 tarball vs its tag: `npm pack dcs-command-system@0.7.2` extracted
  and compared per-file sha256 against `git show 3d559ce:<path>` — 75
  compared (76 minus `package.json`), **0 differing**. Against `33c2dd4`:
  1 differing, `CHANGELOG.md`. (analyst 1, re-derived independently)
- `npm view dcs-command-system@0.7.2 gitHead` = `3d559ce…`, and
  `@0.7.1 gitHead` = `aa9b00b…`. **The registry already records the
  published commit**, so provenance is verifiable with one cheap metadata
  call and no tarball download. (analyst 1)
- Publish/commit timeline, refuting the "stale tag" narrative: `3d559ce`
  authored 2026-08-01T11:42:24+11:00 (=00:42:24Z); npm publish
  00:45:48.541Z; `33c2dd4` authored 11:51:51+11:00 (=00:51:51Z). Verified
  directly by the IC, not only by analyst report. (analyst 1 + IC)
- 0.7.1 provenance was absent at publish: `gh release list` shows the
  `v0.7.1` release created 2026-08-01T00:52:40Z and `v0.7.2` at
  00:52:53Z — 13 seconds apart, both a day after 0.7.1's
  2026-07-30T21:49:38Z publish. (analyst 1)
- Nothing in the suite could catch it: `package.json` `scripts.test` is
  three network-free Python scripts; a grep of `tests/` for
  `urllib|requests|socket` and for git/npm subprocess calls returns
  nothing. The sole version check is `tests/test_doctrine_integrity.py`
  version-sync (`dcs/VERSION` == `package.json`), green in all three
  failures. (analyst 1)
- **Prior instance, third of three:** v0.4.2 → v0.4.3 has the same shape —
  "0.4.2 was published from a tree that predated the audit-trail/compliance
  README section", resolved only by shipping a follow-up patch, because npm
  forbids republishing. (analyst 1)
- Existing machinery does not cover the failing file:
  `tests/payload_check.py` walks exactly three roots — `dcs/`,
  `agents/dcs-*.md`, `skills/dcs-*/` — so it never sees `CHANGELOG.md`.
  Pointing it unmodified at an extracted tarball would still have missed
  0.7.2. Its interface is `--repo PATH --installed PATH`, exit 0/1/2/3.
  (analyst 2)
- Structural prior art for the fix's shape: `dcs/workflows/deploy.md`
  step 7 plus `test_doctrine_integrity.py` check 15 already distinguish a
  cheap "commit-ish marker" (insufficient alone) from an independent
  "content witness" (byte diff) — the same distinction, one checkpoint
  earlier. (analyst 2)
- **A second false statement in the same runbook:** `docs/publishing.md`
  step 7 states `package.json` is excluded "because npm normalizes it
  during packing, so it never matches byte-for-byte". Measured: the
  published 0.7.2 `package.json` and `git show 3d559ce:package.json` have
  identical sha256 (`1e9d3b45…`). npm 11.8.0 did not normalize it.
  (analyst 1, re-verified by the IC)
- No prior art proposes this guard: `vault/Decisions/` (all 8 files),
  `vault/Backlog.md` items 1–22, and every `REGISTER.md` row were searched;
  items 9/12/13 are adjacent but concern the local install marker, not a
  published tarball. (analyst 2)

## Reproduction path

The two publish-time defects are not re-triggerable — npm forbids
republishing a version — so what reproduces is the **detection gap**, not a
live failure. Run `npm test`: green (123/123 in the integrity suite alone)
while `npm view dcs-command-system@0.7.1 gitHead` resolves to a commit that
carried no tag and no changelog entry at publish time. Full forensic path:
`npm pack dcs-command-system@<ver>` → extract → per-file sha256 vs
`git show <tag>:<path>`; cross-check with `npm view <pkg>@<ver> gitHead`;
compare `gh release list` and `npm view <pkg> time --json` timestamps to
establish whether a tag existed at publish time.

## Blast radius (best guess at intake)

Narrowed by the Owner's command-point-1 answers (blocking prepublish gate,
`npm test` stays offline), which point at a standalone script rather than a
new case inside the integrity suite:

- `tests/release_provenance_check.py` (new) — offline invariants: a tag
  exists for `dcs/VERSION`, it resolves to `HEAD`, and `CHANGELOG.md` has
  an entry for this version. Follows `payload_check.py`'s convention of a
  non-`test_`-prefixed script outside `npm test`.
- `package.json` — `scripts.prepublishOnly` wiring
- `docs/publishing.md` — two verified corrections owed regardless
- `tests/test_doctrine_integrity.py` — **only if the Planning Chief finds
  it necessary; this is the conflicted file, see below**

**Out of territory:** widening `tests/payload_check.py`'s walked root set
belongs to `shipped-set-defined-three-times` — the commander ruled that
widening *is* that defect's fix. Treat as a sequencing dependency, never
absorb it here (the seam rule, `vault/Meta/building-dcs-lessons.md` §15).

## Prior art

Three instances of the same class, none previously registered: v0.4.2→v0.4.3
(README section missing from the published tree), 0.7.1 (no tag, no release,
no changelog entry), 0.7.2 (tip published faithfully, tip's changelog false).
No `vault/Decisions/` file, `vault/Backlog.md` item, or register row proposes
release-provenance verification. `dcs/workflows/deploy.md` step 7 and
integrity check 15 are the structural precedent for the marker-vs-witness
shape. `tests/payload_check.py`'s docstring cites `deploy-marker-blind` for
the same "a correct ship can leave the marker unchanged" problem in the
local-install channel.

## Type + rationale

**Proposed type:** 3
**Rationale (IC = `dcs-commander`, fable, command point 1, 2026-08-01):**
Root cause fully measured (registry `gitHead` + verified timeline) and the
footprint bounded at 2–4 known files — a new provenance check plus two
verified `docs/publishing.md` corrections — with no Type-1 trigger firing
(no `dcs/hooks/**`, no schema, no workflow-gate change, trivially
reversible), matching this register's standing Type-3 precedent for
`test_doctrine_integrity.py` guards; the open prevent-vs-detect and
network-call questions are Owner policy to answer at typing/IAP, not
structural risk.

**214-LOG entry owed when this opens** (verbatim):
`command: typed 3 -- root cause measured, footprint 2-4 files, no Type-1 trigger fires (IC=dcs-commander)`

**Owner confirmation:** confirmed as proposed, 2026-08-01, plus two policy
answers to the commander's `open_questions`:
1. **Enforcement = blocking prepublish gate.** The guard may mechanically
   fail `npm publish` when provenance is absent (no tag for `dcs/VERSION`,
   tag not pointing at `HEAD`, or no `CHANGELOG.md` entry). All three are
   local and need no network. This is the only option that would have
   *prevented* the 0.7.1 class.
2. **`npm test` stays network-free.** Only offline invariants run in the
   default suite. Any networked verification (`npm view … gitHead`, or the
   full `npm pack` + sha256 witness) lives in a separate script the runbook
   invokes after publishing — following the precedent that
   `payload_check.py` is deliberately excluded from `npm test`.

## Stem disposition — QUEUED, not opened

**Refused at step 7b on a territory conflict**, Owner-confirmed 2026-08-01:
`revision-preservation-map` is ACTIVE with a live worktree at
`C:\DCS-wt\revision-preservation-map` and holds `tests/test_doctrine_integrity.py`,
which this stem's blast radius named. No worktree, branch, or `.dcs/ACTIVE`
was created.

The Owner was offered opening early with territory narrowed to exclude that
file (the standalone-script shape their own answers imply) and **declined in
favour of waiting** for the conflict to clear. Re-run `/dcs-new` — or open
directly from this brief — once `revision-preservation-map` closes, is
parked, or is killed.

**Field repair since, 2026-08-01:** the two false statements in
`docs/publishing.md` (`91aec02`) were corrected at `e25dc75` on Owner
direction, outside this incident. `docs/publishing.md` is therefore dropped
from this incident's territory, and the "two corrections owed" line under
Blast radius is discharged. What that repair deliberately did **not** do,
and this incident still owns: tagging happens at step 8, *after* publishing,
so a "does a tag exist for this version" check can only detect after the
fact. Making it the preventer the Owner asked for means reordering the
runbook's steps — which would bring `docs/publishing.md` back into
territory.

## Intake source (for /dcs-close to route back to)

Owner chat, 2026-08-01 ("open an incident for the tarball-tag guard"),
following the 0.7.1/0.7.2 release session. Intake premise corrected at the
stem and the slug renamed from `tarball-tag-guard` — see Symptom.
