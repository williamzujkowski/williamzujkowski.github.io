---
title: "SIEM for Homelab: Wazuh vs Graylog Performance Comparison"
description: "Deploy and benchmark Wazuh and Graylog SIEM solutions in your homelab. Performance analysis, resource usage, and integration patterns for security monitoring."
author: "William Zujkowski"
date: 2025-11-05
tags: [threat-detection, security, monitoring, homelab, python]
post_type: tutorial
---

Security monitoring needs centralized log analysis. I deployed both Wazuh and Graylog in my homelab to compare performance, resource usage, and detection capabilities. Wazuh excelled at threat detection (it caught all five test scenarios out of the box, and was quicker than Graylog on the two attacks both tools caught), Graylog dominated log search speed.

Here's how to choose and deploy the right SIEM for your homelab.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/siem.png'); width: min(230px, 60%); aspect-ratio: 400/425; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">one eye, all the logs</p>

## The Homelab SIEM Problem

Distributed logs across 47 services make security monitoring impossible. Firewall blocks attack at 14:32, IDS flags suspicious traffic at 14:35, application crashes at 14:38. Are these related? Manual correlation takes 45 minutes. You need SIEM.

What SIEM solves:

- **Centralized visibility:** All logs in one place (firewall, IDS, application, system)
- **Correlation:** "SSH brute force + successful login + sudo su" = potential compromise
- **Alerting:** Real-time notifications for security events
- **Investigation:** Query logs from the last 30 days quickly

Why homelab SIEMs different from enterprise: Resource constraints (8-64GB RAM vs enterprise 256GB+), complexity tolerance (manual setup OK), cost sensitivity (free open source only).

Options compared: Wazuh (security-focused), Graylog (log management-focused), ELK Stack (not tested - resource intensive), Splunk (not free).

## Architecture: Wazuh vs Graylog

Both use agent-based collection, centralized storage, and web UI. Architectures differ in focus.

Wazuh architecture:

<div class="flow" role="group" aria-label="Wazuh log collection architecture">
  <div class="flow-parallel" role="group" aria-label="Runs in parallel">
    <div class="flow-node"><b>Wazuh Agent</b><i>Host 1 logs</i></div>
    <div class="flow-node"><b>Wazuh Agent</b><i>Host 2 logs</i></div>
  </div>
  <div class="flow-node">Wazuh Manager</div>
  <div class="flow-branch" role="group" aria-label="Branch outcomes">
    <div class="flow-leg" data-branch="Index" role="group" aria-label="Index"><div class="flow-node"><b>Wazuh Indexer</b><i>OpenSearch</i></div></div>
    <div class="flow-leg" data-branch="Alerts" role="group" aria-label="Alerts"><div class="flow-node"><b>Wazuh Dashboard</b><i>queries indexer</i></div></div>
  </div>
</div>

Graylog architecture:

<div class="flow" role="group" aria-label="Graylog log collection architecture">
  <div class="flow-parallel" role="group" aria-label="Runs in parallel">
    <div class="flow-node"><b>Filebeat</b><i>Host 1 syslog</i></div>
    <div class="flow-node"><b>Filebeat</b><i>Host 2 syslog</i></div>
  </div>
  <div class="flow-node">Graylog Server</div>
  <div class="flow-parallel" role="group" aria-label="Runs in parallel">
    <div class="flow-node"><b>MongoDB</b><i>store</i></div>
    <div class="flow-node"><b>Elasticsearch</b><i>index</i></div>
    <div class="flow-node"><b>Graylog Web</b><i>search</i></div>
  </div>
</div>

Key differences:

| Feature | Wazuh | Graylog |
|---------|-------|---------|
| Log collection | Wazuh agent (C binary) | Filebeat/Logstash/Syslog |
| Storage backend | OpenSearch/Elasticsearch | Elasticsearch + MongoDB |
| Primary focus | Threat detection | Log aggregation |
| Built-in rules | 4,400+ security rules | Basic extraction rules |
| Alert correlation | Event-driven | Stream-based |

## Homelab Deployment: Both SIEMs Side-by-Side

I deployed both SIEMs in parallel to compare real-world performance. Infrastructure: Proxmox cluster, 3 VMs (16GB RAM each), Ubuntu 24.04.

### Wazuh deployment (Docker Compose)

```bash
# Host prerequisite: the indexer needs at least 262,144 memory-mapped areas
# (persist it in /etc/sysctl.conf)
sudo sysctl -w vm.max_map_count=262144

# Official single-node stack (Wazuh 4.9 Docker documentation)
git clone https://github.com/wazuh/wazuh-docker.git -b v4.9.2
cd wazuh-docker/single-node

# Generate the self-signed certificates the stack expects
docker-compose -f generate-indexer-certs.yml run --rm generator

# Deploy stack
docker-compose up -d

# Verify deployment
docker-compose ps
# -k because the lab certificate is self-signed; SecretPassword is the shipped
# default -- change it. A 401 body has no cluster_name, so bad credentials fail here.
curl -sk -u admin:SecretPassword https://localhost:9200/ | grep -q cluster_name && echo "indexer up"
```

*Correction (October 2026):* an earlier version of this block downloaded
`https://packages.wazuh.com/4.9/docker-compose.yml` with `curl -sO`. That URL
answers 403 with an XML `AccessDenied` body, and without `--fail` curl saves the
error as `docker-compose.yml` and exits 0. The block now follows the
[Wazuh 4.9 Docker deployment guide](https://documentation.wazuh.com/4.9/deployment-options/docker/wazuh-container.html).
It also exported `WAZUH_MANAGER_RAM` and `WAZUH_INDEXER_RAM`, which the
[v4.9.2 single-node compose file](https://github.com/wazuh/wazuh-docker/blob/v4.9.2/single-node/docker-compose.yml)
never reads; the indexer heap is set there by `OPENSEARCH_JAVA_OPTS`. The
`vm.max_map_count` prerequisite comes from Wazuh's
[Docker installation requirements](https://documentation.wazuh.com/4.9/deployment-options/docker/docker-installation.html),
and the health check now looks for `cluster_name` in the indexer's response
instead of trusting curl's exit status, which is 0 on a 401 too.

Wazuh components:

- **Wazuh Manager:** Log processing, rule engine, alerting
- **Wazuh Indexer:** OpenSearch cluster (3 nodes in production, 1 for homelab)
- **Wazuh Dashboard:** Kibana fork for visualization

### Graylog deployment (Docker Compose)

```bash
# MongoDB for metadata
docker run -d --name mongodb mongo:6.0

# Elasticsearch for log storage
docker run -d --name elasticsearch \
  -e "discovery.type=single-node" \
  -e "ES_JAVA_OPTS=-Xms2g -Xmx2g" \
  docker.elastic.co/elasticsearch/elasticsearch:8.11.0

# Graylog server
docker run -d --name graylog \
  -e "GRAYLOG_ROOT_PASSWORD_SHA2=$(echo -n password | shasum -a 256 | cut -d' ' -f1)" \
  -e "GRAYLOG_HTTP_EXTERNAL_URI=http://localhost:9000/" \
  -e "GRAYLOG_ELASTICSEARCH_HOSTS=http://elasticsearch:9200" \
  -e "GRAYLOG_MONGODB_URI=mongodb://mongodb:27017/graylog" \
  -p 9000:9000 \
  graylog/graylog:5.2
```

Complete deployment scripts: https://gist.github.com/williamzujkowski/79146ef623363155e85d244a91c383cf

### Agent deployment (both)

- 47 homelab hosts monitored (Docker containers, VMs, physical servers)
- **Wazuh agents:** Installed via package manager (`apt-get install wazuh-agent`)
- **Filebeat agents:** Configured for Graylog syslog input

Deployment time: Wazuh took longer (manager + indexer + dashboard + 47 agents) than Graylog (server + MongoDB + Elasticsearch + 47 Filebeat agents). I did not keep the timings, so I won't quote minutes.

## Performance Benchmark: Detection Speed

I simulated 5 common attack patterns to measure detection speed.

Test scenarios:

1. **SSH brute force:** 50 failed login attempts in 60 seconds
2. **Port scan:** Nmap SYN scan of 1,000 ports
3. **Web attack:** SQL injection attempts (20 requests)
4. **Privilege escalation:** Unauthorized sudo command
5. **File integrity:** Modify /etc/passwd

Detection results (I did not retain the per-scenario timings from these runs, so the table shows coverage rather than seconds):

| Attack Type | Wazuh | Graylog* |
|-------------|-------|----------|
| SSH brute force | Detected | Detected, slower than Wazuh |
| Port scan | Detected | N/A (no built-in rule) |
| SQL injection | Detected | N/A (requires custom rule) |
| Privilege escalation | Detected | Detected, slower than Wazuh |
| File integrity | Detected | N/A (no FIM capability) |
| **Scenarios caught** | **5 of 5** | **2 of 5** |

*Graylog detection via custom stream rules. No packaged security detection content in Graylog Open — the aggregation event processor does correlation, but curated rules and the Correlation Engine sit behind Enterprise.

Why Wazuh faster: Built-in correlation rules trigger on pattern match. Graylog requires manual stream creation and alert conditions.

Alert accuracy:

- **Wazuh false positives:** fewer, though it flagged legitimate SSH retries as brute force
- **Graylog false positives:** more (stream rules less sophisticated)

I did not retain the false-positive counts, so I won't quote rates.

Winner (detection): Wazuh excels at security-specific use cases with minimal configuration.

## Performance Benchmark: Log Search Speed

Query performance matters when investigating incidents.

Test queries:

1. **Simple keyword:** Search "error" in last 24 hours
2. **Field filter:** Find all SSH events (`program:sshd`) in last 7 days
3. **Time range:** Load all events from 14:00-15:00 yesterday
4. **Aggregation:** Count events by source IP, last 30 days
5. **Complex:** Multi-field correlation (source IP + failed auth + 10 minute window)

Query speed results: Graylog (Elasticsearch) was faster than Wazuh (OpenSearch) across the query types I tried. I did not retain the per-query timings, so I won't quote seconds.

Data volume: a week of retention across 47 hosts logging.

Why Graylog faster: Elasticsearch-first design optimizes for search speed. Wazuh adds security processing overhead (rule evaluation, enrichment).

Winner (search): Graylog delivers clearly faster queries for log investigation workflows.

## Resource Usage Comparison

Both SIEMs consume significant resources. Graylog lighter footprint.

Memory: the Wazuh stack used more RAM at steady state than Graylog. In both, the storage layer (Wazuh indexer, Elasticsearch) took the largest share, and Graylog adds a small MongoDB footprint on top.

CPU: during log ingestion the Wazuh manager used more CPU than the Graylog server.

Disk I/O: the Wazuh indexer sustained heavier writes than Elasticsearch under Graylog. MongoDB's writes were small (metadata only).

Storage growth: Wazuh grew faster per day than Graylog across the 47 hosts.

I did not retain the measurements behind these comparisons, so I won't quote numbers.

Winner (resources): Graylog uses less memory and less disk space.

## Integration: Custom Python Automation

Both SIEMs expose REST APIs for automation. I built Python scripts to automate alert enrichment and response.

Wazuh API example (alert query):

```python
import requests
from requests.auth import HTTPBasicAuth

WAZUH_API = "https://wazuh-manager:55000"
AUTH = HTTPBasicAuth(os.environ["WAZUH_USER"], os.environ["WAZUH_PASSWORD"])

# Query recent alerts
response = requests.get(
    f"{WAZUH_API}/security/alerts",
    auth=AUTH,
    params={"limit": 100, "severity": "high"},
    verify=True
)

alerts = response.json()["data"]
for alert in alerts:
    print(f"[{alert['severity']}] {alert['rule']['description']}")
```

Graylog API example (stream query):

```python
import requests

GRAYLOG_API = "http://graylog-server:9000/api"
TOKEN = "your_api_token_here"

# Query security stream
response = requests.get(
    f"{GRAYLOG_API}/streams/stream_id/alerts",
    headers={"Authorization": f"Bearer {TOKEN}"},
    params={"limit": 100}
)

alerts = response.json()["alerts"]
for alert in alerts:
    print(f"[{alert['condition_title']}] Triggered at {alert['triggered_at']}")
```

Automation built:

1. **Auto-remediation:** Block IP addresses after 10 failed SSH attempts (firewall API integration)
2. **Enrichment:** Query VirusTotal for file hashes in malware alerts
3. **Escalation:** Create PagerDuty incident for critical alerts
4. **Reporting:** Daily security summary (Slack notification)

API comparison:

| Feature | Wazuh API | Graylog API |
|---------|-----------|-------------|
| Authentication | HTTP Basic | API tokens |
| Documentation | Good | Excellent |
| Response format | JSON | JSON |
| Rate limiting | 300 req/min | not documented |

Python integration examples: https://gist.github.com/williamzujkowski/4df107e30a0d2e5f5156df1d9203ca13

## Security Detection: Built-In Rules vs Custom

Wazuh ships with 4,400+ security rules. Graylog requires custom stream creation.

Wazuh out-of-box detections:

- SSH brute force (8 failed attempts in 120 seconds, rule 5712's shipped default)
- Web attacks (SQL injection, XSS, LFI patterns)
- File integrity monitoring (detects /etc, /bin changes)
- Privilege escalation (unauthorized sudo, su)
- Malware detection (ClamAV integration)
- Compliance (PCI-DSS, GDPR, HIPAA rule sets)

Graylog custom rule example (SSH brute force):

```
# Create stream: "Failed SSH Logins"
Field: program
Value: sshd
Condition: message matches "Failed password"

# Create alert:
Condition: message count > 10 in 2 minutes
Action: Send email notification
```

Detection coverage (my homelab):

| Detection Type | Wazuh (Built-in) | Graylog (Custom) |
|----------------|------------------|------------------|
| Brute force | ✅ Default rule | ⚠️ Manual stream |
| Port scanning | No host-based default rule; needs an IDS in the loop | Aggregation event definition in core |
| Web attacks | ✅ ~120 rules | ⚠️ Manual rules |
| File integrity | ✅ FIM module | ❌ Not supported |
| Malware | ✅ ClamAV integration | ❌ External only |
| Anomaly detection | ⚠️ Basic | Licensed content pack (Graylog Security) |

Winner (detection): Wazuh requires zero configuration for common threats. Graylog demands security expertise to replicate coverage.

## Hybrid Deployment: Best of Both

Some teams run Wazuh + Graylog together. Wazuh handles threat detection, Graylog provides flexible log search.

Hybrid architecture:

<figure class="arch-fig">
<div class="arch" role="group" aria-label="Hybrid Wazuh and Graylog deployment">
  <section class="arch-tier" data-label="Inputs" role="group" aria-label="Inputs"><span class="arch-chip">Homelab Hosts</span></section>
  <section class="arch-tier" data-label="Security Path" role="group" aria-label="Security Path"><span class="arch-chip is-primary">Wazuh Manager</span><span class="arch-chip">Alert Dashboard</span></section>
  <section class="arch-tier" data-label="Application Path" role="group" aria-label="Application Path"><span class="arch-chip is-primary">Graylog Server</span><span class="arch-chip">Investigation UI</span></section>
  <section class="arch-tier" data-label="Integration" role="group" aria-label="Integration"><span class="arch-chip is-guard">Forward Wazuh Alerts to Graylog</span><span class="arch-chip is-guard">Enrich Graylog Events in Wazuh</span></section>
</div>
<figcaption>Security logs flow to Wazuh, application logs flow to Graylog, and the two systems exchange alerts for unified investigation.</figcaption>
</figure>

Integration patterns:

1. **Wazuh → Graylog:** Forward Wazuh alerts to Graylog for unified dashboard
2. **Graylog → Wazuh:** Send suspicious events from Graylog to Wazuh for correlation
3. **Shared storage:** Both write to same Elasticsearch cluster (resource optimization)

Real-world example: Use Wazuh for security monitoring (SSH, malware, FIM). Use Graylog for application logs (Django debug logs, Nginx access logs). Graylog's stream processing creates custom alerts Wazuh doesn't cover (business logic errors, API rate limiting).

Why hybrid works: Separate concerns (security vs operations), leverage strengths (Wazuh rules vs Graylog search).

Configuration: https://gist.github.com/williamzujkowski/c5ea53300957068928678f3f6927cab6

## When to Choose Wazuh vs Graylog

Choose Wazuh if:

- Primary goal is security threat detection
- Need out-of-box coverage (brute force, malware, compliance)
- File integrity monitoring required
- Regulatory compliance matters (PCI-DSS, HIPAA)
- Limited security expertise (pre-built rules)

Choose Graylog if:

- Primary goal is centralized log aggregation
- Need fast log search and investigation
- Application debugging more important than security
- Custom log parsing and enrichment critical
- Resource constrained (Graylog lighter footprint)

My homelab choice: Started with Graylog (easier setup, faster search). Added Wazuh later for security-specific rules. Now run hybrid deployment.

## Limitations and Trade-Offs

Wazuh challenges:

1. **Resource usage:** Plan for a lot of RAM in production (Indexer memory hungry)
2. **Learning curve:** Dashboard overwhelming (100+ pre-built visualizations)
3. **Alert noise:** Default rules generate high false positive rate (tuning required)

Graylog challenges:

1. **Security rules:** Manual creation time-consuming (building the streams took hours)
2. **No FIM:** File integrity monitoring requires external tools (OSSEC, AIDE)
3. **Correlation limits:** Stream-based correlation less powerful than Wazuh event engine

Common challenges (both):

- **Retention costs:** Storing 30 days of logs for 47 hosts takes substantial disk
- **Agent deployment:** Manual install on 47 hosts took hours (automation needed)
- **Tune

 vs alert fatigue:** The first week was far noisier than after tuning.

## Further Reading

SIEM comparisons and research:

- [Comparative Analysis of Wazuh, Graylog, and ELK Stack](https://infonomics-society.org/icitst-2024/icitst-abstract-15/) - ICITST 2024 conference
- [Wazuh vs Graylog: Which SIEM Tools Wins in 2025?](https://www.selecthub.com/siem-tools/wazuh-vs-graylog/) - SelectHub analysis

Official documentation:

- [Wazuh Documentation](https://documentation.wazuh.com/) - Deployment, configuration, rule reference
- [Graylog Documentation](https://go2docs.graylog.org/) - Stream processing, extractors, alerts
- [OpenSearch](https://opensearch.org/docs/latest/) - Wazuh backend (Elasticsearch fork)

Deployment guides:

- [Wazuh Docker Deployment](https://documentation.wazuh.com/current/deployment-options/docker/index.html)
- [Graylog Docker Deployment](https://go2docs.graylog.org/current/downloading_and_installing_graylog/docker_installation.htm)

Alternative SIEMs (not tested):

- [Elastic Security](https://www.elastic.co/security) - Commercial ELK Stack with security
- [Splunk Free](https://help.splunk.com/en/data-management/splunk-enterprise-admin-manual/10.2/configure-splunk-licenses/about-splunk-free) - 500MB/day limit
- [Security Onion](https://securityonionsolutions.com/) - Network security monitoring platform

Implementation references:

- **Deployment scripts:** https://gist.github.com/williamzujkowski/79146ef623363155e85d244a91c383cf
- **Python automation:** https://gist.github.com/williamzujkowski/4df107e30a0d2e5f5156df1d9203ca13
- **Hybrid configuration:** https://gist.github.com/williamzujkowski/c5ea53300957068928678f3f6927cab6

---

Deploy centralized security monitoring. Start with one SIEM, validate detection coverage, then optimize. Most homelabs need Graylog's search speed OR Wazuh's security rules, not both.

Run hybrid if resources allow. Alert fatigue comes from poor tuning, not too many tools. In my homelab, SIEM caught a handful of real security incidents. Manual log review would have missed them.
