# AAR — After Action Report

**Incident:** release-provenance-guard
**Type:** 3
**Opened:** 2026-08-01
**Closed:** 2026-08-01
**Operational periods:** 1

## Outcome

All 5 acceptance criteria from `202-OBJECTIVES.md` (period 1, the only
period) were met, verified independently by `dcs-safety-officer` (not
taken on either specialist's word) and cross-checked a second time by
`dcs-commander` at the final verdict-disposition command point:

1. `tests/release_provenance_check.py` checks the `dcs/VERSION` ==
   `package.json` version precondition (distinct exit `2`), then tag-at-
   HEAD and a real-em-dash `CHANGELOG.md` entry (exit `1` on failure,
   `0` on all-clear) — verified against a 10-fixture matrix (the Safety
   Officer's own, built from scratch), all 10 at their required exit
   codes.
2. `package.json`'s `scripts.prepublishOnly` invokes the script;
   confirmed to fire on `npm publish --dry-run` before registry contact
   (proven against a dead registry, not merely asserted) and to leave
   `npm pack`/`npm pack --dry-run` unaffected (measured, npm 11.8.0).
3. `npm test`'s script list and file count are unchanged — `git diff
   package.json` shows exactly one addition, `scripts.test` byte-
   identical.
4. `docs/publishing.md`'s steps are reordered so tagging (step 6)
   precedes publish (step 7); every internal "step N" citation re-
   resolves correctly after the renumbering.
5. `npm test` passes in full: 100/100, 18/18, 133/133.

Fixes the class behind three unrepairable past releases (v0.4.2, 0.7.1,
0.7.2) that shipped with incomplete or false provenance while `npm test`
stayed green throughout.

## What worked

- **The territory partition held exactly as declared** — S1 and S2 never
  touched each other's files, and the Safety Officer's own `git status`/
  `git diff --name-only` audit (both passes) found nothing outside
  `tests/release_provenance_check.py`, `package.json`,
  `docs/publishing.md`.
- **The precondition-vs-failure exit-code split** (`2` = cannot check,
  `1` = real provenance failure), mirroring `tests/payload_check.py`'s
  existing convention, survived both Safety passes without challenge once
  command point 2's second `iap_review` pass fixed it into criterion 1.
- **The Safety Officer never accepted a fix as closing its own class on
  the specialist's report alone** — it re-built the halt fixture against
  the fix, then went further and independently probed a related form
  (the qualified-string-as-branch-name case) nobody had asked it to
  check, which is exactly what surfaced advisory 1 (see Lessons).
- **`dcs-commander` independently reproduced load-bearing claims before
  ruling, both times** — at command point 2 (rebuilding the CHANGELOG
  em-dash and `dcs/VERSION`-vs-`package.json` gap claims before accepting
  the Chief's revision) and at command point 4, twice (rebuilding the
  advisory-1 fixture itself before ruling on its disposition).

## Lessons

- Qualifying a git ref lookup to a namespace prefix (`refs/tags/<tag>`)
  fed into `git rev-parse --verify` is **not** disambiguation-free — the
  qualified string still runs through git's full resolution table
  (`refs/heads/<qualified-string>` still matches). The disambiguation-
  free form is `git show-ref --verify <exact-full-refname>`. Full account
  and a worked reproduction: `vault/Meta/building-dcs-lessons.md` #28.
- An advisory whose fix would rewrite the load-bearing line of a
  security-relevant check the current Safety pass just verified should
  not fold into the same period's 9b integration commit by
  `execute.md`'s ordinary default — it ships unverified under a verdict
  that never saw it. `dcs-commander` caught this by reasoning past the
  written default rather than applying it literally; the default itself
  has no carve-out yet. Candidate workflow-text fix (not built here, to
  avoid editing a hot-path file as a side effect of this close):
  `vault/Backlog.md` #29.
- A specialist that notices its own tasking's count doesn't add up
  ("nine" vs. an enumerated ten) and says so, rather than silently
  picking one, is the tasking-compliance behavior the whole verification
  chain depends on — `204-TASKING/S1-FIX1.md`'s self-flagged discrepancy
  became the Safety Officer's advisory 3 instead of a silent paper error.

## Deviations this incident

Two, both resolved within period 1 — no return to planning was needed:

1. **Command point 2 (`iap_review`), one REJECT before ACCEPT.** The
   Planning Chief's first tactics keyed criterion 1 to `dcs/VERSION`
   alone (missing that npm ships `package.json`'s version) and used an
   ASCII `--` in the CHANGELOG regex against the file's real U+2014 em
   dash convention. Both independently re-verified by the IC and by
   `dcs-commander` before the reject was issued; the Chief's revision
   addressed both, re-verified again, accepted. `214-LOG.md`
   `[2026-08-01T15:33:15+11:00]` / `[2026-08-01T15:47:53+11:00]`.
2. **Command point 4 (`verdict_disposition`), one SAFETY-HALT before
   PASS.** `check_tag_at_head`'s original unqualified refname let a
   branch masquerade as a tag with zero real tags present. Routed through
   a fix-tasking (`204-TASKING/S1-FIX1.md`), not a return to planning —
   the commander judged the plan's own logic sound and the fix confined
   to one call site plus fixtures, no 202/IAP.md content change.
   Re-verification passed. `214-LOG.md`
   `[2026-08-01T16:46:47+11:00]` through `[2026-08-01T17:40:20+11:00]`.

## Memory routing

Written to this incident's worktree copies (per `close.md` step 3/4 —
committed here, riding the merge into main, never written to the main
checkout directly):

- `vault/Backlog.md` #29 — candidate `execute.md` text change for the
  advisory-folding carve-out.
- `vault/Meta/building-dcs-lessons.md` #28 — the ref-disambiguation
  lesson and the advisory-routing override, in full narrative form.

(Self-correction recorded in `214-LOG.md`
`[2026-08-01T17:55:52+11:00]`: both entries were first written to the
main checkout by reflex, caught before any commit, and reverted there
before being re-applied here.)

No `dcs/references/doctrine.md` or `dcs/workflows/execute.md` edit was
made — both candidate hardenings are recorded as proposals for a future,
deliberate change, not applied as a side effect of this close.

## Intake source closure

Ad hoc — Owner chat, 2026-08-01 ("open an incident for the tarball-tag
guard"). No external tracker row or ticket to close.

## Safety Officer's final verdict (verbatim, from SAFETY.md)

```json
{
  "verdict": "pass",
  "refutations": [],
  "advisories": [
    {
      "finding": "RESIDUAL ref-namespace hole, same class as the halted one but not reachable by accident — reported here, not as a refutation, and NOT a paperwork item. `check_tag_at_head` (tests/release_provenance_check.py:159-160) qualifies to `refs/tags/` but `git rev-parse` still applies its full disambiguation table to that qualified string, including rule 4 (`refs/heads/<refname>`). I built the fixture: zero tags, plus `git branch \"refs/tags/v0.7.2\"` — plain porcelain, exit 0, ref lands at `refs/heads/refs/tags/v0.7.2`. Measured: `git tag --list` empty, and `python tests/release_provenance_check.py --repo <fx>` printed `PROVENANCE OK: v0.7.2 is HEAD, …` with EXIT=0. Not a halt because it is unreachable by the failure mode this gate exists to stop: no convention, refspec, fetch, or typo produces a branch literally named `refs/tags/v0.7.2`, and any actor who can create that ref can trivially run `git tag v0.7.2` instead — so it grants no capability and cannot be arrived at by forgetting to tag. The plausible forms are all closed and I proved each: branch named `v0.7.2` -> EXIT=1; `refs/remotes/origin/v0.7.2` with zero tags -> EXIT=1.",
      "fix": "Replace the rev-parse tag lookup with a lookup that does no disambiguation at all: `git show-ref --verify refs/tags/<tag>` (exact full refname only), then peel with `git rev-parse <sha>^{commit}`. Because this edits the load-bearing line of a security guard, it should NOT be hand-folded into the 9b integration commit like a docstring advisory — route it as a follow-up tasking so it gets independent re-verification."
    },
    {
      "finding": "docs/publishing.md:80-81 — `\"npm pack` and `npm pack --dry-run` are unaffected — they never run `prepublishOnly`\"` is an unqualified derived fact about npm behaviour with no version named and no regenerating command, in a file that already qualifies its other measured claim (line 169: `\"identical sha256 under npm 11.8.0\"`). This is the prior verdict's advisory 4, deliberately excluded from S1-FIX1 and still open. I re-measured it rather than carrying it forward on paper: in a fixture with zero tags, `npm pack --dry-run` EXIT=0 and plain `npm pack` EXIT=0 (prepublishOnly never fired, or they would have gone red), under npm 11.8.0. The claim is true; only its qualifier is missing.",
      "fix": "Qualify with the measured version — e.g. `\"…are unaffected — they never run `prepublishOnly` (measured, npm 11.8.0)\"` — matching the file's own existing convention at line 169."
    },
    {
      "finding": "204-TASKING/S1-FIX1.md:111-114 carries a self-contradicting durable count: it orders `\"all **nine** fixtures now\"` and `\"the three new ones\"`, then enumerates four new ones and corrects itself mid-sentence (`\"that is four new fixtures, not three\"`). Six original + four new = ten, not nine. I measured the enumeration by building it: ten fixtures, all ten at their stated exit codes (lightweight-clean 0, annotated-clean 0, no-tag 1, tag-not-HEAD 1, no-changelog-entry 1, version-mismatch 2, branch-not-tag 1, dateless-heading 1, undecodable-dcs-VERSION 2, undecodable-CHANGELOG 1).",
      "fix": "Record ten in the AAR/close note, with the regenerating harness path, so the incident's own paper does not preserve a count that never added up."
    },
    {
      "finding": "The fixed line-number citation the fix-tasking removed from the script survives in this period's planning artifacts: 202-OBJECTIVES.md:38 and :114, and IAP.md:31 and :61, all cite `CHANGELOG.md:28`. Same rot class, same file, same next-release trigger. I re-measured: `grep -n \"^## \" CHANGELOG.md | head -1` returns `28:## 0.7.2 — 2026-08-01`, so all four are true today. The script itself is clean — `grep -n \"CHANGELOG.md:[0-9]\" tests/release_provenance_check.py` returns nothing, and both replacements carry the regenerating command (lines 53 and 88).",
      "fix": "Note the regenerating command at close/AAR rather than editing the frozen artifacts. Do NOT amend 202-OBJECTIVES.md mid-period to fix a citation — a 202 edit is a re-stamp trigger, and that cost is not worth a line number that is currently correct."
    }
  ],
  "checked": [
    "Read tests/release_provenance_check.py in full (257 lines) at C:\\DCS-wt\\release-provenance-guard\\tests\\release_provenance_check.py — confirmed line 159-160 is `_git_rev_parse(repo_root, \"--verify\", \"refs/tags/\" + tag + \"^{commit}\")`, line 163 `\"--verify\", \"HEAD\"`, line 196 uses `[ \\t]+` on both sides of EM_DASH (not `\\s+`), lines 126 and 193 both `except (OSError, ValueError)`.",
    "Read 202-OBJECTIVES.md, IAP.md, 204-TASKING/S1-FIX1.md and 214-LOG.md in the incident directory; took no claim in them as established.",
    "Built my own 10-fixture matrix from scratch (own harness, own isolated scratch git repos, no specialist fixture reused): all 10 hit their required exit codes — lightweight-clean 0, annotated-clean 0, no-tag 1, tag-not-HEAD 1, no-changelog-entry 1, version-mismatch 2, branch-not-tag 1, dateless-heading 1, undecodable-dcs-VERSION 2, undecodable-CHANGELOG 1. Zero mismatches.",
    "Reproduced the EXACT halt fixture myself against the fixed file: zero tags + `git branch v0.7.2` at HEAD. Measured `git tag --list` empty, unqualified `git rev-parse v0.7.2^{commit}` still resolves to the branch commit, `git rev-parse --verify refs/tags/v0.7.2^{commit}` rc=128 — and the script now prints `PROVENANCE INCOMPLETE … - no git tag v0.7.2 exists`, EXIT=1. The prior refutation is closed.",
    "sha256-verified both clean fixtures' CHANGELOG.md byte-identical to the worktree's real CHANGELOG.md (copied via shutil.copyfile, never hand-authored) — the anti-drift rule holds, so the green fixtures cannot be green against a fake convention.",
    "Caught that a UTF-16LE dcs/VERSION is *valid* UTF-8 (NUL-interleaved ASCII) and therefore never exercises the ValueError catch, so I built a genuinely undecodable one (`utf-16` with BOM, leading 0xFF): EXIT=2 with `\"cannot check -- dcs/VERSION is missing or unreadable\"`, no traceback. Same for an undecodable package.json: EXIT=2.",
    "Ran 11 further adversarial fixtures I devised myself, all fail-closed, none traceback: prefix collision (V=0.7.1 vs a 0.7.10-only changelog) 1; remote-tracking ref `refs/remotes/origin/v0.7.2` with zero tags 1; ASCII `--` heading 1; two simultaneous failures (both listed) 1; CHANGELOG.md absent 1; blank dcs/VERSION 2; not-a-git-repo-at-all 1; CRLF changelog 0; tag pointing at a tree 1; packed-refs-only tag 0; detached HEAD at the tag 0.",
    "Probed the pathological case `git branch \"refs/tags/v0.7.2\"` and confirmed porcelain accepts it (exit 0) and the gate then returns EXIT=0 with zero tags — see advisory 1.",
    "Criterion-2 probe in my own fresh npm fixture: with zero tags, `npm publish --dry-run` EXIT=1 citing the script's own message; `npm pack --dry-run` EXIT=0 and plain `npm pack` EXIT=0 (prepublishOnly never fires).",
    "Proved the failure precedes registry contact, not merely asserted it: re-ran `npm publish --dry-run --registry http://127.0.0.1:1/` (nothing listening) — it failed with the provenance message, not a network error.",
    "Tested the passing direction too: tagged the fixture at HEAD, script EXIT=0, and `npm publish --dry-run` then proceeded past the gate. No real publish was ever attempted.",
    "Ran `npm test` in the worktree myself: 100/100, 18/18, 133/133, exit 0.",
    "Live no-args run in the worktree: EXIT=1, `tag v0.7.2 points at 3d559ced9e9ef0ec5c56ae32281cb05079ae9f63, which is not HEAD (998bcd443aab8395b222d6097639df58b87eaa17)` — the designed red case, unchanged by the fix.",
    "Criterion 3: `package.json` scripts keys are exactly `['postinstall','test','prepublishOnly']`; `scripts.test` byte-identical to before (`git diff package.json` shows one added line only); `grep -rn \"scripts\" tests/*.py` finds no assertion pinning script shape anywhere in the suite; package.json is 1440 bytes against the `< 8 kB` assertion at test_doctrine_integrity.py:414-416.",
    "IAP item 6 (three-way interface): `package.json.scripts.prepublishOnly` == `\"python tests/release_provenance_check.py\"`; that exact string and the exact path both appear in docs/publishing.md; the shipped file exists at that path; the only `tests/` paths named in the docs are `payload_check.py` and `release_provenance_check.py` — no third, no variant spelling.",
    "Criterion 4: `grep -nE \"^[0-9]+\\.\" docs/publishing.md` gives steps 1-9 with 6=Tag-and-push and 7=Publish (tagging now precedes publish); the only surviving by-number citations are line 47 `\"step 2\"` -> `dcs bump` and line 73 `\"step 5\"` -> the tip gate, both correct, plus line 146 `\"the next step\"` -> step 7, correct. The lint baseline's third citation (old line 78, `\"step 8\"`) was legitimately deleted with the rewritten 0.7.1 bullet, not left dangling. Repo-wide, README.md:259 links publishing.md without citing a step number.",
    "Traced the reordered runbook end to end against the new gate to test criterion 4's stated purpose (that the gate can pass on a fresh version): step 3 uses `npm pack --dry-run` which I confirmed does not fire the gate; step 6 tags at HEAD; step 7's publish then satisfies all three checks. The runbook is executable, not self-blocking.",
    "IAP item 7 (territory): `git status --porcelain`, `git diff --name-only` and `git ls-files --others --exclude-standard` together show exactly docs/publishing.md, package.json, tests/release_provenance_check.py plus the IC's .dcs/ paperwork — no forbidden-zone file touched by either specialist.",
    "IAP item 8 (tag audit): `git tag --list | wc -l` = 33, newest v0.7.2 — measured before AND after all my fixture work, so no fixture tag leaked into the shared ref store from the specialists or from me.",
    "Byte purity of the new script, measured directly: 11163 bytes, 0 non-ASCII, 0 CRLF, no BOM. Confirmed the `chr(0x2014)` construction yields the correct runtime character empirically — clean fixtures matching the real em-dash CHANGELOG go green while an ASCII `--` heading goes red.",
    "Principle-15 sweep: re-measured `grep -n \"^## \" CHANGELOG.md | head -1` -> `28:## 0.7.2 — 2026-08-01`; confirmed zero surviving `CHANGELOG.md:<N>` citations in the script and found the four that survive in 202/IAP; re-measured the npm-pack claim under npm 11.8.0; re-counted the fixture enumeration against the tasking's `\"nine\"`.",
    "Post-work integrity: re-hashed the script (sha256 cbf7b47aa134217320e224c060934f45b3a66d59cbc5bc13d651fcd5267f7e90) and re-ran `git status --porcelain` — the worktree is exactly as I found it; I wrote nothing anywhere in it."
  ]
}
```

Advisory 3's fixture count, regenerable: `python tests/release_provenance_check.py` fixture harness builds ten fixtures total (six original + four added by `S1-FIX1`) — see `SAFETY.md`'s "checked" list, third bullet, for the full enumeration.

Advisory 4's citation, regenerable: `grep -n "^## " CHANGELOG.md | head -1` (currently `28:## 0.7.2 — 2026-08-01`, true as of this close; the citations at `202-OBJECTIVES.md:38,:114` and `IAP.md:31,:61` are frozen planning artifacts, deliberately not edited — see this file's Memory routing section).
