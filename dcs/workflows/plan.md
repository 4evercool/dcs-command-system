<purpose>
The planning arc of the P-loop: objectives, chief-authored tactics and
tasking partition, integration into a single IAP, Owner approval, and a
hash-stamped approval marker that opens the gate for /dcs-execute.
</purpose>

<required_reading>
@$HOME/.claude/dcs/references/doctrine.md
@$HOME/.claude/dcs/references/schemas.md
@$HOME/.claude/dcs/references/forms.md
</required_reading>

<process>

## 1. Verify incident state

```bash
cat "<project>/.dcs/ACTIVE"
```

Parse `<slug>|<type>|<phase>`. If no `ACTIVE` file: stop, tell the Owner
there's no open incident — run `/dcs-new` first. If `phase` is
`execution`: this incident already has (or had) an approved IAP for the
current period; ask the Owner whether they mean to revise the plan
(counts as a re-plan — proceed, but flag that this will void the current
approval once IAP.md changes) or actually meant `/dcs-status` /
`/dcs-execute`.

Determine the operational period number `N` — 1 if this is the first pass
through this step for this incident, else increment from the last period
recorded in `214-LOG.md`.

**Command-chain check (entry gate — do this before drafting anything):**
read `214-LOG.md` and confirm a `command: typed` entry exists (command
point 1). If it is missing, the Dispatcher in `/dcs-new` typed the
incident itself — a doctrine violation observed repeatedly in the field
(three times on day one, always by the weakest-model dispatcher, always
in its own voice: "this is clearly a Type N"). Repair NOW, before any
202 work: run command point 1 properly (spawn `dcs-commander` with the
201 text if this session is not Fable; decide yourself if it is), log
the decision, and if the commander's type differs from what the 201
recorded, correct the 201 and re-confirm with the Owner. Do not carry an
unratified typing decision into planning — the whole activation level
(chiefs, ceremony, approval requirements) hangs off it.

## 2. Draft 202-OBJECTIVES.md

Read `201-BRIEF.md`. Draft the goal (outcome-shaped) and numbered,
verifiable acceptance criteria using
`$HOME/.claude/dcs/templates/202-OBJECTIVES.md`. If this is a re-plan after
a deviation (see step 6 of `execute.md`), fold the deviation's `proposal`
into the goal/criteria explicitly rather than pretending it's a fresh
period with no history.

Present the draft to the Owner via `AskUserQuestion` for a quick
confirm/edit — this is a lightweight check (forms.md: 202 is authored by
IC **+ Owner**), not the full IAP approval gate that comes later. Write the
confirmed version to `202-OBJECTIVES.md` in the incident directory.

## 3. Spawn the Planning Chief (and Logistics Chief for Type 1)

Spawn `dcs-planning-chief` via Task, passing **only** the full text of
`201-BRIEF.md` and `202-OBJECTIVES.md` inline in the prompt (not file
paths — the chief's information diet is deliberately restricted to what
these two files contain, per its agent charter). For Type 1, also spawn
`dcs-logistics-chief` in the same message with the same two files' text
(both can run in parallel — they don't depend on each other's output).

If this is a re-plan triggered by a deviation, also include the
triggering specialist's `found` / `why_plan_wrong` / `proposal` fields in
the Planning Chief's prompt.

## 4. Validate the returns — COMMAND POINT 2 (IAP acceptance)

From the Planning Chief: `objectives_feedback`, `tactics[]`, `taskings[]`,
`partition_ok`, `risks[]`, `verification_plan` (schema in
`references/schemas.md` #2).

This is a command point (doctrine: "Transfer of command"). **If this
session is not running Fable**: spawn `dcs-commander` via Task (model
`fable`) with the full 201 + 202 text and the chiefs' complete structured
returns; its `iap_review` decision (schemas.md #6) governs — on
`"reject"`, use its `required_changes` verbatim as the re-spawn
instruction to the Planning Chief and repeat this step; on `"accept"`,
proceed. Record the decision in `214-LOG.md`
(`command: iap_review <verdict> (IC=dcs-commander)`). **If this session is
Fable**, apply the checks below yourself.

**Partition check (hard gate):** if `partition_ok` is `false`, read
`risks[]` for a justification (sequential staging or worktree isolation).
If the justification is present and coherent, proceed — the IAP will
record it as a sequential/worktree execution mode. If `partition_ok` is
`false` with no real justification, or `true` but the `territory[]` arrays
visibly overlap anyway: **reject.** Re-spawn `dcs-planning-chief` with a
one-line explanation of what was wrong, and repeat this step. Do not
integrate a plan with an unjustified overlapping partition into the IAP —
this is doctrine principle 6, non-negotiable.

If `objectives_feedback` flags a 202 criterion as untestable, resolve it
now: either revise 202 (brief Owner confirm) or explicitly accept the risk
and note why.

## 5. Write the planning artifacts

- `203-ORG.md` — activated positions this period, from
  `$HOME/.claude/dcs/templates/203-ORG.md`.
- `204-TASKING/S1.md`, `S2.md`, ... — one per tasking, transcribed from the
  chief's `taskings[]`, using `$HOME/.claude/dcs/templates/204-TASKING.md`.
- `IAP.md` — integrated from `$HOME/.claude/dcs/templates/IAP.md`: links
  202+203+204, the partition table (with disjoint/overlap-justified
  status), risks, verification plan, and (Type 1) the Logistics Chief's
  deploy/env/migration/rollback plan.

## 5a. Refine the register's territory (v0.3)

Now that `IAP.md`'s partition table is final, resolve `esg_root`
(doctrine "Parallel operation": `git worktree list --porcelain`, first
entry). If `<esg_root>/.dcs/esg/REGISTER.md` exists, update this
incident's row's `territory` column to the **union** of every
`204-TASKING/*.md`'s `territory[]` globs — this replaces the coarser
201-blast-radius estimate `/dcs-new` recorded when the incident opened,
with the plan's own precise partition. This is what keeps the portfolio-
level territory check in `new.md` step 7b accurate for whatever incident
gets typed next. If `REGISTER.md` doesn't exist, skip this step.

## 6. Approve the IAP — Delegation-aware (v0.2)

**Delegation check (Type 3 only):** if the incident is Type 3 AND
`<project>/.dcs/esg/DELEGATION.md` exists, parse its latest (highest
`version`) fenced ```delegation-bounds``` JSON block — never the prose
around it (schemas.md #7 is the authoritative shape). Evaluate ALL of:

- `max_files` is >= the IAP's total partitioned file count.
- every `territory[]` glob across every `204-TASKING/*.md` misses every
  entry in `forbidden_globs`.
- the `201-BRIEF.md` / `202-OBJECTIVES.md` text doesn't match any string
  in `forbidden_topics`.
- `max_specialists` is >= the 204 tasking count.
- if `require_tests_green` is `true`, the chief's `verification_plan`
  names a concrete automated test run, not "manual only."

**All bounds hold AND `auto_approve_type3` is `true`:** the IC approves on
the Owner's behalf — skip the `AskUserQuestion` in step 6b below and
proceed directly to step 7 (stamp the marker), with `approved_by: IC
(Delegation v<N>)` instead of `approved_by: Owner` in `IAP-APPROVED`'s
metadata. Append to `214-LOG.md`: `approved under Delegation v<N> (Type 3,
bounds held)`. If `<project>/.dcs/esg/REGISTER.md` exists, also update or
add this incident's row there (id, title, type, priority, intake source,
opened date) so the register reflects every incident that ran, delegated
or not — doctrine principle 12: never silent. **Tell the Owner in one
visible line regardless:** e.g. "IAP for `<slug>` auto-approved under
Delegation v`<N>` (all bounds held); proceeding to `/dcs-execute`."

**Any bound fails, `auto_approve_type3` is `false`/absent, no
`DELEGATION.md`, or Type 1:** fall through to step 6b — if a delegation
check was attempted and failed, name the specific failed bound(s) in the
summary so the Owner sees exactly why it didn't auto-approve.

**No `DELEGATION.md` at all (project has no ESG):** `config.json`'s
`auto_approve_type3` key is superseded by, but still the fallback for,
projects without an ESG — it carries no bounds beyond the Type/config
check itself (no `max_files`, no `forbidden_globs`), so treat it far more
conservatively: only auto-approve on this fallback path if `Type == 3`
AND `auto_approve_type3: true` AND the IAP touches no file matching any
glob in `guarded_paths` outside the ordinary source tree (i.e. nothing
that already looks unusual for a routine change). This fallback predates
v0.2 and is unchanged by it; a project that runs `/dcs-esg` and gets a
real `DELEGATION.md` should prefer that path — it is auditable per-bound,
this one isn't.

## 6b. Present the IAP to the Owner

Use `AskUserQuestion` — **not** plan mode. This is deliberate: DCS's own
approval gate is a distinct mechanism from the global ExitPlanMode
handoff hook, and routing IAP approval through plan mode would collide
with it. Summarize the IAP (goal, tactics, partition, risks) — and, if a
delegation check ran and failed, the named failed bound(s) — then ask:
approve / request changes / reject.

- **Request changes:** revise the relevant artifact(s) (202, taskings, or
  IAP integration) and re-present. Loop until approved or rejected.
- **Reject:** the incident doesn't proceed this period — return to intake
  framing (more analyst work via a fresh `/dcs-new`-style investigation)
  or consider closing the incident as abandoned; this is rare and mostly
  signals the Type or the whole premise needs rethinking, not just the
  plan.

## 7. On approval: stamp the marker

**Pre-stamp checklist (hard stop):** before computing any hash, read
`214-LOG.md` and confirm it contains a `command: typed` entry (command
point 1, from `/dcs-new`) and a `command: iap_review` entry (command point
2, step 4 above). If either is missing, the command points were skipped —
this is the exact drift transfer-of-command exists to prevent. **Stop, run
the missed command point now** (spawn `dcs-commander` if not Fable, decide
yourself if Fable), log it, and only then proceed. Never stamp an approval
over an unlogged command chain.

Compute the sha256 of the final `IAP.md`:

```bash
python -c "import hashlib; print(hashlib.sha256(open(r'<incident_dir>/IAP.md','rb').read()).hexdigest())"
```

(or `certutil -hashfile IAP.md SHA256` on Windows if Python isn't
convenient in context — the value must match what `dcs_gate.py` computes,
which is a plain sha256 of the file's bytes).

Write `IAP-APPROVED` with the hash as its **first line** (the gate hook
only reads that line), followed by metadata:

```
<hex sha256>
approved_by: Owner
approved_at: <ISO8601 local timestamp>
period: <N>
```

(v0.2: if step 6 auto-approved under a Delegation, `approved_by: IC
(Delegation v<N>)` instead — the hash mechanism and every other line are
identical either way.)

**Windows caveat:** write this file WITHOUT a BOM. PowerShell 5.1's
`Set-Content -Encoding utf8` prepends one; use the Write tool, or
`[System.IO.File]::WriteAllText(path, content)`. The gate hook tolerates a
BOM since v0.1.1, but a BOM-free file is the contract. Same applies to
`.dcs/ACTIVE`.

## 8. Open the gate

Update `<project>/.dcs/ACTIVE` to `<slug>|<type>|execution`.

Append to `214-LOG.md`:
```
[<timestamp>] phase: planning -> execution (IAP approved, hash=<hash prefix>...)
```

## 9. Report

Tell the Owner the gate is open and the next step is `/dcs-execute`.

</process>
