# Gates & Verification

The factory replaces "a human reviews every query" with **a verification system the human trusts**. Three layers:

1. **Acceptance checks** (in the spec, visible) — builders aim at them.
2. **Sealed holdouts** (written by the inspector before build, never shown to builders) — catch overfitting to the visible checks, exactly like held-out scenarios in a software factory or a holdout set in ML.
3. **Adversarial review** — the inspector independently re-derives headline numbers and hunts for known failure modes.

## Autonomy levels (`factory.yaml → autonomy`)
| Level | Human approves | Use when |
|---|---|---|
| `supervised` | spec, every handoff, ship | new factory, new domain, sensitive data |
| `gated` (default) | spec, ship | normal operation |
| `lights-out` | nothing during the run; reviews the trace & ship report | recurring requests with strong `truths.md` and a track record of PASS verdicts |
**No level ever writes to production.** Gate 2 (merge/publish/schedule) always belongs to a human.

## Gate 1 — spec approval (6-line summary)
```
Intent:        …
Deliverables:  …
Key definitions: …
Acceptance checks: n
Assumptions to veto: …
Stations: DE → Analyst → BI   (size M)
```

## Inspection loop
```
INSPECT → PASS ─────────────► SHIP
        → REWORK ─► stations fix ─► INSPECT (max 2 loops)
        → BLOCK ──► human decision
```
- Rework orders describe **symptom + evidence**, never quote the holdout.
- After the max loops, escalate with: what keeps failing, the evidence, and your recommendation (accept with caveat / change the spec / fix the source).

## Escalate to the human immediately when
- A truth anchor disagrees by more than tolerance and nobody can explain why.
- Source data appears broken (row-count cliff, duplicated loads, missing days).
- The honest answer is "the data cannot answer this".
- A definition decision would change the conclusion.
