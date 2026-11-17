# Work Order {{NN}} — {{station}}

| Field | Value |
|---|---|
| Run | {{run_id}} |
| Depends on | {{upstream orders or "none"}} |
| Spec | `../spec.md` |

## Objective
One or two sentences. What exists when this is done that does not exist now.

## Inputs
- Tables / files: …
- Upstream handoffs: `../handoffs/…`

## Deliverables
- `{{path}}` — {{what}}

## Definition of done
- Acceptance checks owned: AC…
- Tests / validation required: …

## Constraints
- Environment: dev only
- Conventions: see `factory.yaml`
- Do **not** read `../sealed/`
