# Router — platforms

| `factory.yaml` value | Load |
|---|---|
| `warehouse: snowflake` | `snowflake.md` |
| `warehouse: bigquery` | `bigquery.md` |
| `warehouse: databricks` | `databricks.md` |
| `warehouse: postgres` or `redshift` | `postgres-redshift.md` |
| `warehouse: duckdb` (also MotherDuck, local files, demos) | `duckdb.md` |
| `transform: dbt` or `sqlmesh` | `transformation.md` |
| `orchestrator: airflow / dagster / prefect / dbt-cloud / github-actions` | `orchestrators.md` |
| `bi: <anything except html>` | `bi-tools.md` |
| `query_runner: mcp:<name>` | use that MCP server's query tool; still apply the warehouse reference for dialect |

Unknown platform → use ANSI SQL, check syntax with a tiny query first, and note the gap in the handoff.
