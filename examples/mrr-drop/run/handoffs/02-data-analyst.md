# Handoff 02 — data-analyst (after rework loop 1)

**Status:** done

## Built
| Path | What |
|---|---|
| `analyses/01_mrr_bridge.sql` | monthly MRR bridge |
| `analyses/02_churn_drivers.sql` | Aug churn vs trailing-6-month baseline by segment × plan × billing |
| `analyses/03_logo_churn_rates.sql` | logo churn rate by group, monthly |
| `analyses/04_segment_summary.sql` | MRR by segment & plan |
| `analyses/findings.md` | memo |

## How I verified
| Check | Result |
|---|---|
| AC3 drivers sum to total | new +$84.3k, expansion +$14.7k, contraction −$3.1k, churn −$158.4k = **−$62.5k** ✅ |
| Hypotheses tested | price-change churn (supported) · Enterprise churn (rejected after rework — internal accounts) · seasonal dip (rejected: Aug 2025 +$41.7k) · weak new sales (partial: −$18k vs avg) |

## Numbers that matter
- Aug ΔMRR −$62,468 (−1.37%); churn $158.4k vs $67.5k Feb–Jul average.
- 235 of 262 churned accounts in Aug were SMB Starter monthly; their excess churned MRR $88.5k ≈ 97% of all excess churn.

## Changed in rework
Draft 1 attributed $47.4k of the drop to "two Enterprise churns". The inspector flagged that both were internal QA accounts; the conclusion now rests on the clean mart.
