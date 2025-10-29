# Diagrams for 2025-09-08-zero-trust-vlan-segmentation-homelab.md

## How to use these diagrams:

1. Copy the Mermaid diagram code blocks
2. Replace verbose code sections in your blog post
3. The diagrams will render automatically in markdown
4. Extract large configuration blocks (55+ lines) to GitHub gists

---

## Zero Trust Network Segmentation

```mermaid
graph TB
    subgraph "VLAN 10: Management"
        MGT[Management<br/>Interface]
        Proxmox[Proxmox Hosts]
        Switch[Switch Management]
    end

    subgraph "VLAN 20: Production"
        Web[Web Services]
        API[API Services]
        DB[Databases]
    end

    subgraph "VLAN 30: Development"
        DevEnv[Dev Environment]
        TestServers[Test Servers]
        CI[CI/CD Pipeline]
    end

    subgraph "VLAN 40: IoT/Guest"
        IoT[IoT Devices]
        Guest[Guest Devices]
        NoTrust[Untrusted Zone]
    end

    subgraph "Security Layer"
        FW[OPNsense Firewall]
        IDS[Suricata IDS/IPS]
        Monitor[Wazuh Monitoring]
    end

    FW -->|Rules| MGT
    FW -->|Rules| Web
    FW -->|Rules| DevEnv
    FW -->|Rules| IoT

    IDS --> Monitor
    Monitor --> FW

    MGT -.->|Admin| Proxmox
    MGT -.->|Admin| Switch

    Web --> API
    API --> DB

    style MGT fill:#f44336
    style Web fill:#4caf50
    style DevEnv fill:#ffc107
    style IoT fill:#9e9e9e
    style FW fill:#2196f3
```

## Traffic Flow and Firewall Rules

```mermaid
flowchart TD
    Start([Packet Arrives]) --> CheckSrc{Source<br/>VLAN?}

    CheckSrc -->|VLAN 10<br/>Management| CheckMgmt{Destination?}
    CheckSrc -->|VLAN 20<br/>Production| CheckProd{Destination?}
    CheckSrc -->|VLAN 30<br/>Development| CheckDev{Destination?}
    CheckSrc -->|VLAN 40<br/>IoT/Guest| CheckIoT{Destination?}

    CheckMgmt -->|To Prod| BlockMgmtProd[DENY: No direct access]
    CheckMgmt -->|To Dev| AllowMgmtDev[ALLOW: Admin access]
    CheckMgmt -->|To IoT| BlockMgmtIoT[DENY: No IoT access]

    CheckProd -->|To Mgmt| BlockProdMgmt[DENY: No mgmt access]
    CheckProd -->|Within Prod| AllowProdProd[ALLOW: Inter-service]
    CheckProd -->|To Internet| AllowProdNet[ALLOW: Controlled egress]

    CheckDev -->|To Prod| BlockDevProd[DENY: No prod access]
    CheckDev -->|To Internet| AllowDevNet[ALLOW: Package repos]
    CheckDev -->|Within Dev| AllowDevDev[ALLOW: Internal]

    CheckIoT -->|To Mgmt| BlockIoTMgmt[DENY: No mgmt access]
    CheckIoT -->|To Prod| BlockIoTProd[DENY: No prod access]
    CheckIoT -->|To Dev| BlockIoTDev[DENY: No dev access]
    CheckIoT -->|To Internet| AllowIoTNet[ALLOW: Internet only]

    AllowMgmtDev --> Log[Log & Forward]
    AllowProdProd --> Log
    AllowProdNet --> Log
    AllowDevNet --> Log
    AllowDevDev --> Log
    AllowIoTNet --> Log

    BlockMgmtProd --> Drop[Drop & Alert]
    BlockMgmtIoT --> Drop
    BlockProdMgmt --> Drop
    BlockDevProd --> Drop
    BlockIoTMgmt --> Drop
    BlockIoTProd --> Drop
    BlockIoTDev --> Drop

    Log --> End([Forward Packet])
    Drop --> End

    style AllowMgmtDev fill:#4caf50
    style AllowProdProd fill:#4caf50
    style AllowProdNet fill:#4caf50
    style BlockMgmtProd fill:#f44336
    style BlockProdMgmt fill:#f44336
    style BlockIoTMgmt fill:#f44336
```

## VLAN Tagging and Trunking

```mermaid
graph LR
    subgraph "Physical Infrastructure"
        Router[OPNsense Router]
        CoreSwitch[Core Switch]
        EdgeSwitch1[Edge Switch 1]
        EdgeSwitch2[Edge Switch 2]
    end

    subgraph "Tagged Ports (Trunk)"
        Trunk1[VLAN 10,20,30,40]
        Trunk2[VLAN 10,20,30,40]
    end

    subgraph "Untagged Ports (Access)"
        Access10[VLAN 10 Only]
        Access20[VLAN 20 Only]
        Access30[VLAN 30 Only]
        Access40[VLAN 40 Only]
    end

    subgraph "Connected Devices"
        ProxNode[Proxmox Node]
        WebServer[Web Server]
        DevMachine[Dev Machine]
        IoTHub[IoT Hub]
    end

    Router -->|Trunk| CoreSwitch
    CoreSwitch -->|Trunk| EdgeSwitch1
    CoreSwitch -->|Trunk| EdgeSwitch2

    EdgeSwitch1 -->|Access| Access10
    EdgeSwitch1 -->|Access| Access20
    EdgeSwitch2 -->|Access| Access30
    EdgeSwitch2 -->|Access| Access40

    Access10 --> ProxNode
    Access20 --> WebServer
    Access30 --> DevMachine
    Access40 --> IoTHub

    style Trunk1 fill:#2196f3
    style Trunk2 fill:#2196f3
    style Access10 fill:#f44336
    style Access20 fill:#4caf50
    style Access30 fill:#ffc107
    style Access40 fill:#9e9e9e
```

## Zero Trust Policy Enforcement

```mermaid
graph TB
    subgraph "Authentication Layer"
        User[User/Service]
        MFA[MFA Verification]
        Cert[Certificate Check]
    end

    subgraph "Authorization Layer"
        RBAC[RBAC Rules]
        Policies[Policy Engine]
        Context[Context Analysis]
    end

    subgraph "Verification Layer"
        DeviceCheck[Device Posture]
        NetworkCheck[Network Context]
        TimeCheck[Time-based Rules]
    end

    subgraph "Decision Engine"
        Evaluate[Evaluate All Factors]
        Decision{Allow?}
    end

    subgraph "Enforcement"
        Allow[Grant Access]
        Deny[Deny Access]
        MFA2[Step-up MFA]
        Monitor[Continuous Monitor]
    end

    User --> MFA
    MFA --> Cert
    Cert --> RBAC

    RBAC --> Policies
    Policies --> Context

    Context --> DeviceCheck
    DeviceCheck --> NetworkCheck
    NetworkCheck --> TimeCheck

    TimeCheck --> Evaluate
    Evaluate --> Decision

    Decision -->|Yes| Allow
    Decision -->|No| Deny
    Decision -->|Maybe| MFA2

    Allow --> Monitor
    MFA2 --> Monitor
    Monitor --> Evaluate

    style User fill:#2196f3
    style MFA fill:#ff9800
    style Decision fill:#9c27b0
    style Allow fill:#4caf50
    style Deny fill:#f44336
```

## Micro-segmentation Strategy

```mermaid
graph TD
    subgraph "Traditional Network"
        FlatNet[Flat Network<br/>10.0.0.0/24]
        NoSegment[No Segmentation]
        FullAccess[All-to-All Access]
    end

    subgraph "VLAN Segmentation"
        VLAN1[VLAN 10<br/>10.10.0.0/24]
        VLAN2[VLAN 20<br/>10.20.0.0/24]
        VLAN3[VLAN 30<br/>10.30.0.0/24]
        BasicFW[Basic Firewall Rules]
    end

    subgraph "Micro-segmentation"
        Service1[Web Service<br/>10.20.1.0/28]
        Service2[API Service<br/>10.20.2.0/28]
        Service3[Database<br/>10.20.3.0/28]
        GranularFW[Granular Firewall<br/>Per-Service Rules]
    end

    FlatNet --> NoSegment
    NoSegment --> FullAccess

    VLAN1 --> BasicFW
    VLAN2 --> BasicFW
    VLAN3 --> BasicFW

    Service1 --> GranularFW
    Service2 --> GranularFW
    Service3 --> GranularFW

    style FlatNet fill:#f44336
    style VLAN1 fill:#ffc107
    style Service1 fill:#4caf50
```

## Usage Example

Replace this verbose configuration:
```bash
# 55 lines of VLAN and firewall config
```

With:
```bash
# Essential config only
opnsense-cli vlan create \
  --id 20 --name "Production" \
  --interface em0 --rules zero-trust

# Full configuration: https://gist.github.com/...
```

And add network topology diagram above the code.

## Monitoring and Alerting

```mermaid
sequenceDiagram
    participant Device
    participant Switch
    participant Firewall
    participant IDS
    participant SIEM

    Device->>Switch: Send packet
    Switch->>Switch: Check VLAN tag
    Switch->>Firewall: Forward with VLAN ID

    activate Firewall
    Firewall->>Firewall: Apply rules

    alt Rule allows
        Firewall->>IDS: Mirror traffic
        Firewall-->>Switch: Forward packet
    else Rule denies
        Firewall->>SIEM: Send deny alert
        Firewall-->>Device: Drop packet
    end
    deactivate Firewall

    activate IDS
    IDS->>IDS: Deep inspection

    alt Threat detected
        IDS->>SIEM: Send alert
        IDS->>Firewall: Update rules
    else Clean traffic
        IDS->>IDS: Log flow
    end
    deactivate IDS

    SIEM->>SIEM: Correlate events
    SIEM->>SIEM: Update dashboard
```
