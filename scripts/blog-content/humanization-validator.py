#!/usr/bin/env python3
"""
SCRIPT: humanization-validator.py
PURPOSE: Validate blog posts for human tone and detect AI-generated content tells
CATEGORY: content_validation
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-10-29

DESCRIPTION:
    Validates blog posts against humanization requirements to ensure authentic,
    engaging content that doesn't sound AI-generated. Checks for:
    - AI-tells (em dashes, semicolons, generic transitions)
    - Required humanization elements (first-person, uncertainty, specificity)
    - Sentiment analysis (reject overly positive/hype content)
    - Sentence and paragraph structure
    - Corporate jargon and buzzwords

    NEW in v2.0: Batch processing with parallel execution for portfolio-wide validation.

LLM_USAGE:
    python scripts/blog-content/humanization-validator.py [options]

ARGUMENTS:
    --post (str): Path to blog post file (single-post mode)
    --batch (bool): Process all posts in src/posts/ directory
    --dir (str): Custom directory for batch processing
    --config (str): Path to humanization patterns YAML (default: scripts/blog-content/humanization-patterns.yaml)
    --output (str): Output format [text|json] (default: text)
    --format (str): Batch output format [summary|json|detailed] (default: summary)
    --strict (bool): Strict mode - fail on any violation (default: False)
    --min-score (int): Minimum passing score 0-100 (default: 70)
    --filter-below (int): In batch mode, only show posts scoring below this threshold
    --save-report (str): Save batch report to file
    --compare (str): Compare with previous report JSON
    --workers (int): Number of parallel workers (default: 4)

EXAMPLES:
    # Validate single post
    python scripts/blog-content/humanization-validator.py --post src/posts/2025-01-15-example.md

    # Batch validate all posts
    python scripts/blog-content/humanization-validator.py --batch

    # Batch with filtering and JSON output
    python scripts/blog-content/humanization-validator.py --batch --filter-below 90 --format json

    # Save batch report
    python scripts/blog-content/humanization-validator.py --batch --save-report reports/validation-2025-10-29.json

    # Compare with previous report
    python scripts/blog-content/humanization-validator.py --batch --compare reports/validation-2025-10-28.json

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
import time
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict
from multiprocessing import Pool, cpu_count
from datetime import datetime

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

        # Check for measurements and apply bonus scoring
        measurements = self.detect_measurements(content)
        total_measurements = sum(measurements.values())
        if total_measurements >= 10:
            self.score += 10
            self.passed_checks.append({
                'type': 'measurement_richness',
                'total': total_measurements,
                'bonus': 10,
                'breakdown': measurements,
                'message': f'Excellent: {total_measurements} measurements found across diverse categories'
            })
        elif total_measurements >= 5:
            self.score += 5
            self.passed_checks.append({
                'type': 'measurement_richness',
                'total': total_measurements,
                'bonus': 5,
                'breakdown': measurements,
                'message': f'Good: {total_measurements} measurements found'
            })

        # Calculate final score
        final_score = max(0, self.score)

        return {
            'score': final_score,
            'violations': self.violations,
            'warnings': self.warnings,
            'passed_checks': self.passed_checks,
            'post_path': post_path,
            'measurements': measurements
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

            # Special handling for trade-offs: analyze depth
            if pattern_type == 'trade_offs' and found_count >= min_required:
                depth_score = self._analyze_tradeoff_depth(content)
                self.passed_checks.append({
                    'type': pattern_type,
                    'found': found_count,
                    'required': min_required,
                    'depth_score': depth_score,
                    'depth_analysis': self._get_depth_description(depth_score)
                })
            elif found_count >= min_required:
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

    def _analyze_tradeoff_depth(self, content: str) -> int:
        """
        Analyze the depth of trade-off discussion.
        Returns a score from 0-10:
        - 1-2: Simple mention of trade-offs
        - 3-4: Basic two-sided comparison
        - 5-6: Detailed comparison with some metrics
        - 7-8: Multi-option evaluation with quantified comparisons
        - 9-10: Comprehensive multi-option analysis with context-dependent recommendations
        """
        score = 0
        text = content.lower()

        # Category 1: Multi-option evaluation (3 points max)
        # Look for evidence of testing multiple options (3+)
        multi_option_indicators = 0

        # Pattern 1: Explicit "tested/tried X, Y, and Z" patterns
        if re.search(r'(?:tested|tried|compared|experimented with)\s+\d+.*?and\s+\d+', text):
            multi_option_indicators += 1

        # Pattern 2: Multiple "with X" comparisons in same section
        with_patterns = re.findall(r'with\s+\d+\s+(?:heads|layers|options|configurations|approaches|parameters|features|nodes)', text)
        if len(with_patterns) >= 3:
            multi_option_indicators += 1

        # Pattern 2b: Also look for capitalized "With X" at sentence starts
        with_capital_patterns = re.findall(r'\.\s+with\s+\d+\s+(?:heads|layers|options|configurations|approaches|parameters)', text)
        if len(with_capital_patterns) >= 2:
            multi_option_indicators += 1

        # Pattern 3: Explicit "tried N different" statements
        if re.search(r'(?:tried|tested|compared)\s+(?:\d+|several|multiple)\s+(?:different\s+)?(?:approaches|options|configurations|values)', text):
            multi_option_indicators += 1

        # Pattern 4: Sequential option analysis (With X... With Y... With Z...)
        option_analysis_pattern = r'(?:with|using|at)\s+\d+\s+\w+,.*?(?:with|using|at)\s+\d+\s+\w+,.*?(?:with|using|at)\s+\d+\s+\w+'
        if re.search(option_analysis_pattern, text, re.DOTALL):
            multi_option_indicators += 1

        # Score based on indicators
        if multi_option_indicators >= 3:
            score += 3  # Excellent multi-option analysis
        elif multi_option_indicators >= 2:
            score += 2.5
        elif multi_option_indicators == 1:
            score += 2

        # Category 2: Constraint discussion (2 points max)
        constraint_patterns = [
            r'limited by',
            r'constrained by',
            r'bounded by',
            r'bottleneck',
            r'constraint',
            r'can\'?t go beyond',
            r'restricted to',
        ]
        constraint_count = sum(len(re.findall(p, text)) for p in constraint_patterns)
        if constraint_count >= 3:
            score += 2
        elif constraint_count >= 1:
            score += 1

        # Category 3: Nuanced conclusions (2 points max)
        nuance_patterns = [
            r'depends on',
            r'varies by',
            r'better for .{1,30} but worse for',
            r'faster .{1,30} but .{1,30} memory',
            r'trades .{1,30} for',
            r'at the cost of',
            r'in exchange for',
        ]
        nuance_count = sum(len(re.findall(p, text)) for p in nuance_patterns)
        if nuance_count >= 3:
            score += 2
        elif nuance_count >= 1:
            score += 1

        # Category 4: Performance vs. X comparisons (1 point max)
        perf_patterns = [
            r'(?:speed|performance|throughput)\s+vs\.?\s+(?:accuracy|memory|cost|complexity)',
            r'(?:accuracy|precision)\s+vs\.?\s+(?:speed|memory|simplicity)',
            r'(?:cost|price)\s+vs\.?\s+(?:performance|features|capabilities)',
        ]
        if any(re.search(p, text) for p in perf_patterns):
            score += 1

        # Category 5: Quantified comparisons (3 points max - increased for rich data)
        quant_patterns = [
            r'\d+x\s+(?:faster|slower|more|less)',
            r'\d+%\s+(?:faster|slower|more|less|better|worse)',
            r'from\s+\d+.*\s+to\s+\d+',
            r'improved.*by\s+\d+',
            r'increased.*by\s+\d+',
            r'reduced.*by\s+\d+',
        ]
        quant_count = sum(len(re.findall(p, text)) for p in quant_patterns)
        if quant_count >= 10:
            score += 3  # Exceptional quantified data richness
        elif quant_count >= 5:
            score += 2
        elif quant_count >= 2:
            score += 1

        # Bonus: Context-dependent recommendations (1 point max)
        context_patterns = [
            r'use .{1,30} when',
            r'choose .{1,30} if',
            r'opt for .{1,30} when',
            r'works (?:well|better) for',
            r'(?:ideal|best) for .{1,30} but',
        ]
        if sum(len(re.findall(p, text)) for p in context_patterns) >= 2:
            score += 1

        return min(int(score), 11)  # Cap at 11 (increased max from quantified comparisons) and convert to int

    def _get_depth_description(self, score: int) -> str:
        """Return a human-readable description of the trade-off depth score."""
        if score >= 9:
            return "Excellent: Comprehensive multi-option analysis with context-dependent recommendations"
        elif score >= 7:
            return "Very Good: Multi-option evaluation with quantified comparisons"
        elif score >= 5:
            return "Good: Detailed comparison with metrics"
        elif score >= 3:
            return "Fair: Basic two-sided comparison"
        elif score >= 1:
            return "Minimal: Simple trade-off mention"
        else:
            return "None: No measurable trade-off depth"

    def detect_measurements(self, content: str) -> Dict[str, int]:
        """
        Detect various types of measurements and quantitative data in content.
        Returns dict with counts by category for comprehensive measurement analysis.
        """
        measurements = {
            'percentages': 0,
            'multipliers': 0,
            'comparisons': 0,
            'performance_metrics': 0,
            'hardware_specs': 0,
            'time_measurements': 0,
            'data_sizes': 0,
            'experimental_data': 0
        }

        # Percentages: "73%", "25.5% improvement", "15.6% true positive rate"
        percentage_pattern = r'\b\d+(?:\.\d+)?%'
        measurements['percentages'] = len(re.findall(percentage_pattern, content))

        # Multipliers: "2.1x faster", "4x improvement", "10× speedup"
        multiplier_pattern = r'\b\d+(?:\.\d+)?[x×](?:\s+(?:faster|slower|more|less|improvement|speedup|reduction))?'
        measurements['multipliers'] = len(re.findall(multiplier_pattern, content, re.IGNORECASE))

        # Comparisons: "X vs Y", "compared to", "faster than", "better than"
        comparison_patterns = [
            r'\bvs\.\s+\w+',
            r'\bversus\s+\w+',
            r'\bcompared\s+to\s+\w+',
            r'\bfaster\s+than\s+\w+',
            r'\bslower\s+than\s+\w+',
            r'\bbetter\s+than\s+\w+',
            r'\bworse\s+than\s+\w+',
            r'\bfrom\s+\d+.*\s+to\s+\d+'
        ]
        for pattern in comparison_patterns:
            measurements['comparisons'] += len(re.findall(pattern, content, re.IGNORECASE))

        # Performance metrics: "requests per second", "3.2 seconds", "latency"
        perf_patterns = [
            r'\b\d+(?:\.\d+)?\s+(?:requests?|queries|operations?|transactions?)\s+per\s+(?:second|minute|hour)',
            r'\b\d+(?:\.\d+)?\s+(?:req/s|qps|ops/s|tps)',
            r'\b\d+(?:\.\d+)?\s*(?:ms|μs|microseconds?|milliseconds?|seconds?)\b',
            r'\bthroughput\s+(?:of\s+)?\d+(?:\.\d+)?',
            r'\blatency.*?\d+(?:\.\d+)?\s*(?:ms|seconds?)'
        ]
        for pattern in perf_patterns:
            measurements['performance_metrics'] += len(re.findall(pattern, content, re.IGNORECASE))

        # Hardware specs: "64GB RAM", "Intel i9-9900K", "RTX 3090", "8 cores"
        hardware_patterns = [
            r'\b\d+\s*(?:GB|MB|KB|TB)\s+(?:RAM|memory|storage|disk)',
            r'\b(?:Intel|AMD)\s+\w+[-\s]\w+',
            r'\bRTX\s+\d+',
            r'\bGTX\s+\d+',
            r'\b\d+\s+(?:cores?|threads?)\b',
            r'\b\d+(?:\.\d+)?\s*(?:GHz|MHz)',
            r'\bRaspberry\s+Pi\s+\w+'
        ]
        for pattern in hardware_patterns:
            measurements['hardware_specs'] += len(re.findall(pattern, content, re.IGNORECASE))

        # Time measurements: "3 hours", "2 days", "5 minutes"
        time_pattern = r'\b\d+(?:\.\d+)?\s*(?:seconds?|minutes?|hours?|days?|weeks?|months?|years?)\b'
        measurements['time_measurements'] = len(re.findall(time_pattern, content, re.IGNORECASE))

        # Data sizes: "48,000 lines", "150 lines of code", "400 LOC", "12 projects"
        data_size_patterns = [
            r'\b\d+(?:,\d{3})*\s+(?:lines?(?:\s+of\s+code)?|LOC|files?|projects?|objects?|tables?)',
            r'\b\d+K\s+LOC\b',
            r'\b\d+\s+(?:vulnerabilities|issues|bugs|problems|challenges|patterns)'
        ]
        for pattern in data_size_patterns:
            measurements['data_sizes'] += len(re.findall(pattern, content, re.IGNORECASE))

        # Experimental data: "tested with 50 samples", "measured over 3 months", "scan found 147"
        experimental_patterns = [
            r'\btested\s+(?:with|on|against)\s+\d+',
            r'\bmeasured\s+(?:over|across|with)\s+\d+',
            r'\bscanned?\s+\d+',
            r'\bfound\s+\d+\s+(?:potential\s+)?(?:vulnerabilities|issues|bugs|problems)',
            r'\bidentified\s+\d+\s+(?:potential\s+)?(?:attack|threat|vulnerability)',
            r'\bimplemented\s+\d+\s+(?:mitigations?|fixes?|solutions?)',
            r'\bapplied.*to\s+\d+\s+(?:services?|accounts?|systems?)',
            r'\breduced.*(?:from|by)\s+\d+'
        ]
        for pattern in experimental_patterns:
            measurements['experimental_data'] += len(re.findall(pattern, content, re.IGNORECASE))

        return measurements

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


    def _score_failure_narratives(self, content: str) -> Dict:
        """
        Score failure narratives to detect authentic human storytelling through mistakes and lessons.

        Failure narratives are a key indicator of authentic human writing because:
        - They show vulnerability and honesty
        - They demonstrate real experience and learning
        - They help readers avoid similar mistakes
        - AI-generated content typically avoids admitting failures

        Returns dict with:
        - score: 0-10 points based on richness
        - categories: breakdown by failure type
        - examples: specific failure mentions found
        """
        failure_patterns = {
            'bug_admissions': {
                'patterns': [
                    r'\b(I made|made|had) (a |an |the )?(mistake|error|bug|misstep)\b',
                    r'\b(overlooked|forgot|missed|neglected) (to |the )?\w+\b',
                    r'\b(didn\'t|did not) (think|consider|account|realize)\b',
                    r'\b(rookie mistake|beginner mistake|silly mistake)\b',
                ],
                'weight': 1.5  # High value for explicit admissions
            },
            'debugging_stories': {
                'patterns': [
                    r'\b(spent|took|wasted|consumed) \d+[\+]? (hours?|minutes?|days?) (debugging|troubleshooting|investigating|fixing)\b',
                    r'\b(debugging|troubleshooting) (nightmare|hell|marathon|session)\b',
                    r'\bdiscovered (after|during|while)\b',
                    r'\b(traced|tracked) (down|back) (the )?(bug|issue|problem)\b',
                ],
                'weight': 2.0  # Very high value for detailed debugging stories
            },
            'learning_from_failure': {
                'patterns': [
                    r'\b(learned|taught me) (the )?(hard way|lesson)\b',
                    r'\b(now I (always|never)|now I know|this taught me)\b',
                    r'\b(won\'t make|never (again|make) that) (mistake|error)\b',
                    r'\b(painful|expensive|costly) (lesson|experience)\b',
                ],
                'weight': 1.5
            },
            'time_costs': {
                'patterns': [
                    r'\b(cost|took|wasted|spent|consumed) (me |us |the team )?(\d+[\+]?|several|many) (hours?|days?|weeks?|months?)\b',
                    r'\b(\d+[\+]?) (hours?|days?) (of )?(panic|frustration|confusion|downtime)\b',
                    r'\b(lost|wasted) (\d+[\+]?|several) (hours?|days?)\b',
                ],
                'weight': 1.5  # Time costs show real impact
            },
            'explicit_mistakes': {
                'patterns': [
                    r'\b(misconfigured|misunderstood|underestimated|overestimated)\b',
                    r'\b(incorrectly|improperly|wrongly) (configured|assumed|believed|thought)\b',
                    r'\b(failed to|didn\'t|did not) (validate|check|test|verify|account for)\b',
                    r'\bcompletely (forgot|missed|overlooked|underestimated)\b',
                ],
                'weight': 1.5
            },
            'recovery_narratives': {
                'patterns': [
                    r'\b(had to|needed to) (redo|rebuild|rewrite|reconfigure|restart)\b',
                    r'\b(went back|rolled back|reverted) and (fixed|corrected|addressed)\b',
                    r'\b(recovery|remediation|fix|repair) (took|required|needed)\b',
                    r'\bafter (\d+) (attempts?|tries|iterations)\b',
                ],
                'weight': 1.0
            }
        }

        results = {
            'score': 0,
            'raw_score': 0,
            'categories': {},
            'examples': [],
            'total_mentions': 0
        }

        # Detect each pattern type
        for category, config in failure_patterns.items():
            matches = []
            for pattern in config['patterns']:
                found = re.finditer(pattern, content, re.IGNORECASE)
                for match in found:
                    # Get surrounding context (50 chars before and after)
                    start = max(0, match.start() - 50)
                    end = min(len(content), match.end() + 50)
                    context = content[start:end].replace('\n', ' ')
                    matches.append({
                        'text': match.group(0),
                        'context': context
                    })

            if matches:
                results['categories'][category] = {
                    'count': len(matches),
                    'weight': config['weight'],
                    'contribution': len(matches) * config['weight']
                }
                results['examples'].extend(matches[:3])  # Keep first 3 examples per category
                results['total_mentions'] += len(matches)

        # Calculate score (0-10 based on richness)
        raw_score = sum(cat['contribution'] for cat in results['categories'].values())
        results['raw_score'] = round(raw_score, 2)

        # Scoring rubric:
        # 0 points: No failures mentioned
        # 2-3 points: Generic failure mention (1-2 simple mentions)
        # 5-6 points: Specific failure with details (3-5 mentions or 1-2 rich stories)
        # 8-10 points: Rich narrative with time costs, recovery, lessons (6+ mentions or multiple rich stories)

        if raw_score == 0:
            results['score'] = 0
            results['quality'] = 'none'
        elif raw_score < 3:
            results['score'] = 2
            results['quality'] = 'minimal'
        elif raw_score < 6:
            results['score'] = 4
            results['quality'] = 'moderate'
        elif raw_score < 10:
            results['score'] = 6
            results['quality'] = 'good'
        elif raw_score < 15:
            results['score'] = 8
            results['quality'] = 'excellent'
        else:
            results['score'] = 10
            results['quality'] = 'exceptional'

        return results


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
            if 'depth_score' in p:
                # Color code depth score
                depth_color = Colors.GREEN if p['depth_score'] >= 7 else Colors.YELLOW if p['depth_score'] >= 4 else Colors.RED
                print(f"    Depth Score: {depth_color}{p['depth_score']}/10{Colors.RESET}")
                print(f"    Analysis: {p['depth_analysis']}")
            if 'breakdown' in p:
                # Display measurement breakdown
                print(f"    Total: {p.get('total', 0)} (+{p.get('bonus', 0)} bonus points)")
                print(f"    Breakdown:")
                for category, count in p['breakdown'].items():
                    if count > 0:
                        print(f"      - {category.replace('_', ' ').title()}: {count}")
            print()

    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")



# ========================================
# BATCH PROCESSING FUNCTIONS (NEW in v2.0)
# ========================================

def validate_post_wrapper(args_tuple):
    """Wrapper for multiprocessing."""
    post_path, config_path = args_tuple
    try:
        validator = HumanizationValidator(config_path)
        results = validator.validate_post(post_path)
        return results
    except Exception as e:
        return {
            'score': 0,
            'violations': [{'type': 'error', 'message': str(e)}],
            'warnings': [],
            'passed_checks': [],
            'post_path': post_path,
            'error': True
        }

def batch_validate_posts(posts_dir: str, config_path: str, workers: int = 4) -> List[Dict]:
    """Validate multiple posts in parallel."""
    # Find all markdown files
    posts_path = Path(posts_dir)
    post_files = sorted(posts_path.glob('*.md'))

    if not post_files:
        print(f"{Colors.YELLOW}No markdown files found in {posts_dir}{Colors.RESET}")
        return []

    total_posts = len(post_files)
    print(f"\n{Colors.BOLD}Starting batch validation...{Colors.RESET}")
    print(f"Posts to validate: {Colors.CYAN}{total_posts}{Colors.RESET}")
    print(f"Workers: {Colors.CYAN}{workers}{Colors.RESET}\n")

    # Prepare arguments for multiprocessing
    args_list = [(str(post), config_path) for post in post_files]

    # Process with progress tracking
    start_time = time.time()
    results = []

    with Pool(processes=workers) as pool:
        # Use imap for ordered results with progress tracking
        for i, result in enumerate(pool.imap(validate_post_wrapper, args_list), 1):
            results.append(result)

            # Progress indicator
            progress = (i / total_posts) * 100
            elapsed = time.time() - start_time
            avg_time = elapsed / i
            eta = avg_time * (total_posts - i)

            status = "✓" if result['score'] >= 70 else "✗"
            color = Colors.GREEN if result['score'] >= 70 else Colors.RED
            score = int(result['score'])  # Convert to int for display

            print(f"{color}{status}{Colors.RESET} [{i}/{total_posts}] {progress:5.1f}% | "
                  f"Score: {color}{score:3d}{Colors.RESET} | "
                  f"ETA: {eta:5.1f}s | {Path(result['post_path']).name}")

    total_time = time.time() - start_time
    print(f"\n{Colors.GREEN}Batch validation complete!{Colors.RESET}")
    print(f"Total time: {Colors.CYAN}{total_time:.2f}s{Colors.RESET}")
    print(f"Average: {Colors.CYAN}{total_time/total_posts:.2f}s{Colors.RESET} per post\n")

    return results

def print_batch_summary(results: List[Dict], format_type: str = 'summary',
                        filter_below: int = None, min_score: int = 70):
    """Print batch validation summary."""

    # Filter results if requested
    if filter_below:
        results = [r for r in results if r['score'] < filter_below]

    if format_type == 'json':
        output = {
            'timestamp': datetime.now().isoformat(),
            'total_posts': len(results),
            'results': results,
            'statistics': calculate_statistics(results, min_score)
        }
        print(json.dumps(output, indent=2))
        return

    # Calculate statistics
    stats = calculate_statistics(results, min_score)

    # Print header
    print(f"\n{Colors.BOLD}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}BATCH VALIDATION SUMMARY{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*80}{Colors.RESET}\n")

    # Statistics
    print(f"{Colors.BOLD}Statistics:{Colors.RESET}")
    print(f"  Total Posts: {Colors.CYAN}{stats['total_posts']}{Colors.RESET}")
    print(f"  Passed: {Colors.GREEN}{stats['passed']}{Colors.RESET} ({stats['pass_rate']:.1f}%)")
    print(f"  Failed: {Colors.RED}{stats['failed']}{Colors.RESET} ({stats['fail_rate']:.1f}%)")
    print(f"  Average Score: {Colors.CYAN}{stats['avg_score']:.1f}{Colors.RESET}")
    print(f"  Median Score: {Colors.CYAN}{stats['median_score']}{Colors.RESET}")
    print(f"  Min Score: {Colors.RED}{stats['min_score']}{Colors.RESET}")
    print(f"  Max Score: {Colors.GREEN}{stats['max_score']}{Colors.RESET}\n")

    if format_type == 'summary':
        # Table header
        print(f"{Colors.BOLD}{'Post':<50} {'Score':>6} {'Status':>10} {'Issues':>7}{Colors.RESET}")
        print(f"{'-'*80}")

        # Sort by score (lowest first for attention)
        sorted_results = sorted(results, key=lambda x: x['score'])

        for result in sorted_results:
            post_name = Path(result['post_path']).name[:48]
            score = int(result['score'])  # Convert to int for display
            status = "PASS" if score >= min_score else "FAIL"
            status_color = Colors.GREEN if score >= min_score else Colors.RED
            score_color = Colors.GREEN if score >= 70 else (Colors.YELLOW if score >= 50 else Colors.RED)
            issues = len(result['violations'])

            print(f"{post_name:<50} {score_color}{score:>6}{Colors.RESET} "
                  f"{status_color}{status:>10}{Colors.RESET} {issues:>7}")

    elif format_type == 'detailed':
        # Detailed view with violations
        for result in sorted(results, key=lambda x: x['score']):
            print(f"\n{Colors.BOLD}{'='*80}{Colors.RESET}")
            print(f"{Colors.CYAN}{Path(result['post_path']).name}{Colors.RESET}")
            print(f"Score: {int(result['score'])}/100")

            if result['violations']:
                print(f"\n{Colors.RED}Violations:{Colors.RESET}")
                for v in result['violations']:
                    print(f"  • {v['type']}: {v.get('message', 'N/A')}")

            if result['warnings']:
                print(f"\n{Colors.YELLOW}Warnings:{Colors.RESET}")
                for w in result['warnings']:
                    print(f"  • {w['type']}: {w.get('message', 'N/A')}")

    print(f"\n{Colors.BOLD}{'='*80}{Colors.RESET}\n")

def calculate_statistics(results: List[Dict], min_score: int) -> Dict:
    """Calculate batch statistics."""
    scores = [r['score'] for r in results]
    total = len(results)
    passed = sum(1 for s in scores if s >= min_score)
    failed = total - passed

    sorted_scores = sorted(scores)
    median_score = sorted_scores[len(sorted_scores) // 2] if sorted_scores else 0

    return {
        'total_posts': total,
        'passed': passed,
        'failed': failed,
        'pass_rate': (passed / total * 100) if total > 0 else 0,
        'fail_rate': (failed / total * 100) if total > 0 else 0,
        'avg_score': sum(scores) / total if total > 0 else 0,
        'median_score': median_score,
        'min_score': min(scores) if scores else 0,
        'max_score': max(scores) if scores else 0
    }

def compare_reports(current_results: List[Dict], previous_report_path: str):
    """Compare current results with previous report."""
    with open(previous_report_path, 'r') as f:
        previous_data = json.load(f)

    previous_results = previous_data['results']

    # Create lookup by post name
    prev_lookup = {Path(r['post_path']).name: r['score'] for r in previous_results}
    curr_lookup = {Path(r['post_path']).name: r['score'] for r in current_results}

    print(f"\n{Colors.BOLD}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}COMPARISON WITH PREVIOUS REPORT{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*80}{Colors.RESET}\n")

    improvements = []
    regressions = []
    unchanged = []

    for post_name in curr_lookup:
        if post_name in prev_lookup:
            prev_score = prev_lookup[post_name]
            curr_score = curr_lookup[post_name]
            diff = curr_score - prev_score

            if diff > 0:
                improvements.append((post_name, prev_score, curr_score, diff))
            elif diff < 0:
                regressions.append((post_name, prev_score, curr_score, diff))
            else:
                unchanged.append(post_name)

    if improvements:
        print(f"{Colors.GREEN}{Colors.BOLD}Improvements ({len(improvements)}):{Colors.RESET}")
        for name, prev, curr, diff in sorted(improvements, key=lambda x: x[3], reverse=True):
            print(f"  {Colors.GREEN}↑{Colors.RESET} {name[:50]:<50} {prev:>3} → {curr:>3} (+{diff})")
        print()

    if regressions:
        print(f"{Colors.RED}{Colors.BOLD}Regressions ({len(regressions)}):{Colors.RESET}")
        for name, prev, curr, diff in sorted(regressions, key=lambda x: x[3]):
            print(f"  {Colors.RED}↓{Colors.RESET} {name[:50]:<50} {prev:>3} → {curr:>3} ({diff})")
        print()

    if unchanged:
        print(f"{Colors.CYAN}Unchanged: {len(unchanged)} posts{Colors.RESET}\n")

    print(f"{Colors.BOLD}{'='*80}{Colors.RESET}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Validate blog posts for human tone and detect AI-generated content',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single post validation
  python scripts/blog-content/humanization-validator.py --post src/posts/example.md

  # Batch validation
  python scripts/blog-content/humanization-validator.py --batch

  # Batch with filtering
  python scripts/blog-content/humanization-validator.py --batch --filter-below 90 --format detailed

  # Save report
  python scripts/blog-content/humanization-validator.py --batch --save-report validation-report.json
        """
    )

    parser.add_argument('--post', help='Path to blog post file (single-post mode)')
    parser.add_argument('--batch', action='store_true', help='Process all posts in directory')
    parser.add_argument('--dir', default='src/posts', help='Directory for batch processing')
    parser.add_argument('--config', help='Path to humanization patterns YAML')
    parser.add_argument('--output', choices=['text', 'json'], default='text', help='Output format (single-post mode)')
    parser.add_argument('--format', choices=['summary', 'json', 'detailed'], default='summary',
                        help='Batch output format')
    parser.add_argument('--strict', action='store_true', help='Strict mode - fail on any violation')
    parser.add_argument('--min-score', type=int, default=70, help='Minimum passing score (0-100)')
    parser.add_argument('--filter-below', type=int, help='Only show posts scoring below threshold')
    parser.add_argument('--save-report', help='Save batch report to file')
    parser.add_argument('--compare', help='Compare with previous report JSON')
    parser.add_argument('--workers', type=int, default=min(4, cpu_count()),
                        help='Number of parallel workers')

    args = parser.parse_args()

    # Determine mode
    if args.batch:
        # Batch mode
        if not os.path.exists(args.dir):
            print(f"{Colors.RED}Error: Directory not found: {args.dir}{Colors.RESET}", file=sys.stderr)
            return 2

        # Run batch validation
        results = batch_validate_posts(args.dir, args.config, args.workers)

        if not results:
            return 2

        # Compare with previous if requested
        if args.compare:
            if os.path.exists(args.compare):
                compare_reports(results, args.compare)
            else:
                print(f"{Colors.YELLOW}Warning: Previous report not found: {args.compare}{Colors.RESET}")

        # Print results
        print_batch_summary(results, args.format, args.filter_below, args.min_score)

        # Save report if requested
        if args.save_report:
            output = {
                'timestamp': datetime.now().isoformat(),
                'total_posts': len(results),
                'results': results,
                'statistics': calculate_statistics(results, args.min_score)
            }
            os.makedirs(os.path.dirname(args.save_report) or '.', exist_ok=True)
            with open(args.save_report, 'w') as f:
                json.dump(output, f, indent=2)
            print(f"{Colors.GREEN}Report saved to: {args.save_report}{Colors.RESET}\n")

        # Exit code: 0 if all pass, 1 if any fail
        failed_count = sum(1 for r in results if r['score'] < args.min_score)
        return 1 if failed_count > 0 else 0

    else:
        # Single-post mode
        if not args.post:
            print(f"{Colors.RED}Error: --post required for single-post mode (or use --batch){Colors.RESET}",
                  file=sys.stderr)
            return 2

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
