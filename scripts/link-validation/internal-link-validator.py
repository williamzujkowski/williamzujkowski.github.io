#!/usr/bin/env -S uv run python3
"""
SCRIPT: internal-link-validator.py
PURPOSE: Internal Link Validator and Recommendation Engine
CATEGORY: link-validation
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-11-04

DESCRIPTION:
    Validates existing internal links and suggests new links based on research
    recommendations. Tracks implementation progress toward 6-10 links/post target.

LLM_USAGE:
    python scripts/link-validation/internal-link-validator.py [options]

ARGUMENTS:
    --validate: Validate all existing internal links
    --analyze: Count links per post and identify gaps
    --recommend: Show link recommendations
    --post SLUG: Filter recommendations by post slug
    --phase PHASE: Filter recommendations by implementation phase
    --priority PRIORITY: Filter recommendations by priority (P0, P1, P2)
    --batch: Run full analysis + recommendations
    --progress: Show implementation progress metrics
    --json: Output in JSON format
    --debug: Enable debug logging

EXAMPLES:
    # Validate all existing internal links
    python scripts/link-validation/internal-link-validator.py --validate

    # Analyze current state (count links per post)
    python scripts/link-validation/internal-link-validator.py --analyze

    # Show recommendations for specific post
    python scripts/link-validation/internal-link-validator.py --recommend --post 2025-04-24-building-secure-homelab-adventure

    # Show Phase 1 recommendations
    python scripts/link-validation/internal-link-validator.py --recommend --phase Phase_1

    # Show P0 priority recommendations
    python scripts/link-validation/internal-link-validator.py --recommend --priority P0

    # Full batch analysis
    python scripts/link-validation/internal-link-validator.py --batch

    # Check implementation progress
    python scripts/link-validation/internal-link-validator.py --progress

OUTPUT:
    - Link validation results (broken links, valid links)
    - Link count analysis per post
    - Prioritized recommendations
    - Implementation progress metrics

DEPENDENCIES:
    - Python 3.8+
    - frontmatter: Parse markdown frontmatter
    - rich: Terminal output formatting
    - tqdm: Progress bars
    - concurrent.futures: Parallel processing

RELATED_SCRIPTS:
    - scripts/lib/logging_config.py: Centralized logging
    - docs/reports/internal-link-recommendations.csv: Link recommendations

MANIFEST_REGISTRY: scripts/link-validation/internal-link-validator.py
"""

import argparse
import csv
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

# Setup logging FIRST (before other imports)
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

logger = setup_logger(__name__)

# Now import dependencies (with logging available for errors)
try:
    import frontmatter
    from rich.console import Console
    from rich.table import Table
    from rich.progress import track
    from tqdm import tqdm
except ImportError as e:
    logger.error(f"Missing required dependency: {e}")
    logger.error("Install with: uv pip install python-frontmatter rich tqdm")
    sys.exit(1)

console = Console()

VERSION = "2.0.0"

# Repository paths
REPO_ROOT = Path(__file__).parent.parent.parent
POSTS_DIR = REPO_ROOT / "src" / "posts"
RECOMMENDATIONS_CSV = REPO_ROOT / "docs" / "reports" / "internal-link-recommendations.csv"

# Target metrics (from research)
TARGET_LINKS_MIN = 6
TARGET_LINKS_MAX = 10
CURRENT_BASELINE = 27  # Starting point: 27 links across 63 posts
TARGET_TOTAL_MIN = 378  # 63 posts × 6 links
TARGET_TOTAL_MAX = 630  # 63 posts × 10 links


@dataclass
class InternalLink:
    """Represents an internal link found in a blog post."""
    source_post: str  # Slug of source post
    target_post: str  # Slug of target post
    anchor_text: str  # Link text
    line_number: int  # Line in markdown file
    is_valid: bool    # Does target exist?


@dataclass
class LinkRecommendation:
    """Represents a recommended internal link from CSV."""
    source_post: str
    source_title: str
    target_post: str
    target_title: str
    anchor_text: str
    link_type: str     # Hub→Hub, Hub→Spoke, etc.
    priority: str      # P0, P1, P2
    phase: str         # Phase_1, Phase_2, etc.
    rationale: str


@dataclass
class PostAnalysis:
    """Analysis results for a single post."""
    slug: str
    title: str
    link_count: int
    links: List[InternalLink]
    broken_links: int
    meets_target: bool
    gap: int  # How many links needed to reach minimum target


def extract_slug_from_filename(filepath: Path) -> str:
    """
    Extract post slug from filename.

    Args:
        filepath: Path to markdown file

    Returns:
        Post slug (e.g., "2025-04-24-building-secure-homelab-adventure")

    Examples:
        >>> extract_slug_from_filename(Path("2025-04-24-building-secure-homelab-adventure.md"))
        '2025-04-24-building-secure-homelab-adventure'
    """
    return filepath.stem


def extract_slug_from_url(url: str) -> str:
    """
    Extract post slug from internal link URL.

    Args:
        url: Internal link URL (e.g., "/posts/2025-04-24-building-secure-homelab-adventure")

    Returns:
        Post slug or empty string if not an internal post link

    Examples:
        >>> extract_slug_from_url("/posts/2025-04-24-building-secure-homelab-adventure")
        '2025-04-24-building-secure-homelab-adventure'
        >>> extract_slug_from_url("/posts/privacy-first-ai-lab-local-llms/")
        'privacy-first-ai-lab-local-llms'
    """
    # Match /posts/[slug] or /posts/[slug]/
    match = re.match(r'^/posts/([^/\)]+)/?', url)
    if match:
        return match.group(1)
    return ""


def parse_post(file_path: Path, all_post_slugs: Set[str]) -> PostAnalysis:
    """
    Parse markdown post and extract internal links.

    Args:
        file_path: Path to markdown file
        all_post_slugs: Set of all valid post slugs in the blog

    Returns:
        PostAnalysis object with link data

    Raises:
        IOError: If file cannot be read
        ValueError: If frontmatter is invalid
    """
    slug = extract_slug_from_filename(file_path)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            title = post.get('title', slug)
            content = post.content
    except Exception as e:
        logger.error(f"Failed to parse {file_path}: {e}")
        return PostAnalysis(
            slug=slug,
            title=slug,
            link_count=0,
            links=[],
            broken_links=0,
            meets_target=False,
            gap=TARGET_LINKS_MIN
        )

    # Find all internal links: [text](/posts/slug)
    link_pattern = re.compile(r'\[([^\]]+)\]\((/posts/[^\)]+)\)')
    links = []

    for line_num, line in enumerate(content.split('\n'), start=1):
        for match in link_pattern.finditer(line):
            anchor_text = match.group(1)
            url = match.group(2)
            target_slug = extract_slug_from_url(url)

            if target_slug:
                is_valid = target_slug in all_post_slugs
                links.append(InternalLink(
                    source_post=slug,
                    target_post=target_slug,
                    anchor_text=anchor_text,
                    line_number=line_num,
                    is_valid=is_valid
                ))

    link_count = len(links)
    broken_links = sum(1 for link in links if not link.is_valid)
    meets_target = link_count >= TARGET_LINKS_MIN
    gap = max(0, TARGET_LINKS_MIN - link_count)

    return PostAnalysis(
        slug=slug,
        title=title,
        link_count=link_count,
        links=links,
        broken_links=broken_links,
        meets_target=meets_target,
        gap=gap
    )


def get_all_post_slugs() -> Set[str]:
    """
    Get set of all valid post slugs in the blog.

    Returns:
        Set of post slugs

    Examples:
        >>> slugs = get_all_post_slugs()
        >>> '2025-04-24-building-secure-homelab-adventure' in slugs
        True
    """
    slugs = set()
    if not POSTS_DIR.exists():
        logger.error(f"Posts directory not found: {POSTS_DIR}")
        return slugs

    for post_file in POSTS_DIR.glob("*.md"):
        slugs.add(extract_slug_from_filename(post_file))

    logger.info(f"Found {len(slugs)} posts")
    return slugs


def load_recommendations() -> List[LinkRecommendation]:
    """
    Load link recommendations from CSV file.

    Returns:
        List of LinkRecommendation objects

    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If CSV format is invalid
    """
    if not RECOMMENDATIONS_CSV.exists():
        logger.error(f"Recommendations CSV not found: {RECOMMENDATIONS_CSV}")
        return []

    recommendations = []

    try:
        with open(RECOMMENDATIONS_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                recommendations.append(LinkRecommendation(
                    source_post=row['Source_Post_Slug'],
                    source_title=row['Source_Post_Title'],
                    target_post=row['Target_Post_Slug'],
                    target_title=row['Target_Post_Title'],
                    anchor_text=row['Anchor_Text_Suggestion'],
                    link_type=row['Link_Type'],
                    priority=row['Priority'],
                    phase=row['Implementation_Phase'],
                    rationale=row['Rationale']
                ))
    except Exception as e:
        logger.error(f"Failed to load recommendations: {e}")
        return []

    logger.info(f"Loaded {len(recommendations)} recommendations")
    return recommendations


def analyze_all_posts(parallel: bool = True) -> List[PostAnalysis]:
    """
    Analyze all blog posts for internal links.

    Args:
        parallel: Use parallel processing for faster analysis

    Returns:
        List of PostAnalysis objects
    """
    all_slugs = get_all_post_slugs()
    post_files = list(POSTS_DIR.glob("*.md"))

    if not post_files:
        logger.warning("No markdown files found in posts directory")
        return []

    results = []

    if parallel and len(post_files) > 10:
        # Parallel processing for large batches
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(parse_post, post_file, all_slugs): post_file
                for post_file in post_files
            }

            for future in tqdm(as_completed(futures), total=len(futures), desc="Analyzing posts"):
                try:
                    results.append(future.result())
                except Exception as e:
                    logger.error(f"Analysis failed: {e}")
    else:
        # Sequential processing
        for post_file in track(post_files, description="Analyzing posts"):
            results.append(parse_post(post_file, all_slugs))

    return sorted(results, key=lambda x: x.link_count, reverse=True)


def validate_links(analyses: List[PostAnalysis]) -> Dict:
    """
    Validate all internal links and generate report.

    Args:
        analyses: List of PostAnalysis objects

    Returns:
        Validation summary dict
    """
    total_links = sum(a.link_count for a in analyses)
    total_broken = sum(a.broken_links for a in analyses)
    posts_with_broken = sum(1 for a in analyses if a.broken_links > 0)

    broken_link_details = []
    for analysis in analyses:
        for link in analysis.links:
            if not link.is_valid:
                broken_link_details.append({
                    'source': analysis.slug,
                    'target': link.target_post,
                    'line': link.line_number,
                    'anchor': link.anchor_text
                })

    return {
        'total_links': total_links,
        'total_broken': total_broken,
        'posts_with_broken': posts_with_broken,
        'broken_links': broken_link_details
    }


def calculate_progress(analyses: List[PostAnalysis]) -> Dict:
    """
    Calculate implementation progress metrics.

    Args:
        analyses: List of PostAnalysis objects

    Returns:
        Progress metrics dict
    """
    total_posts = len(analyses)
    total_links = sum(a.link_count for a in analyses)
    posts_meeting_target = sum(1 for a in analyses if a.meets_target)

    # Distribution by link count
    no_links = sum(1 for a in analyses if a.link_count == 0)
    few_links = sum(1 for a in analyses if 1 <= a.link_count < TARGET_LINKS_MIN)
    meets_min = sum(1 for a in analyses if TARGET_LINKS_MIN <= a.link_count < TARGET_LINKS_MAX)
    exceeds_target = sum(1 for a in analyses if a.link_count >= TARGET_LINKS_MAX)

    return {
        'total_posts': total_posts,
        'total_links': total_links,
        'avg_links_per_post': total_links / total_posts if total_posts > 0 else 0,
        'target_min': TARGET_TOTAL_MIN,
        'target_max': TARGET_TOTAL_MAX,
        'progress_pct': (total_links / TARGET_TOTAL_MIN * 100) if TARGET_TOTAL_MIN > 0 else 0,
        'posts_meeting_target': posts_meeting_target,
        'posts_meeting_target_pct': (posts_meeting_target / total_posts * 100) if total_posts > 0 else 0,
        'distribution': {
            '0_links': no_links,
            '1-5_links': few_links,
            '6-9_links': meets_min,
            '10+_links': exceeds_target
        }
    }


def print_validation_report(validation: Dict, json_output: bool = False):
    """Print validation results."""
    if json_output:
        print(json.dumps(validation, indent=2))
        return

    console.print("\n[bold cyan]Internal Link Validation Report[/bold cyan]")
    console.print("=" * 60)
    console.print(f"\nTotal links: {validation['total_links']}")
    console.print(f"Broken links: [red]{validation['total_broken']}[/red]")
    console.print(f"Posts with broken links: {validation['posts_with_broken']}")

    if validation['broken_links']:
        console.print("\n[bold red]Broken Links:[/bold red]")
        table = Table(show_header=True)
        table.add_column("Source Post", style="cyan")
        table.add_column("Target (Missing)", style="red")
        table.add_column("Line", style="yellow")

        for link in validation['broken_links']:
            table.add_row(link['source'], link['target'], str(link['line']))

        console.print(table)
    else:
        console.print("\n[green]✓ All internal links are valid![/green]")


def print_analysis_report(analyses: List[PostAnalysis], json_output: bool = False):
    """Print analysis results."""
    if json_output:
        data = [asdict(a) for a in analyses]
        print(json.dumps(data, indent=2))
        return

    console.print("\n[bold cyan]Internal Link Analysis[/bold cyan]")
    console.print("=" * 60)

    table = Table(show_header=True)
    table.add_column("Post", style="cyan", width=40)
    table.add_column("Links", justify="right")
    table.add_column("Status", justify="center")
    table.add_column("Gap", justify="right")

    for analysis in analyses:
        status = "[green]✓[/green]" if analysis.meets_target else "[yellow]⚠[/yellow]"
        gap_str = f"+{analysis.gap}" if analysis.gap > 0 else "—"

        table.add_row(
            analysis.slug[:40],
            str(analysis.link_count),
            status,
            gap_str
        )

    console.print(table)


def print_recommendations(
    recommendations: List[LinkRecommendation],
    post_slug: Optional[str] = None,
    phase: Optional[str] = None,
    priority: Optional[str] = None,
    json_output: bool = False
):
    """Print link recommendations with optional filtering."""
    filtered = recommendations

    if post_slug:
        filtered = [r for r in filtered if r.source_post == post_slug]
    if phase:
        filtered = [r for r in filtered if r.phase == phase]
    if priority:
        filtered = [r for r in filtered if r.priority == priority]

    if json_output:
        data = [asdict(r) for r in filtered]
        print(json.dumps(data, indent=2))
        return

    if not filtered:
        console.print("[yellow]No recommendations match the filters.[/yellow]")
        return

    console.print(f"\n[bold cyan]Link Recommendations ({len(filtered)} total)[/bold cyan]")
    console.print("=" * 80)

    # Group by source post
    by_source = {}
    for rec in filtered:
        if rec.source_post not in by_source:
            by_source[rec.source_post] = []
        by_source[rec.source_post].append(rec)

    for source_slug, recs in by_source.items():
        console.print(f"\n[bold green]{source_slug}[/bold green]")
        console.print(f"[dim]{recs[0].source_title}[/dim]")

        # Group by priority
        p0 = [r for r in recs if r.priority == 'P0']
        p1 = [r for r in recs if r.priority == 'P1']
        p2 = [r for r in recs if r.priority == 'P2']

        for priority_group, label in [(p0, 'P0'), (p1, 'P1'), (p2, 'P2')]:
            if priority_group:
                console.print(f"\n  [bold]{label} Recommendations ({len(priority_group)}):[/bold]")
                for i, rec in enumerate(priority_group, 1):
                    console.print(f"    {i}. → {rec.target_title}")
                    console.print(f"       Anchor: \"{rec.anchor_text}\"")
                    console.print(f"       Type: {rec.link_type} | Phase: {rec.phase}")
                    console.print(f"       Rationale: {rec.rationale}")


def print_progress_report(progress: Dict, json_output: bool = False):
    """Print implementation progress report."""
    if json_output:
        print(json.dumps(progress, indent=2))
        return

    console.print("\n[bold cyan]Internal Link Implementation Progress[/bold cyan]")
    console.print("=" * 60)

    console.print("\n[bold]Current State:[/bold]")
    console.print(f"  Total links: {progress['total_links']} ({progress['avg_links_per_post']:.2f}/post)")
    console.print(f"  Target: {progress['target_min']} links ({TARGET_LINKS_MIN}/post minimum)")
    console.print(f"  Progress: [yellow]{progress['progress_pct']:.1f}% complete[/yellow] ({progress['total_links']}/{progress['target_min']})")

    console.print("\n[bold]Posts by Link Count:[/bold]")
    dist = progress['distribution']
    console.print(f"  0 links: {dist['0_links']} posts ({dist['0_links']/progress['total_posts']*100:.1f}%)")
    console.print(f"  1-5 links: {dist['1-5_links']} posts ({dist['1-5_links']/progress['total_posts']*100:.1f}%)")
    console.print(f"  6-9 links: {dist['6-9_links']} posts ({dist['6-9_links']/progress['total_posts']*100:.1f}%)")
    console.print(f"  10+ links: {dist['10+_links']} posts ({dist['10+_links']/progress['total_posts']*100:.1f}%)")

    console.print(f"\n[bold]Posts Meeting Target ({TARGET_LINKS_MIN}+ links):[/bold]")
    console.print(f"  {progress['posts_meeting_target']} / {progress['total_posts']} posts ({progress['posts_meeting_target_pct']:.1f}%)")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Internal Link Validator and Recommendation Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Validate all existing internal links:
    %(prog)s --validate

  Analyze current state:
    %(prog)s --analyze

  Show recommendations for specific post:
    %(prog)s --recommend --post 2025-04-24-building-secure-homelab-adventure

  Show Phase 1 recommendations:
    %(prog)s --recommend --phase Phase_1

  Show P0 priority recommendations:
    %(prog)s --recommend --priority P0

  Full batch analysis:
    %(prog)s --batch

  Check implementation progress:
    %(prog)s --progress
        """
    )

    parser.add_argument('--validate', action='store_true', help='Validate all existing internal links')
    parser.add_argument('--analyze', action='store_true', help='Count links per post and identify gaps')
    parser.add_argument('--recommend', action='store_true', help='Show link recommendations')
    parser.add_argument('--post', type=str, help='Filter recommendations by post slug')
    parser.add_argument('--phase', type=str, help='Filter recommendations by phase (e.g., Phase_1)')
    parser.add_argument('--priority', type=str, choices=['P0', 'P1', 'P2'], help='Filter by priority')
    parser.add_argument('--batch', action='store_true', help='Run full analysis + recommendations')
    parser.add_argument('--progress', action='store_true', help='Show implementation progress metrics')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')

    args = parser.parse_args()

    # Configure logging
    if args.debug:
        logger.setLevel('DEBUG')

    # Run appropriate command
    if args.validate or args.batch:
        analyses = analyze_all_posts()
        validation = validate_links(analyses)
        print_validation_report(validation, args.json)

    if args.analyze or args.batch:
        analyses = analyze_all_posts()
        print_analysis_report(analyses, args.json)

    if args.recommend or args.batch:
        recommendations = load_recommendations()
        print_recommendations(
            recommendations,
            post_slug=args.post,
            phase=args.phase,
            priority=args.priority,
            json_output=args.json
        )

    if args.progress or args.batch:
        analyses = analyze_all_posts()
        progress = calculate_progress(analyses)
        print_progress_report(progress, args.json)

    if not any([args.validate, args.analyze, args.recommend, args.progress, args.batch]):
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
