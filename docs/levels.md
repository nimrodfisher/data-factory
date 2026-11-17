# The 6 levels of the Data Factory

Where is your data team today? Inspired by the "levels of AI adoption" discussion around dark software factories.

| Level | Name | Who does the work | What the human does | You know you're here when… |
|---|---|---|---|---|
| **0** | Hand-crafted | you | everything | every number is a query you typed |
| **1** | Autocomplete | you + copilot | writes SQL, accepts suggestions | AI finishes your `GROUP BY` |
| **2** | Chat analyst | you + chatbot | pastes schemas in, copies SQL out, checks it | you have a "useful prompts" doc |
| **3** | Agent in the repo | one agent with context | asks, reviews every query and chart | the agent runs queries, you read all of them |
| **4** | **Data Factory (gated)** | specialist agents + inspector | approves specs and ships; reads the trace | you review a verdict and 5 numbers, not 40 queries |
| **5** | Lights-out | factory, on a schedule | curates truths & definitions, audits traces | recurring questions answer themselves; you spend time on new ones |

## How to climb
- **0–2 → 3:** put context in the repo (`/data-factory:init`): business, metric definitions, source quirks.
- **3 → 4:** add *independent verification*. Fill `context/truths.md` with 3–5 numbers from finance/CRM/board decks. Turn on the inspector. Use gates.
- **4 → 5:** track inspector verdicts over runs. When a recurring request passes holdouts consistently, set `autonomy: lights-out` for it. Never let any level write to production.

The lever at every step is the same: **better definitions and better truth anchors**, not a smarter model.
