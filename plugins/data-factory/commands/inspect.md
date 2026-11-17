---
description: Run the Quality Inspector on a run, a model, a query or an analysis — acceptance checks, reconciliation and adversarial review.
argument-hint: "[run folder, file path, or blank for the latest run]"
---

Inspect: **$ARGUMENTS** (if blank, use the most recent folder in `.data-factory/runs/`).

Dispatch the **quality-inspector** agent in INSPECT mode with:
- the target (run folder or file paths),
- the spec, if one exists (if inspecting a standalone file, ask the inspector to infer intent from the file and `.data-factory/context/` and state it explicitly),
- `.data-factory/context/truths.md` for reconciliation anchors.

When it returns, show the human: verdict, failed checks with evidence, headline numbers (builder vs inspector) and confidence. If the verdict is REWORK, offer to dispatch the rework orders to the right stations.
