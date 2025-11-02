#!/usr/bin/env -S uv run python3
"""
Validate Mermaid diagram syntax in all blog posts.

This script:
1. Finds all Mermaid code blocks in posts
2. Validates basic syntax (proper fencing, valid diagram types, common errors)
3. Reports issues with file locations and suggested fixes
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Any

# Valid Mermaid diagram types
VALID_DIAGRAM_TYPES = {
    'graph', 'flowchart', 'sequenceDiagram', 'classDiagram',
    'stateDiagram', 'erDiagram', 'gantt', 'pie', 'gitGraph',
    'journey', 'requirementDiagram', 'quadrantChart', 'timeline'
}

# Common syntax patterns that cause issues
PROBLEMATIC_PATTERNS = [
    (r'[^\\][{}\[\]<>()]', 'Unescaped special characters in node labels'),
    (r'--+(?!>|[-|])', 'Invalid arrow syntax (missing > or proper connection)'),
    (r'^\s*subgraph\s+[^"\w]', 'Subgraph name must be quoted or alphanumeric'),
    (r'^\s*end\s+\S', 'end keyword must be on its own line'),
]

def extract_mermaid_blocks(content: str, filepath: Path) -> List[Dict[str, Any]]:
    """Extract all Mermaid code blocks from markdown content."""
    blocks = []
    lines = content.split('\n')
    in_mermaid = False
    current_block = []
    start_line = 0

    for i, line in enumerate(lines, 1):
        if line.strip() == '```mermaid':
            in_mermaid = True
            start_line = i
            current_block = []
        elif line.strip() == '```' and in_mermaid:
            blocks.append({
                'content': '\n'.join(current_block),
                'start_line': start_line,
                'end_line': i,
                'filepath': filepath
            })
            in_mermaid = False
            current_block = []
        elif in_mermaid:
            current_block.append(line)

    return blocks

def validate_mermaid_block(block: Dict[str, Any]) -> List[Dict[str, str]]:
    """Validate a single Mermaid block and return list of errors."""
    errors = []
    content = block['content'].strip()

    if not content:
        errors.append({
            'type': 'EMPTY_BLOCK',
            'message': 'Empty Mermaid block',
            'line': block['start_line']
        })
        return errors

    # Check for valid diagram type
    first_line = content.split('\n')[0].strip()
    diagram_type = first_line.split()[0] if first_line.split() else ''

    if diagram_type not in VALID_DIAGRAM_TYPES:
        errors.append({
            'type': 'INVALID_DIAGRAM_TYPE',
            'message': f'Invalid or missing diagram type: "{diagram_type}"',
            'line': block['start_line'] + 1,
            'suggestion': f'Valid types: {", ".join(sorted(VALID_DIAGRAM_TYPES))}'
        })

    # Check for common syntax issues
    for line_num, line in enumerate(content.split('\n'), 1):
        for pattern, description in PROBLEMATIC_PATTERNS:
            if re.search(pattern, line):
                errors.append({
                    'type': 'SYNTAX_ERROR',
                    'message': description,
                    'line': block['start_line'] + line_num,
                    'content': line.strip()
                })

    # Check for balanced quotes
    for line_num, line in enumerate(content.split('\n'), 1):
        # Count unescaped quotes
        quote_count = line.count('"') - line.count('\\"')
        if quote_count % 2 != 0:
            errors.append({
                'type': 'UNBALANCED_QUOTES',
                'message': 'Unbalanced quotes in line',
                'line': block['start_line'] + line_num,
                'content': line.strip()
            })

    # Check for proper subgraph structure
    if 'subgraph' in content:
        subgraph_count = content.count('subgraph')
        end_count = len([line for line in content.split('\n') if line.strip() == 'end'])
        if subgraph_count != end_count:
            errors.append({
                'type': 'SUBGRAPH_MISMATCH',
                'message': f'Subgraph/end mismatch: {subgraph_count} subgraphs but {end_count} ends',
                'line': block['start_line']
            })

    return errors

def validate_posts_directory(posts_dir: Path) -> Dict[str, List]:
    """Validate all Mermaid blocks in posts directory."""
    all_issues = {}
    post_count = 0
    block_count = 0

    for post_file in sorted(posts_dir.glob('*.md')):
        content = post_file.read_text(encoding='utf-8')
        blocks = extract_mermaid_blocks(content, post_file)

        if blocks:
            post_count += 1
            block_count += len(blocks)

            for block in blocks:
                errors = validate_mermaid_block(block)
                if errors:
                    if str(post_file) not in all_issues:
                        all_issues[str(post_file)] = []
                    all_issues[str(post_file)].extend(errors)

    print(f"\n📊 Scan Summary:")
    print(f"  - Posts scanned: {len(list(posts_dir.glob('*.md')))}")
    print(f"  - Posts with Mermaid: {post_count}")
    print(f"  - Total Mermaid blocks: {block_count}")
    print(f"  - Files with issues: {len(all_issues)}")

    return all_issues

def main():
    """Main validation entry point."""
    print("🔍 Validating Mermaid diagram syntax...\n")

    repo_root = Path(__file__).parent.parent.parent
    posts_dir = repo_root / 'src' / 'posts'

    if not posts_dir.exists():
        print(f"❌ Posts directory not found: {posts_dir}")
        sys.exit(1)

    issues = validate_posts_directory(posts_dir)

    if not issues:
        print("\n✅ All Mermaid diagrams validated successfully!")
        return 0

    print(f"\n⚠️  Found issues in {len(issues)} files:\n")

    for filepath, errors in sorted(issues.items()):
        rel_path = Path(filepath).relative_to(repo_root)
        print(f"\n📄 {rel_path}")
        print("=" * 80)

        for error in errors:
            print(f"\n  Line {error['line']}: {error['type']}")
            print(f"  ├─ {error['message']}")
            if 'content' in error:
                print(f"  ├─ Content: {error['content']}")
            if 'suggestion' in error:
                print(f"  └─ Suggestion: {error['suggestion']}")

    print(f"\n\n❌ Validation failed with {sum(len(e) for e in issues.values())} total errors")
    return 1

if __name__ == '__main__':
    sys.exit(main())
