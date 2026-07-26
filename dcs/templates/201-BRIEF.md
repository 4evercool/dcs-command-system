<!--
201-BRIEF.md — written by the IC from dcs-situation-analyst findings, once,
at the stem (/dcs-new). Never edited after typing is confirmed except to
append a note if a later period's assessment reveals the original blast
radius was wrong (append, don't rewrite — 214-LOG.md is the append-only
one, but this file's Symptom/Evidence should stay a true record of what was
known at intake).
-->

# 201 — Incident Brief

**Incident:** {{slug}}
**Opened:** {{date}} ({{operational_period timezone if relevant}})
**Type:** {{5 | 3 | 1}}

## Symptom

<!-- One paragraph. What is observed, from whose perspective (user? owner?
     a failing test? an audit finding row?). Not the root cause -- that's
     what the analysts and later the Planning Chief dig into. -->

{{symptom}}

## Evidence

<!-- One bullet per analyst finding, each citing its source. Pull directly
     from the dcs-situation-analyst structured returns (schemas.md #1,
     situation-analyst findings) -- do not paraphrase away the citation. -->

- {{evidence item 1 -- source: action_log / codegraph / grep / test run / vault}}
- {{evidence item 2}}

## Reproduction path

{{repro_path, or "not reproducible: <why>"}}

## Blast radius (best guess at intake)

<!-- Files/subsystems believed affected. The Planning Chief will refine
     this into an actual territory partition during /dcs-plan -- this is
     a starting hypothesis, not a commitment. -->

{{affected_files list}}

## Prior art

{{what project memory (vault, tasks/lessons.md, prior incident) says about this, or "none found"}}

## Type + rationale

**Proposed type:** {{5 | 3 | 1}}
**Rationale:** {{why this type, per references/typing.md's triggers and examples}}
**Owner confirmation:** {{confirmed as proposed | overridden to Type N: <owner's reason>}}

## Intake source (for /dcs-close to route back to)

{{e.g. "Owner chat report", "audit_results row id=482, needs_fix", "GitHub issue #N" -- or "none, ad hoc"}}
