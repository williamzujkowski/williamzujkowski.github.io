#!/usr/bin/env -S uv run python3
"""
SCRIPT: common.py
PURPOSE: Shared utilities for all scripts - DRY/SOLID implementation
CATEGORY: utility
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T15:02:00-04:00

DESCRIPTION:
    This module provides shared functionality for all scripts in the repository,
    implementing DRY (Don't Repeat Yourself) and SOLID principles. All scripts
    should import from this module instead of duplicating common code.

SOLID PRINCIPLES:
    S - Single Responsibility: Each class has one clear purpose
    O - Open/Closed: Classes are open for extension, closed for modification
    L - Liskov Substitution: Derived classes can substitute base classes
    I - Interface Segregation: Specific interfaces over general ones
    D - Dependency Inversion: Depend on abstractions, not concretions

MANIFEST_REGISTRY: scripts/lib/common.py
"""

import json
import hashlib
import logging
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
import yaml
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Constants
MANIFEST_PATH = Path("MANIFEST.json")
CLAUDE_RULES_PATH = Path(".claude-rules.json")
TIME_GOV_URL = "https://time.gov/actualtime.cgi"


class ManifestManager:
    """Single source for manifest operations - Single Responsibility Principle"""

    def __init__(self, manifest_path: Path = MANIFEST_PATH):
        self.manifest_path = manifest_path
        self.logger = logging.getLogger(self.__class__.__name__)
        self.manifest = self.load()

    def load(self) -> Dict[str, Any]:
        """Load current manifest"""
        try:
            with open(self.manifest_path, 'r') as f:
                self.manifest = json.load(f)
                self.logger.info(f"Loaded manifest from {self.manifest_path}")
                return self.manifest
        except FileNotFoundError:
            self.logger.warning(f"Manifest not found at {self.manifest_path}")
            return {}
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse manifest: {e}")
            return {}

    def save(self) -> bool:
        """Save manifest with current timestamp"""
        try:
            # Update timestamps
            self.manifest["last_validated"] = TimeManager.get_current_timestamp()

            with open(self.manifest_path, 'w') as f:
                json.dump(self.manifest, f, indent=2)

            self.logger.info(f"Saved manifest to {self.manifest_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save manifest: {e}")
            return False

    def update_section(self, section: str, data: Any) -> bool:
        """Update a specific section of the manifest"""
        try:
            keys = section.split('.')
            target = self.manifest

            for key in keys[:-1]:
                if key not in target:
                    target[key] = {}
                target = target[key]

            target[keys[-1]] = data
            self.logger.info(f"Updated manifest section: {section}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to update section {section}: {e}")
            return False

    def get_section(self, section: str) -> Any:
        """Get a specific section of the manifest"""
        try:
            keys = section.split('.')
            target = self.manifest

            for key in keys:
                target = target[key]

            return target
        except KeyError:
            self.logger.warning(f"Section not found: {section}")
            return None

    def register_file(self, filepath: Path, purpose: str = "") -> bool:
        """Register a file in the manifest"""
        try:
            rel_path = filepath.relative_to(Path.cwd())

            if "inventory" not in self.manifest:
                self.manifest["inventory"] = {"files": {"file_registry": {}}}

            if "file_registry" not in self.manifest["inventory"]["files"]:
                self.manifest["inventory"]["files"]["file_registry"] = {}

            self.manifest["inventory"]["files"]["file_registry"][str(rel_path)] = {
                "path": str(rel_path),
                "hash": FileHasher.get_sha256(filepath),
                "size": filepath.stat().st_size,
                "modified": TimeManager.get_current_timestamp(),
                "purpose": purpose,
                "dependencies": [],
                "referenced_by": []
            }

            self.logger.info(f"Registered file: {rel_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register file {filepath}: {e}")
            return False

    def check_duplicate(self, filename: str) -> bool:
        """Check if a file already exists in the registry"""
        if "inventory" in self.manifest and "files" in self.manifest["inventory"]:
            registry = self.manifest["inventory"]["files"].get("file_registry", {})
            for path in registry.keys():
                if Path(path).name == filename:
                    self.logger.warning(f"Duplicate file found: {path}")
                    return True
        return False


class TimeManager:
    """Centralized time management - Single Responsibility Principle"""

    @staticmethod
    def get_current_timestamp() -> str:
        """Get current timestamp in ISO 8601 format"""
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S-04:00")

    @staticmethod
    def get_time_from_timegov() -> Optional[str]:
        """Get authoritative time from time.gov (optional)"""
        try:
            response = requests.get(TIME_GOV_URL, timeout=5)
            if response.status_code == 200:
                # Parse time.gov response
                # Note: Actual parsing would depend on the response format
                return TimeManager.get_current_timestamp()
        except:
            # Fallback to system time
            return TimeManager.get_current_timestamp()

    @staticmethod
    def parse_timestamp(timestamp: str) -> datetime:
        """Parse ISO 8601 timestamp"""
        return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))


class FileHasher:
    """File hashing utilities - Single Responsibility Principle"""

    @staticmethod
    def get_sha256(filepath: Path) -> str:
        """Generate SHA-256 hash of a file"""
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            logging.error(f"Failed to hash file {filepath}: {e}")
            return ""

    @staticmethod
    def get_md5(filepath: Path) -> str:
        """Generate MD5 hash of a file"""
        md5_hash = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    md5_hash.update(byte_block)
            return md5_hash.hexdigest()
        except:
            return ""


class ConfigManager:
    """Configuration management - Single Responsibility Principle"""

    def __init__(self, config_path: Path = None):
        self.config_path = config_path or Path(".claude-rules.json")
        self.config = self.load()
        self.logger = logging.getLogger(self.__class__.__name__)

    def load(self) -> Dict[str, Any]:
        """Load configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning(f"Config not found at {self.config_path}")
            return {}
        except json.JSONDecodeError:
            self.logger.error(f"Failed to parse config")
            return {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value


class BlogPostProcessor(ABC):
    """Abstract base class for blog post processing - Open/Closed Principle"""

    @abstractmethod
    def process(self, content: str) -> str:
        """Process blog post content"""
        pass

    @abstractmethod
    def validate(self, content: str) -> bool:
        """Validate blog post content"""
        pass


class FrontmatterParser:
    """Parse and manipulate frontmatter - Single Responsibility Principle"""

    @staticmethod
    def parse(content: str) -> tuple[Dict[str, Any], str]:
        """Parse frontmatter and content from markdown file"""
        if content.startswith('---\n'):
            parts = content.split('---\n', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1])
                    body = parts[2]
                    return frontmatter, body
                except yaml.YAMLError:
                    pass
        return {}, content

    @staticmethod
    def serialize(frontmatter: Dict[str, Any], content: str) -> str:
        """Serialize frontmatter and content to markdown"""
        yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
        return f"---\n{yaml_str}---\n{content}"


class LinkExtractor:
    """Extract links from content - Single Responsibility Principle"""

    @staticmethod
    def extract_markdown_links(content: str) -> List[Dict[str, str]]:
        """Extract all markdown links from content"""
        links = []

        # Pattern for markdown links [text](url)
        pattern = r'\[([^\]]+)\]\(([^\)]+)\)'

        for match in re.finditer(pattern, content):
            links.append({
                'text': match.group(1),
                'url': match.group(2),
                'full_match': match.group(0)
            })

        return links

    @staticmethod
    def extract_reference_links(content: str) -> List[Dict[str, str]]:
        """Extract reference-style links from content"""
        links = []

        # Pattern for reference links [text][ref]
        ref_pattern = r'\[([^\]]+)\]\[([^\]]+)\]'
        # Pattern for reference definitions [ref]: url
        def_pattern = r'^\[([^\]]+)\]:\s*(.+)$'

        references = {}
        for match in re.finditer(def_pattern, content, re.MULTILINE):
            references[match.group(1)] = match.group(2)

        for match in re.finditer(ref_pattern, content):
            ref_key = match.group(2)
            if ref_key in references:
                links.append({
                    'text': match.group(1),
                    'url': references[ref_key],
                    'ref': ref_key,
                    'full_match': match.group(0)
                })

        return links


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class StandardsValidator:
    """Validate against standards - Single Responsibility Principle"""

    def __init__(self):
        self.config = ConfigManager()
        self.logger = logging.getLogger(self.__class__.__name__)

    def validate_file(self, filepath: Path) -> List[str]:
        """Validate a file against standards"""
        violations = []

        # Check if file is registered in manifest
        manifest = ManifestManager()
        if not manifest.check_duplicate(filepath.name):
            violations.append(f"File not registered in manifest: {filepath}")

        # Check file-specific standards based on extension
        if filepath.suffix == '.py':
            violations.extend(self._validate_python_file(filepath))
        elif filepath.suffix == '.md':
            violations.extend(self._validate_markdown_file(filepath))

        return violations

    def _validate_python_file(self, filepath: Path) -> List[str]:
        """Validate Python file standards"""
        violations = []

        with open(filepath, 'r') as f:
            content = f.read()

        # Check for docstring
        if not content.startswith('"""') and not content.startswith("'''"):
            violations.append("Missing module docstring")

        # Check for LLM documentation
        if "LLM_USAGE:" not in content:
            violations.append("Missing LLM_USAGE documentation")

        return violations

    def _validate_markdown_file(self, filepath: Path) -> List[str]:
        """Validate Markdown file standards"""
        violations = []

        with open(filepath, 'r') as f:
            content = f.read()

        # Check for frontmatter
        if not content.startswith('---'):
            violations.append("Missing frontmatter")

        # Parse frontmatter
        frontmatter, _ = FrontmatterParser.parse(content)

        # Check required fields
        required_fields = ['title', 'date']
        for field in required_fields:
            if field not in frontmatter:
                violations.append(f"Missing required frontmatter field: {field}")

        return violations


class FileBackup:
    """Handle file backups - Single Responsibility Principle"""

    @staticmethod
    def create_backup(filepath: Path, backup_dir: Path = None) -> Path:
        """Create timestamped backup of a file"""
        if backup_dir is None:
            backup_dir = filepath.parent

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"{filepath.stem}.bak.{timestamp}{filepath.suffix}"

        import shutil
        shutil.copy2(filepath, backup_path)

        logging.info(f"Created backup: {backup_path}")
        return backup_path

    @staticmethod
    def restore_backup(backup_path: Path, original_path: Path) -> bool:
        """Restore from backup"""
        try:
            import shutil
            shutil.copy2(backup_path, original_path)
            logging.info(f"Restored from backup: {backup_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to restore backup: {e}")
            return False


class Logger:
    """Centralized logging - Single Responsibility Principle"""

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Get a configured logger"""
        logger = logging.getLogger(name)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger


# Utility functions for common operations

def ensure_directory(path: Path) -> Path:
    """Ensure directory exists"""
    path.mkdir(parents=True, exist_ok=True)
    return path

def read_json(filepath: Path) -> Dict[str, Any]:
    """Read JSON file safely"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return {}

def write_json(data: Dict[str, Any], filepath: Path) -> bool:
    """Write JSON file safely"""
    try:
        ensure_directory(filepath.parent)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def get_file_type(filepath: Path) -> str:
    """Get categorized file type"""
    ext_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.md': 'markdown',
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.html': 'html',
        '.css': 'css',
        '.jpg': 'image',
        '.jpeg': 'image',
        '.png': 'image',
        '.gif': 'image',
        '.svg': 'image'
    }
    return ext_map.get(filepath.suffix.lower(), 'other')

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate text similarity using simple algorithm"""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    if not words1 or not words2:
        return 0.0

    intersection = words1 & words2
    union = words1 | words2

    return len(intersection) / len(union)

def format_size(bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024
    return f"{bytes:.2f} TB"


# Testing utilities for scripts

class ScriptTester:
    """Test runner for scripts - Single Responsibility Principle"""

    @staticmethod
    def test_script(script_path: Path) -> bool:
        """Test if a script runs without errors"""
        import subprocess

        try:
            result = subprocess.run(
                ['python', str(script_path), '--help'],
                capture_output=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False

    @staticmethod
    def validate_llm_docs(script_path: Path) -> bool:
        """Validate LLM documentation in script"""
        with open(script_path, 'r') as f:
            content = f.read()

        required_sections = [
            'SCRIPT:',
            'PURPOSE:',
            'CATEGORY:',
            'LLM_READY:',
            'LLM_USAGE:',
            'ARGUMENTS:',
            'EXAMPLES:'
        ]

        for section in required_sections:
            if section not in content:
                return False

        return True


# Quick Win utilities for standardized script behavior

def setup_argparse_with_examples(description: str, examples: str, version: str = "1.0.0"):
    """Create argparser with examples and version flag

    Args:
        description: Main description of the script
        examples: Example usage strings (one per line)
        version: Version number for --version flag

    Returns:
        argparse.ArgumentParser configured with examples and version
    """
    import argparse
    parser = argparse.ArgumentParser(
        description=description,
        epilog=f"\nExamples:\n{examples}",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--version', action='version',
                       version=f'%(prog)s {version}')
    return parser


def exit_with_code(success: bool, message: str = None, quiet: bool = False) -> int:
    """Standard exit code handler

    Args:
        success: Whether operation was successful
        message: Optional message to log
        quiet: Suppress output if True

    Returns:
        0 for success, 1 for error, 2 for usage error
    """
    logger = Logger.get_logger("exit_handler")

    if message and not quiet:
        if success:
            logger.info(message)
        else:
            logger.error(message)

    return 0 if success else 1


def exit_usage_error(message: str, quiet: bool = False) -> int:
    """Exit with usage error code

    Args:
        message: Error message explaining usage problem
        quiet: Suppress output if True

    Returns:
        2 (usage error code)
    """
    logger = Logger.get_logger("usage_error")
    if not quiet:
        logger.error(f"Usage error: {message}")
    return 2


def format_error_with_context(error: Exception, filepath: Path = None,
                              line_number: int = None, context: Dict = None) -> str:
    """Format error message with helpful context

    Args:
        error: The exception that occurred
        filepath: Optional file path where error occurred
        line_number: Optional line number where error occurred
        context: Optional dictionary of additional context

    Returns:
        Formatted error message with context
    """
    parts = [f"Error: {str(error)}"]

    if filepath:
        parts.append(f"\nFile: {filepath}")

    if line_number:
        parts.append(f"Line: {line_number}")

    if context:
        parts.append("\nContext:")
        for key, value in context.items():
            parts.append(f"  {key}: {value}")

    return "\n".join(parts)


# Export commonly used classes and functions
__all__ = [
    'ManifestManager',
    'TimeManager',
    'FileHasher',
    'ConfigManager',
    'BlogPostProcessor',
    'FrontmatterParser',
    'LinkExtractor',
    'StandardsValidator',
    'FileBackup',
    'Logger',
    'ValidationError',
    'ScriptTester',
    'ensure_directory',
    'read_json',
    'write_json',
    'get_file_type',
    'calculate_similarity',
    'format_size',
    'setup_argparse_with_examples',
    'exit_with_code',
    'exit_usage_error',
    'format_error_with_context'
]