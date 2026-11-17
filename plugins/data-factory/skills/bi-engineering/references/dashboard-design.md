# Dashboard Design

## Brief (write before building)
```
Audience:    who opens it, how often, on what device
Decision:    what they decide or monitor with it
Questions:   3–5 questions it must answer, in priority order
Metrics:     from context/metrics.md (names only — defined in the semantic layer)
Filters:     the 2–4 slices users actually need
Refresh:     cadence + freshness SLA
```

## Dashboard types
| Type | Purpose | Shape |
|---|---|---|
| Executive / KPI | "are we on track?" | 4–6 KPIs with targets & comparisons, one trend each, minimal filters |
| Operational | "what needs action today?" | lists/tables sorted by urgency, thresholds, conditional formatting, links to records |
| Analytical | "why is it moving?" | trends + breakdowns, rich filters, drill-down |
Don't mix types on one page.

## Layout (Z-pattern, top-down)
1. **Header**: title (the question), date range, filters, freshness timestamp.
2. **KPI row**: 3–6 tiles. Each: value, comparison (vs prior period / target / last year) with direction colour, sparkline optional.
3. **Trend**: the main metric over time, with annotation of known events (price change, launch).
4. **Breakdown**: by the most decision-relevant dimension.
5. **Detail**: table for drill-down/export.

## KPI tile rules
- Value + delta + the comparison's name ("−4.1% vs Jul").
- Colour encodes good/bad, not up/down (churn up = bad = red).
- Avoid more than 6 tiles; more means you have not prioritised.

## Interactivity
- Global filters at the top, applied consistently; show active filters.
- Drill paths follow the metric tree (total → segment → account).
- Defaults matter more than options: the default view must answer question #1.

## Definition of done
- [ ] Brief answered; every question maps to a visual.
- [ ] Every KPI reconciled to a direct mart query (numbers recorded in handoff).
- [ ] Freshness visible; date range explicit.
- [ ] Loads in < 5s on the default view.
- [ ] Titles state takeaways or questions; units on axes; no chartjunk.
- [ ] Owner and description set in the BI tool.
