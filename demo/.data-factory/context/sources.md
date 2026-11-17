# Source systems & known quirks

| Source | Tables | Loaded by | Freshness | Known quirks |
|---|---|---|---|---|
| Billing system | `raw.accounts`, `raw.subscriptions`, `raw.invoices` | managed connector, daily | ~1 day | A plan, seat or price change closes the subscription row and opens a new one. Invoice history starts 2025-01-01. |
