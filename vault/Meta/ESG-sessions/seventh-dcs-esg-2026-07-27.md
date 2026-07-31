### Seventh `/dcs-esg`, 2026-07-27 — the deploy evidence arrived, and two things moved on it

Portfolio: **8 DEPLOYED, 17 QUEUED (ranks 1–17, contiguous), 2 PARKED,
5 KILLED, nothing ACTIVE, nothing deploy-pending.** Audit clean: one worktree,
**zero** `dcs/*` branches, none dangling, no stale actives, all five 209 sitreps
carrying filled decisions, all three suites green, witness at exit `0`.

**This session existed because the sixth held rank 1 empty on purpose**, waiting
on the one train that would run under `deploy-marker-blind`'s content-shaped
step 7. It ran, and it is the first ship in five that needed **no
Owner-authorised substitution** of the verification step. Both decisions below
rest on that.

**Rank 1 is `register-field-repair-path`** — the Owner's call, over the Chief of
Staff's standing recommendation of `criterion-unmeasured-fact` (now rank 2). The
argument for it is that its blocker is not merely cleared but *delivered*: the
`RESOLVED` state is live in the installed tree, defined under a hard
scenario-neutrality bound, and the Safety Officer verified **by reading** that
this row consumes it unchanged. So it writes a registration path against a state
that already exists rather than proposing one — and on that footing it may not
even be Type 1. Ranks 2–17 are the prior order shifted down one; **while rank 1
is `ACTIVE` it blocks ranks 5, 6, 7, 8, 9, 12 and 14**, derived from the
Territory column at this session, not carried forward.

**Delegation amended to v4 — `deploy.auto` `false` → `true`, and nothing else.**
v3 wrote its own revisit condition and that condition is now *satisfied*, not
merely fired: it kept the bound because *"a step that needs a human decision on
each use is precisely the step that must not be delegated"*, and step 7 no
longer needs one — the red before-run it used to require a human to rule on is
now classified by the workflow itself as expected input to the ship.
**`auto_after_close` stays `false`**: that is the setting the Owner's v2 override
was actually about, and close-and-ship remain separate acts. Revert the first
time a train ships something the Owner would have stopped.

**Hygiene, and one of these is a decision about the audit rather than the tree.**
`C:\DCS-wt\schema-citation-guard` will **no longer be reported**: six removal
attempts across four sessions have failed, the first two explained by the acting
session's own shell and the rest unexplained, and the directory is empty, absent
from `git worktree list`, and carries no `.dcs/ACTIVE` — so it is a **non-finding
being re-reported**, which is the same bloat `esg-artifact-bloat` names, in the
audit meant to catch real problems. Recorded as an accepted boundary at
`vault/Decisions/orphan-worktree-husk.md`, with the one-line manual remedy kept
there. Separately, `.dcs/esg/QUEUED-201/`'s spent brief was **removed after
verifying** the merged copy is tracked in git and its row reads `DEPLOYED`.

**Measurement carried forward, not acted on:** these two files are now
**143 KB**, 86 % of the 167 KB that motivated `esg-artifact-bloat` (rank 8), and
the growth is now coming from the sweeps themselves as much as from incidents.
Regenerate with `wc -c .dcs/esg/REGISTER.md .dcs/esg/STRATEGY.md`. The rank was
not raised — rank 1 had a stronger claim this session — but the number should
decide it at the next one.

