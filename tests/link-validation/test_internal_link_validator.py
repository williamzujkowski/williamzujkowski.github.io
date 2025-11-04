#!/usr/bin/env -S uv run python3
"""
Tests for internal-link-validator.py

Run with:
    pytest tests/link-validation/test_internal_link_validator.py -v
"""

import sys
from pathlib import Path
from textwrap import dedent
import tempfile
import csv

import pytest

# Add scripts to path
script_path = Path(__file__).parent.parent.parent / "scripts" / "link-validation"
sys.path.insert(0, str(script_path))

# Import as module using importlib
import importlib.util
spec = importlib.util.spec_from_file_location(
    "internal_link_validator",
    script_path / "internal-link-validator.py"
)
ilv = importlib.util.module_from_spec(spec)
sys.modules["internal_link_validator"] = ilv
spec.loader.exec_module(ilv)

# Now import from the loaded module
extract_slug_from_filename = ilv.extract_slug_from_filename
extract_slug_from_url = ilv.extract_slug_from_url
parse_post = ilv.parse_post
validate_links = ilv.validate_links
calculate_progress = ilv.calculate_progress
load_recommendations = ilv.load_recommendations
InternalLink = ilv.InternalLink
LinkRecommendation = ilv.LinkRecommendation
PostAnalysis = ilv.PostAnalysis
TARGET_LINKS_MIN = ilv.TARGET_LINKS_MIN
TARGET_LINKS_MAX = ilv.TARGET_LINKS_MAX


class TestSlugExtraction:
    """Test slug extraction functions."""

    def test_extract_slug_from_filename(self):
        """Test extracting slug from markdown filename."""
        filepath = Path("2025-04-24-building-secure-homelab-adventure.md")
        slug = extract_slug_from_filename(filepath)
        assert slug == "2025-04-24-building-secure-homelab-adventure"

    def test_extract_slug_from_filename_no_extension(self):
        """Test extracting slug from file without extension."""
        filepath = Path("2025-04-24-building-secure-homelab-adventure")
        slug = extract_slug_from_filename(filepath)
        assert slug == "2025-04-24-building-secure-homelab-adventure"

    def test_extract_slug_from_url_standard(self):
        """Test extracting slug from standard /posts/slug URL."""
        url = "/posts/2025-04-24-building-secure-homelab-adventure"
        slug = extract_slug_from_url(url)
        assert slug == "2025-04-24-building-secure-homelab-adventure"

    def test_extract_slug_from_url_trailing_slash(self):
        """Test extracting slug from URL with trailing slash."""
        url = "/posts/privacy-first-ai-lab-local-llms/"
        slug = extract_slug_from_url(url)
        assert slug == "privacy-first-ai-lab-local-llms"

    def test_extract_slug_from_url_invalid(self):
        """Test extracting slug from invalid URL returns empty string."""
        assert extract_slug_from_url("/about/") == ""
        assert extract_slug_from_url("https://example.com/posts/slug") == ""
        assert extract_slug_from_url("") == ""


class TestPostParsing:
    """Test markdown post parsing."""

    def test_parse_post_no_links(self):
        """Test parsing post with no internal links."""
        content = dedent("""
            ---
            title: Test Post
            date: 2025-01-01
            ---
            This is a test post with no internal links.

            It has some content but no [external links](https://example.com).
        """).strip()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            analysis = parse_post(temp_path, set())
            assert analysis.link_count == 0
            assert len(analysis.links) == 0
            assert analysis.broken_links == 0
            assert not analysis.meets_target
            assert analysis.gap == TARGET_LINKS_MIN
        finally:
            temp_path.unlink()

    def test_parse_post_with_valid_links(self):
        """Test parsing post with valid internal links."""
        content = dedent("""
            ---
            title: Test Post
            date: 2025-01-01
            ---
            Check out my [security guide](/posts/2025-04-24-building-secure-homelab-adventure).

            Also see [cryptography basics](/posts/2024-01-18-demystifying-cryptography-beginners-guide).
        """).strip()

        all_slugs = {
            "2025-04-24-building-secure-homelab-adventure",
            "2024-01-18-demystifying-cryptography-beginners-guide"
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            analysis = parse_post(temp_path, all_slugs)
            assert analysis.link_count == 2
            assert len(analysis.links) == 2
            assert all(link.is_valid for link in analysis.links)
            assert analysis.broken_links == 0
        finally:
            temp_path.unlink()

    def test_parse_post_with_broken_links(self):
        """Test parsing post with broken internal links."""
        content = dedent("""
            ---
            title: Test Post
            date: 2025-01-01
            ---
            This links to a [non-existent post](/posts/does-not-exist).

            And another [broken link](/posts/also-missing).
        """).strip()

        all_slugs = set()  # No valid slugs

        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            analysis = parse_post(temp_path, all_slugs)
            assert analysis.link_count == 2
            assert len(analysis.links) == 2
            assert all(not link.is_valid for link in analysis.links)
            assert analysis.broken_links == 2
        finally:
            temp_path.unlink()

    def test_parse_post_mixed_links(self):
        """Test parsing post with both valid and broken links."""
        content = dedent("""
            ---
            title: Test Post
            date: 2025-01-01
            ---
            Valid: [security guide](/posts/2025-04-24-building-secure-homelab-adventure).
            Broken: [non-existent](/posts/does-not-exist).
        """).strip()

        all_slugs = {"2025-04-24-building-secure-homelab-adventure"}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            analysis = parse_post(temp_path, all_slugs)
            assert analysis.link_count == 2
            assert analysis.broken_links == 1
            valid_links = [link for link in analysis.links if link.is_valid]
            assert len(valid_links) == 1
        finally:
            temp_path.unlink()

    def test_parse_post_meets_target(self):
        """Test parsing post that meets link target."""
        # Create post with 6 links (minimum target)
        links = [
            f"[Link {i}](/posts/post-{i})"
            for i in range(TARGET_LINKS_MIN)
        ]
        content = dedent(f"""
            ---
            title: Test Post
            date: 2025-01-01
            ---
            {' '.join(links)}
        """).strip()

        all_slugs = {f"post-{i}" for i in range(TARGET_LINKS_MIN)}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            analysis = parse_post(temp_path, all_slugs)
            assert analysis.link_count == TARGET_LINKS_MIN
            assert analysis.meets_target
            assert analysis.gap == 0
        finally:
            temp_path.unlink()


class TestLinkValidation:
    """Test link validation functions."""

    def test_validate_links_all_valid(self):
        """Test validation with all valid links."""
        analyses = [
            PostAnalysis(
                slug="post-1",
                title="Post 1",
                link_count=2,
                links=[
                    InternalLink("post-1", "post-2", "link", 10, True),
                    InternalLink("post-1", "post-3", "link", 20, True),
                ],
                broken_links=0,
                meets_target=False,
                gap=4
            )
        ]

        validation = validate_links(analyses)
        assert validation['total_links'] == 2
        assert validation['total_broken'] == 0
        assert validation['posts_with_broken'] == 0
        assert len(validation['broken_links']) == 0

    def test_validate_links_with_broken(self):
        """Test validation with broken links."""
        analyses = [
            PostAnalysis(
                slug="post-1",
                title="Post 1",
                link_count=3,
                links=[
                    InternalLink("post-1", "post-2", "link", 10, True),
                    InternalLink("post-1", "missing", "broken", 20, False),
                    InternalLink("post-1", "also-missing", "broken", 30, False),
                ],
                broken_links=2,
                meets_target=False,
                gap=3
            )
        ]

        validation = validate_links(analyses)
        assert validation['total_links'] == 3
        assert validation['total_broken'] == 2
        assert validation['posts_with_broken'] == 1
        assert len(validation['broken_links']) == 2

        broken = validation['broken_links']
        assert broken[0]['target'] == 'missing'
        assert broken[1]['target'] == 'also-missing'


class TestProgressCalculation:
    """Test progress calculation functions."""

    def test_calculate_progress_empty(self):
        """Test progress calculation with no posts."""
        progress = calculate_progress([])
        assert progress['total_posts'] == 0
        assert progress['total_links'] == 0
        assert progress['avg_links_per_post'] == 0

    def test_calculate_progress_basic(self):
        """Test basic progress calculation."""
        analyses = [
            PostAnalysis("post-1", "Post 1", 0, [], 0, False, 6),
            PostAnalysis("post-2", "Post 2", 3, [], 0, False, 3),
            PostAnalysis("post-3", "Post 3", 6, [], 0, True, 0),
            PostAnalysis("post-4", "Post 4", 10, [], 0, True, 0),
        ]

        progress = calculate_progress(analyses)
        assert progress['total_posts'] == 4
        assert progress['total_links'] == 19  # 0 + 3 + 6 + 10
        assert progress['avg_links_per_post'] == 19 / 4
        assert progress['posts_meeting_target'] == 2  # post-3 and post-4

    def test_calculate_progress_distribution(self):
        """Test progress distribution calculation."""
        analyses = [
            PostAnalysis("post-1", "Post 1", 0, [], 0, False, 6),
            PostAnalysis("post-2", "Post 2", 0, [], 0, False, 6),
            PostAnalysis("post-3", "Post 3", 3, [], 0, False, 3),
            PostAnalysis("post-4", "Post 4", 5, [], 0, False, 1),
            PostAnalysis("post-5", "Post 5", 6, [], 0, True, 0),
            PostAnalysis("post-6", "Post 6", 8, [], 0, True, 0),
            PostAnalysis("post-7", "Post 7", 10, [], 0, True, 0),
            PostAnalysis("post-8", "Post 8", 12, [], 0, True, 0),
        ]

        progress = calculate_progress(analyses)
        dist = progress['distribution']

        assert dist['0_links'] == 2  # post-1, post-2
        assert dist['1-5_links'] == 2  # post-3, post-4
        assert dist['6-9_links'] == 2  # post-5, post-6
        assert dist['10+_links'] == 2  # post-7, post-8


class TestRecommendationLoading:
    """Test recommendation CSV loading."""

    def test_load_recommendations_csv(self):
        """Test loading recommendations from CSV file."""
        csv_content = dedent("""
            Source_Post_Slug,Source_Post_Title,Target_Post_Slug,Target_Post_Title,Anchor_Text_Suggestion,Link_Type,Priority,Implementation_Phase,Rationale
            post-1,Post 1,post-2,Post 2,link to post 2,Hub→Hub,P0,Phase_1,Test rationale
            post-1,Post 1,post-3,Post 3,link to post 3,Hub→Spoke,P1,Phase_2,Another rationale
        """).strip()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = Path(f.name)

        try:
            # Temporarily override CSV path
            original_path = ilv.RECOMMENDATIONS_CSV
            ilv.RECOMMENDATIONS_CSV = temp_path

            recommendations = load_recommendations()
            assert len(recommendations) == 2

            rec1 = recommendations[0]
            assert rec1.source_post == "post-1"
            assert rec1.target_post == "post-2"
            assert rec1.priority == "P0"
            assert rec1.phase == "Phase_1"

            rec2 = recommendations[1]
            assert rec2.source_post == "post-1"
            assert rec2.target_post == "post-3"
            assert rec2.priority == "P1"
            assert rec2.phase == "Phase_2"

            # Restore original path
            ilv.RECOMMENDATIONS_CSV = original_path
        finally:
            temp_path.unlink()


class TestDataClasses:
    """Test dataclass structures."""

    def test_internal_link_creation(self):
        """Test InternalLink dataclass creation."""
        link = InternalLink(
            source_post="post-1",
            target_post="post-2",
            anchor_text="test link",
            line_number=42,
            is_valid=True
        )

        assert link.source_post == "post-1"
        assert link.target_post == "post-2"
        assert link.anchor_text == "test link"
        assert link.line_number == 42
        assert link.is_valid is True

    def test_link_recommendation_creation(self):
        """Test LinkRecommendation dataclass creation."""
        rec = LinkRecommendation(
            source_post="post-1",
            source_title="Post 1",
            target_post="post-2",
            target_title="Post 2",
            anchor_text="link text",
            link_type="Hub→Hub",
            priority="P0",
            phase="Phase_1",
            rationale="Test rationale"
        )

        assert rec.source_post == "post-1"
        assert rec.priority == "P0"
        assert rec.phase == "Phase_1"

    def test_post_analysis_creation(self):
        """Test PostAnalysis dataclass creation."""
        analysis = PostAnalysis(
            slug="test-post",
            title="Test Post",
            link_count=5,
            links=[],
            broken_links=1,
            meets_target=False,
            gap=1
        )

        assert analysis.slug == "test-post"
        assert analysis.link_count == 5
        assert analysis.broken_links == 1
        assert not analysis.meets_target
        assert analysis.gap == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
