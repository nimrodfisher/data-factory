# Planning & Dispatch

## Size the job
| Size | Shape | Gates | Example |
|---|---|---|---|
| **S** — express lane | one station, one deliverable, no new production models | skip Gate 1, still inspect | "how many accounts churned last month?" |
| **M** | 2–3 stations, linear dependencies | Gate 1 + Gate 2 | "why did MRR drop?" with a new mart + memo |
| **L** | 4+ stations, or new pipelines, or anything scheduled | Gate 1 + Gate 2, consider `supervised` | "build churn model + CS dashboard + weekly refresh" |

## Station routing rules
- Need a table that does not exist or is not trustworthy → **data-engineer** first. Analysts never build production models inside an analysis.
- Need an explanation of the past → **data-analyst**.
- Need a prediction, uncertainty, or causal effect → **data-scientist**.
- Need ongoing visibility → **bi-engineer**, *after* metrics are defined and marts exist.
- Every run ends with **quality-inspector**. It also starts every M/L run (SEAL).

## Typical graphs
```
Question:      DE(mart) ─► Analyst
Forecast:      DE(mart) ─► DS
Investigation + tracking:  DE ─► Analyst ─┐
                                 DE ─► DS ─┼─► BI
Pure dashboard: DE(mart, metrics) ─► BI
```
Analyst and DS can run **in parallel** once the mart exists. BI waits for the metric definitions the analysis confirms.

## Writing a good work order
- **Objective** in one or two sentences, outcome-shaped.
- **Inputs** are concrete: table names, upstream handoff paths.
- **Deliverables** are file paths in the user's repo (from `factory.yaml → paths`), plus the handoff path.
- **Definition of done** lists the acceptance checks this order owns. Each AC is owned by exactly one order.
- Keep orders small enough that one agent finishes in one pass. Split by grain or by deliverable, not by step.

## Dispatch prompt (use this shape)
```
You are working on Data Factory run <run_path>.
Your work order: <run_path>/orders/<NN>-<station>.md
Upstream handoffs: <paths or "none">
Config: .data-factory/factory.yaml · Context: .data-factory/context/
Write your handoff to <run_path>/handoffs/<NN>-<station>.md.
Do not read <run_path>/sealed/.
```
Dispatch independent orders in the same message so they run in parallel.

## When a station returns `blocked`
1. Read the reason. If it is missing access or a business definition → ask the human.
2. If it is a planning gap (missing upstream table) → add a work order, re-dispatch.
3. Never let a downstream station work around an upstream block silently.
