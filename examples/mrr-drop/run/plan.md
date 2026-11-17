# Plan — 2026-11-17-mrr-drop

Size **L** · autonomy `gated` · max rework loops 2

```
              ┌─► 02 data-analyst ──────┐
01 data-engineer                         ├─► 04 bi-engineer ─► INSPECT ─► SHIP
              └─► 03 data-scientist ────┘
SEAL (quality-inspector) runs before 01.
```

| Order | Station | Depends on | Owns | Deliverables |
|---|---|---|---|---|
| 01 | data-engineer | — | AC1, AC2 | `models/01–05_*.sql`, `tests/*.sql` |
| 02 | data-analyst | 01 | AC3 | `analyses/01–04_*.sql`, `analyses/findings.md` |
| 03 | data-scientist | 01 | AC4 | `notebooks/price_change_impact.py`, `notebooks/model_card.md` |
| 04 | bi-engineer | 02, 03 | AC5 | `dashboards/build_dashboard.py`, `dashboards/mrr_dashboard.html` |

02 and 03 were dispatched **in parallel** after 01's handoff.
