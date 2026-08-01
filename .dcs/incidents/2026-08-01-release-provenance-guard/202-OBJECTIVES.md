# 202 — Objectives (Operational Period 1)

**Incident:** release-provenance-guard
**Period:** 1

## Goal

A version cannot be published to npm unless the commit being published
already carries a matching git tag and a truthful `CHANGELOG.md` entry for
that version — checked automatically at publish time, never left to
operator discipline. This is the enforcement shape the Owner chose at
command point 1: a **blocking prepublish gate**, with `npm test` staying
network-free.

One structural consequence the Planning Chief must design against, not
discover mid-tactics: tagging currently happens at `docs/publishing.md`
step 8, *after* `npm publish` at step 6. A prepublish gate that requires a
tag can never pass on a version's first publish attempt under that order —
tagging must move ahead of publishing for the gate to be usable at all.

## Acceptance criteria (the Definition of Done)

1. A new standalone script — not `test_`-prefixed, not added to `npm
   test`'s script list, following `tests/payload_check.py`'s existing
   convention for machine/environment-dependent checks — checks, for
   `V` = `package.json`'s version (what npm actually ships): a
   **precondition** that `dcs/VERSION` equals `V` (unequal, or either
   unreadable, exits a *distinct* non-zero code — `2` — mirroring
   `payload_check.py`'s exit-2 "cannot check" class, never conflated with
   a real provenance failure; mechanizes `docs/publishing.md`'s existing
   "Version-sync rule (HARD)" at publish time, which merge-time checks
   alone cannot enforce since this incident exists because publish flows
   bypass them). Past that precondition: exits `1` when no git tag `vV`
   exists, OR that tag's commit (`git rev-parse vV^{commit}`) is not
   `HEAD`, OR `CHANGELOG.md` has no entry for `V`. Exits `0` when the
   precondition and all three checks hold. **`CHANGELOG.md`'s real
   heading convention is `## <version> — <date>` with a literal U+2014 em
   dash** (verified: `CHANGELOG.md:28` is `## 0.7.2 — 2026-08-01`) — not
   ASCII `--`; the check must be anchored against this exact convention
   (and against `0.7.1` matching `0.7.10`), and the file read with
   `encoding="utf-8"` explicitly, or the em dash mis-decodes. Verifiable:
   run it against six constructed git fixtures — the four failure modes
   individually (no-tag, tag-not-HEAD, no-changelog-entry → `1`;
   version-mismatch → `2`, shown distinct from the `1`s) plus two
   all-clear fixtures (lightweight and annotated tag) whose
   `CHANGELOG.md` is a byte-verbatim copy of the real one (sha256-matched
   — never authored by hand, so fixture-vs-reality drift cannot pass
   green) — each must produce the stated exit code.
2. `package.json`'s `scripts.prepublishOnly` invokes that script, so a
   `npm publish` attempt fails before any registry contact when provenance
   is incomplete. Verifiable, no real publish needed: confirmed this
   period that `prepublishOnly` fires on `npm publish --dry-run` (fails
   before network activity) and does **not** fire on `npm pack` or
   `npm pack --dry-run` — reproduce this same probe against a fixture with
   deliberately incomplete provenance and confirm `npm publish --dry-run`
   exits non-zero citing the new script's message.
3. `npm test`'s script list and file count are unchanged from this
   period's starting point — diff `package.json`'s `scripts.test` before
   and after; the new check must not appear in it.
4. `docs/publishing.md`'s numbered release steps are reordered so tag
   creation precedes `npm publish`, and every cross-reference to a step by
   number inside that file still points at the right step after the
   reorder (`grep -n "^[0-9]\+\." docs/publishing.md` read against the
   file's own internal "step N" citations). This criterion exists because
   of the structural consequence named under Goal — without it, criterion
   1's gate can never pass on a fresh version and every release blocks.
5. `npm test` still passes in full, and no existing test's assertions
   about `package.json`'s script count or shape break as a side effect of
   this period's edits.

## Out of scope this period

- Widening `tests/payload_check.py`'s walked root set (owns `CHANGELOG.md`
  and other root-level shipped files) — that is `shipped-set-defined-
  three-times`'s fix, not this incident's; treat it as a dependency to
  sequence around, never absorb.
- Any edit to `tests/test_doctrine_integrity.py` — out of this incident's
  confirmed territory (register row `release-provenance-guard`). If the
  Planning Chief finds the goal genuinely requires touching it, that is a
  territory-expansion request to flag back to the Owner, not something to
  fold in silently.
- A registry-content witness (downloading the published tarball and
  diffing it byte-for-byte, as `docs/publishing.md` step 7 already does by
  hand) — that is detection-only and explicitly the piece the Owner chose
  to keep outside `npm test`; this period's gate is the offline,
  local-git prevention half only.
- Deciding whether `npm view <pkg>@<ver> gitHead` (confirmed this session
  to already record the published commit) becomes part of any future
  post-publish tooling — a real option, not this period's problem.

## Chief feedback

Two passes at command point 2. Pass one rejected the Chief's original
return: criterion 1 keyed every check to `dcs/VERSION` alone, missing that
npm actually ships `package.json`'s version — a real gap given this
incident's own premise (publish flows bypass merge-time suites); and the
Chief's planned CHANGELOG heading regex used ASCII `--`, which does not
match the file's real `em dash` convention and would have let every
fixture pass green while the shipped gate silently misread every real
release. Both were independently verified by the IC and by
`dcs-commander` directly against the repo before being acted on, not taken
on either party's word.

Pass two (Chief's own words, accepted): "Criterion 1 must be read as
AMENDED per required change 1: `dcs/VERSION != package.json` version — or
either being unreadable — is a precondition failure with its own distinct
non-zero 'cannot check' exit code, mirroring `tests/payload_check.py`'s
exit-2 class... Mechanizes `docs/publishing.md:40-47`'s existing HARD
version-sync rule at publish time... Re-verified this revision: the
worktree has `dcs/VERSION` = `package.json` version = `0.7.2`, so the
amendment does not change the live red case's expected exit (still `1` via
tag-not-HEAD, not `2`). Conceded as settled fact: the CHANGELOG heading
convention I planned against was wrong — the real file uses an em dash
(U+2014), verified at `CHANGELOG.md:28`... Unchanged from prior return:
criterion 2's probe... all criteria remain verifiable; no criterion
asserts state outside the working tree; criterion 5 remains satisfiable
without touching `tests/test_doctrine_integrity.py`."

Criterion 1's text above already reflects this amendment — the IC edited
it into this file before `IAP.md` was written, per `dcs-commander`'s
explicit instruction at acceptance (the amendment previously existed only
in the Chief's return, never on disk, which would have let the Safety
Officer refute the accepted plan against stale criteria).
