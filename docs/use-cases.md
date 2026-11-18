---
title: "Use cases — what a lean data team runs through an AI data team"
description: "Practical playbooks: metric investigations, weekly KPI reviews, dashboards, new data sources, A/B tests and forecasts with Data Factory's AI agents."
---
# Use cases — what a lean data team actually runs through the factory

Each one: **who asks → what you type → what you get → how much you're involved.**
Six of them ship as ready-made specs ("recipes") that `/data-factory:init` copies into `.data-factory/specs/`. Re-run any of them with `/data-factory:run <name>`.

---

### 1. "Why did this number change?" — the most common request
**Who asks:** CEO, finance, a PM — usually in Slack, usually urgent.
**You type:**
```
/data-factory:run Signups dropped 18% last week. Real or tracking? What drove it?
```
or use the recipe: `/data-factory:run metric-alert-investigation` (it asks for the metric and period).
**You get:** a memo that first says *whether the change is real*, then the drivers in $ or counts that add up to the total, alternatives it ruled out, and what would change its mind. If the data is broken, a fix on a branch.
**Your involvement:** approve the spec (1 min), read the ship report (3 min).
**Replaces:** half a day of an analyst slicing dashboards.

### 2. Weekly KPI review — on autopilot
**Who asks:** nobody — it just arrives every Monday.
**You type (once):** fill the KPI list in `.data-factory/specs/weekly-kpi-review.md`, then schedule it ([GitHub Actions template](https://github.com/nimrodfisher/data-factory/blob/main/integrations/github/scheduled-recipe.yml)).
**You get:** a PR every Monday with the KPI table (vs last week and 4-week average), a short "why" note for anything outside its normal range, and a refreshed dashboard.
**Your involvement:** skim the PR. The recipe runs `lights-out` — it's safe because it only reads tested marts and reconciles to your truth anchors.
**Replaces:** the Monday-morning spreadsheet ritual.

### 3. Dashboard requests
**Who asks:** "Can I get a dashboard for X?"
**You type:** `/data-factory:run dashboard-request` (or describe it in plain words).
**You get:** a dashboard brief (audience, decision, 3–5 questions), metrics defined once in your semantic layer, the dashboard in your BI tool's dev folder, every KPI reconciled to the mart.
**Your involvement:** approve the brief; publish it yourself.
**Tip:** half of dashboard requests are really a question. The spec step makes the requester name the decision — sometimes a one-off memo is the right answer.

### 4. Onboard a new data source
**Who asks:** "We just bought HubSpot / added a payments provider."
**You type:** `/data-factory:run new-source-onboarding` → "Onboard HubSpot deals and contacts for the pipeline dashboard".
**You get:** a source profile (keys, nulls, duplicates, freshness), staging models with tests, one mart for the first use case, and a schedule definition in a PR — disabled.
**Your involvement:** `supervised` by default — you see each handoff. New pipelines deserve it.

### 5. A/B test readouts
**Who asks:** product team, end of an experiment.
**You type:** `/data-factory:run experiment-readout` → "Onboarding v2, randomised by account, primary = activation in 7 days".
**You get:** SRM check first, effect with 95% CI, guardrails, a one-sentence ship/no-ship recommendation with an impact range.
**Your involvement:** approve the spec — this is where you stop p-hacking before it starts (primary metric declared up front).

### 6. Monthly forecast for the board
**You type:** `/data-factory:run monthly-forecast`
**You get:** base / downside / upside with 80% intervals, last month's forecast vs actual (honestly), backtest against naive baselines, a forecast panel on the dashboard.

### 7. Audit something that already exists
**Who asks:** you, before a board meeting, or when inheriting a dbt project.
**You type:** `/data-factory:inspect models/marts/finance/` or `/data-factory:inspect analyses/q3_pricing.sql`
**You get:** the inspector's verdict on existing work — grain tests, reconciliation to `truths.md`, adversarial checklist, independently re-derived headline numbers.
**Great for:** checking a contractor's or a teammate's analysis before it goes to the exec team.

### 8. Scope a vague request before anyone builds
**You type:** `/data-factory:spec Marketing wants "a single view of the customer"`
**You get:** a spec with the decision, definitions and acceptance checks — and the 3 questions you need to ask marketing. Paste it back to them.
**Why it matters:** most wasted data work is a definition problem. This takes 2 minutes.

### 9. Teach it once, benefit forever
```
/data-factory:learn Active account = at least 1 login in the last 28 days, excludes internal and trial accounts
/data-factory:learn Finance close Oct 2026 invoiced revenue = 5,112,040 USD ±0.5%
/data-factory:learn Stripe re-syncs duplicate invoices — dedupe on invoice_id, keep latest _loaded_at
```
Every future run uses these. Truth anchors (the second one) make the inspector dramatically stronger.

---

## Which autonomy for which work

| Work | Autonomy | Why |
|---|---|---|
| Recurring reports on tested marts | `lights-out` | same spec every time, reconciled to truths |
| Questions & investigations | `gated` | approve the spec, read the result |
| Dashboards, forecasts, experiments | `gated` | you publish/present it, so you approve it |
| New pipelines & sources | `supervised` | new code paths into the warehouse |
| Anything touching production | always a PR | the factory never deploys |

Set the default in `factory.yaml`; a saved spec can override it with an `autonomy:` line.
