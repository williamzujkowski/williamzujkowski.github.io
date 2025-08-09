#!/usr/bin/env python3
"""
Blog Diagram Generator
Creates Mermaid diagrams to replace verbose code blocks in blog posts
"""

from pathlib import Path
from typing import Dict, List
import yaml
import re

class BlogDiagramGenerator:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.posts_dir = self.base_path / "src" / "posts"
        self.diagrams_generated = []
    
    def parse_frontmatter(self, content: str) -> tuple[dict, str]:
        """Parse frontmatter and content from markdown file"""
        if content.startswith('---'):
            try:
                _, fm, content = content.split('---', 2)
                frontmatter = yaml.safe_load(fm)
                return frontmatter, content.lstrip()
            except:
                return {}, content
        return {}, content
    
    def create_vulnerability_management_diagrams(self) -> str:
        """Create diagrams for vulnerability management post"""
        return """
## System Architecture

```mermaid
graph TB
    subgraph "Data Sources"
        NVD[NVD API]
        MITRE[MITRE CVE]
        GH[GitHub Security]
        OSV[OSV Database]
    end
    
    subgraph "Processing Pipeline"
        Collector[Data Collector]
        Parser[CVE Parser]
        Enricher[Data Enricher]
        Scorer[Risk Scorer]
    end
    
    subgraph "Storage"
        DB[(PostgreSQL)]
        Cache[(Redis Cache)]
        S3[S3 Buckets]
    end
    
    subgraph "Analysis"
        ML[ML Models]
        Rules[Rule Engine]
        Correlator[Correlation Engine]
    end
    
    subgraph "Output"
        API[REST API]
        Dashboard[Web Dashboard]
        Alerts[Alert System]
        Reports[Report Generator]
    end
    
    NVD --> Collector
    MITRE --> Collector
    GH --> Collector
    OSV --> Collector
    
    Collector --> Parser
    Parser --> Enricher
    Enricher --> Scorer
    
    Scorer --> DB
    Scorer --> Cache
    Parser --> S3
    
    DB --> ML
    DB --> Rules
    DB --> Correlator
    
    ML --> API
    Rules --> API
    Correlator --> API
    
    API --> Dashboard
    API --> Alerts
    API --> Reports
    
    style NVD fill:#e1f5fe
    style MITRE fill:#e1f5fe
    style GH fill:#e1f5fe
    style OSV fill:#e1f5fe
    style DB fill:#fff3e0
    style ML fill:#f3e5f5
    style Dashboard fill:#e8f5e9
```

## Vulnerability Processing Workflow

```mermaid
flowchart LR
    Start([New CVE]) --> Fetch[Fetch Details]
    Fetch --> Parse[Parse CVE Data]
    Parse --> Check{Asset Affected?}
    
    Check -->|No| Archive[Archive]
    Check -->|Yes| Enrich[Enrich Data]
    
    Enrich --> Score[Calculate CVSS]
    Score --> Priority{Priority Level?}
    
    Priority -->|Critical| Alert[Immediate Alert]
    Priority -->|High| Ticket[Create Ticket]
    Priority -->|Medium| Queue[Add to Queue]
    Priority -->|Low| Log[Log Entry]
    
    Alert --> Remediate[Start Remediation]
    Ticket --> Remediate
    Queue --> Review[Weekly Review]
    
    Remediate --> Verify[Verify Fix]
    Verify --> Close[Close Issue]
    
    style Start fill:#ffebee
    style Alert fill:#ff5252
    style Remediate fill:#4caf50
```
"""
    
    def create_ebpf_diagrams(self) -> str:
        """Create diagrams for eBPF security monitoring"""
        return """
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
"""
    
    def create_home_network_diagrams(self) -> str:
        """Create diagrams for home network security"""
        return """
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
"""
    
    def create_claude_flow_diagrams(self) -> str:
        """Create diagrams for Claude-Flow post"""
        return """
## Claude-Flow Swarm Architecture

```mermaid
graph TB
    subgraph "Swarm Topologies"
        Mesh[Mesh Topology]
        Hier[Hierarchical]
        Ring[Ring Network]
        Star[Star Pattern]
    end
    
    subgraph "Agent Types"
        Research[Researcher]
        Arch[Architect]
        Coder[Coder]
        Tester[Tester]
        Review[Reviewer]
    end
    
    subgraph "Coordination"
        Orch[Orchestrator]
        Memory[(Memory Store)]
        Queue[Task Queue]
    end
    
    subgraph "Execution"
        Parallel[Parallel Tasks]
        Sequential[Sequential Tasks]
        Adaptive[Adaptive Strategy]
    end
    
    Mesh --> Orch
    Hier --> Orch
    Ring --> Orch
    Star --> Orch
    
    Orch --> Research
    Orch --> Arch
    Orch --> Coder
    Orch --> Tester
    Orch --> Review
    
    Research --> Memory
    Arch --> Memory
    Coder --> Queue
    Tester --> Queue
    Review --> Queue
    
    Queue --> Parallel
    Queue --> Sequential
    Queue --> Adaptive
    
    style Orch fill:#9c27b0
    style Memory fill:#ffd54f
    style Parallel fill:#4caf50
```

## SPARC Development Flow

```mermaid
flowchart LR
    S[Specification] --> P[Pseudocode]
    P --> A[Architecture]
    A --> R[Refinement]
    R --> C[Completion]
    
    S -.-> M1{{Requirements Analysis}}
    P -.-> M2{{Algorithm Design}}
    A -.-> M3{{System Design}}
    R -.-> M4{{TDD Implementation}}
    C -.-> M5{{Integration}}
    
    style S fill:#e3f2fd
    style P fill:#f3e5f5
    style A fill:#fff3e0
    style R fill:#e8f5e9
    style C fill:#ffebee
```

## Agent Collaboration Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant O as Orchestrator
    participant R as Researcher
    participant A as Architect
    participant C as Coder
    participant T as Tester
    
    U->>O: Task Request
    O->>R: Research Requirements
    R-->>O: Analysis Complete
    O->>A: Design Architecture
    A-->>O: Architecture Ready
    O->>C: Implement Code
    O->>T: Prepare Tests
    C-->>O: Code Complete
    T-->>O: Tests Ready
    O->>T: Run Tests
    T-->>O: All Tests Pass
    O-->>U: Task Complete
```
"""
    
    def create_zero_trust_diagrams(self) -> str:
        """Create diagrams for Zero Trust post"""
        return """
## Zero Trust Architecture

```mermaid
graph TB
    subgraph "Users & Devices"
        User[Users]
        Device[Devices]
        Service[Services]
    end
    
    subgraph "Policy Engine"
        PDP[Policy Decision Point]
        PEP[Policy Enforcement Point]
        PA[Policy Administrator]
    end
    
    subgraph "Trust Engine"
        ID[Identity Verification]
        Dev[Device Trust]
        Risk[Risk Assessment]
        Behavior[Behavior Analysis]
    end
    
    subgraph "Resources"
        App[Applications]
        Data[(Data Stores)]
        API[APIs]
        Cloud[Cloud Services]
    end
    
    User --> PEP
    Device --> PEP
    Service --> PEP
    
    PEP --> PDP
    PDP --> PA
    
    PA --> ID
    PA --> Dev
    PA --> Risk
    PA --> Behavior
    
    ID --> PDP
    Dev --> PDP
    Risk --> PDP
    Behavior --> PDP
    
    PDP -->|Allow/Deny| PEP
    PEP -->|Conditional| App
    PEP -->|Conditional| Data
    PEP -->|Conditional| API
    PEP -->|Conditional| Cloud
    
    style PDP fill:#ff5252
    style PEP fill:#ff9800
    style Risk fill:#ffd54f
```

## Zero Trust Verification Flow

```mermaid
flowchart TD
    Request([Access Request]) --> Verify[Verify Identity]
    Verify --> Device[Check Device]
    Device --> Context[Evaluate Context]
    Context --> Risk[Risk Score]
    
    Risk --> Score{Risk Level?}
    Score -->|High| Deny[Deny Access]
    Score -->|Medium| MFA[Require MFA]
    Score -->|Low| Check[Policy Check]
    
    MFA --> Valid{MFA Valid?}
    Valid -->|No| Deny
    Valid -->|Yes| Check
    
    Check --> Policies{Policies Pass?}
    Policies -->|No| Deny
    Policies -->|Yes| Grant[Grant Access]
    
    Grant --> Monitor[Continuous Monitoring]
    Monitor --> Anomaly{Anomaly?}
    Anomaly -->|Yes| Revoke[Revoke Access]
    Anomaly -->|No| Monitor
    
    style Deny fill:#ff5252
    style Grant fill:#4caf50
    style Monitor fill:#2196f3
```
"""
    
    def create_dns_over_https_diagrams(self) -> str:
        """Create diagrams for DNS-over-HTTPS post"""
        return """
## DNS-over-HTTPS Architecture

```mermaid
graph LR
    subgraph "Clients"
        PC[Computer]
        Phone[Smartphone]
        IoT[IoT Devices]
    end
    
    subgraph "Local DNS"
        PiHole[Pi-hole]
        Cache[(DNS Cache)]
        Block[Blocklists]
    end
    
    subgraph "DoH Proxy"
        Proxy[cloudflared]
        TLS[TLS Encryption]
    end
    
    subgraph "Upstream"
        CF[Cloudflare]
        Quad9[Quad9]
        Google[Google DNS]
    end
    
    PC --> PiHole
    Phone --> PiHole
    IoT --> PiHole
    
    PiHole --> Cache
    PiHole --> Block
    PiHole --> Proxy
    
    Proxy --> TLS
    TLS --> CF
    TLS --> Quad9
    TLS --> Google
    
    style PiHole fill:#4caf50
    style TLS fill:#ff9800
    style CF fill:#2196f3
```

## DNS Query Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant P as Pi-hole
    participant Ca as Cache
    participant D as DoH Proxy
    participant U as Upstream DoH
    
    C->>P: DNS Query (Port 53)
    P->>P: Check Blocklist
    alt Blocked Domain
        P-->>C: NXDOMAIN
    else Allowed Domain
        P->>Ca: Check Cache
        alt Cache Hit
            Ca-->>P: Cached Response
            P-->>C: DNS Response
        else Cache Miss
            P->>D: Forward Query
            D->>D: Encrypt (TLS)
            D->>U: HTTPS Request
            U-->>D: HTTPS Response
            D->>D: Decrypt
            D-->>P: DNS Response
            P->>Ca: Update Cache
            P-->>C: DNS Response
        end
    end
```
"""
    
    def create_raspberry_pi_diagrams(self) -> str:
        """Create diagrams for Raspberry Pi security projects"""
        return """
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
"""
    
    def create_local_llm_diagrams(self) -> str:
        """Create diagrams for Local LLM deployment"""
        return """
## Local LLM Architecture

```mermaid
graph TB
    subgraph "Hardware Layer"
        GPU[GPU/TPU]
        CPU[CPU]
        RAM[Memory]
        Storage[(Model Storage)]
    end
    
    subgraph "Model Layer"
        Llama[Llama 2]
        Mistral[Mistral]
        Custom[Fine-tuned]
    end
    
    subgraph "Inference Engine"
        GGML[GGML]
        ONNX[ONNX Runtime]
        TRT[TensorRT]
    end
    
    subgraph "API Layer"
        REST[REST API]
        WS[WebSocket]
        GRPC[gRPC]
    end
    
    subgraph "Applications"
        Web[Web UI]
        CLI[CLI Tool]
        Apps[Applications]
    end
    
    GPU --> GGML
    GPU --> TRT
    CPU --> ONNX
    
    Storage --> Llama
    Storage --> Mistral
    Storage --> Custom
    
    Llama --> GGML
    Mistral --> ONNX
    Custom --> TRT
    
    GGML --> REST
    ONNX --> WS
    TRT --> GRPC
    
    REST --> Web
    WS --> CLI
    GRPC --> Apps
    
    style GPU fill:#ff9800
    style GGML fill:#4caf50
    style REST fill:#2196f3
```

## LLM Request Processing

```mermaid
sequenceDiagram
    participant U as User
    participant A as API
    participant Q as Queue
    participant L as LLM Engine
    participant C as Cache
    participant M as Model
    
    U->>A: Send Prompt
    A->>C: Check Cache
    alt Cache Hit
        C-->>A: Cached Response
        A-->>U: Return Response
    else Cache Miss
        A->>Q: Queue Request
        Q->>L: Process Request
        L->>M: Load Model
        M-->>L: Model Ready
        L->>M: Generate Response
        M-->>L: Token Stream
        L->>C: Store in Cache
        L-->>A: Stream Response
        A-->>U: Stream to User
    end
```
"""
    
    def process_high_priority_posts(self):
        """Process posts with high code ratios and add diagrams"""
        updates = []
        
        # Map of post patterns to diagram generators
        diagram_mappings = {
            'vulnerability-management': self.create_vulnerability_management_diagrams,
            'ebpf': self.create_ebpf_diagrams,
            'home-network': self.create_home_network_diagrams,
            'claude-flow': self.create_claude_flow_diagrams,
            'zero-trust': self.create_zero_trust_diagrams,
            'dns-over-https': self.create_dns_over_https_diagrams,
            'raspberry-pi': self.create_raspberry_pi_diagrams,
            'local-llm': self.create_local_llm_diagrams,
        }
        
        # High priority posts that need diagrams
        high_priority_files = [
            '2025-07-15-vulnerability-management-scale-open-source.md',
            '2025-07-01-ebpf-security-monitoring-practical-guide.md',
            '2025-02-10-automating-home-network-security.md',
            '2025-08-07-supercharging-development-claude-flow.md',
            '2024-08-27-zero-trust-security-principles.md',
            '2025-07-08-implementing-dns-over-https-home-networks.md',
            '2025-03-10-raspberry-pi-security-projects.md',
            '2025-06-25-local-llm-deployment-privacy-first.md',
        ]
        
        for post_file in high_priority_files:
            post_path = self.posts_dir / post_file
            if not post_path.exists():
                continue
            
            # Determine which diagrams to create
            file_lower = post_file.lower()
            diagram_func = None
            
            for pattern, func in diagram_mappings.items():
                if pattern in file_lower:
                    diagram_func = func
                    break
            
            if diagram_func:
                diagrams = diagram_func()
                updates.append({
                    'file': post_file,
                    'diagrams': diagrams
                })
                print(f"✅ Generated diagrams for: {post_file}")
        
        return updates
    
    def save_diagram_templates(self, updates):
        """Save diagram templates for manual integration"""
        output_dir = self.base_path / "diagram_templates"
        output_dir.mkdir(exist_ok=True)
        
        for update in updates:
            output_file = output_dir / f"{Path(update['file']).stem}_diagrams.md"
            
            content = f"# Diagrams for {update['file']}\n\n"
            content += "## How to use these diagrams:\n\n"
            content += "1. Copy the Mermaid diagram code blocks\n"
            content += "2. Replace verbose code sections in your blog post\n"
            content += "3. The diagrams will render automatically in markdown\n\n"
            content += "---\n\n"
            content += update['diagrams']
            
            with open(output_file, 'w') as f:
                f.write(content)
            
            print(f"📁 Saved template: {output_file.name}")

def main():
    """Main execution"""
    print("📊 Blog Diagram Generator")
    print("=" * 50)
    
    generator = BlogDiagramGenerator()
    updates = generator.process_high_priority_posts()
    
    if updates:
        generator.save_diagram_templates(updates)
        
        print("\n" + "=" * 50)
        print("✨ Diagram generation complete!")
        print(f"\n📁 Templates saved in: diagram_templates/")
        print("\n🎯 Next steps:")
        print("1. Review the generated diagrams")
        print("2. Integrate them into your blog posts")
        print("3. Remove or condense the verbose code blocks")
        print("4. Test that Mermaid diagrams render correctly")
        print("\n💡 Tips:")
        print("• Place diagrams near the beginning for context")
        print("• Keep essential code snippets (5-10 lines)")
        print("• Link to full code in GitHub gists if needed")
    else:
        print("No high-priority posts found for diagram generation")

if __name__ == "__main__":
    main()