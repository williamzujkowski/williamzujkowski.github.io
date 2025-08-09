#!/usr/bin/env python3
"""
Integrate Mermaid diagrams and optimize code blocks in blog posts
"""

import re
from pathlib import Path
import yaml

class DiagramIntegrator:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.posts_dir = self.base_path / "src" / "posts"
        self.templates_dir = self.base_path / "diagram_templates"
        
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
    
    def reduce_code_block(self, code: str, language: str, max_lines: int = 10) -> str:
        """Reduce a code block to essential lines"""
        lines = code.strip().split('\n')
        
        # Skip import/boilerplate lines
        essential_lines = []
        skip_patterns = ['import ', 'from ', 'require(', 'use ', '#include']
        
        for line in lines:
            # Skip empty lines and imports
            if not line.strip() or any(pattern in line for pattern in skip_patterns):
                continue
            essential_lines.append(line)
        
        # If still too long, take the most important parts
        if len(essential_lines) > max_lines:
            # Try to find the main function/class
            main_indices = []
            for i, line in enumerate(essential_lines):
                if any(keyword in line.lower() for keyword in ['def main', 'class ', 'function ', 'async def']):
                    main_indices.append(i)
            
            if main_indices:
                # Take lines around the main function
                start = main_indices[0]
                essential_lines = essential_lines[start:start + max_lines]
            else:
                # Take middle section
                mid = len(essential_lines) // 2
                start = max(0, mid - max_lines // 2)
                essential_lines = essential_lines[start:start + max_lines]
            
            # Add ellipsis to indicate truncation
            if start > 0:
                essential_lines.insert(0, '# ... previous code omitted ...')
            if start + max_lines < len(lines):
                essential_lines.append('# ... additional code omitted ...')
        
        return '\n'.join(essential_lines)
    
    def integrate_claude_flow_diagrams(self, post_file: Path):
        """Integrate diagrams into Claude-Flow post"""
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        frontmatter, post_content = self.parse_frontmatter(content)
        
        # Find the architecture section
        architecture_pattern = r'(## The Architecture of Intelligence.*?)(```javascript.*?```\n)'
        match = re.search(architecture_pattern, post_content, re.DOTALL)
        
        if match:
            # Insert diagram before the code
            diagram = """

## System Architecture Overview

```mermaid
graph TB
    subgraph "Swarm Topologies"
        Mesh[Mesh - P2P Collaboration]
        Hier[Hierarchical - Queen/Worker]
        Ring[Ring - Sequential Pipeline]
        Star[Star - Centralized Control]
    end
    
    subgraph "Core Agents"
        Orch[🎭 Orchestrator]
        Research[🔍 Researcher]
        Arch[🏗️ Architect]
        Coder[💻 Coder]
        Tester[🧪 Tester]
    end
    
    subgraph "Intelligence Layer"
        Memory[(💾 Persistent Memory)]
        Neural[🧠 Neural Training]
        Pattern[🔄 Pattern Recognition]
    end
    
    Mesh --> Orch
    Hier --> Orch
    Ring --> Orch
    Star --> Orch
    
    Orch --> Research
    Orch --> Arch
    Orch --> Coder
    Orch --> Tester
    
    Research --> Memory
    Arch --> Pattern
    Coder --> Neural
    Tester --> Memory
    
    style Orch fill:#9c27b0,stroke:#fff,stroke-width:2px,color:#fff
    style Memory fill:#ffd54f,stroke:#333,stroke-width:2px
    style Neural fill:#4caf50,stroke:#fff,stroke-width:2px,color:#fff
```

"""
            post_content = post_content[:match.start(2)] + diagram + match.group(2) + post_content[match.end():]
        
        # Find and reduce the YAML execution plan
        yaml_pattern = r'```yaml\n# The swarm\'s execution plan.*?```'
        match = re.search(yaml_pattern, post_content, re.DOTALL)
        if match:
            # Replace with a simplified version
            simplified = """```yaml
# Simplified swarm execution plan
swarm_execution:
  specification: [researcher, analyst] → Requirements analysis
  architecture: [architect, system-architect] → System design  
  implementation: [backend-dev, coder, api-docs] → Parallel coding
  testing: [tester, tdd-london-swarm] → Comprehensive testing
  refinement: [reviewer, perf-analyzer] → Optimization
```"""
            post_content = post_content[:match.start()] + simplified + post_content[match.end():]
        
        # Add SPARC flow diagram
        sparc_section = "## Practical Use Cases"
        if sparc_section in post_content:
            sparc_diagram = """

## SPARC Development Methodology

```mermaid
flowchart LR
    S[📋 Specification] --> P[🔢 Pseudocode]
    P --> A[🏛️ Architecture]
    A --> R[🔧 Refinement]
    R --> C[✅ Completion]
    
    S -.-> M1{{Define Requirements}}
    P -.-> M2{{Design Algorithms}}
    A -.-> M3{{System Structure}}
    R -.-> M4{{TDD & Iteration}}
    C -.-> M5{{Integration & Deploy}}
    
    style S fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    style P fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style A fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    style R fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
    style C fill:#ffebee,stroke:#d32f2f,stroke-width:2px
```

"""
            idx = post_content.find(sparc_section)
            post_content = post_content[:idx] + sparc_diagram + post_content[idx:]
        
        # Save updated content
        new_content = '---\n'
        new_content += yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
        new_content += '---\n'
        new_content += post_content
        
        with open(post_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Updated Claude-Flow post with diagrams")
    
    def integrate_vulnerability_diagrams(self, post_file: Path):
        """Integrate diagrams into vulnerability management post"""
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        frontmatter, post_content = self.parse_frontmatter(content)
        
        # Add architecture diagram at the beginning
        intro_end = post_content.find("## The Challenge")
        if intro_end > 0:
            architecture = """

## System Architecture

```mermaid
graph TB
    subgraph "Data Sources"
        NVD[NVD Database]
        CVE[CVE/MITRE]
        GH[GitHub Advisory]
    end
    
    subgraph "Processing"
        Collect[Data Collector]
        Enrich[Enrichment Engine]
        Score[Risk Scoring]
    end
    
    subgraph "Storage & Analysis"
        DB[(PostgreSQL)]
        ML[ML Models]
        Alert[Alert System]
    end
    
    NVD --> Collect
    CVE --> Collect
    GH --> Collect
    
    Collect --> Enrich
    Enrich --> Score
    Score --> DB
    
    DB --> ML
    ML --> Alert
    
    style Alert fill:#ff5252,stroke:#fff,stroke-width:2px,color:#fff
    style ML fill:#4caf50,stroke:#fff,stroke-width:2px,color:#fff
```

"""
            post_content = post_content[:intro_end] + architecture + post_content[intro_end:]
        
        # Find and reduce large code blocks
        code_pattern = r'```python\n(.*?)```'
        matches = list(re.finditer(code_pattern, post_content, re.DOTALL))
        
        # Process from end to avoid offset issues
        for match in reversed(matches):
            code = match.group(1)
            lines = code.strip().split('\n')
            if len(lines) > 30:
                # This is a large block, reduce it
                reduced = self.reduce_code_block(code, 'python', 15)
                post_content = post_content[:match.start(1)] + reduced + post_content[match.end(1):]
        
        # Save updated content
        new_content = '---\n'
        new_content += yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
        new_content += '---\n'
        new_content += post_content
        
        with open(post_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Updated vulnerability management post")
    
    def integrate_ebpf_diagrams(self, post_file: Path):
        """Integrate diagrams into eBPF post"""
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        frontmatter, post_content = self.parse_frontmatter(content)
        
        # Add eBPF architecture diagram
        intro_section = "## Understanding eBPF"
        if intro_section in post_content:
            diagram = """

## eBPF Architecture

```mermaid
graph TB
    subgraph "Kernel Space"
        KProbe[Kernel Probes]
        BPF[eBPF Program]
        Maps[(BPF Maps)]
    end
    
    subgraph "User Space"
        Loader[Program Loader]
        Monitor[Event Monitor]
        Analyzer[Security Analyzer]
    end
    
    subgraph "Events"
        Syscall[System Calls]
        Network[Network Packets]
        File[File Operations]
    end
    
    Syscall --> KProbe
    Network --> BPF
    File --> KProbe
    
    KProbe --> BPF
    BPF --> Maps
    Maps --> Monitor
    
    Loader --> BPF
    Monitor --> Analyzer
    
    style BPF fill:#ff9800,stroke:#fff,stroke-width:2px,color:#fff
    style Analyzer fill:#4caf50,stroke:#fff,stroke-width:2px,color:#fff
```

"""
            idx = post_content.find(intro_section)
            end_idx = idx + len(intro_section)
            post_content = post_content[:end_idx] + diagram + post_content[end_idx:]
        
        # Reduce large code blocks
        code_pattern = r'```c\n(.*?)```'
        matches = list(re.finditer(code_pattern, post_content, re.DOTALL))
        
        for match in reversed(matches):
            code = match.group(1)
            lines = code.strip().split('\n')
            if len(lines) > 25:
                reduced = self.reduce_code_block(code, 'c', 12)
                post_content = post_content[:match.start(1)] + reduced + post_content[match.end(1):]
        
        # Save
        new_content = '---\n'
        new_content += yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
        new_content += '---\n'
        new_content += post_content
        
        with open(post_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Updated eBPF post with diagrams")
    
    def process_all_high_priority_posts(self):
        """Process all high-priority posts"""
        posts_to_process = [
            ('2025-08-07-supercharging-development-claude-flow.md', self.integrate_claude_flow_diagrams),
            ('2025-07-15-vulnerability-management-scale-open-source.md', self.integrate_vulnerability_diagrams),
            ('2025-07-01-ebpf-security-monitoring-practical-guide.md', self.integrate_ebpf_diagrams),
        ]
        
        for post_file, integration_func in posts_to_process:
            post_path = self.posts_dir / post_file
            if post_path.exists():
                try:
                    integration_func(post_path)
                except Exception as e:
                    print(f"❌ Error processing {post_file}: {e}")

def main():
    print("🎨 Integrating Diagrams and Optimizing Blog Posts")
    print("=" * 50)
    
    integrator = DiagramIntegrator()
    integrator.process_all_high_priority_posts()
    
    print("\n✨ Integration complete!")
    print("Diagrams added and code blocks optimized.")

if __name__ == "__main__":
    main()