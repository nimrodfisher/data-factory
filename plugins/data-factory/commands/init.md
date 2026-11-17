---
description: Set up the Data Factory in this repo — detect your data stack and create .data-factory/ (config, context, memory).
argument-hint: "[optional stack hints, e.g. 'snowflake dbt looker']"
---

Set up the Data Factory for this repository. Hints from the user: **$ARGUMENTS**

Load the `factory-playbook` skill. Its `templates/` folder holds `factory.yaml` and the `context/` templates.

1. **Detect the stack** (read-only):
   - Transform: `dbt_project.yml` → dbt (read `profiles.yml`/`target` for the warehouse) · `config.yaml` with `model_defaults` or `sqlmesh` → SQLMesh · plain `*.sql` → none.
   - Warehouse: dbt profile type, connection strings in `.env.example`, `snowflake`/`bigquery`/`databricks`/`psycopg`/`duckdb` in requirements or lockfiles.
   - Orchestrator: `dags/` with airflow imports, `dagster` / `prefect` in deps, `.github/workflows` with schedules.
   - BI: `*.lkml` → Looker · `*.pbip`/`*.pbix` → Power BI · `lightdash.yml` · `metabase` / `superset` configs · `hex` / `streamlit` apps.
   - Query runner: which CLI or MCP tool can execute SQL here (`snowsql`, `bq`, `databricks`, `psql`, `duckdb`, `dbt show`, an MCP database tool).
2. **Ask at most 3 questions** for anything you could not detect — always confirm: how to run SQL safely against **dev**, and which schema/target is **prod** (never written to).
3. **Write** `.data-factory/factory.yaml` from the template with what you found. Default `autonomy: gated`.
4. **Create** `.data-factory/context/` from the templates: `business.md`, `metrics.md`, `sources.md`, `truths.md`. Pre-fill anything discoverable (dbt model descriptions, existing metric YAML, source definitions). Leave clear `TODO` prompts for the rest.
5. Create `.data-factory/lessons.md` (from the template) and `.data-factory/runs/`. Copy the ready-made specs from the skill's `recipes/` folder into `.data-factory/specs/` (weekly KPI review, metric alert investigation, new source onboarding, experiment readout, dashboard request, monthly forecast) and fill in what you can from context.
6. Suggest adding `.data-factory/runs/*/sealed/` to `.gitignore` if the team does not want holdouts in version control.
7. Report: detected stack (table), what the user should fill in first (usually `metrics.md` and `truths.md` — they make the inspector strong), and the next commands: `/data-factory:run <request in plain words>` or `/data-factory:run weekly-kpi-review`.
