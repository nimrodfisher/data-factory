# BigQuery

**Run queries:** `bq query --use_legacy_sql=false --format=pretty '<sql>'`. Always estimate first: `bq query --use_legacy_sql=false --dry_run '<sql>'` prints bytes processed. Use a dev dataset; label jobs: `--label=factory:run_id`.

## Dialect notes
- Dedup: `qualify row_number() over (partition by id order by _loaded_at desc) = 1` (if BigQuery rejects a bare QUALIFY, add `where true`).
- Dates: `date_trunc(d, month)`, `timestamp_trunc(ts, month)`, `date_add(d, interval 1 month)`, `date_diff(b, a, day)`, `last_day(d, month)`.
- Time zones: `timestamp` is UTC; `datetime(ts, 'America/New_York')` converts for reporting.
- Spines: `unnest(generate_date_array('2025-01-01', current_date(), interval 1 month))`.
- Nested data: `unnest(items) as item`, `struct`, `array_agg(struct(...))`.
- Safe math: `safe_divide(a, b)`, `safe_cast`.
- Identifiers with project: `` `project.dataset.table` ``.
- Upserts: `merge` statement; for incremental models prefer `insert_overwrite` on partitions.

## Cost & performance
- On-demand pricing charges **bytes scanned**: select only needed columns; `select *` on a wide table is the classic expensive mistake. `limit` does not reduce bytes.
- Partition tables by date (`partition by date(ts)`) and cluster by common filters; require partition filters on large tables (`require_partition_filter = true`).
- Use `tablesample system (1 percent)` for exploration.
- Set `--maximum_bytes_billed` on agent queries as a hard guardrail.

## Safety
Service account with `bigquery.dataViewer` on prod datasets and `bigquery.dataEditor` only on dev datasets; `bigquery.jobUser` on the project.
