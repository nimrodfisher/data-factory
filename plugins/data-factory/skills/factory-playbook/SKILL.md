---
name: factory-playbook
description: Operating manual for the Data Factory — how a request becomes a spec, a plan of work orders, sealed holdouts, station handoffs, an inspection and a ship report. Load when running /data-factory commands or acting as the Factory Manager.
---

# Data Factory Playbook

The Data Factory applies the software-factory model to data work: **humans own intent and approvals, specialist agents own the work, an independent inspector owns quality.** Specs and checks drive the agents; the human reviews the trace, not every query.

## The line
```
request → SPEC → [gate 1] → SEAL holdouts → PLAN work orders → BUILD (stations) → INSPECT → (rework ≤2) → SHIP → [gate 2] → LEARN
```

## Stations
| Station | Owns |
|---|---|
| `data-engineer` | sources → staging → marts, tests, pipelines |
| `data-analyst` | questions → reproducible findings memo |
| `data-scientist` | forecasts, experiments, models, causal estimates |
| `bi-engineer` | semantic layer, dashboards, reconciled KPIs |
| `quality-inspector` | sealed holdouts, acceptance checks, adversarial review, verdict |

## Files
Project state lives in `.data-factory/` (config, `context/`, `lessons.md`, `runs/<id>/`). Templates for every artifact are in this skill's `templates/` folder; ready-made specs for recurring work are in `recipes/`.

## How to use this skill
Read `references/router.md` and load **only** the reference it points to for the step you are on.
