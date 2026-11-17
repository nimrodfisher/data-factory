---
recipe: new-source-onboarding
autonomy: supervised          # new pipelines: approve each handoff
size: L
---
# Data Spec — Onboard {{source}} into the warehouse

## 1. Intent
Make {{source}} data ({{tables/entities}}) trustworthy and usable for {{first use case}}.

## 2. Deliverables
- [ ] Source profile (row counts, keys, nulls, freshness, quirks) → `context/sources.md` row + `analyses/<slug>/profile.md` (data-engineer)
- [ ] Staging models with tests + source freshness → `models/staging/{{source}}/` (data-engineer)
- [ ] One mart for the first use case → `models/marts/` (data-engineer)
- [ ] Schedule definition, **disabled**, in a PR (data-engineer)

## 3. Definitions
Grain of each staging model = one row per {{source entity}}. Dedup rule documented.

## 5. Acceptance checks
- AC1 Every staging model: unique + not_null on its key, accepted values on enums.
- AC2 Source row counts reconcile to staging after the documented dedup rule.
- AC3 Freshness check defined with an SLA.
- AC4 Nothing written outside dev; schedule ships disabled.

## 6. Out of scope
Dashboards, analysis.
