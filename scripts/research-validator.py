#!/usr/bin/env python3
"""
Research Validator - Ensures all blog post claims are backed by reputable sources
"""

import re
import json
import frontmatter
from pathlib import Path
from typing import Dict, List, Tuple
import argparse
from datetime import datetime

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
    
    def generate_report(self, posts_dir: Path = Path('src/posts')):
        """Generate a comprehensive research validation report for all posts."""
        posts = sorted(posts_dir.glob('*.md'))
        results = []
        
        print("="*80)
        print("BLOG POST RESEARCH VALIDATION REPORT")
        print("="*80)
        print(f"\nAnalyzing {len(posts)} posts for research integrity...\n")
        
        for post_path in posts:
            result = self.validate_post(post_path)
            results.append(result)
            
            # Print summary for posts needing attention
            if result['citation_rate'] < 80 or result['low_quality_sources'] > 0:
                print(f"\n⚠️  {result['file']}")
                print(f"   Citation Rate: {result['citation_rate']:.1f}%")
                print(f"   Uncited Claims: {result['uncited_claims']}")
                if result['low_quality_sources'] > 0:
                    print(f"   Low Quality Sources: {result['low_quality_sources']}")
                for rec in result['recommendations'][:3]:
                    print(f"   • {rec}")
        
        # Overall statistics
        avg_citation_rate = sum(r['citation_rate'] for r in results) / len(results)
        total_uncited = sum(r['uncited_claims'] for r in results)
        posts_needing_work = sum(1 for r in results if r['citation_rate'] < 80)
        
        print("\n" + "="*80)
        print("OVERALL STATISTICS")
        print("="*80)
        print(f"Average Citation Rate: {avg_citation_rate:.1f}%")
        print(f"Total Uncited Claims: {total_uncited}")
        print(f"Posts Needing Citations: {posts_needing_work}/{len(posts)}")
        
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
        
        print(f"\nDetailed report saved to: docs/research-validation-report.json")
        
        return results

def main():
    parser = argparse.ArgumentParser(description='Validate research citations in blog posts')
    parser.add_argument('--post', help='Specific post to validate')
    parser.add_argument('--check-claims', action='store_true', help='Check all claims')
    parser.add_argument('--fix', action='store_true', help='Suggest fixes for uncited claims')
    
    args = parser.parse_args()
    
    validator = ResearchValidator()
    
    if args.post:
        post_path = Path(f'src/posts/{args.post}.md')
        if post_path.exists():
            result = validator.validate_post(post_path)
            print(json.dumps(result, indent=2))
    else:
        validator.generate_report()

if __name__ == "__main__":
    main()