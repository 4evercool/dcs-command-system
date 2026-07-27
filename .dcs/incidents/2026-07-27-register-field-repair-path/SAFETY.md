<!--
SAFETY.md -- written by the Safety Officer, verbatim, per doctrine forms.md.
Not summarized or softened by the IC. This incident had three Safety Officer
spawns in period 1 (revision 1's first pass, revision 2's pass, and revision
2's scoped repair re-check); all three verdicts are recorded below in full,
in order, because 214-LOG.md's entries about them are IC summaries, not the
substitute for this file.
-->

# SAFETY — Period 1

**Incident:** register-field-repair-path

## Verdict 1 (revision 1, 2026-07-27T18:43:41+11:00) — HALT

```json
{
  "verdict": "halt",
  "refutations": [
    {
      "claim": "204-TASKING/S2.md line 42 states as fact: \"NO version bump, NO new version heading, NO edit to `dcs/VERSION` or `package.json` -- 0.6.10 is unpublished and this rides in it, exactly as `direct-resolution-lane` did.\" 202/IAP criterion 6 accordingly requires the entry to land in \"the current open (unpublished) version's section\", and S2 reports it added the entry under the existing `## 0.6.10 — 2026-07-26` / `### Added` heading with no version bump.",
      "evidence": "0.6.10 is PUBLISHED, and was already published before this incident opened. Measured two independent ways this session. (1) `npm view dcs-command-system time --json` -> `\"0.6.10\": \"2026-07-27T05:39:23.099Z\"` = 2026-07-27T16:39:23+11:00. The incident's own `201-BRIEF.md` mtime is 2026-07-27 17:28:27+11:00 and `204-TASKING/S2.md` is 17:54+11 -- the publish preceded the 201 by 49 minutes and the tasking's claim by 75. This is not the world moving mid-incident; the premise was false when written. (2) I downloaded the registry tarball (`npm pack dcs-command-system@0.6.10`) and diffed it: the published `CHANGELOG.md` is BYTE-IDENTICAL to repo HEAD's `CHANGELOG.md` (`diff <(git show HEAD:CHANGELOG.md) package/CHANGELOG.md` -> no output), published `dcs/VERSION` is `0.6.10`, and `grep -rn \"field repair\" package/dcs/ package/agents/` in the published payload returns ZERO hits. So the `## 0.6.10` section is a shipped, closed section, and the working tree now adds a fourth `### Added` bullet to it. CONSEQUENCE: `CHANGELOG.md` (user-facing; `README.md#upgrading` routes readers to it, and its own preamble says entries are \"written from the repository's own artifacts... not from recollection\") now tells anyone who installed 0.6.10 that they have `RESOLVED (field repair)`. They do not. This reproduces exactly the defect the 0.6.10 section's own header was cut to correct: \"0.6.9 shipped twice with different contents. If you installed 0.6.9, take 0.6.10.\" Bar cleared two ways per step 6: acceptance criterion 6 covers it EXPLICITLY (\"current open (unpublished)\"), and it is operational harm in a shipped, user-facing artifact. Nobody ran the registry marker `npm view dcs-command-system version` that `CLAUDE.md` documents for precisely this question -- grepping every incident artifact for \"npm view|unpublish|registry marker\" returns only the three places that ASSERT 0.6.10 is unpublished, and none that measured it. NOTE FOR THE IC, not a fix I am authorizing: `CHANGELOG.md` has no `Unreleased` heading convention (`grep -n '^## ' CHANGELOG.md` -> every heading is a concrete version), and a version bump is explicitly out of scope this period, so this cannot be resolved by re-running S2 alone."
    }
  ],
  "advisories": [
    {
      "finding": "S2's claim \"citing S1's convention by name, restating none of its rules\" is not accurate. `dcs/workflows/esg.md` step 4's new bullet restates a rule the declaring block also states: \"verify the commit reference (`git show <sha> --stat`) before writing the row, since its facts are reported rather than observed\" vs REGISTER.md's WRITER paragraph \"verify the commit reference first (`git show <sha> --stat`) before the row is written.\" Two files now carry that rule; changing one leaves the other stale. I did NOT treat this as a criterion-3 failure: esg.md names its authority (\"per the register template's `RESOLVED (field repair)` convention (`dcs/templates/REGISTER.md`)\"), it narrates a workflow ACTION rather than defining the convention (check 15's own declaring predicate calls that shape a false positive, per the comment at tests/test_doctrine_integrity.py:996-1017), and the file's existing shipped idiom already does restate-plus-cite (\"same fallback as `close.md` step 5a.4\").",
      "fix": "Either drop the restated clause and let the citation carry it, or leave it and accept the house-style precedent -- but correct the specialist's claim in the AAR so the next reader does not inherit \"restating none of its rules\" as fact."
    },
    {
      "finding": "The CELLS paragraph enumerates Type, Priority, Worktree, Branch, Opened, Closed and Outcome, but not Territory or Intake source. I ran IAP verification item 4 (read-through against `C:\\DCS\\.dcs\\esg\\REGISTER.md` line 91, `package-json-description-corruption`, read-only, not edited): a Chief of Staff holding only the block cannot derive those two cells from it. The generative rule (\"every cell that would otherwise record a DCS act\") arguably reaches them, but does not say so. Criterion 1 names only Worktree/Branch/Opened/Closed, all four of which ARE specified -- so this is a gap in the read-through, not in the criterion.",
      "fix": "One clause in the CELLS paragraph: Territory = the paths the fix touched (from the verified commit), Intake source = the Owner report at /dcs-esg."
    },
    {
      "finding": "Principle 15: the WRITER paragraph carries a census with no regenerating command beside it -- \"Every other writer of this file either transitions a row that already exists or originates one into QUEUED/ACTIVE; this is the one writer that ORIGINATES a row directly in a terminal state.\" I re-measured it rather than trusting it, and it is TRUE today (`dcs/workflows/new.md` 7a.5 is update-only: \"If ... holds a row for this incident, set that row's state to `RESOLVED` ... Otherwise -- no register, or no matching row -- do nothing\"; `close.md`:245 is `ACTIVE` -> `RESOLVED`; deploy is `MERGED` -> `DEPLOYED`). But it is a shipped 'all X are Y' claim with no way to regenerate it, in a template whose writer map is the subject of a still-QUEUED incident (`register-writer-map-completeness`).",
      "fix": "Add the command beside it, e.g. `grep -rn \"REGISTER.md\" dcs/workflows/*.md`, or hand the census to `register-writer-map-completeness` and keep only the distinguishing property here."
    }
  ],
  "checked": [
    "git status --porcelain --untracked-files=all in C:\\DCS-wt\\register-field-repair-path -- exactly 3 modified files, nothing untracked outside .dcs/incidents/. Territory discipline verified: S1 stayed in REGISTER.md, S2 in esg.md + CHANGELOG.md, no forbidden-zone crossing.",
    "git diff (full, read line by line) -- confirms IAP verification item 7: no doctrine.md, schemas.md, forms.md, new.md, VERSION, package.json, tests/**, dcs/hooks/**, bin/**, installer.",
    "python tests/test_doctrine_integrity.py (independent re-run) -- 82/82 passed. Criterion 4 MET at the suite's own reported count.",
    "python tests/test_dcs_gate.py (independent re-run) -- 100/100 passed.",
    "python tests/test_dcs_intake.py (independent re-run) -- 10/10 passed.",
    "Check 15's three PASS lines read from my own run, unchanged.",
    "grep -rn \"field repair\" dcs/ agents/ skills/ -- 6 hits, classified: REGISTER.md declaring block DECLARING (the one site); REGISTER.md's RESOLVED-clause hits CITING; esg.md hits CITING. Exactly one declaring site. Criterion 3 MET.",
    "Read dcs/templates/REGISTER.md in full -- criterion 1 MET.",
    "State-enum line -- exactly seven tokens, no eighth. IAP verification item 5 MET.",
    "Re-measured S1's token claims myself: DEPLOYED 7 now and at HEAD; U+2192 0 now and at HEAD. Unchanged as claimed.",
    "Re-measured the WRITER paragraph's census against new.md/close.md/deploy writers -- criterion 2 MET.",
    "Read IAP.md \"Criterion 5, answered\" -- present and coherent. Criterion 5 MET.",
    "IAP verification item 8: exactly one comment closer, renders as comment only.",
    "grep -nE '^\\([a-g]\\)' dcs/workflows/esg.md -- items (a)-(f) unmoved; (g) appended.",
    "Read package-json-description-corruption row read-only for the integrated read-through -- confirms the convention has teeth (that row's Outcome carries a bare sha and no Safety-look statement, both forbidden by the new OUTCOME MINIMUM).",
    "npm view dcs-command-system version/time/versions -- 0.6.10 is latest published.",
    "git log -- HEAD (33efabc) precedes the npm publish, i.e. the publish was cut from this tree.",
    "npm pack dcs-command-system@0.6.10, extracted -- published payload has RESOLVED, ZERO hits for \"field repair\".",
    "diff HEAD:CHANGELOG.md vs published tarball CHANGELOG.md -- IDENTICAL. Decisive evidence for the refutation.",
    "grep for npm-view/unpublish/registry-marker mentions across the incident directory -- only assertions, no measurement.",
    "ls --time-style=full-iso on incident artifacts and touched files -- all after the publish."
  ]
}
```

## Verdict 2 (revision 2, 2026-07-27T20:43:41+11:00) — HALT

```json
{
  "verdict": "halt",
  "refutations": [
    {
      "claim": "202 revision 2 and IAP.md both assert \"Acceptance criteria 1-5: unchanged from revision 1, already Safety-verified... Not reopened this revision\" -- i.e. criterion 5 (\"The plan states explicitly, with a one-line reason IN THE IAP, whether esg.md/doctrine.md need a carrier... rather than leaving the question implicit\") is still satisfied by the artifacts on disk.",
      "evidence": "It is not. The revision-2 rewrite of IAP.md deleted the section that satisfied it. grep -n -i 'criterion 5|carrier|doctrine\\.md|trivial-work-inline' IAP.md returns exit 1, zero hits. Its headings are only: Objectives / Tactics / File-territory partition / Risks / Verification plan / Deviation history -- no \"Criterion 5, answered\". 214-LOG.md line 11 is the direct record that revision 1's IAP did carry it (\"IAP.md written, integrating 202+203+204, criterion 5's answer, partition table, risks...\"), and the reasoning now survives only outside the plan: as a one-clause summary in 214-LOG.md line 10, and quoted secondhand in the register row at REGISTER.md line 94. Criterion 5's deliverable IS IAP text -- this is a refutation, not an advisory. The AAR at /dcs-close will be written from this IAP."
    },
    {
      "claim": "IAP.md: criteria 1-5 are \"protected by the pinned-hash evidence requirement in 204-TASKING/S3.md\" -- the mechanism the plan names as its substitute for re-verification.",
      "evidence": "That protection does not cover criterion 5, and the plan does not say so. Reproduced the pin myself: git diff -- dcs/templates/REGISTER.md dcs/workflows/esg.md | sha256sum = b2450322f3a1bb848c474bab1285ea772cf1a65cc0e2608a935f31ffb5e81f8a, matching exactly. But its pathspec is two payload files only. Criteria 1-4's deliverables live in those files; criterion 5's deliverable is IAP prose, tagged [IC] precisely because specialists are barred from .dcs/** -- so no tasking artifact carries it either, and .dcs/** is unguarded in .dcs/config.json, so dcs_gate.py never saw the deletion. The one criterion whose object sat outside the pin is the one that was destroyed, and the false protection claim is why it passed unnoticed through the IAP rewrite, two IC re-verifications, and Owner approval."
    }
  ],
  "advisories": [
    {"finding": "Main checkout C:\\DCS still has an uncommitted CHANGELOG.md modification (145 insertions/2 deletions) touching the same preamble region this branch edits.", "fix": "Owner commits or stashes it before /dcs-close's --no-ff merge, which will otherwise refuse outright."},
    {"finding": "The bullet's \"the same qualifier shape as MERGED (deploy pending) in 0.6.10\" reads ambiguously (\"in <version>\" usually means \"introduced in\"); satisfied literally, wording only.", "fix": "\"as described in 0.6.10\" or \"MERGED (deploy pending) (v0.3)\"."},
    {"finding": "IAP.md tactic 4 cites test_doctrine_integrity.py lines 947-964 for the CHANGELOG exclusion; actual range is 947-969, and a line range is an uncited derived fact (principle 15).", "fix": "Cite by content: grep -n 'CHANGELOG.md and docs/ are' tests/test_doctrine_integrity.py."},
    {"finding": "Carried from revision 1, re-confirmed live: esg.md step 4's bullet still partially restates the WRITER paragraph's commit-verification rule rather than only citing it.", "fix": "Trim to citation, or accept as a deliberate operative reminder."},
    {"finding": "Carried from revision 1: WRITER paragraph's writer-census claim still uncited (principle 15); CELLS paragraph still silent on Territory/Intake source (not a criterion-1 failure).", "fix": "Add the regenerating command beside the census."},
    {"finding": "## Unreleased ships as an undocumented convention; confirmed harmless for now (no workflow reads/writes CHANGELOG.md).", "fix": "Ensure the promised /dcs-esg follow-up candidate is actually registered before close."}
  ],
  "checked": [
    "Read the full git diff HEAD for all three files myself, not the specialists' summaries.",
    "npm view dcs-command-system version/time -- premise re-measured live, matching to the millisecond.",
    "npm pack + tar extraction; sha256 of published CHANGELOG.md = 9ae04cccee1304ca9d5181e6742a177b0788004c425e7598723f053f9ce46c82, identical to git show HEAD:CHANGELOG.md.",
    "Byte-level Python comparison (finer grain than the tasked awk/diff): the 0.6.10-onward tail is byte-identical in both published tarball and edited worktree file; the tarball's head is an exact byte prefix.",
    "git diff --numstat HEAD -- single hunk in CHANGELOG.md, zero deletion lines; git status --porcelain clean otherwise.",
    "Reproduced the pinned hash myself -- criteria 1-4's payload work confirmed byte-for-byte untouched.",
    "git diff HEAD -- dcs/VERSION package.json empty; no version bump anywhere.",
    "All three suites independently: 82/82, 100/100, 10/10. Check 15's declaring-population line unchanged.",
    "Manual read of the new section: --- separators both sides, no date, no false 'Shipped by incident' line.",
    "Verified every factual claim inside the new bullet against the source files.",
    "Independently re-measured the criterion-2 census.",
    "Confirmed state enum still exactly 7 tokens.",
    "Encoding: no BOM, 0 CRLF, valid UTF-8, ends with newline.",
    "Verified the non-destructiveness argument: merge 05d63b0 (05:03:14Z) precedes publish (05:39:23Z).",
    "Read test_doctrine_integrity.py lines 940-975 to confirm the CHANGELOG.md exclusion.",
    "Read .dcs/config.json -- CHANGELOG.md matches neither guarded_paths nor unguarded_paths; noticed .dcs/** is equally unguarded, which is how the IAP.md deletion went unseen.",
    "Grepped the entire incident directory for the criterion-5 answer before halting -- confirmed not merely moved.",
    "Checked the main checkout's own working tree for merge-time interference."
  ]
}
```

## Verdict 3 (revision 2 repair, 2026-07-27T22:22:57+11:00 approval, verdict returned shortly after) — PASS

```json
{
  "verdict": "pass",
  "refutations": [],
  "advisories": [
    {
      "finding": "IAP.md Tactics item 5 still reads \"Pin the Safety-verified criteria 1-5 work with a pre-registered hash\" -- the exact claim halt 2 refuted, still standing in a third site. It directly contradicts the same file's corrected line 32 (\"this pin covers criteria 1-4 only\") and Risk 3 (\"Criterion 5 ... is not protected by this pin\"). The commander's directive was to correct the disproven pinned-hash claim; it was corrected at two of three sites, and 214-LOG.md's preservation map asserts the file was \"re-read in full\" and is \"internally consistent\" -- a claim this contradiction falsifies. Not a refutation: no 202 criterion covers the IAP's description of its own pin, the pin itself reproduces correctly, and criterion 5 is met on evidence gathered directly, not via the pin.",
      "fix": "Change \"criteria 1-5\" to \"criteria 1-4\" in IAP.md Tactics item 5, before the AAR -- leaving it inverts halt 2's own lesson in the durable record. Highest-priority advisory here."
    },
    {
      "finding": "The \"restored verbatim\" provenance claim is false. Neither 214-LOG.md's 17:55:39 entries nor REGISTER.md line 94 contain the restored section's actual prose -- both hold only a one-clause summary / a differently-worded partial paraphrase. A tree-wide grep for the section's distinctive phrases returns hits in exactly one file: the current IAP.md. The section is a reconstruction, not a restoration -- the impossible instruction originated upstream (halt 2's own report claimed the text was \"fully recoverable verbatim\"). Not a refutation: criterion 5 orders the IN/OUT answer with a reason, not a provenance note, and the answer's correctness was verified first-hand against the actual files (esg.md steps 1/4, REGISTER.md's header, package.json's files whitelist, the roadmap) independent of its claimed lineage.",
      "fix": "Reword IAP.md's provenance lines and the 214-LOG preservation-map entry to say the section was reconstructed from the surviving summary plus REGISTER.md's partial paraphrase, and re-verified on its merits -- not recovered verbatim. Drop \"the reasoning is unchanged from revision 1\", which no artifact can support."
    },
    {
      "finding": "IAP.md cites a dead register row: \"the roadmap's Phase 1 item 3, already registered as trivial-work-inline-lane\". That row is KILLED (folded into decomposition-backlog-routing, rank 9, at the sixth /dcs-esg). REGISTER.md line 94's own quotation carries the same stale name -- two-sited. The roadmap half of the claim checks out (Phase 1 item 3 is genuinely \"Inline-fix recommendation at stem\"). Advisory not refutation: the doctrine.md-OUT reason is unaffected, and the killed row carries its own forwarding address.",
      "fix": "Name decomposition-backlog-routing (rank 9) as the live owner in both IAP.md and REGISTER.md line 94, with a regenerating command beside it: grep -n \"trivial-work-inline-lane\" .dcs/esg/REGISTER.md."
    },
    {
      "finding": "IAP.md's \"Supersedes\" line names revision 1's stamp (a6e93fbf0de6...) as voided by \"this content change\" -- but the stamp this repair's edit actually voided is revision 2's 123657f4c460 (the current stamp is 4c9c9dc48748...). Written for revision 2 and not updated for the repair.",
      "fix": "Name 123657f4c460 as the stamp voided by the repair edit, keeping the revision-1 reference as history."
    },
    {
      "finding": "214-LOG.md's preservation-map entry states the Deviation history section has \"3 entries\" -- an un-regenerated miscount; it has 2 (\"Revision 1 -> 2\" and \"Revision 2, repair (halt 2)\"). A miscount inside the artifact whose purpose was proving nothing was lost.",
      "fix": "Correct to 2 entries, or drop the count."
    }
  ],
  "checked": [
    "Read IAP.md in full (221 lines) -- \"## Criterion 5, answered\" present immediately before \"## Tactics\" as claimed.",
    "Read 214-LOG.md in full -- both 17:55:39 entries inspected; neither contains the restored prose.",
    "Read REGISTER.md lines 93-95 in full -- line 94's quotation covers only the doctrine.md-OUT half, reworded; line 95 shows trivial-work-inline-lane KILLED/folded.",
    "Read 202-OBJECTIVES.md in full -- criterion 5's exact wording confirmed.",
    "grep -rn for the restored section's distinctive phrases across C:\\DCS and the worktree -- hits in exactly one file, the current IAP.md.",
    "ls .dcs/esg/SITREPS/ -- both 209s exist, confirmed not the text's source.",
    "Verified criterion 5's esg.md-IN reasoning against the files directly: esg.md step 1 sweeps QUEUED only; step 4's pre-existing bullet says Update (presuming a row); the incident's added bullet supplies the missing Originate verb.",
    "Read dcs/templates/REGISTER.md header -- confirms Chief-of-Staff ownership and that every other writer requires an incident.",
    "package.json files whitelist includes dcs/ (channel 1); esg.md step 1 reads templates only at founding.",
    "Read vault/Decisions/fable-review-roadmap.md -- Phase 1 item 3 confirmed as the routing question's origin.",
    "Re-measured the hot-path slack independently: 36,683 B used, 1,205 B slack against 37 kB -- exact.",
    "git diff -- dcs/templates/REGISTER.md dcs/workflows/esg.md | sha256sum -> b2450322... -- reproduces the pin exactly.",
    "git diff --stat -- 3 files, matches verification-plan item 3 exactly.",
    "git diff -- CHANGELOG.md -- pure 19-line insertion, zero deletions, nothing at/below the 0.6.10 heading.",
    "git show HEAD:CHANGELOG.md sha256 matches the published-tarball equality claim.",
    "sed -n '119p;133p' on HEAD:CHANGELOG.md -- both carry MERGED (deploy pending), confirming the corrected coordinates.",
    "python tests/test_doctrine_integrity.py -- 82/82 passed, matching the shipped bullet's count.",
    "Scope check: no dcs/VERSION, package.json, hooks, tests, installer, agents, skills touched; enum still 7 tokens.",
    "cat IAP-APPROVED -- matches the re-stamp claim.",
    "Full-file consistency scan of IAP.md hunting a third fidelity casualty -- found two (Tactics item 5, stale Supersedes hash)."
  ]
}
```
