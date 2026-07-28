<purpose>
The strategic layer above the P-loop: a standing session where the Owner
chairs and the main session acts as ESG Chief of Staff. Sweeps the
incident register and intake sources, presents a portfolio agenda, records
the Owner's priority and Delegation-of-Authority decisions to
STRATEGY.md / DELEGATION.md / REGISTER.md, and hands off to /dcs-new for
whatever gets opened. Does not plan or run incidents itself — that stays
the P-loop's job.
</purpose>

<required_reading>
@$HOME/.claude/dcs/references/doctrine.md
@$HOME/.claude/dcs/references/schemas.md
@$HOME/.claude/dcs/references/forms.md
</required_reading>

<process>

## 1. Prepare (Chief of Staff hat)

**(v0.3)** Resolve `esg_root` first (doctrine "Parallel operation":
`git worktree list --porcelain`, first entry — always the main checkout).
`/dcs-esg` operates on `<esg_root>/.dcs/esg/`, never on whatever tree this
session happens to be rooted in — run this session from the main checkout
by convention, but the resolution rule is what actually matters
mechanically.

Check `<esg_root>/.dcs/esg/` for `STRATEGY.md`, `DELEGATION.md`,
`REGISTER.md`. **If any are missing:** this is the founding session —
create all of them (plus an empty `SITREPS/` directory) from
`$HOME/.claude/dcs/templates/{STRATEGY,DELEGATION,REGISTER,209-SITREP}.md`.
Tell the Owner plainly this is the founding `/dcs-esg` session, and note
that `DELEGATION.md` ships with `auto_approve_type3: false` — the
delegation exists but grants nothing until the Owner amends it later in
this same session or a future one.

**Sweep intake sources:**

- `REGISTER.md`'s `QUEUED` rows — always.
- Project-specific sources, but **only** if the project's own `CLAUDE.md`
  documents them (doctrine's "Relationship to project-specific protocols"
  — DCS discovers these, it never assumes them). An example of the shape
  such a source takes (not a universal DCS default): a project whose
  `CLAUDE.md` documents an `audit_results` table with a `needs_fix` flag,
  or an `open-bugs.md` / `tech-debt.md` file in its own knowledge base —
  sweep exactly what that project's `CLAUDE.md` names, nothing invented
  for a project that documents none.

Spawn 1-2 `dcs-situation-analyst` subagents (read-only) for the sweep if
it needs file or DB digging beyond a simple read. **Never any writes** to
a project's own data during this sweep, even read-modify-write on an
audit-style table — analysts read only, same as their stem-phase charter.

**(v0.3) Run the worktree audit.** Follow doctrine's canonical checklist
("Parallel operation" section) in full: `git worktree list --porcelain`,
`git branch --list 'dcs/*' --no-merged main`, cross-referenced against
`REGISTER.md` for orphans, stale actives (older than
`esg.max_incident_age_days`), deploy-pending `MERGED` rows, and dangling
branches. Its findings feed agenda item (f) below.

## 2. Draft agenda

Present to the Owner:

(a) **Portfolio state** — active/queued/parked incidents from
    `REGISTER.md`, with ages (days since opened or queued).
(b) **New intake found** this sweep, each with a proposed type +
    priority. **(v0.6.13)** An item proposed at the lowest tier (`L`) is
    below the bar (`new.md` step 4a): when the project's own `CLAUDE.md`
    documents a lightweight backlog-style surface (doctrine's
    "Relationship to project-specific protocols"), offer routing it
    there — instead of a `REGISTER.md` row — as one of step 3's options
    alongside queueing it. With none documented, queueing is the only
    option, exactly as today.
(c) **Stale items** worth parking or killing — the Owner's call, never
    automatic.
(d) **Pending 209 sitreps** in `SITREPS/` — any file whose `Decision`
    field is still unfilled, awaiting an Owner decision. **IC-requested
    ESG activations (escalation trigger (e), doctrine principle 14) go
    FIRST** — the ESG exists precisely to answer them, and an incident is
    sitting paused behind each one.
(e) **Proposed Delegation amendments**, each with a concrete rationale
    grounded in what the register/sitreps actually show (e.g. "3 clean
    Type 3 closes this month with no bound violations → propose raising
    `max_files` 4→6") — never a generic "loosen it" suggestion with no
    evidence behind it.
(f) **(v0.3) Worktree/branch hygiene** — the worktree audit's findings
    from step 1, presented as concrete Owner decisions: for each orphan,
    stale `ACTIVE`, deploy-pending `MERGED` row, or dangling branch —
    **finish** (no action here; the Owner just needs to go run
    `/dcs-plan`/`/dcs-execute`/`/dcs-close`/`/dcs-deploy` themselves),
    **park** (worktree removed, branch kept, row → `PARKED`), or **kill**
    (worktree removed, branch deleted, row → `KILLED` with reason).
    **Parking always removes the worktree** — never leave a "parked"
    incident's directory sitting on disk; that is precisely the half-
    measure this audit exists to prevent (doctrine principle 10 amended,
    v0.3).
(g) **Field repairs reported since the last sweep** — each Owner-reported
    fix applied outside DCS's lifecycle, needing a post-hoc register row
    per the register template's `RESOLVED (field repair)` convention
    (`dcs/templates/REGISTER.md`).

## 3. Decide

One `AskUserQuestion` round per decision cluster above (`multiSelect`
where natural — e.g. picking which stale items to park). The Owner may
also free-text strategy edits outside the structured options; take those
at face value into step 4.

## 4. Record

- Update `STRATEGY.md`'s ranked priorities per the Owner's decisions.
- Update `REGISTER.md` rows per the (a)/(c)/(e)/(f) decisions above,
  applying its own two-state Territory rule (`dcs/templates/REGISTER.md`):
  a BARE GLOB LIST while State is QUEUED or ACTIVE, collapsed to ONE LINE
  each (Territory, Outcome, Intake source) the moment a row here reaches
  a terminal state. For (f) specifically: `git worktree remove <path>`
  for every park/kill decision (write `.dcs/CLOSED` into the worktree and
  note manual removal is owed if the removal fails, same fallback as
  `close.md` step 5a.4), `git branch -D dcs/<slug>` additionally for kill
  decisions only (park keeps the branch), and apply that collapse now as
  the row lands on `PARKED`/`KILLED`: Territory to a pointer at
  `IAP.md`'s partition table (its existing glob list instead, if the row
  never reached planning), Outcome to a pointer at `AAR.md`'s Outcome
  section (a one-line reason in Notes instead, if none was written),
  Intake source to a pointer at the original intake citation.
- Originate a post-hoc `REGISTER.md` row for each field repair reported
  under (g), per the register template's `RESOLVED (field repair)`
  convention (`dcs/templates/REGISTER.md`) — verify the commit reference
  (`git show <sha> --stat`) before writing the row, since its facts are
  reported rather than observed.
- If the Delegation changed: append a **new version block** to
  `DELEGATION.md` — bump `version`, date-stamp it, and keep every prior
  version block in the file exactly as written. It is the audit trail;
  never overwrite or delete a past block.
- Append an entry to the `## Sessions` log at the bottom of `STRATEGY.md`,
  capped at <= 5 LINES total (`dcs/templates/STRATEGY.md`'s own cap):
  date, a one-line summary of the decisions made, the Delegation version
  in force after this session, and an OPTIONAL one-line pointer to the
  project's own decision-rationale store — only if that project's own
  `CLAUDE.md` documents one (doctrine's "Relationship to
  project-specific protocols"). Route substantial rationale behind that
  pointer, never inline in this entry; a project with no such store
  documented gets no pointer line, and the rationale that would sit
  behind it stays out of this log too.

## 5. Hand off

If the Owner opened incident(s) this session: tell them the next step is
`/dcs-new <top-priority item>` (or `/dcs-run <top-priority item>` /
`/dcs-run --next` if they want the whole chain driven automatically).
**Do not auto-start it yourself.** `/dcs-esg` sets priorities, it does not
run incidents — that's unchanged from v0.1 through v0.3; what v0.3
changes is only that "run incidents" can now mean several, each in its
own worktree, opened one `/dcs-new` at a time (each with its own
territory check against the register — see doctrine's "Parallel
operation").

</process>
