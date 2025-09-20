#!/usr/bin/env python3
"""
SCRIPT: create_enforcement_rules.py
PURPOSE: Generate comprehensive enforcement rules from standards submodule
CATEGORY: validation
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T16:10:00-04:00

DESCRIPTION:
    Creates .claude-rules.json with mandatory enforcement rules extracted from
    the standards submodule. This ensures all future LLM operations follow
    established patterns and prevents violations.

LLM_USAGE:
    python scripts/create_enforcement_rules.py [options]

ARGUMENTS:
    --force (bool): Overwrite existing rules file
    --validate (bool): Validate rules after creation
    --verbose (bool): Show detailed output

EXAMPLES:
    # Create enforcement rules
    python scripts/create_enforcement_rules.py

    # Force recreate and validate
    python scripts/create_enforcement_rules.py --force --validate

OUTPUT:
    - .claude-rules.json with comprehensive enforcement rules
    - Validation report if --validate is used

DEPENDENCIES:
    - Python 3.8+
    - scripts/lib/common.py for shared utilities

MANIFEST_REGISTRY: scripts/create_enforcement_rules.py
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))
from lib.common import TimeManager, ManifestManager, Logger

class EnforcementRulesGenerator:
    """Generate enforcement rules from standards submodule"""

    def __init__(self):
        self.time_mgr = TimeManager()
        self.manifest_mgr = ManifestManager()
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.standards_dir = Path(".standards/docs/standards")

        # Map standards files to their enforcement areas
        self.standards_map = {
            "KNOWLEDGE_MANAGEMENT": {
                "file": "KNOWLEDGE_MANAGEMENT_STANDARDS.md",
                "applies_to": ["docs/", "MANIFEST.json", "CLAUDE.md", "*.md"],
                "critical": True
            },
            "CODING_STANDARDS": {
                "file": "CODING_STANDARDS.md",
                "applies_to": ["scripts/", "src/", ".eleventy.js", "*.py", "*.js"],
                "critical": True
            },
            "FRONTEND_MOBILE": {
                "file": "FRONTEND_MOBILE_STANDARDS.md",
                "applies_to": ["src/", "tailwind.config.js", "*.css", "*.html"],
                "critical": False
            },
            "CONTENT_STANDARDS": {
                "file": "CONTENT_STANDARDS.md",
                "applies_to": ["src/posts/", "src/pages/", "*.md"],
                "critical": True
            },
            "GITHUB_PLATFORM": {
                "file": "GITHUB_PLATFORM_STANDARDS.md",
                "applies_to": [".github/", "README.md", ".gitignore"],
                "critical": True
            },
            "SEO_WEB_MARKETING": {
                "file": "SEO_WEB_MARKETING_STANDARDS.md",
                "applies_to": ["src/posts/", "src/pages/", "sitemap.xml"],
                "critical": False
            },
            "TESTING_STANDARDS": {
                "file": "TESTING_STANDARDS.md",
                "applies_to": ["tests/", "*.test.py", "*.test.js"],
                "critical": False
            }
        }

    def extract_rules_from_standard(self, filepath: Path) -> List[str]:
        """Extract actionable rules from a standards markdown file"""
        rules = []

        if not filepath.exists():
            self.logger.warning(f"Standards file not found: {filepath}")
            return rules

        with open(filepath, 'r') as f:
            content = f.read()

        # Extract MUST/SHALL rules
        must_pattern = r'(?:^|\n)[\s\-\*]*(?:MUST|SHALL)\s+([^.\n]+[.\n])'
        must_matches = re.findall(must_pattern, content, re.IGNORECASE)

        for match in must_matches[:10]:  # Limit to top 10 rules per standard
            rule = match.strip().replace('\n', ' ')
            if len(rule) > 20:  # Filter out very short matches
                rules.append(f"MUST {rule}")

        # Extract SHOULD rules
        should_pattern = r'(?:^|\n)[\s\-\*]*SHOULD\s+([^.\n]+[.\n])'
        should_matches = re.findall(should_pattern, content, re.IGNORECASE)

        for match in should_matches[:5]:  # Limit to top 5 SHOULD rules
            rule = match.strip().replace('\n', ' ')
            if len(rule) > 20:
                rules.append(f"SHOULD {rule}")

        # Extract specific patterns for this repository
        if "KNOWLEDGE_MANAGEMENT" in filepath.name:
            rules.extend([
                "MUST maintain MANIFEST.json as single source of truth",
                "MUST use progressive disclosure in documentation",
                "MUST provide token-optimized content loading",
                "MUST include machine-readable metadata",
                "MUST update MANIFEST.json after any file operation",
                "MUST check file_registry before creating any new file"
            ])
        elif "CODING_STANDARDS" in filepath.name:
            rules.extend([
                "MUST follow language-specific standards",
                "MUST include comprehensive docstrings",
                "MUST use semantic naming",
                "MUST implement error handling",
                "MUST follow DRY principles",
                "MUST implement SOLID principles"
            ])
        elif "CONTENT_STANDARDS" in filepath.name:
            rules.extend([
                "MUST include proper frontmatter",
                "MUST optimize for SEO",
                "MUST use consistent formatting",
                "MUST provide alt text for images",
                "MUST include citations for claims",
                "MUST validate links regularly"
            ])

        return rules

    def create_enforcement_rules(self) -> Dict[str, Any]:
        """Generate comprehensive enforcement rules"""

        timestamp = self.time_mgr.get_current_timestamp()

        claude_rules = {
            "version": "2.0.0",
            "standards_source": "https://github.com/williamzujkowski/standards",
            "generated": timestamp,
            "last_validated": timestamp,

            "MANDATORY_STANDARDS": {},

            "LLM_ENFORCEMENT": {
                "CRITICAL_RULES": [
                    "ALWAYS check MANIFEST.json before ANY file operation",
                    "NEVER create duplicate files - use existing files",
                    "ALWAYS use time.gov for timestamps when available",
                    "MUST update MANIFEST.json after EVERY file change",
                    "MUST follow standards from https://github.com/williamzujkowski/standards",
                    "NEVER save working files to root - use appropriate directories",
                    "ALWAYS update existing files instead of creating new ones",
                    "MUST maintain backward compatibility",
                    "ALWAYS validate changes against standards",
                    "MUST use scripts/lib/common.py for shared functionality"
                ],

                "BEFORE_ANY_OPERATION": [
                    "CHECK: MANIFEST.json is current",
                    "CHECK: No duplicate files exist for intended operation",
                    "CHECK: Target directory is appropriate for file type",
                    "CHECK: Standards compliance for operation type",
                    "CHECK: Time source (prefer time.gov, fallback to system)"
                ],

                "FILE_OPERATIONS": {
                    "CREATE": [
                        "MUST check file_registry in MANIFEST.json for duplicates",
                        "MUST use appropriate directory structure",
                        "MUST add to MANIFEST.json immediately",
                        "MUST include proper documentation",
                        "NEVER create files in root directory"
                    ],
                    "UPDATE": [
                        "MUST preserve file purpose and structure",
                        "MUST update modified timestamp",
                        "MUST validate against standards",
                        "MUST update MANIFEST.json",
                        "MUST backup critical files before major changes"
                    ],
                    "DELETE": [
                        "MUST check for dependencies",
                        "MUST update all references",
                        "MUST remove from MANIFEST.json",
                        "MUST document reason for deletion",
                        "NEVER delete protected files"
                    ]
                },

                "SCRIPT_OPERATIONS": [
                    "MUST follow LLM documentation standard from Phase 2",
                    "MUST import from scripts/lib/common.py for shared functionality",
                    "MUST update llm_interface in MANIFEST.json",
                    "MUST provide clear examples",
                    "MUST handle errors gracefully"
                ],

                "CONTENT_OPERATIONS": [
                    "MUST validate frontmatter against schema",
                    "MUST ensure hero images exist or generate them",
                    "MUST verify research citations with hyperlinks",
                    "MUST limit code blocks to essential examples",
                    "MUST check alt text for all images",
                    "MUST run link validation after changes"
                ]
            },

            "VALIDATION_GATES": {
                "pre_commit": {
                    "scripts": [
                        "scripts/validate_manifest.py",
                        "scripts/check_standards.py",
                        "scripts/verify_no_duplicates.py"
                    ],
                    "must_pass": True
                },
                "ci_pipeline": {
                    "workflows": [
                        ".github/workflows/standards_enforcement.yml",
                        ".github/workflows/manifest_validation.yml",
                        ".github/workflows/link-monitor.yml"
                    ],
                    "blocks_merge": True
                }
            },

            "PENALTIES": {
                "duplicate_file_created": "BLOCK and require cleanup",
                "manifest_not_updated": "BLOCK until synchronized",
                "standards_violation": "WARNING with required fix",
                "documentation_missing": "WARNING with 24-hour fix window",
                "time_not_authoritative": "WARNING - document time source used",
                "vestigial_content": "FLAG for removal",
                "protected_file_modified": "BLOCK and require review"
            },

            "PROTECTED_FILES": [
                "CLAUDE.md",
                "MANIFEST.json",
                ".claude-rules.json",
                ".eleventy.js",
                "package.json",
                "tailwind.config.js",
                "README.md",
                "scripts/lib/common.py"
            ],

            "DIRECTORY_STRUCTURE": {
                "scripts": {
                    "purpose": "Python and shell scripts for automation",
                    "allowed": ["*.py", "*.sh"],
                    "subdirs": ["lib", "link-validation"]
                },
                "src": {
                    "purpose": "Source files for static site",
                    "allowed": ["*.md", "*.njk", "*.html", "*.css", "*.js"],
                    "subdirs": ["posts", "pages", "assets", "_includes", "_data"]
                },
                "docs": {
                    "purpose": "Documentation and guides",
                    "allowed": ["*.md", "*.txt"],
                    "subdirs": ["guides", "standards", "archive"]
                },
                "reports": {
                    "purpose": "Generated reports and analysis",
                    "allowed": ["*.md", "*.json", "*.html"],
                    "subdirs": []
                },
                "tests": {
                    "purpose": "Test files and fixtures",
                    "allowed": ["*.test.py", "*.test.js", "*.json"],
                    "subdirs": ["fixtures", "unit", "integration"]
                }
            }
        }

        # Process each standard and extract rules
        for standard_name, config in self.standards_map.items():
            filepath = self.standards_dir / config["file"]
            rules = self.extract_rules_from_standard(filepath)

            if rules:
                # Use simple relative path instead of relative_to
                relative_path = str(filepath).replace(str(Path.cwd()) + "/", "")
                claude_rules["MANDATORY_STANDARDS"][standard_name] = {
                    "source": relative_path,
                    "rules": rules[:10],  # Limit to top 10 rules per standard
                    "applies_to": config["applies_to"],
                    "critical": config["critical"]
                }
                self.logger.info(f"Extracted {len(rules)} rules from {standard_name}")

        return claude_rules

    def validate_rules(self, rules: Dict[str, Any]) -> bool:
        """Validate the generated rules structure"""
        required_sections = [
            "version",
            "standards_source",
            "MANDATORY_STANDARDS",
            "LLM_ENFORCEMENT",
            "VALIDATION_GATES",
            "PENALTIES",
            "PROTECTED_FILES"
        ]

        for section in required_sections:
            if section not in rules:
                self.logger.error(f"Missing required section: {section}")
                return False

        # Check that we have at least some standards
        if not rules["MANDATORY_STANDARDS"]:
            self.logger.error("No standards extracted")
            return False

        self.logger.info("Rules structure validated successfully")
        return True

    def save_rules(self, rules: Dict[str, Any], force: bool = False) -> bool:
        """Save rules to .claude-rules.json"""
        rules_path = Path(".claude-rules.json")

        if rules_path.exists() and not force:
            # Merge with existing rules instead of overwriting
            self.logger.info("Merging with existing .claude-rules.json")
            with open(rules_path, 'r') as f:
                existing_rules = json.load(f)

            # Update version and timestamp
            existing_rules["version"] = rules["version"]
            existing_rules["generated"] = rules["generated"]
            existing_rules["last_validated"] = rules["last_validated"]

            # Merge standards
            for standard, config in rules["MANDATORY_STANDARDS"].items():
                if standard not in existing_rules["MANDATORY_STANDARDS"]:
                    existing_rules["MANDATORY_STANDARDS"][standard] = config

            rules = existing_rules

        with open(rules_path, 'w') as f:
            json.dump(rules, f, indent=2)

        self.logger.info(f"Saved enforcement rules to {rules_path}")
        return True


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate enforcement rules from standards submodule"
    )

    parser.add_argument('--force', action='store_true',
                       help='Overwrite existing rules file')
    parser.add_argument('--validate', action='store_true',
                       help='Validate rules after creation')
    parser.add_argument('--verbose', action='store_true',
                       help='Show detailed output')

    args = parser.parse_args()

    # Initialize generator
    generator = EnforcementRulesGenerator()

    # Generate rules
    print("📋 Generating enforcement rules from standards submodule...")
    rules = generator.create_enforcement_rules()

    # Validate if requested
    if args.validate:
        if not generator.validate_rules(rules):
            print("❌ Rules validation failed")
            return 1

    # Save rules
    if generator.save_rules(rules, force=args.force):
        print("✅ Created .claude-rules.json with comprehensive enforcement rules")

        # Print summary
        print(f"\n📊 Summary:")
        print(f"  Standards processed: {len(rules['MANDATORY_STANDARDS'])}")
        print(f"  Critical rules: {len(rules['LLM_ENFORCEMENT']['CRITICAL_RULES'])}")
        print(f"  Protected files: {len(rules['PROTECTED_FILES'])}")
        print(f"  Validation gates: {len(rules['VALIDATION_GATES'])}")

        if args.verbose:
            print(f"\n📜 Standards included:")
            for standard in rules['MANDATORY_STANDARDS'].keys():
                print(f"  - {standard}")

        return 0
    else:
        print("❌ Failed to save enforcement rules")
        return 1


if __name__ == "__main__":
    sys.exit(main())