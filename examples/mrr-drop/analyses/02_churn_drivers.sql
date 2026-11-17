-- Supports: "excess churn is concentrated in SMB Starter monthly" (findings §2)
-- Churned MRR by segment x plan x billing: August 2026 vs the trailing 6-month average (Feb-Jul 2026).
with churn as (
    select
        month_end,
        segment,
        prev_plan as plan,
        billing_period,
        -sum(mrr_change) as churned_mrr,
        count(*)         as churned_accounts
    from fct_mrr_monthly
    where movement = 'churn'
    group by all
)
select
    segment,
    plan,
    billing_period,
    sum(churned_mrr)      filter (where month_end = date '2026-08-31')                       as aug_churned_mrr,
    sum(churned_accounts) filter (where month_end = date '2026-08-31')                       as aug_churned_accounts,
    sum(churned_mrr)      filter (where month_end between date '2026-02-28' and date '2026-07-31') / 6 as baseline_churned_mrr,
    aug_churned_mrr - baseline_churned_mrr                                                   as excess_churned_mrr
from churn
group by all
order by excess_churned_mrr desc
