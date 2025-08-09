# Diagrams for 2025-03-10-raspberry-pi-security-projects.md

## How to use these diagrams:

1. Copy the Mermaid diagram code blocks
2. Replace verbose code sections in your blog post
3. The diagrams will render automatically in markdown

---


## Raspberry Pi Security Hub

```mermaid
graph TB
    subgraph "Hardware"
        Pi4[Raspberry Pi 4]
        Sense[Sense HAT]
        Cam[Pi Camera]
        USB[USB Devices]
    end
    
    subgraph "Security Services"
        VPN[WireGuard VPN]
        IDS[Snort IDS]
        DNS[Pi-hole DNS]
        Mon[Motion Detection]
    end
    
    subgraph "Monitoring"
        Prom[Prometheus]
        Graf[Grafana]
        Log[Rsyslog]
    end
    
    subgraph "Storage"
        SD[SD Card]
        NAS[Network Storage]
        Cloud[Cloud Backup]
    end
    
    Pi4 --> VPN
    Pi4 --> IDS
    Pi4 --> DNS
    Cam --> Mon
    Sense --> Prom
    
    VPN --> Log
    IDS --> Log
    DNS --> Log
    Mon --> Log
    
    Log --> SD
    Log --> NAS
    Prom --> Graf
    
    NAS --> Cloud
    
    style Pi4 fill:#c8e6c9
    style VPN fill:#ff9800
    style Graf fill:#2196f3
```

## Motion Detection Flow

```mermaid
flowchart LR
    Start([Motion Sensor]) --> Detect[Detect Movement]
    Detect --> Capture[Capture Image]
    Capture --> Analyze[Analyze Image]
    
    Analyze --> Face{Face Detected?}
    Face -->|Yes| Known{Known Person?}
    Face -->|No| Object[Object Detection]
    
    Known -->|Yes| Log[Log Entry]
    Known -->|No| Alert[Send Alert]
    
    Object --> Threat{Threat?}
    Threat -->|Yes| Alert
    Threat -->|No| Log
    
    Alert --> Notify[Push Notification]
    Alert --> Record[Start Recording]
    
    style Alert fill:#ff5252
    style Log fill:#4caf50
```
