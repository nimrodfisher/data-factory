# Handoff 04 — bi-engineer

**Status:** done

## Built
| Path | What |
|---|---|
| `dashboards/build_dashboard.py` | generates the dashboard from marts, analyses and DS outputs |
| `dashboards/mrr_dashboard.html` | self-contained (no CDN), light/dark, hover tooltips, mobile layout |

Brief: CEO/CFO, monthly. Q1 Where is MRR? Q2 Why did it move in August? Q3 Is the price change paying off? Q4 Where is it heading?
Layout: 5 KPIs → MRR trend + forecast (annotated events) → Aug bridge → churn: re-priced vs comparison → price-change ledger → segment table.

## How I verified (AC5)
| KPI | Dashboard | Direct mart query | OK |
|---|---|---|---|
| MRR Oct 2026 | $4.67M | 4,671,314.10 | ✅ |
| MRR change Aug | −$62.5k | −62,467.90 | ✅ |
| Starter monthly churn Oct | 4.9% | 73 / 1,487 = 4.91% | ✅ |
| Net price impact | −$10.6k | −10,638.83 (DS output) | ✅ |

Freshness: "Data as of 2026-10-31" + build timestamp in the header.
