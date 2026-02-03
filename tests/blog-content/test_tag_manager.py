#!/usr/bin/env -S uv run python3
"""
Test suite for tag-manager.py

Tests tag strategy management functionality:
- Frontmatter parsing (YAML list and array formats)
- Tag normalization (lowercase, strip whitespace)
- Distribution analysis (frequency, co-occurrence)
- Quality scoring (0-100 scale)
- Consolidation detection (plurals, synonyms, similar tags)
- Tag application (dry-run and actual writes)

Run:
    pytest tests/blog-content/test_tag_manager.py -v
    pytest tests/blog-content/test_tag_manager.py::TestTagManager::test_parse_tags -v
"""

import pytest
import yaml
from pathlib import Path
from collections import Counter

# Import module under test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts" / "blog-content"))
from tag_manager import TagManager


class TestTagManager:
    """Test TagManager class functionality."""

    @pytest.fixture
    def manager(self):
        """Create TagManager instance for tests."""
        return TagManager()

    @pytest.fixture
    def sample_frontmatter_array(self):
        """Sample frontmatter with array-style tags."""
        return """---
title: Test Post
date: 2024-01-01
tags: [kubernetes, docker, security]
---

Post content here.
"""

    @pytest.fixture
    def sample_frontmatter_list(self):
        """Sample frontmatter with YAML list-style tags."""
        return """---
title: Test Post
date: 2024-01-01
tags:
  - kubernetes
  - docker
  - security
---

Post content here.
"""

    def test_extract_frontmatter_array_format(self, manager, sample_frontmatter_array):
        """Test frontmatter extraction with array-format tags."""
        frontmatter, frontmatter_text, body = manager.extract_frontmatter(sample_frontmatter_array)

        assert frontmatter is not None
        assert 'tags' in frontmatter
        assert isinstance(frontmatter['tags'], list)
        assert len(frontmatter['tags']) == 3
        assert 'Post content here.' in body

    def test_extract_frontmatter_list_format(self, manager, sample_frontmatter_list):
        """Test frontmatter extraction with YAML list-format tags."""
        frontmatter, frontmatter_text, body = manager.extract_frontmatter(sample_frontmatter_list)

        assert frontmatter is not None
        assert 'tags' in frontmatter
        assert isinstance(frontmatter['tags'], list)
        assert len(frontmatter['tags']) == 3

    def test_parse_tags_normalization(self, manager):
        """Test tag normalization (lowercase, strip whitespace)."""
        frontmatter = {
            'tags': ['Kubernetes', 'DOCKER', ' security ', 'AI']
        }

        tags = manager.parse_tags(frontmatter)

        assert tags == ['kubernetes', 'docker', 'security', 'ai']

    def test_parse_tags_empty(self, manager):
        """Test parsing when no tags present."""
        frontmatter = {}
        tags = manager.parse_tags(frontmatter)
        assert tags == []

    def test_calculate_quality_score_optimal(self, manager):
        """Test quality score calculation for optimal tags (3-5 tags, all criteria met)."""
        tags = ['kubernetes', 'docker', 'security', 'homelab']

        score, issues = manager.calculate_quality_score('test.md', tags)

        # Should get 100 (40 + 20 + 20 + 10 + 10)
        assert score == 100
        assert len(issues) == 0

    def test_calculate_quality_score_too_few_tags(self, manager):
        """Test quality score when post has fewer than 3 tags."""
        tags = ['kubernetes', 'docker']

        score, issues = manager.calculate_quality_score('test.md', tags)

        assert score < 100
        assert any('Too few tags' in issue for issue in issues)

    def test_calculate_quality_score_too_many_tags(self, manager):
        """Test quality score when post has more than 5 tags."""
        tags = ['kubernetes', 'docker', 'security', 'homelab', 'ai', 'llm']

        score, issues = manager.calculate_quality_score('test.md', tags)

        assert score < 100
        assert any('Too many tags' in issue for issue in issues)

    def test_calculate_quality_score_duplicates(self, manager):
        """Test quality score when duplicate tags present."""
        tags = ['kubernetes', 'docker', 'kubernetes', 'security']

        score, issues = manager.calculate_quality_score('test.md', tags)

        assert score < 100
        assert any('Duplicate tags' in issue for issue in issues)

    def test_calculate_quality_score_naming_violations(self, manager):
        """Test quality score when naming conventions violated."""
        tags = ['Kubernetes', 'machine_learning', 'AI ML']  # Uppercase, underscore, space

        score, issues = manager.calculate_quality_score('test.md', tags)

        assert score < 100
        assert any('Naming violations' in issue for issue in issues)

    def test_calculate_quality_score_deprecated_tags(self, manager):
        """Test quality score when deprecated tags used."""
        tags = ['kubernetes', 'security', 'posts', 'blog']  # 'posts' and 'blog' are deprecated

        score, issues = manager.calculate_quality_score('test.md', tags)

        assert score < 100
        assert any('Deprecated tags' in issue for issue in issues)



class TestTagConsolidation:
    """Test tag consolidation logic (not yet implemented)."""

    def test_detect_plural_singular(self):
        """Test detection of plural/singular variants (containers ↔ container)."""
        pytest.skip("Consolidation logic not yet implemented")

    def test_detect_synonyms(self):
        """Test detection of known synonyms (k8s ↔ kubernetes)."""
        pytest.skip("Consolidation logic not yet implemented")

    def test_detect_hyphenation(self):
        """Test detection of hyphenation inconsistencies."""
        pytest.skip("Consolidation logic not yet implemented")

    def test_detect_similar_fuzzy(self):
        """Test detection of similar tags via fuzzy matching."""
        pytest.skip("Consolidation logic not yet implemented")


class TestTagApplication:
    """Test tag strategy application (not yet implemented)."""

    def test_apply_dry_run_mode(self):
        """Test that dry-run mode doesn't write files."""
        pytest.skip("Apply logic not yet implemented")

    def test_apply_writes_correctly(self):
        """Test that tags are written correctly to frontmatter."""
        pytest.skip("Apply logic not yet implemented")

    def test_apply_preserves_formatting(self):
        """Test that frontmatter formatting is preserved."""
        pytest.skip("Apply logic not yet implemented")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
