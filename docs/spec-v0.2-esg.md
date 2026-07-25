# DCS v0.2 — ESG (Emergency Support Group) strategic layer

**Status: implemented in v0.2.0** (commit `a3fb60b`, 2026-07-22; this line was flipped late — it originally gated implementation on v0.1's verification, which passed). This spec is self-contained: it assumes the v0.1 package exists at `C:\Users\4ever\.claude\dcs\` (payload), `C:\Users\4ever\.claude\agents\dcs-*.md`, `C:\Users\4ever\.claude\skills\dcs-*\SKILL.md`, per the v0.1 plan at `C:\Users\4ever\.claude\plans\bubbly-jingling-candle.md`.

## Context

v0.1 deliberately has no strategic layer — no answer to "what should we work on next," and the Owner plays two roles at once: executive (approve each IAP) and strategist (decide priorities). v0.2 adds the ICS layer above the IC — the ESG (EOC / MAC Group / Agency Executive analog): a **standing** strategic body that manages the incident portfolio, sets priorities, and issues a **Delegation of Authority** that lets the IC approve routine work on the Owner's behalf within signed bounds. The Owner is promoted, not bypassed: they chair the ESG; the main session acts as **ESG Chief of Staff** during `/dcs-esg` sessions (staff-prep work — any model, per v0.1.1's transfer-of-command doctrine) and as IC/Dispatcher during incidents (same session, two hats — "phases, not nesting" applied vertically). Note (v0.1.1): command judgment transfers to the `dcs-commander` agent (`model: fable`) when the main session isn't running Fable; ESG *decisions* are the Owner's regardless, so `/dcs-esg` needs no command-point spawns.

## Doctrine amendments (`dcs/references/doctrine.md`)

1. **Hierarchy table gains a top row** above the IC:

   | **ESG** | Standing body: Owner (chair) + main session as Chief of Staff | Fable | Sets strategy and priorities across incidents, opens/parks/kills incidents, issues and amends the Delegation of Authority, decides continue/pivot/demobilize at escalations. Does NOT plan or run incidents. |

   And the Owner row is reworded: ultimate authority, *exercised primarily through ESG sessions and the Delegation*; direct IAP approval only where the Delegation doesn't cover.

2. **New principle 12 — Govern by delegation, not by click-through.** The Owner's routine control instrument is the written Delegation of Authority, reviewed at ESG sessions. IC approvals on the Owner's behalf are always logged (214 + register), never silent.

3. **New principle 13 — Escalation triggers are mandatory.** The IC MUST file a 209 sitrep and convene the Owner (pause the incident) when ANY of: (a) scope grows beyond the approved IAP's stated blast radius; (b) the Safety Officer halts twice on the same objective; (c) the incident enters operational period N+1 where N = `esg.max_periods_before_review` (default 3); (d) a Delegation bound would be crossed. Continue / pivot / demobilize is the Owner's decision, recorded in the sitrep.

4. **Lifecycle diagram** gains the strategic loop around the P:

   ```
   ESG SESSION (standing, periodic):  sweep intake → update REGISTER → set priorities
        → amend STRATEGY / DELEGATION → open next incident(s) via /dcs-new
   INCIDENT (tactical):  stem → P-loop → close   [escalation triggers → 209 → ESG decision]
   CLOSE:  AAR → register updated → next incident per STRATEGY priority
   ```

## New project-side artifacts (created lazily by first `/dcs-esg`, templates in payload)

```
<project>/.dcs/esg/
├── STRATEGY.md      # long-term objectives + ranked priorities. Incident-centric: decides WHICH
│                    # incidents get opened and in what order — never HOW they're implemented.
├── DELEGATION.md    # versioned Delegation of Authority, Owner-signed (see below)
├── REGISTER.md      # incident portfolio: QUEUED / ACTIVE / PARKED / CLOSED table —
│                    # id, title, type, priority, intake source, opened, closed, outcome line
└── SITREPS/
    └── <incident-id>-p<period>.md   # 209-style rollups filed at escalation triggers
```

### DELEGATION.md format

Human-readable terms + a fenced `delegation-bounds` JSON block that is the machine-readable source of truth (workflows parse the JSON block, never the prose):

```markdown
# Delegation of Authority — v3 (signed 2026-07-30)
The IC may approve Type 3 IAPs on the Owner's behalf when ALL bounds hold. Outside
bounds, or for Type 1, Owner approval is required as in v0.1. Revocable at any ESG session.

```delegation-bounds
{
  "version": 3,
  "auto_approve_type3": true,
  "max_files": 6,
  "forbidden_globs": ["**/migrations.py", "**/auth/**", "**/payment*/**"],
  "forbidden_topics": ["schema migration", "payments", "auth/JWT", "deploy scripts"],
  "require_tests_green": true,
  "max_specialists": 2
}
```
```

Template default: `auto_approve_type3: false` (delegation exists but grants nothing until the Owner amends it — safe start). The v0.1 `config.json` key `auto_approve_type3` is superseded: workflows read DELEGATION.md when present, falling back to config for projects without an ESG.

## New command: `/dcs-esg` (skill `dcs-esg` + workflow `esg.md`)

Skill frontmatter mirrors v0.1 style (`allowed-tools`: Read, Write, Edit, Bash, Grep, Glob, Task, AskUserQuestion); thin body `@`-includes `$HOME/.claude/dcs/workflows/esg.md`. Workflow process:

1. **Prepare (Chief of Staff hat).** Read `.dcs/esg/*` (create from templates on first run, telling the Owner it's the founding session). Sweep intake sources: `REGISTER.md` queued rows, plus project-specific sources if the project's CLAUDE.md documents them (bread_bot: `audit_results` rows flagged `needs_fix` via the Remote Diagnostics read-only pattern; open items in `docs/open-bugs.md` and `docs/tech-debt.md`). Spawn 1–2 `dcs-situation-analyst` (read-only) for the sweep if it needs file/DB digging — never do prod writes.
2. **Draft agenda.** Present to the Owner: (a) portfolio state — active/queued/parked with ages; (b) new intake found, each with a proposed type + priority; (c) stale items to park/kill; (d) any pending 209 sitreps awaiting decision; (e) proposed Delegation amendments with rationale (e.g. "3 clean Type 3 closes this month → propose raising max_files 4→6").
3. **Decide.** One `AskUserQuestion` round per decision cluster (multiSelect where natural). The Owner may also free-text strategy edits.
4. **Record.** Update STRATEGY.md, REGISTER.md; if the Delegation changed, write a new version block into DELEGATION.md (bump `version`, date-stamp; keep prior versions in the file — it's the audit trail). Append an ESG-session entry to a `## Sessions` log at the bottom of STRATEGY.md (date, decisions, delegation version in force).
5. **Hand off.** If the Owner opened incidents: instruct running `/dcs-new <top-priority item>` (do not auto-start — one incident active at a time still holds).

## Amendments to existing v0.1 files

- **`workflows/plan.md`** — approval step becomes: if Type 3 AND `.dcs/esg/DELEGATION.md` exists AND all bounds hold (parse the `delegation-bounds` JSON; check `max_files` against the IAP partition, `forbidden_globs` against every 204 territory, `forbidden_topics` against the 201/202 text, `max_specialists` against the 204 count) → the IC approves on the Owner's behalf: write IAP-APPROVED (same hash mechanism), log `approved under Delegation v<N>` in 214-LOG.md and REGISTER.md, and *tell the Owner in one line* (visible, not silent). Any bound fails or Type 1 → Owner approval via AskUserQuestion exactly as v0.1, with the failed bound named.
- **`workflows/execute.md`** — add escalation-trigger checks (doctrine principle 13) at period boundaries and after Safety verdicts: on trigger, write `SITREPS/<id>-p<n>.md` from the 209 template, pause, put continue/pivot/demobilize to the Owner via AskUserQuestion, record the decision in the sitrep and 214.
- **`workflows/close.md`** — add: update REGISTER.md row (ACTIVE → CLOSED, one-line outcome); if STRATEGY.md exists, mention the next queued priority in the closing sitrep.
- **`workflows/new.md`** — add: if REGISTER.md exists, register the new incident (QUEUED → ACTIVE) and take priority/typing hints from it; intake may simply be "next from the register."
- **`workflows/status.md`** — add a `--campaign` variant: portfolio table from REGISTER.md + delegation version in force + pending sitreps.
- **`references/forms.md`** — add entries: STRATEGY (ESG/Owner), DELEGATION (Owner-signed, CoS-drafted), REGISTER (CoS), 209-SITREP (IC files, Owner decides).
- **`references/schemas.md`** — add the `delegation-bounds` JSON schema and the 209 sitrep structure `{incident, period, status_summary, objectives_state, safety_state, resource_spend, options: [continue|pivot|demobilize], decision, decided_by}`.
- **`doctrine.md`** — amendments listed above.
- **`dcs/templates/`** — add `STRATEGY.md`, `DELEGATION.md`, `REGISTER.md`, `209-SITREP.md` templates with `{{placeholders}}`.
- **`dcs/VERSION`** → `0.2.0`; README updated (one paragraph on the ESG layer + `/dcs-esg`).

**No changes to `dcs_gate.py` or the agents** — the gate mechanism is untouched (delegation changes *who approves*, not *what approval is*), and no new agent types are needed (Chief of Staff is a hat on the main session; analysts are reused).

## Explicit non-goals (do not build)

- No separate ESG agent hierarchy or strategic Opus staff — one command, artifacts, and the delegation are the whole layer.
- No multi-active-incident execution: REGISTER tracks a portfolio; `.dcs/ACTIVE` stays singular.
- No automated cron/scheduled ESG sessions in v0.2 (the Owner convenes; a scheduled variant can be v0.3 if wanted).
- No GSD-style roadmap machinery (requirements docs, phase dependency graphs) — STRATEGY.md stays a ranked list with rationale.

## Verification

1. Scratch project with v0.1 already initialized: `/dcs-esg` founding session creates `.dcs/esg/` with all four artifacts; second run reads them and presents a real agenda.
2. Delegation OFF (default): `/dcs-plan` on a Type 3 still asks the Owner — behavior identical to v0.1.
3. Delegation ON with tight bounds: (a) a Type 3 within bounds auto-approves, visibly logged with delegation version in 214 + REGISTER; gate opens (hash marker written correctly — `/dcs-execute` accepts it); (b) a Type 3 violating one bound (e.g. a 204 territory matching a forbidden glob) escalates to the Owner naming the failed bound; (c) Type 1 always escalates.
4. Escalation trigger: simulate a second Safety halt on the same objective → 209 sitrep file appears and the Owner is asked continue/pivot/demobilize before anything proceeds.
5. `/dcs-close` moves the register row to CLOSED; `/dcs-status --campaign` shows the portfolio.
