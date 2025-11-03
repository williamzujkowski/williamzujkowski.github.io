---
STATUS: AUTHORITATIVE
VERSION: 4.0.1
LAST_AUDIT: 2025-11-02
COMPLIANCE: 100%
ARCHITECTURE: MODULAR
TOKEN_EFFICIENCY: 84.9%
---

# Claude Code Configuration - SPARC Development Environment

# 🏛️ AUTHORITATIVE DOCUMENTATION NOTICE

This file (CLAUDE.md) serves as the **root anchor** for a modular documentation architecture:
- Progressive context loading based on task requirements
- 28 specialized modules organized by priority (core, workflows, standards, technical, reference, templates)
- Token-efficient: Load only what you need for the current task
- Complete index: `docs/context/INDEX.yaml`

**Previous architecture:** 12,900-word monolith (80,000+ tokens) loaded for every task
**New architecture:** ~2,000-word anchor (8,000 tokens) + selective module loading (2,000-15,000 tokens)
**Efficiency gain:** 84.9% reduction in unnecessary context (2.6K vs 17K tokens for simple tasks)

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
- 28 existing modules (5 core + 5 workflows + 5 standards + 6 technical + 3 reference + 4 templates)
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

### 4.3: Python Package Management with UV

**This repository uses UV (Rust-based Python package manager) instead of pip.**

**Why UV:**
- 10-100x faster than pip
- Reliable dependency resolution
- Automatic virtual environment management
- Zero configuration required

**Installation:**
```bash
# Already installed (v0.7.3)
# To verify: uv --version

# If needed:
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Common Commands:**
```bash
# Install project dependencies
uv sync

# Install specific package
uv pip install package-name

# Run Python script
uv run python scripts/blog-content/humanization-validator.py --batch

# Run tool without installation
uv run black .
uv run ruff check .
```

**All Python scripts now use:** `#!/usr/bin/env -S uv run python3`

**Centralized logging:** Use `scripts/lib/logging_config.py` for consistent logging across scripts
- Structured JSON logging
- Automatic file + console handlers
- Debug mode support

**Migration guide:** `docs/guides/UV_MIGRATION_GUIDE.md`

### 4.4: Concurrent Execution

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

**Swarm coordination:** For complex tasks, 5 specialized agents completed 11 tasks in 27 minutes using parallel execution patterns. Load `workflows/swarm-orchestration.md` for multi-agent coordination.

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
- Metadata format (dates must be YYYY-MM-DD)?

# Run validation scripts:
python scripts/blog-content/metadata-validator.py --batch
python scripts/blog-content/build-monitor.py
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

**Workflow 3: Swarm Orchestration**
```bash
# 1. Load required modules
- core/enforcement.md
- workflows/swarm-orchestration.md
- technical/agent-coordination.md (for agent type validation)

# 2. Validate agent types exist (prevent hallucination)
# Check docs/context/technical/agent-coordination.md for 54 available agent types

# 3. Decompose task into parallel subtasks
# Pattern: research → implement → test → review

# 4. Deploy swarm with TodoWrite batching
# Use concurrent execution (1 message = all operations)

# 5. Coordinate via shared memory/TodoWrite
# Track progress: 6 agents, 11 tasks, 27 minutes typical
```

### Emergency Contacts

**If something breaks:**

1. **Build fails:** Check `npm run build` output, review recent commits
2. **Pre-commit rejects:** Run `git diff --cached` to see what's being committed
3. **Duplicate file error:** Check `MANIFEST.json` file_registry for existing files
4. **Standards violation:** Review `.claude-rules.json` and `docs/context/core/enforcement.md`
5. **Context confusion:** Return to `docs/context/INDEX.yaml` and reload appropriate modules
6. **Dependency issues:** Check Mermaid syntax (v10+), date formats (YYYY-MM-DD), metadata fields (author, tags)

**General principle:** When unsure, load `core/mandatory-reading.md` and follow documentation hierarchy.

---

## 📚 Module Index

Complete list of existing modules (28 total). For full catalog with tags, dependencies, and load conditions, see `docs/context/INDEX.yaml`.

| Module | Priority | Load When | Location | Tokens |
|--------|----------|-----------|----------|--------|
| **enforcement** | HIGH | Any file operation, before commits, creating content | `docs/context/core/` | 3140 |
| **nda-compliance** | HIGH | Writing blog posts, discussing work/career, security topics | `docs/context/core/` | 4532 |
| **file-management** | HIGH | Creating files, cleanup operations, concurrent execution | `docs/context/core/` | 4772 |
| **mandatory-reading** | HIGH | First session, onboarding, understanding structure | `docs/context/core/` | 3708 |
| **standards-integration** | HIGH | Before file operations, validation, MANIFEST.json updates | `docs/context/core/` | 4104 |
| **blog-writing** | MEDIUM | Creating new blog post, editing existing post, content review | `docs/context/workflows/` | 7776 |
| **sparc-development** | MEDIUM | Using SPARC methodology, TDD development, architecture work | `docs/context/workflows/` | 4240 |
| **swarm-orchestration** | MEDIUM | Multi-agent coordination, complex task decomposition, parallel execution | `docs/context/workflows/` | 4124 |
| **blog-transformation** | MEDIUM | Transforming existing posts, Smart Brevity refinement, citation enhancement | `docs/context/workflows/` | 5084 |
| **gist-management** | LOW | Managing code examples, blog post code ratio >20%, creating shareable snippets | `docs/context/workflows/` | 4660 |

**Additional modules (18 total, all implemented):**
- **standards/**: humanization-standards (9128), citation-research (5604), image-standards (5720), accessibility (5448), writing-style (7460)
- **technical/**: script-catalog (3992), git-workflow (5436), build-automation (4160), agent-coordination (4620), research-automation (3904), image-automation (4144)
- **reference/**: batch-history (5872), compliance-history (4292), directory-structure (4316)
- **templates/**: blog-post-template (4556), module-template (3804), script-template (4688), documentation-template (5056)

**Accurate token budgets (all 28 modules measured):**
- Core modules: **20,256 tokens** (5 modules) - was 6,300
- Workflow modules: **25,884 tokens** (5 modules) - was 6,492
- Standards modules: **33,360 tokens** (5 modules) - was 10,177
- Technical modules: **26,256 tokens** (6 modules) - was 7,850
- Reference modules: **14,480 tokens** (3 modules) - was 5,080
- Template modules: **18,104 tokens** (4 modules) - was 6,334
- **ACTUAL TOTAL: 138,340 tokens** (28 modules complete)
- **Previous estimate: 42,233 tokens (3.3x underestimate)**
- Note: High token count emphasizes importance of selective modular loading

**Full index:** `docs/context/INDEX.yaml`

---

## 🔗 Related Resources

**Essential Documentation:**
- **[docs/ENFORCEMENT.md](docs/ENFORCEMENT.md)** - Extended enforcement rules and examples
- **[docs/GUIDES/LLM_ONBOARDING.md](docs/GUIDES/LLM_ONBOARDING.md)** - Detailed onboarding guide for AI agents
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture and design principles
- **[docs/GUIDES/SCRIPT_CATALOG.md](docs/GUIDES/SCRIPT_CATALOG.md)** - Script catalog (37 core utilities documented, 85+ total)
- **[MANIFEST.json](MANIFEST.json)** - Single source of truth for repository inventory
- **[docs/context/INDEX.yaml](docs/context/INDEX.yaml)** - Complete module catalog with tags and dependencies
- **[TODO.md](TODO.md)** - Active tasks and improvement backlog (code ratio fixes, Python migration, etc.)

**Standards Repository:**
- **[github.com/williamzujkowski/standards](https://github.com/williamzujkowski/standards)** - Coding standards submodule (referenced in enforcement)

**Key Configuration Files:**
- **.claude-rules.json** - Enforcement rules
- **.eleventy.js** - Eleventy configuration
- **package.json** - npm scripts and dependencies
- **tailwind.config.js** - Tailwind CSS customization

---

**Remember:** This is a modular architecture. Load only what you need for the current task. Trust your judgment to navigate autonomously. When unsure, return to `docs/context/INDEX.yaml`.

**Architecture version:** 4.0.1 (modular + swarm learnings)
**Previous version:** 3.0.0 (monolith, 12,900 words)
**Efficiency gain:** 84.9% token reduction for simple tasks (2.6K vs 17K tokens)

**Recent improvements (2025-11-02):**
- Added Mermaid v10 migration guidance (88% posts had v9 syntax)
- Documented validation infrastructure (metadata-validator, build-monitor)
- Emphasized date format enforcement (YYYY-MM-DD via pre-commit hooks)
- Added Python logging standards reference (scripts/lib/logging_config.py)
- Documented swarm coordination patterns (5 agents, 11 tasks, 27 minutes; updated to 6-agent deployments with agent type validation)
- Documented gist extraction strategy for code ratio compliance (21.0% verified, extract >30 line blocks, see CODE_RATIO_MEASUREMENT_METHODOLOGY.md for methodology)
- Verified token estimate accuracy (corrected 3.3x underestimate: 42K claimed → 138K actual)
- Created Python script template (503 lines, docs/context/templates/script-template.md) with logging, error handling, type hints
- Documented performance optimization insights (validation scripts <2s/<100MB, incremental improvements: 34% speedup potential via date regex pre-filter)
- Established monthly repository cleanup pattern (vestigial file scanning, archive vs delete criteria, documentation accuracy audits)
- Completed Python logging Phase 1: metadata-validator.py refactored (710 lines, v4.0, centralized logging, dataclasses, comprehensive docstrings)
- Implemented parallel validation (ThreadPoolExecutor, 6 workers, 20-25% speedup for I/O-bound operations)
- Created test infrastructure (tests/validation/fixtures/) with automated regression prevention
- Documented SEO description formula (120-160 chars optimal, validation integrated into metadata-validator)
- Session 5: Validated gist embed rendering with Playwright (8 gists in Claude-Flow post, zero console errors, <2s load time)
- Session 5: Container Security code ratio compliance achieved (32.8%→20.5% with 10 gists, 717→441 lines, below 25% threshold)
- Session 6: Fixed pre-commit validator regex bug (closing fences matched, 40% overestimation; implemented line-by-line parser from code-ratio-calculator.py)
- Session 6: Completed Container Security gist extraction (17 total gists, final ratio 10.5%, well below 25% threshold)
- Session 6: Corrected Python logging migration status (actual 19.5%, 15/77 scripts; previous 29.9% claim was inaccurate; documented in comprehensive analysis)
- Session 6: Established validator cross-verification requirement (always verify with code-ratio-calculator.py, not pre-commit alone, to prevent false positives)
