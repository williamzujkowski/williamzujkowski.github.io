#!/usr/bin/env -S uv run python3
"""
SCRIPT: citation-repair.py
PURPOSE: Citation Repair Tool
CATEGORY: academic_research
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T15:08:08-04:00

DESCRIPTION:
    Citation Repair Tool. This script is part of the academic research
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/citation-repair.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/citation-repair.py

    # With verbose output
    python scripts/citation-repair.py --verbose

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

MANIFEST_REGISTRY: scripts/citation-repair.py
"""

import json
import re
import asyncio
import aiohttp
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from urllib.parse import urlparse, quote
import hashlib

@dataclass
class RepairSuggestion:
    """Suggested repair for a broken link"""
    original_url: str
    link_hash: str
    issue_type: str
    suggested_url: str
    source: str  # Where the replacement was found
    confidence: float  # 0-100
    title: str
    description: str
    is_archived: bool
    repair_type: str  # direct, wayback, alternative, doi_resolution
    notes: str

    def to_dict(self):
        return asdict(self)

class CitationRepair:
    """Find replacements for broken citations"""

    # Academic search APIs and databases
    ACADEMIC_SOURCES = {
        'arxiv': 'https://export.arxiv.org/api/query',
        'crossref': 'https://api.crossref.org/works',
        'core': 'https://core.ac.uk/api-v2/search',
        'semantic_scholar': 'https://api.semanticscholar.org/v1/paper',
        'unpaywall': 'https://api.unpaywall.org/v2',
        'pmc': 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/'
    }

    # Documentation sources
    DOC_SOURCES = {
        'mdn': 'https://developer.mozilla.org',
        'python': 'https://docs.python.org',
        'github': 'https://docs.github.com',
        'aws': 'https://docs.aws.amazon.com',
        'kubernetes': 'https://kubernetes.io/docs'
    }

    def __init__(self):
        self.session = None
        self.stats = {
            'total_processed': 0,
            'direct_fixes': 0,
            'wayback_fixes': 0,
            'alternative_fixes': 0,
            'no_fix_found': 0
        }
        self.repair_cache = {}

    async def initialize(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession(
            headers={'User-Agent': 'CitationRepair/1.0 (https://williamzujkowski.github.io)'}
        )

    async def cleanup(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()

    async def find_repairs(self, links_data: Dict, validation_data: Dict,
                          relevance_data: Dict) -> List[RepairSuggestion]:
        """Find repairs for all broken links"""
        repairs = []

        # Identify broken links
        broken_links = self._identify_broken_links(
            links_data, validation_data, relevance_data
        )

        print(f"🔍 Found {len(broken_links)} links needing repair")

        # Process each broken link
        for link_info in broken_links:
            self.stats['total_processed'] += 1
            suggestion = await self._find_replacement(link_info)

            if suggestion:
                repairs.append(suggestion)
            else:
                self.stats['no_fix_found'] += 1

        return repairs

    def _identify_broken_links(self, links_data: Dict, validation_data: Dict,
                              relevance_data: Dict) -> List[Dict]:
        """Identify links that need repair"""
        broken = []

        # Map validation and relevance results
        validation_map = {r['url']: r for r in validation_data.get('results', [])}
        relevance_map = {r['url']: r for r in relevance_data.get('results', [])}

        for link in links_data.get('links', []):
            url = link['url']
            validation = validation_map.get(url, {})
            relevance = relevance_map.get(url, {})

            # Check if link needs repair
            needs_repair = False
            issue_type = None

            if validation.get('status') in ['broken', 'timeout', 'error']:
                needs_repair = True
                issue_type = validation.get('issue_type', 'broken')
            elif validation.get('issue_type') == 'paywall':
                needs_repair = True
                issue_type = 'paywall'
            elif relevance.get('suggested_action') == 'replace':
                needs_repair = True
                issue_type = 'low_relevance'

            if needs_repair:
                broken.append({
                    'link': link,
                    'validation': validation,
                    'relevance': relevance,
                    'issue_type': issue_type
                })

        return broken

    async def _find_replacement(self, link_info: Dict) -> Optional[RepairSuggestion]:
        """Find replacement for a single broken link"""
        link = link_info['link']
        url = link['url']
        issue_type = link_info['issue_type']

        # Check cache
        cache_key = f"{url}:{issue_type}"
        if cache_key in self.repair_cache:
            return self.repair_cache[cache_key]

        suggestion = None

        # Try different repair strategies based on link type
        if self._is_academic_url(url) or link['type'] == 'citation':
            suggestion = await self._repair_academic_citation(link_info)
        elif self._is_documentation_url(url) or link['type'] == 'documentation':
            suggestion = await self._repair_documentation_link(link_info)
        elif issue_type == '404':
            suggestion = await self._repair_with_wayback(link_info)
        elif issue_type == 'redirect':
            suggestion = await self._validate_redirect(link_info)
        elif issue_type == 'paywall':
            suggestion = await self._find_open_access_version(link_info)

        # Cache result
        if suggestion:
            self.repair_cache[cache_key] = suggestion

        return suggestion

    async def _repair_academic_citation(self, link_info: Dict) -> Optional[RepairSuggestion]:
        """Repair academic citations"""
        link = link_info['link']
        url = link['url']
        context = link.get('context_before', '') + ' ' + link.get('context_after', '')

        # Extract paper details from context
        paper_info = self._extract_paper_info(context, url)

        # Try different academic sources
        strategies = [
            self._search_arxiv,
            self._search_crossref,
            self._search_semantic_scholar,
            self._check_doi_resolution,
            self._find_pmc_version
        ]

        for strategy in strategies:
            try:
                result = await strategy(paper_info, url)
                if result:
                    self.stats['alternative_fixes'] += 1
                    return result
            except Exception as e:
                print(f"  Strategy {strategy.__name__} failed: {e}")
                continue

        return None

    async def _search_arxiv(self, paper_info: Dict, original_url: str) -> Optional[RepairSuggestion]:
        """Search arXiv for paper"""
        if not paper_info.get('title'):
            return None

        try:
            query = quote(paper_info['title'])
            search_url = f"{self.ACADEMIC_SOURCES['arxiv']}?search_query=ti:{query}&max_results=1"

            async with self.session.get(search_url) as response:
                if response.status == 200:
                    content = await response.text()

                    # Parse arXiv response (simplified)
                    if '<entry>' in content:
                        # Extract URL
                        url_match = re.search(r'<id>([^<]+)</id>', content)
                        title_match = re.search(r'<title>([^<]+)</title>', content)

                        if url_match:
                            new_url = url_match.group(1)
                            title = title_match.group(1) if title_match else paper_info['title']

                            return RepairSuggestion(
                                original_url=original_url,
                                link_hash=paper_info.get('hash', ''),
                                issue_type='broken_citation',
                                suggested_url=new_url,
                                source='arXiv',
                                confidence=85,
                                title=title,
                                description='Found on arXiv',
                                is_archived=False,
                                repair_type='alternative',
                                notes='Open access version available on arXiv'
                            )
        except Exception as e:
            print(f"    arXiv search error: {e}")

        return None

    async def _search_crossref(self, paper_info: Dict, original_url: str) -> Optional[RepairSuggestion]:
        """Search CrossRef for DOI"""
        if not paper_info.get('title'):
            return None

        try:
            query = quote(paper_info['title'])
            search_url = f"{self.ACADEMIC_SOURCES['crossref']}?query={query}&rows=1"

            async with self.session.get(search_url) as response:
                if response.status == 200:
                    data = await response.json()

                    if data.get('message', {}).get('items'):
                        item = data['message']['items'][0]
                        doi = item.get('DOI')

                        if doi:
                            new_url = f"https://doi.org/{doi}"
                            title = item.get('title', [''])[0] or paper_info['title']

                            return RepairSuggestion(
                                original_url=original_url,
                                link_hash=paper_info.get('hash', ''),
                                issue_type='broken_citation',
                                suggested_url=new_url,
                                source='CrossRef',
                                confidence=90,
                                title=title,
                                description='DOI resolution link',
                                is_archived=False,
                                repair_type='doi_resolution',
                                notes='Permanent DOI link'
                            )
        except Exception as e:
            print(f"    CrossRef search error: {e}")

        return None

    async def _search_semantic_scholar(self, paper_info: Dict,
                                      original_url: str) -> Optional[RepairSuggestion]:
        """Search Semantic Scholar"""
        # Simplified - would need API key for production
        return None

    async def _check_doi_resolution(self, paper_info: Dict,
                                   original_url: str) -> Optional[RepairSuggestion]:
        """Check if DOI can be resolved"""
        doi = paper_info.get('doi')
        if not doi:
            # Try to extract DOI from URL
            doi_match = re.search(r'10\.\d{4,}/[-._;()/:\w]+', original_url)
            if doi_match:
                doi = doi_match.group(0)

        if doi:
            new_url = f"https://doi.org/{doi}"
            # In production, would verify this resolves
            return RepairSuggestion(
                original_url=original_url,
                link_hash=paper_info.get('hash', ''),
                issue_type='broken_citation',
                suggested_url=new_url,
                source='DOI',
                confidence=95,
                title=paper_info.get('title', 'Paper'),
                description='Direct DOI link',
                is_archived=False,
                repair_type='doi_resolution',
                notes='Permanent DOI resolution'
            )

        return None

    async def _find_pmc_version(self, paper_info: Dict,
                               original_url: str) -> Optional[RepairSuggestion]:
        """Find PubMed Central open access version"""
        # Simplified - would use PMC API
        return None

    async def _repair_documentation_link(self, link_info: Dict) -> Optional[RepairSuggestion]:
        """Repair broken documentation links"""
        link = link_info['link']
        url = link['url']

        # Try Wayback Machine first
        wayback_result = await self._repair_with_wayback(link_info)
        if wayback_result:
            return wayback_result

        # Try to find updated documentation URL
        parsed = urlparse(url)
        domain = parsed.netloc

        # Check if it's a known documentation site
        for doc_name, doc_base in self.DOC_SOURCES.items():
            if doc_name in domain or doc_base in url:
                # Try to find updated path
                # In production, would search the documentation site
                pass

        return None

    async def _repair_with_wayback(self, link_info: Dict) -> Optional[RepairSuggestion]:
        """Try to find archived version in Wayback Machine"""
        url = link_info['link']['url']

        try:
            # Check Wayback Machine availability API
            wayback_api = f"https://archive.org/wayback/available?url={quote(url)}"

            async with self.session.get(wayback_api) as response:
                if response.status == 200:
                    data = await response.json()

                    if data.get('archived_snapshots', {}).get('closest'):
                        snapshot = data['archived_snapshots']['closest']
                        wayback_url = snapshot['url']

                        # Ensure HTTPS
                        wayback_url = wayback_url.replace('http://', 'https://')

                        self.stats['wayback_fixes'] += 1

                        return RepairSuggestion(
                            original_url=url,
                            link_hash=link_info['link'].get('hash', ''),
                            issue_type=link_info['issue_type'],
                            suggested_url=wayback_url,
                            source='Wayback Machine',
                            confidence=70,
                            title=link_info['link'].get('text', 'Archived Page'),
                            description=f"Archived on {snapshot.get('timestamp', 'unknown')}",
                            is_archived=True,
                            repair_type='wayback',
                            notes='Historical snapshot - content may be outdated'
                        )
        except Exception as e:
            print(f"    Wayback Machine error: {e}")

        return None

    async def _validate_redirect(self, link_info: Dict) -> Optional[RepairSuggestion]:
        """Validate and suggest accepting redirects"""
        validation = link_info.get('validation', {})
        final_url = validation.get('final_url')

        if final_url and final_url != link_info['link']['url']:
            # Check if redirect is reasonable
            original_domain = urlparse(link_info['link']['url']).netloc
            new_domain = urlparse(final_url).netloc

            # Same domain or known redirects
            if original_domain == new_domain or self._is_known_redirect(
                original_domain, new_domain
            ):
                confidence = 95
                notes = 'Same domain redirect'
            else:
                confidence = 60
                notes = 'Different domain - manual review recommended'

            self.stats['direct_fixes'] += 1

            return RepairSuggestion(
                original_url=link_info['link']['url'],
                link_hash=link_info['link'].get('hash', ''),
                issue_type='redirect',
                suggested_url=final_url,
                source='HTTP Redirect',
                confidence=confidence,
                title=link_info['link'].get('text', 'Redirected Page'),
                description='Following HTTP redirect',
                is_archived=False,
                repair_type='direct',
                notes=notes
            )

        return None

    async def _find_open_access_version(self, link_info: Dict) -> Optional[RepairSuggestion]:
        """Find open access version of paywalled content"""
        # Would use Unpaywall API or similar
        # For now, try arXiv as fallback
        return await self._repair_academic_citation(link_info)

    def _is_academic_url(self, url: str) -> bool:
        """Check if URL is academic"""
        academic_domains = [
            'arxiv.org', 'doi.org', 'pubmed', 'ieee.org', 'acm.org',
            'springer', 'sciencedirect', 'nature.com', 'plos.org'
        ]
        return any(domain in url.lower() for domain in academic_domains)

    def _is_documentation_url(self, url: str) -> bool:
        """Check if URL is documentation"""
        doc_indicators = ['docs', 'documentation', 'api', 'reference', 'guide', 'manual']
        return any(indicator in url.lower() for indicator in doc_indicators)

    def _is_known_redirect(self, old_domain: str, new_domain: str) -> bool:
        """Check if this is a known redirect pattern"""
        known_redirects = [
            ('twitter.com', 'x.com'),
            ('www.twitter.com', 'www.x.com'),
            ('github.io', 'github.com'),
        ]

        for old, new in known_redirects:
            if old in old_domain and new in new_domain:
                return True

        # Check for www vs non-www
        if old_domain.replace('www.', '') == new_domain.replace('www.', ''):
            return True

        return False

    def _extract_paper_info(self, context: str, url: str) -> Dict:
        """Extract paper information from context"""
        info = {}

        # Try to extract title (text in quotes or before year)
        title_match = re.search(r'"([^"]+)"', context)
        if not title_match:
            title_match = re.search(r'([A-Z][^.]+)\s*\(\d{4}\)', context)

        if title_match:
            info['title'] = title_match.group(1).strip()

        # Extract authors
        author_match = re.search(r'by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+et\s+al\.?)?)', context)
        if author_match:
            info['authors'] = author_match.group(1)

        # Extract year
        year_match = re.search(r'\((\d{4})\)', context)
        if year_match:
            info['year'] = year_match.group(1)

        # Extract DOI if present
        doi_match = re.search(r'10\.\d{4,}/[-._;()/:\w]+', context + ' ' + url)
        if doi_match:
            info['doi'] = doi_match.group(0)

        # Extract arXiv ID if present
        arxiv_match = re.search(r'(\d{4}\.\d{4,5}(?:v\d+)?)', url)
        if arxiv_match:
            info['arxiv_id'] = arxiv_match.group(1)

        return info

    def save_results(self, repairs: List[RepairSuggestion], output_file: Path):
        """Save repair suggestions"""
        data = {
            'repair_date': datetime.now().isoformat(),
            'stats': self.stats,
            'repairs': [r.to_dict() for r in repairs]
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        print(f"✅ Processed {self.stats['total_processed']} broken links")
        print(f"🔧 Direct fixes: {self.stats['direct_fixes']}")
        print(f"📚 Wayback fixes: {self.stats['wayback_fixes']}")
        print(f"🔄 Alternative fixes: {self.stats['alternative_fixes']}")
        print(f"❌ No fix found: {self.stats['no_fix_found']}")
        print(f"💾 Results saved to {output_file}")

async def main():
    parser = argparse.ArgumentParser(description='Find repairs for broken citations')
    parser.add_argument('--links', type=Path,
                       default=Path('links.json'),
                       help='Links data file')
    parser.add_argument('--validation', type=Path,
                       default=Path('validation.json'),
                       help='Validation results file')
    parser.add_argument('--relevance', type=Path,
                       default=Path('relevance.json'),
                       help='Relevance results file')
    parser.add_argument('--output', type=Path,
                       default=Path('repairs.json'),
                       help='Output file')

    args = parser.parse_args()

    # Load input data
    with open(args.links, 'r') as f:
        links_data = json.load(f)

    with open(args.validation, 'r') as f:
        validation_data = json.load(f)

    with open(args.relevance, 'r') as f:
        relevance_data = json.load(f)

    # Initialize repair tool
    repair_tool = CitationRepair()
    await repair_tool.initialize()

    try:
        # Find repairs
        repairs = await repair_tool.find_repairs(
            links_data, validation_data, relevance_data
        )

        # Save results
        repair_tool.save_results(repairs, args.output)
    finally:
        await repair_tool.cleanup()

    return 0

if __name__ == '__main__':
    asyncio.run(main())