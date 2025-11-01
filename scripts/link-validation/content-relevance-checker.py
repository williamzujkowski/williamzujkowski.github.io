#!/usr/bin/env -S uv run python3
"""
SCRIPT: content-relevance-checker.py
PURPOSE: Content Relevance Checker
CATEGORY: blog_management
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T15:08:08-04:00

DESCRIPTION:
    Content Relevance Checker. This script is part of the blog management
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/content-relevance-checker.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/content-relevance-checker.py

    # With verbose output
    python scripts/content-relevance-checker.py --verbose

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

MANIFEST_REGISTRY: scripts/content-relevance-checker.py
"""

import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
from difflib import SequenceMatcher
import unicodedata
import string

# Try to import advanced NLP libraries
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("⚠️  scikit-learn not installed. Using basic text similarity.")

@dataclass
class RelevanceResult:
    """Result of content relevance check"""
    url: str
    link_hash: str
    relevance_score: float  # 0-100
    title_match_score: float
    content_match_score: float
    keyword_overlap: float
    domain_reliability: float
    potential_issues: List[str]
    suggested_action: str  # keep, review, replace
    confidence: float
    analysis_time: str

    def to_dict(self):
        return asdict(self)

class ContentRelevanceChecker:
    """Check if linked content matches the citation context"""

    # Domain reliability scores
    DOMAIN_SCORES = {
        # Academic/Research - Highest reliability
        'arxiv.org': 95,
        'doi.org': 95,
        'pubmed.ncbi.nlm.nih.gov': 95,
        'ieee.org': 90,
        'acm.org': 90,
        'springer.com': 90,
        'nature.com': 95,
        'sciencedirect.com': 90,
        'plos.org': 90,

        # Official documentation
        'docs.python.org': 95,
        'developer.mozilla.org': 95,
        'docs.microsoft.com': 90,
        'docs.aws.amazon.com': 90,
        'kubernetes.io': 90,
        'golang.org': 90,

        # Code repositories
        'github.com': 85,
        'gitlab.com': 85,
        'bitbucket.org': 80,

        # Security/Standards
        'owasp.org': 95,
        'nist.gov': 95,
        'cve.mitre.org': 95,
        'nvd.nist.gov': 95,
        'cisa.gov': 95,
        'first.org': 90,

        # News/Blogs - Variable reliability
        'medium.com': 60,
        'dev.to': 65,
        'hackernews.com': 70,
        'reddit.com': 50,
        'twitter.com': 40,
        'x.com': 40,

        # General
        'wikipedia.org': 75,
        'stackoverflow.com': 80,
    }

    # Keywords that indicate specific content types
    CONTENT_TYPE_KEYWORDS = {
        'research': ['study', 'research', 'analysis', 'findings', 'results',
                    'methodology', 'experiment', 'hypothesis', 'conclusion'],
        'documentation': ['api', 'reference', 'guide', 'tutorial', 'documentation',
                         'syntax', 'parameter', 'function', 'method', 'class'],
        'news': ['breaking', 'announced', 'released', 'update', 'news',
                'report', 'coverage', 'story', 'article'],
        'code': ['repository', 'commit', 'pull request', 'issue', 'branch',
                'fork', 'clone', 'merge', 'release', 'tag'],
        'security': ['vulnerability', 'cve', 'exploit', 'patch', 'advisory',
                    'disclosure', 'threat', 'attack', 'mitigation']
    }

    def __init__(self):
        self.stats = {
            'total_checked': 0,
            'high_relevance': 0,
            'medium_relevance': 0,
            'low_relevance': 0,
            'review_needed': 0
        }

    def check_relevance(self, link_data: Dict, validation_data: Dict) -> RelevanceResult:
        """Check relevance of a single link"""
        self.stats['total_checked'] += 1

        url = link_data['url']
        link_hash = link_data['hash']
        context = link_data.get('context_before', '') + ' ' + link_data.get('context_after', '')
        link_text = link_data.get('text', '')

        # Get validation results for this URL
        validation = self._find_validation_result(url, validation_data)

        if not validation or validation['status'] != 'valid':
            # Can't check relevance for broken links
            return self._create_result(
                url, link_hash, 0, 0, 0, 0,
                ['Link is not accessible'],
                'replace' if validation else 'review'
            )

        page_title = validation.get('page_title', '')
        content_type = validation.get('content_type', '')

        # Calculate various relevance scores
        title_score = self._calculate_title_relevance(link_text, page_title, context)
        content_score = self._calculate_content_relevance(context, page_title)
        keyword_score = self._calculate_keyword_overlap(context, page_title, url)
        domain_score = self._get_domain_reliability(url)

        # Weighted average of scores
        weights = {
            'title': 0.3,
            'content': 0.3,
            'keywords': 0.2,
            'domain': 0.2
        }

        relevance_score = (
            title_score * weights['title'] +
            content_score * weights['content'] +
            keyword_score * weights['keywords'] +
            domain_score * weights['domain']
        )

        # Identify potential issues
        issues = self._identify_issues(
            relevance_score, title_score, content_score,
            keyword_score, domain_score, url, context
        )

        # Determine suggested action
        if relevance_score >= 70:
            action = 'keep'
            self.stats['high_relevance'] += 1
        elif relevance_score >= 40:
            action = 'review'
            self.stats['medium_relevance'] += 1
            self.stats['review_needed'] += 1
        else:
            action = 'replace'
            self.stats['low_relevance'] += 1
            self.stats['review_needed'] += 1

        # Calculate confidence
        confidence = self._calculate_confidence(
            title_score, content_score, keyword_score, domain_score
        )

        return self._create_result(
            url, link_hash, relevance_score, title_score,
            content_score, keyword_score, issues, action, confidence
        )

    def _find_validation_result(self, url: str, validation_data: Dict) -> Optional[Dict]:
        """Find validation result for a URL"""
        for result in validation_data.get('results', []):
            if result['url'] == url:
                return result
        return None

    def _calculate_title_relevance(self, link_text: str, page_title: str,
                                  context: str) -> float:
        """Calculate how well the page title matches expectations"""
        if not page_title:
            return 0

        # Clean and normalize text
        link_text = self._normalize_text(link_text)
        page_title = self._normalize_text(page_title)
        context = self._normalize_text(context)

        scores = []

        # Direct match between link text and title
        if link_text:
            link_similarity = self._text_similarity(link_text, page_title)
            scores.append(link_similarity * 100)

        # Check if key words from context appear in title
        context_words = set(context.split())
        title_words = set(page_title.split())
        if context_words and title_words:
            overlap = len(context_words & title_words) / len(context_words)
            scores.append(overlap * 100)

        return sum(scores) / len(scores) if scores else 0

    def _calculate_content_relevance(self, context: str, page_title: str) -> float:
        """Calculate content relevance using text similarity"""
        if not context or not page_title:
            return 50  # Neutral score if we can't determine

        context = self._normalize_text(context)
        page_title = self._normalize_text(page_title)

        if SKLEARN_AVAILABLE:
            # Use TF-IDF for better similarity measurement
            try:
                vectorizer = TfidfVectorizer(
                    max_features=100,
                    stop_words='english',
                    ngram_range=(1, 2)
                )
                vectors = vectorizer.fit_transform([context, page_title])
                similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
                return similarity * 100
            except:
                pass

        # Fallback to simple similarity
        return self._text_similarity(context, page_title) * 100

    def _calculate_keyword_overlap(self, context: str, page_title: str,
                                  url: str) -> float:
        """Calculate keyword overlap between context and content"""
        context_lower = context.lower()
        title_lower = page_title.lower() if page_title else ''
        url_lower = url.lower()

        # Extract important keywords from context
        important_words = self._extract_important_words(context)
        if not important_words:
            return 50

        # Check how many appear in title or URL
        found_count = 0
        for word in important_words:
            if word in title_lower or word in url_lower:
                found_count += 1

        return (found_count / len(important_words)) * 100

    def _extract_important_words(self, text: str) -> List[str]:
        """Extract important words from text"""
        # Remove common words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
            'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is',
            'was', 'are', 'were', 'been', 'be', 'have', 'has',
            'had', 'do', 'does', 'did', 'will', 'would', 'should',
            'could', 'may', 'might', 'can', 'this', 'that', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }

        words = text.lower().split()
        important = []

        for word in words:
            # Clean word
            word = re.sub(r'[^\w]', '', word)
            if len(word) > 3 and word not in stop_words:
                important.append(word)

        return important[:10]  # Return top 10 important words

    def _get_domain_reliability(self, url: str) -> float:
        """Get domain reliability score"""
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc

            # Remove www prefix
            if domain.startswith('www.'):
                domain = domain[4:]

            # Check exact match
            if domain in self.DOMAIN_SCORES:
                return self.DOMAIN_SCORES[domain]

            # Check partial match (e.g., subdomain.example.com)
            for known_domain, score in self.DOMAIN_SCORES.items():
                if known_domain in domain:
                    return score * 0.9  # Slightly lower for subdomains

            # Default score for unknown domains
            return 50

        except:
            return 50

    def _identify_issues(self, relevance_score: float, title_score: float,
                        content_score: float, keyword_score: float,
                        domain_score: float, url: str, context: str) -> List[str]:
        """Identify potential issues with the link"""
        issues = []

        if relevance_score < 40:
            issues.append('Low overall relevance to context')

        if title_score < 30:
            issues.append('Page title does not match expected content')

        if content_score < 30:
            issues.append('Content similarity is very low')

        if keyword_score < 20:
            issues.append('Few keywords from context found in linked page')

        if domain_score < 50:
            issues.append('Low domain reliability score')

        # Check for specific mismatches
        context_lower = context.lower()
        url_lower = url.lower()

        # Academic citation pointing to non-academic source
        if any(word in context_lower for word in ['research', 'study', 'paper']):
            if not any(domain in url_lower for domain in
                      ['arxiv', 'doi', 'pubmed', 'ieee', 'acm']):
                issues.append('Academic citation links to non-academic source')

        # Documentation link pointing to wrong type
        if 'documentation' in context_lower and 'blog' in url_lower:
            issues.append('Documentation reference links to blog post')

        return issues

    def _calculate_confidence(self, title_score: float, content_score: float,
                             keyword_score: float, domain_score: float) -> float:
        """Calculate confidence in the relevance assessment"""
        scores = [title_score, content_score, keyword_score, domain_score]

        # High confidence if all scores are consistent
        std_dev = np.std(scores) if SKLEARN_AVAILABLE else self._simple_std_dev(scores)

        if std_dev < 10:
            confidence = 90
        elif std_dev < 20:
            confidence = 75
        elif std_dev < 30:
            confidence = 60
        else:
            confidence = 40

        # Boost confidence for highly reliable domains
        if domain_score > 90:
            confidence = min(100, confidence + 10)

        return confidence

    def _simple_std_dev(self, values: List[float]) -> float:
        """Simple standard deviation calculation"""
        if not values:
            return 0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5

    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison"""
        if not text:
            return ''

        # Convert to lowercase
        text = text.lower()

        # Remove punctuation
        text = re.sub(r'[^\w\s]', ' ', text)

        # Normalize whitespace
        text = ' '.join(text.split())

        return text

    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity"""
        if not text1 or not text2:
            return 0

        # Use SequenceMatcher for basic similarity
        return SequenceMatcher(None, text1, text2).ratio()

    def _create_result(self, url: str, link_hash: str, relevance_score: float,
                      title_score: float, content_score: float,
                      keyword_score: float, issues: List[str],
                      action: str, confidence: float = 50) -> RelevanceResult:
        """Create a relevance result"""
        domain_score = self._get_domain_reliability(url)

        return RelevanceResult(
            url=url,
            link_hash=link_hash,
            relevance_score=round(relevance_score, 2),
            title_match_score=round(title_score, 2),
            content_match_score=round(content_score, 2),
            keyword_overlap=round(keyword_score, 2),
            domain_reliability=round(domain_score, 2),
            potential_issues=issues,
            suggested_action=action,
            confidence=round(confidence, 2),
            analysis_time=datetime.now().isoformat()
        )

    def save_results(self, results: List[RelevanceResult], output_file: Path):
        """Save relevance check results"""
        data = {
            'analysis_date': datetime.now().isoformat(),
            'stats': self.stats,
            'results': [r.to_dict() for r in results]
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        print(f"✅ Checked relevance for {self.stats['total_checked']} links")
        print(f"✔️  High relevance: {self.stats['high_relevance']}")
        print(f"⚠️  Medium relevance: {self.stats['medium_relevance']}")
        print(f"❌ Low relevance: {self.stats['low_relevance']}")
        print(f"🔍 Review needed: {self.stats['review_needed']}")
        print(f"💾 Results saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Check content relevance of validated links')
    parser.add_argument('--links', type=Path,
                       default=Path('links.json'),
                       help='Input JSON file with extracted links')
    parser.add_argument('--validation', type=Path,
                       default=Path('validation.json'),
                       help='Input JSON file with validation results')
    parser.add_argument('--output', type=Path,
                       default=Path('relevance.json'),
                       help='Output JSON file')

    args = parser.parse_args()

    if not args.links.exists():
        print(f"❌ Links file not found: {args.links}")
        return 1

    if not args.validation.exists():
        print(f"❌ Validation file not found: {args.validation}")
        return 1

    # Load data
    with open(args.links, 'r', encoding='utf-8') as f:
        links_data = json.load(f)

    with open(args.validation, 'r', encoding='utf-8') as f:
        validation_data = json.load(f)

    print(f"📋 Loaded {len(links_data['links'])} links to check")

    # Check relevance
    checker = ContentRelevanceChecker()
    results = []

    for link in links_data['links']:
        result = checker.check_relevance(link, validation_data)
        results.append(result)

    # Save results
    checker.save_results(results, args.output)

    return 0

if __name__ == '__main__':
    exit(main())