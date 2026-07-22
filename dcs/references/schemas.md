# DCS Structured Return Schemas

Doctrine principle 9: every agent return follows a fixed JSON schema.
Free-text summaries from four specialists are how an IC gets snowed — a
schema forces the disagreement between "I did the task" and "I did *a*
task" into a field the IC has to actually read.

Agents return these as the final block of their response (fenced ```json```
or bare — the IC parses either). Subagents do **not** write these to disk
themselves; the IC transcribes them into the relevant numbered file
(203/204/IAP/SAFETY/AAR) per `references/forms.md`. This keeps a single
writer per artifact and lets the IC reject a malformed or incomplete return
before it becomes doctrine for the rest of the period.

## 1. Situation-analyst findings (feeds 201-BRIEF.md)

Returned by `dcs-situation-analyst`.

```json
{
  "summary": "One paragraph: what the incident is and why it matters",
  "evidence": [
    "action_log row: category=error, actor_id=123, ts=2026-07-22T03:14Z, traceback tail: ...",
    "codegraph: get_blocking_ingredients has 3 callers, none touch delivery_date window"
  ],
  "affected_files": ["Copilot/db/inventory_repo.py", "Copilot/plugins/steve_plugin.py"],
  "repro_path": "1. Create order for tomorrow  2. Run get_blocking_ingredients  3. Order flagged as stuck",
  "prior_art": "vault/Память/pitfalls/inventory.md #12 — same symptom, different root cause, closed 2026-06-01"
}
```

| Field | Type | Notes |
|---|---|---|
| `summary` | string | One paragraph, no hedging — this goes straight into 201's Symptom section |
| `evidence` | string[] | Each item cites its source (log query, codegraph query, grep, test run) — no unsourced claims |
| `affected_files` | string[] | Best-guess blast radius; the Planning Chief will refine this, not trust it blindly |
| `repro_path` | string | Numbered steps, or `"not reproducible: <why>"` |
| `prior_art` | string | Reference to project memory (vault, tasks/lessons.md, prior incident) or `"none found"` |

## 2. Chief plan (feeds 203-ORG.md, 204-TASKING/\*.md, IAP.md)

Returned by `dcs-planning-chief` (and, for deploy/env/migration concerns
only, `dcs-logistics-chief` — see its own return shape below).

```json
{
  "objectives_feedback": "202's acceptance criteria are testable as written; no changes requested",
  "tactics": [
    "Add a delivery_date window check inside get_blocking_ingredients' existing transaction",
    "Update the Steve plugin's stuck-order heuristic to respect the same window"
  ],
  "taskings": [
    {
      "id": "S1",
      "task": "Add delivery_date window to get_blocking_ingredients per 202 acceptance criterion 1",
      "territory": ["Copilot/db/inventory_repo.py"],
      "forbidden": ["Copilot/plugins/**"],
      "evidence_required": ["pytest Copilot/tests/test_inventory_repo.py -x output"]
    },
    {
      "id": "S2",
      "task": "Stop flagging future-dated orders as stuck in Steve's heuristic per 202 acceptance criterion 2",
      "territory": ["Copilot/plugins/steve_plugin.py"],
      "forbidden": ["Copilot/db/**"],
      "evidence_required": ["pytest Copilot/tests/test_steve_plugin.py -x output"]
    }
  ],
  "partition_ok": true,
  "risks": ["Both files import db/connection.py — read-only import, not a write conflict"],
  "verification_plan": "Run both test files, then a manual repro of the 201 repro_path against a scratch order"
}
```

| Field | Type | Notes |
|---|---|---|
| `objectives_feedback` | string | Chief may push back on unmeasurable/untestable 202 criteria here — IC decides whether to revise 202 |
| `tactics` | string[] | The "how", one level above individual taskings |
| `taskings` | object[] | See below — this becomes 204-TASKING/\*.md, one file per entry |
| `partition_ok` | boolean | `true` only if every `territory` array is disjoint from every other tasking's `territory`. If `false`, the Chief MUST use `risks` to justify sequential staging or worktree isolation — the IC rejects `false` with no justification and re-spawns |
| `risks` | string[] | Partition risk, ordering risk, anything that could break the "disjoint files, parallel execution" assumption |
| `verification_plan` | string | Feeds the Safety Officer's brief — what "done" should look like end to end |

**Tasking object** (each entry in `taskings`):

| Field | Type | Notes |
|---|---|---|
| `id` | string | `S1`, `S2`, ... — matches the 204 filename (`204-TASKING/S1.md`) |
| `task` | string | Specific, references a 202 acceptance criterion by number |
| `territory` | string[] | Glob(s) this specialist may edit — must be disjoint from every other tasking's territory unless staged sequentially |
| `forbidden` | string[] | Explicit "do not touch" globs — usually the other specialists' territories, called out for clarity |
| `evidence_required` | string[] | Concrete command(s) whose real output the specialist must include in its return |

## 3. Logistics-chief plan (Type 1 only — feeds IAP.md's deploy section)

```json
{
  "deploy_path": "Copilot/deploy/deploy.sh (full deploy — migration touches backend and frontend build)",
  "env_deps": ["No new env vars", "requirements.txt: add alembic==1.13.1"],
  "migration_ordering": "Run schema migration before restarting bread-api.service, not after",
  "rollback_plan": "Migration is additive (new nullable column) — rollback is redeploying the prior commit; no down-migration needed",
  "risks": ["~2GB RAM server — avoid concurrent vite build + migration"]
}
```

## 4. Ops-specialist return (feeds 214-LOG.md, informs SAFETY.md)

Returned by `dcs-ops-specialist`.

```json
{
  "status": "done",
  "files_touched": ["Copilot/db/inventory_repo.py"],
  "tests_run": ["pytest Copilot/tests/test_inventory_repo.py -x"],
  "evidence": "5 passed in 1.2s (full pytest output pasted below)",
  "deviation": null
}
```

Deviation example (`status: "deviation"`):

```json
{
  "status": "deviation",
  "files_touched": [],
  "tests_run": [],
  "evidence": "get_blocking_ingredients has no single transaction to add the window check into — it's three separate db_connection() calls, which is itself a TOCTOU bug the 204 tasking didn't anticipate",
  "deviation": {
    "found": "The function is not atomic; adding a window check inside 'the existing transaction' is impossible because there isn't one",
    "why_plan_wrong": "202/204 assumed get_blocking_ingredients already used db_transaction() based on the 201 evidence, which only showed the function's output, not its internals",
    "proposal": "Wrap the three calls in a single db_transaction() first (small, in-territory fix), then add the window check — recommend as a 202 amendment, not a silent scope add"
  }
}
```

| Field | Type | Notes |
|---|---|---|
| `status` | `"done"` \| `"blocked"` \| `"deviation"` | `blocked` = external obstacle (missing credential, flaky env); `deviation` = the plan itself doesn't fit reality |
| `files_touched` | string[] | Must be a subset of the tasking's `territory` — the IC/Safety Officer treat any file outside territory as a violation, not evidence |
| `tests_run` | string[] | Commands actually executed, not commands that should be run |
| `evidence` | string | Real output, not a paraphrase — this is what the Safety Officer will refuse to trust and check again anyway |
| `deviation` | object \| null | Present only when `status: "deviation"`. `proposal` is a recommendation, not an action — the specialist never improvises the fix itself |

## 5. Safety-officer verdict (feeds SAFETY.md)

Returned by `dcs-safety-officer`.

```json
{
  "verdict": "pass",
  "refutations": [],
  "checked": [
    "git diff Copilot/db/inventory_repo.py — window check present, matches 202 criterion 1",
    "pytest Copilot/tests/test_inventory_repo.py -x — 5 passed (ran independently, not copied from S1's return)",
    "pytest Copilot/tests/test_steve_plugin.py -x — 8 passed",
    "manual repro of 201 repro_path against a scratch order — no longer flagged"
  ]
}
```

Halt example:

```json
{
  "verdict": "halt",
  "refutations": [
    {
      "claim": "S1 reported 'done' with tests_run: pytest test_inventory_repo.py -x, 5 passed",
      "evidence": "Re-ran it myself: 4 passed, 1 skipped (test_window_boundary is marked xfail and was never un-marked) — the boundary case from 202 criterion 1 is untested"
    }
  ],
  "checked": ["git diff Copilot/db/inventory_repo.py", "pytest Copilot/tests/test_inventory_repo.py -x (independent re-run)"]
}
```

| Field | Type | Notes |
|---|---|---|
| `verdict` | `"pass"` \| `"halt"` | Binding on the IC — a `halt` cannot be argued past, only resolved (fix-tasking or re-plan) |
| `refutations` | object[] | Empty on `pass`. Each has `claim` (what was asserted) and `evidence` (what the Safety Officer independently found) |
| `checked` | string[] | Everything the Safety Officer actually did — diff inspected, tests re-run itself, manual repro. Specialist self-reports are never listed here as the check itself, only as the claim being checked |

**Charter reminder:** the Safety Officer's job is to *attempt to refute*
completion. When uncertain, it refutes. A `pass` is earned by failing to
find a hole, not by finding no obvious one.

## 6. Commander decisions (transfer of command — feeds 214-LOG.md)

Returned by `dcs-commander`, one decision per invocation, at the four
command points defined in doctrine's "Transfer of command" section. When
the main session runs Fable it makes these calls itself and no spawn
occurs — the decision is still logged in `214-LOG.md` the same way.

```json
{"command_point": "typing", "type": 3, "rationale": "3 files, fix pattern known, no schema impact", "open_questions": []}
```

```json
{"command_point": "iap_review", "verdict": "accept", "reasons": ["partition disjoint, verified against territory globs"], "required_changes": []}
```

```json
{"command_point": "deviation", "disposition": "replan", "rationale": "the 204 premise (single transaction) is false", "directives": ["re-plan must first make the function atomic"]}
```

```json
{"command_point": "verdict_disposition", "disposition": "fix_taskings", "rationale": "refutation is one untested boundary case", "directives": ["S3: un-xfail test_window_boundary and make it pass, territory unchanged"]}
```

Any decision may additionally carry an ESG-activation request (doctrine
principle 14, v0.2.1) — the tactical decision is still returned; the
request rides along with it:

```json
{"command_point": "deviation", "disposition": "escalate_owner", "rationale": "fix requires touching the payment flow", "directives": [], "esg_activation": {"requested": true, "reason": "payment flow is a forbidden_globs bound AND the same defect pattern spans two other queued register items -- scope is strategic, not tactical"}}
```

| Field | Type | Notes |
|---|---|---|
| `command_point` | `"typing"` \| `"iap_review"` \| `"deviation"` \| `"verdict_disposition"` | Which decision this is |
| `type` / `verdict` / `disposition` | enum per point | The decision itself — see `agents/dcs-commander.md` for each point's enum |
| `rationale` / `reasons` | string / string[] | One line; grounded in verified inputs, not the Dispatcher's summary |
| `required_changes` / `directives` | string[] | Concrete, one line each — usable verbatim as re-spawn or fix-tasking instructions |
| `open_questions` | string[] | Only where the call is genuinely the Owner's — framed as the exact question to relay |
| `esg_activation` | object, optional | `{requested: bool, reason: string}` — the IC requesting ESG activation (escalation trigger (e)); the Dispatcher files a 209 with a **convene ESG** option, marks the register row `ESCALATED`, and pauses for the Owner |

## 7. Delegation bounds (v0.2 — feeds `.dcs/esg/DELEGATION.md`, parsed by `plan.md`/`run.md`/`loop.md`)

The fenced ```delegation-bounds``` JSON block inside `DELEGATION.md` — the
only part of that file workflows parse; the surrounding prose is for
humans only.

```json
{
  "version": 1,
  "auto_approve_type3": false,
  "max_files": 4,
  "forbidden_globs": ["**/migrations.py", "**/auth/**", "**/payment*/**"],
  "forbidden_topics": ["schema migration", "payments", "auth/JWT", "deploy scripts"],
  "require_tests_green": true,
  "max_specialists": 2
}
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

`esg.max_periods_before_review` (doctrine principle 13, trigger c) is
**not** part of this block — it lives in `config.json`'s `esg` key
(default `3`), because trigger (c) applies to every incident regardless
of whether a Delegation is even in force.

## 8. 209 sitrep (v0.2 — feeds `.dcs/esg/SITREPS/<slug>-p<N>.md`)

Filed by the IC at any escalation trigger (doctrine principle 13). Not a
subagent return — the IC assembles this directly from `202-OBJECTIVES.md`,
`SAFETY.md`, and `214-LOG.md`, then the Owner's `AskUserQuestion` answer
fills in `decision`/`decided_by`.

```json
{
  "incident": "slug",
  "period": 2,
  "status_summary": "One paragraph: what's true right now",
  "objectives_state": "criterion 1 met, criterion 2 partially met",
  "safety_state": "halt -- boundary case untested (second halt on this objective)",
  "resource_spend": "2 periods, 3 specialists total",
  "options": ["continue", "pivot", "demobilize"],
  "decision": "pivot",
  "decided_by": "Owner"
}
```

| Field | Type | Notes |
|---|---|---|
| `incident` | string | slug |
| `period` | number | operational period this sitrep was filed during |
| `status_summary` | string | one paragraph, no hedging |
| `objectives_state` | string | plain-language rollup of 202 criteria |
| `safety_state` | string | last verdict + why, if `halt` |
| `resource_spend` | string | periods/specialists/scope, for the Owner's cost judgment |
| `options` | `["continue","pivot","demobilize"]` | fixed enum, always all three offered |
| `decision` | one of `options` | filled in only after the Owner answers `AskUserQuestion` |
| `decided_by` | string | always `"Owner"` — this decision is never delegated, Delegation bounds or not |
