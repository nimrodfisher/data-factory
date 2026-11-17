# ML Modeling (classification / regression / scoring)

## Dataset construction
- Build a **snapshot table**: one row per entity per prediction date, features computed with data **up to** that date, label from the window **after** it.
- Multiple snapshots per entity are fine for training — then split by time and group by entity.
- Exclude entities that cannot have the outcome (already churned, not yet eligible).

## Leakage hunt (do this explicitly)
| Leak | Example | Test |
|---|---|---|
| Future information | "last login" computed at extraction time, not prediction time | recompute features as-of the snapshot date |
| Target proxies | `cancellation_reason`, `downgrade_requested` | features with suspiciously high importance; AUC > 0.95 is a red flag |
| Post-treatment variables | CS outreach that happened because the model would flag | drop or time-shift |
| Split leakage | same account in train and test | grouped split |
| Preprocessing leakage | scaling/encoding fit on the full dataset | fit transforms inside the CV pipeline |

## Validation
- Temporal: train on earlier snapshots, validate on later (out-of-time).
- Grouped k-fold when no temporal aspect but entities repeat.
- Report: baseline vs model on the chosen metric, with CI via bootstrap.
- Check stability: performance by segment and by time period.

## Model choice
1. Logistic/linear regression with sensible features — baseline and often good enough.
2. Gradient-boosted trees (LightGBM/XGBoost/sklearn HistGradientBoosting) — default for tabular data.
3. Anything heavier needs a reason.
Tune moderately (early stopping, a small search); most lift comes from features and labels, not hyperparameters.

## Interpretability & calibration
- Global: permutation importance or SHAP summary. Local: top reasons per prediction (CS teams need "why").
- Calibrate probabilities (isotonic/Platt) if they are used as probabilities.
- Choose the threshold from the cost of errors and team capacity, not 0.5.

## Model card (`model_card.md`)
```
Purpose & decision fed · Owner
Data: sources, window, snapshot logic, label definition, exclusions
Features: list, as-of logic
Performance: baseline vs model (metric, CI), by segment, out-of-time
Threshold & expected volume
Known failure modes & fairness considerations
Monitoring: drift checks, performance re-check cadence, retrain trigger
```
