# DCS Structured Return Schemas

Fixed JSON return schema closes the "I did the task" gap. Agents return the JSON block; the IC alone transcribes it (single writer per artifact) — provenance in `doctrine-appendix.md`.

## 1. Situation-analyst findings (feeds 201-BRIEF.md)

Returned by `dcs-situation-analyst`.

```json
{"summary": "One paragraph: what the incident is and why it matters", "evidence": ["log row: category=error, actor_id=123, ts=2026-07-22T03:14Z", "call graph: get_blocking_ingredients has 3 callers, none touch delivery_date"], "affected_files": ["src/db/inventory_repo.py", "src/plugins/reminder_plugin.py"], "repro_path": "1. Create order for tomorrow 2. Run get_blocking_ingredients 3. Order flagged stuck", "prior_art": "docs/pitfalls.md #12 — same symptom, different cause"}
```

| Field | Type | Notes |
|---|---|---|
| `summary` | string | One paragraph, no hedging — feeds 201's Symptom section |
| `evidence` | string[] | Each item cites its source (log/codegraph query, grep, test run) — no unsourced claims |
| `affected_files` | string[] | Best-guess blast radius the Planning Chief refines, not blindly trusts |
| `repro_path` | string | Numbered steps, or `"not reproducible: <why>"` |
| `prior_art` | string | Reference to project memory (vault, tasks/lessons.md, prior incident) or `"none found"` |

## 2. Chief plan (feeds 203-ORG.md, 204-TASKING/\*.md, IAP.md)

Returned by `dcs-planning-chief` (and, for deploy/env/migration only, `dcs-logistics-chief` — see #3). Contract producer: `dcs-planning-chief`.

```json
{"objectives_feedback": "202's criteria are testable as written; no changes requested", "tactics": ["Add a delivery_date window check to get_blocking_ingredients' transaction", "Update the reminder plugin's stale-order heuristic for it"], "taskings": [{"id": "S1", "task": "Add delivery_date window to get_blocking_ingredients per criterion 1", "territory": ["src/db/inventory_repo.py"], "forbidden": ["src/plugins/**"], "evidence_required": ["pytest tests/test_inventory_repo.py -x"]}, {"id": "S2", "task": "Stop flagging future-dated orders as stale per criterion 2", "territory": ["src/plugins/reminder_plugin.py"], "forbidden": ["src/db/**"], "evidence_required": ["pytest tests/test_reminder_plugin.py -x"]}], "partition_ok": true, "risks": ["Both import db/connection.py — read-only, no write conflict"], "verification_plan": "Run both test files, then repro 201's path against a scratch order"}
```

| Field | Type | Notes |
|---|---|---|
| `objectives_feedback` | string | Chief may push back on unmeasurable/untestable criteria — IC decides on 202's revision |
| `tactics` | string[] | The "how", one level above individual taskings |
| `taskings` | object[] | See tasking table below — becomes 204-TASKING/\*.md, one file per entry |
| `partition_ok` | boolean | `true` only if every `territory` is disjoint; `false` must be justified in `risks` (staging or worktree isolation), else IC re-spawns |
| `risks` | string[] | Partition or ordering risk — anything threatening the "disjoint files, parallel execution" assumption |
| `verification_plan` | string | Feeds the Safety Officer's brief — what "done" looks like end to end |

**Tasking object** (each entry in `taskings`):

| Field | Type | Notes |
|---|---|---|
| `id` | string | `S1`, `S2`, ... — matches the 204 filename (`204-TASKING/S1.md`) |
| `task` | string | Specific, references a 202 criterion by number |
| `territory` | string[] | Glob(s) this specialist may edit; disjoint from every other tasking's territory unless staged sequentially |
| `forbidden` | string[] | Explicit "do not touch" globs — usually the other specialists' territories |
| `evidence_required` | string[] | Concrete command(s) to run, reporting real output — cite decisive excerpt, never full transcript |

## 3. Logistics-chief plan (Type 1 only — feeds IAP.md's deploy section)

Returned by `dcs-logistics-chief`.

```json
{"deploy_path": "deploy/deploy.sh (full deploy — migration touches backend and frontend)", "env_deps": ["No new env vars", "requirements.txt: add alembic==1.13.1"], "migration_ordering": "Run the schema migration before restarting the api service", "rollback_plan": "Migration is additive (new nullable column) — rollback is the prior commit, no down-migration needed", "risks": ["low-memory host — avoid frontend build and migration running concurrently"]}
```

| Field | Type | Notes |
|---|---|---|
| `deploy_path` | string | Full or scoped target |
| `env_deps` | string[] | Env vars, deps, config |
| `migration_ordering` | string | Restart ordering, or none |
| `rollback_plan` | string | Stated even if none needed |
| `risks` | string[] | What could turn deploy into its own incident |

## 4. Ops-specialist return (feeds 214-LOG.md, informs SAFETY.md)

Returned by `dcs-ops-specialist`.

```json
{"status": "done", "files_touched": ["src/db/inventory_repo.py"], "tests_run": ["pytest tests/test_inventory_repo.py -x"], "evidence": "5 passed in 1.2s (output below)", "deviation": null}
```

Deviation shape (`status: "deviation"`), needing the nested `deviation` object below:

```json
{"status": "deviation", "files_touched": [], "tests_run": [], "evidence": "get_blocking_ingredients has no single transaction for the check", "deviation": {"found": "Function not atomic — three separate db_connection() calls, a TOCTOU bug unanticipated", "why_plan_wrong": "202/204 assumed db_transaction() was already used, based on 201 evidence showing only output", "proposal": "Wrap the three calls in one db_transaction(), then add the window check — recommend as a 202 amendment"}}
```

| Field | Type | Notes |
|---|---|---|
| `status` | `"done"` \| `"blocked"` \| `"deviation"` | `blocked` = external obstacle (missing credential, flaky env); `deviation` = the plan doesn't fit reality |
| `files_touched` | string[] | A subset of the tasking's `territory` — anything outside is a violation, not evidence |
| `tests_run` | string[] | Commands actually executed, not what should run |
| `evidence` | string | Real output, not a paraphrase — the Safety Officer re-checks regardless; cite the decisive excerpt or `file:line`, never a full transcript |
| `deviation` | object \| null | Present only when `status: "deviation"`; keys `found` / `why_plan_wrong` / `proposal`. `proposal` is a recommendation, not an action the specialist takes |

## 5. Safety-officer verdict (feeds SAFETY.md)

Returned by `dcs-safety-officer`.

```json
{"verdict": "pass", "refutations": [], "advisories": [{"finding": "docstring states '16 batches violate the guard', no regenerating command", "fix": "delete the count or add the query beside it (principle 15)"}], "checked": ["git diff inventory_repo.py — window check present, matches criterion 1", "pytest tests/test_inventory_repo.py -x — 5 passed", "pytest tests/test_reminder_plugin.py -x — 8 passed", "repro of 201 path — no longer flagged"]}
```
Advisory/refutation bar: `agents/dcs-safety-officer.md` step 6.

**`pass` with advisories is the normal healthy verdict (v0.6.5)**:
advisories are fixed by the IC and never block a merge; only a `halt`'s
refutations do (bar: `agents/dcs-safety-officer.md` step 6).

Halt shape, showing the `refutations` object:

```json
{"verdict": "halt", "refutations": [{"claim": "S1 reported 'done': pytest test_inventory_repo.py -x, 5 passed", "evidence": "Re-ran it: 4 passed, 1 skipped (test_window_boundary still marked xfail) — criterion 1's boundary case is untested"}], "checked": ["git diff inventory_repo.py — window check present, matches criterion 1", "pytest test_inventory_repo.py -x (re-run) — 4 passed, 1 skipped, test_window_boundary still xfail"]}
```

| Field | Type | Notes |
|---|---|---|
| `verdict` | `"pass"` \| `"halt"` | Binding on the IC — a `halt` cannot be argued past, only resolved (fix-tasking or re-plan) |
| `refutations` | object[] | Empty on `pass`; each has `claim` (what was asserted) and `evidence` (what the Safety Officer independently found). **Reserved for the acceptance criteria and code behaviour** — the only findings that justify stopping a merge |
| `advisories` | object[], optional | (v0.6.5) Artifact-hygiene findings that don't block: `finding` + `fix`. Principle-15 issues in docstrings/comments/logs/AARs live here unless they clear one of the three bars in `agents/dcs-safety-officer.md` step 6; IC folds them into the integration commit |
| `checked` | string[] | Everything the Safety Officer actually did — diff inspected, tests re-run, manual repro, each entry a **regenerable** command whose output a later reader can re-run and compare, never a description or a one-off manual observation; specialist self-reports are the claim checked, never the check itself. Same for `refutations`/`advisories`: cite the decisive excerpt or `file:line`, never a full transcript |

## 6. Commander decisions (transfer of command — feeds 214-LOG.md)

Returned by `dcs-commander`, one decision per invocation, at the four command points doctrine's "Transfer of command" defines; if the main session runs Fable it decides directly, logged in `214-LOG.md` the same way.

```json
{"command_point": "typing", "type": 3, "rationale": "3 files, fix pattern known, no schema impact", "open_questions": []}
```

Any decision may also carry an ESG-activation request (doctrine principle 14):

```json
{"command_point": "deviation", "disposition": "escalate_owner", "rationale": "fix requires touching the payment flow", "directives": [], "esg_activation": {"requested": true, "reason": "payment flow is forbidden; spans two other items -- strategic, not tactical"}}
```

| Field | Command point | Type | Notes |
|---|---|---|---|
| `command_point` | typing, iap_review, deviation, verdict_disposition | string | Which decision this is |
| `type` | typing | number | Type 5/3/1, see `dcs-commander.md` |
| `verdict` | iap_review | string | `"accept"` or `"reject"`; `reject` needs `required_changes` |
| `disposition` | deviation, verdict_disposition | string | Enum differs per point, see `dcs-commander.md` |
| `rationale` | typing, deviation, verdict_disposition | string | One line, grounded in verified inputs |
| `reasons` | iap_review | string[] | Same grounding as `rationale` |
| `required_changes` | iap_review | string[] | One line each, verbatim re-spawn instruction |
| `directives` | deviation, verdict_disposition | string[] | One line each, verbatim re-spawn or fix-tasking |
| `open_questions` | typing | string[] | Only where the call is genuinely the Owner's |
| `esg_activation` | any | object, optional | `{requested, reason}` — rides with any decision (doctrine principle 14) |

## 7. Delegation bounds (v0.2 — feeds `.dcs/esg/DELEGATION.md`, parsed by `plan.md`/`run.md`/`loop.md`)

The fenced ```delegation-bounds``` block inside `DELEGATION.md` — the only part workflows parse; surrounding prose is for humans only.

```json
{"version": 1, "auto_approve_type3": false, "approved_models": ["fable"], "max_files": 4, "forbidden_globs": ["**/migrations.py", "**/auth/**"], "forbidden_topics": ["schema migration", "payments", "auth/JWT"], "require_tests_green": true, "max_specialists": 2, "deploy": {"auto": false, "auto_after_close": false, "frontend_only": true, "forbidden_globs": ["**/migrations.py", "**/auth/**"], "max_rows_per_train": 3}}
```

| Field | Type | Notes |
|---|---|---|
| `version` | number | Bumped every amendment; `DELEGATION.md` keeps every prior version block — this is the one currently in force |
| `auto_approve_type3` | boolean | Master switch; `false` = identical to v0.1 behavior even with a `DELEGATION.md` present |
| `approved_models` | string[] | Session operating models allowed to use this Delegation's unattended bounds (`auto_approve_type3`, `deploy.auto`, `deploy.auto_after_close`) at any site reading them; **empty or absent = no model approved** — every site falls back to full v0.1 every-gate-is-an-Owner-gate behavior (fail-closed) |
| `max_files` | number | Compared against the IAP's total partitioned file count |
| `forbidden_globs` | string[] | Any 204 tasking's `territory` glob matching one of these voids auto-approval for that IAP |
| `forbidden_topics` | string[] | Checked against the 201/202 text |
| `require_tests_green` | boolean | If `true`, the chief's `verification_plan` must name a concrete automated test run, not "manual only" |
| `max_specialists` | number | Compared against the 204 tasking count |
| `deploy` (v0.4) | object, optional | Deploy delegation keys: `auto`, `auto_after_close`, `frontend_only`, `forbidden_globs`, `max_rows_per_train`. Behavior: `deploy.md` step 5, `run.md` step 7a. |

`esg.max_periods_before_review` (principle 13, trigger c) is **not** part of this block — it lives in `config.json`'s `esg` key (default `3`), applying incident-wide regardless of Delegation.

## 8. 209 sitrep (v0.2 — feeds `.dcs/esg/SITREPS/<slug>-p<N>.md`)

Relocated to `$HOME/.claude/dcs/templates/209-SITREP.md`: its prose headings carry the
same fields, plus a trigger enum, `Decided at`, and `Notes` this section
never had. The number `8` stays reserved, keeping existing citations
pointing here.

## 9. Preservation map (6c amendment pre-stamp proof)

The JSON block a `## 6c.` amendment appends to `214-LOG.md` beside its
re-stamp, proving every 202 criterion it doesn't name still holds in the
artifact as it stands. Checked by `dcs/tools/preservation_map.py`.

```json
{"preservation_map": {"amendment_entry": "6c re-stamp, criterion 6", "amended_criteria": [6], "preserved": [{"criterion": 5, "artifact": "IAP.md", "section": "Criterion 5, answered", "anchor": "criterion 5 restored", "verified_by": "grep -n -F \"criterion 5 restored\" IAP.md", "output": "34:criterion 5 restored"}]}}
```

| Field | Type | Notes |
|---|---|---|
| `amendment_entry` | string | The triggering `## 6c.` re-stamp's log line |
| `amended_criteria` | number[] | Criteria the amendment names — excluded below |
| `preserved[]` | object[] | One entry per un-amended criterion, paired to its satisfying section |
| `criterion` | number | The criterion proved satisfied |
| `artifact` | string | `IAP.md`, `203-ORG.md`, or a `204-TASKING/*.md` |
| `section` | string | The satisfying heading or passage in `artifact` |
| `anchor` | string | Literal text present in `artifact`'s bytes — the proof itself |
| `verified_by` | string | Command confirming `anchor`'s presence |
| `output` | string | Self-reported result — the validator re-derives it from disk, never trusts it |
