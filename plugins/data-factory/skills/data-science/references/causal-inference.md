# Causal Inference (observational data)

Use when the question is "what did X *cause*?" and there was no randomised test.

## Pick the design from the situation
| Situation | Design | Key assumption to defend |
|---|---|---|
| Change hit one group, a comparable group was unaffected, data before and after | **Difference-in-differences (DiD)** | parallel trends — check pre-period trends visually and with an event-study plot |
| One treated unit (a market, the whole company), several untreated units | **Synthetic control** | donor pool can reproduce the pre-period path |
| Treatment assigned by a cutoff on a score (discount for accounts > 50 seats) | **Regression discontinuity** | no manipulation at the cutoff; units just above/below are comparable |
| Opt-in treatment, rich pre-treatment covariates | **Propensity score matching / weighting, doubly robust** | no unmeasured confounders (strong — state it) |
| Single time series, a known intervention date, no control | **Interrupted time series** | nothing else changed at that date; weakest design |
| An instrument affects treatment but not outcome directly | **Instrumental variables** | exclusion restriction (rarely convincing in business data) |

## DiD recipe
```
outcome ~ treated + post + treated:post   (+ unit and time fixed effects)
effect = coefficient on treated:post
```
- Cluster standard errors by unit.
- Plot treated vs control over time with the event date marked; show pre-trends.
- Placebo tests: fake event date in the pre-period → effect ≈ 0; fake treated group → effect ≈ 0.

## Reporting
- State the estimand ("average effect on the treated over 3 months").
- Effect with CI, the design, and the assumption it rests on.
- Robustness: alternative control groups, windows, placebo tests.
- Language: "estimated effect", and say what would invalidate it.
