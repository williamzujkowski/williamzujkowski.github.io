# Diagrams for 2025-07-01-ebpf-security-monitoring-practical-guide.md

## How to use these diagrams:

1. Copy the Mermaid diagram code blocks
2. Replace verbose code sections in your blog post
3. The diagrams will render automatically in markdown

---


## eBPF Security Architecture

```mermaid
graph TB
    subgraph "Kernel Space"
        KProbe[Kernel Probes]
        TProbe[Tracepoints]
        UProbe[User Probes]
        BPF[eBPF Program]
        Maps[(BPF Maps)]
    end
    
    subgraph "User Space"
        Loader[BPF Loader]
        Controller[Control Plane]
        Analyzer[Event Analyzer]
        Storage[(Event Store)]
    end
    
    subgraph "Monitoring Targets"
        Syscalls[System Calls]
        Network[Network Stack]
        Files[File Operations]
        Process[Process Events]
    end
    
    Syscalls --> KProbe
    Network --> TProbe
    Files --> KProbe
    Process --> UProbe
    
    KProbe --> BPF
    TProbe --> BPF
    UProbe --> BPF
    
    BPF --> Maps
    Maps --> Controller
    
    Loader --> BPF
    Controller --> Analyzer
    Analyzer --> Storage
    
    style BPF fill:#ff9800
    style Maps fill:#ffd54f
    style Analyzer fill:#4caf50
```

## eBPF Event Processing Flow

```mermaid
sequenceDiagram
    participant K as Kernel
    participant B as eBPF Program
    participant M as BPF Maps
    participant U as User Space
    participant A as Analyzer
    participant D as Dashboard
    
    K->>B: System Event
    B->>B: Filter & Process
    B->>M: Store Event Data
    U->>M: Poll Maps
    M-->>U: Event Data
    U->>A: Send for Analysis
    A->>A: Correlate Events
    A->>D: Update Dashboard
    A-->>U: Trigger Alert (if needed)
```
