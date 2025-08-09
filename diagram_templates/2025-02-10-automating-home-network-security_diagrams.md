# Diagrams for 2025-02-10-automating-home-network-security.md

## How to use these diagrams:

1. Copy the Mermaid diagram code blocks
2. Replace verbose code sections in your blog post
3. The diagrams will render automatically in markdown

---


## Home Network Security Architecture

```mermaid
graph LR
    subgraph "Internet"
        ISP[ISP Router]
    end
    
    subgraph "DMZ"
        FW[pfSense Firewall]
        IDS[Suricata IDS]
    end
    
    subgraph "Internal Network"
        SW[Managed Switch]
        AP[WiFi AP]
        
        subgraph "VLANs"
            V1[IoT VLAN]
            V2[Guest VLAN]
            V3[Trusted VLAN]
            V4[Security VLAN]
        end
    end
    
    subgraph "Security Stack"
        PH[Pi-hole DNS]
        VPN[WireGuard VPN]
        LOG[Graylog]
        MON[Prometheus]
    end
    
    ISP --> FW
    FW --> IDS
    IDS --> SW
    SW --> V1
    SW --> V2
    SW --> V3
    SW --> V4
    
    V3 --> PH
    V3 --> VPN
    V4 --> LOG
    V4 --> MON
    
    AP --> V2
    
    style FW fill:#ff5252
    style IDS fill:#ff9800
    style V4 fill:#4caf50
```

## Network Monitoring Flow

```mermaid
flowchart TD
    Start([Network Packet]) --> Cap[Packet Capture]
    Cap --> Parse[Parse Headers]
    Parse --> Check{Known Device?}
    
    Check -->|Yes| Analyze[Deep Analysis]
    Check -->|No| Alert[Security Alert]
    
    Analyze --> Threat{Threat Detected?}
    Threat -->|Yes| Block[Block Traffic]
    Threat -->|No| Log[Log Activity]
    
    Alert --> Investigate[Manual Review]
    Block --> Notify[Send Notification]
    
    Investigate --> Decision{Allow?}
    Decision -->|Yes| Whitelist[Add to Whitelist]
    Decision -->|No| Blacklist[Add to Blacklist]
    
    style Alert fill:#ff5252
    style Block fill:#ff5252
    style Log fill:#4caf50
```
