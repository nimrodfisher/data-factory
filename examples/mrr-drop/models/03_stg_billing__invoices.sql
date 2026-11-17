-- grain: one row per invoice
-- The billing connector re-synced on 2026-09-03 and re-delivered ~40% of August invoices
-- with the same invoice_id. Keep the latest load per invoice_id (see context/sources.md).
select
    invoice_id,
    account_id,
    subscription_id,
    invoice_date::date as invoice_date,
    amount_usd,
    status,
    _loaded_at
from raw.invoices
qualify row_number() over (partition by invoice_id order by _loaded_at desc) = 1
