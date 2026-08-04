# field-lesson-guard-bare-date-weakening — post-mortem

Closed 2026-08-04, Type 3 (Owner override from a proposed Type 1), one
operational period, two attempts (halt → fix-tasking → pass).
Integration commit `54d5b41` (verify: `git show 54d5b41 --stat`).
Artifacts: `.dcs/incidents/2026-08-04-field-lesson-guard-bare-date-weakening/`.

## What it was

The parent (`field-lesson-guard-vacuity`, deploy held on this very
defect) repaired check 20's vacuity but silently widened `_FL_ID_RE` to
accept a bare same-line date as a sufficient field-lesson identifier —
the v0.5.10 unverifiable-claim shape, reintroduced by the guard's own
repair. Folded in by ESG decision: Backlog item 31, the
`RECORD-CORRECTION:` sentinel invisible to check 12's census.

## The lesson that earned this file: relocate-instead-of-remove

The tasking said "remove every identifier `bcf9468` inserted into
non-claim prose". S2 complied at three sites and, at
`doctrine-appendix.md:13`, *relocated* instead: `follows (v0.5.0)`
became "Since v0.5.0, every field lesson … follows one of three citation
forms" — grammatical, natural-reading, load-bearing for check 20a, and
**false** (the convention arrived at v0.7.1, commit `710cf52`;
`git grep -l "predates self-hosting" d5d8106` → empty at v0.5.0). The
guard cannot tell a true identifier from a false one; only provenance
checking can. The Safety Officer caught it by running
`git log -S "one of three citation forms"` — the check the parent
incident's PASS never performed, performed this time.

Reusable form: **a "since vX.Y.Z" (or any dated-origin) claim in prose
is a measured claim about repository history** — it gets `git log -S` +
`git show <commit>:dcs/VERSION` before it is written, exactly as 202
criteria already require for out-of-tree facts (`202-OBJECTIVES.md`'s
MEASURED CLAIM rule). And a tasking that says "remove X" should say what
the evidence of removal looks like *including the relocation case* —
S2's own evidence commands (grep for the four parenthetical shapes) all
passed while the defect stood, because the relocation changed the shape.

## Secondary findings

- **Deliberate keep at `:670`:** the in-sentence `v0.6.9` there is true
  (the section quotes the original v0.6.9 ceiling text) — criterion 5
  met as stuffing-removed, not identifier-erased; IC decision at command
  point 4, restated in the AAR so the question stays closed.
- **Hot-path spend:** the second defect's documentation (doctrine.md's
  fourth-sentinel clause) was funded by trimming principle 15's
  rhetorical sentence, leaving 25 B of slack as of `54d5b41`
  (regenerate: `python -c "import os;p='dcs/references/';a=os.path.getsize(p+'doctrine.md');b=os.path.getsize(p+'schemas.md');print(37*1024-(a+b))"`).
  The next doctrine.md sentence needs a paired trim; consider whether
  the fold pattern (two defects, one incident) should carry a budget
  check at the stem.
- **The parent's "false-positive storm" justification measured to 3
  sites** — the register row's dispute held up: an unmeasured storm
  claim was accepted by four seats in the parent; this incident's plan
  measured it in lint 3a baselines before a single edit.
- **`verdict_rerun.py` / `->` separator:** this close exercised the
  em-dash gap again (register rank 2, `verdict-rerun-em-dash-gap`) —
  see the close-out entries in `214-LOG.md` for what the tool actually
  selected.

## Links

[[Backlog]] item 31 (discharged here) · register row
`field-lesson-guard-bare-date-weakening` · parent post-close review at
the eighteenth ESG session note.
