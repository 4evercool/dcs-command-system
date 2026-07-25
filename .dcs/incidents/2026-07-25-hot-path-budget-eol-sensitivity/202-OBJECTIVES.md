<!--
202-OBJECTIVES.md — written by the IC together with the Owner, at the
start of EACH operational period (/dcs-plan).
-->

# 202 — Objectives (Operational Period 1)

**Incident:** hot-path-budget-eol-sensitivity
**Period:** 1

## Goal

**The repo has one line-ending policy, and no byte-exact mechanism can give a
different answer in a different checkout of the same commit.**

Two things must stop being true: that `git ls-files --eol` reports a mixture, and
that the gate's approval hash depends on which tree materialised the file. The
second is the one that matters — it is the enforcement mechanism, it is already
broken for the incident that closed today, and unlike the size check it **ships**.

The success condition is an invariant, not a number: *the same commit yields the
same bytes, and the same content yields the same verdict, in every tree.*

## Acceptance criteria (the Definition of Done)

**POLICY DECIDED BY THE OWNER at the 202 confirm, 2026-07-25: `* text=auto
eol=lf` — LF in every checkout on every OS.** The alternative (`* text=auto`
alone, giving native EOL per platform) was presented and declined. It would have
made each platform internally consistent but left the gate hash diverging
*across* platforms — and `dcs_gate.py` ships to any OS — and it would not have
healed the archived stamp, which was computed from LF bytes. The Owner accepted
the visible cost: every file in the Windows working tree becomes LF.

1. **A line-ending policy exists and is explicit.** `.gitattributes` is present
   and tracked, and normalises text to LF (`* text=auto eol=lf`). Verified by
   `git check-attr text eol -- dcs/references/doctrine.md dcs/hooks/dcs_gate.py .dcs/incidents/2026-07-25-doctrine-hot-path-trim/IAP.md`
   returning a definite `text`/`eol` setting for each rather than `unspecified`.

2. **[IC]** **No tracked text file is in a mixed state, in this worktree.** The
   population is enumerated by this command and the criterion is *its output
   containing no `w/crlf` row*:

   ```
   git ls-files --eol | awk '{print $1, $2}' | sort | uniq -c | sort -rn
   ```

   Baselines recorded 2026-07-25 at `12b212f`: **this worktree** `83 i/lf w/crlf`
   + `2 i/none w/none`; **main checkout** `68 i/lf w/lf` + `15 i/lf w/crlf` +
   `2 i/none w/none`. Target `84 i/lf w/lf` + `2 i/none w/none`.

   **Tagged [IC] after chief review.** Clearing `w/crlf` requires a repo-wide
   working-tree re-materialisation, which crosses every territory line, is
   invisible to the gate (it is not an Edit or a Write), and destroys uncommitted
   work. Both chiefs concluded independently that it cannot be a specialist
   tasking. The Logistics Chief additionally measured that
   `git add --renormalize .` alone is a **no-op** here — the index is already
   all-LF — so the file-clearing step is a distinct, deliberate IC act.

3. **The hot-path measurement is tree-independent.** Split after chief review;
   the original single criterion was unsatisfiable in-period.

   **3a — the check itself.** `tests/test_doctrine_integrity.py`'s hot-path
   measurement must not depend on line endings: it computes a normalised byte
   count, so the same commit yields the same number in any checkout. Verifiable
   in this worktree, in-period. Target `21966 15613 37579`.

   **3b — [IC]** the raw `os.path.getsize` figures in this worktree and in
   `C:\DCS` agree. **Not verifiable this period**: it requires the merge *and* a
   re-materialisation of `C:\DCS`'s own working tree, which is outside this
   worktree and therefore outside every legal territory. Baseline: worktree
   `22121 15785 37906`, main `22121 15613 37734` — 172 B apart on the same
   commit. Verified at close, after the post-merge refresh.

4. **The gate's verdict does not depend on line endings — asserted as an
   invariant, never as an instance.** For any `IAP.md` and its `IAP-APPROVED`
   stamp, converting the file between LF and CRLF must not change whether the
   gate permits an edit. *(Principle 15's test clause: assert the invariant, not
   a particular hash. A test pinning today's specific digest would go red the
   first time the IAP's prose changes.)*

5. **A regression test exists that fails against the current implementation.**
   In `tests/test_dcs_gate.py`, a cross-EOL fixture — the same logical `IAP.md`
   materialised both ways — proving criterion 4. **The specialist must
   demonstrate it fails before the fix and passes after**, pasting both runs.
   Today's suite cannot catch this: `tests/test_dcs_gate.py:71-75` writes its
   fixture and hashes it in one process, self-consistent by construction.

6. **[IC]** **The archived audit trail verifies again.** The closed incident's stamp
   currently matches the git blob and not the on-disk file. After the fix, this
   must agree on all three lines:

   ```
   D=.dcs/incidents/2026-07-25-doctrine-hot-path-trim
   head -1 $D/IAP-APPROVED
   python -c "import hashlib;print(hashlib.sha256(open('$D/IAP.md','rb').read()).hexdigest())"
   git show HEAD:$D/IAP.md | python -c "import hashlib,sys;print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())"
   ```

   Baseline: line 1 `a5eec3b4…`, line 2 `375c4859…`, line 3 `a5eec3b4…`.
   **Healing the archive is a consequence of the fix, not extra work** — the
   stamp was computed from LF bytes, so normalising the tree to LF restores it.
   If a chosen approach does *not* restore it, that is a signal about the
   approach and belongs in a deviation.

7. **[IC]** **A fresh checkout is clean too.** The fix must hold for a tree that
   does not exist yet, which is where the defect actually lives. Verified by
   cloning to a throwaway path and running criterion 2's command there — no
   `w/crlf` rows. The clone is deleted afterwards and is **not** part of the
   deliverable.

   **Tagged [IC] after chief review:** a specialist mid-execution has nothing to
   clone — its work is uncommitted. This is verified by the IC/Safety Officer
   after the final commit. Command shape verified by the Planning Chief:
   `git clone --no-local -q <worktree> <scratch>` carries the incident branch.

8. **All three suites green:** `python tests/test_doctrine_integrity.py`,
   `python tests/test_dcs_gate.py`, `python tests/test_dcs_intake.py`.

9. **`HOT_PATH_BUDGET_KB`'s value is unchanged.** Ratchet *resolution* is a
   separate defect owned by register rank 2 (`schemas-md-trim`). The constant's
   surrounding comment may be updated to describe the new measurement basis; the
   number may not move. Verified by `git diff` on that file.

10. **[Owner]** Owner confirms the policy is the one they want — specifically
    that **LF-in-the-working-tree on Windows** is acceptable, since that is what
    `eol=lf` produces and it is a visible change to every file they open.

11. **[IC]** The version bump is **decided at merge, not claimed here.**
    `doctrine-hot-path-trim` claimed 0.6.5 at plan time and found 0.6.5 and 0.6.6
    both taken by close; its AAR names this as a lesson. No version number is
    fixed by this 202.

12. **[deploy period]** `~/.claude/dcs/VERSION` matches `dcs/VERSION` after
    `/dcs-deploy`. Not verifiable this period.

## The sequencing constraint (not a criterion — a hazard the plan must route around)

**This incident's own fix can invalidate this incident's own approval marker.**
A renormalise pass rewrites working-tree files. Run inside this worktree after
`IAP.md` is stamped, it changes `IAP.md`'s bytes, changes its sha256, and
`IAP-APPROVED` stops matching — the gate denies every subsequent edit on a plan
that was validly approved, mid-execution.

The Logistics Chief owns the ordering. At least three shapes exist (land the gate
normalisation first; run the renormalise last with an IC re-stamp; exclude
`.dcs/` from the attributes) and they are not equivalent — the third leaves
incident artifacts permanently outside the policy, which is where the defect was
found in the first place.

## Out of scope this period

- **`HOT_PATH_BUDGET_KB`'s value** and the kB-granularity band — register rank 2.
- **Trimming anything.** No file's *content* changes in this incident; only its
  representation, plus the two mechanisms and their tests.
- **`install.ps1` / `install.sh`.** They are byte-for-byte copies and propagate
  whatever is on disk; if the tree is consistent they are correct. Touching them
  is out of territory and a deviation.
- **The BOM / double-encoding guards** added by `0428ac4`. Same defect *family*,
  different defect; they work and are not this incident's business.
- **Rewriting history.** The index is already all-LF; nothing needs
  `filter-branch` or a rewrite, and proposing one is a deviation.

## Chief feedback (filled in after /dcs-plan spawns the chiefs)

{{pending}}
