# Intake & Spec

A software factory is only as good as its specs. In data work, most failures are **definition failures**, not code failures: "revenue" meant bookings to sales and recognised revenue to finance; "active" had no window; the time zone was assumed.

## Classify the request
| Type | Signal | Typical stations |
|---|---|---|
| Question | "why", "how many", "which", "what happened" | (DE) → Analyst |
| Prediction / experiment | "forecast", "will", "A/B", "impact of", "likely to" | (DE) → DS |
| Data product | "table", "pipeline", "model", "ingest", "sync" | DE |
| Visibility | "dashboard", "report", "track", "KPI" | (DE) → BI |
| Mixed | "why … and track it", "forecast … dashboard" | several |

## Turn vague words into definitions
Every one of these words must be pinned down in the Definitions table:
- **Entity**: customer = account? workspace? paying org? Are trials/test/internal accounts included?
- **Metric**: formula, numerator and denominator, currency, gross vs net, refunds.
- **Time**: event time vs processing time, time zone, calendar vs fiscal, window ("last month" = calendar month? trailing 30 days?).
- **Grain**: one row per what?
- **Status**: "active", "churned", "engaged" — threshold and window.
Prefer definitions in `context/metrics.md`. If none exists, propose one and list it under assumptions.

## Writing acceptance checks
Acceptance checks are visible to builders. Each must be pass/fail and checkable by query or inspection.
- Good: "AC1 `fct_mrr_monthly` has exactly one row per account per month (unique test passes)."
- Good: "AC2 Sum of new + expansion − contraction − churn MRR equals the month-over-month change in total MRR for every month."
- Good: "AC3 The findings memo states the size of each driver in USD and they sum to the total change ±1%."
- Bad: "The analysis is accurate." "The dashboard looks good."
Aim for 3–8. Cover: grain/uniqueness, reconciliation of components to totals, coverage (date range, all segments), the deliverable's shape (memo answers the question first, dashboard shows freshness).

## When to ask the human (max 3 questions, one message)
Ask only when a wrong guess would change the answer or waste a full run:
1. The decision is unclear (two plausible decisions lead to different analyses).
2. A core definition has two common, materially different meanings and no context file settles it.
3. Access: where the data is / which environment is safe.
Everything else → make the assumption, write it down, let the spec gate catch it.

## Spec quality bar
- Intent names a decision and a decision-maker.
- Every deliverable has a path and a station.
- No undefined metric words remain.
- Out-of-scope is explicit (prevents gold-plating).
