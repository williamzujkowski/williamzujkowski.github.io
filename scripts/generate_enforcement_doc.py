#!/usr/bin/env python3
"""
SCRIPT: generate_enforcement_doc.py
PURPOSE: Generate enforcement documentation for all LLMs
CATEGORY: documentation
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T19:05:00-04:00

DESCRIPTION:
    Generates ENFORCEMENT.md with mandatory rules that all LLMs must follow.
    Extracts rules from .claude-rules.json and presents them in a clear,
    unambiguous format that leaves no room for interpretation.

LLM_USAGE:
    python scripts/generate_enforcement_doc.py [options]

ARGUMENTS:
    --output (str): Output file path (default: docs/ENFORCEMENT.md)
    --strict (bool): Use even stricter language

EXAMPLES:
    # Generate enforcement documentation
    python scripts/generate_enforcement_doc.py

    # Generate with stricter language
    python scripts/generate_enforcement_doc.py --strict

OUTPUT:
    - Mandatory enforcement rules documentation
    - Clear penalties for violations
    - Required workflows and checks

DEPENDENCIES:
    - Python 3.8+
    - scripts/lib/common.py for shared utilities
    - .claude-rules.json for rule definitions

MANIFEST_REGISTRY: scripts/generate_enforcement_doc.py
"""

import json
import sys
from pathlib import Path
import argparse

# Add parent directory for imports
sys.path.append(str(Path(__file__).parent))
from lib.common import TimeManager, Logger

class EnforcementDocGenerator:
    """Generate enforcement documentation for all LLMs"""

    def __init__(self):
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.time_mgr = TimeManager()

    def generate_enforcement_doc(self, output_path: str = None, strict: bool = False) -> str:
        """Generate ENFORCEMENT.md with mandatory rules"""

        if not output_path:
            output_path = "docs/ENFORCEMENT.md"

        timestamp = self.time_mgr.get_current_timestamp()

        # Load current enforcement rules
        rules_path = Path(".claude-rules.json")
        if rules_path.exists():
            with open(rules_path, 'r') as f:
                rules = json.load(f)
        else:
            rules = {}
            self.logger.warning(".claude-rules.json not found")

        # Extract key rules
        critical_rules = rules.get('LLM_ENFORCEMENT', {}).get('CRITICAL_RULES', [])
        file_ops = rules.get('LLM_ENFORCEMENT', {}).get('FILE_OPERATIONS', {})
        protected_files = rules.get('PROTECTED_FILES', [])
        penalties = rules.get('PENALTIES', {})

        doc_content = f"""# 🚨 MANDATORY ENFORCEMENT RULES FOR ALL LLMS 🚨

**Generated:** {timestamp}
**Version:** 1.0.0
**Status:** ENFORCED
**Severity:** CRITICAL

## ⛔ CRITICAL: READ THIS FIRST

{'**THESE RULES ARE ABSOLUTE. NO EXCEPTIONS. NO INTERPRETATIONS. NO WORKAROUNDS.**' if strict else '**THESE RULES ARE NOT OPTIONAL. VIOLATIONS WILL BE AUTOMATICALLY BLOCKED.**'}

**YOUR OPERATIONS WILL FAIL IF YOU VIOLATE ANY RULE.**

## 🔴 ABSOLUTE REQUIREMENTS

### Before ANY Operation - NO EXCEPTIONS

1. **CHECK** `MANIFEST.json` exists and is valid JSON
2. **VERIFY** `.claude-rules.json` contains current enforcement rules
3. **CONFIRM** no duplicate files will be created (check file_registry)
4. **OBTAIN** timestamp from time.gov (Washington DC timezone)
5. **VALIDATE** operation follows standards from https://github.com/williamzujkowski/standards

**If ANY check fails → STOP IMMEDIATELY**

## 📋 Critical Enforcement Rules

### The Following Rules Are MANDATORY:

"""

        # Add critical rules
        for i, rule in enumerate(critical_rules, 1):
            doc_content += f"{i}. **{rule}**\n"

        doc_content += """

## 🚫 File Operation Rules

### CREATE Operations - MANDATORY CHECKS:
"""

        for rule in file_ops.get('CREATE', []):
            doc_content += f"- ✓ {rule}\n"

        doc_content += """

### UPDATE Operations - MANDATORY CHECKS:
"""

        for rule in file_ops.get('UPDATE', []):
            doc_content += f"- ✓ {rule}\n"

        doc_content += """

### DELETE Operations - MANDATORY CHECKS:
"""

        for rule in file_ops.get('DELETE', []):
            doc_content += f"- ✓ {rule}\n"

        doc_content += """

## 🛡️ Protected Resources

**THESE FILES MUST NEVER BE DELETED, RENAMED, OR MOVED:**

```
"""

        for file in protected_files:
            doc_content += f"{file}\n"

        doc_content += """```

**Attempting to modify protected files = IMMEDIATE BLOCK**

## ⚖️ Penalties for Violations

| Violation | Severity | Consequence |
|-----------|----------|-------------|
"""

        if penalties:
            for violation, details in penalties.items():
                if isinstance(details, dict):
                    severity = details.get('severity', 'UNKNOWN')
                    action = details.get('action', 'Undefined')
                else:
                    severity = 'HIGH'
                    action = str(details)
                doc_content += f"| {violation.replace('_', ' ').title()} | **{severity}** | {action} |\n"
        else:
            # Add default penalties if none specified
            doc_content += """| Duplicate File Creation | **CRITICAL** | Operation blocked, warning issued |
| Manifest Not Updated | **HIGH** | Pre-commit hook fails |
| Missing Documentation | **MEDIUM** | CI/CD warning |
| Wrong Directory | **HIGH** | Operation blocked |
| Protected File Modified | **CRITICAL** | Immediate block, rollback |
"""

        doc_content += """

## 📝 Required Script Header

**EVERY Python script MUST have this EXACT header:**

```python
#!/usr/bin/env python3
\"\"\"
SCRIPT: script_name.py
PURPOSE: Clear one-line description
CATEGORY: [utility|validation|documentation|enhancement]
LLM_READY: True
VERSION: x.x.x
UPDATED: YYYY-MM-DDTHH:MM:SS-TZ:TZ

DESCRIPTION:
    Detailed description for LLMs

LLM_USAGE:
    python scripts/script_name.py [options]

ARGUMENTS:
    --arg (type): Description

EXAMPLES:
    python scripts/script_name.py --example

OUTPUT:
    What the script produces

DEPENDENCIES:
    - Python 3.8+
    - scripts/lib/common.py

MANIFEST_REGISTRY: scripts/script_name.py
\"\"\"

# MANDATORY imports
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from lib.common import ManifestManager, TimeManager, Logger
```

## ⏱️ Time Management Rules

### ONLY Acceptable Time Sources:

1. **PRIMARY**: time.gov API
```python
import requests
response = requests.get("https://www.time.gov/actualtime.cgi?lzbc=siqm9b")
# Parse Washington DC time
```

2. **FALLBACK**: System time with UTC
```python
from datetime import datetime, timezone
timestamp = datetime.now(timezone.utc).isoformat()
```

**NEVER use datetime.now() without timezone**

## 🔄 Mandatory Workflow

### For EVERY Operation:

```mermaid
graph TD
    A[Start] --> B{MANIFEST.json valid?}
    B -->|No| STOP[BLOCK OPERATION]
    B -->|Yes| C{Check duplicates}
    C -->|Found| STOP
    C -->|None| D{Standards OK?}
    D -->|No| STOP
    D -->|Yes| E[Perform Operation]
    E --> F[Update MANIFEST.json]
    F --> G{Validate}
    G -->|Fail| H[Rollback]
    G -->|Pass| I[Complete]
```

## ✅ Pre-Operation Checklist

**YOU MUST CHECK ALL ITEMS:**

- [ ] MANIFEST.json exists and is valid JSON
- [ ] MANIFEST.json last_validated is within 24 hours
- [ ] .claude-rules.json has been read
- [ ] Target file is not in protected list
- [ ] No duplicate file will be created
- [ ] Directory structure is appropriate
- [ ] Standards compliance verified
- [ ] Time source identified (time.gov preferred)

## ❌ Common Violations That WILL Be Blocked

1. **Creating duplicate files**
   - Example: Creating `analyze_blog.py` when `analyze-blog-content.py` exists
   - **ALWAYS** check file_registry first

2. **Not updating MANIFEST.json**
   - Every file operation MUST update manifest
   - No exceptions

3. **Using wrong time source**
   - datetime.now() without timezone = BLOCK
   - Always use time.gov or UTC

4. **Modifying protected files**
   - Never edit CLAUDE.md, MANIFEST.json directly
   - Use appropriate scripts

5. **Missing LLM documentation**
   - All scripts MUST have complete header
   - No "TODO" placeholders

6. **Saving to root directory**
   - Working files go in appropriate subdirectories
   - Never save to repository root

## 🚨 Enforcement Mechanisms

### 1. Pre-commit Hooks
- Location: `.git/hooks/pre-commit`
- Validates EVERYTHING before commit
- Cannot be bypassed

### 2. CI/CD Pipeline
- Workflow: `.github/workflows/standards_enforcement.yml`
- Runs on ALL pushes and PRs
- Blocks merge on ANY failure

### 3. Runtime Validation
- Every script self-validates
- Checks manifest before operations
- Updates manifest after changes

## 📊 Validation Commands

### Run These Before ANY Commit:

```bash
# Check manifest validity
python scripts/validate_manifest.py

# Check for duplicates
python scripts/check_duplicates.py

# Validate standards
python scripts/validate_standards.py

# Generate compliance report
python scripts/generate_compliance_report.py
```

## 🔗 Required Reading

**YOU MUST READ THESE DOCUMENTS:**

1. [.claude-rules.json](../.claude-rules.json) - Current enforcement rules
2. [MANIFEST.json](../MANIFEST.json) - Repository inventory
3. [CLAUDE.md](../CLAUDE.md) - Primary interface
4. [Standards Repository](https://github.com/williamzujkowski/standards)

## ⚠️ Final Warning

**ENFORCEMENT IS AUTOMATIC AND UNFORGIVING**

- Rules are checked by machines, not humans
- There is no appeals process
- Violations block operations immediately
- Compliance is mandatory, not optional

**YOUR SUCCESS DEPENDS ON FOLLOWING THESE RULES**

---

*Generated by `scripts/generate_enforcement_doc.py` - DO NOT EDIT MANUALLY*
"""

        # Write the document
        doc_path = Path(output_path)
        doc_path.parent.mkdir(parents=True, exist_ok=True)
        doc_path.write_text(doc_content)

        self.logger.info(f"Generated {output_path}")
        return doc_content

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Generate enforcement documentation for all LLMs"
    )

    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--strict', action='store_true',
                       help='Use even stricter language')

    args = parser.parse_args()

    generator = EnforcementDocGenerator()
    doc = generator.generate_enforcement_doc(args.output, args.strict)

    print(f"✅ Generated ENFORCEMENT.md")
    print(f"   Rules documented: {doc.count('✓')}")
    print(f"   Warnings issued: {doc.count('⚠️')}")

    return 0

if __name__ == "__main__":
    sys.exit(main())