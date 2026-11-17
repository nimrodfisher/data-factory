# Metrics

## A complete metric definition
| Part | Example (MRR) |
|---|---|
| Name & owner | MRR — Finance |
| Formula | Σ monthly-normalised recurring amount of active subscriptions (annual ÷ 12) |
| Grain & time | month-end snapshot, UTC |
| Inclusions / exclusions | excludes one-off fees, taxes, test/internal accounts; includes discounts |
| Currency | USD at month-end rate |
| Source | `fct_mrr_monthly` |
| Known caveats | backdated plan changes restate prior months |

## Metric trees
Decompose an outcome into multiplicative/additive drivers so any change can be attributed:
```
Revenue = Customers × ARPA
Customers(t) = Customers(t-1) + New − Churned
MRR Δ = New MRR + Expansion − Contraction − Churned MRR (+ Reactivation)
Conversion = Visitors × Signup rate × Activation rate × Paid conversion
Gross margin = Revenue − COGS
```
Rules: components must reconcile exactly to the parent; each leaf has an owner who can act on it.

## Choosing metrics
- **North star**: captures delivered customer value and predicts revenue (e.g. weekly active teams, not page views).
- **Input metrics**: levers teams control that move the north star.
- **Guardrails**: things that must not get worse while optimising (refund rate, latency, support tickets per account).
- **Counter-metric** for every target metric to prevent gaming.

## Rates and ratios
- Always state numerator **and** denominator, and show both counts.
- Ratios of sums, not averages of ratios (unless the unit-level average is what you mean).
- Pick the denominator that matches the decision: churn rate on start-of-period customers, not average customers, unless defined otherwise in `context/metrics.md`.
- Revenue churn ≠ logo churn. Report both when they diverge.

## SaaS reference definitions (use unless context overrides)
| Metric | Definition |
|---|---|
| Logo churn rate | customers lost in period ÷ customers at start of period |
| Gross revenue retention (GRR) | (start MRR − contraction − churn) ÷ start MRR, cohort of start-of-period customers |
| Net revenue retention (NRR) | (start MRR + expansion − contraction − churn) ÷ start MRR, same cohort |
| ARPA | MRR ÷ paying accounts |
| CAC payback (months) | CAC ÷ (ARPA × gross margin %) |
| LTV (simple) | ARPA × gross margin % ÷ monthly revenue churn rate — directional only |
