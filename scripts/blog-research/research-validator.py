#!/usr/bin/env -S uv run python3
"""
SCRIPT: research-validator.py
PURPOSE: Research Validator - Ensures all blog post claims are backed by reputable sources
CATEGORY: academic_research
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T15:08:08-04:00

DESCRIPTION:
    Research Validator - Ensures all blog post claims are backed by reputable sources. This script is part of the academic research
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/research-validator.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/research-validator.py

    # With verbose output
    python scripts/research-validator.py --verbose

OUTPUT:
    - Processed results based on script functionality
    - Log messages if verbose mode enabled

DEPENDENCIES:
    - Python 3.8+
    - See imports for specific package requirements
    - scripts/lib/common.py for shared utilities (if applicable)

RELATED_SCRIPTS:
    - scripts/lib/common.py: Shared utilities
    - [Other related scripts in academic_research category]

MANIFEST_REGISTRY: scripts/research-validator.py
"""

import re
import json
import sys
import logging
import frontmatter
from pathlib import Path
from typing import Dict, List, Tuple
import argparse
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

class ResearchValidator:
    def __init__(self):
        self.claim_patterns = [
            # Statistics and percentages
            (r'\b\d+(?:\.\d+)?%', 'percentage'),
            (r'\b\d+(?:\.\d+)?x\s+(?:faster|slower|better|worse|improvement)', 'multiplier'),
            (r'(?:increased?|decreased?|improved?|reduced?)\s+by\s+\d+', 'metric_change'),
            
            # Absolute statements
            (r'(?:studies show|research (?:shows|indicates|proves))', 'research_claim'),
            (r'(?:scientists|researchers|experts)\s+(?:say|believe|found)', 'expert_claim'),
            (r'according to\s+(?:a\s+)?(?:study|research|report)', 'study_reference'),
            
            # Technical specifications
            (r'\b\d+(?:GB|MB|KB|TB)\b', 'memory_spec'),
            (r'\b\d+(?:GHz|MHz|Hz)\b', 'frequency_spec'),
            (r'\b\d+(?:ms|μs|ns)\s+(?:latency|delay|response)', 'latency_spec'),
            
            # Comparative claims
            (r'(?:better|worse|faster|slower)\s+than', 'comparison'),
            (r'(?:most|least)\s+(?:popular|used|effective)', 'superlative'),
            (r'(?:only|first|last)\s+(?:solution|approach|method)', 'exclusivity'),
        ]
        
        self.citation_patterns = [
            r'\[([^\]]+)\]\(https?://[^\)]+\)',  # Markdown links
            r'\[\d+\]',  # Numbered references
            r'\([A-Z][a-z]+(?:\s+et\s+al\.)?,?\s+\d{4}\)',  # Academic citations
        ]
        
    def extract_claims(self, content: str) -> List[Dict]:
        """Extract all claims that need citation from content."""
        claims = []
        
        for pattern, claim_type in self.claim_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                # Get context (50 chars before and after)
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 50)
                context = content[start:end].strip()
                
                claims.append({
                    'type': claim_type,
                    'text': match.group(),
                    'context': context,
                    'position': match.start()
                })
        
        return claims
    
    def find_citations(self, content: str) -> List[Dict]:
        """Find all existing citations in content."""
        citations = []
        
        for pattern in self.citation_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                citations.append({
                    'text': match.group(),
                    'position': match.start()
                })
        
        return citations
    
    def validate_claim_citations(self, claims: List[Dict], citations: List[Dict]) -> List[Dict]:
        """Check which claims lack proper citations."""
        uncited_claims = []
        
        for claim in claims:
            # Check if there's a citation within 100 characters
            has_citation = False
            for citation in citations:
                if abs(citation['position'] - claim['position']) < 100:
                    has_citation = True
                    break
            
            if not has_citation:
                uncited_claims.append(claim)
        
        return uncited_claims
    
    def check_source_quality(self, url: str) -> Dict:
        """Evaluate the quality of a source URL."""
        quality_indicators = {
            'high': [
                'arxiv.org', 'zenodo.org', 'core.ac.uk', 'doi.org',
                'ieee.org', 'acm.org', 'nature.com', 'science.org',
                'nist.gov', 'owasp.org', 'cve.mitre.org'
            ],
            'medium': [
                'github.com', 'gitlab.com', 'stackoverflow.com',
                'medium.com/@official', 'dev.to', 'hashnode.com'
            ],
            'low': [
                'wikipedia.org', 'reddit.com', 'quora.com',
                'personal-blog', 'medium.com'
            ]
        }
        
        for quality, domains in quality_indicators.items():
            if any(domain in url.lower() for domain in domains):
                return {'quality': quality, 'url': url}
        
        return {'quality': 'unknown', 'url': url}
    
    def validate_post(self, post_path: Path) -> Dict:
        """Validate a single blog post for research integrity."""
        with open(post_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        content = post.content
        claims = self.extract_claims(content)
        citations = self.find_citations(content)
        uncited_claims = self.validate_claim_citations(claims, citations)
        
        # Extract URLs from citations and check quality
        url_pattern = r'https?://[^\s\)\"\'<>]+'
        urls = re.findall(url_pattern, content)
        source_quality = [self.check_source_quality(url) for url in urls]
        
        # Calculate metrics
        total_claims = len(claims)
        cited_claims = total_claims - len(uncited_claims)
        citation_rate = (cited_claims / total_claims * 100) if total_claims > 0 else 100
        
        high_quality_sources = sum(1 for s in source_quality if s['quality'] == 'high')
        low_quality_sources = sum(1 for s in source_quality if s['quality'] == 'low')
        
        return {
            'file': post_path.name,
            'total_claims': total_claims,
            'cited_claims': cited_claims,
            'uncited_claims': len(uncited_claims),
            'citation_rate': citation_rate,
            'total_sources': len(source_quality),
            'high_quality_sources': high_quality_sources,
            'low_quality_sources': low_quality_sources,
            'uncited_details': uncited_claims[:10],  # Top 10 uncited claims
            'recommendations': self.generate_recommendations(
                citation_rate, high_quality_sources, low_quality_sources, uncited_claims
            )
        }
    
    def generate_recommendations(self, citation_rate: float, high_quality: int, 
                                low_quality: int, uncited_claims: List) -> List[str]:
        """Generate specific recommendations for improving research quality."""
        recommendations = []
        
        if citation_rate < 80:
            recommendations.append(f"Add citations for {len(uncited_claims)} uncited claims")
        
        if low_quality > 0:
            recommendations.append(f"Replace {low_quality} low-quality sources with academic sources")
        
        if high_quality < 3:
            recommendations.append("Add more high-quality academic sources (arXiv, Zenodo, etc.)")
        
        # Specific claim type recommendations
        claim_types = set(claim['type'] for claim in uncited_claims)
        if 'percentage' in claim_types:
            recommendations.append("Add sources for all percentage claims")
        if 'research_claim' in claim_types:
            recommendations.append("Cite specific studies when mentioning research")
        if 'technical_spec' in claim_types:
            recommendations.append("Verify technical specifications with official documentation")
        
        return recommendations
    
    def generate_report(self, posts_dir: Path = Path('src/posts'), logger=None):
        """Generate a comprehensive research validation report for all posts."""
        posts = sorted(posts_dir.glob('*.md'))
        results = []

        if logger:
            logger.info("="*80)
            logger.info("BLOG POST RESEARCH VALIDATION REPORT")
            logger.info("="*80)
            logger.info(f"\nAnalyzing {len(posts)} posts for research integrity...\n")

        for post_path in posts:
            result = self.validate_post(post_path)
            results.append(result)

            # Print summary for posts needing attention
            if result['citation_rate'] < 80 or result['low_quality_sources'] > 0:
                if logger:
                    logger.info(f"\n⚠️  {result['file']}")
                    logger.info(f"   Citation Rate: {result['citation_rate']:.1f}%")
                    logger.info(f"   Uncited Claims: {result['uncited_claims']}")
                    if result['low_quality_sources'] > 0:
                        logger.info(f"   Low Quality Sources: {result['low_quality_sources']}")
                    for rec in result['recommendations'][:3]:
                        logger.info(f"   • {rec}")

        # Overall statistics
        avg_citation_rate = sum(r['citation_rate'] for r in results) / len(results)
        total_uncited = sum(r['uncited_claims'] for r in results)
        posts_needing_work = sum(1 for r in results if r['citation_rate'] < 80)

        if logger:
            logger.info("\n" + "="*80)
            logger.info("OVERALL STATISTICS")
            logger.info("="*80)
            logger.info(f"Average Citation Rate: {avg_citation_rate:.1f}%")
            logger.info(f"Total Uncited Claims: {total_uncited}")
            logger.info(f"Posts Needing Citations: {posts_needing_work}/{len(posts)}")

        # Save detailed report
        report = {
            'generated': datetime.now().isoformat(),
            'summary': {
                'total_posts': len(posts),
                'average_citation_rate': avg_citation_rate,
                'total_uncited_claims': total_uncited,
                'posts_needing_work': posts_needing_work
            },
            'posts': results
        }

        with open('docs/research-validation-report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)

        if logger:
            logger.info(f"\nDetailed report saved to: docs/research-validation-report.json")

        return results

def main():
    parser = argparse.ArgumentParser(
        description='Validate research citations in blog posts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate all posts
  python scripts/blog-research/research-validator.py

  # Validate specific post
  python scripts/blog-research/research-validator.py --post 2024-01-01-example

  # Check all claims
  python scripts/blog-research/research-validator.py --check-claims

  # Quiet mode
  python scripts/blog-research/research-validator.py --quiet
        """
    )
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('--post', help='Specific post to validate')
    parser.add_argument('--check-claims', action='store_true', help='Check all claims')
    parser.add_argument('--fix', action='store_true', help='Suggest fixes for uncited claims')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable debug output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress output messages')
    parser.add_argument('--log-file', type=Path, help='Write logs to file')

    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(__name__, level=level, log_file=args.log_file, quiet=args.quiet)

    try:
        validator = ResearchValidator()

        if args.post:
            post_path = Path(f'src/posts/{args.post}.md')
            if not post_path.exists():
                logger.error(f"❌ Error: Post not found: {post_path}")
                return 1
            result = validator.validate_post(post_path)
            if not args.quiet:
                logger.info(json.dumps(result, indent=2))
        else:
            validator.generate_report(logger=logger)

        return 0

    except FileNotFoundError as e:
        logger.error(f"❌ Error: File not found - {e}")
        return 1
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return 2

if __name__ == "__main__":
    import sys
    sys.exit(main())