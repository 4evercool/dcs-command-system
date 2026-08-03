# SAFETY — Verdict (Operational Period 1)

**Incident:** spawn-effort-control
**Period:** 1
**Attempt:** 1

## Verdict (verbatim, as returned by dcs-safety-officer)

```json
{
  "verdict": "pass",
  "refutations": [],
  "advisories": [
    {
      "finding": "doctrine-appendix.md:695 (D5) states the removed items were \"both already established two paragraphs earlier in the same section\". Half false. The `dcs-commander`/`model: fable` framing is established (doctrine.md:20), but the definition `\"Fable\" = the strongest tier available` appears nowhere earlier — `grep -n \"strongest tier\" dcs/references/doctrine.md` returns line 31 only, and doctrine.md:17/19/20 name Fable solely as a seat and a model value. No operational harm (a Dispatcher passes `model: fable` per line 20 and falls back per line 31 without needing the gloss), but the provenance note is inaccurate.",
      "fix": "Amend D5's parenthetical to claim only the `model: fable` framing, or spend ~6 of the 54 free bytes restoring a gloss to doctrine.md:31."
    },
    {
      "finding": "D5's \"Removed:\" list for passage (1) discloses the `(v0.6.1)` tag and the explanatory tail, but not two further losses: the normative **MUST** and the bold emphasis on `Availability is per-spawn and MUST be re-tested at every command point (v0.6.1)`, now the plain `Availability is re-tested at every command point.` Substance holds (the sentence still states the rule unconditionally, `per spawn` is restored in the paragraph lead, and doctrine-appendix.md:63 still calls re-testing \"mandatory\"), so criterion 4 is met — but an undisclosed MUST removal is exactly the silent normative erosion the appendix exists to prevent.",
      "fix": "Restore `MUST` (5 bytes of the 54 free), or add both losses to D5's \"Removed:\" list."
    },
    {
      "finding": "The field lesson (doctrine-appendix.md:97) cites verification \"against the Agent tool's own parameter schema\". The incident's own record cites a different source: 214-LOG.md, 2026-08-03T14:14:16 — \"consulted claude-code-guide\", matching 201-BRIEF.md:128 (\"verified via `claude-code-guide`\"). I have no Agent/Task tool in this session and cannot confirm the appendix's stated method; the underlying claim is independently corroborated (`grep -ri effort agents/` exits 1). Separately, a platform-capability absence is a principle-15 derived fact with a lifetime and carries no `as of … — it moves` annotation; 201-BRIEF.md:152 anticipated it (\"upgrades transparently if/when a real per-call effort parameter ships\") but the appendix does not.",
      "fix": "Name the source the log actually records (or both), and add an explicit re-check trigger — e.g. \"as of 2026-08-03; recheck when a per-call effort parameter ships\"."
    },
    {
      "finding": "D5's heading reads \"two relocations\", but passage (2) was compressed in place under its unchanged heading (`### Project-supplied provision hook (v0.7.1)` is still at doctrine.md:156) — the body says so correctly at doctrine-appendix.md:697. D5's \"Removed:\" list for (2) is also non-exhaustive: it omits \"content and\" (from \"the script's content and correctness\") and \"the incident proceeds with a note that provision returned non-zero\".",
      "fix": "Retitle to \"one relocation, one in-place compression\" and complete the \"Removed:\" list."
    },
    {
      "finding": "Optional strengthening against criterion 8's \"grounded in real DCS work\": both worked examples (doctrine-appendix.md:103-116) are archetypes, not actual incidents. They live in doctrine-appendix.md, where the D1-D4 convention and tasking (f) both permit citing this repo's incident slugs — permitted, but unused.",
      "fix": "Optionally anchor one example to a real slug from `.dcs/incidents/`. Criterion 8's operative requirement (a clear discriminator, not an unguided judgment call) is already met without this."
    }
  ],
  "checked": [
    "Read the full diff myself: `git diff 5e17284e56c85c599ae75efbd35fa7f258a74459 -- dcs/references/doctrine.md dcs/references/doctrine-appendix.md` — 8 changed lines in doctrine.md, 46 added in the appendix.",
    "`git diff --name-only 5e17284…` returns exactly the two claimed files; `git status --porcelain` shows only the untracked incident directory. No forbidden-zone file touched.",
    "Ran all three suites myself: test_doctrine_integrity.py 156/156, test_dcs_gate.py 100/100, test_dcs_intake.py 18/18; `grep -c '^FAIL'` = 0 on each.",
    "Re-derived the budget independently with my own read_bytes/CRLF-normalised command: doctrine=23872, schemas=13962, sum=37834, free=54 (<=37888). Matches the specialist's figures exactly.",
    "Confirmed `HOT_PATH_BUDGET_KB = 37` at tests/test_doctrine_integrity.py:212 and that `git diff --quiet 5e17284… -- tests/` is empty — no ceiling raise.",
    "Read the whole `## Transfer of command` section (doctrine.md:15-37) and every tier/model mention in the file. Exactly one rule governs per-spawn tier selection (line 31); line 45 is a seat default and line 36's \"next tier\" is the pre-existing, unchanged liveness re-spawn — criterion 2 holds.",
    "Re-ran all five guarantee anchors with `grep -F`: all HIT. `grep -niE 'xhigh|x-high|low/medium/high|low-medium-high' doctrine.md` exit 1; `grep -ri effort agents/` exit 1.",
    "Confirmed both empty-diff claims with `git diff --quiet 5e17284… -- dcs/workflows/ agents/ dcs/templates/ tests/ dcs/references/schemas.md` (exit 0).",
    "Byte-compared all four relocated passages against `git show 5e17284…:dcs/references/doctrine.md` in Python: the Model-availability paragraph and all three provision-hook paragraphs are verbatim in the D5 blockquotes, zero drift.",
    "Derived the funding arithmetic myself (dispatcher note 1): baseline free was 17 bytes; the rewritten paragraph grew 524 -> 865 (+341); the provision trim saved exactly 378; net -37. The paragraph's own compression was mathematically insufficient — the five mandated verbatim anchors alone consume ~200 of the 541 bytes that would have been available — so tasking (d)'s escalation path was correctly triggered, not exceeded.",
    "Verified the new cross-reference resolves: doctrine.md:31 points at doctrine-appendix.md, \"Transfer of command\"; that section exists at doctrine-appendix.md:46 and both worked examples (103-116) sit inside it.",
    "Verified principle numbering by reading doctrine.md:50-69 — 1..16 plus 9b, no new principle added.",
    "Read the appendix's own citation convention (doctrine-appendix.md:11-30) and confirmed both new entries use the post-self-hosting form (slug in backticks).",
    "Proved the merge guard's check 20 examined the new entry non-vacuously: ran its own `_FL_LINE_RE`/`_FL_ID_RE` against doctrine-appendix.md line 92 — line matches, identifier co-located on the same line.",
    "Encoding: both files have no BOM, zero CRLF, no Cyrillic, valid UTF-8.",
    "Read the 201 repro path (201-BRIEF.md:158-176). The two in-scope steps are closed: step 2 (\"doctrine.md:31's only per-spawn dynamic-tier rule is availability-driven, not complexity-driven\") is now false, and step 4 (no mechanism for the ~90% of spawns that never touch dcs-commander) is answered by the per-call `model` override. Steps 1 and 3 (charter defaults, schemas.md #6) are explicitly out of scope for this period.",
    "Confirmed doctrine.md is `@`-included at every workflow spawn call-site (new.md:10, plan.md:8, execute.md:9, esg.md:12, plus close/deploy/init/loop/run) and that doctrine-appendix.md ships (package.json `files` includes `dcs/`), so the pointer is reachable by a spawned agent.",
    "Read 204-TASKING/S1.md and cross-checked territory, mandates (a)-(g) and evidence requirements against the diff; read 214-LOG.md including the IC's command-point-2 ruling on the criterion 2 bright line.",
    "Cross-checked the appendix's capability claim against 201-BRIEF.md:126-156 and 214-LOG.md — the Workflow-tool hedge (\"unconfirmed as a shipping capability\") accurately reflects what was found and does not overstate."
  ]
}
```

## Disposition

`pass`, 0 refutations, 5 advisories. All five are artifact-hygiene findings
in the new `### D5:` appendix entry's own provenance/disclosure text —
none clears a refutation bar (agents/dcs-safety-officer.md step 6): the
deliverable (doctrine.md's rule, the appendix field lesson and worked
examples) is sound, and the acceptance criteria are met. The IC folds all
five into the integration commit per execute.md's advisory clause.
