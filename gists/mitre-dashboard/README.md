# MITRE ATT&CK Threat Intelligence Dashboard

A personal threat intelligence dashboard that aggregates open-source threat feeds and maps them to the MITRE ATT&CK framework for actionable intelligence.

## Overview

This dashboard reduces threat intelligence noise by 94% (from 10,000+ daily indicators to ~600 relevant ones) by focusing on ATT&CK technique-based threat correlation.

**Source Blog Post:** [Building Your Own MITRE ATT&CK Threat Intelligence Dashboard](https://williamzujkowski.github.io/posts/threat-intelligence-mitre-attack-dashboard/)

## Features

- **MITRE ATT&CK Integration**: Automatically fetches latest ATT&CK framework data via STIX
- **Threat Feed Aggregation**: Integrates AlienVault OTX, CISA KEV, and custom feeds
- **Interactive Visualizations**: Heatmaps and timelines with Plotly
- **Threat Actor Profiling**: Matches observed TTPs to known threat actors
- **Automated Alerting**: Email notifications for high-priority threats
- **Real-time Updates**: Hourly collection with async architecture

## Files

| File | Purpose | Lines |
|------|---------|-------|
| `dashboard-core.py` | Main dashboard class with initialization | ~60 |
| `attack-data-loader.py` | MITRE ATT&CK data fetching and processing | ~50 |
| `alienvault-collector.py` | AlienVault OTX pulse integration | ~40 |
| `cisa-alert-mapper.py` | CISA KEV alert mapping | ~35 |
| `threat-actor-profiler.py` | Threat actor attribution | ~45 |
| `threat-visualizer.py` | Plotly visualization generation | ~40 |
| `threat-alerting.py` | Alert generation and email notifications | ~35 |
| `dashboard-main.py` | Main application loop | ~35 |

## Prerequisites

```bash
pip install aiohttp stix2 OTXv2 plotly requests
```

## Quick Start

```python
# Initialize dashboard
from dashboard_main import MITREDashboard

dashboard = MITREDashboard()
await dashboard.run()
```

## Configuration

Edit `dashboard-main.py` to configure:

- Threat feed API keys (AlienVault OTX)
- SMTP settings for alerting
- Priority techniques for alerting
- Update frequency (default: hourly)

## Results

After 6 months of operation:

- **Noise reduction**: 94% (10,000+ → ~600 indicators)
- **Detection time**: Average 4 hours from publication to alert
- **Technique coverage**: 47 high-frequency techniques = 91% attack coverage
- **Actor attribution**: 3 targeted campaigns identified early

## Architecture

```
ThreatIntelligenceDashboard
├── ATTACKDataLoader (STIX processing)
├── AlienVaultCollector (OTX API)
├── CISAAlertMapper (KEV feed)
├── ThreatVisualizer (Plotly charts)
├── ThreatActorProfiler (Attribution)
└── ThreatAlerting (Email notifications)
```

## Customization

1. **Identify critical assets** and their attack surface
2. **Map defensive capabilities** to ATT&CK techniques
3. **Prioritize techniques** you can't currently detect
4. **Focus feeds** on your industry and technology stack
5. **Tune alerting** based on false positive rates

## License

MIT License - Free for personal and commercial use

## Related Resources

- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [AlienVault OTX](https://otx.alienvault.com/)
- [CISA Known Exploited Vulnerabilities](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/)

---

**Author:** William Zujkowski
**Blog:** https://williamzujkowski.github.io/
