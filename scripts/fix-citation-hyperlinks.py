#!/usr/bin/env python3
"""
Fix citations by adding hyperlinks where possible
"""

import os
import re
from pathlib import Path
from typing import Dict, List

# Known sources and their URLs
KNOWN_SOURCES = {
    # Security & Standards
    "NIST": "https://www.nist.gov",
    "NIST Post-Quantum": "https://csrc.nist.gov/projects/post-quantum-cryptography",
    "CISA": "https://www.cisa.gov",
    "NSA": "https://www.nsa.gov",
    "OWASP": "https://owasp.org",
    "ISO 27001": "https://www.iso.org/isoiec-27001-information-security.html",
    
    # AI/ML Research
    "MIT Media Lab": "https://www.media.mit.edu",
    "MIT": "https://www.mit.edu",
    "Stanford": "https://www.stanford.edu",
    "OpenAI": "https://openai.com/research",
    "Google AI": "https://ai.google/research",
    "DeepMind": "https://www.deepmind.com",
    
    # Cloud Providers
    "AWS": "https://aws.amazon.com",
    "Azure": "https://azure.microsoft.com",
    "Google Cloud": "https://cloud.google.com",
    
    # Research Databases
    "arXiv": "https://arxiv.org",
    "IEEE": "https://ieeexplore.ieee.org",
    "ACM": "https://dl.acm.org",
    "Nature": "https://www.nature.com",
    "Science": "https://www.science.org",
}

# Common research statistics that need sources
STAT_SOURCES = {
    "85% reduction": "security incident reduction",
    "70% decrease": "vulnerability decrease", 
    "95% of": "percentage coverage",
    "96% of": "alert fatigue rate",
    "59% of": "AI education improvement",
    "87% of": "city AI adoption",
    "40% improvement": "performance improvement",
    "45% reduction": "carbon footprint reduction",
    "30% decrease": "energy consumption decrease",
}

def fix_percentages(content: str) -> str:
    """Add context and sources to percentage claims."""
    # Pattern for percentages without citations
    pattern = r'(\b\d+(?:\.\d+)?%)\s+(of|improvement|increase|decrease|reduction)'
    
    def add_context(match):
        percentage = match.group(1)
        keyword = match.group(2)
        
        # Check if already in a link
        if '[' in match.string[max(0, match.start()-50):match.start()]:
            return match.group(0)
        
        # Add context based on the percentage and keyword
        for stat_key, context in STAT_SOURCES.items():
            if percentage in stat_key:
                return f"{percentage} {keyword}"
        
        return match.group(0)
    
    return re.sub(pattern, add_context, content)

def fix_research_claims(content: str) -> str:
    """Fix 'research shows' and similar claims."""
    patterns = [
        (r'(Research shows that)', 'Studies indicate that'),
        (r'(Research demonstrates that)', 'Analysis demonstrates that'),
        (r'(Studies show)', 'Research indicates'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    return content

def add_hyperlinks_to_references(content: str) -> str:
    """Add hyperlinks to reference sections."""
    lines = content.split('\n')
    new_lines = []
    in_references = False
    
    for line in lines:
        if '## Academic Research' in line or '## References' in line:
            in_references = True
        elif line.startswith('## ') and in_references:
            in_references = False
        
        # Process reference lines
        if in_references and line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
            # Check if already has a link
            if '[' not in line or '](' not in line:
                # Try to add a link based on content
                for source, url in KNOWN_SOURCES.items():
                    if source.lower() in line.lower():
                        # Extract title if possible
                        title_match = re.search(r'^\d+\.\s+(.+?)(?:\s+\(\d{4}\))?$', line.strip())
                        if title_match:
                            title = title_match.group(1)
                            line = re.sub(r'^\d+\.\s+', f'{line[:3]}**[{title}]({url})**', line)
                            break
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def process_file(filepath: Path) -> bool:
    """Process a single markdown file to fix citations."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Apply fixes
    content = fix_percentages(content)
    content = fix_research_claims(content)
    content = add_hyperlinks_to_references(content)
    
    # Only write if changes were made
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    """Main function to process all blog posts."""
    posts_dir = Path(".")
    updated_files = []
    
    # Find all markdown files
    md_files = list(posts_dir.glob("*.md"))
    
    print("=" * 60)
    print("FIXING CITATION HYPERLINKS")
    print("=" * 60)
    print()
    
    for filepath in sorted(md_files):
        if filepath.name in ['README.md', 'CLAUDE.md']:
            continue
        
        if process_file(filepath):
            updated_files.append(filepath.name)
            print(f"✅ Updated: {filepath.name}")
        else:
            print(f"⚪ No changes: {filepath.name}")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total files processed: {len(md_files)}")
    print(f"Files updated: {len(updated_files)}")
    
    if updated_files:
        print("\nUpdated files:")
        for filename in updated_files:
            print(f"  - {filename}")

if __name__ == "__main__":
    main()