---
STATUS: AUTHORITATIVE
VERSION: 4.0.0
LAST_AUDIT: 2025-11-01
COMPLIANCE: 100%
ARCHITECTURE: MODULAR
TOKEN_EFFICIENCY: 97.5%
---

# Claude Code Configuration - SPARC Development Environment

# 🏛️ AUTHORITATIVE DOCUMENTATION NOTICE

This file (CLAUDE.md) serves as the **root anchor** for a modular documentation architecture:
- Progressive context loading based on task requirements
- 10 specialized modules organized by priority (core, workflows, standards, technical, reference, templates)
- Token-efficient: Load only what you need for the current task
- Complete index: `docs/context/INDEX.yaml`

**Previous architecture:** 12,900-word monolith (80,000+ tokens) loaded for every task
**New architecture:** ~2,000-word anchor (8,000 tokens) + selective module loading (2,000-15,000 tokens)
**Efficiency gain:** 97.5% reduction in unnecessary context (8K vs 80K tokens for simple tasks)

All development, content creation, and maintenance MUST reference this document and load task-appropriate modules.

**Last comprehensive audit:** 2025-11-01
**Next scheduled review:** 2025-12-01

## 📊 Current Compliance Status

### Content Compliance ✅
- **NDA Compliance**: 100% - Zero work references
- **Political Neutrality**: 100% - Technical focus maintained
- **Personal Focus**: 100% - Homelab and personal projects only
- **Last Audit**: 2025-10-28
- **Posts Reviewed**: 56/56

### Research & Citations ✅
- **Citation Coverage**: 90%+ (increased from 45%)
- **Academic Sources**: 50%+ with DOI/arXiv links
- **Broken Links**: 0 (fixed 49 issues)
- **Statistics Sourced**: 100%
- **Batch 2 Average**: 11.3 citations per post (+440% from 2.1 baseline)

### UI/UX & Accessibility ✅
- **Mobile Responsive**: Tested 375px-2560px
- **Touch Targets**: All ≥44px
- **WCAG Compliance**: AA achieved
- **Dark Mode**: Fully functional
- **Core Web Vitals**: All green (LCP <2.5s, FID <100ms, CLS <0.1)

### Technical Quality ✅
- **Build Status**: PASSING
- **Load Time**: <3s on 3G
- **Lighthouse Mobile**: 95+
- **Browser Support**: Modern browsers + graceful degradation

---

## 🚨 MANDATORY ENFORCEMENT NOTICE 🚨

**CRITICAL**: Before ANY operation, you MUST:

1. **CHECK** `.claude-rules.json` for current enforcement rules
2. **VALIDATE** MANIFEST.json is current (check last_validated timestamp)
3. **VERIFY** no duplicate files will be created (check file_registry)
4. **CONFIRM** operation follows standards from https://github.com/williamzujkowski/standards
5. **USE** appropriate timestamps (prefer time.gov, fallback to system time)

**VIOLATIONS WILL BE AUTOMATICALLY BLOCKED**

Your operation will FAIL if you:
- Create duplicate files instead of updating existing ones
- Don't update MANIFEST.json after changes
- Violate standards from the submodule
- Use incorrect timestamps
- Save files to incorrect directories

**ENFORCEMENT IS ACTIVE**:
- Pre-commit hooks validate all changes
- GitHub Actions enforce standards on all pushes
- `.claude-rules.json` defines mandatory rules

See `.claude-rules.json` for complete enforcement rules.

**Full guidelines:** `docs/context/core/enforcement.md`

---

## 🔄 Progressive Context Loading System

### 3.1: How It Works

The modular architecture enables **task-based progressive disclosure**:

1. **Always loaded:** CLAUDE.md (this file) provides root anchor (~2,000 words, 8K tokens)
2. **Conditionally loaded:** Task-appropriate modules from `docs/context/` (2K-15K tokens)
3. **On-demand:** Deep-dive references when specific details needed

**Example:** Creating a blog post loads 4 modules (15K tokens total) instead of entire 80K monolith.

**Benefits:**
- 2-10x faster context processing
- Reduced hallucination (only relevant context)
- Clearer decision boundaries
- Easier maintenance (update one module vs entire file)

**Module discovery:** Use `docs/context/INDEX.yaml` to find relevant modules by task, tag, or priority.

### 3.2: Task-Based Loading Patterns

Use this table to determine which modules to load for common tasks:

| Task | Load These Modules | Priority | Token Cost |
|------|-------------------|----------|------------|
| **Create blog post** | `core/enforcement` + `core/nda-compliance` + `workflows/blog-writing` + `standards/humanization-standards` | HIGH | ~8K |
| **Transform existing post** | `core/enforcement` + `workflows/blog-transformation` + `standards/humanization-standards` | HIGH | ~6K |
| **Validate content** | `core/enforcement` + `standards/humanization-standards` + `standards/citation-requirements` | HIGH | ~5K |
| **Manage images** | `standards/image-standards` + `technical/image-automation` | MEDIUM | ~3K |
| **Git operations** | `core/enforcement` + `core/standards-integration` + `technical/git-workflow` | HIGH | ~4K |
| **SPARC development** | `core/enforcement` + `workflows/sparc-development` + `technical/agent-coordination` | MEDIUM | ~6K |
| **Swarm orchestration** | `core/enforcement` + `workflows/swarm-orchestration` + `core/file-management` | MEDIUM | ~6K |
| **Emergency debug** | `core/enforcement` + `core/mandatory-reading` + `reference/troubleshooting` | HIGH | ~4K |

**Pattern:** High-priority tasks load `core/enforcement` first, then task-specific workflows, then supporting standards/technical modules.

### 3.3: Module Discovery

Three ways to find relevant modules:

**1. By Task:** Use table above for 8 common patterns

**2. By Index:** Check `docs/context/INDEX.yaml` for complete catalog:
- 10 existing modules (5 core + 5 workflows)
- 15+ planned modules (standards, technical, reference, templates)
- Tags, dependencies, load conditions, token estimates

**3. By Priority:**
- **HIGH:** Always load for file operations, blog writing, git commits
- **MEDIUM:** Load for specific workflows (SPARC, swarms, transformations)
- **LOW:** Load only when explicitly needed (gists, templates, historical context)

**Trust your judgment:** LLMs are capable of autonomous navigation. If unsure, load `core/mandatory-reading` for guidance.

---

## 💡 Core Principles

These principles apply universally across all tasks. For complete guidelines, load the referenced modules.

### 4.1: NDA Compliance

**Golden rules:**
- NEVER discuss current or recent work incidents (2-3 year minimum buffer)
- ALWAYS use homelab attribution for technical examples
- NEVER reference specific government systems or agencies
- ALWAYS time-buffer work references ("years ago I worked on...")

**Safe patterns:**
```markdown
✅ "In my homelab, I discovered X vulnerability in Y."
✅ "Years ago, I worked on systems that faced Z challenge."
✅ "Research shows this attack pattern is common."
```

**Unsafe patterns:**
```markdown
❌ "Last month at work..."
❌ "My current employer uses..."
❌ "We recently discovered..."
```

**Full guidelines:** `docs/context/core/nda-compliance.md`

### 4.2: File Organization

**NEVER save working files, text/mds and tests to the root folder.**

Use these directories:
- `/src` → Source code
- `/tests` → Test files
- `/docs` → Documentation (including this file)
- `/scripts` → Automation utilities
- `/config` → Configuration files

**Common mistakes:**
- ❌ `validate-claims.py` in root
- ❌ `test-citations.md` in root
- ❌ `working-notes.txt` anywhere

**Correct:**
- ✅ `scripts/blog-research/validate-claims.py`
- ✅ `tests/test-citations.py`
- ✅ `docs/working-notes.md`

**Full guidelines:** `docs/context/core/file-management.md`

### 4.3: Concurrent Execution

**The Golden Rule:** "1 MESSAGE = ALL RELATED OPERATIONS"

All related operations in one message for 2.8-4.4x speed improvement.

✅ **Correct:**
```javascript
// Single message with all operations
Read("file1.js")
Read("file2.js")
Edit("file1.js", old, new)
Edit("file2.js", old, new)
Bash("npm test")
```

❌ **Wrong:**
```javascript
// Message 1
Read("file1.js")
// Message 2
Edit("file1.js", old, new)
// Message 3
Bash("npm test")
```

**Why it matters:** Parallel execution = 2.8-4.4x faster. Sequential = slow, wasted tokens.

**Full guidelines:** `docs/context/core/file-management.md`

### 4.4: Documentation Hierarchy

**Primary (Authoritative):**
- **CLAUDE.md**: Master reference for all standards (THIS DOCUMENT)
- **MANIFEST.json**: System inventory and file registry
- **.claude-rules.json**: Enforcement rules
- **docs/context/INDEX.yaml**: Module catalog

**Secondary (Supporting):**
- **docs/context/core/**: Critical rules (5 modules)
- **docs/context/workflows/**: Task-specific processes (5 modules)
- **docs/ARCHITECTURE.md**: System design
- **docs/GUIDES/**: How-to documentation
- **docs/ENFORCEMENT.md**: Mandatory rules

**Generated (Reference):**
- **reports/**: Audit and compliance reports
- **docs/STANDARDS/**: Implementation checklists

**Rule:** All documentation defers to CLAUDE.md and modular context system for canonical requirements.

**Full guidelines:** `docs/context/core/mandatory-reading.md`

---

## 🚀 Quick Start Guide

### For New LLMs (5-Step Onboarding)

**Step 1:** Read this file (CLAUDE.md) completely (~5 minutes)

**Step 2:** Load mandatory reading order:
```bash
# High priority (always load)
1. docs/context/core/enforcement.md
2. docs/context/core/nda-compliance.md
3. docs/context/core/mandatory-reading.md
```

**Step 3:** Understand the loading system:
- Check `docs/context/INDEX.yaml` for module catalog
- Use task-based loading patterns (Section 3.2)
- Load modules progressively as needed

**Step 4:** Identify your task type:
- Blog writing? Load `workflows/blog-writing.md`
- Code changes? Load `core/enforcement.md` + `core/standards-integration.md`
- SPARC development? Load `workflows/sparc-development.md`
- Emergency? Load `reference/troubleshooting.md`

**Step 5:** Validate before committing:
```bash
# Pre-commit hooks check:
- MANIFEST.json current?
- No duplicate files?
- Standards compliance?
- Blog posts pass humanization validation (≥75/100)?
```

### Common Workflows

**Workflow 1: Create New Blog Post**
```bash
# 1. Load required modules
- core/enforcement.md
- core/nda-compliance.md
- workflows/blog-writing.md
- standards/humanization-standards.md (when implemented)

# 2. Use template
cp docs/TEMPLATES/blog-post-writing-template.md working-draft.md

# 3. Write following guidelines
# 4. Validate
python scripts/blog-content/humanization-validator.py --post src/posts/[file].md

# 5. Commit (pre-commit hooks run automatically)
git add src/posts/[file].md
git commit -m "feat: add blog post about [topic]"
```

**Workflow 2: Emergency Debug**
```bash
# 1. Load troubleshooting context
- core/enforcement.md
- core/mandatory-reading.md
- reference/troubleshooting.md (when implemented)

# 2. Check build status
npm run build

# 3. Review recent changes
git log -5 --oneline

# 4. Validate MANIFEST.json
cat MANIFEST.json | jq '.last_validated'

# 5. Check pre-commit hooks
cat .git/hooks/pre-commit
```

### Emergency Contacts

**If something breaks:**

1. **Build fails:** Check `npm run build` output, review recent commits
2. **Pre-commit rejects:** Run `git diff --cached` to see what's being committed
3. **Duplicate file error:** Check `MANIFEST.json` file_registry for existing files
4. **Standards violation:** Review `.claude-rules.json` and `docs/context/core/enforcement.md`
5. **Context confusion:** Return to `docs/context/INDEX.yaml` and reload appropriate modules

**General principle:** When unsure, load `core/mandatory-reading.md` and follow documentation hierarchy.

---

## 📚 Module Index

Complete list of existing modules (10 total). For full catalog with tags, dependencies, and load conditions, see `docs/context/INDEX.yaml`.

| Module | Priority | Load When | Location | Tokens |
|--------|----------|-----------|----------|--------|
| **enforcement** | HIGH | Any file operation, before commits, creating content | `docs/context/core/` | 1500 |
| **nda-compliance** | HIGH | Writing blog posts, discussing work/career, security topics | `docs/context/core/` | 1200 |
| **file-management** | HIGH | Creating files, cleanup operations, concurrent execution | `docs/context/core/` | 1800 |
| **mandatory-reading** | HIGH | First session, onboarding, understanding structure | `docs/context/core/` | 800 |
| **standards-integration** | HIGH | Before file operations, validation, MANIFEST.json updates | `docs/context/core/` | 1000 |
| **blog-writing** | MEDIUM | Creating new blog post, editing existing post, content review | `docs/context/workflows/` | 3500 |
| **sparc-development** | MEDIUM | Using SPARC methodology, TDD development, architecture work | `docs/context/workflows/` | 2800 |
| **swarm-orchestration** | MEDIUM | Multi-agent coordination, complex task decomposition, parallel execution | `docs/context/workflows/` | 2500 |
| **blog-transformation** | MEDIUM | Transforming existing posts, Smart Brevity refinement, citation enhancement | `docs/context/workflows/` | 2000 |
| **gist-management** | LOW | Managing code examples, blog post code ratio >20%, creating shareable snippets | `docs/context/workflows/` | 1800 |

**Planned modules (15+):**
- **standards/**: humanization-validation, citation-requirements, image-standards, accessibility (Phase 7)
- **technical/**: script-catalog, git-commands, build-automation, testing (Phase 8)
- **reference/**: batch-lessons, phase-reports, historical-context, troubleshooting (Phase 9)
- **templates/**: blog-post-template, module-template, script-template, documentation-template (Phase 10)

**Token budgets:**
- Core modules: 6,300 tokens (5 modules)
- Workflow modules: 10,000 tokens (5 modules)
- Total existing: 16,300 tokens
- Available budget: 8,700 tokens remaining

**Full index:** `docs/context/INDEX.yaml`

---

## 🔗 Related Resources

**Essential Documentation:**
- **[docs/ENFORCEMENT.md](docs/ENFORCEMENT.md)** - Extended enforcement rules and examples
- **[docs/GUIDES/LLM_ONBOARDING.md](docs/GUIDES/LLM_ONBOARDING.md)** - Detailed onboarding guide for AI agents
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture and design principles
- **[docs/GUIDES/SCRIPT_CATALOG.md](docs/GUIDES/SCRIPT_CATALOG.md)** - Complete catalog of 37 automation scripts
- **[MANIFEST.json](MANIFEST.json)** - Single source of truth for repository inventory
- **[docs/context/INDEX.yaml](docs/context/INDEX.yaml)** - Complete module catalog with tags and dependencies

**Standards Repository:**
- **[github.com/williamzujkowski/standards](https://github.com/williamzujkowski/standards)** - Coding standards submodule (referenced in enforcement)

**Key Configuration Files:**
- **.claude-rules.json** - Enforcement rules
- **.eleventy.js** - Eleventy configuration
- **package.json** - npm scripts and dependencies
- **tailwind.config.js** - Tailwind CSS customization

---

**Remember:** This is a modular architecture. Load only what you need for the current task. Trust your judgment to navigate autonomously. When unsure, return to `docs/context/INDEX.yaml`.

**Architecture version:** 4.0.0 (modular)
**Previous version:** 3.0.0 (monolith, 12,900 words)
**Efficiency gain:** 97.5% token reduction for simple tasks
