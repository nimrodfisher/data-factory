-- grain: one row per account per month-end where the account has an active subscription
-- active at month-end = started_at <= month_end and (ended_at is null or ended_at > month_end)
-- Test / internal accounts are excluded here, once, for everything downstream.
with months as (
    select last_day(unnest(generate_series(date '2025-01-01', date '2026-10-01', interval 1 month)))::date as month_end
),

subs as (
    select s.*
    from stg_billing__subscriptions as s
    join stg_billing__accounts as a using (account_id)
    where not a.is_test
)

select
    m.month_end,
    s.account_id,
    s.plan,
    s.billing_period,
    s.seats,
    s.mrr
from months as m
join subs as s
    on s.started_at <= m.month_end
   and (s.ended_at is null or s.ended_at > m.month_end)
