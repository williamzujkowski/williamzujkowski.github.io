#!/usr/bin/env python3
"""
SCRIPT: generate_compliance_report.py
PURPOSE: Generate comprehensive compliance report for standards enforcement
CATEGORY: validation
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T18:24:00-04:00

DESCRIPTION:
    Generates detailed compliance reports showing the current state
    of standards adherence across the repository. Checks manifest,
    enforcement rules, pre-commit hooks, GitHub Actions, and script
    documentation compliance.

LLM_USAGE:
    python scripts/generate_compliance_report.py [options]

ARGUMENTS:
    --format (str): Output format [markdown|json|html] (default: markdown)
    --output (str): Output file path (default: reports/compliance_report.md)
    --verbose (bool): Show detailed information

EXAMPLES:
    # Generate markdown report
    python scripts/generate_compliance_report.py

    # Generate JSON report
    python scripts/generate_compliance_report.py --format json --output report.json

OUTPUT:
    - Compliance report in specified format
    - Summary of passes and violations
    - Recommendations for improvements

DEPENDENCIES:
    - Python 3.8+
    - scripts/lib/common.py for shared utilities

MANIFEST_REGISTRY: scripts/generate_compliance_report.py
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple
import argparse

# Add parent directory for imports
sys.path.append(str(Path(__file__).parent))
from lib.common import TimeManager, ManifestManager, Logger

class ComplianceReportGenerator:
    """Generate comprehensive compliance reports"""

    def __init__(self):
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.time_mgr = TimeManager()
        self.manifest_mgr = ManifestManager()
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)

    def check_manifest_compliance(self) -> Tuple[str, List[str], List[str]]:
        """Check MANIFEST.json compliance"""
        passes = []
        violations = []

        try:
            manifest = self.manifest_mgr.manifest

            # Check required fields
            required = ['version', 'inventory', 'standards_compliance']
            for field in required:
                if field in manifest:
                    passes.append(f"✅ MANIFEST.json has required field: {field}")
                else:
                    violations.append(f"❌ MANIFEST.json missing required field: {field}")

            # Check last validated timestamp
            if 'last_validated' in manifest:
                from datetime import timezone
                last_validated = datetime.fromisoformat(manifest['last_validated'].replace('Z', '+00:00').replace('-04:00', '+00:00').replace('-05:00', '+00:00'))
                age_hours = (datetime.now(timezone.utc) - last_validated).total_seconds() / 3600
                if age_hours < 24:
                    passes.append(f"✅ MANIFEST.json validated {age_hours:.1f} hours ago")
                else:
                    violations.append(f"⚠️  MANIFEST.json last validated {age_hours:.1f} hours ago (>24h)")
            else:
                violations.append("❌ MANIFEST.json missing last_validated timestamp")

            status = "PASS" if len(violations) == 0 else "FAIL"
            return status, passes, violations

        except Exception as e:
            self.logger.error(f"Error checking MANIFEST.json: {e}")
            return "ERROR", [], [f"❌ Error checking MANIFEST.json: {e}"]

    def check_enforcement_rules(self) -> Tuple[str, List[str], List[str]]:
        """Check enforcement rules compliance"""
        passes = []
        violations = []

        rules_path = Path(".claude-rules.json")
        if rules_path.exists():
            passes.append("✅ .claude-rules.json exists")

            try:
                with open(rules_path, 'r') as f:
                    rules = json.load(f)

                # Check version
                if 'version' in rules:
                    passes.append(f"✅ Rules version: {rules['version']}")

                # Check standards count
                standards = rules.get('MANDATORY_STANDARDS', {})
                passes.append(f"✅ {len(standards)} standards loaded")

                # Check critical rules
                critical_rules = rules.get('LLM_ENFORCEMENT', {}).get('CRITICAL_RULES', [])
                passes.append(f"✅ {len(critical_rules)} critical rules defined")

            except Exception as e:
                violations.append(f"❌ Error reading .claude-rules.json: {e}")
        else:
            violations.append("❌ .claude-rules.json not found")

        status = "PASS" if len(violations) == 0 else "FAIL"
        return status, passes, violations

    def check_pre_commit_hooks(self) -> Tuple[str, List[str], List[str]]:
        """Check pre-commit hooks status"""
        passes = []
        violations = []

        hook_path = Path(".git/hooks/pre-commit")
        if hook_path.exists():
            passes.append("✅ Pre-commit hook installed")

            # Check if executable
            if hook_path.stat().st_mode & 0o111:
                passes.append("✅ Pre-commit hook is executable")
            else:
                violations.append("⚠️  Pre-commit hook not executable")

            # Check content
            content = hook_path.read_text()
            required_scripts = [
                "validate_manifest.py",
                "check_duplicates.py",
                "check_standards.py"
            ]

            for script in required_scripts:
                if script in content:
                    passes.append(f"✅ Pre-commit runs {script}")
                else:
                    violations.append(f"⚠️  Pre-commit missing {script}")
        else:
            violations.append("❌ Pre-commit hook not installed")

        status = "PASS" if len(violations) == 0 else "FAIL"
        return status, passes, violations

    def check_github_actions(self) -> Tuple[str, List[str], List[str]]:
        """Check GitHub Actions workflows"""
        passes = []
        violations = []

        workflows_dir = Path(".github/workflows")
        if workflows_dir.exists():
            passes.append("✅ .github/workflows directory exists")

            # Check for enforcement workflow
            enforcement_workflow = workflows_dir / "standards_enforcement.yml"
            if enforcement_workflow.exists():
                passes.append("✅ standards_enforcement.yml exists")
            else:
                violations.append("❌ standards_enforcement.yml not found")

            # Check for other workflows
            workflow_count = len(list(workflows_dir.glob("*.yml")))
            passes.append(f"✅ {workflow_count} GitHub Actions workflows found")
        else:
            violations.append("❌ .github/workflows directory not found")

        status = "PASS" if len(violations) == 0 else "FAIL"
        return status, passes, violations

    def check_script_documentation(self) -> Tuple[str, List[str], List[str]]:
        """Check script documentation compliance"""
        passes = []
        violations = []

        scripts_dir = Path("scripts")
        if scripts_dir.exists():
            python_scripts = list(scripts_dir.glob("*.py"))
            documented_count = 0
            undocumented = []

            for script in python_scripts:
                with open(script, 'r') as f:
                    content = f.read(1000)  # Read first 1000 chars

                if "LLM_READY: True" in content or "LLM_USAGE:" in content:
                    documented_count += 1
                else:
                    undocumented.append(script.name)

            passes.append(f"✅ {documented_count}/{len(python_scripts)} scripts documented")

            if undocumented:
                for script in undocumented[:5]:  # Show first 5
                    violations.append(f"⚠️  {script} missing LLM documentation")
                if len(undocumented) > 5:
                    violations.append(f"⚠️  ...and {len(undocumented)-5} more")
        else:
            violations.append("❌ scripts directory not found")

        status = "PASS" if len(violations) == 0 else "WARN" if any("⚠️" in v for v in violations) else "FAIL"
        return status, passes, violations

    def generate_markdown_report(self, results: Dict[str, Any]) -> str:
        """Generate markdown format report"""
        timestamp = self.time_mgr.get_current_timestamp()

        report = f"""# 📋 Standards Compliance Report

**Generated:** {timestamp}
**Overall Status:** {results['overall_status']}

## 📊 Summary

| Component | Status | Passes | Violations |
|-----------|--------|--------|------------|
"""

        for component, data in results['components'].items():
            status_icon = "✅" if data['status'] == "PASS" else "⚠️" if data['status'] == "WARN" else "❌"
            report += f"| {component} | {status_icon} {data['status']} | {len(data['passes'])} | {len(data['violations'])} |\n"

        report += "\n## 📝 Detailed Results\n\n"

        for component, data in results['components'].items():
            report += f"### {component}\n\n"

            if data['passes']:
                report += "**Passes:**\n"
                for pass_item in data['passes']:
                    report += f"- {pass_item}\n"
                report += "\n"

            if data['violations']:
                report += "**Violations:**\n"
                for violation in data['violations']:
                    report += f"- {violation}\n"
                report += "\n"

        report += """## 🎯 Recommendations

1. **Fix Critical Issues:** Address any ❌ violations immediately
2. **Review Warnings:** Investigate ⚠️ warnings and plan fixes
3. **Maintain Compliance:** Run validation regularly
4. **Update Documentation:** Keep all documentation current

## 🔗 Resources

- [Standards Repository](https://github.com/williamzujkowski/standards)
- [Enforcement Rules](.claude-rules.json)
- [CLAUDE.md](CLAUDE.md) - Project configuration

---

*This report was generated by `scripts/generate_compliance_report.py`*
"""
        return report

    def generate_json_report(self, results: Dict[str, Any]) -> str:
        """Generate JSON format report"""
        return json.dumps(results, indent=2)

    def generate_report(self, format: str = "markdown", output_path: str = None) -> bool:
        """Generate comprehensive compliance report"""

        self.logger.info("Generating compliance report...")

        # Run all compliance checks
        results = {
            "timestamp": self.time_mgr.get_current_timestamp(),
            "overall_status": "PASS",
            "components": {}
        }

        # Check each component
        checks = [
            ("MANIFEST.json", self.check_manifest_compliance),
            ("Enforcement Rules", self.check_enforcement_rules),
            ("Pre-commit Hooks", self.check_pre_commit_hooks),
            ("GitHub Actions", self.check_github_actions),
            ("Script Documentation", self.check_script_documentation)
        ]

        for component_name, check_func in checks:
            status, passes, violations = check_func()
            results['components'][component_name] = {
                "status": status,
                "passes": passes,
                "violations": violations
            }

            # Update overall status
            if status == "FAIL":
                results['overall_status'] = "FAIL"
            elif status == "WARN" and results['overall_status'] != "FAIL":
                results['overall_status'] = "WARN"

        # Generate report in requested format
        if format == "json":
            report_content = self.generate_json_report(results)
            default_output = "reports/compliance_report.json"
        else:  # Default to markdown
            report_content = self.generate_markdown_report(results)
            default_output = "reports/compliance_report.md"

        # Determine output path
        if not output_path:
            output_path = default_output

        output_file = Path(output_path)
        output_file.parent.mkdir(exist_ok=True)

        # Write report
        output_file.write_text(report_content)
        self.logger.info(f"Report saved to {output_file}")

        # Update manifest entry
        # Note: ManifestManager update methods vary by implementation
        # This is a safe operation that can fail silently
        try:
            if hasattr(self.manifest_mgr, 'update_file'):
                self.manifest_mgr.update_file(
                    str(output_file),
                    category="reports",
                    description="Standards compliance report"
                )
            elif hasattr(self.manifest_mgr, 'save_manifest'):
                # Just save the current manifest
                self.manifest_mgr.save_manifest()
        except Exception as e:
            self.logger.debug(f"Could not update manifest: {e}")

        # Print summary
        print(f"\n📋 Compliance Report Generated")
        print(f"   Status: {results['overall_status']}")
        print(f"   Location: {output_file}")

        return results['overall_status'] != "FAIL"

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive compliance report"
    )

    parser.add_argument('--format', choices=['markdown', 'json', 'html'],
                       default='markdown', help='Output format')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--verbose', action='store_true',
                       help='Show detailed information')

    args = parser.parse_args()

    generator = ComplianceReportGenerator()

    try:
        if generator.generate_report(format=args.format, output_path=args.output):
            return 0
        else:
            print("\n⚠️  Some compliance checks failed - see report for details")
            return 1
    except Exception as e:
        print(f"\n❌ Error generating report: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())