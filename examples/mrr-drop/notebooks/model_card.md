# Model card — Starter price-change impact & MRR forecast

**Purpose:** inform the decision on extending the Starter price increase; give the board a Nov–Dec MRR outlook. **Owner:** data team. **Code:** `price_change_impact.py` (seeded; `python build.py` reproduces everything).

## 1. Causal estimate (difference-in-differences)
| Item | Value |
|---|---|
| Treated | SMB · Starter · monthly billing (re-priced $29 → $35 per seat on Sep 1; announced Jul 15) |
| Comparison | SMB · Growth · monthly billing (not re-priced) |
| Outcome | monthly logo churn rate |
| Pre / post | Feb 2025–Jul 2026 / Aug–Oct 2026 |
| Pre-trend | gap slope +0.04pp/month (flat) |
| Effect | **+5.8pp/month** average (95% CI +2.2 to +11.1pp, block bootstrap); Aug +11.1, Sep +4.0, Oct +2.2pp |
| Net MRR ledger | re-pricing uplift +$129.3k/mo (1,304 accounts) − excess churned MRR $139.9k/mo = **−$10.6k/mo** |

Assumptions: parallel trends (supported pre-period); no spill-over to the comparison group; uplift measured only on accounts active in Oct.
Failure modes: only 3 post months → wide interval; if churned accounts were going to churn soon anyway, the cost is overstated.

## 2. Forecast
| Item | Value |
|---|---|
| Method | component model: MRR(t+1) = MRR(t) + new + MRR × (expansion − contraction − churn); rates from trailing 6 pre-change months, Sep re-price excluded |
| Baselines | naive (last value), drift (trailing average change) |
| Backtest | 11 rolling origins, h = 1–2 months, pre-change only · MAE naive $83.8k · drift $30.3k · **component $28.6k** |
| Scenarios (Starter monthly churn, Nov/Dec) | upside 2.6/2.6% · base 4.0/3.3% · downside 4.9/4.9% |
| Dec 2026 MRR | base **$4.74M** (80% interval $4.70–4.79M) · downside $4.72M · upside $4.76M |

Not modelled: annual seasonality (history < 2 years), new-sign-up price sensitivity.
**Re-run:** monthly; re-estimate the DiD when Nov and Dec close.
