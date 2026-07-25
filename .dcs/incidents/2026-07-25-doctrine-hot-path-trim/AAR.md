# AAR — After Action Report

**Incident:** doctrine-hot-path-trim
**Type:** 3
**Opened:** 2026-07-25
**Closed:** 2026-07-25
**Operational periods:** 1 (one stamped IAP; three Safety verifications within it)

## Outcome

**Goal met at the approved bar.** Period 1's 202 acceptance criteria 1–9 and 11
are met; criterion 10 (Owner end-to-end read) was approved by the Owner at close;
criterion 12 is deploy-period work and remains open.

Delivered — **as measured in the incident worktree**, which is what Safety
verified (regenerate with
`python -c "import os; print(os.path.getsize('dcs/references/doctrine.md'), os.path.getsize('dcs/references/schemas.md'))"`):

| | before | after |
|---|---|---|
| `doctrine.md` | 27,167 B | **22,121 B** (−5,046) |
| hot path (`doctrine.md` + `schemas.md`) | 41,763 B | **36,717 B** (target 36,864) |
| `HOT_PATH_BUDGET_KB` ratchet | 42 | 37 |
| `doctrine-appendix.md` | 11,302 B | grew by 114 lines (`git diff --numstat` on the incident commit) |
| version | 0.6.4 | 0.6.5 |

**And as actually merged, which differs — see "Deviations" below.** The
integration branch advanced three commits while this incident was open, one of
which grew `schemas.md` by 1,189 B:

| | main before merge | after merge |
|---|---|---|
| hot path | 42,623 B | **37,734 B** (−4,889) |
| `HOT_PATH_BUDGET_KB` ratchet | 42 | **38** (re-derived on the merge result) |
| version | 0.6.6 | **0.6.7** |

`doctrine.md` at 22,121 B is the one figure identical in both tables — the trim
itself was never in question.

**No rule changed, moved, or disappeared.** All 12 `##` headings, the
`### A command point is never a silent wait` sub-heading, and all 28 numbered
labels (including `9b`) are byte-identical. Verified three times by three
independent Safety Officers.

**The 201's directional goal ("toward the post-diet size") is partially
recovered, deliberately.** Post-diet equivalence in this tree's units is
~32,031 B; delivered is 36,717 B, so roughly half the regrowth came back. The IC
ruled at close that the binding bar is criterion 1 (36,864 B) — which the Owner
explicitly declined to relax at IAP approval, and which therefore also fixes it as
the bar — and that the remaining ~4.7 kB is register material, not un-shippable
work half-done.

## What worked

- **Enumerating every cut span-by-span at plan time, with a KEEP-list per cut.**
  The Planning Chief measured each candidate span (`len(span.encode('utf-8'))`)
  rather than estimating, and the IC re-measured the seven largest itself before
  accepting — all matched to the byte. The specialist then executed a ledger
  rather than exercising fresh editorial judgment, and hit the target on the first
  attempt with no reserve draws and no deviation.
- **Pre-authorizing a reserve.** The IC's ruling (A) gave the specialist ~491 B of
  pre-approved fallback cuts and an explicit *deviate, do not cut into rule text*
  instruction. The reserve went unused, but its existence is what made "file a
  deviation" the cheap option instead of a last resort.
- **One seat for both ends of the edit.** The chief argued against splitting
  `doctrine.md` and `doctrine-appendix.md` across two specialists despite the
  files being trivially disjoint — the cut and its landing are one act, and the
  routing ledger needs one hand holding both. That judgment held: no partition
  friction, and the ledger was coherent as authored.
- **Surgical-Edit-only as a stated method.** Forbidding a wholesale `Write`
  prevented a CRLF→LF flip that would have booked a ~157 B phantom win and
  produced an unreviewable all-lines diff. `git diff --numstat` showed 18/20 lines
  on a 155-line file — reviewable by a human.
- **Adversarial verification finding what greps cannot.** All three officers ran
  the mechanical criteria; what actually mattered was the manual read
  ("a principle reduced to a slogan with its operative clause amputated will pass
  every grep above") and the ledger reconciliation. Both halts came from the
  latter.

## Lessons

- **A line citation into a file the same incident is editing rots before anyone
  reads it.** This incident's ledger cited appendix line ranges that were correct
  when written and wrong by the time the Safety Officer opened them — invalidated
  by the same 114-line append they documented. **Cite by content anchor**
  (`grep -n -F "<distinctive phrase>" <file>`), not by line range: an anchor is
  the substance rather than a fact derived about it, resolves in any tree, and
  fails loudly (zero hits) instead of silently resolving to the wrong text.
- **Content anchors have their own failure mode: markdown hard-wrapping.** An
  anchor phrase spanning a line break matches nothing under line-based `grep`.
  The first draft of one anchor here returned 0 hits for exactly that reason.
  Choose anchors **within a single physical line** and uniqueness-check each one
  (`grep -c -F` must return 1) before writing it down.
- **Anchors eliminate rot, not under-coverage** — a correction to this incident's
  own claim, per the third officer. A row can still name too few anchors, which is
  precisely what the second halt was. What the scheme actually buys is that the
  population becomes *enumerable* and each member becomes a one-command binary
  check — which is why one officer could exercise all 19 in a single script
  instead of the one-instance-per-cycle grind the convergence read described.
- **A corrective can be worse than the defect it fixes.** Correction 1 narrowed a
  citation from `116-135` to `128-135` on a prior officer's observation, and
  thereby broke a coverage that had been correct. Three seats — officer, IC,
  Dispatcher — each faithfully transcribed the one before and none re-derived
  against the source. **The seat applying a corrective owes the same
  re-derivation as the seat that found the defect.**
- **When the convergence read says "same class", the altitude fix is cheaper than
  it looks.** Replacing ~30 citations wholesale cost one write plus one verify —
  the same as the site-by-site fix would have cost for its *one* instance, with no
  third instance possible in the same form.
- **Where the corrective lands decides who can execute it.** This refutation named
  `214-LOG.md`, under `.dcs/**`, which specialists are barred from by
  construction. `execute.md`'s "fix-taskings" path was therefore unavailable and
  the IC had to name the Dispatcher as executor. Worth checking the corrective's
  *location* before choosing a disposition.
- **A byte-count acceptance criterion is line-ending-sensitive on Windows.**
  `core.autocrlf=true` with no `.gitattributes` means a fresh worktree measures
  larger than a long-lived checkout of the same commit — here 319 B on a 43,008 B
  ceiling. Measure in the worktree (conservative), say which tree in the criterion,
  and treat the sensitivity itself as a separate defect. *Sharper form discovered
  at the merge:* the merged tree now holds `doctrine.md` at CRLF and `schemas.md`
  at LF simultaneously, so the metric depends on which files git last rewrote —
  it has no stable definition, not merely an offset.
- **A threshold derived inside an incident can expire before the incident
  merges.** The ratchet here was derived correctly from a hot path that a
  concurrent commit then changed underneath it. **Derive any budget from the
  merge result, not from the branch** — and run the project's merge-time guard
  before merging, which is the only step that can see it. `close.md` step 1a
  earned its keep on this incident's first use.
- **An incident cannot assume it owns the version number.** This one claimed
  0.6.5 at plan time and found 0.6.5 and 0.6.6 both taken by close. Where version
  bumps are atomic with the change (as `CLAUDE.md` requires here), the number is
  only safely chosen at merge — or the incident should not claim one at all and
  let the merge assign it.

## Deviations this incident

**No specialist deviation.** OPS-1 returned `status: "done"` on its first and only
spawn, reached the byte target on tier-1 cuts alone, drew nothing from the
pre-authorized reserve, and filed no deviation.

**Two Safety halts, both against the routing ledger, neither against the trim**
(from `214-LOG.md`, not memory):

1. **Halt 1** — six of the ledger's redundancy citations pointed at unrelated text
   in the delivered tree: they carried pre-edit line numbers, rotted by this
   incident's own 114-line appendix append, with no regenerating command beside
   any of ~30 citations. A principle-15 violation inside the incident's own
   append-only artifact. Disposition: `fix_taskings`, executed by the Dispatcher
   as IC work (`.dcs/**` is barred to specialists).
2. **Halt 2** — that corrective narrowed row 17's citation from `116-135` to
   `128-135` and broke a coverage that had been correct: the deletion has three
   clauses and `128-135` homes only one. The officer also found the wording
   internally incoherent (disjoint ranges called "the full range" in contrast to
   each other). **Escalation trigger (b)** fired; 209 filed at
   `.dcs/esg/SITREPS/doctrine-hot-path-trim-p1.md`; convergence read returned
   **same class**; the Owner chose **raise the altitude** over the cheaper
   site-by-site fix.
3. **Correction 2** replaced all ~30 line-range citations with content anchors.
   Third verification: **pass, zero refutations** — 19/19 anchors returned exactly
   one hit.

**Two Dispatcher defects, recorded rather than smoothed over:** transcribing the
ledger into the append-only log without adding regenerating commands (cause of
halt 1), and applying directive 7 literally without re-deriving it against the
source (cause of halt 2).

**A third escalation, at the merge — trigger (a).** Between this incident
opening and closing, the integration branch advanced **three commits made
outside DCS** (`6a57b97` v0.6.5, `c09f0fd`, `0428ac4` v0.6.6). Not a territory
violation — the portfolio partition governs incidents, and nothing polices
direct commits to main — but it invalidated three premises:

1. **`schemas.md` grew 1,189 B** (`6a57b97`). This incident's arithmetic treated
   it as a fixed 14,596 B constant; criterion 1's derivation and criterion 8's
   ratchet both rested on that. The merged pair came to 37,906 B against the
   ratchet of 37,888 — **the merge-time guard would have landed red on main by
   18 B**, while passing on both branches independently. This is precisely the
   defect class `close.md` step 1a exists to catch, and it caught it.
2. **The version was taken twice over** — 0.6.5 and 0.6.6 both shipped while this
   incident held 0.6.5. `dcs/VERSION` conflicted.
3. **`package.json` was rebuilt** by `0428ac4`, which already fixed the
   corruption this incident's specialist discovered. This branch had edited the
   old 6.3 MB file, so `package.json` conflicted and main's side had to win
   entirely.

A second 209 was filed
(`.dcs/esg/SITREPS/doctrine-hot-path-trim-p1-merge.md`) and the Owner chose:
re-seat the ratchet from the merge result, resolve `dcs/VERSION` to **0.6.7**,
take main's `package.json` wholesale, and merge. Re-derived:
`ceil(37906/1024) + 1 = 38`. The merge-time guard then passed 14/14 on the
resolved tree.

**This is principle 15 operating on the incident's own output.** The ratchet was
correctly derived from a measurement that was true when taken and false when
merged. No amount of care inside the incident would have prevented it; only
measuring the merge result did.

**One command-point ruling amended mid-incident:** ruling B originally had the AAR
carry the routing ledger; as amended it carries the original ledger (for its
coverage mapping) together with Correction 2 (authoritative on all citations).
Correction 1 is superseded and is never carried as authoritative.

**Five officer observations carried to the Owner's criterion-10 read**, all
explicitly not refutations, all recorded verbatim in `SAFETY.md`: row 16 absent
from Correction 2's accounting (no citation owed, substance verified surviving);
"rows 17 and 18 have different homes" is imprecise (superset, not different set);
"the defect class stops being representable" overclaims by half; row 17 clause 3's
home is generalized rather than literal; and the new `HOT_PATH_BUDGET_KB`
comment's "~319 B" lacks a command beside that specific number.

**Owner-UAT (criterion 10): DONE.** The Owner was shown the complete
`doctrine.md` diff (38 changed lines) plus two flagged borderline compressions —
principle 13(f)'s diagnosis of what three rejects mean, and *Parallel operation*
bullet 3's explicit "never reaches into a worktree early" — and approved with no
rule lost and no restoration requested.

**Deploy status: NOT DEPLOYED — deploy pending.** `DELEGATION.md` v1 carries
`deploy.auto_after_close: true`, which would have run the deploy train in-line at
`/dcs-run` step 7a; the **Owner explicitly declined** it at close and chose to
leave the row deploy-pending. `~/.claude/dcs/VERSION` therefore still reads the
pre-incident version until someone runs `/dcs-deploy`; the version bump to 0.6.5
means the marker will genuinely advance when they do. Recommend amending the
Delegation at the next `/dcs-esg` so it stops asserting a default the Owner
overrode on its first use.

## Memory routing

`CLAUDE.md` documents a three-store routing rule (doctrine = rules,
`doctrine-appendix.md` = provenance, `vault/` = maintainer-only) and names
`vault/00-Navigation.md` as the entry point. Routed accordingly:

- `vault/Meta/building-dcs-lessons.md` — appended "Citations into a file the
  incident is editing", covering the anchors-over-line-ranges lesson, the
  hard-wrap failure mode, the anchors-kill-rot-not-under-coverage correction, and
  the corrective-can-be-worse-than-the-defect pattern.
- `vault/Metrics/incident-metrics.md` — hot-path row updated with this incident's
  measurement and its regenerating command; the pre-existing mixed-kB-base defect
  (1000-based "31.7 kB" beside 1024-based "40.5 kB") corrected to a single 1024
  basis, matching the guard.
- `vault/Backlog.md` — item 1 marked done with the closing commit; three new items
  added from this incident's discoveries — renumbered to **7, 8, 9** at the
  merge, because commits landing on main in parallel had already claimed 5 and 6
  (7: the remaining regrowth, with `schemas.md` now named as the strongest
  candidate; 8: the EOL sensitivity and the guard-blind band; 9: the
  `package.json` corruption, **written up as already fixed out-of-band** by
  `0428ac4`, which repaired it before this incident reached its merge). The
  same collision hit `Meta/building-dcs-lessons.md`, where the auto-merge
  produced two sections numbered 7; this incident's became §8. **Position-based
  numbering in an append-heavy shared file collides silently under a clean
  auto-merge** — worth its own fix if it recurs.

**Nothing was routed to `doctrine.md` or `doctrine-appendix.md`.** The lessons here
are about *building* DCS, not about how DCS behaves — the vault's own stated test.
If any of them should become a rule, that is its own incident.

## Intake source closure

**Owner chat via `/dcs-run`, restating `vault/Backlog.md` item 1** ("Hot-path
regrowth — trim doctrine again"). The intake source is repo-local and
maintainer-owned, not an external production system, so there is no routine to
delegate to and no ad hoc production write at risk. Item 1 was marked done in the
same close commit, citing the integration commit sha.

The register row `doctrine-hot-path-trim` moves `ACTIVE` → `MERGED (deploy
pending)`; it reaches `DEPLOYED` only when `/dcs-deploy` confirms the marker
advanced.

**One row this incident created was retired unused.**
`package-json-description-corruption` — registered at priority H when OPS-1
flagged the 6.3 MB `package.json` — was fixed out-of-band by `0428ac4` before
this incident merged, and closes as `KILLED (fixed out-of-band)`. The specialist's
behaviour was still exactly right: it found a real defect outside its territory,
did not touch it, and reported it. That the Owner got there first is a good
outcome, not a wasted one.

## Safety Officer's final verdict (verbatim, from SAFETY.md)

**`verdict: pass`** · **`refutations: []`**

> I went looking for the fourth instance of the class and did not find one. [...]
> Every one of the 19 anchors returns exactly one hit — I extracted the commands
> programmatically [...] rather than retyping them, so a transcription
> normalization on my side could not mask a broken anchor. None returns 0 (the
> hard-wrap mode), none returns 2+. [...] Row 17 is genuinely fixed. All three
> clauses are homed, and the second anchor `keystroke, not a record` resolves to
> `51dd073:126` — the exact sentence halt 2 said CORRECTION 1 had wrongly
> excluded. [...] Nothing outside `.dcs/**` moved. Five files, identical counts,
> hot path 36,717 B measured by me, guard 12/12, gate 25/25, intake 10/10, version
> sync atomic at 0.6.5. [...] The observations are real and I would not have
> written them if they were not, but each one is a sentence in the entry's prose
> reasoning that is looser than the citation it accompanies. None of them leaves a
> cut byte unaccounted, none of them can rot, and none of them would mislead a
> later seat into a wrong measurement — which is the harm principle 15 exists to
> prevent.

The full verdict, its 14 `checks_run` entries and all five observations are in
`SAFETY.md`.
