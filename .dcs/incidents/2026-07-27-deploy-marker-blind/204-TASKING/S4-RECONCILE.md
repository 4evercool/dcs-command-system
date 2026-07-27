# 204 — Tasking S4-RECONCILE (revision 2)

**Incident:** deploy-marker-blind · **Period:** 1 · **Revision:** 2
**Specialist:** dcs-ops-specialist (S4-RECONCILE) — fresh spawn
**Runs LAST, after S1, S2 and S3. READ-ONLY. You have NO territory.**

## Why this tasking exists

The Planning Chief spent three of the permitted four specialists
deliberately, arguing that the only credible fourth was a second prose
owner — and **splitting the contract surfaces across two heads is the
measured cause of halt 2.** The IC agreed and used the slot for the one
thing that cannot recreate that seam: **the Safety Officer's own manual
read, performed before Safety sees it.**

Halt count stands at **2 of 3**. The new IAP stamp resets it, but a period
that has already halted twice on one class should not discover a third
instance from the officer.

## Task — reconcile, report, edit nothing

### 1. The manual read the verification plan says matters most

Two passes, both as a human role rather than as a grep:

- **Read `dcs/templates/REGISTER.md` end to end as a maintainer
  instantiating it in a new project.** Does the file answer "what makes a
  row `DEPLOYED`?" **once**, or more than once?
- **Read `dcs/workflows/deploy.md` steps 4 and 7 back to back as an
  operator running a deploy.** Same question. Note that a step-4 /
  step-7 divergence for the "cannot check" case is **deliberate and
  protected** — step 4 treats an unreadable marker as unshipped, step 7
  stops, and step 7 says so. That is not a finding; its **absence** would
  be.

You are looking for exactly what halted this incident twice: **two places
in one document answering the same question differently.**

### 2. Confirm the guard's parse matches S1's final prose

Read check 15's body and run the suite. Confirm the **printed** population
and the **parsed** class→disposition map correspond to what
`deploy.md` step 7 actually now says, and that S1's citation census matches
check 15's population. **A guard that parses a contract nobody wrote is
worse than no guard.**

### 3. Criterion 5's walk, asking the role question

Re-run the enumerator and, for **every** hit, ask *"does this paragraph
tell a reader what makes a row `DEPLOYED`?"* — the **role** question, not
the vocabulary question.

> **If the tree is green and you find two declaring paragraphs in one file
> by eye, the GUARD is the defect, not just the prose.** Say so in those
> words; it is the most valuable thing you could return.

### 4. The known narrowness, checked rather than assumed

The chief stated an honest limit: **check 15 holds disposition-stating
sites; it does not hold vocabulary.** `close.md:66`'s exemplar phrasing
states no disposition, so only criterion 5's human walk catches it.
Confirm that limit is *exactly* as stated — no wider, no narrower — and
name any site that falls in the gap.

### 5. The rulings survived

- `wc -l dcs/workflows/deploy.md` — ≤ 265, or ≤ 275 with S1's written
  justification and every extra line inside step 7's disposition section.
- `grep -nE 'payload_check|~/\.claude|dcs/VERSION' dcs/workflows/deploy.md`
  — must return nothing.
- The step-4 / step-7 asymmetry survived compression **intact**. This is
  the nuance a line-budget squeeze deletes, and it is protected.
- `git status --short` / `git diff --stat` — `install.ps1`, `install.sh`,
  `package.json`, `dcs/VERSION`, `bin/**` and `tests/payload_check.py` all
  untouched; no scratch artefact, no forged text, no perturbed-and-reverted
  file left behind.

## Territory

**NONE. You may edit nothing.** Read anything; run any read-only command;
work in the session scratch directory if you need to. **Do not run
`install.ps1` / `install.sh`; do not write to `~/.claude`; do not commit.**

**Findings route as fix-taskings to the owning specialist via the IC.** If
you find a defect, **name the file, the paragraph and the owner** — do not
fix it. Fixing it yourself would make you the second prose owner this
roster exists to avoid.

## Evidence required in the return

Return `status: "done"` with `files_touched: []`.

1. The two manual reads, each with an explicit verdict: **one statement, or
   more than one** — and if more than one, the file, both paragraphs
   quoted, and the owning specialist.
2. Check 15's printed population and parsed map, pasted, with your
   confirmation that they correspond to `deploy.md` step 7's live text.
3. The criterion-5 walk with the role question answered per hit, and
   explicitly whether any hit lacks a disposition from S1.
4. The narrowness check: is the guard's limit exactly as stated? Name any
   site in the gap.
5. The five ruling checks above, with real output.
6. All three suites, each from its own `N/M passed` line **and exit code**.
7. **Your own judgement, in one paragraph: is there anything here a
   Safety Officer would halt on?** You have the whole picture and no stake
   in it. Say so plainly either way — "nothing I can find" is a complete
   answer and is what the IC is hoping for, but a third halt found here
   costs one fix-tasking instead of a full verify cycle.

## On discovering the plan doesn't fit reality

You cannot deviate in the ordinary sense — you change nothing. If the plan
itself is wrong, say so under item 7 and the IC will route it.
