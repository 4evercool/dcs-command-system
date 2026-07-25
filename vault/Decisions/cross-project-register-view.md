---
tags: [dcs, decision]
updated: 2026-07-25
---

# Decision: no cross-project register view

**Decided:** 2026-07-25, second `/dcs-esg` session
**Status:** closed — register row `cross-project-register-view` `KILLED`
**Reopen if:** a second DCS-onboarded project makes the pain concrete

## The question

Each project's `REGISTER.md` is its own portfolio, and that is correct —
doctrine principle 6 as amended by v0.6.2 ("territory never leaves its own
project: one session, one project"), enforced at plan time by `plan.md` lint
check 8. `/dcs-status --campaign` is per-project by design, for the same reason.

But an Owner running DCS across several repos has no single place showing what
is in flight everywhere. `vault/Backlog.md` raised this at founding, explicitly
"noted so it is a decision rather than an oversight."

## The decision

**Not building it.** Recorded here so it stays decided rather than being
rediscovered and relitigated.

## Why

**The thing that would make it valuable is the thing that makes it wrong.** A
cross-project view is only useful if it can *act* — reorder priorities, spot a
territory conflict, tell you what to open next. But every one of those acts is
scoped to a project by construction: territory partitioning is per-repo because
the gate cannot judge a tree it has no `.dcs/` for; the Delegation is per-repo
because "routine" means different things in different codebases; `esg_root`
resolution is per-repo by definition. A view that aggregates without being able
to act on the aggregate is a dashboard, and DCS has no other dashboards.

**The cost is not the reading, it is the writing.** A cross-project register
would be a second write target on every state transition — open, plan, close,
deploy — each of which currently writes exactly one register under a courtesy
lock. Doubling that surface to serve a read-only convenience inverts the
cost/benefit, and a second store that drifts from the first is precisely the
rot `vault/00-Navigation.md` warns about in its own charter.

**There is no evidence of the pain.** As of this decision DCS is onboarded in
exactly one repo. The item was queued on a hypothetical, and the honest read of
`vault/Backlog.md` item 3's own wording — *"not obviously worth solving"* — is
that its author already suspected this.

## What to do instead, if it comes up

Run `/dcs-status --campaign` per repo. If an Owner genuinely runs three or more
DCS projects at once and finds themselves doing that by hand every morning,
**that** is the evidence this decision lacks, and it should be reopened with it.

## Links

- [[Backlog]] item 3 — where this was raised
- [[Decisions/distribution-and-scheduling]] — the other choices kept out of doctrine
