# Semantic Layer & Governance

## Why
Without a semantic layer, every dashboard re-implements "revenue" slightly differently and numbers drift. Define measures and dimensions once, close to the marts; BI tools and AI agents query them.

## Options
| Option | Where metrics live |
|---|---|
| dbt Semantic Layer (MetricFlow) | `semantic_models` + `metrics` YAML in the dbt project |
| LookML | `measure:` / `dimension:` in view files, `explore:` for joins |
| Cube | `cubes` with `measures` / `dimensions` (YAML/JS) |
| Power BI | DAX measures in the semantic model (dataset) |
| Tableau | published data sources with calculated fields |
| Lightdash | `meta.metrics` in dbt YAML |
| Metabase / Superset | Metabase *Metrics* & *Models* / Superset datasets with metrics |
| None | a `metrics.yml` in the repo + SQL views — the factory keeps it in sync with `context/metrics.md` |

## Measure definition checklist
- Aggregation type (sum, count_distinct, average) and the column.
- Filters baked in (exclude test accounts) — visible in the description.
- Ratio metrics defined as ratio of two measures (`sum(a)/sum(b)`), never as a stored average.
- Time dimension and grain(s) supported.
- Description, owner, and "certified" flag/tag.

## Governance
- **Certified** vs **exploratory** content: certified dashboards only use certified metrics and are owned.
- Naming conventions for folders/spaces: `01 Company KPIs`, `02 Finance`, `99 Sandbox`.
- Deprecate rather than delete: mark, redirect, then remove after a window.
- Usage review quarterly: archive dashboards with no views in 90 days.

## Performance
- Dashboards query marts or aggregate tables, never raw events.
- Use the tool's caching/extracts/aggregate awareness (Looker aggregate tables, Power BI aggregations / import mode, Tableau extracts).
- Limit default date range; push filters down to the warehouse; avoid high-cardinality dimensions on default views.
