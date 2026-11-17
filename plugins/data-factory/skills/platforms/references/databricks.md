# Databricks (Databricks SQL / Spark SQL, Unity Catalog)

**Run queries:** the Databricks SQL CLI (`dbsqlcli -e "<sql>"`), a Python script using `databricks-sql-connector`, `dbt show` with the dbt-databricks adapter, or a connected Databricks MCP server. Point at a SQL warehouse and a dev catalog/schema (`dev_catalog.analytics_dev`).

## Dialect notes
- Three-level names: `catalog.schema.table`.
- Dedup: `qualify row_number() over (partition by id order by _loaded_at desc) = 1` (supported in recent runtimes; otherwise wrap in a subquery).
- Dates: `date_trunc('MONTH', ts)`, `add_months(d, 1)`, `datediff(end, start)`, `last_day(d)`.
- Time zones: `from_utc_timestamp(ts, 'America/New_York')`; session time zone affects `current_timestamp()`.
- Spines: `explode(sequence(to_date('2025-01-01'), current_date(), interval 1 month))`.
- Upserts: `merge into` on Delta tables; `insert overwrite … partition` for partition replacement.
- Semi-structured: `payload:customer.id` (variant/JSON path), `from_json`, `explode`.

## Performance & cost
- Delta: `optimize` + liquid clustering (`cluster by`) or Z-order on common filter columns; avoid many small files.
- Photon-enabled SQL warehouses for BI/SQL; serverless with auto-stop for agent work.
- Filter on partition/clustering columns with ranges; check the query profile for files pruned.
- Delta time travel (`version as of`) for debugging and recovery in dev.

## ML
MLflow for experiment tracking and model registry; feature tables in Unity Catalog. The data-scientist station should log runs to MLflow when available and still write the model card to the repo.

## Safety
Agent principal gets `USE CATALOG`/`SELECT` on prod and `ALL PRIVILEGES` only on the dev schema.
