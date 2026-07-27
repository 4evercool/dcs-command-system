# 202 — Objectives (Operational Period 1)

**Incident:** direct-resolution-lane
**Period:** 1

## Goal

The register tells the truth about work resolved without a worktree. An
incident taken off the queue and fixed inline leaves a **terminal** row, not a
`QUEUED` row that outlives the work — and the state it lands in is defined
generally enough that the two split-out manifestations later consume it without
reopening the enum.

## Acceptance criteria (the Definition of Done)

1. **`dcs/templates/REGISTER.md`'s state enum carries exactly one new terminal
   state** — seven values where there are six today. **Verified by command, not
   by line number** (the change moves the block, so a cited range is a derived
   fact that expires on contact — lint defect 3, fixed at plan time):

   ```bash
   sed -n '/<!-- State values/,/^$/p' dcs/templates/REGISTER.md | tr -d '\n' | sed 's/.*State values[^:]*: *//' | tr '|' '\n' | sed 's/^ *//;s/ *$//' | grep -c .
   ```

   → must print `7`. Prints `6` at HEAD.

2. **The new state's definition is scenario-neutral** — terminal for *any*
   resolution that never opened a worktree/deploy lifecycle. It must not name a
   type, a workflow step, or a lane:

   ```bash
   sed -n '/^ *RESOLVED /,/^$/p' dcs/templates/REGISTER.md | grep -inE "type ?5|step 7a|express lane"
   ```

   → **must return empty.** The extraction boundary requires the new state's
   description be placed **last** in the description block, which the plan fixes.
   *(IC bound from command point 1 — this is what lets
   `register-field-repair-path` and `trivial-work-inline-lane` consume the state
   instead of editing the enum again.)* **The grep is necessary, not
   sufficient:** it catches three literal strings, while the real criterion is
   that the definition would serve both split-out rows unchanged. The Safety
   Officer must read it and say so, not just run it.

3. **Every in-territory carrier of the literal state enumeration agrees with the
   canonical enum.** The population is enumerated, never hand-listed:

   ```bash
   grep -rnE "QUEUED" dcs/ agents/ skills/ CLAUDE.md README.md --include=*.md | grep -E "ACTIVE|DEPLOYED|PARKED|KILLED"
   ```

   Run at plan time, 2026-07-27T15:33+11:00 — **3 in-territory carriers**:
   `dcs/references/forms.md:22`, `dcs/templates/REGISTER.md:25` (the enum
   comment) and `dcs/templates/REGISTER.md:71` (**the row template's own state
   cell — a second carrier inside the same file, surfaced by running the command
   rather than trusting the 201's list**). One further hit,
   `dcs/workflows/status.md:102`, is **out of territory** and already its own
   register row. The criterion is that re-running this command shows **every
   in-territory site naming the same seven state VALUES** — not that "these
   three sites were fixed".

   **"Agrees" means the same set of values, each site keeping its own existing
   style. It does NOT mean byte-identical lists.** This was a real defect in the
   first draft of this criterion, caught by the Planning Chief and confirmed
   mechanically at plan time: the three carriers **already disagree textually at
   HEAD**, before this incident edits anything —

   | site | rendering at HEAD |
   |---|---|
   | `dcs/templates/REGISTER.md:25` | `QUEUED \| ACTIVE \| MERGED (deploy pending) \| DEPLOYED \| PARKED \| KILLED` |
   | `dcs/templates/REGISTER.md:71` | `{{QUEUED\|ACTIVE\|MERGED\|DEPLOYED\|PARKED\|KILLED}}` |
   | `dcs/references/forms.md:22` | `QUEUED / ACTIVE / MERGED / DEPLOYED / PARKED / KILLED` |

   Three separators and two spellings of `MERGED`. Read strictly, the criterion
   would have been **red before a single edit**, and Safety would have halted on
   a pre-existing difference this period did not cause. **Normalising those
   differences is explicitly out of scope** — it is a separate defect and does
   not belong here.

4. **`new.md` step 7a writes the register.** The Type 5 express lane gains a
   substep transitioning the row to the new state. Verified by
   `grep -n "REGISTER" ` inside the step 7a block → non-empty, plus reading the
   substep.

5. **`dcs/workflows/close.md:239` remains true as written** — *"the register's
   terminal state for a shipped incident is `DEPLOYED`, reached later via
   `/dcs-deploy`"*. Either it is still accurate beside the new state, or it is
   reworded so it is. Verified by reading the line.

6. **`python tests/test_doctrine_integrity.py` is green, and check 15 in
   particular.** Read the suite's own count line, and read check 15's own PASS
   line: it must still name `dcs/templates/REGISTER.md` in its declaring
   population and report **one** declaring paragraph. Baseline at plan time,
   read from its own line: `82/82 passed`. *(Rule C allows at most one declaring
   paragraph per file, and the new state's prose lands beside the pinned
   `DEPLOYED` paragraph — this criterion is what makes that collision visible
   rather than discovered at the merge.)*

7. **The neighbouring suites stay green**, each count read from its own line:
   `python tests/test_dcs_gate.py` (`100/100` at plan time) and
   `python tests/test_dcs_intake.py` (`10/10` at plan time).

8. **If `dcs/references/doctrine.md` is touched, the hot path stays under its
   ceiling with `HOT_PATH_BUDGET_KB` untouched.** Raising the ratchet is a
   deviation, not an option. Regenerate:

   ```bash
   python -c "import pathlib; d=pathlib.Path('dcs/references/doctrine.md').read_bytes().replace(b'\r\n',b'\n'); s=pathlib.Path('dcs/references/schemas.md').read_bytes().replace(b'\r\n',b'\n'); print(len(d)+len(s), 37*1024-len(d)-len(s))"
   ```

   At plan time: `36683 1205` — 1,205 B of slack.

9. **The `CHANGELOG.md` entry lands in the existing 0.6.10 section and no
   version bump is made — and this rests on a MEASURED fact, not an asserted
   one.** Split ownership, tagged because the halves have different owners
   (lint check 6): the **local half** — the entry is in the existing section,
   `dcs/VERSION` and `package.json` both still read 0.6.10 — is specialist work.
   The **registry re-measure is [IC] at close**, because `npm view` needs
   network and may not run in a specialist harness. Measured at plan time,
   2026-07-27T15:33+11:00:
   `npm view dcs-command-system version` → **0.6.9**, `cat dcs/VERSION` →
   **0.6.10**, therefore 0.6.10 is unpublished and the open section is the right
   home. **Re-run both commands at close and record the output** — if the
   registry has moved to 0.6.10 by then, this criterion is void and the bump
   becomes a real question. *(This criterion is written this way on purpose:
   asserting "0.6.10 is unpublished" without an owner for the measurement is
   exactly the defect register row `criterion-unmeasured-fact`, rank 2, exists
   for — it cost a version published twice with different contents.)*

10. **Owner-UAT.** **[Owner]** — the Owner reads the diff and confirms the new
    state is the shape they want in the portfolio's state machine, given it is
    the first state added to the enum since the v0.3 design established all six
    together.

## Out of scope this period

- **Manifestation (b)** — field repairs with no registration path. Split at
  command point 1 to `register-field-repair-path`.
- **Manifestation (c)** — the inline-diff-plus-post-hoc-row sizing branch. Split
  to `trivial-work-inline-lane`, whose relationship to
  `decomposition-backlog-routing` (rank 9) is the next `/dcs-esg`'s to decide.
- **`dcs/workflows/status.md`** — its enum paraphrase is wrong **today**, before
  this incident touches anything. Registered as `status-md-enum-drift`; fixing
  it here would absorb a pre-existing defect.
- **`tests/test_doctrine_integrity.py`** — **forbidden territory**, not merely
  out of scope. If check 15 reddens, the remedy is rewording
  `dcs/templates/REGISTER.md`. Editing the check is a deviation, full stop
  (IC bound, command point 1).
- **`dcs/workflows/esg.md`, `run.md`, `loop.md`** — dropped with (b) and (c),
  **conditionally**. `run.md:54-57` and `loop.md` step 5 both describe Type 5 as
  register-neutral. If criterion 4's change makes either text false, the
  coherent fix for this period touches them, and **the Planning Chief must say
  so in `objectives_feedback` now** — surfacing it after the IAP is stamped is
  escalation trigger (a), not a tidy-up.

## Owed after this period, owned but not criteria

- **[IC, post-deploy] Touch up this repo's own live register legend.**
  `C:\DCS\.dcs\esg\REGISTER.md` carries a verbatim copy of the template's
  six-state legend, and `.dcs/` is in **neither installer's payload** — so the
  install updates the shipped template and leaves every already-onboarded
  project's live register declaring six states while the installed `new.md`
  step 7a instructs writing a seventh. Verified low severity: nothing parses the
  enum (`grep -rn 'REGISTER.md' --include=*.py --include=*.js` hits only check
  15's machinery, which reads the shipped **template**). Named here so it has an
  owner rather than dangling — it is a post-close act, not this period's work.
- **[follow-up row] `deploy.md` step 8's intake-closure keys off `DEPLOYED`**
  (`deploy.md:252-259`), so a directly-resolved row will never have its intake
  source closed by the deploy train. This is a gap the new state **exposes**, not
  one it creates, and it belongs to the next `/dcs-esg` alongside the three rows
  the split already produced.

## Chief feedback

**Planning Chief — the caveat this 202 asked for is ANSWERED, and the answer is
"no".** Making step 7a write the register does **not** falsify `run.md:54-57` or
`loop.md` step 5. `run.md` says a Type 5 resolves inline with *"no incident
directory, no gate"* — a register row is neither, so the sentence stays literally
true and becomes merely **incomplete**. `loop.md` step 5 never claims Type 5 is
register-neutral; it simply does not name the short-circuit as a continuation
condition, a gap identical at HEAD. Same for `typing.md:33-35` and `doctrine.md`'s
Type 5 row: both enumerate *"no chiefs, no Safety Officer, no incident directory,
no gate"* and make no register claim. **All four stay out of territory**, and
`run.md`/`loop.md` completeness becomes a follow-up rather than a scope
expansion.

**Chief hardening accepted:** `doctrine.md` and `typing.md` are **forbidden**,
not merely out of scope. No doctrine *rule* changes here — a bookkeeping substep
is not a rule — and with 1,205 B of slack the cheapest way to guarantee
criterion 8 is to make breaching it structurally impossible. A specialist that
concludes a hot-path carrier is genuinely needed reports a **deviation**, which
is the IC's call, not a judgement made inside a tasking.

**Criterion 3's ambiguity** was raised by the chief and is fixed above.

**Criteria 1 and 2's line-number citations** were raised by the chief and are
replaced above with extraction commands.

**Criterion 6's `82/82` is itself derived** — check 15's Rule A emits one check
per declaring file, so the total moves if and only if the declaring population
changes. That is now a feature: a total other than 82 is the tripwire, not a
counting quibble.
