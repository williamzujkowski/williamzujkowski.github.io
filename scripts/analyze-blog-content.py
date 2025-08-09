#!/usr/bin/env python3
"""
Blog Content Analyzer
Analyzes blog posts for code-to-content ratio, readability, and improvement opportunities
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
import frontmatter
from datetime import datetime

class BlogContentAnalyzer:
    def __init__(self, posts_dir: str = "src/posts"):
        self.posts_dir = Path(posts_dir)
        self.analysis_results = []
        
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
        print(f"Analyzing {len(posts)} blog posts...")
        
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
        
        print("\n" + "="*80)
        print("BLOG CONTENT ANALYSIS REPORT")
        print("="*80)
        
        print(f"\nTotal Posts Analyzed: {report['total_posts']}")
        print(f"Posts with High Code Ratio (>25%): {len(report['high_code_posts'])}")
        print(f"Posts Needing Images: {len(report['needs_images'])}")
        print(f"Posts Needing More Content: {len(report['needs_content'])}")
        
        # High code ratio posts
        if report['high_code_posts']:
            print("\n" + "-"*40)
            print("HIGH CODE RATIO POSTS (Need Mermaid Diagrams):")
            print("-"*40)
            for post in sorted(report['high_code_posts'], 
                             key=lambda x: x['metrics']['total_code_ratio'], 
                             reverse=True)[:10]:
                print(f"\n📄 {post['file']}")
                print(f"   Code Ratio: {post['metrics']['total_code_ratio']}%")
                print(f"   Code Blocks: {post['metrics']['code_blocks']}")
                if post['metrics']['long_blocks']:
                    print(f"   Long Blocks: {len(post['metrics']['long_blocks'])} blocks >10 lines")
                
                # Mermaid suggestions
                mermaid_suggestions = self.generate_mermaid_suggestions(post)
                if mermaid_suggestions:
                    print(f"   Suggested Diagrams:")
                    for diagram in mermaid_suggestions:
                        print(f"     - {diagram}")
        
        # Posts needing images
        if report['needs_images'][:10]:
            print("\n" + "-"*40)
            print("POSTS NEEDING IMAGES:")
            print("-"*40)
            for post in report['needs_images'][:10]:
                print(f"\n📷 {post['file']}")
                tags = ', '.join(post['metadata'].get('tags', []))
                print(f"   Tags: {tags}")
                print(f"   Suggested image types: Hero, 2-3 inline diagrams")
        
        # Summary statistics
        print("\n" + "-"*40)
        print("OVERALL STATISTICS:")
        print("-"*40)
        
        avg_code_ratio = sum(p['metrics']['total_code_ratio'] 
                           for p in report['all_results']) / len(report['all_results'])
        avg_word_count = sum(p['metrics']['word_count'] 
                           for p in report['all_results']) / len(report['all_results'])
        
        print(f"Average Code Ratio: {avg_code_ratio:.2f}%")
        print(f"Average Word Count: {avg_word_count:.0f}")
        
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
            print(f"\nDetailed report saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Analyze blog content for improvements')
    parser.add_argument('--posts-dir', default='src/posts', help='Directory containing blog posts')
    parser.add_argument('--output', help='Output JSON file for detailed report')
    parser.add_argument('--post', help='Analyze single post')
    
    args = parser.parse_args()
    
    analyzer = BlogContentAnalyzer(args.posts_dir)
    
    if args.post:
        # Analyze single post
        post_path = Path(args.posts_dir) / args.post
        if post_path.exists():
            result = analyzer.analyze_post(post_path)
            print(f"\nAnalysis for {args.post}:")
            print(f"Code Ratio: {result['metrics']['total_code_ratio']}%")
            print(f"Word Count: {result['metrics']['word_count']}")
            print(f"Suggestions:")
            for suggestion in result['suggestions']:
                print(f"  - {suggestion}")
        else:
            print(f"Post not found: {post_path}")
    else:
        # Analyze all posts
        analyzer.generate_report(args.output)

if __name__ == "__main__":
    main()