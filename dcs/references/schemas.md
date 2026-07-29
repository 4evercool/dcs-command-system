# DCS Structured Return Schemas

Fixed JSON return schema closes the "I did the task" gap; provenance in `doctrine-appendix.md`.

Agents return the JSON block; the IC alone transcribes it to disk (single writer per artifact, `doctrine-appendix.md`).

## 1. Situation-analyst findings (feeds 201-BRIEF.md)

Returned by `dcs-situation-analyst`.

```json
{"summary": "One paragraph: what the incident is and why it matters", "evidence": ["error-log row: category=error, actor_id=123, ts=2026-07-22T03:14Z, traceback tail: ...", "call graph: get_blocking_ingredients has 3 callers, none touch the delivery_date window"], "affected_files": ["src/db/inventory_repo.py", "src/plugins/reminder_plugin.py"], "repro_path": "1. Create order for tomorrow  2. Run get_blocking_ingredients  3. Order flagged as stuck", "prior_art": "docs/pitfalls.md #12 — same symptom, different root cause, closed earlier"}
```

| Field | Type | Notes |
|---|---|---|
| `summary` | string | One paragraph, no hedging — feeds 201's Symptom section |
| `evidence` | string[] | Each item cites its source (log query, codegraph query, grep, test run) — no unsourced claims |
| `affected_files` | string[] | Best-guess blast radius; the Planning Chief refines it, not trusts it blindly |
| `repro_path` | string | Numbered steps, or `"not reproducible: <why>"` |
| `prior_art` | string | Reference to project memory (vault, tasks/lessons.md, prior incident) or `"none found"` |

## 2. Chief plan (feeds 203-ORG.md, 204-TASKING/\*.md, IAP.md)

Returned by `dcs-planning-chief` (and, for deploy/env/migration concerns only, `dcs-logistics-chief` — see #3). Contract producer: `dcs-planning-chief`.

```json
{"objectives_feedback": "202's acceptance criteria are testable as written; no changes requested", "tactics": ["Add a delivery_date window check inside get_blocking_ingredients' existing transaction", "Update the reminder plugin's stale-order heuristic to respect the same window"], "taskings": [{"id": "S1", "task": "Add delivery_date window to get_blocking_ingredients per 202 acceptance criterion 1", "territory": ["src/db/inventory_repo.py"], "forbidden": ["src/plugins/**"], "evidence_required": ["pytest tests/test_inventory_repo.py -x output"]}, {"id": "S2", "task": "Stop flagging future-dated orders as stale per 202 acceptance criterion 2", "territory": ["src/plugins/reminder_plugin.py"], "forbidden": ["src/db/**"], "evidence_required": ["pytest tests/test_reminder_plugin.py -x output"]}], "partition_ok": true, "risks": ["Both files import db/connection.py — read-only import, not a write conflict"], "verification_plan": "Run both test files, then a manual repro of the 201 repro_path against a scratch order"}
```

| Field | Type | Notes |
|---|---|---|
| `objectives_feedback` | string | Chief may push back on unmeasurable/untestable 202 criteria — IC decides whether to revise 202 |
| `tactics` | string[] | The "how", one level above individual taskings |
| `taskings` | object[] | See tasking table below — becomes 204-TASKING/\*.md, one file per entry |
| `partition_ok` | boolean | `true` only if every `territory` array is disjoint from every other's. `false` requires `risks` to justify sequential staging or worktree isolation — the IC rejects `false` with no justification and re-spawns |
| `risks` | string[] | Partition risk, ordering risk, anything threatening the "disjoint files, parallel execution" assumption |
| `verification_plan` | string | Feeds the Safety Officer's brief — what "done" should look like end to end |

**Tasking object** (each entry in `taskings`):

| Field | Type | Notes |
|---|---|---|
| `id` | string | `S1`, `S2`, ... — matches the 204 filename (`204-TASKING/S1.md`) |
| `task` | string | Specific, references a 202 acceptance criterion by number |
| `territory` | string[] | Glob(s) this specialist may edit — disjoint from every other tasking's territory unless staged sequentially |
| `forbidden` | string[] | Explicit "do not touch" globs — usually the other specialists' territories |
| `evidence_required` | string[] | Concrete command(s) whose real output the specialist must include in its return; cite the decisive excerpt or `file:line`, never paste a full unabridged transcript |

## 3. Logistics-chief plan (Type 1 only — feeds IAP.md's deploy section)

Returned by `dcs-logistics-chief`.

```json
{"deploy_path": "deploy/deploy.sh (full deploy — migration touches backend and frontend build)", "env_deps": ["No new env vars", "requirements.txt: add alembic==1.13.1"], "migration_ordering": "Run the schema migration before restarting the api service, not after", "rollback_plan": "Migration is additive (new nullable column) — rollback is redeploying the prior commit; no down-migration needed", "risks": ["low-memory host — avoid running the frontend build and the migration concurrently"]}
```

| Field | Type | Notes |
|---|---|---|
| `deploy_path` | string | Full or scoped target |
| `env_deps` | string[] | Env vars, dependencies, config |
| `migration_ordering` | string | Restart ordering, or none |
| `rollback_plan` | string | Stated even if none needed |
| `risks` | string[] | What could turn deploy into its own incident |

## 4. Ops-specialist return (feeds 214-LOG.md, informs SAFETY.md)

Returned by `dcs-ops-specialist`.

```json
{"status": "done", "files_touched": ["src/db/inventory_repo.py"], "tests_run": ["pytest tests/test_inventory_repo.py -x"], "evidence": "5 passed in 1.2s (full pytest output pasted below)", "deviation": null}
```

Deviation shape (`status: "deviation"`), which needs the nested `deviation` object the table below describes:

```json
{"status": "deviation", "files_touched": [], "tests_run": [], "evidence": "get_blocking_ingredients has no single transaction to add the window check into", "deviation": {"found": "The function is not atomic — it's three separate db_connection() calls, itself a TOCTOU bug the tasking didn't anticipate", "why_plan_wrong": "202/204 assumed the function already used db_transaction() based on the 201 evidence, which only showed output, not internals", "proposal": "Wrap the three calls in a single db_transaction() first, then add the window check — recommend as a 202 amendment, not a silent scope add"}}
```

| Field | Type | Notes |
|---|---|---|
| `status` | `"done"` \| `"blocked"` \| `"deviation"` | `blocked` = external obstacle (missing credential, flaky env); `deviation` = the plan itself doesn't fit reality |
| `files_touched` | string[] | Must be a subset of the tasking's `territory` — anything outside is a violation, not evidence |
| `tests_run` | string[] | Commands actually executed, not commands that should be run |
| `evidence` | string | Real output, not a paraphrase — the Safety Officer will refuse to trust and check again anyway; cite the decisive excerpt or `file:line`, never paste a full unabridged transcript |
| `deviation` | object \| null | Present only when `status: "deviation"`; keys `found` / `why_plan_wrong` / `proposal`. `proposal` is a recommendation, not an action — the specialist never improvises the fix itself |

## 5. Safety-officer verdict (feeds SAFETY.md)

Returned by `dcs-safety-officer`.

```json
{"verdict": "pass", "refutations": [], "advisories": [{"finding": "docstring of _check_batch_energy_identity states '16 batches violate the guard' with no regenerating command", "fix": "delete the count or add the query beside it (principle 15)"}], "checked": ["git diff src/db/inventory_repo.py — window check present, matches 202 criterion 1", "pytest tests/test_inventory_repo.py -x — 5 passed (ran independently)", "pytest tests/test_reminder_plugin.py -x — 8 passed", "manual repro of 201 repro_path — no longer flagged"]}
```
Advisory/refutation bar: `agents/dcs-safety-officer.md` step 6.

**`pass` with advisories is the normal healthy verdict (v0.6.5)**:
advisories are fixed by the IC and never block a merge; only a `halt`'s
refutations do. Bar for what counts as a refutation instead of an
advisory: `agents/dcs-safety-officer.md` step 6.

Halt shape, showing the `refutations` object:

```json
{"verdict": "halt", "refutations": [{"claim": "S1 reported 'done' with tests_run: pytest test_inventory_repo.py -x, 5 passed", "evidence": "Re-ran it myself: 4 passed, 1 skipped (test_window_boundary marked xfail, never un-marked) — the boundary case from 202 criterion 1 is untested"}], "checked": ["git diff src/db/inventory_repo.py", "pytest tests/test_inventory_repo.py -x (independent re-run)"]}
```

| Field | Type | Notes |
|---|---|---|
| `verdict` | `"pass"` \| `"halt"` | Binding on the IC — a `halt` cannot be argued past, only resolved (fix-tasking or re-plan) |
| `refutations` | object[] | Empty on `pass`. Each has `claim` (what was asserted) and `evidence` (what the Safety Officer independently found). **Reserved for the acceptance criteria and the behaviour of the code** — the only findings that justify stopping a merge |
| `advisories` | object[], optional | (v0.6.5) Artifact-hygiene findings that do **not** block: `finding` + `fix`. Principle-15 issues in docstrings, comments, logs and AARs live here unless they clear one of the three bars in `agents/dcs-safety-officer.md` step 6. The IC folds them into the integration commit |
| `checked` | string[] | Everything the Safety Officer actually did — diff inspected, tests re-run itself, manual repro. Specialist self-reports are never listed here as the check itself, only as the claim being checked. Same for `refutations`/`advisories`: cite the decisive excerpt or `file:line`, never paste a full unabridged transcript |

## 6. Commander decisions (transfer of command — feeds 214-LOG.md)

Returned by `dcs-commander`, one decision per invocation, at the four command points doctrine's "Transfer of command" defines. When the main session runs Fable it makes these calls itself and no spawn occurs — the decision is still logged in `214-LOG.md` the same way.

```json
{"command_point": "typing", "type": 3, "rationale": "3 files, fix pattern known, no schema impact", "open_questions": []}
```

Any decision may also carry an ESG-activation request (doctrine principle 14):

```json
{"command_point": "deviation", "disposition": "escalate_owner", "rationale": "fix requires touching the payment flow", "directives": [], "esg_activation": {"requested": true, "reason": "payment flow is forbidden AND the pattern spans two other queued items -- strategic, not tactical"}}
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

The fenced ```delegation-bounds``` JSON block inside `DELEGATION.md` — the only part of that file workflows parse; the surrounding prose is for humans only.

```json
{"version": 1, "auto_approve_type3": false, "max_files": 4, "forbidden_globs": ["**/migrations.py", "**/auth/**", "**/payment*/**"], "forbidden_topics": ["schema migration", "payments", "auth/JWT", "deploy scripts"], "require_tests_green": true, "max_specialists": 2, "deploy": {"auto": false, "auto_after_close": false, "frontend_only": true, "forbidden_globs": ["**/migrations.py", "**/auth/**", "**/payment*/**"], "max_rows_per_train": 3}}
```

| Field | Type | Notes |
|---|---|---|
| `version` | number | Bumped every amendment; `DELEGATION.md` keeps every prior version block — this is the one currently in force |
| `auto_approve_type3` | boolean | Master switch. `false` = identical to v0.1 behavior even with a `DELEGATION.md` present |
| `max_files` | number | Compared against the IAP's total partitioned file count |
| `forbidden_globs` | string[] | Any 204 tasking's `territory` glob matching one of these voids auto-approval for that IAP |
| `forbidden_topics` | string[] | Checked against the 201/202 text |
| `require_tests_green` | boolean | If `true`, the chief's `verification_plan` must name a concrete automated test run, not "manual only" |
| `max_specialists` | number | Compared against the 204 tasking count |
| `deploy` (v0.4) | object, optional | Deploy delegation keys: `auto`, `auto_after_close`, `frontend_only`, `forbidden_globs`, `max_rows_per_train`. Behavior: `deploy.md` step 5, `run.md` step 7a. |

`esg.max_periods_before_review` (principle 13, trigger c) is **not** part of this block — it lives in `config.json`'s `esg` key (default `3`); trigger (c) applies incident-wide regardless of Delegation.

## 8. 209 sitrep (v0.2 — feeds `.dcs/esg/SITREPS/<slug>-p<N>.md`)

Relocated to `$HOME/.claude/dcs/templates/209-SITREP.md`: its prose headings carry the
same fields, plus a trigger enum, `Decided at`, and `Notes` that this
section never had. The number `8` stays reserved on purpose, so every
existing citation of this section keeps pointing here.
