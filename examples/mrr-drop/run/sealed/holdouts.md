# Sealed holdouts — 2026-11-17-mrr-drop

> Written by the quality-inspector in SEAL mode before any build. Builders never read this file.
> (Published here, after the run, so you can see how the inspector works.)

**H1 · July MRR reconciles to the July board deck** — $4,551,409 ±0.5%.
How to check: `sum(mrr)` in `fct_mrr_monthly` at 2026-07-31. · Severity: **blocker** · Why: catches population and normalisation errors (test accounts, annual ÷ 12).

**H2 · August invoiced revenue reconciles to finance close** — $4,958,131 ±0.5%, paid invoices, excluding test accounts.
How to check: sum of paid invoices dated Aug 2026 from the staging invoice model. · Severity: **blocker** · Why: protects against connector duplicates; billing connectors are known to re-sync.

**H3 · Invariant: MRR bridge reconciles exactly** — new + expansion − contraction − churn = ΔMRR, every month, ±$0.01. · Severity: blocker · Why: any fan-out or misclassification breaks it.

**H4 · No duplicate business keys in staging** — `invoice_id`, `subscription_id`, `account_id` unique after staging. · Severity: major.

**H5 · Population: no test/internal accounts in any mart or analysis** — names containing "Test", "QA", "Internal", or `is_test = true`. · Severity: **blocker** · Why: internal accounts created in May 2026 per `business.md`.

**H6 · Independent re-derivation** — Jul, Aug and Oct MRR recomputed by the inspector straight from `raw.subscriptions` match the mart exactly. · Severity: blocker.

**H7 · Directional sanity** — August churned MRR in SMB Starter monthly exceeds its own trailing-6-month mean (the price change was announced Jul 15). If not, the "price change" story needs extra scrutiny. · Severity: minor.
