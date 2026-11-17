---
name: bi-engineering
description: BI engineering knowledge for the Data Factory — dashboard design for decisions, chart selection, semantic layers and metric governance, self-serve, performance, and a dependency-free HTML dashboard fallback. Load when building or changing dashboards, reports or metric layers.
---

# BI Engineering

Principles:
1. **One dashboard, one audience, one job.** If you cannot name the decision it supports, don't build it.
2. **Define once, use everywhere.** Metrics live in the semantic layer; dashboards reference them.
3. **Top-down layout.** KPIs with comparison → trend → breakdown → detail.
4. **Titles state the takeaway.** Axes have units; date range and freshness are visible.
5. **Reconcile.** Every dashboard number matches the mart queried directly.

Read `references/router.md` and load only what the task needs.
