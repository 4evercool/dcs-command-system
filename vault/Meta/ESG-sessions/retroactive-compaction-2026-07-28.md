### Retroactive compaction of pre-existing rows, 2026-07-28 — Owner-directed, outside any incident

`token-economy` shipped a pointer-not-copy mechanism for `Territory`/
`Outcome`/`Intake source` (criterion 3), applied going forward at
`close.md`/`deploy.md`/`esg.md`'s write points — never retroactively, by
that incident's own design (the Safety Officer only verified the
mechanism and its first application, not a rewrite of every existing
row). The Owner explicitly asked for the retroactive rewrite too ("I do
want that done as it will further diminish the size of that file"),
after noticing an older row (`hot-path-budget-eol-sensitivity`) still
carrying its original long-form Outcome and asking why.

Applied to the 11 `DEPLOYED` rows with a real incident directory
(verified `IAP.md`/`AAR.md`/`201-BRIEF.md` all present before touching
each one — `deploy-marker-blind`, `direct-resolution-lane`,
`safety-halt-functional-scope`, `schema-citation-guard`,
`criterion-unmeasured-fact`, `deviation-path-proportionality`,
`schemas-md-trim`, `halt-loop-unbounded`, `register-field-repair-path`,
`hot-path-budget-eol-sensitivity`, `doctrine-hot-path-trim`) — each row's
`Territory`/`Intake source`/`Outcome` collapsed to the same three
pointers `token-economy`'s own row already uses. Regenerate the byte
savings with:
`awk -F'|' '/^\| [A-Za-z0-9]/ && NF>=13 {print length($9)+length($10)+length($13)}' .dcs/esg/REGISTER.md`
summed before/after (measured this session: 118,955 B -> 73,769 B, this
file, `wc -c .dcs/esg/REGISTER.md`).

**Deliberately NOT touched — 10 `KILLED`/`PARKED` rows with no incident
directory** (`trivial-work-inline-lane`, `halt-binding-status`,
`charter-schema-agreement`, `commander-output-contract`,
`safety-officer-incremental-verify`, `esg-artifact-bloat`,
`log-read-scoping-incomplete`, `cross-project-register-view`,
`package-json-description-corruption`, `type5-express-lane-tuning`) —
these were killed/parked before ever opening a worktree (folded into
another incident, or ended at the ESG/intake level), so there is no
`IAP.md`/`AAR.md`/`201-BRIEF.md` to point to. Collapsing these to the
same pointer text would create a dangling reference, which is worse than
the existing prose. If these ever need trimming, it would have to be a
genuine rewrite of the prose itself, not a mechanical pointer swap — a
different, riskier operation this note deliberately does not attempt.
`STRATEGY.md`'s `## Sessions` log was not touched either — that is a
separate cap (5 lines, routing to a decision store) the Owner did not
ask to apply retroactively this time.

