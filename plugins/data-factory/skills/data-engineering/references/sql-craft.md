# SQL Craft

## Style
- CTEs top-down: `import` CTEs (select from refs) → logical CTEs (one transformation each) → `final` → `select * from final`.
- Lowercase keywords, one column per line in marts, trailing logic commented with *why*.
- Explicit join types and explicit join keys. No `natural join`, no `using` across differently named keys.
- No `select *` in marts; fine in staging import CTEs.

## Correctness traps (check every query)
| Trap | Symptom | Guard |
|---|---|---|
| Fan-out join | sums inflate after a join | check row count before/after each join; aggregate to grain before joining |
| `NULL` in `NOT IN` | returns zero rows | use `not exists` |
| `NULL` arithmetic / comparisons | rows vanish from filters, sums ignore rows | `coalesce` deliberately; `is distinct from` for null-safe compare |
| Integer division | ratios become 0 | cast to decimal/float |
| `count(col)` vs `count(*)` | silently excludes nulls | choose deliberately; `count(distinct key)` for entities |
| Time zones | day boundaries shift, double counts around midnight | convert to the reporting zone once, in staging |
| `between` on timestamps | includes the end boundary twice across buckets | `>= start and < end` |
| Window frame defaults | running totals wrong with ties | specify `rows between …` explicitly |
| Filter in `where` on an outer-joined table | turns left join into inner join | move the filter into the `on` clause |
| Average of averages | wrong weighted mean | sum numerators / sum denominators |
| Currency mixing | sums across currencies | convert first; keep currency column |

## Validation queries to run after any change
```sql
-- grain
select key_cols, count(*) from model group by key_cols having count(*) > 1;
-- nulls on keys
select count(*) - count(key) as null_keys from model;
-- totals reconcile with source
select (select sum(amount) from source_after_dedup) - (select sum(amount) from model) as diff;
-- coverage
select min(date_col), max(date_col), count(distinct date_trunc('month', date_col)) from model;
```

## Performance & cost
- Filter early on partition/cluster columns; avoid functions on partition columns in `where` (`date(ts) = …` can block pruning — use a range on `ts`).
- Select only needed columns (columnar storage charges by bytes scanned).
- Replace `count(distinct)` on huge tables with approximate functions for exploration (`approx_count_distinct`), exact for reporting.
- Pre-aggregate in marts for dashboards; dashboards should not scan event-level tables.
- Avoid repeated self-joins for "previous row" — use `lag()`/`lead()`.
- Materialise heavy intermediate CTEs reused by several marts.
