# DCS Forms — What Each File Is, Who Writes It

Every ICS-numbered file has exactly one writer per doctrine principle 9's
sibling rule: one artifact, one authority, no ambiguity about who's allowed
to edit it. "IC-transcribed" means a subagent's structured JSON return
becomes this file's content, but the IC does the actual writing — subagents
never write directly into the incident directory.

| File | Author | Written during | Contains |
|---|---|---|---|
| `201-BRIEF.md` | IC, from situation-analyst findings | Stem (`/dcs-new`) | Symptom, evidence (action-log/codegraph/prior-art findings per the analyst-findings schema), blast radius, TYPE + rationale |
| `202-OBJECTIVES.md` | IC + Owner | Start of each operational period (`/dcs-plan`) | Goal (outcome-shaped, not task-shaped) + measurable acceptance criteria — this is the incident's Definition of Done |
| `203-ORG.md` | IC | `/dcs-plan`, after chief(s) return | Which positions are activated this period (Planning Chief only? + Logistics Chief? how many specialists?). **Type 1:** always written. **Type 3 (v0.5):** written only if activation differs from the default (Logistics Chief activated, specialist count ≠ 204 tasking count, or non-parallel execution mode) — otherwise skipped, noted in `214-LOG.md`, since the IAP's partition table already carries the default-case information |
| `204-TASKING/S1.md`, `S2.md`, ... | Chief-authored, IC-transcribed | `/dcs-plan` | One file per specialist: task, file territory, forbidden zones, evidence required — transcribed verbatim from the chief-plan schema's `taskings[]` |
| `IAP.md` | IC | `/dcs-plan`, integration step | Links 202+203+204, the partition table, risks, verification plan (+ logistics-chief's deploy/rollback plan for Type 1) |
| `IAP-APPROVED` | IC, on Owner approval | `/dcs-plan`, after AskUserQuestion approval | sha256 of `IAP.md` at the moment of approval, plus approver/timestamp metadata. First line is always the bare hex hash — the gate hook only reads that line |
| `214-LOG.md` | IC, append-only | Every phase transition, every workflow | The shift-change record — never edited or rewritten, only appended to. This is what a fresh session reads to resume losslessly |
| `SAFETY.md` | Safety Officer, verbatim | `/dcs-execute`, after specialists finish | The Safety Officer's verdict per operational period, copied in as returned — not summarized or softened by the IC |
| `AAR.md` | IC | `/dcs-close` | Close-out: what worked, lessons learned, links to where those lessons were written in the project's memory system |
| `.dcs/esg/STRATEGY.md` | ESG (Owner decides, Chief of Staff drafts) | `/dcs-esg` | Long-term objectives + ranked priorities — incident-centric, decides WHICH incidents get opened, never HOW |
| `.dcs/esg/DELEGATION.md` | Owner-signed, Chief of Staff-drafted | `/dcs-esg` | Versioned Delegation of Authority — human-readable terms plus the machine-readable `delegation-bounds` JSON block workflows actually parse |
| `.dcs/esg/REGISTER.md` | Chief of Staff (CoS) | `/dcs-esg`, and touched by `/dcs-new`, `/dcs-plan`, `/dcs-close`, `/dcs-deploy` | Incident portfolio: QUEUED / ACTIVE / MERGED / DEPLOYED / PARKED / KILLED table, plus (v0.3) worktree/branch/territory columns — lives in the main checkout only (`esg_root`) |
| `.dcs/esg/SITREPS/<slug>-p<N>.md` | IC files it, Owner decides | `/dcs-execute`, at any escalation trigger | 209-style rollup: status, objectives/safety state, resource spend, continue/pivot/demobilize decision |

## Why append-only for 214-LOG.md

The log is the only artifact that must never be "corrected" — if a phase
transition happened, it happened, even if it later turns out to have been
premature (e.g. an IAP approved and then voided by a deviation). Deleting
or editing a past entry to make the incident's history look cleaner defeats
its purpose: a future session (or a human auditing what went wrong) needs
the honest sequence, not a tidied one. Log entry format:

```
[2026-07-22T14:03:00+11:00] phase: planning -> execution (IAP approved, hash=3f2a...)
[2026-07-22T15:41:00+11:00] deviation reported by S1 -- returning to planning
[2026-07-22T16:10:00+11:00] phase: planning -> execution (IAP re-approved, hash=9b7c...)
[2026-07-22T17:22:00+11:00] SAFETY: pass -- period 2 complete
[2026-07-22T17:25:00+11:00] incident closed, archived
```

## Why 204 is chief-authored but IC-transcribed

The Planning Chief returns taskings as structured JSON (the chief-plan
schema) in its response — it does not have Write access to the incident
directory (see `agents/dcs-planning-chief.md` tools list: read-only +
codegraph). The IC is the one file-system-writing party for planning
artifacts; this keeps a single point of truth for what the specialists
actually receive, and lets the IC catch a malformed or partition-less
return before it ever touches disk.
