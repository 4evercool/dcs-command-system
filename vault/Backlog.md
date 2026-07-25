---
tags: [dcs, backlog]
updated: 2026-07-25
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

## 2. Field-lesson citations are unverifiable

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

## 4. Intake nudge has no telemetry

`dcs_intake.py` fires once per session, but nothing records whether the
offer was accepted, declined, or ignored. Without that, there is no
evidence for tuning it — and tuning by impression is what principle 15
warns about. A single line appended to a local (gitignored) log would be
enough.

## 5. Version bumps still go through PowerShell — QUEUED

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

## 7. The other half of the hot-path regrowth — QUEUED (rank 2)

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
