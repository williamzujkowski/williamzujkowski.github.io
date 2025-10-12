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
- **Last Audit**: 2025-09-23
- **Posts Reviewed**: 48/48

### Research & Citations ✅
- **Citation Coverage**: 90%+ (increased from 45%)
- **Academic Sources**: 50%+ with DOI/arXiv links
- **Broken Links**: 0 (fixed 49 issues)
- **Statistics Sourced**: 100%
- **Last Enhancement**: 2025-09-21

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
1. **Phased Approach**: Compliance → Citations → UI/UX
2. **Homelab Focus**: Safe, engaging, valuable content
3. **Personal Stories**: Connection through shared failures
4. **Academic Citations**: Credibility through research
5. **Mobile-First**: Better experience across all devices

### Challenges Overcome:
1. **NDA Boundaries**: "Public sector platforms" phrasing
2. **Citation Formatting**: Automated broken link detection
3. **Resume to Story**: Personal narrative transformation
4. **Touch Targets**: Systematic 44px minimum implementation
5. **Pre-commit Hooks**: Proper handling of build artifacts

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

**NEVER save to root folder. Use these directories:**
- `/src` - Source code files
- `/tests` - Test files
- `/docs` - Documentation and markdown files
- `/config` - Configuration files
- `/scripts` - Utility scripts
- `/examples` - Example code

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

### ✅ CORRECT (Single Message):
```javascript
[BatchTool]:
  // Initialize swarm
  mcp__claude-flow__swarm_init { topology: "mesh", maxAgents: 6 }
  mcp__claude-flow__agent_spawn { type: "researcher" }
  mcp__claude-flow__agent_spawn { type: "coder" }
  mcp__claude-flow__agent_spawn { type: "tester" }
  
  // Spawn agents with Task tool
  Task("Research agent: Analyze requirements...")
  Task("Coder agent: Implement features...")
  Task("Tester agent: Create test suite...")
  
  // Batch todos
  TodoWrite { todos: [
    {id: "1", content: "Research", status: "in_progress", priority: "high"},
    {id: "2", content: "Design", status: "pending", priority: "high"},
    {id: "3", content: "Implement", status: "pending", priority: "high"},
    {id: "4", content: "Test", status: "pending", priority: "medium"},
    {id: "5", content: "Document", status: "pending", priority: "low"}
  ]}
  
  // File operations
  Bash "mkdir -p app/{src,tests,docs}"
  Write "app/src/index.js"
  Write "app/tests/index.test.js"
  Write "app/docs/README.md"
```

### ❌ WRONG (Multiple Messages):
```javascript
Message 1: mcp__claude-flow__swarm_init
Message 2: Task("agent 1")
Message 3: TodoWrite { todos: [single todo] }
Message 4: Write "file.js"
// This breaks parallel coordination!
```

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

### Research Verification Process
1. **Claim Identification**: Scan content for any factual claims, statistics, or technical statements
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

#### Every Technical Claim Must Have:
- **Primary Source**: Original research paper or official documentation
- **Secondary Validation**: Additional supporting sources
- **Context**: Explain methodology, sample size, limitations
- **Recency Check**: Ensure information is current (check publication dates)

#### Red Flags to Avoid:
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

### ✅ Quality Checklist

Before Publishing Any Post:
- [ ] All factual claims have citations
- [ ] Statistics include methodology and source
- [ ] Technical specs verified against official docs
- [ ] At least 3 reputable sources per major point
- [ ] No outdated information (check dates)
- [ ] Opposing viewpoints acknowledged
- [ ] Limitations clearly stated
- [ ] Visual aids properly attributed
- [ ] References section complete
- [ ] Playwright verification completed

### 🚫 Never Do This:
- Invent statistics or percentages
- Paraphrase without attribution
- Use Wikipedia as primary source
- Cite outdated documentation
- Cherry-pick data without context
- Ignore contradicting research
- Make absolute statements without evidence
- Use anecdotal evidence as fact
- Network setup (Dream Machine Pro, Ubiquiti, VLANs)
- Security tools (Nessus, Grype, OSV, Bitwarden self-hosted)
- Development environment (VS Code, Ghostty terminal, Zsh)

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

## Content Philosophy

### Core Principles
- **Be Genuine**: Write conversationally, share real experiences including failures
- **Add Value**: Every post should provide practical tips, new perspectives, or thought-provoking questions
- **Stay Curious**: Write about genuine interests, update old posts when learning something new

## Writing Voice & Style

### Voice Characteristics
- **Conversational but Thoughtful**: Like explaining something just learned
- **Personal but Professional**: Share relevant stories while maintaining boundaries
- **Helpful but Humble**: Share what worked personally, acknowledge different approaches

### Language Guidelines
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

### Structure
- Mix short punchy sentences with detailed ones
- One idea per paragraph
- Use white space for readability
- Start paragraphs with strong hooks

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

**ABSOLUTE RULES FOR GOVERNMENT EMPLOYEES:**
- **NO current incidents**: Never discuss anything that could be interpreted as a current or recent security incident
- **Time buffer required**: Only discuss professional incidents from "years ago" (minimum 2-3 years)
- **Generic examples only**: When discussing work scenarios, make them generic and hypothetical
- **Personal projects safe**: Home lab and personal research projects are fine to discuss
- **Academic tone**: Frame security topics as research, learning, or general best practices

**Safe Content Patterns:**
- "Years ago, I learned..." (with vague timeframes)
- "In my home lab, I discovered..."
- "While researching [topic], I found..."
- "A common scenario in security is..." (hypothetical)
- "Best practices suggest..." (general guidance)

**NEVER Use These Patterns:**
- "Last week/month at work..."
- "We recently had an incident..."
- "My current employer..."
- "In our production environment..."
- "I just dealt with..."

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
- Family members' personal details
- Employer confidential information
- Others' stories without permission
- Financial specifics
- Personal relationship details

## Remember
- Perfect is the enemy of published
- Voice will evolve—that's good
- Not every post needs to be epic
- It's okay to have opinions
- Writing gets easier with practice

---

# 📝 Blog Post Creation Guidelines

## Overview

When creating blog posts for williamzujkowski.github.io, follow these comprehensive guidelines to ensure quality, consistency, and alignment with the blog's mission.

## Target Audience

- **Primary**: Technology enthusiasts with varying levels of expertise
- **Secondary**: Beginners seeking to understand complex technical concepts
- **Approach**: Begin with concise summaries to help beginners grasp key points, then dive deeper for advanced readers

## Topic Selection and Diversity

### Pre-Writing Topic Analysis

**MANDATORY**: Before starting any blog post, complete this topic diversity analysis:

```
TOPIC DIVERSITY ANALYSIS:
Last 10 blog post primary topics: [list them from /src/posts/]
Over-represented topics: [identify any topics appearing 2+ times in recent posts]
Under-represented topics: [identify topics from focus areas not covered recently]
Selected primary topic for this post: [your choice]
Justification: [brief explanation of why this topic adds diversity]
```

**Note**: This analysis should remain in working notes and not appear in the final blog post.

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

## Content Development

### Required Elements

1. **Opening Hook**: Start with a compelling story, question, or interesting fact
2. **Context Setting**: Explain why this topic matters now
3. **Core Content**: Main technical information and insights
4. **Personal Experience**: Incorporate insights from homelab experiments or research
5. **Practical Examples**: Include code samples, diagrams, or images to illustrate concepts
6. **Security Considerations**: When relevant, discuss vulnerabilities (CVSS 9.5+) and mitigation strategies
7. **Trade-offs and Limitations**: Provide balanced analysis of technologies and solutions
8. **Personal Reflection**: What this means to you and why you find it interesting
9. **Conclusion**: Summarize main points and reinforce critical insights
10. **Call to Action**: Encourage readers to apply knowledge, participate in discussions, or explore related topics

### Content Quality Standards

- **Analogies and Real-World Examples**: Use to simplify complex technical concepts
- **Balanced Perspective**: Discuss trade-offs and limitations for credibility
- **Simple Language**: Where possible, with explanations for necessary jargon
- **Conversational Tone**: Engage readers by posing questions and addressing them directly
- **Structured Format**: Clear headings, subheadings, bullet points, and numbered lists

### Code Integration

- Store code samples in appropriate folders within the website's repository
- Include instructions or direct links in the blog post to these resources
- Use syntax highlighting and add comments for clarity
- Keep code examples concise and focused on key concepts

## Reading Time and Length Requirements

### Minimum Standards

- **Target Reading Time**: 6 to 9 minutes
- **Word Count**: Approximately 1,400 to 2,100 words (based on 238 words/minute average reading speed)
- **Rejection Criteria**: Posts under 1,400 words will be rejected for being too short

### Length by Post Type

- **Personal Essays**: 800-2000 words
- **Tutorials**: As needed for completeness (typically 1,500-2,500 words)
- **Thought Pieces**: 600-1500 words
- **Project Documentation**: As needed for comprehensive coverage

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

## Visual Enhancements

### Image Requirements

**MANDATORY**: Incorporate actual images throughout the post, not just suggestions.

#### Required Images

1. **Header Image**: At the top of the post (1200x630px)
2. **Section Images**: Approximately one image per major section
3. **Relevant Illustrations**: Images that directly illustrate or enhance concepts being discussed

#### Image Sources

Use copyright-free websites:
- [Unsplash](https://unsplash.com/)
- [Pexels](https://www.pexels.com/)
- [Pixabay](https://pixabay.com/)
- [Wikimedia Commons](https://commons.wikimedia.org/)
- [NASA Image Gallery](https://www.nasa.gov/multimedia/imagegallery/)
- [StockSnap.io](https://stocksnap.io/)
- [Kaboompics](https://kaboompics.com/)
- [ISO Republic](https://isorepublic.com/)
- [Burst by Shopify](https://burst.shopify.com/)
- [Rawpixel](https://www.rawpixel.com/)

#### Image Details

For each image, provide:
- Direct URL to the specific image (not just the website)
- Proper attribution if required by the source
- Descriptive alt text for accessibility
- Complete Markdown formatting for inclusion in the post
- Appropriate search terms to find highly relevant images

## Citations and References

### Citation Requirements

- **Full URLs**: Include complete URLs for all external sources
- **Reputable Sources**: Link to authoritative sources (see Research & Credibility Model section)
- **Academic Papers**: Prefer DOI links or arXiv references
- **90%+ Coverage**: Maintain the blog's 90%+ citation coverage standard
- **Hyperlinked Citations**: ALL citations MUST include clickable hyperlinks to sources

### Further Exploration Section

At the end of each post, include:
- Links to related articles
- Official documentation
- Tutorials and guides
- Relevant public repositories (even if not owned by author)
- Projects that readers may find interesting to explore

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

Before submitting any blog post:

- [ ] Topic diversity analysis completed
- [ ] Title is unique (verified against existing posts)
- [ ] Word count meets minimum (1,400+ words)
- [ ] Reading time is 6-9 minutes
- [ ] All factual claims have citations with working hyperlinks
- [ ] At least 3 reputable sources per major point
- [ ] Header image and section images included
- [ ] All images have descriptive alt text
- [ ] Code examples are tested and functional
- [ ] Links are verified (no broken links)
- [ ] Mobile preview checked
- [ ] Accessibility requirements met
- [ ] NDA compliance verified (no work references)
- [ ] Personal experience incorporated
- [ ] Call to action included
- [ ] Further reading section populated
- [ ] Metadata complete (date, tags, description, images)
- [ ] Trade-offs and limitations discussed
- [ ] Conversational tone maintained
- [ ] Grammar and spelling checked

## Integration with Existing Workflows

When creating blog posts, also:

1. Run `python scripts/blog-images/update-blog-images.py` to update image metadata
2. Generate hero images with `python scripts/blog-images/generate-blog-hero-images.py`
3. Optimize images with `bash scripts/optimize-blog-images.sh`
4. Validate citations with `python scripts/blog-research/research-validator.py`
5. Check for broken links before committing

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
