"""Test configuration and fixtures"""
import sys
import os
import pytest
from pathlib import Path

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

@pytest.fixture
def manifest_fixture():
    """Provide test manifest data"""
    return {
        "version": "4.0.0",
        "repository": {"name": "test-repo"},
        "inventory": {"files": {"total_count": 0, "file_registry": {}}}
    }

@pytest.fixture
def temp_dir(tmp_path):
    """Provide temporary directory for tests"""
    return tmp_path