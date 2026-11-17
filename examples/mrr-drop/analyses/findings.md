# Why did MRR fall in August 2026 — and was the Starter price increase a mistake?

**Decision:** extend the Starter price increase to annual renewals in 2027, roll it back, or change it.

## Answer
MRR fell **$62.5k (−1.4%)**, from $4.55M to $4.49M, because **SMB Starter customers on monthly billing cancelled after the Jul 15 price-increase e-mail**. Churn hit $158.4k, 2.3× the Feb–Jul average, and Starter monthly accounts drove 97% of the excess. **Confidence: High.**
September's rebound (+$136k) is the price increase itself landing on the customers who stayed — not a recovery in retention.

## Why we believe it
1. **Churn is the only component that moved.** Aug bridge: new +$84.3k, expansion +$14.7k, contraction −$3.1k, churn **−$158.4k** (avg −$67.5k). (`01_mrr_bridge.sql`)
2. **It is concentrated in the re-priced group.** SMB Starter monthly churned $109.0k vs a $20.5k baseline (+$88.5k); every other group moved by less than $10k. 235 of 262 churned accounts were Starter monthly. (`02_churn_drivers.sql`)
3. **Timing matches the announcement, and a comparable group didn't move.** Starter monthly logo churn: 2.5% baseline → **13.6%** Aug → 7.3% Sep → 4.9% Oct. SMB Growth monthly (similar customers, no price change): 2.1% → 2.1% / 2.9% / 2.3%. (`03_logo_churn_rates.sql`)

## What it is not
| Hypothesis | Verdict | Evidence |
|---|---|---|
| Enterprise churn | ❌ rejected | the two "Enterprise churns" in Aug are internal QA accounts (caught by the inspector); clean Enterprise churn in Aug = $0 |
| Seasonal August dip | ❌ rejected | Aug 2025 MRR grew +$41.7k |
| Weak new sales | partial | new MRR $84.3k vs $102.3k average (−$18k) — explains ~16% of the gap to a normal month (avg net +$48k); flagged as a separate question |
| Data artefact | ❌ rejected | MRR reconciles to the July board figure; invoice duplicates removed and reconciled to finance close |

## So — was the price increase a mistake?
Not decided by this memo alone (see the data-scientist's estimate), but the descriptive picture is: the uplift is real and recurring (+$129k/month), and so is the lost MRR from customers who left. The DS difference-in-differences estimate puts the net at **−$10.6k/month at the October run-rate**, with Starter churn still above normal.

## Recommendation
Hold the annual-renewal extension. Re-check in January. Test a win-back offer on the 421 Starter accounts that churned Aug–Oct.

## What would change my mind
- Starter monthly churn back at ≤ 2.5% in Nov–Dec → the increase turns net positive within months.
- Evidence that churned Starter accounts were low-usage accounts likely to churn soon anyway (would lower the true cost).

## Method & caveats
MRR per `context/metrics.md` (annual ÷ 12, active at month-end, test accounts excluded). Baseline = Feb–Jul 2026 monthly average. Logo churn rate = churned ÷ active at prior month-end. Data: Jan 2025 – Oct 2026.
