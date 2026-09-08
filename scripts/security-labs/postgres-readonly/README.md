# PostgreSQL read-only authorization lab

From the repository root, with Python 3.11+ and Docker available:

```sh
python3 scripts/security-labs/postgres-readonly/run.py > /tmp/postgres-readonly-results.json
```

The runner pulls the pinned official PostgreSQL image if absent (about 304 MB
uncompressed), starts a uniquely named container with no network, published ports,
or host mounts, initializes synthetic records, and checks actual SQL results and
SQLSTATE errors. PostgreSQL runs as the container's `postgres` OS user. Its data
directory uses tmpfs; memory is capped at 512 MB. The bootstrap password is generated
per invocation and never written to the report.

Connections use `docker exec` and the image's local Unix-socket authentication.
They establish `session_user = current_user = agent_reader`; they do **not** test
password authentication, TLS, an MCP transport, or application SQL validation.
No MCP server is installed. The bootstrap admin creates objects; all test SQL uses
the restricted role. Anyone controlling the Docker daemon can administer this
disposable database; that control is outside the tested boundary.

The runner removes only its own container and anonymous volumes in `finally`,
including after assertion failures. An uncatchable termination or Docker daemon
failure can require manual removal of its `postgres-readonly-lab-*` container.
The downloaded image remains cached. Exit status is zero only when every SQL
expectation passes and container removal succeeds. JSON contains every tested SQL
statement, expectation, observed output, version, platform, image digest, and result.

`setup.sql` is a complete **fresh database** fixture, not an existing-database
migration. It revokes public database privileges, denies schema creation, grants
SELECT on one explicit table, and removes public execution of owner-created
functions. It deliberately omits future-table grants. Review existing ownership,
memberships, defaults, extensions, views and routines separately before adapting it.

`results-2026-09-08.json` records the actual first successful run: PostgreSQL 18.6,
linux/amd64, 24 checks passed, 15 expected permission denials, container removed.
The positive control temporarily grants a SECURITY DEFINER routine, observes an
UPDATE through SELECT, rolls back the mutation, revokes execution, and checks denial.
The final check confirms that both original synthetic rows remain unchanged.

This is an author-time lab, not a CI or production deployment dependency.
