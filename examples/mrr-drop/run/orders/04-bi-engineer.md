# Work Order 04 — bi-engineer

| Field | Value |
|---|---|
| Run | 2026-11-17-mrr-drop |
| Depends on | 02, 03 |

## Objective
A dashboard leadership can use monthly to track MRR, Starter churn and whether the price change is paying off.

## Inputs
- `fct_mrr_monthly`, analyses outputs, DS results · handoffs 02, 03

## Deliverables
- `dashboards/build_dashboard.py` → `dashboards/mrr_dashboard.html` (`bi: html` — self-contained, no CDN)

## Definition of done
- AC5: KPIs reconcile to direct mart queries (record both numbers); freshness visible.
- Brief: audience = CEO/CFO, monthly; questions = Where is MRR? Why did it move? Is the price change paying off? Where is it heading?

## Constraints
- Do **not** read `../sealed/`.
