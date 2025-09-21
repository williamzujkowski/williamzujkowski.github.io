"""
Unit tests for scripts/lib/common.py modules
"""

import pytest
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
sys.path.append('scripts')
from lib.common import (
    ManifestManager, TimeManager, Logger
)

class TestManifestManager:
    """Test ManifestManager functionality"""

    def test_manifest_load(self, temp_dir, manifest_fixture):
        """Test loading manifest file"""
        manifest_path = temp_dir / "MANIFEST.json"
        manifest_path.write_text(json.dumps(manifest_fixture))

        with patch('lib.common.Path.cwd') as mock_cwd:
            mock_cwd.return_value = temp_dir
            manager = ManifestManager()

            assert manager.manifest['version'] == "4.0.0"
            assert manager.manifest['repository']['name'] == "test-repo"

    def test_manifest_update_section(self, temp_dir, manifest_fixture):
        """Test updating manifest sections"""
        manifest_path = temp_dir / "MANIFEST.json"
        manifest_path.write_text(json.dumps(manifest_fixture))

        with patch('lib.common.Path.cwd') as mock_cwd:
            mock_cwd.return_value = temp_dir
            manager = ManifestManager()

            # Update a section
            manager.manifest["test_section"] = {"test": "data"}
            assert manager.manifest["test_section"]["test"] == "data"

    def test_manifest_save(self, temp_dir, manifest_fixture):
        """Test saving manifest with timestamp"""
        manifest_path = temp_dir / "MANIFEST.json"
        manifest_path.write_text(json.dumps(manifest_fixture))

        with patch('lib.common.Path.cwd') as mock_cwd:
            mock_cwd.return_value = temp_dir
            manager = ManifestManager()

            # Save manifest
            manager.save_manifest()

            saved_data = json.loads(manifest_path.read_text())
            assert "last_updated" in saved_data

class TestTimeManager:
    """Test TimeManager functionality"""

    @patch('requests.get')
    def test_get_time_from_timegov(self, mock_get):
        """Test fetching time from time.gov"""
        mock_response = Mock()
        mock_response.text = '<timestamp time="1234567890000"/>'
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        time_mgr = TimeManager()
        # Note: get_current_timestamp is the actual method
        result = time_mgr.get_current_timestamp()

        assert result is not None
        assert isinstance(result, str)

    def test_timestamp_format(self):
        """Test timestamp generation"""
        time_mgr = TimeManager()
        timestamp = time_mgr.get_current_timestamp()

        # Should be in ISO format
        assert "T" in timestamp
        assert "-" in timestamp  # Date separators
        assert ":" in timestamp  # Time separators

class TestLogger:
    """Test Logger functionality"""

    def test_logger_creation(self):
        """Test logger can be created"""
        logger = Logger.get_logger("test_logger")

        assert logger is not None
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'warning')

    def test_logger_singleton(self):
        """Test logger returns same instance for same name"""
        logger1 = Logger.get_logger("test")
        logger2 = Logger.get_logger("test")

        assert logger1 is logger2

def test_all_common_imports():
    """Test that all common modules can be imported"""
    from lib import common

    # Check all expected classes exist
    assert hasattr(common, 'ManifestManager')
    assert hasattr(common, 'TimeManager')
    assert hasattr(common, 'Logger')