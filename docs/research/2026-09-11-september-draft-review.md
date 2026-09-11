# September 8 draft review and September 11 publication

Reviewed September 11, 2026. Publication uses September 11, not the abandoned
September 8 draft date. The September 14 and September 21 posts keep their dates.

## Editorial decision

| Draft | Decision | Evidence |
| --- | --- | --- |
| Read-only PostgreSQL role | Correct and publish September 11 | Reproducible database permission checks, a positive control, and current primary-source context |
| Agent memory recovery | Hold for narrower rewrite | 27 real calls, but nine scenario labels represent four distinct inputs; action success does not establish clean stored state |
| Static-site search | Shelve standalone proposal | Its proposed fixes already shipped; historical measurements remain valid for their stated revision |

The held drafts remain unchanged under [shelved drafts](../shelved-drafts/README.md).
The memory rewrite is tracked in [issue 605](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/605).
Neither shelving decision refutes the retained evidence.

Three parallel agent reviews covered database security and primary sources,
memory experiment validity, and search implementation history. Root reviewed
argument, voice, provenance, publication timing and alternatives. Corrections
remove unverified personal participation, fix the transaction-probe scope and
separate a database permission experiment from a connector vulnerability test.

## Research and orchestration

The existing PostgreSQL draft was compared with a narrower memory rewrite and
new research. Existing ZIP-parser and DNS research proposals remain tracked in
issues 591 and 598. A bounded Nexus arXiv search for 2026 systems-security parser
research returned three low-relevance leads; none was verified as a replacement
article. Discovery results are not cited as evidence. The existing database
artifact provided a better basis for this publication slot.

Primary AWS bulletins dated [September 4](https://aws.amazon.com/security/security-bulletins/2026-101-aws/)
and [September 9](https://aws.amazon.com/security/security-bulletins/2026-104-aws/)
were checked alongside PostgreSQL 18 documentation. The September 9 issue has
specific privileged-role and connection-profile prerequisites. The lab does not
install the affected MCP package, reproduce either CVE or validate its patch.

Nexus consensus job `job-vote-6a14b1ce-7f79-4408-864e-941ba66bada2` selected
`publish_database`: 3 of 3 votes, named-option threshold met, no errors or
simulated votes. The other declared options were `publish_memory` and
`research_replacement`. All three roles used the same model family, so this is
role diversity, not independent model diversity. The panel's suggestion that
the lab fits CI was not adopted: this remains an author-time experiment.

Nexus `execute_spec` parsed the publication requirements and acceptance criteria
in dry-run mode. It did not execute implementation or tests. Actual verification
is recorded separately below.

## Fresh database evidence

The unchanged runner and setup were re-executed September 11 using the already
cached digest-pinned PostgreSQL image. The container had no networking, published
ports or host mounts, with a 512 MiB memory limit, one CPU and a temporary data
directory. The enclosing invocation had a five-minute timeout.

The run completed in 5.158 seconds with exit status 0; all 24 checks passed and
the unique disposable container was removed. The breakdown is 15 expected
permission denials, one read-only transaction denial and eight successful checks.
The positive control observed a changed row, rolled back the transaction, revoked
the deliberately granted function capability and verified denial and original data.

The [September 11 raw results](../../scripts/security-labs/postgres-readonly/results-2026-09-11.json)
retain source SHA-256 hashes, the baseline commit, process exit status and elapsed
time. The original September 8 results remain unchanged. These were agent-executed
checks; they do not establish that the author personally performed the experiment.

## Publication verification

Archiving the remaining drafts exposes a valid state after September 21: there
are no hidden posts. The hidden-post-specific browser test now explicitly skips
in that state; the independent comparison of the complete published set still
runs. Keeping an artificial draft solely to satisfy a test would hide the issue.

Release validation and the final merge decision are recorded in the publishing PR.
