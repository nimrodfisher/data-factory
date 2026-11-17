# data-factory (plugin)

Run a full AI data team as one person: **data-engineer, data-analyst, data-scientist, bi-engineer** and an independent **quality-inspector**, coordinated by a Factory Manager. Specs in, verified data products out — with sealed holdout checks, truth-anchor reconciliation, two human gates and a safety hook that blocks destructive SQL and production writes.

## Install
```
/plugin install data-factory --marketplace nimrodfisher/data-factory
```
(Older Claude Code: `/plugin marketplace add nimrodfisher/data-factory` then `/plugin install data-factory@data-factory`.)

## Use
1. `/data-factory:init` — detect your stack and create `.data-factory/` (config, context, memory).
2. `/data-factory:run <request>` — spec → seal → plan → build → inspect → ship → learn.
3. Also: `/data-factory:spec`, `/data-factory:inspect`, `/data-factory:status`, `/data-factory:learn`.

Works with Snowflake, BigQuery, Databricks, Redshift, Postgres, DuckDB; dbt or SQLMesh; Airflow, Dagster, Prefect; Looker, Power BI, Tableau, Metabase, Superset, Lightdash, Hex, Streamlit or a self-contained HTML dashboard.

Full docs, demo and a reference run: https://github.com/nimrodfisher/data-factory
