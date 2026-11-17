# BI tools

| Tool | Where the factory writes | Metric definition | Ship as |
|---|---|---|---|
| **Looker** | LookML: `views/*.view.lkml`, `models/*.model.lkml`, `dashboards/*.dashboard.lookml` | `measure:` in views; `explore:` joins with explicit `relationship:` | branch in the LookML repo (dev mode); validate with LookML validator / Spectacles |
| **Power BI** | PBIP project (`*.SemanticModel/`, `*.Report/`, TMDL files) | DAX measures in the semantic model — `CALCULATE`, `DIVIDE` (never `/`), time intelligence needs a marked date table | branch with the PBIP; publish to a dev workspace via deployment pipelines |
| **Tableau** | published data source + workbook (`.twb` XML is diffable) | calculated fields in the published data source; LOD expressions for fixed-grain metrics | dev project on the server; Tableau Server/Cloud REST API |
| **Metabase** | Models (curated SQL), Metrics, dashboards via API or serialization export | Metabase Metrics on Models | a "Data Factory – review" collection; serialization YAML in git (paid) or API script |
| **Superset** | datasets (virtual SQL), charts, dashboards; YAML export/import | metrics on datasets | dev workspace; `superset import-dashboards` |
| **Lightdash** | dbt YAML `meta:` (dimensions, metrics), charts as code | `meta.metrics` on dbt models | preview environment via `lightdash preview`; `lightdash deploy` is the human's step |
| **Hex** | project with SQL + Python cells | in the dbt semantic layer or the project's SQL | draft project; app published by a human |
| **Streamlit** | `app.py` reading marts | in a `metrics.py` module or SQL views | branch; deploy by human |
| **html** | self-contained file in `paths.dashboards` | `metrics.yml` + the build script | file in the repo / PR |

## Rules for every tool
- Point dashboards at marts or aggregates, not raw tables.
- Never re-implement a metric inside a chart; reference the defined measure.
- Ratio measures: `sum(num) / nullif(sum(den), 0)` (DAX: `DIVIDE(SUM(num), SUM(den))`).
- Set owner + description; put the freshness timestamp on the dashboard.
- Reconcile 2–3 KPIs against direct mart queries and record both numbers in the handoff.
- If the tool's API/CLI is not reachable from this environment, produce the code/config files plus an HTML preview, and list the manual publish steps.
