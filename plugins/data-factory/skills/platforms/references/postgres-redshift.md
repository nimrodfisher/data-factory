# Postgres & Redshift

**Run queries:** `psql "$DATABASE_URL" -c "<sql>"` (works for both; Redshift also via `redshift-data` API / `aws redshift-data execute-statement`). Use a dev schema and a read-only role on prod schemas. Add `-v ON_ERROR_STOP=1` for scripts.

## Shared dialect notes
- Dates: `date_trunc('month', ts)`, `ts + interval '1 month'`, `ts::date`.
- Time zones: `ts at time zone 'UTC' at time zone 'America/New_York'` (Postgres `timestamptz` vs `timestamp` matters).
- Null-safe compare: `a is distinct from b`.
- Upserts: Postgres `insert … on conflict (key) do update`; Redshift `merge` (or delete+insert in a transaction).

## Postgres specifics
- **No `QUALIFY`** — dedup with `distinct on (id) … order by id, _loaded_at desc`, or a `row_number()` subquery.
- Spines: `generate_series('2025-01-01'::date, current_date, interval '1 month')`.
- `filter (where …)` on aggregates; `percentile_cont(0.5) within group (order by x)`.
- It is OLTP-first: big analytical scans on a production replica can hurt the app — query a replica/warehouse copy, use `explain analyze` for heavy queries, add `statement_timeout`.

## Redshift specifics
- `qualify` supported. No `generate_series` on tables (leader-node only) — build spines from a numbers table or `dbt_utils.date_spine`.
- Distribution (`distkey`) and sort keys drive performance: distribute large facts on the join key, sort on the date filter column. Avoid broadcasting big tables.
- `vacuum` / `analyze` after big loads (automatic in recent versions but check). Use Spectrum or `unload` for very large exports.
- `listagg` instead of `string_agg`; `approximate count(distinct x)`.
