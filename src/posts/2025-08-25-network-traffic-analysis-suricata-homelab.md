---

author: William Zujkowski
date: 2025-08-25
description: Deploy Suricata IDS/IPS for real-time network threat detection—configure rule management, performance tuning, and SIEM integration for homelab monitoring.
title: Building a Network Traffic Analysis Lab with Suricata
images:
  hero:
    src: /assets/images/blog/hero/2025-08-25-network-traffic-analysis-suricata-homelab-hero.jpg
    alt: network topology and connections for Building a Network Traffic Analysis Lab with Suricata
    caption: Visual representation of Building a Network Traffic Analysis Lab with Suricata
    width: 1200
    height: 630
  og:
    src: /assets/images/blog/hero/2025-08-25-network-traffic-analysis-suricata-homelab-og.jpg
    alt: network topology and connections for Building a Network Traffic Analysis Lab with Suricata
tags:
  - homelab
  - networking
  - security
  - threat-detection

---
## The Invisible Threat

![Network monitoring visualization with glowing connections](https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1920&q=80)
*Photo by Alina Grubnyak on Unsplash*

Last year, I noticed unusual DNS queries from my homelab network. Hundreds of requests to obscure domains at 3 AM. Without network monitoring, I would never have caught the IoT device beaconing home to its manufacturer with telemetry data I didn't authorize.

That incident convinced me: you can't protect what you can't see. If you're [building a security-focused homelab](/posts/2025-04-24-building-secure-homelab-adventure), network traffic analysis with Suricata should be a core component of your monitoring strategy.

## Network Traffic Analysis Architecture

⚠️ **Warning:** Network traffic analysis must comply with privacy laws and organizational policies. Deploy only on networks you own or have explicit authorization to monitor.

```mermaid
flowchart TB
    subgraph trafficcollection["Traffic Collection"]
        Mirror[Port Mirroring]
        Tap[Network TAP]
        Span[SPAN Port]
    end
    subgraph suricataengine["Suricata Engine"]
        Capture[Packet Capture]
        Decode[Protocol Decoder]
        Detection[Detection Engine]
        Logger[Event Logger]
    end
    subgraph rulemanagement["Rule Management"]
        Emerging[Emerging Threats]
        Custom[Custom Rules]
        ETPRO[ET Pro Rules]
        Update[Rule Updates]
    end
    subgraph analysisresponse["Analysis & Response"]
        EVE[EVE JSON Logs]
        Filebeat[Filebeat Shipper]
        Elastic[Elasticsearch]
        Kibana[Kibana Dashboard]
        Wazuh[Wazuh SIEM]
    end

    Mirror --> Capture
    Tap --> Capture
    Span --> Capture

    Capture --> Decode
    Decode --> Detection
    Detection --> Logger

    Emerging --> Detection
    Custom --> Detection
    ETPRO --> Detection
    Update --> Detection

    Logger --> EVE
    EVE --> Filebeat
    Filebeat --> Elastic
    Filebeat --> Wazuh
    Elastic --> Kibana

    classDef criticalStyle fill:#f44336,color:#fff
    classDef successStyle fill:#4caf50,color:#fff
    classDef infoStyle fill:#00bcd4,color:#fff
    class Detection criticalStyle
    class Elastic successStyle
    class Kibana infoStyle
```

Building my network traffic analysis lab with Suricata transformed my homelab from a black box into a transparent, monitored environment. Here's how I did it.

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

I run Suricata on my Dell R940 with:
- **CPU**: 8 cores dedicated to packet processing
- **RAM**: 16GB allocated
- **Storage**: 500GB SSD for fast log writes
- **NIC**: Dedicated 10Gb interface for mirrored traffic

## Suricata Installation and Configuration

### Installing Suricata

<script src="https://gist.github.com/williamzujkowski/ac871dd21758d0f1f44986c4ee6e21e7.js"></script>

## Writing Custom Suricata Rules

### Rule Syntax Basics

Suricata rules follow this structure:

⚠️ **Warning:** Network detection rules must be tested in lab environments before production deployment. Improper rules can cause false positives or network disruption.

```text
action protocol source_ip source_port -> dest_ip dest_port (rule options)
```

### Custom Detection Rules

One particularly valuable use case is detecting suspicious IoT device behavior. After working through [lessons from OWASP IoTGoat on IoT security](/posts/2025-09-20-iot-security-homelab-owasp), I developed custom rules to catch the most common IoT attack patterns:

<script src="https://gist.github.com/williamzujkowski/fdd48db6a837ca02c00c79f7c4fd6cde.js"></script>

## Testing and Validation

<script src="https://gist.github.com/williamzujkowski/55bec7428ee6cb7ba25a59a6aabca57d.js"></script>

## Integration with SIEM

<script src="https://gist.github.com/williamzujkowski/4f6b12b16ec06c596b3baefe837ecf95.js"></script>

## Visualization with Kibana

### Creating Suricata Dashboard

```bash
# Import Suricata dashboards
sudo filebeat setup --dashboards -E output.elasticsearch.hosts=["10.0.1.5:9200"]
```

Custom visualization queries:

<script src="https://gist.github.com/williamzujkowski/35c585bdda7f328093d18b40c29ccb22.js"></script>

## Advanced Detection Techniques

<script src="https://gist.github.com/williamzujkowski/a6630cefcbe03030515d0b3310251b7a.js"></script>

## Operational Best Practices

<script src="https://gist.github.com/williamzujkowski/d370286436bb31c998340c63afe8e501.js"></script>

## Incident Response Workflow

When Suricata triggers an alert:

1. **Triage**: Review alert in Kibana dashboard
2. **Investigate**: Extract full PCAP for the flow
3. **Analyze**: Review payload and context
4. **Contain**: Block malicious IPs/domains
5. **Remediate**: Clean affected systems
6. **Document**: Update runbooks

## Lessons Learned

After running Suricata in production for years:

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

## Research & References

### IDS/IPS Technology

1. **[Snort vs Suricata Performance](https://ieeexplore.ieee.org/document/8726695)** (2019)
   - IEEE - Comparative analysis of IDS performance

2. **[Suricata Official Documentation](https://docs.suricata.io/)** - Comprehensive configuration guide

### Threat Detection Research

1. **[Machine Learning for Intrusion Detection](https://arxiv.org/abs/1904.02426)** (2019)
   - arXiv preprint - ML-based network anomaly detection

2. **[MITRE ATT&CK for Network Defense](https://attack.mitre.org/)** - Adversary tactics and techniques

### Rule Development

- **[Emerging Threats Rules](https://rules.emergingthreats.net/)** - Community ruleset
- **[Suricata Language Reference](https://suricata.readthedocs.io/en/latest/rules/index.html)** - Rule syntax documentation
- **[OISF GitHub](https://github.com/OISF/suricata)** - Suricata source code and examples

## Conclusion

Network traffic analysis with Suricata transformed my homelab from an opaque network into a monitored, understood environment. The visibility gained from IDS/IPS isn't just about catching threats. It's about understanding normal behavior so you can spot anomalies.

Start with basic installation, enable Emerging Threats rules, and gradually add custom detections for your specific environment. The investment in proper monitoring pays dividends the first time you catch an incident before it escalates.

---

*Running Suricata in your environment? What detection rules have proven most valuable? Share your custom rules and detection strategies. Let's build better defenses together!*
