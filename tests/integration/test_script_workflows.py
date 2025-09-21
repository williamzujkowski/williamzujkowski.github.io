"""
Integration tests for script workflows
"""

import pytest
import json
from pathlib import Path
import subprocess
import sys

class TestBlogWorkflow:
    """Test blog enhancement workflow"""

    def test_blog_scripts_exist(self):
        """Test that blog scripts exist"""
        blog_scripts = [
            "scripts/analyze-blog-content.py",
            "scripts/generate-blog-hero-images.py",
            "scripts/update-blog-images.py",
            "scripts/optimize-blog-content.py"
        ]

        for script in blog_scripts:
            assert Path(script).exists(), f"Script {script} not found"

    def test_image_generation_script_exists(self):
        """Test hero image generation script exists"""
        assert Path("scripts/generate-blog-hero-images.py").exists()

class TestValidationWorkflow:
    """Test validation workflow"""

    def test_standards_validation(self):
        """Test standards validation workflow"""
        result = subprocess.run(
            ["python", "scripts/validate_standards.py"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Should run without Python errors (even if validation fails)
        assert "Traceback" not in result.stderr

    def test_check_duplicates_exists(self):
        """Test duplicate checking script exists"""
        assert Path("scripts/check_duplicates.py").exists()

class TestEnforcementWorkflow:
    """Test enforcement system workflow"""

    def test_claude_rules_exist(self):
        """Test that enforcement rules exist"""
        rules_path = Path(".claude-rules.json")
        assert rules_path.exists()

        # Rules should be valid JSON
        rules = json.loads(rules_path.read_text())
        assert "version" in rules
        assert "MANDATORY_STANDARDS" in rules or "LLM_ENFORCEMENT" in rules

    def test_pre_commit_hook_exists(self):
        """Test that pre-commit hook is installed"""
        hook_path = Path(".git/hooks/pre-commit")
        # Note: Might not exist in CI environment
        if hook_path.exists():
            content = hook_path.read_text()
            # Check for validation commands
            assert "python" in content or "validate" in content

class TestDocumentationGeneration:
    """Test documentation generation scripts"""

    def test_documentation_generators_exist(self):
        """Test that all doc generators exist"""
        generators = [
            "scripts/generate_architecture_doc.py",
            "scripts/generate_enforcement_doc.py",
            "scripts/generate_llm_onboarding.py",
            "scripts/generate_script_catalog.py"
        ]

        for generator in generators:
            assert Path(generator).exists(), f"Generator {generator} not found"

    def test_generated_docs_exist(self):
        """Test that generated documentation exists"""
        docs = [
            "docs/ARCHITECTURE.md",
            "docs/ENFORCEMENT.md",
            "docs/GUIDES/LLM_ONBOARDING.md",
            "docs/GUIDES/SCRIPT_CATALOG.md"
        ]

        for doc in docs:
            assert Path(doc).exists(), f"Documentation {doc} not found"