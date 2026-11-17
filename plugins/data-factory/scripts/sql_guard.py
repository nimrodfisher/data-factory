#!/usr/bin/env python3
"""Data Factory safety interlock (Claude Code PreToolUse hook for Bash).

Blocks destructive SQL and production writes issued through SQL clients:
  - DROP / TRUNCATE / ALTER ... DROP
  - DELETE or UPDATE without a WHERE clause
  - any write statement that targets the prod schema named in .data-factory/factory.yaml
  - dbt / sqlmesh commands aimed at a prod target

Exit 0 = allow, exit 2 = block (stderr is shown to the agent).
Humans can bypass for a session with DATA_FACTORY_ALLOW_DESTRUCTIVE=1 in the
environment that launches Claude Code. Agents cannot set it from inside a command.
"""
import json
import os
import re
import sys

SQL_CLIENTS = re.compile(
    r"\b(duckdb|psql|snowsql|snow\s+sql|bq|databricks|dbt|sqlmesh|sqlite3|mysql|clickhouse(-client)?|"
    r"trino|presto|spark-sql|beeline|redshift|q\.py|sqlcmd)\b",
    re.I,
)
WRITE_VERBS = r"(insert\s+into|create\s+(or\s+replace\s+)?(table|view|schema)|merge\s+into|update|delete\s+from|drop|alter|truncate)"


def prod_schema(cwd: str):
    path = os.path.join(cwd or ".", ".data-factory", "factory.yaml")
    try:
        with open(path) as f:
            m = re.search(r"^\s*prod:\s*([\w.\-]+)", f.read(), re.M)
            return m.group(1) if m else None
    except OSError:
        return None


def statements(sql: str):
    return [s.strip() for s in re.split(r";", sql) if s.strip()]


def check(command: str, cwd: str = "."):
    """Return a reason string if the command must be blocked, else None."""
    if not SQL_CLIENTS.search(command):
        return None
    low = command.lower()

    if re.search(r"\b(dbt|sqlmesh)\b", low) and re.search(r"(--target|-t)[\s=]+prod\w*\b|\bplan\s+prod\b", low):
        return "dbt/sqlmesh command aimed at a prod target. Agents work in dev; shipping to prod is a human-approved PR."

    for stmt in statements(low):
        if re.search(r"\bdrop\s+(table|schema|database|view|materialized\s+view)\b", stmt):
            return f"DROP statement: `{stmt[:80]}`"
        if re.search(r"\btruncate\b", stmt):
            return f"TRUNCATE statement: `{stmt[:80]}`"
        if re.search(r"\balter\s+table\b.*\bdrop\b", stmt):
            return f"ALTER ... DROP statement: `{stmt[:80]}`"
        if re.search(r"\bdelete\s+from\b", stmt) and not re.search(r"\bwhere\b", stmt):
            return f"DELETE without WHERE: `{stmt[:80]}`"
        if re.search(r"\bupdate\s+[\w.\"`]+\s+set\b", stmt) and not re.search(r"\bwhere\b", stmt):
            return f"UPDATE without WHERE: `{stmt[:80]}`"

    prod = prod_schema(cwd)
    if prod:
        p = re.escape(prod.lower())
        for stmt in statements(low):
            if re.search(rf"\b{WRITE_VERBS}\b", stmt) and re.search(rf"(?<![\w]){p}\.", stmt):
                return f"write statement touching the protected prod schema `{prod}`: `{stmt[:80]}`"
    return None


def main():
    if os.environ.get("DATA_FACTORY_ALLOW_DESTRUCTIVE") == "1":
        sys.exit(0)
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)
    command = (payload.get("tool_input") or {}).get("command", "")
    reason = check(command, payload.get("cwd", "."))
    if reason:
        print(
            f"🛑 Data Factory safety interlock blocked this command — {reason}\n"
            "Rewrite it to run in the dev environment with a bounded WHERE clause, "
            "or ask the human to run it themselves.",
            file=sys.stderr,
        )
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
