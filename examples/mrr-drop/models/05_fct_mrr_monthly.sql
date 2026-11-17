-- grain: one row per account per month-end, for every month the account had MRR now or in the prior month
-- movement: opening (first month of history) | new | expansion | contraction | churn | flat
-- Plan/billing for churn rows = the plan the account churned from (prior month).
with cur as (
    select * from int_mrr__account_months
),

prev as (
    select
        last_day(month_end + interval 1 day)::date as month_end,
        account_id,
        plan           as prev_plan,
        billing_period as prev_billing_period,
        mrr            as prev_mrr
    from cur
    where month_end < (select max(month_end) from cur)
),

joined as (
    select
        coalesce(c.month_end, p.month_end)           as month_end,
        coalesce(c.account_id, p.account_id)         as account_id,
        coalesce(c.plan, p.prev_plan)                as plan,
        coalesce(c.billing_period, p.prev_billing_period) as billing_period,
        p.prev_plan,
        coalesce(c.mrr, 0)                           as mrr,
        coalesce(p.prev_mrr, 0)                      as prev_mrr
    from cur as c
    full outer join prev as p
        on c.month_end = p.month_end
       and c.account_id = p.account_id
),

first_month as (
    select min(month_end) as month_end from cur
)

select
    j.month_end,
    j.account_id,
    a.segment,
    a.region,
    j.plan,
    j.prev_plan,
    j.billing_period,
    j.mrr,
    j.prev_mrr,
    j.mrr - j.prev_mrr as mrr_change,
    case
        when j.month_end = f.month_end            then 'opening'
        when j.prev_mrr = 0 and j.mrr > 0         then 'new'
        when j.prev_mrr > 0 and j.mrr = 0         then 'churn'
        when j.mrr > j.prev_mrr                   then 'expansion'
        when j.mrr < j.prev_mrr                   then 'contraction'
        else 'flat'
    end as movement
from joined as j
cross join first_month as f
join stg_billing__accounts as a using (account_id)
