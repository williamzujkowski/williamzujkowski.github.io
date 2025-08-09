# Claude Code Configuration - SPARC Development Environment

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

### 📸 Blog Image System
**Quick Commands for Blog Images:**
```bash
# Full pipeline for new blog post images
python scripts/update-blog-images.py && \
python scripts/generate-blog-hero-images.py && \
bash scripts/optimize-blog-images.sh
```
See [Blog Image Standards section](#blog-image-standards--implementation) for complete documentation.

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

### Build Commands
- `npm run build` - Build project
- `npm run test` - Run tests
- `npm run lint` - Linting
- `npm run typecheck` - Type checking

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

## Blog Image Management
When working with blog posts:
1. ALWAYS add image metadata to frontmatter
2. Run `python scripts/update-blog-images.py` after creating posts
3. Generate hero images with `python scripts/generate-blog-hero-images.py`
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
python scripts/update-blog-images.py
```
This script:
- Scans all blog posts
- Generates appropriate image metadata
- Creates context-aware alt text
- Updates frontmatter automatically

### 2. Generate Hero Images
```bash
# Creates hero images for all blog posts
python scripts/generate-blog-hero-images.py
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
2. **Run metadata update**: `python scripts/update-blog-images.py`
3. **Generate hero image**: `python scripts/generate-blog-hero-images.py`
4. **Optimize images**: `bash scripts/optimize-blog-images.sh`
5. **Review and customize** if needed

### For Existing Posts:
1. **Update metadata**: `python scripts/update-blog-images.py`
2. **Generate missing images**: `python scripts/generate-blog-hero-images.py`
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
python scripts/generate-blog-hero-images.py --post="YYYY-MM-DD-post-slug"
```

**Images too large:**
```bash
# Force re-optimization
bash scripts/optimize-blog-images.sh --force
```

**Broken image paths:**
```bash
# Validate all image references
python scripts/validate-blog-images.py
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
python scripts/update-blog-images.py && \
python scripts/generate-blog-hero-images.py && \
bash scripts/optimize-blog-images.sh

# Check image statistics
find src/assets/images/blog -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.webp" \) | wc -l

# View image index
cat docs/blog-image-index.json | jq '.stats'

# Generate report
python scripts/generate-image-report.py > docs/image-report.md
```
