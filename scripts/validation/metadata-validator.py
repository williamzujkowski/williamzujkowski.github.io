#!/usr/bin/env -S uv run python3
"""
Metadata Quality Validator
Validates frontmatter metadata across all blog posts

Usage:
    uv run python scripts/validation/metadata-validator.py [--format json|text]
"""

import os
import sys
import yaml
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class MetadataValidator:
    def __init__(self, posts_dir: str = "src/posts"):
        self.posts_dir = Path(posts_dir)
        self.results = {
            "total_posts": 0,
            "posts_with_issues": [],
            "metadata_coverage": {},
            "issues_summary": {
                "missing_tags": 0,
                "missing_description": 0,
                "missing_author": 0,
                "missing_date": 0,
                "missing_hero_image": 0,
                "invalid_description_length": 0,
                "invalid_date_format": 0,
                "broken_image_paths": 0,
                "missing_title": 0
            }
        }

    def extract_frontmatter(self, file_path: Path) -> Tuple[Dict, str]:
        """Extract YAML frontmatter from markdown file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.startswith('---'):
            return {}, "No frontmatter found"

        try:
            # Find second --- delimiter
            end_index = content.find('---', 3)
            if end_index == -1:
                return {}, "Malformed frontmatter (no closing ---)"

            frontmatter_text = content[3:end_index].strip()
            frontmatter = yaml.safe_load(frontmatter_text)
            return frontmatter, None
        except yaml.YAMLError as e:
            return {}, f"YAML parsing error: {str(e)}"

    def validate_description_length(self, description: str) -> Tuple[bool, str]:
        """Validate description length (optimal: 120-160 chars for SEO)"""
        if not description:
            return False, "Missing"

        length = len(description)
        if length < 50:
            return False, f"Too short ({length} chars, recommend 120-160)"
        elif length > 200:
            return False, f"Too long ({length} chars, recommend 120-160)"
        elif length < 120 or length > 160:
            return True, f"Acceptable ({length} chars, optimal: 120-160)"
        else:
            return True, f"Optimal ({length} chars)"

    def validate_date_format(self, date_value) -> Tuple[bool, str]:
        """Validate date format"""
        if not date_value:
            return False, "Missing"

        # Handle both string and datetime objects
        if isinstance(date_value, datetime):
            return True, "Valid (datetime object)"

        try:
            # Try parsing common date formats
            datetime.strptime(str(date_value), '%Y-%m-%d')
            return True, "Valid (YYYY-MM-DD)"
        except ValueError:
            try:
                datetime.strptime(str(date_value), '%Y-%m-%dT%H:%M:%S')
                return True, "Valid (ISO 8601)"
            except ValueError:
                return False, f"Invalid format: {date_value}"

    def validate_image_path(self, image_path: str) -> Tuple[bool, str]:
        """Validate hero image path exists"""
        if not image_path:
            return False, "Missing"

        # Check if absolute path exists
        if os.path.isabs(image_path):
            if not os.path.exists(image_path):
                return False, f"Path not found: {image_path}"
        else:
            # Check relative to project root
            full_path = Path(self.posts_dir).parent.parent / image_path.lstrip('/')
            if not full_path.exists():
                return False, f"Path not found: {image_path}"

        return True, "Valid"

    def validate_tags(self, tags: List[str]) -> Tuple[bool, str]:
        """Validate tags presence and count"""
        if not tags:
            return False, "Missing"

        if not isinstance(tags, list):
            return False, "Not a list"

        tag_count = len(tags)
        if tag_count == 0:
            return False, "Empty list"
        elif tag_count < 3:
            return True, f"Sparse ({tag_count} tags, recommend 3-8)"
        elif tag_count > 10:
            return False, f"Too many ({tag_count} tags, recommend 3-8)"
        else:
            return True, f"Good ({tag_count} tags)"

    def validate_post(self, file_path: Path) -> Dict:
        """Validate all metadata for a single post"""
        post_result = {
            "file": file_path.name,
            "issues": [],
            "warnings": [],
            "valid": True
        }

        # Extract frontmatter
        frontmatter, error = self.extract_frontmatter(file_path)
        if error:
            post_result["issues"].append(f"Frontmatter error: {error}")
            post_result["valid"] = False
            return post_result

        # Validate title
        if not frontmatter.get('title'):
            post_result["issues"].append("Missing title")
            post_result["valid"] = False
            self.results["issues_summary"]["missing_title"] += 1

        # Validate description
        description_valid, description_msg = self.validate_description_length(
            frontmatter.get('description', '')
        )
        if not description_valid:
            if "Missing" in description_msg:
                post_result["issues"].append(f"Description: {description_msg}")
                self.results["issues_summary"]["missing_description"] += 1
            else:
                post_result["issues"].append(f"Description: {description_msg}")
                self.results["issues_summary"]["invalid_description_length"] += 1
            post_result["valid"] = False
        elif "Acceptable" in description_msg:
            post_result["warnings"].append(f"Description: {description_msg}")

        # Validate date
        date_valid, date_msg = self.validate_date_format(frontmatter.get('date'))
        if not date_valid:
            post_result["issues"].append(f"Date: {date_msg}")
            post_result["valid"] = False
            self.results["issues_summary"]["invalid_date_format"] += 1

        # Validate author
        if not frontmatter.get('author'):
            post_result["issues"].append("Missing author")
            post_result["valid"] = False
            self.results["issues_summary"]["missing_author"] += 1

        # Validate tags
        tags_valid, tags_msg = self.validate_tags(frontmatter.get('tags', []))
        if not tags_valid:
            post_result["issues"].append(f"Tags: {tags_msg}")
            post_result["valid"] = False
            self.results["issues_summary"]["missing_tags"] += 1
        elif "Sparse" in tags_msg:
            post_result["warnings"].append(f"Tags: {tags_msg}")

        # Validate hero image
        hero_image = frontmatter.get('hero_image') or frontmatter.get('heroImage')
        if hero_image:
            image_valid, image_msg = self.validate_image_path(hero_image)
            if not image_valid:
                post_result["issues"].append(f"Hero image: {image_msg}")
                post_result["valid"] = False
                self.results["issues_summary"]["broken_image_paths"] += 1
        else:
            post_result["warnings"].append("Hero image: Missing (not critical)")
            self.results["issues_summary"]["missing_hero_image"] += 1

        if not post_result["valid"] or post_result["warnings"]:
            self.results["posts_with_issues"].append(post_result)

        return post_result

    def validate_all_posts(self):
        """Validate all posts in the posts directory"""
        post_files = list(self.posts_dir.glob("*.md"))
        self.results["total_posts"] = len(post_files)

        print(f"{Colors.HEADER}{'=' * 80}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}METADATA VALIDATION REPORT{Colors.ENDC}")
        print(f"{Colors.HEADER}{'=' * 80}{Colors.ENDC}\n")

        print(f"Validating {len(post_files)} posts in {self.posts_dir}/...\n")

        valid_count = 0
        warning_count = 0

        for post_file in post_files:
            result = self.validate_post(post_file)
            if result["valid"] and not result["warnings"]:
                valid_count += 1
            elif result["warnings"] and not result["issues"]:
                warning_count += 1

        # Calculate coverage
        self.results["metadata_coverage"] = {
            "posts_valid": valid_count,
            "posts_with_warnings": warning_count,
            "posts_with_errors": len(self.results["posts_with_issues"]) - warning_count,
            "validation_rate": f"{(valid_count / self.results['total_posts'] * 100):.1f}%"
        }

    def print_text_report(self):
        """Print formatted text report"""
        # Summary statistics
        print(f"{Colors.OKBLUE}{Colors.BOLD}Summary Statistics:{Colors.ENDC}")
        print(f"  Total posts: {self.results['total_posts']}")
        print(f"  Posts valid: {Colors.OKGREEN}{self.results['metadata_coverage']['posts_valid']}{Colors.ENDC}")
        print(f"  Posts with warnings: {Colors.WARNING}{self.results['metadata_coverage']['posts_with_warnings']}{Colors.ENDC}")
        print(f"  Posts with errors: {Colors.FAIL}{self.results['metadata_coverage']['posts_with_errors']}{Colors.ENDC}")
        print(f"  Validation rate: {self.results['metadata_coverage']['validation_rate']}\n")

        # Issues breakdown
        print(f"{Colors.OKBLUE}{Colors.BOLD}Issues Breakdown:{Colors.ENDC}")
        issues = self.results["issues_summary"]
        for issue_type, count in issues.items():
            if count > 0:
                color = Colors.FAIL if count > 5 else Colors.WARNING
                print(f"  {color}{issue_type.replace('_', ' ').title()}: {count}{Colors.ENDC}")

        # Detailed issues
        if self.results["posts_with_issues"]:
            print(f"\n{Colors.OKBLUE}{Colors.BOLD}Detailed Issues:{Colors.ENDC}")
            for post in self.results["posts_with_issues"]:
                print(f"\n  {Colors.BOLD}{post['file']}{Colors.ENDC}")

                if post["issues"]:
                    print(f"    {Colors.FAIL}Errors:{Colors.ENDC}")
                    for issue in post["issues"]:
                        print(f"      - {issue}")

                if post["warnings"]:
                    print(f"    {Colors.WARNING}Warnings:{Colors.ENDC}")
                    for warning in post["warnings"]:
                        print(f"      - {warning}")

        print(f"\n{Colors.HEADER}{'=' * 80}{Colors.ENDC}")

        # Exit code
        if self.results['metadata_coverage']['posts_with_errors'] > 0:
            print(f"{Colors.FAIL}Validation FAILED - Fix errors before committing{Colors.ENDC}")
            return 1
        elif self.results['metadata_coverage']['posts_with_warnings'] > 0:
            print(f"{Colors.WARNING}Validation PASSED with warnings{Colors.ENDC}")
            return 0
        else:
            print(f"{Colors.OKGREEN}Validation PASSED - All metadata valid{Colors.ENDC}")
            return 0

    def print_json_report(self):
        """Print JSON report"""
        print(json.dumps(self.results, indent=2))
        return 0

def main():
    parser = argparse.ArgumentParser(description="Validate blog post metadata")
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                       help='Output format (default: text)')
    parser.add_argument('--posts-dir', default='src/posts',
                       help='Posts directory (default: src/posts)')
    args = parser.parse_args()

    validator = MetadataValidator(posts_dir=args.posts_dir)
    validator.validate_all_posts()

    if args.format == 'json':
        return validator.print_json_report()
    else:
        return validator.print_text_report()

if __name__ == "__main__":
    sys.exit(main())
