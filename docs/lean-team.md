---
title: "Running a lean data team with AI agents"
description: "How one or two data people run a full AI data team: roles, setup, weekly rhythm and a scorecard."
---
# Running a lean data team with the factory

**The model:** 1–2 data people run the factory; the factory does the station work; stakeholders send requests in and get verified answers out.

```
Stakeholders ──requests──► Factory (5 agents) ──PRs, memos, dashboards──► Stakeholders
                               ▲          │
                   specs, truths,       traces,
                   approvals            verdicts
                               │          ▼
                        Data lead (you) — owns intent, definitions, truths, shipping
```

## Who does what

| Role | Who | Owns |
|---|---|---|
| **Data lead** (factory owner) | you | approves specs and ships · curates `metrics.md` and `truths.md` · decides autonomy · reviews inspector verdicts |
| **Second data person** (optional) | analytics/data engineer | reviews pipeline PRs · grows the marts the factory builds on · adds platform knowledge |
| **The factory** | 5 agents | everything between an approved spec and a ship report |
| **Stakeholders** | everyone else | ask in plain words, name the decision, read the answer |

## Set it up — day 1, week 1, month 1

### Day 1 (1 hour)
1. Install the plugin in your data repo (the one with dbt / SQL): `/plugin install data-factory --marketplace nimrodfisher/data-factory`
2. Run `/data-factory:init`. Answer its ≤3 questions (how to run SQL on dev, what is prod).
3. Give the factory a **dev-only** warehouse role. Read on prod sources, write only to a dev schema.
4. Fill `context/metrics.md` with your top 5 metrics and `context/truths.md` with 3 numbers from finance or the last board deck.
5. Run one real question you already know the answer to. Compare.

### Week 1
- Route every incoming request through `/data-factory:spec` first, even ones you build by hand. You'll see the value of definitions immediately.
- Run 3–5 real requests end to end with `autonomy: gated`.
- After each run, read `lessons.md` — it's where the factory gets smarter.
- Commit `.claude/settings.json` ([template](https://github.com/nimrodfisher/data-factory/blob/main/integrations/claude/settings.json)) so anyone opening the repo gets the plugin.

### Month 1
- Put the weekly KPI review on a schedule ([template](https://github.com/nimrodfisher/data-factory/blob/main/integrations/github/scheduled-recipe.yml)).
- Open the request door: GitHub issue form or Slack ([how](interfaces.md)).
- Move recurring requests that keep passing inspection to `lights-out`.
- Save every request that repeats as a spec in `.data-factory/specs/`.

## Your weekly rhythm (≈ 3 hours of factory management)

| When | What | Time |
|---|---|---|
| Daily | approve new specs (Gate 1), merge/ship PRs (Gate 2) | 15–20 min |
| Monday | skim the automatic KPI review PR | 10 min |
| Friday | `/data-factory:status` — anything stuck? read new lessons, update `truths.md` with the latest finance numbers | 30 min |
| Monthly | review the factory scorecard (below), promote/demote autonomy | 30 min |

The rest of your week goes to what the factory can't do: understanding the business, deciding what matters, and building trust with stakeholders.

## Factory scorecard — is it working?

| Metric | Healthy | If not |
|---|---|---|
| First-pass inspection PASS rate | > 60% and rising | weak specs or missing context — improve `metrics.md` / `sources.md` |
| Rework loops per run | ≤ 1 | builders hitting the same trap — add it to `sources.md` |
| Holdouts using truth anchors | ≥ 1 per run | add more numbers to `truths.md` |
| Time from request to ship report | hours, not days | specs too big — split them |
| Human edits to ship reports | rare | definitions disagree with stakeholders — fix `metrics.md` |
| BLOCK verdicts | rare, and always resolved by a definition or source fix | |

`/data-factory:status` gives you the raw material; the trace in `.data-factory/runs/` has the rest.

## What NOT to hand over
- **Deciding what matters.** The factory answers questions; you pick which questions.
- **Definitions.** It proposes; you (and finance) decide.
- **Production.** It prepares PRs; humans merge and deploy.
- **Truth.** If `truths.md` is empty, the inspector can only check internal consistency. Keep it fed.
