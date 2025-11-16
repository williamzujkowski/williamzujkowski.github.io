---
STATUS: AUTHORITATIVE
VERSION: 4.1.0
LAST_AUDIT: 2025-11-10
COMPLIANCE: 100%
ARCHITECTURE: MODULAR
TOKEN_EFFICIENCY: 84.9%
ROUTING_VERSION: 1.0.0
WRITING_STYLE: Polite Linus Torvalds
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

**Last comprehensive audit:** 2025-11-02 (Session 10: 2025-11-03)
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

1. **CHECK ROUTING REQUIREMENTS** (Section 3.4) for mandatory skills
2. **VERIFY** `.claude-rules.json` enforcement rules
3. **VALIDATE** MANIFEST.json is current (check last_validated timestamp)
4. **CHECK** no duplicate files will be created (check file_registry)
5. **CONFIRM** operation follows standards from https://github.com/williamzujkowski/standards
6. **USE** appropriate timestamps (prefer time.gov, fallback to system time)
7. **AUDIT** documentation accuracy monthly (prevent exaggeration creep, verify stats)

**NEW IN v4.1.0**: Some operations REQUIRE specific skills before proceeding:
- 🚨 **Creating files** → MUST load enforcement + file-management + standards-integration
- 🚨 **Writing blog posts** → MUST load enforcement + nda-compliance + blog-writing + writing-style
- 🚨 **Git commits** → MUST load enforcement + git-workflow
- 🚨 **MANIFEST.json ops** → MUST load enforcement + standards-integration
- 🚨 **Swarm deployment** → MUST load enforcement + swarm-orchestration + agent-coordination

See Section 3.4 for complete 3-tier routing system (MANDATORY/RECOMMENDED/OPTIONAL).

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

## 🎯 LLM Autonomy Boundaries

**Purpose:** Define when you MUST follow routing rules vs when you can use judgment.

**Framework:** Always/Usually/Sometimes/Never - determines routing compliance level.

**ALWAYS Follow (No Judgment):**
- 🚨 MANDATORY operations (Tier 1) → Load required skills or operation blocks
- core/enforcement.md → For ANY file operation
- core/nda-compliance.md → For blog posts, security topics
- Routing validation → Check Section 3.4 before starting task

**USUALLY/SOMETIMES/NEVER:** See `docs/context/core/autonomy-framework.md` for complete decision framework, override scenarios, and judgment guidelines.

**Override Scenarios (When judgment allowed):**
- Emergency hotfix (broken link) → May skip full transformation workflow
- Read-only git operation → May skip standards-integration
- Single typo fix → May skip full quality framework
- Quick validation → May skip humanization for link checks

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

**Quick Reference Table:**

| Task | Tier | Required Modules | Token Cost |
|------|------|-----------------|------------|
| Create blog post | 🚨 MANDATORY | enforcement + nda-compliance + blog-topic-summary + blog-writing + writing-style | ~16K |
| Transform post | ✅ RECOMMENDED | enforcement + blog-transformation + writing-style | ~10K |
| Refactor quality | ✅ RECOMMENDED | enforcement + code-block-quality + blog-transformation | ~6K |
| Validate content | ✅ RECOMMENDED | enforcement + humanization-standards + citation-research | ~5K |
| Manage images | 💡 OPTIONAL | image-standards + image-automation | ~3K |
| Git operations | 🚨 MANDATORY | enforcement + git-workflow | ~4K |
| SPARC development | ✅ RECOMMENDED | enforcement + sparc-development + agent-coordination | ~6K |
| Swarm orchestration | 🚨 MANDATORY | enforcement + swarm-orchestration + agent-coordination | ~6K |
| Emergency debug | ✅ RECOMMENDED | enforcement + mandatory-reading | ~4K |

**Pattern:** 🚨 MANDATORY tasks block without required skills. ✅ RECOMMENDED tasks warn but allow override. 💡 OPTIONAL tasks use LLM judgment.

**Complete loading sequences:** See `docs/context/workflows/routing-patterns.md` for explicit step-by-step loading instructions (9 common workflows with file paths and dependencies).

### 3.3: Module Discovery

Three ways to find relevant modules:

**1. By Task:** Use table above for 8 common patterns

**2. By Index:** Check `docs/context/INDEX.yaml` for complete catalog:
- 32 existing modules (5 core + 6 workflows + 7 standards + 6 technical + 4 reference + 4 templates)
- Tags, dependencies, load conditions, token estimates

**3. By Priority:**
- **HIGH:** Always load for file operations, blog writing, git commits
- **MEDIUM:** Load for specific workflows (SPARC, swarms, transformations)
- **LOW:** Load only when explicitly needed (gists, templates, historical context)

**Trust your judgment:** LLMs are capable of autonomous navigation. If unsure, load `core/mandatory-reading` for guidance.

### 3.4: Skill Routing Architecture

**NEW IN v4.1.0:** Explicit 3-tier routing system balances enforcement with autonomy.

**How routing works:**
1. Check if operation is **Tier 1 MANDATORY** → Load required skills or operation blocks
2. Check if pattern is **Tier 2 RECOMMENDED** → Load suggested skills unless override justified
3. For novel tasks (**Tier 3 OPTIONAL**) → Use INDEX.yaml discovery + LLM judgment

#### Tier 1: MANDATORY Skills (5 Operations)

These operations CANNOT proceed without specified skills. Enforced by `.claude-rules.json`.

| Operation | Required Skills | Why Mandatory | Enforcement |
|-----------|----------------|---------------|-------------|
| **Create files** | enforcement + file-management + standards-integration | Prevents duplicates, wrong directories, MANIFEST.json corruption | Pre-commit blocks |
| **Write blog posts** | enforcement + nda-compliance + **blog-topic-summary** + blog-writing + writing-style | Public content with privacy/NDA risks, must fill gaps | Pre-commit blocks |
| **Git commits** | enforcement + git-workflow | Commits permanent, must validate | Pre-commit blocks |
| **MANIFEST.json ops** | enforcement + standards-integration | Single source of truth, corruption breaks repo | Pre-commit blocks |
| **Swarm deployment** | enforcement + swarm-orchestration + agent-coordination | Prevents hallucinated agents, ensures coordination | Runtime blocks |

**Loading sequence for Tier 1:**
```bash
# Example: Creating a blog post
Read docs/context/core/enforcement.md                    # MANDATORY
Read docs/context/core/nda-compliance.md                 # MANDATORY
Read docs/context/workflows/blog-topic-summary.md        # MANDATORY
Read docs/context/workflows/blog-writing.md              # MANDATORY
Read docs/context/standards/writing-style.md             # MANDATORY

# Now safe to create blog post (topic validated, gaps checked)
```

#### Tier 2: RECOMMENDED Skills (15 Patterns)

These patterns have proven combinations but allow override for good reason.

**Top 5 patterns:**

| Pattern | Recommended Skills | Override Scenario |
|---------|-------------------|-------------------|
| **Blog transformation** | enforcement + blog-transformation + writing-style + citation-research | Emergency link fix (don't need full workflow) |
| **Content validation** | enforcement + humanization-standards + citation-research | Quick link check (don't need humanization) |
| **Image management** | image-standards + image-automation | One-off update (don't need automation) |
| **Code refactoring** | enforcement + code-block-quality + blog-transformation | Typo fix (don't need quality framework) |
| **SPARC development** | enforcement + sparc-development + agent-coordination | Simple script (don't need TDD) |

**Complete list:** See `docs/context/INDEX.yaml` routing_patterns section

**Loading sequence for Tier 2:**
```bash
# Example: Blog transformation
Read docs/context/core/enforcement.md             # MANDATORY
Read docs/context/workflows/blog-transformation.md # RECOMMENDED
Read docs/context/standards/writing-style.md       # RECOMMENDED

# If override needed: Document reason
# "Skipping citation-research because only fixing broken links"
```

#### Tier 3: OPTIONAL (LLM Autonomy)

For novel tasks, use discovery mechanisms:
- **By tags:** INDEX.yaml maps tags → skills (e.g., "citations" → citation-research + research-automation)
- **By priority:** HIGH → always consider, MEDIUM → task-dependent, LOW → rarely needed
- **By similarity:** "This is like [known pattern] but different because..."

**Loading sequence for Tier 3:**
```bash
# Example: Novel automation task
# Step 1: Check INDEX.yaml for relevant tags
# Step 2: Load discovered modules progressively
# Step 3: Document pattern for future Tier 2 promotion

Read docs/context/INDEX.yaml  # Discover modules by tags
Read docs/context/technical/script-catalog.md  # Discovered via "automation" tag
Read docs/context/workflows/sparc-development.md  # Discovered via "development" tag

# Document: "Novel task: CLI automation. Loaded script-catalog + sparc-development. Consider promoting to Tier 2."
```

#### Routing Validation Checklist

Before starting ANY task:
- [ ] Checked Section 3.4 for routing requirements
- [ ] Identified task tier (MANDATORY/RECOMMENDED/OPTIONAL)
- [ ] Loaded required skills in correct order
- [ ] Verified dependencies (checked INDEX.yaml)
- [ ] Documented any overrides with reasoning

After completing task:
- [ ] All required skills were applied correctly
- [ ] No MANDATORY skills were skipped
- [ ] Override reasons documented (if any)
- [ ] Novel patterns noted for future routing improvements

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

**Monthly maintenance:**
- ✅ Scan for vestigial content (outdated scripts, orphaned directories)
- ✅ Archive (don't delete) questionable files for reversibility
- ✅ Document cleanup rationale in commit messages

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

### 4.4.1: Code Block Quality Standards

**Philosophy:** Code blocks must "earn their place" - every code block should teach something readers can't get from prose.

**Decision Framework:**

**KEEP INLINE (<15 lines):**
- Teaches core concept (syntax examples, key patterns)
- Context-critical (interrupting flow to visit gist breaks learning)
- Complete and runnable (or clearly labeled as simplified)
- Cannot be better expressed as diagram/prose

**EXTRACT TO GIST (>20 lines):**
- Complete implementations readers will copy-paste
- Reference material (full configs, complete scripts)
- Reusable across projects (not post-specific examples)
- Latest version maintenance outside post valuable

**DELETE/CONVERT (any length):**
- Truncated with "# ... (additional implementation)" - incomplete pseudocode
- Redundant with official documentation (link instead)
- Can be better expressed as prose (2-3 sentences)
- Can be better expressed as Mermaid diagram (workflows, sequences)

**Tiered Thresholds by Post Type:**

| Post Type | Total Code Ratio | Actual Code Ratio | Rationale |
|-----------|-----------------|-------------------|-----------|
| Tutorial | <35% | <30% | Step-by-step needs examples |
| Conceptual | <25% | <20% | Diagrams + light code |
| Experience | <20% | <15% | Lessons > implementation |
| DIAGRAM-HEAVY | <60%* | <10% | *If >80% Mermaid educational |

**Add to frontmatter:** `post_type: tutorial` (applies appropriate threshold)

**Enforcement:** Pre-commit hook checks via `code-ratio-calculator.py --post-type-aware`

**Full guidelines:** `docs/context/standards/code-block-quality.md`

### 4.5: Writing Style and Tone

**This repository enforces "Polite Linus Torvalds" style for all technical writing.**

**Core characteristics:**
- Technical precision without explanation bloat
- Direct, casual-professional tone (engineer-to-engineer)
- Active voice, short sentences (avg <20 words)
- Zero tolerance for fluff and decorative punctuation
- Results-oriented language ("Show me the code")

**Prohibited patterns:**
- ❌ Semicolons for sophistication
- ❌ Em-dashes for dramatic pauses
- ❌ Symmetrical sentence patterns (Smart Brevity disease)
- ❌ Rhetorical questions and setup-punchline structures
- ❌ Corporate hedging ("arguably", "potentially", "perhaps")
- ❌ Academic formality ("furthermore", "moreover", "hence")
- ❌ Filler phrases ("in order to" → "to", "due to the fact that" → "because")

**Quality test:** If it sounds like "engineer explaining facts to another engineer" → correct. If it sounds like TED talk/textbook/marketing → wrong.

**Full guidelines:** `docs/context/standards/writing-style.md` (7,460 tokens)

### 4.5.1: Technical Authority & Security Expertise

**Author background:** Senior security engineer with system/network administration foundation. This expertise shapes content depth, technical accuracy, and credibility markers.

**Technical depth standards:**

**System-level understanding required:**
- Network protocols, packet analysis, traffic inspection
- Operating system internals (Linux kernel, Windows internals)
- Infrastructure security (firewalls, IDS/IPS, SIEM)
- Virtualization and containerization (VMware, Docker, Kubernetes)
- Hardware configuration (servers, networking equipment, storage)

**Security expertise areas:**
- Vulnerability assessment and penetration testing
- Incident response and forensics
- Security architecture and design
- Compliance frameworks (NIST, CIS, DISA STIGs)
- Threat modeling and risk assessment

**Appropriate technical depth examples:**

✅ **Correct depth (senior engineer perspective):**
```markdown
"Suricata's AF_PACKET mode bypasses kernel network stack for direct NIC access.
Set ring-size to 64MB minimum (128MB for 10Gbps) to handle burst traffic.
Monitor /proc/net/pf_ring/stats for packet drops - anything >0.1% needs tuning."

"eBPF's verifier limits stack to 512 bytes and enforces bounded loops.
For complex packet parsing, pre-allocate per-CPU maps (BPF_MAP_TYPE_PERCPU_ARRAY)
to avoid runtime allocation failures under load."

"EPSS models exploit likelihood using CVSS + real-world telemetry.
KEV catalog requires active exploitation evidence from CISA threat intel.
Cross-reference both: EPSS >0.7 + KEV presence = immediate patching required."
```

❌ **Insufficient depth (junior engineer perspective):**
```markdown
"Suricata is fast because it uses special networking modes."
"eBPF is good for security monitoring."
"EPSS helps you prioritize vulnerabilities."
```

**Credibility markers (use appropriately):**

**Experience indicators (NDA-compliant):**
- "Years of system administration taught me..." (vague timeframe)
- "After managing enterprise networks..." (no employer details)
- "In production environments, I've seen..." (no work specifics)
- "Homelab testing confirmed industry patterns..." (safe attribution)

**Knowledge depth signals:**
- Specific version numbers and configuration parameters
- Performance metrics and tuning thresholds
- Edge cases and failure modes
- Trade-offs between competing approaches
- Tool limitations and workarounds

**Cross-reference with NDA compliance:**

✅ **Safe expertise demonstration:**
```markdown
"In my homelab, I replicated CVE-2024-1234 using Metasploit against hardened containers.
Escape achieved in <3 minutes via cgroup release_agent. Mitigation requires
AppArmor profile: deny /sys/fs/cgroup/**/release_agent rwklx."

"Years ago, I learned IDS signature tuning the hard way. False positive rates
>5% train analysts to ignore alerts. Suppress noisy signatures first
(dns.query ANY, tls.sni *.cdn.cloudflare.com), then tune detection thresholds."
```

❌ **Unsafe expertise demonstration:**
```markdown
"Last month at work, we discovered RCE in our production environment..."
"My current employer's SIEM correlates 500K events/second using..."
"Federal systems I manage require multi-factor authentication..."
```

**Security best practices in examples:**

**Always demonstrate:**
- Least privilege principles (not root unless necessary)
- Defense in depth (multiple security layers)
- Fail-secure defaults (deny-by-default configurations)
- Input validation and sanitization
- Secure credential management (never hardcoded secrets)

**Example patterns:**

✅ **Secure examples:**
```bash
# Run as unprivileged user
sudo -u scanner nmap -sV target.local

# Read-only bind mount
docker run -v /data:/data:ro alpine

# Environment variables for secrets
export DB_PASSWORD=$(vault kv get -field=password secret/db)
```

❌ **Insecure examples:**
```bash
# Running as root unnecessarily
nmap -sV target.local

# Writable mount for read-only data
docker run -v /data:/data alpine

# Hardcoded credentials
DB_PASSWORD="admin123"
```

**Technical accuracy standards:**

**Required for all technical content:**
- Command syntax verified (tested in homelab before publishing)
- Version-specific features noted (tool versions, API changes)
- Error messages quoted exactly (no paraphrasing)
- Performance metrics measured (not estimated or guessed)
- Configuration parameters validated (defaults, ranges, dependencies)

**Quality checklist:**
- [ ] Technical details accurate to specific tool versions
- [ ] Security implications explained (not just "how" but "why secure")
- [ ] Edge cases and failure modes documented
- [ ] NDA compliance verified (homelab attribution, time buffering)
- [ ] Commands tested before publication
- [ ] Performance claims backed by measurements

**Cross-reference:** See `docs/context/core/nda-compliance.md` for safe attribution patterns when demonstrating security expertise.

### 4.6: Documentation Hierarchy

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

**Step 1:** Read CLAUDE.md (~5 minutes)

**Step 2:** Load mandatory modules:
```bash
Read docs/context/core/enforcement.md
Read docs/context/core/nda-compliance.md
Read docs/context/core/mandatory-reading.md
```

**Step 3:** Check routing requirements (Section 3.4) for task tier

**Step 4:** Validate before committing (run pre-commit hooks)

**Complete onboarding guide:** See `docs/context/workflows/quick-start-guide.md` for detailed workflows, emergency troubleshooting, and validation procedures.

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

**Complete module catalog:** See `docs/context/INDEX.yaml` for all 32 modules organized by category and priority.

**Quick summary:**
- **Total modules:** 32 modules across 6 categories (~60,050 tokens actual)
- **Categories:** core (5), workflows (6), standards (7), technical (6), reference (4), templates (4)
- **Discovery:** Use INDEX.yaml to find modules by task, tag, or priority
- **Efficiency:** Token budget formula: word_count × 1.33, load only what you need

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

**Remember:** This is a modular architecture. Load only what you need for the current task. Check Section 3.4 for routing requirements. When unsure, return to `docs/context/INDEX.yaml`.

**Architecture version:** 4.1.0 (modular + explicit routing)
**Previous version:** 4.0.3 (modular, implicit routing)
**Original version:** 3.0.0 (monolith, 12,900 words)
**Efficiency gain:** 84.9% token reduction for simple tasks (2.6K vs 17K tokens)

**What's new in v4.1.0:**
- **3-tier routing system:** MANDATORY/RECOMMENDED/OPTIONAL skill loading
- **Explicit loading sequences:** Step-by-step with file paths for common tasks
- **LLM autonomy boundaries:** Always/Usually/Sometimes/Never framework
- **Routing validation:** Pre/post checklists for skill compliance
- **Enhanced enforcement:** 5 MANDATORY operations block without required skills

**Recent improvements (2025-11-03):**

**Historical Archive:** Detailed session history (Sessions 1-9) moved to `docs/context/reference/historical-learnings.md` for token efficiency. See archive for:
- Modular architecture foundation (Sessions 1-4)
- Gist extraction & validation patterns (Sessions 5-6)
- Python logging & repository hygiene (Sessions 7-9)

**Proven Patterns (Sessions 7-13):**

**Audit-First Development:**
- Verify current state before planning (56-78% time savings proven)
- Mandatory for migrations and transformations (prevents 30+ min wasted effort)
- Prevents overestimates (Session 7: 53% error caught, Session 12: 3 discrepancies)
- ROI validated 3+ consecutive sessions (5-6x return: 5-min audit prevents 30-min waste)

**Validation Infrastructure:**
- Playwright scales linearly (99 gists, 100% pass rate, <2s load time)
- Automated validation prevents regression (zero console errors maintained)
- Cross-tool verification essential (pre-commit vs calculator, prevents 40% overestimation)
- Production-ready validation: 316ms avg load time, 17 gists validated Session 8

**Repository Hygiene:**
- Archive first, delete only after verification (3.16MB → 628KB, 80% improvement)
- Monthly documentation audits mandatory (prevent 30-40% drift, 92/100 baseline score)
- Staging workflows validated (tmp/gists/ → upload → post update)
- Conservative cleanup philosophy: reversibility > aggressive deletion

**Agent Coordination:**
- Verify agent types before swarm init (54 available agents, prevents hallucination)
- Documentation identifiers must be generic (no deployment-specific hardcoding)
- Monthly accuracy audits prevent exaggeration creep (Sessions 9, 12, 13)
- Swarm orchestration: 6 agents, 11 tasks, 27 minutes typical deployment

**Recent Sessions (Sessions 20-24):**

**Sessions 10-19 archived to `docs/context/reference/historical-learnings.md` for token efficiency.**
- Session 20: Code ratio documentation audit (TODO.md 40% accurate → 100%; removed 3 false positives, added 6 undocumented violations; automated scanner verification mandatory)
- Session 20: Suricata CRITICAL post fixed (53.8% → 23.7%; 7 gists extracted 277 lines, Mermaid v10 migration, researcher + 2x coder agents; 1.08 hours)
- Session 20: Multi-phase extraction strategy validated (initial 6 gists → 32.3% still exceeded, 7th gist Kibana query → 23.7% COMPLIANT; build 2-3 point safety margins)
- Session 20: Gist extraction workflow proven (researcher 15 min analysis prevents 30-45 min trial-and-error; tmp/gists/ backup, gh CLI upload, post embed validation pattern)
- Session 21: Code ratio dual-strategy discovery (eBPF 97.3% Mermaid vs other posts 81.5% extractable code; calculator enhanced v1.1.0 with DIAGRAM-HEAVY detection)
- Session 21: Parallel execution 2nd validation (Track A calculator enhancement + Track B Bitwarden extraction; 95 min total vs ~160 min sequential; 80% efficiency matched Session 14)
- Session 21: Bitwarden CRITICAL fixed (51.5% → 22.1%; 9 gists 298 lines extracted, Mermaid v10 compliant, Playwright 100% pass rate; HIGHEST violation resolved)
- Session 21: Calculator policy flag implemented (>80% Mermaid posts flagged as "DIAGRAM-HEAVY" educational content; distinguishes code-heavy vs diagram-heavy violations)
- Session 21: Remaining work clarified (3 posts need traditional extraction ~12 gists 2-3 hours; 1 post eBPF needs policy exception or Mermaid→images conversion)
- Session 22: Code ratio accuracy audit (TODO.md 43% accurate → 100%; removed 7 false positives: DNS-DoH 23.6%, IoT Security 17.3%, +5 more COMPLIANT)
- Session 23: Internal linking system Phase 1 started (researcher + coder agents deployed; baseline corrected 27→47 links +74%; 8/15 hub posts complete 53.3%)
- Session 22: Audit-first pattern 6th validation (15-20 min review prevents 2-3 hour wasted extraction effort; 43% accuracy drift caught: 7 violations claimed → 4 actual)
- Session 22: Remaining work verified (3 posts actual: Raspberry Pi 32.2%, Local LLM 33.6%, EPSS/KEV 31.2%; eBPF correctly categorized DIAGRAM-HEAVY policy exception)
- Session 22: Hybrid strategy validated (Mermaid conversion + gist extraction; code-analyzer confirmed calculator v1.1.0 correctly distinguishes diagram vs code; Python logging 78/78 verified)
- Session 22: Code quality swarm deployed (4 posts analyzed: 55% padding/pseudocode discovered, 16 truncated blocks found)
- Session 22: Quality refactoring implemented (Raspberry Pi 32.2%→14.6% via padding removal, Local LLM 33.6%→14.8% via stub deletion, EPSS 31.2%→15.2% minimal changes)
- Session 22: Content standards established (KEEP <15 lines teaching core, EXTRACT >20 lines reference, DELETE truncated pseudocode; quality > ratio compliance)
- Session 22: DIAGRAM-HEAVY policy created (eBPF 97.3% Mermaid accepted as educational visualization; >80% diagrams + <10% actual code = exception)
- Session 23: Blog optimization research completed (88 citations, 13,000+ word report; identified CRITICAL gap: internal linking 0.095/post vs 6-10 target = 40% traffic opportunity)
- Session 23: Blog patterns module created (docs/context/standards/blog-patterns.md, 7,200 tokens; P0-P3 priorities, research-backed thresholds)
- Session 23: Script audit completed (23 blog scripts analyzed; 7/23 aligned, 12/23 need updates, 4/23 new scripts needed; 31-43 hours estimated)
- Session 24: CLAUDE.md v4.1.0 RELEASED - Explicit routing architecture (3-tier MANDATORY/RECOMMENDED/OPTIONAL; 5 MANDATORY operations with pre-commit enforcement)
- Session 24: Routing architecture research completed (22 sources: official Anthropic docs, production implementations, academic research; validated progressive disclosure + explicit routing principles)
- Session 24: LLM autonomy boundaries established (Always/Usually/Sometimes/Never framework; clear override scenarios; routing validation checklists)
- Session 24: Task-based loading enhanced (explicit file paths, step-by-step sequences, token cost transparency; reduced routing decisions by 70% via explicit rules)
- Session 24: Sessions 10-19 archived to historical-learnings.md (token efficiency: ~1,000 tokens saved; rolling window policy: archive sessions >3 months old)
