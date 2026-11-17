-- Supports: churn-rate trend for treated vs comparison groups (findings §2, DS work order)
-- Logo churn rate = accounts churned in month / accounts active at the prior month-end, by group.
with base as (
    select
        month_end,
        case
            when segment = 'SMB' and coalesce(prev_plan, plan) = 'Starter' and billing_period = 'month' then 'SMB Starter · monthly'
            when segment = 'SMB' and coalesce(prev_plan, plan) = 'Starter'                              then 'SMB Starter · annual'
            when segment = 'SMB' and billing_period = 'month'                                           then 'SMB Growth · monthly'
            when segment = 'SMB'                                                                        then 'SMB Growth · annual'
            else segment
        end as grp,
        prev_mrr > 0           as was_active,
        movement = 'churn'     as churned
    from fct_mrr_monthly
    where movement <> 'opening'
)
select
    month_end,
    grp,
    count(*) filter (where was_active)                    as accounts_at_start,
    count(*) filter (where churned)                       as churned_accounts,
    churned_accounts / accounts_at_start                  as logo_churn_rate
from base
group by all
order by grp, month_end
