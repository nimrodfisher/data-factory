-- grain: one row per account
-- raw.accounts is a full daily snapshot; keep the latest load per account.
select
    account_id,
    account_name,
    segment,
    region,
    signup_date::date as signup_date,
    is_test
from raw.accounts
qualify row_number() over (partition by account_id order by _loaded_at desc) = 1
