# Paper discovery: measured boot, DNS, storage (2026-10-01)

**Status:** discovery record. No post written or scheduled (scope changed mid-pass: the
2026-10-29 slot went to another topic by consensus vote). Two proposals drafted, not
filed as issues. One control-only feasibility check run and retained.
**Window:** submissions since 2026-07-03 (last 90 days). Prior-art search undated.
**Procedure:** [blog-research.md](../blog-research.md) §1–2.

## Search log

| Step | Query / action | Result |
| --- | --- | --- |
| Seed | 5 arXiv IDs from a same-day Nexus `research_discover` pass (unverified metadata) | All five abstract pages fetched from `export.arxiv.org/abs/<id>`; titles, authors and dates matched the seed |
| arXiv API 1 | `cat:cs.CR AND (abs:"measured boot" OR abs:TPM OR abs:"secure boot")`, newest first, 15 results | 10 in window; 2 new leads (dTPM reset, Veraison freshness) |
| arXiv API 2 | `(cat:cs.CR OR cat:cs.NI) AND (abs:DNS AND abs:resolver)` | 4 in window; 3 new leads |
| arXiv API 3 | `(cat:cs.OS OR cat:cs.CR) AND (abs:filesystem OR abs:"disk encryption" OR abs:LUKS)` | 15 in window; mostly agent-security papers; 2 storage leads |
| Full text | TPMSpy v1 PDF (sha256 `20c65e4e…eef73f`); Runnable-to-Verifiable v1 PDF (sha256 `d7fb1c3f…3a87ea`) | Read §3–6 and §2, §5–8 respectively |
| Upstream | systemd `TPM2_PCR_MEASUREMENTS` doc; `man/systemd-pcrlock.xml`, `src/pcrlock/pcrlock.c`, `src/pcrextend/pcrextend.c`, `src/shared/{tpm2-util,efi-loader}.c` at tag v257/v258 via `gh api` | See prior art below |

API requests were sequential with a 3-second sleep and cached locally. Searched
2026-10-01 between roughly 04:00 and 04:50 UTC.

**Stop reason:** 12 leads reached; 3 checked in full or near-full (TPMSpy, Runnable-to-
Verifiable, plus upstream systemd source for the first); top candidate passed its
feasibility gate, so the #592 fallback was not taken. The scope change then ended work
before a main experiment.

## Leads (12)

| # | Lead | Checked | Decision | Reason / strongest objection |
| --- | --- | --- | --- | --- |
| 1 | Lacko, Švenda. *TPMSpy: Validation of Measured Boot Systems by Low-Level Tracing of TPM Usage*. [arXiv:2609.05011v1](https://arxiv.org/abs/2609.05011v1), submitted 2026-09-04, preprint, 20 pp. Artifact: [crocs-muni/tpmspy](https://github.com/crocs-muni/tpmspy) (MIT, created 2026-01-08, last push 2026-04-25) | Full text | **Proposal 1: research needed → new post** | Fits the archive's boot-security thread; feasible offline. Objection: systemd already documents the separate user-space log and pcrlock already merges both; see below |
| 2 | Bo Chen. *From Runnable to Verifiable: An Independent Reproducibility Study of LLM/Agent-Driven Vulnerability Validation Artifacts*. [arXiv:2608.09567v1](https://arxiv.org/abs/2608.09567v1), 2026-08-10, preprint | Full text (§2, §4–5.6, §8) | **Proposal 2: reading post, lower priority** | Strong "an oracle that fires on the patched build is not evidence" lesson. Objections: single author; no public pre-registration locator found in the text; theme sits close to the upcoming mutation-testing CI-gate post |
| 3 | Brož, Čierniková, Kozina, Sedláček. *Linux disk encryption and self-encrypting drives — A case study on Opal2 drives security*. [arXiv:2607.11563v1](https://arxiv.org/abs/2607.11563v1), 2026-07-13 | Abstract only | Research needed | High reader value (LUKS/Opal on Linux) but the evidence is a 38-drive hardware testbed; no lab possible here, and an abstract cannot support a detailed claim |
| 4 | Shahar, Klein. *Cross User/App Network Attacks — Hijacking TCP Connections and DNS Cache Poisoning via a Malicious User/App*. [arXiv:2609.09345v2](https://arxiv.org/abs/2609.09345v2), v1 2026-09-08, v2 2026-09-10; comments state accepted to ACM CCS 2026 | Abstract only | Defer | Includes systemd-resolved poisoning; a lab would be exploit reproduction, outside a bounded synthetic pass. Acceptance claim taken from arXiv comments only, not verified at the venue |
| 5 | Solarin, Kalu, Davis, Amusuo. *Reproducibility is Not Enough: Artifact Verifiability in Decentralized-Build Package Ecosystems*. [arXiv:2608.18180v1](https://arxiv.org/abs/2608.18180v1), 2026-08-18 | Abstract | Excluded | Overlaps the upcoming npm-provenance post |
| 6 | Gedela, Yaswanth. *TPM-Attest: Hardware-Rooted Integrity Attestation as a Kernel-Level Anti-Cheat Alternative for Linux*. [arXiv:2609.20909v1](https://arxiv.org/abs/2609.20909v1), 2026-09-17 | Abstract | Shelve | 100% detection over 500 *constructed* tamper sessions is the authors' own fixture; weak evidence for a post |
| 7 | Werling, Zahin, Seifert. *Not Discrete Enough: On the Inherent Insecurity of dTPMs for Measured Boot*. [arXiv:2608.14736v1](https://arxiv.org/abs/2608.14736v1), arXiv 2026-08-13 | Abstract | Background only | arXiv comment: published in ACSAC Workshops 2025, so not new work in this window (§1). Useful context for lead 1 (reset-and-replay) |
| 8 | Thiagarajan, Bustamante. *Who Resolves Your DNS? Measuring Resolver Opacity and Closing the Visibility Gap*. [arXiv:2608.29371v1](https://arxiv.org/abs/2608.29371v1), 2026-08-29 | Abstract | Reading only | RIPE Atlas measurement; reproducing it means probing third parties |
| 9 | *Domain Decoupling Attack: Exploiting the Validation Gap Between Protective DNS and Shared Edge Routing*, arXiv 2608.00643 | Title only | Not checked | Budget |
| 10 | *A Challenge-Nonce Freshness Gap in Project Veraison's TPM Reference Schemes…*, arXiv 2608.03534 | Title only | Not checked | Possible companion to lead 1 |
| 11 | *Isolation Failure From Shared Storage: Page-Cache SCA Leakage Across Containers and VMs*, arXiv 2607.17518v2 | Title only | Excluded | Overlaps [the 2026-09-21 VM disk-cache post](../../src/posts/2026-09-21-vm-disk-cache-isolation-boundary.md); first-version date not checked |
| 12 | *Securing Filesystems for Confidential Computing*, arXiv 2608.19924 | Title only | Not checked | Budget |

## Candidate 1 in detail: TPMSpy

**Source findings** (v1 PDF, read 2026-10-01):

- Method: an interposer between QEMU and swtpm records every TPM command, so the
  event log can be checked against an independent trace (§3.3, Fig. 1).
- 1,000 boots per systemd version, v245–v258, on NixOS; plus Ubuntu 24 (v255), Fedora
  41–43 (v256–v258) and Windows 11 (§5). Traces agreed with recovered event logs.
- Undocumented measurement: systemd-boot extended PCR 8 in v245, before the docs first
  mention TPM use in v248; traced to a 2016 commit released in v230 (§5.1).
- The load-bearing finding (§5.2, Fig. 4c–d): with a UKI on Fedora 43/v258, later PCR 11
  measurements (systemd-pcrphase) and the PCR 15 volume-key measurement (systemd-
  cryptsetup) were seen by TPMSpy but **not recorded in the firmware TPM event log**;
  IMA's PCR 10 measurements likewise. They live in `/run/log/systemd/tpm2-measure.log`
  (v255+) or the IMA runtime list. "The TPM Event Log alone is thus insufficient for
  remote attestation."
- Stated limit (§4.1, §6): it cannot detect a component that was never measured.

**Source-claim caution:** the abstract says the inconsistent measurements "prevent
reliable remote attestation and LUKS disk decryption." The body shows the attestation
side (an appraiser unaware of the extra logs fails); I found no unsealing or decryption
experiment. A post must not repeat the LUKS half as a demonstrated result.

**Prior art that weakens novelty (upstream, verified 2026-10-01):**

- systemd's [TPM2 PCR Measurements](https://systemd.io/TPM2_PCR_MEASUREMENTS/) page:
  "A userspace measurement event log in a format close to TCG CEL-JSON is maintained in
  `/run/log/systemd/tpm2-measure.log`." The separation is documented, not hidden.
- `systemd-pcrlock` (v258 man page, `man/systemd-pcrlock.xml` lines 49–75, 129–135,
  455–470) reads both the firmware log and the user-space log, validates the combined
  log against PCR state, and makes no prediction for a PCR whose value does not match
  the log, has unrecognized records, or is missing defined components.

**Strongest objection:** the paper's §5.2 finding is the documented design, and the main
systemd consumer already handles it. A post saying "the event log is two files" tells a
pcrlock user nothing. The remaining reader value is narrower: what an appraiser that is
*not* pcrlock does with a PCR it cannot explain, and what "no prediction for that PCR"
means for the strength of a policy. That has to be measured, not asserted. External
appraisers (e.g. Keylime) were **not** checked; no claim about them is supported.

**Reason to exist (provisional):** a reader binding a LUKS key or an attestation policy to
PCR 11/15 would learn which logs their appraiser must collect and how to tell
"unexplained PCR" from "tampered PCR" with a control they can run. Falsified if the main
matrix shows pcrlock and a firmware-log-only replay behave identically on every case.

## Feasibility check (control-only)

Lab branch `lab/tpm-event-log`, commit `fa8c7ec` in a research-labs worktree (not pushed).
Files: `labs/tpm-event-log/{Dockerfile,control.sh,README.md}`, `scripts/tpm-control.sh`,
`docs/evidence/tpm-event-log-feasibility/`.

Environment: Docker 29.8.1; `debian:trixie-slim@sha256:a99cfc51…1b20a`; swtpm 0.7.1-1.5,
tpm2-tools 5.7-1, libtss2-tcti-swtpm0t64 4.1.3-1.2, systemd 257.13-1~deb13u1. Container:
`--network none --read-only --user 65532 --cap-drop ALL --security-opt no-new-privileges`,
512 MiB, 64 pids, 16 MiB tmpfs, 120 s kill timeout. Each case uses a fresh swtpm.

| Case | Setup | Expected | Run 1 | Runs 2–3 |
| --- | --- | --- | --- | --- |
| c1 healthy | 4 phases via real `systemd-pcrextend`, logged; `pcrlock log` reads that log | match | match | match (calc = obs = `38d2047d…f23531e`) |
| c2 negative | Same extends; `pcrlock` given an absent user-space log | mismatch | **match (vacuous)** | mismatch (calc = zero, obs = `38d2047d…`) |
| c3 negative | c1 plus one unlogged `tpm2_pcrextend` to PCR 11 | mismatch | mismatch | mismatch (obs = `8e0debdd…ca002d9d7d`) |

c1 also passes a replay that does not use pcrlock: folding the four logged sha256
digests from zero reproduces the TPM value, and each digest equals sha256 of its word.

**Run 1 failed its own negative control, and the cause was the harness.** With
`SYSTEMD_MEASURE_LOG_FIRMWARE=/dev/null` and no declared bank, pcrlock loaded zero hash
algorithms; `event_log_pcr_checks_out()` (v257 `pcrlock.c` line 2197) loops over
`el->n_algorithms`, so it returned true without comparing anything. Setting
`SYSTEMD_TPM2_HASH_ALGORITHMS=sha256` (read at line 393) fixed it. A real firmware log
declares its banks, so this is a test-rig trap rather than a pcrlock defect, but it is
exactly the "empty log reads as clean" failure the main experiment would look for, and
any container-based policy test that omits the firmware log can hit it.

Also observed: `pcrlock log` exited 0 in all cases, including mismatches. It is a
reporting command; that is not a defect claim.

Evidence hashes: `run1-vacuous-c2.json` `ae484ff2…02a48c`, `run2.json` `f8a5546b…a244`,
`run3.json` `07b2e22d…4dbd`. Host `bootId` is redacted in retained output.

Commands (from the lab worktree root): `./scripts/tpm-control.sh > results/tpm-control.json`.
A final re-run of the committed script reported `all_controls_ok: true`.

## Claim ledger (for a future post)

| Proposed claim | Kind | Evidence and locator | Scope/caveat | Status |
| --- | --- | --- | --- | --- |
| systemd user-space PCR 11/15 measurements are absent from the firmware event log on Fedora 43/v258 with UKI | source finding | TPMSpy v1 §5.2, Fig. 4c–d | One distro/config; virtualized | verified (in source) |
| systemd documents a separate user-space log at `/run/log/systemd/tpm2-measure.log` | source finding | systemd.io TPM2_PCR_MEASUREMENTS | Current docs, fetched 2026-10-01 | verified |
| pcrlock reads both logs and withholds prediction for inconsistent PCRs | source finding | `systemd-pcrlock.xml` v258 lines 49–75, 129–135 | Documentation, not behaviour | verified (docs); behaviour of `predict` not run |
| pcrlock flags PCR 11 when the user-space log is absent or an extend is unlogged | our observation | runs 2–3, cases c2/c3 | swtpm, no firmware log, bank declared via env | verified (n=2 runs) |
| With zero known banks, pcrlock's PCR comparison passes vacuously | our observation + source | run 1 c2; `pcrlock.c` v257 l.2197 | Requires empty firmware log and no declared bank | verified |
| The inconsistency prevents LUKS decryption | source claim (abstract) | No supporting experiment found in body | — | unsupported; do not repeat |
| An appraiser that is not pcrlock fails open on unexplained PCRs | hypothesis | none | Needs named tools and runs | unsupported |

## Overlap check

`rg -il 'measured boot|\bPCR\b|swtpm|tpm2|systemd-pcr|TPMSpy|event log' src/posts docs`:
only [aegis-boot (2026-04-14)](../../src/posts/2026-04-14-signed-usb-rescue-boot-aegis-boot-persona-harness.md)
is related (QEMU+OVMF+swtpm personas, Secure Boot posture; no PCR/event-log analysis):
moderate, cross-link candidate. Two other hits are incidental. `docs/shelved-drafts/`: no match.
`gh issue list --state all --search` for `TPM`, `measured boot`, `PCR`, `systemd`: no results.
For candidate 2, `rg 'negative control|counterfactual|mutation test'` hit one unrelated post;
the shelved "checks that pass for the wrong reason" draft is thematically adjacent.

## Layer-1 coverage

No post exists, so the seven review stages were not run. Overlap was checked at the
candidate level as above. Proposal drafts (`proposal-1-tpm-event-log.md`, `proposal-2-oracle-counterfactual.md`) are session scratch files for root, not filed issues.

## Limitations

Abstract-only for leads 3–8; title-only for 9–12. No Keylime or other appraiser examined.
No VM, firmware or interposer, so nothing here replicates TPMSpy. Apt packages are
version-pinned but not snapshot-pinned. One machine, linux/amd64.
