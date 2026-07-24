---
tags: [dcs, decision, adr]
updated: 2026-07-25
---

# Decision: distribution, scheduling, and what stays out of doctrine

Choices made deliberately and kept **out** of the shipped doctrine —
recorded here so they are not silently relitigated.

## npm package, not a Claude Code plugin

DCS installs as a flat copy into `~/.claude/` (payload, agents, skills),
delivered by npm with a small stdlib-only Node CLI.

**Why:** the flat-install model works in every Claude Code surface today,
with no dependency on a plugin format or marketplace. It mirrors what GSD
does, which is proven at scale on the same machine.

**Cost accepted:** the user must run `dcs install` (or accept the guarded
postinstall), and upgrades need a per-project `/dcs-init` re-run because
projects hold their own copy of the gate hook. Revisit if a public plugin
marketplace makes distribution meaningfully better.

## The postinstall is guarded, not eager

`npm i -g` auto-installs into `~/.claude`, but skips in CI, skips when
`~/.claude` does not exist, honours `DCS_SKIP_POSTINSTALL`, and never
fails the surrounding npm install.

**Why:** silently modifying a user's agent configuration from an npm
lifecycle script is rude and breaks in headless contexts. Being helpful
by default is fine; being helpful *unconditionally* is not.

## DCS is scheduler-agnostic — no cron, no daemon, no self-rescheduling

`/dcs-loop` runs **one sweep per invocation**. Standing recurrence is the
Owner's job, paired with the harness's own scheduling.

**Why:** a system that can start work unattended *and* schedule itself
has no natural stopping point, and its failure modes compound while
nobody is watching. The Delegation of Authority bounds *what* may run
unattended; keeping the *when* outside DCS bounds how much can happen
before a human looks. Hard rule 2 (the loop never deploys) exists for the
same reason.

## Self-hosting: what it does and does not buy

DCS governs changes to itself (`C:\DCS` is onboarded, gate armed).

**What makes it safe:** a running session reads its workflows from
`~/.claude/dcs/` (installed) while an incident edits the repo. A
specialist rewriting `plan.md` cannot change the `plan.md` the session is
following. Install is the deploy step and happens after close — never
mid-incident.

**What it does not buy:** verification of *meaning*. The doctrine guard
checks structure — numbering, references, includes, size, encoding — not
whether a rule is wise or a field lesson true. That still requires the
Safety Officer to read the cited evidence, which is exactly the check
that would have caught the false lesson in v0.5.10.

## Deliberate non-goals

- **No automated ESG sessions.** The strategic layer convenes when the
  Owner convenes it, or when an IC requests activation (principle 14).
- **No multi-active incidents per worktree.** One `.dcs/ACTIVE` per tree;
  parallelism comes from worktrees, not from relaxing the lock.
- **No automatic conflict resolution, ever.** A merge conflict means a
  territory promise was violated; that is an escalation, not a puzzle to
  solve silently.
