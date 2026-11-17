# Orchestration

## DAG design
- One DAG per **data product / domain**, not one per table and not one monolith.
- Tasks are idempotent and parameterised by the logical date/window, never by "now".
- Dependencies come from data lineage (dbt `ref`, asset dependencies), not from wall-clock guesses ("run at 6am because loads finish at 5:30").
- Prefer asset/data-aware scheduling (Dagster assets, Airflow datasets, dbt Cloud job triggers) over cron chains.

## Reliability
| Concern | Default |
|---|---|
| Retries | 2–3 with exponential backoff for transient failures (network, locks). Zero retries for data-quality test failures — those need a human or an upstream fix. |
| Timeouts | per task, ~3× typical runtime |
| Concurrency | cap per warehouse to protect cost and locks |
| Catchup/backfill | off by default; explicit backfill commands with bounded windows |
| Failure handling | fail fast, alert once, include the failing test and a link to logs |

## SLAs & freshness
- Define the consumer SLA ("finance dashboard fresh by 07:00 UTC") and work backwards.
- Monitor freshness on marts (`max(loaded_at)`), not only job success — a green job can load zero rows.
- Volume anomaly check per run: row count vs trailing 7-day median.

## Alerting
- Route by ownership (domain owner), not to one shared channel nobody reads.
- Every alert answers: what broke, impact (which dashboards/consumers), first diagnostic step.
- Silence flapping alerts by fixing them, not muting them.

## What the Data Factory ships
Schedules are delivered as code in a PR, **disabled by default**, with: schedule, upstream dependencies, expected runtime, owner, alert route.
