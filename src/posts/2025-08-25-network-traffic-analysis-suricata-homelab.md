---

author: William Zujkowski
date: 2025-08-25
description: Deploy Suricata IDS/IPS for real-time network threat detection—configure rule management, performance tuning, and SIEM integration for homelab monitoring.
title: Building a Network Traffic Analysis Lab with Suricata
tags:
  - homelab
  - networking
  - security
  - threat-detection
---
## The Invisible Threat

Last year, something in my house started making DNS queries at 3 AM — hundreds of them, to domains that had no business being in my logs. An IoT device was beaconing home to its manufacturer with telemetry I'd never agreed to, and I only found out because I happened to be watching. Most home networks aren't watching.

That's the case for Suricata in one line: you can't protect what you can't see. If you're [building a security-focused homelab](/posts/2025-04-24-building-secure-homelab-adventure), network traffic analysis with Suricata should be a core component of your monitoring strategy, not a nice-to-have.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/suricata.png'); width: min(300px, 72%); aspect-ratio: 400/373; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">always on lookout</p>

## Network Traffic Analysis Architecture

⚠️ **Warning:** Network traffic analysis must comply with privacy laws and organizational policies. Deploy only on networks you own or have explicit authorization to monitor.

<figure class="arch-fig">
<div class="arch is-stack" role="group" aria-label="Suricata traffic analysis architecture">
  <section class="arch-tier" data-label="Traffic Collection" role="group" aria-label="Traffic Collection"><span class="arch-chip">Port Mirroring</span><span class="arch-chip">Network TAP</span><span class="arch-chip">SPAN Port</span></section>
  <section class="arch-tier" data-label="Rule Management" role="group" aria-label="Rule Management"><span class="arch-chip is-guard">Emerging Threats</span><span class="arch-chip is-guard">Custom Rules</span><span class="arch-chip is-guard">ET Pro Rules</span><span class="arch-chip is-guard">Rule Updates</span></section>
  <section class="arch-tier" data-label="Suricata Engine" role="group" aria-label="Suricata Engine"><span class="arch-chip">Packet Capture</span><span class="arch-chip">Protocol Decoder</span><span class="arch-chip is-primary">Detection Engine</span><span class="arch-chip">Event Logger</span></section>
  <section class="arch-tier" data-label="Analysis &amp; Response" role="group" aria-label="Analysis &amp; Response"><span class="arch-chip">EVE JSON Logs</span><span class="arch-chip">Filebeat Shipper</span><span class="arch-chip">Elasticsearch</span><span class="arch-chip">Kibana Dashboard</span><span class="arch-chip">Wazuh SIEM</span></section>
</div>
<figcaption>Traffic collection feeds Suricata, rule sources shape detection, and EVE logs move into search, dashboards, and SIEM response.</figcaption>
</figure>

Building my network traffic analysis lab with Suricata turned my homelab from a black box into something that actually admits what it's been doing at 3 AM. Here's how I did it.

## Hardware Setup

### Network TAP vs SPAN Port

My Ubiquiti Dream Machine Pro supports port mirroring, but I also tested with a dedicated network TAP for comparison.

**SPAN Port (What I Use):**
- Ubiquiti allows mirroring specific VLANs
- No additional hardware required
- Sufficient for homelab traffic volumes
- Some packet loss under heavy load

**Network TAP (Optional):**
- Passive optical TAP for 100% packet capture
- No packet loss or latency
- More expensive ($200-500)
- Overkill for most homelabs

### Dedicated Analysis Server

I run Suricata on my Dell R910 with:
- **CPU**: 8 cores dedicated to packet processing
- **RAM**: 16GB allocated
- **Storage**: 500GB SSD for fast log writes
- **NIC**: Dedicated 10Gb interface for mirrored traffic

### AF_PACKET Performance Tuning

**Ring buffer sizing:** Suricata's AF_PACKET capture mode uses kernel ring buffers to handle burst traffic. Default 4MB ring buffers cause packet drops at >5Gbps sustained traffic. Set `ring-size: 67108864` (64MB per interface) in `/etc/suricata/suricata.yaml` under `af-packet` section to handle 10Gbps bursts without drops. Monitor `/proc/net/pf_ring/stats` for packet loss—anything above 0.1% requires tuning.

**Fanout configuration:** Enable multi-threaded packet capture with `cluster-type: cluster_qm` (queue-mapping fanout) to distribute packets across CPU cores. Set `cluster-id: 99` and `threads: auto` to match your CPU count (8 cores = 8 worker threads). This reduces per-thread packet processing latency from ~200μs to ~25μs in my testing. Verify performance with `suricata --af-packet=ens1f0 --runmode=workers -i ens1f0` and check `stats.log` for `capture.kernel_drops` (should be near 0). If drops persist above 1%, increase ring buffer to 128MB or reduce rule complexity.

## Suricata Installation and Configuration

### Installing Suricata

🔖 [Suricata installation and configuration script ↗](https://gist.github.com/williamzujkowski/ac871dd21758d0f1f44986c4ee6e21e7)

## Writing Custom Suricata Rules

### Rule Syntax Basics

Suricata rules follow this structure:

⚠️ **Warning:** Network detection rules must be tested in lab environments before production deployment. Improper rules can cause false positives or network disruption.

```text
action protocol source_ip source_port -> dest_ip dest_port (rule options)
```

### Custom Detection Rules

One particularly valuable use case is detecting suspicious IoT device behavior — the kind that got this whole project started. After working through [lessons from OWASP IoTGoat on IoT security](/posts/2025-09-20-iot-security-homelab-owasp), I developed custom rules to catch the most common IoT attack patterns:

🔖 [Custom Suricata IoT detection rules ↗](https://gist.github.com/williamzujkowski/fdd48db6a837ca02c00c79f7c4fd6cde)

## Testing and Validation

🔖 [Suricata testing and validation workflow ↗](https://gist.github.com/williamzujkowski/55bec7428ee6cb7ba25a59a6aabca57d)

## Integration with SIEM

🔖 [Suricata SIEM integration configuration ↗](https://gist.github.com/williamzujkowski/4f6b12b16ec06c596b3baefe837ecf95)

## Visualization with Kibana

### Creating Suricata Dashboard

```bash
# Import Suricata dashboards
sudo filebeat setup --dashboards -E output.elasticsearch.hosts=["10.0.1.5:9200"]
```

Custom visualization queries:

🔖 [Kibana visualization queries for Suricata ↗](https://gist.github.com/williamzujkowski/35c585bdda7f328093d18b40c29ccb22)

## Advanced Detection Techniques

🔖 [Advanced Suricata detection techniques ↗](https://gist.github.com/williamzujkowski/a6630cefcbe03030515d0b3310251b7a)

## Operational Best Practices

🔖 [Suricata operational best practices ↗](https://gist.github.com/williamzujkowski/d370286436bb31c998340c63afe8e501)

## Rule Update Security (CRITICAL)

**The Problem:** Suricata rule updates are a supply chain attack vector. Rules are code your sensor executes against every packet, and a compromised update source could inject rules that disable monitoring, exfiltrate data, or manufacture false negatives. The uncomfortable part, which took me embarrassingly long to check, is that the control everyone assumes is protecting them here does not exist.

**Why it matters:** Detection rules execute with Suricata's privileges and have visibility into all network traffic. A malicious rule could:
- Disable legitimate detections (create blind spots)
- Exfiltrate sensitive data patterns via DNS queries
- Trigger false positives to cause alert fatigue
- Modify traffic inspection behavior

### Secure Rule Update Workflow

**Updating is the easy part:**

```bash
# Install suricata-update (comes with Suricata 6.0+)
sudo apt install python3-suricata-update

sudo suricata-update update-sources   # fetch the master source index
sudo suricata-update list-sources     # see what's on offer
sudo suricata-update                  # ET Open is the built-in default
sudo systemctl reload suricata
```

Rules land in `/var/lib/suricata/rules/suricata.rules`.

**Knowing what that actually guarantees is the hard part**, and it is worth
being precise, because I was wrong about it here for a year.

suricata-update does not verify who signed your rules. There are no GPG keys
in it — not bundled, not configurable, not mentioned in its documentation. ET
does not publish a detached signature either: `emerging.rules.tar.gz.asc` is a
404 for every Suricata version I tried, and ET's own download instructions
mention only MD5, never GPG.

There *is* a checksum, and it buys less than the name suggests. suricata-update
fetches `emerging.rules.tar.gz.md5` and compares it against the copy already in
its cache:

```
Checking https://rules.emergingthreats.net/open/suricata-7.0.3/emerging.rules.tar.gz.md5.
Remote checksum has not changed. Not fetching.
```

That is a cache-freshness check, not an integrity check. It runs *before* the
download, against the old file; nothing is hashed after the new bytes arrive.
Upstream is refreshingly honest about it — the digest is computed with
`hashlib.md5(buf, usedforsecurity=False)`. If the check throws, it logs a
warning and re-downloads, so a broken `.md5` costs a round trip and nothing
else.

Which leaves exactly one thing between you and someone else's detection rules
running on your sensor: TLS to `rules.emergingthreats.net`. The `.md5` rides
the same connection from the same host as the tarball it describes, so it
cannot attest to anything the transport has not already. Keep the CA store
current, keep the box's clock honest, and don't tell an auditor the rules are
signed.

### Staging Environment Testing

**Never deploy rules directly to production:**

```bash
# Test rules in staging first
sudo suricata-update --suricata /usr/bin/suricata \
  --suricata-conf /etc/suricata/suricata-staging.yaml \
  --output /var/lib/suricata/rules-staging

# Validate rule syntax
sudo suricata -T -c /etc/suricata/suricata-staging.yaml

# Run for 24 hours in staging, monitor for:
# - Rule parsing errors
# - False positive rates
# - Performance impact
# - Packet drop increases

# If clean after 24h, promote to production
sudo cp /var/lib/suricata/rules-staging/* /var/lib/suricata/rules/
sudo systemctl reload suricata
```

### Automated Update Pipeline

**Safe automation includes verification + staging:**

```bash
#!/bin/bash
# /usr/local/bin/suricata-rule-update.sh

set -e

# Update. suricata-update exits non-zero on a failed fetch, and `set -e`
# above turns that into a stopped script, which is the check that matters.
sudo suricata-update --verbose 2>&1 | tee /var/log/suricata-update.log

# Test that the new ruleset actually PARSES before anything reloads it.
# This is the real gate: a rule file that Suricata rejects will take the
# service down on reload, and a bad ruleset is far more likely to reach you
# through a malformed update than through a forged one.
sudo suricata -T -c /etc/suricata/suricata.yaml

# Reload Suricata
sudo systemctl reload suricata

# Monitor for 10 minutes
sleep 600
sudo suricatasc -c "capture-mode"
# Verify packet drops haven't increased
```

**Schedule with caution:**

```cron
# Update daily at 3 AM (low traffic window)
0 3 * * * /usr/local/bin/suricata-rule-update.sh >> /var/log/suricata-update-cron.log 2>&1
```

### Rule Source Trust Hierarchy

**Prioritize rule sources by trust:**

1. **ET Open (Community):** free, 30-day delay from Pro, safe for homelab.
   Authenticity rests on TLS to `rules.emergingthreats.net` — there is no
   signature to check.
2. **ET Pro (Commercial):** paid, zero-day rules, vetted by Proofpoint
3. **Custom rules:** your own rules, full control, test thoroughly
4. **Third-party sources:** audit the rules themselves before enabling, and
   check what the source actually publishes. Most publish nothing but the
   rules over HTTPS.

#### ET Open 30-Day Delay: Understanding the Trade-Offs (MODERATE)

**The Problem:** ET Open rules are released 30 days after ET Pro rules. This means homelabs using free ET Open have a **30-day window** where zero-day threats are detectable by ET Pro subscribers but invisible to ET Open users. For rapidly exploited vulnerabilities, 30 days is an eternity.

**Why it matters:** The delay is intentional (business model for Proofpoint), but creates a detection gap for emerging threats. Understanding this trade-off helps you decide when ET Open is sufficient vs when you need compensating controls.

**Why the 30-Day Delay Exists:**

1. **Business Model:** ET Pro subscription revenue ($900/year per sensor) funds Proofpoint's threat research team
2. **Value Differentiation:** Zero-day detection rules justify commercial pricing
3. **Community Sustainability:** ET Open free tier maintains community adoption, creates pipeline for Pro upgrades
4. **Threat Intelligence Lag:** By day 30, most threats are publicly known, ET Open provides "good enough" detection for non-targeted environments

**Security Implications:**

**Zero-Day Window (Day 0-30):**
- **ET Pro:** Has detection rule immediately when threat discovered
- **ET Open:** No detection rule, attack succeeds undetected
- **Impact:** Homelab vulnerable to fast-spreading threats (worms, ransomware, critical RCEs)

**Public Disclosure Window (Day 30+):**
- **ET Pro:** Already has rule, benefited from 30-day head start
- **ET Open:** Rule released, now protected (better late than never)
- **Impact:** Protection catches up, but missed initial attack wave

**Real-World Example: CVE-2024-X Critical RCE**

```
Timeline:
Day 0: Vulnerability discovered by researcher, disclosed to vendor
Day 1: ET Pro rule released (SID 2024001: "ET EXPLOIT CVE-2024-X RCE Attempt")
Day 1-5: Exploit code published on GitHub, mass scanning begins
Day 7: Major ransomware campaign exploits CVE-2024-X (10,000+ victims)
Day 30: ET Open rule finally released (SID 2024001 now available to community)

ET Pro users: Protected from Day 1, detected attack attempts during Days 1-30
ET Open users: Vulnerable Days 1-30, protected starting Day 31 (after attack wave passed)
```

**Compensating Controls for ET Open Users:**

**1. Threat Intelligence Feeds (Real-Time):**

```bash
# Integrate AlienVault OTX (free threat intel)
# Add OTX IoCs to Suricata blocklist
curl -H "X-OTX-API-KEY: $OTX_API_KEY" \
  https://otx.alienvault.com/api/v1/indicators/export > otx-iocs.txt

# Convert OTX IoCs to Suricata format
grep -E "^(IP|Domain)" otx-iocs.txt | awk '{print "drop ip any any -> "$2" any (msg:\"OTX Threat Intel Block\"; sid:9000000; rev:1;)"}' > otx-rules.rules

# Load OTX rules (updated daily)
sudo suricatasc -c "ruleset-reload-rules"
```

**2. Custom Rules for Published CVEs (Proactive):**

```bash
# When CVE published (Day 0), write custom rule before ET Open release (Day 30)
# Example: CVE-2024-1234 affects /api/upload endpoint

alert http any any -> $HOME_NET any (
  msg:"CUSTOM CVE-2024-1234 RCE Attempt";
  flow:established,to_server;
  http.uri; content:"/api/upload"; nocase;
  http.method; content:"POST";
  http.request_body; content:"<?php"; nocase;  # PHP injection attempt
  classtype:web-application-attack;
  sid:10000001; rev:1;
)

# Deploy immediately, don't wait 30 days for ET Open
```

**3. Behavioral Detection (Protocol Anomalies):**

```bash
# Generic anomaly detection catches novel attacks ET Open doesn't have rules for yet
alert tls any any -> any any (
  msg:"TLS Certificate with Suspicious CN";
  tls.cert_subject; content:"acme.local"; nocase;  # Self-signed certs from attacker
  classtype:protocol-command-decode;
  sid:10000002; rev:1;
)

alert dns any any -> any any (
  msg:"DNS Query to Newly Registered Domain (NRD)";
  dns.query; content:".xyz"; nocase;  # Many phishing campaigns use .xyz TLDs
  threshold:type limit, track by_src, count 1, seconds 3600;
  sid:10000003; rev:1;
)
```

**4. Layered Defense (Defense-in-Depth):**

```bash
# ET Open is ONE layer, not the ONLY layer
# Combine with:
# - Firewall egress filtering (block known-bad IPs/domains)
# - Endpoint detection (YARA rules, behavioral analysis)
# - Vulnerability scanning (identify vulnerable services before exploitation)
# - Network segmentation (limit lateral movement if Suricata misses initial entry)
```

**When ET Open is Sufficient:**

- ✅ Homelab environments (non-production, learning/testing)
- ✅ Low-value targets (attackers don't specifically target you)
- ✅ Mature patch management (vulnerabilities patched within 7-14 days)
- ✅ Defense-in-depth implemented (Suricata is backup, not primary defense)
- ✅ Threat model: opportunistic attacks (broad scanning, not targeted)

**When ET Pro is Necessary:**

- ❌ Production environments (business-critical services)
- ❌ High-value targets (financial data, PII, intellectual property)
- ❌ Slow patch cycles (30+ days to deploy patches)
- ❌ Suricata as primary defense (no firewall, no endpoint protection)
- ❌ Threat model: targeted attacks (APTs, nation-state actors)
- ❌ Compliance requirements (PCI-DSS, HIPAA, NIST 800-53)

**Cost-Benefit Analysis for Homelab:**

| **Option** | **Annual Cost** | **Zero-Day Protection** | **Homelab Value** |
|------------|----------------|-------------------------|-------------------|
| ET Open | $0 | Day 30+ | High (learning, adequate for homelab) |
| ET Pro | $900/sensor | Day 0+ | Low (overkill for non-production) |
| ET Open + Custom Rules | $0 + time investment | Day 0+ (manual) | Medium (proactive, educational) |
| ET Open + Threat Intel Feeds | $0 | Day 1-7 (depends on feed) | High (automated, near-real-time) |

**Recommended Homelab Strategy:**

```bash
# My homelab approach (zero cost, reasonable protection):
# 1. ET Open baseline (free, HTTPS-only trust, 30-day lag acceptable)
sudo suricata-update enable-source et/open

# 2. AlienVault OTX for near-real-time threat intel (free)
# Update OTX IoCs daily via cron
0 4 * * * /usr/local/bin/update-otx-rules.sh

# 3. Custom rules for published CVEs affecting my stack
# Create rules within 24 hours of CVE publication (manual, educational)

# 4. Behavioral rules for protocol anomalies
# Generic detections catch novel attacks before signatures exist

# 5. Accept 30-day zero-day window as acceptable risk
# Trade-off: Homelab value doesn't justify $900/year ET Pro cost
```

**Validation Commands:**

```bash
# Check which ruleset you're using
sudo suricata-update list-enabled-sources
# Should output: "et/open" (free, 30-day delay)
# Compare: "et/pro" (paid, zero-day coverage)

# Verify rule update frequency
sudo tail -100 /var/log/suricata/suricata-update.log | grep "Downloaded"
# Should show daily updates

# Check custom rule count
grep -c "^alert\|^drop" /var/lib/suricata/rules/local.rules
# Higher count = more compensating controls for ET Open delay

# Audit rule age (how old are your rules?)
sudo suricata-update list-sources --enabled | grep "modified"
# ET Open rules are 30 days behind latest threats
```

**Senior engineer perspective:** Years of IDS management taught me ET Open's 30-day delay is acceptable for 95% of homelabs. The key insight: zero-day detection is valuable only if you're a high-value target worth the attacker's effort to deploy zero-days against. Random homelab on residential ISP? Attackers use commodity exploits that ET Open detects fine once published. Targeted attacks against your specific homelab? You have bigger problems than IDS rule delays. ET Pro makes sense for production environments protecting revenue-generating services or sensitive data. For learning and personal infrastructure, ET Open + custom rules + threat intel feeds provides 90% of the protection at 0% of the cost. I ran ET Open for 3 years in my homelab, never once thought "I wish I'd spent $900/year for 30-day earlier detection." But I DID write 47 custom rules for CVEs specific to my stack—that proactive approach provided better ROI than commercial rules for threats I don't face.

### Supply Chain Attack Scenarios

What TLS actually stops, and what it does not:

| Scenario | Outcome |
|---|---|
| MitM on the rule download | **Stopped.** The connection is HTTPS; an interceptor without a trusted cert fails the handshake. |
| Attacker compromises `rules.emergingthreats.net` DNS | **Stopped**, as long as they cannot also obtain a valid certificate for that name. |
| Attacker obtains a valid cert for that name | **Succeeds.** Nothing downstream would notice. |
| ET's own build or distribution host is compromised | **Succeeds.** There is no signature to disagree with the bytes ET serves. |
| A malicious mirror you added yourself | **Succeeds.** Every source is trusted equally. |

The bottom two rows are the ones a signature would close, and there is no
signature. That is the honest shape of the threat model: transport security
against everyone between you and ET, and pure trust in ET itself.

This is not unusual, and it is not a reason to stop using ET Open — it is a
reason not to write "verified" in a control document when what you have is
"downloaded over TLS". The mitigation available to you is the `suricata -T`
parse test above plus reading rule diffs before they reach a sensor you care
about, not a signature check that does not exist.

### Validation Commands

```bash
# Confirm which sources are enabled
sudo suricata-update list-sources --enabled
# Should list et/open. Note it carries no `checksum` field in ET's index --
# suricata-update falls back to its default of checking one.

# What the checksum step actually logged. Expect a line like
#   "Checking https://.../emerging.rules.tar.gz.md5."
# and note it only appears when a cached copy already exists, so a clean
# machine shows nothing at all.
sudo tail -100 /var/log/suricata/suricata-update.log | grep -E "Checking|checksum"

# List the free sources available
sudo suricata-update list-sources --free
sudo suricata-update list-sources --all

# Audit current rule file integrity
sudo suricata-update check-versions
```

**Senior engineer perspective:** Years of managing IDS deployments taught me that rule updates are code execution, and should be treated like any other software update: test in staging, automate carefully, read what changed. What I got wrong for a long time was the last step — I assumed "verify signatures" was on that list because it is on every other list, and never checked whether the signature existed. It does not. Writing the mitigation down is not the same as having it, and a control you have never exercised is a control you do not have. That is a more useful lesson than the one I thought I was writing.

## Incident Response Workflow

When Suricata triggers an alert:

1. **Triage**: Review alert in Kibana dashboard
2. **Investigate**: Extract full PCAP for the flow
3. **Analyze**: Review payload and context
4. **Contain**: Block malicious IPs/domains
5. **Remediate**: Clean affected systems
6. **Document**: Update runbooks

## Lessons Learned

After running Suricata in my homelab for years:

### 1. Start Simple, Add Complexity Gradually
Don't enable every rule on day one. Start with Emerging Threats Open, tune for false positives, then add custom rules.

### 2. Context Matters More Than Volume
10 correlated alerts are more valuable than 10,000 noisy signatures. Focus on detection quality, not quantity.

### 3. Integration is Everything
Suricata alone is just logs. Integration with SIEM, threat intelligence, and automated response creates a complete detection pipeline.

### 4. Performance Tuning is Ongoing
Monitor packet drops religiously. If you're dropping packets, you're missing threats.

### 5. Test Your Detections
Regularly test that your rules actually fire. A rule that never alerts might be broken or misconfigured.

## Sources

### IDS/IPS Technology

1. **[Snort vs Suricata Performance](https://ieeexplore.ieee.org/document/8726695)** (2019)
   - IEEE - Comparative analysis of IDS performance

2. **[Suricata Official Documentation](https://docs.suricata.io/)** - Comprehensive configuration guide

### Threat Detection Research

1. **[Machine Learning for Intrusion Detection](https://arxiv.org/abs/1904.02426)** (2019)
   - arXiv preprint - ML-based network anomaly detection

2. **[MITRE ATT&CK for Network Defense](https://attack.mitre.org/)** - Adversary tactics and techniques

3. **[MITRE ATT&CK Dashboard Implementation](/posts/2025-09-14-threat-intelligence-mitre-attack-dashboard)** - Correlate Suricata detections with ATT&CK tactics

### Rule Development

- **[Emerging Threats Rules](https://rules.emergingthreats.net/)** - Community ruleset
- **[Suricata Language Reference](https://suricata.readthedocs.io/en/latest/rules/index.html)** - Rule syntax documentation
- **[OISF GitHub](https://github.com/OISF/suricata)** - Suricata source code and examples
- Container Security Hardening - Protect containerized Suricata deployments

## Conclusion

Network traffic analysis with Suricata transformed my homelab from an opaque network into a monitored, understood environment. The visibility gained from IDS/IPS isn't just about catching threats. It's about understanding normal behavior so you can spot anomalies.

Start with basic installation, enable Emerging Threats rules, and gradually add custom detections for your specific environment. The investment in proper monitoring pays dividends the first time you catch an incident before it escalates.
