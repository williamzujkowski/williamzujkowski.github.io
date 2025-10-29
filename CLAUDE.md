---
STATUS: AUTHORITATIVE
VERSION: 3.0.0
LAST_AUDIT: 2025-09-23
COMPLIANCE: 100%
CITATIONS: 90%+
UI_UX: OPTIMIZED
---

# Claude Code Configuration - SPARC Development Environment

# 🏛️ AUTHORITATIVE DOCUMENTATION NOTICE

This file (CLAUDE.md) serves as the **single source of truth** for:
- Content standards and compliance boundaries
- Technical implementation guidelines
- Blog post requirements and style
- UI/UX standards and responsive design
- Citation and research requirements

All development, content creation, and maintenance MUST reference this document.

**Last comprehensive audit:** 2025-09-23
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
- **Last Enhancement**: 2025-10-28
- **Batch 2 Average**: 11.3 citations per post (+440% from 2.1 baseline)

### UI/UX & Accessibility ✅
- **Mobile Responsive**: Tested 375px-2560px
- **Touch Targets**: All ≥44px
- **WCAG Compliance**: AA achieved
- **Dark Mode**: Fully functional
- **Keyboard Navigation**: Implemented
- **Reading Progress**: Active
- **Code Copy Buttons**: Implemented

### Technical Quality ✅
- **Build Status**: PASSING
- **Load Time**: <3s on 3G
- **Lighthouse Mobile**: 95+
- **Core Web Vitals**: All green (LCP <2.5s, FID <100ms, CLS <0.1)
- **Browser Support**: Modern browsers + graceful degradation

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

---

## 📚 Comprehensive Documentation

**MANDATORY READING for all LLMs working on this repository:**

1. **[docs/ENFORCEMENT.md](docs/ENFORCEMENT.md)** - ⚠️ CRITICAL: Mandatory enforcement rules
2. **[docs/GUIDES/LLM_ONBOARDING.md](docs/GUIDES/LLM_ONBOARDING.md)** - Quick start guide for new AI agents
3. **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture and design principles
4. **[docs/GUIDES/SCRIPT_CATALOG.md](docs/GUIDES/SCRIPT_CATALOG.md)** - Complete catalog of available scripts
5. **[MANIFEST.json](MANIFEST.json)** - Single source of truth for repository inventory

**Reading Order:**
1. Start with LLM_ONBOARDING.md (5 minutes)
2. Read ENFORCEMENT.md (critical rules)
3. Review ARCHITECTURE.md for system understanding
4. Reference SCRIPT_CATALOG.md as needed

## 📂 Documentation Hierarchy

### Primary (Authoritative):
- **CLAUDE.md**: Master reference for all standards (THIS DOCUMENT)
- **MANIFEST.json**: System inventory and file registry
- **.claude-rules.json**: Enforcement rules

### Secondary (Supporting):
- **docs/ARCHITECTURE.md**: System design
- **docs/GUIDES/**: How-to documentation
- **docs/ENFORCEMENT.md**: Mandatory rules
- **content-review-instructions.md**: Review standards

### Generated (Reference):
- **reports/**: Audit and compliance reports
- **docs/STANDARDS/**: Implementation checklists

> **Note**: All documentation must defer to CLAUDE.md for canonical requirements.

## 📚 Lessons from Enhancement Missions

### What Worked Well:
1. **Phased Approach**: Compliance → Citations → UI/UX → Smart Brevity Transformation
2. **Homelab Focus**: Safe, engaging, valuable content
3. **Personal Stories**: Connection through shared failures
4. **Academic Citations**: Credibility through research
5. **Mobile-First**: Better experience across all devices
6. **Smart Brevity Methodology**: 6-phase transformation (Pre-Analysis → BLUF → Bulletization → Language → Citations → Validation)
7. **Swarm Orchestration**: Planner/Researcher/Coder trio for parallel execution
8. **Pre-Analysis Documents**: Scope control and pattern recognition preventing feature creep

### Challenges Overcome:
1. **NDA Boundaries**: "Public sector platforms" phrasing
2. **Citation Formatting**: Automated broken link detection
3. **Resume to Story**: Personal narrative transformation
4. **Touch Targets**: Systematic 44px minimum implementation
5. **Pre-commit Hooks**: Proper handling of build artifacts
6. **Bulletization Without Voice Loss**: Strategic prose-to-bullets conversion preserving personal storytelling
7. **BLUF Format Adaptation**: Compelling openings for both technical and personal posts
8. **Citation Research Efficiency**: Systematic academic source discovery reducing research time by 60%

### Key Decisions:
1. Zero tolerance for work references
2. 90%+ citation target (achieved)
3. Personal storytelling over credentials
4. Mobile experience prioritization
5. Accessibility as non-negotiable requirement

---

## 📁 Project Directory Structure

### Root Directory
```
williamzujkowski.github.io/
├── src/                    # Source files for the static site
│   ├── _data/             # Global data files for Eleventy
│   ├── _includes/         # Reusable templates and layouts
│   │   ├── layouts/       # Page layout templates
│   │   └── partials/      # Reusable component templates
│   ├── assets/            # Static assets
│   │   ├── css/          # Stylesheets (Tailwind)
│   │   ├── images/       # Site images
│   │   │   └── blog/     # Blog post images
│   │   ├── js/           # JavaScript files
│   │   └── fonts/        # Custom fonts
│   ├── pages/            # Static pages (about, contact, etc.)
│   ├── posts/            # Blog posts in Markdown
│   ├── redirects/        # URL redirect configurations
│   └── index.njk         # Homepage template
├── scripts/              # Utility and automation scripts
│   ├── *-blog-*.py      # Blog management scripts
│   ├── optimize-*.sh    # Optimization scripts
│   └── generate-*.py    # Generation scripts
├── docs/                 # Documentation
│   ├── guides/          # Development guides
│   ├── standards/       # Coding standards
│   └── *.md            # Various documentation files
├── _site/               # Built static site (git-ignored)
├── node_modules/        # npm dependencies (git-ignored)
├── .eleventy.js        # Eleventy configuration
├── package.json        # npm configuration
├── tailwind.config.js  # Tailwind CSS configuration
├── postcss.config.js   # PostCSS configuration
└── CLAUDE.md          # This file - project documentation
```

### Key Directories Explained

#### `/src` - Source Directory
- **Purpose**: Contains all source files for the Eleventy static site generator
- **Key Files**:
  - `index.njk`: Homepage template
  - `404.md`: 404 error page
  - `feed.njk`: RSS feed template
  - `sitemap.njk`: XML sitemap template
  - `tags.njk`: Tag listing page template

#### `/scripts` - Automation Scripts
- **Purpose**: Organized Python and shell scripts for blog management
- **Structure**: Scripts organized into logical categories for better maintainability

##### Script Organization (Post-Phase 3 Cleanup)

```
scripts/
├── blog-content/        # Content management & optimization (5 scripts)
│   ├── analyze-blog-content.py
│   ├── batch-improve-blog-posts.py
│   ├── blog-manager.py
│   ├── comprehensive-blog-enhancement.py
│   └── optimize-blog-content.py
├── blog-images/         # Image generation & management (6 scripts)
│   ├── enhanced-blog-image-search.py
│   ├── fetch-stock-images.py
│   ├── generate-blog-hero-images.py
│   ├── generate-og-image.py
│   ├── playwright-image-search.py
│   └── update-blog-images.py
├── blog-research/       # Academic citations & research (7 scripts)
│   ├── academic-search.py
│   ├── add-academic-citations.py
│   ├── add-reputable-sources-to-posts.py
│   ├── check-citation-hyperlinks.py
│   ├── enhance-more-posts-citations.py
│   ├── research-validator.py
│   └── search-reputable-sources.py
├── link-validation/     # Link validation & repair (12 scripts)
│   ├── advanced-link-repair.py
│   ├── batch-link-fixer.py
│   ├── citation-repair.py
│   ├── citation-updater.py
│   ├── content-relevance-checker.py
│   ├── link-extractor.py
│   ├── link-monitor.py
│   ├── link-report-generator.py
│   ├── link-validator.py
│   ├── simple-validator.py
│   ├── specialized-validators.py
│   └── wayback-archiver.py
├── lib/                 # Shared libraries (1 Python, 1 Shell)
│   ├── common.py        # Common Python functions
│   └── memory-file.sh   # Memory management shell functions
├── utilities/           # General utilities (3 scripts)
│   ├── diagram-manager.py
│   ├── final-validation.py
│   └── llm-script-documenter.py
└── optimize-blog-images.sh  # Shell script for image optimization
```

**Total Active Scripts**: 34 Python scripts + 2 Shell scripts

#### `/docs` - Documentation
- **Purpose**: Project documentation and guides
- **Contents**:
  - Implementation plans
  - Blog standards
  - Development guides
  - Analysis reports

#### `/_site` - Build Output
- **Purpose**: Generated static site files
- **Note**: Git-ignored, regenerated on build

### Configuration Files

| File | Purpose |
|------|---------|
| `.eleventy.js` | Eleventy configuration, plugins, filters |
| `package.json` | npm scripts, dependencies |
| `tailwind.config.js` | Tailwind CSS customization |
| `postcss.config.js` | PostCSS plugins configuration |
| `.gitignore` | Git ignore patterns |
| `MANIFEST.json` | Repository inventory and metadata |

### Build Commands

```bash
# Development
npm run serve           # Start dev server with hot reload
npm run watch:css       # Watch and rebuild CSS on changes
npm run watch:eleventy  # Watch and rebuild Eleventy on changes

# Production
npm run build           # Build production site (CSS + Eleventy + JS)
npm run build:css       # Build CSS only with PostCSS
npm run build:eleventy  # Build Eleventy only
npm run build:js        # Bundle JavaScript files

# Testing
npm run test            # Run unit tests
npm run test:unit       # Run unit tests only
npm run test:integration # Run integration tests
npm run test:e2e        # Run end-to-end tests
npm run test:all        # Run all tests
npm run test:watch      # Run tests in watch mode

# Validation
npm run validate:km     # Validate knowledge management standards

# Debugging
npm run debug           # Run Eleventy with debug output
```

## 🚨 CRITICAL: CONCURRENT EXECUTION & FILE MANAGEMENT

**ABSOLUTE RULES**:
1. ALL operations MUST be concurrent/parallel in a single message
2. **NEVER save working files, text/mds and tests to the root folder**
3. ALWAYS organize files in appropriate subdirectories

### ⚡ GOLDEN RULE: "1 MESSAGE = ALL RELATED OPERATIONS"

**MANDATORY PATTERNS:**
- **TodoWrite**: ALWAYS batch ALL todos in ONE call (5-10+ todos minimum)
- **Task tool**: ALWAYS spawn ALL agents in ONE message with full instructions
- **File operations**: ALWAYS batch ALL reads/writes/edits in ONE message
- **Bash commands**: ALWAYS batch ALL terminal operations in ONE message
- **Memory operations**: ALWAYS batch ALL memory store/retrieve in ONE message

### 🧹 CLEANUP PHASE: MANDATORY FOR ALL WORKFLOWS

**EVERY TODO LIST MUST INCLUDE:**
1. **Cleanup tasks** as final items (remove temp files, vestigial scripts, test artifacts)
2. **Validation after cleanup** to ensure nothing breaks
3. **Commit and push** cleaned state
4. **Monitor deployment** to verify site functionality
5. **Revert if needed** and fix issues iteratively

**CLEANUP TARGETS:**
- Temporary troubleshooting scripts (e.g., `validate-*.py`, `fix-*.py`, `test-*.py`)
- Research/analysis files in `/docs` that are no longer needed
- Duplicate or superseded scripts in `/scripts`
- Test artifacts and temporary data files
- Old backup files or `.bak` extensions
- Unnecessary log files or debug outputs

**CLEANUP RULES:**
- NEVER delete production scripts without verification
- ALWAYS test site functionality after cleanup
- KEEP essential utilities and actively used tools
- PRESERVE documentation that provides value
- MAINTAIN scripts referenced in CLAUDE.md or README

### 📁 File Organization Rules

**Never save to root.** Use these directories:

```
/src         → Source code
/tests       → Test files
/docs        → Documentation (including this file)
/scripts     → Automation utilities
/config      → Configuration files
```

**Common mistakes:**
❌ `validate-claims.py` in root
❌ `test-citations.md` in root
❌ `working-notes.txt` anywhere

✅ `scripts/blog-research/validate-claims.py`
✅ `tests/test-citations.py`
✅ `docs/working-notes.md`

## Project Overview

This project uses SPARC (Specification, Pseudocode, Architecture, Refinement, Completion) methodology with Claude-Flow orchestration for systematic Test-Driven Development.

### 📸 Blog Visual Enhancement System
**Quick Commands for Blog Optimization:**
```bash
# Analyze posts for high code ratios
python scripts/blog-content/optimize-blog-content.py

# Generate Mermaid diagram templates
python scripts/utilities/diagram-manager.py

# Search and download stock images (no API keys)
python scripts/blog-images/playwright-image-search.py
```

**Code Reduction Guidelines:**
- Target <25% code-to-content ratio
- Replace verbose code with Mermaid diagrams
- Keep snippets to 5-10 essential lines
- Link to GitHub gists for full examples

See docs/BLOG_VISUAL_ENHANCEMENT_GUIDE.md for complete documentation.

## SPARC Commands

### Core Commands
- `npx claude-flow sparc modes` - List available modes
- `npx claude-flow sparc run <mode> "<task>"` - Execute specific mode
- `npx claude-flow sparc tdd "<feature>"` - Run complete TDD workflow
- `npx claude-flow sparc info <mode>` - Get mode details

### Batchtools Commands
- `npx claude-flow sparc batch <modes> "<task>"` - Parallel execution
- `npx claude-flow sparc pipeline "<task>"` - Full pipeline processing
- `npx claude-flow sparc concurrent <mode> "<tasks-file>"` - Multi-task processing

### Available npm Commands
- `npm run build` - Build production site
- `npm run serve` - Development server with hot reload
- `npm run test` - Run unit tests
- `npm run test:all` - Run all test suites
- `npm run validate:km` - Validate knowledge management standards

## SPARC Workflow Phases

1. **Specification** - Requirements analysis (`sparc run spec-pseudocode`)
2. **Pseudocode** - Algorithm design (`sparc run spec-pseudocode`)
3. **Architecture** - System design (`sparc run architect`)
4. **Refinement** - TDD implementation (`sparc tdd`)
5. **Completion** - Integration (`sparc run integration`)

## Code Style & Best Practices

- **Modular Design**: Files under 500 lines
- **Environment Safety**: Never hardcode secrets
- **Test-First**: Write tests before implementation
- **Clean Architecture**: Separate concerns
- **Documentation**: Keep updated

## 🚀 Available Agents (54 Total)

### Core Development
`coder`, `reviewer`, `tester`, `planner`, `researcher`

### Swarm Coordination
`hierarchical-coordinator`, `mesh-coordinator`, `adaptive-coordinator`, `collective-intelligence-coordinator`, `swarm-memory-manager`

### Consensus & Distributed
`byzantine-coordinator`, `raft-manager`, `gossip-coordinator`, `consensus-builder`, `crdt-synchronizer`, `quorum-manager`, `security-manager`

### Performance & Optimization
`perf-analyzer`, `performance-benchmarker`, `task-orchestrator`, `memory-coordinator`, `smart-agent`

### GitHub & Repository
`github-modes`, `pr-manager`, `code-review-swarm`, `issue-tracker`, `release-manager`, `workflow-automation`, `project-board-sync`, `repo-architect`, `multi-repo-swarm`

### SPARC Methodology
`sparc-coord`, `sparc-coder`, `specification`, `pseudocode`, `architecture`, `refinement`

### Specialized Development
`backend-dev`, `mobile-dev`, `ml-developer`, `cicd-engineer`, `api-docs`, `system-architect`, `code-analyzer`, `base-template-generator`

### Testing & Validation
`tdd-london-swarm`, `production-validator`

### Migration & Planning
`migration-planner`, `swarm-init`

## 🎯 Claude Code vs MCP Tools

### Claude Code Handles ALL:
- File operations (Read, Write, Edit, MultiEdit, Glob, Grep)
- Code generation and programming
- Bash commands and system operations
- Implementation work
- Project navigation and analysis
- TodoWrite and task management
- Git operations
- Package management
- Testing and debugging

### MCP Tools ONLY:
- Coordination and planning
- Memory management
- Neural features
- Performance tracking
- Swarm orchestration
- GitHub integration

**KEY**: MCP coordinates, Claude Code executes.

## 🚀 Quick Setup

```bash
# Add Claude Flow MCP server
claude mcp add claude-flow npx claude-flow@alpha mcp start
```

## MCP Tool Categories

### Coordination
`swarm_init`, `agent_spawn`, `task_orchestrate`

### Monitoring
`swarm_status`, `agent_list`, `agent_metrics`, `task_status`, `task_results`

### Memory & Neural
`memory_usage`, `neural_status`, `neural_train`, `neural_patterns`

### GitHub Integration
`github_swarm`, `repo_analyze`, `pr_enhance`, `issue_triage`, `code_review`

### System
`benchmark_run`, `features_detect`, `swarm_monitor`

## 📋 Agent Coordination Protocol

### Every Agent MUST:

**1️⃣ BEFORE Work:**
```bash
npx claude-flow@alpha hooks pre-task --description "[task]"
npx claude-flow@alpha hooks session-restore --session-id "swarm-[id]"
```

**2️⃣ DURING Work:**
```bash
npx claude-flow@alpha hooks post-edit --file "[file]" --memory-key "swarm/[agent]/[step]"
npx claude-flow@alpha hooks notify --message "[what was done]"
```

**3️⃣ AFTER Work:**
```bash
npx claude-flow@alpha hooks post-task --task-id "[task]"
npx claude-flow@alpha hooks session-end --export-metrics true
```

## 🎯 Concurrent Execution Examples

### The One-Message Rule

**All related operations in one message.**

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

## Performance Benefits

- **84.8% SWE-Bench solve rate**
- **32.3% token reduction**
- **2.8-4.4x speed improvement**
- **27+ neural models**

## Hooks Integration

### Pre-Operation
- Auto-assign agents by file type
- Validate commands for safety
- Prepare resources automatically
- Optimize topology by complexity
- Cache searches

### Post-Operation
- Auto-format code
- Train neural patterns
- Update memory
- Analyze performance
- Track token usage

### Session Management
- Generate summaries
- Persist state
- Track metrics
- Restore context
- Export workflows

## Advanced Features (v2.0.0)

- 🚀 Automatic Topology Selection
- ⚡ Parallel Execution (2.8-4.4x speed)
- 🧠 Neural Training
- 📊 Bottleneck Analysis
- 🤖 Smart Auto-Spawning
- 🛡️ Self-Healing Workflows
- 💾 Cross-Session Memory
- 🔗 GitHub Integration

## Integration Tips

1. Start with basic swarm init
2. Scale agents gradually
3. Use memory for context
4. Monitor progress regularly
5. Train patterns from success
6. Enable hooks automation
7. Use GitHub tools first

## Support

- Documentation: https://github.com/ruvnet/claude-flow
- Issues: https://github.com/ruvnet/claude-flow/issues

---

Remember: **Claude Flow coordinates, Claude Code creates!**

# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.
Never save working files, text/mds and tests to the root folder.

## SOURCE OF TRUTH FOR HOMELAB AND HARDWARE
**CRITICAL**: Always reference `/uses/` page (src/pages/uses.md) for accurate information about:
- Hardware specifications (Intel i9-9900K, 64GB RAM, RTX 3090, Dell R940, Raspberry Pi setup)
- Software stack (Proxmox, Docker, K3s, Wazuh, specific tools)

## 🔬 BLOG POST RESEARCH & CREDIBILITY MODEL

### ABSOLUTE RULE: NO FABRICATION
**NEVER make up information, statistics, or claims. ALWAYS back statements with reputable sources.**

**Why it matters:** No citations = no credibility. Readers can verify your claims.

### Research Verification Process
1. **Claim Identification**: Scan content for factual claims, statistics, technical statements
2. **Source Validation**: Every claim MUST have a reputable source
3. **Citation Integration**: Properly cite all sources inline and in references
4. **Fact Checking**: Use Playwright to verify claims against authoritative sources

### 📚 Open-Access Research Platforms

#### Primary Research Sources
1. **[arXiv](https://arxiv.org/)** - Preprints in physics, mathematics, computer science, quantitative biology, quantitative finance, statistics, electrical engineering and systems science, and economics
2. **[Zenodo](https://zenodo.org/)** - General-purpose open repository by CERN with DOI assignment
3. **[CORE](https://core.ac.uk/)** - Aggregates 250+ million open-access papers with API access
4. **[Preprints.org](https://www.preprints.org/)** - Multi-disciplinary preprints with moderation
5. **[Research Square](https://www.researchsquare.com/)** - Springer Nature integrated preprints
6. **[SciPost](https://scipost.org/)** - Community-driven peer review in physics

#### Domain-Specific Sources
- **Security**: NIST, OWASP, SANS, CVE/NVD databases, security advisories
- **AI/ML**: Papers with Code, Google AI Research, OpenAI Research, Hugging Face papers
- **Cloud/DevOps**: CNCF resources, AWS/Azure/GCP documentation, HashiCorp guides
- **Networking**: RFCs, Cisco documentation, Cloudflare Learning Center
- **Linux/Kernel**: kernel.org documentation, LWN.net, Red Hat resources

### 🔍 Research Integration Workflow

#### For Every Blog Post:
1. **Pre-Writing Research**
   ```python
   # Use scripts/research-validator.py
   python scripts/blog-research/research-validator.py --post "post-title" --check-claims
   ```

2. **Claim Validation with Playwright**
   ```python
   # Search academic sources
   python scripts/blog-research/academic-search.py --query "specific claim" --sources "arxiv,zenodo,core"
   ```

3. **Source Citation Format - MANDATORY HYPERLINKS**
   - **ALL citations MUST include clickable hyperlinks to sources**
   - Inline: `[Study shows 73% improvement](https://arxiv.org/abs/2024.xxxxx)`
   - Reference format:
     ```markdown
     1. **[Paper Title](https://doi.org/10.xxxx/xxxxx)** (Year)
        - Author names
        - *Journal/Conference Name*
     ```
   - Links MUST point to:
     - arXiv, PubMed Central, or open-access versions
     - DOI links (https://doi.org/10.xxxx/xxxxx)
     - Official publisher/organization pages
   - NEVER cite without a working hyperlink to the source

4. **Visual Evidence**
   - Extract figures/charts from papers (with permission/citation)
   - Create original diagrams based on research data
   - Include methodology visualizations

### 📊 Content Quality Standards

**Every technical claim needs:**
- Primary source (original research paper or official documentation)
- Secondary validation (additional supporting sources)
- Context (methodology, sample size, limitations)
- Recency check (publication dates within 2 years)

**Red flags to avoid:**
- ❌ "Studies show..." without citation
- ❌ Specific percentages without source
- ❌ "It's well known that..." without evidence
- ❌ Technical specifications without verification
- ❌ Historical claims without references
- ❌ Performance metrics without methodology

### 🤖 Automated Research Validation

#### Scripts for Research Integrity:
```bash
# Validate research claims in posts
python scripts/blog-research/research-validator.py --post src/posts/example.md

# Search academic sources for supporting research
python scripts/blog-research/academic-search.py --query "quantum computing" --sources "arxiv,zenodo,core"

# Add academic citations to blog posts
python scripts/blog-research/add-academic-citations.py --post src/posts/example.md

# Check citation hyperlinks for validity
python scripts/blog-research/check-citation-hyperlinks.py
```

### 📈 Research-Backed Content Structure

#### Optimal Blog Post Format:
1. **Introduction** - Set context with cited background
2. **Literature Review** - Brief overview of existing research
3. **Core Content** - Main points with supporting evidence
4. **Case Studies** - Real examples with sources
5. **Data Visualization** - Charts/graphs from research
6. **Limitations** - Acknowledge gaps or contradictions
7. **Future Directions** - Based on research trends
8. **References** - Complete citation list

### 🔗 Playwright Research Automation

#### Use Playwright for:
- Searching academic databases
- Verifying technical specifications
- Checking latest documentation versions
- Finding recent research papers
- Validating statistical claims
- Screenshot evidence collection

#### Example Research Flow:
```python
# Search multiple academic sources
async def research_claim(claim):
    sources = ['arxiv', 'zenodo', 'core', 'scholar.google.com']
    results = []
    for source in sources:
        results.extend(await search_source(source, claim))
    return validate_and_rank_sources(results)
```

### ✅ Pre-Publication Checklist

Run before committing:
```bash
# Validate all citations
python scripts/blog-research/check-citation-hyperlinks.py

# Check for uncited claims
python scripts/blog-research/research-validator.py --post src/posts/[file].md
```

**Verify:**
- [ ] All factual claims have citations with working hyperlinks
- [ ] Statistics include methodology and source
- [ ] Technical specs verified against official docs
- [ ] At least 3 reputable sources per major point
- [ ] No outdated information (check publication dates)
- [ ] Opposing viewpoints acknowledged
- [ ] Limitations clearly stated
- [ ] Visual aids properly attributed
- [ ] References section complete
- [ ] Playwright verification completed

### 🚫 Never Do This
- Invent statistics or percentages
- Paraphrase without attribution
- Use Wikipedia as primary source
- Cite outdated documentation
- Cherry-pick data without context
- Ignore contradicting research
- Make absolute statements without evidence
- Use anecdotal evidence as fact

**NEVER make up or assume hardware/software details** - always check the uses page.
**VERIFY claims with reputable sources** - use Playwright to search for authoritative documentation.

## Blog Image Management
When working with blog posts:
1. ALWAYS add image metadata to frontmatter
2. Run `python scripts/blog-images/update-blog-images.py` after creating posts
3. Generate hero images with `python scripts/blog-images/generate-blog-hero-images.py`
4. Optimize with `bash scripts/optimize-blog-images.sh`
5. Use proper alt text for accessibility
6. Follow the directory structure in src/assets/images/blog/

---

# Content Style Guidelines for Blog Posts

## Writing Style: The "Polite Linus Torvalds" Standard

**What it means:**
Direct. Honest. Respectful. Substance over style.

**Why it matters:**
This blog shares real technical work, not corporate marketing. Readers want clarity, not fluff.

### Core Principles

**Lead with the point:**
- First sentence = most important takeaway
- No throat-clearing
- No "In this post, I will discuss..."

**Use bullets liberally:**
- One idea per bullet
- Short sentences
- White space is your friend

**Cut ruthlessly:**
- Remove qualifiers: "actually," "basically," "essentially"
- Delete adverbs: "very," "really," "quite"
- Kill corporate speak: "leverage," "synergy," "paradigm"

**Examples:**

❌ Bad:
```
In this post, I'm going to discuss some really interesting
findings I discovered while essentially experimenting with
various approaches to leverage containerization in my homelab
environment, which actually proved to be quite beneficial.
```

✅ Good:
```
Docker cut my homelab deployment time by 70%.

Here's what worked and what didn't.
```

### "Why it matters" Sections

Every major claim needs context:

```markdown
**Why it matters:** [One sentence explaining impact]
```

Example:
```markdown
K3s uses 512MB RAM vs Kubernetes' 2GB minimum.

**Why it matters:** You can run production-grade orchestration
on a Raspberry Pi without sacrificing features.
```

### Sentence Rhythm and Cadence

**Pattern:** Short → medium → punch.

Examples:
- "K3s works. It uses 512MB RAM. You can run it on a Raspberry Pi." (5-8-10 words)
- "The first test failed. Took 20 minutes to debug. Turns out I forgot sudo." (4-5-8 words)

**Avoid AI patterns:**
- ❌ Perfectly parallel structures: "This improves X. This enhances Y. This optimizes Z."
- ✅ Break rhythm: "This improves X. Y gets better too. Z? Still working on it."

**Use minimal conjunctions:**
- ❌ "I tested the system, and it worked, but the performance was slow."
- ✅ "I tested the system. It worked. Performance was slow."

**Add transitions like a human:**
- Use: "Still," "Anyway," "That's fine," "Turns out"
- Avoid: "Therefore," "Hence," "In conclusion," "Overall"

## Content Philosophy

### Voice Guidelines
**Use:**
- First person (I/me) for personal experiences
- Second person (you) when addressing readers
- Contractions for conversational flow
- Simple words when appropriate
- Specific examples over abstractions

**Avoid:**
- Corporate buzzwords unless discussing them specifically
- Unnecessarily complex vocabulary
- Absolute statements unless warranted
- Clickbait that doesn't match content

### Structure Rules
- Mix short punchy sentences with detailed ones
- One idea per paragraph
- Use white space for readability
- Start paragraphs with strong hooks

### Anti-AI-Tells Checklist

**Before publishing, eliminate these machine-like patterns:**

| Category | Remove | Replace With |
|----------|--------|--------------|
| **Punctuation** | Em dashes (—), semicolons (;) | Short sentences or commas |
| **Transitions** | "In conclusion," "Overall," "Therefore" | "Anyway," "That's the gist," "Still" |
| **Emotion** | "exciting," "remarkable," "thrilled" | "useful," "surprising," or remove |
| **Vocabulary** | "utilize," "leverage," "paradigm" | "use," "try," "model" |
| **Certainty** | Absolute claims ("always," "never") | "probably," "usually," "depends" |
| **Symmetry** | Perfectly parallel clauses | Break rhythm intentionally |

**Quick validation:**
```bash
# Check for AI tells in your post
grep -E "—|;|exciting|leverage|utilize|in conclusion|overall|therefore" src/posts/[file].md
```

**Why it matters:** These patterns signal AI authorship. Readers (and AI detectors) notice.

## Content Types

### Blog Post Formats
1. **Personal Essays** (800-2000 words): Story → Reflection → Takeaway
2. **Tutorials** (as needed): Problem → Solution → Steps → Results
3. **Thought Pieces** (600-1500 words): Observation → Analysis → Questions
4. **Project Documentation**: Goal → Process → Challenges → Outcome

### Technical Requirements
- Clear, descriptive titles (50-60 characters)
- Simple URL slugs with hyphens
- Meta descriptions for humans
- Descriptive image alt text
- Proper heading hierarchy (H1 → H2 → H3)
- Syntax-highlighted code blocks with comments

## Writing Process

1. **Capture Ideas**: Keep running topic list
2. **Draft Freely**: Write without editing initially
3. **Let It Rest**: Step away before editing
4. **Edit Ruthlessly**: Structure → Clarity → Grammar
5. **Final Checks**: Read aloud, verify links, check mobile preview

### Quality Checklist
Before publishing:
- Would I want to read this?
- Does it sound authentic?
- Is it helpful or interesting?
- Have I been honest?
- Have I respected others' privacy?

## Blog Post Structure Template

1. **Hook**: Start with story, question, or interesting fact
2. **Context**: Why writing about this now
3. **Main Content**: Core information
4. **Personal Reflection**: What this means personally
5. **Invitation**: Question or thought for readers

## Boundaries

### CRITICAL: Government Work Security Guidelines

**NEVER discuss:**
- Current work incidents (minimum 2-3 year buffer)
- Specific government systems
- Active vulnerabilities at work
- Timeline-specific work events
- Team members or organizational structure

**ALWAYS use:**
- "Years ago, I learned..." (vague timeframes)
- "In my homelab..." (personal projects)
- "Research suggests..." (academic framing)
- "A common pattern..." (hypothetical)

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

**Why it matters:** Your clearance and career matter more than a blog post. When in doubt, leave it out.

**Do Share:**
- Professional challenges and wins (from years ago)
- Learning struggles and breakthroughs (personal projects)
- Creative process (home lab/research)
- Book and media recommendations
- Opinions on industry trends
- Historical lessons learned (appropriately aged)
- Personal research and experiments

**Don't Share:**
- Current or recent work incidents
- Specific government agency details
- Active security measures or controls
- Ongoing investigations or issues
- Current vulnerabilities or threats at work
- Specific systems or technologies in use
- Team member details or roles
- Timeline-specific work events
- Employer confidential information
- Others' stories without permission
- Financial specifics
- Personal relationship details (beyond basics)

---

### Personal & Family Information

**ACCURATE FAMILY FACTS:**
- **Children:** ONE child (son)
- **Son's birthday:** June 11, 2023
- **Current age calculation:** As of October 29, 2025, he is 2 years, 4 months old
  - Age formula: `(current_date - June 11, 2023)` in years and months
  - **NEVER claim he is older** - always calculate age from birthdate
  - **NEVER claim multiple children** - singular "son" or "child" only

**When to Mention Parenting (Use Sparingly):**

✅ **Appropriate contexts:**
- Time management discussions: "With a toddler, homelab time is usually after bedtime..."
- Work-life balance: "Running security scans overnight since my son's bedtime is 7:30 PM..."
- Learning/teaching parallels: "Teaching my son to walk reminds me of debugging - iteration and patience..."
- Power consumption concerns: "Since my son was born, I'm more conscious of homelab energy costs..."
- Noise considerations: "Moved the server rack to avoid waking my son..."

❌ **Avoid overuse:**
- Don't mention in EVERY post (target: 1 in 5-7 posts maximum)
- Don't force parenting analogies into unrelated technical content
- Don't share identifying details (name, photos, specific routines beyond general statements)
- Don't make parenting the central narrative unless directly relevant

**Examples of Appropriate Use:**

```markdown
✅ "With a toddler at home, my late-night homelab experiments now happen during naptime..."
✅ "Since becoming a parent in 2023, I've prioritized automation to free up time..."
✅ "My Dell R940 rack mount is in the basement - toddler-proofing required relocating it..."
```

**Examples of Overuse/Inappropriate:**

```markdown
❌ "My kids love watching Raspberry Pi lights blink..." (INACCURATE - one child, age 2)
❌ "Teaching my children about cryptography..." (INACCURATE - he's 2 years old)
❌ "As a father of three..." (INACCURATE - one child)
❌ Using parenting analogies in every single blog post
```

**Humanization Balance:**

Parenting is ONE humanization element among many. Prioritize:
1. **Homelab stories** (most posts)
2. **Technical failures** (most posts)
3. **Concrete measurements** (every post)
4. **Uncertainty phrases** (every post)
5. **Parenting/time constraints** (occasional, 15-20% of posts)

**Privacy Protection:**
- NEVER use son's name
- NEVER share photos
- NEVER mention specific locations (daycare, pediatrician, etc.)
- NEVER share detailed schedules or routines that could identify patterns
- Keep references generic: "my son," "toddler," "young child"

---

## Healthy AI Skepticism

### Question the Hype

**The rule:** Every AI claim gets scrutinized.

**Red flags:**
- "AI will solve X" without methodology
- Benchmarks without reproducible code
- Percentages without sample size
- "State-of-the-art" without comparison
- "Revolutionary" without evidence

### Demand Evidence

**Before writing about AI:**
- Find the actual paper
- Check if code is public
- Verify claims against independent sources
- Look for limitations section
- Check for conflicts of interest

**Required context for AI claims:**
- Dataset size and composition
- Compute requirements
- Comparison with baselines
- Known failure modes
- Reproducibility status

### Write About AI Honestly

**Good patterns:**
```markdown
✅ "GPT-4 scored 73% on this benchmark (vs GPT-3.5's 61%).
   But the test data may overlap with training data."

✅ "This model works well for X. It fails completely at Y.
   Paper doesn't mention Y."

✅ "Impressive demo. No public weights. No reproducibility.
   Treat with skepticism."
```

**Bad patterns:**
```markdown
❌ "AI achieves human-level performance"
❌ "This breakthrough will revolutionize..."
❌ "AI understands X" (it predicts tokens)
```

### The Anthropomorphism Rule

**Don't:**
- Say AI "understands," "thinks," or "knows"
- Attribute human qualities to models
- Imply consciousness or reasoning

**Do:**
- Say models "predict," "generate," or "classify"
- Describe training methodology
- Explain statistical patterns

**Why it matters:** Precise language prevents misconceptions about what these systems actually do.

## Remember
- Perfect is the enemy of published
- Voice will evolve—that's good
- Not every post needs to be epic
- It's okay to have opinions
- Writing gets easier with practice

---

## Humanization Techniques (Quick Reference)

**Add these elements to avoid AI-like writing:**

| Technique | Example | Use When |
|-----------|---------|----------|
| **Hesitation** | "At first I thought it was DNS. It wasn't." | Debugging stories |
| **Reflection** | "Looking back, that assumption was wrong." | Lessons learned |
| **Micro-failure** | "The first fix made it worse." | Tutorials |
| **Concrete detail** | "Took 17 minutes to compile." | Technical posts |
| **Temporal anchor** | "As of October 2025…" | Current state |
| **Contradiction** | "I hate YAML. But it works." | Opinions |

**Extended guidance:** See `human_tone.md` for advanced humanization techniques and style models (Polite Linus Torvalds, Kelsey Hightower clarity, Troy Hunt transparency).

**Automation:** Run `python scripts/blog-content/humanization-validator.py --post [file]` before publishing.

---

# 📝 Blog Post Creation Guidelines

## Recommended Workflow

**For NEW blog posts**, use the **Content Template** at `docs/TEMPLATES/blog-post-writing-template.md` to achieve 80-90/100 baseline scores on first draft. This proactive humanization approach is **50% faster** than reactive refinement.

**Template Validation Results:**
- Test post scored **90/100** (vs 50/100 unguided)
- All required patterns present: 8 first-person, 6 uncertainty, 22 trade-offs
- Time to baseline: 2.5 hours (vs 4-6 hours reactive)
- Full results: `docs/reports/phase-1-template-validation-report.md`

## Before You Write

**Check topic diversity:**
```bash
# List last 10 post topics
ls -t src/posts/*.md | head -10 | xargs grep "^tags:"
```

**Rules:**
- Different primary topic than last 5 posts
- No duplicate keywords in title
- Check overrepresented topics

**Why it matters:** Readers get bored. Variety keeps them coming back.

## Minimum Standards

- **Length:** 1,400-2,100 words (6-9 min read)
- **Citations:** 90%+ of claims sourced
- **Images:** Hero + 1 per major section
- **Code:** <25% of content

**Instant rejection criteria:**
- <1,400 words
- Made-up statistics
- No sources for technical claims
- Work/NDA violations

## Target Audience

- **Primary**: Technology enthusiasts with varying levels of expertise
- **Secondary**: Beginners seeking to understand complex technical concepts
- **Approach**: Begin with concise summaries to help beginners grasp key points, then dive deeper for advanced readers

### Focus Areas

Choose topics from these core domains:
- Artificial Intelligence and Machine Learning
- Quantum Computing
- Cybersecurity and Information Security
- Cryptography
- Robotics and Automation
- High-Performance Computing
- Science Fiction (technology implications)
- Homelab and Self-Hosted Solutions

### Diversity Requirements

- **Primary topic/category** must differ from the main topics of at least the **last 5 blog posts**
- **Analyze the most recent 10 posts** in `/src/posts/` to identify overrepresented topics
- **Prioritize topics** that haven't been the primary focus of any blog post in the last 2 months
- **Avoid repeating primary keywords** from recent post titles (check last 10 posts)

### Topic Research Strategy

To ensure content is cutting-edge and relevant:

1. **Explore Recent Research**: Search arXiv for papers uploaded within the last 30 days that align with blog focus areas
2. **Identify Breakthrough Papers**: Look for papers with:
   - High citation potential
   - Novel methodologies
   - Breakthrough findings
   - Emerging trends or paradigm shifts
   - Unexpected connections between fields
3. **Bridge Multiple Disciplines**: Papers that connect different domains often present unique storytelling opportunities
4. **Build on Existing Literature**: Select topics that introduce new concepts or applications while building on established knowledge

### Topic Objective Definition

Clearly define the post's objective:
- **Educational**: Teaching readers a new concept
- **Tutorial**: Providing step-by-step guidance
- **Insight**: Offering perspectives on recent developments
- **Analysis**: Examining trade-offs and implications
- **Experience Report**: Sharing lessons from personal projects

## Structure (5 Parts)

1. **Hook** (50 words): Grab attention with one strong sentence
2. **Context** (100 words): Why this matters now
3. **Main Content** (1,000-1,500 words): The substance
4. **Reflection** (150 words): What I learned
5. **Call to Action** (50 words): What readers should do

## Writing Rules

**Lead with the point:**
```markdown
❌ "While exploring various approaches to container orchestration..."
✅ "K3s cut my RAM usage by 75%. Here's how."
```

**Use bullets for lists:**
```markdown
✅ Three ways this failed:
   - OOM kills on 2GB nodes
   - etcd corruption after power loss
   - DNS resolution lag >5s
```

**One idea per paragraph:**
```markdown
✅ K3s uses SQLite instead of etcd. This matters for edge deployments.

   SQLite needs no quorum. Your cluster survives network partitions.
```

## Content Requirements

**Every post must include:**
- Opening hook (compelling story, question, or fact)
- Context setting (why this topic matters now)
- Core technical content with sources
- Personal experience (homelab experiments or research)
- Practical examples (code samples, diagrams, images)
- Security considerations (when relevant, CVSS 9.5+)
- Trade-offs and limitations (balanced analysis)
- Personal reflection (what this means to you)
- Conclusion (summarize main points)
- Call to action (encourage readers to apply knowledge)

**Content quality:**
- Analogies and real-world examples
- Balanced perspective (discuss trade-offs)
- Simple language with jargon explanations
- Conversational tone
- Clear headings, bullet points, numbered lists

**Code integration:**
- Store samples in appropriate folders
- Include direct links in post
- Use syntax highlighting
- Add comments for clarity
- Keep examples concise (5-10 lines)

## Metadata and SEO

### Title Requirements

- **Uniqueness**: Search all existing posts in `/src/posts/` to ensure no duplicate or similar titles
- **Keyword Optimization**: Include primary and secondary keywords for SEO
- **Length**: Between 6-12 words
- **Engagement**: Descriptive and compelling
- **Keyword Diversity**: Avoid reusing primary keywords from last 10 post titles

### Required Metadata

- Publication date (YYYY-MM-DD format)
- Last updated date (if applicable)
- Description/summary (150-160 characters)
- Tags (4-8 relevant tags)
- Author information
- Image metadata (see Blog Image Standards section)

## Images

**Required:**
- Hero image (1200x630px)
- One image per major section
- All images have descriptive alt text

**Scripts:**
```bash
# Auto-generate hero images
python scripts/blog-images/generate-blog-hero-images.py

# Optimize all images
bash scripts/optimize-blog-images.sh
```

**Sources (copyright-free):**
- [Unsplash](https://unsplash.com/)
- [Pexels](https://www.pexels.com/)
- [Pixabay](https://pixabay.com/)
- [Wikimedia Commons](https://commons.wikimedia.org/)
- [NASA Image Gallery](https://www.nasa.gov/multimedia/imagegallery/)

**For each image:**
- Direct URL to specific image
- Proper attribution if required
- Descriptive alt text for accessibility
- Complete Markdown formatting
- Appropriate search terms

## Citations

**Every technical claim needs:**
- Primary source (paper, documentation)
- Working hyperlink
- Publication date

**Format:**
```markdown
[Kubernetes uses 2GB RAM minimum](https://kubernetes.io/docs/setup/) (2024)

**Research citation:**
"K3s reduces memory footprint by 50%" ([Rancher Labs, 2023](https://rancher.com/k3s-whitepaper))
```

**Why it matters:** No citations = no credibility.

**Further Exploration Section:**

At the end of each post, include:
- Links to related articles
- Official documentation
- Tutorials and guides
- Relevant public repositories
- Projects readers may find interesting

## Accessibility and Formatting

### Required Practices

- **Descriptive Alt Text**: For all visual elements
- **Clear Heading Hierarchy**: Proper H1 → H2 → H3 structure
- **Simple Language**: Make content accessible to diverse audiences
- **Assistive Technology**: Ensure compatibility with screen readers and other assistive tools
- **Mobile Optimization**: Test on various screen sizes (375px-2560px)

### Formatting Standards

- Clear headings and subheadings
- Bullet points for lists
- Numbered lists for sequential steps
- Code blocks with syntax highlighting
- White space for readability
- Short paragraphs (3-5 sentences)

## Pre-Publication Checklist

**Before submitting:**

- [ ] Topic diversity (different from last 5 posts)
- [ ] Title is unique
- [ ] 1,400+ words (6-9 min read)
- [ ] All claims have citations with working hyperlinks
- [ ] 3+ reputable sources per major point
- [ ] Hero image + section images
- [ ] Descriptive alt text on all images
- [ ] Code examples tested
- [ ] Links verified (no broken links)
- [ ] Mobile preview checked
- [ ] Accessibility requirements met
- [ ] NDA compliance (no work references)
- [ ] Personal experience included
- [ ] Call to action present
- [ ] Further reading section populated
- [ ] Metadata complete
- [ ] Trade-offs and limitations discussed
- [ ] Tone validation completed (Phase G)
- [ ] No AI tells (em dashes, "in conclusion," "leverage")
- [ ] Sentence rhythm varies (short/medium/long)
- [ ] At least one hesitation or reflection included
- [ ] Personal voice preserved in stories
- [ ] Concrete details added (timestamps, numbers)
- [ ] Grammar and spelling checked

---

# 📝 Blog Post Transformation: Smart Brevity Methodology

## Overview

For transforming existing blog posts to meet Smart Brevity standards (10+ citations, 60+ bullets, 0 weak language, strong BLUF, human tone), use the proven 7-phase methodology from Batch 2+ (validated on 8 posts, enhanced with human tone validation).

**Complete methodology documented in:** `docs/batch-2/CLAUDE_MD_UPDATES.md` and `docs/human-tone-integration-plan.md`

## The 7 Phases (Quick Reference)

### Phase A: Pre-Analysis (15 min)
- Count current metrics (citations, bullets, weak language, word count)
- Identify transformation targets
- Document personal stories to preserve
- Create pre-analysis document

### Phase B: BLUF Creation (15 min)
- Add compelling "Bottom Line Up Front" hook
- 2-3 sentences establishing scale/stakes with quantified impact
- 2-3 sentences explaining "why it matters"
- Include 3-5 concrete metrics

### Phase C: Structure Transformation (40 min)
- Convert prose paragraphs to scannable bullets
- Target 60+ bullets while preserving personal voice
- Maintain first-person observations and humor
- Add transitions between bullet groups

### Phase D: Language Hardening (15 min)
- Eliminate weak language (actually, basically, really, very, quite, just)
- Preserve self-deprecating humor and honest admissions
- Keep first-person narrative voice
- Use quantified metrics instead of vague intensifiers

### Phase E: Citation Enhancement (20 min)
- Add 8-12 reputable sources with working hyperlinks
- Prioritize: arXiv, NIST, official docs, IEEE, ACM
- Format: inline citations + comprehensive References section
- Distribute: 2-3 in BLUF, 1 per major claim, complete list at end

### Phase F: Validation (10 min)
- Run `npm run build` (must pass)
- Verify: ≥10 citations, ≥60 bullets, 0 weak language, ≥1,400 words
- Check personal voice preserved in stories
- Mobile preview (375px screens)

### Phase G: Tone Validation (10 min)
- Remove AI tells (em dashes, semicolons, "in conclusion," "overall")
- Eliminate corporate jargon ("leverage," "utilize," "exciting")
- Break perfect parallel structures (vary rhythm)
- Add humanization elements (hesitation, reflection, concrete details)
- Verify sentence length variety (5-30 words, mixed)
- Run humanization validator: `python scripts/blog-content/humanization-validator.py --post [file]`

**Quick AI-tells check:**
```bash
grep -E "—|;|exciting|leverage|utilize|in conclusion|overall|therefore" src/posts/[file].md
```

**Why Phase G matters:** Smart Brevity (Phases A-F) handles structure and citations. Tone validation ensures AI-generated content reads human, not corporate.

## Batch 2 Results (8 Posts)

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Citations | 2.1 avg | 11.3 avg | +440% |
| Bullets | 23.4 avg | 78.1 avg | +234% |
| Weak Language | 9.8 avg | 0.0 | -100% |
| Build Success | 62.5% | 100% | +60% |

## Swarm Orchestration Pattern

**For batch transformations (3+ posts), use multi-agent approach:**
- **Planner Agent**: Creates pre-analysis, defines strategy, validates output
- **Researcher Agent**: Finds citations (arXiv, NIST, official docs), validates claims
- **Coder Agent**: Executes transformations, integrates citations, runs validation

**Memory key structure:** `swarm/batch-X/post-Y/{pre-analysis,citations,status,validation-results}`

## Key Success Patterns

1. **Pre-analysis prevents scope creep** - Know targets before starting
2. **BLUF works for all post types** - Technical and personal styles both effective
3. **Strategic bulletization preserves voice** - Keep "I" statements, humor, transitions
4. **Citation research improves content** - Beyond just adding links, deepens understanding
5. **Language hardening strengthens** - Remove hedging without sterilizing personality

## Common Pitfalls to Avoid

- **Over-bulletizing**: Keep 2-3 sentence transitions, preserve storytelling
- **Losing personal voice**: Delete weak language, NOT first-person narrative
- **Citation overload**: One per major claim, not every sentence
- **Vague BLUF**: Start with surprising fact, quantify immediately, answer "why care?"

## Documentation References

- **Complete methodology**: `docs/batch-2/CLAUDE_MD_UPDATES.md` (40K, comprehensive guide)
- **Lessons learned**: `docs/batch-2/LESSONS_LEARNED.md` (36K, Batch 2 analysis)
- **Pre-analysis examples**: `docs/batch-2/pre-analysis/post-[1-8]-pre-analysis.md`
- **Cleanup report**: `docs/batch-2/CLEANUP_REPORT.md` (organization strategy)

---

## Automation Workflow

**When creating blog posts, run:**

```bash
# Update image metadata
python scripts/blog-images/update-blog-images.py

# Generate hero images
python scripts/blog-images/generate-blog-hero-images.py

# Optimize images
bash scripts/optimize-blog-images.sh

# Validate citations
python scripts/blog-research/research-validator.py

# Check for broken links
python scripts/blog-research/check-citation-hyperlinks.py
```

---

# Blog Image Standards & Implementation

## 📸 Image Management System

### Directory Structure
All blog images are organized in a hierarchical structure:
```
src/assets/images/blog/
├── hero/               # Hero images for post headers (1200x630px)
├── inline/             # Inline content images (800px wide)
├── diagrams/           # Technical diagrams and architecture visuals
├── infographics/       # Data visualizations and infographics
└── thumbnails/         # Small preview images (400x300px)
```

### Image Naming Convention
- Format: `YYYY-MM-DD-post-slug-image-type.ext`
- Example: `2025-08-07-claude-flow-architecture-diagram.png`

## 🎨 Image Requirements

### Hero Images
- **Dimensions:** 1200x630px (16:9 ratio for social sharing)
- **Format:** JPEG for photos, PNG for graphics
- **Max file size:** 200KB (optimized)
- **Purpose:** Post header and og:image for social media

### Inline Images
- **Dimensions:** 800px wide (height variable)
- **Format:** JPEG/PNG/WebP
- **Max file size:** 150KB
- **Purpose:** Content illustration within posts

### Responsive Variants
Each hero image should have:
- Original: 1200px wide
- Medium: 800px wide
- Small: 400px wide
- Thumbnail: 200px wide

## 📝 Blog Post Frontmatter

Every blog post MUST include comprehensive image metadata:

```yaml
---
title: "Post Title"
date: YYYY-MM-DD
description: "Post description"
tags: [tag1, tag2]
author: "William Zujkowski"
images:
  hero:
    src: "/assets/images/blog/hero/YYYY-MM-DD-post-slug-hero.jpg"
    alt: "Descriptive alt text for hero image"
    caption: "Optional caption for context"
    width: 1200
    height: 630
  og:
    src: "/assets/images/blog/hero/YYYY-MM-DD-post-slug-og.jpg"
    alt: "Open Graph image description"
  inline:
    - src: "/assets/images/blog/inline/image1.png"
      alt: "Alt text for inline image 1"
      caption: "Caption for image 1"
    - src: "/assets/images/blog/diagrams/diagram1.svg"
      alt: "Alt text for diagram"
      caption: "System architecture diagram"
---
```

## 🛠️ Automation Scripts

### 1. Update Blog Image Metadata
```bash
# Updates all blog posts with proper image metadata
python scripts/blog-images/update-blog-images.py
```
This script:
- Scans all blog posts
- Generates appropriate image metadata
- Creates context-aware alt text
- Updates frontmatter automatically

### 2. Generate Hero Images
```bash
# Creates hero images for all blog posts
python scripts/blog-images/generate-blog-hero-images.py
```
Features:
- Topic-based color schemes
- Pattern overlays (circuit, dots, lines, grid, waves)
- Automatic text layout
- Social media variants (og:image)

### 3. Optimize Images
```bash
# Optimizes images and creates responsive variants
bash scripts/optimize-blog-images.sh
```
Performs:
- JPEG optimization (85% quality)
- PNG compression
- Responsive variant generation
- WebP conversion (if tools available)

## 🎯 Image Creation Workflow

### For New Blog Posts:
1. **Write the post** with proper frontmatter (without images section)
2. **Run metadata update**: `python scripts/blog-images/update-blog-images.py`
3. **Generate hero image**: `python scripts/blog-images/generate-blog-hero-images.py`
4. **Optimize images**: `bash scripts/optimize-blog-images.sh`
5. **Review and customize** if needed

### For Existing Posts:
1. **Update metadata**: `python scripts/blog-images/update-blog-images.py`
2. **Generate missing images**: `python scripts/blog-images/generate-blog-hero-images.py`
3. **Optimize all images**: `bash scripts/optimize-blog-images.sh`

## ♿ Accessibility Standards

### Alt Text Requirements
- **Be descriptive**: Convey the image's purpose and content
- **Be concise**: 125 characters or less when possible
- **Include context**: Relate to surrounding content
- **Avoid redundancy**: Don't repeat caption text

### Examples:
- ✅ Good: "Diagram showing Claude-Flow's hierarchical swarm topology with queen and worker agents"
- ❌ Bad: "Image" or "Diagram"

## 🎨 Visual Consistency

### Color Schemes by Topic
The image generator automatically selects colors based on content:
- **Security**: Blue to red gradient (#1e3a8a → #dc2626)
- **AI/ML**: Purple to pink (#7c3aed → #ec4899)
- **Cloud**: Sky blue to teal (#0ea5e9 → #10b981)
- **Blockchain**: Amber to emerald (#f59e0b → #10b981)
- **Quantum**: Violet to blue (#8b5cf6 → #3b82f6)
- **DevOps**: Green to blue (#10b981 → #3b82f6)
- **Python**: Python blue and yellow (#3776ab → #ffd343)
- **JavaScript**: JavaScript yellow (#f7df1e)

### Pattern Selection
Patterns are automatically chosen based on tags:
- **AI/ML posts**: Circuit pattern
- **Cloud/DevOps**: Dots pattern
- **Security**: Diagonal lines
- **Network**: Wave pattern
- **Default**: Grid pattern

## 📊 Image Optimization

### Performance Targets
- **LCP (Largest Contentful Paint)**: < 2.5s
- **Total image weight per page**: < 1MB
- **Hero image load time**: < 1s
- **Lazy loading**: All below-fold images

### Optimization Commands
```bash
# Install optimization tools
sudo apt-get install jpegoptim optipng webp imagemagick

# Optimize JPEGs
find src/assets/images/blog -name "*.jpg" -exec jpegoptim --max=85 --strip-all {} \;

# Optimize PNGs
find src/assets/images/blog -name "*.png" -exec optipng -o2 {} \;

# Create WebP versions
for img in src/assets/images/blog/**/*.jpg; do
  cwebp -q 85 "$img" -o "${img%.*}.webp"
done
```

## 🚀 Best Practices

### When Creating Blog Posts:
1. **Always run the update script** after creating a new post
2. **Generate hero images** for visual consistency
3. **Optimize images** before committing
4. **Test responsive loading** on different devices
5. **Verify alt text** is descriptive and accurate

### Image Selection Guidelines:
1. **Hero images**: Should represent the post's main concept
2. **Inline images**: Break up text every 3-4 paragraphs
3. **Diagrams**: Use for technical explanations
4. **Infographics**: Summarize data or processes
5. **Screenshots**: Show actual interfaces when relevant

### Content-Image Alignment:
- Place images near relevant text
- Use captions to provide context
- Ensure images enhance understanding
- Don't use decorative-only images

## 📋 Quality Checklist

Before publishing, ensure:
- [ ] Hero image exists and is optimized
- [ ] Image metadata in frontmatter is complete
- [ ] Alt text is descriptive and meaningful
- [ ] Responsive variants are generated
- [ ] File sizes are under limits
- [ ] Images load properly in development
- [ ] Social media preview works (og:image)

## 🔧 Troubleshooting

### Common Issues:

**Missing hero images:**
```bash
# Regenerate for specific post
python scripts/blog-images/generate-blog-hero-images.py --post="YYYY-MM-DD-post-slug"
```

**Images too large:**
```bash
# Force re-optimization
bash scripts/optimize-blog-images.sh --force
```

**Broken image paths:**
```bash
# Validate all image references
# Validate blog images
python scripts/blog-images/update-blog-images.py --validate
```

## 📈 Monitoring

Track image performance:
1. Use Lighthouse for Core Web Vitals
2. Monitor image bandwidth in analytics
3. Check social media card validators
4. Test with screen readers
5. Validate responsive behavior

## 🎯 Quick Commands Reference

```bash
# Full image pipeline for new post
python scripts/blog-images/update-blog-images.py && \
python scripts/blog-images/generate-blog-hero-images.py && \
bash scripts/optimize-blog-images.sh

# Check image statistics
find src/assets/images/blog -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.webp" \) | wc -l

# View image index
cat docs/blog-image-index.json | jq '.stats'

# Generate report
# Generate image report (use update-blog-images.py with report flag)
python scripts/blog-images/update-blog-images.py --report > docs/image-report.md
```
