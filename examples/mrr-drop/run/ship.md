# Ship Report — August MRR drop & the Starter price change

## The answer
**MRR fell $62.5k (−1.4%) in August because Starter customers cancelled after the Jul 15 price-increase e-mail** — churn more than doubled ($158k vs $67k average), and 97% of the excess came from SMB Starter on monthly billing.
**So far the price increase is net negative: +$129k/month from re-pricing vs −$140k/month lost to excess churn → −$10.6k/month**, and Starter churn is still ~2pp above normal.
**Recommendation: don't extend the increase to annual renewals yet.** Re-check in January; base forecast Dec MRR $4.74M (80%: $4.70–4.79M).

## Deliverables
| What | Path | Station |
|---|---|---|
| Clean MRR mart + tests | `models/`, `tests/` | data-engineer |
| Findings memo + queries | `analyses/findings.md`, `analyses/*.sql` | data-analyst |
| Causal estimate + forecast + model card | `notebooks/` | data-scientist |
| Dashboard | `dashboards/mrr_dashboard.html` | bi-engineer |

## How we know it is right
- Acceptance checks: **5/5** passed
- Sealed holdouts: **7/7** passed (loop 2)
- Headline MRR (Jul, Aug, Oct) re-derived independently from raw by the inspector: exact match
- Rework loops: **1** — what it caught:
  - **1,132 duplicated invoices** from a connector re-sync (would have overstated August revenue by 46%)
  - **3 internal QA accounts** in the MRR base — two "Enterprise churns" in August were QA clean-up, which would have made the drop look **76% bigger** (−$109.9k) and blamed the wrong segment

## Confidence & caveats
**High** on why MRR dropped. **Medium** on the net price effect: only 3 months after the change; 95% CI on excess churn is +2.2 to +11.1pp/month. Forecast is a short-horizon component model (beats naive clearly, drift marginally).

## Needs your decision
- [ ] Approve the definitions decision: test/internal accounts excluded from MRR (now in `context/metrics.md`)
- [ ] Merge `models/` + `tests/` (PR prepared, not merged)
- [ ] Share the dashboard with CEO/CFO
- [ ] Decide on annual-renewal price extension (recommend: hold until January re-check)

## Recommended next steps
- Re-run this spec in January (`/data-factory:run` on the same spec) — the effect estimate tightens with each month.
- Win-back test for the 421 Starter accounts that churned Aug–Oct.
- Separate question for a future run: did new-sign-up conversion fall at $35? (Aug new MRR was 18% below its 6-month average.)
