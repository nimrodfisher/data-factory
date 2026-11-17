# Source systems & known quirks

| Source | Tables | Loaded by | Freshness | Known quirks |
|---|---|---|---|---|
| TODO e.g. Billing (Stripe) | raw.invoices | Fivetran, hourly | ~1h | re-syncs can duplicate invoice rows — dedupe on invoice_id, latest _loaded_at |
