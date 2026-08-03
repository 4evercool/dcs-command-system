# AAR — After Action Report

**Incident:** spawn-effort-control
**Type:** 1
**Opened:** 2026-08-03
**Closed:** 2026-08-03
**Operational periods:** 1

## Outcome

All 8 acceptance criteria from `202-OBJECTIVES.md` (period 1) were met,
verified independently by the Safety Officer and re-verified by
`dcs-commander` at command point 4 (`214-LOG.md`,
`2026-08-03T15:45:34+11:00`): `dcs/references/doctrine.md`'s new
"Capability tier" rule (line 31) governs per-spawn tier selection on two
axes — availability (unchanged for the four command points) and a
spawn's own complexity (new, for the other six seats) — grounded in the
Agent tool's real per-call `model` override, phrased provider-agnostically,
as one mechanism rather than two. `python tests/test_doctrine_integrity.py`
passed 156/156 in the worktree (re-run independently by both the Safety
Officer and the IC), including the hot-path budget check with the ceiling
held fixed at 37 KB per the Owner's command-point-1 ruling.
`dcs/references/doctrine-appendix.md` gained a field-lesson entry and two
worked examples. Integration commit `1b301f2` (`git show 1b301f2 --stat`:
2 files, +50/−4) landed on `dcs/spawn-effort-control`.

## What worked

- **Reusing the existing tier-fallback mechanism instead of inventing a
  new one.** The Planning Chief's central tactic — generalize
  doctrine.md's existing "Model availability" paragraph into one rule
  spanning both axes, rather than adding a 17th principle — is what made
  the incident fit inside a 17-byte hot-path budget at all. Confirmed by
  `dcs-commander` at both command points 2 and 4: exactly one
  tier-selection rule exists in `doctrine.md` after this incident.
- **"Relocate, never delete" held under real budget pressure.** The
  specialist funded the addition partly by compressing an unrelated,
  already-compressible passage (the "Project-supplied provision hook"
  body) rather than the paragraph alone — broader than the tasking's
  literal wording anticipated, but the Safety Officer byte-compared all
  four relocated/compressed passages against the pre-incident blob and
  confirmed nothing was silently lost; both originals are preserved
  verbatim in a new `### D5:` appendix entry.
- **A platform-capability check before drafting objectives, not after.**
  Verifying (via `claude-code-guide`) that the interactive Agent/Task
  tool has no per-invocation effort parameter — only `model` — before
  writing `202-OBJECTIVES.md` avoided drafting acceptance criteria around
  a capability that does not exist, and reframed the whole incident
  around a much smaller, buildable mechanism.
- **The territory-conflict queue-and-wait worked as designed.** The stem
  found `close-integrity-guard-bundle` already claimed the same
  constitution files; queuing (`.dcs/esg/QUEUED-201/spawn-effort-control.md`)
  and resuming once it merged avoided the exact concurrent-doctrine-edit
  risk principle 6 exists to prevent.

## Lessons

- **A stem's byte-budget measurement is a snapshot, not a fact that
  survives a wait.** The 201 recorded "50 bytes of hot-path slack";
  by the time planning actually ran, `close-integrity-guard-bundle` had
  merged and the true figure was 17 bytes. The Planning Chief caught this
  by re-measuring rather than trusting the 201, and `dcs-commander`
  independently re-confirmed it at command point 2. Any incident that
  queues on a territory conflict should re-derive its own byte/line
  budget claims at planning time, not carry the stem's numbers forward.
- **A Safety Officer flagging record-accuracy defects in a newly-written
  appendix entry, rather than in the operative rule, is a real and useful
  finding class distinct from a refutation.** All 5 advisories here were
  about whether the new `### D5:` entry's own "Removed:" disclosure text
  accurately described what changed (e.g. a "two relocations" heading
  when one was actually an in-place compression) — none touched
  `doctrine.md`'s actual rule. This is exactly the artifact-hygiene /
  behavior-correctness split `agents/dcs-safety-officer.md` step 6 draws,
  observed in a case where the artifact in question was created by this
  same incident, not inherited from an earlier one.
- **Deferring Safety-passed advisories to a follow-up incident, rather
  than folding them into the same integration commit, is itself a
  judgment call the IC should make explicitly, not by default.**
  `execute.md`'s own text describes "the IC fixes them now" as the normal
  path; `dcs-commander` chose to defer here, citing the
  `token-economy-advisory-fixes` precedent (an unverified last-minute
  edit riding the merge with no Safety pass of its own). Both paths are
  legitimate; which one applies is worth stating a reason for, not
  defaulting to silently.

## Deviations this incident

None — executed as planned. Zero `SAFETY-HALT:` entries in `214-LOG.md`;
one `IAP-APPROVED:` stamp, one execution attempt, one `SAFETY-PASS:`.

## Memory routing

This repo's own `CLAUDE.md` documents a three-store routing rule for DCS's
own lessons: `dcs/references/doctrine.md` (a change to a rule),
`dcs/references/doctrine-appendix.md` (the provenance of a rule), and
`vault/` (maintainer-only cross-incident analysis, never shipped) —
"if it would only ever be read while improving DCS itself → vault."
Followed on all three:

- **Rule:** `dcs/references/doctrine.md` — the unified "Capability tier"
  paragraph (line 31), committed in `1b301f2`.
- **Provenance:** `dcs/references/doctrine-appendix.md` — the platform-
  capability field lesson and the `### D5:` funding-relocation entry,
  same commit.
- **Meta:** `vault/Meta/building-dcs-lessons.md` §30 ("A capability check
  before drafting objectives is cheaper than discovering the gap after")
  — a pattern about verifying platform capabilities before drafting 202
  objectives, and about a specialist's scope-broadening decision being a
  separate axis from whether it was disclosed accurately. Written to the
  worktree's copy; commits with this close's step 5a.1.

The follow-up work to fix `### D5:`'s own disclosure-text defects is
registered in `REGISTER.md` at this close (see below), which is this
repo's normal place for queued follow-up work, not the vault.

## Intake source closure

Owner chat report, via `/dcs-run` direct intake description (not from
the register) — ad hoc, no external reference to close.

## Follow-up to register at this close

Per `dcs-commander`'s command-point-4 directives (`214-LOG.md`,
`2026-08-03T15:45:34+11:00`): a follow-up incident to correct
`### D5:`'s own disclosure-text defects (the "half-false" provenance
parenthetical, the undisclosed `MUST`/bold-emphasis removal, the
"two relocations" heading contradicted by its own body text plus two
incomplete "Removed:" lists, and the field-lesson's verification-source
citation mismatch against `214-LOG.md`'s actual record) — territory
`dcs/references/doctrine.md` + `dcs/references/doctrine-appendix.md`,
same two files, likely Type 5 or 3 (prose-accuracy corrections to an
unbudgeted appendix file, no hot-path pressure). Optional, non-blocking:
anchor one worked example to a real incident slug.

## Safety Officer's final verdict (verbatim, from SAFETY.md)

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
    "Read the full diff, re-ran all 3 suites independently (156/156, 100/100, 18/18), re-derived the byte budget independently (23872+13962=37834, 54 free), re-ran all 5 guarantee anchors, confirmed both empty-diff claims, byte-compared all 4 relocated passages verbatim against baseline, verified principle numbering 1-16 intact, verified check-20 field-lesson identifier co-location, confirmed encoding clean, confirmed the 201 repro path's in-scope steps are closed, confirmed doctrine.md's @-inclusion reaches all 10 spawn call-sites"
  ]
}
```
