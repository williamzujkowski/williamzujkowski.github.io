---

author: William Zujkowski
date: 2025-02-10
lastUpdate: 2026-09-13
description: "A homelab security automation design, with archived Python fragments and a corrected account of their dependencies and limitations."
title: Automating Home Network Security with Python and Open Source Tools
tags:
  - automation
  - homelab
  - networking
  - open-source
  - python
  - security
---
## The Problem: Security Doesn't Scale Without Automation

My process used to be: check the router admin page when I remembered to, glance at the Pi-hole dashboard once a week, and otherwise assume nothing had gone wrong since the last look. That held up fine, right up until an unrecognized device sat quietly on the LAN for who knows how long before I noticed. With 25+ connected devices and a family that does not share my threat model, "I'll check on it later" stopped being a security posture.


<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/network-auto.png'); width: min(300px, 78%); aspect-ratio: 400/353; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">a guard that never sleeps</p>

## Requirements

**Dependency correction, September 13, 2026:** The original command incorrectly listed Python standard-library modules as packages and used `nmap` where the intended Python distribution is `python-nmap`. The linked scripts are incomplete fragments; installing their imports does not make them runnable automation.

**Artifact correction, September 13, 2026:** All six implementation gists below are now marked archived and unsupported. Five fail Python syntax checks; the firewall fragment parses but refers to undefined names in its class body. Earlier wording presented these fragments as working scripts. The sections below now describe their intended roles and the missing implementation. The files remain available as historical records, with no deployment or scheduling instructions. [Artifact review and verification](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/628).

For Python 3.11, `collections`, `email`, `ipaddress`, `smtplib`, `sqlite3`, and `subprocess` are supplied by the [standard library](https://docs.python.org/3.11/library/index.html). An optional virtual environment lets you inspect the third-party imports; reading the archived fragments requires no installation:

```bash
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install python-nmap requests vulners
```

The [`python-nmap` distribution](https://pypi.org/project/python-nmap/0.7.1/) supplies `import nmap`. It wraps the separate [Nmap executable](https://nmap.org/book/install.html), which must be installed and available on `PATH` before scanning. The other external imports are [`requests`](https://pypi.org/project/requests/) and [`vulners`](https://pypi.org/project/vulners/). None of the inspected fragments imports `schedule`.

The [corrected requirements file](https://gist.github.com/williamzujkowski/7bb056a1b487f9fc2e4a61f9a76ab8a4) contains the same three distribution names. A clean Python 3.11.12 environment installed and imported `python-nmap` 0.7.1, `requests` 2.34.2, and `vulners` 4.3.0 on September 13, 2026. This verifies dependency installation and imports only; no scan, API request, firewall change, or notification ran. These are current verification versions, not a reconstruction of the February 2025 environment. [Inspection and validation record](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/main/docs/research/2026-09-13-network-helper-maintenance.md).

Managing home network security is like being a one-person SOC (Security Operations Center). You've got multiple devices, various family members with different tech literacy levels, and new threats emerging daily. Manual security management doesn't scale. Especially when you're also trying to be present for bedtime stories.

After running my [home network](/posts/2025-04-24-building-secure-homelab-adventure) with 25+ connected devices (including IoT gadgets, family laptops, and that inevitable "smart" toaster), I've developed Python scripts and automation workflows that maintain security without sacrificing family time.

This post shares what I've learned from automating my own network defense.

## The Foundation: Network Discovery and Asset Management

First challenge: knowing what's actually on your network. New devices appear constantly – kids' friends' phones, that new smart gadget someone bought, the mysterious device that might be the neighbor's printer.

True story: Years ago, I spent an hour hunting down an "ESP_8266_UNKNOWN" device on my network. I was ready to declare a security incident when my wife walked in: "Oh, that's probably the smart light bulb I installed in the guest bathroom."

Silence.

"You installed a what now?"

That's when I realized we needed automation – not just for security, but for marital harmony.

### Automated Device Discovery

Device discovery was intended to identify new devices and feed an alert. The archived fragment contains imports and a print statement, but omits discovery, state comparison, scheduling, and notification. It cannot perform the hourly discovery or immediate alerts previously attributed to it.

🔖 [Archived device-discovery fragment — incomplete and unsupported ↗](https://gist.github.com/williamzujkowski/2abad62ff98d044d09102ae06ecf3b0f)

## DNS Monitoring and Ad Blocking

One of the most effective security measures is controlling DNS. I use Pi-hole for ad blocking but enhanced it with security monitoring.

### Detecting Suspicious DNS Queries

The DNS-monitoring design called for reading query logs and identifying suspicious patterns. The fragment omits both the log reader and detection logic, leaving imports and an unmatched closing brace.

🔖 [Archived DNS-monitoring fragment — incomplete and unsupported ↗](https://gist.github.com/williamzujkowski/6c7c754be164e75b84f6b9e601753531)

## Automated Vulnerability Scanning

The intended vulnerability-scanning step combined service discovery with vulnerability lookup. The fragment imports the wrappers but supplies neither operation nor a scheduler; its `return report` has no enclosing function or report construction. It does not implement the weekly scan previously described here.

🔖 [Archived vulnerability-scanning fragment — incomplete and unsupported ↗](https://gist.github.com/williamzujkowski/e3e41c782e4099a06a6ac1f482cd3119)

## Smart Firewall Rules Management

The firewall fragment was intended to update filtering rules. Its only operation is a call in the class body to an undefined method, using undefined `self` and `country_code` names. There is no working rule-update procedure to deploy.

🔖 [Archived firewall fragment — incomplete and unsupported ↗](https://gist.github.com/williamzujkowski/6af94c70d3afd57829d26c12940d1cb1)

## Notification System

Notifications would make the earlier checks visible to the person responsible for the network. This fragment imports mail and HTTP libraries, then calls a missing `send_email` method with undefined content. Message delivery, configuration, and error handling are absent.

🔖 [Archived notification fragment — incomplete and unsupported ↗](https://gist.github.com/williamzujkowski/f025bd03e6d265b8aa9fdb8d73df9740)

## Putting It All Together

An orchestrator would need to connect the checks and handle their failures. The archived file refers to `SecurityOrchestrator`, but supplies no class definition or coordination logic. Combining the fragments above does not fill those gaps.

🔖 [Archived orchestration fragment — incomplete and unsupported ↗](https://gist.github.com/williamzujkowski/9cc496653878271d7045108bead98a65)

## Lessons Learned

### 1. Start with Visibility
You can't secure what you can't see. Network discovery and asset management should be your first automation project.

### 2. Alert Fatigue is Real
Fine-tune your alerts. Too many notifications and you'll start ignoring them. I learned this the hard way when I received 47 alerts in a single evening (turned out my kids were streaming Netflix on multiple devices simultaneously, triggering bandwidth anomaly detection). Now I use severity thresholds and rate limiting – my phone stays sane.

### 3. Family-Friendly Automation
Your security automation shouldn't disrupt family life. Useful design requirements include:
- Whitelisting for family devices
- "Quiet hours" for non-critical alerts
- Easy override mechanisms

### 4. Test in Isolation
Always test security automation in an isolated environment first. I once accidentally blocked my entire home network for 2 hours while troubleshooting. The family was... not amused.

### 5. Document Everything
Future you (or your family when you're not home) needs to understand how to disable things. I maintain a simple wiki with:
- What each script does
- How to temporarily disable automation
- Emergency contacts

## Tools and Resources

Here are the key tools I use in my homelab:
- **nmap 7.94.0**: Network discovery and port scanning
- **Pi-hole**: DNS filtering and logging (I configured mine on a [Raspberry Pi 4](/posts/2024-09-15-running-llama-raspberry-pi-pipeload))
- **Dream Machine Professional**: Firewall and routing
- **Python 3.11** with the third-party imports shown in the fragments: python-nmap, requests, vulners; see the dated dependency correction above.
- **Notification**: Pushover for mobile alerts

For background on encryption, see [demystifying cryptography](/posts/2024-01-18-demystifying-cryptography-beginners-guide/).

## What's Next?

Security automation is an ongoing journey. My upcoming projects include:
- Machine learning for anomaly detection
- Automated incident response playbooks
- Integration with threat intelligence feeds
- Voice alerts for critical events ("Alexa, announce security alert")

## Conclusion

Automating home network security has transformed my approach to protecting my family's digital life. Instead of constantly checking logs and running manual scans, I can focus on improving defenses while automation handles the routine work.

Remember: the goal isn't to build Fort Knox, it's to raise the bar high enough that attackers move on to easier targets. Automation helps you maintain that bar without burning out.



## Further Reading

For more in-depth information on the topics covered in this post:

[NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

[OWASP Top 10](https://owasp.org/www-project-top-ten/)

- [Cloudflare Learning Center](https://www.cloudflare.com/learning/)
- [RFC Editor](https://www.rfc-editor.org/)
