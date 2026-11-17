# Work Order 02 — data-analyst

| Field | Value |
|---|---|
| Run | 2026-11-17-mrr-drop |
| Depends on | 01 |

## Objective
Explain why MRR fell in August 2026, with each driver sized in USD, and say what it means for the price decision.

## Inputs
- `fct_mrr_monthly` (dev) · handoff `../handoffs/01-data-engineer.md` · `context/business.md`

## Deliverables
- `analyses/01_mrr_bridge.sql` … `04_segment_summary.sql` (each with a comment naming the claim it supports)
- `analyses/findings.md` (pyramid format)

## Definition of done
- AC3: August change in USD and %, drivers sum to the total.
- At least two hypotheses tested; "what would change my mind" section.

## Constraints
- Use definitions in `context/metrics.md`. Do **not** read `../sealed/`.
