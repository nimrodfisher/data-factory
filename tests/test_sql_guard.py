"""Tests for the safety interlock. Run: python3 -m pytest tests/ (or python3 tests/test_sql_guard.py)."""
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARD = os.path.join(ROOT, "plugins", "data-factory", "scripts", "sql_guard.py")
sys.path.insert(0, os.path.dirname(GUARD))
from sql_guard import check  # noqa: E402

BLOCK = [
    'duckdb dev.duckdb -c "drop table customers"',
    'psql $DB -c "TRUNCATE orders"',
    'snowsql -q "delete from analytics.orders"',
    'bq query "UPDATE ds.users SET active = false"',
    'psql -c "alter table t drop column x"',
    "dbt run --target prod",
    "dbt build -t prod --select fct_orders",
]
ALLOW = [
    'duckdb dev.duckdb -c "select count(*) from customers"',
    'psql -c "delete from dev.tmp where run_id = 7"',
    'bq query "UPDATE dev.users SET active = false WHERE id = 1"',
    "dbt run --target dev --select stg_orders",
    'git commit -m "drop table support in docs"',  # not a SQL client
    "ls -la",
]


def test_blocks():
    for cmd in BLOCK:
        assert check(cmd), f"should block: {cmd}"


def test_allows():
    for cmd in ALLOW:
        assert check(cmd) is None, f"should allow: {cmd}"


def test_prod_schema_from_config():
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, ".data-factory"))
        with open(os.path.join(d, ".data-factory", "factory.yaml"), "w") as f:
            f.write("environments:\n  dev: analytics_dev\n  prod: analytics\n")
        assert check('psql -c "insert into analytics.orders select * from x"', d)
        assert check('psql -c "insert into analytics_dev.orders select * from x"', d) is None
        assert check('psql -c "select * from analytics.orders"', d) is None


def test_hook_exit_codes():
    def run(cmd):
        p = subprocess.run([sys.executable, GUARD], input=json.dumps({"tool_input": {"command": cmd}}),
                           capture_output=True, text=True)
        return p.returncode
    assert run('duckdb x.db -c "drop table a"') == 2
    assert run('duckdb x.db -c "select 1"') == 0


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
