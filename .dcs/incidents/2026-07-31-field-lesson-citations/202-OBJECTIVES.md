# 202 — Objectives (Operational Period 1)

**Incident:** field-lesson-citations
**Period:** 1

## Goal

Every shipped field lesson is verifiable in one lookup: a reader can identify the originating incident (and ideally the artifact) from the citation itself. The package's own conventions — not institutional memory — carry the provenance.

## Acceptance criteria (the Definition of Done)

1. **Population census.** `grep -rni '[Ff]ield lesson' dcs/references/doctrine-appendix.md dcs/workflows/deploy.md dcs/workflows/new.md dcs/workflows/close.md dcs/templates/202-OBJECTIVES.md dcs/templates/REGISTER.md` (run at period start, output in 214-LOG.md) establishes the current population of field lesson mentions.
2. **Every appendix field lesson names its incident.** The same command against `doctrine-appendix.md` returns zero lines where a field lesson claim lacks an incident slug — every "field lesson <date>" or "field lesson <version>" paragraph names the incident that produced it.
3. **Every workflow field lesson names its incident.** The same command against `deploy.md`, `new.md`, `close.md` returns zero lines where a field lesson mention lacks an incident slug.
4. **Every template field lesson names its incident.** The same command against `202-OBJECTIVES.md`, `REGISTER.md` returns zero lines where a field lesson mention lacks an incident slug.
5. **The convention is documented.** `doctrine-appendix.md` states, in at least one sentence, that field lessons must carry an originating incident identifier — so a future author reading the appendix learns the rule from the same file that carries the examples.
6. **Pre-self-hosting lessons are accounted for.** Field lessons whose date predates the earliest `.dcs/incidents/` entry (2026-07-25) carry the best available identifier (version + date, or an explicit "predates self-hosting" note) rather than being left blank — `grep -n '[Ff]ield lesson' dcs/references/doctrine-appendix.md` returns zero lines where a field lesson has neither an incident slug nor a "predates self-hosting" marker.
7. [IC] `tests/test_doctrine_integrity.py` gains a mechanical check: field lesson mentions without an incident-identifier pattern are flagged. Scope of the check (regex format, whether it covers only appendix or also workflows/templates) is the Planning Chief's call — the criterion is satisfied if a check exists and `python tests/test_doctrine_integrity.py` exits 0 with it passing.

## Out of scope this period

- Retroactively reconstructing incident slugs for pre-self-hosting field lessons that cannot be identified from version/date alone — the "best available identifier" in criterion 6 is a best effort, not a research project.
- Adding field-lesson verification to the Safety Officer charter — backlog item 2's option B. Criterion 7 makes verification mechanical, which is the direction the backlog leaned toward.

## Chief feedback (filled in after /dcs-plan spawns the Planning Chief)

{{objectives_feedback from the chief-plan schema}}
