---
recipe: metric-alert-investigation
autonomy: gated
size: M
---
# Data Spec — Why did {{metric}} change?

## 1. Intent
{{who}} needs to know whether the {{metric}} change on {{date/period}} is real, what drove it, and whether to act.
> Real + actionable driver → owner acts. Data issue → fix the pipeline. Noise → no action.

## 2. Deliverables
- [ ] Findings memo (answer first, drivers sized, alternatives rejected) → `analyses/<slug>/findings.md` (data-analyst)
- [ ] If the data is broken: a fix on a branch + tests (data-engineer)

## 3. Definitions
{{metric}} per `context/metrics.md`. Comparison: {{prior period / same period last year}}.

## 5. Acceptance checks
- AC1 The memo states first whether the change is real (data checks + outside normal variation) before explaining it.
- AC2 Driver contributions sum to the total change (±1%).
- AC3 At least two hypotheses tested, with evidence for/against.
- AC4 Every number traceable to a saved query.

## 6. Out of scope
Forecasting, dashboards (unless the human asks after the memo).
