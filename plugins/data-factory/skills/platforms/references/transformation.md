# Transformation tools: dbt & SQLMesh

## dbt
| Need | How |
|---|---|
| Run in dev | `dbt build --select <model>+ --target dev` (build = run + test) |
| Preview | `dbt show --select <model> --limit 20` or `dbt show --inline "<sql>"` |
| Only changed | `dbt build --select state:modified+ --defer --state <prod-artifacts>` |
| Compile to inspect SQL | `dbt compile --select <model>` → `target/compiled/…` |
| Sources & freshness | `sources.yml` with `loaded_at_field` + `freshness:`; `dbt source freshness` |
| Tests | generic (`unique`, `not_null`, `accepted_values`, `relationships`) under `data_tests:`; singular SQL tests in `tests/`; `dbt_utils.unique_combination_of_columns`; `dbt_expectations` for distributions |
| Contracts | `config: contract: {enforced: true}` with typed columns on marts |
| Incremental | `materialized='incremental'`, `unique_key`, `incremental_strategy` (merge / insert_overwrite / delete+insert / microbatch), `{% if is_incremental() %}` filter with lookback |
| Snapshots | SCD2 via `snapshots/` (`strategy: timestamp` or `check`) |
| Docs | `description:` on models/columns; `dbt docs generate` |
| Semantic layer | `semantic_models:` + `metrics:` (MetricFlow) |

Conventions: one YAML per model folder (`_<folder>__models.yml`), `ref()` everything, never hard-code schema names, staging models as views, marts as tables/incremental.
**Never** run with `--target prod` (the safety hook blocks it). Shipping = PR; CI/dbt Cloud deploys.

## SQLMesh
- Environments are virtual: `sqlmesh plan dev` creates a dev environment without copying data; `sqlmesh plan` (prod) is the human's job.
- Models declare `kind` (`FULL`, `INCREMENTAL_BY_TIME_RANGE`, `INCREMENTAL_BY_UNIQUE_KEY`, `SCD_TYPE_2`), `grain`, and `audits`.
- `sqlmesh test` for unit tests with fixture data; `sqlmesh audit` for data audits; `sqlmesh table_diff` to compare dev vs prod.
- Column-level lineage is built in — use it to report downstream impact in the PR.

## No transformation tool (`transform: none`)
Write plain `.sql` files in `paths.models` named by layer, plus a small runner script that executes them in dependency order against dev and runs assertion queries. Keep the dbt naming conventions so migrating later is trivial.
