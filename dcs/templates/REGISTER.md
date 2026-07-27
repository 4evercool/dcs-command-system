<!--
REGISTER.md -- the incident portfolio, and (v0.3) the portfolio-level
territory-partition lock table. Lives ONLY in the main checkout's
.dcs/esg/ (the esg_root resolution rule, doctrine "Parallel operation") --
never in an incident worktree, even though the worktree is where the
incident's own row gets read/decided about. Owned by the Chief of Staff
(main session during /dcs-esg); also touched by /dcs-new (territory check
+ QUEUED -> ACTIVE with worktree/branch, or QUEUED -> RESOLVED with
neither), /dcs-plan (territory refined to
the IAP partition's union; Delegation auto-approval logging), /dcs-close
(ACTIVE -> MERGED (deploy pending)), and /dcs-deploy (MERGED -> DEPLOYED,
branch deleted). Every incident that opens should end up with a row here,
whether or not it started at a /dcs-esg session.

REGISTER-LOCK (v0.3, courtesy lock, not a database): before any
read-modify-write of this file from a parallel session, create-exclusive
.dcs/esg/REGISTER-LOCK (contents: holder + ISO8601 timestamp), delete it
when done. Treat a lock older than 10 minutes as stale -- take it over,
but note the takeover (who, when, why) in this file's Notes section.
Contention here is human-paced; this exists to catch two sessions racing
a write, not to serialize normal usage.
-->

# REGISTER — Incident Portfolio

<!-- State values (v0.3): QUEUED | ACTIVE | MERGED (deploy pending) |
     DEPLOYED | PARKED | KILLED | RESOLVED

     QUEUED    -- not yet opened; waiting its turn (territory conflict,
                  or just not picked up yet).
     ACTIVE    -- has a live worktree; multiple rows may be ACTIVE at
                  once (that's the whole point of v0.3). The per-worktree
                  .dcs/ACTIVE file is the gate's own input; this column
                  is the cross-incident view.
     MERGED    -- /dcs-close's anti-rot core has merged the incident's
                  branch into main (--no-ff) and removed (or flagged for
                  manual removal, see Worktree column) its worktree.
                  Shipped only once a deploy train (/dcs-deploy) confirms
                  it -- "deploy pending" until then.
     DEPLOYED  -- /dcs-deploy verified, per `dcs/workflows/deploy.md` step
                  7's shape-dependent disposition, that this incident
                  shipped -- an ancestry check for a commit-ish marker, or
                  a green (or stale-extras-only) witness run against the
                  integration tip for a content marker (a bare version
                  label is never sufficient on its own) -- and deleted its
                  dcs/<slug> branch.
     PARKED    -- intentionally not running now (e.g. /dcs-loop's hard
                  rule 1 parking a Type 1 it will not run unattended,
                  reason "awaits Owner"; or an ESG hygiene decision).
                  Parking ALWAYS removes the worktree first -- a parked
                  incident is a row and a kept branch, never a directory
                  quietly aging on disk.
     KILLED    -- abandoned; worktree removed, branch deleted, reason
                  recorded in Notes.
     RESOLVED  -- terminal for an incident whose work completed inline:
                  no worktree was ever opened, and it never enters the
                  deploy lifecycle. Worktree and Branch stay unset, and
                  Closed and Outcome are recorded at the same time as
                  this state.

     FACTS-ONLY (v0.4.1, same rule as close.md's AAR): a row states what
     was VERIFIED, never what was intended or attempted. "branch deleted"
     only after `git branch --list` shows it gone; "worktree removed"
     only after it is off disk (removal refused for modified/untracked
     files is a NOT-removed, and never force it); DEPLOYED only per the
     deploy-evidence disposition defined above -- a row never restates
     that condition. A row may reach DEPLOYED because someone ELSE's
     deploy carried it (DCS is not the only shipper) -- record that as
     out-of-band, naming the sha or witness result that carried it,
     rather than implying DCS shipped it. Field lesson 2026-07-23: rows
     claimed a deleted branch that was still on disk and a pending
     deploy that was already live. -->


| ID | Title | Type | Priority | State | Worktree | Branch | Territory | Intake source | Opened | Closed | Outcome |
|---|---|---|---|---|---|---|---|---|---|---|---|
| {{slug}} | {{one-line title}} | {{5\|3\|1\|?}} | {{H\|M\|L or rank}} | {{QUEUED\|ACTIVE\|MERGED\|DEPLOYED\|PARKED\|KILLED\|RESOLVED}} | {{`<repo>-wt\<slug>` path, or "—" once removed, or "—" if never opened}} | {{`dcs/<slug>`, or "—" if never opened (Type 5 has none)}} | {{glob(s) -- 201 blast radius initially, refined to the IAP partition's union after /dcs-plan}} | {{Owner chat / audit_results id / vault tech-debt / ...}} | {{date, or "—" while still QUEUED}} | {{date the row left ACTIVE (merged/parked/killed) or was resolved, or "—"}} | {{one-line outcome, or "—" until MERGED/DEPLOYED/RESOLVED}} |

## Notes

{{free text -- e.g. why an item is PARKED/KILLED, territory-overlap Owner
overrides (which row, which conflicting row, Owner's reasoning),
REGISTER-LOCK takeovers, links to relevant sitreps in SITREPS/}}
