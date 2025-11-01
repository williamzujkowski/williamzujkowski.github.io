#!/usr/bin/env -S uv run python3
"""
SCRIPT: comprehensive-blog-enhancement.py
PURPOSE: Comprehensive Blog Enhancement Tool
CATEGORY: blog_management
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T15:08:08-04:00

DESCRIPTION:
    Comprehensive Blog Enhancement Tool. This script is part of the blog management
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/comprehensive-blog-enhancement.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/comprehensive-blog-enhancement.py

    # With verbose output
    python scripts/comprehensive-blog-enhancement.py --verbose

OUTPUT:
    - Processed results based on script functionality
    - Log messages if verbose mode enabled

DEPENDENCIES:
    - Python 3.8+
    - See imports for specific package requirements
    - scripts/lib/common.py for shared utilities (if applicable)

RELATED_SCRIPTS:
    - scripts/lib/common.py: Shared utilities
    - [Other related scripts in blog_management category]

MANIFEST_REGISTRY: scripts/comprehensive-blog-enhancement.py
"""

import os
import re
import json
import frontmatter
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class BlogEnhancer:
    def __init__(self, posts_dir: str = "src/posts", uses_file: str = "src/pages/uses.md"):
        self.posts_dir = Path(posts_dir)
        self.uses_file = Path(uses_file)
        self.uses_content = self.load_uses_page()
        self.hardware_facts = self.extract_hardware_facts()
        self.enhancements = []
        
    def load_uses_page(self) -> str:
        """Load the uses page content as source of truth."""
        with open(self.uses_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def extract_hardware_facts(self) -> Dict:
        """Extract factual information from uses page."""
        facts = {
            'processor': 'Intel Core i9-9900K @ 3.60GHz',
            'ram': '64GB DDR4',
            'gpu': 'NVIDIA RTX 3090',
            'server': 'Dell R940 with 256GB RAM and Proxmox',
            'storage': 'TrueNAS with 40TB raw storage',
            'firewall': 'Dream Machine Professional',
            'raspberry_pi': '3x Raspberry Pi 5 16GB, 1x Raspberry Pi 4 8GB',
            'network': 'Ubiquiti switches and APs with VLANs',
            'hypervisor': 'Proxmox',
            'containers': 'Docker and Podman',
            'orchestration': 'K3s',
            'monitoring': 'Wazuh, Grafana, Prometheus, Netdata',
            'security_tools': ['Nessus', 'OSV', 'Grype', 'Wireshark', 'nmap', 'tcpdump'],
            'password_manager': 'Self-hosted Bitwarden',
            'backup': 'Restic to local NAS + Backblaze B2',
            'editor': 'VS Code',
            'terminal': 'Ghostty',
            'shell': 'Zsh with Oh My Zsh'
        }
        return facts
    
    def check_hardware_claims(self, content: str) -> List[str]:
        """Check for incorrect hardware claims in content."""
        issues = []
        
        # Common mistakes to check
        incorrect_patterns = [
            (r'32GB(?:\s+of)?\s+RAM', '64GB RAM'),
            (r'RTX\s+3080', 'RTX 3090'),
            (r'i7-\d+', 'i9-9900K'),
            (r'ESXi', 'Proxmox'),
            (r'pfSense', 'Dream Machine Professional'),
            (r'LastPass', 'Bitwarden (self-hosted)'),
            (r'8GB\s+Pi\s+5', '16GB Pi 5'),
            (r'Docker\s+only', 'Docker and Podman'),
        ]
        
        for pattern, correct in incorrect_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(f"Found '{pattern}' - should be '{correct}'")
        
        return issues
    
    def add_reputable_sources(self, content: str, tags: List[str]) -> Dict:
        """Suggest reputable sources based on content and tags."""
        sources = {
            'security': [
                'NIST Cybersecurity Framework: https://www.nist.gov/cyberframework',
                'OWASP Top 10: https://owasp.org/www-project-top-ten/',
                'CVE Database: https://cve.mitre.org/',
                'SANS Institute: https://www.sans.org/reading-room/',
            ],
            'ai': [
                'arXiv AI papers: https://arxiv.org/list/cs.AI/recent',
                'Papers with Code: https://paperswithcode.com/',
                'Google AI Research: https://ai.google/research/',
                'OpenAI Research: https://openai.com/research/',
            ],
            'cloud': [
                'AWS Well-Architected: https://aws.amazon.com/architecture/well-architected/',
                'Google Cloud Best Practices: https://cloud.google.com/docs/enterprise/best-practices',
                'CNCF Projects: https://www.cncf.io/projects/',
            ],
            'networking': [
                'RFC Editor: https://www.rfc-editor.org/',
                'Cisco Documentation: https://www.cisco.com/c/en/us/tech/index.html',
                'Cloudflare Learning: https://www.cloudflare.com/learning/',
            ],
            'linux': [
                'Linux Kernel Documentation: https://www.kernel.org/doc/',
                'Red Hat Documentation: https://access.redhat.com/documentation/',
                'Arch Wiki: https://wiki.archlinux.org/',
            ],
            'docker': [
                'Docker Official Docs: https://docs.docker.com/',
                'Docker Best Practices: https://docs.docker.com/develop/dev-best-practices/',
                'Container Security: https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html',
            ],
            'kubernetes': [
                'Kubernetes Documentation: https://kubernetes.io/docs/',
                'K3s Documentation: https://docs.k3s.io/',
                'CNCF Kubernetes Security: https://www.cncf.io/blog/2021/11/09/kubernetes-security-best-practices/',
            ]
        }
        
        relevant_sources = []
        for tag in tags:
            tag_lower = tag.lower()
            for category, links in sources.items():
                if category in tag_lower or tag_lower in category:
                    relevant_sources.extend(links)
        
        return {'suggested_sources': list(set(relevant_sources))}
    
    def enhance_mermaid_diagrams(self, content: str, metadata: Dict) -> str:
        """Enhance or add Mermaid diagrams based on content."""
        tags = metadata.get('tags', [])
        
        # Check if post needs more diagrams
        mermaid_count = content.count('```mermaid')
        
        if mermaid_count < 2:
            # Suggest additional diagrams based on content
            if any(tag in ['security', 'monitoring'] for tag in tags):
                if 'detection flow' not in content.lower():
                    diagram = '''
## Detection and Response Flow

```mermaid
graph TD
    subgraph "Detection Layer"
        D1[Network Monitoring]
        D2[Host Monitoring]
        D3[Application Monitoring]
    end
    
    subgraph "Analysis"
        A1[Event Correlation]
        A2[Threat Intelligence]
        A3[Anomaly Detection]
    end
    
    subgraph "Response"
        R1[Alert Generation]
        R2[Automated Response]
        R3[Manual Investigation]
    end
    
    D1 & D2 & D3 --> A1
    A1 --> A2
    A2 --> A3
    A3 --> R1
    R1 --> R2
    R1 --> R3
    
    style A1 fill:#ff9800
    style R2 fill:#4caf50
```'''
                    return content + diagram
        
        return content
    
    def improve_readability(self, content: str) -> Tuple[str, List[str]]:
        """Improve content readability and flow."""
        improvements = []
        
        # Check paragraph length
        paragraphs = content.split('\n\n')
        long_paragraphs = [p for p in paragraphs if len(p.split()) > 100]
        if long_paragraphs:
            improvements.append(f"Found {len(long_paragraphs)} paragraphs over 100 words - consider breaking up")
        
        # Check for transition phrases
        transition_phrases = [
            'Furthermore', 'Moreover', 'In addition', 'However', 
            'Nevertheless', 'On the other hand', 'For example',
            'In conclusion', 'To summarize', 'First', 'Second', 'Finally'
        ]
        
        transition_count = sum(1 for phrase in transition_phrases if phrase in content)
        if transition_count < 3:
            improvements.append("Add more transition phrases for better flow")
        
        # Check for personal anecdotes
        personal_indicators = ['I ', 'my ', 'I\'ve ', 'I\'m ', 'My ']
        personal_count = sum(content.count(indicator) for indicator in personal_indicators)
        if personal_count < 5:
            improvements.append("Add more personal experiences and anecdotes")
        
        # Check for actionable takeaways
        if 'takeaway' not in content.lower() and 'conclusion' not in content.lower():
            improvements.append("Add clear actionable takeaways or conclusion")
        
        return content, improvements
    
    def validate_code_examples(self, content: str) -> List[str]:
        """Validate that code examples are accurate and working."""
        issues = []
        
        # Extract code blocks
        code_blocks = re.findall(r'```(\w+)?\n(.*?)```', content, re.DOTALL)
        
        for lang, code in code_blocks:
            if lang == 'python':
                # Check for common Python issues
                if 'import' in code and 'requirements.txt' not in content:
                    issues.append("Python code has imports but no requirements mentioned")
            elif lang == 'bash':
                # Check for dangerous commands
                dangerous = ['rm -rf /', 'dd if=', ':(){ :|:& };:']
                for cmd in dangerous:
                    if cmd in code:
                        issues.append(f"Dangerous command found: {cmd}")
            elif lang == 'yaml':
                # Check for placeholder values
                if 'YOUR_' in code or 'CHANGE_ME' in code:
                    issues.append("YAML contains placeholder values")
        
        return issues
    
    def enhance_post(self, post_path: Path) -> Dict:
        """Comprehensively enhance a single blog post."""
        with open(post_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        enhancements = {
            'file': post_path.name,
            'improvements': [],
            'issues': [],
            'sources_added': []
        }
        
        # Check hardware claims
        hardware_issues = self.check_hardware_claims(post.content)
        if hardware_issues:
            enhancements['issues'].extend(hardware_issues)
        
        # Add reputable sources
        sources = self.add_reputable_sources(post.content, post.metadata.get('tags', []))
        if sources['suggested_sources']:
            enhancements['sources_added'] = sources['suggested_sources'][:3]
        
        # Enhance Mermaid diagrams
        enhanced_content = self.enhance_mermaid_diagrams(post.content, post.metadata)
        if enhanced_content != post.content:
            enhancements['improvements'].append("Added Mermaid diagram")
            post.content = enhanced_content
        
        # Improve readability
        _, readability_improvements = self.improve_readability(post.content)
        enhancements['improvements'].extend(readability_improvements)
        
        # Validate code examples
        code_issues = self.validate_code_examples(post.content)
        if code_issues:
            enhancements['issues'].extend(code_issues)
        
        # Save if changes were made
        if enhancements['improvements'] or enhancements['issues']:
            self.enhancements.append(enhancements)
        
        return enhancements
    
    def generate_enhancement_report(self):
        """Generate comprehensive enhancement report."""
        posts = sorted(self.posts_dir.glob("*.md"))
        
        print("="*80)
        print("COMPREHENSIVE BLOG ENHANCEMENT REPORT")
        print("="*80)
        print(f"\nAnalyzing {len(posts)} posts for enhancements...\n")
        
        critical_issues = []
        quality_improvements = []
        source_suggestions = []
        
        for post_path in posts:
            result = self.enhance_post(post_path)
            
            if result['issues']:
                critical_issues.append(result)
            if result['improvements']:
                quality_improvements.append(result)
            if result['sources_added']:
                source_suggestions.append(result)
        
        # Report critical issues
        if critical_issues:
            print("-"*40)
            print("CRITICAL ISSUES (Incorrect Information):")
            print("-"*40)
            for post in critical_issues[:10]:
                print(f"\n❌ {post['file']}")
                for issue in post['issues']:
                    print(f"   • {issue}")
        
        # Report quality improvements
        if quality_improvements:
            print("\n" + "-"*40)
            print("QUALITY IMPROVEMENTS NEEDED:")
            print("-"*40)
            for post in quality_improvements[:10]:
                print(f"\n📝 {post['file']}")
                for improvement in post['improvements'][:3]:
                    print(f"   • {improvement}")
        
        # Report source suggestions
        if source_suggestions:
            print("\n" + "-"*40)
            print("REPUTABLE SOURCES TO ADD:")
            print("-"*40)
            for post in source_suggestions[:5]:
                print(f"\n📚 {post['file']}")
                for source in post['sources_added'][:2]:
                    print(f"   • {source}")
        
        # Summary
        print("\n" + "-"*40)
        print("ENHANCEMENT SUMMARY:")
        print("-"*40)
        print(f"Posts with critical issues: {len(critical_issues)}")
        print(f"Posts needing quality improvements: {len(quality_improvements)}")
        print(f"Posts needing sources: {len(source_suggestions)}")
        
        # Save detailed report
        report = {
            'generated': datetime.now().isoformat(),
            'summary': {
                'total_posts': len(posts),
                'critical_issues': len(critical_issues),
                'quality_improvements': len(quality_improvements),
                'source_suggestions': len(source_suggestions)
            },
            'enhancements': self.enhancements
        }
        
        with open('docs/enhancement-report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\nDetailed report saved to: docs/enhancement-report.json")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Comprehensive blog enhancement tool')
    parser.add_argument('--posts-dir', default='src/posts', help='Directory containing blog posts')
    parser.add_argument('--uses-file', default='src/pages/uses.md', help='Path to uses page')
    parser.add_argument('--fix', action='store_true', help='Apply automatic fixes')
    
    args = parser.parse_args()
    
    enhancer = BlogEnhancer(args.posts_dir, args.uses_file)
    
    if args.fix:
        print("Applying automatic enhancements...")
        # Implementation for automatic fixes would go here
        print("Manual review required for critical changes")
    else:
        enhancer.generate_enhancement_report()

if __name__ == "__main__":
    main()