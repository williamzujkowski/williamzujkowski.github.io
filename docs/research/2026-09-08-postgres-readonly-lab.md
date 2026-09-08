# PostgreSQL authorization lab, September 8, 2026

Issue: #559. Status: executed successfully; companion post remains a draft.

The motivating primary source is [AWS bulletin 2026-101-AWS](https://aws.amazon.com/security/security-bulletins/2026-101-aws/),
published September 4. It identifies CVE-2026-85787 in
`awslabs.postgres-mcp-server` before 1.1.7, reports the fix in 1.1.7, and recommends
minimal PostgreSQL privileges. We tested the database authorization boundary
directly; this is neither an exploit reproduction nor verification of the MCP fix.
No vulnerable or patched MCP server was installed.

## Reproduction and observations

Run `python3 scripts/security-labs/postgres-readonly/run.py` from the repository root.
Complete source, setup SQL, operational limits and recorded JSON are in
[`scripts/security-labs/postgres-readonly/`](../../scripts/security-labs/postgres-readonly/).

- Actual start: 2026-09-08T11:55:08.494195+00:00.
- Docker daemon: 29.7.2. Container platform: linux/amd64.
- Database reports PostgreSQL 18.6.
- Image: `postgres@sha256:d3e1620b530c944afa6e887d22eb899824da68e19c52024bf98f5220c88a65b2`.
- Image initially resolved from official `postgres:18-alpine`; the runner pins its
  immutable digest. Local reported image size: 303,696,065 bytes.
- Container: unprivileged PostgreSQL OS user, network disabled, no host mounts or
  ports, tmpfs data, 512 MB memory cap, one CPU, 128-process limit.
- Outcome: 24/24 checks passed, including 15 expected SQLSTATE 42501 permission
  denials. Container and its anonymous volumes removed; image retained in cache.

Effective grants were checked through `has_*_privilege` functions: CONNECT true;
database CREATE/TEMP false; inventory USAGE true and CREATE false; public CREATE
false; hosts SELECT true and UPDATE false; sequence USAGE and function EXECUTE
false. Both session and current identity were `agent_reader`. Superuser, database
creation, role creation, replication and RLS-bypass attributes were all false.

Default transaction read-only was `on`; UPDATE failed with SQLSTATE 25006. The same
role successfully requested `BEGIN READ WRITE`, proving that this role default is
not an immutable authorization policy. Direct write/DDL requests then failed with
42501. So did schema creation, temporary tables, sequence advancement, an ungranted
table, a newly created table, switching to the owner and the restricted function.

Positive control: explicitly granting EXECUTE on an owner-powered function enabled
`SELECT inventory.rename_host()` to update a synthetic row inside a transaction.
The query returned the changed value, and a second SELECT observed it before
rollback. Revoking EXECUTE restored denial; the final SELECT showed the original
two rows. This prevents a misleading conclusion that table SELECT alone defines
everything a role can do.

## Source checks and limits

[PostgreSQL privileges](https://www.postgresql.org/docs/18/ddl-priv.html) documents
ownership and public defaults. [Schema documentation](https://www.postgresql.org/docs/18/ddl-schemas.html)
distinguishes fresh installations from upgraded databases' public-schema grants.
[CREATE FUNCTION](https://www.postgresql.org/docs/18/sql-createfunction.html) documents
SECURITY DEFINER, public execution and safe search paths. Our function fixes its
search path and schema-qualifies its table; its deliberate write capability is the
positive control, not a search-path exploit.

[ALTER DEFAULT PRIVILEGES](https://www.postgresql.org/docs/18/sql-alterdefaultprivileges.html)
applies to future objects of the creating role; the fixture changes that owner's
function defaults without automatically exposing future tables.
[SET TRANSACTION](https://www.postgresql.org/docs/18/sql-set-transaction.html) and
[client defaults](https://www.postgresql.org/docs/18/runtime-config-client.html)
support the distinction between transaction mode and object privileges.

This single-version, single-platform fixture does not assess RLS policies, column
redaction, inherited production grants, extension routines, database links, resource
exhaustion, metadata visibility, authentication, TLS or data exfiltration through
permitted SELECT results. Statement timeout is a convenience, not an evaluated DoS
defense. Raw observations are version-scoped and every denied statement is recorded.
