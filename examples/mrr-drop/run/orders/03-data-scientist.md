# Work Order 03 — data-scientist

| Field | Value |
|---|---|
| Run | 2026-11-17-mrr-drop |
| Depends on | 01 |

## Objective
(a) Estimate the causal effect of the Starter price change on churn and its net recurring MRR effect. (b) Forecast MRR for Nov–Dec 2026 with scenarios.

## Inputs
- `fct_mrr_monthly`, `int_mrr__account_months` (dev) · handoff 01 · spec §3 treated/comparison groups

## Deliverables
- `notebooks/price_change_impact.py` (seeded, runnable)
- `notebooks/model_card.md`

## Definition of done
- AC4: effect with 95% interval + pre-trend check; forecast backtested against naive and drift baselines and beats naive.

## Constraints
- Do **not** read `../sealed/`.
