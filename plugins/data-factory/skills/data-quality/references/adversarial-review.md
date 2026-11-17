# Adversarial Review

For each deliverable, ask "how could this be wrong and still look right?" Run the checks; record each as R<n> in the inspection.

## Data engineer output (models, pipelines)
- [ ] Grain stated and unique-tested? Try the grain query yourself.
- [ ] Row counts per layer: source → staging (dedup explained) → mart. Any unexplained loss/gain?
- [ ] Joins: row count before/after each join; any fan-out?
- [ ] Dedup logic: keeps the right row (latest load / latest update)? Why were there duplicates?
- [ ] Time zone and period boundaries handled once, consistently?
- [ ] Test/internal/deleted records handled as the spec says?
- [ ] Incremental: idempotent on re-run? Lookback for late data?
- [ ] Nothing written outside dev?

## Analyst output (findings memo)
- [ ] Every number traceable to a saved query; re-run 2–3 of them.
- [ ] Driver contributions sum to the total change.
- [ ] Baseline appropriate (seasonality, trailing range)?
- [ ] Mix shift / Simpson's checked when segments disagree with totals?
- [ ] Alternative explanations considered and evidence stated?
- [ ] Causal language justified?
- [ ] Denominators and counts shown?
- [ ] Conclusion actually answers the question in the spec's Intent?

## Data scientist output (models, forecasts, tests)
- [ ] Baseline reported and beaten by a meaningful margin?
- [ ] Validation matches production (time split, grouped split)?
- [ ] Leakage: features available at prediction time? Suspiciously high scores?
- [ ] Intervals reported; coverage checked in backtest?
- [ ] For experiments: SRM checked, metric pre-declared, no peeking?
- [ ] Reproducible: seed fixed, script runs end-to-end?

## BI output (dashboards, semantic layer)
- [ ] Each KPI equals the direct mart query (re-query 2–3 yourself).
- [ ] Filters apply to every tile; default date range explicit.
- [ ] Metric definitions match `context/metrics.md`.
- [ ] Freshness shown; titles/units correct; no misleading axes.
- [ ] Not published to a production workspace.

## Independent re-derivation
For the 1–3 headline numbers, write your own query **from the raw or staging layer**, without reading the builder's SQL first. Agreement within tolerance → strong evidence. Disagreement → find out which is wrong before any verdict.
