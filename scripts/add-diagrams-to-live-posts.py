#!/usr/bin/env python3
"""
Add Mermaid diagrams to existing published blog posts
"""

from pathlib import Path
import yaml
import re

class DiagramAdder:
    def __init__(self):
        self.base_path = Path(".")
        self.posts_dir = self.base_path / "src" / "posts"
        
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
    
    def add_vulnerability_diagrams_to_existing(self):
        """Add diagrams to the existing vulnerability post"""
        post_file = self.posts_dir / "2025-07-15-vulnerability-management-scale-open-source.md"
        
        if post_file.exists():
            with open(post_file, 'r') as f:
                content = f.read()
            
            frontmatter, post_content = self.parse_frontmatter(content)
            
            # Check if already has diagrams
            if "```mermaid" in post_content:
                print(f"✅ {post_file.name} already has Mermaid diagrams")
                return
            
            # Add architecture diagram early in the post
            architecture_diagram = """

## Vulnerability Management Architecture

```mermaid
graph TB
    subgraph "Data Collection"
        NVD[NVD Database]
        CVE[CVE/MITRE]
        GitHub[GitHub Advisory]
        OSV[OSV Database]
    end
    
    subgraph "Processing Pipeline"
        Collect[Data Collector]
        Parse[CVE Parser]
        Enrich[Data Enricher]
        Score[Risk Scorer]
    end
    
    subgraph "Storage & Analysis"
        DB[(PostgreSQL)]
        Cache[(Redis Cache)]
        ML[ML Analysis]
    end
    
    subgraph "Output"
        API[REST API]
        Dashboard[Dashboard]
        Alerts[Alert System]
    end
    
    NVD --> Collect
    CVE --> Collect
    GitHub --> Collect
    OSV --> Collect
    
    Collect --> Parse
    Parse --> Enrich
    Enrich --> Score
    
    Score --> DB
    Score --> Cache
    DB --> ML
    
    ML --> API
    ML --> Dashboard
    ML --> Alerts
    
    style Collect fill:#4caf50
    style Score fill:#ff9800
    style Alerts fill:#f44336
```

"""
            
            # Find where to insert - after the introduction
            if "## The Challenge" in post_content:
                idx = post_content.find("## The Challenge")
                post_content = post_content[:idx] + architecture_diagram + post_content[idx:]
            else:
                # Add after first paragraph
                first_para_end = post_content.find("\n\n", 100)
                if first_para_end > 0:
                    post_content = post_content[:first_para_end] + architecture_diagram + post_content[first_para_end:]
            
            # Save updated content
            new_content = '---\n'
            new_content += yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
            new_content += '---\n'
            new_content += post_content
            
            with open(post_file, 'w') as f:
                f.write(new_content)
            
            print(f"✅ Added diagrams to {post_file.name}")
    
    def add_ebpf_diagrams_to_existing(self):
        """Add diagrams to the eBPF post"""
        post_file = self.posts_dir / "2025-07-01-ebpf-security-monitoring-practical-guide.md"
        
        if post_file.exists():
            with open(post_file, 'r') as f:
                content = f.read()
            
            frontmatter, post_content = self.parse_frontmatter(content)
            
            if "```mermaid" in post_content:
                print(f"✅ {post_file.name} already has Mermaid diagrams")
                return
            
            ebpf_diagram = """

## eBPF Security Architecture

```mermaid
graph TB
    subgraph "Kernel Space"
        Probe[Kernel Probes]
        BPF[eBPF Programs]
        Maps[(BPF Maps)]
    end
    
    subgraph "User Space"
        Loader[BPF Loader]
        Monitor[Event Monitor]
        Analyzer[Security Analyzer]
    end
    
    subgraph "Monitored Events"
        Syscalls[System Calls]
        Network[Network Events]
        Files[File Operations]
        Process[Process Events]
    end
    
    Syscalls --> Probe
    Network --> Probe
    Files --> Probe
    Process --> Probe
    
    Probe --> BPF
    BPF --> Maps
    
    Loader --> BPF
    Maps --> Monitor
    Monitor --> Analyzer
    
    style BPF fill:#ff9800
    style Maps fill:#ffd54f
    style Analyzer fill:#4caf50
```

## Event Processing Flow

```mermaid
sequenceDiagram
    participant K as Kernel
    participant B as eBPF Program
    participant M as BPF Maps
    participant U as User Space
    participant A as Analyzer
    
    K->>B: System Event
    B->>B: Filter & Process
    B->>M: Store Event Data
    U->>M: Poll Maps
    M-->>U: Event Data
    U->>A: Analyze Events
    A-->>U: Security Alert (if needed)
```

"""
            
            # Add after introduction
            if "## Understanding eBPF" in post_content:
                idx = post_content.find("## Understanding eBPF")
                post_content = post_content[:idx] + ebpf_diagram + post_content[idx:]
            else:
                first_section = post_content.find("\n##")
                if first_section > 0:
                    post_content = post_content[:first_section] + ebpf_diagram + post_content[first_section:]
            
            # Save
            new_content = '---\n'
            new_content += yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
            new_content += '---\n'
            new_content += post_content
            
            with open(post_file, 'w') as f:
                f.write(new_content)
            
            print(f"✅ Added diagrams to {post_file.name}")
    
    def add_zero_trust_diagrams(self):
        """Add diagrams to Zero Trust post"""
        post_file = self.posts_dir / "2024-08-27-zero-trust-security-principles.md"
        
        if not post_file.exists():
            print(f"⚠️ {post_file.name} not found")
            return
        
        with open(post_file, 'r') as f:
            content = f.read()
        
        frontmatter, post_content = self.parse_frontmatter(content)
        
        if "```mermaid" in post_content:
            print(f"✅ {post_file.name} already has Mermaid diagrams")
            return
        
        zero_trust_diagram = """

## Zero Trust Architecture

```mermaid
graph TB
    subgraph "Identity & Access"
        User[Users]
        Device[Devices]
        Apps[Applications]
    end
    
    subgraph "Policy Engine"
        PEP[Policy Enforcement]
        PDP[Policy Decision]
        Trust[Trust Engine]
    end
    
    subgraph "Verification"
        MFA[Multi-Factor Auth]
        Risk[Risk Assessment]
        Context[Context Analysis]
    end
    
    subgraph "Resources"
        Data[(Data)]
        Services[Services]
        Network[Network]
    end
    
    User --> PEP
    Device --> PEP
    Apps --> PEP
    
    PEP --> PDP
    PDP --> Trust
    
    Trust --> MFA
    Trust --> Risk
    Trust --> Context
    
    MFA --> PDP
    Risk --> PDP
    Context --> PDP
    
    PDP -->|Allow/Deny| Data
    PDP -->|Allow/Deny| Services
    PDP -->|Allow/Deny| Network
    
    style PEP fill:#ff5252
    style Trust fill:#ff9800
    style PDP fill:#4caf50
```

## Zero Trust Verification Flow

```mermaid
flowchart TD
    Start([Access Request]) --> Identity[Verify Identity]
    Identity --> Device[Verify Device]
    Device --> Context[Check Context]
    Context --> Risk[Assess Risk]
    
    Risk --> Level{Risk Level?}
    Level -->|High| Deny[Deny Access]
    Level -->|Medium| MFA[Require MFA]
    Level -->|Low| Policy[Check Policies]
    
    MFA --> Valid{Valid?}
    Valid -->|No| Deny
    Valid -->|Yes| Policy
    
    Policy --> Pass{Pass?}
    Pass -->|No| Deny
    Pass -->|Yes| Grant[Grant Access]
    
    Grant --> Monitor[Monitor Session]
    Monitor --> Anomaly{Anomaly?}
    Anomaly -->|Yes| Revoke[Revoke Access]
    Anomaly -->|No| Monitor
    
    style Deny fill:#f44336
    style Grant fill:#4caf50
    style Monitor fill:#2196f3
```

"""
        
        # Find where to add - after introduction
        first_section = post_content.find("\n## ")
        if first_section > 0:
            post_content = post_content[:first_section] + zero_trust_diagram + post_content[first_section:]
        
        # Save
        new_content = '---\n'
        new_content += yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
        new_content += '---\n'
        new_content += post_content
        
        with open(post_file, 'w') as f:
            f.write(new_content)
        
        print(f"✅ Added diagrams to {post_file.name}")
    
    def add_local_llm_diagrams(self):
        """Add diagrams to Local LLM post"""
        post_file = self.posts_dir / "2025-06-25-local-llm-deployment-privacy-first.md"
        
        if post_file.exists():
            with open(post_file, 'r') as f:
                content = f.read()
            
            frontmatter, post_content = self.parse_frontmatter(content)
            
            if "```mermaid" in post_content:
                print(f"✅ {post_file.name} already has Mermaid diagrams")
                return
            
            llm_diagram = """

## Local LLM Architecture

```mermaid
graph TB
    subgraph "Hardware"
        GPU[GPU/TPU]
        CPU[CPU]
        RAM[Memory]
    end
    
    subgraph "Model Layer"
        Models[(Model Files)]
        Weights[Weights]
        Config[Configuration]
    end
    
    subgraph "Inference"
        Engine[Inference Engine]
        Cache[Token Cache]
        Batch[Batch Processing]
    end
    
    subgraph "Interface"
        API[REST API]
        UI[Web UI]
        CLI[CLI Tool]
    end
    
    GPU --> Engine
    CPU --> Engine
    RAM --> Cache
    
    Models --> Engine
    Weights --> Engine
    Config --> Engine
    
    Engine --> Cache
    Engine --> Batch
    
    Batch --> API
    API --> UI
    API --> CLI
    
    style GPU fill:#ff9800
    style Engine fill:#4caf50
    style API fill:#2196f3
```

"""
            
            # Add after introduction
            first_section = post_content.find("\n## ")
            if first_section > 0:
                post_content = post_content[:first_section] + llm_diagram + post_content[first_section:]
            
            # Save
            new_content = '---\n'
            new_content += yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
            new_content += '---\n'
            new_content += post_content
            
            with open(post_file, 'w') as f:
                f.write(new_content)
            
            print(f"✅ Added diagrams to {post_file.name}")
    
    def process_all(self):
        """Process all posts"""
        print("🎨 Adding Mermaid Diagrams to Blog Posts")
        print("=" * 50)
        
        # Add to existing published posts
        self.add_zero_trust_diagrams()
        
        # Add to future posts (they'll be ready when published)
        self.add_vulnerability_diagrams_to_existing()
        self.add_ebpf_diagrams_to_existing()
        self.add_local_llm_diagrams()
        
        print("\n✨ Diagram integration complete!")

def main():
    adder = DiagramAdder()
    adder.process_all()

if __name__ == "__main__":
    main()