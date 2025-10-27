# Batch 1 Execution Plan: Smart Brevity Refactoring

**Status**: READY FOR EXECUTION
**Date**: 2025-10-26
**Priority**: HIGH
**Estimated Duration**: 6 hours
**Batch**: 1 of 7

---

## Executive Summary

**One big thing**: Refactor top 3 priority posts using Smart Brevity principles.

**Why it matters**:
- These posts are the most verbose (3,507, 2,516, 2,445 words)
- Highest compliance violations (missing BLUF, weak language, no AI skepticism)
- Most impactful word reduction targets (41%, 36%, 37%)
- First batch sets quality standards for remaining 52 posts

**Success criteria**:
- Word counts: 3,507→2,200, 2,516→1,600, 2,445→1,550
- Compliance scores: 40→80+ for all three
- 100% citation retention
- Build passes
- Reading time maintained at 6-9 minutes

---

## Batch 1 Posts Overview

### Post 1: Progressive Context Loading LLM Workflows
- **File**: `2025-10-17-progressive-context-loading-llm-workflows.md`
- **Current**: 3,507 words
- **Target**: 2,200 words (37% reduction, 1,307 words cut)
- **Compliance Score**: 40/100
- **Estimated Time**: 2.5 hours
- **Priority**: CRITICAL

**Key Issues**:
- Missing BLUF (opens with story, not point-first)
- 27 weak language instances
- Missing AI skepticism section
- Extensive code blocks need reduction
- Long narrative paragraphs

### Post 2: AI Cognitive Infrastructure
- **File**: `2025-08-09-ai-cognitive-infrastructure.md`
- **Current**: 2,516 words
- **Target**: 1,600 words (36% reduction, 916 words cut)
- **Compliance Score**: 60/100
- **Estimated Time**: 2 hours
- **Priority**: HIGH

**Key Issues**:
- Weak language throughout
- Missing AI skepticism (ironic for AI critique post)
- Good Mermaid diagrams already (preserve these)
- Some long paragraphs need bulletization
- Strong citations (maintain 100%)

### Post 3: Embodied AI Robots Physical World
- **File**: `2025-10-13-embodied-ai-robots-physical-world.md`
- **Current**: 2,445 words
- **Target**: 1,550 words (37% reduction, 895 words cut)
- **Compliance Score**: 60/100
- **Estimated Time**: 1.5 hours
- **Priority**: HIGH

**Key Issues**:
- Weak language instances
- Missing strong AI skepticism section
- Hardware recommendations verbose (can be more concise)
- Good security section (preserve)
- Needs BLUF strengthening

---

## Detailed Refactoring Steps by Post

## Post 1: Progressive Context Loading (2.5 hours)

### Phase 1A: Pre-Refactoring Analysis (15 min)

**Tasks**:
1. Read full post and note structure
2. Extract all citations to preserve
3. Identify code blocks for reduction strategy
4. Note weak language patterns to fix
5. Mark sections for bulletization

**Expected Output**:
- Citation inventory (JSON format)
- Code block inventory with reduction strategy
- Weak language list with replacements

### Phase 1B: BLUF Creation (20 min)

**Current Opening**:
```markdown
Last week, I caught myself mid-conversation realizing I couldn't remember...
```

**New BLUF** (2-3 sentences max):
```markdown
Progressive context loading cuts LLM token usage by 98%. Load only what's needed, when it's needed. Here's how to implement it in production workflows.

**Why it matters**: Token costs scale linearly with context size. Most workflows waste 90%+ tokens on unused context. Progressive loading changes the economics of LLM applications.
```

**Success Criteria**:
- First 3 sentences convey core value
- "Why it matters" section present
- Specific numbers included (98% reduction)
- Action-oriented ("Here's how")

### Phase 1C: Structure Transformation (45 min)

**Section-by-section approach**:

1. **Introduction** (Current: ~300 words → Target: ~100 words)
   - Cut personal narrative to 2-3 sentences
   - Move immediately to technical problem
   - Delete throat-clearing

2. **How Progressive Loading Works** (Current: ~600 words → Target: ~350 words)
   - Convert prose explanations to bullets
   - Reduce code examples to essential lines only
   - Add Mermaid diagram if helpful

3. **Implementation Guide** (Current: ~800 words → Target: ~500 words)
   - Keep code blocks focused (10-15 lines max)
   - Convert setup steps to numbered list
   - Link to GitHub gist for full code

4. **Performance Results** (Current: ~400 words → Target: ~250 words)
   - Lead with numbers in bullet format:
     - Token reduction: 98%
     - Latency improvement: X%
     - Cost savings: $X per 1M requests
   - Cut verbose explanations

5. **AI Skepticism Section** (NEW: ~200 words)
   - Add "Reality Check" section
   - Document failure modes:
     - When progressive loading fails
     - Token estimation accuracy limits
     - Edge cases requiring monolithic context
   - Include "When NOT to use" guidance

6. **Conclusion** (Current: ~200 words → Target: ~100 words)
   - One paragraph max
   - Reinforce key numbers
   - Clear next action

**Bulletization Targets**:
- Convert at least 5 paragraphs to bullet lists
- Minimum 15 bullets across post
- Each bullet: one clear idea

### Phase 1D: Language Hardening (30 min)

**Find/Replace Patterns**:

| Weak | Strong |
|------|--------|
| "could potentially" | "can" or "will" |
| "might help" | "reduces" / "improves" |
| "should consider" | "use" / "implement" |
| "basically" | DELETE |
| "essentially" | DELETE |
| "actually" | DELETE (unless essential) |
| "In this post, I'll show" | DELETE |
| "Let me explain" | DELETE |

**Manual Review**:
- Scan for hedging language
- Replace passive voice with active
- Strengthen technical claims with data
- Remove unnecessary qualifiers

**Success Criteria**:
- Weak language instances: 27 → <5
- Direct imperatives throughout
- No throat-clearing phrases

### Phase 1E: Code Reduction (20 min)

**Strategy**:
- Keep code blocks <25% of total content
- Show 5-10 line snippets with key logic
- Link to full implementations

**Example Transformation**:

❌ **Before** (50 lines of full implementation):
```python
# [entire class implementation]
```

✅ **After** (10 lines highlighting key concept):
```python
# Progressive loading: match skills to file types
def load_context_on_demand(file_type: str) -> str:
    """Load only relevant context for file type."""
    if file_type.endswith('.py'):
        return load_python_context()
    elif file_type.endswith('.md'):
        return load_markdown_context()
    return load_minimal_context()

# Full implementation: [GitHub Gist Link]
```

### Phase 1F: Validation (25 min)

**Automated Checks**:
```bash
# Word count
wc -w src/posts/2025-10-17-progressive-context-loading-llm-workflows.md
# Target: 2,200 words (±100)

# Citation validation
python scripts/blog-research/check-citation-hyperlinks.py \
  --post src/posts/2025-10-17-progressive-context-loading-llm-workflows.md

# Style compliance
python scripts/blog-content/validate-style-compliance.py \
  --file src/posts/2025-10-17-progressive-context-loading-llm-workflows.md
```

**Manual Checks**:
- [ ] BLUF present and strong
- [ ] "Why it matters" section exists
- [ ] AI skepticism section complete
- [ ] Code examples concise
- [ ] Minimum 15 bullets
- [ ] No weak language patterns
- [ ] All citations preserved
- [ ] Images/diagrams referenced correctly
- [ ] Reading time 6-9 minutes

---

## Post 2: AI Cognitive Infrastructure (2 hours)

### Phase 2A: Pre-Refactoring Analysis (10 min)

**Current State Analysis**:
- Has good Mermaid diagrams (PRESERVE)
- Strong citation game already (MAINTAIN)
- Some weak language but not excessive
- Missing AI skepticism (ironic for AI critique)
- Long paragraphs need conversion

### Phase 2B: BLUF Enhancement (15 min)

**Current Opening**:
```markdown
Last week, I caught myself mid-conversation realizing I couldn't remember...
```

**New BLUF**:
```markdown
AI isn't just tools anymore—it's infrastructure. Like roads enabled commerce and electricity powered industry, AI now shapes how we think, decide, and understand reality.

**Why it matters**: Invisible infrastructure controls our cognitive processes. You don't notice it until it fails. By then, dependency is complete.

**The reality**: We're outsourcing memory, navigation, and judgment to systems we barely understand. Cognitive debt is accumulating.
```

### Phase 2C: Structure Transformation (60 min)

**Section Targets**:

1. **Introduction** (300 words → 150 words)
   - Cut personal story to 2-3 sentences
   - Lead with infrastructure analogy
   - Delete redundant context

2. **Architecture of Thought** (500 words → 300 words)
   - Keep Mermaid diagram
   - Bulletize key mechanisms:
     - Semantic transportation
     - Anticipatory personalization
     - Adaptive invisibility
   - Cite research directly (preserve links)

3. **Embedding Revolution** (600 words → 350 words)
   - Lead with market numbers as bullets
   - Convert healthcare/education examples to compact format
   - Preserve code example but reduce to 10-15 lines

4. **Cognitive Debt Crisis** (NEW subsection: ~200 words)
   - Add explicit "AI Skepticism" heading
   - Document research on cognitive offloading
   - Include failure modes:
     - Skill atrophy statistics
     - Dependency patterns
     - Mitigation strategies

5. **Double Edge Section** (400 words → 250 words)
   - Convert promise/peril to side-by-side bullets
   - More concise examples
   - Preserve key statistics

6. **Building Ethical Infrastructure** (400 words → 250 words)
   - Bulletize principles
   - Keep code example concise
   - Strengthen imperatives

7. **Personal Reflection** (200 words → 100 words)
   - One paragraph max
   - Focus on key insight
   - Cut verbose narrative

8. **Conclusion** (200 words → 100 words)
   - Reinforce main points
   - Clear call to action
   - No redundant recap

### Phase 2D: Language Hardening (20 min)

**Weak Language Audit**:
- Find all instances of "could," "might," "should," "basically"
- Replace with direct language
- Strengthen claims with citations
- Remove hedging around research findings

**Example**:
- ❌ "AI could potentially reshape how we think"
- ✅ "AI reshapes cognition patterns (Riva 2025)"

### Phase 2E: AI Skepticism Integration (15 min)

**Add Reality Check Section**:
```markdown
## Reality Check: The Cognitive Costs

**The hype**: AI augments human intelligence
**The truth**: AI creates dependency faster than capability

**Documented impacts**:
- 72% correlation: AI usage → cognitive offloading
- 75% inverse correlation: offloading → critical thinking
- Younger users (17-25): highest dependence, lowest critical thinking

**What doesn't work**:
- "AI will enhance human thinking" without mitigation
- Assuming users maintain skills while offloading
- Treating cognitive infrastructure as neutral

**Mitigation**:
- Regular AI-free cognitive exercises
- Explicit skill maintenance programs
- Transparency in AI influence
```

### Phase 2F: Validation (10 min)

**Checks**:
- [ ] Word count: 1,600 (±100)
- [ ] BLUF enhanced
- [ ] AI skepticism section prominent
- [ ] Citations preserved (90%+)
- [ ] Mermaid diagrams intact
- [ ] Code examples concise
- [ ] Minimum 12 bullets total
- [ ] Weak language <5 instances

---

## Post 3: Embodied AI Robots (1.5 hours)

### Phase 3A: Pre-Refactoring Analysis (10 min)

**Current State**:
- Strong technical content
- Hardware recommendations verbose
- Security section good (preserve)
- Missing strong AI skepticism
- Some weak language

### Phase 3B: BLUF Strengthening (10 min)

**Current Opening**:
```markdown
Last week, I watched my 3D printer fail...
```

**New BLUF**:
```markdown
Vision-Language-Action (VLA) models give AI agents physical bodies. Not someday—now. Google's Gemini Robotics achieves 90%+ success on real-world manipulation tasks.

**Why it matters**: The gap between AI that writes code and robots that execute plans is closing. Your terminal AI can soon control your workshop robots.

**Reality check**: We're 1-2 years from practical homelab implementations. Budget entry point: $500-2,000.
```

### Phase 3C: Structure Transformation (40 min)

**Section Targets**:

1. **Introduction** (250 words → 100 words)
   - 3D printer story: 2-3 sentences
   - Cut to technical problem immediately

2. **VLA Model Explanation** (300 words → 200 words)
   - Keep Mermaid diagram
   - Bulletize three capabilities
   - One paragraph on breakthrough

3. **Gemini Robotics Breakthrough** (400 words → 250 words)
   - Lead with numbers:
     - 10M training episodes
     - 90%+ success rate
     - 38 robot embodiments
   - Competing approaches: bullet list only
   - Cut verbose comparisons

4. **Homelab Integration** (800 words → 500 words)
   - **Hardware section verbose** - major reduction target
   - Simplify budget tiers:
     - Entry: $500-2k (used arm + webcam)
     - Mid: $3k-5k (better hardware)
     - Dream: $10k-20k (aspirational, note limited budget)
   - Phase plan: bullets only, remove verbose explanations

5. **Security Section** (400 words → 300 words)
   - Keep security stack diagram
   - Preserve threat model
   - Bulletize mitigations
   - Code example: 10 lines max

6. **AI Skepticism Section** (NEW: ~150 words)
   - Add "What Can Go Wrong" section:
     - Sim-to-real gap
     - Safety failures
     - Sensor spoofing risks
     - When VLA models fail
   - Include "Not AGI" reminder

7. **Getting Started Roadmap** (300 words → 200 words)
   - Condense learning paths to bullets
   - Remove redundant explanations
   - Keep resource links

8. **Conclusion** (200 words → 100 words)
   - One paragraph
   - Reinforce key insight
   - Clear next step

### Phase 3D: Hardware Section Reduction (15 min)

**Current**: ~400 words across budget tiers
**Target**: ~200 words

**Strategy**:
```markdown
### Hardware: Three Realistic Tiers

**Entry ($500-2k)**: Learning fundamentals
- Used Lynxmotion AL5D arm ($500-800)
- Webcam or basic RealSense ($50-400)
- Existing gaming PC (RTX 3060+)

**Mid-Range ($3k-5k)**: Serious projects
- Better arm with more DOF
- RealSense D455 depth camera ($600)
- Jetson AGX Orin edge compute ($2k)

**Aspirational ($10k-20k+)**: Watching the field
- Mobile manipulators (used Fetch)
- Humanoids like Unitree G1 ($16k)
- Professional arms (used Kinova)
- Note: Beyond current learning budget, useful to understand trajectory
```

### Phase 3E: Language Hardening (10 min)

**Weak Language Patterns**:
- "could help" → "enables"
- "might be" → "is"
- Remove hedging around VLA capabilities
- Strengthen technical claims

### Phase 3F: Validation (5 min)

**Checks**:
- [ ] Word count: 1,550 (±100)
- [ ] BLUF strong and specific
- [ ] AI skepticism section added
- [ ] Hardware section concise
- [ ] Security content preserved
- [ ] Citations maintained
- [ ] Minimum 15 bullets
- [ ] Weak language <5 instances

---

## Sequential Execution Strategy

### Recommended Approach: SEQUENTIAL

**Why not parallel?**
- First batch sets quality bar for remaining 52 posts
- Each post informs refinements to next
- Easier to maintain voice consistency
- Better citation tracking
- Simpler rollback if issues found

**Order**:
1. Progressive Context Loading (hardest, learn from it)
2. AI Cognitive Infrastructure (medium difficulty)
3. Embodied AI Robots (easiest of three)

### Execution Schedule

**Session 1** (2.5 hours):
- Post 1: Progressive Context Loading
- Complete all phases 1A through 1F
- Validate thoroughly before proceeding

**Break** (15 min):
- Review Session 1 output
- Note any process improvements
- Adjust approach for Session 2 if needed

**Session 2** (2 hours):
- Post 2: AI Cognitive Infrastructure
- Apply learnings from Post 1
- Complete all phases 2A through 2F

**Break** (15 min):
- Review progress
- Prepare for final post

**Session 3** (1.5 hours):
- Post 3: Embodied AI Robots
- Apply refined process
- Complete all phases 3A through 3F

**Final Validation** (30 min):
- Run full test suite on all three posts
- Build verification
- Mobile preview check
- Commit preparation

---

## Critical Checkpoints

### Checkpoint 1: After Post 1 (2.5 hours in)

**Validation**:
```bash
# Word count check
wc -w src/posts/2025-10-17-progressive-context-loading-llm-workflows.md
# Must be: 2,200 ±100 words

# Citation check
python scripts/blog-research/check-citation-hyperlinks.py \
  --post src/posts/2025-10-17-progressive-context-loading-llm-workflows.md
# Must show: 100% citations preserved

# Build test
npm run build
# Must pass cleanly

# Style compliance
python scripts/blog-content/validate-style-compliance.py \
  --file src/posts/2025-10-17-progressive-context-loading-llm-workflows.md
# Must show: Score ≥80/100
```

**Go/No-Go Decision**:
- ✅ GO if all checks pass → Proceed to Post 2
- ❌ NO-GO if any check fails → Fix before proceeding

**Why this matters**: First post sets the quality bar. Don't compound errors across three posts.

### Checkpoint 2: After Post 2 (4.5 hours in)

**Same validation suite as Checkpoint 1**

**Additional Check**:
- Compare tone/voice between Post 1 and Post 2
- Ensure consistency in BLUF format
- Verify AI skepticism sections comparable

### Checkpoint 3: After Post 3 (6 hours in)

**Full Batch Validation**:
```bash
# Validate all three posts
for post in \
  "2025-10-17-progressive-context-loading-llm-workflows.md" \
  "2025-08-09-ai-cognitive-infrastructure.md" \
  "2025-10-13-embodied-ai-robots-physical-world.md"; do

  echo "Validating $post..."

  # Word count
  words=$(wc -w < "src/posts/$post")
  echo "Word count: $words"

  # Citations
  python scripts/blog-research/check-citation-hyperlinks.py \
    --post "src/posts/$post"

  # Style
  python scripts/blog-content/validate-style-compliance.py \
    --file "src/posts/$post"
done

# Final build test
npm run build
npm run test
```

**Success Criteria**:
- All word counts within target ±100
- All citations valid
- All builds pass
- Style compliance ≥80 for all three

---

## Validation Criteria

### Per-Post Success Metrics

| Metric | Before | Target | Validation |
|--------|--------|--------|------------|
| **Post 1 Word Count** | 3,507 | 2,200 (±100) | `wc -w` |
| **Post 2 Word Count** | 2,516 | 1,600 (±100) | `wc -w` |
| **Post 3 Word Count** | 2,445 | 1,550 (±100) | `wc -w` |
| **Compliance Score** | 40-60 | 80+ | Automated script |
| **Citation Retention** | 100% | ≥95% | Citation validator |
| **BLUF Present** | No | Yes | Manual check |
| **AI Skepticism** | No | Yes | Manual check |
| **Weak Language** | 27, varied | <5 each | Manual scan |
| **Bullet Count** | Low | ≥15 each | Manual count |
| **Build Status** | N/A | PASS | `npm run build` |

### Batch-Level Success Metrics

- **Total Word Reduction**: 3,118 words cut (37% average)
- **Average Compliance Improvement**: 40-60 → 80+ (30+ point gain)
- **Citation Integrity**: 100% of working links maintained
- **Voice Consistency**: All three posts match tone/style
- **Build Health**: Zero errors, zero warnings
- **Mobile Rendering**: All posts render correctly at 375px width

---

## Commit Strategy

### Individual Commits per Post (RECOMMENDED)

**Why**:
- Easier to review changes
- Simpler rollback if one post has issues
- Clearer git history
- Better for identifying regressions

**Commit Format**:
```bash
# After Post 1
git add src/posts/2025-10-17-progressive-context-loading-llm-workflows.md
git commit -m "refactor: apply Smart Brevity to progressive context loading post

- Add BLUF (3 sentences + why it matters)
- Reduce 3,507 → 2,200 words (37% reduction)
- Add AI skepticism section (failure modes, limitations)
- Convert 5 paragraphs to bullet lists (15+ bullets total)
- Remove 22 weak language instances (27 → 5)
- Preserve all citations (100% retention)
- Reduce code examples (50+ lines → 10-15 line snippets)

Compliance score: 40 → 85

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# After Post 2
git add src/posts/2025-08-09-ai-cognitive-infrastructure.md
git commit -m "refactor: apply Smart Brevity to AI cognitive infrastructure post

- Enhance BLUF with infrastructure analogy
- Reduce 2,516 → 1,600 words (36% reduction)
- Add explicit AI skepticism section (cognitive debt reality check)
- Bulletize promise/peril comparison
- Remove weak language patterns (15 → 3 instances)
- Preserve Mermaid diagrams and citations (100% retention)
- Convert 4 long paragraphs to bullet lists (12+ bullets)

Compliance score: 60 → 82

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# After Post 3
git add src/posts/2025-10-13-embodied-ai-robots-physical-world.md
git commit -m "refactor: apply Smart Brevity to embodied AI robots post

- Strengthen BLUF with specific VLA model capabilities
- Reduce 2,445 → 1,550 words (37% reduction)
- Add 'What Can Go Wrong' AI skepticism section
- Condense hardware recommendations (400 → 200 words)
- Bulletize learning roadmap and budget tiers
- Preserve security section and diagrams
- Remove weak language (11 → 4 instances)

Compliance score: 60 → 83

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Alternative: Single Batch Commit

**Only if**:
- All three posts pass validation
- Voice consistency confirmed
- No issues found during review

**Format**:
```bash
git add src/posts/2025-10-17-progressive-context-loading-llm-workflows.md \
        src/posts/2025-08-09-ai-cognitive-infrastructure.md \
        src/posts/2025-10-13-embodied-ai-robots-physical-world.md

git commit -m "refactor: apply Smart Brevity to Batch 1 (3 posts)

Posts updated:
- progressive-context-loading-llm-workflows.md (3,507 → 2,200 words)
- ai-cognitive-infrastructure.md (2,516 → 1,600 words)
- embodied-ai-robots-physical-world.md (2,445 → 1,550 words)

Changes:
- Added BLUF sections to all posts
- Converted 14 paragraphs to bullet lists (40+ bullets total)
- Added AI skepticism sections
- Removed 48 weak language instances across posts
- Preserved all citations (100% retention)
- Reduced code examples to essential snippets

Total word reduction: 3,118 words (37% average)
Compliance improvement: 40-60 → 80+ (all posts)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Build Verification Steps

### After Each Post

```bash
# Quick build check
npm run build

# Should see:
# [11ty] Writing _site/posts/[post-name]/index.html from ./src/posts/[post-name].md
# [11ty] Wrote 1 file in 0.12 seconds (v2.0.1)
```

**If build fails**:
1. Check error message for syntax issues
2. Validate markdown formatting
3. Check frontmatter YAML
4. Verify image paths
5. Look for broken internal links

### After Full Batch

```bash
# Full build
npm run build

# Run tests
npm run test

# Check for warnings
npm run build 2>&1 | grep -i warning

# Validate no broken links
npm run build 2>&1 | grep -i "broken"

# Check lighthouse scores (if available)
npm run lighthouse

# Mobile preview
npm run serve
# Then test at http://localhost:8080 with browser DevTools mobile view
```

---

## Rollback Plan

### If Post 1 Fails Validation

**Symptoms**:
- Word count off by >100 words
- Citations broken
- Build fails
- Compliance score <80

**Action**:
```bash
# Don't commit yet
git diff src/posts/2025-10-17-progressive-context-loading-llm-workflows.md

# Review what changed
# Fix specific issues
# Re-run validation

# Only commit when all checks pass
```

### If Post 2 or 3 Fails After Post 1 Committed

**Action**:
```bash
# Commit good posts, hold back failed post
git add src/posts/[good-post].md
git commit -m "refactor: [good post description]"

# Fix failed post
# Validate thoroughly
# Commit separately when ready
```

### If Entire Batch Needs Rollback

**Action**:
```bash
# If not yet pushed to GitHub
git reset --soft HEAD~3  # Undo last 3 commits
# Or
git reset --soft HEAD~1  # Undo single batch commit

# Fix issues
# Re-apply changes carefully

# If already pushed
git revert [commit-hash]
# Then fix and commit corrected version
```

### Nuclear Option

**If fundamental approach is wrong**:
```bash
# Create new branch from before changes
git checkout -b batch-1-v2 [commit-before-changes]

# Re-apply strategy with lessons learned
# Don't rush to match timeline
# Quality over speed
```

---

## Risk Mitigation

### Risk 1: Over-Compression Below 1,400 Words

**Mitigation**:
- Target ranges include ±100 word buffer
- Post 1: 2,200 (well above 1,400)
- Post 2: 1,600 (safe margin)
- Post 3: 1,550 (safe margin)
- Monitor word count at each phase
- If approaching minimum, preserve more content

### Risk 2: Citation Loss During Rewrite

**Mitigation**:
- Run citation check pre-refactoring
- Capture citation inventory (JSON)
- Run citation check post-refactoring
- Compare pre/post results
- Require ≥95% retention (allow 5% for truly redundant citations)
- Manual review of any lost citations

### Risk 3: Voice Inconsistency Across Posts

**Mitigation**:
- Sequential execution (learn from each post)
- Use same BLUF template structure
- Consistent AI skepticism section format
- Same weak language replacement patterns
- Review all three together before commit

### Risk 4: Build Failure from Syntax Errors

**Mitigation**:
- Test build after each post
- Validate markdown syntax
- Check frontmatter YAML
- Test image references
- Verify internal links
- Use linter if available

### Risk 5: Lost Technical Depth

**Mitigation**:
- Preserve key statistics and numbers
- Keep technical diagrams
- Maintain code examples (but concise)
- Citations prove claims
- Reviewer agent final check for accuracy

---

## Tools & Scripts Required

### Existing Scripts (Must Work)

1. **Citation Validator**:
   ```bash
   python scripts/blog-research/check-citation-hyperlinks.py \
     --post src/posts/[filename].md
   ```

2. **Style Compliance Checker**:
   ```bash
   python scripts/blog-content/validate-style-compliance.py \
     --file src/posts/[filename].md
   ```

3. **Build Tools**:
   ```bash
   npm run build
   npm run test
   ```

### Manual Validation Checklist

**Per-Post Checklist** (copy for each post):

```markdown
## [Post Title] Validation

- [ ] BLUF present (first 2-3 sentences)
- [ ] "Why it matters" section included
- [ ] AI skepticism section added (if AI-related)
- [ ] Word count: [target] ±100
- [ ] Weak language reduced to <5 instances
- [ ] Minimum 15 bullets across post
- [ ] Paragraphs average ≤5 sentences
- [ ] Code blocks <25% of content
- [ ] Citations preserved (≥95%)
- [ ] Images/diagrams referenced correctly
- [ ] Build passes (`npm run build`)
- [ ] Mobile preview tested
- [ ] Reading time 6-9 minutes
- [ ] Compliance score ≥80 (if script available)
```

---

## Post-Batch Actions

### After All Three Posts Validated

1. **Create Batch Report**:
```markdown
# Batch 1 Completion Report

**Status**: COMPLETE
**Date**: [completion date]
**Duration**: [actual hours]

## Results

| Post | Before | After | Reduction | Compliance |
|------|--------|-------|-----------|------------|
| Progressive Context | 3,507 | [actual] | [%] | 40 → [score] |
| AI Cognitive | 2,516 | [actual] | [%] | 60 → [score] |
| Embodied AI | 2,445 | [actual] | [%] | 60 → [score] |

## Lessons Learned

- [What worked well]
- [What was challenging]
- [Process improvements for Batch 2]

## Metrics

- Total words cut: [actual]
- Average reduction: [%]
- Citation retention: [%]
- Build health: [status]
- Time vs estimate: [comparison]
```

2. **Update Refactoring Progress**:
```bash
# Update hive memory (if using)
npx claude-flow@alpha hooks post-task --task-id "batch-1-refactoring"
```

3. **Prepare for Batch 2**:
- Review learnings
- Adjust templates if needed
- Update process documentation
- Plan Batch 2 timing

4. **Monitor Deployment**:
- Watch GitHub Actions
- Check production build
- Verify live site renders correctly
- Monitor analytics for any bounce rate changes

---

## Success Celebration Criteria

**Batch 1 is successful when**:
- ✅ All three posts reduced to target word counts (±100)
- ✅ Compliance scores improved 40-60 → 80+
- ✅ 100% citation retention maintained
- ✅ Builds pass cleanly
- ✅ Mobile rendering confirmed
- ✅ Voice consistency across posts
- ✅ AI skepticism sections added appropriately
- ✅ Process documented for Batch 2-7

**If all criteria met**:
- Merge to main
- Deploy to production
- Monitor for 24 hours
- Proceed with Batch 2 planning

---

## Recommended Approach Summary

**SEQUENTIAL execution, individual commits**

**Why**:
- First batch is the learning experience
- Each post improves next post's process
- Easier rollback granularity
- Better git history
- Clearer review process

**Estimated Timeline**:
- Post 1: 2.5 hours (hardest, sets quality bar)
- Post 2: 2 hours (apply learnings)
- Post 3: 1.5 hours (refined process)
- **Total**: 6 hours

**Critical Success Factors**:
1. Don't skip validation checkpoints
2. Maintain citation integrity
3. Preserve technical accuracy
4. Consistent voice across posts
5. Build verification at each step
6. Don't rush to meet time estimates

**Remember**: Quality over speed. It's better to take 8 hours and get it right than rush 6 hours and need to redo.

---

## Appendix: Quick Reference

### BLUF Template

```markdown
[Core value proposition in 1-2 sentences with specific numbers]

**Why it matters**: [Impact/significance in 1-2 sentences]

[Optional third sentence: Reality check or key insight]
```

### AI Skepticism Section Template

```markdown
## Reality Check

**The hype**: [What's being claimed]
**The truth**: [What actually works]

**Limitations**:
- [Known failure mode 1]
- [Known failure mode 2]
- [Edge case that breaks it]

**When NOT to use**: [Specific scenarios where approach fails]

**Mitigation**: [How to handle limitations]
```

### Weak Language Find/Replace

```
could potentially → can
might help → reduces / improves
should consider → use / implement
basically → DELETE
essentially → DELETE
actually → DELETE (unless essential)
In this post, I'll → DELETE
Let me explain → DELETE
```

### Validation Command Sequence

```bash
# Per post
wc -w src/posts/[filename].md
python scripts/blog-research/check-citation-hyperlinks.py --post src/posts/[filename].md
python scripts/blog-content/validate-style-compliance.py --file src/posts/[filename].md
npm run build

# Full batch
npm run build && npm run test
```

---

**End of Batch 1 Execution Plan**

**Status**: READY FOR EXECUTION
**Next Step**: Begin Phase 1A (Progressive Context Loading analysis)
**Estimated Completion**: 6 hours from start
