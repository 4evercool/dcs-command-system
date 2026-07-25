<!--
201-BRIEF.md — written by the IC from dcs-situation-analyst findings, once,
at the stem (/dcs-new). Never edited after typing is confirmed except to
append a note if a later period's assessment reveals the original blast
radius was wrong (append, don't rewrite — 214-LOG.md is the append-only
one, but this file's Symptom/Evidence should stay a true record of what was
known at intake).
-->

# 201 — Incident Brief

**Incident:** doctrine-hot-path-trim
**Opened:** 2026-07-25
**Type:** 3

## Symptom

The DCS hot path — the file pair `@`-included on every workflow invocation and
every command-point spawn (`dcs/references/doctrine.md` + `dcs/references/schemas.md`)
— has regrown to within ~1.5 kB of the guard's ceiling. The v0.5.0 "doctrine diet"
cut the pair to 31.7 kB by splitting rules (core) from provenance (appendix); twelve
version bumps since have carried it back to 40.47 kB against a 42 kB ratchet enforced
by `tests/test_doctrine_integrity.py` check 7. All growth is in `doctrine.md`
(`schemas.md` is byte-identical to its post-diet state), and it is almost entirely
*inline elaboration appended to existing numbered principles* — version-tagged
parenthetical clauses and two embedded field-lesson narratives — not new rules. This
is the exact category `doctrine.md`'s own line 3 says belongs in
`doctrine-appendix.md`. Nothing is red yet; the guard is anticipatory and the next
one or two doctrine additions will trip it.

## Evidence

- **Hot path measured today: 41,444 B (40.47 kB)** — `doctrine.md` 27,010 B / 157
  lines, `schemas.md` 14,434 B / 162 lines. Regenerate:
  `wc -c dcs/references/doctrine.md dcs/references/schemas.md` from `C:\DCS`.
  *(source: analyst A, measurement angle)*
- **Budget is 42 kB (43,008 B), currently PASSING with 1,564 B of headroom.**
  `tests/test_doctrine_integrity.py:40` (`HOT_PATH_BUDGET_KB = 42`) and `:146-150`
  (`hot = getsize(doctrine.md) + getsize(schemas.md)`). The file's own comment at
  `:34-40` calls the budget "a ratchet… set just above current usage deliberately."
  Regenerate: `python tests/test_doctrine_integrity.py` — currently `12/12 passed`.
  *(source: analyst A; corroborated by analyst B)*
- **Growth is 100 % in `doctrine.md`: +9,721 B (+56.2 %) since the diet.** At the
  diet commit `d5d8106` (v0.5.0) `doctrine.md` was 17,289 B / 146 lines; at HEAD
  `75e1547` (v0.6.3) it is 27,010 B / 157 lines. `schemas.md` has had **zero**
  commits since `d5d8106` and measures 14,434 B at every sampled commit. Regenerate:
  `git -C C:/DCS log --oneline -- dcs/references/doctrine.md`, then per sha
  `git -C C:/DCS show <sha>:dcs/references/doctrine.md | wc -c`. *(source: analyst A)*
- **Per-commit growth table (12 commits, v0.5.1 → v0.6.3):** +277, +1202, +696,
  +1091, +926, +530, +1129, +758, **+1574 (v0.5.12, largest)**, +853, +681, +4.
  Same regeneration commands as above. *(source: analyst A)*
- **The weight is in one section.** `## The working principles` is 9,145 B — 33.9 %
  of `doctrine.md`. Next largest: `Transfer of command` 4,464 B, `Parallel operation`
  3,389 B. Regenerate by splitting the file on `^## ` and measuring each block.
  *(source: analyst A)*
- **The two largest single additions were elaborations, not new rules.**
  `git -C C:/DCS diff d53adc1 2fd1aea -- dcs/references/doctrine.md` (v0.5.12,
  +1,574 B) appended clauses to principles 4 and 13(c) and to the P-loop line;
  `git -C C:/DCS diff bf6fd3d 5d20443 -- …` (v0.5.2, +1,202 B) added principle 15
  whole. *(source: analyst A)*
- **Two field-lesson narratives sit in the core in violation of `doctrine.md:3`**
  ("Provenance, field lessons, and extended rationale live in doctrine-appendix.md").
  `doctrine.md:38` ("Field lesson 2026-07-24", inside *A command point is never a
  silent wait*) and `doctrine.md:120` (inside *Relationship to project-specific
  protocols*). The `:120` lesson is already substantially covered by
  `doctrine-appendix.md:91-114`; the `:38` lesson has **no** appendix counterpart
  under *Transfer of command* (`doctrine-appendix.md:29-44`), so relocating it is not
  a pure cut-paste. *(source: analyst B)*
- **The destination exists and is unconstrained.** `doctrine-appendix.md` is
  11,116 B / 186 lines, ships but is never `@`-included, and is not part of check 7.
  Six of its `##` headings mirror `doctrine.md`'s verbatim (*Why phases not nesting,
  Transfer of command, The working principles, Relationship to project-specific
  protocols, Automation layers, Parallel operation*); six core sections have no
  appendix counterpart yet. Regenerate: `grep '^## ' dcs/references/doctrine-appendix.md`.
  *(source: analyst B)*
- **Blast radius of the *references*, not the prose — the real hazard.** 17 sites
  quote a doctrine **section heading** verbatim (checked live by
  `test_doctrine_integrity.py:128-144`), across `dcs/workflows/{close,deploy,esg,execute,init,loop,new,plan}.md`,
  `skills/dcs-deploy/SKILL.md`, `dcs/references/schemas.md:102`; headings cited are
  *Parallel operation* (11×), *Transfer of command* (4×), *Relationship to
  project-specific protocols* (2×), *Automation layers* (1×). And **49 sites cite a
  principle by number** (checked by `test_doctrine_integrity.py:72-96` contiguity/
  uniqueness), including load-bearing comments in `dcs/hooks/dcs_gate.py:7,34,44,229`
  (principles 5, 8, 11), `CLAUDE.md:91`, four agent charters, four templates, both
  `docs/spec-*.md`, and 11 self-references inside `doctrine.md` itself. Regenerate:
  `grep -rnoE "principle ('?)[0-9]+[a-z]?" dcs/ agents/ skills/ tests/ CLAUDE.md docs/`
  and `grep -rnoE 'doctrine('\''s)?[,:]? *"[^"]{4,80}"' dcs/workflows agents skills dcs/references/schemas.md`.
  **A trim that moves rationale prose while preserving every heading and every
  principle number leaves all 66 sites intact; renaming or renumbering breaks them.**
  *(source: analyst B)*
- **No prior trim incident.** `d5d8106` (v0.5.0) is the only trim ever. `.dcs/incidents/`
  was empty and `.dcs/esg/` did not exist — this is the first self-hosted DCS incident
  in this repo. *(source: analyst B)*

## Reproduction path

Not a functional defect; the symptom is a measurement. It reproduces deterministically:

```
python tests/test_doctrine_integrity.py     # from C:\DCS
```

— currently `12/12 passed`, check 7 reading 40.47 kB against a 42 kB ceiling
(1,564 B of margin). Independently: `wc -c dcs/references/doctrine.md dcs/references/schemas.md`.
Nothing is red today; the guard fails only once usage exceeds budget, so the intake
is anticipatory rather than corrective.

## Blast radius (best guess at intake)

Primary (edited):

- `dcs/references/doctrine.md` — the trim itself
- `dcs/references/doctrine-appendix.md` — destination for relocated provenance
- `tests/test_doctrine_integrity.py` — **the `HOT_PATH_BUDGET_KB` constant and its
  comment only**, to re-seat the ratchet after the trim. The IC ruled this in scope
  at command point 1; any other edit to this file (check logic, the reference
  scanners) is out of territory and is a deviation.

Possibly touched (unguarded, post-close bookkeeping):

- `vault/Metrics/incident-metrics.md`, `vault/Backlog.md`

Read-only but constraining — must remain valid, must not be edited by this trim:
`dcs/references/schemas.md`, all `dcs/workflows/*.md`, `agents/dcs-*.md`,
`skills/*/SKILL.md`, `dcs/templates/*.md`, `dcs/hooks/dcs_gate.py`, `CLAUDE.md`,
`docs/spec-v0.2-esg.md`, `docs/spec-v0.3-parallel.md`.

## Prior art

Directly on point: **`vault/Backlog.md:11-23`, item 1 — "Hot-path regrowth — trim
doctrine again."** It names this symptom with matching numbers ("back to 40.5 kB from
the 31.7 kB the v0.5.0 diet achieved… twelve versions of additions, each individually
justified… the guard budget sits at 42 kB as a ratchet, so this bites soon"),
prescribes the mechanism ("move provenance and worked examples added since v0.5.0
into doctrine-appendix.md, keeping only judgment-shaping rationale in the core"), and
frames it as "the natural first self-hosted incident — bounded, verifiable by the
guard, and it exercises the whole loop on a low-risk change."

`vault/Metrics/incident-metrics.md:51-64` corroborates the trend and supplies the
pre-diet baseline (42.2 kB) that git history of the current file cannot reconstruct,
with its regeneration command (`python vault/_scripts/incident_metrics.py <root>`).

Precedent for the mechanics: commit `d5d8106`, "release(v0.5.0): the doctrine diet —
split doctrine, trim schemas, merge ceremony."

## Type + rationale

**Proposed type:** 3

**Rationale (IC — `dcs-commander`, Fable seat, command point 1):** The analysts found
a bounded prose relocation across two known files whose only real hazard — 66
heading/number reference sites — is already mechanically enforced by the merge-time
guard, matching `CLAUDE.md`'s stated convention that doctrine changes are Type 3. The
ratchet edit is **in** scope but confined to the `HOT_PATH_BUDGET_KB` constant and its
comment in `tests/test_doctrine_integrity.py`, because lowering a ratchet only tightens
enforcement and is that constant's designed maintenance, whereas the `CLAUDE.md` Type 1
clause covers the *gate* (`dcs_gate.py` and `test_dcs_gate.py`), not this guard's
constant — any edit to the guard's check logic itself is out of territory and a
deviation.

**Open questions carried forward from the IC:**

1. What value the ratchet is lowered to is a planning decision the Owner confirms at
   IAP approval — recommend post-trim size plus a deliberate margin, mirroring the
   "just above current usage" pattern at `tests/test_doctrine_integrity.py:34-40`.
2. The `doctrine.md:38` *Transfer of command* field lesson has no appendix
   counterpart, so the Planning Chief must task it as a **write-then-cut**, not a
   pure relocation — the 202's acceptance criteria should require the lesson's
   substance survives in the appendix.

**Owner confirmation:** confirmed as proposed (Type 3), 2026-07-25. The Owner
additionally directed that the ESG be founded before this incident opened; that was
done in the same session and answered the IC's `esg_activation` request.

## Intake source (for /dcs-close to route back to)

Owner chat report via `/dcs-run` ("trim the doctrine hot path back toward the
post-diet size"), which restates `vault/Backlog.md` item 1. Register row:
`doctrine-hot-path-trim`.
