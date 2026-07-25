<!--
202-OBJECTIVES.md -- written by the IC together with the Owner, at the
start of EACH operational period (/dcs-plan). Re-drafted (new file content,
same filename) each time the incident re-enters the P-loop for another
period -- the prior period's 202 is preserved in 214-LOG.md's phase-
transition history and, once complete, in AAR.md's summary, not in this
file itself.
-->

# 202 — Objectives (Operational Period 1)

**Incident:** doctrine-hot-path-trim
**Period:** 1

## Goal

The doctrine hot path costs materially less to read on every invocation and
every command-point spawn, **without any rule changing, moving, or
disappearing.** Every version-tagged war story, field lesson and worked
example that accumulated since the v0.5.0 diet is relocated to
`doctrine-appendix.md` (which ships but is never `@`-included), leaving the
core carrying the operative rule and only the rationale a reader needs *at
the moment of applying it*. The budget ratchet is re-seated behind the
result so the win cannot silently erode again.

The success condition is a byte count, but the *risk* is a rule quietly
lost in the editing — which is why criteria 3–5 and 9 exist and why the
Owner reads the result.

## Measurement convention (read before interpreting any criterion)

Every size below is **raw on-disk bytes of the two hot-path files, measured
inside this incident's worktree**, by the guard's own method:

```
python -c "import os; d=os.path.getsize('dcs/references/doctrine.md'); s=os.path.getsize('dcs/references/schemas.md'); print(d, s, d+s)"
```

This tree measures **larger** than the main checkout: `core.autocrlf=true`
with no `.gitattributes`, so a fresh worktree checks out CRLF while the
long-lived main checkout holds LF. Same commit, measured 2026-07-25:
main `41,444` B, this worktree `41,763` B — a 319 B spread against the
43,008 B ceiling. Measuring in the worktree is therefore the **conservative**
choice and is the convention for this period. That sensitivity is itself a
defect; it is registered separately as `hot-path-budget-eol-sensitivity` and
is explicitly out of scope here (see below).

## Acceptance criteria (the Definition of Done)

1. **Hot path is at or below 36,864 B (36 kB) combined**, measured by the
   command above in this worktree. Baseline recorded 2026-07-25:
   `doctrine.md 27,167` + `schemas.md 14,596` = `41,763` B, so this requires
   removing **at least 4,899 B** from `doctrine.md`. (For orientation only,
   not a criterion: the post-diet equivalent in these units is ~32,031 B.)

2. **No field-lesson narrative remains in the core.** The population is
   enumerated by, and the criterion is *this command returning empty*:

   ```
   grep -n "Field lesson" dcs/references/doctrine.md
   ```

   Current output, recorded now: lines **38** and **120** (two matches). The
   lowercase pointer at line 3 — "Provenance, field lessons, and extended
   rationale live in doctrine-appendix.md" — is the routing rule itself and
   **must survive**; it does not match this command.

3. **Every principle still exists, still numbered as it is today.** The
   criterion is that this command's output is byte-identical to the baseline
   recorded in `214-LOG.md`:

   ```
   grep -noE "^[0-9]+b?\." dcs/references/doctrine.md
   ```

   No renumbering, no merging two principles into one, no dropping `9b`.
   49 sites across the package cite principles by number and the guard
   checks contiguity — renumbering breaks both.

4. **Every `##` heading in the core is unchanged.** The criterion is that
   this command's output matches the baseline in `214-LOG.md` exactly
   (same 12 headings, same text; line numbers will differ and that is fine):

   ```
   grep -n "^## " dcs/references/doctrine.md
   ```

   17 sites quote these headings verbatim and the guard checks them.

5. **The guard is green:** `python tests/test_doctrine_integrity.py` reports
   all checks passing. This is the mechanical proof for criteria 3 and 4 and
   for version sync, `@`-include resolution, agent/template references and
   encoding.

6. **Nothing is deleted without a home.** For every passage removed from the
   core, `214-LOG.md` carries a routing line naming where it went: either
   the `doctrine-appendix.md` section it now lives in, or — if it was
   redundant — the *existing* appendix text that already covers it, cited by
   line. A cut with no routing line is a failed criterion even if the byte
   count is met.

7. **The `doctrine.md:38` command-point field lesson survives in substance.**
   It has no appendix counterpart today (`doctrine-appendix.md`'s *Transfer
   of command* section is lines 29–44), so this is a **write-then-cut**, not
   a relocation. Criterion — this command returns non-empty:

   ```
   grep -n "quota\|transcript" dcs/references/doctrine-appendix.md
   ```

8. **The ratchet is re-seated behind the result.** `HOT_PATH_BUDGET_KB` in
   `tests/test_doctrine_integrity.py` is set to the post-trim measured size
   rounded up to the next whole kB **plus 1 kB of margin**, and must be
   strictly less than its current value of 42 — a ratchet only ever tightens.
   The surrounding comment states that derivation and the measuring command,
   not just a number (principle 15). **Only this constant and its comment may
   change in that file.**

9. **The rules are all still there, in the core, as rules.** The trimmed
   core must still state, in its own words: the model-availability
   re-test-per-spawn rule; the announce-before-spawn and
   empty-return-is-a-failed-spawn rules; principle 4's typing-sets-ceremony-
   not-size rule; principle 6's territory-never-leaves-its-project rule;
   principle 9b's fresh-spawn rule; principle 13's convergence-read and
   attempt-counting rules; principle 15's write-the-derivation and
   tests-pin-immutable-evidence rules. What may go is the *story* behind
   each; what may not go is the *instruction*. Verified by the Safety
   Officer reading the diff, and by criterion 10.

10. **[Owner]** Owner reads the trimmed `doctrine.md` end to end and confirms
    no rule was lost or weakened. No test can catch a silently dropped rule;
    this is the real gate on this incident and is the Owner-UAT at close.

11. **Version bump, atomic.** `dcs/VERSION` and `package.json` both move to
    `0.6.5` in this incident. `CLAUDE.md` requires the two to change in the
    same commit and the guard checks it; the deploy train that follows this
    close verifies the deployed marker *advanced*, which cannot happen if the
    version stands still. **If the Owner strikes this criterion at IAP
    approval, criterion 12 must be struck with it.**

12. **[deploy period]** `~/.claude/dcs/VERSION` equals `dcs/VERSION` after
    `/dcs-deploy` runs `install.ps1`. Not verifiable this period — the deploy
    train runs after close, with `.dcs/ACTIVE` already cleared.

## Out of scope this period

- **Renaming any `##` heading or renumbering any principle.** 66 sites
  depend on both. If the trim seems to need it, that is a deviation, not a
  judgment call.
- **The guard's check *logic*.** Only `HOT_PATH_BUDGET_KB` and its comment
  may change in `tests/test_doctrine_integrity.py` (IC ruling, command point
  1). Touching the checks themselves is a deviation.
- **`schemas.md`.** It is 14,596 B — 35 % of the hot path — but it has not
  changed since the diet already trimmed it, and the 201's blast radius does
  not cover it. Trimming it is a separate call on a separate day.
- **`hot-path-budget-eol-sensitivity`** — the CRLF/LF measurement spread
  found at plan time. Registered as its own `QUEUED` row; adding
  `.gitattributes` here would change every file in the tree and drown this
  diff.
- **The vault's mixed kB bases.** `vault/Metrics/incident-metrics.md` states
  the post-diet size as "31.7 kB" (1000-based) alongside "40.5 kB"
  (1024-based). Real, small, and unguarded — fix it as close-time
  bookkeeping, not as execution work.
- **Any rewrite that improves doctrine's wording for its own sake.** This
  period removes provenance; it does not re-argue rules.

## Chief feedback (filled in after /dcs-plan spawns the Planning Chief)

{{pending}}
