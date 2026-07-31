---
tags: [dcs, backlog]
updated: 2026-07-29
---

# Backlog

Known gaps, each with the evidence behind it. Items here are candidates
for `/dcs-esg` to queue as incidents — this file is *not* a register.

## 1. Hot-path regrowth — trim doctrine again ✅ DONE (partially)

**Closed 2026-07-25** by incident `doctrine-hot-path-trim`, integration
commit `de50257`, merged as `b3ab5a8`, shipped in v0.6.7. It was indeed the
natural first self-hosted incident, and it exercised the whole loop rather
thoroughly: one specialist spawn that hit its target first time, **two
Safety halts**, **two escalations** — trigger (b) with a convergence read
and an Owner "raise the altitude" ruling, then trigger (a) at the merge —
and none of it against the trim. See [[Meta/building-dcs-lessons]] §8.

On the merge result: hot path **42,623 → 37,734 B** (−4,889); ratchet
re-seated **42 → 38 kB**.

**Partially** because the post-diet equivalent is ~31,723 B, so roughly
half the regrowth remains — see item 7. A deliberate call at close.

**Read the two numbers above carefully — they are not the ones the incident
measured.** It measured 41,763 → 36,717 B and set the ratchet to 37. While
it was open, `6a57b97` added 1,189 B to `schemas.md`, so the merged pair
came out larger than either branch predicted and a 37 kB budget would have
landed red on main. The merge-time guard caught it (`close.md` step 1a
doing exactly its job — a check that passes on both branches saying nothing
about the merged tree), and the budget was re-derived from the merge
result. **A size is a derived fact with a lifetime; this one expired
between being measured and being merged.**

## 2. Field-lesson citations are unverifiable ✅ RESOLVED — `field-lesson-citations`, 2026-07-31

`tests/test_doctrine_integrity.py` checks structure but cannot check
whether *"field lesson 2026-07-24: X happened"* is true — the evidence
lives in another project's incident logs, and the package must not depend
on them ([[Decisions/distribution-and-scheduling]]).

A false lesson shipped exactly once (v0.5.10, corrected in v0.5.11).
Options: require every field lesson to name the incident slug and
artifact so a human can verify in one lookup; or keep verification a
Safety Officer duty and state it explicitly in its charter. Leaning
toward the first — it makes the claim checkable without adding a
dependency.

**Resolved by `field-lesson-citations` (commit `710cf52`, 2026-07-31):**
every field lesson citation in the 6 target files now carries an incident
identifier (slug, version, or "(predates self-hosting)"); the convention
is documented in `doctrine-appendix.md`; check 20 in
`test_doctrine_integrity.py` mechanically guards against recurrence. See
`.dcs/incidents/2026-07-31-field-lesson-citations/AAR.md`.

## 3. The register has no cross-project view ✅ DECIDED — not building it

Each project's register is its own portfolio (correct — see
`plan.md` lint 8). But an Owner running DCS in several repos has no
single place showing what is in flight everywhere. `/dcs-status
--campaign` is per-project by design.

Not obviously worth solving; noted so it is a decision rather than an
oversight. **Decided 2026-07-25** at the second `/dcs-esg`: not building it.
The reasoning is in [[Decisions/cross-project-register-view]] — briefly, the
thing that would make the view valuable (acting on the aggregate) is scoped
per-project by construction, and the cost is a second write target on every
state transition. Register row `KILLED`. Reopen if a second onboarded project
makes the pain concrete.

## 4. Intake nudge has no telemetry — RESOLVED (2026-07-31)

`dcs_intake.py` fires once per session, but nothing records whether the
offer was accepted, declined, or ignored. Without that, there is no
evidence for tuning it — and tuning by impression is what principle 15
warns about. A single line appended to a local (gitignored) log would be
enough.

**Resolved by incident `intake-nudge-telemetry` (Type 3, period 1).**
`record_telemetry()` appends one-line JSON to `.dcs/esg/intake-telemetry.log`
on each first-session invocation. See `.dcs/incidents/2026-07-31-intake-nudge-telemetry/AAR.md`.

## 5. Version bumps still go through PowerShell — FOLDED into the `bin/dcs.js` incident

> **Folded at the eleventh `/dcs-esg`, 2026-07-29:** register row
> `version-bump-command` was absorbed into `doctor-version-only-check`
> (one `bin/dcs.js` incident — content-aware `doctor` + `bump`), per
> [[Decisions/v0.7-scope]]'s weighing. The hazard class below carries
> across unchanged.

The encoding disaster in [[Meta/building-dcs-lessons]] §6 was repaired
and guarded (no-Cyrillic check, `package.json` < 8 kB), but the *process*
that caused it is unchanged: version bumps are still typed as PowerShell
read-modify-write one-liners, now merely watched by a guard.

**Queued 2026-07-25** as register row `version-bump-command`, rank 3.

The durable fix is a tiny `bin/dcs.js bump <version>` that edits
`dcs/VERSION` and `package.json` in Node — one command, correct
encoding, both files always in sync, no shell involved. Small, and it
removes a whole hazard class rather than detecting it.

**Second piece of evidence, 2026-07-25:** `doctrine-hot-path-trim` had to
edit `package.json`'s version field at merge time and did it with the Edit
tool specifically to avoid this hazard — a workaround a seat has to
*remember*, which is the shape of a missing mechanism (§1).

## 6. Type 5 express lane is under-used — PARKED

Six of eight incidents ran the full Type 3 loop; several sub-parts would
have qualified for the express lane (one specialist, IC verifies, no
incident directory). Worth watching whether typing is systematically
conservative — if so, the typing guide needs sharper Type 5 examples
rather than a doctrine change.

**Parked 2026-07-25** at the second `/dcs-esg`. The ratio above is from one
*other* project, and this repo's first closed incident (`doctrine-hot-path-trim`,
a genuine Type 3) adds nothing either way. Changing the typing guide on this
base would be exactly the speculative mechanism §5 warns about. Revisit once
several self-hosted incidents have closed.

## 7. Trim schemas.md ✅ DONE

**Closed 2026-07-26** by incident `schemas-md-trim`, integration commit
`08f75f0`. Type 3, **one period, one specialist, one attempt, zero
deviations, zero Safety halts** — the second clean self-hosted incident.

`schemas.md` 15,613 → **13,296 B**; the pair 38,878 → **36,561**; ratchet
**38 → 37**; slack **34 B → 1,327 B**. Slack restored *and* the ceiling
lowered in one act, because unclaimed slack under an unchanged ceiling grows
straight back. Regenerate:

```bash
python -c "import pathlib; d=pathlib.Path('dcs/references/doctrine.md').read_bytes().replace(b'\r\n',b'\n'); s=pathlib.Path('dcs/references/schemas.md').read_bytes().replace(b'\r\n',b'\n'); print(len(d), len(s), len(d)+len(s), 37*1024-len(d)-len(s))"
```

**This item's own framing was wrong, and the stem caught it.** It said "the
other half of the hot-path regrowth". Two analysts independently measured
that `schemas.md` had **not changed since `6a57b97`** — 15,613 B at that
commit, at `bbb17ac`, and at HEAD. The 1,299 B that consumed the slack came
from `doctrine.md` during `halt-loop-unbounded`. This file was the **donor**,
not the source. Worth remembering when filing the next item: a title is a
claim, and this one survived unmeasured through a `/dcs-esg` session and into
a register row.

**Two rows were split out at the stem** and are queued:
`schema-citation-guard` (rank 2) and `json-examples-unparsed` (rank 11). The
first exists because an analyst *demonstrated* the hazard instead of arguing
it — deleting a section and renumbering its neighbours left all three suites
green while 19 `schemas.md #N` citations pointed at the wrong sections. The
trim therefore forbade renumbering outright and left section 8's number
reserved with a pointer.

> **Corrected 2026-07-26 by `schema-citation-guard` (Safety advisory 5).**
> The population is **20 citations in 14 files**, not 19, and "pointed at the
> wrong sections" overstates it: the measured split is **14 drifted, 6 kept
> their meaning, 0 dangled**. Both errors have the same root — the count
> above came from a line-based `grep` that cannot see the citation wrapped
> across a newline in `agents/dcs-commander.md:101-102`. That the dangling
> count is **zero** is the load-bearing fact, not a detail: it is why a guard
> checking that a number *resolves* would have caught none of the 14.
> Regenerate both figures with the enumerator recorded in
> `.dcs/incidents/2026-07-26-schema-citation-guard/202-OBJECTIVES.md`
> ("Область и метод"), which normalises wraps before matching; the drift
> split comes from `201-BRIEF.md`'s Evidence section. `schema-citation-guard`
> closed 2026-07-26; the hazard is now guarded by check 13 in
> `tests/test_doctrine_integrity.py`.

This item's second candidate — a ratchet re-seat — was executed as part of
the same act rather than deferred, for the reason above. The open question it
inherited from item 8 (budget in bytes rather than kB) was **not** taken: the
period changed the ratchet's value, not its unit.

### As originally filed

`doctrine-hot-path-trim` landed the pair at 37,734 B against a post-diet
31,723 B (regenerate both via [[Metrics/incident-metrics]]). The remaining
~6 kB is a harder cut than the first: item 1 took the provenance that was
obviously provenance, and what is left is more entangled with the rules.

Two specific candidates the closing IC named, and `schemas.md` has since
become the stronger one:

- **`schemas.md` is now 15,613 B — 41 % of the hot path** — and it grew
  1,189 B in `6a57b97` *while item 1's incident was open*, which is what
  forced that incident's ratchet up from 37 to 38 at the merge. It has
  never been re-examined since the v0.5.0 diet trimmed it, and it was
  explicitly out of scope for item 1. It is now the single largest
  untouched block in the hot path.
- A ratchet re-seat to 37 or 36 kB after a period of stability, which would
  also narrow the guard-blind band described in item 8.

**Fresh evidence, 2026-07-26 — the slack is now 34 B.** `halt-loop-unbounded`
closed at **38 878 of 38 912 B**, having spent almost the whole remaining
margin on one rewritten clause of principle 13. It held the ratchet at 38
(the IAP forbade raising it, and a raise was declared a deviation rather
than an option), so nothing is broken — but this item stopped being a
tidiness project. **34 B is less than one line of prose.** The next
doctrine or schemas addition of any size turns the merge-time guard red,
and whoever hits it will be mid-incident with a ratchet they are not
allowed to touch. Regenerate:

```bash
python -c "import pathlib; d=pathlib.Path('dcs/references/doctrine.md').read_bytes().replace(b'\r\n',b'\n'); s=pathlib.Path('dcs/references/schemas.md').read_bytes().replace(b'\r\n',b'\n'); print(len(d)+len(s), 38*1024, 38*1024-len(d)-len(s))"
```

## 8. Hot-path budget check is line-ending-sensitive ✅ DONE

**Closed 2026-07-25** by incident `hot-path-budget-eol-sensitivity`,
integration commit `bbb17ac`. Typed **1**, one operational period, four
specialists, **no deviations and no Safety halts** — the first self-hosted
incident to run clean.

It turned out to be bigger than this item described. The item framed a
*measurement* defect; the real find was that `dcs/hooks/dcs_gate.py`'s
approval marker had the **same** defect and was **already broken** for the
incident that closed hours earlier — its stamp verified against the git blob
and failed against the on-disk file. That is the enforcement mechanism, and
unlike the size check it **ships**, so the fix had to live in the mechanism
and not only in the tree. Hence Type 1 rather than the Type 3 assumed here.

Delivered: `.gitattributes` = `* text=auto eol=lf`; the gate accepts a
digest **set** (raw / LF-normalised / CRLF-normalised) instead of one hash;
the hot-path measurement normalises before counting; a new shipped check
forbids CRLF in the packaged set; and the three other readers of the marker
contract (`execute.md`, `status.md`, `forms.md`) were migrated with it.
`plan.md` was deliberately left alone — it stamps a raw digest, which the
widened set contains by construction, so the change is read-side only.

Result: `84 i/lf w/lf` with zero `w/crlf`; the hot path measures
`21966 15613 37579` in *any* checkout; and the previous incident's archived
stamp verifies again.

**The guard-blind band this item also raised is now moot for the reason it
was raised** — the metric has a stable definition, so an acceptance bar and
the guard's bar no longer disagree because of representation. Whether the
budget should take bytes rather than kB is a live question, but it belongs
with `schemas-md-trim` (item 7), which owns the ratchet value.

### Three follow-ups registered from this incident

- **`.gitattributes` matches neither `guarded_paths` nor `unguarded_paths`**
  in `.dcs/config.json`, so the repo's own line-ending policy file is
  ungated. Harmless today; wrong in principle.
- **`plan.md:348-349` still describes the gate as computing "a plain sha256
  of the file's bytes".** The *instruction* remains correct and safe — the IC
  stamps a raw digest, a member by construction — but the parenthetical is
  stale. Deferred deliberately: `plan.md` was forbidden territory precisely
  because touching the stamper is how you break the asymmetry that makes the
  widening safe.
- **`close.md` should codify the post-merge re-materialisation.** Merging an
  EOL policy leaves the *consuming* checkout stale, and no workflow knows to
  refresh it — the merge-time guard cannot see the omission either, since
  both the stale and the fresh measurement pass. Its own incident: `close.md`
  is guarded territory.

## 9. `package.json` ships a corrupted description ✅ FIXED OUT-OF-BAND

**Already fixed before this item was ever committed**, by `0428ac4`
(v0.6.6), which rebuilt `package.json` from 13.5 MB to 1.3 kB with an
ASCII-safe description. Recorded rather than deleted, because how it was
found and how it was fixed are both worth keeping.

An Ops Specialist working item 1 noticed, from inside its own territory,
that `package.json` was 6,322,630 B with ~2,942,431 characters of mojibake
in its `description`. It correctly did **not** touch it — out of territory —
and flagged it instead, which is exactly the behaviour doctrine's deviation
rule asks for. It was registered as `package-json-description-corruption` at
priority H. By the time item 1 reached its merge, `0428ac4` had already
repaired it, and the register row was retired `KILLED (fixed out-of-band)`.

**The cause is worth remembering**, from `0428ac4`'s own message: every
version bump used PowerShell `Get-Content -Raw` + `WriteAllText`, which
reads with the system ANSI codepage rather than UTF-8, so each bump
re-encoded the description's em-dash — 1,378 → 4,356 → 139,473 → 6,322,630
characters across thirteen commits. Exponential, invisible in diffs, and
`CLAUDE.md` already forbade PowerShell `Set-Content`/`Out-File` for exactly
this class. See [[Meta/building-dcs-lessons]] §6, and item 5 above for the
process fix that would remove the hazard rather than watch it.

**And the guard could not see it:** the BOM/U+FFFD check passes on
double-encoded text, because it is *valid* UTF-8. `0428ac4` added the two
checks that can — no Cyrillic anywhere in the shipped package, and
`package.json` under 8 kB.

Regenerate:

```bash
wc -c package.json
python -c "import json; print(len(json.load(open('package.json',encoding='utf-8'))['description']))"
```

It was priority H because `package.json` is the npm release surface — and
that was borne out: `npm publish` failed with E415, "the package.json file
in the tarball is too large (>10 MB)", which is what prompted the
out-of-band fix. `install.ps1` never references `package.json`, so the
local deploy path was never affected; it gated the registry release only.

## 10. Safety's `halt` is binding on the IC — should it be?

**Raised by the Owner, 2026-07-26**, during `halt-loop-unbounded`, from
having watched real ICS: *the Safety Officer exercises the right to halt,
but assessing and accepting the risk is the IC's own responsibility.*
Today's doctrine says the opposite in as many words — `execute.md` step 9:
"**`halt` (binding — no closing over this)**", and the officer's charter:
"its halt verdict is binding on the IC". The IC picks the *disposition*
of a halt and may escalate, but cannot close over one.

The Owner's broader claim, which this item exists to carry: **the process
must be results-oriented, not process-oriented**, and blind adherence
produces paralysis. The evidence is this incident: 17 h from opening to
its **first commit**, four stamps, two halts, one deviation, six specialist
spawns, eight IC command-point spawns.

**The counter-argument, so it is not relitigated from one side.** The
201 of this very incident documents the failure mode: a safeguard a human
can lift *gets lifted*. Trigger (b) asks the Owner on every halt, and on
the fourth the Owner issued a blanket pre-authorization forward. Make the
halt overridable by the IC and the pressure that currently produces
"continue" simply moves to overriding halts — and the IC here is a model,
not a person. [[Meta/building-dcs-lessons]] §1 ("Prose fails; mechanisms
hold") classifies exactly this.

**A third framing that may be the real one:** a `halt` in DCS is not "stop
an unsafe act" but "the work is not done." Those are different objects.
The ICS analogy transfers cleanly to the first and not obviously to the
second.

Adjacent and possibly the cheaper lever: the already-queued
`safety-halt-functional-scope` row — 8 of 10 halts on `prod-tools-drift`
found no functional defect, so refutations about prose and stale line
numbers weigh the same as functional ones. Narrowing what may be *called*
a halt is mechanizable; making the halt advisory is not.

**Not queued by the close** — putting a row in the register is an ESG act.
Candidate for the next `/dcs-esg`.

## 11. `amend_tasking` has no cheap route — the deviation path has no proportionality ✅ DONE

> **Closed 2026-07-28 by incident `deviation-path-proportionality`**
> (Type 3, integration commit `e285108`). `plan.md` gained `## 6c.`, a
> bounded route reachable only from an already-logged command-point
> decision: 0 agent spawns, at most 1 Owner round-trip (a Delegation
> delta-screen, never the whole plan), terminating at the unmodified
> steps 7-8 so `marker_valid()` and trigger (c)'s attempt tally stay
> exactly as accurate as the full path — "cheap but still-counted," the
> direction this item's own text guessed at. Also shipped: backlog Rec 2
> (transcription by reference), folded in at typing by explicit Owner
> decision — doctrine principle 15 extended to seat-to-seat transfer, two
> `execute.md` command-point spawn prompts rewritten to cite sources.
>
> **Not a clean first pass — three Safety halts, all one class**, fixed
> by a structural change (IC-authored validation fixtures; deleting a
> recurring "these checks are provably unneeded" claim rather than
> re-wording it a fourth time) rather than by narrowing the fix. Full
> account: `.dcs/incidents/2026-07-28-deviation-path-proportionality/AAR.md`
> and [[Meta/building-dcs-lessons]] §20 — the lesson worth carrying
> forward is about how DCS verifies its own fixes, not about this
> boundary condition specifically. Two follow-ups queued below (items 19,
> 20) rather than absorbed into this incident. Owner-UAT: no distinct UAT
> section — all 9 acceptance criteria were agent-verifiable (tests, byte
> counts, greps), no browser/manual observation involved. Deploy pending.

### As originally filed

**Measured in `halt-loop-unbounded`, 2026-07-26.** S3 returned a
`deviation` whose fix was: add one derived regex built by concatenation
from an existing constant, and reword one bullet in a check's
specification. Reaching that fix cost an IC arbitration spawn, a
transcription pass, a full `/dcs-plan` run, a tasking lint, a second IC
spawn for acceptance, an IAP rewrite, a 209 sitrep, two Owner questions,
and a re-stamp.

`schemas.md` #6 offers three dispositions — `replan`, `amend_tasking`,
`escalate_owner` — but `execute.md` step 6 routes **all** of them through
the same return-to-planning, because any tasking edit changes `IAP.md` at
the next pass and voids the hash. So `amend_tasking` is a label on the
`replan` path, not a cheaper one. **The scale of the response is not
derived from the scale of the finding.**

Why it is not simply "make amendments skip the stamp": the re-stamp is
what made trigger (c) fire on the fourth attempt, which is the counter
doing its job (see §10's evidence). A design that lets amendments bypass
the stamp re-opens exactly the blind spot `halt-loop-unbounded` closed.
The wanted thing is a **cheap but still-counted** route — plausibly: the
counter counts cycles rather than stamps, so a stamp stops being the only
observable unit of cost.

**Not queued by the close** — same reason as §10. Candidate for the next
`/dcs-esg`, and it pairs naturally with §10 as one "cost of the process"
agenda item.

## 12. The deployed-version marker is blind to a same-version ship ✅ DONE

> **Closed 2026-07-27 by incident `deploy-marker-blind`** (Type 1,
> integration commit `916bebc`). **Candidate fix (2) was chosen** — the
> permanent content gate — and **not** fix (1), the installer-written hash
> marker. Both chiefs recommended (2) independently, and the reasoning was
> sharper than "less invasive": an aggregate hash **cannot produce the
> per-file report** the criterion required, so (1) is (2) *plus* installer
> edits *plus* a redundant marker; and a marker the installer writes
> attests to what it **believes it copied**, not to what is on disk. Fix
> (3), a mandatory bump every deploy, stayed rejected on this item's own
> merits.
>
> Delivered: `tests/payload_check.py` (the witness, payload set derived by
> walking, exits 0/1/3/2); `deploy.md` steps 4 and 7 shape-aware with step
> 7 the single source of every disposition; integrity checks 15 and 16
> (suite 73 → 82); `CLAUDE.md`'s Deploy table restated. Both installers
> untouched, so `install.*` never entered territory.
>
> **What this item asked for and did NOT get — recorded rather than
> quietly dropped:** a mechanism holding *disposition content*. Three
> attempts were defeated in succession — **vocabulary, then token, then
> markup** — and the Owner ruled the guard's claim be narrowed to what it
> demonstrably enforces. Carried forward as `check-15-role-coverage`.
>
> Cost: 1 period, 2 stamped attempts, **5 Safety Officer spawns, 4 halts**
> (three of them one class), three escalations. Full account in
> `.dcs/incidents/2026-07-27-deploy-marker-blind/AAR.md`.

### As originally filed

**Found by running the deploy train, 2026-07-26**, shipping
`schemas-md-trim`. Not a hypothesis — it happened, and it broke two separate
steps of `deploy.md` in the same run.

`deploy.md` uses `~/.claude/dcs/VERSION` as the deployed-version marker in
two load-bearing places: step 4 reconciles every `MERGED` row against it to
avoid re-shipping what is already live, and step 7 refuses to mark anything
`DEPLOYED` unless the marker **advanced**. Both assume the marker changes
when the payload does.

It does not. `schemas-md-trim` deliberately did not bump the version — 0.6.9
was unmerged and unpublished, so it was nobody's contract, and the incident's
own criterion 10 permitted skipping the bump. The marker therefore read
**0.6.9 before the deploy and 0.6.9 after**, while the payload genuinely
changed: installed `schemas.md` went 15,613 → 13,296 B and the installed hot
path 38,878 → 36,561 B.

Both failure directions are real and neither is loud:

- **Step 4 says "already live" for something unshipped.** The reconciliation
  would have excluded this row from the train and quietly recorded it as
  shipped out-of-band. Nothing would have deployed, and the register would
  have claimed it did.
- **Step 7 can never pass.** Its stop condition fires on a correct ship,
  which trains whoever hits it to override the check — the exact erosion
  `halt-loop-unbounded` documented for prose safeguards.

**A stronger witness already exists and was used here** with the Owner's
explicit authorisation: a byte-for-byte sha256 comparison of every payload
file against the repo (31 files, all matching after the run). That is a
direct check on reality, which is what step 7 was reaching for when it said
"do not report success because the deploy command exited 0". Regenerate:

```bash
python -c "import hashlib,pathlib; h=pathlib.Path.home()/'.claude'/'dcs'; r=pathlib.Path('dcs'); print([str(f) for f in r.rglob('*') if f.is_file() and '__pycache__' not in f.parts and (not (h/f.relative_to(r)).exists() or hashlib.sha256(f.read_bytes()).hexdigest()!=hashlib.sha256((h/f.relative_to(r)).read_bytes()).hexdigest())] or 'byte-identical')"
```

Candidate fixes, in rough order of how much they change:

1. **Make the payload hash the marker.** `install.ps1` writes a
   `~/.claude/dcs/.deployed` containing a hash of the payload it just wrote;
   step 4 and step 7 compare against that instead of a version string.
   Advances on every real change, same-version or not.
2. **Keep the version marker but add the content check as a second gate** —
   cheaper, and it is exactly what this run did by hand.
3. **Require a bump for every deploy** — rejected here on the merits: it
   would spend a version number on a docs-and-size change to an unpublished
   release, and DCS explicitly permits skipping the bump in that case.

Adjacent, and worth deciding together: `deploy.md` step 4's ancestry check
(`git merge-base --is-ancestor <merge> <deployed sha>`) presumes the marker
is a **sha**. Here it is a version string, so that check has never been
runnable in this repo and both deploys to date said so and skipped it.

**Not queued** — putting a row in the register is an ESG act, not a
deploy-train side effect. Candidate for the next `/dcs-esg`, and it belongs
next to §10 and §11 as a third "the mechanism does not measure what it
claims" item.

## 13. An acceptance criterion may rest on a fact nobody is required to measure

**CLOSED by incident `criterion-unmeasured-fact`, merged 2026-07-28
(`35c3507`):** candidate fix (1) landed as `plan.md` lint 4a check 3b
("Claims about state outside the tree must be measured"), plus the
MEASURED CLAIM authoring block in the 202 template and a volatility-
classification step in the Planning Chief's charter. Candidate (2)
deliberately not taken — the step-7 pre-stamp zone is left to
`revision-preservation-map` (register rank 5); candidate (3) remains open
as its own potential row. Register row `criterion-unmeasured-fact` is
`MERGED (deploy pending)`.

**Cost 2026-07-26: a version published twice with different contents, and a
0.6.10 spent to correct it.** Not a near miss — it shipped.

`schemas-md-trim`'s criterion 10 read, in substance, *"no version bump: 0.6.9
is unpublished."* That is a claim about **external, volatile state** — the npm
registry — and it was false when it was written. Timeline, local +1100:

| time | event |
|---|---|
| 11:57 | `npm view dcs-command-system version` → `0.6.7`. **Correct at that moment** |
| **14:33:16** | **Owner publishes 0.6.9** |
| 15:35 | 202 written, criterion 10 waives the bump on "0.6.9 unpublished" |
| 15:48 | tasking lint runs, **including lint 3a — which executes commands and records their output** |
| 15:59 | IC accepts at command point 2, having verified other figures against the tree |
| 16:03 | Owner approves the IAP |

**Four checkpoints after publication, and one command at any of them would
have caught it.** The 11:57 reading was cited three times — in the 201, in
the AAR, and in a deploy sitrep — and **every citation was honestly labelled
with its basis** ("measured during the previous incident's deploy"). The
labelling worked exactly as §2 intends: no reader was deceived about where
the number came from. It simply does not follow that the number was still
true, and nothing in the process asked.

**The diagnosis is not "re-measure later".** The gap is not between plan time
and stamp time — 105 minutes separated the publish from the stamp, but the
lint sat in the middle of that window and ran commands. The gap is that
**the fact was never classified as measurable at all.** It read as prose
inside a criterion, so no step owned running anything.

That is what makes this distinct from Meta §10 (a count done by ambiguous
grep) and Meta §11 (a historical measurement recomputed instead of
labelled) — `vault/Meta/building-dcs-lessons.md` sections, not this file's
items 10/11, which are about unrelated matters (citation style fixed
2026-07-28; the same slip had propagated into the register row's prose).
Here the
measurement was never attempted, and the artefact that would normally catch
it — lint 3a — only triggers on criteria whose scope is a *population*
("all", "every", "no remaining"). Criterion 10's scope was a single external
boolean, which 3a does not recognise.

### Candidate fixes

1. **Widen lint 3a's trigger from "population" to "measured claim".** Any 202
   criterion asserting a fact about state outside the working tree — a
   registry version, a deployed marker, another repo's contents — must carry
   the command that establishes it, and the Dispatcher runs that command and
   records the output, exactly as 3a already does for sweeps. This is the
   smallest change and reuses machinery that exists and works.
2. **Mark volatile criteria and re-run at the pre-stamp checklist.** Stronger
   for facts that can change *during* planning, which is precisely what
   happened here. `plan.md` step 7 already refuses to stamp over a broken
   command chain; refusing to stamp over an unrefreshed volatile fact is the
   same shape of gate.
3. **Mechanical and partial, but free:** a guard can never reach npm, but it
   *can* check that every 202 criterion containing a figure also contains a
   regeneration command. That catches the shape of the defect without
   knowing the domain, and it pairs naturally with `schema-citation-guard`.

Worth noting which fix the evidence actually supports: (1) would have caught
this one, because the lint ran 75 minutes after the publish. (2) is the
belt-and-braces version and costs a command at every stamp.

**Related and probably one agenda item together:** §12 (the deployed-version
marker cannot witness a same-version ship) is the same failure from the other
end — there the mechanism measured the wrong thing, here it measured nothing.
Both surfaced on the same day, on the same release, and both were found by
*doing* the ship rather than by reviewing it.

**Not queued** — an ESG act. Candidate for the next `/dcs-esg`.

---

## 14. Return-form drift: a specialist can answer without answering in the schema

Two returns in one period (`schema-citation-guard`, 2026-07-26) diverged from
the shape their own charter and `schemas.md` define, and **neither was caught
by any mechanism** — both surfaced only because someone read the whole return
instead of skimming for the JSON block.

- **S2** found a real semantic divergence (check 13 matches the `schemas.md`
  token case-insensitively because it reuses `norm()`; the 202 enumerator
  matches case-sensitively) and reported it inside `evidence`. Its tasking
  said in as many words that a semantic divergence must come back as
  `status: "deviation"`. It measured the divergence to be currently empty and
  chose to narrate rather than return the shape.
- **S1-FIX1** returned no schema #4 block at all — evidence in prose, no
  `status`, no `files_touched`, no `deviation`. `execute.md` step 4 says to
  treat that as a failed spawn and re-spawn. The IC judged a re-spawn to be a
  cycle spent on an envelope over work already on disk, logged the deviation
  openly, and went to Safety instead.

**The consequence was concrete, not theoretical.** With no `files_touched`
claim, nobody had asserted the territory bound. The Safety Officer had to
establish it forensically — `find -newermt` against the tasking file's mtime,
which showed exactly three files changed after it. The territory guarantee for
that fix came from the verifier, not from the worker. That inverts who is
supposed to claim and who is supposed to check.

**Why this is its own item and not a note on the queued row.** The queued
`prompt-vs-schema-drift` row covers the *inbound* direction — a prompt naming
a field the schema does not have. This is the *outbound* direction: a return
omitting or relocating a field the schema does have. Same root (no arbiter
between two hand-written copies of one contract), opposite direction, and a
guard over the tree cannot see either — a prompt is not a file, and neither is
a return.

**Evidence:** `.dcs/incidents/2026-07-26-schema-citation-guard/214-LOG.md`
entries at 19:43:40 and 20:04:06; `SAFETY.md` advisory 6 of the second run.

**Not queued** — an ESG act, and probably one agenda item with
`prompt-vs-schema-drift`.

---

## 15. Check 13's population stops at the shipped package — and one live citation is outside it

Recorded as an **accepted boundary**, not a shortfall, so it is not
relitigated by the next reader.

Check 13 (`schema-citation-guard`, 2026-07-26) walks `*.md` and excludes
`.git`, `node_modules`, `__pycache__`, **`.dcs/`** and **`vault/`**. The
exclusions were argued at plan time and confirmed by the Owner: `.dcs/esg/` is
in `.gitignore` and absent from a fresh clone, so a guard over it would
produce different results on different clones; `.dcs/incidents/**` is tracked
but is an immutable archive; `vault/` never ships.

**But the boundary has a live inhabitant.** `vault/Backlog.md` §11 carries a
real `schemas.md` #6 citation that nothing verifies. If §6 were ever
renumbered, that line would silently point elsewhere and no suite would say so.

**A claim about this line was made twice and is false — recorded here so it
is not inherited.** The Safety Officer's advisory said the citation form
"evades even a naive grep" because a backtick splits the pattern, and the IC
repeated it in a directive. The Dispatcher tested it at close rather than
transcribing it:

| form | matches `` schemas\.md`?\s*#\s*(\d+) `` |
|---|---|
| `` `schemas.md` #6 `` (this line) | **yes**, `#6` |
| `` `references/schemas.md` #4 `` | yes, `#4` |
| `schemas.md #1` | yes, `#1` |

The optional backtick in the pattern is exactly what absorbs the closing one.
This line is outside the guard **only because `vault/` is excluded from the
walk** — not because its grammar defeats the matcher. Two verifiers asserted a
mechanism without running it, inside the incident whose subject is claims that
nobody re-measures.

**The detail worth keeping** is how it is written:

```
`schemas.md` #6 offers three dispositions
```

The backtick closes **before** the `#`, so the pattern
`` schemas\.md`?\s*#\s*(\d+) `` does match it — but only because the optional
backtick is in the right place. The adjacent uncovered populations named in
`201-BRIEF.md` (79 "principle N", 34 "`<file>.md` step N", 25 "escalation
trigger (x)") have wider grammars still, and the analyst already warned that
one grammar will not serve two of them: `agents/dcs-safety-officer.md` has no
markdown headings at all, while `dcs/workflows/deploy.md`'s steps are `## N.`
headings.

**Consequence for whoever widens the guard:** the citation *grammar* is the
hard part, not the scope. Widening the walk to `vault/` is a one-line change;
widening it to a population whose citation form was never standardised is a
different job, and it should be scoped from measurement rather than from the
assumption that today's regex generalises.

**Not queued** — evidence for the adjacent-populations work, and an accepted
boundary in the meantime.

## 16. Check 14 goes green on a declaring site that drops its citation entirely

Two facets of one carrier, both raised as Safety advisories on
`safety-halt-functional-scope` (2026-07-27) and deliberately **not** pulled
into that period — no acceptance criterion ordered them, and moving the bar
after the verdict is the thing the incident existed to stop.

**Facet (a) — silence passes.** Check 14 goes red when a declaring site
*disagrees* with the charter (wrong step number, wrong bar count, wrong default
verdict token) and when the population collapses. It does **not** go red when a
declaring site simply stops citing the charter at all. Measured by the officer:
deleting both `agents/dcs-safety-officer.md` step 6 references from
`schemas.md` still gives `73/73 passed` — that file's own named case stays
green vacuously, because there is nothing left to compare. The degeneracy guard
does not catch it either: the site is still a declaring site by the
co-occurrence predicate, so the population never empties. Direction of the fix:
a declaring site must carry **at least one** charter-step reference, or FAIL.

**Facet (b) — the `N of M` rule stops at the charter.** The bare-census check
is scoped to `agents/dcs-safety-officer.md` on purpose (a whole-tree version
false-positives), so the one remaining `[0-9]+ of [0-9]+` in the shipped
package is outside it: `grep -rnE "[0-9]+ of [0-9]+" dcs/ agents/ --include=*.md`
→ `dcs/references/doctrine-appendix.md:326`. That one is a **quotation** of the
census the incident retired, which is a legitimate reason for it to exist —
which is exactly why widening the scope needs a quotation-aware rule rather
than a wider glob. Decide it: widen to `dcs/references/` with a quotation
exclusion, or record the narrow scope as a deliberate boundary the way item 15
records check 13's.

**Language defect that belongs with the fix.** That incident's IAP verification
plan said "delete one declaring place (the charter reference in `schemas.md`
§5)" and predicted RED; the officer correctly got GREEN. The step conflated
*declaring site* (defined by token co-occurrence) with *site carrying a
reference*. Whoever writes facet (a) should settle the vocabulary, because the
two are only the same thing once (a) is implemented.

**Queued** as register row `check-14-hardening` at that incident's close.
Related but distinct: [[Backlog]] item 15 is check **13**'s population
boundary; this is check **14**'s predicate.

## 17. Check 15 holds the deploy contract's citations, not its content — and cannot reach `CLAUDE.md`

**Registered at the close of `deploy-marker-blind`, 2026-07-27**, from two
things that incident tried three times and could not make a mechanism hold.
Both are recorded as **unmet aims**, not as oversights: the Owner ruled at
the third-halt escalation that the guard's claim be narrowed to what it
demonstrably enforces, and check 15 now says exactly that.

**(a) Disposition content is not checked anywhere.** A per-class comparator
(rule B) was built and withdrawn. The reason it is not merely
under-engineered: a contradiction can **cite step 7 correctly while naming
none of its classes**, in superseded vocabulary — so a class-name
comparator cannot see it *by construction*. Measured during that incident:
on the live tree rule B matched **zero** times, because
`dcs/templates/REGISTER.md`'s declaring paragraph names none of step 7's
four class tokens. Regenerate the class map with `python
tests/test_doctrine_integrity.py` and read check 15's own PASS line.

**(b) `CLAUDE.md` is outside the predicate and cannot be brought in by
widening the token match.** `grep -n DEPLOYED CLAUDE.md` → **zero hits**:
it states dispositions entirely in exit-code vocabulary (*"exit `1` … and
exit `2` … are step 7's stop dispositions"*), which is a contract
declaration **by role** with none of the token the predicate keys on. An IC
directive held rule C tree-wide *expressly* to cover `CLAUDE.md`; that aim
is unmet, and it is defeated by the predicate rather than by the
population. A specialist widened the token match to accept a bare
`DEPLOYED`, re-checked the population, and correctly **reported non-entry
rather than bending the predicate to force it**.

**Why this is worth its own row rather than a fix-tasking.** The pattern
across that incident is the finding: **three detectors, each defeated by a
narrower surface assumption than the last — vocabulary → token → markup.**
Whoever takes this should start from that, not from patching the regex. The
honest question is whether a role-defined population is reachable by a
recognizer at all in this suite's idiom, or whether it needs a different
mechanism; answering *"no, and here is why"* in `vault/Decisions/` would be
a legitimate outcome. **Territory collision:**
`tests/test_doctrine_integrity.py`, shared with `check-14-hardening`
(rank 3), `schemas-contract-format` and `json-examples-unparsed`.

## 19. A narrow revision has no required check that it preserved every other criterion

**Registered at the close of `register-field-repair-path`, 2026-07-27.**
That incident's period 1 halted twice: once on a stale external fact
(another field measurement for item 13/`criterion-unmeasured-fact`), and
once because **fixing the first halt's `IAP.md` silently dropped a
different, already-Safety-verified criterion's answer** — not
contradicted, just omitted, because the rewrite's whole attention was on
the one criterion being fixed.

Nothing mechanical could have caught it. The plan's own protection for
already-verified work was a pinned sha256 of the *payload* files; the
dropped criterion's deliverable was IAP *prose*, `[IC]`-tagged and
`.dcs/**`, outside both the pin's pathspec and `dcs_gate.py`'s reach (the
same file family item 17 found the gate cannot police for a different
reason). The false claim that the pin covered "criteria 1-5" rode through
the rewrite, an IC self-review, and an Owner approval before a Safety
Officer's full re-read caught it.

**A second, smaller instance in the same incident's own repair**: told the
dropped text was "fully recoverable verbatim," the IC restored it and
reported a verbatim recovery. It was a faithful reconstruction, not a
literal copy — a tree-wide grep found the phrasing nowhere but the
just-written file. Same shape as the first halt: an unverified assertion
standing in for a checked fact, this time about the fix itself rather than
about the registry.

### Candidate fix

A narrow revision (one criterion rewritten, others "unchanged") should be
required to produce a **preservation map** before re-stamping: every 202
acceptance criterion, paired with the section of the revised artifact that
satisfies it. Cheap to require, and it converts "I only touched criterion
N" from a claim about intent into a checked claim about the result — the
same move item 13's candidate fix (1) makes for external facts, applied to
internal document structure instead.

**Related, same incident, worth deciding together:** this is a second,
sharper field measurement for item 11 (`deviation-path-proportionality`)
— the fix here was one paragraph, IC-authored, `.dcs/**`-only, and still
had no route cheaper than a full replan-and-reapprove cycle.

**Not queued** — an ESG act. Full account:
`.dcs/incidents/2026-07-27-register-field-repair-path/AAR.md` and
[[Meta/building-dcs-lessons]] §18.

## 18. The ~250-line workflow budget is a rule no suite enforces ✅ DONE

**Queued as register row `workflow-budget-enforcement` at rank 1, ninth
`/dcs-esg`, 2026-07-28**, on fresh measurement: `plan.md` is now 666 lines.

**CLOSED by incident `workflow-budget-enforcement`, merged into `main` at
`c73e498` (integration commit `ce8ad1a` on its own branch), 2026-07-28 —
register row reads `MERGED (deploy pending)`:** built as a check, not
retired as advice — `tests/test_doctrine_integrity.py` gained a
per-file line-count check (`WORKFLOW_BUDGET_LINES` = 250,
`WORKFLOW_GRANDFATHERED_LINES` for the four files already over budget,
pinned at zero headroom rather than a ratchet with slack — see
`vault/Meta/building-dcs-lessons.md` §24 for why zero headroom was
chosen over a ratchet). `CLAUDE.md`'s rule corrected to name the
mechanism explicitly. Trimming the four grandfathered files back toward
~250 is deliberately not part of this close — tracked as its own
follow-up row below.

**2026-07-31: 4 of 5 grandfathered files discharged by incident
`workflow-file-trim-grandfathered`** (plan.md 246, execute.md 250,
deploy.md 246, close.md 243). `new.md` (263, grandfathered at 270)
remains — the sole grandfathered file. CLAUDE.md text updated accordingly.

**Registered at the close of `deploy-marker-blind`, 2026-07-27.**
`CLAUDE.md` sets a ≤ ~250-line budget for workflow files. **Nothing checks
it** — `tests/test_doctrine_integrity.py`'s size budget covers
`doctrine.md` + `schemas.md` only, so a workflow may overrun silently.

Not theoretical: it needed an **IC ruling twice in one incident**.
`dcs/workflows/deploy.md` hit exactly 265 (the first ruling's ceiling), then
landed at exactly **275** under a pre-authorised band. Both times a
specialist compressed prose under a hard ceiling, and both times the IC had
to name the step-4 / step-7 asymmetry as a **protected** element, because
that nuance is precisely what a line squeeze deletes.

Third measurement, Safety advisory 3 on `criterion-unmeasured-fact`
(2026-07-28): `plan.md` went 403 → 422 lines (IAP-bounded at ≤ 425, held),
against the same unenforced ~250 — the officer's wording: *"a written
budget nothing measures is itself a principle-15 defect."*

Regenerate: `wc -l dcs/workflows/*.md`. Decide whether the budget becomes a
check (with a per-file ratchet like the hot path's) or is retired as
advice. **Either is defensible; the current state — a rule enforced only by
whoever remembers to measure — is the one that is not.** Territory:
`tests/test_doctrine_integrity.py` (same collision as item 17), or
`CLAUDE.md` alone if retired.

## 20. `doctrine.md` is reloaded once per phase within a single incident, not once per incident — ✅ RESOLVED, see item 24

**Resolved inside `token-economy`, 2026-07-28** — the automation-path share
was fixed for free, the hand-typed-lifecycle share closed as infeasible with
today's tools. Recorded here rather than argued twice; full account at item 24
below.

**Raised by a situation analyst on the `automation-layer-eager-reading` stem,
2026-07-28.** Objective 1 and the hot-path ratchet govern `doctrine.md`'s
*size* (currently 23,387 B, healthy, 1,205 B of slack under the 37 kB
ceiling). This item is a different axis: how often that size gets paid.
`new.md`, `plan.md`, `execute.md` and `close.md` each declare their own
`<required_reading>` `@`-include of `doctrine.md`, and there is no documented
convention for a later phase to treat it as already loaded. Summing the four
phase workflows' own `required_reading` blocks for one ordinary lifecycle
(stem → plan → execute → close, as four separate command invocations) gives
150,062 B total, of which `doctrine.md` alone contributes **23,387 × 4 =
93,548 B (62.3 %)**. Regenerate:
`wc -c dcs/references/doctrine.md dcs/references/typing.md dcs/references/schemas.md dcs/references/forms.md dcs/workflows/{new,plan,execute,close}.md`,
then sum each phase file's own named `@`-includes from its
`<required_reading>` block.

**Why this is not `esg-artifact-bloat` (rank 8) or the hot-path work under a
different name.** `esg-artifact-bloat` is about `REGISTER.md`/`STRATEGY.md`
growing without bound. The hot-path ratchet is about `doctrine.md`'s
*absolute size*, and it already has a working mechanical guard. This item is
about *re-read frequency* within a single incident's lifecycle — a
healthy-sized file, paid for repeatedly.

**Why this is not a clean cut, and is filed here rather than queued
directly.** Doctrine principle 5: *"Operational period = context window. Any
session, even after a full reset, resumes losslessly by reading the files."*
The repeated per-phase read may be load-bearing for exactly that guarantee —
a session that skips re-reading `doctrine.md` because "an earlier phase this
incident already loaded it" is a session assuming continuity that a context
reset would break. A fix here trades resilience for token savings, which is
the kind of call `CLAUDE.md`'s "without harming the system effectiveness"
framing exists to guard against, and it is sharper than a Planning Chief's
territory-partition judgment — closer to a STRATEGY-level design question
than a Type 3 fix.

**Not queued** — an ESG act, and only after weighing whether any candidate
preserves principle 5's resilience guarantee rather than quietly trading it
away. Candidate framing for that discussion: distinguish "same session,
same incident, no reset occurred" (plausibly safe to skip re-reading) from
"fresh spawn, possibly post-reset" (must re-read) — but no mechanism today
tells a workflow which case it is in, so the candidate fix may itself be
nontrivial. Related: `esg-artifact-bloat` (rank 8) is the same "read
repeatedly, at every X" shape one layer up, in the ESG's own files rather
than the hot path.

## 21. Migrate `REGISTER.md` (and other structured-enough files) to SQLite — ✅ DECIDED — declining

**Declined at the ninth `/dcs-esg`, 2026-07-28** — recorded at
[[Decisions/sqlite-migration-register]] rather than queued, so it isn't
relitigated cold. The case against below is what decided it.

**Raised by the Owner during the `token-economy` stem, 2026-07-28**, on the
reasoning that moving anything table-shaped to a real database would let
agents retrieve exactly the row they need without reading surrounding
context, which should be both simpler and cheaper. Worth recording as a
live proposal even though the Dispatcher's assessment below argues against
it — the disagreement itself is the ESG-relevant fact.

**Where the reasoning holds.** Selective retrieval instead of whole-file
reads is exactly right, and three of `token-economy`'s six items
(`automation-layer-eager-reading`, `log-read-scoping-incomplete`,
`esg-artifact-bloat`) already chase that same goal by other means. The
question is whether a database is the mechanism that gets there in this
package, not whether the goal is worth pursuing.

**Against, five separate points:**

1. **Selective reads already work on text, without a database.** `grep -n`
   for an ID, or `Read` with an offset, already returns one row without
   loading the rest of the file — this session did exactly that against
   `REGISTER.md` repeatedly. A `SELECT * WHERE id=...` returns the same
   underlying cell content (the same multi-paragraph Territory/Outcome
   prose), just delimited differently. Storage format does not shrink the
   answer; it changes how reliably a narrow query can be aimed — a real
   difference, but a smaller one than "reads unnecessary context" implies.
2. **`.dcs/incidents/**` is git-tracked and merged `--no-ff` at close —
   a database breaks under exactly that model.** `214-LOG.md` (this
   incident's own item 2) is append-only text: two worktrees each adding
   lines in disjoint time ranges merge cleanly under git's line-based
   algorithm almost every time. A binary SQLite file has no line-based
   merge — two independently-modified copies differ at the byte/page
   level almost everywhere, so the first parallel incident touching the
   same database file conflicts outright. This is not an inconvenience to
   engineer around; it is incompatible with the worktree-isolation model
   `doctrine.md`'s "Parallel operation" section describes.
3. **`REGISTER.md` itself (`.gitignore`d, single copy, courtesy-locked —
   no git-merge issue) still doesn't gain what the measurement shows is
   missing.** The 169,571 B `esg-artifact-bloat` measured is free-text
   cell content (Territory, Intake source, Outcome), not absence of
   schema — the table already has 12 well-defined columns. A `TEXT`
   column holds the same paragraph at the same length; the fix for
   unbounded prose is a content bound, independent of storage engine.
4. **The migration's own footprint is large.** Every workflow file that
   currently reads or edits `REGISTER.md` via `Read`/`Edit`/`grep`
   (`new.md`, `plan.md`, `execute.md`, `close.md`, `esg.md`, `deploy.md`,
   `status.md`, `loop.md`, `run.md` — effectively the whole package) would
   need rewriting to issue SQL instead, every touching agent charter would
   need the same, and `tests/test_doctrine_integrity.py`'s regex/glob-based
   checks would need a parallel database-aware implementation.
   `references/typing.md` names "a database schema migration" as the
   textbook Type 1 trigger — this migration is plausibly larger than the
   six items already bundled into `token-economy`.
5. **Current scale does not need indexed lookup.** The register holds on
   the order of three dozen rows across this project's entire self-hosted
   history to date. A full-text `grep` over a file this size is
   sub-second; the "databases win at scale" argument is true in general
   and not load-bearing here.

**A cheaper mechanism already exists in the package and gets most of the
stated benefit.** `DELEGATION.md` embeds one fenced `delegation-bounds`
JSON block inside an otherwise prose file — `schemas.md` itself calls it
"the only part workflows parse." Applied to `REGISTER.md`, the same pattern
(a small structured block per row, or one at the file level for
state/territory, with Notes/Outcome staying free prose under a length
bound) would give reliable, schema-checked field access without losing
git-diffability or breaking the merge model. It would also have caught, at
write time, the one concrete failure already on record: an `Edit` call
that embedded literal newlines into a table cell and silently broke the
table into stray paragraph text, with nothing to flag it mechanically
(`REGISTER.md`'s own Notes, eighth `/dcs-esg` session).

**Not queued** — an ESG-level architectural question, and the Dispatcher's
assessment above disagrees with the proposal as stated. If the Owner still
wants a database after weighing points 1–5, that is the Owner's call to
make at `/dcs-esg`, not something to decide inside an already-open
incident.

## 22. The per-attempt halt ceiling re-anchors on every re-stamp, including a mechanical IC re-stamp with no fresh Owner approval

**Measured in `deviation-path-proportionality`, 2026-07-28** (IC-requested
ESG activation at its own command point 4, trigger e). `dcs_gate.py`'s
`halt_cycles()` resets on any `IAP-APPROVED:` sentinel — by design, since
a genuine re-plan should reset the tally. But the same sentinel is also
what the new `plan.md` `## 6c.` amendment path writes on a purely
mechanical re-stamp (recording IC bookkeeping, no fresh chief spawn, no
fresh Owner approval). Measured directly: this incident ran three real
Safety halts on one objective, and its own live `--halt-count` read `0`
or `1` throughout, never approaching the ceiling of 3 — because each halt
was followed by a re-stamp before the next verification pass.

**The doctrinal backstop held regardless** — trigger (b) (second halt on
the same objective, counted log-wide across `214-LOG.md`, never reset)
and trigger (c) (cumulative `IAP-APPROVED:` count against
`esg.max_periods_before_review`) both fired correctly and both escalated
to the Owner, per [[Meta/building-dcs-lessons]] §20. So nothing shipped
unsafe. The gap is that `dcs_gate.py`'s own mechanical ceiling — the one
piece of this machinery that is gate-*enforced* rather than prose-*relied
upon* — is nearly unreachable in exactly the cycle `## 6c.` makes cheap.

**Not queued by the close** — this incident's own typing carried a
standing constraint against touching `dcs/hooks/dcs_gate.py`
(`command: typed 3`, 2026-07-28), so the fix, if one is wanted, is a
future Type 1 by `CLAUDE.md`'s own rule. Candidate shape: distinguish a
stamp that followed a fresh Owner approval from one that didn't (a
mechanical re-stamp), and have `halt_cycles()` reset only on the former —
or accept the current design on the grounds that the doctrinal triggers
are the intended backstop and the gate-level counter was only ever meant
to catch the case nobody escalates. Candidate for the next `/dcs-esg`.

## 23. A fix-tasking's validation fixtures should not be authored by the same agent that authored the fix

**Measured in `deviation-path-proportionality`, 2026-07-28** (IC-requested
ESG activation, same command point as item 22). Three consecutive
fix-taskings on one incident each closed the specific defect a Safety
halt named, and each opened or re-exposed a different one in the same
boundary — not because the fixes were careless, but because the same
agent that wrote each fix also wrote the fixture set that validated it,
so the fix's own blind spots propagated into its own test. Full account
in [[Meta/building-dcs-lessons]] §20.

**What broke the pattern, on the fourth attempt**: the IC (not the
fix-tasking specialist) pre-authored the validation fixture population —
must-admit, must-reject, and must-catch-by-execution cases, specified
before the specialist was spawned, extensible but not substitutable. It
held on the first try. One incident is not proof the mechanism
generalizes, but the contrast (three same-class recurrences under
specialist-authored fixtures, zero under IC-authored ones, in the same
incident) is a clean natural experiment.

**Candidate doctrine change**: a general rule that any fix responding to
a Safety refutation — not just this incident's amendment-path repair —
carries its acceptance fixtures from the command point that dispositions
it (the IC, via `dcs-commander`), not from the specialist executing the
fix. Costed honestly: this adds authoring work at exactly the command
point already busiest (verdict disposition), and the one data point
available is a single incident's own self-referential repair, not a
controlled comparison. **Not queued** — an ESG act, worth deciding
alongside item 22 as one "verification methodology" agenda item.

## 24. `doctrine.md`'s per-phase reread cannot be safely reduced with tools available today

**Found and closed as infeasible in `token-economy`, 2026-07-28** (Type 1,
one period, one attempt, Safety pass, zero refutations). The 201 framed
this as a token-economy item alongside five others; the Planning Chief
tested the actual mechanism this period and invoked the 202's own
pre-authorized escape hatch rather than force a fix.

**The mechanism, tested directly:** `doctrine.md` is `@`-included at the
top of every phase workflow and every automation-layer file, so a
hand-typed four-command lifecycle (stem→plan→execute→close) reads it
four times — 95,492 B of 152,064 B total required reading (62.8%),
per `token-economy`'s own 201-BRIEF.md. The fix this item wanted was:
skip the reread when the session is provably the same one that already
read it this incident, still read it in full for a fresh spawn or a
session that may be resuming after a reset.

**Why no tactic could do this safely.** Three candidates, all tested,
all fail: (a) the harness resolves `@`-includes before the model ever
sees the prompt — reading `dcs/workflows/run.md` this period returned
its `@` lines as literal, unresolved text, confirming there is no point
at which a running session could make the *inclusion itself*
conditional on anything; (b) a disk marker recording "session X read
doctrine.md at time T" proves only that *someone* read it once, never
that *this* context still holds it — a post-reset session reading the
marker and skipping the reread is precisely the failure mode; (c) a
model self-report about its own context ("I already have this loaded")
is exactly the "assume continuity" the criterion was written to forbid,
and is silently wrong across an auto-compaction, which preserves
whatever session id a hook could supply while discarding the very
context the marker claims is still there.

**Consolation finding, independently valuable and already shipped:**
the 4× reload does not occur on the `/dcs-run` automation path at all.
`run.md`'s own phase-file reads happen via the `Read` tool, which never
re-resolves a nested `@`-include — so removing `run.md`/`loop.md`'s
eager top-of-file block (this incident's item 1,
[[Backlog#1|already the first item here]]) collects this item's
automation-layer share for free, with no continuity assumption needed.
What remains unaddressed is only the hand-typed four-separate-command
lifecycle, which is the minority path.

**Reopen only if the tool surface changes** — specifically, a harness
signal that both identifies the session unambiguously and reports
whether a reset or compaction happened since a named point. DCS cannot
observe that today. Until then this is a known, evidenced gap, not a
missing effort. **Not queued** — no register row; nothing here is
actionable with tools available.

## 25. The ESG Chief-of-Staff seat has no model guidance — the one judgment-dense seat with no Safety pass behind it

**Raised by the Owner, 2026-07-29**, asking which model to run `/dcs-esg`
on and noting nothing pins one. Confirmed: doctrine's model rule covers
the **IC seat only** ("command judgment belongs to Fable"; `new.md`,
`plan.md`, `execute.md` all spawn `dcs-commander` with `model: fable`
when the session isn't Fable), while `esg.md` has no model clause at all
and `dcs/templates/STRATEGY.md` says the opposite out loud: "Chief of
Staff: main session (**any model**)". Regenerate:
`grep -in "model" dcs/workflows/esg.md` (zero hits);
`grep -n "any model" dcs/templates/STRATEGY.md`.

**Why "any model" undersells the seat.** The implicit theory — ESG
decisions belong to the Owner, so the model doesn't matter — ignores
that the Chief of Staff authors the analysis the Owner's decisions rest
on: pairwise territory-collision derivation, fold-vs-sequence arguments
(the `trivial-work-inline-lane` merge case), re-measuring deploy
witnesses rather than trusting them, drafting decline cases
([[Decisions/sqlite-migration-register]]). And unlike execution, **ESG
has no Safety Officer** — nothing adversarially verifies the CoS's
claims before they land in `REGISTER.md` and `STRATEGY.md`. At ESG the
model *is* the quality floor. Every sweep to date (sessions one through
nine) ran with Fable in the main session, so the current register
quality is evidence for that configuration, not for "any model."

### Candidate fix

A one-line advisory in `esg.md` step 1 — "the Chief of Staff seat
should run the strongest available model (Fable; Opus as fallback):
ESG has no Safety pass, so the CoS's analysis is unverified" — plus
correcting `STRATEGY.md`'s "any model" parenthetical to match. Both
files are guarded territory, so the edit needs a lifecycle, but it is
Type 5-sized.

**Deliberately a backlog line, not a register row** — the first live
application of the priority bar `decomposition-backlog-routing` just
shipped: real, evidenced, and below the bar. Fold into whichever
incident next touches `esg.md`; `esg-intake-writeback-gap` (QUEUED,
unranked) owns exactly that file and is the natural carrier.

> **Confirmed at the tenth `/dcs-esg`, 2026-07-29:** stays a backlog
> line; the carrier `esg-intake-writeback-gap` entered the ranks at 5,
> and its register row now records this fold explicitly.

## 26. The hot-path budget corridor is 6 bytes after `schemas-contract-format`

**Evidence.** `schemas-contract-format`'s Safety Officer measured the
pair at period 1's close (2026-07-29): `doctrine.md` + `schemas.md` =
37 882 normalized bytes against `HOT_PATH_BUDGET_KB = 37` → 37 888 — a
6-byte corridor. Regenerate (from repo root):

```bash
python -c "d=open('dcs/references/doctrine.md','rb').read().replace(b'\r\n',b'\n'); s=open('dcs/references/schemas.md','rb').read().replace(b'\r\n',b'\n'); print(len(d)+len(s),'of',37*1024)"
```

(the ceiling itself is `HOT_PATH_BUDGET_KB` in
`tests/test_doctrine_integrity.py` — read it there, not here, if the
ratchet has since been recomputed).

**Why it matters.** Any next edit adding more than 6 net bytes to either
hot-path file turns the budget check red at merge time, likely surprising
the incident that does it mid-close. That incident's Safety advisory 4
asked for exactly this note: plan the trim (or a deliberate ratchet
recompute, measured on the MERGE RESULT per the comment block beside the
budget check in `tests/test_doctrine_integrity.py`) at 202 time, not at
the red check.

**Not an incident.** A constraint to plan around, not a defect to fix —
the ratchet working as designed. Becomes an incident only if a rank
demands hot-path growth no honest trim can pay for.

## Follow-up registered at `token-economy`'s close, 2026-07-28

Four one-line package-text fixes surfaced as Safety advisories, none
rising to a refutation, deliberately **not** folded into the period's
integration commit (an edit to a guarded workflow file riding the merge
with no Safety pass of its own costs more auditability than any one
sentence is worth — `dcs-commander`'s own ruling at command point 4).
Queued as register row `token-economy-advisory-fixes`, unranked pending
the next `/dcs-esg`:

1. `dcs/workflows/run.md`'s new `doctrine.md` carve-out ("re-read it
   only where there is real doubt it is still in context") reintroduces
   the exact self-report judgment item 24 above was just closed for
   being unsafe. Replace with the unconditional fact that `doctrine.md`
   is `@`-included at the top, so it loads regardless.
2. `dcs/templates/204-TASKING.md`'s worked example still models
   `"-- full output"` three lines below the brevity rule it is supposed
   to demonstrate.
3. `agents/dcs-safety-officer.md`'s by-reference "unchanged" test does
   not yet distinguish a derived subject (a test result, a byte budget —
   whose *inputs* live elsewhere) from a direct one (the file itself).
   See [[Meta/building-dcs-lessons]] §21 for why this matters more than
   it looks.
4. `dcs/templates/STRATEGY.md`'s Sessions-entry cap comment enumerates
   four items under a stated 5-line cap with the fifth line unexplained,
   and its own placeholder wraps to 6 physical lines until filled in.

Full verdict text: `.dcs/incidents/2026-07-28-token-economy/SAFETY.md`.

**Merge note (principle 15):** this file was reconciled from two
independent sessions' uncommitted work landing on `vault/Backlog.md` at
the same time — `criterion-unmeasured-fact`'s close (items 19-23,
already numbered against the pre-existing 1-18) and `token-economy`'s
own close (originally drafted as item 21). Renumbered to 24 at merge
time, definitively (both sides were visible during reconciliation, so
this is not a provisional numbering like the note it replaces) — no
content from either side was dropped.

## Follow-up registered at `decomposition-backlog-routing`'s close, 2026-07-28

Three package-text findings surfaced as Safety advisories on period 1,
none rising to a refutation, deliberately **not** folded into the
period's integration commit — `dcs/workflows/new.md` closed the period
at 248/250 lines and `dcs/references/doctrine.md` + `schemas.md` at
37,735/37,888 bytes, and a same-commit fix for wording nuances would
have spent the last of either budget on prose already Safety-passed as
correct. Full verdict text and the IC's resolution of every advisory:
`.dcs/incidents/2026-07-28-decomposition-backlog-routing/SAFETY.md`.

1. **`new.md` step 4a's rewritten first bullet loses the all-`L` case.**
   The pre-incident text read "...then open **one** *of them*", where
   "them" was every defect just decomposed; the rewrite reads "...then
   open **one**", implicitly scoped to the `H`/`M` set the same bullet
   just introduced. If a stem decomposes into defects that are *all*
   `L`, no row is written and the bullet no longer names a set to open
   the incident from. Bounded in practice — a stem is normally opened
   because something in scope already warrants acting on now, and step
   4a's third bullet ("say plainly ... where they went") makes a silent
   drop Owner-visible rather than silent — but real. Candidate fix, one
   clause: "...then open **one** — the one on the critical path; where
   every defect is `L`, open the one the Owner came for and route the
   rest."
2. **"Harm is never `L`." exists in only one of the three hunks this
   incident wrote.** `new.md` carries it; the `doctrine.md` principle 4
   amendment and the `esg.md` cluster-(b) mirror both omit it, so the
   constitution — which wins on conflict in this project — is silent on
   the guard that stops a harm-causing defect being demoted below the
   bar. Risk is partly bounded on the `esg.md` side because routing
   there is an `AskUserQuestion` option, Owner-decided, not automatic.
   Candidate fix: carry the clause into principle 4's parenthetical, or
   formally accept the asymmetry as stem-only.
3. **`new.md`'s new bullet calls `H`/`M`/`L` "the register template's
   vocabulary"**, but `dcs/templates/REGISTER.md`'s own Priority
   placeholder is `{{H|M|L or rank}}` — a superset. Nothing is
   un-followable (the step mandates one of `H`/`M`/`L`, and this
   project's live register already writes both letter tiers and ranks),
   but the parenthetical slightly overstates what the referenced file
   says. Optional wording: "(`H`/`M`/`L`, the register template's letter
   tiers)".

**Also recorded, not a Backlog item — a live budget fact from the same
close, principle 15's regenerating command attached rather than a bare
number:** both files this incident enlarged are now within a few
lines/bytes of their hard ceilings. Regenerate:

```bash
python -c "from pathlib import Path;d=Path('dcs/references/doctrine.md').read_bytes().replace(b'\r\n',b'\n');s=Path('dcs/references/schemas.md').read_bytes().replace(b'\r\n',b'\n');print('hot path', len(d)+len(s), 'of', 37*1024)"
python -c "from pathlib import Path;r=Path('dcs/workflows/new.md').read_bytes().replace(b'\r\n',b'\n').replace(b'\r',b'\n');print('new.md lines', r.count(b'\n')+(0 if r.endswith(b'\n') else 1), 'of 250')"
```

At close time this read 37,735 of 37,888 B and 248 of 250 lines — treat
both files as budget-blocked for the next incident that touches them
until a trim lands (see item 7's ratchet history for the shape such a
trim takes, and the still-open `workflow-file-trim-grandfathered`
register row for the grandfathered-file half of the same problem).

## 27. ENTRY_PREFIX `*` quantifier allows empty bracket content

**Evidence.** `dcs_gate.py:106` — `ENTRY_PREFIX = r"^\[[^\]]*\]\s+"`.
The `*` quantifier on `[^\]]*` allows zero-length bracket content:
`sentinel_of('[] SAFETY-HALT:')` returns `'halt'`, contradicting
GRAMMAR_LINE's "mandatory bracketed timestamp" (line 134). Found by a
`situation-analyst` during `halt-enumeration-grammar-drift`'s stem,
2026-07-30 — verified against all 20 incident logs (zero actual entries
use empty brackets).

**Why it matters.** Latent, never exploited — no real log entry has empty
brackets. But the same class of defect as the three grammar revisions in
`halt-loop-unbounded` (prose says one thing, regex allows slightly more).
A future inline edit to `sendinel_of()` or its callers that widens the
gap between prose and implementation would have no guard catching it.

**Candidate fix.** One character: `*` → `+`. But `[^\]]+` requires at
least one bracket-content character, which is strictly correct per
GRAMMAR_LINE — the regex then matches the prose. Must also update
`GRAMMAR_LINE`'s enclosing comment (lines 91-105, ~14 lines) if the
prose statement of the boundary rule changes.

## 28. `execute.md` trigger (b) provides no anchored regex

**Evidence.** `dcs/workflows/execute.md` line 374: "Grep 214-LOG.md for
prior SAFETY-HALT: lines before deciding." Provides no anchored regex
pattern. Compare to trigger (c) at lines 88-92, which quotes GRAMMAR_LINE
verbatim. A literal `grep "SAFETY-HALT:" 214-LOG.md` would return
continuation-line quotations alongside true sentinels. Found by a
`situation-analyst` during `halt-enumeration-grammar-drift`'s stem,
2026-07-30.

**Why it matters.** A human or agent following trigger (b) literally
could miscount by including continuation-line narrative quotations as
verdicts. The same `halt-enumeration-grammar-drift` register row
documents exactly this failure in `incident_metrics.py` (unanchored
substring match over-counts). Bounded in practice because the surrounding
prose explains the grammar concept, and a careful reader would apply the
GRAMMAR_LINE rule — but the instruction as written does not give them the
command to do so.

**Candidate fix.** Replace the bare instruction with an anchored grep
command, same pattern as trigger (c) uses for IAP-APPROVED:
`grep -c -E '^\[[^]]*\]\s+SAFETY-HALT:'` — one line, no new
infrastructure needed.
