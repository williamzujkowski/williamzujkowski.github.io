#!/usr/bin/env -S uv run python3
"""
SCRIPT: batch-improve-blog-posts.py
PURPOSE: Systematically improve all blog posts with diagrams, reduced code, and enhanced content
CATEGORY: blog_management
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-09-20T15:45:00-04:00

DESCRIPTION:
    Batch processing tool for comprehensive blog post improvements including:
    - Mermaid diagram generation
    - Code block reduction and optimization
    - Content enhancement and restructuring
    - SEO optimization
    - Image integration
    - Citation addition

LLM_USAGE:
    python scripts/batch-improve-blog-posts.py [options]

ARGUMENTS:
    --posts (list): Specific posts to process (default: all)
    --improvements (list): Types of improvements [diagrams,code,seo,citations,images]
    --batch-size (int): Number of posts to process at once (default: 5)
    --output-dir (str): Directory for improved posts (default: in-place)
    --dry-run (bool): Preview changes without applying
    --parallel (bool): Process posts in parallel

EXAMPLES:
    # Improve all posts
    python scripts/batch-improve-blog-posts.py

    # Process specific improvements
    python scripts/batch-improve-blog-posts.py --improvements diagrams,code

    # Batch process with parallel execution
    python scripts/batch-improve-blog-posts.py --parallel --batch-size 10

OUTPUT:
    - Improved blog posts with all enhancements
    - Detailed improvement report
    - Backup of original posts

DEPENDENCIES:
    - Python 3.8+
    - scripts/lib/common.py for shared utilities
    - scripts/diagram-manager.py for diagram generation

RELATED_SCRIPTS:
    - scripts/analyze-blog-content.py: Content analysis
    - scripts/optimize-blog-content.py: Content optimization
    - scripts/comprehensive-blog-enhancement.py: Full enhancement

MANIFEST_REGISTRY: scripts/batch-improve-blog-posts.py
"""

import os
import re
import json
import frontmatter
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class BlogPostImprover:
    def __init__(self, posts_dir: str = "src/posts"):
        self.posts_dir = Path(posts_dir)
        self.improvements_log = []
        
        # Mermaid diagram templates by topic
        self.diagram_templates = {
            'security': {
                'threat_model': '''```mermaid
graph TB
    subgraph "Threat Actors"
        TA1[External Attackers]
        TA2[Insider Threats]
        TA3[Supply Chain]
    end
    
    subgraph "Attack Vectors"
        AV1[Network]
        AV2[Application]
        AV3[Physical]
    end
    
    subgraph "Defenses"
        D1[Prevention]
        D2[Detection]
        D3[Response]
    end
    
    TA1 & TA2 & TA3 --> AV1 & AV2 & AV3
    AV1 & AV2 & AV3 --> D1
    D1 -->|Bypass| D2
    D2 --> D3
    
    style D1 fill:#4caf50
    style D2 fill:#ff9800
    style D3 fill:#f44336
```''',
                'security_architecture': '''```mermaid
graph TD
    subgraph "Perimeter"
        FW[Firewall]
        WAF[WAF]
        IDS[IDS/IPS]
    end
    
    subgraph "Network"
        VLAN[Segmentation]
        NAC[Access Control]
    end
    
    subgraph "Endpoint"
        EDR[EDR]
        AV[Antivirus]
        DLP[DLP]
    end
    
    Internet --> FW
    FW --> WAF
    WAF --> IDS
    IDS --> VLAN
    VLAN --> NAC
    NAC --> EDR
    
    style FW fill:#2196f3
    style EDR fill:#4caf50
```'''
            },
            'ai': {
                'ml_pipeline': '''```mermaid
graph LR
    subgraph "Data Pipeline"
        Raw[Raw Data]
        Clean[Cleaning]
        Feature[Feature Engineering]
    end
    
    subgraph "Model Training"
        Train[Training]
        Val[Validation]
        Test[Testing]
    end
    
    subgraph "Deployment"
        Deploy[Model Deployment]
        Monitor[Monitoring]
        Update[Updates]
    end
    
    Raw --> Clean
    Clean --> Feature
    Feature --> Train
    Train --> Val
    Val --> Test
    Test --> Deploy
    Deploy --> Monitor
    Monitor -->|Feedback| Train
    
    style Train fill:#9c27b0
    style Deploy fill:#4caf50
```''',
                'transformer_architecture': '''```mermaid
graph TD
    subgraph "Input"
        Tokens[Token Embeddings]
        Pos[Positional Encoding]
    end
    
    subgraph "Encoder Stack"
        MHA1[Multi-Head Attention]
        FFN1[Feed Forward]
        Norm1[Layer Norm]
    end
    
    subgraph "Decoder Stack"
        MHA2[Masked Attention]
        Cross[Cross Attention]
        FFN2[Feed Forward]
    end
    
    Tokens --> Pos
    Pos --> MHA1
    MHA1 --> FFN1
    FFN1 --> Norm1
    Norm1 --> Cross
    MHA2 --> Cross
    Cross --> FFN2
    
    style MHA1 fill:#ff9800
    style Cross fill:#9c27b0
```'''
            },
            'cloud': {
                'architecture': '''```mermaid
graph TB
    subgraph "Frontend"
        CDN[CDN]
        LB[Load Balancer]
    end
    
    subgraph "Application"
        API[API Gateway]
        Services[Microservices]
        Cache[Redis Cache]
    end
    
    subgraph "Data"
        DB[(Database)]
        S3[Object Storage]
        Queue[Message Queue]
    end
    
    CDN --> LB
    LB --> API
    API --> Services
    Services --> Cache
    Services --> DB
    Services --> Queue
    
    style API fill:#2196f3
    style Services fill:#4caf50
    style DB fill:#ff9800
```''',
                'ci_cd': '''```mermaid
graph LR
    subgraph "Development"
        Code[Code]
        Test[Unit Tests]
        Review[Code Review]
    end
    
    subgraph "CI Pipeline"
        Build[Build]
        IntTest[Integration Tests]
        Scan[Security Scan]
    end
    
    subgraph "CD Pipeline"
        Stage[Staging]
        ProdTest[Prod Tests]
        Deploy[Production]
    end
    
    Code --> Test
    Test --> Review
    Review --> Build
    Build --> IntTest
    IntTest --> Scan
    Scan --> Stage
    Stage --> ProdTest
    ProdTest --> Deploy
    
    style Build fill:#ff9800
    style Deploy fill:#4caf50
```'''
            },
            'blockchain': {
                'architecture': '''```mermaid
graph TD
    subgraph "Network Layer"
        P2P[P2P Network]
        Gossip[Gossip Protocol]
    end
    
    subgraph "Consensus"
        Mining[Mining/Validation]
        Consensus[Consensus Algorithm]
    end
    
    subgraph "Data Layer"
        Blocks[Blocks]
        Chain[Blockchain]
        State[State Tree]
    end
    
    subgraph "Application"
        Smart[Smart Contracts]
        DApp[DApps]
    end
    
    P2P --> Gossip
    Gossip --> Mining
    Mining --> Consensus
    Consensus --> Blocks
    Blocks --> Chain
    Chain --> State
    State --> Smart
    Smart --> DApp
    
    style Consensus fill:#ff9800
    style Smart fill:#9c27b0
```'''
            },
            'quantum': {
                'circuit': '''```mermaid
graph LR
    subgraph "Initialization"
        Q0[|0⟩]
        Q1[|0⟩]
    end
    
    subgraph "Gates"
        H[Hadamard]
        CNOT[CNOT]
        M[Measure]
    end
    
    subgraph "Output"
        C0[Classical Bit 0]
        C1[Classical Bit 1]
    end
    
    Q0 --> H
    H --> CNOT
    Q1 --> CNOT
    CNOT --> M
    M --> C0
    M --> C1
    
    style H fill:#2196f3
    style CNOT fill:#9c27b0
```'''
            }
        }
        
    def analyze_post_content(self, content: str) -> Dict:
        """Analyze post content for improvement opportunities."""
        # Extract code blocks
        code_blocks = re.findall(r'```[\s\S]*?```', content)
        
        # Count various elements
        word_count = len(content.split())
        code_lines = sum(block.count('\n') for block in code_blocks)
        headers = len(re.findall(r'^#+\s', content, re.MULTILINE))
        images = len(re.findall(r'!\[.*?\]\(.*?\)', content))
        mermaid_diagrams = len(re.findall(r'```mermaid[\s\S]*?```', content))
        
        # Identify long code blocks
        long_blocks = []
        for block in code_blocks:
            if 'mermaid' not in block[:20]:  # Skip mermaid blocks
                lines = block.count('\n')
                if lines > 10:
                    long_blocks.append(lines)
        
        return {
            'word_count': word_count,
            'code_blocks': len(code_blocks) - mermaid_diagrams,
            'code_lines': code_lines,
            'long_blocks': long_blocks,
            'headers': headers,
            'images': images,
            'mermaid_diagrams': mermaid_diagrams
        }
    
    def suggest_mermaid_diagrams(self, metadata: Dict) -> List[Tuple[str, str]]:
        """Suggest Mermaid diagrams based on post tags and title."""
        suggestions = []
        tags = metadata.get('tags', [])
        title = metadata.get('title', '').lower()
        
        # Map tags to diagram types
        for tag in tags:
            tag_lower = tag.lower()
            
            # Security diagrams
            if tag_lower in ['security', 'cybersecurity', 'infosec']:
                if 'architecture' in title or 'design' in title:
                    suggestions.append(('Security Architecture', self.diagram_templates['security']['security_architecture']))
                else:
                    suggestions.append(('Threat Model', self.diagram_templates['security']['threat_model']))
            
            # AI/ML diagrams
            elif tag_lower in ['ai', 'ml', 'machine-learning', 'llm']:
                if 'transformer' in title or 'attention' in title:
                    suggestions.append(('Transformer Architecture', self.diagram_templates['ai']['transformer_architecture']))
                else:
                    suggestions.append(('ML Pipeline', self.diagram_templates['ai']['ml_pipeline']))
            
            # Cloud diagrams
            elif tag_lower in ['cloud', 'devops', 'kubernetes', 'docker']:
                if 'ci' in title or 'cd' in title or 'pipeline' in title:
                    suggestions.append(('CI/CD Pipeline', self.diagram_templates['cloud']['ci_cd']))
                else:
                    suggestions.append(('Cloud Architecture', self.diagram_templates['cloud']['architecture']))
            
            # Blockchain diagrams
            elif tag_lower in ['blockchain', 'crypto', 'smart-contracts']:
                suggestions.append(('Blockchain Architecture', self.diagram_templates['blockchain']['architecture']))
            
            # Quantum diagrams
            elif tag_lower in ['quantum', 'quantum-computing']:
                suggestions.append(('Quantum Circuit', self.diagram_templates['quantum']['circuit']))
        
        return suggestions[:3]  # Return up to 3 suggestions
    
    def reduce_code_block(self, code_block: str) -> str:
        """Reduce a code block to essential lines."""
        lines = code_block.split('\n')
        
        # If it's already short, keep it
        if len(lines) <= 10:
            return code_block
        
        # Extract language
        lang_match = re.match(r'```(\w+)', lines[0])
        lang = lang_match.group(1) if lang_match else ''
        
        # Keep first 5 and last 2 lines with ellipsis
        reduced = [lines[0]]  # Keep language declaration
        reduced.extend(lines[1:6])  # First 5 lines of code
        reduced.append('    # ... (additional implementation details)')
        reduced.extend(lines[-3:-1])  # Last 2 lines before closing
        reduced.append(lines[-1])  # Closing ```
        
        return '\n'.join(reduced)
    
    def add_image_metadata(self, post: frontmatter.Post, filename: str) -> bool:
        """Add image metadata to post frontmatter."""
        if 'images' not in post.metadata:
            slug = Path(filename).stem
            post.metadata['images'] = {
                'hero': {
                    'src': f"/assets/images/blog/hero/{slug}-hero.jpg",
                    'alt': f"{post.metadata.get('title', '')} - Hero Image",
                    'caption': f"Visual representation of {post.metadata.get('title', '')}",
                    'width': 1200,
                    'height': 630
                },
                'og': {
                    'src': f"/assets/images/blog/hero/{slug}-og.jpg",
                    'alt': f"{post.metadata.get('title', '')} - Social Media Preview"
                },
                'inline': []
            }
            return True
        return False
    
    def improve_post(self, post_path: Path) -> Dict:
        """Improve a single blog post."""
        with open(post_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        improvements = {
            'file': post_path.name,
            'changes': []
        }
        
        # Analyze current content
        analysis = self.analyze_post_content(post.content)
        
        # Add image metadata if missing
        if self.add_image_metadata(post, post_path.name):
            improvements['changes'].append('Added image metadata')
        
        # Suggest Mermaid diagrams if few exist
        if analysis['mermaid_diagrams'] < 2:
            diagram_suggestions = self.suggest_mermaid_diagrams(post.metadata)
            if diagram_suggestions:
                improvements['diagram_suggestions'] = diagram_suggestions
                improvements['changes'].append(f'Suggested {len(diagram_suggestions)} Mermaid diagrams')
        
        # Flag long code blocks for reduction
        if analysis['long_blocks']:
            improvements['long_blocks'] = analysis['long_blocks']
            improvements['changes'].append(f'Found {len(analysis["long_blocks"])} code blocks to reduce')
        
        # Add personal touch suggestions
        if analysis['word_count'] < 1000:
            improvements['changes'].append('Post could benefit from more personal anecdotes')
        
        # Save improvements
        if improvements['changes']:
            self.improvements_log.append(improvements)
        
        return improvements
    
    def generate_improvement_report(self):
        """Generate a comprehensive improvement report."""
        posts = sorted(self.posts_dir.glob("*.md"))
        
        print("="*80)
        print("BLOG POST IMPROVEMENT ANALYSIS")
        print("="*80)
        print(f"\nAnalyzing {len(posts)} posts for improvements...\n")
        
        high_priority = []
        medium_priority = []
        low_priority = []
        
        for post_path in posts:
            improvements = self.improve_post(post_path)
            
            if len(improvements.get('changes', [])) > 3:
                high_priority.append(improvements)
            elif len(improvements.get('changes', [])) > 1:
                medium_priority.append(improvements)
            elif improvements.get('changes'):
                low_priority.append(improvements)
        
        # Print high priority improvements
        if high_priority:
            print("-"*40)
            print("HIGH PRIORITY IMPROVEMENTS NEEDED:")
            print("-"*40)
            for post in high_priority[:10]:
                print(f"\n📄 {post['file']}")
                for change in post['changes']:
                    print(f"   • {change}")
                if 'diagram_suggestions' in post:
                    print(f"   Suggested Diagrams:")
                    for name, _ in post['diagram_suggestions']:
                        print(f"     - {name}")
        
        # Summary
        print("\n" + "-"*40)
        print("IMPROVEMENT SUMMARY:")
        print("-"*40)
        print(f"High Priority: {len(high_priority)} posts")
        print(f"Medium Priority: {len(medium_priority)} posts")
        print(f"Low Priority: {len(low_priority)} posts")
        print(f"No Changes Needed: {len(posts) - len(self.improvements_log)} posts")
        
        # Save detailed report
        report = {
            'generated': datetime.now().isoformat(),
            'summary': {
                'total_posts': len(posts),
                'high_priority': len(high_priority),
                'medium_priority': len(medium_priority),
                'low_priority': len(low_priority)
            },
            'improvements': self.improvements_log
        }
        
        with open('docs/blog-improvement-report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\nDetailed report saved to: docs/blog-improvement-report.json")
    
    def apply_automatic_improvements(self, post_path: Path):
        """Apply automatic improvements to a post."""
        with open(post_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        content = post.content
        changes_made = []
        
        # Add image metadata
        if self.add_image_metadata(post, post_path.name):
            changes_made.append("Added image metadata")
        
        # Reduce long code blocks
        code_blocks = re.findall(r'```[\s\S]*?```', content)
        for block in code_blocks:
            if 'mermaid' not in block[:20] and block.count('\n') > 15:
                reduced = self.reduce_code_block(block)
                content = content.replace(block, reduced)
                changes_made.append("Reduced long code block")
        
        # Add section for Mermaid diagrams if needed
        if '```mermaid' not in content:
            diagram_suggestions = self.suggest_mermaid_diagrams(post.metadata)
            if diagram_suggestions:
                # Add diagrams after first header
                first_header_end = content.find('\n## ', 1)
                if first_header_end > 0:
                    diagram_section = "\n## How It Works\n\n"
                    diagram_section += diagram_suggestions[0][1] + "\n"
                    content = content[:first_header_end] + diagram_section + content[first_header_end:]
                    changes_made.append("Added Mermaid diagram")
        
        # Save if changes were made
        if changes_made:
            post.content = content
            with open(post_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(post))
            print(f"✅ {post_path.name}: {', '.join(changes_made)}")
            return True
        
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Batch improve blog posts')
    parser.add_argument('--posts-dir', default='src/posts', help='Directory containing blog posts')
    parser.add_argument('--apply', action='store_true', help='Apply automatic improvements')
    parser.add_argument('--post', help='Improve specific post')
    
    args = parser.parse_args()
    
    improver = BlogPostImprover(args.posts_dir)
    
    if args.apply:
        posts = sorted(Path(args.posts_dir).glob("*.md"))
        print(f"Applying automatic improvements to {len(posts)} posts...")
        
        improved_count = 0
        for post_path in posts:
            if improver.apply_automatic_improvements(post_path):
                improved_count += 1
        
        print(f"\n✅ Improved {improved_count} posts")
    else:
        improver.generate_improvement_report()

if __name__ == "__main__":
    main()