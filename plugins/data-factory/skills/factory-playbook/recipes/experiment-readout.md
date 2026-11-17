---
recipe: experiment-readout
autonomy: gated
size: M
---
# Data Spec — A/B test readout: {{experiment}}

## 1. Intent
Decide whether to ship {{variant}}.
> Primary metric up with guardrails flat → ship. Flat → keep control or iterate. Guardrail down → don't ship.

## 2. Deliverables
- [ ] Readout with effect, 95% CI, guardrails, SRM check → `analyses/<slug>/readout.md` (data-scientist)

## 3. Definitions
Randomisation unit: {{user/account}}. Primary metric: {{metric}}. Guardrails: {{metrics}}. Window: {{dates}}.

## 5. Acceptance checks
- AC1 SRM check reported before any metric.
- AC2 Primary metric effect with 95% CI and the pre-declared test.
- AC3 Guardrails reported; any post-hoc segment labelled exploratory.
- AC4 Recommendation in one sentence with expected business impact range.
