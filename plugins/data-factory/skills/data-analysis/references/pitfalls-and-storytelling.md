# Pitfalls & Storytelling

## Pitfalls checklist (run before writing conclusions)
- [ ] **Simpson's paradox / mix shift** — totals move differently from every segment.
- [ ] **Survivorship** — analysing only customers who are still here.
- [ ] **Selection bias** — users who chose a feature differ from those who didn't; "feature users retain better" is not causal.
- [ ] **Regression to the mean** — extreme periods/segments drift back on their own.
- [ ] **Small numbers** — big % changes on tiny bases; show counts and intervals.
- [ ] **Multiple comparisons** — slicing 40 ways guarantees a "significant" segment. Treat post-hoc segments as hypotheses.
- [ ] **Right-censoring** — recent cohorts haven't had time to convert/churn.
- [ ] **Denominator drift** — definition or population of the denominator changed.
- [ ] **Seasonality & calendar** — month length, weekdays per month, holidays, fiscal vs calendar.
- [ ] **Data artefacts** — tracking changes, duplicate loads, backfills, timezone shifts masquerading as behaviour.
- [ ] **Correlation ≠ causation** — use "associated with" unless there is a causal design.

## Confidence labels
| Label | Meaning |
|---|---|
| High | data validated, effect large vs noise, timing + segment + size all consistent, alternatives ruled out |
| Medium | consistent story, one alternative not fully ruled out or data caveat remains |
| Low | directional only; small sample, data issues or competing explanations |

## The findings memo (pyramid principle)
```
# <Question restated as a decision>

## Answer
<1–3 sentences. Conclusion + the number + confidence.>

## Why we believe it
1. <Supporting point with number> (query: analyses/…sql)
2. …
3. …

## What it is not
<Alternatives considered and the evidence against them.>

## Recommendation
<Action, owner, metric to watch, when to re-check.>

## What would change my mind
<Evidence that would overturn the conclusion.>

## Method & caveats
<Definitions used, data window, exclusions, data issues found.>
```

## Writing rules
- Lead with the "so what". Headlines state the takeaway ("SMB churn drove 71% of the drop"), not the topic ("Churn by segment").
- Numbers: round sensibly ($18.4k, 4.1%), always with the comparison (vs last month / vs last year / vs plan).
- One idea per paragraph; tables for comparisons, charts for shapes/trends.
- Separate facts ("the data shows") from interpretation ("this suggests").
