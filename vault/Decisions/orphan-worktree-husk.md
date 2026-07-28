---
tags: [dcs, decision]
updated: 2026-07-28
---

# Decision: stop reporting `C:\DCS-wt\schema-citation-guard`

**Decided:** 2026-07-27, seventh `/dcs-esg` session
**Status:** REOPENED 2026-07-28, ninth `/dcs-esg` session — see update below
**Reopen if:** the directory acquires contents, or a *second* husk appears (one
is an accident; two is a pattern in how worktrees are removed)

## Update, 2026-07-28 (ninth `/dcs-esg`): the reopen trigger fired, and one husk is gone

**`C:\DCS-wt\token-economy` is a second husk**, same shape as this one — empty
but for DCS's own `.dcs/CLOSED` marker, git-forgotten, and its own closing
session's `git worktree remove` failed with `Permission denied` because that
session's cwd sat inside it (`.dcs/incidents/2026-07-28-token-economy/214-LOG.md`,
step 5a.4). Per this decision's own reopen condition, two is a pattern — queued
as register row `worktree-removal-self-conflict` rather than silently
re-applying "accepted boundary" to both.

**`schema-citation-guard` itself was removed this session** —
`rmdir "C:\DCS-wt\schema-citation-guard"` succeeded on the first attempt from a
session rooted in `C:\DCS`, after six failures across four prior sessions. That
part of this decision is now moot; kept here as the record rather than deleted,
since the reopened question (why removal fails at all) is a different one.

**New evidence that narrows, not confirms, the original explanation.** The same
session that finally removed `schema-citation-guard` immediately tried
`C:\DCS-wt\token-economy` and got `Device or resource busy` — from a cwd
(`C:\DCS`) that was **not** inside the worktree being removed. `.git/worktrees/`
doesn't even exist (git has no metadata left to hold a lock), so the "closing
session's own cwd" explanation, which fit attempts 1–2 on the original husk,
does **not** cover this failure. This matches the *unexplained* half of the
original table below (attempts 3–6) more than the *explained* half (1–2) — the
two husks are not necessarily one mechanism, and whoever works
`worktree-removal-self-conflict` should treat "some other process holds a
handle on the directory" as the open question, not "the closing session is
rooted inside it" as a settled answer.

## The question

`C:\DCS-wt\schema-citation-guard` has been on disk since 2026-07-26, when that
incident's close removed its worktree. Every worktree audit since has flagged it
as an **orphan** — DCS-owned by container location, no register row, absent from
`git worktree list` — and the Owner decided **remove it** at the fourth session.

**Six removal attempts have failed**, across four different sessions and two
different explanations:

| attempt | context | result |
|---|---|---|
| 1 | 4th `/dcs-esg` | *"The process cannot access the file … used by another process"* |
| 2 | `deploy-marker-blind` close | *Device or resource busy* |
| 3 | 5th `/dcs-esg` | *Device or resource busy* |
| 4–6 | `direct-resolution-lane` close, 6th and 7th `/dcs-esg` | flagged, not retried or retried and refused |

The first two failures were each explained by the acting session's own shell
being rooted inside the directory. **That explanation is spent**: attempts from
sessions rooted in `C:\DCS` failed identically, so the holder is some other
process and has never been identified.

## What was decided, and why it is not surrender

**The audit stops reporting it.** Not because it was fixed, but because it is
**not a finding** — and six sessions of carrying a line item that requires no
decision is exactly the artifact bloat `esg-artifact-bloat` (rank 8) is about,
reproduced in the audit that is supposed to surface real problems.

The properties that make it a non-finding were re-verified at each attempt, not
assumed:

- **Empty.** Zero entries, tracked or untracked. Nothing to preserve.
- **Not a worktree.** Absent from `git worktree list --porcelain`, so git holds
  no state pointing at it and no incident can resume inside it.
- **Not a gate hazard.** It has no `.dcs/ACTIVE`, so it cannot become a second
  life for merged work — and `dcs_gate.py`'s `.dcs/CLOSED` zombie rule exists
  for precisely the case where that risk is real, which this is not.

Regenerate all three:

```bash
ls -la "C:/DCS-wt/schema-citation-guard"; git -C C:/DCS worktree list --porcelain | grep -c schema-citation-guard
```

**Still owed, and it is one line from any terminal that does not hold it:**

```bash
rmdir "C:\DCS-wt\schema-citation-guard"
```

## The lesson worth keeping, which is smaller than the paragraph

**A repeated non-finding is a reporting defect, not a persistence problem.** The
audit correctly identified an orphan once. Re-identifying it six times, when
every re-identification ended in the same decision that could not be executed
for an environmental reason, converted a hygiene check into noise — and noise in
an audit is worse than silence, because it trains the reader to skim.

The related lesson from the fourth session still stands and is why the container
is awkward in the first place: **a session rooted inside the worktree container
cannot clean that container**, which is why `CLAUDE.md`'s *"run DCS incidents
from a session rooted in `C:\DCS`"* is a rule and not a preference. That
explains attempts 1–2. It does not explain 3–6, and nothing does yet.

## Links

- [[Backlog]] — item 15 records a comparable *accepted boundary* rather than a
  gap, and this note follows that precedent
- [[Meta/building-dcs-lessons]] §16 — territory and artifact width as a cost
  paid by every later reader
