# AAR — After Action Report

**Incident:** hot-path-budget-eol-sensitivity
**Type:** 1
**Opened:** 2026-07-25
**Closed:** 2026-07-25
**Operational periods:** 1 (one stamped IAP, one Safety verification, no halts)

## Outcome

**Goal met.** The repo now has one line-ending policy, and neither byte-exact
mechanism can give a different answer in a different checkout of the same
commit.

| | before | after |
|---|---|---|
| `git ls-files --eol` (this worktree) | `83 i/lf w/crlf` | **`84 i/lf w/lf`**, zero `w/crlf` |
| hot path, raw `getsize` | 37,906 here vs 37,734 in main — same commit | **identical in both** |
| hot path, as the check measures it | tree-dependent | **normalised — `21966 15613 37579` anywhere** |
| archived approval stamp | `a5eec3b4` ≠ on-disk `375c4859` | **all three digests agree at `a5eec3b4`** |
| gate suite | 25 cases | **32** |
| integrity suite | 14 checks | **15** |

The substantive change is one line:

```python
- return bool(stored_hash) and stored_hash == sha256_of(iap)
+ return bool(stored_hash) and stored_hash in approval_digests(iap)
```

**Criterion 3b** (raw `getsize` agreeing between this worktree and `C:\DCS`)
was deferred by construction — it needs the merge plus `C:\DCS`'s own
re-materialisation — and is discharged at close, below. Criterion 10 was
approved by the Owner; 11 settles at merge; 12 is the deploy period's.

## What worked

- **Both chiefs worked empirically, in disposable clones, and deleted them.**
  Neither reasoned about git's behaviour where it could be measured. That is
  what overturned the incident's own founding premise (below) and what produced
  the mandatory path-scoped re-materialisation form after both git-FAQ forms
  were measured destroying a planted uncommitted edit.
- **The IC decided the chiefs' ordering conflict on a number, not a preference.**
  83 files `w/crlf`, 54 in shipped scope, therefore S3 could not deliver green
  evidence for its own tasking before re-materialisation. The Logistics
  counter-reason was ruled void *by its own measurements*.
- **Extending scope rather than registering it.** The Planning Chief found three
  more readers of the marker contract outside territory. The IC added S4 instead
  of deferring, on the grounds that shipping a changed contract with unmigrated
  readers is the canonical non-shippable half-migration. `execute.md` and
  `status.md` would otherwise have hard-stopped on exactly the drift the gate
  had just been taught to tolerate.
- **Writing the contract precisely enough that a specialist could not get it
  subtly wrong.** The tactic specified `crlf` must derive from `lf` and never
  from `raw` (or an already-CRLF file doubles into `\r\r\n`), and that a lone
  `\r` stays untouched. Both survived adversarial review.
- **The read-side-only widening.** `plan.md` was forbidden and stayed untouched
  because the IC stamps a raw digest, which is a member of the accepted set by
  construction. That is what made the change safe to land on a live gate
  mid-incident: the new `marker_valid` returns `True` wherever the old one did,
  so it can only ever allow more.
- **The v0.6.5 advisory path, on its first use.** Seven findings that would have
  been binding halts under the previous charter were fixed by the IC and folded
  into the integration commit. Zero re-verify cycles spent on prose.

## Lessons

- **A mechanism that reads raw on-disk bytes will diverge from what git
  records, unless the repo pins a line-ending policy.** Not a Windows quirk —
  `core.autocrlf` is only one way to get there. If a hash or a size decides
  something, ask which representation it is deciding on, and pin it.
- **Fix the defect where it ships, not where you happen to notice it.**
  `.gitattributes` is absent from `package.json`'s `files` whitelist and npm
  performs no git checkout, so a tree-only fix would have repaired this repo and
  shipped the defect to every downstream project. That single fact moved the
  incident from Type 3 to Type 1 and added the gate to territory.
- **When you change a contract, enumerate its readers before you ship.** Four
  places computed a raw sha256 of `IAP.md`. Fixing one and leaving three would
  have made the workflows *stricter than the gate* — a false halt on a validly
  approved plan. S4's tasking ended with "if you find a fourth reader, that is a
  deviation", precisely because the population had been under-enumerated once
  already.
- **An untracked deliverable is invisible to every in-tree check.** The Safety
  Officer found `.gitattributes` untracked and demonstrated both halves: a clone
  of the then-HEAD reproduced the entire original defect, while every criterion
  measured inside the worktree still read green. `git commit -a` would have
  silently shipped nothing. **Stage new files explicitly and verify with
  `git show --stat`.**
- **A derived number in a durable artifact should be deleted, not corrected.**
  `CLAUDE.md`'s suite counts had rotted from 25/12 to 32/15. Updating them would
  have reset the clock; removing them and pointing at the suite's own `N/M`
  output ends the class. Same reasoning retired the bad budget derivation rather
  than silently overwriting it.
- **Verify the arithmetic in a derivation, not just its shape.** The budget
  comment read `ceil(37906/1024) + 1 = 38` — wrong twice: that expression is
  **39**, and 37,906 was a basis this incident replaced. It survived a previous
  incident's review because the *value* was right and nobody evaluated the
  formula.
- **A planned mitigation for an unmeasured hazard is waste.** This incident's
  201 was planned around "the fix can invalidate its own approval marker", and
  the Logistics Chief dissolved it in three measurements: the renormalise is a
  no-op here, untracked files are never rewritten, and the Write tool emits LF so
  the artifacts were already in the target representation. **Measure the hazard
  before designing around it** — and note the real risk was somewhere else
  entirely (the live tracked duplicate of the gate hook).

## Deviations this incident

**None.** All four specialists returned `status: "done"` on their first and only
spawn. No deviation was filed, no reserve drawn, no re-plan.

**No Safety halts** — a first for this repo's self-hosted incidents. One
verification, `pass`, zero refutations.

**One premise overturned before execution** (not a deviation — it was found at
planning): the self-invalidation hazard the 201 built its ordering around does
not exist. Confirmed in practice afterwards — this incident's own
`IAP-APPROVED` still matched its `IAP.md` after 83 files were re-materialised.

**Two chief-flagged scope gaps**, both resolved by the IC at command point 2
rather than deferred: the live tracked duplicate `.claude/hooks/dcs_gate.py`
(added to S2's territory, plus a new test asserting the two copies match), and
the three other contract readers (new tasking S4).

**Seven Safety advisories**, all resolved by the IC before the integration
commit per `execute.md` v0.6.5 — including one genuine arithmetic error, one
counterexample to a docstring claim found by exhaustive search (a CR immediately
preceding a CRLF is not distinguished, because git's own fold is lossy there),
and the untracked-`.gitattributes` finding that would have voided the
deliverable.

**One scope addition by a specialist, disclosed rather than found:** S3 filled in
docstring entries for two pre-existing checks that were already missing. The
Safety Officer ruled it in-territory tidying rather than drift — documenting only
the new check would have left the enumeration reading 1–8 then 10, which is
itself a false census.

**One scope addition by the IC:** applying advisory 4 required editing
`CLAUDE.md`, outside every specialist territory. Surfaced to the Owner as a
Type 1 scope change and signed off.

**One environment halt:** the C: volume hit **0 bytes free** while `IAP.md` was
being written. The write created nothing rather than a truncated file, so state
stayed consistent; reported as a blocker rather than resolved by deleting the
Owner's files. The Owner cleared space and the chain resumed with every artifact
verified at its pre-halt byte count.

## Memory routing

Per `CLAUDE.md`'s three-store rule, written to the **worktree's** copies so they
ride the merge:

- `vault/Meta/building-dcs-lessons.md` — new section on byte-representation
  defects as a family, the enumerate-the-readers rule, and the
  measure-the-hazard-before-designing-around-it lesson.
- `vault/Backlog.md` — item 8 marked done; the three new register candidates
  recorded with their evidence.
- `vault/Metrics/incident-metrics.md` — hot-path row updated to the normalised
  basis, with the note that the metric now *has* a stable definition.

Nothing routed to `doctrine.md` or `doctrine-appendix.md`: these are lessons
about building DCS, not changes to how DCS behaves.

## Intake source closure

`/dcs-run` from the Owner, register rank 1 `hot-path-budget-eol-sensitivity`,
from `vault/Backlog.md` item 8 — repo-local and maintainer-owned, no external
system and no curating routine to delegate to. Item 8 marked done in the close
commit.

Register row moves `ACTIVE` → `MERGED (deploy pending)`.

## Safety Officer's final verdict (verbatim, from SAFETY.md)

**`verdict: pass`** · **`refutations: []`** · seven advisories

> All nine in-period acceptance criteria are met, and criterion 4 — the one I
> was told to attack hardest — survives an exhaustive assault: 13,120
> uniform-conversion combos with zero violations, 1.19 million text pairs with
> zero leakage, and 8/8 correct verdicts through the real hook binary. I
> reconstructed criterion 5's red-before myself rather than trusting the paste,
> and it landed exactly as claimed. No forbidden-zone violations; the 83-file
> re-materialisation lost nothing.

The full verdict, its 24 `checks_run` entries, all seven advisories with their
resolutions, and five observations are in `SAFETY.md`.
