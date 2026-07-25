---
tags: [dcs, backlog]
updated: 2026-07-25
---

# Backlog

Known gaps, each with the evidence behind it. Items here are candidates
for `/dcs-esg` to queue as incidents — this file is *not* a register.

## 1. Hot-path regrowth — trim doctrine again

`doctrine.md` + `schemas.md` are back to **40.5 kB** from the 31.7 kB the
v0.5.0 diet achieved (see [[Metrics/incident-metrics]]). Twelve versions
of additions, each individually justified, each read on every invocation
and every command-point spawn.

The guard budget sits at 42 kB as a ratchet, so this bites soon. The
trim is mechanical: move provenance and worked examples added since
v0.5.0 into `doctrine-appendix.md`, keeping only judgment-shaping
rationale in the core. **Natural first self-hosted incident** — bounded,
verifiable by the guard, and it exercises the whole loop on a low-risk
change.

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

## 5. Version bumps still go through PowerShell

The encoding disaster in [[Meta/building-dcs-lessons]] §6 was repaired
and guarded (no-Cyrillic check, `package.json` < 8 kB), but the *process*
that caused it is unchanged: version bumps are still typed as PowerShell
read-modify-write one-liners, now merely watched by a guard.

The durable fix is a tiny `bin/dcs.js bump <version>` that edits
`dcs/VERSION` and `package.json` in Node — one command, correct
encoding, both files always in sync, no shell involved. Small, and it
removes a whole hazard class rather than detecting it.

## 6. Type 5 express lane is under-used

Six of eight incidents ran the full Type 3 loop; several sub-parts would
have qualified for the express lane (one specialist, IC verifies, no
incident directory). Worth watching whether typing is systematically
conservative — if so, the typing guide needs sharper Type 5 examples
rather than a doctrine change.
