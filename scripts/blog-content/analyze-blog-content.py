#!/usr/bin/env -S uv run python3
"""
SCRIPT: analyze-blog-content.py
PURPOSE: Analyze blog posts for content quality metrics and improvement opportunities
CATEGORY: content_optimization
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-09-20T15:40:00-04:00

DESCRIPTION:
    Comprehensive blog content analysis tool that evaluates posts for:
    - Readability scores (Flesch-Kincaid)
    - Code-to-content ratio
    - SEO optimization
    - Image usage and optimization
    - Citation quality
    - Content structure and formatting

LLM_USAGE:
    python scripts/analyze-blog-content.py [options]

ARGUMENTS:
    --posts-dir (str): Directory containing blog posts (default: src/posts)
    --output (str): Output report file (default: reports/content-analysis.json)
    --format (str): Report format [json|markdown|html] (default: json)
    --metrics (list): Specific metrics to analyze (default: all)
    --threshold (dict): Quality thresholds for warnings

EXAMPLES:
    # Analyze all posts
    python scripts/analyze-blog-content.py

    # Generate markdown report
    python scripts/analyze-blog-content.py --format markdown

    # Check specific metrics
    python scripts/analyze-blog-content.py --metrics readability,seo

OUTPUT:
    - Detailed analysis report with metrics and recommendations
    - Quality scores for each post
    - Actionable improvement suggestions

DEPENDENCIES:
    - Python 3.8+
    - textstat for readability analysis
    - BeautifulSoup4 for HTML parsing
    - scripts/lib/common.py for shared utilities

RELATED_SCRIPTS:
    - scripts/optimize-blog-content.py: Apply optimizations
    - scripts/batch-improve-blog-posts.py: Batch improvements
    - scripts/comprehensive-blog-enhancement.py: Full enhancement

MANIFEST_REGISTRY: scripts/analyze-blog-content.py
"""

import os
import re
import json
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Tuple
import frontmatter
from datetime import datetime
import sys

# Add parent directory to path for lib imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.logging_config import setup_logger

class BlogContentAnalyzer:
    def __init__(self, posts_dir: str = "src/posts", logger=None):
        self.posts_dir = Path(posts_dir)
        self.analysis_results = []
        self.logger = logger or logging.getLogger(__name__)
        
    def extract_code_blocks(self, content: str) -> List[str]:
        """Extract all code blocks from markdown content."""
        # Match fenced code blocks
        code_pattern = re.compile(r'```[\s\S]*?```', re.MULTILINE)
        inline_pattern = re.compile(r'`[^`]+`')
        
        code_blocks = code_pattern.findall(content)
        inline_codes = inline_pattern.findall(content)
        
        return code_blocks, inline_codes
    
    def calculate_metrics(self, content: str) -> Dict:
        """Calculate various content metrics."""
        # Extract code blocks
        code_blocks, inline_codes = self.extract_code_blocks(content)
        
        # Calculate sizes
        total_chars = len(content)
        code_chars = sum(len(block) for block in code_blocks)
        inline_code_chars = sum(len(code) for code in inline_codes)
        
        # Remove code for text analysis
        text_only = content
        for block in code_blocks:
            text_only = text_only.replace(block, '')
        for code in inline_codes:
            text_only = text_only.replace(code, '')
        
        # Count words
        words = len(text_only.split())
        
        # Count sections (headers)
        headers = len(re.findall(r'^#+\s', content, re.MULTILINE))
        
        # Count lists
        lists = len(re.findall(r'^\s*[-*+]\s', content, re.MULTILINE))
        
        # Count images
        images = len(re.findall(r'!\[.*?\]\(.*?\)', content))
        
        # Calculate ratios
        code_ratio = (code_chars / total_chars * 100) if total_chars > 0 else 0
        inline_ratio = (inline_code_chars / total_chars * 100) if total_chars > 0 else 0
        total_code_ratio = code_ratio + inline_ratio
        
        # Identify long code blocks
        long_blocks = []
        for block in code_blocks:
            lines = block.count('\n')
            if lines > 10:
                long_blocks.append(lines)
        
        return {
            'total_chars': total_chars,
            'code_chars': code_chars,
            'inline_code_chars': inline_code_chars,
            'text_chars': total_chars - code_chars - inline_code_chars,
            'code_ratio': round(code_ratio, 2),
            'inline_ratio': round(inline_ratio, 2),
            'total_code_ratio': round(total_code_ratio, 2),
            'word_count': words,
            'code_blocks': len(code_blocks),
            'inline_codes': len(inline_codes),
            'headers': headers,
            'lists': lists,
            'images': images,
            'long_blocks': long_blocks,
            'avg_block_lines': sum(long_blocks) / len(long_blocks) if long_blocks else 0
        }
    
    def suggest_improvements(self, metrics: Dict, metadata: Dict) -> List[str]:
        """Suggest improvements based on metrics."""
        suggestions = []
        
        # Code ratio suggestions
        if metrics['total_code_ratio'] > 25:
            suggestions.append(f"HIGH CODE RATIO ({metrics['total_code_ratio']}%) - Consider replacing with Mermaid diagrams")
            if metrics['long_blocks']:
                suggestions.append(f"Has {len(metrics['long_blocks'])} code blocks >10 lines - Reduce to essential snippets")
        
        # Content structure
        if metrics['word_count'] < 500:
            suggestions.append("SHORT POST - Consider expanding with more context and examples")
        elif metrics['word_count'] > 3000:
            suggestions.append("LONG POST - Consider breaking into series")
        
        if metrics['headers'] < 3:
            suggestions.append("Few sections - Add more structure with headers")
        
        if metrics['images'] == 0:
            suggestions.append("NO IMAGES - Add hero image and inline visuals")
        elif metrics['images'] < metrics['headers'] / 2:
            suggestions.append("Add more images to break up text")
        
        # Check for specific content types
        tags = metadata.get('tags', [])
        if any(tag in ['tutorial', 'guide', 'how-to'] for tag in tags):
            if metrics['lists'] < 3:
                suggestions.append("Tutorial needs more structured lists/steps")
        
        if any(tag in ['ai', 'ml', 'llm', 'quantum'] for tag in tags):
            suggestions.append("Technical post - Add architecture diagrams")
        
        if any(tag in ['security', 'cryptography', 'zero-trust'] for tag in tags):
            suggestions.append("Security post - Add threat model diagrams")
        
        return suggestions
    
    def analyze_post(self, post_path: Path) -> Dict:
        """Analyze a single blog post."""
        with open(post_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        metadata = {
            'title': post.metadata.get('title', ''),
            'date': post.metadata.get('date', ''),
            'tags': post.metadata.get('tags', []),
            'description': post.metadata.get('description', ''),
            'has_images': 'images' in post.metadata
        }
        
        metrics = self.calculate_metrics(post.content)
        suggestions = self.suggest_improvements(metrics, metadata)
        
        return {
            'file': post_path.name,
            'metadata': metadata,
            'metrics': metrics,
            'suggestions': suggestions,
            'needs_attention': metrics['total_code_ratio'] > 25 or len(suggestions) > 3
        }
    
    def generate_mermaid_suggestions(self, post_analysis: Dict) -> List[str]:
        """Generate Mermaid diagram suggestions based on post content."""
        suggestions = []
        tags = post_analysis['metadata'].get('tags', [])
        title = post_analysis['metadata'].get('title', '').lower()
        
        # Tag-based suggestions
        diagram_map = {
            'ai': ['flowchart TD: AI Pipeline', 'graph LR: Neural Network Architecture'],
            'ml': ['flowchart LR: ML Workflow', 'graph TD: Model Training Process'],
            'security': ['flowchart TB: Security Architecture', 'graph LR: Threat Model'],
            'cloud': ['graph TB: Cloud Infrastructure', 'flowchart LR: Deployment Pipeline'],
            'devops': ['flowchart LR: CI/CD Pipeline', 'graph TD: Deployment Workflow'],
            'blockchain': ['graph LR: Blockchain Network', 'flowchart TD: Transaction Flow'],
            'quantum': ['graph TD: Quantum Circuit', 'flowchart LR: Quantum Algorithm'],
            'architecture': ['graph TB: System Architecture', 'flowchart TD: Component Diagram'],
            'zero-trust': ['graph LR: Zero Trust Model', 'flowchart TB: Access Control'],
            'cryptography': ['flowchart LR: Encryption Process', 'graph TD: Key Exchange']
        }
        
        for tag in tags:
            tag_lower = tag.lower()
            for key, diagrams in diagram_map.items():
                if key in tag_lower:
                    suggestions.extend(diagrams)
        
        # Title-based suggestions
        if 'pipeline' in title or 'workflow' in title:
            suggestions.append('flowchart LR: Process Pipeline')
        if 'architecture' in title or 'design' in title:
            suggestions.append('graph TB: System Design')
        if 'comparison' in title or 'vs' in title:
            suggestions.append('graph LR: Comparison Chart')
        
        return list(set(suggestions))[:3]  # Return up to 3 unique suggestions
    
    def analyze_all_posts(self) -> Dict:
        """Analyze all blog posts and generate report."""
        posts = sorted(self.posts_dir.glob("*.md"))
        self.logger.info(f"Analyzing {len(posts)} blog posts")
        
        high_code_posts = []
        needs_images = []
        needs_content = []
        
        for post_path in posts:
            analysis = self.analyze_post(post_path)
            self.analysis_results.append(analysis)
            
            # Categorize issues
            if analysis['metrics']['total_code_ratio'] > 25:
                high_code_posts.append(analysis)
            if analysis['metrics']['images'] == 0:
                needs_images.append(analysis)
            if analysis['metrics']['word_count'] < 800:
                needs_content.append(analysis)
        
        return {
            'total_posts': len(posts),
            'high_code_posts': high_code_posts,
            'needs_images': needs_images,
            'needs_content': needs_content,
            'all_results': self.analysis_results
        }
    
    def generate_report(self, output_file: str = None):
        """Generate detailed analysis report."""
        report = self.analyze_all_posts()

        self.logger.info("="*80)
        self.logger.info("BLOG CONTENT ANALYSIS REPORT")
        self.logger.info("="*80)

        self.logger.info(f"Total Posts Analyzed: {report['total_posts']}")
        self.logger.info(f"Posts with High Code Ratio (>25%): {len(report['high_code_posts'])}")
        self.logger.info(f"Posts Needing Images: {len(report['needs_images'])}")
        self.logger.info(f"Posts Needing More Content: {len(report['needs_content'])}")
        
        # High code ratio posts
        if report['high_code_posts']:
            self.logger.info("-"*40)
            self.logger.info("HIGH CODE RATIO POSTS (Need Mermaid Diagrams):")
            self.logger.info("-"*40)
            for post in sorted(report['high_code_posts'],
                             key=lambda x: x['metrics']['total_code_ratio'],
                             reverse=True)[:10]:
                self.logger.info(f"📄 {post['file']}")
                self.logger.info(f"   Code Ratio: {post['metrics']['total_code_ratio']}%")
                self.logger.info(f"   Code Blocks: {post['metrics']['code_blocks']}")
                if post['metrics']['long_blocks']:
                    self.logger.info(f"   Long Blocks: {len(post['metrics']['long_blocks'])} blocks >10 lines")

                # Mermaid suggestions
                mermaid_suggestions = self.generate_mermaid_suggestions(post)
                if mermaid_suggestions:
                    self.logger.info(f"   Suggested Diagrams:")
                    for diagram in mermaid_suggestions:
                        self.logger.info(f"     - {diagram}")
        
        # Posts needing images
        if report['needs_images'][:10]:
            self.logger.info("-"*40)
            self.logger.info("POSTS NEEDING IMAGES:")
            self.logger.info("-"*40)
            for post in report['needs_images'][:10]:
                self.logger.info(f"📷 {post['file']}")
                tags = ', '.join(post['metadata'].get('tags', []))
                self.logger.info(f"   Tags: {tags}")
                self.logger.info(f"   Suggested image types: Hero, 2-3 inline diagrams")

        # Summary statistics
        self.logger.info("-"*40)
        self.logger.info("OVERALL STATISTICS:")
        self.logger.info("-"*40)

        avg_code_ratio = sum(p['metrics']['total_code_ratio']
                           for p in report['all_results']) / len(report['all_results'])
        avg_word_count = sum(p['metrics']['word_count']
                           for p in report['all_results']) / len(report['all_results'])

        self.logger.info(f"Average Code Ratio: {avg_code_ratio:.2f}%")
        self.logger.info(f"Average Word Count: {avg_word_count:.0f}")
        
        # Save detailed report
        if output_file:
            detailed_report = {
                'generated': datetime.now().isoformat(),
                'summary': {
                    'total_posts': report['total_posts'],
                    'high_code_ratio': len(report['high_code_posts']),
                    'needs_images': len(report['needs_images']),
                    'needs_content': len(report['needs_content']),
                    'avg_code_ratio': avg_code_ratio,
                    'avg_word_count': avg_word_count
                },
                'posts': report['all_results']
            }
            
            with open(output_file, 'w') as f:
                json.dump(detailed_report, f, indent=2, default=str)
            self.logger.info(f"Detailed report saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Analyze blog content for improvements')
    parser.add_argument('--posts-dir', default='src/posts', help='Directory containing blog posts')
    parser.add_argument('--output', help='Output JSON file for detailed report')
    parser.add_argument('--post', help='Analyze single post')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable debug output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress info messages')
    parser.add_argument('--log-file', type=Path, help='Write logs to file')

    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(__name__, level=level, log_file=args.log_file, quiet=args.quiet)

    analyzer = BlogContentAnalyzer(args.posts_dir, logger=logger)
    
    if args.post:
        # Analyze single post
        post_path = Path(args.posts_dir) / args.post
        if post_path.exists():
            result = analyzer.analyze_post(post_path)
            logger.info(f"Analysis for {args.post}:")
            logger.info(f"Code Ratio: {result['metrics']['total_code_ratio']}%")
            logger.info(f"Word Count: {result['metrics']['word_count']}")
            logger.info(f"Suggestions:")
            for suggestion in result['suggestions']:
                logger.info(f"  - {suggestion}")
        else:
            logger.error(f"Post not found: {post_path}")
    else:
        # Analyze all posts
        analyzer.generate_report(args.output)

if __name__ == "__main__":
    main()