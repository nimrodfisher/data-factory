# Lessons written by this run (appended to `.data-factory/lessons.md`)

- 2026-11-17 · billing connector re-sync on 2026-09-03 duplicated 1,132 August invoices; dedupe `invoice_id` keeping latest `_loaded_at` (caught by inspector, H2/H4)
- 2026-11-17 · 3 internal QA accounts (`is_test`) look like Enterprise customers; their Aug clean-up looked like $47k Enterprise churn — exclude in `int_` layer (caught by inspector, H5)
- 2026-11-17 · Sep 2026 expansion is a one-off re-price level shift; exclude from expansion-rate baselines
- 2026-11-17 · SMB Growth monthly is a good comparison group for SMB Starter (flat pre-trend gap)
