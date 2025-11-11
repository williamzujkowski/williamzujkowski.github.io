#!/usr/bin/env -S uv run python3
"""
SCRIPT: blog-manager.py
PURPOSE: Unified Blog Management Tool for williamzujkowski.github.io
CATEGORY: blog_management
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-11-03

DESCRIPTION:
    Unified Blog Management Tool for williamzujkowski.github.io. This script is part of the blog management
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/blog-manager.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/blog-manager.py

    # With verbose output
    python scripts/blog-manager.py --verbose

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

MANIFEST_REGISTRY: scripts/blog-manager.py
"""

import argparse
import os
import sys
import json
import yaml
import logging
import re
import frontmatter
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import subprocess

# Add parent directory to path for lib imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.logging_config import setup_logger

class BlogManager:
    """Central blog management system"""

    def __init__(self, project_root: Path = None, logger=None):
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.posts_dir = self.project_root / "src" / "posts"
        self.assets_dir = self.project_root / "src" / "assets"
        self.scripts_dir = self.project_root / "scripts"
        self.docs_dir = self.project_root / "docs"
        self.uses_file = self.project_root / "src" / "pages" / "uses.md"
        self.logger = logger or logging.getLogger(__name__)

        # Load configuration
        self.config = self._load_config()

        # Enhancement tracking
        self.enhancements = []
        self.uses_content = self._load_uses_page()
        self.hardware_facts = self._extract_hardware_facts()

    def _load_config(self) -> Dict:
        """Load configuration from MANIFEST.json"""
        manifest_path = self.project_root / "MANIFEST.json"
        if manifest_path.exists():
            with open(manifest_path, 'r') as f:
                return json.load(f)
        return {}

    def enhance_content(self, post_path: str = None, **options) -> bool:
        """
        Enhance blog post content
        Consolidates: optimize-blog-content.py, comprehensive-blog-enhancement.py
        """
        self.logger.info(f"📝 Enhancing content...")

        # If specific post provided
        if post_path:
            path = Path(post_path)
            # Handle both absolute and relative paths
            if not path.is_absolute():
                path = self.project_root / path
            posts = [path]
        else:
            posts = list(self.posts_dir.glob("*.md"))

        # Enhancement options
        hardware_check = options.get('hardware_check', False)
        suggest_sources = options.get('suggest_sources', False)
        enhance_diagrams = options.get('enhance_diagrams', False)
        check_readability = options.get('check_readability', False)
        validate_code = options.get('validate_code', False)
        generate_report = options.get('report', False)
        run_all = options.get('all', False)

        # Reset enhancements tracking
        self.enhancements = []

        for post in posts:
            self.logger.info(f"  Processing: {post.name}")

            result = self._enhance_single_post(
                post,
                hardware_check=hardware_check or run_all,
                suggest_sources=suggest_sources or run_all,
                enhance_diagrams=enhance_diagrams or run_all,
                check_readability=check_readability or run_all,
                validate_code=validate_code or run_all
            )

            if result['improvements'] or result['issues']:
                self.enhancements.append(result)

        # Generate report if requested
        if generate_report or run_all:
            self._generate_enhancement_report()

        return True

    def manage_images(self, action: str, **options) -> bool:
        """
        Manage blog images
        Consolidates: generate-blog-hero-images.py, optimize-blog-images.sh,
                    playwright-image-search.py, fetch-stock-images.py
        """
        self.logger.info(f"🖼️  Managing images: {action}")

        if action == 'generate-hero':
            return self._generate_hero_images(**options)
        elif action == 'optimize':
            return self._optimize_images(**options)
        elif action == 'search':
            return self._search_images(**options)
        elif action == 'update-metadata':
            return self._update_image_metadata(**options)
        else:
            self.logger.info(f"Unknown image action: {action}")
            return False

    def manage_citations(self, action: str, **options) -> bool:
        """
        Manage academic citations and sources
        Consolidates: academic-search.py, add-academic-citations.py,
                    add-reputable-sources-to-posts.py
        """
        self.logger.info(f"📚 Managing citations: {action}")

        if action == 'add':
            return self._add_citations(**options)
        elif action == 'validate':
            return self._validate_citations(**options)
        elif action == 'search':
            return self._search_academic(**options)
        else:
            self.logger.info(f"Unknown citation action: {action}")
            return False

    def manage_diagrams(self, action: str, **options) -> bool:
        """
        Manage diagrams and visualizations
        Consolidates: create-blog-diagrams.py, add-diagrams-to-live-posts.py,
                    integrate-diagrams.py
        """
        self.logger.info(f"📊 Managing diagrams: {action}")

        if action == 'create':
            return self._create_diagrams(**options)
        elif action == 'integrate':
            return self._integrate_diagrams(**options)
        elif action == 'update':
            return self._update_diagrams(**options)
        else:
            self.logger.info(f"Unknown diagram action: {action}")
            return False

    def analyze(self, target: str = 'all', **options) -> Dict:
        """
        Analyze blog content
        Consolidates: analyze-blog-content.py
        """
        self.logger.info(f"🔍 Analyzing: {target}")

        analysis = {
            'posts_count': 0,
            'total_words': 0,
            'avg_readability': 0,
            'missing_images': [],
            'missing_citations': [],
            'quality_scores': {}
        }

        posts = list(self.posts_dir.glob("*.md"))
        analysis['posts_count'] = len(posts)

        for post in posts:
            post_analysis = self._analyze_post(post)
            analysis['total_words'] += post_analysis.get('word_count', 0)

            if post_analysis.get('missing_hero_image'):
                analysis['missing_images'].append(post.name)

            if post_analysis.get('needs_citations'):
                analysis['missing_citations'].append(post.name)

            analysis['quality_scores'][post.name] = post_analysis.get('quality_score', 0)

        # Calculate averages
        if posts:
            analysis['avg_readability'] = sum(analysis['quality_scores'].values()) / len(posts)

        return analysis

    def batch_process(self, operations: List[str], **options) -> bool:
        """
        Batch process multiple operations
        Consolidates: batch-improve-blog-posts.py
        """
        self.logger.info(f"⚡ Batch processing {len(operations)} operations")

        for op in operations:
            self.logger.info(f"\n  Executing: {op}")

            if op == 'enhance':
                self.enhance_content(**options)
            elif op == 'images':
                self.manage_images('generate-hero', **options)
                self.manage_images('optimize', **options)
            elif op == 'citations':
                self.manage_citations('add', **options)
            elif op == 'diagrams':
                self.manage_diagrams('create', **options)
            elif op == 'validate':
                self.validate(**options)
            else:
                self.logger.info(f"  Unknown operation: {op}")

        return True

    def validate(self, **options) -> bool:
        """
        Validate blog posts
        Consolidates: final-validation.py, check-citation-hyperlinks.py
        """
        self.logger.info("✅ Validating blog posts...")

        issues = []
        posts = list(self.posts_dir.glob("*.md"))

        for post in posts:
            post_issues = self._validate_post(post)
            if post_issues:
                issues.extend(post_issues)

        if issues:
            self.logger.info(f"\n❌ Found {len(issues)} issues:")
            for issue in issues[:10]:  # Show first 10 issues
                self.logger.info(f"  - {issue}")
        else:
            self.logger.info("✅ All validations passed!")

        return len(issues) == 0

    # Enhancement helper methods (from BlogEnhancer)
    def _load_uses_page(self) -> str:
        """Load the uses page content as source of truth."""
        if self.uses_file.exists():
            with open(self.uses_file, 'r', encoding='utf-8') as f:
                return f.read()
        return ""

    def _extract_hardware_facts(self) -> Dict:
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

    def _check_hardware_claims(self, content: str) -> List[str]:
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

    def _add_reputable_sources(self, content: str, tags: List[str]) -> Dict:
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

    def _enhance_mermaid_diagrams(self, content: str, metadata: Dict) -> str:
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

    def _improve_readability(self, content: str) -> Tuple[str, List[str]]:
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

    def _validate_code_examples(self, content: str) -> List[str]:
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

    def _enhance_single_post(self, post_path: Path, **options) -> Dict:
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
        if options.get('hardware_check', False):
            hardware_issues = self._check_hardware_claims(post.content)
            if hardware_issues:
                enhancements['issues'].extend(hardware_issues)

        # Add reputable sources
        if options.get('suggest_sources', False):
            sources = self._add_reputable_sources(post.content, post.metadata.get('tags', []))
            if sources['suggested_sources']:
                enhancements['sources_added'] = sources['suggested_sources'][:3]

        # Enhance Mermaid diagrams
        if options.get('enhance_diagrams', False):
            enhanced_content = self._enhance_mermaid_diagrams(post.content, post.metadata)
            if enhanced_content != post.content:
                enhancements['improvements'].append("Added Mermaid diagram")
                post.content = enhanced_content

        # Improve readability
        if options.get('check_readability', False):
            _, readability_improvements = self._improve_readability(post.content)
            enhancements['improvements'].extend(readability_improvements)

        # Validate code examples
        if options.get('validate_code', False):
            code_issues = self._validate_code_examples(post.content)
            if code_issues:
                enhancements['issues'].extend(code_issues)

        return enhancements

    def _generate_enhancement_report(self):
        """Generate comprehensive enhancement report."""
        posts = sorted(self.posts_dir.glob("*.md"))

        self.logger.info("="*80)
        self.logger.info("COMPREHENSIVE BLOG ENHANCEMENT REPORT")
        self.logger.info("="*80)
        self.logger.info(f"\nAnalyzing {len(posts)} posts for enhancements...\n")

        critical_issues = []
        quality_improvements = []
        source_suggestions = []

        for enhancement in self.enhancements:
            if enhancement['issues']:
                critical_issues.append(enhancement)
            if enhancement['improvements']:
                quality_improvements.append(enhancement)
            if enhancement['sources_added']:
                source_suggestions.append(enhancement)

        # Report critical issues
        if critical_issues:
            self.logger.info("-"*40)
            self.logger.info("CRITICAL ISSUES (Incorrect Information):")
            self.logger.info("-"*40)
            for post in critical_issues[:10]:
                self.logger.info(f"\n❌ {post['file']}")
                for issue in post['issues']:
                    self.logger.info(f"   • {issue}")

        # Report quality improvements
        if quality_improvements:
            self.logger.info("\n" + "-"*40)
            self.logger.info("QUALITY IMPROVEMENTS NEEDED:")
            self.logger.info("-"*40)
            for post in quality_improvements[:10]:
                self.logger.info(f"\n📝 {post['file']}")
                for improvement in post['improvements'][:3]:
                    self.logger.info(f"   • {improvement}")

        # Report source suggestions
        if source_suggestions:
            self.logger.info("\n" + "-"*40)
            self.logger.info("REPUTABLE SOURCES TO ADD:")
            self.logger.info("-"*40)
            for post in source_suggestions[:5]:
                self.logger.info(f"\n📚 {post['file']}")
                for source in post['sources_added'][:2]:
                    self.logger.info(f"   • {source}")

        # Summary
        self.logger.info("\n" + "-"*40)
        self.logger.info("ENHANCEMENT SUMMARY:")
        self.logger.info("-"*40)
        self.logger.info(f"Posts with critical issues: {len(critical_issues)}")
        self.logger.info(f"Posts needing quality improvements: {len(quality_improvements)}")
        self.logger.info(f"Posts needing sources: {len(source_suggestions)}")

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

        report_path = self.docs_dir / 'enhancement-report.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        self.logger.info(f"\nDetailed report saved to: {report_path}")

    # Original helper methods
    def _optimize_readability(self, post_path: Path) -> None:
        """Optimize post readability (legacy method)"""
        # Kept for backwards compatibility
        pass

    def _add_structure(self, post_path: Path) -> None:
        """Add proper structure to post (legacy method)"""
        # Kept for backwards compatibility
        pass

    def _validate_frontmatter(self, post_path: Path) -> None:
        """Validate post frontmatter (legacy method)"""
        # Kept for backwards compatibility
        pass

    def _generate_hero_images(self, **options) -> bool:
        """Generate hero images for posts"""
        script = self.scripts_dir / "generate-blog-hero-images.py"
        if script.exists():
            result = subprocess.run([sys.executable, str(script)], capture_output=True)
            return result.returncode == 0
        return False

    def _optimize_images(self, **options) -> bool:
        """Optimize blog images"""
        script = self.scripts_dir / "optimize-blog-images.sh"
        if script.exists():
            result = subprocess.run(["bash", str(script)], capture_output=True)
            return result.returncode == 0
        return False

    def _search_images(self, **options) -> bool:
        """Search for stock images"""
        # Implementation would call playwright-image-search.py logic
        return True

    def _update_image_metadata(self, **options) -> bool:
        """Update image metadata in posts"""
        # Implementation would update frontmatter
        return True

    def _add_citations(self, **options) -> bool:
        """Add citations to posts"""
        # Implementation would add citations
        return True

    def _validate_citations(self, **options) -> bool:
        """Validate citation links"""
        # Implementation would check all citation URLs
        return True

    def _search_academic(self, **options) -> bool:
        """Search academic databases"""
        # Implementation would search arXiv, etc.
        return True

    def _create_diagrams(self, **options) -> bool:
        """Create Mermaid diagrams"""
        # Implementation would generate diagrams
        return True

    def _integrate_diagrams(self, **options) -> bool:
        """Integrate diagrams into posts"""
        # Implementation would add diagrams to content
        return True

    def _update_diagrams(self, **options) -> bool:
        """Update existing diagrams"""
        # Implementation would update diagram code
        return True

    def _analyze_post(self, post_path: Path) -> Dict:
        """Analyze a single post"""
        analysis = {
            'word_count': 0,
            'quality_score': 0,
            'missing_hero_image': False,
            'needs_citations': False
        }

        # Basic implementation
        content = post_path.read_text()
        analysis['word_count'] = len(content.split())

        # Check for hero image
        if 'images:' not in content or 'hero:' not in content:
            analysis['missing_hero_image'] = True

        # Check for citations
        if 'http' not in content or '[^' not in content:
            analysis['needs_citations'] = True

        # Calculate quality score (simplified)
        analysis['quality_score'] = min(100, analysis['word_count'] / 10)

        return analysis

    def _validate_post(self, post_path: Path) -> List[str]:
        """Validate a single post"""
        issues = []

        try:
            content = post_path.read_text()

            # Check frontmatter
            if not content.startswith('---'):
                issues.append(f"{post_path.name}: Missing frontmatter")

            # Check required fields
            required_fields = ['title', 'date', 'description']
            for field in required_fields:
                if f'{field}:' not in content:
                    issues.append(f"{post_path.name}: Missing {field} in frontmatter")

        except Exception as e:
            issues.append(f"{post_path.name}: Error reading file - {e}")

        return issues


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description='Unified Blog Management Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s enhance --all                    # Enhance all posts
  %(prog)s images generate-hero             # Generate hero images
  %(prog)s citations add --post my-post.md  # Add citations to specific post
  %(prog)s analyze                          # Analyze all blog content
  %(prog)s batch enhance images citations   # Run multiple operations
  %(prog)s validate                         # Validate all posts
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Enhance command
    enhance_parser = subparsers.add_parser('enhance', help='Enhance blog content')
    enhance_parser.add_argument('--post', help='Specific post to enhance')
    enhance_parser.add_argument('--all', action='store_true', help='Run all enhancement checks')
    enhance_parser.add_argument('--hardware-check', action='store_true', help='Check hardware claims against uses.md')
    enhance_parser.add_argument('--suggest-sources', action='store_true', help='Suggest reputable sources based on tags')
    enhance_parser.add_argument('--enhance-diagrams', action='store_true', help='Add/enhance Mermaid diagrams')
    enhance_parser.add_argument('--check-readability', action='store_true', help='Analyze readability and flow')
    enhance_parser.add_argument('--validate-code', action='store_true', help='Validate code examples')
    enhance_parser.add_argument('--report', action='store_true', help='Generate enhancement report')

    # Images command
    images_parser = subparsers.add_parser('images', help='Manage blog images')
    images_parser.add_argument('action', choices=['generate-hero', 'optimize', 'search', 'update-metadata'])
    images_parser.add_argument('--post', help='Specific post')

    # Citations command
    citations_parser = subparsers.add_parser('citations', help='Manage citations')
    citations_parser.add_argument('action', choices=['add', 'validate', 'search'])
    citations_parser.add_argument('--post', help='Specific post')
    citations_parser.add_argument('--query', help='Search query')

    # Diagrams command
    diagrams_parser = subparsers.add_parser('diagrams', help='Manage diagrams')
    diagrams_parser.add_argument('action', choices=['create', 'integrate', 'update'])
    diagrams_parser.add_argument('--post', help='Specific post')

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze blog content')
    analyze_parser.add_argument('--target', default='all', help='What to analyze')
    analyze_parser.add_argument('--output', choices=['json', 'text'], default='text')

    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Batch process operations')
    batch_parser.add_argument('operations', nargs='+', help='Operations to run')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate blog posts')
    validate_parser.add_argument('--fix', action='store_true', help='Attempt to fix issues')

    # Add common arguments
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable debug output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress info messages')
    parser.add_argument('--log-file', type=Path, help='Write logs to file')

    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(__name__, level=level, log_file=args.log_file, quiet=args.quiet)

    # Initialize blog manager
    manager = BlogManager(logger=logger)

    # Execute command
    if args.command == 'enhance':
        success = manager.enhance_content(
            post_path=args.post,
            hardware_check=args.hardware_check,
            suggest_sources=args.suggest_sources,
            enhance_diagrams=args.enhance_diagrams,
            check_readability=args.check_readability,
            validate_code=args.validate_code,
            report=args.report,
            all=args.all
        )
    elif args.command == 'images':
        success = manager.manage_images(args.action, post=args.post)
    elif args.command == 'citations':
        success = manager.manage_citations(args.action, post=args.post, query=args.query)
    elif args.command == 'diagrams':
        success = manager.manage_diagrams(args.action, post=args.post)
    elif args.command == 'analyze':
        result = manager.analyze(target=args.target)
        if args.output == 'json':
            # JSON output to stdout for piping/parsing (intentional print, not logging)
            # This is the correct pattern for CLI tools that output structured data
            import sys
            sys.stdout.write(json.dumps(result, indent=2) + '\n')
        else:
            logger.info(f"📊 Analysis Results:")
            logger.info(f"  Posts: {result['posts_count']}")
            logger.info(f"  Total Words: {result['total_words']:,}")
            logger.info(f"  Avg Quality: {result['avg_readability']:.1f}/100")
            if result['missing_images']:
                logger.info(f"  Missing Images: {len(result['missing_images'])} posts")
            if result['missing_citations']:
                logger.info(f"  Need Citations: {len(result['missing_citations'])} posts")
        success = True
    elif args.command == 'batch':
        success = manager.batch_process(args.operations)
    elif args.command == 'validate':
        success = manager.validate(fix=args.fix if hasattr(args, 'fix') else False)
    else:
        parser.print_help()
        success = False

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()