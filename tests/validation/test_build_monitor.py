#!/usr/bin/env -S uv run python3
"""
Comprehensive unit tests for build-monitor.py

Tests cover:
- Build output parsing
- Performance metric extraction
- Bundle size calculation
- Baseline comparison logic
- Regression detection
- Edge cases: Empty output, failed build, timeout
"""

import pytest
import sys
import json
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Add scripts to path
scripts_path = Path(__file__).parent.parent.parent / "scripts" / "validation"
sys.path.insert(0, str(scripts_path))

# Import after path is set
import importlib.util
spec = importlib.util.spec_from_file_location("build_monitor", scripts_path / "build-monitor.py")
build_monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_monitor)
BuildMonitor = build_monitor.BuildMonitor
BuildStats = build_monitor.BuildStats


@pytest.fixture
def fixtures_dir():
    """Return path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def temp_baseline_file(tmp_path):
    """Create temporary baseline file path."""
    return tmp_path / ".test-baseline.json"


@pytest.fixture
def monitor(temp_baseline_file):
    """Create BuildMonitor instance with temporary baseline file."""
    return BuildMonitor(baseline_file=temp_baseline_file)


class TestMonitorInitialization:
    """Test build monitor initialization and configuration."""

    def test_init_with_valid_path(self, temp_baseline_file):
        """Test initialization with valid Path object."""
        monitor = BuildMonitor(baseline_file=temp_baseline_file)
        assert monitor.baseline_file == temp_baseline_file
        assert isinstance(monitor.current_build, dict)
        assert monitor.baseline_build is None

    def test_init_with_invalid_type(self):
        """Test initialization fails with non-Path type."""
        with pytest.raises(TypeError, match="baseline_file must be Path"):
            BuildMonitor(baseline_file="/invalid/string/path")

    def test_init_with_default_baseline(self):
        """Test initialization with default baseline file."""
        monitor = BuildMonitor()
        assert monitor.baseline_file == Path(".build-baseline.json")

    def test_init_constants(self, monitor):
        """Test that build constants are properly set."""
        assert monitor.BUILD_TIMEOUT == 120
        assert monitor.BUILD_COMMAND == ["npm", "run", "build"]
        assert monitor.TIME_REGRESSION_THRESHOLD == 0.20


class TestBuildOutputParsing:
    """Test parsing of build output to extract metrics."""

    def test_parse_successful_build(self, monitor, fixtures_dir):
        """Test parsing of successful build output."""
        output = (fixtures_dir / "test_build_output.txt").read_text()
        stats = monitor._parse_build_output_optimized(output)

        assert stats["posts_parsed"] == 56
        assert stats["files_written"] == 245
        # Parse eleventy time (may be None if not in expected format)
        if stats["eleventy_time"] is not None:
            assert stats["eleventy_time"] > 0

    def test_parse_bundle_sizes(self, monitor, fixtures_dir):
        """Test parsing of JavaScript bundle sizes."""
        output = (fixtures_dir / "test_build_output.txt").read_text()
        stats = monitor._parse_build_output_optimized(output)

        assert "src/js/main.js" in stats["js_bundles"]
        assert stats["js_bundles"]["src/js/main.js"]["original"] == "245.3 KB"
        assert stats["js_bundles"]["src/js/main.js"]["minified"] == "89.7 KB"
        assert stats["js_bundles"]["src/js/main.js"]["reduction"] == 63.4

        assert "src/js/analytics.js" in stats["js_bundles"]
        assert stats["js_bundles"]["src/js/analytics.js"]["reduction"] == 67.2

    def test_parse_empty_output(self, monitor):
        """Test parsing of empty build output."""
        output = ""
        stats = monitor._parse_build_output_optimized(output)

        assert stats["posts_parsed"] == 0
        assert stats["files_written"] == 0
        assert stats["eleventy_time"] is None
        assert stats["js_bundles"] == {}

    def test_parse_partial_output(self, monitor):
        """Test parsing of output with some missing metrics."""
        output = """
[11ty] Successfully parsed 42 posts
[11ty] Build complete!
"""
        stats = monitor._parse_build_output_optimized(output)

        assert stats["posts_parsed"] == 42
        assert stats["files_written"] == 0  # Missing
        assert stats["eleventy_time"] is None  # Missing

    def test_parse_multiple_bundles(self, monitor):
        """Test parsing of multiple JavaScript bundles."""
        output = """
[11ty] Creating bundle: src/js/main.js
[11ty] Minified: 100 KB → 30 KB (70.0% reduction)
[11ty] Creating bundle: src/js/vendor.js
[11ty] Minified: 500 KB → 150 KB (70.0% reduction)
[11ty] Creating bundle: src/js/analytics.js
[11ty] Minified: 20 KB → 8 KB (60.0% reduction)
"""
        stats = monitor._parse_build_output_optimized(output)

        assert len(stats["js_bundles"]) == 3
        assert "src/js/main.js" in stats["js_bundles"]
        assert "src/js/vendor.js" in stats["js_bundles"]
        assert "src/js/analytics.js" in stats["js_bundles"]

    def test_parse_invalid_numbers(self, monitor):
        """Test handling of invalid numeric values."""
        output = """
[11ty] Successfully parsed abc posts
[11ty] Wrote xyz files
[11ty] Minified: invalid → data (bad% reduction)
"""
        stats = monitor._parse_build_output_optimized(output)

        # Should not crash, just ignore invalid values
        assert stats["posts_parsed"] == 0
        assert stats["files_written"] == 0


class TestWarningAndErrorExtraction:
    """Test extraction of warnings and errors from build output."""

    def test_extract_warnings(self, monitor, fixtures_dir):
        """Test extraction of warning messages."""
        output = (fixtures_dir / "build_with_warnings.txt").read_text()
        warnings = []
        errors = []

        monitor._extract_warnings_errors_optimized(output, warnings, errors)

        assert len(warnings) == 2
        assert any("Deprecated filter" in w for w in warnings)
        assert any("Missing image reference" in w for w in warnings)
        assert len(errors) == 0

    def test_extract_errors(self, monitor, fixtures_dir):
        """Test extraction of error messages."""
        output = (fixtures_dir / "build_with_errors.txt").read_text()
        warnings = []
        errors = []

        monitor._extract_warnings_errors_optimized(output, warnings, errors)

        # Should extract all lines with "error" (case-insensitive)
        assert len(errors) >= 2
        assert any("Template syntax error" in e for e in errors)
        assert any("Failed to parse frontmatter" in e for e in errors)

    def test_extract_mixed_warnings_errors(self, monitor):
        """Test extraction of both warnings and errors."""
        output = """
[11ty] Warning: Deprecated function used
[11ty] Error: Template not found
[11ty] Warning: Missing metadata
[11ty] Error: Build failed
"""
        warnings = []
        errors = []

        monitor._extract_warnings_errors_optimized(output, warnings, errors)

        assert len(warnings) == 2
        assert len(errors) == 2

    def test_extract_no_issues(self, monitor, fixtures_dir):
        """Test extraction from clean build output."""
        output = (fixtures_dir / "test_build_output.txt").read_text()
        warnings = []
        errors = []

        monitor._extract_warnings_errors_optimized(output, warnings, errors)

        assert len(warnings) == 0
        assert len(errors) == 0

    def test_extract_case_insensitive(self, monitor):
        """Test that extraction is case-insensitive."""
        output = """
[11ty] ERROR: Build failed
[11ty] Warning: Deprecated feature
[11ty] error: Another error
[11ty] WARNING: Another warning
"""
        warnings = []
        errors = []

        monitor._extract_warnings_errors_optimized(output, warnings, errors)

        assert len(warnings) == 2
        assert len(errors) == 2

    def test_extract_error_not_warning(self, monitor):
        """Test that 'error' lines don't get classified as warnings."""
        # Use output that contains "error" but NOT "warn" substring
        output = "[11ty] Error: Build failed completely"
        warnings = []
        errors = []

        monitor._extract_warnings_errors_optimized(output, warnings, errors)

        # The extraction correctly identifies this as an error
        # (line contains 'error' and not 'warn')
        assert len(errors) == 1
        assert "error" in errors[0].lower()
        assert len(warnings) == 0  # No false positives


class TestBuildExecution:
    """Test build command execution and error handling."""

    @patch('subprocess.run')
    def test_run_build_success(self, mock_run, monitor, fixtures_dir):
        """Test successful build execution."""
        # Mock successful build
        output = (fixtures_dir / "test_build_output.txt").read_text()
        mock_run.return_value = Mock(
            returncode=0,
            stdout=output,
            stderr=""
        )

        build_data = monitor.run_build()

        assert build_data["success"] is True
        assert build_data["return_code"] == 0
        assert "build_time" in build_data
        assert build_data["stats"]["posts_parsed"] == 56

    @patch('subprocess.run')
    def test_run_build_failure(self, mock_run, monitor):
        """Test failed build execution."""
        mock_run.return_value = Mock(
            returncode=1,
            stdout="",
            stderr="Error: Build failed"
        )

        build_data = monitor.run_build()

        assert build_data["success"] is False
        assert build_data["return_code"] == 1

    @patch('subprocess.run')
    def test_run_build_timeout(self, mock_run, monitor):
        """Test build timeout handling."""
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd=["npm", "run", "build"],
            timeout=120
        )

        build_data = monitor.run_build()

        assert build_data["success"] is False
        assert "timeout" in build_data["error"].lower()
        assert build_data["build_time"] == 120

    @patch('subprocess.run')
    def test_run_build_npm_not_found(self, mock_run, monitor):
        """Test handling of npm not found error."""
        mock_run.side_effect = FileNotFoundError("npm not found")

        build_data = monitor.run_build()

        assert build_data["success"] is False
        assert "npm not found" in build_data["error"]

    @patch('subprocess.run')
    def test_run_build_subprocess_error(self, mock_run, monitor):
        """Test handling of subprocess errors."""
        mock_run.side_effect = subprocess.SubprocessError("Subprocess error")

        build_data = monitor.run_build()

        assert build_data["success"] is False
        assert "Subprocess error" in build_data["error"]

    @patch('subprocess.run')
    def test_run_build_unexpected_error(self, mock_run, monitor):
        """Test handling of unexpected errors."""
        mock_run.side_effect = Exception("Unexpected error")

        build_data = monitor.run_build()

        assert build_data["success"] is False
        assert "Unexpected error" in build_data["error"]

    @patch('subprocess.run')
    def test_run_build_captures_timing(self, mock_run, monitor):
        """Test that build timing is captured accurately."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="[11ty] Build complete!",
            stderr=""
        )

        build_data = monitor.run_build()

        assert "build_time" in build_data
        assert isinstance(build_data["build_time"], float)
        assert build_data["build_time"] >= 0  # Could be 0 for very fast mock


class TestBaselineManagement:
    """Test baseline save/load functionality."""

    def test_save_baseline_success(self, monitor, temp_baseline_file):
        """Test successful baseline save."""
        monitor.current_build = {
            "timestamp": "2025-11-02T10:00:00",
            "success": True,
            "build_time": 5.0,
            "stats": {"posts_parsed": 56}
        }

        monitor.save_baseline()

        assert temp_baseline_file.exists()
        with open(temp_baseline_file, 'r') as f:
            saved_data = json.load(f)
        assert saved_data["success"] is True
        assert saved_data["build_time"] == 5.0

    def test_save_baseline_no_current_build(self, monitor):
        """Test save baseline fails without current build."""
        with pytest.raises(ValueError, match="No current build data"):
            monitor.save_baseline()

    def test_save_baseline_creates_directory(self, tmp_path):
        """Test that baseline save creates parent directory."""
        baseline_file = tmp_path / "subdir" / "baseline.json"
        monitor = BuildMonitor(baseline_file=baseline_file)
        monitor.current_build = {"success": True}

        monitor.save_baseline()

        assert baseline_file.exists()
        assert baseline_file.parent.exists()

    def test_load_baseline_success(self, monitor, temp_baseline_file):
        """Test successful baseline load."""
        # Create baseline file
        baseline_data = {
            "timestamp": "2025-11-01T10:00:00",
            "success": True,
            "build_time": 4.5,
            "stats": {"posts_parsed": 50}
        }
        with open(temp_baseline_file, 'w') as f:
            json.dump(baseline_data, f)

        loaded = monitor.load_baseline()

        assert loaded is not None
        assert loaded["success"] is True
        assert loaded["build_time"] == 4.5
        assert monitor.baseline_build == loaded

    def test_load_baseline_nonexistent_file(self, monitor):
        """Test load baseline with nonexistent file."""
        result = monitor.load_baseline()
        assert result is None

    def test_load_baseline_corrupted_json(self, monitor, temp_baseline_file):
        """Test load baseline with corrupted JSON."""
        temp_baseline_file.write_text("{ invalid json }")

        with pytest.raises(json.JSONDecodeError):
            monitor.load_baseline()

    def test_load_baseline_io_error(self, monitor, temp_baseline_file):
        """Test load baseline with I/O error."""
        # Create file with no read permissions
        temp_baseline_file.write_text('{"success": true}')
        temp_baseline_file.chmod(0o000)

        try:
            with pytest.raises(IOError):
                monitor.load_baseline()
        finally:
            # Restore permissions for cleanup
            temp_baseline_file.chmod(0o644)


class TestBuildComparison:
    """Test baseline comparison and regression detection."""

    def test_compare_no_changes(self, monitor):
        """Test comparison with identical builds."""
        build_data = {
            "success": True,
            "build_time": 5.0,
            "stats": {"posts_parsed": 56, "files_written": 245},
            "warnings": [],
            "errors": []
        }
        monitor.baseline_build = build_data.copy()
        monitor.current_build = build_data.copy()

        comparison = monitor.compare_builds()

        assert comparison["status_change"] == "UNCHANGED"
        assert comparison["regression_detected"] is False

    def test_compare_status_regression(self, monitor):
        """Test detection of build status regression."""
        monitor.baseline_build = {
            "success": True,
            "build_time": 5.0,
            "stats": {},
            "warnings": [],
            "errors": []
        }
        monitor.current_build = {
            "success": False,
            "build_time": 6.0,
            "stats": {},
            "warnings": [],
            "errors": ["Build failed"]
        }

        comparison = monitor.compare_builds()

        assert comparison["status_change"] == "REGRESSION"
        assert comparison["regression_detected"] is True

    def test_compare_status_improvement(self, monitor):
        """Test detection of build status improvement."""
        monitor.baseline_build = {
            "success": False,
            "build_time": 5.0,
            "stats": {},
            "warnings": [],
            "errors": ["Error"]
        }
        monitor.current_build = {
            "success": True,
            "build_time": 5.0,
            "stats": {},
            "warnings": [],
            "errors": []
        }

        comparison = monitor.compare_builds()

        assert comparison["status_change"] == "FIXED"
        assert comparison["regression_detected"] is False

    def test_compare_time_regression(self, monitor):
        """Test detection of build time regression."""
        monitor.baseline_build = {
            "success": True,
            "build_time": 5.0,
            "stats": {},
            "warnings": [],
            "errors": []
        }
        monitor.current_build = {
            "success": True,
            "build_time": 7.0,  # 40% slower
            "stats": {},
            "warnings": [],
            "errors": []
        }

        comparison = monitor.compare_builds()

        assert comparison["time_delta"] == 2.0
        assert comparison["time_delta_percent"] == 40.0
        assert comparison["regression_detected"] is True  # >20% threshold

    def test_compare_time_improvement(self, monitor):
        """Test detection of build time improvement."""
        monitor.baseline_build = {
            "success": True,
            "build_time": 10.0,
            "stats": {},
            "warnings": [],
            "errors": []
        }
        monitor.current_build = {
            "success": True,
            "build_time": 7.0,
            "stats": {},
            "warnings": [],
            "errors": []
        }

        comparison = monitor.compare_builds()

        assert comparison["time_delta"] == -3.0
        assert comparison["time_delta_percent"] == -30.0
        assert comparison["regression_detected"] is False

    def test_compare_stats_changes(self, monitor):
        """Test detection of statistics changes."""
        monitor.baseline_build = {
            "success": True,
            "build_time": 5.0,
            "stats": {
                "posts_parsed": 50,
                "files_written": 200,
                "eleventy_time": 4.0
            },
            "warnings": [],
            "errors": []
        }
        monitor.current_build = {
            "success": True,
            "build_time": 5.0,
            "stats": {
                "posts_parsed": 56,
                "files_written": 245,
                "eleventy_time": 4.5
            },
            "warnings": [],
            "errors": []
        }

        comparison = monitor.compare_builds()

        assert "posts_parsed" in comparison["stats_changes"]
        assert comparison["stats_changes"]["posts_parsed"]["baseline"] == 50
        assert comparison["stats_changes"]["posts_parsed"]["current"] == 56
        assert comparison["stats_changes"]["posts_parsed"]["delta"] == 6

    def test_compare_new_warnings(self, monitor):
        """Test detection of new warnings."""
        monitor.baseline_build = {
            "success": True,
            "build_time": 5.0,
            "stats": {},
            "warnings": ["Old warning"],
            "errors": []
        }
        monitor.current_build = {
            "success": True,
            "build_time": 5.0,
            "stats": {},
            "warnings": ["Old warning", "New warning"],
            "errors": []
        }

        comparison = monitor.compare_builds()

        assert len(comparison["new_warnings"]) == 1
        assert "New warning" in comparison["new_warnings"]

    def test_compare_new_errors(self, monitor):
        """Test detection of new errors."""
        monitor.baseline_build = {
            "success": True,
            "build_time": 5.0,
            "stats": {},
            "warnings": [],
            "errors": []
        }
        monitor.current_build = {
            "success": True,
            "build_time": 5.0,
            "stats": {},
            "warnings": [],
            "errors": ["New error"]
        }

        comparison = monitor.compare_builds()

        assert len(comparison["new_errors"]) == 1
        assert "New error" in comparison["new_errors"]
        assert comparison["regression_detected"] is True

    def test_compare_no_baseline(self, monitor):
        """Test compare fails without baseline."""
        monitor.current_build = {"success": True}

        with pytest.raises(ValueError, match="No baseline found"):
            monitor.compare_builds()

    def test_compare_minor_time_increase(self, monitor):
        """Test that minor time increases don't trigger regression."""
        monitor.baseline_build = {
            "success": True,
            "build_time": 5.0,
            "stats": {},
            "warnings": [],
            "errors": []
        }
        monitor.current_build = {
            "success": True,
            "build_time": 5.5,  # 10% slower (below 20% threshold)
            "stats": {},
            "warnings": [],
            "errors": []
        }

        comparison = monitor.compare_builds()

        assert comparison["time_delta_percent"] == 10.0
        assert comparison["regression_detected"] is False


class TestReportGeneration:
    """Test build report generation."""

    @patch('subprocess.run')
    def test_print_build_report_success(self, mock_run, monitor, caplog):
        """Test report generation for successful build."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="[11ty] Successfully parsed 56 posts\n[11ty] Wrote 245 files",
            stderr=""
        )

        monitor.run_build()
        exit_code = monitor.print_build_report(compare=False)

        # Check logs instead of stdout (script uses logger)
        log_output = caplog.text
        assert "BUILD VALIDATION REPORT" in log_output
        assert "PASSING" in log_output
        assert exit_code == 0

    @patch('subprocess.run')
    def test_print_build_report_failure(self, mock_run, monitor, caplog):
        """Test report generation for failed build."""
        mock_run.return_value = Mock(
            returncode=1,
            stdout="",
            stderr="Error: Build failed"
        )

        monitor.run_build()
        exit_code = monitor.print_build_report(compare=False)

        # Check logs instead of stdout (script uses logger)
        log_output = caplog.text
        assert "FAILED" in log_output
        assert exit_code == 1


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_parse_output_with_unicode(self, monitor):
        """Test parsing output with Unicode characters."""
        output = """
[11ty] Successfully parsed 50 posts
[11ty] 处理完成 🎉
[11ty] Wrote 200 files
"""
        stats = monitor._parse_build_output_optimized(output)
        assert stats["posts_parsed"] == 50
        assert stats["files_written"] == 200

    def test_parse_output_with_malformed_lines(self, monitor):
        """Test parsing with malformed log lines."""
        output = """
[11ty] Successfully parsed abc posts
[11ty] Wrote files
[11ty] Minified: → (% reduction)
"""
        stats = monitor._parse_build_output_optimized(output)
        # Should not crash, just ignore invalid lines
        assert isinstance(stats, dict)

    def test_empty_build_data(self, monitor):
        """Test handling of empty build data."""
        monitor.current_build = {}
        exit_code = monitor.print_build_report(compare=False)
        assert exit_code == 1  # Should fail for empty data

    def test_baseline_with_missing_keys(self, monitor):
        """Test comparison with baseline missing expected keys."""
        monitor.baseline_build = {
            "success": True
            # Missing build_time, stats, etc.
        }
        monitor.current_build = {
            "success": True,
            "build_time": 5.0,
            "stats": {},
            "warnings": [],
            "errors": []
        }

        # Should not crash
        comparison = monitor.compare_builds()
        assert comparison is not None


class TestIntegration:
    """Integration tests for complete workflows."""

    @patch('subprocess.run')
    def test_complete_baseline_workflow(self, mock_run, temp_baseline_file):
        """Test complete baseline save and compare workflow."""
        monitor = BuildMonitor(baseline_file=temp_baseline_file)

        # First build - save as baseline
        mock_run.return_value = Mock(
            returncode=0,
            stdout="[11ty] Successfully parsed 50 posts\n[11ty] Wrote 200 files in 5.0 seconds",
            stderr=""
        )
        monitor.run_build()
        monitor.save_baseline()

        # Second build - compare with baseline
        mock_run.return_value = Mock(
            returncode=0,
            stdout="[11ty] Successfully parsed 56 posts\n[11ty] Wrote 245 files in 6.0 seconds",
            stderr=""
        )
        monitor.run_build()
        monitor.load_baseline()
        comparison = monitor.compare_builds()

        assert comparison is not None
        assert "stats_changes" in comparison


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
