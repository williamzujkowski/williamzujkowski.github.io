#!/usr/bin/env python3
"""
SCRIPT: humanization-validator.py
PURPOSE: Validate blog posts for human tone and detect AI-generated content tells
CATEGORY: content_validation
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-10-28

DESCRIPTION:
    Validates blog posts against humanization requirements to ensure authentic,
    engaging content that doesn't sound AI-generated. Checks for:
    - AI-tells (em dashes, semicolons, generic transitions)
    - Required humanization elements (first-person, uncertainty, specificity)
    - Sentiment analysis (reject overly positive/hype content)
    - Sentence and paragraph structure
    - Corporate jargon and buzzwords

LLM_USAGE:
    python scripts/blog-content/humanization-validator.py [options]

ARGUMENTS:
    --post (str): Path to blog post file (required)
    --config (str): Path to humanization patterns YAML (default: scripts/blog-content/humanization-patterns.yaml)
    --output (str): Output format [text|json] (default: text)
    --strict (bool): Strict mode - fail on any violation (default: False)
    --min-score (int): Minimum passing score 0-100 (default: 70)

EXAMPLES:
    # Validate single post
    python scripts/blog-content/humanization-validator.py --post src/posts/2025-01-15-example.md

    # Strict validation with JSON output
    python scripts/blog-content/humanization-validator.py --post src/posts/example.md --strict --output json

    # Custom minimum score
    python scripts/blog-content/humanization-validator.py --post src/posts/example.md --min-score 80

OUTPUT:
    - Human tone score (0-100)
    - Specific violations with line numbers
    - Required patterns status
    - Sentiment analysis
    - Recommendations for improvement
    - Exit code: 0 (pass), 1 (fail), 2 (error)

DEPENDENCIES:
    - Python 3.8+
    - PyYAML for config parsing
    - frontmatter for post parsing
    - re for pattern matching

RELATED_SCRIPTS:
    - scripts/blog-content/full-post-validation.py: Comprehensive validation
    - scripts/blog-content/humanization-patterns.yaml: Pattern definitions
    - scripts/blog-content/analyze-blog-content.py: Content analysis

MANIFEST_REGISTRY: scripts/blog-content/humanization-validator.py
"""

import os
import re
import sys
import json
import yaml
import argparse
import frontmatter
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

# ANSI color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class HumanizationValidator:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent / "humanization-patterns.yaml"

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.violations = []
        self.warnings = []
        self.passed_checks = []
        self.score = 100

    def validate_post(self, post_path: str) -> Dict:
        """Main validation function."""
        post = frontmatter.load(post_path)
        content = post.content

        # Remove code blocks for text analysis (but keep for pattern matching)
        text_without_code = self._remove_code_blocks(content)

        # Run all validation checks
        self._check_banned_tokens(content, text_without_code)
        self._check_required_patterns(content)
        self._check_sentiment(text_without_code)
        self._check_sentence_structure(text_without_code)
        self._check_paragraph_structure(text_without_code)

        # Calculate final score
        final_score = max(0, self.score)

        return {
            'score': final_score,
            'violations': self.violations,
            'warnings': self.warnings,
            'passed_checks': self.passed_checks,
            'post_path': post_path
        }

    def _remove_code_blocks(self, content: str) -> str:
        """Remove code blocks from content for text analysis."""
        # Remove fenced code blocks
        text = re.sub(r'```[\s\S]*?```', '', content)
        # Remove inline code
        text = re.sub(r'`[^`]+`', '', text)
        return text

    def _check_banned_tokens(self, full_content: str, text_content: str):
        """Check for AI-tells and banned tokens."""
        # Check punctuation (only in non-code text)
        for punct in self.config['banned_tokens']['punctuation']:
            token = punct['token']
            # Special handling for semicolons - allow in code blocks
            if token == ';':
                matches = re.finditer(re.escape(token), text_content)
            else:
                matches = re.finditer(re.escape(token), text_content)

            count = sum(1 for _ in matches)
            if count > 0:
                self.violations.append({
                    'type': 'banned_token',
                    'severity': punct['severity'],
                    'token': token,
                    'count': count,
                    'message': punct['message']
                })
                self.score += self.config['scoring']['banned_token_penalty'] * count

        # Check transitions
        for trans in self.config['banned_tokens']['transitions']:
            pattern = r'\b' + re.escape(trans['phrase']) + r'\b'
            matches = list(re.finditer(pattern, text_content, re.IGNORECASE))
            if matches:
                self.violations.append({
                    'type': 'ai_transition',
                    'severity': trans['severity'],
                    'phrase': trans['phrase'],
                    'count': len(matches),
                    'message': trans['message']
                })
                self.score += self.config['scoring']['banned_token_penalty'] * len(matches)

        # Check jargon
        for jargon in self.config['banned_tokens']['jargon']:
            pattern = r'\b' + re.escape(jargon['word']) + r'\b'
            matches = list(re.finditer(pattern, text_content, re.IGNORECASE))
            if matches:
                self.warnings.append({
                    'type': 'jargon',
                    'severity': jargon['severity'],
                    'word': jargon['word'],
                    'count': len(matches),
                    'message': jargon['message'],
                    'suggestions': jargon.get('suggested_replacements', [])
                })
                # Lighter penalty for jargon (warning, not violation)
                self.score += self.config['scoring']['banned_token_penalty'] * len(matches) * 0.5

        # Check hype words
        for hype in self.config['banned_tokens']['hype_words']:
            pattern = r'\b' + re.escape(hype['word']) + r'\b'
            matches = list(re.finditer(pattern, text_content, re.IGNORECASE))
            if matches:
                self.violations.append({
                    'type': 'hype_word',
                    'severity': hype['severity'],
                    'word': hype['word'],
                    'count': len(matches),
                    'message': hype['message']
                })
                self.score += self.config['scoring']['banned_token_penalty'] * len(matches)

    def _check_required_patterns(self, content: str):
        """Check for required humanization patterns."""
        for pattern_type, config in self.config['required_patterns'].items():
            found_count = 0

            for pattern in config['patterns']:
                if isinstance(pattern, dict) and 'regex' in pattern:
                    matches = re.findall(pattern['regex'], content)
                    found_count += len(matches)
                else:
                    # String literal pattern
                    found_count += len(re.findall(re.escape(pattern), content, re.IGNORECASE))

            min_required = config['min_occurrences']
            if found_count >= min_required:
                self.passed_checks.append({
                    'type': pattern_type,
                    'found': found_count,
                    'required': min_required
                })
            else:
                self.violations.append({
                    'type': 'missing_required_pattern',
                    'severity': 'high',
                    'pattern_type': pattern_type,
                    'found': found_count,
                    'required': min_required,
                    'message': config['message']
                })
                self.score += self.config['scoring']['missing_required_pattern_penalty']

    def _check_sentiment(self, content: str):
        """Check sentiment to avoid overly positive/hype content."""
        sentiment_config = self.config['sentiment']

        # Count positive and negative emotion words
        positive_words = sentiment_config['positive_emotion_words']
        negative_words = sentiment_config['negative_balance_words']

        positive_count = sum(len(re.findall(r'\b' + re.escape(word) + r'\b', content, re.IGNORECASE))
                           for word in positive_words)
        negative_count = sum(len(re.findall(r'\b' + re.escape(word) + r'\b', content, re.IGNORECASE))
                           for word in negative_words)

        # Calculate paragraphs
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        paragraph_count = len(paragraphs)

        if paragraph_count == 0:
            sentiment_score = 0
        else:
            # Mean sentiment = (positive - negative) / paragraphs
            # Scale: -2 (very negative) to +2 (very positive)
            sentiment_score = (positive_count - negative_count) / paragraph_count

        threshold = sentiment_config['overly_positive_threshold']

        if sentiment_score > threshold:
            self.violations.append({
                'type': 'overly_positive_sentiment',
                'severity': 'high',
                'sentiment_score': round(sentiment_score, 2),
                'threshold': threshold,
                'positive_count': positive_count,
                'negative_count': negative_count,
                'message': f'Content is too positive/hype (score: {sentiment_score:.2f}, threshold: {threshold}). Add more balanced perspective with trade-offs and limitations.'
            })
            self.score += self.config['scoring']['overly_positive_sentiment_penalty']
        else:
            self.passed_checks.append({
                'type': 'sentiment_balance',
                'sentiment_score': round(sentiment_score, 2),
                'threshold': threshold
            })

    def _check_sentence_structure(self, content: str):
        """Check sentence length variety."""
        # Split into sentences
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return

        # Count words per sentence
        sentence_lengths = [len(s.split()) for s in sentences]
        avg_length = sum(sentence_lengths) / len(sentence_lengths)
        short_sentences = sum(1 for length in sentence_lengths if length < 10)

        config = self.config['sentence_structure']

        # Check average length
        if avg_length > config['max_avg_sentence_length']:
            self.warnings.append({
                'type': 'long_sentences',
                'severity': 'low',
                'avg_length': round(avg_length, 1),
                'max_avg': config['max_avg_sentence_length'],
                'message': config['message']
            })

        # Check for short sentences
        if short_sentences < config['min_short_sentences']:
            self.warnings.append({
                'type': 'insufficient_short_sentences',
                'severity': 'low',
                'found': short_sentences,
                'required': config['min_short_sentences'],
                'message': config['message']
            })
        else:
            self.passed_checks.append({
                'type': 'sentence_variety',
                'short_sentences': short_sentences,
                'avg_length': round(avg_length, 1)
            })

    def _check_paragraph_structure(self, content: str):
        """Check paragraph length."""
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

        if not paragraphs:
            return

        paragraph_lengths = [len(p.split()) for p in paragraphs]
        avg_length = sum(paragraph_lengths) / len(paragraph_lengths)
        short_paragraphs = sum(1 for length in paragraph_lengths if length < 50)

        config = self.config['paragraph_structure']

        if avg_length > config['max_avg_paragraph_length']:
            self.warnings.append({
                'type': 'long_paragraphs',
                'severity': 'medium',
                'avg_length': round(avg_length, 1),
                'max_avg': config['max_avg_paragraph_length'],
                'message': config['message']
            })

        if short_paragraphs < config['min_short_paragraphs']:
            self.warnings.append({
                'type': 'insufficient_paragraph_variety',
                'severity': 'low',
                'found': short_paragraphs,
                'required': config['min_short_paragraphs'],
                'message': config['message']
            })
        else:
            self.passed_checks.append({
                'type': 'paragraph_variety',
                'short_paragraphs': short_paragraphs,
                'avg_length': round(avg_length, 1)
            })

def print_results(results: Dict, output_format: str = 'text'):
    """Print validation results."""
    if output_format == 'json':
        print(json.dumps(results, indent=2))
        return

    # Text format with colors
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}HUMANIZATION VALIDATION REPORT{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")

    score = results['score']
    if score >= 70:
        color = Colors.GREEN
        status = "PASS"
    elif score >= 50:
        color = Colors.YELLOW
        status = "NEEDS IMPROVEMENT"
    else:
        color = Colors.RED
        status = "FAIL"

    print(f"Post: {Colors.CYAN}{results['post_path']}{Colors.RESET}")
    print(f"Score: {color}{score}/100 - {status}{Colors.RESET}\n")

    # Violations
    if results['violations']:
        print(f"{Colors.RED}{Colors.BOLD}VIOLATIONS ({len(results['violations'])}){Colors.RESET}")
        for v in results['violations']:
            severity_color = Colors.RED if v['severity'] == 'high' else Colors.YELLOW
            print(f"  {severity_color}[{v['severity'].upper()}]{Colors.RESET} {v['type']}")
            print(f"    {v['message']}")
            if 'count' in v:
                print(f"    Found: {v['count']} occurrence(s)")
            if 'suggestions' in v:
                print(f"    Suggestions: {', '.join(v['suggestions'])}")
            print()

    # Warnings
    if results['warnings']:
        print(f"{Colors.YELLOW}{Colors.BOLD}WARNINGS ({len(results['warnings'])}){Colors.RESET}")
        for w in results['warnings']:
            print(f"  {Colors.YELLOW}[{w['severity'].upper()}]{Colors.RESET} {w['type']}")
            print(f"    {w['message']}")
            if 'count' in w:
                print(f"    Found: {w['count']} occurrence(s)")
            if 'suggestions' in w:
                print(f"    Suggestions: {', '.join(w['suggestions'])}")
            print()

    # Passed checks
    if results['passed_checks']:
        print(f"{Colors.GREEN}{Colors.BOLD}PASSED CHECKS ({len(results['passed_checks'])}){Colors.RESET}")
        for p in results['passed_checks']:
            print(f"  {Colors.GREEN}✓{Colors.RESET} {p['type']}")
            if 'found' in p and 'required' in p:
                print(f"    Found: {p['found']} (required: {p['required']})")
            print()

    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")

def main():
    parser = argparse.ArgumentParser(
        description='Validate blog posts for human tone and detect AI-generated content',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/blog-content/humanization-validator.py --post src/posts/example.md
  python scripts/blog-content/humanization-validator.py --post src/posts/example.md --strict
  python scripts/blog-content/humanization-validator.py --post src/posts/example.md --output json
        """
    )

    parser.add_argument('--post', required=True, help='Path to blog post file')
    parser.add_argument('--config', help='Path to humanization patterns YAML')
    parser.add_argument('--output', choices=['text', 'json'], default='text', help='Output format')
    parser.add_argument('--strict', action='store_true', help='Strict mode - fail on any violation')
    parser.add_argument('--min-score', type=int, default=70, help='Minimum passing score (0-100)')

    args = parser.parse_args()

    # Validate post exists
    if not os.path.exists(args.post):
        print(f"{Colors.RED}Error: Post file not found: {args.post}{Colors.RESET}", file=sys.stderr)
        return 2

    # Run validation
    validator = HumanizationValidator(args.config)
    results = validator.validate_post(args.post)

    # Print results
    print_results(results, args.output)

    # Determine exit code
    if args.strict and results['violations']:
        return 1
    elif results['score'] < args.min_score:
        return 1
    else:
        return 0

if __name__ == '__main__':
    sys.exit(main())
