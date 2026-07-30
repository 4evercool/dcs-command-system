# SAFETY — Period 1

**Incident:** worktree-path-propagation
**Verdict:** pass

## Verdict (verbatim)

```json
{
  "verdict": "pass",
  "refutations": [],
  "advisories": [
    {
      "finding": "execute.md line 117 says 'the worktree line is the absolute path' but git worktree list --porcelain can produce multiple worktree lines. In this repo there are two worktrees (main at C:/DCS and the incident at C:/DCS-wt/worktree-path-propagation). Without specifying how to select the right one — by matching the branch line to refs/heads/dcs/<slug>, or by matching the worktree line to the current directory — the instruction is formally ambiguous. In practice the session runs from inside the worktree, so an operator would figure it out, but an explicit filter by branch name would match the 202-OBJECTIVES criterion text ('по имени ветки dcs/<slug>') precisely.",
      "fix": "Append to line 118: 'Match the branch line refs/heads/dcs/<slug> to the slug, then take the preceding worktree line for that entry.'"
    }
  ],
  "checked": [
    "git diff --stat at C:/dcs-wt/worktree-path-propagation: confirmed only 3 files touched",
    "Read the full unified diff: 12 insertions, 1 deletion across 3 files",
    "Independent re-run of python tests/test_dcs_gate.py: 100/100 passed",
    "Independent re-run of python tests/test_dcs_intake.py: 10/10 passed",
    "Independent re-run of python tests/test_doctrine_integrity.py: 122/122 passed",
    "grep -rn 'worktree_root' across worktree: confirmed at least one match in each target file",
    "wc -l dcs/workflows/execute.md: 449, under the 450 ceiling",
    "grep 'git worktree list --porcelain' dcs/workflows/execute.md: confirmed",
    "Manual read of agents/dcs-ops-specialist.md: worktree_root in <inputs> + territory-resolution rule confirmed",
    "Manual read of dcs/templates/204-TASKING.md: ## Worktree root section with {{worktree_root}} confirmed",
    "Manual read of dcs/workflows/execute.md: worktree_root computation + pass-to-specialist confirmed",
    "No BOM, CRLF, or NUL bytes in modified files",
    "No principle-15 durable claims added"
  ]
}
```

## Advisory resolution

**Advisory 1** (execute.md branch-matching ambiguity): исправлено. Строки 117-119 теперь содержат явную инструкцию: «match the branch line `refs/heads/dcs/<slug>`, then take the preceding `worktree` line». Записано IC, без повторной проверки Safety Officer — офицер уже выдал pass по всем критериям.
