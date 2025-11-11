---
author: William Zujkowski
date: 2025-09-08
description: Implement zero trust with VLAN segmentation—secure homelab networks using micro-segmentation and layer 3 firewalls for defense in depth.
tags:
- security
- networking
- zero-trust
- vlan
- homelab
- ubiquiti
title: Implementing Zero Trust Microsegmentation with VLANs
images:
  hero:
    src: /assets/images/blog/hero/2025-09-08-zero-trust-vlan-segmentation-homelab-hero.jpg
    alt: network topology and connections for Implementing Zero Trust Microsegmentation with VLANs
    caption: Visual representation of Implementing Zero Trust Microsegmentation with VLANs
    width: 1200
    height: 630
  og:
    src: /assets/images/blog/hero/2025-09-08-zero-trust-vlan-segmentation-homelab-og.jpg
    alt: network topology and connections for Implementing Zero Trust Microsegmentation with VLANs
---
## The IoT Camera That Taught Me About Network Segmentation

![Network security and segmentation visualization](https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1920&q=80)
*Photo by Alina Grubnyak on Unsplash*

Years ago, I bought a cheap IP camera for my homelab. Within hours, it was beaconing to servers in China, scanning my network, and attempting to access my NAS. All because I put it on the same network as my trusted devices.

That camera is now in a VLAN jail, where it belongs. This experience became a core lesson in [building a security-focused homelab with VLANs](/posts/2025-04-24-building-secure-homelab-adventure), where network segmentation proved essential for containing untrusted devices.

## Zero Trust Network Architecture

```mermaid
flowchart TB
    subgraph internetedge["Internet Edge"]
        WAN[WAN Connection]
        UDM[Dream Machine Pro]
    end
    subgraph managementvlan10["Management VLAN 10"]
        Admin[Admin Devices]
        Proxmox[Proxmox Host]
        Switches[Network Switches]
    end
    subgraph trustedvlan20["Trusted VLAN 20"]
        Workstation[Workstations]
        Laptops[Laptops]
        Phones[Personal Phones]
    end
    subgraph servervlan30["Server VLAN 30"]
        Web[Web Servers]
        DB[Databases]
        Apps[Applications]
    end
    subgraph iotvlan40["IoT VLAN 40"]
        Camera[IP Cameras]
        Smart[Smart Devices]
        Sensors[IoT Sensors]
    end
    subgraph guestvlan50["Guest VLAN 50"]
        GuestDevices[Guest Devices]
    end
    subgraph securityservices["Security Services"]
        Firewall[Firewall Rules]
        IDS[Suricata IDS]
        DNS[Pi-hole DNS]
    end

    WAN --> UDM
    UDM --> Firewall

    Firewall --> Admin
    Firewall --> Workstation
    Firewall --> Web
    Firewall --> Camera
    Firewall --> GuestDevices

    Firewall --> IDS
    Firewall --> DNS

    classDef redNode fill:#f44336,color:#fff
    classDef orangeNode fill:#ff9800,color:#fff
    classDef deepOrangeNode fill:#ff5722,color:#fff
    class Firewall redNode
    class Camera,Smart,Sensors orangeNode
    class GuestDevices deepOrangeNode
```

## VLAN Design Philosophy

### The Zero Trust Principle

**Traditional approach:** Trust everything inside the network perimeter.
**Zero trust approach:** Verify explicitly, enforce least privilege, assume breach.

These principles build on the foundational concepts I explored in my guide to [zero trust architecture fundamentals](/posts/2024-07-09-zero-trust-architecture-implementation). VLAN segmentation is one practical implementation of those abstract security principles.

My VLAN design follows these principles:

1. **Default deny**: No traffic flows between VLANs unless explicitly allowed
2. **Least privilege**: Each VLAN has minimum required access
3. **Explicit allow**: Every connection must have a business justification
4. **Continuous monitoring**: Log and alert on anomalous traffic

### VLAN Segmentation Strategy

| VLAN ID | Name | Purpose | Trust Level | Internet Access |
|---------|------|---------|-------------|-----------------|
| 1 | Default | Unused (disabled) | None | No |
| 10 | Management | Network infrastructure | High | Limited |
| 20 | Trusted | Personal devices | High | Full |
| 30 | Servers | Production services | Medium | Controlled |
| 40 | IoT | Smart home devices | Low | Restricted |
| 50 | Guest | Visitor devices | None | Full (isolated) |
| 60 | Lab | Testing/experiments | Low | Full |
| 70 | DMZ | Public-facing services | Low | Full |

## Ubiquiti Dream Machine Pro Configuration

### Initial Setup

📎 **Complete configuration:**
[Full UDM Pro VLAN setup with all 7 VLANs](https://gist.github.com/williamzujkowski/5422062bf5c4c6054de281cb912ce5d9)

Each VLAN gets dedicated interface: `set interfaces ethernet eth1 vif <id> address <gateway>`

### DHCP Configuration

📎 **Complete configuration:**
[All VLAN DHCP configs with DNS and gateways](https://gist.github.com/williamzujkowski/f5de5f7a5b7e30b7eaa59de0bd55a91b)

Each VLAN subnet gets DHCP pool starting at .100 address

## Firewall Rules

### Rule Structure

Follow this rule ordering for predictable behavior:

1. Explicit allow rules (most specific first)
2. Logging rules
3. Explicit deny rules
4. Default deny (implicit)

### Management VLAN Rules

📎 **Complete ruleset:**
[All management firewall rules with logging](https://gist.github.com/williamzujkowski/088045937fa7c77821a67f31cf994556)

Management VLAN (10.0.10.0/24) can access all VLANs. All VLANs can SSH to management.

### IoT VLAN Rules (Most Restrictive)

📎 **Complete ruleset:**
[Full IoT isolation rules with default-deny](https://gist.github.com/williamzujkowski/42d5f269c97a1fbd8335316d09f90068)

IoT blocked from all VLANs. Only HTTP/HTTPS to internet allowed. These strict rules are essential for [IoT security with VLAN isolation](/posts/2025-09-20-iot-security-homelab-owasp), where untrusted devices need containment without breaking functionality.

### Server VLAN Rules

📎 **Complete ruleset:**
[Server VLAN firewall rules with update policies](https://gist.github.com/williamzujkowski/337822d5fca33ab0bbd5806204df73af)

Trusted VLAN can reach servers on HTTPS. Servers blocked from management VLAN.

## Advanced Segmentation Techniques

### Micro-Segmentation with mDNS Reflector

Allow service discovery across VLANs without full connectivity:

📎 **Complete configuration:**
[Full Avahi mDNS reflector setup for UDM Pro](https://gist.github.com/williamzujkowski/2b9b624d76d9a7f139cbcbd914559a2b)

Enable Avahi reflector for AirPlay, Chromecast, HomeKit services across VLANs

### Private VLAN (PVLAN) for IoT Isolation

📎 **Complete configuration:**
[Full PVLAN isolation setup with promiscuous ports](https://gist.github.com/williamzujkowski/48d68afcb132e2f3b924ce74ce7adfa8)

Set `private-vlan isolated` on IoT interface so devices can't reach each other

### Dynamic VLAN Assignment with RADIUS

📎 **Complete configuration:**
[Full FreeRADIUS dynamic VLAN config with device mappings](https://gist.github.com/williamzujkowski/841cea35e4eb424d28f927b596808674)

Map MAC addresses to VLAN IDs via RADIUS `Tunnel-Private-Group-Id` attribute

## DNS-Based Access Control

### Pi-hole for VLAN-Specific Filtering

📎 **Complete blocklists:**
[IoT telemetry blocklist and conditional forwarding](https://gist.github.com/williamzujkowski/c58aa2ce297f125633f090549146c536)

Block vendor telemetry domains per VLAN, conditional forwarding for local zones

### DNS Query Logging for Threat Detection

📎 **Complete script:**
[Full DNS query analyzer with alerting](https://gist.github.com/williamzujkowski/345730384bf7d77c8b82e7ee4299ce43)

Analyze Pi-hole logs for IoT VLAN unusual query patterns

## Monitoring and Alerting

### NetFlow Analysis

📎 **Complete configuration:**
[Full NetFlow setup with nfdump analysis queries](https://gist.github.com/williamzujkowski/05e39be6317d012d22991a51fe603bbb)

Export NetFlow to collector for cross-VLAN traffic analysis

### Traffic Analysis Alerts

📎 **Complete script:**
[Full VLAN traffic monitor with multiple alert channels](https://gist.github.com/williamzujkowski/b2224d5ef6333717d24d18575c597044)

Alert on cross-VLAN flows not in allowed whitelist

## Testing and Validation

### Connectivity Testing Matrix

📎 **Complete script:**
[Full VLAN segmentation test suite with all protocols](https://gist.github.com/williamzujkowski/2281086bfb8a52a7ab14fb72f47b9635)

Test all VLAN pairs with ping/curl to verify firewall rules work

### Automated Penetration Testing

📎 **Complete script:**
[VLAN breakout testing with nmap and metasploit](https://gist.github.com/williamzujkowski/12ecda690c2c3b878ca981f8a09dc50d)

Attempt VLAN breakout from IoT using nmap source-ip spoofing

## Troubleshooting Common Issues

<!-- 📎 **Complete troubleshooting guide:**
[All common VLAN issues and solutions](https://gist.github.com/williamzujkowski/vlan-troubleshooting) -->

**DHCP issues:** Check daemon logs, tcpdump VLAN traffic on port 67
**Routing issues:** Verify `ip_forward=1`, traceroute between VLANs
**mDNS issues:** Verify Avahi daemon running, browse services

## Performance Optimization

<!-- 📎 **Complete optimization guide:**
[Hardware offloading and VLAN tuning](https://gist.github.com/williamzujkowski/vlan-performance-tuning) -->

Enable hardware NAT offloading, increase MTU to 9000 for storage VLANs

## Lessons Learned

After years of running segmented VLANs:

### 1. Start Simple, Add Complexity Gradually
I made the mistake of creating 12 VLANs on day one. Half of them sat unused for months. Start with 3-4 logical segments, validate they work, then expand. Your mileage may vary depending on your network complexity.

### 2. Document Your Rules
Future you will thank present you. I maintain a wiki page with every firewall rule and its justification. When I review rules 6 months later, I'm usually glad I documented why that specific port was opened.

### 3. Default Deny is Your Friend
Block everything by default, then explicitly allow what's needed. It's harder to setup but probably more secure in the long run. I spent 3 hours debugging why HomeKit wasn't working until I realized default-deny was blocking mDNS.

### 4. Test Your Segmentation Regularly
I run automated tests weekly to ensure segmentation hasn't degraded over time.

### 5. Monitor, Don't Just Configure
Firewall rules without logging are security theater. Log everything and alert on anomalies.

## Security Benefits Realized

Since implementing VLAN segmentation:

- **Reduced attack surface**: Compromised IoT devices can't pivot to trusted networks
- **Easier forensics**: VLAN ID in logs immediately identifies affected segment
- **Improved performance**: Broadcast domains are smaller, reducing noise
- **Compliance**: Network segmentation requirement satisfied
- **Peace of mind**: Sketchy cameras can't access my NAS

## Research & References

### Zero Trust Networking

1. **[BeyondCorp: A New Approach to Enterprise Security](https://research.google/pubs/pub43231/)** (2014)
   - Google's zero trust implementation
   - ACM Queue

2. **[Zero Trust Networks](https://www.oreilly.com/library/view/zero-trust-networks/9781491962183/)** - O'Reilly book by Gilman and Barth

### VLAN Best Practices

1. **[VLAN Security Best Practices](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst6500/ios/12-2SX/configuration/guide/book/vlans.html)** - Cisco documentation

2. **[Private VLAN (PVLAN) Deployment Guide](https://tools.ietf.org/html/rfc5517)** - IETF RFC 5517

### Network Segmentation Standards

- **[PCI DSS Scoping and Segmentation Guidance](https://www.pcisecuritystandards.org/documents/Guidance-PCI-DSS-Scoping-and-Segmentation_v1.pdf)** - Payment Card Industry requirements
- **[NIST SP 800-41: Guidelines on Firewalls and Firewall Policy](https://csrc.nist.gov/publications/detail/sp/800-41/rev-1/final)**
- **[CIS Controls v8: Network Segmentation](https://www.cisecurity.org/controls/network-infrastructure-management)**

## Conclusion

VLAN segmentation transformed my homelab from a flat, vulnerable network into a defense-in-depth architecture. The cheap IoT camera that inspired this journey is now safely contained, unable to reach anything important.

Zero trust isn't about perfection. It's about making each compromised device a dead end rather than a jumping-off point. Start with logical segments, implement strict firewall rules, monitor everything, and iterate.

Your homelab will be more secure, more organized, and far more interesting to manage.

---

*How are you segmenting your homelab network? What firewall rules have saved you from disaster? Share your VLAN strategies and war stories!*
