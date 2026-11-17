# Modeling

## Layers
| Layer | Prefix | Purpose | Rules |
|---|---|---|---|
| Sources | — | declared raw tables | never transformed in place |
| Staging | `stg_<source>__<entity>` | 1:1 with a source table: rename, cast, dedupe, standardise units/time zones | no joins (except trivial lookups), no business logic, view or ephemeral |
| Intermediate | `int_<entity>__<verb>` | reusable building blocks: joins, pivots, sessionisation, spine generation | not exposed to BI |
| Marts | `fct_<event>` / `dim_<entity>` | business-facing, documented, tested | explicit columns, stable names, grain stated |

## Facts & dimensions (Kimball, pragmatically)
- **Fact** = events or periodic measurements. Types: transaction (one row per event), periodic snapshot (one row per entity per period — e.g. `fct_mrr_monthly`), accumulating snapshot (one row per process instance with milestone dates — e.g. order lifecycle).
- **Dimension** = descriptive context (account, product, date). Conformed dimensions are shared across facts so metrics slice consistently.
- Wide, denormalised marts are fine for BI performance; keep the conformed `dim_` as the source of truth.

## Grain discipline
- Write the grain as the first comment: `-- grain: one row per account per calendar month`.
- Test it: `unique` on the grain columns (combination test).
- Joining two facts? Aggregate both to a common grain first. Joining fact-to-fact at different grains is the #1 source of inflated numbers.

## Slowly changing dimensions
| Type | Behaviour | Use |
|---|---|---|
| 0 | never changes | signup date, first touch |
| 1 | overwrite | typo fixes, attributes you only need "as is now" |
| 2 | new row per change with `valid_from`, `valid_to`, `is_current` | plan, segment, owner — anything you report "as it was then" |
For SCD2: non-overlapping validity ranges (test it), `valid_to` null or `9999-12-31` for current rows, join facts with `event_at >= valid_from and event_at < valid_to`.

## Date spines & periodic snapshots
For "per month" metrics (MRR, active users, inventory), generate a spine (entity × period) and left-join activity onto it. Without a spine, months with zero activity disappear and churn/retention math breaks.

## Metrics-ready marts
- One column per additive measure; derive ratios in the semantic layer, not in the table.
- Store amounts in a single currency (convert in staging/intermediate with the rate at the event date) and keep the original currency column.
- Include `is_test`/`is_internal` flags rather than silently filtering, so analysts can see what was excluded.

## Documentation minimum
Every mart: description (what, grain, owner), every column described, tests listed. Business definitions must match `context/metrics.md`.
