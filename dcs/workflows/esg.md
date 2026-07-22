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

Check `<project>/.dcs/esg/` for `STRATEGY.md`, `DELEGATION.md`,
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

## 2. Draft agenda

Present to the Owner:

(a) **Portfolio state** — active/queued/parked incidents from
    `REGISTER.md`, with ages (days since opened or queued).
(b) **New intake found** this sweep, each with a proposed type + priority.
(c) **Stale items** worth parking or killing — the Owner's call, never
    automatic.
(d) **Pending 209 sitreps** in `SITREPS/` — any file whose `Decision`
    field is still unfilled, awaiting an Owner decision.
(e) **Proposed Delegation amendments**, each with a concrete rationale
    grounded in what the register/sitreps actually show (e.g. "3 clean
    Type 3 closes this month with no bound violations → propose raising
    `max_files` 4→6") — never a generic "loosen it" suggestion with no
    evidence behind it.

## 3. Decide

One `AskUserQuestion` round per decision cluster above (`multiSelect`
where natural — e.g. picking which stale items to park). The Owner may
also free-text strategy edits outside the structured options; take those
at face value into step 4.

## 4. Record

- Update `STRATEGY.md`'s ranked priorities per the Owner's decisions.
- Update `REGISTER.md` rows per the (a)/(c)/(e) decisions above.
- If the Delegation changed: append a **new version block** to
  `DELEGATION.md` — bump `version`, date-stamp it, and keep every prior
  version block in the file exactly as written. It is the audit trail;
  never overwrite or delete a past block.
- Append an entry to the `## Sessions` log at the bottom of `STRATEGY.md`:
  date, one-line summary of the decisions made, and the Delegation version
  in force after this session.

## 5. Hand off

If the Owner opened incident(s) this session: tell them the next step is
`/dcs-new <top-priority item>` (or `/dcs-run <top-priority item>` /
`/dcs-run --next` if they want the whole chain driven automatically).
**Do not auto-start it yourself.** One incident active at a time still
holds — doctrine's v0.1 constraints are unchanged by the ESG layer;
`/dcs-esg` sets priorities, it does not run incidents.

</process>
