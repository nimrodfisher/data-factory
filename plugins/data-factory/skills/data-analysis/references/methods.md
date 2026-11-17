# Analysis Methods

## Cohort & retention
- Cohort = entities grouped by a shared start event and period (signup month, first purchase week).
- Retention table: rows = cohort, columns = periods since start, values = % of cohort still active (logo) or % of starting revenue retained (revenue).
- Use **a spine**: every cohort member × every period, so inactive periods count as zero.
- Read it three ways: down a column (are newer cohorts better at the same age?), across a row (decay shape — does it flatten?), diagonals (calendar effects hitting all cohorts at once → external event).
- Unbounded vs bounded retention: "active in exactly period N" vs "active in N or later". State which.
- Do not compare cohorts at ages the youngest cohort has not reached.

## Funnels
- Define steps as ordered events within a conversion window per entity (e.g. signup → activated within 7 days → paid within 30 days).
- Report step conversion and overall conversion with counts; time-to-convert distribution (median, p75) matters as much as the rate.
- Cohort the funnel by entry date, so recent cohorts are not penalised for not having had time to convert (right-censoring).
- Strict order vs any order — state it.

## Segmentation
- Start with segments the business can act on (plan, size, channel, region, persona), then data-driven (RFM, behavioural clustering) only if needed.
- Each segment report: count, share, metric, metric vs overall, and the trend.
- Beware tiny segments: show counts; suppress or flag segments under a minimum size (e.g. n < 30).

## Unit economics
- ARPA, gross margin, CAC by channel, payback period, LTV:CAC (directional). Use cohort-based realised values over formula-based LTV whenever history allows.

## Sizing (TAM-style or impact sizing)
- Bottom-up beats top-down: count × rate × value, each input sourced.
- Give a range (low/base/high) and name the input that drives the uncertainty most.

## Comparisons & baselines
| Question | Baseline |
|---|---|
| Is this month unusual? | trailing 6–12 month distribution of the metric or of its MoM change |
| Seasonal business? | same period last year, or YoY growth vs prior trend |
| Did a change work? | a comparable unaffected segment / period (natural control) |
| Is this segment good? | overall average **and** the segment's own history |
