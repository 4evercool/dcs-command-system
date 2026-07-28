---
tags: [dcs, vault, navigation]
updated: 2026-07-27
---

# DCS vault — maintainer's knowledge base

Open this folder as an Obsidian vault. It holds what a **maintainer of
DCS** needs and a **user of DCS** does not — so it is deliberately
*outside* the shipped package.

## The split (read this before adding anything)

DCS already has a memory system. A second one that overlaps it would rot,
which is the failure this vault exists to avoid rather than cause:

| Where | What lives there | Ships to users? |
|---|---|---|
| `dcs/references/doctrine.md` | **The rules.** Normative core, read on every invocation. | yes — hot path |
| `dcs/references/doctrine-appendix.md` | **Provenance of the rules.** Why a rule exists, the field lesson behind it. | yes, never `@`-included |
| `docs/` | Specs and runbooks for a version (v0.2 ESG, v0.3 parallel, publishing). | yes |
| **`vault/` (here)** | Cross-incident analysis, metrics over time, decisions that did *not* become doctrine, meta-lessons about building DCS, the improvement backlog. | **no** |

**Rule of thumb:** if it changes how DCS *behaves*, it belongs in
doctrine and ships. If it explains how we *learned* something, or would
only ever be read while improving DCS itself, it belongs here.

## Map

- [[Post-mortems/energy-cost-model-rework|Post-mortem: energy-cost-model-rework]] — the 31-hour incident that produced v0.5.12
- [[Metrics/incident-metrics|Incident metrics]] — comparative numbers across every incident, with the command that regenerates them
- [[Meta/building-dcs-lessons|Meta: lessons about building DCS]] — the patterns that keep recurring in the *construction*, not the doctrine
- [[Decisions/distribution-and-scheduling|Decision: distribution and scheduling]] — choices deliberately kept out of doctrine
- [[Decisions/fable-review-roadmap|Decision: reform roadmap from the third-party review]] — the 2026-07-27 phase plan (proportionality lanes, structured register, deviation route), recovered from the cleared session
- [[Backlog]] — known gaps, with evidence

## Conventions

- **Write the derivation, not the result** (doctrine principle 15). Any
  number here carries the command that regenerates it; a bare figure is
  stale the moment the tree moves.
- Cross-incident claims cite the incident and the artifact, not memory.
- Notes are linked with `[[wikilinks]]` so the graph view is navigable.
- Nothing here is `@`-included by a workflow — this vault costs zero
  runtime latency, which is why it can afford to be discursive.
