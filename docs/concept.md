# From software factory to data factory

## The software factory, in one paragraph
In 2026 a handful of teams showed that a few engineers can run a "software factory": specialised coding agents write, test and ship software while humans define intent and judge outcomes. StrongDM's AI team published the most radical version in February 2026 — two rules, *code must not be written by humans* and *code must not be reviewed by humans* — with specs and scenarios driving agents that converge without human review ([StrongDM](https://factory.strongdm.ai/), [Simon Willison's write-up](https://simonwillison.net/2026/Feb/7/software-factory/)). Factory.ai, BCG Platinion, Mastra, LaunchDarkly and others have since described agent-native delivery where engineers define intent and review the trace, and the bottleneck moves from writing code to **specifying and verifying it** ([Factory.ai](https://factory.ai/articles/what-is-a-software-factory), [Unblocked](https://getunblocked.com/blog/what-is-an-ai-software-factory-buyers-guide/), [Mastra](https://mastra.ai/blog/software-factory)).

The recurring building blocks:
1. **Specs** instead of tickets — intent precise enough for an agent to execute.
2. **Specialised agents** with clear stations and handoffs.
3. **Verification the agents cannot game** — StrongDM keeps customer scenarios *hidden from the coding agents*, like a holdout set.
4. **Human gates** on intent and on shipping, not on every line.
5. **A trace** humans can audit, and **memory** that compounds.

## Why data needs its own factory
Data work fails differently from software:

| Software | Data |
|---|---|
| Wrong code usually fails loudly (tests, crashes) | Wrong numbers look exactly like right numbers |
| Correctness ≈ "does it do what the spec says" | Correctness ≈ "does it agree with reality" — finance, CRM, the board deck |
| Bugs live in code | Bugs live in **definitions** ("active", "revenue") and **sources** (duplicates, late data, test accounts) |
| One kind of builder | Four crafts: engineering, analysis, statistics, BI |

So a data factory needs:
- **Definition-first specs** — every metric word pinned down before anyone writes SQL.
- **Truth anchors** — known-good external numbers (`context/truths.md`) the outputs must reconcile to.
- **Sealed holdouts** — written by an independent inspector *before* the build; the builders never see them.
- **Adversarial re-derivation** — the inspector recomputes the headline numbers from raw data with its own query.
- **Stations for four crafts**, each with deep, on-demand knowledge.

## The Data Factory line
```
request → SPEC → [gate 1] → SEAL → PLAN → BUILD (DE · Analyst · DS · BI) → INSPECT ⟲ rework → SHIP → [gate 2] → LEARN
```

| Software factory idea | Data Factory implementation |
|---|---|
| Spec | `spec.md`: intent as a decision, definitions table, testable acceptance checks |
| Hidden scenarios | `sealed/holdouts.md`: truth anchors, invariants, known traps |
| Specialised agents | `data-engineer`, `data-analyst`, `data-scientist`, `bi-engineer` |
| Verification agent | `quality-inspector` — independent, never builds, PASS / REWORK / BLOCK |
| Human gates | spec approval + ship approval; nothing touches prod (enforced by a hook) |
| Trace | `runs/<id>/`: spec → orders → handoffs → inspection → ship |
| Memory | `context/` + `lessons.md`, updated after every run |
| Autonomy dial | `supervised` → `gated` → `lights-out` |

## What stays human
Intent (which decision matters), definitions (what "revenue" means here), truth anchors (what reality says), and the decision to ship. The factory makes those four things the *only* things you have to do.

See [`levels.md`](levels.md) for the maturity model and [`../examples/mrr-drop`](../examples/mrr-drop) for a full run.
