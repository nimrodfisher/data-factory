# Experimentation (A/B tests)

## Design (before launch)
1. **Hypothesis**: change → mechanism → expected metric movement.
2. **Primary metric** (one), **secondary** metrics, **guardrails** (must not degrade). Declare them before launch.
3. **Randomisation unit** = the unit the metric is measured on (user, account). Randomising users while measuring accounts causes interference.
4. **Sample size** from baseline rate, minimum detectable effect (MDE), α = 0.05, power = 0.8:
   - proportions, per arm ≈ `16 · p(1−p) / MDE²` (absolute MDE) — rule of thumb.
   - Compute exactly with `statsmodels.stats.power` (`NormalIndPower`, `TTestIndPower`).
5. **Duration**: at least one full business cycle (usually ≥ 1–2 weeks) even if sample size is reached sooner — weekday effects.
6. Write the analysis plan (tests, segments to check, stopping rule) before data arrives.

## Readout checklist
- [ ] **SRM check first**: chi-square on assignment counts vs expected split; p < 0.001 → stop, the experiment is broken.
- [ ] Exposure: analyse users who were eligible and assigned (intent-to-treat), not only those who "saw" the feature.
- [ ] Primary metric: effect, 95% CI, p-value. Report the CI — it carries the business meaning.
- [ ] Guardrails: no significant degradation.
- [ ] Novelty/primacy: effect over time within the test.
- [ ] Segments: pre-declared only; others are hypotheses for the next test.

## Pitfalls
| Pitfall | Fix |
|---|---|
| Peeking and stopping at first significance | fixed horizon, or sequential testing (mSPRT / alpha spending) |
| Many metrics/segments | Bonferroni/Holm for confirmatory, or label as exploratory |
| Ratio metrics (revenue per session) with user randomisation | delta method or bootstrap at the user level |
| Heavy-tailed revenue | winsorise (pre-declared cap) or use a bootstrap; consider a transformed metric |
| Network effects / shared accounts | cluster randomisation |

## Variance reduction
**CUPED**: adjust the metric with its pre-experiment value: `Y_adj = Y − θ (X_pre − mean(X_pre))`, `θ = cov(Y, X_pre)/var(X_pre)`. Typically cuts required sample size substantially when pre-period behaviour predicts the metric.

## Readout format
"Variant B increased paid conversion from 4.1% to 4.6% (+0.5pp, 95% CI +0.1 to +0.9pp, p = 0.02, n = 41,200). Guardrails flat. Recommend ship. Expected impact ≈ +$X MRR/month (range …)."
