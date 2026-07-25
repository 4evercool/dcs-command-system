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
cat "<project>/.dcs/ACTIVE" 2>/dev/null
```

**If absent:** report "no active incident — gate open, DCS idle for this
project." Optionally note how many closed incidents exist under
`.dcs/incidents/` (a quick `ls` count) for context. Nothing further to do.

## 2. Parse the active incident

Parse `<slug>|<type>|<phase>` from `ACTIVE`.

## 3. Read the incident directory

```bash
ls "<project>/.dcs/incidents/<slug>/"
tail -n 15 "<project>/.dcs/incidents/<slug>/214-LOG.md"
cat "<project>/.dcs/incidents/<slug>/SAFETY.md" 2>/dev/null
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
| `planning` | no IAP.md yet | — | `/dcs-plan` |
| `planning` | IAP.md drafted, no `IAP-APPROVED` | — | `/dcs-plan` (finish Owner approval) |
| `execution` | `IAP-APPROVED` valid (hash matches) | none yet | `/dcs-execute` |
| `execution` | `IAP-APPROVED` valid | `halt` | `/dcs-execute` (fix-taskings) or `/dcs-plan` (if the halt requires a re-plan) |
| `execution` | `IAP-APPROVED` **invalid** (hash mismatch or missing) | any | `/dcs-plan` (re-approval required — IAP.md was edited after approval) |
| `execution` | — | `pass`, objectives fully met | `/dcs-close` |
| `execution` | — | `pass`, objectives partially met | `/dcs-plan` (next operational period) |

To check `IAP-APPROVED` validity from status (read-only, same check the
gate hook and `/dcs-execute` both perform):

```bash
python -c "
import hashlib
raw = open(r'<incident_dir>/IAP.md', 'rb').read()
lf = raw.replace(b'\r\n', b'\n')
crlf = lf.replace(b'\n', b'\r\n')
print({hashlib.sha256(v).hexdigest() for v in (raw, lf, crlf)})
"
```

Compare the first line of `IAP-APPROVED` against this set — valid if it
matches **any member** of it. The set holds up to three digests (raw bytes,
LF-normalised, and CRLF-normalised derived from the LF form) and fewer when
those forms coincide: a pure-LF file yields two, since `raw` and `lf` are the
same bytes.

## 6. Stop

No writes, no subagent spawns. This workflow only reads and reports.

## `--campaign` variant (v0.2)

If `$ARGUMENTS` contains `--campaign`, report the portfolio instead of (or
alongside, if an incident is also active) the single-incident sitrep
above. Still read-only — no writes, no subagent spawns.

1. If `<project>/.dcs/esg/` doesn't exist: report "no ESG on this
   project — run `/dcs-esg` to found one" and stop.
2. Read `REGISTER.md` and print its full table (QUEUED / ACTIVE / PARKED
   / CLOSED, all rows — CLOSED rows give the Owner history at a glance).
3. Read `DELEGATION.md`'s latest version block and report the delegation
   version in force plus `auto_approve_type3`'s current value (so the
   Owner knows at a glance whether routine work is currently unattended-
   capable).
4. List any files under `SITREPS/` whose `Decision` field is still
   `{{continue | pivot | demobilize}}` (unfilled) or otherwise blank —
   these are pending sitreps awaiting an Owner decision; name each one.
5. **(v0.3)** Run doctrine's canonical worktree audit ("Parallel
   operation" section) and print its findings (orphans, stale actives,
   deploy-pending, dangling branches) — still read-only, the audit itself
   only inspects `git worktree list` / `git branch --list` and reads
   `REGISTER.md`, it writes nothing. This is the same checklist
   `/dcs-esg` step 1, `/dcs-loop`'s preconditions, and `/dcs-deploy` run;
   `--campaign` is simply another place a stale or orphaned worktree gets
   surfaced instead of quietly rotting.

</process>
