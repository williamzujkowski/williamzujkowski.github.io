#!/usr/bin/env python3
"""Exercise PostgreSQL authorization in a disposable, network-isolated container.

Requires Python 3.11+ and Docker. Prints JSON; exits nonzero on any mismatch.
Does not install an MCP server or connect to any existing database.
"""

from __future__ import annotations

import json
import os
import secrets
import subprocess
import time
import uuid
from datetime import UTC, datetime
from pathlib import Path

IMAGE = "postgres@sha256:d3e1620b530c944afa6e887d22eb899824da68e19c52024bf98f5220c88a65b2"


def main() -> None:
    name = f"postgres-readonly-lab-{uuid.uuid4().hex[:12]}"
    results = []

    def docker(*args: str, **kwargs) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["docker", *args], text=True, capture_output=True, timeout=120, **kwargs
        )

    def sql(query: str, role: str = "agent_reader") -> subprocess.CompletedProcess:
        return docker(
            "exec", "-i", "--user", "postgres", name,
            "psql", "-X", "-qAt", "-v", "ON_ERROR_STOP=1",
            "-v", "VERBOSITY=verbose", "-U", role, "-d", "lab", input=query,
        )

    def admin(query: str) -> str:
        result = sql(query, "postgres")
        if result.returncode:
            raise RuntimeError(result.stderr)
        return result.stdout.strip()

    def check(label: str, query: str, expected: str, error: bool = False) -> None:
        result = sql(query)
        observed = result.stderr.strip() if error else result.stdout.strip()
        passed = (result.returncode != 0 if error else result.returncode == 0)
        passed = passed and (f"{expected}:" in observed if error else observed == expected)
        results.append({"test": label, "sql": query, "expected": expected,
                        "observed": observed, "passed": passed})
        if not passed:
            raise RuntimeError(f"{label}: {result.stdout} {result.stderr}")

    started = datetime.now(UTC).isoformat()
    report = {"started_utc": started, "image": IMAGE, "tests": results}
    try:
        launch = docker(
            "run", "-d", "--rm", "--name", name, "--network", "none",
            "--user", "postgres", "--memory", "512m", "--cpus", "1", "--pids-limit", "128",
            "--tmpfs", "/var/lib/postgresql:rw,mode=1777",
            "-e", "POSTGRES_PASSWORD", "-e", "POSTGRES_DB=lab", IMAGE,
            env={**os.environ, "POSTGRES_PASSWORD": secrets.token_urlsafe(32)},
        )
        if launch.returncode:
            raise RuntimeError(launch.stderr)
        for _ in range(60):
            ready = sql("SELECT 1;", "postgres")
            if ready.returncode == 0:
                break
            time.sleep(0.5)
        else:
            raise RuntimeError("Database did not become ready")
        report["server_version"] = admin("SHOW server_version;")
        report["platform"] = docker("image", "inspect", IMAGE, "--format",
                                    "{{.Os}}/{{.Architecture}}").stdout.strip()
        admin(Path(__file__).with_name("setup.sql").read_text())
        check("session identity", "SELECT session_user, current_user;", "agent_reader|agent_reader")
        check("minimal role attributes", "SELECT rolsuper, rolcreatedb, rolcreaterole, "
              "rolreplication, rolbypassrls FROM pg_roles WHERE rolname = current_user;", "f|f|f|f|f")
        check("effective grants", "SELECT has_database_privilege(current_user, 'lab', 'CONNECT'), "
              "has_database_privilege(current_user, 'lab', 'CREATE'), "
              "has_database_privilege(current_user, 'lab', 'TEMP'), "
              "has_schema_privilege(current_user, 'inventory', 'USAGE'), "
              "has_schema_privilege(current_user, 'inventory', 'CREATE'), "
              "has_schema_privilege(current_user, 'public', 'CREATE'), "
              "has_table_privilege(current_user, 'inventory.hosts', 'SELECT'), "
              "has_table_privilege(current_user, 'inventory.hosts', 'UPDATE'), "
              "has_sequence_privilege(current_user, 'inventory.ticket_number', 'USAGE'), "
              "has_function_privilege(current_user, 'inventory.rename_host()', 'EXECUTE');",
              "t|f|f|t|f|f|t|f|f|f")
        check("allowed SELECT", "SELECT id, name FROM inventory.hosts ORDER BY id;", "1|lab-router\n2|lab-nas")
        check("read-only default", "SHOW default_transaction_read_only;", "on")
        check("default blocks UPDATE", "UPDATE inventory.hosts SET name = 'changed' WHERE id = 1;", "25006", True)
        check("role can request read-write", "BEGIN READ WRITE; SHOW transaction_read_only; ROLLBACK;", "off")
        denied = {
            "INSERT": "INSERT INTO inventory.hosts VALUES (3, 'extra')",
            "UPDATE": "UPDATE inventory.hosts SET name = 'changed' WHERE id = 1",
            "DELETE": "DELETE FROM inventory.hosts WHERE id = 1",
            "TRUNCATE": "TRUNCATE inventory.hosts",
            "ALTER": "ALTER TABLE inventory.hosts ADD COLUMN extra text",
            "DROP": "DROP TABLE inventory.hosts",
            "schema CREATE": "CREATE TABLE inventory.extra (id integer)",
            "public CREATE": "CREATE TABLE public.extra (id integer)",
            "temporary CREATE": "CREATE TEMP TABLE extra (id integer)",
            "sequence nextval": "SELECT nextval('inventory.ticket_number')",
            "ungranted table SELECT": "SELECT * FROM inventory.private_notes",
            "owner role switch": "SET ROLE lab_owner",
            "definer function": "SELECT inventory.rename_host()",
        }
        for label, statement in denied.items():
            check(f"denied {label} in read-write transaction",
                  f"BEGIN READ WRITE; {statement}; ROLLBACK;", "42501", True)
        admin("SET ROLE lab_owner; CREATE TABLE inventory.future_data (id integer);")
        check("future table denied", "SELECT * FROM inventory.future_data;", "42501", True)
        # Positive control: deliberately grant a dangerous function, observe
        # mutation, then roll it back and remove that capability immediately.
        admin("GRANT EXECUTE ON FUNCTION inventory.rename_host() TO agent_reader;")
        check("granted definer function can write", "BEGIN READ WRITE; SELECT inventory.rename_host(); "
              "SELECT name FROM inventory.hosts WHERE id = 1; ROLLBACK;",
              "changed-by-function\nchanged-by-function")
        admin("REVOKE EXECUTE ON FUNCTION inventory.rename_host() FROM agent_reader;")
        check("revoked definer function denied", "BEGIN READ WRITE; SELECT inventory.rename_host(); ROLLBACK;", "42501", True)
        check("original rows preserved", "SELECT id, name FROM inventory.hosts ORDER BY id;", "1|lab-router\n2|lab-nas")
        report["passed"] = all(item["passed"] for item in results)
    except Exception as error:
        report["passed"] = False
        report["error"] = str(error)
    finally:
        # Only the uniquely named container created by this invocation is removed.
        removed = docker("rm", "-f", "-v", name)
        report["container_removed"] = removed.returncode == 0
        print(json.dumps(report, indent=2))
    if not report["passed"] or not report["container_removed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
