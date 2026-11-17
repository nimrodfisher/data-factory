# Testing & Reconciliation

## The data testing pyramid
| Level | What | Examples | Runs |
|---|---|---|---|
| Schema / contract | structure is as promised | column exists, type, not null on keys | every load |
| Integrity | model logic holds | unique grain, relationships, accepted values, non-overlapping SCD ranges | every build |
| Reconciliation | numbers agree with something independent | source vs mart totals, truth anchors, cross-system counts | every build / every run |
| Distribution / anomaly | data looks like it usually does | row volume vs 7-day median, null-rate drift, metric z-score | every load |
| Business assertions | domain rules | no revenue before signup; churn date ≥ start date; discounts ≤ 100% | every build |

## Inspector's standard battery for any mart used in a run
```sql
-- 1. grain
select <grain cols>, count(*) c from <mart> group by all having c > 1 limit 10;
-- 2. key nulls
select count(*) filter (where <key> is null) from <mart>;
-- 3. coverage
select min(<date>), max(<date>), count(distinct <period>) from <mart>;
-- 4. source-to-mart reconciliation (after documented dedup)
select (select sum(x) from <deduped source>) as src, (select sum(x) from <mart>) as mart;
-- 5. population exclusions
select count(*) from <mart> where is_test or is_internal;
-- 6. volume by period — look for cliffs and spikes
select <period>, count(*) from <mart> group by 1 order by 1;
```

## Reconciliation rules
- Reconcile at the **lowest common grain** possible (per month per segment beats grand totals — offsetting errors hide in totals).
- Explain every difference above tolerance with a named cause (timing, FX, exclusions, refunds). Unexplained = failed.
- Record both numbers, the delta and the tolerance in the inspection table.

## Tool mapping
| Tool | How to express |
|---|---|
| dbt | `data_tests:` (unique, not_null, relationships, accepted_values), `dbt_utils.unique_combination_of_columns`, `dbt_expectations`, singular tests in `tests/`, source `freshness:` |
| SQLMesh | `audits` |
| Great Expectations / Soda | expectation suites / SodaCL checks |
| Plain SQL | assertion queries that return rows only on failure |
| Python | `assert` in the build script + pandas checks |
