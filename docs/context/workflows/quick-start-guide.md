---
title: Quick Start Guide for New LLMs
category: workflows
priority: HIGH
version: 1.0.0
last_updated: 2025-11-16
estimated_tokens: 1500
load_when:
  - First session onboarding
  - Learning common workflows
  - Emergency troubleshooting
  - Understanding repository structure
dependencies:
  - core/enforcement
  - core/nda-compliance
  - core/mandatory-reading
tags: [onboarding, workflows, quick-start, tutorial, emergency]
---

# Quick Start Guide for New LLMs

## Purpose

This module provides **step-by-step onboarding** for new LLMs, common workflow recipes, and emergency troubleshooting procedures. Use this during first session or when learning repository conventions.

---

## When to Load This Module

- **First session with repository** - Complete 5-step onboarding
- **Learning common workflows** - Follow recipe patterns
- **Emergency troubleshooting** - Quick debug procedures
- **Understanding repo structure** - Navigation guidance

---

## 5-Step Onboarding Process

### Step 1: Read CLAUDE.md (~3 minutes)

**Location:** `/home/william/git/williamzujkowski.github.io/CLAUDE.md`

**Read for:**
- Enforcement rules (Section 1)
- Routing system (Section 3.4)
- Core principle summaries (Section 4)
- Module index (Section 6)

**Why first:** Root anchor provides navigation to all other modules

---

### Step 2: Load Mandatory Modules (~5 minutes)

**High priority (always load):**

```bash
# 1. Enforcement rules
Read docs/context/core/enforcement.md

# 2. NDA compliance
Read docs/context/core/nda-compliance.md

# 3. Mandatory reading order
Read docs/context/core/mandatory-reading.md
```

**Why these three:**
- enforcement.md → Blocks operations if violated
- nda-compliance.md → Prevents privacy breaches
- mandatory-reading.md → Guides to other modules

---

### Step 3: Understand Loading System (~2 minutes)

**Check these resources:**
- `docs/context/INDEX.yaml` - Module catalog (33 modules)
- `docs/context/workflows/routing-patterns.md` - Task-based loading
- `CLAUDE.md Section 3.4` - 3-tier routing system

**Discovery mechanisms:**
1. **By Task:** Use routing-patterns.md for common workflows
2. **By Index:** Check INDEX.yaml for complete catalog
3. **By Priority:** HIGH → always load, MEDIUM → task-specific, LOW → rarely needed

---

### Step 4: Check Routing Requirements (~1 minute)

**Tier 1 (MANDATORY):**
- Creating files? Load enforcement + file-management + standards-integration
- Writing blog posts? Load enforcement + nda-compliance + blog-writing + writing-style
- Git commits? Load enforcement + git-workflow
- Updating MANIFEST.json? Load enforcement + standards-integration
- Deploying swarms? Load enforcement + swarm-orchestration + agent-coordination

**Tier 2 (RECOMMENDED):**
- Transforming posts? Load enforcement + blog-transformation + writing-style
- Validating content? Load enforcement + humanization-standards + citation-research
- Managing images? Load image-standards + image-automation
- Code refactoring? Load enforcement + code-block-quality

**Tier 3 (DISCOVERY):**
- Novel tasks? Search INDEX.yaml by tags → Compare to patterns → Load progressively

---

### Step 5: Validate Before Committing (~2 minutes)

**Pre-commit hooks check:**
- MANIFEST.json current?
- No duplicate files?
- Standards compliance?
- Blog posts pass humanization validation (≥75/100)?
- Metadata format (dates must be YYYY-MM-DD)?

**Run validation scripts:**
```bash
python scripts/validation/metadata-validator.py --format text
python scripts/validation/build-monitor.py
```

**Note:** Playwright tests are JavaScript-based, run via npm (see scripts/*.js)

---

## Common Workflows

### Workflow 1: Create New Blog Post

**Estimated time:** 30-60 minutes
**Complexity:** Medium

**Steps:**

```bash
# 1. Load required modules
Read docs/context/core/enforcement.md
Read docs/context/core/nda-compliance.md
Read docs/context/workflows/blog-writing.md
Read docs/context/standards/humanization-standards.md

# 2. Use template
cp docs/TEMPLATES/blog-post-writing-template.md working-draft.md

# 3. Write following guidelines
# - BLUF (Bottom Line Up Front)
# - Polite Linus Torvalds style
# - Humanization score ≥75/100
# - 12+ academic citations
# - NDA compliant (homelab attribution)

# 4. Validate
python scripts/blog-content/humanization-validator.py --post src/posts/[file].md

# 5. Commit (pre-commit hooks run automatically)
git add src/posts/[file].md
git commit -m "feat: add blog post about [topic]"
```

**Pre-flight checklist:**
- [ ] Topic fills content gap (check blog-topic-summary.md)
- [ ] NDA compliant (no work references, 2-3 year buffer)
- [ ] Humanization score ≥75/100
- [ ] 12+ citations (50%+ academic with DOI/arXiv)
- [ ] Frontmatter complete (author, date, description, tags, images)

---

### Workflow 2: Emergency Debug

**Estimated time:** 10-20 minutes
**Complexity:** Low

**Steps:**

```bash
# 1. Load troubleshooting context
Read docs/context/core/enforcement.md
Read docs/context/core/mandatory-reading.md
# Read docs/context/reference/troubleshooting.md (if available)

# 2. Check build status
npm run build

# 3. Review recent changes
git log -5 --oneline

# 4. Validate MANIFEST.json
cat MANIFEST.json | jq '.last_validated'

# 5. Check pre-commit hooks
cat .git/hooks/pre-commit
```

**Common issues:**
1. **Build fails** → Check npm run build output, review recent commits
2. **Pre-commit rejects** → Run git diff --cached to see staged changes
3. **Duplicate file error** → Check MANIFEST.json file_registry
4. **Standards violation** → Review .claude-rules.json and enforcement.md
5. **Context confusion** → Return to INDEX.yaml, reload modules
6. **Dependency issues** → Check Mermaid syntax (v10+), date formats (YYYY-MM-DD)

---

### Workflow 3: Swarm Orchestration

**Estimated time:** 20-30 minutes
**Complexity:** High

**Steps:**

```bash
# 1. Load required modules
Read docs/context/core/enforcement.md
Read docs/context/workflows/swarm-orchestration.md
Read docs/context/technical/agent-coordination.md

# 2. Validate agent types exist (prevent hallucination)
# Check agent-coordination.md for 54 available agent types

# 3. Decompose task into parallel subtasks
# Pattern: research → implement → test → review

# 4. Deploy swarm with TodoWrite batching
# Use concurrent execution (1 message = all operations)
TodoWrite([
  {"content": "Research task", "status": "in_progress"},
  {"content": "Implement feature", "status": "pending"},
  {"content": "Test implementation", "status": "pending"},
  {"content": "Review code", "status": "pending"}
])

# 5. Coordinate via shared memory/TodoWrite
# Track progress: 6 agents, 11 tasks, 27 minutes typical

# 6. Validate deployment identifiers
# NEVER hardcode swarm IDs in documentation
# Pattern: Use generic examples ("swarm-[id]"), not deployment-specific values
```

**Agent types available:**
- Core: coder, reviewer, tester, planner, researcher
- Specialized: code-analyzer, system-architect, backend-dev, mobile-dev
- GitHub: pr-manager, code-review-swarm, issue-tracker
- SPARC: sparc-coord, specification, pseudocode, architecture, refinement

**See:** `docs/context/technical/agent-coordination.md` for complete list (54 total)

---

## Emergency Contacts (Troubleshooting Decision Tree)

**If something breaks, follow this decision tree:**

### Issue 1: Build Fails

**Symptoms:** `npm run build` exits with error

**Debug steps:**
```bash
# 1. Check build output
npm run build 2>&1 | tee build-error.log

# 2. Review recent commits
git log -5 --oneline
git diff HEAD~1

# 3. Validate dependencies
npm ci  # Clean install
```

**Common causes:**
- Mermaid syntax error (check v10+ compliance)
- Missing frontmatter fields (author, date, description, tags)
- Broken internal links
- Invalid date format (must be YYYY-MM-DD)

---

### Issue 2: Pre-Commit Rejects

**Symptoms:** `git commit` blocked by pre-commit hook

**Debug steps:**
```bash
# 1. See what's being committed
git diff --cached

# 2. Check validation errors
# Pre-commit output shows specific violations

# 3. Fix violations or bypass (with justification)
git commit --no-verify -m "emergency: [reason for bypass]"
```

**Common violations:**
- NDA compliance (work references, org ownership)
- Humanization score <75/100
- Code ratio >25%
- Metadata format errors
- Duplicate files

---

### Issue 3: Duplicate File Error

**Symptoms:** Operation blocked - duplicate file detected

**Debug steps:**
```bash
# 1. Check MANIFEST.json
grep -r "scripts/blog-research/validate-claims.py" MANIFEST.json

# 2. Update existing file instead
# OR remove existing file first (with justification)

# 3. Verify no duplicates
jq '.file_registry | keys' MANIFEST.json
```

**Prevention:** Always check MANIFEST.json before creating files

---

### Issue 4: Standards Violation

**Symptoms:** GitHub Actions fail, .claude-rules.json violation

**Debug steps:**
```bash
# 1. Review enforcement rules
cat .claude-rules.json

# 2. Check specific violation
# GitHub Actions output shows failing check

# 3. Fix violation
# Follow guidance in docs/context/core/enforcement.md
```

**Common standards:**
- File organization (no root directory clutter)
- Python logging (use centralized logging_config.py)
- Code block quality (earn-their-place philosophy)
- Citation research (no fabrication, verify sources)

---

### Issue 5: Context Confusion

**Symptoms:** Unclear which modules to load, routing uncertainty

**Debug steps:**
```bash
# 1. Return to INDEX.yaml
Read docs/context/INDEX.yaml

# 2. Check routing patterns
Read docs/context/workflows/routing-patterns.md

# 3. Reload appropriate modules
# Use tier system (MANDATORY/RECOMMENDED/OPTIONAL)
```

**Prevention:** Always check routing-patterns.md before starting task

---

### Issue 6: Dependency Issues

**Symptoms:** Missing dependencies, version conflicts

**Debug steps:**
```bash
# 1. Check Mermaid syntax (v10+)
grep -r "```mermaid" src/posts/*.md

# 2. Validate date formats
grep -r "date:" src/posts/*.md | grep -v "YYYY-MM-DD"

# 3. Check metadata fields
python scripts/validation/metadata-validator.py --format text
```

**Requirements:**
- Mermaid v10+ syntax (no `style` attribute on subgraphs)
- Date format: YYYY-MM-DD
- Metadata: author, date, description, tags, images

---

## General Principle

**When unsure:**
1. Load `core/mandatory-reading.md` for guidance
2. Check `docs/context/INDEX.yaml` for module discovery
3. Follow documentation hierarchy (Primary → Secondary → Generated)
4. Ask user for clarification before proceeding

---

## Navigation Tips

### Finding Specific Documentation

**Primary (Authoritative):**
- CLAUDE.md - Root anchor
- MANIFEST.json - File registry
- .claude-rules.json - Enforcement rules
- INDEX.yaml - Module catalog

**Secondary (Supporting):**
- docs/ENFORCEMENT.md - Extended rules
- docs/ARCHITECTURE.md - System design
- docs/GUIDES/ - How-to guides
- docs/context/core/ - Critical rules

**Generated (Reference):**
- reports/ - Audit reports
- docs/STANDARDS/ - Checklists

### Module Discovery Strategies

**By Task:**
- Check routing-patterns.md first
- Find matching workflow
- Load explicit sequence

**By Tag:**
- Check INDEX.yaml tags
- Find related modules
- Load dependencies

**By Priority:**
- HIGH → Load for most tasks
- MEDIUM → Load for specific workflows
- LOW → Load only when needed

---

## Post-Onboarding

**After completing onboarding:**
- [ ] Understand enforcement rules (what blocks operations)
- [ ] Know routing system (3-tier MANDATORY/RECOMMENDED/OPTIONAL)
- [ ] Can navigate via INDEX.yaml
- [ ] Validated pre-commit hooks work
- [ ] Completed at least one workflow

**Next steps:**
- Practice common workflows (blog post, git commit, swarm orchestration)
- Explore module catalog (INDEX.yaml)
- Read historical learnings (proven patterns)
- Understand repository architecture (docs/ARCHITECTURE.md)

---

## Cross-References

**Related modules:**
- [enforcement.md](../core/enforcement.md) - Mandatory rules
- [nda-compliance.md](../core/nda-compliance.md) - Privacy protection
- [mandatory-reading.md](../core/mandatory-reading.md) - Documentation hierarchy
- [routing-patterns.md](./routing-patterns.md) - Task-based loading

**External references:**
- `docs/GUIDES/LLM_ONBOARDING.md` - Detailed onboarding guide
- `docs/ARCHITECTURE.md` - System architecture
- `docs/context/INDEX.yaml` - Complete module catalog
- `CLAUDE.md` - Root anchor

---

## Changelog

- **2025-11-16**: Initial extraction from CLAUDE.md v4.1.0 Section 5 (Quick Start Guide)
