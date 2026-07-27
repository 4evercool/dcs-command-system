# AAR — After Action Report

**Incident:** register-field-repair-path
**Type:** 3
**Opened:** 2026-07-27
**Closed:** 2026-07-27
**Operational periods:** 1 (two revisions within the period, both fixing Safety halts, not re-scoping objectives)

## Outcome

All 6 acceptance criteria from `202-OBJECTIVES.md` met, Safety-verified
(`SAFETY.md` verdict 3: `pass`, zero refutations). `dcs/templates/REGISTER.md`
now declares a `RESOLVED (field repair)` convention for Owner-authorized
fixes applied entirely outside the DCS lifecycle -- a fixed, quotable
label (qualifying the existing `RESOLVED` state, not an eighth enum
token), a cell-shape rule, and a three-part Outcome minimum. `dcs/workflows/esg.md`
gives it a live writer (agenda item (g), a Record-step bullet). `CHANGELOG.md`
documents the change under a new `## Unreleased` heading. Integration commit
`e17fa7f` (3 files: `dcs/templates/REGISTER.md`, `dcs/workflows/esg.md`,
`CHANGELOG.md`), verified to touch only those files and reference the
intake source.

## What worked

- **Reusing an existing state, qualified, instead of adding a new enum
  token.** This kept the incident's own Type-3 typing internally
  consistent (the Type-1-shaped ceremony had already been spent by the
  sibling incident that shipped `RESOLVED` itself) and survived Safety
  review on both the mechanical claim (state-enum line still exactly 7
  tokens) and the design claim (the qualifier idiom already existed in
  the template one line above, `MERGED (deploy pending)`).
- **Territory-enforced single-declaring-site.** Forbidding the specialist
  who wrote the citing surface (`esg.md`) from touching the declaring
  surface (`dcs/templates/REGISTER.md`) made the "cite, never restate"
  requirement mechanical rather than a style request, and the integrated
  grep the Safety Officer ran confirmed exactly one declaring site across
  both revisions.
- **Byte-for-byte verification, not a text diff, for the CHANGELOG revert.**
  Both the specialist and the Safety Officer independently proved the
  `## 0.6.10` section's restoration was byte-identical to the published
  npm tarball -- the Safety Officer went further than the tasking required
  (a whole-file prefix/suffix comparison in Python, not just the tasked
  `awk`/`diff`), which is exactly the "attempt to refute, don't confirm"
  charter working as intended.
- **A pinned sha256 hash as territory enforcement where the gate can't
  reach.** `CHANGELOG.md` matches neither `guarded_paths` nor
  `unguarded_paths` in `.dcs/config.json`, so `dcs_gate.py` does not
  mechanically defend a `CHANGELOG.md`-only tasking's forbidden zones
  against the two payload files sharing the worktree. A hash of those
  files' diff, checked by both the specialist and independently
  reproduced by the IC and the Safety Officer at every step, substituted
  for gate enforcement successfully -- though see Lessons below for where
  its coverage had a real gap.

## Lessons

- **An acceptance criterion that asserts a fact about external state
  (here: "0.6.10 is unpublished") must be re-measured every time it is
  used, never inherited from a sibling incident's artifacts.** The
  premise was true when `direct-resolution-lane`'s AAR recorded it and
  false by the time this incident's tasking repeated it -- the Owner
  published 0.6.10 between the two incidents, and nothing in the chain
  (situation analysts, Planning Chief, IC, dcs-commander) ran `npm view`
  to check. This is the second field-measured instance of the still-QUEUED
  register row `criterion-unmeasured-fact` (rank 2) -- the first was the
  version-publish confusion that row itself was filed over.
- **A pinned-hash (or any payload-file-scoped) protection mechanism
  cannot reach `.dcs/**` prose, and a plan that claims otherwise will not
  be caught by the gate.** When the IC rewrote `IAP.md` to fix the
  criterion-6 halt, it silently dropped the unrelated "Criterion 5,
  answered" section -- not contradicted, just omitted, because the
  rewrite's attention was entirely on the one criterion being fixed.
  `dcs_gate.py`'s `.dcs/**` exemption meant nothing mechanical noticed;
  only the Safety Officer's full re-read of `IAP.md` caught it. A narrow
  IAP revision should include an explicit preservation check (map every
  acceptance criterion to the section that satisfies it, in the revised
  file) as a standard step, not an ad hoc response to having already been
  caught once. This is also the second field measurement for the
  still-QUEUED `deviation-path-proportionality` (rank 5): a one-paragraph,
  IC-authored, `.dcs/**`-only restoration still had no route cheaper than
  a full replan-and-reapprove cycle.
- **An unverified claim of fidelity is the same defect shape as the fact
  it is trying to restore.** The IC's own repair claimed the dropped
  section was "restored verbatim" from two cited sources; the Safety
  Officer checked and found neither source contains the actual prose --
  the text is a faithful *reconstruction*, re-verified on its own merits,
  not a verbatim recovery. The claim was wrong in the same way halt 1's
  claim was wrong: an assertion about a source nobody checked against the
  source. See `vault/Meta/building-dcs-lessons.md` §18 for the full
  writeup.
- **A killed/folded register row's name keeps propagating in citations
  after the row is retired**, because nothing re-checks a citation
  against current state once it is written. This incident's own 201 and
  IAP cited `trivial-work-inline-lane` as the routing question's owner;
  it had already been folded into `decomposition-backlog-routing` at the
  sixth `/dcs-esg`, hours before this incident's stem. Corrected in both
  `IAP.md` and `REGISTER.md` line 94 at close.

## Deviations this incident

No specialist deviations (zero `status: "deviation"` returns across S1,
S2, S3). Two Safety halts, both resolved within period 1 (no new period,
per `execute.md` 9b -- the halts corrected the plan/paperwork, not the
objectives):

1. **Halt 1** (criterion 6): tasking's premise that 0.6.10 was unpublished
   was false. Disposed `replan, narrow` by dcs-commander (command point 4)
   -- criterion 6 rewritten to target a new `## Unreleased` heading.
   Escalation trigger (e) (IC-requested ESG activation) fired alongside;
   Owner chose `continue`. See `.dcs/esg/SITREPS/register-field-repair-path-p1.md`.
2. **Halt 2** (criterion 5): the revision-1→2 `IAP.md` rewrite silently
   dropped criterion 5's already-satisfied "Criterion 5, answered"
   section. Disposed `fix_taskings` by dcs-commander -- an IC-authored
   `.dcs/**`-only restoration (no ops-specialist tasking possible;
   criterion 5 is `[IC]`-tagged). Convergence read: different class from
   halt 1 (converging, not whack-a-mole). Escalation trigger (b) (mandatory,
   second halt on the same objective) fired; Owner chose `continue`. See
   `.dcs/esg/SITREPS/register-field-repair-path-p1-halt2.md`.

Both halts, their disposals, and the repair are recorded verbatim (all
three Safety Officer verdicts) in `SAFETY.md` and in full narrative detail
in `214-LOG.md`.

## Memory routing

`vault/Meta/building-dcs-lessons.md` +1 section (§18: "A revision that
fixes one criterion can silently unfix another, and an unverified fidelity
claim is the same shape of defect as the fact it repairs") -- covers both
halts' generalizable lessons and the meta-lesson about the repair's own
overstated provenance claim. No `doctrine.md` or `doctrine-appendix.md`
changes: this incident's own scope (documenting a recording convention,
not a routing/bypass rule) does not warrant a doctrine amendment, and the
two strategic observations above are already carried by existing QUEUED
register rows (`criterion-unmeasured-fact`, `deviation-path-proportionality`)
rather than needing a new one.

## Intake source closure

Ad hoc -- intake was `/dcs-run --next` resolving `.dcs/esg/REGISTER.md`'s
rank-1 `QUEUED` row `register-field-repair-path`, which this same
incident's close (step 5a.3 / 6a) transitions to `MERGED (deploy pending)`
directly. No external system to flag or close separately.

## Safety Officer's final verdict (verbatim, from SAFETY.md)

```json
{
  "verdict": "pass",
  "refutations": [],
  "advisories": [
    {
      "finding": "IAP.md Tactics item 5 still reads \"Pin the Safety-verified criteria 1-5 work with a pre-registered hash\" -- the exact claim halt 2 refuted, still standing in a third site. It directly contradicts the same file's corrected line 32 (\"this pin covers criteria 1-4 only\") and Risk 3 (\"Criterion 5 ... is not protected by this pin\"). Not a refutation: no 202 criterion covers the IAP's description of its own pin, the pin itself reproduces correctly, and criterion 5 is met on evidence gathered directly, not via the pin.",
      "fix": "Change \"criteria 1-5\" to \"criteria 1-4\" in IAP.md Tactics item 5 -- FIXED before this AAR."
    },
    {
      "finding": "The \"restored verbatim\" provenance claim is false. Neither cited source contains the section's actual prose; a tree-wide grep proves it exists nowhere but the current IAP.md. The section is a reconstruction, not a restoration. Not a refutation: criterion 5 orders the IN/OUT answer with a reason, not a provenance note, and the answer's correctness was verified first-hand against the actual files independent of its claimed lineage.",
      "fix": "Reworded IAP.md's provenance lines to describe reconstruction-and-reverification, not verbatim recovery -- FIXED before this AAR."
    },
    {
      "finding": "IAP.md and REGISTER.md line 94 both cite the dead register row trivial-work-inline-lane (KILLED, folded into decomposition-backlog-routing) as the routing question's owner.",
      "fix": "Named decomposition-backlog-routing (rank 9) as the live owner in both files, with a regenerating command -- FIXED before this AAR."
    },
    {
      "finding": "IAP.md's \"Supersedes\" line named the wrong voided stamp (revision 1's hash, not revision 2's, which is what the repair edit actually voided).",
      "fix": "Corrected to name the actually-voided stamp, keeping the revision-1 reference as history -- FIXED before this AAR."
    },
    {
      "finding": "214-LOG.md's preservation-map entry miscounted Deviation history's entries as 3 when it has 2.",
      "fix": "Corrected to 2 -- FIXED before this AAR."
    }
  ],
  "checked": ["see SAFETY.md verdict 3 for the full 20-item independent verification list"]
}
```

Full verbatim text of all three Safety Officer verdicts this period
(halt 1, halt 2, and this final pass) is in `SAFETY.md`, per
`dcs/references/forms.md`'s verbatim rule -- not reproduced a second time
here beyond the final verdict this section requires.
