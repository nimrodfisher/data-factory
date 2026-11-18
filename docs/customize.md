---
title: "Customize Data Factory for your data stack"
description: "Point the AI data team at Snowflake, BigQuery, Databricks, dbt, Looker or Power BI, and add your own stations and knowledge."
---
# Customize the factory

Everything is markdown and YAML. Change it like any other code.

## Point it at your stack
Run `/data-factory:init` — it detects dbt/SQLMesh, the warehouse, orchestrator and BI tool, then writes `.data-factory/factory.yaml`. Key fields:

| Field | Examples |
|---|---|
| `stack.warehouse` | `snowflake`, `bigquery`, `databricks`, `redshift`, `postgres`, `duckdb` |
| `stack.transform` | `dbt`, `sqlmesh`, `none` |
| `stack.bi` | `looker`, `powerbi`, `tableau`, `metabase`, `superset`, `lightdash`, `hex`, `streamlit`, `html` |
| `stack.query_runner` | `snow sql -q`, `bq query --use_legacy_sql=false`, `psql $DATABASE_URL -c`, `mcp:<server>` |
| `environments.prod` | schema/target the safety hook protects |
| `autonomy` | `supervised`, `gated`, `lights-out` |

Using a database MCP server (Snowflake, BigQuery, Postgres…)? Set `query_runner: mcp:<server-name>` — stations will use its query tool.

## Make it smarter about *your* business (biggest win)
| File | Put here |
|---|---|
| `context/metrics.md` | your official metric definitions |
| `context/truths.md` | 3–5 numbers from finance/CRM/board decks with tolerances — these power the inspector |
| `context/sources.md` | source quirks: re-syncs, late data, test accounts |
| `context/business.md` | pricing changes, launches, org events |

Or just tell it: `/data-factory:learn active user = 1+ session in 28 days, excludes internal`.

## Turn stations on/off or swap them
`stations:` in `factory.yaml`. Set `data-scientist: off` if you don't need it. To use your own agent for a station, put its name there (e.g. `bi-engineer: my-looker-agent`) and keep the handoff format.

## Add a station
Create `plugins/data-factory/agents/<name>.md` following the existing agents: frontmatter (`name`, `description`, `tools`), a protocol (read work order → load skill → build → verify → handoff), and non-negotiables (dev only, never read `sealed/`). Add a routing rule in `skills/factory-playbook/references/planning-and-dispatch.md`. Ideas: analytics-engineer for a semantic layer, ML engineer for deployment, data steward for governance.

## Add a platform
Copy the closest file in `skills/platforms/references/`, adapt: how to run queries safely, dialect notes, cost/performance, safety (roles/permissions). Add one row to the router. PRs welcome.

## Add knowledge
Skills use a 3-layer structure so agents only load what they need:
```
skills/<skill>/SKILL.md              ← lean: principles + "read the router"
skills/<skill>/references/router.md  ← which reference for which task
skills/<skill>/references/*.md       ← deep content, loaded on demand
```
Add a reference file and one router row.

## Use outside Claude Code
The agents and skills are plain markdown. Codex, Cursor, Gemini CLI and other agent tools can use `skills/*` directly (Agent Skills format) and the agent files as role prompts; see `AGENTS.md` at the repo root.

## Safety interlock
`hooks/hooks.json` runs `scripts/sql_guard.py` before every shell command. It blocks `DROP`/`TRUNCATE`, `DELETE`/`UPDATE` without `WHERE`, writes to the `environments.prod` schema, and dbt/SQLMesh prod targets. Humans can bypass for a session with `DATA_FACTORY_ALLOW_DESTRUCTIVE=1` set before launching Claude Code. Treat it as a seatbelt, not a permission system — give agents a dev-only role in your warehouse too.
