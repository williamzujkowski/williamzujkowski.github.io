# Timelock retention model — 2026-09-11

Status: original offline model executed; article reviewed for September 14 scheduling. Issue #597.
No storage devices, backup systems, malware, or remote services were exercised.

## Source identity and review

- Jonah Rosenblum, Juechu Dong, Peter Chen, and Satish Narayanasamy, [Timelock Drive: Isolated Time-Based Defense for Storage Systems](https://www.usenix.org/conference/osdi26/presentation/rosenblum), OSDI 2026, July 13–15, pp. 1683–1698. Exact title, authors, venue, publication month and pages checked against the official record on 2026-09-11.
- [Proceedings PDF](https://www.usenix.org/system/files/osdi26-rosenblum.pdf), read §§2–3 and prototype discussion on 2026-09-11. Figure 2b says Current time > Expiry time. Frozen is indefinite; unfreeze at Ut starts the original duration δ.
- [OSDI proceedings](https://www.usenix.org/conference/osdi26/technical-sessions) linked three errata checked 2026-09-11: [MEGALON](https://www.usenix.org/system/files/osdi26-errata_hu-jiyu.pdf), [Ambulance](https://www.usenix.org/system/files/osdi26-errata_giridharan.pdf), [MAC](https://www.usenix.org/system/files/osdi26-errata_lee.pdf). None concerns Timelock Drive. This is a scoped check, not proof that no correction exists anywhere.
- [S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html), accessed 2026-09-11, retention modes and delete behavior. Governance bypass, compliance restriction including root, account-deletion exception, and object-version/delete-marker distinction verified. Variable retention/event-hold release-plus-duration behavior also verified during independent review and credited as a close existing analogue. No AWS API calls performed.

## Claim ledger

| Claim | Kind | Evidence | Boundary |
| --- | --- | --- | --- |
| Frozen persists; unfreeze starts original duration | Source finding | Paper §3.1/Figure 2b | Not creation-based expiry |
| Checker protects metadata and relies on isolated non-decreasing clock | Source finding | Paper §§2–3 | Model assumes isolation; does not implement it |
| Physical destruction/exfiltration outside retention guarantee | Source finding | Paper §2 | No universal ransomware-prevention claim |
| Detection must occur while useful pre-intrusion state remains | Source finding | Paper §2 | No universal recommended retention duration |
| Eight cases, 34 operations, correct and broken policies differ | Original observation | Raw JSON, commands below | Deterministic selected cases, no exhaustive proof |
| Five tests pass | Original observation | unittest output | Only Python-model behavior |
| Governance/compliance differ; marker does not erase retained version | Product documentation | S3 Object Lock linked above | No account or product reproduction |
| Proposed version-manifest/restore procedure | Proposed work | Article analysis | Not executed, no results claimed |

## Reproduction

```bash
python3 scripts/security-labs/timelock/timelock_model.py
python3 -m unittest discover -s scripts/security-labs/timelock -p 'test_*.py'
uv run --with ruff ruff check scripts/security-labs/timelock
```

Runner output retained at [results-2026-09-11.json](../../scripts/security-labs/timelock/results-2026-09-11.json).
Execution used Python 3.12.3, no third-party runtime packages, and synthetic ticks.
The runner's global case total is 34, bounded below 1,000; each model also rejects
calls after 1,000 operations. Five tests passed in 0.001s on the initial run.
Ruff reported an import-order finding, corrected before the final clean run.
Sandbox startup failed on initial attempts; elevated offline runs succeeded.

Cases include indefinite frozen retention, expiry strictly after the boundary,
early overwrite/delete, shortening/repeated-unfreeze rejection, host clock forward
and rollback, checker rollback, and deliberately broken host-clock and
creation-expiry controls. Identical host-forward attacks preserve the correct
model's value and delete the broken model's value. These negative controls are
not vulnerabilities discovered in any real implementation.

## Editorial novelty and limits

Nearest posts: [Proxmox private cloud](../../src/posts/2025-12-24-private-cloud-homelab-proxmox-security.md),
[Proxmox HA](../../src/posts/2025-09-29-proxmox-high-availability-homelab.md), and
[resilience](../../src/posts/2024-06-25-designing-resilient-systems.md). Those address
deployment/availability and general failure handling. This article examines who
can revoke retention and the specific frozen-to-countdown distinction.

Native `.arch` and `.flow` visuals depict original simplified views with existing
tokens/classes. No copied paper figures or decorative raster assets. First-person
author experience, firmware adoption, and storage performance are not claimed.
The full model and test artifacts remain in the repository, with links from the
article; there is no new gist or long inline implementation.

Reviewed locally: source facts, temporal assumptions, mathematical boundary,
contextual NDA, obvious overlap, artifact scope, and raw result counts. Independent reviewers re-fetched primary sources and exactly reproduced all eight cases and 34 operations; root independently recomputed counts. Draft false denotes the reviewed September 14 schedule, not immediate website publication. Rendering and release checks are recorded in the staggered-release note.

## Artifact fingerprints at handoff

SHA-256, recorded after the module rename and both broken controls:

| Artifact | SHA-256 |
| --- | --- |
| `timelock_model.py` | `56dfd97a341f074803b9b0073dc0408374ae3d9bb717aec9f3bc4e632b494cdb` |
| `test_timelock.py` | `0a91b19ee7b5b2435ec54f9cd6a8de8f48fe9e620187cb43cb10e41751279cd2` |
| `results-2026-09-11.json` | `24431183abacff18b019b53c5e4577b552393d23ded5430fabf7defc9c5eeb39` |

Creation-based expiry is a valid alternative retention policy, but deliberately
violates the frozen-live contract tested here. It is not described as a universal
product defect. Draft body is approximately 1,000 words excluding frontmatter/URLs.
