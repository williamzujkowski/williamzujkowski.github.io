---
author: William Zujkowski
date: 2025-08-18
description: Harden container security with Docker and K3s best practices—implement rootless containers, seccomp profiles, and image scanning for Kubernetes production workloads.
  in a homelab environment, from base image selection to runtime security monitoring
tags:
- security
- containers
- docker
- kubernetes
- homelab
- devops
title: Container Security Hardening in My Homelab
images:
  hero:
    src: /assets/images/blog/hero/2025-08-18-container-security-hardening-homelab-hero.jpg
    alt: cybersecurity concept illustration for Container Security Hardening in My
      Homelab
    caption: Visual representation of Container Security Hardening in My Homelab
    width: 1200
    height: 630
  og:
    src: /assets/images/blog/hero/2025-08-18-container-security-hardening-homelab-og.jpg
    alt: cybersecurity concept illustration for Container Security Hardening in My
      Homelab
---
## The Wake-Up Call

![Container security concept with locks and shields](https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1920&q=80)
*Photo by Timelab Pro on Unsplash*

In July 2025, I tested container escape techniques in my homelab. I ran a privileged container with the `--privileged` flag to see what could go wrong. Using `nsenter`, I achieved host filesystem access in under 3 minutes. That scared me enough to audit my 47 running containers.

I found 12 containers running with unnecessary privileges. A few years back, I'd been careless with a test web app container, skipping security best practices because "it's just for testing." A month later, I discovered it was mining cryptocurrency. The attacker got in through an outdated nginx base image with CVE-2019-9511 (CVSS 7.5).

That mistake taught me container security isn't optional, even in a homelab. **However**, learning what "hardened" actually means required breaking things repeatedly.

## Container Security Architecture

```mermaid
flowchart TB
    subgraph buildtimesecurity["Build Time Security"]
        Base[Base Image Selection]
        Scan[Vulnerability Scanning]
        Secrets[Secrets Management]
        Build[Secure Build Process]
    end
    subgraph runtimesecurity["Runtime Security"]
        Runtime[Runtime Protection]
        Network[Network Policies]
        Resources[Resource Limits]
        Monitor[Continuous Monitoring]
    end
    subgraph defenselayers["Defense Layers"]
        AppArmor[AppArmor/SELinux]
        Seccomp[Seccomp Profiles]
        Capabilities[Capability Dropping]
        RO[Read-Only Filesystems]
    end

    Base --> Scan
    Scan --> Secrets
    Secrets --> Build

    Build --> Runtime
    Runtime --> Network
    Network --> Resources
    Resources --> Monitor

    Runtime --> AppArmor
    Runtime --> Seccomp
    Runtime --> Capabilities
    Runtime --> RO

    classDef criticalNode fill:#f44336,color:#fff
    classDef warningNode fill:#ff9800,color:#fff
    classDef successNode fill:#4caf50,color:#fff

    class Scan criticalNode
    class Runtime warningNode
    class Monitor successNode
```

Today, my homelab runs 47 containers across Docker and K3s with layered security controls. Here's how I hardened them, including the failures that taught me the most.

## The Foundation: Base Image Selection

Your security posture starts with the base image. I learned this through painful trial and error.

### The nginx:alpine Migration Disaster

I ran vulnerability scans with Grype across my 12 primary images in August 2025. The results were sobering:
- nginx:latest had 42 CVEs (7 HIGH, 2 CRITICAL)
- postgres:15 had 31 CVEs (5 HIGH)
- Total across all images: 178 CVEs

I switched from `nginx:latest` to `nginx:alpine` to reduce the attack surface. The image size dropped from 142MB to 41MB (71% reduction), and CVE count fell to 6. **But** three of my custom nginx modules broke immediately because alpine uses musl libc instead of glibc. I spent 8 hours recompiling modules and debugging segfaults before I got the site working again.

**The trade-off**: Alpine images are smaller and have fewer vulnerabilities, **yet** they may lack libraries your app expects. Test thoroughly.

### Minimal Base Images

Choosing the right base image significantly impacts your attack surface:

<script src="https://gist.github.com/williamzujkowski/42e9323a7b2cefb6d88bd12e306debfd.js"></script>

**Why distroless?** No shell, no package manager, no utilities. Just your application binary. An attacker with code execution can't pivot because there's nothing to execute. I think this is the single most effective hardening technique, **though** it makes debugging significantly harder (no shell means no `docker exec` troubleshooting).

### Image Verification

Always verify image signatures to prevent supply chain attacks:

<script src="https://gist.github.com/williamzujkowski/85bc2f174d54f6f1e080f2ce2ed0266b.js"></script>

## Build-Time Security

### Multi-Stage Builds

Separate build dependencies from runtime to minimize attack surface:

<script src="https://gist.github.com/williamzujkowski/1f42aca62d981a71aeb28d2389f5ca2f.js"></script>

This approach:
- Removes build tools from final image
- Reduces image size by 90%+ (I've seen 340MB drop to 28MB)
- Limits attack surface dramatically

**The trade-off**: Multi-stage builds are more secure, **but** they complicate local development. I keep a `Dockerfile.dev` with a full base image for debugging, and use the hardened multi-stage build for production.

### Vulnerability Scanning Pipeline

I scan every image before deployment using Grype. This saved me from deploying a Node.js image with CVE-2023-30581 (CVSS 9.8, remote code execution) in September 2025.

<script src="https://gist.github.com/williamzujkowski/b74f50dae6a9bc1e28c9dd66b7c7682e.js"></script>

### Secrets Management: My Docker Hub Disaster

In June 2025, I made a catastrophic mistake. I hardcoded database credentials in a Dockerfile (yes, I know better). I built the image and pushed it to Docker Hub's public registry without thinking. Within 4 hours, the image had 23 pulls from IPs I didn't recognize (confirmed via Docker Hub analytics).

I immediately:
1. Revoked all database credentials (10 minutes)
2. Deleted the image from Docker Hub (2 minutes)
3. Rotated API keys for 6 affected services (45 minutes)
4. Audited all other images for secrets (2 hours)

**Never bake secrets into images.** Use secret injection at runtime:

<script src="https://gist.github.com/williamzujkowski/42401bccef5d92145c452c1bcbf2a047.js"></script>

## Runtime Security

### User Namespaces: The Permission Nightmare

I enabled user namespace remapping in Docker daemon.json in July 2025. I thought it would be straightforward. It wasn't.

Within 10 minutes of restarting Docker, 8 of my 23 services failed with permission errors:
- PostgreSQL couldn't write to `/var/lib/postgresql/data`
- Redis couldn't access `/data`
- Nginx couldn't bind to port 80 (even though I mapped it)

I spent 2 days debugging volume mount permissions. User namespace remapping maps root inside the container to a non-privileged UID on the host (typically 100000+). My bind mounts had wrong ownership on the host.

The fix involved running `chown -R 100000:100000` on all Docker volumes. **The trade-off**: User namespaces provide strong isolation **but** break existing deployments and complicate permission management. I'm not sure the security benefit is worth the operational complexity for a homelab. **Probably** makes more sense in multi-tenant production environments.

### Non-Root Execution

Run containers as non-root users to limit privilege escalation:

<script src="https://gist.github.com/williamzujkowski/8535f615dd34bb4af5d8140b684dac3c.js"></script>

Enable user namespace remapping in Docker (warning: this will break things):

<script src="https://gist.github.com/williamzujkowski/4f47cc3ed04d0fc86f0c7ab834801c1b.js"></script>

**Note**: Only enable this if you're prepared for significant troubleshooting. Test on non-critical services first.

### Capability Dropping

Drop unnecessary Linux capabilities to enforce least privilege:

<script src="https://gist.github.com/williamzujkowski/438af483fa09e6562fdf02663245415f.js"></script>

For K3s pods:

<script src="https://gist.github.com/williamzujkowski/d33270b316cfdf2db0ef4689ae1f0cb5.js"></script>

### Network Policies: The Debugging Trap

I segmented my K3s containers into 5 separate Docker networks in July 2025 to enforce isolation:
- `frontend` (Nginx, web apps)
- `backend` (APIs, application servers)
- `data` (PostgreSQL, Redis)
- `monitoring` (Prometheus, Grafana)
- `security` (Wazuh, Falco)

Default deny all traffic between networks. **The trade-off**: Redis on the `data` network couldn't talk to the webapp on the `backend` network, which I intended. **However**, when the webapp started throwing 500 errors, it took me 3 hours to realize it was a network policy issue, not an application bug.

I added explicit network links between `backend` and `data`, which **probably** reduced my isolation by 30% (rough estimate based on the attack surface increase). Perfect security makes debugging nearly impossible.

### Zero-Trust Networking in K3s

Here's how I balance security with usability:

<script src="https://gist.github.com/williamzujkowski/e1fe286b78df31a6e7272de0a948a163.js"></script>

### Resource Limits

Prevent resource exhaustion attacks:

<script src="https://gist.github.com/williamzujkowski/762ac3185fb99798cca0fd42ce728976.js"></script>

## Advanced Hardening

### AppArmor Profiles: 14 Iterations of Failure

I wrote a custom AppArmor profile for my Nginx container in August 2025. I thought I understood AppArmor. I didn't.

**Attempt 1-5**: Profile too restrictive. Blocked legitimate operations:
- Log writes to `/var/log/nginx` (access denied)
- PID file creation in `/var/run` (permission denied)
- Config reload via signals (operation not permitted)

**Attempt 6-10**: Profile too permissive. Allowed things I wanted to block:
- Network socket creation beyond HTTP/HTTPS
- File writes outside intended directories
- Execution of shell commands (why does Nginx need this?)

**Attempt 11-14**: Gradual refinement. Took 3 days total to get a profile that was both secure and functional. I logged every denied operation with `auditd`, analyzed the logs, and incrementally allowed only necessary operations.

**The lesson**: AppArmor adds defense in depth, **but** requires extensive testing and iteration. Start with Docker's default profile and tighten gradually.

### Custom AppArmor Profile

Here's my battle-tested Nginx profile (after 14 iterations):

<script src="https://gist.github.com/williamzujkowski/48b62cc12f3954b2b9a48f4ee3be51ae.js"></script>

### Read-Only Root Filesystem: 6 Hours of Refactoring

In September 2025, I made my FastAPI container's root filesystem read-only with the `--read-only` flag. The container crashed immediately with:

```
OSError: [Errno 30] Read-only file system: '/tmp/cache'
```

The app was writing to:
- `/tmp` for temporary request data
- `/app/cache` for computed results
- `/var/log/app` for application logs

I spent 6 hours refactoring:
1. Changed temp file usage to in-memory buffers (4 hours of code changes)
2. Moved cache to Redis instead of local disk (1 hour)
3. Switched logging to stdout/stderr instead of files (30 minutes)
4. Added tmpfs mounts for unavoidable temp files (30 minutes)

**The trade-off**: Read-only root filesystem prevents persistence attacks, **yet** requires significant application changes. Not all apps can be easily adapted. I'm still learning which workloads benefit most from this control.

### Read-Only Root Configuration

Mount root filesystem as read-only:

<script src="https://gist.github.com/williamzujkowski/ae734fa07c6018017c2eb836b2cd28ff.js"></script>

## Continuous Monitoring

### Runtime Security with Falco

Install Falco for runtime threat detection:

<script src="https://gist.github.com/williamzujkowski/1518c584a50e706aa0bfa6807dde8d95.js"></script>

### Log Aggregation and Analysis

Ship container logs to Wazuh:

<script src="https://gist.github.com/williamzujkowski/ecaf4fb3899e4c9f153eaf4abdd1676b.js"></script>

## Compliance and Auditing

### CIS Benchmark Scanning

Use automated tools to audit container security against CIS benchmarks:

<script src="https://gist.github.com/williamzujkowski/2b88c8b46eb919ca4563dfc314977cdd.js"></script>

### Admission Controllers

Enforce policies with OPA Gatekeeper:

<script src="https://gist.github.com/williamzujkowski/619d1992d4c487a6f1b1bc3a191664e4.js"></script>

## Lessons Learned from Breaking Things

After hardening 47 containers in my homelab (and breaking many of them):

### 1. Security is Layers, Not a Single Wall
No single control prevents all attacks. I've learned that combining image scanning (178 CVEs found), runtime protection (AppArmor, seccomp), network policies (5 isolated networks), and monitoring (Falco, Wazuh) provides real defense. **However**, each layer adds operational complexity. The **trade-off** between security and maintainability is constant.

### 2. Hardening Always Breaks Something First
User namespace remapping broke 8 of 23 services. Read-only root broke my FastAPI app. AppArmor took 14 iterations to get right. **Every** security control I enabled required troubleshooting and refactoring. Budget time for this, **probably** 2-3x your initial estimate.

### 3. Vulnerability Scanning Creates Alert Fatigue
Finding 178 CVEs across 12 images sounds useful, **but** 89% were LOW or MEDIUM severity in packages I don't even use. I set my threshold to HIGH+ only, which reduced alerts by 74%. **The trade-off**: I **might be** missing important medium-severity issues in core dependencies.

### 4. Perfect Security Makes Debugging Impossible
Network policies that deny all traffic by default are great for security, terrible for troubleshooting. Distroless images with no shell make `docker exec` useless. I keep a `debug` variant of each critical container with a shell for emergencies. **The trade-off**: Debug containers are less secure **but** massively more debuggable.

### 5. Some Hardening Isn't Worth the Cost
User namespace remapping provides strong isolation, **but** the 2 days I spent fixing permissions **probably** outweighs the security benefit for my single-tenant homelab. I've since disabled it. **The trade-off**: Not every security control makes sense for every environment. Context matters.

### 6. Automation Catches What I Miss
My Grype scans in CI/CD blocked a Node.js image with CVE-2023-30581 (CVSS 9.8) from deploying. I would have missed it manually. Automate image scanning, **probably** the highest ROI security investment I've made.

### 7. Test Your Defenses
I use [botb](https://github.com/brompwnie/botb) to test container escape paths quarterly. My privileged container escape test (3 minutes to host access) revealed real vulnerabilities I thought I'd fixed. Regular testing is the only way to verify your hardening actually works.

## Practical Checklist

Before deploying any container:

- [ ] Use minimal base images (Alpine, distroless)
- [ ] Scan for vulnerabilities (Grype, Trivy)
- [ ] Run as non-root user
- [ ] Drop all unnecessary capabilities
- [ ] Enable read-only root filesystem
- [ ] Set resource limits (CPU, memory)
- [ ] Use secrets management (not environment variables)
- [ ] Apply network policies (default deny)
- [ ] Enable security profiles (AppArmor, seccomp)
- [ ] Configure logging and monitoring
- [ ] Test container escape scenarios

## Research & References

### Container Security Standards

1. **[CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)** - Docker security best practices
   - Center for Internet Security

2. **[CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)** - Kubernetes security hardening guide
   - Center for Internet Security

### Academic Research

1. **[Container Security: Issues, Challenges, and the Road Ahead](https://ieeexplore.ieee.org/document/7966067)** (2017)
   - IEEE Access: Comprehensive container security analysis

2. **[Analysis of Docker Security](https://arxiv.org/abs/1804.05039)** (2018)
   - arXiv preprint: Docker attack surface analysis

### Security Tools

- **[Anchore Grype](https://github.com/anchore/grype)** - Vulnerability scanner
- **[Aqua Trivy](https://github.com/aquasecurity/trivy)** - Multi-purpose security scanner
- **[Falco](https://falco.org/)** - Runtime security monitoring
- **[OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/)** - Policy enforcement

### Best Practices Guides

- **[Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)** - OWASP
- **[Kubernetes Security Overview](https://kubernetes.io/docs/concepts/security/)** - Official docs
- **[NSA Kubernetes Hardening Guide](https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF)** - NSA/CISA

## Conclusion

Container security isn't complicated, **but** it's tedious and requires iteration. Start with secure base images (distroless **probably** has the best security-to-effort ratio), scan for vulnerabilities (Grype catches 90%+ of issues), apply runtime protections (drop all capabilities by default), and monitor continuously (Falco for anomalies).

My homelab cryptocurrency mining incident taught me that "just testing" environments need security rigor too. The controls I've shared are battle-tested across my 47 Docker and K3s containers. They've caught real threats:
- 178 CVEs in vulnerable images (before scanning)
- 23 unauthorized Docker Hub pulls (secrets exposure)
- 12 unnecessarily privileged containers (reduced attack surface)
- 1 container escape test that succeeded (fixed by dropping `--privileged`)

**The big lesson**: Every hardening control broke something initially. User namespaces broke 8 services. AppArmor took 14 iterations. Read-only root required 6 hours of refactoring. **However**, each failure taught me how containers actually work, which **probably** made me a better engineer.

Security is iterative, not perfect. I'm still learning what "good enough" looks like for a homelab. Start with the basics, automate scanning, expect to break things, and improve continuously.

---

*Running containers in your homelab? What security controls have you implemented? I'd love to hear about your approach and lessons learned!*
