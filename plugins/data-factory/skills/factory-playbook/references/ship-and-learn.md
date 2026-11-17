# Ship & Learn

## Ship report rules
- **Answer first**, in three lines, with the number. ("MRR fell 4.1% in Aug (−$18.4k). 71% of the drop is SMB churn on the Starter plan after the Aug 1 price increase. Forecast: flat through Dec unless win-back works.")
- Every deliverable has a path.
- "How we know it is right" lists checks passed, holdouts passed, the builder-vs-inspector headline numbers, and what rework caught. This section is what lets a human trust the factory without reading every query.
- Confidence (High/Medium/Low) with the reason.
- "Needs your decision" is a checklist: PRs to merge, dashboards to publish, definitions to approve.

## Shipping to production
The factory prepares; the human deploys.
- Models / pipelines → a branch + PR description (what changed, tests, row counts, downstream impact).
- Dashboards → a dev/staging folder or a branch for code-based BI.
- Schedules → the DAG/job definition in a PR, disabled by default.

## Learn (the compounding loop)
After every run, write 1–5 lessons. A lesson is something that would have made this run faster or more correct.
| Learned | Write to |
|---|---|
| A definition the human confirmed | `context/metrics.md` |
| A source quirk (duplicates, late data, timezone) | `context/sources.md` |
| A known-good number | `context/truths.md` |
| A business event that explains data | `context/business.md` |
| A process lesson | `lessons.md` (dated, one line each) |

Lessons format: `- 2026-09-04 · billing re-syncs duplicate invoices; dedupe on invoice_id keeping latest _loaded_at (caught by inspector H2)`

Keep context files short and current: when a fact changes, edit the line — don't append a contradiction.
