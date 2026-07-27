# 204 — Tasking S1-FIX (fix round, after Safety halt 1)

**Incident:** deploy-marker-blind
**Period:** 1 · **Fix round:** 1 (halt count 1 of 3)
**Specialist:** dcs-ops-specialist (S1-FIX) — a **fresh** spawn, not the
original S1 resumed (doctrine principle 9b).

**No refutation was raised against your file.** The Safety Officer proved
the witness red four distinct ways and proved its payload set is genuinely
derived by adding three payload files the script had never seen (all three
surfaced as repo-only) and two non-payload files (both correctly ignored).
Criteria 1 and 2 are met on its own independent evidence. This round closes
two **advisories** in the same file.

## Task

### 1. Advisory 6 — mirror the repo-side guard on the installed side

Lines 204-211: a repo root without `dcs/` returns exit **2** ("not a DCS
repo"), but an **installed** root that exists and contains no DCS install
returns exit **1**. The officer ran it against an empty directory and got
`0 identical, 0 differing, 47 repo-only, 0 installed-only`, exit 1.

That conflates "cannot check" with "differs" — which your own docstring
names as the thing that must never happen, because `deploy.md`'s
marker-unreadable branch is the caller that has to tell them apart. It
currently fails in the *safe* direction under both step 4 and step 7, which
is why it is an advisory and not a refutation; fix it anyway:

> `if not (installed_root / "dcs").is_dir(): return 2` — "not a DCS
> install"

**Update the docstring's exit-class text to match.** The two guards should
read as one rule applied to both sides, not as a repo-side special case.

### 2. Advisory 5 — the census in the docstring needs its regenerating command

Docstring lines 44-52 carry counts that are **all true** — the officer
re-measured every one against the live tree (6 `dcs-*` agents in the repo;
33 `gsd-*` among 39 in `~/.claude/agents/`; 10 `dcs-*` skills among 13
installed, the 3 foreign ones being exactly `find-skills`, `humanizer`,
`reconciliation`). The gap is only that nothing beside them regenerates
them, which is principle 15. Attach the command, e.g.:

```
ls ~/.claude/agents | wc -l ; ls -d ~/.claude/skills/*/ | wc -l
```

For contrast, your installer line references at lines 33-42 are **done
right** — the officer verified all six land where claimed, and the
docstring states its own re-check condition. Match that standard here.

### Explicitly NOT in this round

The IC directed a constants-equality check in
`tests/test_doctrine_integrity.py` (advisory 1). **The IC's directive is
held by the Dispatcher and is not yours to do.** Three reasons, recorded so
this is not rediscovered as an omission: that file is in your **forbidden**
list and outside every territory in the approved partition; you writing the
guard that validates your own file is the section verifying its own work
(principle 7); and three `QUEUED` register rows claim that file. It closes
an advisory, not a refutation, and an advisory does not justify widening an
approved partition. It goes to the Owner at the UAT gate.

**Do not touch `tests/test_doctrine_integrity.py`.**

## File territory (may edit ONLY this)

- `tests/payload_check.py`

## Forbidden zones

Unchanged from `204-TASKING/S1.md`. Note especially
`tests/test_doctrine_integrity.py` (still forbidden, see above),
`dcs/workflows/deploy.md` (S2-FIX's), and `CLAUDE.md` (S3-FIX's).

## Evidence required in the return

1. **Re-prove the witness after the guard change**, against a scratch copy,
   **no install**, `~/.claude` never written. All of:
   - green baseline `python tests/payload_check.py --repo C:/DCS` → exit 0
   - altered file → exit 1 under **differing**, naming it
   - deleted file → exit 1 under **repo-only**, naming it
   - extra file → exit 3 under **installed-only**, naming it
   - differing **and** installed-only together → exit **1** (precedence
     preserved)
   - nonexistent `--installed` path → exit 2
   - **new:** `--installed <empty existing directory>` → exit **2**, "not a
     DCS install" — this is the fix; it returned exit 1 before
   - `--repo` pointed at a non-DCS tree → exit 2 (unchanged)
2. The new guard's code, and the updated docstring exit-class text.
3. The docstring census with its regenerating command attached, plus that
   command's real current output.
4. `git diff --stat` — proving `tests/test_doctrine_integrity.py` is
   **untouched**.
5. `python tests/test_doctrine_integrity.py`, `python tests/test_dcs_gate.py`,
   `python tests/test_dcs_intake.py` — each suite's own `N/M passed` line.

## On discovering the plan doesn't fit reality

STOP. Return `status: "deviation"` per `schemas.md` #4 with `found`,
`why_plan_wrong`, `proposal`.
