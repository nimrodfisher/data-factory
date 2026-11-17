"""Tiny query runner for the demo: python3 q.py "select ..."  |  python3 q.py -f path.sql
Runs against saas.duckdb (schemas: raw = source data, dev = where the factory builds)."""
import os
import sys

import duckdb

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saas.duckdb")
sql = open(sys.argv[2]).read() if sys.argv[1:2] == ["-f"] else " ".join(sys.argv[1:])
if not sql.strip():
    sys.exit(__doc__)
con = duckdb.connect(DB)
con.execute("create schema if not exists dev")
for stmt in [s for s in sql.split(";") if s.strip()][:-1]:
    con.execute(stmt)
res = con.execute([s for s in sql.split(";") if s.strip()][-1])
if res.description:
    df = res.df()
    print(df.head(200).to_string(index=False))
    if len(df) > 200:
        print(f"... {len(df):,} rows total")
else:
    print("OK")
