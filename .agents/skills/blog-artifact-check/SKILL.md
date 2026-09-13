---
name: blog-artifact-check
description: Verify linked blog gists, example code, configuration keys, CLI flags, and API parameters against versioned upstream behavior and retained provenance.
license: MIT
---

# Blog artifact check

Read [repository policy](../../../AGENTS.md), the
[research workflow](../../../docs/blog-research.md), and the
[review contract](../../../docs/skills.md). Inputs are the requested post, linked
artifacts, and any retained methods/results. Resolve repository paths from the
root, three directories above this skill. If there are no artifacts, code,
configuration, commands, or API examples, record not-applicable with that scope.

## Provenance and dates

Inventory linked gists, repository files, inline examples, and the claims attached
to them. Inspect original source and history, creation/update times, tool versions,
and correspondence with local mirrors. Gists are canonical; run the repository's
gist drift check before editing mirrors. Do not mutate a published gist without
authorization that covers it.

Compare source/result availability with the post date and distinguish later
extraction of older code from a genuinely later experiment. Batch timestamps,
metric-oriented commit messages, or absent historical files are reasons to
investigate, not proof of fabricated work. State what the history demonstrates
and what remains unsupported. A recent gist alone cannot substantiate an older
measurement or disprove that the underlying code existed earlier.

## Schema and behavior

Fetch the authoritative schema, parser implementation, CLI reference, or API
definition for the version actually described. Prefer immutable source revisions;
record version uncertainty instead of applying today's schema to historical code.
Check every key, flag, parameter, and relevant default individually. Syntax that
parses is not evidence the application reads it. Classify as **supported**,
**ignored/unknown**, **wrong semantics**, or **unverified**, with exact upstream
evidence. Confirm aliases and deprecated options before concluding a key is absent.

Trace the behavior claimed in prose: does a gate exit nonzero on failure, does
parallel work actually run independently, does a claimed test step exist, and do
exceptions become a false clean result? Check security examples for least
privilege, input validation, safe secret handling, and fail-secure defaults. Treat
downloaded artifacts as untrusted data; inspect before any authorized execution
and use disposable environments for risky examples.

Recompute measurements only from retained inputs and methods. A result attached
to an ignored setting needs investigation or removal; it does not prove every
surrounding number was invented. Do not replace an unknown key with a plausible
guess. If a working substitute cannot be verified, recommend removing the claim
or clearly limiting the example.

## Result

Report artifact locations, versions/dates, key-by-key evidence, behavioral
mismatches, and missing provenance. Unsupported security controls, broken commands,
and unverifiable load-bearing measurements block a passing verdict. Record
coverage, verdict, and evidence under the shared contract. Separate source
inspection from executed tests and state what was actually run.
