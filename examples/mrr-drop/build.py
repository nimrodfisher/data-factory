"""Rebuild the reference run end to end from the demo data.

    python ../../demo/generate_data.py      # once
    python build.py                          # models -> tests -> analyses -> DS -> dashboard

Reads demo/saas.duckdb read-only; everything is built in memory (the "dev" environment),
so the demo database stays clean for your own factory run.
"""
import glob
import json
import os
import sys

import duckdb

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "..", "..", "demo", "saas.duckdb")
OUT = os.path.join(HERE, "outputs")


def connect():
    if not os.path.exists(DB):
        sys.exit("demo/saas.duckdb not found — run: python demo/generate_data.py")
    con = duckdb.connect()
    con.execute(f"attach '{DB}' as src (read_only)")
    con.execute("create schema raw")
    for t in ("accounts", "subscriptions", "invoices"):
        con.execute(f"create view raw.{t} as select * from src.raw.{t}")
    return con


def build_models(con):
    for path in sorted(glob.glob(os.path.join(HERE, "models", "*.sql"))):
        name = os.path.basename(path)[3:-4]
        kind = "table" if name.startswith("fct_") else "view"
        con.execute(f"create or replace {kind} {name} as {open(path).read()}")
        n = con.execute(f"select count(*) from {name}").fetchone()[0]
        print(f"  model  {name:<32} {kind:<5} {n:>8,} rows")


def run_tests(con):
    failed = 0
    for path in sorted(glob.glob(os.path.join(HERE, "tests", "*.sql"))):
        rows = con.execute(open(path).read()).fetchall()
        ok = len(rows) == 0
        failed += not ok
        print(f"  test   {os.path.basename(path)[:-4]:<32} {'PASS' if ok else f'FAIL ({len(rows)} rows)'}")
    if failed:
        sys.exit(f"{failed} test(s) failed")


def run_analyses(con):
    results = {}
    for path in sorted(glob.glob(os.path.join(HERE, "analyses", "*.sql"))):
        name = os.path.basename(path)[:-4]
        df = con.execute(open(path).read()).df()
        df.to_csv(os.path.join(OUT, f"{name}.csv"), index=False)
        results[name] = df
        print(f"  query  {name:<32} -> outputs/{name}.csv")
    return results


def main():
    os.makedirs(OUT, exist_ok=True)
    con = connect()
    print("▶ data-engineer: models")
    build_models(con)
    print("▶ data-engineer: tests")
    run_tests(con)
    print("▶ data-analyst: analyses")
    results = run_analyses(con)
    print("▶ data-scientist: impact + forecast")
    sys.path.insert(0, os.path.join(HERE, "notebooks"))
    from price_change_impact import run as ds_run
    ds = ds_run(con, OUT)
    print("▶ bi-engineer: dashboard")
    sys.path.insert(0, os.path.join(HERE, "dashboards"))
    from build_dashboard import build
    path = build(con, results, ds, os.path.join(HERE, "dashboards", "mrr_dashboard.html"))
    print(f"  wrote  {os.path.relpath(path, HERE)}")
    with open(os.path.join(OUT, "headline.json"), "w") as f:
        json.dump(ds["headline"], f, indent=2, default=float)
    print("✅ done")


if __name__ == "__main__":
    main()
