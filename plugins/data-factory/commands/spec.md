---
description: Turn a fuzzy data request into a Data Spec with testable acceptance checks — without building anything yet.
argument-hint: "<the request, e.g. 'a churn dashboard for the CS team'>"
---

Write a Data Spec for: **$ARGUMENTS**

1. Load the `factory-playbook` skill and read its intake-and-spec reference.
2. Read `.data-factory/factory.yaml` and `.data-factory/context/` if they exist.
3. Create `.data-factory/runs/<YYYY-MM-DD>-<slug>/spec.md` from the template. Fill every section; turn every vague word ("active", "revenue", "recent") into an explicit definition.
4. Ask the human at most 3 blocking questions in one message; record everything else as an assumption.
5. If the user says this request will recur, also save a copy as `.data-factory/specs/<slug>.md` so it can be re-run with `/data-factory:run <slug>`.
6. Show the spec summary and tell the user they can run `/data-factory:run` on this spec (point it at the run folder) once they approve.
