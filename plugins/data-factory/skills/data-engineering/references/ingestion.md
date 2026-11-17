# Ingestion & Incremental Loads

## Choose the pattern
| Pattern | Use when | Watch out for |
|---|---|---|
| Full refresh | small tables (< ~10M rows), sources without reliable timestamps | cost grows silently; schedule size checks |
| Incremental append | immutable events (clicks, logs) | late-arriving events → use a lookback window |
| Incremental merge/upsert | mutable entities (orders, subscriptions) with a primary key + `updated_at` | deletes are invisible unless the source emits them |
| CDC (log-based) | high-volume OLTP sources, need deletes and history | ordering, tombstones, schema drift; land the change log raw |
| Snapshot (SCD2) | source overwrites state and you need history | snapshot cadence = resolution of your history |

## Incremental model rules
- Filter on a **watermark** with a lookback: `where updated_at >= (select max(updated_at) from {{ this }}) - interval '3 days'`. The lookback absorbs late data; the merge key makes it idempotent.
- Always define a `unique_key` for merge. If the source has no reliable key, build a surrogate from the natural key columns (hash) and **test its uniqueness**.
- Make backfills a first-class path: the model must work for an arbitrary `[start, end)` window, not only "since last run".
- Partition/cluster target tables on the watermark or event date.

## Deduplication
Duplicates have causes. Find the cause before choosing the fix:
| Cause | Signature | Fix |
|---|---|---|
| Connector re-sync / replay | identical business key, different `_loaded_at`/`_synced_at` | `qualify row_number() over (partition by key order by _loaded_at desc) = 1` |
| Source update history | same key, different `updated_at` and changed fields | keep latest per key (or snapshot if history matters) |
| Fan-out join | duplicates appear only after a join | fix the join grain; never `distinct` it away |
| Genuine repeats | same customer buys twice | not a duplicate — check the grain |
Record every dedup rule in `context/sources.md`.

## Late-arriving & out-of-order data
- Separate **event time** (when it happened) from **load time** (when we saw it). Model on event time, monitor on load time.
- Dimensions arriving after facts → join with "unknown member" defaults (`-1` key) and repair on the next run, or build facts with a lookback.

## Data contracts (source ↔ warehouse)
A contract states: schema (columns, types, nullability), primary key, freshness SLA, volume range, owner, and change policy. Enforce at staging:
- schema tests (column exists, type), key tests, `accepted_values` on enums,
- freshness (`max(loaded_at)` within SLA),
- volume (today's row count within ±X% of trailing 7-day median).
Breaking change → the pipeline fails loudly, not silently nulls.

## Backfill checklist
1. Run on a copy/dev target first; compare row counts and key metrics with the current table.
2. Backfill in bounded windows (by month/day) so failures are resumable.
3. Disable downstream schedules or tell consumers.
4. Re-run downstream models and their tests.
