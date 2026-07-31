### `deploy-marker-blind` opened 2026-07-27 — territory clean, one row sequenced behind it

Opened by `/dcs-run deploy-marker-blind` at rank 1, typed **1** at its stem.
Worktree `C:\DCS-wt\deploy-marker-blind`, branch `dcs/deploy-marker-blind`.

**No territory conflict at open:** it was the only `ACTIVE` row at the time,
and no `QUEUED` row claims `dcs/workflows/deploy.md`, `install.ps1`,
`install.sh` or `CLAUDE.md` — checked by a full table scan at the stem.

**One conflict appeared when `/dcs-plan` refined the territory (2026-07-27),
and it was not visible at the stem.** The IAP's partition dropped
`install.*` and `package.json` and picked up four files the 201 never named
— including `dcs/templates/REGISTER.md`, which **`esg-artifact-bloat`
(rank 8) claims** via `dcs/templates/`. That row must not open until this
one closes. Nothing else collides: this incident's `tests/payload_check.py`
is a **new** file and not `tests/test_doctrine_integrity.py`, so the
three-row cluster on that file (`check-14-hardening`,
`schemas-contract-format`, `json-examples-unparsed`) is untouched, and
`dcs/workflows/close.md` is claimed by no other row.

**One row was split out of its intake and must not open until it closes:**
`doctor-version-only-check`. Not a hard territory collision — the parent
deliberately leaves `bin/**` outside its blast radius, which is why the split
happened — but the parent is expected to produce a reusable payload-witness
command, and reimplementing that inside `doctor()` first would be waste.
`bin/dcs.js` is *also* claimed by `version-bump-command` (rank 9), so those
two collide with each other regardless of this incident.

**Delegation interaction, expected rather than anomalous:** this row can
never auto-approve, and not only because it is Type 1 (which no
`auto_approve_type3` bound reaches). Its blast radius includes `install.ps1`
and `install.sh`, in `forbidden_globs` at both the top level and inside the
`deploy` object, and possibly `package.json`. Delegation v3's own notes
already anticipated this row: *"The whole `deploy` object stays as written,
`auto: false` included … Revisit only after that row closes."*

**`halt-loop-unbounded` opened 2026-07-25 from Owner chat, and holds a
territory that blocks two queued rows.** Its evidence is empirical and lives in
*another* project — `C:\bread_bot`'s incident artifacts — while the defect and
the fix are both here. Incident cost there is bimodal: 7 of 9 closed incidents
run 2–7 h with a 5–31 KB log; `energy-cost-model-rework` ran 30 h 34 min / 292 KB
with 6 halts (its own AAR says "seven" — the discrepancy is recorded, not
reconciled) and `prod-tools-drift` is at 16 h 40 min / 144 KB with **10 halts and
an attempt counter reading 2**. Regenerate with `grep -c "SAFETY: halt"` against
`grep -c "IAP APPROVED"` on each incident's `214-LOG.md`. The contrast case
matters: `baking-plan-demand-and-units` is also large (19 h, 184 KB) but has only
2 halts — its size is real scope, not re-verification churn. Halt count, not task
size, separates the expensive incidents from the cheap ones.

Territory overlaps to enforce while this row is `ACTIVE`: **`schemas-md-trim`**
(rank 2) shares `tests/test_doctrine_integrity.py`, and **`field-lesson-citations`**
(rank 4) shares `dcs/references/doctrine.md` and `doctrine-appendix.md`. Neither
may open until this row closes — `/dcs-new` step 7b's check enforces it.

**Three rows were split out of this incident's intake at its stem**
(`new.md` step 4a — the one-incident-one-defect rule): `safety-halt-functional-scope`,
`safety-officer-incremental-verify`, `esg-artifact-bloat`. The Owner's intake
described all four; only the one on the critical path was opened, because until
the loop has a ceiling the other three are optimisations under an unbounded cost.
Their types are carried as `?` where typing genuinely belongs at their own stem.

**Reconciled at the 2026-07-26 ESG.** Ranks are no longer provisional: this
row closed and deployed, and `STRATEGY.md`'s list was rebuilt around what it
left behind. Two further rows were queued from `vault/Backlog.md` items 10 and
11, both raised by this incident — `halt-binding-status` and
`deviation-path-proportionality`.

