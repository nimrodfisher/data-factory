---
recipe: weekly-kpi-review
autonomy: lights-out          # recurring + reconciled to truths → safe to run unattended
size: M
schedule: every Monday 06:00 UTC
---
# Data Spec — Weekly KPI review

## 1. Intent
Leadership's Monday check: are we on track, and what needs attention this week?
> If a KPI moved outside its normal range we investigate it this week; if not, no action.

## 2. Deliverables
- [ ] KPI table for the last complete week vs prior week and 4-week average → `analyses/weekly/<date>.md` (data-analyst)
- [ ] For any KPI outside its normal range (beyond the last 8 weeks' min–max): a 5-line "why" note using the investigation playbook (data-analyst)
- [ ] Refreshed KPI dashboard → `dashboards/weekly_kpis.html` (bi-engineer)

## 3. Definitions
KPIs: MRR, new MRR, churned MRR, logo churn rate, paying accounts (all per `context/metrics.md`).
Week = Monday–Sunday, UTC. "Normal range" = min–max of the previous 8 weeks.

## 4. Sources & assumptions
Marts already exist and are tested; no new models in this recipe.

## 5. Acceptance checks
- AC1 Every KPI shows value, Δ vs prior week, Δ vs 4-week average, with counts behind rates.
- AC2 Each out-of-range KPI has a driver note; in-range KPIs have none.
- AC3 Dashboard KPIs equal the memo's numbers.

## 6. Out of scope
New metrics, new models, forecasts.
