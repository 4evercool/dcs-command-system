# Post-mortem: prompt-vs-schema-drift

**Incident:** prompt-vs-schema-drift (Type 1, 1 period, 2026-07-29)
**Merge:** `6d3d08e` (5 files, +214/-27)

## What happened

DCS had no mechanical validation that dispatcher prompts and agent returns conform to declared schemas. Inbound: the dispatcher named fields the schema didn't have (`checks_run` instead of `checked`, `findings[]` instead of `evidence[]`). Outbound: agents returned unstructured prose or wrong field names. v0.6.14 fixed the on-disk half (machine-readable contracts + checks 18/19). This incident fixed the off-disk half — workflow-level validation at dispatch and receipt.

## What changed

1. **Inline schema contracts in workflows** — new.md, plan.md, execute.md now list the required fields for each agent role directly in the spawn prompt prose. The agent sees the contract it must conform to.

2. **Return validation instructions** — after each agent return collection, the workflow now instructs the dispatcher to validate: JSON block present, required fields present, no fields outside schema.

3. **Commander examples** — all 4 JSON examples now include `esg_activation: null`.

4. **Check 20 (inbound field-presence guard)** — verifies every required schema field appears in backtick context in the workflow that spawns that agent type. 5 cases.

5. **Check 21 (outbound missing-required-fields guard)** — walks historical incident artifacts and reports field mismatches as informational (not blocking).

## What worked well

- The inline-contract approach was simpler than expected — no new hooks or runtime infrastructure needed. A backtick-enclosed field name in workflow prose is visible to both the agent and the test.
- Check 20's discovery-based design (parses schema sections, parses workflow files, compares — no hardcoded field names or file paths) follows the same discipline as checks 13-19.
- Sequential S1→S3 execution was correct: S3's line-count measurements needed S1's actual output.

## What surprised us

- S1's reformatting of citation anchors (removing `references/` prefix, changing comma to parenthesis) broke check 13 silently. The fix was one word per citation — adding the section's short title right after `#N`.
- The first S1 spawn failed on API error mid-edit, leaving partial changes on disk. The second spawn found new.md and plan.md already done. This is both efficient (no rework) and risky (no agent verified the partial work — check 20 caught it post-hoc).

## Key numbers

- 120/120 tests (from 115 baseline, +5 check-20 cases)
- 5 files modified, 214 insertions, 27 deletions
- Line counts: new.md 248→255 (+7), plan.md 666→682 (+16), execute.md 424→445 (+21)
- 3 workflow spawn points covered, 6 agent roles, 5 schema sections
- 4 specialist spawns (S1, S1-FIX, S2, S3) + 1 Safety Officer
- 0 refutations, 0 advisories, 1 clean Safety pass
