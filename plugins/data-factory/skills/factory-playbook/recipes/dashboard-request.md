---
recipe: dashboard-request
autonomy: gated
size: M
---
# Data Spec — Dashboard for {{audience}}

## 1. Intent
{{audience}} uses it {{how often}} to decide {{decision}}.

## 2. Deliverables
- [ ] Dashboard brief (audience, decision, 3–5 questions, filters, refresh) (bi-engineer)
- [ ] Metrics defined once in the semantic layer / `metrics.yml` (bi-engineer)
- [ ] Dashboard in {{BI tool}} dev folder or `dashboards/` (bi-engineer)
- [ ] Any missing mart (data-engineer)

## 5. Acceptance checks
- AC1 Every question in the brief maps to one visual.
- AC2 Every KPI reconciles to a direct mart query (both numbers in the handoff).
- AC3 Freshness and date range visible; titles state the takeaway.
- AC4 Not published to a production workspace.
