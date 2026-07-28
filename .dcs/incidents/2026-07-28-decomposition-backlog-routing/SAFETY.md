# SAFETY — Safety Officer Verdict

**Incident:** decomposition-backlog-routing
**Period:** 1
**Verdict:** pass

Copied verbatim from the Safety Officer's return (forms.md: "copied in as returned — not summarized or softened by the IC").

```json
{
  "verdict": "pass",
  "refutations": [],
  "advisories": [
    {
      "finding": "new.md:81-86 — the all-`L` corner case is under-specified. Bullet 1 now reads \"Register every defect at `H`/`M` ... then open **one** — the one on the critical path\"; the pre-change text read \"Register every defect ... then open **one** of them\", where \"them\" was every defect. Dropping \"of them\" re-scopes the open-one instruction to the H/M set. If a stem decomposes into defects that are ALL `L` and the project documents a surface, no row is written and no set is named to open the incident from — /dcs-new could produce nothing. Not an AC1 failure: the routing bar itself stays decidable in all four cases the IAP plan named (H+surface, H-none, L+surface, L-none), and bullet 4's \"say plainly ... where they went\" makes a silent drop visible to the Owner.",
      "fix": "One clause at close: \"...then open **one** — the one on the critical path; where every defect is `L`, open the one the Owner came for and route the rest.\""
    },
    {
      "finding": "\"Harm is never `L`.\" (new.md:91-92) exists in only one of the three hunks. The doctrine.md:55 amendment and the esg.md:68-75 mirror both omit it, so the constitution — which wins on conflict in this project — is silent on the guard that stops a harm-causing defect being demoted below the bar. Risk is bounded on the esg side because routing is offered as an option inside step 3's `AskUserQuestion` round (esg.md:105), i.e. Owner-decided. Not a divergence in the three elements the IAP plan named: tier (`L`), condition (project's own `CLAUDE.md` documents a lightweight backlog-style surface) and fallback (unconditional row) agree verbatim across all three.",
      "fix": "Carry the harm clause into doctrine principle 4's parenthetical at close, or record in the AAR that the guard is deliberately stem-only."
    },
    {
      "finding": "The new cluster-(b) option widens the separately-registered `esg-intake-writeback-gap` rather than leaving it flat. I confirmed \"(b)\" appears exactly once in the whole of esg.md (line 67, the cluster definition) and that step 4's Record bullet enumerates only (a)/(c)/(e)/(f) — so cluster (b) now carries TWO decision outcomes with no write-back instruction where it previously carried one, and the new outcome's target is a file esg.md never names again. The text itself is untouched and not worsened (steps 3/4/5 byte-identical to HEAD), and the 202's out-of-scope constraint to avoid step 4's Record lines was honoured in full.",
      "fix": "At close, amend the `esg-intake-writeback-gap` register row's scope to name both branches (queue → REGISTER.md, and route → the project-documented surface), so its eventual fix does not land half-done."
    },
    {
      "finding": "Both files this incident enlarged are now close to their ceilings, and the next edit to either goes red: hot path 37,735 / 37,888 bytes (153 left), new.md 248 / 250 lines (2 left). esg.md is comfortable at 159 / 250. Regenerate with the guard's own method, not `wc -l` — CRLF→LF-normalised byte count over `dcs/references/doctrine.md` + `dcs/references/schemas.md` for the hot path, and `_workflow_line_count` in `tests/test_doctrine_integrity.py:1273` for lines (it adds 1 for content after the last LF, where `wc -l` under-counts by exactly one).",
      "fix": "Note the measured headroom plus its regenerating command in the AAR; treat doctrine.md and new.md as budget-blocked for the next incident until a trim."
    },
    {
      "finding": "`(v0.6.13)` appears exactly three times, one per touched file (doctrine.md:55, new.md:87, esg.md:68), while `dcs/VERSION` and `package.json` both read `0.6.12`. This was ruled in-scope at command point 2 (`214-LOG.md:29`), so it is not a defect — but nothing mechanical will catch a missed bump: the merge guard's version-sync check compares `dcs/VERSION` against `package.json` only, and never compares either against a prose version label.",
      "fix": "Close must bump both files in the same commit (CLAUDE.md: \"Version sync is atomic\"). Manual step — no test covers it."
    },
    {
      "finding": "new.md:81-82 calls `H`/`M`/`L` \"the register template's vocabulary\"; `dcs/templates/REGISTER.md:150`'s Priority placeholder is actually `{{H\\|M\\|L or rank}}`. The branch stays total because the step mandates the stem propose one of H/M/L, and this project's live register writes both (`**L (rank 12)**`), so nothing is un-followable — but the parenthetical slightly overstates what the referenced file says.",
      "fix": "Optional: \"(`H`/`M`/`L`, the register template's letter tiers)\"."
    }
  ],
  "checked": [
    "git diff -U15 on all three files in C:\\DCS-wt\\decomposition-backlog-routing — 3 files, +21/-8, matching the declared union of territories exactly; git status --porcelain -uno and git diff --cached --stat confirm no fourth tracked file and nothing staged, so no forbidden-zone violation against S1's list (esg.md, schemas.md, doctrine-appendix.md, VERSION, package.json) or S2's (new.md, doctrine.md, schemas.md, VERSION, package.json)",
    "AC1 repro walk on the rendered text at new.md:81-92, all four IAP cases: H+surface -> row (bullet 1); H+no surface -> row; L+surface -> project surface (bullet 2); L+no surface -> \"the row is written as before\". Every branch decidable from text alone, no reader judgment call",
    "AC1 no-hardcoded-path: per-token grep over ADDED diff lines only -- vault 0 hits, Backlog.md 0, backlog.md 0, C:\\DCS 0, C:/DCS 0. The three case-insensitive hits are all the generic descriptor \"backlog-style surface\"",
    "S1's \"pre-existing baseline text\" characterization of the vault mention, checked rather than accepted: diff of doctrine.md:114-118 HEAD vs worktree is empty -- the string is \"query the vault before a non-trivial fix\", a quoted illustration of a foreign project's protocol inside the \"Relationship to project-specific protocols\" section, untouched by this diff",
    "S1's \"restored a missing word\" claim, checked independently: git show HEAD:dcs/references/doctrine.md line 55 reads \"A stem that finds several registers each of them\" -- the word was genuinely absent; git log -S dates the omission to 2fd1aea (v0.5.12), so it is a pre-existing typo in the sentence under amendment, not new scope",
    "AC2: esg.md:68-75 adds the mirror to cluster (b); esg.md:105 confirms step 3 is \"One AskUserQuestion round per decision cluster above\", so \"one of step 3's options\" satisfies the criterion's AskUserQuestion wording",
    "AC2 scope containment (IAP plan item 8): diff of HEAD esg.md lines 96-152 against worktree lines 103-159 returns empty -- steps 3, 4 and 5 byte-for-byte unchanged, so esg-intake-writeback-gap is neither silently fixed nor silently worsened in text",
    "AC3: principle numbering extracted from both HEAD and worktree doctrine.md and diffed -- identical, 24 numbered items, sequence 1..4, 1..9, 9b, 10..15, 1,2,3,5 unchanged; the amendment is one line in place inside principle 4, no principle added, principle 4 still principle 4",
    "AC4, my own fresh runs in the worktree: python tests/test_doctrine_integrity.py -> 86/86 passed; python tests/test_dcs_gate.py -> 100/100 passed; python tests/test_dcs_intake.py -> 10/10 passed",
    "IAP plan item 3, three hunks side by side, mechanically: all three carry tier L, all three carry the condition (CLAUDE.md + \"backlog-style surface\"), all three carry the unconditional fallback (\"stands as before\" / \"written as before\" / \"exactly as today\"). Only divergence found is the extra \"Harm is never L\" in new.md -- advisory 2",
    "IAP plan item 5, budgets measured with the guard's own method (CRLF->LF normalised bytes; _workflow_line_count, not wc -l): hot path 37,458 -> 37,735 (+277) against cap 37,888; new.md 242 -> 248 against 250; esg.md 152 -> 159 against 250. All under, and all three match the specialists' claimed numbers",
    "Cross-references resolve, checked against the file rather than the test: both workflows cite doctrine's \"Relationship to project-specific protocols\" -- heading exists verbatim at doctrine.md:114, and the guard's own \"doctrine sections referenced by name exist\" check (test_doctrine_integrity.py:273) is green with the new text present",
    "Package-wide grep for other readers of the changed steps (step 4a, cluster (b), decision cluster across dcs/, agents/, skills/): only doctrine.md:55 and esg.md:69, both updated in this diff; plan.md's \"step 4a\" hits are its own tasking-lint step, unrelated namespace",
    "Encoding audit on all three touched files (CLAUDE.md flags BOM as a twice-shipped defect here): UTF-8 decodes, no BOM, zero CRLF",
    "Live-register cross-check of the new vocabulary against C:\\DCS\\.dcs\\esg\\REGISTER.md: rows write **L (rank 12)**, **M (rank 8)** -- the H/M/L tiers the new bar keys on exist in practice, so the step is followable in this project today",
    "Confirmed this is a first verification, not a re-verify: no SAFETY.md in the incident directory and no SAFETY-HALT: sentinel in 214-LOG.md (last entry is IAP-APPROVED: 279b72f4f944), so nothing was cited by reference from a prior verdict"
  ]
}
```

## IC resolution of each advisory (execute.md step 9: "record each advisory and its resolution")

1. **All-`L` decomposition edge case — deferred, not fixed inline.** `new.md` sits at 248/250 lines (2 lines of headroom); a same-commit fix here risks reopening the budget question this incident was careful to respect, for an edge case (every split-out defect landing at `L` simultaneously) that is uncommon in practice — the incident is normally opened because *something* in scope is worth acting on now. Routed to `vault/Backlog.md` at close instead of a register row, matching the very principle this incident just implemented: a small, low-priority wording gap belongs on the lightweight surface, not the register.
2. **"Harm is never `L`" absent from doctrine.md/esg.md — recorded as deliberately stem-only, not fixed inline.** Same budget reasoning (`doctrine.md` hot-path headroom is 153 bytes). The esg.md side is already Owner-mediated (`AskUserQuestion`), which bounds the practical risk. Noted in the AAR as an accepted asymmetry, and in `vault/Backlog.md`.
3. **`esg-intake-writeback-gap` scope widened — fixed now.** `.dcs/esg/REGISTER.md`'s row for that incident has been updated (2026-07-28) to name both cluster-(b) outcomes needing a write-back instruction, not one. This is `.dcs/esg/**` bookkeeping, outside guarded source territory and outside this IAP's own partition, so it needed no specialist and no re-verification.
4. **Budget headroom — recorded in AAR**, with the regenerating commands (principle 15), not fixed (nothing to fix — it's a measurement, not a defect).
5. **Version-label sync — deferred to close**, per this incident's own IAP risk note and command-point-2 ruling: `dcs/VERSION` and `package.json` bump to `0.6.13` in the close commit, atomically (CLAUDE.md: "Version sync is atomic").
6. **"Register template's vocabulary" slightly overstates the template — deferred, optional.** Routed to `vault/Backlog.md` alongside advisory 1; not worth the remaining `new.md` headroom for a wording nuance with zero functional effect (the step already names the literal tiers `H`/`M`/`L`).

None of the six advisories cleared `agents/dcs-safety-officer.md` step 6's halt bars — no re-verification was triggered, per doctrine's "never upgrade an advisory to a halt to be thorough."
