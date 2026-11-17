"""Data-scientist station — price-change impact (difference-in-differences) and MRR forecast.

Work order 03. Inputs: fct_mrr_monthly, int_mrr__account_months (dev). Seeded, deterministic.
1. DiD on monthly logo churn: treated = SMB Starter monthly (re-priced), control = SMB Growth monthly (not re-priced).
2. Net impact of the price change at Oct-2026 run-rate: re-pricing uplift vs MRR lost to excess churn.
3. Component forecast of MRR for Nov-Dec 2026 with scenarios, backtested against naive & drift baselines.
"""
import json
import os

import numpy as np
import pandas as pd

RNG = np.random.default_rng(7)
PRE_END, POST = pd.Timestamp("2026-07-31"), ["2026-08-31", "2026-09-30", "2026-10-31"]
OLD_PRICE, NEW_PRICE = 29, 35


def did(con):
    rates = con.execute(open(os.path.join(os.path.dirname(__file__), "..", "analyses", "03_logo_churn_rates.sql")).read()).df()
    rates["month_end"] = pd.to_datetime(rates["month_end"])
    p = rates.pivot(index="month_end", columns="grp", values="logo_churn_rate")
    t, c = p["SMB Starter · monthly"], p["SMB Growth · monthly"]
    gap = t - c
    pre, post = gap[gap.index <= PRE_END], gap[gap.index > PRE_END]
    effect_by_month = post - pre.mean()
    boots = [RNG.choice(post.values, len(post)).mean() - RNG.choice(pre.values, len(pre)).mean() for _ in range(5000)]
    slope = np.polyfit(np.arange(len(pre)), pre.values, 1)[0]
    return dict(
        effect_by_month={str(k.date()): float(v) for k, v in effect_by_month.items()},
        avg_effect=float(effect_by_month.mean()),
        ci95=[float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))],
        pre_trend_slope_per_month=float(slope),
        treated_pre=float(t[t.index <= PRE_END].mean()), control_pre=float(c[c.index <= PRE_END].mean()),
        treated_post={str(k.date()): float(v) for k, v in t[t.index > PRE_END].items()},
        control_post={str(k.date()): float(v) for k, v in c[c.index > PRE_END].items()},
        series=dict(months=[str(d.date()) for d in p.index], treated=t.round(4).tolist(), control=c.round(4).tolist()),
    )


def net_impact(con, effect_by_month):
    # Starter-monthly MRR at the start of each post month (prior month-end)
    start_mrr = con.execute("""
        select last_day(month_end + interval 1 day)::date as month_end, sum(mrr) as mrr
        from fct_mrr_monthly f
        where segment = 'SMB' and plan = 'Starter' and billing_period = 'month' and mrr > 0
        group by 1""").df()
    start_mrr["month_end"] = start_mrr["month_end"].astype(str)
    start = dict(zip(start_mrr.month_end, start_mrr.mrr))
    lost = {m: effect_by_month[m] * start[m] for m in POST}
    uplift = con.execute(f"""
        select sum(m.seats * ({NEW_PRICE} - {OLD_PRICE})) as uplift, count(*) as accounts
        from int_mrr__account_months m join stg_billing__accounts a using (account_id)
        where m.month_end = date '2026-10-31' and m.plan = 'Starter' and m.billing_period = 'month'
          and a.signup_date < date '2026-08-01'""").fetchone()
    lost_total = sum(lost.values())
    return dict(excess_churned_mrr_by_month=lost, excess_churned_mrr=lost_total,
                repricing_uplift_mrr=float(uplift[0]), repriced_accounts=int(uplift[1]),
                net_run_rate_mrr=float(uplift[0] - lost_total),
                oct_excess_churn_mrr=lost["2026-10-31"])


def components(con):
    b = con.execute(open(os.path.join(os.path.dirname(__file__), "..", "analyses", "01_mrr_bridge.sql")).read()).df()
    b["month_end"] = pd.to_datetime(b["month_end"])
    b = b.set_index("month_end").fillna(0)
    b["prev"] = b["mrr"].shift(1)
    return b.iloc[1:]


def component_step(mrr, new, exp_rate, con_rate, churn_rate):
    return mrr + new + mrr * (exp_rate - con_rate - churn_rate)


def backtest(b):
    errs = {"naive": [], "drift": [], "component": []}
    idx = list(b.index)
    for i in range(6, len(idx) - 2):
        origin = idx[i]
        if origin > pd.Timestamp("2026-05-31"):
            break
        hist = b.iloc[i - 5:i + 1]
        mrr0 = b.loc[origin, "mrr"]
        r = dict(new=hist.new_mrr.mean(), exp=(hist.expansion_mrr / hist.prev).mean(),
                 con=(-hist.contraction_mrr / hist.prev).mean(), churn=(-hist.churned_mrr / hist.prev).mean())
        comp = mrr0
        for h in (1, 2):
            actual = b.iloc[i + h]["mrr"]
            comp = component_step(comp, r["new"], r["exp"], r["con"], r["churn"])
            errs["naive"].append(abs(actual - mrr0))
            errs["drift"].append(abs(actual - (mrr0 + h * hist.net_change.mean())))
            errs["component"].append(abs(actual - comp))
    return {k: float(np.mean(v)) for k, v in errs.items()}, float(np.std(errs["component"]))


def forecast(con, b, sigma):
    pre = b[(b.index > PRE_END - pd.DateOffset(months=6)) & (b.index <= PRE_END)]
    new = b[b.index > pd.Timestamp("2026-04-30")].new_mrr.mean()          # last 6 months incl. new price
    exp_rate = (pre.expansion_mrr / pre.prev).mean()                       # excludes the Sep re-price one-off
    con_rate = (-pre.contraction_mrr / pre.prev).mean()
    # churn split: Starter-monthly (scenario-driven) vs everything else (pre-change rate)
    sm = con.execute("""
        select month_end, -sum(mrr_change) filter (where movement = 'churn') as churned, sum(prev_mrr) as start_mrr
        from fct_mrr_monthly where segment = 'SMB' and coalesce(prev_plan, plan) = 'Starter' and billing_period = 'month'
        group by 1 order by 1""").df()
    sm["month_end"] = pd.to_datetime(sm["month_end"])
    sm = sm.set_index("month_end")
    other_churn = ((-pre.churned_mrr - sm.loc[pre.index, "churned"]) / (pre.prev - sm.loc[pre.index, "start_mrr"])).mean()
    starter_share = float(con.execute("""select sum(mrr) filter (where segment='SMB' and plan='Starter' and billing_period='month') / sum(mrr)
        from fct_mrr_monthly where month_end = date '2026-10-31'""").fetchone()[0])
    scenarios = {"upside": [0.026, 0.026], "base": [0.040, 0.033], "downside": [0.049, 0.049]}
    out = {}
    for name, starter_rates in scenarios.items():
        mrr, path = float(b["mrr"].iloc[-1]), []
        for rate in starter_rates:
            churn = starter_share * rate + (1 - starter_share) * other_churn
            mrr = component_step(mrr, new, exp_rate, con_rate, churn)
            path.append(mrr)
        out[name] = path
    band = [[out["base"][h] - 1.28 * sigma * np.sqrt(h + 1), out["base"][h] + 1.28 * sigma * np.sqrt(h + 1)] for h in range(2)]
    return dict(months=["2026-11-30", "2026-12-31"], scenarios=out, base_80pct=band,
                assumptions=dict(new_mrr_per_month=new, expansion_rate=exp_rate, contraction_rate=con_rate,
                                 non_starter_churn_rate=other_churn, starter_monthly_share=starter_share,
                                 starter_churn_scenarios=scenarios))


def run(con, out_dir):
    d = did(con)
    impact = net_impact(con, d["effect_by_month"])
    b = components(con)
    mae, sigma = backtest(b)
    fc = forecast(con, b, sigma)
    jul, aug = float(b.loc["2026-07-31", "mrr"]), float(b.loc["2026-08-31", "mrr"])
    headline = dict(mrr_jul=jul, mrr_aug=aug, aug_change=aug - jul, aug_change_pct=(aug - jul) / jul,
                    mrr_oct=float(b["mrr"].iloc[-1]))
    res = dict(did=d, impact=impact, backtest_mae=mae, forecast=fc, headline=headline)
    with open(os.path.join(out_dir, "ds_results.json"), "w") as f:
        json.dump(res, f, indent=2, default=float)
    print(f"  DiD    excess Starter-monthly churn {d['avg_effect']:+.1%}/mo (95% CI {d['ci95'][0]:+.1%} to {d['ci95'][1]:+.1%})")
    print(f"  impact uplift ${impact['repricing_uplift_mrr']:,.0f}/mo vs lost ${impact['excess_churned_mrr']:,.0f}/mo -> net ${impact['net_run_rate_mrr']:,.0f}/mo")
    print(f"  backtest MAE  naive ${mae['naive']:,.0f} · drift ${mae['drift']:,.0f} · component ${mae['component']:,.0f}")
    print(f"  forecast Dec base ${fc['scenarios']['base'][1]:,.0f} (down ${fc['scenarios']['downside'][1]:,.0f} / up ${fc['scenarios']['upside'][1]:,.0f})")
    return res
