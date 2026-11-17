---
name: data-engineering
description: Data engineering knowledge for the Data Factory — ingestion and incremental loads, layered modeling (staging/intermediate/marts, Kimball, SCD), orchestration, data contracts, SQL craft and warehouse performance. Load when building or changing pipelines, models or tables.
---

# Data Engineering

Principles that never change:
1. **Grain first.** Every table has one grain you can state in a sentence.
2. **Idempotent everything.** Re-running a load or model for the same window yields the same result.
3. **Raw is immutable.** Land raw data untouched; clean in staging; business logic in intermediate/marts.
4. **Test at the boundaries.** Keys unique and not null, relationships hold, freshness and volume within expectations.
5. **Explicit over clever.** CTEs, explicit columns, named joins, comments that explain *why*.

Read `references/router.md` and load only what the task needs.
