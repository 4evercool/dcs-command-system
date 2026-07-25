---
tags: [dcs, backlog]
updated: 2026-07-25
---

# Backlog

Known gaps, each with the evidence behind it. Items here are candidates
for `/dcs-esg` to queue as incidents — this file is *not* a register.

## 1. Hot-path regrowth — trim doctrine again ✅ DONE (partially)

**Closed 2026-07-25** by incident `doctrine-hot-path-trim`, integration
commit `de50257`, shipped in v0.6.5. It was indeed the natural first
self-hosted incident, and it exercised the whole loop rather thoroughly:
one specialist spawn that hit its target first time, **two Safety halts**,
an escalation trigger (b) with a convergence read, and an Owner
"raise the altitude" ruling — none of it against the trim, all of it
against the bookkeeping that recorded it. See [[Meta/building-dcs-lessons]] §7.

Hot path 41,444 → **36,717 B**; ratchet re-seated 42 → 37 kB.

**Partially** because the post-diet equivalent is ~32,031 B, so about half
the regrowth remains — see item 6. That was a deliberate call at close: the
Owner-approved acceptance bar was 36,864 B and it was met; further trimming
needs its own incident with its own criteria.

## 6. The other half of the hot-path regrowth

`doctrine-hot-path-trim` recovered 41,444 → 36,717 B against a post-diet
equivalent of ~32,031 B (regenerate both via [[Metrics/incident-metrics]]).
The remaining ~4.7 kB is a harder cut than the first: item 1 took the
provenance that was obviously provenance, and what is left is more
entangled with the rules.

Two specific candidates the closing IC named:

- `schemas.md` is 14,596 B — 35 % of the hot path — and has not been
  touched since the v0.5.0 diet trimmed it. It was explicitly out of scope
  for item 1 and has never been re-examined.
- A ratchet re-seat to 36 kB after a period of stability, which would also
  narrow the guard-blind band described in item 7.

## 7. Hot-path budget check is line-ending-sensitive

`core.autocrlf=true` with no `.gitattributes`, and
`tests/test_doctrine_integrity.py` check 7 reads raw `os.path.getsize`. So
a fresh worktree checks out CRLF while a long-lived main checkout may hold
LF, and the *same commit* measures differently in the two trees. Measured
2026-07-25 at `51dd073`: main 41,444 B, fresh worktree 41,763 B — a 319 B
spread against a 43,008 B ceiling.

Regenerate: `wc -c dcs/references/doctrine.md dcs/references/schemas.md`
in each tree.

Candidate remedies: a `.gitattributes` normalising these files, or
normalising line endings inside the check itself. Registered as
`hot-path-budget-eol-sensitivity`.

**Related, and worth fixing in the same pass:** the guard's bar is coarser
than an incident's acceptance bar can be. After item 1, criterion 1 sat at
36,864 B but the guard does not turn red until 37,888 B — so there is a
band in which the incident's own target is breached and nothing complains.
Inherent to a kB-granularity ratchet; the question is whether the guard
should take bytes rather than kB.

## 8. `package.json` ships a 2.9 M-character corrupted description

`package.json` is **6,322,630 B** because its `description` field holds
~2,942,431 characters of mojibake. Pre-existing at `51dd073`, so introduced
by neither DCS incident nor tooling under DCS's control. Found by an Ops
Specialist during item 1, from inside its own territory, and correctly left
untouched and flagged.

Regenerate:

```bash
wc -c package.json
python -c "import json; print(len(json.load(open('package.json',encoding='utf-8'))['description']))"
```

**Priority H — this is the npm release surface**, and `npm publish` would
ship it. Note `install.ps1` never references `package.json`, so the local
deploy path is unaffected; this gates the registry release only.

Worth carrying into the fix: the guard's encoding check (no BOM, no U+FFFD)
**passes** on this file, because the mojibake is well-formed UTF-8 —
Cyrillic and Latin sequences, not replacement characters. The existing
check cannot detect this class.

Registered as `package-json-description-corruption`.

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

## 3. The register has no cross-project view

Each project's register is its own portfolio (correct — see
`plan.md` lint 8). But an Owner running DCS in several repos has no
single place showing what is in flight everywhere. `/dcs-status
--campaign` is per-project by design.

Not obviously worth solving; noted so it is a decision rather than an
oversight.

## 4. Intake nudge has no telemetry

`dcs_intake.py` fires once per session, but nothing records whether the
offer was accepted, declined, or ignored. Without that, there is no
evidence for tuning it — and tuning by impression is what principle 15
warns about. A single line appended to a local (gitignored) log would be
enough.

## 5. Type 5 express lane is under-used

Six of eight incidents ran the full Type 3 loop; several sub-parts would
have qualified for the express lane (one specialist, IC verifies, no
incident directory). Worth watching whether typing is systematically
conservative — if so, the typing guide needs sharper Type 5 examples
rather than a doctrine change.
