---

author: William Zujkowski
date: 2025-10-06
description: Build automated security scanning pipelines with Grype, OSV, and Trivy—integrate vulnerability detection into CI/CD workflows with actionable reporting.
title: Automated Security Scanning Pipeline with Grype and OSV
tags:
  - automation
  - devops
  - security
  - supply-chain
  - vulnerability-management
---
## The Dependency That Haunted Me


I built an automated security pipeline that scans every commit with Grype, OSV-Scanner, and Trivy. Tuning the three scanners cut their combined runtime from 6m 30s to 2m, and `npm audit fix` clears a useful share of findings without human involvement. Two of the three scanners fail their own job on a critical finding; the third is advisory, and the final aggregate gate is still a stub I have not implemented.

**Why it matters:** Last year, I deployed a "simple" web app to my homelab. Three months later, a critical vulnerability was discovered in a nested dependency I didn't even know existed. The vulnerable code ran there for months before a scanner told me. Hope is not a security strategy.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/scan-pipeline.png'); width: min(240px, 62%); aspect-ratio: 340/332; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">each pass finer than the last</p>

## Automated Security Pipeline Architecture

⚠️ **Warning:** Security scanning pipelines must be configured with appropriate policies and approval gates. Automated remediation should include review processes for production environments.

<div class="flow" role="group" aria-label="Automated security scanning pipeline">
  <div class="flow-parallel" role="group" aria-label="Runs in parallel">
    <div class="flow-node">Git Push</div>
    <div class="flow-node">Pull Request</div>
  </div>
  <div class="flow-node">GitHub Actions Trigger</div>
  <div class="flow-node">Build Stage</div>
  <div class="flow-node">Test Stage</div>
  <div class="flow-node is-gate">Security Scan Stage</div>
  <div class="flow-node"><b>OSV-Scanner</b><i>dependency scanning — runs first</i></div>
  <div class="flow-parallel" role="group" aria-label="Runs in parallel">
    <div class="flow-node"><b>Grype</b><i>container scanning</i></div>
    <div class="flow-node"><b>Trivy</b><i>multi-scanner</i></div>
  </div>
  <div class="flow-node">SARIF Reports</div>
  <div class="flow-parallel" role="group" aria-label="Runs in parallel">
    <div class="flow-node">GitHub Security</div>
    <div class="flow-node">Slack Alerts</div>
    <div class="flow-node">Wazuh SIEM</div>
  </div>
  <div class="flow-node is-gate">Quality Gates</div>
  <div class="flow-branch" role="group" aria-label="Branch outcomes">
    <div class="flow-leg" data-branch="Critical" role="group" aria-label="Critical"><div class="flow-node is-bad">Block on Critical</div></div>
    <div class="flow-leg" data-branch="Review" role="group" aria-label="Review"><div class="flow-node">Manual Review</div></div>
  </div>
</div>

Today, every commit to my repositories is automatically scanned for vulnerabilities. Here's how I built it — including the part that is not finished.

## Tool Selection and Comparison

### Why Multiple Scanners?

I tested these three scanners in September 2024 against my homelab services to understand their strengths. These tools complement my broader approach to [smart vulnerability prioritization with EPSS and KEV](/posts/2025-09-20-vulnerability-prioritization-epss-kev).

This helps me focus on what actually matters instead of raw CVE counts.

| Scanner | Strengths | Best For | My Test Results |
|---------|-----------|----------|-----------------|
| **Grype** | Fast, low false positives, container-native | Container images, compiled binaries | 3.2s scan time, found 12 CVEs |
| **OSV-Scanner** | Language-specific, lockfile parsing | npm, pip, cargo, go.mod | 8.1s scan time, found 8 CVEs (4 overlapping) |
| **Trivy** | All-in-one, config scanning | Full coverage, IaC | 42s scan time, found 15 CVEs total |

**My strategy:** Run all three, correlate findings, reduce false positives. When I tested this on my Python microservices project, Grype caught a critical vulnerability in a base image layer that OSV missed entirely.

Meanwhile, OSV found a transitive npm dependency issue that Grype didn't detect. Between them the two produced 16 distinct findings and agreed on only 4 of those — about a quarter. Whichever single scanner I had picked, I would have missed either 4 or 8 real issues.

### Installation

I installed all three scanners on my Ubuntu 22.04 homelab server. The process took about 10 minutes: `curl` script for Grype, `go install` for OSV-Scanner, and `dpkg` for Trivy's Debian package.

**Note from experience:** OSV-Scanner requires Go 1.21+. My first install failed with Go 1.19.

## GitHub Actions Integration

### Complete Scan Workflow

The pipeline orchestrates three scanners in parallel with a final quality gate:

<div class="flow" role="group" aria-label="GitHub Actions security scanning pipeline">
  <div class="flow-node">Git Push / PR</div>
  <div class="flow-node is-gate">Trigger Pipeline</div>
  <div class="flow-node"><b>OSV</b><i>dependency scan — fails job on critical</i></div>
  <div class="flow-parallel" role="group" aria-label="Runs in parallel">
    <div class="flow-node"><b>Grype</b><i>container scan — fail-build on high</i></div>
    <div class="flow-node"><b>Trivy</b><i>filesystem scan — SARIF upload</i></div>
  </div>
  <div class="flow-node">Upload SARIF</div>
  <div class="flow-node is-gate">Security Gate <i>reads each job's result</i></div>
</div>

**Key workflow features:** Triggers on push, pull requests, and daily at 2 AM UTC. SARIF reports upload to GitHub Security tab automatically. Slack notifications alert on failure.

**What blocks, precisely.** OSV's critical check exits non-zero and fails
`dependency-scan`. Grype's `fail-build: true` with `severity-cutoff: high` fails
`container-scan`. The `security-gate` job then aggregates all three.

That gate is worth looking at closely, because the obvious way to write it is
wrong in a way that is invisible:

```yaml
security-gate:
  needs: [dependency-scan, container-scan, comprehensive-scan]
  if: always()
  steps:
    - run: echo "All security scans completed"
```

`if: always()` is there so the gate still runs when an upstream job failed — you
want it to report rather than be skipped. But `always()` also means the gate
**passes** when everything upstream failed, unless it explicitly inspects the
results. A job that echoes a string and exits 0 is not a gate; it is a label
that says "gate". Mine has to read `needs.<job>.result` and exit non-zero itself,
and treat `skipped` and `cancelled` as failures rather than passes.

The scanners are not parallel, either. `container-scan` and `comprehensive-scan`
both declare `needs: dependency-scan`, so OSV runs alone first and the other two
follow. There is no matrix strategy over scanners anywhere in the file.

**Every third-party action is pinned to a commit SHA**, with the version in a
trailing comment. This matters more here than in most workflows: an action
referenced as `@master` — which is how `trivy-action` is usually documented —
means whoever controls that branch decides what runs in your CI, holding your
repository credentials. In a pipeline whose entire purpose is supply-chain
security, that is the wrong way round. Tags move too, so pin the SHA.

📎 **Full GitHub Actions workflow:**
[Complete implementation with SARIF uploads, quality gates, and Slack notifications](https://gist.github.com/williamzujkowski/8185611a406dd91806f37d51778cdd16)

### Slack Notifications

Add real-time alerts when scans fail:

📎 **Complete Slack notification workflow with formatted blocks:**
[Full implementation](https://gist.github.com/williamzujkowski/31cb8443a5a00f58568308a9b3c641fc)

The notification uses `slackapi/slack-github-action@v1.24.0` with failure condition, including repo, branch, commit SHA, and direct link to failed run.

## Local Development Integration

One lesson I learned the hard way: catching vulnerabilities in CI is good, but catching them before you even commit is better. I added pre-commit hooks after repeatedly pushing code only to have it rejected by the security gate 5 minutes later.

### Pre-Commit Hooks

Create `.pre-commit-config.yaml` with local hooks for Grype (`fail-on high`) and OSV-Scanner (`--lockfile=package-lock.json`). Install with `pip install pre-commit && pre-commit install`.

**Reality check:** These hooks add 30-45 seconds per commit. Some developers use `--no-verify` to bypass them.

No good solution exists for this yet. It's a constant tension between security and developer experience.

### VS Code Integration

Run scans directly from your IDE with custom tasks. Each task outputs JSON for easy parsing with `jq`.

📎 **Complete VS Code tasks configuration:**
[Full tasks.json with all three scanners](https://gist.github.com/williamzujkowski/a63e9adf2fa91764899517c5b40b6829)

## Advanced Scanning Configurations

### Grype Custom Configuration

Control false positives and severity thresholds.

📎 **Complete Grype configuration:**
[Full .grype.yaml with all ignore rules](https://gist.github.com/williamzujkowski/90a547307bb8d0158bcadc43b86df18f)

Configure `fail-on-severity: high` and `scope: all-layers`, and give every ignore rule a `reason`.

**Grype ignore rules do not expire.** The `IgnoreRule` struct has no `expiration` field, so a date written into `.grype.yaml` is silently ignored and the suppression is permanent. The config linked above carries `expiration: 2025-12-31` and that line has never done anything — the rule is still live. If you want time-boxed risk acceptance you have to enforce it outside grype, or use OSV-Scanner's `ignoreUntil`, which is real.

### OSV-Scanner Configuration

`osv-scanner.toml` has a much smaller schema than I originally documented here. The supported surface is `[[IgnoredVulns]]` (with `id`, `ignoreUntil`, `reason`), `[[PackageOverrides]]`, `ScanGoModVersion` and `GoVersionOverride`. There is no worker-count, scan-depth, or private-registry configuration, so there is no tuning knob to benchmark:

```toml
[[IgnoredVulns]]
id = "GHSA-1234-5678-9abc"
ignoreUntil = 2026-03-01
reason = "Vulnerable path not reachable; revisit at the date above"
```

`ignoreUntil` is the one genuine expiry mechanism across these three tools. Use it.

### Trivy policy: what it can and cannot do

Trivy's Rego support is worth understanding precisely, because it is easy to write a policy that appears to enforce a control and does the opposite.

The flag is `--ignore-policy`, and the clue is in the name: the policy **filters findings out**. It cannot deny, block, or fail a build. Trivy expects a rule named `ignore`, and the input is a single `DetectedVulnerability` object rather than a collection — so a policy written as `deny[msg]` iterating `input.Vulnerabilities[_]` never matches anything and silently evaluates to no-op.

A policy written to "deny on critical" is therefore, under the only mechanism that exists, either inert or a policy that suppresses criticals. If you want Trivy to fail a build, set `exit-code: 1` with a `severity` filter and skip Rego entirely.

## Continuous Monitoring

### Scheduled Scans

Daily automated scans catch newly-published CVEs. I scan 3 production images daily. Results go to Wazuh for trend analysis.

📎 **Complete scheduled scan workflow:**
[Full workflow with matrix strategy and SIEM integration](https://gist.github.com/williamzujkowski/4ba54b27bc5b2038bbdea88e6e14e5e2)

Configure cron schedule (`0 6 * * *` for daily 6 AM) with matrix strategy scanning multiple production images.

### Scan Comparison Script

Track vulnerability trends by detecting drift. This helped me identify 12 new CVEs in a dependency I thought was stable.

📎 **Complete scan comparison tool:**
[Full Python script with JSON parsing and reporting](https://gist.github.com/williamzujkowski/185d9d21330cf2b935c466ee27696a6b)

Compare two scan results to detect new and fixed vulnerabilities. Run with `--current today.json --baseline baseline.json`.

## SBOM Generation and Management

### Generate Software Bill of Materials

Use `syft` to generate CycloneDX SBOM, scan with `grype sbom:./sbom.json`, and compare versions with `jq` to track dependency changes.

### SBOM-Based Vulnerability Tracking

Generate and scan SBOMs on every release. I store historical SBOMs to track dependency evolution over time.

📎 **Complete SBOM workflow:**
[Full workflow with CycloneDX generation and S3 storage](https://gist.github.com/williamzujkowski/1b74fbcb94cfaccfa91151fb75287f38)

Trigger on release publication, generate CycloneDX format, scan with Grype, and upload to S3 for historical tracking.

## Remediation Workflows

### Automated Dependency Updates

Weekly auto-remediation with PR creation. `npm audit fix` clears a meaningful share of findings on its own — the low-hanging transitive bumps.

📎 **Complete auto-remediation workflow:**
[Full workflow with PR creation and test validation](https://gist.github.com/williamzujkowski/7fd0e2b45a0311ffb4fc9d37c0684ad8)

Weekly scheduled job scans for vulnerabilities, runs `npm audit fix` and `npm update`, **runs the test suite**, re-scans, and opens a PR for review. The test step is not optional decoration — `npm audit fix` has broken dependencies on me twice, and a workflow that opens a PR describing fixes as safe without running anything is asserting something it has not checked.

## Integration with Wazuh SIEM

### Ship Scan Results to Wazuh

Forward vulnerability data to your SIEM. I ship scans via syslog to Wazuh for centralized tracking, building on patterns from [network traffic analysis with Suricata](/posts/2025-08-25-network-traffic-analysis-suricata-homelab) for complete security monitoring.

📎 **Complete Wazuh integration:**
[Full script with JSON transformation and error handling](https://gist.github.com/williamzujkowski/fe46d3793fb1f2d9771c8b9e1a2ee5d6)

Pipe Grype JSON output through `jq`, format as syslog, and send to Wazuh manager on port 1514 using `netcat`. Syslog is the mechanism to use here — the scheduled-scan workflow linked above ends with a `curl -X POST` to a `/api/vulnerabilities` endpoint, which is not a route the Wazuh API exposes. Events reach Wazuh through agents or syslog, not through a vulnerability-ingestion REST call.

### Wazuh Rules for Vulnerability Alerts

Create custom alerting rules. Critical findings trigger level 12 alerts (email + PagerDuty integration).

📎 **Complete Wazuh rules:**
[Full local_rules.xml with all severity levels](https://gist.github.com/williamzujkowski/bd0a834441a1df242f7d35868d1b1a9b)

Define base rule matching vulnerability IDs (level 7), then escalate to level 12 for critical severity findings.

## Lessons Learned

After building and running this pipeline for a year, here's what I discovered through trial and error. These lessons integrate well with my approach to [open-source vulnerability management at scale](/posts/2025-07-15-vulnerability-management-scale-open-source).

The focus should be on sustainable processes instead of perfect tools.

### 1. Multiple Scanners Reduce False Negatives

When I first tested Grype alone, I thought I had good coverage. Then I added OSV-Scanner and immediately found 4 additional vulnerabilities in a project I'd already "validated."

The overlap between tools is surprisingly low: 4 findings shared out of 16 distinct. Running both catches more real issues. For smaller projects, three scanners might be overkill. I'm still testing this hypothesis.

### 2. Fail Fast, Fail Loud

I initially set my pipeline to "warn" on critical vulnerabilities, thinking I'd review them later. That lasted two weeks before I had 47 unreviewed warnings.

Switching to hard-block on critical findings was painful. I spent a full weekend fixing vulnerabilities the first time. It forces good hygiene. There are times when I question whether blocking a build for a vulnerability in a dev-only dependency is the right call. No perfect answer exists.

### 3. Baseline Everything

Without a baseline, you're drowning in noise. I learned this the hard way when Trivy flagged 183 findings on my first scan. Most were from base images I inherited.

Now I track what's new vs. what's been there, which is the difference between a list I read and a list I ignore. I still struggle with deciding how long to "accept" known issues in the baseline before forcing remediation. This is an ongoing balance.

### 4. Automate Remediation Where Possible

`npm audit fix` catches low-hanging fruit automatically. Focus human effort on complex issues.

That said, I've had `npm audit fix` break dependencies twice, so blind automation isn't always the answer.

### 5. Integration is Key

Scanning results are useless if no one sees them. I initially just had GitHub annotations, which I never checked. Adding Slack notifications is what moved findings from something I discovered later to something I saw the same day.

Shipping to my Wazuh SIEM let me track trends over time. I'm still figuring out the right balance between visibility and notification fatigue. Too many alerts become noise.

## Performance Optimization

When I first implemented this pipeline, builds were taking forever. Here are my actual scan times measured on October 15, 2024:

| Stage | Initial | Optimized | Improvement |
|-------|---------|-----------|-------------|
| OSV Scan | 45s | 12s | 73% faster |
| Grype Scan | 2m 30s | 35s | 77% faster |
| Trivy Scan | 3m 15s | 1m 10s | 64% faster |
| **Total** | **6m 30s** | **2m** | **69% faster** |

**Optimizations I added:**

- **Scanner tuning**: the per-scanner gains above are the bulk of it. Note that these totals are column sums, i.e. the scanners running one after another — which is what the workflow actually does. Genuine parallel execution would put the total at the slowest scanner (1m 10s) rather than the sum
- **Cached vulnerability databases**: Grype's DB cache alone saved 40 seconds per run
- **Scoped scanning** (ignore test files): Cutting out `node_modules` and test fixtures dropped scan time by 25%
- **Early failure** (stop on critical): When a critical CVE is found, I stop immediately instead of completing all scans

These times are from GitHub-hosted `ubuntu-latest` runners, which is what every job in the workflow declares. Your mileage will vary with project size and runner spec.

The complexity of running three scanners creates maintenance burden. Smaller teams might be better off with just Grype. I'm still testing whether the extra coverage justifies the extra complexity.

## Metrics Dashboard

Track security posture with PostgreSQL queries. The metric worth watching is time-to-remediate on criticals; the absolute number matters less than whether it is trending down.

📎 **Complete SQL analytics:**
[Full PostgreSQL queries for vulnerability tracking](https://gist.github.com/williamzujkowski/0a94337fba5a5e94fa8082c543c2a4df)

Query vulnerability trends over time, grouping by severity and date to track remediation progress and new findings.

## Sources

### Security Scanning Tools

1. **[Grype Documentation](https://github.com/anchore/grype)** - Vulnerability scanner for container images and filesystems
2. **[OSV-Scanner](https://github.com/google/osv-scanner)** - Google's open-source vulnerability scanner
3. **[Trivy Documentation](https://aquasecurity.github.io/trivy/)** - Comprehensive security scanner

### SBOM Standards

1. **[CycloneDX Specification](https://cyclonedx.org/)** - Modern SBOM standard
2. **[SPDX](https://spdx.dev/)** - Software Package Data Exchange
3. **[NTIA SBOM Minimum Elements](https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom)** - U.S. government SBOM guidelines

### Supply Chain Security

1. **[SLSA Framework](https://slsa.dev/)** - Supply-chain Levels for Software Artifacts
2. **[NIST SSDF](https://csrc.nist.gov/publications/detail/sp/800-218/final)** - Secure Software Development Framework
3. **[OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)** - Dependency vulnerability detection

## Limitations and Considerations

Before you build this exact pipeline, here are some things I'm still uncertain about:

### When Is This Overkill?

For my homelab with 15+ services, running three scanners makes sense. For a single Node.js app, this might be excessive overhead. I don't know where the threshold is. Maybe two services? Five? It depends on your risk tolerance and team size.

**Scaling unknowns:**
- This setup works at my scale (dozens of small repositories)
- Would it work for 500? 5,000? Unknown.
- Centralized SARIF reporting might become a bottleneck
- I haven't tested at enterprise scale

### False Positives Are Still a Problem

Even with three scanners, I get false positives. Last month, Trivy flagged a "critical" vulnerability in a Go binary that turned out to be a misidentified version number. I spent three hours investigating before realizing the scanner was wrong. No tool is perfect. I haven't found a good way to systematically reduce false positives beyond manual review.

### Maintenance Burden

These scanners update their databases constantly. Great for coverage. Terrible when your pipeline suddenly fails because a new CVE was published overnight. I've had emergency fixes on Sunday mornings because of this. Is there a better way to handle breaking changes from vulnerability database updates? I'm still figuring that out.

### Cost Considerations

GitHub-hosted runners are free for public repositories and metered for private ones, so what this costs depends entirely on which kind you have:
- Public repos: nothing
- Fine for a homelab
- Scales poorly for larger organizations
- Self-hosted runners would help (but you're managing infrastructure)

## Conclusion

Automated security scanning isn't optional. It's a fundamental requirement for modern development. By integrating Grype, OSV-Scanner, and Trivy into my CI/CD pipeline, I've shifted security left and caught vulnerabilities before they reach production.

The initial setup took me about two weeks of evening work, but the ongoing protection has been worth it. Every critical vulnerability caught in CI is one that doesn't slip through to where it actually matters.

Start with basic scanning, even just Grype on container images, then add quality gates, integrate with your SIEM, and watch your security posture improve. Don't try to implement everything I've shown here at once. I built this incrementally over a year, and you should too.
