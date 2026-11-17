# Forecasting

## Process
1. **Plot it.** Trend, seasonality (weekly/annual), level shifts, outliers, structural breaks (pricing change, COVID-style shocks).
2. **Decide the level**: forecast the total, or components (new, expansion, churn) and sum? Component forecasts are more explainable and let you run scenarios ("what if churn returns to baseline?").
3. **Baselines**: naive, seasonal naive, drift. Record their backtest error.
4. **Candidate models** (in order of preference):
   - Exponential smoothing (ETS / Holt-Winters) — strong default for business series.
   - ARIMA/SARIMA — when autocorrelation structure matters.
   - Regression with drivers (pipeline, price, marketing spend) — when you have leading indicators and need scenarios.
   - Prophet-style decomposition — many seasonalities/holidays; check it actually beats ETS.
   - Gradient boosting on lag features — many related series (per SKU/region), enough history.
5. **Backtest** with rolling origin (expanding window): forecast h steps from several historical cut-offs; compare MAE/WAPE vs baselines.
6. **Intervals**: report 80% and 95% prediction intervals; check empirical coverage in the backtest.
7. **Scenarios** for decisions: base / downside / upside with explicit assumptions.

## Short series (≤ 24 monthly points — common in SaaS)
- Keep models simple: drift, damped trend ETS, or component-based arithmetic (e.g. MRR_t+1 = MRR_t × (1 + new rate + expansion rate − churn rate − contraction rate), rates from trailing averages).
- Annual seasonality cannot be learned from < 2 years — don't pretend.
- Widen intervals; say so.

## Structural breaks
After a known event (price change), either model pre/post separately, add a level-shift regressor, or fit only on post-event data and state the shorter history. Never let a one-off spike drive the trend.

## Report
| Horizon | Base | 80% interval | Downside | Upside |
|---|---|---|---|---|
Plus: model chosen and why, backtest error vs baseline, key assumptions, when to re-forecast.
