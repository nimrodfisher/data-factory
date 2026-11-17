# Data Spec — August MRR drop & the Starter price change

| Field | Value |
|---|---|
| Run | 2026-11-17-mrr-drop |
| Requested by | Head of Data (one-person data team) |
| Size | **L** — 4 stations |
| Type | mixed: model + analysis + ml + dashboard |
| Status | approved (Gate 1, with one edit: "add the forecast to the dashboard") |

> **Request:** "MRR dropped in August. Why — and was the Starter price increase a mistake? Forecast to December and give me a dashboard to track it."

## 1. Intent
Leadership must decide whether to **extend the Starter price increase to annual renewals in 2027**, roll it back, or change it.
> If the increase is net positive and churn is normalising → extend it. If it is net negative or churn is still elevated → don't extend; consider a smaller increase or a retention offer.

## 2. Deliverables
- [ ] Clean MRR mart with movements (`fct_mrr_monthly`) → `models/` (data-engineer)
- [ ] Findings memo: why MRR fell in August, sized drivers → `analyses/findings.md` (data-analyst)
- [ ] Causal estimate of the price change's effect on churn and net MRR; forecast Nov–Dec 2026 with scenarios → `notebooks/` (data-scientist)
- [ ] Dashboard to track MRR, Starter churn and the price-change ledger → `dashboards/mrr_dashboard.html` (bi-engineer)

## 3. Definitions
| Term | Definition | Grain | Filters / exclusions | Source |
|---|---|---|---|---|
| MRR | per `context/metrics.md` — annual ÷ 12, active at month-end | account × month | excludes test & internal accounts | `raw.subscriptions` |
| MRR movements | new / expansion / contraction / churn, sum to ΔMRR | account × month | first month of history = opening | `fct_mrr_monthly` |
| Logo churn rate | per `context/metrics.md` | group × month | | `fct_mrr_monthly` |
| Treated group | SMB · Starter · monthly billing (re-priced Sep 1) | | | |
| Comparison group | SMB · Growth · monthly billing (not re-priced, similar customers) | | | |
| "Was it a mistake?" | net recurring MRR effect = re-pricing uplift − MRR lost to churn **in excess of** the comparison trend | MRR / month | | |

## 4. Sources & assumptions
- Sources: `raw.accounts`, `raw.subscriptions`, `raw.invoices` (DuckDB `saas.duckdb`).
- Window: Jan 2025 – Oct 2026, month-ends, UTC.
- A1 — Excess churn is measured against the comparison group (difference-in-differences), not against Starter's own history alone.
- A2 — Annual Starter contracts are out of the effect estimate (not re-priced yet).
- A3 — Forecast horizon Nov–Dec 2026 only; 22 months of history is too short to learn annual seasonality.

## 5. Acceptance checks (visible to builders)
- **AC1** `fct_mrr_monthly` has exactly one row per account per month.
- **AC2** new + expansion − contraction − churn equals the month-over-month change in total MRR for every month (±$0.01).
- **AC3** The memo states the August change in USD and %, and sizes each driver so the drivers sum to the total.
- **AC4** The DS estimate reports an effect with a 95% interval and a pre-trend check; the forecast beats a naive baseline in backtest.
- **AC5** Every dashboard KPI equals the same number queried directly from the mart; freshness is shown.

## 6. Out of scope
Changing prices, contacting churned customers, scheduling a refresh job.

## 7. Risks & open questions
- New-sign-up conversion may also have reacted to the new price (Aug new MRR looked soft) — flag, don't analyse in this run.
