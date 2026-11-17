# Handoff 01 — data-engineer (after rework loop 1)

**Status:** done

## Built
| Path | What | Grain |
|---|---|---|
| `models/01_stg_billing__accounts.sql` | latest load per account | account |
| `models/02_stg_billing__subscriptions.sql` | `mrr` = annual ÷ 12 | subscription |
| `models/03_stg_billing__invoices.sql` | **dedup on `invoice_id`, latest `_loaded_at`** (added in rework) | invoice |
| `models/04_int_mrr__account_months.sql` | active subscription at each month-end, **test accounts excluded** (added in rework) | account × month |
| `models/05_fct_mrr_monthly.sql` | MRR + prior MRR + movement | account × month |

## How I verified
| Check | Method | Result |
|---|---|---|
| AC1 grain | `tests/assert_fct_mrr_grain.sql` | PASS |
| AC2 bridge | `tests/assert_bridge_reconciles.sql` | PASS (all 21 months, ±$0.01) |
| one active sub per account-month | `tests/assert_one_active_sub.sql` | PASS |
| invoice uniqueness | `tests/assert_invoice_unique.sql` | PASS — 1,132 duplicate rows removed |
| no test accounts | `tests/assert_no_test_accounts.sql` | PASS — 3 accounts excluded |

Row counts: stg accounts 5,385 · stg subscriptions 8,602 · stg invoices 57,667 (raw 58,799) · int 75,103 · fct 76,732.

## Numbers that matter
- MRR Jul 2026 **$4,551,409** · Aug **$4,488,941** · Oct **$4,671,314** (`select month_end, sum(mrr) from fct_mrr_monthly group by 1`)

## Source quirks found (written to `context/sources.md`)
- 2026-09-03 connector re-sync re-delivered 1,132 August invoices with the same `invoice_id`.
- 3 internal accounts (`is_test = true`) created 2026-05-04 at $23.7k MRR each; 2 cancelled 2026-08-12 — they look like Enterprise churn.

## For the next stations
- Use `fct_mrr_monthly.prev_plan` to attribute churn to the plan an account churned **from**.
- Sep 2026 expansion is mostly the Starter re-price (one-off level shift), not organic expansion.
