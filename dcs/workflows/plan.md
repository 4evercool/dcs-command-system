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

## 6. Present the IAP to the Owner

Use `AskUserQuestion` — **not** plan mode. This is deliberate: DCS's own
approval gate is a distinct mechanism from the global ExitPlanMode
handoff hook, and routing IAP approval through plan mode would collide
with it. Summarize the IAP (goal, tactics, partition, risks) and ask:
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
