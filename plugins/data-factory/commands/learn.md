---
description: Teach the factory — capture a definition, source quirk, truth anchor or lesson so every future run uses it.
argument-hint: "<what to remember, e.g. 'active user = 1+ session in 28 days, excludes internal accounts'>"
---

Capture: **$ARGUMENTS**

Classify it and write it to exactly one place in `.data-factory/`:
- Metric or entity definition → `context/metrics.md` (name, formula, grain, filters, owner).
- Source system behaviour or quirk → `context/sources.md`.
- A known-good number (finance close, CRM total, board figure) → `context/truths.md` with date, value, source and tolerance. These become holdout anchors.
- Business fact (pricing change, launch date, org change) → `context/business.md`.
- A process lesson ("always exclude test accounts", "the inspector caught X") → `lessons.md`.

If it contradicts something already written, show both and ask which one wins. Confirm in one line where it was saved.
