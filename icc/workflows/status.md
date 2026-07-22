<purpose>
Read-only sitrep from disk: what incident (if any) is active, what phase
it's in, and exactly which command resumes the Planning P. This is the
resume entry point after any context reset — it makes no writes and spawns
no subagents, by design (doctrine principle 5: the files are the
shift-change briefing).
</purpose>

<process>

## 1. Determine project root and check for an active incident

```bash
cat "<project>/.icc/ACTIVE" 2>/dev/null
```

**If absent:** report "no active incident — gate open, ICC idle for this
project." Optionally note how many closed incidents exist under
`.icc/incidents/` (a quick `ls` count) for context. Nothing further to do.

## 2. Parse the active incident

Parse `<slug>|<type>|<phase>` from `ACTIVE`.

## 3. Read the incident directory

```bash
ls "<project>/.icc/incidents/<slug>/"
tail -n 15 "<project>/.icc/incidents/<slug>/214-LOG.md"
cat "<project>/.icc/incidents/<slug>/SAFETY.md" 2>/dev/null
```

Note presence/absence of: `202-OBJECTIVES.md`, `203-ORG.md`,
`204-TASKING/*.md`, `IAP.md`, `IAP-APPROVED`, `SAFETY.md`. Determine the
operational period count from phase-transition entries in `214-LOG.md`
(each `planning -> execution` transition marks one period's approval).
Determine open taskings: any `204-TASKING/*.md` file whose specialist ID
has no corresponding completion noted in `214-LOG.md` for the current
period.

## 4. Print the sitrep

A short table:

| Field | Value |
|---|---|
| Incident | `<slug>` |
| Type | `<type>` |
| Phase | `<phase>` |
| Operational period | `<N>` |
| Open taskings | `<list of IDs, or "none">` |
| Safety state | `<none yet | pass | halt>` |

Plus the last few `214-LOG.md` lines verbatim, for context on exactly what
just happened.

## 5. State the exact resuming command

Apply this table literally — do not paraphrase into vague advice:

| Phase | IAP state | Safety state | Resume with |
|---|---|---|---|
| `planning` | no IAP.md yet | — | `/icc-plan` |
| `planning` | IAP.md drafted, no `IAP-APPROVED` | — | `/icc-plan` (finish Owner approval) |
| `execution` | `IAP-APPROVED` valid (hash matches) | none yet | `/icc-execute` |
| `execution` | `IAP-APPROVED` valid | `halt` | `/icc-execute` (fix-taskings) or `/icc-plan` (if the halt requires a re-plan) |
| `execution` | `IAP-APPROVED` **invalid** (hash mismatch or missing) | any | `/icc-plan` (re-approval required — IAP.md was edited after approval) |
| `execution` | — | `pass`, objectives fully met | `/icc-close` |
| `execution` | — | `pass`, objectives partially met | `/icc-plan` (next operational period) |

To check `IAP-APPROVED` validity from status (read-only, same check the
gate hook and `/icc-execute` both perform):

```bash
python -c "import hashlib; print(hashlib.sha256(open(r'<incident_dir>/IAP.md','rb').read()).hexdigest())"
```

Compare against the first line of `IAP-APPROVED`.

## 6. Stop

No writes, no subagent spawns. This workflow only reads and reports.

</process>
