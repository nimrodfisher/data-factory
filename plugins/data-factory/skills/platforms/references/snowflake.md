# Snowflake

**Run queries:** Snowflake CLI `snow sql -q "<sql>" -c <connection>` (or legacy `snowsql -q`). Use a dev role and dev database/schema; set `QUERY_TAG = 'data-factory:<run>'` so runs are traceable.

## Dialect notes
- Dedup: `qualify row_number() over (partition by id order by _loaded_at desc) = 1`.
- Dates: `date_trunc('month', ts)`, `dateadd(month, 1, d)`, `datediff('day', a, b)`, `last_day(d)`.
- Time zones: `convert_timezone('UTC', 'America/New_York', ts)`; know whether columns are `TIMESTAMP_NTZ`/`LTZ`/`TZ` — NTZ is the usual raw type and carries no zone.
- Semi-structured: `payload:customer.id::string`, `lateral flatten(input => payload:items)`.
- Identifiers are uppercased unless quoted — avoid quoted mixed-case names.
- `generator(rowcount => n)` + `seq4()` for spines; or `dbt_utils.date_spine`.
- `merge into t using s on … when matched then update … when not matched then insert …` for upserts.

## Cost & performance
- Warehouse size × runtime = credits. Use an XS/S warehouse for agent exploration; auto-suspend ≤ 60s.
- Pruning: filter on clustering/date columns with ranges; check `Partitions scanned / total` in the query profile.
- `limit` does not reduce scan cost on its own — filter first. Use `sample (1)` for exploration.
- Zero-copy `clone` a prod table into dev for safe experiments: `create table dev.x clone prod.x;`.
- Results cache: identical queries within 24h are free — don't defeat it with `current_timestamp()` in exploration queries.

## Safety
Never use `ACCOUNTADMIN`/`SYSADMIN` for agent work. Grant the agent role `USAGE`+`SELECT` on prod and `ALL` only on dev schemas. Time Travel (`at(offset => -60*5)`) can recover mistakes in dev.
