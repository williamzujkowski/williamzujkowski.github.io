#!/usr/bin/env -S uv run python3
"""
SCRIPT: test_manifest_v5_comprehensive.py
PURPOSE: Comprehensive testing suite for MANIFEST.json v5.0 production readiness
CATEGORY: testing
LLM_READY: True
VERSION: 1.0.0
CREATED: 2025-11-02

DESCRIPTION:
    Complete test suite validating MANIFEST v5.0 lazy loading implementation
    for production deployment. Tests functional requirements, performance,
    integration, stress conditions, regressions, and edge cases.

    Test categories:
    1. Functional: Lazy loading, hash validation, backward compatibility
    2. Performance: Load times, token reduction, pre-commit speedup
    3. Integration: Blog workflows, validation scripts, pre-commit hooks
    4. Stress: Large registry, duplicate detection, hash collisions
    5. Regression: Phase 1/2 optimizations, cross-references, build
    6. Edge Cases: Missing files, corruption, graceful fallback

USAGE:
    # Run all tests
    uv run pytest tests/integration/test_manifest_v5_comprehensive.py -v

    # Run specific test category
    uv run pytest tests/integration/test_manifest_v5_comprehensive.py -v -k functional

    # Generate detailed report
    uv run pytest tests/integration/test_manifest_v5_comprehensive.py -v --tb=short > test-results.txt

DEPENDENCIES:
    - pytest
    - scripts/lib/manifest_loader.py
    - MANIFEST.json v5.0
    - .manifest/file-registry.json

MANIFEST_REGISTRY: tests/integration/test_manifest_v5_comprehensive.py
"""

import json
import pytest
import time
import tempfile
import shutil
import hashlib
from pathlib import Path
from typing import Dict, Any
import sys
import subprocess

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from lib.manifest_loader import ManifestLoader


class TestFunctional:
    """Test 1: Functional Requirements - Core functionality validation"""

    def test_lazy_loading_core_only(self):
        """Verify core manifest loads without file registry"""
        loader = ManifestLoader()

        # Core should load instantly
        core = loader.get_core()

        # Registry should not be loaded yet
        assert loader._file_registry is None

        # Core should have essential fields
        assert "version" in core
        assert "repository" in core
        assert "enforcement" in core
        assert core["version"] == "5.0.0"

    def test_lazy_loading_registry_on_demand(self):
        """Verify file registry loads only when accessed"""
        loader = ManifestLoader()

        # Initial state: nothing loaded
        assert loader._file_registry is None

        # Access core: registry still not loaded
        core = loader.get_core()
        assert loader._file_registry is None

        # Access registry: now it loads
        registry = loader.get_file_registry()
        assert loader._file_registry is not None
        assert isinstance(registry, dict)
        assert len(registry) > 0

    def test_hash_validation(self):
        """Verify hash validation works correctly"""
        loader = ManifestLoader()

        # Get stored hash
        stored_hash = loader.get_registry_hash()
        assert stored_hash
        assert len(stored_hash) == 16  # First 16 chars of SHA256

        # Calculate hash from registry
        calculated_hash = loader.calculate_registry_hash()

        # Should match
        assert stored_hash == calculated_hash

    def test_file_exists_check(self):
        """Verify file existence checking"""
        loader = ManifestLoader()

        # Check known file
        assert loader.file_exists("MANIFEST.json")
        assert loader.file_exists("CLAUDE.md")

        # Check non-existent file
        assert not loader.file_exists("nonexistent-file-xyz-123.txt")

    def test_backward_compatibility_v4_format(self):
        """Verify v4.0 format compatibility"""
        loader = ManifestLoader()

        # Get legacy format
        legacy = loader.get_legacy_format()

        # Should have v4.0 structure
        assert "inventory" in legacy
        assert "files" in legacy["inventory"]
        assert "file_registry" in legacy["inventory"]["files"]

        # Registry should be dict, not lazy-load pointer
        registry = legacy["inventory"]["files"]["file_registry"]
        assert isinstance(registry, dict)
        assert "_lazy_load" not in registry

        # Should have file count
        assert legacy["inventory"]["files"]["total_count"] == len(registry)

    def test_file_registry_structure(self):
        """Verify file registry structure is valid"""
        loader = ManifestLoader()
        registry = loader.get_file_registry()

        # Should have entries
        assert len(registry) > 0

        # Check structure of a few entries
        for filepath, metadata in list(registry.items())[:5]:
            assert isinstance(filepath, str)
            assert isinstance(metadata, dict)
            # Should have standard fields
            assert "size" in metadata or "type" in metadata

    def test_add_file_to_registry(self, tmp_path):
        """Verify adding files to registry works"""
        # Create temporary manifest
        test_manifest = tmp_path / "MANIFEST.json"
        test_registry_dir = tmp_path / ".manifest"
        test_registry_dir.mkdir()
        test_registry = test_registry_dir / "file-registry.json"

        # Copy current structure
        shutil.copy("MANIFEST.json", test_manifest)
        shutil.copy(".manifest/file-registry.json", test_registry)

        # Create loader for temp manifest
        loader = ManifestLoader(test_manifest)

        # Add new file
        test_file = "test/new-file.txt"
        test_metadata = {"size": 100, "type": "txt", "modified": "2025-11-02"}

        initial_count = len(loader.get_file_registry())
        loader.add_file_to_registry(test_file, test_metadata)

        # Reload and verify
        loader_reload = ManifestLoader(test_manifest)
        registry = loader_reload.get_file_registry()

        assert test_file in registry
        assert registry[test_file] == test_metadata
        assert len(registry) == initial_count + 1


class TestPerformance:
    """Test 2: Performance Requirements - Speed and efficiency validation"""

    def test_core_load_time(self):
        """Verify core manifest loads under 100ms"""
        loader = ManifestLoader()

        # Measure load time
        start = time.time()
        core = loader.get_core()
        duration_ms = (time.time() - start) * 1000

        # Should be VERY fast (typically <1ms)
        assert duration_ms < 100
        print(f"\n    Core load time: {duration_ms:.2f}ms")

    def test_registry_load_time(self):
        """Verify file registry loads reasonably fast"""
        loader = ManifestLoader()

        # Measure load time
        start = time.time()
        registry = loader.get_file_registry()
        duration_ms = (time.time() - start) * 1000

        # Should be under 500ms even for large registry
        assert duration_ms < 500
        print(f"\n    Registry load time: {duration_ms:.2f}ms for {len(registry)} files")

    def test_hash_check_performance(self):
        """Verify hash checking is instant"""
        loader = ManifestLoader()

        # Measure hash check time
        start = time.time()
        hash_val = loader.get_registry_hash()
        duration_ms = (time.time() - start) * 1000

        # Should be nearly instant (<10ms)
        assert duration_ms < 10
        print(f"\n    Hash check time: {duration_ms:.2f}ms")

    def test_token_reduction_validation(self):
        """Verify claimed token reduction is accurate"""
        loader = ManifestLoader()

        # Get core (small)
        core = loader.get_core()
        core_json = json.dumps(core)
        core_tokens = len(core_json) // 4  # Rough estimate: 4 chars per token

        # Get legacy (full)
        legacy = loader.get_legacy_format()
        legacy_json = json.dumps(legacy)
        legacy_tokens = len(legacy_json) // 4

        # Calculate actual reduction
        reduction = ((legacy_tokens - core_tokens) / legacy_tokens) * 100

        print(f"\n    Core tokens: ~{core_tokens}")
        print(f"\n    Legacy tokens: ~{legacy_tokens}")
        print(f"\n    Reduction: {reduction:.1f}%")

        # Should be >90% reduction
        assert reduction > 90

    def test_concurrent_access(self):
        """Verify thread-safe concurrent access"""
        from concurrent.futures import ThreadPoolExecutor

        loader = ManifestLoader()

        def access_manifest():
            core = loader.get_core()
            registry = loader.get_file_registry()
            hash_val = loader.get_registry_hash()
            return len(registry)

        # Access from multiple threads
        with ThreadPoolExecutor(max_workers=10) as executor:
            start = time.time()
            futures = [executor.submit(access_manifest) for _ in range(20)]
            results = [f.result() for f in futures]
            duration_ms = (time.time() - start) * 1000

        # All should return same count
        assert len(set(results)) == 1
        print(f"\n    20 concurrent accesses: {duration_ms:.2f}ms")


class TestIntegration:
    """Test 3: Integration Testing - Real workflow validation"""

    def test_precommit_validators_integration(self):
        """Verify pre-commit validators work with v5.0"""
        # Import validators
        from lib.precommit_validators import (
            validate_manifest,
            check_duplicates,
            check_standards_compliance
        )

        # Run validators
        success, msg = validate_manifest()
        assert success, f"Manifest validation failed: {msg}"

        success, msg = check_duplicates()
        assert success or "No files staged" in msg, f"Duplicate check failed: {msg}"

        success, msg = check_standards_compliance()
        assert success, f"Standards check failed: {msg}"

    def test_manifest_loader_import(self):
        """Verify manifest loader can be imported from validators"""
        # This is what pre-commit validators do
        try:
            from lib.manifest_loader import ManifestLoader
            loader = ManifestLoader()
            core = loader.get_core()
            assert core["version"] == "5.0.0"
        except ImportError as e:
            pytest.fail(f"Failed to import ManifestLoader: {e}")

    def test_hash_based_duplicate_detection(self):
        """Verify hash-based duplicate detection works"""
        loader = ManifestLoader()

        # Get current hash
        hash_before = loader.get_registry_hash()

        # Simulate checking for duplicates
        # In real workflow, we'd compare hash to detect changes
        # without loading full registry

        # Load registry (only if needed)
        registry = loader.get_file_registry()

        # Calculate hash from loaded registry
        hash_calculated = loader.calculate_registry_hash()

        # Should match
        assert hash_before == hash_calculated

    def test_backward_compatible_script_access(self):
        """Verify scripts expecting v4.0 still work"""
        # Simulate old script accessing manifest
        with open("MANIFEST.json") as f:
            manifest = json.load(f)

        # Old scripts would check version
        assert "version" in manifest

        # For v5.0, they need to use loader
        if manifest.get("schema") == "optimized-lazy-loading":
            loader = ManifestLoader()
            legacy_manifest = loader.get_legacy_format()

            # Should have old structure
            assert "inventory" in legacy_manifest
            assert "files" in legacy_manifest["inventory"]
            assert isinstance(
                legacy_manifest["inventory"]["files"]["file_registry"],
                dict
            )


class TestStress:
    """Test 4: Stress Testing - Performance under load"""

    def test_large_file_additions(self, tmp_path):
        """Test adding 100 files to registry"""
        # Create temporary manifest
        test_manifest = tmp_path / "MANIFEST.json"
        test_registry_dir = tmp_path / ".manifest"
        test_registry_dir.mkdir()
        test_registry = test_registry_dir / "file-registry.json"

        # Start with minimal registry
        shutil.copy("MANIFEST.json", test_manifest)

        # Create small initial registry
        initial_registry = {"test.txt": {"size": 100, "type": "txt"}}
        with open(test_registry, "w") as f:
            json.dump(initial_registry, f)

        loader = ManifestLoader(test_manifest)

        # Add 100 files
        start = time.time()
        for i in range(100):
            filepath = f"test/file-{i}.txt"
            metadata = {"size": i * 100, "type": "txt", "modified": "2025-11-02"}
            loader.add_file_to_registry(filepath, metadata)
            loader = ManifestLoader(test_manifest)  # Reload to simulate real usage

        duration = time.time() - start

        # Reload and verify
        final_loader = ManifestLoader(test_manifest)
        final_registry = final_loader.get_file_registry()

        assert len(final_registry) == 101  # 1 initial + 100 added
        print(f"\n    Added 100 files in {duration:.2f}s ({duration/100:.3f}s per file)")

    def test_duplicate_detection_performance(self):
        """Test duplicate detection with large registry"""
        loader = ManifestLoader()
        registry = loader.get_file_registry()

        # Simulate checking 100 new files for duplicates
        test_files = [f"new-file-{i}.txt" for i in range(100)]

        start = time.time()
        duplicates = []
        for test_file in test_files:
            # Check if filename exists
            test_name = Path(test_file).name
            for existing in registry.keys():
                if Path(existing).name == test_name:
                    duplicates.append((test_file, existing))
                    break
        duration_ms = (time.time() - start) * 1000

        print(f"\n    Checked 100 files for duplicates in {duration_ms:.2f}ms")
        assert duration_ms < 1000  # Should be under 1 second

    def test_hash_collision_handling(self):
        """Verify hash provides sufficient uniqueness"""
        # Hash is first 16 chars of SHA256
        # Collision probability is negligible for our use case

        loader = ManifestLoader()
        registry = loader.get_file_registry()

        # Calculate hash
        hash_val = loader.calculate_registry_hash()

        # Hash should be consistent
        hash_val2 = loader.calculate_registry_hash()
        assert hash_val == hash_val2

        # Different registry should have different hash
        registry_modified = registry.copy()
        registry_modified["test-collision-file.txt"] = {"size": 999}

        modified_json = json.dumps(registry_modified, sort_keys=True)
        modified_hash = hashlib.sha256(modified_json.encode()).hexdigest()[:16]

        assert hash_val != modified_hash


class TestRegression:
    """Test 5: Regression Testing - Ensure previous optimizations still work"""

    def test_phase1_parallel_precommit_still_works(self):
        """Verify Phase 1 parallel pre-commit hooks still work"""
        # Check pre-commit hook exists
        hook_path = Path(".git/hooks/pre-commit")
        assert hook_path.exists(), "Pre-commit hook missing"

        # Should use parallel execution
        with open(hook_path) as f:
            content = f.read()
            assert "parallel" in content.lower() or "concurrent" in content.lower()

    def test_phase2_cli_standardization_intact(self):
        """Verify Phase 2 CLI standardization still present"""
        # Check a few key scripts for standardization
        test_scripts = [
            "scripts/blog-content/humanization-validator.py",
            "scripts/lib/manifest_loader.py"
        ]

        for script in test_scripts:
            script_path = Path(script)
            if script_path.exists():
                with open(script_path) as f:
                    content = f.read()
                    # Should have LLM-ready header
                    assert "SCRIPT:" in content or "PURPOSE:" in content

    def test_manifest_structure_preserved(self):
        """Verify core MANIFEST fields preserved from v4.0"""
        loader = ManifestLoader()
        core = loader.get_core()

        # Essential fields from v4.0
        assert "version" in core
        assert "repository" in core
        assert "enforcement" in core
        assert "inventory" in core

        # v5.0 additions
        assert "lazy_metadata" in core
        assert "optimization" in core
        assert "migration" in core

    def test_build_still_passes(self):
        """Verify npm build still works"""
        result = subprocess.run(
            ["npm", "run", "build"],
            capture_output=True,
            text=True,
            timeout=60
        )

        # Build should succeed
        assert result.returncode == 0, f"Build failed: {result.stderr}"


class TestEdgeCases:
    """Test 6: Edge Cases - Error handling and graceful degradation"""

    def test_missing_registry_file(self, tmp_path):
        """Verify graceful handling of missing registry file"""
        # Create manifest without registry file
        test_manifest = tmp_path / "MANIFEST.json"

        # Copy core manifest
        shutil.copy("MANIFEST.json", test_manifest)

        # Don't create .manifest directory
        loader = ManifestLoader(test_manifest)

        # Should gracefully return empty registry
        registry = loader.get_file_registry()
        assert isinstance(registry, dict)
        # May be empty or fall back to core manifest

    def test_corrupted_registry_json(self, tmp_path):
        """Verify handling of corrupted registry JSON"""
        # Create manifest with corrupted registry
        test_manifest = tmp_path / "MANIFEST.json"
        test_registry_dir = tmp_path / ".manifest"
        test_registry_dir.mkdir()
        test_registry = test_registry_dir / "file-registry.json"

        shutil.copy("MANIFEST.json", test_manifest)

        # Write corrupted JSON
        with open(test_registry, "w") as f:
            f.write("{ invalid json")

        loader = ManifestLoader(test_manifest)

        # Should raise appropriate error
        with pytest.raises(json.JSONDecodeError):
            loader.get_file_registry()

    def test_manual_manifest_edit_detection(self):
        """Verify hash detects manual edits"""
        loader = ManifestLoader()

        # Get current hash
        original_hash = loader.get_registry_hash()

        # Get registry
        registry = loader.get_file_registry()

        # Modify registry
        registry["manual-edit-test.txt"] = {"size": 999}

        # Calculate new hash
        modified_json = json.dumps(registry, sort_keys=True)
        new_hash = hashlib.sha256(modified_json.encode()).hexdigest()[:16]

        # Hashes should differ
        assert original_hash != new_hash

    def test_rollback_procedure(self, tmp_path):
        """Verify rollback to v4.0 works"""
        # Check legacy backup exists
        legacy_path = Path(".manifest/MANIFEST.legacy.json")
        assert legacy_path.exists(), "Legacy backup missing"

        # Verify it's valid JSON
        with open(legacy_path) as f:
            legacy = json.load(f)

        # Should have v4.0 structure
        assert "inventory" in legacy
        assert "files" in legacy["inventory"]
        registry = legacy["inventory"]["files"]["file_registry"]
        assert isinstance(registry, dict)
        assert "_lazy_load" not in registry

    def test_empty_registry_handling(self, tmp_path):
        """Verify handling of empty registry"""
        # Create manifest with empty registry
        test_manifest = tmp_path / "MANIFEST.json"
        test_registry_dir = tmp_path / ".manifest"
        test_registry_dir.mkdir()
        test_registry = test_registry_dir / "file-registry.json"

        shutil.copy("MANIFEST.json", test_manifest)

        # Write empty registry
        with open(test_registry, "w") as f:
            json.dump({}, f)

        loader = ManifestLoader(test_manifest)
        registry = loader.get_file_registry()

        # Should handle empty registry
        assert isinstance(registry, dict)
        assert len(registry) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
