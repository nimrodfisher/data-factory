# Demo — run a data team in 5 minutes

A fictional B2B SaaS ("Fieldnote") in a local DuckDB file. No warehouse, no credentials.

```bash
cd demo
pip install duckdb pandas numpy
python generate_data.py                # → saas.duckdb (raw.accounts, raw.subscriptions, raw.invoices)
claude                                 # start Claude Code in this folder
```
Inside Claude Code:
```
/plugin install data-factory --marketplace nimrodfisher/data-factory
/data-factory:run MRR dropped in August. Why — and was the Starter price increase a mistake? Forecast to December and give me a dashboard to track it.
```

The demo already has a `.data-factory/` folder (config + business context + metric definitions + two truth anchors), so the factory skips setup and goes straight to the spec.

## What to watch for
- **Gate 1** — the factory shows you a spec summary. Approve or edit it.
- **The inspector** — the data hides two traps. A good run catches both before shipping. No spoilers here; compare with the [reference run](../examples/mrr-drop) afterwards.
- **Gate 2** — the ship report lists what needs your decision.

## Files
| File | What |
|---|---|
| `generate_data.py` | deterministic synthetic data (seed 42) |
| `q.py` | the query runner the agents use: `python3 q.py "select …"` |
| `.data-factory/` | factory config, context, truth anchors |

Reset anytime: `python generate_data.py` (rebuilds `saas.duckdb` from scratch; delete `.data-factory/runs/*` to clear runs).
