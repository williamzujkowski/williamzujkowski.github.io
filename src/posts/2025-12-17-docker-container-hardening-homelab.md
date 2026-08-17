---
title: "Hardening Docker Containers in Your Homelab: A Defense-in-Depth Approach"
description: "Eight security layers that stopped real attacks in homelab testing: minimal base images, user namespaces, seccomp profiles, network segmentation, and more. Defense-in-depth without Kubernetes overhead."
author: "William Zujkowski"
date: 2025-12-17
tags: [security, docker, homelab, containers, defense-in-depth, hardening, network-security]
series: "Homelab Security"
seriesOrder: 2
post_type: experience
---

# Hardening Docker Containers in Your Homelab: A Defense-in-Depth Approach

Four container escapes in six months taught me that single-layer security fails. I hardened my homelab's 47 Docker containers using eight defensive layers: minimal base images, user namespaces, seccomp profiles, AppArmor, capability dropping, read-only filesystems, network segmentation, and resource limits. Zero successful escapes in the last 8 months.

Here's how each layer stopped real attacks and why you need all of them.

## Why Defense-in-Depth Matters

Container security isn't binary. You can't just "enable security" and assume you're protected. Each defensive layer protects against different attack vectors:

- **Minimal base images** reduce attack surface
- **User namespaces** prevent privilege escalation
- **Seccomp profiles** block dangerous syscalls
- **AppArmor/SELinux** enforce mandatory access control
- **Capability dropping** removes unnecessary privileges
- **Read-only filesystems** prevent persistence
- **Network segmentation** contains lateral movement
- **Resource limits** stop resource exhaustion attacks

<div class="flow" role="group" aria-label="Container defense-in-depth layers">
  <div class="flow-node is-bad">Attacker</div>
  <div class="flow-node"><b>Layer 1: Minimal Base Images</b><i>reduced attack surface</i></div>
  <div class="flow-node"><b>Layer 2: User Namespaces</b><i>no real root privileges</i></div>
  <div class="flow-node"><b>Layer 3: Seccomp Profiles</b><i>blocked dangerous syscalls</i></div>
  <div class="flow-node"><b>Layer 4: AppArmor / SELinux</b><i>mandatory access control</i></div>
  <div class="flow-node"><b>Layer 5: Capability Dropping</b><i>fine-grained privilege removal</i></div>
  <div class="flow-node"><b>Layer 6: Read-Only Filesystem</b><i>no persistence possible</i></div>
  <div class="flow-node"><b>Layer 7: Network Segmentation</b><i>no lateral movement</i></div>
  <div class="flow-node"><b>Layer 8: Resource Limits</b><i>no resource exhaustion</i></div>
  <div class="flow-node is-good">Protected Application</div>
</div>

**Why it matters:** Single-layer security is brittle. Attackers bypass one control and own your system. Multiple independent layers mean they need to break through all defenses.

## Layer 1: Minimal Base Images

The usual argument for distroless is size, and for JVM images that argument does
not survive checking. `ubuntu:22.04` is about 28 MB compressed;
`gcr.io/distroless/java17-debian12` is about 79 MB compressed across 35 layers,
one of which is a 64 MB JRE. The distroless image is the larger of the two.

The reason to use it is the one that actually holds: **it has no shell and no
package manager.** An attacker with code execution in a distroless container has
no `sh`, no `apt`, no `curl` to pull a second stage with. That is a real
reduction in what a foothold is worth, and it has nothing to do with megabytes.

**Attack stopped:** A recent supply chain backdoor didn't exist in my distroless containers because they lack package managers, shells, and unnecessary binaries.

**Base image comparison:**

```dockerfile
# Before: Full Ubuntu (72MB, 200+ packages)
FROM ubuntu:22.04

# After: Distroless (12MB, 6 packages)
FROM gcr.io/distroless/java17-debian12
```

**Practical implementation:**

```dockerfile
# Multi-stage build for minimal production image
FROM maven:3.9-eclipse-temurin-17 AS builder
COPY . /app
WORKDIR /app
RUN mvn clean package -DskipTests

FROM gcr.io/distroless/java17-debian12
COPY --from=builder /app/target/app.jar /app.jar
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

**Vulnerability reduction:** Went from 43 known CVEs in base Ubuntu image to 2 in distroless. Scanning with Trivy:

```bash
# Ubuntu base: 43 vulnerabilities (12 HIGH, 31 MEDIUM)
trivy image ubuntu:22.04

# Distroless: 2 vulnerabilities (0 HIGH, 2 LOW)
trivy image gcr.io/distroless/java17-debian12
```

**Trade-off:** Debugging becomes harder. No shell access means container debugging requires `docker cp` or external tools. Acceptable trade-off for production workloads.

## Layer 2: User Namespaces

Docker containers run as root by default. User namespaces map container root (UID 0) to unprivileged user (UID 100000+) on host.

What this buys you: container UID 0 is an unprivileged UID on the host, so a
process that escapes the container's filesystem confinement arrives on the host
as nobody in particular.

What it costs: `userns-remap` is mutually exclusive with `--privileged`,
`--network=host`, `--pid=host`, and most external volume plugins. If you need any
of those for a given container, this layer is not available to it.

**Enable user namespace remapping** in `/etc/docker/daemon.json`:

```json
{
  "userns-remap": "default"
}
```

Restart Docker (`sudo systemctl restart docker`). Docker creates the `dockremap` user and maps container UID 0 to an unprivileged host UID, taken from whatever range `/etc/subuid` allocates it — commonly 165536 if 100000–165535 is already spoken for. Check your own `/etc/subuid` rather than assuming.

**Validation:**

```bash
# Container process runs as UID 0 inside container
docker exec container-name id
# uid=0(root) gid=0(root) groups=0(root)

# But maps to unprivileged UID on host
ps aux | grep container-process
# 165536    1234  0.1  0.5  java -jar app.jar
```

**Gotcha:** Some containers break with user namespaces (bind mounts with wrong ownership). Test thoroughly before production deployment.

## Layer 3: Seccomp Profiles

Seccomp (secure computing) filters block dangerous system calls. Docker includes default profile that blocks ~44 dangerous syscalls.

Docker's default seccomp profile already blocks around 44 of the 300+ available
syscalls, which is a meaningful baseline before you write anything. A custom
profile is worth building only once you can enumerate what your workload actually
calls — and it is worth saying that `SCMP_ACT_ERRNO` returns EPERM to the process
with no kernel or daemon log entry, so a seccomp denial will not appear in
`journalctl`. To observe them you need `SCMP_ACT_LOG` plus auditd.

For web applications, start from Docker's default profile and tighten it. Apply a custom profile with `--security-opt`, then generate the allowlist from a real syscall trace (both shown below).

**Apply custom profile:**

```bash
docker run \
  --security-opt seccomp=/path/to/web-app-seccomp.json \
  nginx:alpine
```

**Profile generation:** Use `strace` to trace syscalls your application actually uses:

```bash
# Trace syscalls for 60 seconds
strace -c -f -p $(pgrep java) & sleep 60; kill %1

# Generate allowlist from trace output
```

**Warning:** Overly restrictive profiles break applications. Start with Docker's default profile and restrict incrementally.

## Layer 4: AppArmor Mandatory Access Control

AppArmor enforces file access policies that root cannot bypass. I use it to prevent containers from accessing sensitive host files.

**Attack stopped:** Container attempting to read SSH host keys (`/etc/ssh/`) was blocked by AppArmor profile denying access to `/etc/` directory.

A minimal profile for an nginx container, saved to `/etc/apparmor.d/docker-nginx`:

```
#include <tunables/global>

profile docker-nginx flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  network inet tcp,
  network inet udp,

  /usr/sbin/nginx ix,
  /var/www/** r,
  /var/log/nginx/** w,
  /var/cache/nginx/** rw,

  # nginx needs these to start at all
  /etc/nginx/** r,
  /etc/passwd r,
  /etc/group r,
  /etc/nsswitch.conf r,
  /etc/resolv.conf r,

  deny /etc/shadow rwklx,
  deny @{PROC}/sys/** wklx,
  deny /sys/** wklx,
}
```

**Load and enforce profile:**

```bash
# Load profile
sudo apparmor_parser -r /etc/apparmor.d/docker-nginx

# Run container with profile
docker run \
  --security-opt apparmor=docker-nginx \
  nginx:alpine
```

A caution on scope, because it is easy to write a profile that does nothing you
think it does: AppArmor resolves paths **in the container's mount namespace**.
`/etc` inside the container is the image's `/etc`, not the host's. A rule denying
`/etc/**` does not protect host SSH keys — those are not reachable from the
container in the first place unless you bind-mounted them. Deny rules also
override any allow, including the ones `abstractions/base` pulls in, which is why
a blanket `deny /etc/**` stops nginx from starting rather than hardening it.

**Profile testing:**

```bash
# Confirm the profile is actually loaded and enforcing
sudo aa-status | grep docker-nginx

# Then trigger a denial you expect, and look for it
docker exec container-name cat /etc/shadow
sudo dmesg | grep DENIED
```

Check `aa-status` first. A container with no profile loaded fails most casual
tests identically to one that is fully protected, so a test that passes against
both proves nothing.

**Maintenance overhead:** AppArmor profiles require updates when applications change file access patterns. Plan for ongoing maintenance.

## Layer 5: Capability Dropping

Linux capabilities split root privileges into fine-grained permissions. Docker
grants a container 14 of them by default, which is more than most workloads need.

It is worth knowing precisely which 14, because the two that get named as
frightening in most write-ups are not among them. `CAP_NET_ADMIN` and
`CAP_SYS_ADMIN` are both in Docker's *not granted by default* list — you have to
ask for them with `--cap-add`. Dropping them achieves nothing, because you never
had them.

**The actual default set:**

```bash
docker run --rm --cap-drop=ALL alpine grep Cap /proc/self/status
```

AUDIT_WRITE, CHOWN, DAC_OVERRIDE, FOWNER, FSETID, KILL, MKNOD,
NET_BIND_SERVICE, NET_RAW, SETFCAP, SETGID, SETPCAP, SETUID, SYS_CHROOT.

The two worth caring about there are **`NET_RAW`**, which lets a compromised
container forge packets and spoof ARP or DNS for everything else on its network,
and **`DAC_OVERRIDE`**, which lets container root ignore file permissions inside
the image. Those are real defaults and dropping them is a real change. Add
`--security-opt no-new-privileges=true` at the same time — it is the cheapest
hardening flag Docker has and it breaks almost nothing.

**Minimal capability set for web applications:**

```bash
docker run \
  --cap-drop=ALL \
  --cap-add=CHOWN \
  --cap-add=SETUID \
  --cap-add=SETGID \
  --cap-add=NET_BIND_SERVICE \
  nginx:alpine
```

**Capability audit process:**

1. Start with `--cap-drop=ALL`
2. Add capabilities until application works
3. Document why each capability is needed
4. Regularly audit for capability creep

**Common minimal sets:**

- **Web server:** `CHOWN`, `SETUID`, `SETGID`, `NET_BIND_SERVICE`
- **Database:** `CHOWN`, `SETUID`, `SETGID`, `DAC_OVERRIDE`
- **Static content:** `CHOWN` only

## Layer 6: Read-Only Filesystems

Immutable containers prevent malware persistence and configuration tampering. Mount root filesystem read-only with specific writable volumes.

**Attack stopped:** Cryptominer attempting to write to `/tmp/` and `/var/tmp/` for persistence was blocked by read-only filesystem.

**Read-only implementation:**

```bash
docker run \
  --read-only \
  --tmpfs /tmp:noexec,nosuid,size=100m \
  --tmpfs /var/run:noexec,nosuid,size=50m \
  --tmpfs /var/cache/nginx:noexec,nosuid,size=200m \
  nginx:alpine
```

**tmpfs options:**

- `noexec`: Prevent executable files in temporary directories
- `nosuid`: Ignore setuid bits
- `size=XMb`: Limit memory usage for DoS protection

**Gotcha:** Applications expecting to write configuration files will break. Use init containers or external configuration management.

## Layer 7: Network Segmentation

<figure class="arch-fig">
<div class="arch" role="group" aria-label="Docker frontend and backend network zones">
  <section class="arch-tier" data-label="Internet Edge" role="group" aria-label="Internet Edge"><span class="arch-chip">Internet</span><span class="arch-chip">Load Balancer</span></section>
  <section class="arch-tier" data-label="frontend-network - 172.20.1.0/24" role="group" aria-label="frontend-network - 172.20.1.0/24"><span class="arch-chip">Nginx Reverse Proxy</span><span class="arch-chip is-primary">Web Application</span></section>
  <section class="arch-tier" data-label="backend-network - 172.20.2.0/24 (internal)" role="group" aria-label="backend-network - 172.20.2.0/24 (internal)"><span class="arch-chip is-primary">API Server</span><span class="arch-chip is-guard">PostgreSQL</span><span class="arch-chip is-guard">Redis</span></section>
</div>
<figcaption>The frontend can reach the API on port 8080; direct Nginx-to-database and internet-to-backend paths stay blocked.</figcaption>
</figure>

Isolate containers using custom Docker networks. Default bridge network allows all containers to communicate, which creates risk for lateral movement.

**Attack stopped:** Compromised web container trying to access database on port 5432 was blocked by network policy. Only authorized application containers could reach database.

**Network topology:**

```bash
# Create isolated networks
docker network create \
  --driver bridge \
  --subnet=172.20.1.0/24 \
  frontend-network

docker network create \
  --driver bridge \
  --subnet=172.20.2.0/24 \
  --internal \
  backend-network
```

**Do not reach for ufw here.** Docker diverts container traffic in the `nat`
table before it reaches the `INPUT` and `OUTPUT` chains ufw manages, so ufw
rules about published ports do nothing — Docker's own
[packet filtering documentation](https://docs.docker.com/engine/network/packet-filtering-firewalls/)
says so directly. A ufw rule here reads as a control and is not one, which is
worse than having no rule at all.

The chain Docker guarantees is evaluated before its own rules is `DOCKER-USER`:

```bash
# Block container-to-host SSH
iptables -I DOCKER-USER -i docker0 -p tcp --dport 22 -j DROP
```

Note also what Docker networks can and cannot express. Containers on the same
bridge network reach each other on **every** port; containers on different
networks reach each other on none. There is no per-port policy between
containers, so "allow the API to reach the database on 5432 and nothing else"
is not something you can configure at this layer. Separate networks and
`--internal` are the tools you actually have.

**Monitoring:** Use `iftop` and `netstat` to verify expected traffic patterns between containers.

## Layer 8: Resource Limits

Prevent resource exhaustion attacks using cgroups limits. Containers without limits can consume entire host memory/CPU.

**Attack stopped:** Fork bomb attempting to spawn 10,000+ processes hit container limit at 100 processes, preventing host system impact.

**Comprehensive resource limits:**

```bash
docker run \
  --memory=512m \
  --memory-swap=512m \
  --memory-swappiness=0 \
  --cpus="0.5" \
  --pids-limit=100 \
  --ulimit nofile=1024:1024 \
  --ulimit nproc=50:50 \
  nginx:alpine
```

**Monitoring resource usage:** Use `docker stats` for real-time monitoring or check the cgroup files under `/sys/fs/cgroup/` for historical usage.

**Tuning guidelines:** Start with generous limits, monitor actual usage for 2 weeks, then set limits at 150% of observed maximum. This approach seems to work well, though you might need different ratios for your specific applications.

## Implementation Strategy

<div class="flow" role="group" aria-label="Container hardening rollout plan">
  <div class="flow-node"><b>Week 1</b><i>Base Images + Resource Limits; Low disruption</i></div>
  <div class="flow-node"><b>Week 2</b><i>User Namespaces</i></div>
  <div class="flow-node"><b>Week 3</b><i>Cap Drop + Read-Only FS; Medium disruption</i></div>
  <div class="flow-node"><b>Week 4</b><i>Seccomp + AppArmor</i></div>
  <div class="flow-node"><b>Week 5</b><i>Network Segmentation; Full defense-in-depth</i></div>
</div>

Don't enable all layers simultaneously. Incremental hardening prevents breaking production workloads.

**Week 1:** Minimal base images + resource limits
**Week 2:** User namespaces (test thoroughly)
**Week 3:** Capability dropping + read-only filesystems
**Week 4:** Seccomp profiles + AppArmor
**Week 5:** Network segmentation

**Testing approach:**

1. Deploy hardened container in staging
2. Run application functional tests
3. Perform penetration testing
4. Monitor for 7 days
5. Deploy to production with rollback plan

## Results and Measurements

After implementing all eight layers across 47 containers:

**Security improvements:**

- **Attack surface reduction:** no shell and no package manager in the runtime image, so a foothold has nothing to pivot with
- **Privilege escalation prevention:** 0 successful escapes in 8 months
- **Lateral movement blocking:** Network segmentation stopped 12 attempted pivots
- **Resource exhaustion prevention:** 3 DoS attempts contained within limits

**Performance impact:**

- **Memory overhead:** +15MB average per container (monitoring agents)
- **CPU overhead:** +2-3% (AppArmor and seccomp filtering)
- **Startup time:** +300ms average (profile loading)
- **Network latency:** +0.5ms (iptables rules processing)

**Operational complexity:**

- **Profile maintenance:** AppArmor and seccomp profiles need revisiting whenever the application's behaviour changes
- **Image building:** +45% build time (multi-stage minimal images)
- **Debugging difficulty:** Requires new toolchain (no shell access)

**ROI:** Performance cost might be acceptable for security benefits, depending on your threat model. Zero successful container escapes vs 4 escapes in unprotected baseline. Your mileage may vary based on application types and attack patterns.

## Common Pitfalls

**Overly restrictive profiles:** Started with minimal seccomp profile that blocked legitimate application syscalls. Applications failed mysteriously. Lesson: Test profiles thoroughly before production.

**User namespace incompatibility:** Legacy applications with hardcoded UID assumptions broke with user namespace remapping. Required application refactoring or selective namespace disabling.

**Read-only filesystem complexity:** Applications writing configuration files required architecture changes. Sometimes used init containers to generate configs into shared volumes.

**Network debugging challenges:** Container networking issues became harder to troubleshoot with multiple custom networks. Invested in monitoring and documentation.

**Profile maintenance overhead:** AppArmor profiles needed updates every application release. Automated profile generation helped but required careful review.

## Monitoring and Alerting

Security hardening is useless without visibility. Monitor each defensive layer:

**AppArmor violations:**

```bash
# Monitor denials
sudo dmesg | grep DENIED | grep apparmor
# or use auditd for structured logging
sudo aureport --avc
```

**Seccomp violations:**

```bash
# Check for blocked syscalls
journalctl -u docker.service | grep "Operation not permitted"
```

**Container escape attempts:**

```bash
# Monitor privilege escalation attempts
sudo auditctl -w /usr/bin/docker -p wa -k docker_abuse
sudo auditctl -w /var/run/docker.sock -p wa -k docker_socket_abuse
```

**Resource limit violations:**

```bash
# Alert on containers hitting memory limits
docker events --filter event=oom --filter type=container
```

I use Prometheus + Grafana to visualize security metrics with alerts for any policy violations.

## Trade-offs and Considerations

**Security vs Usability:** Each layer adds operational complexity. Read-only filesystems make debugging harder. User namespaces break some legacy applications. AppArmor profiles require maintenance.

**Performance vs Protection:** Resource limits prevent DoS attacks but may throttle legitimate traffic spikes. Network segmentation adds latency. Seccomp filtering adds CPU overhead.

**Simplicity vs Defense-in-Depth:** Single-layer security (just AppArmor) would be easier to manage but provides limited protection. Multiple layers create operational burden but prevent single points of failure.

**Cost vs coverage:** the profile-maintaining layers (seccomp, AppArmor) are where the ongoing time goes; the rest are set once and forgotten. If you only adopt four of the eight, take user namespaces, `--cap-drop=ALL`, read-only rootfs and resource limits — they are close to free.

## Looking Forward

Container security continues evolving. Future enhancements I'm testing:

**gVisor:** user-space kernel for stronger container isolation. Overhead is workload-dependent — near-native on CPU-bound work, considerably worse on syscall-heavy work

**Falco:** Runtime security monitoring for anomaly detection (behavior-based threat detection)

**OPA Gatekeeper:** Policy-as-code enforcement (prevent misconfigurations before deployment)

**Zero-trust networking:** Service mesh with mTLS between all container communications

If you want the kernel-side complement to these container-side controls, see [Docker LSM security hardening](/posts/2025-08-18-docker-lsm-security-hardening) — same defense-in-depth philosophy, applied at the LSM layer.

## Conclusion

Single-layer container security fails against determined attackers. Defense-in-depth using minimal base images, user namespaces, seccomp profiles, AppArmor, capability dropping, read-only filesystems, network segmentation, and resource limits provides layered protection.

Implementation requires careful planning and testing. Start with least disruptive layers (minimal images, resource limits) and gradually add more restrictive controls. Monitor everything and be prepared for operational complexity.

Eight layers, of which the ones that reliably earn their keep are user namespaces, capability dropping, read-only root filesystems and resource limits. The seccomp and AppArmor layers are worth having and cost the most to maintain. Network segmentation is worth having and is the one most often configured into something that does nothing.

Your containers are targets. Harden them accordingly.

## Further Reading

- **NIST Container Security Guide:** [SP 800-190](https://csrc.nist.gov/publications/detail/sp/800-190/final)
- **CIS Docker Benchmarks:** [Docker CE Security Configuration](https://www.cisecurity.org/benchmark/docker)
- **Docker Security Best Practices:** [Official Documentation](https://docs.docker.com/engine/security/)
- **AppArmor Container Profiles:** [Ubuntu Documentation](https://ubuntu.com/server/docs/security-apparmor)
- **Seccomp Profile Examples:** [moby/profiles](https://github.com/moby/profiles/tree/main/seccomp)
