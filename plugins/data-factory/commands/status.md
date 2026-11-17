---
description: Show the factory floor — every run, its stage, verdict and what is waiting on you.
---

Read `.data-factory/runs/*/` and report a compact table, newest first:

| Run | Size | Stage | Verdict | Waiting on |
|-----|------|-------|---------|------------|

Stage is the furthest artifact present: `spec` → `sealed` → `plan` → `building (n/m handoffs)` → `inspected` → `shipped`. Verdict comes from `inspection.md`. "Waiting on" is `you` when a gate is pending (spec not approved, BLOCK verdict, ship needs PR approval), otherwise `factory`.

Below the table, list the saved specs in `.data-factory/specs/` (name + one-line intent) so the user can re-run them, then the 3 most recent lessons from `.data-factory/lessons.md`. If there is no `.data-factory/` folder, tell the user to run `/data-factory:init`.
