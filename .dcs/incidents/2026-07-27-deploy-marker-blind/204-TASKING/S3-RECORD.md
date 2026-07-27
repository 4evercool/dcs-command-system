# 204 — Tasking S3-RECORD (revision 2)

**Incident:** deploy-marker-blind · **Period:** 1 · **Revision:** 2
**Specialist:** dcs-ops-specialist (S3-RECORD) — fresh spawn
**Runs THIRD**, after S1-CONTRACT and S2-GUARD. You describe what they
actually landed.

## Task — criteria 7 and 8, the CHANGELOG advisory, and the end-state census

1. **Extend the CHANGELOG entry in the EXISTING, UNPUBLISHED `## 0.6.10`
   section.** Never a new version heading, no version bump; `package.json`
   and `dcs/VERSION` untouched. **Re-measure `npm view dcs-command-system
   version` first and record it** — it read `0.6.9` at plan time and at
   both prior plan times, and it will move eventually. Measure, do not copy.
2. **Close the open advisory.** The existing Changed entry lists the
   surfaces describing the contract as *"CLAUDE.md's Deploy table,
   REGISTER.md's DEPLOYED definition and skills/dcs-deploy/SKILL.md"* and
   **omits `dcs/workflows/close.md`**, which revision 1 also changed.
   **Rebuild the surface list from `git diff --stat` at end state**, not
   from the previous entry.
3. **Add the new material:** the one-source-plus-citation contract shape,
   the durable guard (check 15) and the shared-constants check (check 16),
   and `docs/spec-v0.3-parallel.md`'s supersession marker if S1 added one.
   **Describe what the guard ENFORCES, not that it was added.**
4. **Do not restate the contract's dispositions** in prose that would read
   as a second declaring statement. `CHANGELOG.md` is **outside check 15's
   walk by design** — it is a dated record, and holding it to live text
   would rewrite history — so the guard will not catch you. Describe the
   change; cite `` `dcs/workflows/deploy.md` step 7 `` for the contract.
5. **Produce the integrated end-state census** for the Safety Officer
   (below).

## File territory (may edit ONLY this)

`CHANGELOG.md`

## Forbidden zones

`dcs/**` · `agents/**` · `skills/**` · `tests/**` · `docs/**` ·
`CLAUDE.md` · `README.md` · `install.ps1` · `install.sh` ·
`package.json` · `dcs/VERSION` · `bin/**` · `.dcs/**`

**No install, no deploy.**

## Evidence required in the return

1. `npm view dcs-command-system version` — the **re-measured** value, and
   the CHANGELOG heading it justifies writing under. Criterion 7 requires
   the re-measurement, not the plan-time value.
2. `git diff CHANGELOG.md` in full, plus `grep -n '^## ' CHANGELOG.md | head`
   showing your entry sits in the existing 0.6.10 section.
3. `git diff --stat` at end state alongside the surface list your Changed
   entry names — **they must agree file for file.** This is the advisory
   being closed.
4. **Criterion 8:** all three suites, each read from its **own**
   `N/M passed` line **and exit code** — `python tests/test_dcs_gate.py`,
   `python tests/test_dcs_intake.py`, `python tests/test_doctrine_integrity.py`.
   Quote the lines; do not restate counts from anywhere else. The integrity
   suite's total will have moved past 73 with checks 15 and 16 — **read the
   live line, never a number written down.**
5. **END-STATE CENSUS for the Safety Officer.** Re-run criterion 5's
   binding enumerator **and both sides of criterion 5a's negative control**
   at final state; paste all output with counts; and state for each hit
   which tasking owns it and whether it was changed or annotated. **If any
   hit is unaccounted for after S1's walk, say so rather than closing.**
6. **The 201's reproduction path, re-derived at end state:**
   `git merge-base --is-ancestor aab9f06 0.6.10` — still exit 128, because
   **the defect in the world is unchanged; what changed is that the
   workflow now has defined behaviour for it.** And
   `python tests/payload_check.py` run **read-only** against the untouched
   install, with its four-class output pasted. **No install, no deploy.**

## On discovering the plan doesn't fit reality

STOP. Return `status: "deviation"` per `schemas.md` #4.
