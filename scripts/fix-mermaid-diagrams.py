#!/usr/bin/env python3
"""
Fix Mermaid diagram syntax errors across all blog posts
"""

import re
import frontmatter
from pathlib import Path

def fix_quantum_mermaid(content):
    """Fix the quantum computing post's Mermaid diagram."""
    # Replace the problematic quantum notation with standard text
    old_diagram = """```mermaid
graph LR
    subgraph "Initialization"
        Q0[|0⟩]
        Q1[|0⟩]
    end
    
    subgraph "Gates"
        H[Hadamard]
        CNOT[CNOT]
        M[Measure]
    end
    
    subgraph "Output"
        C0[Classical Bit 0]
        C1[Classical Bit 1]
    end
    
    Q0 --> H
    H --> CNOT
    Q1 --> CNOT
    CNOT --> M
    M --> C0
    M --> C1
    
    style H fill:#2196f3
    style CNOT fill:#9c27b0
```"""

    new_diagram = """```mermaid
graph LR
    subgraph "Initialization"
        Q0[Qubit 0: Zero State]
        Q1[Qubit 1: Zero State]
    end
    
    subgraph "Quantum Gates"
        H[Hadamard Gate]
        CNOT[CNOT Gate]
        M[Measurement]
    end
    
    subgraph "Classical Output"
        C0[Classical Bit 0]
        C1[Classical Bit 1]
    end
    
    Q0 --> H
    H --> CNOT
    Q1 --> CNOT
    CNOT --> M
    M --> C0
    M --> C1
    
    style H fill:#2196f3
    style CNOT fill:#9c27b0
    style M fill:#4caf50
```"""
    
    if old_diagram in content:
        content = content.replace(old_diagram, new_diagram)
        return content, True
    return content, False

def scan_mermaid_diagrams(content):
    """Scan content for Mermaid diagrams and check for common issues."""
    mermaid_pattern = r'```mermaid\n(.*?)\n```'
    diagrams = re.findall(mermaid_pattern, content, re.DOTALL)
    
    issues = []
    for i, diagram in enumerate(diagrams, 1):
        # Check for special characters that Mermaid doesn't support
        if any(char in diagram for char in ['⟩', '⟨', '|0⟩', '|1⟩', '†', '⊗']):
            issues.append(f"Diagram {i}: Contains quantum notation characters")
        
        # Check for unescaped quotes in labels
        if re.search(r'[^\[]"[^\]]', diagram):
            issues.append(f"Diagram {i}: May have unescaped quotes")
        
        # Check for missing node definitions
        arrows = re.findall(r'(\w+)\s*-->', diagram)
        nodes = re.findall(r'(\w+)\[', diagram)
        undefined = set(arrows) - set(nodes)
        if undefined and undefined != {'subgraph', 'end', 'style', 'class'}:
            issues.append(f"Diagram {i}: Undefined nodes: {undefined}")
    
    return issues

def fix_common_mermaid_issues(content):
    """Fix common Mermaid syntax issues."""
    fixes_made = []
    
    # Fix special characters in Mermaid diagrams
    mermaid_pattern = r'(```mermaid\n.*?\n```)'
    
    def fix_diagram(match):
        diagram = match.group(1)
        original = diagram
        
        # Replace quantum notation
        replacements = {
            '|0⟩': 'Zero State',
            '|1⟩': 'One State',
            '|+⟩': 'Plus State',
            '|-⟩': 'Minus State',
            '⟨': '(',
            '⟩': ')',
            '†': 'dagger',
            '⊗': 'tensor',
            '∑': 'sum',
            '∏': 'product',
            '∫': 'integral',
            '∞': 'infinity',
            '≈': 'approx',
            '≠': 'not equal',
            '≤': 'less or equal',
            '≥': 'greater or equal',
            '→': '-->',
            '←': '<--',
            '↔': '<-->',
        }
        
        for old, new in replacements.items():
            if old in diagram:
                diagram = diagram.replace(old, new)
                if original != diagram:
                    fixes_made.append(f"Replaced '{old}' with '{new}'")
        
        return diagram
    
    content = re.sub(mermaid_pattern, fix_diagram, content, flags=re.DOTALL)
    
    return content, fixes_made

def process_post(post_path):
    """Process a single blog post for Mermaid fixes."""
    with open(post_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
    
    content = post.content
    original_content = content
    changes_made = []
    
    # Check for Mermaid diagrams
    if '```mermaid' not in content:
        return None
    
    print(f"\n📊 Processing: {post_path.name}")
    
    # Scan for issues
    issues = scan_mermaid_diagrams(content)
    if issues:
        print(f"  Issues found: {len(issues)}")
        for issue in issues:
            print(f"    - {issue}")
    
    # Apply specific fixes for quantum post
    if 'quantum-computing' in post_path.name:
        content, fixed = fix_quantum_mermaid(content)
        if fixed:
            changes_made.append("Fixed quantum notation in diagram")
    
    # Apply general fixes
    content, fixes = fix_common_mermaid_issues(content)
    changes_made.extend(fixes)
    
    # Save if changes were made
    if content != original_content:
        post.content = content
        with open(post_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        
        print(f"  ✅ Fixed {len(changes_made)} issues:")
        for change in changes_made[:5]:  # Show first 5 changes
            print(f"    - {change}")
        if len(changes_made) > 5:
            print(f"    ... and {len(changes_made) - 5} more")
        
        return {
            'file': post_path.name,
            'issues_found': len(issues),
            'fixes_applied': len(changes_made),
            'changes': changes_made
        }
    else:
        print(f"  ✓ No fixes needed")
        return None

def main():
    """Main function to fix all Mermaid diagrams."""
    print("="*60)
    print("FIXING MERMAID DIAGRAM SYNTAX ERRORS")
    print("="*60)
    
    posts_dir = Path('src/posts')
    posts = sorted(posts_dir.glob('*.md'))
    
    results = []
    posts_with_mermaid = 0
    posts_fixed = 0
    
    for post_path in posts:
        result = process_post(post_path)
        if result:
            results.append(result)
            posts_fixed += 1
            posts_with_mermaid += 1
        elif '```mermaid' in post_path.read_text():
            posts_with_mermaid += 1
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total posts scanned: {len(posts)}")
    print(f"Posts with Mermaid diagrams: {posts_with_mermaid}")
    print(f"Posts fixed: {posts_fixed}")
    
    if results:
        print("\n📝 Fixed posts:")
        for result in results:
            print(f"  - {result['file']}: {result['fixes_applied']} fixes")
    
    print("\n✅ Mermaid diagram fixes complete!")
    
    return results

if __name__ == "__main__":
    main()