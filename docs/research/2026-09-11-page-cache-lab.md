# Page-cache mechanism lab — 2026-09-11

Scope: author-authorized, agent-executed local synthetic experiment for proposal #599. This is not a VM reproduction, a real-tenant attack, a new vulnerability, or evidence of author-operated infrastructure beyond this recorded workspace run. Post publication is planned for 2026-09-21; measurements occurred 2026-09-11.

## Source identity and prior art

- [Isolation Failure From Shared Storage: Characterizing and Exploiting Page-Cache SCA Leakage Across Containers and VMs](https://arxiv.org/abs/2607.17518): Alon Abudraham, Xingyu Chen, Itamar Levi, Ari Trachtenberg. First submission July 20, 2026; [v2](https://arxiv.org/html/2607.17518v2), July 21. Preprint; no venue identified on inspected metadata. Accessed September 11, 2026. Read threat model (§3), testbeds/evaluation (§4), and storage configuration appendix. Conditional sharing assumptions and stronger Docker-oracle privileges are material. No author code artifact found during the bounded source search.
- [Page Cache Attacks](https://gruss.cc/files/pagecacheattacks.pdf), Gruss et al., CCS 2019: prior discovery of the page-cache attack class. Credit prevents presenting the July paper or this exercise as discovery of the primitive.
- [Eviction Notice](https://snee.la/pdf/pubs/eviction-notice.pdf), NDSS 2026: relevant intervening work on page-cache primitives. Read introduction and §§II-C/III-D regarding interface restrictions. The own-file use of mincore is explicitly not a bypass.
- [posix_fadvise](https://man7.org/linux/man-pages/man2/posix_fadvise.2.html): DONTNEED is advisory, partial-page requests are ignored, and dirty data should be synchronized first.
- [mincore](https://man7.org/linux/man-pages/man2/mincore.2.html): residency snapshot, not guaranteed future state.

## Feasibility and predefined method

QEMU binary existed at `/usr/bin/qemu-system-x86_64`; no validated guest images or KVM access established within the bounded session. Used the explicitly authorized own-process fallback, rather than claim VM evidence. An attempted `ls /dev/kvm` failed in the command sandbox before providing evidence. No guests were booted and no images downloaded.

Provisional question: does a different process reading the same file change target page residency and elapsed read time differently from reading a separately created byte-identical file? Falsifier/control failure: no established nonresident starting state, or no difference after shared-file priming. No classifier, inference of secrets, statistical significance test, or performance claim was planned.

Budget: five minutes per experiment, at most 100 repetitions per condition, two 8 MiB generated files, one child at a time, each child timeout five seconds; no network, memory-pressure generator, raw disks, host-wide cache flush, root, or other users' files. The run used 60 repetitions per condition. The controller passes already-open descriptors only to its Python child. All fixtures are under its new temporary directory and are deleted on exit. Output is created exclusively to protect existing evidence.

Schedule is seeded, balanced and shuffled. Each trial requests eviction of both own files, samples target residency, optionally primes one file from a child, samples target residency, reads the target from another child, and samples residency again. Each child times only `os.pread`; checksum/JSON/process launch are outside that interval. All successfully completed trials and exceptions are saved. Failed cache-state controls are not discarded.

## Runs and evidence

Commands from repository root:

```bash
python3 scripts/security-labs/page_cache.py run --output docs/research/2026-09-11-page-cache-results.json
python3 scripts/security-labs/page_cache.py run --output docs/research/2026-09-11-page-cache-ext4-results.json --scratch-parent docs/research
python3 -m unittest discover -s scripts/security-labs -p page_cache_test.py
```

Both runs: Python 3.12.3; Linux 7.0.0-31-generic; x86_64; euid 1000; 4096-byte pages; seed 20260911. Exact timestamps, script SHA-256, fixture SHA-256, every ordered trial, and summaries are in the JSON files. Fixture contents are regenerable from the fixed seed. Run scripts are preserved separately because the second run added an explicit scratch-directory option and final lint formatting followed measurement.

Run 1: [raw JSON](2026-09-11-page-cache-results.json), [exact script](2026-09-11-page-cache-run1-script.py). All 180 target pages were resident before priming, so cold-state validity failed. `/proc/mounts` confirmed `tmpfs /tmp tmpfs`; root filesystem was `/dev/mapper/ubuntu--vg-ubuntu--lv / ext4`. Three medians: shared 12746 ns, independent 13029.5 ns, no-primer 12802.5 ns. This result justified exactly one filesystem change rather than an unbounded search for a favorable outcome.

Run 2: [raw JSON](2026-09-11-page-cache-ext4-results.json), [exact script](2026-09-11-page-cache-run2-script.py). Generated fixtures were in a temporary child directory of `docs/research` on ext4. All 180 target pages were nonresident before priming. Post-prime residency: shared 60/60; independent 0/60; no-primer 0/60. Post-probe residency: 180/180. Median elapsed read: shared 13146.5 ns, independent 129680.5 ns, no-primer 199420.5 ns. Maxima: 20283 ns, 4447232 ns, 4503784 ns respectively. No outliers or completed trials excluded. No subsequent timing reruns were needed.

Important limitation: the independently created file has a separate inode, but the experiment does not establish physical-block independence, storage-controller behavior, or all possible cache relationships. Run 2's separate-inode condition did not prime the target page on this filesystem. mincore observes the user's own writable fixtures; it is not a test of another user's access protections. CPU affinity/frequency and background load were not controlled. Process creation is outside the timer but can influence system state. Advice need not work on other filesystems. Snapshots can change before the next operation.

## Claim ledger

| Claim | Kind | Evidence | Scope/status |
| --- | --- | --- | --- |
| The July work is a 2026 preprint, v2 July 21 | Bibliographic fact | arXiv history | Verified September 11 |
| Paper timing signals depend on shared host-cacheable backing objects | Source finding | v2 §§3–4 | Verified as authors' result, not locally reproduced |
| Page-cache attacks predate 2026 | Prior art | CCS 2019 paper | Verified |
| First run did not establish cold pages | Local observation | Run 1 all 180 pre-prime flags true | Verified; retained failure |
| Shared-file priming changed target residency on ext4 | Local observation | Run 2 60/60 shared vs 0/60 independent/no-prime | Verified, own files/processes only |
| Shared-file median was 13.15 µs | Local computation | Median 13146.5 ns / 1000, rounded 2 decimals | Verified; no inferential claim |
| Separate processes prove a VM isolation failure | Unsupported | None | Prohibited; explicitly disclaimed |

## QA record

- Overlap: nearest gVisor and Proxmox posts discuss sandboxing/storage deployment; new contribution is this controlled mechanism experiment and failed tmpfs control. Earlier gVisor post linked. No new general container-hardening tutorial.
- Accuracy/security: all numbers derive from preserved raw files, both runs retained. No secrets, real tenant behavior, or enforcement-bypass claim. Independent reviewers and root recomputed all counts and medians; both run-script hashes match the recorded values.
- Artifact: own stdlib script, no downloaded code, gists or copied paper diagrams. Linux API semantics checked against primary manuals. Two offline method tests check schedule balance/reproducibility/bounds and retention of failed-eviction/outlier denominators. They do not assert environment-dependent timing.
- Voice/contextual NDA: no employer references or invented author deployment history; trial authorship explicitly recorded above. Article distinguishes agent-recorded lab observations from source findings.
- Argument: narrow measured mechanism, clear failed-control falsifier, scoped next architectural question; no claim that direct I/O guarantees general security.
- Visuals: native opening `.arch` with matching accessible labels and inherited tokens; results table. No doodle needed under session-authorized native opening visual. Browser/mobile/theme/feed rendering is recorded in the staggered-release note.
- Vestiges: first-run script is intentional historical evidence; draft false denotes the reviewed September 21 schedule. No placeholder measurements or future-dated experiment claims.
