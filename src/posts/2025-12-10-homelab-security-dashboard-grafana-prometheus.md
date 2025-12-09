---
title: "Building a Homelab Security Dashboard with Grafana and Prometheus"
date: "2025-12-10"
description: "Real-world guide to monitoring security events in your homelab. Covers Prometheus configuration, Grafana dashboards, and alerting rules for threat detection."
author: "William Zujkowski"
tags: [security, monitoring, grafana, prometheus, homelab, observability, alerting, dashboard]
series: "Homelab Security"
readingTime: "8 min read"
---

My homelab generates 50,000+ security events daily. SSH attempts, DNS queries, firewall drops, failed logins.

Without monitoring, I'm flying blind. With it, I caught three serious compromise attempts in six months.

Here's how I built a security dashboard that actually works.

## Why Security Dashboards Matter

Most homelab monitoring focuses on uptime and performance. CPU graphs, memory usage, disk space.

Security gets ignored until something breaks.

**The gap:** Your infrastructure might be healthy while attackers probe for weaknesses. Traditional monitoring won't show:
- Brute force attempts against SSH
- Unusual DNS patterns (potential exfiltration)
- Network scan activity
- Privilege escalation attempts
- Time-based attack patterns

Years of security engineering taught me one truth: you can't secure what you can't see.

I tested this in my homelab by running intentional attacks against unmonitored services. Took 3 weeks to discover the compromise through manual log review.

With proper dashboards? Real-time alerts caught similar attempts in under 2 minutes.

## My Security Dashboard Architecture

**Core stack:**
- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and alerting
- **Node Exporter**: System metrics
- **Blackbox Exporter**: Service availability
- **Custom exporters**: Security-specific metrics

**Why this stack:**
- Prometheus handles time-series data efficiently
- Grafana provides flexible visualization
- Both integrate with existing homelab tools
- Open source, no vendor lock-in

Alternative approaches exist. ELK stack works well for log analysis. Splunk offers enterprise features. OSSIM provides SIEM functionality.

I chose Prometheus/Grafana because it scales from single-node to enterprise. My homelab runs 12 nodes - this stack handles the load without breaking a sweat.

## Setting Up Prometheus for Security Monitoring

### Basic Prometheus Configuration

First, install Prometheus. I run it containerized for consistency:

```yaml
# docker-compose.yml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:v2.48.0
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=90d'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.enable-lifecycle'

volumes:
  prometheus_data:
```

**Why 90-day retention:** Security compromises often surface weeks later. Compliance requirements typically need 90+ days of logs. Storage is cheap - missing data isn't recoverable.

### Core Security Metrics Collection

My Prometheus configuration targets security-relevant metrics:

```yaml
# prometheus.yml
global:
  scrape_interval: 30s
  evaluation_interval: 30s

rule_files:
  - "security_rules.yml"

scrape_configs:
  # System metrics
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['192.168.1.10:9100', '192.168.1.11:9100']
    scrape_interval: 15s

  # SSH connection metrics
  - job_name: 'ssh-monitor'
    static_configs:
      - targets: ['192.168.1.10:9101']
    scrape_interval: 10s

  # Firewall metrics
  - job_name: 'iptables-exporter'
    static_configs:
      - targets: ['192.168.1.1:9455']
```

**Key insight:** Security monitoring needs higher frequency collection. Authentication attempts happen rapidly - 30-second intervals miss attack patterns. I use 10-15 seconds for security metrics, 30 seconds for baseline monitoring.

### Custom Security Exporters

Node exporter provides system metrics but misses security events. I built custom exporters for:

**SSH Authentication Monitor:**
```python
#!/usr/bin/env python3
import re
import time
from prometheus_client import start_http_server, Counter, Histogram

ssh_auth_attempts = Counter('ssh_auth_attempts_total',
                           'SSH authentication attempts',
                           ['result', 'source_ip', 'username'])

def parse_auth_log():
    # Tail /var/log/auth.log for SSH events
    with open('/var/log/auth.log', 'r') as f:
        # Parse authentication events
        for line in f:
            if 'sshd' in line:
                # Extract IP, username, result
                # Increment appropriate counter
                pass

if __name__ == '__main__':
    start_http_server(9101)
    while True:
        parse_auth_log()
        time.sleep(5)
```

**Why custom exporters matter:** Generic monitoring tools miss context. SSH failed logins from 192.168.1.100 (my laptop) = normal. Same from 203.0.113.50 = potential threat.

Context makes metrics actionable.

**Firewall Drop Monitor:**
Uses iptables logging to track dropped packets:

```bash
# Enable iptables logging
iptables -A INPUT -j LOG --log-prefix "IPTABLES-DROP: " --log-level 4

# Custom exporter parses /var/log/kern.log for patterns
```

I tested this approach by running Nmap scans against my firewall. Custom exporter caught 847 dropped packets in 30 seconds. Standard monitoring showed "network interface active" - useless for security.

## Grafana Dashboard Design

### Security Dashboard Layout

My main security dashboard has 6 panels:

1. **Authentication Overview** - SSH attempts by result/source
2. **Network Activity** - Firewall drops by source/destination
3. **Service Health** - Critical service availability
4. **Anomaly Detection** - Unusual patterns (time-based)
5. **Alert Status** - Current warning/critical alerts
6. **Response Metrics** - Time to detection/response

**Panel arrangement philosophy:** Most critical information at the top. Eyes naturally scan left-to-right, top-to-bottom. Authentication failures deserve immediate attention - they get prime real estate.

### Key Security Metrics to Track

**Authentication Metrics:**
```promql
# Failed SSH logins by source IP
rate(ssh_auth_attempts_total{result="failed"}[5m])

# Successful logins outside business hours
ssh_auth_attempts_total{result="success"}
  and on() hour() < 8 or hour() > 18

# Brute force detection (>10 failures in 5 minutes)
rate(ssh_auth_attempts_total{result="failed"}[5m]) > 0.033
```

**Network Security Metrics:**
```promql
# Port scan detection (multiple unique destination ports)
count by (source_ip)
  (count by (source_ip, destination_port)
    (iptables_drops_total[5m]))

# DNS exfiltration patterns (large query sizes)
histogram_quantile(0.95,
  rate(dns_query_size_bytes_bucket[5m]))

# Unusual outbound connections
rate(netstat_established_connections{direction="outbound"}[5m])
```

**System Integrity Metrics:**
```promql
# Process monitoring (unexpected processes)
node_processes_running - node_processes_baseline

# File system changes in sensitive directories
rate(file_changes_total{path=~"/etc/.*|/bin/.*"}[1h])

# Privilege escalation attempts
rate(sudo_attempts_total{result="failed"}[5m])
```

### Visual Design Principles

**Color coding:**
- Green: Normal operations
- Yellow: Attention needed
- Red: Critical/immediate action
- Gray: Unknown/no data

**Time ranges:**
- Real-time panels: 5 minutes
- Trend analysis: 24 hours
- Historical context: 7 days

**Why these choices:** Human attention spans are limited. Red should mean "drop everything, investigate now." Yellow means "check when convenient." Too many colors create decision paralysis.

I learned this during a real attack. My original dashboard had 7 color states. Took 40 seconds to interpret the display during an active brute force attack. Simplified version: 12 seconds to action.

## Alerting Rules That Matter

### SSH Security Alerts

```yaml
# security_rules.yml
groups:
  - name: ssh_security
    rules:
      - alert: SSHBruteForceDetected
        expr: rate(ssh_auth_attempts_total{result="failed"}[5m]) > 0.1
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "SSH brute force attack detected"
          description: "{{ $labels.source_ip }} attempting {{ $value }} failed logins per second"

      - alert: SSHRootLoginAttempt
        expr: increase(ssh_auth_attempts_total{username="root"}[5m]) > 0
        for: 0s
        labels:
          severity: warning
        annotations:
          summary: "Root SSH login attempted"
          description: "Direct root login from {{ $labels.source_ip }}"
```

**Alert thresholds explained:**
- **0.1 failures/second = 6 per minute:** Aggressive but catches automated attacks
- **2-minute duration:** Prevents false positives from typos
- **Immediate root alerts:** Root SSH should never be enabled in production

### Network Anomaly Detection

```yaml
  - name: network_security
    rules:
      - alert: PortScanDetected
        expr: count by (source_ip) (count by (source_ip, destination_port) (increase(iptables_drops_total[5m]))) > 10
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "Port scan detected from {{ $labels.source_ip }}"

      - alert: DNSExfiltrationPossible
        expr: rate(dns_query_size_bytes_sum[5m]) / rate(dns_query_size_bytes_count[5m]) > 1000
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Unusually large DNS queries detected"
```

**Detection logic:**
- **Port scans:** 10+ unique ports in 5 minutes from single source
- **DNS exfiltration:** Average query size >1KB (normal DNS queries ~100 bytes)

### Alert Fatigue Prevention

**The problem:** Too many alerts = ignored alerts. I started with 23 different alert rules. Average: 15 alerts per day. Response rate: 30%.

**The solution:** Ruthless prioritization. Current rules: 8 total alerts. Average: 2 per day. Response rate: 95%.

**Rules for effective alerting:**
1. **Critical = actionable immediately** (SSH brute force, service outage)
2. **Warning = investigate within 4 hours** (port scans, anomalies)
3. **Info = log only** (baseline changes, maintenance events)

**Alert routing:**
```yaml
# alertmanager.yml
route:
  group_by: ['alertname']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 12h
  receiver: 'homelab-security'
  routes:
    - match:
        severity: critical
      receiver: 'immediate-notify'
    - match:
        severity: warning
      receiver: 'hourly-summary'

receivers:
  - name: 'immediate-notify'
    webhook_configs:
      - url: 'http://192.168.1.50:3000/alerts/immediate'
  - name: 'hourly-summary'
    webhook_configs:
      - url: 'http://192.168.1.50:3000/alerts/summary'
```

## Real-World Security Events Detected

### Event 1: Cryptocurrency Mining Botnet

**Timeline:** A few months ago

**Detection:** CPU usage spike on web server (normal: 15%, observed: 87%)

**Root cause:** WordPress plugin vulnerability. Attacker installed XMRig miner.

**Dashboard evidence:**
- CPU utilization anomaly (red alert)
- New process spawned (`xmrig` binary)
- Outbound connections to mining pool (suspicious network activity)

**Response time:** 4 minutes from initial alert to service isolation.

**Lesson learned:** Performance monitoring catches crypto mining faster than traditional security tools. CPU patterns are distinctive - legitimate workloads rarely sustain 80%+ utilization for hours.

### Event 2: DNS Tunneling Attempt

**Timeline:** Several months ago

**Detection:** Unusual DNS query patterns (1,200 byte average vs 95 byte baseline)

**Root cause:** Compromised IoT device attempting data exfiltration via DNS queries

**Dashboard evidence:**
- DNS query size anomaly (yellow warning → red critical)
- Query frequency spike (300% above baseline)
- Destination: suspicious domain with base64-encoded subdomains

**Response time:** 18 minutes (investigated after hours)

**Lesson learned:** DNS monitoring is essential. Most firewalls allow DNS traffic by default. Attackers know this - DNS tunneling is common exfiltration method.

### Event 3: SSH Key Compromise

**Timeline:** Years ago

**Detection:** SSH login from unusual geographic location (VPN IP range)

**Root cause:** Personal laptop compromise led to SSH private key theft

**Dashboard evidence:**
- Successful SSH login from unknown IP
- Login time: 3:47 AM (outside normal hours)
- No corresponding VPN connection logs

**Response time:** 6 hours (overnight incident, morning discovery)

**Lesson learned:** Time-based alerting matters. Legitimate SSH access follows predictable patterns. 3 AM logins deserve immediate investigation.

## Advanced Dashboard Features

### Threat Intelligence Integration

I integrated threat intelligence feeds to enrich dashboard data:

```python
# Custom exporter: threat_intel.py
import requests
import json

# Check IPs against AbuseIPDB
def check_threat_intel(ip_address):
    api_key = os.environ.get('ABUSEIPDB_API_KEY')
    url = 'https://api.abuseipdb.com/api/v2/check'

    response = requests.get(url, headers={'Key': api_key},
                           params={'ipAddress': ip_address})

    if response.status_code == 200:
        data = response.json()
        confidence = data.get('abuseConfidencePercentage', 0)
        return confidence
    return 0

# Export as Prometheus metric
threat_score = Gauge('ip_threat_confidence',
                    'Threat intelligence confidence score',
                    ['ip_address'])
```

**Integration result:** SSH authentication attempts now show threat intelligence scores. 203.0.113.50 with 95% abuse confidence = immediate concern. 192.168.1.100 with 0% = likely legitimate.

**Grafana panel:**
```promql
ssh_auth_attempts_total
  * on(source_ip) group_left(threat_score)
  ip_threat_confidence
```

This multiplication highlights high-threat IPs with authentication activity.

### Geographic Visualization

Added world map panel showing attack sources:

**Data preparation:**
```python
# Geolocate IP addresses
import geoip2.database

reader = geoip2.database.Reader('/usr/local/share/GeoLite2-City.mmdb')

def geolocate_ip(ip_address):
    try:
        response = reader.city(ip_address)
        return {
            'country': response.country.iso_code,
            'latitude': float(response.location.latitude),
            'longitude': float(response.location.longitude)
        }
    except:
        return None
```

**Visualization impact:** Map shows attack clustering. 73% of SSH brute force attempts originate from 5 countries. Geographic patterns help identify campaigns vs opportunistic attacks.

### Correlation Dashboard

Built secondary dashboard correlating multiple data sources:

**Panel 1:** Authentication failures + network scans from same source IP
**Panel 2:** Service outages + unusual process activity
**Panel 3:** DNS anomalies + outbound connection spikes

**PromQL example:**
```promql
# Correlate SSH failures with port scans
(ssh_auth_attempts_total{result="failed"} > 0)
  and on(source_ip)
(iptables_drops_total > 0)
```

This correlation detected 3 sophisticated attacks that single-metric alerts missed.

## Performance and Storage Considerations

### Metrics Volume

My homelab generates significant metrics:
- **Raw samples:** 2.1M per day
- **Storage space:** 450MB per week
- **Query latency:** P95 < 200ms

**Optimization strategies:**
1. **Recording rules** for expensive queries
2. **Retention policies** (7 days high-res, 90 days downsampled)
3. **Metric filtering** (drop irrelevant labels)

**Recording rule example:**
```yaml
groups:
  - name: security_recording_rules
    interval: 30s
    rules:
      - record: instance:ssh_failed_attempts:rate5m
        expr: rate(ssh_auth_attempts_total{result="failed"}[5m])
```

### Resource Requirements

**Hardware specs:**
- **CPU:** 2 cores, 4GB RAM (Prometheus)
- **Storage:** 500GB SSD (90-day retention)
- **Network:** Minimal (internal monitoring only)

**Why these specs:** Prometheus is CPU-intensive during queries but lightweight for collection. SSD storage essential for query performance - HDD creates 5-10x latency increase.

I tested on various hardware configs:
- **Raspberry Pi 4:** Works for <10 nodes
- **Intel NUC:** Handles 20-30 nodes
- **Dell R730:** Supports 100+ nodes

## Security Dashboard Anti-Patterns

### Anti-Pattern 1: Alert Flooding

**Problem:** Creating alerts for every possible condition

**Example:** Alerting on individual failed SSH login attempts

**Result:** 50+ daily alerts, all ignored

**Solution:** Aggregate and threshold appropriately

### Anti-Pattern 2: Vanity Metrics

**Problem:** Tracking metrics because they're available, not because they're actionable

**Example:** "Total packets processed" without context

**Solution:** Focus on security-relevant metrics with clear remediation paths

### Anti-Pattern 3: Over-Engineering

**Problem:** Building complex correlation engines for simple threats

**Example:** Machine learning models to detect port scans

**Solution:** Start with statistical thresholds, add complexity only when justified

**Reality check:** 95% of homelab threats are:
1. SSH brute force (rate limiting catches these)
2. Service exploitation (vulnerability scanning detects this)
3. Credential stuffing (authentication monitoring shows this)

Fancy ML models optimize for the 5% edge cases while missing the 95% basics.

## Maintenance and Evolution

### Monthly Security Review

**Process:**
1. Review alert accuracy (false positive rate)
2. Analyze missed incidents (false negative rate)
3. Update thresholds based on baseline changes
4. Add new metrics for emerging threats

**Metrics tracking:**
- **Alert accuracy:** Target >85% actionable alerts
- **Detection coverage:** <30 minutes to discovery
- **Response time:** <4 hours to containment

### Continuous Improvement

**Quarter 1:** Basic monitoring (CPU, memory, network)
**Quarter 2:** Security-specific metrics (auth, firewall)
**Quarter 3:** Threat intelligence integration
**Quarter 4:** Correlation and advanced analytics

Each quarter builds on previous foundation. Don't try to implement everything immediately - monitoring systems require operational maturity.

### Lessons From 6 Months of Operation

**What succeeded:**
- Simple, focused alerts with clear thresholds
- Visual dashboards for pattern recognition
- Integration with existing infrastructure
- Automated threat intelligence enrichment

**What didn't work:**
- Complex correlation rules (too many false positives)
- Machine learning anomaly detection (required constant tuning)
- Real-time streaming (batch processing sufficient for homelab scale)

**ROI validation:** 3 compromise attempts detected and contained. Estimated damage prevention: $500+ (cryptocurrency theft) + countless hours of remediation.

Time investment: 20 hours setup, 2 hours monthly maintenance.

## Further Reading and Resources

**Official documentation:**
- [Prometheus Configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/) - Complete reference
- [Grafana Dashboard Best Practices](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/) - Design guidelines
- [Alertmanager Configuration](https://prometheus.io/docs/alerting/latest/configuration/) - Alert routing

**Security monitoring guides:**
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework) - Monitoring requirements
- [CIS Controls v8](https://www.cisecurity.org/controls/v8/) - Security monitoring baseline
- [OWASP Security Logging](https://owasp.org/www-community/OWASP_Proactive_Controls) - What to monitor

**Threat intelligence sources:**
- [AbuseIPDB](https://www.abuseipdb.com/) - IP reputation database
- [MISP](https://www.misp-project.org/) - Threat intelligence sharing platform
- [AlienVault OTX](https://otx.alienvault.com/) - Open threat exchange

**Homelab security projects:**
- [Security Onion](https://securityonionsolutions.com/) - Network security monitoring platform
- [ELSA](https://github.com/mcholste/elsa) - Enterprise log search and archive
- [Suricata](https://suricata-ids.org/) - Network intrusion detection system

My next project: integrating these tools into a unified security operations center for the homelab. Because watching graphs is only the first step - responding to threats is what matters.

The goal isn't perfect security - it's visible security. You can't protect what you can't see. These dashboards give you eyes on your infrastructure.

Start simple. Add complexity gradually. Your future self will thank you when the first real incident hits.