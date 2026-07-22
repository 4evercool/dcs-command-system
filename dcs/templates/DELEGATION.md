<!--
DELEGATION.md -- the Delegation of Authority. Human-readable terms above
each version block, machine-readable delegation-bounds JSON block below it
-- workflows (plan.md, run.md, loop.md) parse ONLY the JSON block, never
this file's prose (schemas.md #7 is the authoritative shape). Amended by
appending a NEW version block during a /dcs-esg session, by the Owner --
never edit a past version block in place, it is the audit trail.

Template default: auto_approve_type3=false -- the delegation exists but
grants NOTHING until the Owner explicitly amends it at a real /dcs-esg
session. This is the safe starting state.
-->

# Delegation of Authority — {{project name}}

## v1 (founding version, {{date}})

The IC may approve Type 3 IAPs on the Owner's behalf when ALL bounds below
hold. Outside bounds, or for Type 1, Owner approval is required exactly as
in v0.1 (`AskUserQuestion`). Revocable, or amendable, at any `/dcs-esg`
session.

```delegation-bounds
{
  "version": 1,
  "auto_approve_type3": false,
  "max_files": {{N, e.g. 4}},
  "forbidden_globs": ["**/migrations.py", "**/auth/**", "**/payment*/**"],
  "forbidden_topics": ["schema migration", "payments", "auth/JWT", "deploy scripts"],
  "require_tests_green": true,
  "max_specialists": 2,
  "deploy": {
    "auto": false,
    "auto_after_close": false,
    "frontend_only": true,
    "forbidden_globs": ["{{the project's schema-migration paths -- REQUIRED; migration-bearing deploys are never routine}}", "**/auth/**", "**/payment*/**"],
    "max_rows_per_train": 3
  }
}
```

<!-- /dcs-esg appends further version blocks below this line as the
     Delegation is amended. Never delete a prior block. -->
