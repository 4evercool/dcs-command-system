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
                  this state. A field repair -- an Owner-authorized fix
                  applied entirely outside the incident lifecycle -- is
                  recorded under this same state, qualified: the State
                  cell reads the exact literal `RESOLVED (field repair)`
                  (see the block below).

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

<!-- FIELD REPAIR (a RESOLVED qualifier, not a new state): an
     Owner-authorized fix applied entirely outside DCS's lifecycle -- no
     201, no typing decision, no worktree, no IAP, no Safety review -- is
     recorded under this same terminal state, qualified. State reads the
     exact literal `RESOLVED (field repair)`, the same qualifier shape as
     `MERGED (deploy pending)` above. This differs from RESOLVED's inline
     case above by one clause: that case was a typed incident that ran
     DCS's process end to end, only without a worktree; this one never
     enters that process at all.

     CELLS: every cell that would otherwise record a DCS act reads the
     template's existing em-dash when that act never happened -- Type
     (never typed), Priority (never ranked), Worktree and Branch (never
     opened), Opened (the row never had a QUEUED/ACTIVE phase to leave).
     Closed and Outcome are filled together, exactly as RESOLVED already
     requires; Closed carries the date the fix was applied.

     OUTCOME MINIMUM, all three: one line stating what was fixed; a
     commit/diff reference given as a regenerating command -- `git show
     <sha> --stat` or equivalent -- never a bare sha; and an explicit word
     on whether a retroactive Safety look was done, "none" written out
     when it was not, never left silent.

     WRITER: the Chief of Staff, during /dcs-esg, on the Owner reporting a
     fix made outside the lifecycle. Every other writer of this file
     either transitions a row that already exists or originates one into
     QUEUED/ACTIVE; this is the one writer that ORIGINATES a row directly
     in a terminal state, with no prior QUEUED/ACTIVE phase at all.
     Because the row's facts are REPORTED to the writing session rather
     than observed by it, FACTS-ONLY carries one added rule this writer
     alone needs: verify the commit reference first (`git show <sha>
     --stat`) before the row is written. -->

<!-- TERRITORY / OUTCOME / INTAKE SOURCE -- two-state column shape: each
     of these three columns has exactly two allowed shapes, selected by
     the row's own State, never a mix within one row.

     While State is QUEUED or ACTIVE: Territory is a BARE GLOB LIST --
     glob(s) only, no rationale prose -- because `new.md` step 7b scans
     this column across every ACTIVE row to test for a territory
     conflict; prose there is invisible to that scan, and unscannable to
     a human skimming the column too. Outcome stays the template's own
     em-dash (nothing to report yet); Intake source is whatever free text
     names where the incident came from.

     The moment a row transitions to ANY terminal state (MERGED /
     DEPLOYED / PARKED / KILLED / RESOLVED): Territory, Outcome, and
     Intake source EACH collapse to ONE LINE pointing into the incident's
     own authoritative record, instead of restating it in the row --
       Territory     -> a pointer at IAP.md's partition table (e.g. "see
                         IAP.md partition table") -- the union this row
                         carried while ACTIVE is already exact there. A
                         row that reaches a terminal state before any
                         IAP.md ever existed (QUEUED, parked or killed
                         pre-plan) keeps its existing glob list instead --
                         there is nothing yet to point at.
       Outcome        -> a pointer at AAR.md's Outcome section (e.g. "see
                         AAR.md Outcome"), for any state that wrote one. A
                         state with no AAR (PARKED, KILLED, a field
                         repair) keeps a one-line free-text outcome
                         instead.
       Intake source  -> a pointer at the original intake citation (e.g.
                         "see 201-BRIEF.md Intake source"), never a
                         restatement of the citation's own contents.
     The cap is a NUMBER, not an adjective -- ONE LINE each, full stop, no
     wrapped continuation. The collapse is part of the write that moves a
     row into its terminal state (see `close.md` step 5a.3, `deploy.md`'s
     MERGED -> DEPLOYED step, and `esg.md` step 4's park/kill handling) --
     never a separate pass over rows already terminal. -->

| ID | Title | Type | Priority | State | Worktree | Branch | Territory | Intake source | Opened | Closed | Outcome |
|---|---|---|---|---|---|---|---|---|---|---|---|
| {{slug}} | {{one-line title}} | {{5\|3\|1\|?}} | {{H\|M\|L or rank}} | {{QUEUED\|ACTIVE\|MERGED\|DEPLOYED\|PARKED\|KILLED\|RESOLVED}} | {{`<repo>-wt\<slug>` path, or "—" once removed, or "—" if never opened}} | {{`dcs/<slug>`, or "—" if never opened (Type 5 has none)}} | {{QUEUED/ACTIVE: glob(s) -- 201 blast radius initially, refined to the IAP partition's union after /dcs-plan. Terminal: ONE LINE pointing at IAP.md's partition table}} | {{QUEUED/ACTIVE: Owner chat / audit_results id / vault tech-debt / ... . Terminal: ONE LINE pointing at the original intake citation}} | {{date, or "—" while still QUEUED}} | {{date the row left ACTIVE (merged/parked/killed) or was resolved, or "—"}} | {{"—" until terminal. Terminal: ONE LINE pointing at AAR.md's Outcome section, or a one-line free-text outcome where no AAR exists}} |

## Example (illustrative -- neutral fiction, not a live row)

The same incident, two moments apart, showing both Territory shapes side
by side:

| ID | Title | Type | Priority | State | Worktree | Branch | Territory | Intake source | Opened | Closed | Outcome |
|---|---|---|---|---|---|---|---|---|---|---|---|
| add-retry-logic | Add retry logic to the sync job | 3 | M | ACTIVE | `<repo>-wt\add-retry-logic` | `dcs/add-retry-logic` | `src/sync/**`, `tests/sync/**` | Owner chat | 2026-01-05 | — | — |
| add-retry-logic | Add retry logic to the sync job | 3 | M | MERGED | — | `dcs/add-retry-logic` | see IAP.md partition table | see 201-BRIEF.md Intake source | 2026-01-05 | 2026-01-07 | see AAR.md Outcome |

The ACTIVE row's Territory is a bare glob list, scannable by `new.md`
step 7b. The MERGED row's Territory, Outcome, and Intake source have
each collapsed to one line pointing elsewhere, per the two-state rule
above.

## Notes

{{free text -- e.g. why an item is PARKED/KILLED, territory-overlap Owner
overrides (which row, which conflicting row, Owner's reasoning),
REGISTER-LOCK takeovers, links to relevant sitreps in SITREPS/}}
