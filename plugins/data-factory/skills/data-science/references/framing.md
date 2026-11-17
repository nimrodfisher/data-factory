# Framing & Baselines

## Framing card (fill before any code)
| Question | Answer |
|---|---|
| Decision fed | e.g. which accounts CS calls this week |
| Unit of prediction | account × week |
| Target | churns within next 60 days (yes/no) |
| Prediction time / horizon | every Monday, 60-day horizon |
| Features allowed | only information available **at prediction time** |
| Cost of errors | FN = lost account (~$X), FP = wasted CSM call (~$Y) |
| Evaluation metric | matches the cost: precision@capacity, recall at fixed FP rate, MAE in $, etc. |
| Bar to ship | beats baseline by a margin that matters to the decision |

## Do you need ML at all?
| Situation | Use |
|---|---|
| Explaining the past | analysis, not ML |
| A rule a human can state captures most of the signal | the rule (as the baseline — maybe the product) |
| Need a number with uncertainty for planning | statistical forecast |
| Need a causal effect | experiment or causal design, not a predictive model |
| Many weak signals, repeated decision at scale | ML |

## Baselines
| Task | Baseline |
|---|---|
| Forecast | naive (last value), seasonal naive (same period last year/week), trailing mean |
| Classification | base rate / majority class; one-feature rule; logistic regression on 3–5 obvious features |
| Regression | mean/median; linear regression |
| Experiment | difference in means with a t-test / proportions z-test |
| Ranking | sort by the one most obvious signal (e.g. recent usage drop) |

## Choosing the metric
- Imbalanced classes → PR-AUC, precision/recall at an operating threshold; never accuracy.
- Capacity-limited action (CS can call 50 accounts) → precision@50 / lift in the top decile.
- Forecasts → MAE/MAPE (beware MAPE near zero), WAPE for aggregates, interval coverage for uncertainty.
- Probabilities used directly (expected value, pricing) → calibration (Brier score, reliability plot).
