---
name: platforms
description: Platform adapters for the Data Factory — dialect notes, safe query execution and cost/performance tips for Snowflake, BigQuery, Databricks, Postgres/Redshift and DuckDB; dbt and SQLMesh; Airflow/Dagster/Prefect; and BI tools (Looker, Power BI, Tableau, Metabase, Superset, Lightdash, Hex, Streamlit). Load the one matching factory.yaml.
---

# Platforms

The factory is platform-agnostic: stations reason in portable concepts (grain, layers, tests, metrics) and use this skill to translate to the configured stack in `.data-factory/factory.yaml → stack`.

Read `references/router.md` and load **only** the references for the configured tools.

Missing your platform? Copy the closest reference, adapt it, and open a PR — see CONTRIBUTING.md in the repo.
