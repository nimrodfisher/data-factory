# DuckDB (local files, MotherDuck, demos)

**Run queries:** `duckdb <file>.duckdb -c "<sql>"`, or Python `duckdb.connect('<file>').sql("<sql>").show()`. MotherDuck: `duckdb "md:<db>"`. Great for local development, CSV/Parquet exploration and the factory demo.

## Dialect notes
- Dedup: `qualify row_number() over (partition by id order by _loaded_at desc) = 1`.
- Dates: `date_trunc('month', ts)`, `ts + interval 1 month`, `date_diff('day', a, b)`, `last_day(d)`.
- Spines: `select unnest(generate_series(date '2025-01-01', date '2026-10-01', interval 1 month))` or `range(...)`.
- Read files directly: `select * from 'data/*.parquet'`, `read_csv_auto('x.csv')`.
- Friendly SQL: `group by all`, `order by all`, `select * exclude (col)`, `columns('amount_.*')`, `count(*) filter (where …)`.
- `summarize <table>` gives a quick profile (min/max/nulls/approx unique) — use it when profiling sources.

## Notes
- Single-writer: one process writes a database file at a time. Close connections in scripts.
- Fast enough for tens of millions of rows on a laptop; use Parquet for anything large.
- `dbt-duckdb` adapter if the project uses dbt.
