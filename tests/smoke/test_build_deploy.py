"""
Smoke tests for build and deployment
"""

import subprocess
import pytest
from pathlib import Path

class TestBuildSystem:
    """Test that the site builds correctly"""

    def test_npm_installed(self):
        """Test that npm is available"""
        result = subprocess.run(
            ["npm", "--version"],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert len(result.stdout) > 0

    def test_package_json_exists(self):
        """Test that package.json exists"""
        assert Path("package.json").exists()

    def test_eleventy_config_exists(self):
        """Test that Eleventy config exists"""
        assert Path(".eleventy.js").exists()

    def test_tailwind_config_exists(self):
        """Test that Tailwind config exists"""
        assert Path("tailwind.config.js").exists()

    @pytest.mark.slow
    def test_npm_build(self):
        """Test npm build command"""
        result = subprocess.run(
            ["npm", "run", "build"],
            capture_output=True,
            text=True,
            timeout=60
        )

        # Build should complete
        assert result.returncode == 0

        # Output directory should exist
        assert Path("_site").exists()

    @pytest.mark.slow
    def test_build_output_structure(self):
        """Test that build creates expected files"""
        # Check if already built, otherwise skip
        if not Path("_site").exists():
            pytest.skip("Site not built, run npm build first")

        # Check key files exist
        assert Path("_site/index.html").exists()
        assert Path("_site/assets/css").exists() or Path("_site/css").exists()

class TestCriticalScripts:
    """Test that critical scripts run without errors"""

    def test_manifest_exists(self):
        """Test MANIFEST.json exists"""
        assert Path("MANIFEST.json").exists()

        # Should be valid JSON
        import json
        manifest = json.loads(Path("MANIFEST.json").read_text())
        assert "version" in manifest

    def test_claude_md_exists(self):
        """Test CLAUDE.md exists and has content"""
        claude_path = Path("CLAUDE.md")
        assert claude_path.exists()

        content = claude_path.read_text()
        assert "MANDATORY ENFORCEMENT" in content
        assert "Comprehensive Documentation" in content

    def test_lib_common_imports(self):
        """Test that lib/common.py can be imported"""
        import sys
        sys.path.insert(0, 'scripts')

        try:
            from lib import common
            assert hasattr(common, 'ManifestManager')
            assert hasattr(common, 'TimeManager')
            assert hasattr(common, 'Logger')
        except ImportError as e:
            pytest.fail(f"Failed to import lib.common: {e}")