# Inspection — 2026-11-17-mrr-drop

## Loop 1 → **REWORK**

| ID | Type | Statement (holdouts summarised) | Result | Evidence |
|---|---|---|---|---|
| AC1 | acceptance | MRR mart grain | ✅ | 0 duplicate account-months |
| AC2 | acceptance | bridge reconciles | ✅ | 21/21 months |
| H1 | holdout | July MRR vs external anchor | ❌ | mart $4,622,509 vs anchor $4,551,409 → **+1.56%** (tolerance 0.5%) |
| H2 | holdout | Aug invoiced revenue vs external anchor | ❌ | staging $7,262,053 vs anchor $4,958,131 → **+46.5%** |
| H4 | holdout | unique keys in staging | ❌ | 1,132 duplicate `invoice_id`s, all loaded 2026-09-03 02:14 |
| H5 | holdout | population | ❌ | 3 accounts named "Internal Demo Account", "QA Sandbox Corp", "ACME Test Co" with `is_test = true` in the mart |
| R1 | adversarial | analyst memo drivers | ❌ | memo attributes −$47.4k to "Enterprise churn"; both churned accounts are in the H5 list |

### Rework orders
**→ data-engineer**
- Symptom: Jul MRR in `fct_mrr_monthly` is $71.1k above an independent finance figure; Aug paid invoices in `stg_billing__invoices` are ~46% above finance.
- Evidence: `select invoice_id, count(*) from stg_billing__invoices group by 1 having count(*) > 1` → 1,132 rows; `select account_name from stg_billing__accounts where is_test` → 3 rows present in the mart.
- Expected: deduplicate invoices with a documented rule; apply the `metrics.md` exclusion for test/internal accounts once, upstream of all marts.

**→ data-analyst** (after the engineer's fix)
- Symptom: the "Enterprise churn" driver is two internal accounts. Re-run all analyses on the corrected mart and re-check whether conclusions change.

## Loop 2 → **PASS**

| ID | Type | Result | Evidence |
|---|---|---|---|
| AC1–AC2 | acceptance | ✅ | tests pass |
| AC3 | acceptance | ✅ | +84.3k +14.7k −3.1k −158.4k = −62.5k |
| AC4 | acceptance | ✅ | CI reported, pre-trend flat, component MAE $28.6k < naive $83.8k |
| AC5 | acceptance | ✅ | 4 KPIs reconciled (handoff 04) |
| H1 | holdout | ✅ | $4,551,409.30 vs $4,551,409 (0.00%) |
| H2 | holdout | ✅ | $4,958,131.40 vs $4,958,131 (0.00%) |
| H3 | holdout | ✅ | bridge exact every month |
| H4 | holdout | ✅ | 0 duplicate keys |
| H5 | holdout | ✅ | 0 test accounts in mart, analyses, dashboard |
| H6 | holdout | ✅ | see below |
| H7 | holdout | ✅ | Starter monthly churned MRR Aug $109.0k vs trailing mean $20.5k |
| R2 | adversarial | ✅ | DiD comparison group sensible; uplift counted only on still-active accounts |
| R3 | adversarial | ⚠️ minor | forecast beats drift only marginally ($28.6k vs $30.3k) — acceptable; chosen for scenario ability. Noted in ship report. |

## Headline numbers — builder vs inspector (independent query from `raw.subscriptions`)
| Number | Builder | Inspector | Δ | OK |
|---|---|---|---|---|
| MRR Jul 2026 | 4,551,409.30 | 4,551,409.30 | 0 | ✅ |
| MRR Aug 2026 | 4,488,941.40 | 4,488,941.40 | 0 | ✅ |
| MRR Oct 2026 | 4,671,314.10 | 4,671,314.10 | 0 | ✅ |

**Confidence: High** for the August explanation (data reconciled to two external anchors, timing + segment + size consistent, alternatives rejected). **Medium** for the net price effect (3 post-period months, wide interval).
