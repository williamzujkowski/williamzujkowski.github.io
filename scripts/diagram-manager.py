#!/usr/bin/env python3
"""
SCRIPT: diagram-manager.py
PURPOSE: Unified diagram and technical image management for blog posts
CATEGORY: image_management
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-09-20T15:30:00-04:00

DESCRIPTION:
    Consolidates functionality from multiple diagram scripts:
    - integrate-diagrams.py
    - add-tech-images.py
    - create-blog-diagrams.py
    - add-diagrams-to-live-posts.py

    This unified script handles all diagram-related operations including
    creation, integration, and management of technical diagrams for blog posts.

LLM_USAGE:
    python scripts/diagram-manager.py [command] [options]

COMMANDS:
    create    - Create new diagrams for posts
    integrate - Add diagrams to existing posts
    update    - Update existing diagrams
    validate  - Check diagram references
    optimize  - Optimize diagram files

ARGUMENTS:
    command (str): The operation to perform
    --post (str): Specific post to process
    --all (bool): Process all posts
    --type (str): Diagram type (mermaid, svg, png)
    --force (bool): Force regeneration
    --dry-run (bool): Preview changes without applying

EXAMPLES:
    # Create diagrams for a specific post
    python scripts/diagram-manager.py create --post="2024-03-15-claude-flow"

    # Integrate diagrams into all posts
    python scripts/diagram-manager.py integrate --all

    # Validate diagram references
    python scripts/diagram-manager.py validate --all

    # Optimize all diagram files
    python scripts/diagram-manager.py optimize --force

OUTPUT:
    - Creates/updates diagram files in src/assets/images/blog/diagrams/
    - Updates blog post content with diagram references
    - Generates report in reports/diagram-status.json

DEPENDENCIES:
    - Python 3.8+
    - Required: scripts/lib/common.py
    - Optional: Pillow for image optimization

RELATED_SCRIPTS:
    - scripts/lib/common.py: Shared utilities
    - scripts/generate-blog-hero-images.py: Hero image generation
    - scripts/optimize-blog-content.py: Content optimization

MANIFEST_REGISTRY: scripts/diagram-manager.py
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Import shared utilities from common library
sys.path.append(str(Path(__file__).parent))
from lib.common import (
    ManifestManager,
    TimeManager,
    FileHasher,
    FrontmatterParser,
    StandardsValidator,
    FileBackup,
    Logger,
    ensure_directory,
    read_json,
    write_json
)

class DiagramManager:
    """Unified diagram management for blog posts"""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.manifest = ManifestManager()
        self.posts_dir = Path("src/posts")
        self.diagrams_dir = Path("src/assets/images/blog/diagrams")
        self.report = {
            "generated": TimeManager.get_current_timestamp(),
            "posts_processed": 0,
            "diagrams_created": 0,
            "diagrams_updated": 0,
            "errors": []
        }

    def create_diagrams(self, post: Optional[str] = None, all_posts: bool = False) -> Dict:
        """Create diagrams for posts"""
        posts = self._get_posts_to_process(post, all_posts)

        for post_path in posts:
            try:
                self._create_diagram_for_post(post_path)
                self.report["posts_processed"] += 1
            except Exception as e:
                self.logger.error(f"Failed to create diagram for {post_path}: {e}")
                self.report["errors"].append({
                    "post": str(post_path),
                    "error": str(e)
                })

        return self.report

    def integrate_diagrams(self, post: Optional[str] = None, all_posts: bool = False) -> Dict:
        """Integrate diagrams into existing posts"""
        posts = self._get_posts_to_process(post, all_posts)

        for post_path in posts:
            try:
                self._integrate_diagram_into_post(post_path)
                self.report["posts_processed"] += 1
            except Exception as e:
                self.logger.error(f"Failed to integrate diagram for {post_path}: {e}")
                self.report["errors"].append({
                    "post": str(post_path),
                    "error": str(e)
                })

        return self.report

    def validate_diagrams(self, all_posts: bool = True) -> Dict:
        """Validate all diagram references"""
        validation_report = {
            "valid": [],
            "missing": [],
            "broken": [],
            "unused": []
        }

        # Check all posts for diagram references
        for post_path in self.posts_dir.glob("*.md"):
            with open(post_path, 'r') as f:
                content = f.read()

            # Look for diagram references
            if "diagrams/" in content:
                referenced_diagrams = self._extract_diagram_references(content)
                for diagram_ref in referenced_diagrams:
                    diagram_path = Path("src") / diagram_ref.lstrip('/')
                    if diagram_path.exists():
                        validation_report["valid"].append(str(diagram_ref))
                    else:
                        validation_report["missing"].append({
                            "post": str(post_path),
                            "diagram": str(diagram_ref)
                        })

        # Check for unused diagrams
        existing_diagrams = list(self.diagrams_dir.glob("*"))
        referenced_diagrams = set(validation_report["valid"])

        for diagram_path in existing_diagrams:
            relative_path = f"/assets/images/blog/diagrams/{diagram_path.name}"
            if relative_path not in referenced_diagrams:
                validation_report["unused"].append(str(diagram_path))

        return validation_report

    def optimize_diagrams(self, force: bool = False) -> Dict:
        """Optimize diagram files"""
        optimization_report = {
            "optimized": [],
            "skipped": [],
            "errors": []
        }

        ensure_directory(self.diagrams_dir)

        for diagram_path in self.diagrams_dir.glob("*"):
            try:
                if self._should_optimize(diagram_path, force):
                    original_size = diagram_path.stat().st_size
                    self._optimize_diagram_file(diagram_path)
                    new_size = diagram_path.stat().st_size

                    optimization_report["optimized"].append({
                        "file": str(diagram_path),
                        "original_size": original_size,
                        "new_size": new_size,
                        "saved": original_size - new_size
                    })
                else:
                    optimization_report["skipped"].append(str(diagram_path))

            except Exception as e:
                optimization_report["errors"].append({
                    "file": str(diagram_path),
                    "error": str(e)
                })

        return optimization_report

    def _get_posts_to_process(self, post: Optional[str], all_posts: bool) -> List[Path]:
        """Get list of posts to process"""
        if post:
            post_path = self.posts_dir / f"{post}.md"
            if not post_path.exists():
                # Try to find by partial match
                matches = list(self.posts_dir.glob(f"*{post}*.md"))
                if matches:
                    return matches[:1]
                else:
                    self.logger.warning(f"Post not found: {post}")
                    return []
            return [post_path]
        elif all_posts:
            return list(self.posts_dir.glob("*.md"))
        else:
            return []

    def _create_diagram_for_post(self, post_path: Path):
        """Create diagram for a specific post"""
        with open(post_path, 'r') as f:
            content = f.read()

        frontmatter, body = FrontmatterParser.parse(content)

        # Analyze content to determine appropriate diagram type
        diagram_type = self._determine_diagram_type(body, frontmatter.get('tags', []))

        # Generate diagram content based on post
        diagram_content = self._generate_diagram_content(body, diagram_type)

        if diagram_content and not self.dry_run:
            # Save diagram
            diagram_filename = f"{post_path.stem}-diagram.{diagram_type}"
            diagram_path = self.diagrams_dir / diagram_filename

            ensure_directory(self.diagrams_dir)

            with open(diagram_path, 'w') as f:
                f.write(diagram_content)

            self.report["diagrams_created"] += 1
            self.logger.info(f"Created diagram: {diagram_path}")

            # Register in manifest
            self.manifest.register_file(
                diagram_path,
                purpose=f"Technical diagram for {post_path.stem}"
            )

    def _integrate_diagram_into_post(self, post_path: Path):
        """Integrate diagram into post content"""
        with open(post_path, 'r') as f:
            content = f.read()

        frontmatter, body = FrontmatterParser.parse(content)

        # Check if diagram exists
        diagram_path = self.diagrams_dir / f"{post_path.stem}-diagram.svg"
        if not diagram_path.exists():
            diagram_path = self.diagrams_dir / f"{post_path.stem}-diagram.png"

        if diagram_path.exists():
            # Add diagram reference to frontmatter
            if 'images' not in frontmatter:
                frontmatter['images'] = {}

            if 'diagrams' not in frontmatter['images']:
                frontmatter['images']['diagrams'] = []

            diagram_ref = f"/assets/images/blog/diagrams/{diagram_path.name}"

            if diagram_ref not in [d.get('src') for d in frontmatter['images'].get('diagrams', [])]:
                frontmatter['images']['diagrams'].append({
                    'src': diagram_ref,
                    'alt': f"Technical diagram for {frontmatter.get('title', post_path.stem)}",
                    'caption': 'System architecture and workflow diagram'
                })

                if not self.dry_run:
                    # Update post
                    new_content = FrontmatterParser.serialize(frontmatter, body)

                    # Backup original
                    FileBackup.create_backup(post_path)

                    with open(post_path, 'w') as f:
                        f.write(new_content)

                    self.report["diagrams_updated"] += 1
                    self.logger.info(f"Integrated diagram into: {post_path}")

    def _extract_diagram_references(self, content: str) -> List[str]:
        """Extract diagram references from content"""
        import re

        references = []

        # Match image references
        pattern = r'!\[.*?\]\((/assets/images/blog/diagrams/[^)]+)\)'
        matches = re.findall(pattern, content)
        references.extend(matches)

        # Match src references in frontmatter
        pattern = r'src:\s*["\']?(/assets/images/blog/diagrams/[^"\']+)'
        matches = re.findall(pattern, content)
        references.extend(matches)

        return list(set(references))

    def _determine_diagram_type(self, content: str, tags: List[str]) -> str:
        """Determine appropriate diagram type based on content"""
        content_lower = content.lower()

        # Check for specific patterns
        if 'architecture' in content_lower or 'system' in content_lower:
            return 'svg'
        elif 'workflow' in content_lower or 'process' in content_lower:
            return 'mermaid'
        elif 'network' in content_lower or 'topology' in content_lower:
            return 'svg'
        elif 'ai' in tags or 'ml' in tags:
            return 'svg'
        else:
            return 'png'

    def _generate_diagram_content(self, content: str, diagram_type: str) -> str:
        """Generate diagram content based on post content"""
        if diagram_type == 'mermaid':
            # Generate Mermaid diagram syntax
            return self._generate_mermaid_diagram(content)
        elif diagram_type == 'svg':
            # Generate SVG diagram
            return self._generate_svg_diagram(content)
        else:
            # For PNG, we'd need to use an image generation library
            return ""

    def _generate_mermaid_diagram(self, content: str) -> str:
        """Generate Mermaid diagram syntax"""
        # Basic template - would be enhanced with content analysis
        return """graph TD
    A[Start] --> B{Process}
    B --> C[Step 1]
    B --> D[Step 2]
    C --> E[Result]
    D --> E
    E --> F[End]
"""

    def _generate_svg_diagram(self, content: str) -> str:
        """Generate SVG diagram"""
        # Basic SVG template
        return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600">
    <rect x="10" y="10" width="780" height="580" fill="none" stroke="#333" stroke-width="2"/>
    <text x="400" y="50" text-anchor="middle" font-size="24" font-weight="bold">System Architecture</text>
    <!-- Additional elements would be generated based on content -->
</svg>"""

    def _should_optimize(self, path: Path, force: bool) -> bool:
        """Check if file should be optimized"""
        if force:
            return True

        # Check if already optimized (could check metadata or filename pattern)
        return not path.stem.endswith('-optimized')

    def _optimize_diagram_file(self, path: Path):
        """Optimize a diagram file"""
        import subprocess

        if path.suffix == '.png':
            # Use optipng
            subprocess.run(['optipng', '-o2', str(path)], capture_output=True)
        elif path.suffix == '.svg':
            # Use svgo if available
            try:
                subprocess.run(['svgo', str(path), '-o', str(path)], capture_output=True)
            except FileNotFoundError:
                self.logger.warning("svgo not found, skipping SVG optimization")

    def save_report(self, report_path: Optional[Path] = None):
        """Save report to file"""
        if report_path is None:
            ensure_directory(Path("reports"))
            report_path = Path("reports/diagram-status.json")

        write_json(self.report, report_path)
        self.logger.info(f"Report saved to: {report_path}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Unified diagram and technical image management for blog posts",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('command',
                       choices=['create', 'integrate', 'update', 'validate', 'optimize'],
                       help='Operation to perform')
    parser.add_argument('--post', help='Specific post to process')
    parser.add_argument('--all', action='store_true', help='Process all posts')
    parser.add_argument('--type', choices=['mermaid', 'svg', 'png'],
                       help='Diagram type')
    parser.add_argument('--force', action='store_true',
                       help='Force regeneration/optimization')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview changes without applying')

    args = parser.parse_args()

    # Initialize manager
    manager = DiagramManager(dry_run=args.dry_run)

    # Execute command
    if args.command == 'create':
        report = manager.create_diagrams(post=args.post, all_posts=args.all)
    elif args.command == 'integrate':
        report = manager.integrate_diagrams(post=args.post, all_posts=args.all)
    elif args.command == 'validate':
        report = manager.validate_diagrams(all_posts=True)
    elif args.command == 'optimize':
        report = manager.optimize_diagrams(force=args.force)
    else:
        # Update command would combine create and integrate
        report = manager.create_diagrams(post=args.post, all_posts=args.all)
        report.update(manager.integrate_diagrams(post=args.post, all_posts=args.all))

    # Save report
    if not args.dry_run:
        manager.save_report()

    # Print summary
    print(f"\n{'='*60}")
    print(f"Diagram Manager - {args.command.capitalize()} Complete")
    print(f"{'='*60}")

    if args.command in ['create', 'integrate', 'update']:
        print(f"Posts processed: {report.get('posts_processed', 0)}")
        print(f"Diagrams created: {report.get('diagrams_created', 0)}")
        print(f"Diagrams updated: {report.get('diagrams_updated', 0)}")

    elif args.command == 'validate':
        print(f"Valid references: {len(report.get('valid', []))}")
        print(f"Missing diagrams: {len(report.get('missing', []))}")
        print(f"Broken references: {len(report.get('broken', []))}")
        print(f"Unused diagrams: {len(report.get('unused', []))}")

    elif args.command == 'optimize':
        print(f"Files optimized: {len(report.get('optimized', []))}")
        print(f"Files skipped: {len(report.get('skipped', []))}")

    if report.get('errors'):
        print(f"\n⚠️  Errors encountered: {len(report['errors'])}")
        for error in report['errors'][:5]:
            print(f"  - {error}")

    print(f"{'='*60}\n")

    # Update manifest
    if not args.dry_run:
        manager.manifest.save()

    return 0 if not report.get('errors') else 1


if __name__ == "__main__":
    sys.exit(main())