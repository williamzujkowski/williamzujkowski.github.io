---
title: "The Database Gets a Vote on Your Read-Only Agent"
date: 2026-09-08
description: "A disposable PostgreSQL lab tests what an agent-facing database role can actually do, including the SELECT that writes through a privileged function."
tags: [security, ai, homelab, databases]
author: William Zujkowski
draft: true
---

I built a disposable PostgreSQL lab with two pretend machines and a role that could read their names. Then I asked that role to do several things its job description did not require. PostgreSQL declined most of them. One carefully granted function made it considerably more accommodating.

The useful result was a set of measured permission boundaries: ordinary reads worked, direct writes failed, and a `SELECT` could still write when I handed it the right function. The word “read-only” had been doing several jobs without a particularly thorough interview.

The prompt for this experiment was [AWS's September 4 bulletin](https://aws.amazon.com/security/security-bulletins/2026-101-aws/) about CVE-2026-85787. AWS describes incomplete SQL input validation in `awslabs.postgres-mcp-server` before version 1.1.7 that could permit changes outside its intended read-only scope. The bulletin reports a fix in 1.1.7 and recommends connecting through a dedicated, minimally privileged PostgreSQL role.

This homelab experiment tests that database boundary directly. I did not install the affected MCP server, reproduce the vulnerability, or test its patch. There is no claim here that this website uses it.

## Give the reader something worth reading

The fixture creates `inventory.hosts` with two synthetic rows: `lab-router` and `lab-nas`. A separate, non-login owner creates the objects. The `agent_reader` login gets database `CONNECT`, schema `USAGE`, and `SELECT` on that one table. It has no superuser, role-creation, database-creation, replication or RLS-bypass attribute. Those checks, including the session identity, are in the [recorded results](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/main/scripts/security-labs/postgres-readonly/results-2026-09-08.json).

Ownership is deliberate. PostgreSQL gives owners authority that ordinary privilege revocation cannot remove, including the ability to grant their privileges back. An agent login that owns its tables is a poor starting point for this boundary. [PostgreSQL documents that distinction explicitly](https://www.postgresql.org/docs/18/ddl-priv.html).

<div class="flow" role="group" aria-label="The database evaluates SQL using the connecting role">
  <div class="flow-node"><b>SQL arrives</b><i>From a tool or this lab's psql client</i></div>
  <div class="flow-node is-gate"><b>PostgreSQL checks authority</b><i>Role, object privileges and invoked routines</i></div>
  <div class="flow-node"><b>Observe the outcome</b><i>Returned rows, permission error or permitted side effect</i></div>
</div>

The runner uses a digest-pinned official PostgreSQL image, no container networking, no published ports, no host mounts and an in-memory data directory. PostgreSQL runs as its container OS user. The [complete artifact](https://github.com/williamzujkowski/williamzujkowski.github.io/tree/main/scripts/security-labs/postgres-readonly) includes setup SQL, the assertions and cleanup. From a checkout with Python 3.11+ and Docker:

```sh
python3 scripts/security-labs/postgres-readonly/run.py > /tmp/postgres-readonly-results.json
```

My run used PostgreSQL **18.6 on linux/amd64**. All **24 checks** passed, including **15 expected permission denials**. The JSON records each SQL statement and its actual output. These are observations about this fixture, not a count of attacks defeated.

## A transaction default is changeable

The role starts with `default_transaction_read_only = on`. Its first attempted `UPDATE` failed with SQLSTATE `25006`, a read-only transaction error. Then the same role successfully ran `BEGIN READ WRITE`. PostgreSQL reported `transaction_read_only = off`.

That result matters when “force read-only at the role level” becomes an `ALTER ROLE ... SET` command in a configuration guide. The setting supplies a session default; my ordinary role could select a different transaction mode. PostgreSQL describes the [default setting](https://www.postgresql.org/docs/18/runtime-config-client.html) and [transaction modes](https://www.postgresql.org/docs/18/sql-set-transaction.html) separately from object privileges.

The remaining tests deliberately requested read-write transactions before issuing their SQL. This made the underlying permission checks visible. [The recorded run](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/main/scripts/security-labs/postgres-readonly/results-2026-09-08.json) showed:

| Request | Observed result |
| --- | --- |
| Read the two permitted hosts | Both rows returned |
| Insert, update, delete or truncate hosts | `42501`: insufficient privilege |
| Alter or drop the table | `42501` |
| Create a table in `inventory` or `public` | `42501` |
| Create a temporary table | `42501` |
| Advance the separate sequence | `42501` |
| Read an ungranted or subsequently created table | `42501` |
| Switch to the object-owner role | `42501` |

The transaction preference could change. The missing grants still mattered.

## The SELECT that changed a row

I added a positive control: an owner-created `SECURITY DEFINER` function that updates one host and returns its new name. Such functions run with their owner's privileges. PostgreSQL also grants function execution to `PUBLIC` by default unless that default is changed or the privilege revoked. Both behaviors deserve attention during a “read-only” review. [The function documentation covers both](https://www.postgresql.org/docs/18/sql-createfunction.html).

The fixture initially denied the reader permission to execute it. I then explicitly granted that permission and called the function inside a read-write transaction. `SELECT inventory.rename_host()` returned `changed-by-function`; a second query saw the changed row. I rolled back, revoked execution, and confirmed that the call failed again. The final read showed the original records. [Every step is captured in the results](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/main/scripts/security-labs/postgres-readonly/results-2026-09-08.json).

The function uses a fixed search path and a qualified table name. This is an intentionally granted capability, not a search-path trick. The reader still lacked direct `UPDATE` permission. Giving it an owner-powered routine supplied another route to that operation.

## Defaults have a past

The setup explicitly removes public database privileges, then grants back the reader's connection. It also revokes `CREATE` on `public`. Existing installations need their own inspection: PostgreSQL's schema documentation distinguishes fresh defaults from databases upgraded from older releases that can retain broader public-schema permissions. [Check the actual schema grants](https://www.postgresql.org/docs/18/ddl-schemas.html).

For functions created by `lab_owner`, the fixture changes the default to remove public execution. It does that while acting as the object creator. Default privileges affect that creator's future objects; they do not repair existing objects. I also leave future tables ungranted, so adding a new dataset requires an explicit access decision. [PostgreSQL's default-privilege rules explain why the creating role matters](https://www.postgresql.org/docs/18/sql-alterdefaultprivileges.html).

This is a fresh-database fixture, not a migration to paste into an established service. Existing memberships, ownership, routines, extensions and views can change the authority available to a login.

The lab also leaves plenty unmeasured. Its local socket connections do not test authentication or TLS. It does not evaluate row-level policies, sensitive columns, query exhaustion, extension side effects or what an agent does with legitimately returned data. SELECT access to the wrong table is already a disclosure; no write permission is required.

My [earlier execution-gate post](/posts/2026-07-30-prove-the-gate-not-the-agent/) asked what an enforcement point could establish. This experiment supplies a small, runnable answer for one database role: test useful reads, request forbidden changes, and include a control that becomes dangerous when you grant it. A cheerful permission error is evidence. So is the unexpectedly successful query.
