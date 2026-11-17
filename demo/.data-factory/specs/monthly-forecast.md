---
recipe: monthly-forecast
autonomy: gated
size: M
schedule: 2nd business day of each month
---
# Data Spec — Monthly {{metric}} forecast

## 1. Intent
Board / finance planning: where will {{metric}} land in the next {{n}} months, and what are the risks?

## 2. Deliverables
- [ ] Forecast with base / downside / upside scenarios and 80% intervals → `notebooks/forecast_<month>.py` + `model_card.md` (data-scientist)
- [ ] Forecast-vs-actual for last month's forecast (data-scientist)
- [ ] Forecast panel on the KPI dashboard (bi-engineer)

## 5. Acceptance checks
- AC1 Backtest vs naive and seasonal-naive baselines reported; model beats naive.
- AC2 Last month's forecast error reported honestly.
- AC3 Scenario assumptions listed explicitly.
