-- grain: one row per subscription (a price/seat change closes one subscription and opens another)
-- mrr: monthly-normalised recurring amount. Annual contracts store the yearly amount -> divide by 12.
select
    subscription_id,
    account_id,
    plan,
    seats,
    billing_period,
    amount,
    case when billing_period = 'year' then amount / 12 else amount end as mrr,
    started_at::date as started_at,
    ended_at::date   as ended_at
from raw.subscriptions
qualify row_number() over (partition by subscription_id order by _loaded_at desc) = 1
