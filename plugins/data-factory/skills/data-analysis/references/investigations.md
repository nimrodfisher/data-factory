# Investigations — "Why did X change?"

Follow these steps in order. Most bad answers skip step 1 or stop at step 3.

## 1. Is the change real?
- **Data checks**: duplicates on the grain, missing days/partitions, late loads, a pipeline or definition change, a tracking release, test accounts. Compare against an independent source (`context/truths.md`).
- **Noise check**: is the change outside normal variation? Compare with the trailing 6–12 periods (mean ± 2σ, or the historical range of month-over-month changes). Check seasonality (same period last year).
- If the data is broken → stop, report the data issue as the finding.

## 2. Pin down *when*
Plot at the finest useful grain (daily/weekly). Step change (one date → event: release, price change, outage, tracking change) vs gradual drift (market, mix, competitor) vs spike (one-off, bulk action, bot).

## 3. Decompose the metric
Use the metric tree. Quantify each component's contribution to the change so they **sum to the total**.
```
ΔMRR = new + expansion − contraction − churn
```
Then the component that moved most is the focus.

## 4. Segment the moving component
Slice by the dimensions that plausibly matter: plan, segment/size, region, channel, cohort (signup month), platform, product line. For each segment compute:
- its contribution to the total change (absolute),
- its rate change vs its own baseline.
Use **mix vs rate decomposition** when segment shares shift:
```
Δ total rate = Σ (Δ share_i × rate_i,before)      ← mix effect
             + Σ (share_i,after × Δ rate_i)      ← rate effect
```
If the total moves but no segment's rate does → mix shift (Simpson's paradox territory).

## 5. Match to events
Cross-reference the timing and the segment with `context/business.md` (pricing, launches, campaigns, outages, org changes) and external events (holidays, seasonality). A cause should explain **when, where (which segment) and how much**.

## 6. Test hypotheses — try to disprove
| Hypothesis | Prediction if true | Evidence for | Evidence against | Verdict |
|---|---|---|---|---|
Write at least two. Good disproof tests: the effect should be absent in an unaffected segment (natural control); it should start exactly at the event date; dose-response (bigger exposure → bigger effect).

## 7. Size it and say what to do
- Quantify: "X explains $Y (Z%) of the $T drop."
- Unexplained remainder: say how much is left and why.
- Recommend an action and the metric to watch, and say what evidence would change the conclusion.
- If causality matters for a big decision → hand to the data-scientist station for a causal design (difference-in-differences with the unaffected segment, etc.).
