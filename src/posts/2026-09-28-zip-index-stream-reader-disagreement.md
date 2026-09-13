---
title: "One ZIP, Two Lists of Files"
date: 2026-09-28
draft: false
author: William Zujkowski
description: "A small reproducible ZIP lab shows why indexed and streaming readers can inspect different entries in the same archive."
tags:
  - security
  - software-engineering
  - homelab
---

The [ZIP lab](https://github.com/williamzujkowski/research-labs/tree/68874f0a840c063973f945f68560d7ecaec9e8a1) feeds six tiny archives to three reader APIs and records what each one sees. One archive contains an ordinary text entry followed by an extra entry holding a harmless marker. Both indexed readers miss the extra entry. The streaming reader finds it. All three finish successfully.

The bytes never change. The readers disagree about which records belong in their list of files. If a content check and a later consumer build those lists differently, hashing the original upload does not resolve that disagreement. The lab isolates that boundary without running a scanner or extracting anything to disk.

<div class="flow" role="group" aria-label="Observed result for an archive with an unindexed local entry">
  <div class="flow-node"><b>Identical ZIP bytes</b><i>One indexed entry; an extra local entry</i></div>
  <div class="flow-branch" role="group" aria-label="Reader observations">
    <div class="flow-leg" data-branch="Indexed" role="group" aria-label="Indexed readers"><div class="flow-node"><b>note.txt</b><i>Marker absent from observed entries</i></div></div>
    <div class="flow-leg" data-branch="Streaming" role="group" aria-label="Streaming reader"><div class="flow-node"><b>note.txt and extra.txt</b><i>Marker present in extra.txt</i></div></div>
  </div>
</div>

## The index and the records

ZIP has local file records and a central directory pointing to them. The two carry overlapping metadata. The [format specification, §4.3.2](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT), requires a corresponding central-directory header for each local file header. The extra entry in this fixture deliberately breaks that rule. Successful iteration is not a certificate of format validity.

Java documents the distinction directly: [`ZipInputStream`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/zip/ZipInputStream.html) reads local headers and does not read the central-directory metadata for an entry. Its indexed counterpart, `ZipFile`, offers a different view. In the lab, those two APIs come from the same JDK. Counting them as two independent implementations would make the comparison look broader than it is.

This is established research territory. You, Chen, Wang and Duan's [*My ZIP isn't your ZIP*](https://www.usenix.org/system/files/usenixsecurity25-you.pdf), published at USENIX Security 2025, studies parser disagreements systematically and demonstrates their use in real products. Sections 2 and 4 explain the format and differential-testing method. This much smaller, original corpus is a way to inspect one mechanism; it does not reproduce the paper's fuzzing campaign or its attacks.

## What the six archives showed

The September 13 run used CPython 3.12.14 and Temurin OpenJDK 21.0.12. Python enumerates `ZipInfo` objects and opens each object, Java enumerates indexed entries and immediately opens each one, and Java's streaming API reads successive local entries. Python explicitly supports using a [`ZipInfo` object for duplicate names](https://docs.python.org/3.12/library/zipfile.html#zipfile.ZipFile.open).

| Fixture | Python indexed | Java indexed | Java streaming |
| --- | --- | --- | --- |
| Ordinary control | Ordinary entry | Same | Same |
| Duplicate name, marker first | Both entries | Same | Same |
| Duplicate name, marker last | Both entries | Same | Same |
| Reversed central-directory order | Directory order | Directory order | Local order |
| Conflicting local and indexed names | Rejected | Indexed name | Local name |
| Extra local entry absent from directory | Ordinary entry only | Same | Ordinary and extra entry |

These are [retained observations](https://github.com/williamzujkowski/research-labs/blob/68874f0a840c063973f945f68560d7ecaec9e8a1/docs/evidence/zip-reference.json): 18 executions, 17 successes and one parser rejection. Three fixtures produce different accepted entry sequences. One of those differences is only ordering, and only the unindexed-entry fixture changes the marker decision. Six selected inputs cannot tell us how often this happens in uploaded archives.

The duplicate cases are useful precisely because they agree. Every adapter retains both entries, including their order and content hashes. Writing them straight to a directory would introduce an overwrite policy and could hide one entry. This experiment stops before that step, so it establishes no filesystem-extraction result.

The name-conflict case matters for another reason. Python rejects it. The report keeps that rejection separate from successful reading with no marker found. An error handler that turns both into an empty list would erase the distinction the check needs.

## Try the same inputs

The [fixed revision's instructions](https://github.com/williamzujkowski/research-labs/blob/68874f0a840c063973f945f68560d7ecaec9e8a1/README.md) require Git, Docker with Linux-container support, and a POSIX shell:

```sh
git clone https://github.com/williamzujkowski/research-labs.git
cd research-labs
git checkout 68874f0a840c063973f945f68560d7ecaec9e8a1
./scripts/lab.sh test
mkdir -p results
./scripts/lab.sh run > results/zip.json
```

The first build downloads digest-pinned runtimes. The experiment then runs without networking or host mounts, as a non-root user with a read-only root filesystem and bounded resources. Each reader gets ten seconds, twenty entries and one MiB of decoded content. Those controls suit this fixed, inert corpus; the container is not an invitation to feed it arbitrary hostile archives.

All 23 tests passed. The [GitHub CI run](https://github.com/williamzujkowski/research-labs/actions/runs/34741618089) reproduced the local fixture hashes and all 18 adapter outcomes. Runtime and source identifiers are in the report. Host details and timestamps can differ; compare the observations rather than expecting the entire JSON file to have an identical hash.

## The check belongs at the handoff

My [scanning-pipeline article](/posts/2025-10-06-automated-security-scanning-pipeline) asks whether scanners run and whether their results actually block a build. This lab asks what content reaches a check in the first place.

For a pipeline that checks an archive and then consumes it through another API, I would make the observed entry list part of the integration test: names, ordering where it matters, and payload hashes. Include malformed-input rejection as an explicit outcome. A shared parser is a useful starting point, but different APIs within one runtime already disagree on this fixture.

That recommendation has a boundary. The lab checks a literal marker, not malware, and never invokes a downstream extractor. A real bypass claim would need the actual checking policy and consumer. What it supplies today is a small regression case for a more basic question: did the next stage receive the content the previous stage inspected?
