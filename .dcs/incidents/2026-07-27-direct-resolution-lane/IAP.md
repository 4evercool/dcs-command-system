# IAP — Incident Action Plan

**Incident:** direct-resolution-lane
**Type:** 1
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `203-ORG.md` · `204-TASKING/S1.md` ·
`204-TASKING/S2.md` · logistics plan below (Type 1)

## Objectives (summary of 202)

**Goal.** The register tells the truth about work resolved without a worktree.
An incident taken off the queue and fixed inline leaves a **terminal** row, not a
`QUEUED` row that outlives the work — and the state it lands in is defined
generally enough that the two split-out manifestations later consume it without
reopening the enum.

**Acceptance criteria** (full text in `202-OBJECTIVES.md`; each is verified by a
command or a named read, and where a criterion has a population it carries the
command that enumerates it):

1. The state enum in `dcs/templates/REGISTER.md` carries **exactly one** new
   terminal state — seven values, not six. Counted by command, not by line number.
2. The new state's definition is **scenario-neutral** — names no type, no
   workflow step, no lane. Grepped; **and read**, because the grep catches three
   literal strings while the real test is whether it would serve both split-out
   rows unchanged.
3. Every **in-territory** carrier of the literal enumeration names the same seven
   **values**, each site keeping its own existing style. Population enumerated by
   command; **normalising the pre-existing style differences is out of scope.**
4. `new.md` step 7a writes the register, transitioning the row to the new state.
5. `close.md:239` remains true beside the new state, and `:243-244`'s orphan
   `CLOSED` is reconciled.
6. `test_doctrine_integrity.py` green **and check 15 in particular** — its PASS
   line still naming `dcs/templates/REGISTER.md` with **one** declaring paragraph.
7. `test_dcs_gate.py` and `test_dcs_intake.py` stay green.
8. The hot path is untouched and `HOT_PATH_BUDGET_KB` unmoved.
9. The `CHANGELOG.md` entry lands in the existing 0.6.10 section, no version
   bump — local half specialist work, **registry re-measure [IC] at close**.
10. Owner-UAT. **[Owner]**

## Tactics (from the Planning Chief)

1. **The state literal is fixed at plan time: `RESOLVED`.** Five sites across two
   territories must carry an identical token, so the name is a planning decision,
   not a per-tasking one. Verified collision-free across `dcs/ agents/ skills/
   tests/ CLAUDE.md README.md` — twice, independently. `CLOSED` was considered and
   rejected: it collides with `/dcs-close`'s own vocabulary and with
   `dcs_gate.py`'s `.dcs/CLOSED` zombie-rule filename.
2. **The check-15 remedy is structural, not verbal**, and derived from reading
   the check's source rather than from guessing at its intent. Its unit is the
   blank-line-delimited paragraph; a paragraph declares only on the conjunction of
   token + proof word + rule shape. Hence: append the new description **inside**
   the existing unbroken description block so no new paragraph is created; never
   use the token `DEPLOYED` in the new state's own sentences; and never give any
   other paragraph a rule shape.
3. **Scenario-neutral by construction, not by proofreading.** The type-specific
   knowledge lives in the **writer** (`new.md` step 7a), never in the enum.
4. **Partition by file role, not by criterion** — one specialist owns the
   *definition* surface (`dcs/templates/REGISTER.md` alone, the only file check 15
   constrains), the other owns the *consumer* surfaces. This concentrates the
   entire check-15 hazard in one tasking and one file.
5. **Step 7a's register write is update-only, and silent when there is nothing to
   update.** The rejected alternative is recorded so it is not re-proposed:
   inserting a row for every Type 5 would put every typo fix in the portfolio and
   give the express lane ceremony it has never had, against principle 4. The
   201's defect is a row that *outlives* its work, and only an existing row can.
6. **Budget the prose.** `new.md` is 234 lines against a ~250-line ceiling no
   suite enforces, so the substep is capped at ~12 lines and cross-references 7b
   substep 4a rather than restating it.

## File-territory partition

| Specialist | Territory | Forbidden (abridged — full list in the 204) |
|---|---|---|
| **S1** | `dcs/templates/REGISTER.md` | `tests/**`, `dcs/workflows/**`, `dcs/references/**`, every other `dcs/templates/*`, `CHANGELOG.md`, `agents/**`, `skills/**`, `bin/**`, `install.*`, `package.json`, `dcs/VERSION`, `README.md`, `CLAUDE.md` |
| **S2** | `dcs/workflows/new.md`, `dcs/workflows/close.md`, `dcs/references/forms.md`, `CHANGELOG.md` | `tests/**`, `dcs/templates/**`, `dcs/references/{doctrine,doctrine-appendix,typing,schemas}.md`, `dcs/workflows/{run,loop,status,esg,deploy,plan,execute,init}.md`, `dcs/hooks/**`, `agents/**`, `skills/**`, `bin/**`, `install.*`, `package.json`, `dcs/VERSION`, `README.md`, `CLAUDE.md` |

**Partition status: disjoint — verified by `fnmatch` at plan time, not by
trusting `partition_ok`. Execution is nonetheless SEQUENTIAL (S1 → S2)**, by IC
ruling at command point 2. Disjoint territories made parallelism available; it
was declined because the *verification* surface is shared (both taskings run the
same suite, so a parallel run can produce a spurious red — or a spurious green)
and because the state literal is a cross-tasking contract that nothing mechanical
enforces. Running S2 second lets it read S1's landed literal instead of trusting
the plan's copy. On a Type 1 adjacent to a guard we may not touch, latency loses
to margin; the cost is one round.

**`tests/test_doctrine_integrity.py` is forbidden to BOTH taskings** — not
absent, forbidden. If check 15 reddens, the remedy is rewording
`dcs/templates/REGISTER.md`. Editing the check is a deviation, full stop.

## Deploy / environment plan (Type 1, from the Logistics Chief)

**Deploy path.** `powershell -ExecutionPolicy Bypass -File C:\DCS\install.ps1`
(POSIX `./install.sh`) from the **main checkout after merge** — never from the
worktree, never while the incident is active. Content witness:
`python tests/payload_check.py`, resolved per `deploy.md` step 7 (exit `0`
identical and exit `3` installed-only-only are go; `1` and `2` are stop).

**Payload membership, verified line by line against `install.ps1:7,10,12-15` and
`install.sh:10-11,13,15-19`, not assumed:** `dcs/templates/REGISTER.md`,
`dcs/workflows/new.md`, `dcs/workflows/close.md` and `dcs/references/forms.md`
all sit under `dcs/` and **do** reach users via install. `CHANGELOG.md` is **not**
in the installer payload but **is** in `package.json`'s `files` whitelist, so it
reaches users only on `npm publish`. So: every behavioural change here ships by
install; the CHANGELOG entry ships only on a future publish.

**Environment.** No new env vars, no new dependencies (`payload_check.py` and all
three suites are stdlib-only), no config change, no hook change — so the
installers' postinstall "re-run `/dcs-init`" note does not apply.

**Migration ordering: none, and that is stated rather than manufactured.** No
schema, no runtime state. **But one compatibility question is real and was
verified rather than reasoned about:** a live register is a verbatim copy of this
template *including the state-value legend*, and `.dcs/` is in **neither
installer's payload** — so an install updates the shipped template and touches no
already-onboarded project's register. After this ships, every existing register
declares six states while the installed `new.md` step 7a instructs writing a
seventh. **Severity low, mechanically:** nothing parses the enum
(`grep -rn 'REGISTER.md' --include=*.py --include=*.js` hits only check 15's
machinery, which reads the shipped *template*). Remedy is a one-line post-deploy
touch-up per live register, tagged **[IC, post-deploy]** in the 202 — a live
register is project data, outside both payloads and outside territory, and
writing it mid-incident would break single-writer.

**Rollback.** `git revert -m 1 <merge-sha>` on `main` (the merge is `--no-ff`),
then re-run the deploy command and the witness to exit `0` — the install is
idempotent. The branch `dcs/direct-resolution-lane` is the rollback reference and
must not be deleted before `/dcs-deploy` confirms. Two things a revert does not
cover, both outside the payload: any live-register legend already touched up, and
a CHANGELOG line **if 0.6.10 has been published by then** — publish is
irreversible in practice and Owner-only, so the clean rollback window lasts only
while 0.6.10 remains unpublished. It is unpublished today: **registry reads
0.6.9, measured this session.**

## Risks

1. **The verification surface is shared even though the territories are not.**
   Mitigated by the sequential execution mode above; the *authoritative* suite run
   is the integrated one after both return, never a per-tasking one.
2. **The state literal is a cross-tasking contract with no mechanical enforcement.**
   A silent spelling divergence leaves criterion 3 red in a way per-tasking
   evidence cannot catch — each grep passes locally. Mitigated twice: S2 greps
   S1's landed literal first, and the integrated census catches it regardless.
3. **Check 15's tripwire is placement-sensitive, not word-sensitive.** The
   realistic failure is not bad prose but a specialist inserting a blank line for
   readability inside the description block, splitting one declaring paragraph
   into two. The paragraph-count evidence (`must print 5`) catches that **even
   where the suite stays green by luck**.
3b. **Two paragraphs are one character from declaring, and the IC found it, not
   the chief.** `REGISTER.md`'s header comment — **which S1 edits** — and its
   `FACTS-ONLY` block both already carry `DEPLOYED` **and** a proof word, and are
   non-declaring **only** because their arrows are ASCII `->` rather than the
   `chr(0x2192)` the check matches (`tests/test_doctrine_integrity.py:922`).
   "Tidying" one arrow into `→` would silently create a second declaring
   paragraph. Both taskings carry an explicit rule against it and S1's evidence
   reports the U+2192 count.
4. **Check 15's Rule B was removed at a prior incident's third halt**, so
   disposition-*content* agreement is checked mechanically **nowhere**. A green
   suite proves the citation is present and the paragraph count is one — it does
   **not** prove `REGISTER.md`'s `DEPLOYED` prose still agrees with `deploy.md`.
   Since S1 edits text immediately adjacent, the Safety Officer must **read** that
   description, not trust the PASS line.
5. **A register state added after the fact has no precedent in this package** —
   all six were established together in the v0.3 design. So no prior incident has
   found the stale carriers for us. Criterion 3's population is enumerated by
   command, but a command only finds sites that spell the states **literally**; a
   site that paraphrases is invisible to it. One such was found by hand at plan
   time (`close.md:239`) and is in scope.
6. **`CHANGELOG.md` is outside this repo's gate-guarded set**, so it is S2's by
   plan rather than by enforcement. The final `git status --porcelain` is what
   catches a violation.
7. **Scope pressure toward the hot path.** The instinct on "add a state and a
   convention" is to document it in `doctrine.md`. With 1,205 B of slack and a
   ratchet that must not move, `doctrine.md` and `typing.md` are **forbidden** in
   both taskings rather than merely out of scope. A specialist that judges a
   hot-path carrier necessary reports a deviation — the IC's call, not a tasking's.
8. **The version marker will be blind to this ship — confirmed, not
   hypothetical.** `~/.claude/dcs/VERSION` and `dcs/VERSION` both read 0.6.10, so
   the marker reads the same before and after. The deploy rests on the content
   witness alone. The witness baseline is currently clean (exit `0`, 47 identical),
   which is what makes the post-merge `differing` set attributable to this
   incident — protect it by not installing from a dirty tree meanwhile.
9. **Do not run `payload_check.py` from the worktree without `--repo`.** Its
   default is its own repo root, which here is the worktree, so it would report
   this incident's in-progress edits as `differing` and read as deploy drift.

## Verification plan

Run **after both specialists return**, from `C:\DCS-wt\direct-resolution-lane`.

1. **The integrated suite — the only authoritative run.**
   `test_doctrine_integrity.py` → `82/82`, zero `FAIL`, check-15 PASS line reading
   `1 paragraphs across 1 files: ['dcs/templates/REGISTER.md']`;
   `test_dcs_gate.py` → `100/100`; `test_dcs_intake.py` → `10/10`. **A total other
   than 82 is not a counting quibble** — it means the declaring population changed
   and a construction rule was broken.
2. **The cross-tasking literal.** `grep -rn '\bRESOLVED\b' dcs/ CHANGELOG.md` →
   the same token, spelled identically, in `REGISTER.md` (value list, description,
   row-template cell, header writer-map), `forms.md`, `new.md` step 7a and
   `close.md`. This is the one failure neither tasking's own evidence can catch.
3. **Criterion 3's census, re-run whole**, with `status.md` appearing
   **unchanged** — confirming the out-of-territory boundary held.
4. **Criteria 1 and 2 by command, not by line number** (the counting and
   extraction commands in the 202).
5. **The check-15 structural tripwire, independent of the suite:** the
   `DEPLOYED`-bearing paragraph count → `5`, the HEAD value. Plus the U+2192 count
   in `REGISTER.md`, which must not have increased.
6. **The original 201 repro path, walked forward** — the integrated question no
   per-tasking command answers. Re-read all three traces and confirm each now
   terminates differently; in particular the 7a block must reach a substep naming
   `.dcs/esg/REGISTER.md`, where at HEAD
   `awk '/^## 7a\./{f=1} /^## 7b\./{f=0} f' dcs/workflows/new.md | grep -c 'REGISTER'`
   returns `0`. Also confirm the field-repair grep **still returns zero** —
   correctly, because this period deliberately does *not* add that convention.
7. **Scenario-neutrality, read not grepped.** Answer explicitly in the verdict:
   would this definition serve `register-field-repair-path` and
   `trivial-work-inline-lane` unchanged?
8. **The things that must not have moved.** `git status --porcelain` → exactly
   five modified tracked files; `git diff --stat -- tests/` → empty (the
   forbidden-territory proof); `HOT_PATH_BUDGET_KB` → `37`; hot path →
   `36683 1205`; `dcs/VERSION` and `package.json` → `0.6.10`.
9. **Not mechanical, must still happen.** Read `REGISTER.md`'s `DEPLOYED`
   description and confirm S1's adjacent insertion left it intact and still citing
   `deploy.md` step 7 by the live number. Nothing checks this — see risk 4.
10. **[IC] at close, needs network:** `npm view dcs-command-system version`,
    re-measured against the plan-time `0.6.9` (criterion 9).
11. **[Owner]** Criterion 10 is UAT and is not verifiable by this plan.

## Deviation history (this period)

None — this is period 1's first IAP.
