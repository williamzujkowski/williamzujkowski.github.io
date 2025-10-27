#!/usr/bin/env python3
"""
Blog Compliance Analyzer - CLAUDE.md Standards
Analyzes all blog posts for compliance with new content standards:
1. Smart Brevity (BLUF, bullets, conciseness)
2. Polite Linus Tone (direct, honest, respectful)
3. AI Skepticism (question claims, demand evidence)
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple

# Corporate speak patterns to flag
CORPORATE_SPEAK = [
    r'\bleverage\b', r'\bsynergy\b', r'\bparadigm\s+shift\b',
    r'\bvalue\s+add\b', r'\blow[-\s]hanging\s+fruit\b',
    r'\bcircle\s+back\b', r'\bmove\s+the\s+needle\b',
    r'\btouch\s+base\b', r'\bdrink\s+the\s+kool[-\s]aid\b',
    r'\bthink\s+outside\s+the\s+box\b', r'\bgame[-\s]changer\b',
    r'\bdisruptive\b', r'\binnovative\s+solution\b'
]

# Throat-clearing patterns
THROAT_CLEARING = [
    r'^In\s+this\s+(post|article|piece),?\s+(I|we)\s+will',
    r'^This\s+(post|article)\s+(explores|discusses|examines)',
    r'^Today,?\s+(I|we)\s+(want\s+to|would\s+like\s+to)',
    r"^Let['']s\s+dive\s+into",
    r'^Have\s+you\s+ever\s+wondered',
]

# AI claim patterns (need evidence)
AI_CLAIMS = [
    r'AI\s+(can|will|is\s+able\s+to)\s+\w+',
    r'models?\s+(understand|learn|think|reason)',
    r'\d+%\s+(improvement|accuracy|performance)',
    r'breakthrough\s+in\s+AI',
    r'revolutionary\s+AI',
    r'AI\s+is\s+transforming'
]

# AI anthropomorphism to flag
AI_ANTHROPOMORPHISM = [
    r'\b(wants|desires|believes|feels|thinks|knows)\b',
    r'AI\s+(agent|model)\s+(wants|desires|believes|understands)',
    r'the\s+model\s+(decided|chose|preferred)',
]

class BlogPost:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.content = Path(filepath).read_text(encoding='utf-8')
        self.lines = self.content.split('\n')
        self.word_count = len(self.content.split())
        self.parse_frontmatter()

    def parse_frontmatter(self):
        """Extract frontmatter metadata"""
        if self.content.startswith('---'):
            parts = self.content.split('---', 2)
            if len(parts) >= 3:
                self.frontmatter = parts[1]
                self.body = parts[2]
                # Extract title
                title_match = re.search(r'title:\s*["\']?(.+?)["\']?\s*$', self.frontmatter, re.MULTILINE)
                self.title = title_match.group(1) if title_match else self.filename
                # Extract tags
                tags_match = re.search(r'tags:\s*\[(.+?)\]', self.frontmatter)
                self.tags = [t.strip().strip('"\'') for t in tags_match.group(1).split(',')] if tags_match else []
            else:
                self.frontmatter = ""
                self.body = self.content
                self.title = self.filename
                self.tags = []
        else:
            self.frontmatter = ""
            self.body = self.content
            self.title = self.filename
            self.tags = []

    def is_ai_related(self) -> bool:
        """Check if post is AI-related based on tags and content"""
        ai_keywords = ['ai', 'ml', 'machine learning', 'llm', 'neural', 'deep learning',
                       'artificial intelligence', 'transformer', 'gpt', 'claude']

        # Check tags
        for tag in self.tags:
            if any(keyword in tag.lower() for keyword in ai_keywords):
                return True

        # Check title
        if any(keyword in self.title.lower() for keyword in ai_keywords):
            return True

        return False

class ComplianceAnalyzer:
    def __init__(self, posts_dir: str):
        self.posts_dir = posts_dir
        self.posts = []
        self.results = []

    def load_posts(self):
        """Load all blog posts"""
        posts_path = Path(self.posts_dir)
        md_files = sorted(posts_path.glob('*.md'))

        for filepath in md_files:
            try:
                post = BlogPost(str(filepath))
                self.posts.append(post)
            except Exception as e:
                print(f"Error loading {filepath}: {e}")

        print(f"Loaded {len(self.posts)} blog posts")

    def score_smart_brevity(self, post: BlogPost) -> Tuple[int, List[str]]:
        """Score post on Smart Brevity compliance (1-10)"""
        score = 10
        violations = []

        # Check for BLUF (Bottom Line Up Front)
        first_paragraph = post.body.strip().split('\n\n')[0] if post.body.strip() else ""
        if len(first_paragraph.split()) > 100:
            score -= 2
            violations.append("Opening paragraph too long (>100 words) - no BLUF")

        # Check for throat-clearing
        for i, line in enumerate(post.lines[:10], 1):
            for pattern in THROAT_CLEARING:
                if re.search(pattern, line, re.IGNORECASE):
                    score -= 1
                    violations.append(f"Line {i}: Throat-clearing detected: '{line.strip()}'")

        # Check word count
        if post.word_count > 2500:
            score -= 2
            violations.append(f"Very verbose: {post.word_count} words (recommend <2000)")
        elif post.word_count > 2000:
            score -= 1
            violations.append(f"Verbose: {post.word_count} words (recommend <2000)")

        # Check for bullet usage (should have some)
        bullet_lines = sum(1 for line in post.lines if re.match(r'^\s*[-*+]\s+', line))
        if bullet_lines == 0 and post.word_count > 500:
            score -= 1
            violations.append("No bullet points found - consider using lists")

        # Check average paragraph length
        paragraphs = [p for p in post.body.split('\n\n') if p.strip() and not p.strip().startswith('#')]
        if paragraphs:
            avg_para_words = sum(len(p.split()) for p in paragraphs) / len(paragraphs)
            if avg_para_words > 100:
                score -= 1
                violations.append(f"Paragraphs too long (avg {avg_para_words:.0f} words) - recommend <75")

        return max(1, score), violations

    def score_polite_linus(self, post: BlogPost) -> Tuple[int, List[str]]:
        """Score post on Polite Linus tone (1-10)"""
        score = 10
        violations = []

        # Check for corporate speak
        for i, line in enumerate(post.lines, 1):
            for pattern in CORPORATE_SPEAK:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    score -= 1
                    violations.append(f"Line {i}: Corporate speak: '{match.group()}'")

        # Check for excessive hedging
        hedging_patterns = [
            r'\bmight\s+possibly\b', r'\bperhaps\s+maybe\b',
            r'\bsort\s+of\s+kind\s+of\b', r'\bI\s+think\s+maybe\b'
        ]

        for i, line in enumerate(post.lines, 1):
            for pattern in hedging_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    score -= 0.5
                    violations.append(f"Line {i}: Excessive hedging: '{line.strip()[:80]}...'")

        # Check for passive voice (should be minimal)
        passive_pattern = r'\b(is|are|was|were|been|be)\s+\w+ed\b'
        passive_count = sum(1 for line in post.lines if re.search(passive_pattern, line))
        passive_ratio = passive_count / len(post.lines) if post.lines else 0

        if passive_ratio > 0.15:
            score -= 2
            violations.append(f"High passive voice ratio ({passive_ratio:.1%}) - be more direct")

        return max(1, int(score)), violations

    def score_ai_skepticism(self, post: BlogPost) -> Tuple[int, List[str]]:
        """Score AI-related posts on skepticism (1-10)"""
        if not post.is_ai_related():
            return 10, ["N/A - Not an AI-related post"]

        score = 10
        violations = []

        # Check for unsubstantiated AI claims
        for i, line in enumerate(post.lines, 1):
            for pattern in AI_CLAIMS:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    # Check if there's a citation nearby (within 2 lines)
                    has_citation = False
                    for j in range(max(0, i-2), min(len(post.lines), i+3)):
                        if re.search(r'\[\d+\]|\(http[s]?://|\[.*\]\(http', post.lines[j]):
                            has_citation = True
                            break

                    if not has_citation:
                        score -= 2
                        violations.append(f"Line {i}: Uncited AI claim: '{line.strip()[:80]}...'")

        # Check for anthropomorphism
        for i, line in enumerate(post.lines, 1):
            for pattern in AI_ANTHROPOMORPHISM:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    score -= 1
                    violations.append(f"Line {i}: AI anthropomorphism: '{match.group()}'")

        # Check for "AI will solve X" without caveats
        utopian_patterns = [
            r'AI\s+will\s+solve',
            r'AI\s+will\s+eliminate',
            r'AI\s+is\s+the\s+answer\s+to',
            r'with\s+AI,?\s+we\s+can\s+finally'
        ]

        for i, line in enumerate(post.lines, 1):
            for pattern in utopian_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    score -= 2
                    violations.append(f"Line {i}: Uncritical AI optimism: '{line.strip()[:80]}...'")

        return max(1, score), violations

    def analyze_all(self) -> Dict:
        """Analyze all posts and generate report"""
        stats = {
            'total_posts': len(self.posts),
            'ai_posts': 0,
            'avg_word_count': 0,
            'verbose_posts': [],  # >2000 words
            'avg_brevity_score': 0,
            'avg_tone_score': 0,
            'avg_skepticism_score': 0,
            'worst_offenders': [],
            'best_examples': []
        }

        total_words = 0
        brevity_scores = []
        tone_scores = []
        skepticism_scores = []

        for post in self.posts:
            # Calculate scores
            brevity_score, brevity_violations = self.score_smart_brevity(post)
            tone_score, tone_violations = self.score_polite_linus(post)
            skepticism_score, skepticism_violations = self.score_ai_skepticism(post)

            total_score = (brevity_score + tone_score + skepticism_score) / 3

            result = {
                'filename': post.filename,
                'title': post.title,
                'word_count': post.word_count,
                'is_ai_related': post.is_ai_related(),
                'scores': {
                    'smart_brevity': brevity_score,
                    'polite_linus': tone_score,
                    'ai_skepticism': skepticism_score,
                    'total': round(total_score, 1)
                },
                'violations': {
                    'smart_brevity': brevity_violations,
                    'polite_linus': tone_violations,
                    'ai_skepticism': skepticism_violations
                }
            }

            self.results.append(result)

            # Update stats
            total_words += post.word_count
            brevity_scores.append(brevity_score)
            tone_scores.append(tone_score)
            if post.is_ai_related():
                stats['ai_posts'] += 1
                skepticism_scores.append(skepticism_score)

            if post.word_count > 2000:
                stats['verbose_posts'].append({
                    'filename': post.filename,
                    'word_count': post.word_count
                })

        # Calculate averages
        stats['avg_word_count'] = total_words // len(self.posts) if self.posts else 0
        stats['avg_brevity_score'] = round(sum(brevity_scores) / len(brevity_scores), 1) if brevity_scores else 0
        stats['avg_tone_score'] = round(sum(tone_scores) / len(tone_scores), 1) if tone_scores else 0
        stats['avg_skepticism_score'] = round(sum(skepticism_scores) / len(skepticism_scores), 1) if skepticism_scores else 0

        # Sort by total score
        sorted_results = sorted(self.results, key=lambda x: x['scores']['total'])
        stats['worst_offenders'] = sorted_results[:10]
        stats['best_examples'] = sorted_results[-10:][::-1]

        return stats

    def generate_report(self, output_file: str):
        """Generate detailed markdown report"""
        stats = self.analyze_all()

        report = []
        report.append("# Blog Compliance Analysis Report")
        report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"\n**Total Posts Analyzed:** {stats['total_posts']}")
        report.append(f"**AI-Related Posts:** {stats['ai_posts']}")
        report.append("")

        # Executive Summary
        report.append("## Executive Summary")
        report.append("")
        report.append(f"- **Average Word Count:** {stats['avg_word_count']} words")
        report.append(f"- **Posts >2000 words:** {len(stats['verbose_posts'])} ({len(stats['verbose_posts'])/stats['total_posts']*100:.1f}%)")
        report.append(f"- **Average Smart Brevity Score:** {stats['avg_brevity_score']}/10")
        report.append(f"- **Average Polite Linus Score:** {stats['avg_tone_score']}/10")
        report.append(f"- **Average AI Skepticism Score:** {stats['avg_skepticism_score']}/10")
        report.append("")

        # Worst Offenders
        report.append("## Top 10 Posts Needing Improvement")
        report.append("")
        report.append("| Rank | Post | Word Count | Brevity | Tone | Skepticism | Total |")
        report.append("|------|------|------------|---------|------|------------|-------|")

        for i, result in enumerate(stats['worst_offenders'], 1):
            report.append(f"| {i} | {result['title'][:50]} | {result['word_count']} | "
                         f"{result['scores']['smart_brevity']}/10 | "
                         f"{result['scores']['polite_linus']}/10 | "
                         f"{result['scores']['ai_skepticism']}/10 | "
                         f"**{result['scores']['total']}/10** |")
        report.append("")

        # Best Examples
        report.append("## Top 10 Compliant Posts (Best Examples)")
        report.append("")
        report.append("| Rank | Post | Word Count | Brevity | Tone | Skepticism | Total |")
        report.append("|------|------|------------|---------|------|------------|-------|")

        for i, result in enumerate(stats['best_examples'], 1):
            report.append(f"| {i} | {result['title'][:50]} | {result['word_count']} | "
                         f"{result['scores']['smart_brevity']}/10 | "
                         f"{result['scores']['polite_linus']}/10 | "
                         f"{result['scores']['ai_skepticism']}/10 | "
                         f"**{result['scores']['total']}/10** |")
        report.append("")

        # Verbose Posts
        report.append("## Verbose Posts (>2000 words)")
        report.append("")
        for post in sorted(stats['verbose_posts'], key=lambda x: x['word_count'], reverse=True):
            report.append(f"- **{post['filename']}**: {post['word_count']} words")
        report.append("")

        # Detailed Violations
        report.append("## Detailed Violation Analysis")
        report.append("")

        for result in sorted(self.results, key=lambda x: x['scores']['total']):
            if result['scores']['total'] < 7:  # Only show posts scoring below 7
                report.append(f"### {result['title']}")
                report.append(f"**File:** `{result['filename']}`")
                report.append(f"**Word Count:** {result['word_count']}")
                report.append(f"**Scores:** Brevity: {result['scores']['smart_brevity']}/10, "
                             f"Tone: {result['scores']['polite_linus']}/10, "
                             f"Skepticism: {result['scores']['ai_skepticism']}/10")
                report.append("")

                if result['violations']['smart_brevity']:
                    report.append("**Smart Brevity Violations:**")
                    for v in result['violations']['smart_brevity']:
                        report.append(f"- {v}")
                    report.append("")

                if result['violations']['polite_linus']:
                    report.append("**Polite Linus Violations:**")
                    for v in result['violations']['polite_linus']:
                        report.append(f"- {v}")
                    report.append("")

                if result['violations']['ai_skepticism'] and result['violations']['ai_skepticism'][0] != "N/A - Not an AI-related post":
                    report.append("**AI Skepticism Violations:**")
                    for v in result['violations']['ai_skepticism']:
                        report.append(f"- {v}")
                    report.append("")

                report.append("---")
                report.append("")

        # Write report
        Path(output_file).write_text('\n'.join(report), encoding='utf-8')
        print(f"Report written to: {output_file}")

        # Also save JSON results
        json_file = output_file.replace('.md', '.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'stats': stats,
                'results': self.results,
                'generated_at': datetime.now().isoformat()
            }, f, indent=2)
        print(f"JSON data written to: {json_file}")

        return stats

def main():
    posts_dir = "/home/william/git/williamzujkowski.github.io/src/posts"
    output_file = "/home/william/git/williamzujkowski.github.io/docs/analysis/blog-compliance-report.md"

    analyzer = ComplianceAnalyzer(posts_dir)
    analyzer.load_posts()
    stats = analyzer.generate_report(output_file)

    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print(f"Total Posts: {stats['total_posts']}")
    print(f"Average Word Count: {stats['avg_word_count']}")
    print(f"Average Scores:")
    print(f"  - Smart Brevity: {stats['avg_brevity_score']}/10")
    print(f"  - Polite Linus: {stats['avg_tone_score']}/10")
    print(f"  - AI Skepticism: {stats['avg_skepticism_score']}/10")
    print(f"\nVerbose Posts (>2000 words): {len(stats['verbose_posts'])}")
    print("\nSee detailed report at:")
    print(f"  {output_file}")

if __name__ == "__main__":
    main()
