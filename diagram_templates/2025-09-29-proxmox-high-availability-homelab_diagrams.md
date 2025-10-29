# Diagrams for 2025-09-29-proxmox-high-availability-homelab.md

## How to use these diagrams:

1. Copy the Mermaid diagram code blocks
2. Replace verbose code sections in your blog post
3. The diagrams will render automatically in markdown
4. Extract large configuration blocks (56+ lines) to GitHub gists

---

## Proxmox HA Cluster Architecture

```mermaid
graph TB
    subgraph "Cluster Nodes"
        Node1[Proxmox Node 1<br/>10.10.10.1]
        Node2[Proxmox Node 2<br/>10.10.10.2]
        Node3[Proxmox Node 3<br/>10.10.10.3]
    end

    subgraph "Corosync Cluster"
        Corosync[Corosync<br/>Cluster Communication]
        Quorum[Quorum Device<br/>QDevice]
    end

    subgraph "Shared Storage"
        Ceph[Ceph Cluster]
        CephMon1[Ceph Monitor 1]
        CephMon2[Ceph Monitor 2]
        CephMon3[Ceph Monitor 3]
        CephOSD[(OSD Pool)]
    end

    subgraph "HA Services"
        HAManager[HA Manager]
        CRM[Cluster Resource<br/>Manager]
        Fencing[Fencing Agent]
    end

    subgraph "Virtual Machines"
        VM1[VM: Web Service]
        VM2[VM: Database]
        VM3[VM: Application]
    end

    Node1 --> Corosync
    Node2 --> Corosync
    Node3 --> Corosync

    Corosync --> Quorum
    Quorum --> HAManager

    Node1 --> CephMon1
    Node2 --> CephMon2
    Node3 --> CephMon3

    CephMon1 --> CephOSD
    CephMon2 --> CephOSD
    CephMon3 --> CephOSD

    HAManager --> CRM
    CRM --> Fencing

    CRM -.->|Manages| VM1
    CRM -.->|Manages| VM2
    CRM -.->|Manages| VM3

    style Node1 fill:#4caf50
    style Node2 fill:#4caf50
    style Node3 fill:#4caf50
    style HAManager fill:#2196f3
    style CephOSD fill:#ff9800
```

## Quorum and Voting

```mermaid
graph LR
    subgraph "3-Node Cluster"
        N1[Node 1<br/>Vote: 1]
        N2[Node 2<br/>Vote: 1]
        N3[Node 3<br/>Vote: 1]
        QD[QDevice<br/>Vote: 1]
    end

    subgraph "Quorum Calculation"
        Total[Total Votes: 4]
        Required[Required: 3]
        Decision{Has Quorum?}
    end

    subgraph "Scenarios"
        S1[All nodes up:<br/>4 votes ✓]
        S2[1 node down:<br/>3 votes ✓]
        S3[2 nodes down:<br/>2 votes ✗]
        S4[QDevice + 2 nodes:<br/>3 votes ✓]
    end

    N1 --> Total
    N2 --> Total
    N3 --> Total
    QD --> Total

    Total --> Decision
    Required --> Decision

    Decision --> S1
    Decision --> S2
    Decision --> S3
    Decision --> S4

    style S1 fill:#4caf50
    style S2 fill:#4caf50
    style S3 fill:#f44336
    style S4 fill:#4caf50
```

## VM Migration Workflow

```mermaid
flowchart TD
    Start([Node Failure Detected]) --> CheckQuorum{Has<br/>Quorum?}

    CheckQuorum -->|No| EmergencyMode[Emergency Mode<br/>No Migration]
    CheckQuorum -->|Yes| IdentifyVMs[Identify Running VMs<br/>on Failed Node]

    IdentifyVMs --> CheckHA{HA Enabled<br/>on VM?}

    CheckHA -->|No| SkipVM[Skip VM]
    CheckHA -->|Yes| CheckResources{Target Node<br/>Has Resources?}

    CheckResources -->|No| QueueMigration[Queue for Later]
    CheckResources -->|Yes| CheckStorage{Storage<br/>Accessible?}

    CheckStorage -->|No| StorageError[Alert Storage Issue]
    CheckStorage -->|Yes| FenceOldNode[Fence Old Node]

    FenceOldNode --> CopyMemory[Copy Memory State<br/>from Shared Storage]
    CopyMemory --> StartVM[Start VM on<br/>Target Node]

    StartVM --> VerifyBoot{VM Booted<br/>Successfully?}

    VerifyBoot -->|Yes| UpdateCluster[Update Cluster State]
    VerifyBoot -->|No| Retry{Retry<br/>Count < 3?}

    Retry -->|Yes| StartVM
    Retry -->|No| FailAlert[Send Failure Alert]

    UpdateCluster --> NotifyUsers[Notify Users]
    NotifyUsers --> End([Migration Complete])

    SkipVM --> End
    QueueMigration --> End
    StorageError --> End
    FailAlert --> End
    EmergencyMode --> End

    style FenceOldNode fill:#f44336
    style StartVM fill:#4caf50
    style UpdateCluster fill:#2196f3
```

## Fencing Process

```mermaid
sequenceDiagram
    participant HAManager
    participant Node1
    participant Node2
    participant Node3
    participant IPMI
    participant Watchdog

    Note over Node2: Node failure detected

    HAManager->>HAManager: Detect Node2 unresponsive
    HAManager->>Quorum: Check cluster quorum

    alt Has quorum
        HAManager->>Node1: Attempt soft fence
        HAManager->>Node3: Attempt soft fence

        alt Soft fence fails
            HAManager->>IPMI: Issue hard fence (power off)
            activate IPMI
            IPMI->>Node2: Force power off
            IPMI-->>HAManager: Fencing successful
            deactivate IPMI
        end

        HAManager->>Watchdog: Verify node is fenced
        Watchdog-->>HAManager: Confirmed fenced

        HAManager->>Node1: Identify VMs to migrate
        HAManager->>Node3: Check resource availability

        alt Resources available
            HAManager->>Node3: Start VM migration
            activate Node3
            Node3->>Node3: Start VM from shared storage
            Node3-->>HAManager: VM started
            deactivate Node3
        else Insufficient resources
            HAManager->>HAManager: Queue for later
        end

    else No quorum
        HAManager->>HAManager: Enter emergency mode
        HAManager->>HAManager: No fencing/migration
    end

    HAManager->>HAManager: Update cluster state
    HAManager->>Dashboard: Send notifications
```

## Storage Replication

```mermaid
graph TB
    subgraph "Primary Node"
        VM[Virtual Machine]
        VMDisk[VM Disk<br/>RBD Volume]
    end

    subgraph "Ceph Cluster"
        Pool[Ceph Pool<br/>Replication: 3]
        OSD1[(OSD 1)]
        OSD2[(OSD 2)]
        OSD3[(OSD 3)]
    end

    subgraph "Replication Process"
        Primary[Primary OSD]
        Replica1[Replica OSD 1]
        Replica2[Replica OSD 2]
        Monitor[Ceph Monitor]
    end

    subgraph "Read/Write Path"
        Write[Write Operation]
        Read[Read Operation]
        ACK[ACK to Client]
    end

    VM --> VMDisk
    VMDisk --> Write
    Write --> Primary

    Primary --> Replica1
    Primary --> Replica2

    Replica1 --> ACK
    Replica2 --> ACK
    ACK --> VMDisk

    Read --> Primary
    Primary --> VMDisk

    Monitor --> Primary
    Monitor --> Replica1
    Monitor --> Replica2

    Primary --> OSD1
    Replica1 --> OSD2
    Replica2 --> OSD3

    style Write fill:#ff9800
    style Read fill:#4caf50
    style ACK fill:#2196f3
    style Monitor fill:#9c27b0
```

## HA State Machine

```mermaid
stateDiagram-v2
    [*] --> Stopped

    Stopped --> Starting: HA Manager starts VM
    Starting --> Started: Boot successful

    Started --> Running: Health checks pass
    Running --> Started: Minor issues

    Started --> Stopping: Graceful shutdown
    Running --> Stopping: Admin stop

    Stopping --> Stopped: Shutdown complete

    Running --> Freeze: Node failure detected
    Freeze --> Migrating: Fencing successful

    Migrating --> Starting: Target node ready
    Migrating --> Error: Migration failed

    Error --> Freeze: Retry migration
    Error --> Stopped: Max retries reached

    Running --> Error: Critical failure
    Started --> Error: Boot timeout

    style Running fill:#4caf50
    style Error fill:#f44336
    style Migrating fill:#ff9800
    style Freeze fill:#2196f3
```

## Network Configuration

```mermaid
graph TB
    subgraph "Physical Network"
        Bond0[Bond0: LACP<br/>eth0 + eth1]
        Bond1[Bond1: Active-Backup<br/>eth2 + eth3]
    end

    subgraph "Virtual Bridges"
        VMBR0[vmbr0<br/>Cluster Network]
        VMBR1[vmbr1<br/>VM Network]
        VMBR2[vmbr2<br/>Storage Network]
    end

    subgraph "VLANs"
        VLAN10[VLAN 10<br/>Management]
        VLAN20[VLAN 20<br/>VMs]
        VLAN30[VLAN 30<br/>Ceph]
        VLAN40[VLAN 40<br/>Migration]
    end

    subgraph "IP Addressing"
        IP1[10.10.0.0/24<br/>Cluster]
        IP2[10.20.0.0/24<br/>VMs]
        IP3[10.30.0.0/24<br/>Storage]
        IP4[10.40.0.0/24<br/>Migration]
    end

    Bond0 --> VMBR0
    Bond1 --> VMBR1
    Bond1 --> VMBR2

    VMBR0 --> VLAN10
    VMBR1 --> VLAN20
    VMBR2 --> VLAN30
    VMBR2 --> VLAN40

    VLAN10 --> IP1
    VLAN20 --> IP2
    VLAN30 --> IP3
    VLAN40 --> IP4

    style Bond0 fill:#4caf50
    style Bond1 fill:#4caf50
    style VLAN30 fill:#ff9800
```

## Usage Example

Replace this verbose configuration:
```bash
# 56 lines of cluster configuration
```

With:
```bash
# Essential config only
pvecm create homelab-cluster \
  --bindnet0 10.10.0.0/24 \
  --ring0_addr 10.10.0.1

# Full configuration: https://gist.github.com/...
```

And add cluster architecture diagram above the code.

## Backup Strategy

```mermaid
graph TD
    subgraph "Backup Sources"
        VM1[VM 1]
        VM2[VM 2]
        VM3[VM 3]
        Container1[Container 1]
    end

    subgraph "Backup Methods"
        Snapshot[Snapshot Mode]
        Suspend[Suspend Mode]
        Stop[Stop Mode]
    end

    subgraph "Storage Targets"
        Local[(Local Storage)]
        NFS[(NFS Share)]
        PBS[Proxmox Backup<br/>Server]
    end

    subgraph "Retention"
        Daily[Daily: 7 days]
        Weekly[Weekly: 4 weeks]
        Monthly[Monthly: 6 months]
    end

    VM1 --> Snapshot
    VM2 --> Suspend
    VM3 --> Stop
    Container1 --> Snapshot

    Snapshot --> PBS
    Suspend --> NFS
    Stop --> Local

    PBS --> Daily
    NFS --> Weekly
    Local --> Monthly

    style PBS fill:#4caf50
    style Snapshot fill:#2196f3
```
