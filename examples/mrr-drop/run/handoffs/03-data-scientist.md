# Handoff 03 — data-scientist

**Status:** done

## Built
| Path | What |
|---|---|
| `notebooks/price_change_impact.py` | DiD estimate, net impact ledger, component forecast + backtest (seeded) |
| `notebooks/model_card.md` | model card |
| `outputs/ds_results.json` | all numbers below |

## How I verified
| Check | Result |
|---|---|
| Pre-trend (treated − comparison gap, Feb 2025–Jul 2026) | slope +0.04pp/month ≈ flat ✅ |
| Effect interval | block bootstrap, 5,000 draws |
| Forecast backtest (11 origins, h = 1–2, pre-change only) | MAE naive $83.8k · drift $30.3k · **component $28.6k** ✅ beats naive |

## Numbers that matter
- Excess Starter-monthly churn: **+5.8pp/month** on average Aug–Oct (95% CI +2.2 to +11.1pp); by month +11.1 / +4.0 / +2.2pp.
- Re-pricing uplift **+$129.3k MRR/month** (1,304 accounts) vs MRR lost to excess churn **−$139.9k/month** → **net −$10.6k/month** at Oct run-rate.
- Forecast Dec 2026 MRR: base **$4.74M** (80% interval $4.70–4.79M); downside $4.72M; upside $4.76M.

## Assumptions
- Comparison group (SMB Growth monthly) would have followed the same trend as Starter absent the change (parallel trends — supported by the pre-period).
- The uplift is measured on accounts still active in Oct; it does not include future price-driven churn.

## Open issues
- Oct excess churn (+2.2pp) is still above zero; each further month at that rate costs ≈ $19k MRR. The verdict can flip to positive only if excess churn reaches ~0 soon.
- Effect interval is wide (3 post months). Re-estimate after December.
