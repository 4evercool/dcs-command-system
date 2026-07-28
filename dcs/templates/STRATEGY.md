<!--
STRATEGY.md -- long-term objectives + ranked priorities, owned by the ESG
(Owner decides, Chief of Staff drafts), written/amended during /dcs-esg
sessions. Incident-centric: decides WHICH incidents get opened and in what
order -- never HOW they get implemented (that's the P-loop's job, inside
/dcs-plan). The Sessions log at the bottom is append-only, same discipline
as 214-LOG.md -- never rewrite a past entry.
-->

# STRATEGY — {{project name}}

**Founded:** {{date}} (first `/dcs-esg` session)
**Chair:** Owner
**Chief of Staff:** main session (any model, per v0.1.1 transfer-of-command doctrine)

## Long-term objectives

<!-- Free text, Owner's own words. What does "the project is in good
     shape" mean, at a level above any single incident. -->

{{objective 1}}
{{objective 2}}

## Ranked priorities

<!-- What gets opened next, and why. This is what /dcs-esg step 5 and
     /dcs-new's "next from the register" intake read to decide what's
     next. Kept in sync with REGISTER.md's QUEUED order -- if they drift,
     REGISTER.md is the operational truth and this list should be
     reconciled at the next /dcs-esg session. -->

1. {{priority item -- rationale}}
2. {{priority item -- rationale}}

## Sessions

<!-- Append-only log, one entry per /dcs-esg session. If a past decision
     later looks wrong, the next session's entry says so -- this stays a
     true record of what was decided when, not a tidied-up version.

     CAP: <= 5 LINES total per entry -- a number, not an adjective.
     Nothing beyond these four fits inside the cap:
       1. the `### {{date}}` heading itself;
       2. one line: a one-line summary of the decisions made this
          session;
       3. one line: the Delegation version in force after this session;
       4. OPTIONAL one line: a pointer into the project's own
          decision-rationale store -- ONLY if that project's own
          `CLAUDE.md` documents one (doctrine's "Relationship to
          project-specific protocols"). Name that store by whatever the
          project calls it; never invent one for a project that
          documents none.
     Substantial decision rationale -- the "why," alternatives
     considered, evidence behind a Delegation change -- belongs in that
     project-specific store, reached via line 4's pointer, never written
     inline here. A session with no such store documented simply has no
     line 4, and the rationale that would have gone behind it stays out
     of this file too, not inline instead. -->

### {{date}}

- Decisions: {{one-line summary of what changed this session}}
- Delegation version in force after this session: v{{N}}
- {{optional one-line pointer to this project's own decision-rationale
  store, only if its CLAUDE.md documents one -- omit this line entirely
  otherwise}}
