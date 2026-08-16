---

title: "Sandboxing Untrusted Containers with gVisor: Lessons from G-Fuzz Vulnerability Research"
date: 2024-09-25
description: "Secure containers with gVisor sandboxing—prevent kernel exploits in Kubernetes clusters while managing 59% startup overhead for untrusted workloads."
author: "William Zujkowski"
reading_time: 9
tags:
  - container-orchestration
  - container-security
  - docker
  - homelab
  - security
---

## Bottom Line Up Front

**gVisor adds OS-level sandboxing to containers, preventing kernel exploits by intercepting syscalls in userspace.** The G-Fuzz directed-fuzzing framework has found multiple serious vulnerabilities in gVisor, but it still outperforms runc for untrusted workloads. In my K3s cluster, gVisor increased container startup time from 42ms to 67ms (59% overhead) yet stopped the escape attempts I was able to test meaningfully.

**Why it matters:** [CVE-2024-21626 (CVSS 8.6)](https://nvd.nist.gov/vuln/detail/CVE-2024-21626) enabled runc container escapes in January 2024. [Docker patched it](https://www.docker.com/blog/docker-security-advisory-multiple-vulnerabilities-in-runc-buildkit-and-moby/), but the vulnerability existed for years. gVisor's userspace kernel prevents entire classes of these exploits.

**The research:** [G-Fuzz](https://arxiv.org/abs/2409.13139) (Li et al., *IEEE TDSC* vol. 21 no. 1, Jan-Feb 2024) is a directed fuzzing framework for gVisor out of Zhejiang University and Ant Group — not Google, who wrote gVisor itself. The authors report it significantly outperforms Syzkaller on gVisor and has been deployed in industry, where it detected multiple serious vulnerabilities.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/gvisor-sandbox.png'); width: min(280px, 72%); aspect-ratio: 400/510; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">play here, break nothing</p>

## The Container Escape Problem

Containers share the host kernel. One bad syscall can break containment. This is why [container security hardening](/posts/2025-08-18-docker-lsm-security-hardening) requires multiple layers of defense beyond just namespaces and cgroups.

**Recent escapes:**

- **CVE-2024-21626:** runc working directory manipulation → host filesystem access
- **CVE-2024-23651:** BuildKit race condition → host file exposure
- **CVE-2024-23652:** BuildKit `RUN --mount` cleanup → arbitrary file **deletion** on the host (CVSS 9.1)
- **CVE-2024-23653:** BuildKit GRPC API → privilege escalation

[Snyk's "Leaky Vessels" advisory](https://snyk.io/blog/leaky-vessels-docker-runc-container-breakout-vulnerabilities/) details how attackers weaponized these. The common thread: kernel syscall filtering isn't enough.

**Standard container security relies on:**

- **[Namespaces](https://man7.org/linux/man-pages/man7/namespaces.7.html):** Isolate process trees, networks, filesystems
- **[Cgroups](https://www.kernel.org/doc/Documentation/cgroup-v2.txt):** Limit CPU, memory, I/O
- **[Seccomp-BPF](https://www.kernel.org/doc/html/latest/userspace-api/seccomp_filter.html):** Block dangerous syscalls
- **AppArmor/SELinux:** Mandatory access control

**But:** All these run in the kernel. Kernel bugs bypass them.

<figure class="arch-fig">
<div class="arch is-stack" role="group" aria-label="Traditional container isolation stack">
  <section class="arch-tier" data-label="Workload" role="group" aria-label="Workload"><span class="arch-chip is-primary">Container Process</span></section>
  <section class="arch-tier" data-label="Kernel Isolation Controls" role="group" aria-label="Kernel Isolation Controls"><span class="arch-chip is-guard">Namespaces</span><span class="arch-chip is-guard">Cgroups</span><span class="arch-chip is-guard">Seccomp-BPF</span><span class="arch-chip is-guard">AppArmor / SELinux</span></section>
  <section class="arch-tier" data-label="Shared Boundary" role="group" aria-label="Shared Boundary"><span class="arch-chip is-bad">Host Kernel</span></section>
  <section class="arch-tier" data-label="Platform" role="group" aria-label="Platform"><span class="arch-chip">Hardware</span></section>
</div>
<figcaption>Traditional containers add multiple guardrails, but every path still terminates at the shared host kernel.</figcaption>
</figure>

> All isolation mechanisms run inside the kernel. A single kernel vulnerability bypasses every layer.

**Why it matters:** You can harden seccomp profiles for weeks. One kernel 0-day undoes it all.

## What gVisor Actually Does

gVisor inserts a userspace kernel between containers and the host.

**Architecture:**

```
Container → gVisor Sentry (userspace) → Host Kernel
```

**The Sentry:**

- Written in Go, which eliminates most memory-corruption classes; the remaining `unsafe` code is quarantined into `*_unsafe.go` files by policy
- Intercepts every syscall
- Re-implements most of the Linux syscall surface in userspace
- Only safe operations reach the host kernel

**The Gofer:**

- Handles filesystem access via [9P protocol](https://9p.io/magic/man2html/5/intro)
- Runs with minimal privileges
- Is the component that *does* touch the host filesystem, so that the Sentry never has to

<figure class="arch-fig">
<div class="arch is-stack" role="group" aria-label="gVisor container sandbox architecture">
  <section class="arch-tier" data-label="Container Sandbox" role="group" aria-label="Container Sandbox"><span class="arch-chip is-primary">Container App</span></section>
  <section class="arch-tier" data-label="gVisor Userspace Kernel" role="group" aria-label="gVisor Userspace Kernel"><span class="arch-chip is-guard"><b>Sentry</b><i>Go userspace kernel; 200+ syscalls reimplemented</i></span><span class="arch-chip is-guard"><b>Gofer</b><i>9P filesystem proxy; minimal privileges</i></span></section>
  <section class="arch-tier" data-label="Host" role="group" aria-label="Host"><span class="arch-chip"><b>Host Kernel</b><i>limited syscall surface</i></span><span class="arch-chip">Host Filesystem</span></section>
</div>
<figcaption>Container syscalls hit Sentry first; only safe host syscalls and scoped file requests continue into the host.</figcaption>
</figure>

**Key insight:** Even if a container exploits a syscall bug, it's exploiting Go code in userspace, not the kernel. No privilege escalation to host.

**Trade-off:** Performance. Every syscall crosses userspace boundary twice (container → Sentry → kernel → Sentry → container).

<ol class="seq" aria-label="gVisor syscall handling">
  <li class="seq-step"><b>Container App &rarr; Sentry</b><span>syscall, e.g. open()</span></li>
  <li class="seq-note">Sentry intercepts &amp; validates the syscall</li>
  <li class="seq-label">If: file operation</li>
  <li class="seq-step"><b>Sentry &rarr; Gofer</b><span>9P file request</span></li>
  <li class="seq-step"><b>Gofer &rarr; Host Kernel</b><span>scoped host syscall</span></li>
  <li class="seq-step"><b>Host Kernel &rarr; Gofer</b><span>file data</span></li>
  <li class="seq-step"><b>Gofer &rarr; Sentry</b><span>9P response</span></li>
  <li class="seq-label">Else: non-file operation</li>
  <li class="seq-step"><b>Sentry &rarr; Host Kernel</b><span>filtered host syscall</span></li>
  <li class="seq-step"><b>Host Kernel &rarr; Sentry</b><span>result</span></li>
  <li class="seq-label">Then</li>
  <li class="seq-step"><b>Sentry &rarr; Container App</b><span>syscall result</span></li>
  <li class="seq-note">Dangerous syscalls never reach the host kernel</li>
</ol>

## G-Fuzz: Finding Bugs in the Sandbox

[G-Fuzz](https://arxiv.org/abs/2409.13139) is a directed fuzzing framework targeting gVisor's Go-based kernel.

**The challenge:** Traditional fuzzers like [Syzkaller](https://github.com/google/syzkaller) target C kernels. gVisor is Go. Different memory model, different vulnerabilities.

**G-Fuzz innovations:**

1. **Lightweight distance calculation:** Measures how close inputs are to reaching target code paths without heavyweight instrumentation
2. **Syscall inference:** Identifies which syscalls are most likely to trigger bugs in specific code regions
3. **Dynamic switching:** Alternates between exploration (finding new code) and exploitation (triggering bugs)

**Results:**

- Outperformed Syzkaller on gVisor by significant margins
- Detected multiple serious vulnerabilities
- Methods transferable to other OS kernels

**What the paper doesn't say:** Exact CVE numbers or vulnerability details. Google likely embargoed specifics during responsible disclosure.

**Why it matters:** Even "secure by design" systems have bugs. Continuous fuzzing finds them before attackers do.

## Deploying gVisor in My Homelab

I run a 3-node [K3s](https://k3s.io/) cluster on Raspberry Pi 5s (16GB each) plus one Pi 4 (8GB). K3s is Kubernetes, stripped down.

**Initial attempt:** Deploy gVisor globally.

⚠️ **Warning:** These commands modify system configuration. Only use in controlled lab environments with proper backups.

```bash
# Install gVisor runtime
curl -fsSL https://gvisor.dev/archive.key | sudo gpg --dearmor -o /usr/share/keyrings/gvisor-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/gvisor-archive-keyring.gpg] https://storage.googleapis.com/gvisor/releases release main" | sudo tee /etc/apt/sources.list.d/gvisor.list
sudo apt-get update && sudo apt-get install -y runsc

# Configure containerd
sudo runsc install
sudo systemctl restart containerd
```

**Result:** First pod wouldn't start. Logs showed blocked syscalls.

**Problem:** gVisor implements 288 of 351 syscalls fully or partially, leaving 63 unsupported. Missing syscalls fail hard.

**Solution:** Use gVisor selectively via [RuntimeClass](https://kubernetes.io/docs/concepts/containers/runtime-class/).

```yaml
# runtime.yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: gvisor
handler: runsc
---
# untrusted-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: untrusted-app
spec:
  runtimeClassName: gvisor
  containers:
  - name: app
    image: nginx:latest
```

**This worked.** Pods using `runtimeClassName: gvisor` run in gVisor. Everything else uses runc.

**Debugging incompatible workloads:**

```bash
# Check which syscalls a binary uses
strace -c nginx 2>&1 | grep -v "detached" | sort -n

# Compare against gVisor's supported syscalls
runsc debug --all | grep -o 'syscall.*' | sort
```

Took 2 hours tracing strace output to find that my custom monitoring sidecar used a `ptrace` option gVisor doesn't implement (the syscall itself has partial support). Removed sidecar, monitoring works.

**Current setup:**

- 12 of 30 pods run on gVisor (untrusted images, internet-facing services)
- 18 pods run on runc (trusted workloads, performance-sensitive)
- Zero compatibility issues after initial debugging

## Performance Testing: gVisor vs runc

I benchmarked container startup, syscall overhead, and I/O performance.

**Test environment:**

- Dell R910: 48 threads, 256GB RAM, [Incus](https://linuxcontainers.org/incus/) 6.0
- 2 identical VMs: Ubuntu 24.04, 8 vCPUs, 16GB RAM
- VM1: runc, VM2: gVisor (runsc)

**Container startup (100 iterations):**

```bash
# runc
time for i in {1..100}; do docker run --rm alpine:latest echo "test"; done
# Average: 42ms per container

# gVisor
time for i in {1..100}; do docker run --rm --runtime=runsc alpine:latest echo "test"; done
# Average: 67ms per container
```

**Result:** 59% overhead. Acceptable for untrusted workloads.

**Syscall-heavy workload (compile Linux kernel):**

```bash
# runc
time docker run --rm gcc:latest bash -c "apt-get update && apt-get install -y bc && wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.10.1.tar.xz && tar xf linux-5.10.1.tar.xz && cd linux-5.10.1 && make defconfig && make -j4"
# Time: 8m 32s

# gVisor
time docker run --rm --runtime=runsc gcc:latest bash -c "apt-get update && apt-get install -y bc && wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.10.1.tar.xz && tar xf linux-5.10.1.tar.xz && cd linux-5.10.1 && make defconfig && make -j4"
# Time: 11m 47s
```

**Result:** 38% overhead. Compile is syscall-heavy (file I/O, fork/exec).

**Network throughput (nginx):**

```bash
# runc
ab -n 100000 -c 100 http://runc-nginx/
# Requests/sec: 12,847

# gVisor
ab -n 100000 -c 100 http://gvisor-nginx/
# Requests/sec: 11,203
```

**Result:** 13% overhead. Network syscalls (socket, send, recv) cross userspace boundary.

**Why it matters:** gVisor cost me 13% on network throughput, 38% on a syscall-heavy compile, and 59% on container startup. For security-critical workloads, that's acceptable. For performance-critical workloads, use runc.

## Container Escape Testing

⚠️ **Warning:** This section demonstrates container escape techniques for educational purposes only. These tests should only be performed in isolated lab environments with proper authorization. Never attempt these techniques on production systems or systems you don't own.

I attempted 5 common container escape techniques.

**Test 1: Privileged container with host filesystem mount**

```bash
# runc (baseline)
docker run --rm --privileged -v /:/host alpine chroot /host /bin/bash
# Result: Full host shell access ✓

# gVisor
docker run --rm --runtime=runsc --privileged -v /:/host alpine chroot /host /bin/bash
# Result: Permission denied ✗
```

**Read this one carefully, because I originally drew the wrong conclusion from it.** gVisor's boundary is the host *kernel*, not the host *filesystem*. If you bind-mount `/` into the sandbox you have configured the gofer to serve the host root, and gVisor will serve it — the docs are explicit that it exposes exactly the paths the OCI config dictates. Don't run this under any runtime. The `--privileged` flag disables seccomp/AppArmor but doesn't give direct kernel access.

**Test 2: /proc/sys/kernel write attempt**

```bash
# Attempt to modify kernel parameters
docker run --rm --runtime=runsc alpine sh -c "echo 1 > /proc/sys/kernel/core_pattern"
# Result: Read-only file system ✗
```

**Why gVisor blocked it:** `/proc/sys` is a read-only overlay. No direct kernel parameter modification.

**Test 3: cgroup release_agent exploit (CVE-2022-0492)**

⚠️ **Warning:** This demonstrates a known container escape technique. Only use in isolated lab environments for educational purposes.

```bash
# Classic container escape technique
docker run --rm --runtime=runsc alpine sh -c "echo '/payload.sh' > /sys/fs/cgroup/memory/release_agent"
# Result: Operation not permitted ✗
```

**Why gVisor blocked it:** cgroups are emulated in Sentry. No direct host cgroup manipulation.

**Test 4: Docker socket mount**

```bash
# Mount Docker socket (common misconfiguration)
docker run --rm --runtime=runsc -v /var/run/docker.sock:/var/run/docker.sock docker:latest docker ps
# Result: Works, but limited to gVisor containers
```

**Surprise:** This works because Docker socket access isn't a kernel exploit, it's an API exploit. gVisor doesn't protect against application-level attacks.

**Mitigation:** Don't mount Docker sockets. Use least-privilege service accounts.

**Test 5: Dirty Pipe (CVE-2022-0847) attempt**

⚠️ **Warning:** This tests a known kernel vulnerability (CVE-2022-0847). Only use in isolated lab environments for educational purposes.

```bash
# Attempt to exploit pipe write vulnerability
# (Simplified test, actual exploit is more complex)
docker run --rm --runtime=runsc alpine sh -c "echo 'exploit' | tee /proc/self/mem"
# Result: Operation not permitted ✗
```

**Why gVisor blocked it:** Userspace kernel doesn't have the vulnerable pipe implementation. Bug doesn't exist in Sentry.

**Summary:** gVisor stopped 4 of 5 escapes. The 5th (Docker socket) isn't a kernel exploit, so gVisor's out of scope.

## When to Use gVisor

**Use gVisor for:**

- Untrusted container images (public registries, user-submitted code)
- Multi-tenant workloads (SaaS platforms, CI/CD runners)
- Internet-facing services (web apps, APIs) - combine with [zero-trust architecture](/posts/2024-07-09-zero-trust-architecture-implementation)
- Multi-tenant workloads where you need to argue isolation strength to an auditor

**Don't use gVisor for:**

- Performance-critical workloads (databases, real-time processing)
- Syscall-heavy applications (compilers, development tools)
- Unsupported syscalls (ptrace, some eBPF programs)
- Trusted internal services (monitoring, logging)

**My decision tree:**

<div class="flow" role="group" aria-label="Container runtime selection decision path">
  <div class="flow-node">New Workload</div>
  <div class="flow-node is-gate">Untrusted image?</div>
  <div class="flow-branch" role="group" aria-label="Branch outcomes">
    <div class="flow-leg" data-branch="Yes" role="group" aria-label="Yes"><div class="flow-node is-good">Use gVisor</div></div>
    <div class="flow-leg" data-branch="No" role="group" aria-label="No"><div class="flow-node is-gate">Internet-facing?</div></div>
  </div>
  <div class="flow-branch" role="group" aria-label="Branch outcomes">
    <div class="flow-leg" data-branch="Yes" role="group" aria-label="Yes"><div class="flow-node is-good">Use gVisor</div></div>
    <div class="flow-leg" data-branch="No" role="group" aria-label="No"><div class="flow-node is-gate">Needs native performance?</div></div>
  </div>
  <div class="flow-branch" role="group" aria-label="Branch outcomes">
    <div class="flow-leg" data-branch="Yes" role="group" aria-label="Yes"><div class="flow-node">Use runc</div></div>
    <div class="flow-leg" data-branch="No" role="group" aria-label="No"><div class="flow-node is-gate">Syscall-heavy?</div></div>
  </div>
  <div class="flow-branch" role="group" aria-label="Branch outcomes">
    <div class="flow-leg" data-branch="Yes" role="group" aria-label="Yes"><div class="flow-node">Use runc</div></div>
    <div class="flow-leg" data-branch="No" role="group" aria-label="No"><div class="flow-node"><b>Use runc</b><i>principle of least surprise</i></div></div>
  </div>
</div>

**Trade-off:** Security vs performance. I choose security for attack surfaces, performance for internal services.

## What I Learned

**gVisor isn't perfect.**

- G-Fuzz found bugs. More exist.
- Syscall coverage gaps break some workloads.
- Performance overhead ranged from 13% to 59% in my testing, depending entirely on syscall intensity.

**But it's better than alternatives:**

- [Kata Containers](https://katacontainers.io/): Heavier (full VMs), slower startup
- [Firecracker](https://firecracker-microvm.github.io/): AWS-specific, not Kubernetes-native
- seccomp-only: Kernel bugs bypass it

**The real lesson:** Defense in depth. I use:

- gVisor for untrusted containers
- Network policies to limit lateral movement
- Wazuh for syscall monitoring (integrate with [threat intelligence](/posts/2025-09-14-threat-intelligence-mitre-attack-dashboard))
- Regular vulnerability scanning (Grype, Trivy)

**Container security is layers.** gVisor is one layer. A good one.

## Practical Recommendations

**Start small:**

1. Deploy gVisor on one node
2. Test with non-critical workloads
3. Profile performance for your use case
4. Expand gradually

**Monitor compatibility:**

```bash
# Check for failed syscalls
kubectl logs <pod> | grep "syscall not supported"

# Enable debug logging
runsc --debug --debug-log=/tmp/runsc.log <container_id>
```

**Tune for performance:**

- Use [overlay filesystem](https://opensource.googleblog.com/2023/04/gvisor-improves-performance-with-root-filesystem-overlay.html) — Google measured it halving gVisor's sandboxing overhead on an abseil-cpp Bazel build
- Enable [seccomp optimization](https://gvisor.dev/blog/2024/02/01/seccomp/) — note gVisor's 2024 seccomp work cut filtering overhead ~29% on microbenchmarks but only ~1% of total runtime on real builds, and it ships on by default
- Profile your workload with [gVisor's performance guide](https://gvisor.dev/docs/architecture_guide/performance/)

**Reality check:** gVisor requires investment. Study syscall traces, understand your workload, measure performance. If you're not willing to debug, stick with runc.

## The Bigger Picture

G-Fuzz demonstrates that even secure-by-design systems need adversarial testing. gVisor's Go implementation avoids memory corruption, but logic bugs remain.

**Continuous fuzzing matters:**

- [Syzkaller](https://github.com/google/syzkaller) for C kernels
- [G-Fuzz](https://arxiv.org/abs/2409.13139) for Go kernels
- [Trinity](https://github.com/kernelslacker/trinity) for syscall fuzzing

**Defense ecosystem:**

- gVisor for kernel isolation
- [Falco](https://falco.org/) for runtime detection
- [Open Policy Agent](https://www.openpolicyagent.org/) for admission control
- [Tetragon](https://github.com/cilium/tetragon) for eBPF observability

<figure class="arch-fig">
<div class="arch is-stack" role="group" aria-label="Container defense in depth stack">
  <section class="arch-tier" data-label="Admission Control" role="group" aria-label="Admission Control"><span class="arch-chip is-guard">OPA / Kyverno</span></section>
  <section class="arch-tier" data-label="Runtime Sandbox" role="group" aria-label="Runtime Sandbox"><span class="arch-chip is-primary">gVisor Sentry + Gofer</span></section>
  <section class="arch-tier" data-label="Runtime Detection" role="group" aria-label="Runtime Detection"><span class="arch-chip is-warn">Falco / Tetragon</span></section>
  <section class="arch-tier" data-label="Network Policy" role="group" aria-label="Network Policy"><span class="arch-chip is-guard">Cilium / Calico</span></section>
  <section class="arch-tier" data-label="Vulnerability Scanning" role="group" aria-label="Vulnerability Scanning"><span class="arch-chip">Grype / Trivy</span></section>
</div>
<figcaption>Attackers should be blocked at admission or runtime, detected by monitoring, and contained by network policy before scanning closes the loop.</figcaption>
</figure>

**No silver bullet.** Security is understanding your threat model and layering controls.

## Sources

1. **[G-Fuzz: A Directed Fuzzing Framework for gVisor](https://arxiv.org/abs/2409.13139)** (2024)
   - J. Zhang et al.
   - *IEEE Transactions on Dependable and Secure Computing*

2. **[Docker Security Advisory: Multiple Vulnerabilities in runc, BuildKit, and Moby](https://www.docker.com/blog/docker-security-advisory-multiple-vulnerabilities-in-runc-buildkit-and-moby/)** (2024)
   - Docker Inc.

3. **[Leaky Vessels: Docker and runc Container Breakout Vulnerabilities](https://snyk.io/blog/leaky-vessels-docker-runc-container-breakout-vulnerabilities/)** (2024)
   - Snyk Security Research Team

4. **[CVE-2024-21626: runc process.cwd Container Breakout](https://nvd.nist.gov/vuln/detail/CVE-2024-21626)** (2024)
   - National Vulnerability Database (NVD)

5. **[What is gVisor?](https://gvisor.dev/docs/)** (2024)
   - Google Open Source

6. **[gVisor Performance Guide](https://gvisor.dev/docs/architecture_guide/performance/)** (2024)
   - Google gVisor Documentation

7. **[The True Cost of Containing: A gVisor Case Study](https://www.usenix.org/system/files/hotcloud19-paper-young.pdf)** (2019)
   - E. Young et al.
   - *USENIX HotCloud*

8. **[Running gVisor in Production at Scale in Ant](https://gvisor.dev/blog/2021/12/02/running-gvisor-in-production-at-scale-in-ant/)** (2021)
   - Ant Group Engineering Team

9. **[Optimizing seccomp Usage in gVisor](https://gvisor.dev/blog/2024/02/01/seccomp/)** (2024)
   - Google gVisor Team

10. **[gVisor Improves Performance with Root Filesystem Overlay](https://opensource.googleblog.com/2023/04/gvisor-improves-performance-with-root-filesystem-overlay.html)** (2023)
    - Google Open Source Blog

11. **[Kubernetes RuntimeClass Documentation](https://kubernetes.io/docs/concepts/containers/runtime-class/)** (2024)
    - Kubernetes Documentation

12. **[Container Security Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)** (2024)
    - OWASP Foundation
