# Chart Selection

| Message | Chart | Notes |
|---|---|---|
| Change over time | line | ≤ 5 series; label lines directly instead of a legend |
| Change over time, few periods, discrete | column | |
| Composition over time | stacked column (counts) / 100% stacked (shares) | ≤ 5 components; most important at the baseline |
| Ranking / comparing categories | horizontal bar, sorted | start at zero; long labels fit |
| Part-to-whole, one moment | bar sorted, or pie/donut with ≤ 4 slices | |
| Contribution to a change | waterfall | MRR bridge: start → new → expansion → contraction → churn → end |
| Distribution | histogram / box plot | show n |
| Relationship of two measures | scatter | add trend line only if meaningful |
| Cohort retention | heatmap table | sequential single-hue colour scale |
| Single number | KPI tile | with comparison |
| Plan vs actual | bullet chart / line with target band | |
| Funnel | horizontal bars by step with conversion % labels | |

## Formatting rules
- Bars start at zero. Lines may not, but say so if the range is narrow.
- One highlight colour for the point of the chart; everything else grey.
- Sequential palettes for ordered values, diverging only when there is a meaningful midpoint, categorical ≤ 6 hues.
- Colour-blind safe; never encode meaning by red/green alone — add icons or labels.
- Number formats: thousands separators, `$18.4k`, `4.1%`, consistent decimals per chart.
- No dual axes, no 3D, no gradients, no gridline clutter.
- Annotate known events directly on time series.
