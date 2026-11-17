# Sealed Holdouts

## Why sealed
Builders optimise for what they can see. Visible acceptance checks become targets; sealed holdouts measure whether the work is actually right. This is the same idea as hidden test scenarios in a software factory and as a held-out set in ML: **an evaluation the producer never trained on.**

## Sources of good holdouts
| Kind | Where it comes from | Example |
|---|---|---|
| Truth anchor | `context/truths.md` | "Aug invoiced revenue reconciles to finance close $412,300 ±0.5%" |
| Invariant | the metric tree / model logic | "new + expansion − contraction − churn = ΔMRR every month, exactly" |
| Grain invariant | the entity model | "every paying account appears once per month in the MRR mart" |
| Known trap | `context/sources.md`, `lessons.md` | "no duplicated invoice_id after the Sep re-sync" |
| Boundary | time zones, period edges | "events at 23:30 UTC on the 31st land in that month" |
| Population | exclusions | "test/internal accounts excluded (count = 0 in marts)" |
| Cross-source | two systems that must agree | "active subscriptions in billing ≈ paying accounts in CRM ±1%" |
| Directional sanity | business context | "churned MRR in the price-change month exceeds the trailing 3-month mean" (only when context supports it) |

## Writing a holdout
```
H<n> · <statement>
How to check: <query or procedure>
Tolerance: <exact | ±x% | ±n rows>
Severity: blocker | major | minor
Why: <the failure it protects against>
```
3–8 holdouts per run. At least one truth anchor when `truths.md` has a relevant entry; at least one invariant; at least one known trap. If `truths.md` is empty, say so in the inspection notes — it is the biggest lever for factory reliability.

## Keeping them sealed
- Stored in `runs/<id>/sealed/`; builders are instructed never to read it.
- Rework orders describe **symptoms and evidence** ("Aug revenue in `fct_revenue` is 6.8% above an independent finance figure; investigate duplicate invoice rows"), not the holdout text.
- After shipping, a holdout that caught something becomes a lesson and, if general, a permanent test in the project. Write a fresh holdout next time.
