---
name: dcs-deploy
description: "DCS deploy train (v0.3): Owner-gated, serialized ship of every incident merged to main but not yet deployed. Takes DEPLOY-LOCK, runs the worktree audit, verifies main is clean, lists MERGED rows for Owner confirmation, runs the project's own documented deploy command, verifies the deployed-version marker actually advanced, then marks rows DEPLOYED and deletes their branches. Never run unattended — /dcs-loop never calls this. Use when the Owner wants to ship one or more merged, Safety-passed incidents."
argument-hint: "[notes]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
---

<objective>
Run the deploy train: resolve `esg_root` and take `DEPLOY-LOCK`, run the
canonical worktree audit (doctrine "Parallel operation"), verify the main
checkout is clean, list `REGISTER.md`'s `MERGED` rows for an explicit
Owner go/no-go, run the project's own documented deploy command (never
invented), verify its deployed-version marker actually advanced
(facts-only rule), move shipped rows to `DEPLOYED`, delete their `dcs/*`
branches, and release the lock. Orchestrates; the project's own deploy
script does the actual work.
</objective>

<execution_context>
@$HOME/.claude/dcs/workflows/deploy.md
</execution_context>

<context>
$ARGUMENTS
</context>
