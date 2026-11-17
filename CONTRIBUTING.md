# Contributing

Thanks for helping one-person data teams everywhere. The most valuable contributions:

1. **Platform adapters** — a new warehouse, transform tool, orchestrator or BI tool: one file in `plugins/data-factory/skills/platforms/references/` + one router row.
2. **Knowledge** — sharper references for a station (a new analysis method, a testing pattern, a forecasting technique). Keep them dense, practical and correct; cite nothing you haven't verified.
3. **Holdout patterns** — traps you've seen in real data (timezone edges, currency mixing, CDC tombstones…) for `skills/data-quality/references/holdouts.md`.
4. **New stations** — analytics engineer, ML engineer, data steward. Follow the existing agent shape (protocol, non-negotiables, handoff).
5. **Demos** — another synthetic dataset with a story and traps (e-commerce, marketplace, fintech), plus a reference run.

## Rules of thumb
- **Lean entry points.** `SKILL.md` stays short; depth goes in `references/`, routed by `router.md`.
- **Every agent instruction is testable.** Prefer "state the grain in a header comment" over "write good models".
- **Never weaken safety.** Agents work in dev, never read `sealed/`, never ship to prod.
- **Run the checks:** `python3 tests/validate_repo.py && python3 tests/test_sql_guard.py`.
- For the demo: `python demo/generate_data.py && python examples/mrr-drop/build.py` must pass.

## PR checklist
- [ ] Router updated if you added a reference
- [ ] Frontmatter valid (`name`, `description`) on new agents/skills/commands
- [ ] Checks pass locally
