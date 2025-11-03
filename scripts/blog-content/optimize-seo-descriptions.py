#!/usr/bin/env -S uv run python3
"""
SCRIPT: optimize-seo-descriptions.py
PURPOSE: SEO Meta Description Optimizer
CATEGORY: blog_content
LLM_READY: True
VERSION: 1.1.0
UPDATED: 2025-11-02T14:30:00-05:00

DESCRIPTION:
    Automatically optimizes blog post meta descriptions to the 120-160 character
    range (with 150-160 being optimal) while preserving voice, keywords, and meaning.
    Now uses centralized logging configuration from scripts/lib/logging_config.py.

LLM_USAGE:
    python scripts/blog-content/optimize-seo-descriptions.py [options]

ARGUMENTS:
    --verbose, -v: Enable debug output
    --quiet, -q: Suppress info messages
    --log-file: Write logs to file

EXAMPLES:
    # Basic usage
    python scripts/blog-content/optimize-seo-descriptions.py

    # With verbose logging
    python scripts/blog-content/optimize-seo-descriptions.py --verbose

    # Write logs to file
    python scripts/blog-content/optimize-seo-descriptions.py --log-file logs/seo-optimizer.log

OUTPUT:
    - Updated blog posts with optimized meta descriptions
    - JSON report in docs/reports/seo-optimization-{date}.json
    - Statistics summary

DEPENDENCIES:
    - Python 3.8+
    - PyYAML for frontmatter parsing
    - scripts/lib/logging_config.py for centralized logging

RELATED_SCRIPTS:
    - scripts/blog-content/analyze-blog-content.py: Content analysis
    - scripts/blog-content/metadata-validator.py: Metadata validation

MANIFEST_REGISTRY: scripts/blog-content/optimize-seo-descriptions.py
"""

import os
import re
import json
import yaml
import sys
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Add lib directory to path for logging_config
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.logging_config import setup_logger

# Configuration
POSTS_DIR = Path("src/posts")
REPORT_DIR = Path("docs/reports")
MIN_CHARS = 120
OPTIMAL_MIN = 150
OPTIMAL_MAX = 160
MAX_CHARS = 160


# Manual optimizations for all 44 posts requiring fixes
MANUAL_OPTIMIZATIONS = {
    # Critical (190+  chars) - 9 posts
    "2025-10-13-embodied-ai-robots-physical-world.md":
        "Vision-Language-Action models transform AI from code into physical robots, with practical implications for security, safety, and homelab automation",

    "2025-08-09-ai-cognitive-infrastructure.md":
        "AI is evolving from tools into cognitive infrastructure that shapes how billions think, yet we understand little about its long-term effects",

    "2024-10-22-ai-edge-computing.md":
        "How AI and edge computing create responsive, private systems that process data locally, revolutionizing autonomous vehicles and smart manufacturing",

    "2024-10-10-blockchain-beyond-cryptocurrency.md":
        "Running Ethereum nodes on my homelab taught me blockchain is about building trust without central authorities. Here's what works (and doesn't)",

    "2024-11-05-pizza-calculator.md":
        "How quantifying pizza provisioning enhances team performance during high-pressure development, combining resource planning and behavioral economics",

    "2025-10-17-progressive-context-loading-llm-workflows.md":
        "Progressive skill loading achieves 98% token reduction in LLM workflows through modular context architecture—lessons from building production systems",

    "2024-06-11-beyond-containers-future-deployment.md":
        "After migrating 23 services to Kubernetes and debugging for weeks, I explored what comes after containers. Spoiler: I broke things",

    "2024-03-05-cloud-migration-journey-guide.md":
        "Our cloud migration taught me as much about change management as technology. Lessons from moving from physical servers to the cloud",

    "2024-07-16-sustainable-computing-carbon-footprint.md":
        "ML training consuming as much electricity as a small town sparked my journey into sustainable computing—efficiency as environmental imperative",

    # High (180-189 chars) - 10 posts
    "2024-08-27-zero-trust-security-principles.md":
        "Zero trust security assumes breach and verifies everything. My journey implementing these principles in a homelab environment with practical examples",

    "2024-09-19-biomimetic-robotics.md":
        "How nature's 3.8 billion years of R&D inspires robot design—from gecko feet to swarm intelligence, exploring biomimetic principles in modern robotics",

    "2024-06-25-designing-resilient-systems.md":
        "Building systems that gracefully handle failures through redundancy, circuit breakers, and chaos engineering—lessons from production incidents",

    "2024-07-09-zero-trust-architecture-implementation.md":
        "Practical guide to implementing zero trust architecture: identity verification, micro-segmentation, and continuous monitoring for modern security",

    "2025-09-08-zero-trust-vlan-segmentation-homelab.md":
        "How I implemented zero trust principles using VLAN segmentation on my homelab—practical network security beyond simple firewall rules",

    "2024-02-22-open-source-vs-proprietary-llms.md":
        "Running both Llama and GPT-4 in my homelab taught me the real trade-offs between open-source and proprietary LLMs beyond hype and marketing",

    "2025-08-07-supercharging-development-claude-flow.md":
        "Claude-Flow orchestrates AI agent swarms for development—84.8% SWE-Bench solve rate with neural learning. Here's my experience building with it",

    "2025-05-10-llm-fine-tuning-homelab-guide.md":
        "Complete guide to fine-tuning open-source LLMs on homelab hardware using QLoRA, covering dataset prep, training optimization, and evaluation",

    "2024-10-03-quantum-computing-defense.md":
        "Quantum computers will break current encryption within years. Here's how I'm preparing with post-quantum cryptography and quantum-resistant algorithms",

    "2024-12-03-context-windows-llms.md":
        "From 2K to 2M tokens—how expanding context windows transform LLMs from chatbots to reasoning engines, with practical implications for applications",

    # Medium (170-179 chars) - 11 posts
    "2024-01-08-writing-secure-code-developers-guide.md":
        "Practical guide to writing secure code from the start: input validation, parameterized queries, secrets management, and secure architecture patterns",

    "2024-01-18-demystifying-cryptography-beginners-guide.md":
        "Breaking down cryptography fundamentals—symmetric/asymmetric encryption, hashing, digital signatures—with practical examples and implementation guidance",

    "2024-02-09-deepfake-dilemma-ai-deception.md":
        "AI-generated deepfakes threaten truth itself. Exploring detection techniques, authentication methods, and the arms race between creation and detection",

    "2024-08-13-high-performance-computing.md":
        "High-performance computing brings supercomputer capabilities to research and industry—parallel processing, distributed systems, and optimization strategies",

    "2024-09-09-embodied-ai-teaching-agents.md":
        "Training AI agents to learn from physical interaction with the world, combining vision, language, and action for robots that adapt to real environments",

    "2025-06-25-local-llm-deployment-privacy-first.md":
        "Complete guide to running LLMs locally for privacy: hardware requirements, model selection, optimization techniques, and practical deployment strategies",

    "2025-09-29-proxmox-high-availability-homelab.md":
        "Building high-availability Proxmox clusters on homelab hardware—shared storage, live migration, automated failover, and lessons from three failed attempts",

    "2025-09-01-self-hosted-bitwarden-migration-guide.md":
        "Migrating from cloud password managers to self-hosted Bitwarden: setup, security hardening, backup strategies, and why I made the switch",

    "2025-08-25-network-traffic-analysis-suricata-homelab.md":
        "Setting up Suricata IDS/IPS on homelab for real-time network threat detection—rule management, performance tuning, and integrating with security stack",

    "2024-11-19-llms-smart-contract-vulnerability.md":
        "Can LLMs detect smart contract vulnerabilities? Testing GPT-4 and Claude against known exploits with surprising results and security implications",

    "2024-04-30-quantum-resistant-cryptography-guide.md":
        "Quantum computers threaten today's encryption. Implementing NIST's post-quantum cryptographic algorithms to future-proof security infrastructure",

    # Low (160-169 chars) - 11 posts
    "2024-05-14-ai-new-frontier-cybersecurity.md":
        "AI revolutionizes both attack and defense in cybersecurity—from automated threat detection to AI-powered exploits. Exploring the evolving battleground",

    "2024-05-30-ai-learning-resource-constrained.md":
        "Training effective AI models with limited compute—techniques like quantization, pruning, distillation, and efficient architectures for resource constraints",

    "2024-07-24-multimodal-foundation-models.md":
        "Foundation models that understand text, images, and audio together—architecture, capabilities, and applications beyond single-modality systems",

    "2025-09-20-vulnerability-prioritization-epss-kev.md":
        "Moving beyond CVSS scores to prioritize vulnerabilities using EPSS probability metrics and CISA KEV catalog for risk-based patch management",

    "2025-10-06-automated-security-scanning-pipeline.md":
        "Building automated security scanning pipelines with Grype, OSV, and Trivy—CI/CD integration, vulnerability tracking, and actionable reporting",

    "2024-01-30-securing-cloud-native-frontier.md":
        "Securing cloud-native environments requires new approaches—container security, service mesh, secrets management, and zero trust for microservices",

    "2024-08-02-quantum-computing-leap-forward.md":
        "Recent quantum computing breakthroughs bring us closer to practical quantum advantage—algorithm development, error correction, and real applications",

    "2024-04-11-ethics-large-language-models.md":
        "Ethical implications of LLMs—bias, misinformation, privacy, and accountability. Exploring responsible AI development and deployment frameworks",

    "2024-04-19-mastering-prompt-engineering-llms.md":
        "Effective prompt engineering techniques for LLMs—few-shot learning, chain-of-thought, system prompts, and strategies for reliable outputs",

    "2025-10-29-post-quantum-cryptography-homelab.md":
        "Preparing my homelab for the quantum threat with NIST's post-quantum algorithms—CRYSTALS-Kyber, CRYSTALS-Dilithium, and practical implementation lessons",

    "2024-11-15-gpu-power-monitoring-homelab-ml.md":
        "Monitoring GPU power consumption during ML training with NVIDIA SMI, custom dashboards, and optimization strategies to reduce electricity costs",

    # Acceptable (120-149 chars) - Need to expand to 150-160 - 9 posts
    "2025-09-20-iot-security-homelab-owasp.md":
        "Explore IoT security vulnerabilities hands-on with OWASP IoTGoat—testing firmware extraction, API exploitation, and building secure IoT lab environments",

    "2025-03-10-raspberry-pi-security-projects.md":
        "From network monitoring to physical security—practical Raspberry Pi security projects like Pi-hole, VPN gateway, and honeypots without breaking the bank",

    "2025-07-01-ebpf-security-monitoring-practical-guide.md":
        "Using eBPF for real-time Linux security monitoring—syscall tracking, network observability, and production-ready patterns for kernel-level visibility",

    "2025-07-08-implementing-dns-over-https-home-networks.md":
        "Complete guide to deploying DNS-over-HTTPS on home networks for privacy and security, covering Pi-hole, dnscrypt-proxy, and multiple implementation approaches",

    "2025-07-22-supercharging-claude-cli-with-standards.md":
        "How I built a standards repository that transforms Claude CLI into a context-aware development powerhouse with 90% token reduction and workflow automation",

    "2025-07-29-building-mcp-standards-server.md":
        "The ongoing saga of turning my standards repo into an MCP server for Claude. Spoiler: It's working mostly, and I've only rewritten it three times so far",

    "2025-04-24-building-secure-homelab-adventure.md":
        "How I built a comprehensive security lab at home for learning and experimentation—covering Proxmox, VLANs, IDS/IPS, and keeping my family's data safe",

    "2025-03-24-from-it-support-to-senior-infosec-engineer.md":
        "The winding path from fixing printers to securing federal systems over 10 years—lessons learned, mistakes made, and advice for aspiring security professionals",

    "welcome.md":
        "Why I chose Eleventy for my personal site and the journey of building a fast, accessible, privacy-respecting digital home with modern web technologies",

    # Too short (<120 chars) - Need to expand - 3 posts
    "2025-04-10-securing-personal-ai-experiments.md":
        "Lessons from running LLMs and AI experiments at home while keeping data secure, covering model isolation, network segmentation, and privacy controls",

    "2025-02-24-continuous-learning-cybersecurity.md":
        "How I stay current in a field that changes daily—practical strategies including lab exercises, research tracking, and community engagement without burnout",

    "2025-02-10-automating-home-network-security.md":
        "Automation scripts and tools I built to keep my home network secure, including Ansible playbooks, Python monitors, and automated patching systems",
}


class DescriptionOptimizer:
    """Optimizes blog post meta descriptions for SEO."""

    def __init__(self, logger=None):
        self.posts_dir = POSTS_DIR
        self.report_dir = REPORT_DIR
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.results = []
        self.stats = {
            "processed": 0,
            "updated": 0,
            "skipped": 0,
            "errors": 0
        }
        self.logger = logger or logging.getLogger(__name__)

    def extract_frontmatter(self, content: str) -> Tuple[Optional[Dict], str, str]:
        """Extract YAML frontmatter from markdown content."""
        pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
        match = re.match(pattern, content, re.DOTALL)

        if not match:
            return None, "", content

        frontmatter_text = match.group(1)
        body = match.group(2)

        # Parse YAML frontmatter properly
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            if frontmatter is None:
                frontmatter = {}
        except yaml.YAMLError as e:
            if self.logger:
                self.logger.warning(f"YAML parse error: {e}")
            return None, frontmatter_text, body

        return frontmatter, frontmatter_text, body

    def process_post(self, filepath: Path) -> bool:
        """Process a single blog post and optimize its description."""
        try:
            # Check if this file needs optimization
            if filepath.name not in MANUAL_OPTIMIZATIONS:
                return False

            # Read file
            content = filepath.read_text(encoding='utf-8')
            frontmatter, frontmatter_text, body = self.extract_frontmatter(content)

            if not frontmatter or 'description' not in frontmatter:
                self.logger.warning(f"Skipping {filepath.name}: No description found")
                self.stats["skipped"] += 1
                return False

            current_desc = frontmatter['description']
            current_len = len(current_desc)

            # Get optimized description
            optimized_desc = MANUAL_OPTIMIZATIONS[filepath.name]
            optimized_len = len(optimized_desc)

            # Check if already optimal
            if current_desc == optimized_desc:
                self.logger.info(f"Skipping {filepath.name}: Already optimized ({current_len} chars)")
                self.stats["skipped"] += 1
                return False

            # Update frontmatter in dictionary
            frontmatter['description'] = optimized_desc

            # Serialize back to YAML (preserve order)
            new_frontmatter_text = yaml.dump(
                frontmatter,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
                width=1000  # Prevent line wrapping
            )

            # Reconstruct file
            new_content = f"---\n{new_frontmatter_text}---\n{body}"

            # Write back
            filepath.write_text(new_content, encoding='utf-8')

            # Determine status
            if OPTIMAL_MIN <= optimized_len <= OPTIMAL_MAX:
                status = "optimal"
                status_emoji = "✅"
            elif MIN_CHARS <= optimized_len <= MAX_CHARS:
                status = "acceptable"
                status_emoji = "✅"
            elif optimized_len < MIN_CHARS:
                status = "too_short"
                status_emoji = "⚠️"
            else:
                status = "too_long"
                status_emoji = "⚠️"

            # Record result
            result = {
                "file": filepath.name,
                "before": current_desc,
                "after": optimized_desc,
                "before_length": current_len,
                "after_length": optimized_len,
                "change": optimized_len - current_len,
                "status": status
            }
            self.results.append(result)

            self.logger.info(f"Updated {filepath.name}: {current_len} → {optimized_len} chars ({status})")

            self.stats["processed"] += 1
            self.stats["updated"] += 1
            return True

        except Exception as e:
            self.logger.error(f"Error processing {filepath.name}: {e}")
            self.stats["errors"] += 1
            return False

    def generate_report(self):
        """Generate comprehensive optimization report."""
        timestamp = datetime.now().isoformat()

        # Calculate statistics
        total_before = sum(r['before_length'] for r in self.results)
        total_after = sum(r['after_length'] for r in self.results)
        avg_before = total_before / len(self.results) if self.results else 0
        avg_after = total_after / len(self.results) if self.results else 0

        status_counts = {
            "optimal": len([r for r in self.results if r['status'] == 'optimal']),
            "acceptable": len([r for r in self.results if r['status'] == 'acceptable']),
            "too_short": len([r for r in self.results if r['status'] == 'too_short']),
            "too_long": len([r for r in self.results if r['status'] == 'too_long'])
        }

        report = {
            "timestamp": timestamp,
            "summary": {
                "total_posts": self.stats["processed"],
                "updated": self.stats["updated"],
                "skipped": self.stats["skipped"],
                "errors": self.stats["errors"],
                "avg_length_before": round(avg_before, 1),
                "avg_length_after": round(avg_after, 1),
                "avg_reduction": round(avg_before - avg_after, 1),
                "status_distribution": status_counts
            },
            "results": self.results
        }

        # Write JSON report
        report_file = self.report_dir / f"seo-optimization-{datetime.now().strftime('%Y-%m-%d')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        self.logger.info(f"Report saved to: {report_file}")

        return report

    def print_summary(self, report: Dict):
        """Print summary statistics."""
        summary = report['summary']

        self.logger.info("\n" + "="*70)
        self.logger.info("SEO META DESCRIPTION OPTIMIZATION SUMMARY")
        self.logger.info("="*70)
        self.logger.info(f"\n📈 Processing Statistics:")
        self.logger.info(f"   Total posts processed: {summary['total_posts']}")
        self.logger.info(f"   Successfully updated: {summary['updated']}")
        self.logger.info(f"   Skipped (already optimal): {summary['skipped']}")
        self.logger.info(f"   Errors: {summary['errors']}")

        self.logger.info(f"\n📏 Length Statistics:")
        self.logger.info(f"   Average before: {summary['avg_length_before']:.1f} chars")
        self.logger.info(f"   Average after: {summary['avg_length_after']:.1f} chars")
        self.logger.info(f"   Average change: {summary['avg_reduction']:.1f} chars")

        self.logger.info(f"\n🎯 Status Distribution:")
        status = summary['status_distribution']
        self.logger.info(f"   Optimal (150-160): {status['optimal']}")
        self.logger.info(f"   Acceptable (120-160): {status['acceptable']}")
        self.logger.info(f"   Too short (<120): {status['too_short']}")
        self.logger.info(f"   Too long (>160): {status['too_long']}")

        self.logger.info("\n" + "="*70)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='Optimize SEO Meta Descriptions')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable debug output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress info messages')
    parser.add_argument('--log-file', type=Path, help='Write logs to file')
    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(__name__, level=level, log_file=args.log_file, quiet=args.quiet)

    logger.info("Starting SEO Meta Description Optimization")
    logger.info("="*70)

    optimizer = DescriptionOptimizer(logger=logger)

    # Get all markdown files
    post_files = sorted(POSTS_DIR.glob("*.md"))
    logger.info(f"Found {len(post_files)} blog posts")
    logger.info(f"Targeting {len(MANUAL_OPTIMIZATIONS)} posts for optimization")

    # Process each post
    for filepath in post_files:
        optimizer.process_post(filepath)

    # Generate report
    if optimizer.results:
        report = optimizer.generate_report()
        optimizer.print_summary(report)

    logger.info("Optimization complete!")
    logger.info(f"Updated {optimizer.stats['updated']} posts")
    logger.info(f"Skipped {optimizer.stats['skipped']} posts (already optimal)")
    logger.info(f"Errors: {optimizer.stats['errors']}")

    return 0 if optimizer.stats['errors'] == 0 else 1


if __name__ == "__main__":
    exit(main())
