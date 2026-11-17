"""Generate the Data Factory demo dataset: a small B2B SaaS billing system in DuckDB.

    pip install duckdb pandas numpy
    python generate_data.py            # -> saas.duckdb (schema: raw)

The data hides a real story and two classic traps — the factory should find the
story and its Quality Inspector should catch the traps. No spoilers here; see
../examples/mrr-drop/ for a reference run.
"""
import datetime as dt
import os
import sys

import duckdb
import numpy as np
import pandas as pd

SEED = 42
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saas.duckdb")
START, END = pd.Period("2025-01", "M"), pd.Period("2026-10", "M")
ANNOUNCED = dt.date(2026, 7, 15)          # price change e-mail sent
NEW_PRICE_FOR_NEW = pd.Period("2026-08", "M")   # new sign-ups pay the new price
REPRICE_EXISTING = pd.Period("2026-09", "M")    # existing monthly Starter re-priced on Sep 1
SEAT_PRICE = {"Starter": 29, "Growth": 45, "Scale": 79}
STARTER_NEW = 35
ANNUAL_DISCOUNT = 0.9
SEATS = {("SMB", "Starter"): (3, 31), ("SMB", "Growth"): (5, 41), ("Mid-Market", "Growth"): (30, 151),
         ("Mid-Market", "Scale"): (30, 151), ("Enterprise", "Scale"): (150, 501)}

rng = np.random.default_rng(SEED)
ADJ = ["Blue", "North", "Bright", "Swift", "Prime", "Clear", "Nova", "Peak", "Silver", "Urban", "Deep", "Open"]
NOUN = ["Labs", "Works", "Analytics", "Systems", "Health", "Logistics", "Media", "Retail", "Cloud", "Foods", "Energy", "Studio"]


def rand_day(period: pd.Period) -> dt.date:
    return (period.start_time + pd.Timedelta(days=int(rng.integers(0, period.days_in_month)))).date()


def churn_hazard(segment, plan, billing, period):
    base = {"SMB": 0.025, "Mid-Market": 0.01, "Enterprise": 0.004}[segment]
    if segment == "SMB" and plan == "Growth":
        base = 0.02
    if billing == "year":
        return base / 3                       # annual contracts rarely churn mid-term
    if plan == "Starter":                     # reaction to the announced price increase
        return {"2026-08": 0.13, "2026-09": 0.07, "2026-10": 0.045}.get(str(period), base)
    return base


def pick_plan(segment):
    if segment == "SMB":
        return "Starter" if rng.random() < 0.72 else "Growth"
    if segment == "Mid-Market":
        return "Growth" if rng.random() < 0.7 else "Scale"
    return "Scale"


def main():
    accounts, subs = [], []
    state = {}
    seq = {"sub": 0, "acc": 0}

    def open_sub(acc, plan, seats, billing, start, seat_price=None):
        seq["sub"] += 1
        monthly = (seat_price or SEAT_PRICE[plan]) * seats
        amount = round(monthly * 12 * ANNUAL_DISCOUNT, 2) if billing == "year" else float(monthly)
        subs.append(dict(subscription_id=f"S{seq['sub']:06d}", account_id=acc, plan=plan, seats=seats,
                         billing_period=billing, amount=amount, started_at=start, ended_at=None))
        return len(subs) - 1

    def new_account(segment, signup, period=None, is_test=False, name=None, plan=None, seats=None, billing=None):
        seq["acc"] += 1
        acc = f"A{seq['acc']:05d}"
        plan = plan or pick_plan(segment)
        seats = seats or int(rng.integers(*SEATS[(segment, plan)]))
        billing = billing or ("year" if rng.random() < 0.25 else "month")
        price = STARTER_NEW if (plan == "Starter" and period is not None and period >= NEW_PRICE_FOR_NEW) else None
        accounts.append(dict(account_id=acc, account_name=name or f"{rng.choice(ADJ)} {rng.choice(NOUN)}",
                             segment=segment, region=str(rng.choice(["NA", "EMEA", "APAC"], p=[.5, .35, .15])),
                             signup_date=signup, is_test=is_test))
        state[acc] = dict(sub=open_sub(acc, plan, seats, billing, signup, price), active=True, signup=signup,
                          segment=segment, is_test=is_test)

    # existing customer base on 2025-01-01 (customers since 2022)
    for segment, n in (("SMB", 2600), ("Mid-Market", 260), ("Enterprise", 22)):
        for _ in range(n):
            new_account(segment, rand_day(pd.Period(f"{rng.integers(2022, 2025)}-{rng.integers(1, 13):02d}", "M")))

    for i, period in enumerate(pd.period_range(START, END, freq="M")):
        # 1. re-price existing monthly Starter subscriptions on Sep 1
        if period == REPRICE_EXISTING:
            for acc, s in state.items():
                cur = subs[s["sub"]]
                if s["active"] and cur["plan"] == "Starter" and cur["billing_period"] == "month" and cur["amount"] < STARTER_NEW * cur["seats"]:
                    cur["ended_at"] = period.start_time.date()
                    s["sub"] = open_sub(acc, "Starter", cur["seats"], "month", period.start_time.date(), STARTER_NEW)

        # 2. lifecycle events for accounts active at the start of the month
        for acc, s in list(state.items()):
            if not s["active"] or s["signup"] >= period.start_time.date():
                continue
            cur = subs[s["sub"]]
            if s["is_test"]:
                if period == pd.Period("2026-08", "M") and accounts[[a["account_id"] for a in accounts].index(acc)]["account_name"] != "ACME Test Co":
                    cur["ended_at"] = dt.date(2026, 8, 12)        # QA clean-up of internal accounts
                    s["active"] = False
                continue
            day = rand_day(period)
            seat_price = cur["amount"] / cur["seats"] if cur["billing_period"] == "month" else None
            r = rng.random()
            if r < churn_hazard(s["segment"], cur["plan"], cur["billing_period"], period):
                cur["ended_at"] = day
                s["active"] = False
            elif r < churn_hazard(s["segment"], cur["plan"], cur["billing_period"], period) + 0.018:
                cur["ended_at"] = day
                if cur["plan"] == "Starter" and cur["seats"] >= 20 and rng.random() < 0.3:
                    s["sub"] = open_sub(acc, "Growth", cur["seats"], cur["billing_period"], day)
                else:
                    add = max(1, int(cur["seats"] * rng.uniform(0.1, 0.25)))
                    s["sub"] = open_sub(acc, cur["plan"], cur["seats"] + add, cur["billing_period"], day, seat_price)
            elif r > 0.994 and cur["seats"] > 3:
                cur["ended_at"] = day
                cut = max(1, int(cur["seats"] * 0.15))
                s["sub"] = open_sub(acc, cur["plan"], cur["seats"] - cut, cur["billing_period"], day, seat_price)

        # 3. new sign-ups
        g = 1 + 0.01 * i
        for segment, lam in (("SMB", 95 * g), ("Mid-Market", 4.5 * g), ("Enterprise", 0.35)):
            for _ in range(rng.poisson(lam)):
                new_account(segment, rand_day(period), period)

        # 4. internal QA accounts created in May 2026 — they look like Enterprise customers
        if period == pd.Period("2026-05", "M"):
            for name in ("Internal Demo Account", "QA Sandbox Corp", "ACME Test Co"):
                new_account("Enterprise", dt.date(2026, 5, 4), period, is_test=True, name=name,
                            plan="Scale", seats=300, billing="month")

    # invoices: one per billing cycle while the subscription is active
    cutoff = dt.date(2026, 10, 31)
    invoices, inv_seq = [], 0
    for s in subs:
        step = 12 if s["billing_period"] == "year" else 1
        d, k = s["started_at"], 0
        while d < dt.date(2025, 1, 1):          # connector history starts 2025-01-01
            k += step
            d = (pd.Timestamp(s["started_at"]) + pd.DateOffset(months=k)).date()
        while d <= cutoff and (s["ended_at"] is None or d < s["ended_at"]):
            inv_seq += 1
            loaded = dt.datetime.combine(d, dt.time(1, 0)) + dt.timedelta(minutes=int(rng.integers(0, 600)))
            invoices.append(dict(invoice_id=f"INV{inv_seq:07d}", account_id=s["account_id"],
                                 subscription_id=s["subscription_id"], invoice_date=d, amount_usd=s["amount"],
                                 status="void" if rng.random() < 0.02 else "paid", _loaded_at=loaded))
            k += step
            d = (pd.Timestamp(s["started_at"]) + pd.DateOffset(months=k)).date()

    inv = pd.DataFrame(invoices)
    # connector re-sync on 2026-09-03 re-delivered part of August
    aug = inv[(inv.invoice_date >= dt.date(2026, 8, 1)) & (inv.invoice_date <= dt.date(2026, 8, 31))]
    dup = aug.sample(frac=0.4, random_state=SEED).copy()
    dup["_loaded_at"] = pd.Timestamp("2026-09-03 02:14:00")
    inv = pd.concat([inv, dup]).sort_values(["invoice_date", "invoice_id"]).reset_index(drop=True)

    acc_df = pd.DataFrame(accounts)
    acc_df["_loaded_at"] = pd.Timestamp("2026-11-01 01:00:00")
    sub_df = pd.DataFrame(subs)
    sub_df["_loaded_at"] = pd.Timestamp("2026-11-01 01:00:00")

    if os.path.exists(OUT):
        os.remove(OUT)
    con = duckdb.connect(OUT)
    con.execute("create schema raw")
    for name, df in (("accounts", acc_df), ("subscriptions", sub_df), ("invoices", inv)):
        con.register("df", df)
        con.execute(f"create table raw.{name} as select * from df")
        con.unregister("df")
    counts = {t: con.execute(f"select count(*) from raw.{t}").fetchone()[0] for t in ("accounts", "subscriptions", "invoices")}
    con.close()
    print(f"✅ wrote {OUT}")
    for t, c in counts.items():
        print(f"   raw.{t:<14} {c:>7,} rows")


if __name__ == "__main__":
    sys.exit(main())
