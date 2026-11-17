# Orchestrators

The factory ships schedules **as code in a PR, disabled/paused by default**.

## Airflow
- One DAG file per data product; `schedule` via cron or Datasets (data-aware: `schedule=[Dataset("warehouse://fct_mrr_monthly")]`).
- `catchup=False`, `max_active_runs=1`, `default_args` with `retries=2`, `retry_delay`, `execution_timeout`, owner, alert callback.
- Parameterise by `{{ data_interval_start }}` / `{{ data_interval_end }}`, never `now()`.
- dbt: Cosmos (`DbtTaskGroup`) renders dbt models as tasks, or a single `BashOperator` running `dbt build` for small projects.
- Ship paused: `is_paused_upon_creation=True`.

## Dagster
- Model data as **software-defined assets** (`@asset`, `@dbt_assets` via dagster-dbt); dependencies come from lineage.
- Partitions (`DailyPartitionsDefinition`) for backfills; `AutomationCondition` / schedules / sensors for triggering.
- Asset checks (`@asset_check`) mirror the factory's tests and holdout-style invariants.
- Ship schedules with `default_status=DefaultScheduleStatus.STOPPED`.

## Prefect
- `@flow` / `@task` with `retries`, `retry_delay_seconds`, `timeout_seconds`; deployments define schedules.
- `prefect-dbt` for dbt runs. Ship deployments with the schedule inactive (`paused: true`).

## dbt Cloud
Jobs with `dbt build`; deferral to prod for CI ("Slim CI" on PRs). The factory writes the job spec in the PR description; a human creates/enables it.

## GitHub Actions / cron
Fine for small teams: a workflow with `schedule:` running `dbt build --target prod` **from CI**, with secrets in the repo settings. The factory proposes the workflow file with the schedule commented out.
