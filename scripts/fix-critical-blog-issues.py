#!/usr/bin/env python3
"""
Fix critical blog issues based on uses page as source of truth
"""

import os
import re
import frontmatter
from pathlib import Path
from typing import Dict, List

class BlogFixer:
    def __init__(self, posts_dir: str = "src/posts"):
        self.posts_dir = Path(posts_dir)
        self.fixes_applied = []
        
    def fix_hardware_references(self, content: str) -> str:
        """Fix incorrect hardware/software references based on uses page."""
        
        # Hardware fixes
        replacements = [
            # Firewall - most common error
            (r'\bpfSense\b', 'Dream Machine Professional'),
            (r'\bPfSense\b', 'Dream Machine Professional'),
            (r'\bpfsense\b', 'Dream Machine Professional'),
            
            # RAM corrections
            (r'32GB(?:\s+of)?\s+RAM', '64GB RAM'),
            (r'32\s+GB\s+RAM', '64GB RAM'),
            
            # GPU corrections
            (r'RTX\s+3080', 'RTX 3090'),
            (r'GeForce\s+RTX\s+3080', 'NVIDIA RTX 3090'),
            
            # CPU corrections
            (r'i7-\d+K?', 'i9-9900K'),
            (r'Core\s+i7', 'Core i9-9900K'),
            
            # Hypervisor corrections
            (r'ESXi', 'Proxmox'),
            (r'VMware\s+ESXi', 'Proxmox'),
            (r'vSphere', 'Proxmox'),
            
            # Password manager corrections
            (r'LastPass', 'Bitwarden (self-hosted)'),
            (r'1Password', 'Bitwarden (self-hosted)'),
            
            # Pi corrections
            (r'Raspberry\s+Pi\s+5\s+8GB', 'Raspberry Pi 5 16GB'),
            (r'8GB\s+Pi\s+5', '16GB Pi 5'),
            
            # Container corrections
            (r'Docker\s+only', 'Docker and Podman'),
            (r'just\s+Docker', 'Docker and Podman'),
        ]
        
        modified = content
        for pattern, replacement in replacements:
            if re.search(pattern, modified):
                modified = re.sub(pattern, replacement, modified)
                self.fixes_applied.append(f"Replaced '{pattern}' with '{replacement}'")
        
        return modified
    
    def add_requirements_info(self, content: str) -> str:
        """Add requirements.txt info for Python code blocks."""
        
        # Check if Python imports exist without requirements mention
        if 'import' in content and 'requirements' not in content.lower():
            # Find Python code blocks with imports
            code_blocks = re.findall(r'```python\n(.*?)```', content, re.DOTALL)
            
            imports_found = set()
            for block in code_blocks:
                # Extract import statements
                import_lines = re.findall(r'^(?:from|import)\s+(\w+)', block, re.MULTILINE)
                for imp in import_lines:
                    if imp not in ['os', 'sys', 'json', 'time', 'datetime', 're', 'pathlib']:
                        imports_found.add(imp)
            
            if imports_found:
                # Add requirements section before the first code block
                requirements_text = f"""
## Requirements

To run the code examples in this post, you'll need to install the following packages:

```bash
pip install {' '.join(sorted(imports_found))}
```

Or create a `requirements.txt` file:

```text
{chr(10).join(sorted(imports_found))}
```
"""
                # Insert after the first heading
                first_code_pos = content.find('```python')
                if first_code_pos > 0:
                    # Find the best place to insert (after intro, before first code)
                    sections = content[:first_code_pos].split('\n\n')
                    insert_pos = len('\n\n'.join(sections[:3])) + 2
                    content = content[:insert_pos] + requirements_text + content[insert_pos:]
                    self.fixes_applied.append(f"Added requirements section for: {', '.join(imports_found)}")
        
        return content
    
    def add_reputable_sources(self, content: str, tags: List[str]) -> str:
        """Add reputable sources to posts based on tags."""
        
        # Source mapping by tag
        sources = {
            'security': [
                '[NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)',
                '[OWASP Top 10](https://owasp.org/www-project-top-ten/)',
                '[SANS Reading Room](https://www.sans.org/reading-room/)',
            ],
            'ai': [
                '[Papers with Code](https://paperswithcode.com/)',
                '[arXiv AI Research](https://arxiv.org/list/cs.AI/recent)',
            ],
            'cloud': [
                '[CNCF Projects](https://www.cncf.io/projects/)',
                '[AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)',
            ],
            'networking': [
                '[Cloudflare Learning Center](https://www.cloudflare.com/learning/)',
                '[RFC Editor](https://www.rfc-editor.org/)',
            ],
            'docker': [
                '[Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)',
                '[OWASP Docker Security](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)',
            ],
            'kubernetes': [
                '[Kubernetes Documentation](https://kubernetes.io/docs/)',
                '[CNCF Kubernetes Security](https://www.cncf.io/blog/2021/11/09/kubernetes-security-best-practices/)',
            ],
        }
        
        # Check if sources section exists
        if '## Further Reading' not in content and '## Resources' not in content:
            relevant_sources = []
            
            for tag in tags:
                tag_lower = tag.lower()
                for source_tag, source_list in sources.items():
                    if source_tag in tag_lower or tag_lower in source_tag:
                        relevant_sources.extend(source_list[:2])  # Add top 2 sources
            
            if relevant_sources:
                # Remove duplicates while preserving order
                seen = set()
                unique_sources = []
                for source in relevant_sources:
                    if source not in seen:
                        seen.add(source)
                        unique_sources.append(source)
                
                # Add sources section at the end
                sources_section = "\n\n## Further Reading\n\nFor more in-depth information on the topics covered in this post:\n\n"
                sources_section += '\n'.join(f"- {source}" for source in unique_sources[:5])
                
                # Add before the closing if it exists, otherwise at the end
                if '---\n\n*' in content:
                    content = content.replace('---\n\n*', sources_section + '\n\n---\n\n*')
                else:
                    content += sources_section
                
                self.fixes_applied.append(f"Added {len(unique_sources)} reputable sources")
        
        return content
    
    def fix_post(self, post_path: Path) -> bool:
        """Fix a single blog post."""
        with open(post_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        original_content = post.content
        self.fixes_applied = []
        
        # Apply fixes
        post.content = self.fix_hardware_references(post.content)
        post.content = self.add_requirements_info(post.content)
        post.content = self.add_reputable_sources(post.content, post.metadata.get('tags', []))
        
        # Save if changes were made
        if post.content != original_content:
            with open(post_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(post))
            
            print(f"✅ Fixed: {post_path.name}")
            for fix in self.fixes_applied:
                print(f"   • {fix}")
            return True
        
        return False
    
    def fix_all_posts(self):
        """Fix all blog posts with critical issues."""
        posts_to_fix = [
            '2025-02-10-automating-home-network-security.md',
            '2025-02-24-continuous-learning-cybersecurity.md',
            '2025-03-10-raspberry-pi-security-projects.md',
            '2025-04-10-securing-personal-ai-experiments.md',
            '2025-04-24-building-secure-homelab-adventure.md',
            '2025-07-08-implementing-dns-over-https-home-networks.md',
        ]
        
        print("="*60)
        print("FIXING CRITICAL BLOG ISSUES")
        print("="*60)
        print(f"\nFixing {len(posts_to_fix)} posts with critical issues...\n")
        
        fixed_count = 0
        for post_name in posts_to_fix:
            post_path = self.posts_dir / post_name
            if post_path.exists():
                if self.fix_post(post_path):
                    fixed_count += 1
            else:
                print(f"⚠️  Post not found: {post_name}")
        
        print(f"\n{'='*60}")
        print(f"Fixed {fixed_count} posts successfully!")
        print("="*60)

def main():
    fixer = BlogFixer()
    fixer.fix_all_posts()

if __name__ == "__main__":
    main()