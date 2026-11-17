# Metric definitions

| Metric | Formula | Grain | Filters / exclusions | Owner | Source |
|---|---|---|---|---|---|
| MRR | Σ monthly-normalised recurring amount of subscriptions active at month-end (annual amount ÷ 12) | month-end | excludes test & internal accounts; USD | Finance | `raw.subscriptions` |
| Active at month-end | `started_at <= month_end and (ended_at is null or ended_at > month_end)` | subscription | | Finance | |
| MRR movements | new, expansion, contraction, churn — sum to the MoM change in MRR | account × month | | Finance | |
| Logo churn rate | accounts that go from MRR > 0 to 0 in the month ÷ accounts with MRR > 0 at prior month-end | month | | CS | |
| Invoiced revenue | Σ amount of `paid` invoices dated in the month | month | excludes `void`; excludes test accounts | Finance | `raw.invoices` |
