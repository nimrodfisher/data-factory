# Work Order 01 — data-engineer

| Field | Value |
|---|---|
| Run | 2026-11-17-mrr-drop |
| Depends on | none |
| Spec | `../spec.md` |

## Objective
A trustworthy monthly MRR mart with movement classification that every downstream station can build on.

## Inputs
- `raw.accounts`, `raw.subscriptions`, `raw.invoices`
- `.data-factory/context/metrics.md`, `sources.md`

## Deliverables
- `models/01_stg_billing__accounts.sql`, `02_stg_billing__subscriptions.sql`, `03_stg_billing__invoices.sql`
- `models/04_int_mrr__account_months.sql`, `05_fct_mrr_monthly.sql`
- `tests/*.sql` (assertion queries — return rows only on failure)

## Definition of done
- AC1 (grain) and AC2 (bridge reconciles) pass.
- Every model states its grain; row counts reported per model.

## Constraints
- Build in schema `dev` only. Do **not** read `../sealed/`.
