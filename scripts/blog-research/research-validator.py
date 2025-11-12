#!/usr/bin/env -S uv run python3
"""
SCRIPT: research-validator.py
PURPOSE: Research Validator - Ensures all blog post claims are backed by reputable sources
CATEGORY: academic_research
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-11-11T12:55:00-05:00

DESCRIPTION:
    Research Validator - Ensures all blog post claims are backed by reputable sources.

    v2.0.0 NEW FEATURES:
    - DOI format normalization (5 patterns to canonical HTTPS format)
    - Duplicate citation detection (DOI/arXiv across posts)
    - Enhanced CLI with --normalize-dois, --detect-duplicates, --dry-run

    This script is part of the academic research category and provides automated
    functionality for the static site.

LLM_USAGE:
    # Normalize DOI formats (dry-run)
    python scripts/blog-research/research-validator.py --normalize-dois --dry-run --batch

    # Apply DOI normalization
    python scripts/blog-research/research-validator.py --normalize-dois --batch

    # Detect duplicate citations
    python scripts/blog-research/research-validator.py --detect-duplicates

    # Validate specific post
    python scripts/blog-research/research-validator.py --post [filename]

ARGUMENTS:
    --normalize-dois: Normalize DOI citations to canonical HTTPS format
    --detect-duplicates: Detect duplicate citations across posts
    --dry-run: Preview changes without writing files
    --batch: Process all posts with citations
    --post: Specific post to process
    --verbose: Enable verbose output
    --quiet: Suppress output messages
    --log-file: Write logs to file

EXAMPLES:
    # Basic validation (all posts)
    python scripts/blog-research/research-validator.py

    # Normalize DOIs in all posts
    python scripts/blog-research/research-validator.py --normalize-dois --batch

    # Check for duplicate citations
    python scripts/blog-research/research-validator.py --detect-duplicates

    # Normalize specific post (dry-run)
    python scripts/blog-research/research-validator.py --normalize-dois --dry-run --post 2024-03-20-transformer-architecture-deep-dive

OUTPUT:
    - Citation validation results
    - DOI normalization summary
    - Duplicate citation report
    - Log messages if verbose mode enabled

DEPENDENCIES:
    - Python 3.8+
    - frontmatter
    - scripts/lib/logging_config.py

RELATED_SCRIPTS:
    - scripts/lib/logging_config.py: Centralized logging
    - scripts/blog-research/citation-analyzer.py: Citation analysis

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


# ============================================================================
# v2.0.0: Citation Enhancement Functions
# ============================================================================

def normalize_doi_format(citation_text: str) -> Tuple[str, int]:
    """Normalize DOI citations to canonical HTTPS URL format.

    Args:
        citation_text: Citation text that may contain DOI

    Returns:
        Tuple of (updated citation text, number of changes made)

    Patterns handled:
        1. http://doi.org/... → https://doi.org/...
        2. DOI: 10.xxxx/... → https://doi.org/10.xxxx/...
        3. doi:10.xxxx/... → https://doi.org/10.xxxx/...
        4. Plain 10.xxxx/... → https://doi.org/10.xxxx/...
        5. dx.doi.org/... → doi.org/... (canonical domain)
    """
    original_text = citation_text
    changes = 0

    # Pattern 1: Upgrade HTTP to HTTPS
    before = citation_text
    citation_text = re.sub(
        r'http://doi\.org/',
        'https://doi.org/',
        citation_text
    )
    if citation_text != before:
        changes += len(re.findall(r'https://doi\.org/', citation_text)) - len(re.findall(r'https://doi\.org/', before))

    # Pattern 2: Convert dx.doi.org to doi.org (canonical)
    before = citation_text
    citation_text = re.sub(
        r'https?://dx\.doi\.org/',
        'https://doi.org/',
        citation_text
    )
    if citation_text != before:
        changes += 1

    # Pattern 3: DOI: prefix format → URL
    before = citation_text
    citation_text = re.sub(
        r'DOI:\s*(10\.\d{4,}/[^\s\)]+)',
        r'https://doi.org/\1',
        citation_text,
        flags=re.IGNORECASE
    )
    if citation_text != before:
        changes += len(re.findall(r'https://doi\.org/10\.', citation_text)) - len(re.findall(r'https://doi\.org/10\.', before))

    # Pattern 4: doi: prefix format → URL
    before = citation_text
    citation_text = re.sub(
        r'doi:\s*(10\.\d{4,}/[^\s\)]+)',
        r'https://doi.org/\1',
        citation_text,
        flags=re.IGNORECASE
    )
    if citation_text != before:
        changes += 1

    # Pattern 5: Bare DOI identifiers (conservative - only in citation contexts)
    # Look for patterns like [123] 10.xxxx/yyyy or (Author 2023) 10.xxxx/yyyy
    before = citation_text
    citation_text = re.sub(
        r'(\[\d+\]|\([^)]+\d{4}\))\s+(10\.\d{4,}/[^\s\)]+)',
        r'\1 https://doi.org/\2',
        citation_text
    )
    if citation_text != before:
        changes += 1

    return citation_text, changes


def process_citations_in_post(
    post_path: str,
    normalize_dois: bool = True,
    dry_run: bool = False,
    logger = None
) -> Dict[str, any]:
    """Process all citations in a post's References section.

    Args:
        post_path: Path to markdown post
        normalize_dois: Apply DOI format normalization
        dry_run: Preview changes without writing
        logger: Logger instance

    Returns:
        Dict with processing results
    """
    if logger is None:
        logger = setup_logger(__name__)

    try:
        with open(post_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        logger.error(f"Failed to read {post_path}: {e}")
        return {'error': str(e)}

    # Find References section
    refs_match = re.search(
        r'(## References|### References)(.*?)(?=^## |\Z)',
        content,
        re.MULTILINE | re.DOTALL
    )

    if not refs_match:
        logger.debug(f"No References section in {Path(post_path).name}")
        return {'has_references': False}

    refs_section = refs_match.group(2)
    original_refs = refs_section

    # Apply normalizations
    changes_made = []
    total_changes = 0

    if normalize_dois:
        normalized_refs, change_count = normalize_doi_format(refs_section)

        if change_count > 0:
            changes_made.append(f"Normalized {change_count} DOI format(s)")
            total_changes += change_count
            refs_section = normalized_refs

    # Count citations
    doi_count = len(re.findall(r'doi\.org/10\.\d{4,}', refs_section))
    arxiv_count = len(re.findall(r'arxiv\.org/abs/\d{4}\.\d{4,}', refs_section))

    # Update content if not dry_run
    if not dry_run and changes_made:
        updated_content = content.replace(original_refs, refs_section)

        try:
            with open(post_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            logger.info(f"✅ Updated citations in {Path(post_path).name}")
        except Exception as e:
            logger.error(f"Failed to write {post_path}: {e}")
            return {'error': str(e)}
    elif dry_run and changes_made:
        logger.info(f"🔍 [DRY RUN] Would update {Path(post_path).name}")

    return {
        'has_references': True,
        'changes_made': changes_made,
        'change_count': total_changes,
        'doi_count': doi_count,
        'arxiv_count': arxiv_count,
        'dry_run': dry_run
    }


def detect_duplicate_citations(posts_with_citations: List[str], logger=None) -> Dict[str, any]:
    """Find duplicate DOI/arXiv citations across posts.

    Args:
        posts_with_citations: List of post paths to check
        logger: Logger instance

    Returns:
        Dict mapping citation identifier to list of posts using it
    """
    if logger is None:
        logger = setup_logger(__name__)

    doi_usage = {}
    arxiv_usage = {}

    for post_path in posts_with_citations:
        try:
            with open(post_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.warning(f"Could not read {post_path}: {e}")
            continue

        post_name = Path(post_path).name

        # Extract DOI identifiers (normalized format)
        dois = re.findall(r'10\.\d{4,}/[^\s\)]+', content)
        for doi in set(dois):  # Unique DOIs per post
            if doi not in doi_usage:
                doi_usage[doi] = []
            doi_usage[doi].append(post_name)

        # Extract arXiv identifiers
        arxivs = re.findall(r'arxiv\.org/abs/(\d{4}\.\d{4,})', content, re.IGNORECASE)
        for arxiv_id in set(arxivs):
            if arxiv_id not in arxiv_usage:
                arxiv_usage[arxiv_id] = []
            arxiv_usage[arxiv_id].append(post_name)

    # Filter to only duplicates (used in >1 post)
    doi_duplicates = {k: v for k, v in doi_usage.items() if len(v) > 1}
    arxiv_duplicates = {k: v for k, v in arxiv_usage.items() if len(v) > 1}

    return {
        'doi_duplicates': doi_duplicates,
        'arxiv_duplicates': arxiv_duplicates,
        'total_doi_duplicates': len(doi_duplicates),
        'total_arxiv_duplicates': len(arxiv_duplicates),
        'total_unique_dois': len(doi_usage),
        'total_unique_arxivs': len(arxiv_usage)
    }


def main():
    parser = argparse.ArgumentParser(
        description='Validate research citations in blog posts (v2.0.0)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate all posts
  python scripts/blog-research/research-validator.py

  # Validate specific post
  python scripts/blog-research/research-validator.py --post 2024-01-01-example

  # Normalize DOI formats (dry-run)
  python scripts/blog-research/research-validator.py --normalize-dois --dry-run --batch

  # Apply DOI normalization to all posts
  python scripts/blog-research/research-validator.py --normalize-dois --batch

  # Detect duplicate citations
  python scripts/blog-research/research-validator.py --detect-duplicates

  # Quiet mode
  python scripts/blog-research/research-validator.py --quiet
        """
    )
    parser.add_argument('--version', action='version', version='%(prog)s 2.0.0')
    parser.add_argument('--post', help='Specific post to process (without .md extension)')
    parser.add_argument('--batch', action='store_true', help='Process all posts with citations')
    parser.add_argument('--check-claims', action='store_true', help='Check all claims')
    parser.add_argument('--fix', action='store_true', help='Suggest fixes for uncited claims')
    parser.add_argument('--normalize-dois', action='store_true', help='Normalize DOI citations to canonical HTTPS format')
    parser.add_argument('--detect-duplicates', action='store_true', help='Detect duplicate citations across posts')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without writing files')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable debug output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress output messages')
    parser.add_argument('--log-file', type=Path, help='Write logs to file')

    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(__name__, level=level, log_file=args.log_file, quiet=args.quiet)

    try:
        validator = ResearchValidator()

        # v2.0.0: Citation enhancement features
        if args.normalize_dois:
            if args.batch:
                # Process all posts with citations
                posts_dir = Path('src/posts')
                posts = list(posts_dir.glob('*.md'))

                logger.info("="*80)
                logger.info("DOI NORMALIZATION - BATCH MODE")
                logger.info("="*80)
                if args.dry_run:
                    logger.info("Mode: DRY RUN (no files will be modified)\n")

                results = []
                for post in posts:
                    result = process_citations_in_post(
                        str(post),
                        normalize_dois=True,
                        dry_run=args.dry_run,
                        logger=logger
                    )
                    if result.get('has_references'):
                        results.append((post.name, result))

                # Summary
                total_posts = len(results)
                posts_changed = sum(1 for _, r in results if r.get('change_count', 0) > 0)
                total_changes = sum(r.get('change_count', 0) for _, r in results)

                logger.info("\n" + "="*80)
                logger.info("SUMMARY")
                logger.info("="*80)
                logger.info(f"Posts with citations: {total_posts}")
                logger.info(f"Posts with changes: {posts_changed}")
                logger.info(f"Total DOI normalizations: {total_changes}")

                if args.dry_run:
                    logger.info(f"\nMode: DRY RUN - No files were modified")
                    logger.info(f"Run without --dry-run to apply changes")

            elif args.post:
                # Process specific post
                post_path = Path(f'src/posts/{args.post}.md')
                if not post_path.exists():
                    logger.error(f"❌ Error: Post not found: {post_path}")
                    return 1

                result = process_citations_in_post(
                    str(post_path),
                    normalize_dois=True,
                    dry_run=args.dry_run,
                    logger=logger
                )

                if not args.quiet:
                    logger.info(f"\nPost: {post_path.name}")
                    logger.info(f"  Changes: {result.get('changes_made', [])}")
                    logger.info(f"  DOI count: {result.get('doi_count', 0)}")
                    logger.info(f"  arXiv count: {result.get('arxiv_count', 0)}")
            else:
                logger.error("❌ Error: Must specify --batch or --post with --normalize-dois")
                return 1

        elif args.detect_duplicates:
            # Find posts with citations
            posts_dir = Path('src/posts')
            posts = [str(p) for p in posts_dir.glob('*.md')]

            logger.info("="*80)
            logger.info("DUPLICATE CITATION DETECTION")
            logger.info("="*80)
            logger.info(f"Analyzing {len(posts)} posts...\n")

            duplicates = detect_duplicate_citations(posts, logger=logger)

            logger.info(f"\n" + "="*80)
            logger.info("DUPLICATE CITATION REPORT")
            logger.info("="*80)
            logger.info(f"Total unique DOIs: {duplicates['total_unique_dois']}")
            logger.info(f"Total unique arXiv papers: {duplicates['total_unique_arxivs']}")
            logger.info(f"DOI duplicates: {duplicates['total_doi_duplicates']}")
            logger.info(f"arXiv duplicates: {duplicates['total_arxiv_duplicates']}")

            if duplicates['doi_duplicates']:
                logger.info(f"\nTop 10 DOI Duplicates:")
                sorted_dois = sorted(duplicates['doi_duplicates'].items(), key=lambda x: len(x[1]), reverse=True)
                for doi, posts_list in sorted_dois[:10]:
                    logger.info(f"  {doi}: {len(posts_list)} posts")
                    if args.verbose:
                        for post in posts_list:
                            logger.info(f"    - {post}")

            if duplicates['arxiv_duplicates']:
                logger.info(f"\nTop 10 arXiv Duplicates:")
                sorted_arxivs = sorted(duplicates['arxiv_duplicates'].items(), key=lambda x: len(x[1]), reverse=True)
                for arxiv, posts_list in sorted_arxivs[:10]:
                    logger.info(f"  arxiv.org/abs/{arxiv}: {len(posts_list)} posts")
                    if args.verbose:
                        for post in posts_list:
                            logger.info(f"    - {post}")

        elif args.post:
            # Original validation functionality
            post_path = Path(f'src/posts/{args.post}.md')
            if not post_path.exists():
                logger.error(f"❌ Error: Post not found: {post_path}")
                return 1
            result = validator.validate_post(post_path)
            if not args.quiet:
                logger.info(json.dumps(result, indent=2))
        else:
            # Original batch validation
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