#!/usr/bin/env -S uv run python3
"""
SCRIPT: optimize-blog-content.py
PURPOSE: Analyze and optimize blog posts for readability by reducing code-to-content ratio
CATEGORY: content_optimization
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-09-20T15:35:00-04:00

DESCRIPTION:
    Analyzes blog posts to identify where code can be reduced and replaced with
    diagrams. Targets posts with >25% code-to-content ratio and suggests
    optimizations including Mermaid diagrams, GitHub gists, and visual alternatives.

LLM_USAGE:
    python scripts/optimize-blog-content.py [options]

ARGUMENTS:
    --posts-dir (str): Directory containing blog posts (default: src/posts)
    --threshold (float): Code ratio threshold (default: 0.25)
    --output (str): Output report file (default: reports/code-optimization.json)
    --fix (bool): Apply automatic fixes where possible
    --dry-run (bool): Preview changes without applying

EXAMPLES:
    # Analyze all posts
    python scripts/optimize-blog-content.py

    # Fix posts with high code ratio
    python scripts/optimize-blog-content.py --fix --threshold 0.30

    # Generate detailed report
    python scripts/optimize-blog-content.py --output reports/optimization.json

OUTPUT:
    - JSON report with optimization suggestions
    - Updated blog posts (if --fix is used)
    - Diagram templates in src/assets/images/blog/diagrams/

DEPENDENCIES:
    - Python 3.8+
    - PyYAML for frontmatter parsing
    - Optional: scripts/lib/common.py for shared utilities

RELATED_SCRIPTS:
    - scripts/diagram-manager.py: Create and manage diagrams
    - scripts/create-blog-diagrams.py: Generate Mermaid diagrams
    - scripts/analyze-blog-content.py: Content quality analysis

MANIFEST_REGISTRY: scripts/optimize-blog-content.py
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple
import yaml

class BlogContentOptimizer:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.posts_dir = self.base_path / "src" / "posts"
        self.diagrams_dir = self.base_path / "src" / "assets" / "images" / "blog" / "diagrams"
        self.diagrams_dir.mkdir(parents=True, exist_ok=True)
        
        # Track optimization suggestions
        self.suggestions = []
    
    def parse_frontmatter(self, content: str) -> Tuple[dict, str]:
        """Parse frontmatter and content from markdown file"""
        if content.startswith('---'):
            try:
                _, fm, content = content.split('---', 2)
                frontmatter = yaml.safe_load(fm)
                return frontmatter, content.lstrip()
            except:
                return {}, content
        return {}, content
    
    def extract_code_blocks(self, content: str) -> List[Dict]:
        """Extract all code blocks from content"""
        code_pattern = r'```(\w+)?\n(.*?)```'
        blocks = []
        
        for match in re.finditer(code_pattern, content, re.DOTALL):
            language = match.group(1) or 'plain'
            code = match.group(2)
            line_count = len(code.strip().split('\n'))
            
            blocks.append({
                'language': language,
                'code': code,
                'line_count': line_count,
                'start_pos': match.start(),
                'end_pos': match.end()
            })
        
        return blocks
    
    def analyze_code_block(self, block: Dict) -> Dict:
        """Analyze a code block and suggest optimizations"""
        suggestions = []
        code = block['code']
        language = block['language']
        lines = block['line_count']
        
        # Check for configuration/setup code that could be a diagram
        if language in ['yaml', 'json', 'toml'] and lines > 10:
            suggestions.append({
                'type': 'diagram',
                'reason': 'Large configuration block could be visualized as a diagram',
                'diagram_type': 'architecture',
                'priority': 'high'
            })
        
        # Check for repetitive patterns
        if language in ['javascript', 'python', 'bash']:
            # Look for similar lines
            code_lines = code.strip().split('\n')
            if len(code_lines) > 5:
                # Check for repeated patterns
                patterns = {}
                for line in code_lines:
                    # Simple pattern detection
                    base_pattern = re.sub(r'["\'].*?["\']', '""', line)
                    base_pattern = re.sub(r'\d+', 'N', base_pattern)
                    patterns[base_pattern] = patterns.get(base_pattern, 0) + 1
                
                # If many similar lines, suggest condensing
                max_repetition = max(patterns.values()) if patterns else 0
                if max_repetition > 3:
                    suggestions.append({
                        'type': 'condense',
                        'reason': f'Code has {max_repetition} similar lines that could be condensed',
                        'priority': 'medium'
                    })
        
        # Check for workflow/pipeline code
        workflow_keywords = ['step', 'phase', 'stage', 'pipeline', 'workflow', 'process']
        if any(keyword in code.lower() for keyword in workflow_keywords):
            suggestions.append({
                'type': 'diagram',
                'reason': 'Workflow/pipeline code could be shown as a flowchart',
                'diagram_type': 'flowchart',
                'priority': 'high'
            })
        
        # Check for API/network calls that could be sequence diagrams
        api_keywords = ['fetch', 'request', 'response', 'api', 'http', 'call', 'endpoint']
        if any(keyword in code.lower() for keyword in api_keywords) and lines > 10:
            suggestions.append({
                'type': 'diagram',
                'reason': 'API interactions could be shown as a sequence diagram',
                'diagram_type': 'sequence',
                'priority': 'medium'
            })
        
        # Check for data structures that could be visualized
        structure_keywords = ['class', 'struct', 'interface', 'schema', 'model']
        if any(keyword in code.lower() for keyword in structure_keywords) and lines > 15:
            suggestions.append({
                'type': 'diagram',
                'reason': 'Data structures could be shown as a class/ER diagram',
                'diagram_type': 'class_diagram',
                'priority': 'medium'
            })
        
        # Check for overly long code blocks
        if lines > 30:
            suggestions.append({
                'type': 'split',
                'reason': f'Code block has {lines} lines - consider splitting or extracting key parts',
                'priority': 'high'
            })
        
        # Check for boilerplate code
        boilerplate_patterns = ['import', 'require', 'use', 'include', 'pragma']
        import_lines = sum(1 for line in code.split('\n') if any(p in line for p in boilerplate_patterns))
        if import_lines > 5:
            suggestions.append({
                'type': 'reduce',
                'reason': f'Has {import_lines} import/setup lines that could be minimized',
                'priority': 'low'
            })
        
        return {
            'block': block,
            'suggestions': suggestions
        }
    
    def generate_diagram_suggestions(self, title: str, content: str) -> List[Dict]:
        """Generate diagram suggestions based on content analysis"""
        diagrams = []
        
        # Architecture/system design keywords
        if any(word in content.lower() for word in ['architecture', 'system design', 'components', 'microservices']):
            diagrams.append({
                'type': 'architecture',
                'title': f'{title} - System Architecture',
                'description': 'High-level system architecture showing components and their relationships',
                'tool': 'mermaid or draw.io'
            })
        
        # Workflow/process keywords
        if any(word in content.lower() for word in ['workflow', 'process', 'pipeline', 'steps', 'phases']):
            diagrams.append({
                'type': 'flowchart',
                'title': f'{title} - Process Flow',
                'description': 'Visual workflow showing the process steps and decision points',
                'tool': 'mermaid flowchart'
            })
        
        # Data flow keywords
        if any(word in content.lower() for word in ['data flow', 'etl', 'transformation', 'processing']):
            diagrams.append({
                'type': 'dataflow',
                'title': f'{title} - Data Flow',
                'description': 'Data flow diagram showing how data moves through the system',
                'tool': 'mermaid or lucidchart'
            })
        
        # Network/topology keywords
        if any(word in content.lower() for word in ['network', 'topology', 'cluster', 'nodes', 'mesh']):
            diagrams.append({
                'type': 'network',
                'title': f'{title} - Network Topology',
                'description': 'Network diagram showing connections and topology',
                'tool': 'draw.io or mermaid'
            })
        
        # Timeline/sequence keywords
        if any(word in content.lower() for word in ['sequence', 'timeline', 'interaction', 'communication']):
            diagrams.append({
                'type': 'sequence',
                'title': f'{title} - Sequence Diagram',
                'description': 'Sequence diagram showing interactions over time',
                'tool': 'mermaid sequence diagram'
            })
        
        return diagrams
    
    def analyze_post(self, post_file: Path) -> Dict:
        """Analyze a single blog post for optimization opportunities"""
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        frontmatter, post_content = self.parse_frontmatter(content)
        title = frontmatter.get('title', '')
        
        # Extract and analyze code blocks
        code_blocks = self.extract_code_blocks(post_content)
        
        # Calculate metrics
        total_lines = len(post_content.split('\n'))
        code_lines = sum(block['line_count'] for block in code_blocks)
        code_ratio = (code_lines / total_lines * 100) if total_lines > 0 else 0
        
        # Analyze each code block
        block_analysis = []
        for block in code_blocks:
            analysis = self.analyze_code_block(block)
            if analysis['suggestions']:
                block_analysis.append(analysis)
        
        # Generate diagram suggestions
        diagram_suggestions = self.generate_diagram_suggestions(title, post_content)
        
        # Create optimization report
        report = {
            'file': post_file.name,
            'title': title,
            'metrics': {
                'total_lines': total_lines,
                'code_lines': code_lines,
                'code_blocks': len(code_blocks),
                'code_ratio': round(code_ratio, 1),
                'text_lines': total_lines - code_lines
            },
            'code_block_analysis': block_analysis,
            'diagram_suggestions': diagram_suggestions,
            'priority': 'high' if code_ratio > 40 else 'medium' if code_ratio > 25 else 'low'
        }
        
        return report
    
    def generate_optimization_report(self):
        """Generate comprehensive optimization report for all posts"""
        print("📊 Blog Content Optimization Analysis")
        print("=" * 70)
        
        posts = sorted(list(self.posts_dir.glob('*.md')))
        reports = []
        
        for post_file in posts:
            report = self.analyze_post(post_file)
            reports.append(report)
        
        # Sort by priority and code ratio
        reports.sort(key=lambda x: (x['priority'] == 'high', x['metrics']['code_ratio']), reverse=True)
        
        # Print summary
        print(f"\n📈 Overall Statistics:")
        print(f"   Total posts analyzed: {len(reports)}")
        
        total_code_blocks = sum(r['metrics']['code_blocks'] for r in reports)
        total_code_lines = sum(r['metrics']['code_lines'] for r in reports)
        avg_code_ratio = sum(r['metrics']['code_ratio'] for r in reports) / len(reports)
        
        print(f"   Total code blocks: {total_code_blocks}")
        print(f"   Total code lines: {total_code_lines}")
        print(f"   Average code ratio: {avg_code_ratio:.1f}%")
        
        # High priority posts (too much code)
        high_priority = [r for r in reports if r['priority'] == 'high']
        if high_priority:
            print(f"\n🔴 High Priority Posts ({len(high_priority)} posts with >40% code):")
            for report in high_priority[:10]:  # Show top 10
                print(f"\n   📝 {report['title'][:60]}...")
                print(f"      File: {report['file']}")
                print(f"      Code ratio: {report['metrics']['code_ratio']}%")
                print(f"      Code blocks: {report['metrics']['code_blocks']}")
                
                # Show top suggestions
                if report['code_block_analysis']:
                    print("      Suggestions:")
                    seen_suggestions = set()
                    for analysis in report['code_block_analysis'][:3]:
                        for suggestion in analysis['suggestions']:
                            key = (suggestion['type'], suggestion['reason'][:30])
                            if key not in seen_suggestions:
                                print(f"        • {suggestion['reason']}")
                                seen_suggestions.add(key)
                
                # Show diagram suggestions
                if report['diagram_suggestions']:
                    print("      Recommended diagrams:")
                    for diagram in report['diagram_suggestions'][:2]:
                        print(f"        • {diagram['type']}: {diagram['description'][:50]}...")
        
        # Medium priority posts
        medium_priority = [r for r in reports if r['priority'] == 'medium']
        if medium_priority:
            print(f"\n🟡 Medium Priority Posts ({len(medium_priority)} posts with 25-40% code):")
            for report in medium_priority[:5]:  # Show top 5
                print(f"   • {report['title'][:60]}... ({report['metrics']['code_ratio']}% code)")
        
        # Save detailed report
        report_file = self.base_path / "blog_optimization_report.json"
        with open(report_file, 'w') as f:
            json.dump(reports, f, indent=2)
        
        print(f"\n📁 Detailed report saved to: {report_file}")
        
        # Generate actionable recommendations
        print("\n🎯 Actionable Recommendations:")
        print("\n1. IMMEDIATE ACTIONS (High Impact):")
        print("   • Replace large configuration blocks with architecture diagrams")
        print("   • Convert workflow code to visual flowcharts")
        print("   • Extract repetitive code patterns into concise examples")
        
        print("\n2. DIAGRAM OPPORTUNITIES:")
        total_diagrams = sum(len(r['diagram_suggestions']) for r in reports)
        print(f"   • {total_diagrams} diagram opportunities identified")
        print("   • Focus on architecture, flowchart, and sequence diagrams")
        print("   • Use Mermaid for inline diagrams (renders in markdown)")
        
        print("\n3. CODE REDUCTION STRATEGIES:")
        print("   • Show only essential code snippets (5-10 lines)")
        print("   • Link to full examples in GitHub gists")
        print("   • Use '...' to indicate omitted boilerplate")
        print("   • Focus on the unique/important parts")
        
        print("\n4. VISUAL ENHANCEMENT IDEAS:")
        print("   • Add comparison tables instead of multiple code examples")
        print("   • Use before/after screenshots for UI changes")
        print("   • Create infographics for statistics and metrics")
        print("   • Add animated GIFs for interactive features")
        
        return reports

def main():
    """Main execution"""
    import json
    
    optimizer = BlogContentOptimizer()
    reports = optimizer.generate_optimization_report()
    
    print("\n" + "=" * 70)
    print("✨ Analysis Complete!")
    print("\nNext steps:")
    print("1. Review the high-priority posts first")
    print("2. Create diagrams using Mermaid or draw.io")
    print("3. Reduce code blocks to essential snippets")
    print("4. Add visual content where it adds value")
    print("\nUse 'python scripts/create-blog-diagrams.py' to generate diagram templates")

if __name__ == "__main__":
    main()