#!/usr/bin/env python3
"""
SCRIPT: generate_llm_onboarding.py
PURPOSE: Generate comprehensive LLM onboarding documentation
CATEGORY: documentation
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T19:10:00-04:00

DESCRIPTION:
    Generates LLM_ONBOARDING.md guide for new AI agents working with
    the repository. Provides quick start, common tasks, best practices,
    and essential information for effective operation.

LLM_USAGE:
    python scripts/generate_llm_onboarding.py [options]

ARGUMENTS:
    --output (str): Output file path (default: docs/GUIDES/LLM_ONBOARDING.md)
    --verbose (bool): Show detailed generation progress

EXAMPLES:
    # Generate LLM onboarding guide
    python scripts/generate_llm_onboarding.py

    # Generate with custom output
    python scripts/generate_llm_onboarding.py --output custom_guide.md

OUTPUT:
    - Comprehensive onboarding guide for LLMs
    - Quick reference commands
    - Common task workflows
    - Troubleshooting guidance

DEPENDENCIES:
    - Python 3.8+
    - scripts/lib/common.py for shared utilities

MANIFEST_REGISTRY: scripts/generate_llm_onboarding.py
"""

import json
import sys
from pathlib import Path
import argparse

# Add parent directory for imports
sys.path.append(str(Path(__file__).parent))
from lib.common import ManifestManager, TimeManager, Logger

class LLMOnboardingGenerator:
    """Generate comprehensive LLM onboarding documentation"""

    def __init__(self):
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.manifest_mgr = ManifestManager()
        self.time_mgr = TimeManager()

    def generate_llm_onboarding(self, output_path: str = None) -> str:
        """Generate LLM_ONBOARDING.md guide"""

        if not output_path:
            output_path = "docs/GUIDES/LLM_ONBOARDING.md"

        manifest = self.manifest_mgr.manifest
        timestamp = self.time_mgr.get_current_timestamp()

        # Count scripts by category
        python_scripts = [f for f in manifest.get('inventory', {}).get('files', {}).get('file_registry', {}).keys()
                         if f.endswith('.py') and 'scripts/' in f]

        blog_scripts = [s for s in python_scripts if 'blog' in s.lower()]
        validation_scripts = [s for s in python_scripts if 'validate' in s.lower() or 'check' in s.lower()]
        image_scripts = [s for s in python_scripts if 'image' in s.lower()]

        doc_content = f"""# 🤖 LLM Agent Onboarding Guide

**Version:** 1.0.0
**Generated:** {timestamp}
**Required Reading Time:** 5 minutes
**Compliance Level:** MANDATORY

## 🎯 Welcome, LLM Agent!

This guide provides everything you need to work effectively with the williamzujkowski.github.io repository.

## ⚡ Quick Start Checklist

**Before doing ANYTHING, complete these steps:**

1. ✅ Read [ENFORCEMENT.md](../ENFORCEMENT.md) - **MANDATORY** enforcement rules
2. ✅ Check `MANIFEST.json` - Current repository inventory
3. ✅ Review `.claude-rules.json` - Active enforcement rules
4. ✅ Scan `CLAUDE.md` - Primary LLM interface
5. ✅ Verify time source - Use time.gov or UTC only

**⚠️ SKIP THESE AT YOUR OWN PERIL - OPERATIONS WILL FAIL**

## 🗺️ Repository Navigation

### 🔴 Critical Files (DO NOT MODIFY)
```
CLAUDE.md          # Your primary interface and instructions
MANIFEST.json      # Single source of truth for inventory
.claude-rules.json # Enforcement rules - violations = blocks
scripts/lib/common.py # Shared utilities - import only
```

### 📁 Directory Structure
```
src/              # Website source (Eleventy + Tailwind)
├── posts/        # Blog posts in Markdown
├── pages/        # Static pages
├── assets/       # CSS, JS, images
└── _includes/    # Templates and partials

scripts/          # Automation ({len(python_scripts)} Python scripts)
├── lib/         # Shared modules (DRY implementation)
└── *.py         # Individual automation scripts

docs/            # Documentation (you are here)
├── STANDARDS/   # Standards documentation
├── GUIDES/      # User guides and tutorials
└── AUTOMATION/  # Automation documentation

_site/           # Built website (git-ignored)
reports/         # Generated reports
```

## 📚 Script Categories & Usage

### Blog Management Scripts ({len(blog_scripts)} total)
**Purpose:** Enhance, analyze, and manage blog content
**⚠️ Note:** High duplication (70-89% similarity) - choose carefully

```python
# Primary blog analysis
python scripts/analyze-blog-content.py

# Update blog images
python scripts/update-blog-images.py

# Generate hero images
python scripts/generate-blog-hero-images.py

# Optimize content
python scripts/optimize-blog-content.py
```

### Validation Scripts ({len(validation_scripts)} total)
**Purpose:** Ensure standards compliance
**Priority:** Run BEFORE and AFTER operations

```python
# Validate manifest (CRITICAL)
python scripts/validate_manifest.py

# Check standards compliance
python scripts/validate_standards.py

# Check for duplicate files
python scripts/check_duplicates.py

# Generate compliance report
python scripts/generate_compliance_report.py
```

### Image Management Scripts ({len(image_scripts)} total)
**Purpose:** Generate and optimize images

```python
# Generate hero images for all posts
python scripts/generate-blog-hero-images.py

# Search for stock images
python scripts/enhanced-blog-image-search.py

# Optimize images
bash scripts/optimize-blog-images.sh
```

## 🔄 Standard Workflows

### Workflow 1: Adding a Blog Post
```mermaid
graph LR
    A[Create .md file] --> B[Add frontmatter]
    B --> C[Update images]
    C --> D[Generate hero]
    D --> E[Validate manifest]
    E --> F[Commit]
```

Commands:
```bash
# 1. Create post in src/posts/
# 2. Add required frontmatter
# 3. Update images
python scripts/update-blog-images.py

# 4. Generate hero image
python scripts/generate-blog-hero-images.py

# 5. Validate
python scripts/validate_manifest.py

# 6. Build and test
npm run build
```

### Workflow 2: Running Validations
```bash
# Always run in this order:
python scripts/validate_manifest.py      # Check manifest
python scripts/check_duplicates.py       # No duplicates
python scripts/validate_standards.py     # Standards OK
python scripts/generate_compliance_report.py # Full report
```

### Workflow 3: Cleaning Repository
```bash
# Audit for vestigial content
python scripts/vestigial_audit.py --full --report

# Review report
cat reports/vestigial_audit_report.md

# Remove safe items
python scripts/remove_vestigial.py --safe
```

## 🚨 Common Pitfalls & Solutions

### Pitfall 1: Creating Duplicate Files
**Problem:** Creating `test.py` when `test_script.py` exists
**Solution:** ALWAYS check file_registry in MANIFEST.json first
```python
# Check for similar files
import json
with open('MANIFEST.json') as f:
    manifest = json.load(f)
files = manifest['inventory']['files']['file_registry'].keys()
similar = [f for f in files if 'test' in f]
```

### Pitfall 2: Not Updating Manifest
**Problem:** File operations without manifest update
**Solution:** ALWAYS update after changes
```python
# After any file operation
python scripts/update_manifest.py
```

### Pitfall 3: Wrong Timestamp
**Problem:** Using datetime.now() without timezone
**Solution:** Use proper time sources
```python
# Correct approaches:
from lib.common import TimeManager
time_mgr = TimeManager()
timestamp = time_mgr.get_current_timestamp()
```

## 📊 Using MANIFEST.json Effectively

The manifest is your map to the repository:

```python
import json

# Load manifest
with open('MANIFEST.json', 'r') as f:
    manifest = json.load(f)

# Find scripts by category
scripts = manifest['inventory']['files']['file_registry']
python_scripts = {{k: v for k, v in scripts.items() if k.endswith('.py')}}

# Check file existence
file_path = "scripts/example.py"
exists = file_path in scripts

# Get file metadata
if exists:
    metadata = scripts[file_path]
    print(f"Category: {{{{metadata.get('category')}}}}")
    print(f"Modified: {{{{metadata.get('modified')}}}}")
```

## ⚡ Quick Reference Commands

### Build & Development
```bash
# Build the site
npm run build

# Start dev server (hot reload)
npm run serve

# Build CSS only
npm run build:css

# Clean build
rm -rf _site && npm run build
```

### Git Operations
```bash
# Check status
git status

# Stage changes
git add -A

# Commit with standards validation
git commit -m "type(scope): description"

# Push (after validation)
git push origin main
```

### Python Script Patterns
```python
# Standard script header (MANDATORY)
#!/usr/bin/env python3
\"\"\"
SCRIPT: name.py
PURPOSE: One-line description
CATEGORY: category
LLM_READY: True
[...]
\"\"\"

# Standard imports (MANDATORY)
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from lib.common import ManifestManager, TimeManager, Logger

# Initialize managers
manifest_mgr = ManifestManager()
time_mgr = TimeManager()
logger = Logger.get_logger(__name__)
```

## 🔍 Finding Information

| Need | Location |
|------|----------|
| System architecture | `docs/ARCHITECTURE.md` |
| Enforcement rules | `docs/ENFORCEMENT.md` |
| Script documentation | Script headers (LLM_READY) |
| Current inventory | `MANIFEST.json` |
| Standards | `.standards/` submodule |
| Blog posts | `src/posts/` |
| Configuration | `package.json`, `.eleventy.js` |

## 💡 Best Practices

### DO:
- ✅ Always validate before and after operations
- ✅ Use existing scripts instead of creating new ones
- ✅ Import from `scripts/lib/common.py`
- ✅ Check file_registry before creating files
- ✅ Update MANIFEST.json immediately
- ✅ Use proper time sources
- ✅ Follow LLM documentation standards
- ✅ Run pre-commit validation

### DON'T:
- ❌ Create duplicate files
- ❌ Modify protected files
- ❌ Skip manifest updates
- ❌ Use system time without timezone
- ❌ Ignore validation failures
- ❌ Create scripts without documentation
- ❌ Save files to root directory
- ❌ Bypass enforcement rules

## 🎓 Advanced Topics

### Understanding Enforcement
The enforcement system has three layers:
1. **Development**: LLM documentation, imports
2. **Pre-commit**: Hooks validate everything
3. **CI/CD**: GitHub Actions enforce standards

### Working with Standards
```bash
# Update standards submodule
cd .standards
git fetch origin
git pull origin main
cd ..
git add .standards
git commit -m "chore: Update standards submodule"
```

### Debugging Validation Failures
1. Read error message completely
2. Check relevant enforcement rule
3. Review ENFORCEMENT.md
4. Fix the specific issue
5. Re-run validation
6. Only proceed when passing

## 📚 Required Reading Order

1. **[ENFORCEMENT.md](../ENFORCEMENT.md)** - Rules (5 min)
2. **[ARCHITECTURE.md](../ARCHITECTURE.md)** - System (10 min)
3. **[SCRIPT_CATALOG.md](SCRIPT_CATALOG.md)** - Scripts (15 min)
4. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Issues (as needed)

## 🆘 Getting Help

### When Stuck:
1. Check error messages carefully
2. Review validation reports in `reports/`
3. Ensure MANIFEST.json is current
4. Verify `.claude-rules.json` compliance
5. Check pre-commit hook output
6. Review CI/CD logs

### Common Solutions:
- **"File not found"** → Check MANIFEST.json file_registry
- **"Validation failed"** → Run compliance report
- **"Duplicate detected"** → Check existing files first
- **"Manifest outdated"** → Run update_manifest.py
- **"Standards violation"** → Review .claude-rules.json

## ✅ Onboarding Complete!

You are now equipped to work with this repository effectively.

### Remember the Golden Rules:
1. **MANIFEST.json** is the single source of truth
2. **Enforcement rules** are mandatory, not optional
3. **Validation** must pass before commits
4. **Time.gov** or UTC for timestamps only
5. **Check before create** - no duplicates

### Your Success Metrics:
- ✅ All validations pass
- ✅ No duplicate files created
- ✅ Manifest always current
- ✅ Standards compliance 100%
- ✅ Pre-commit hooks pass

**Good luck, and remember: compliance is not optional!** 🚀

---

*This guide is auto-generated. Regenerate with `python scripts/generate_llm_onboarding.py`*
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
        description="Generate comprehensive LLM onboarding documentation"
    )

    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--verbose', action='store_true',
                       help='Show detailed generation progress')

    args = parser.parse_args()

    generator = LLMOnboardingGenerator()

    if args.verbose:
        print("📚 Generating LLM Onboarding Guide...")

    doc = generator.generate_llm_onboarding(args.output)

    print(f"✅ Generated LLM_ONBOARDING.md")
    if args.verbose:
        print(f"   Sections: {doc.count('##')}")
        print(f"   Commands: {doc.count('```')}")

    return 0

if __name__ == "__main__":
    sys.exit(main())