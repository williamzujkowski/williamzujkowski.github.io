# Using the Blog Post Template

**Purpose**: This guide shows you how to use the blog post template to consistently create high-quality, humanized content that scores 80-90/100 on first draft.

**Location**: `/src/templates/blog-post-template.md`

---

## Quick Start (5 Minutes)

### 1. Copy the Template

```bash
# Create your new post from template
cp src/templates/blog-post-template.md src/posts/YYYY-MM-DD-your-slug.md

# Example with today's date
cp src/templates/blog-post-template.md src/posts/2025-10-29-my-awesome-post.md
```

### 2. Update the Frontmatter

Replace the placeholder values with your post details:

```yaml
---
date: 2025-10-29  # Today's date
title: "My Awesome Post Title (6-12 words)"  # Catchy and descriptive
description: "A compelling 150-160 character description that makes people want to click"
tags:
  - primary-topic      # Main focus (security, AI, homelab, etc.)
  - secondary-topic    # Supporting topic
  - technology        # Specific tech (docker, python, k3s, etc.)
  - optional-tag      # Additional context
# Don't worry about images yet—run update script later
---
```

### 3. Follow the Template Structure

The template includes:
- ✅ Built-in humanization checklist
- ✅ Section-by-section guidance with examples
- ✅ Inline comments explaining "why" for each element
- ✅ Pre-writing checklist for validation

Simply fill in each section with your content, following the examples and guidance provided.

### 4. Run the Image Update Script

After writing your post:

```bash
# Generate image metadata and hero images
python scripts/blog-images/update-blog-images.py
python scripts/blog-images/generate-blog-hero-images.py
bash scripts/optimize-blog-images.sh
```

### 5. Validate Before Committing

```bash
# Check humanization score (target: ≥75/100)
python scripts/blog-content/humanization-validator.py --post src/posts/YYYY-MM-DD-your-slug.md

# Verify citation hyperlinks
python scripts/blog-research/check-citation-hyperlinks.py

# Expected output:
# Score: 85/100 - PASS ✓
# All citation hyperlinks valid ✓
```

---

## Understanding the Template Sections

### Opening Hook: The First Impression

**Purpose**: Draw readers in with a personal, specific story

**What to include:**
- A concrete moment or challenge from your experience
- Specific details (time spent, exact mistake, surprising discovery)
- Emotional honesty (confusion, frustration, excitement)

**Example:**
```markdown
Years ago, I spent an entire weekend debugging why my Kubernetes cluster kept
crashing every 6 hours. I checked logs, profiled memory, rewrote configuration
files. Turned out I'd set `memory_limit: 6MB` instead of `6GB`—a single character
typo that cost me 16 hours. This painful lesson taught me to always validate
units in configs...
```

**Why it works:**
- Specific time: "entire weekend", "16 hours", "6 hours"
- Personal vulnerability: "painful lesson", admitting the typo
- Concrete detail: The exact mistake (6MB vs 6GB)

---

### Context: Why This Matters Now

**Purpose**: Connect the hook to current relevance

**What to include:**
- Time context ("After 3 months of testing", "Last week I discovered")
- Personal project context ("In my homelab", "While upgrading my...")
- Clear motivation ("This prompted me to...", "I wanted to share...")

**Example:**
```markdown
After that disaster, I spent 3 months building a validation system for my homelab
configs. This system has caught 47 potential issues across 12 projects, saving
countless debugging hours. Here's how I built it and what I learned along the way.
```

**Key elements:**
- Time specificity: "3 months"
- Quantitative results: "47 potential issues", "12 projects"
- Personal context: "my homelab"
- Clear value: "saving countless debugging hours"

---

### Core Content: Technical Substance

**Purpose**: Deliver practical, tested information

**Structure:**
1. Start with overview/architecture (Mermaid diagram)
2. Break into logical subsections (H3 headings)
3. Include concrete examples (code, configs, commands)
4. Add measurements from your testing

**Measurement patterns:**
```markdown
✅ GOOD:
"On my Intel i9-9900K with 64GB RAM, cold start took 12-15 seconds,
with throughput of 340-520 req/s and stable memory usage at 4-6GB."

❌ BAD:
"The system starts quickly and has good performance with reasonable
memory usage."
```

**Why measurements matter:**
- Prove real-world testing (authenticity)
- Set realistic expectations (helpfulness)
- Enable reader comparison (practical value)
- Boost humanization score (+5 to +10 points for 10+ measurements)

---

### Trade-offs & Considerations: The Secret Sauce

**Purpose**: This section is CRITICAL for humanization scores (7-10 bonus points possible)

**What makes trade-offs analysis excellent:**

1. **Multi-option evaluation** (3+ options tested)
   ```markdown
   I tested four different worker configurations:
   - 4 workers: 12s startup, 340 req/s, 2GB RAM
   - 8 workers: 18s startup, 520 req/s, 4GB RAM
   - 12 workers: 25s startup, 680 req/s, 8GB RAM ← Sweet spot
   - 16 workers: 28s startup, 710 req/s, 12GB RAM (diminishing returns)
   ```

2. **Quantified comparisons** (specific metrics for each option)
   - Include: speed, memory, CPU, cost, complexity
   - Use: percentages, multipliers, absolute values
   - Compare: A vs B vs C with numbers

3. **Context-dependent recommendations** (when to use each)
   ```markdown
   - Use 8 workers if: You have <16GB RAM
   - Use 12 workers if: You need max throughput and have memory to spare
   - Avoid 16 workers: Diminishing returns and instability
   ```

4. **Performance vs. X analysis**
   - Speed vs. accuracy
   - Cost vs. capability
   - Simplicity vs. features
   - Memory vs. throughput

**Depth scoring:**
- 1-2 points: Simple mention ("there are trade-offs")
- 3-4 points: Basic two-sided comparison
- 5-6 points: Detailed comparison with some metrics
- 7-8 points: Multi-option evaluation with quantified comparisons ⭐
- 9-10 points: Comprehensive multi-option analysis with context-dependent recommendations ⭐⭐

---

### Challenges & Lessons Learned: The Humanity Booster

**Purpose**: Build trust through vulnerability and honesty (+5 to +10 bonus points)

**Failure narrative patterns:**

1. **Bug admissions**
   ```markdown
   "I made a rookie mistake: I forgot to [critical step]..."
   "I completely overlooked [obvious thing] which cost me..."
   "I didn't realize [fact] until after [consequence]..."
   ```

2. **Debugging stories**
   ```markdown
   "I spent 6 hours debugging [issue]. I tried [A], [B], and [C].
   Finally discovered [root cause] after [how I found it]."
   ```

3. **Learning from failure**
   ```markdown
   "This taught me to always [preventive measure]. Now I never [mistake]
   without first [check]."
   ```

4. **Time costs**
   ```markdown
   "Recovery took 8 hours and required [specific actions]. I had to
   [rebuild/reconfigure/rewrite] [component] from scratch."
   ```

**Why failure narratives score highly:**
- Show vulnerability (uniquely human trait)
- Demonstrate real experience (authenticity)
- Help readers avoid same mistakes (value)
- AI rarely admits failures (AI-tell detector)

**Scoring rubric:**
- 0 points: No failures mentioned
- 2-3 points: Generic mention ("there were issues")
- 5-6 points: Specific failure with details ("spent 3 hours on X")
- 8-10 points: Rich narrative with time costs, recovery, and lessons ⭐⭐

---

### Practical Implementation: Make It Actionable

**Purpose**: Enable readers to actually implement what you describe

**Include:**
1. **Installation commands** (with versions)
2. **Configuration examples** (with explanations)
3. **Code snippets** (5-15 lines, well-commented)
4. **Validation steps** (how to verify it works)
5. **Expected outputs** (what success looks like)

**Example structure:**
```markdown
### Setup

\`\`\`bash
# Install specific version (tested and working)
sudo apt-get install -y package-name=2.3.1-1

# Verify installation
package-name --version
# Expected output: v2.3.1
\`\`\`

### Configuration

\`\`\`yaml
# config.yaml - Optimized for 64GB RAM
workers: 12  # From testing above (see Trade-offs section)
memory: 6GB  # Leaves 2GB buffer based on observed 5.2GB peak
\`\`\`

**Why these values:**
- `workers: 12` provides best throughput (680 req/s) without excessive memory
- `memory: 6GB` is conservative—I saw peaks at 5.2GB during load testing

### Validation

\`\`\`bash
# Test the setup
curl localhost:8080/health
# Expected: {"status": "healthy", "uptime": 123}
\`\`\`

**Troubleshooting:**
If you see `{"status": "degraded"}`, check [specific log] for [common issue].
```

---

### Conclusion: End Strong

**Purpose**: Summarize key takeaways without being generic

**AVOID these AI-tells:**
- ❌ "In conclusion..."
- ❌ "Overall..."
- ❌ "To summarize..."
- ❌ "Looking ahead..."

**USE these patterns instead:**
- ✅ "Key Lessons from 6 Months of Testing"
- ✅ "What I'd Do Differently Next Time"
- ✅ "Three Things That Actually Matter"
- ✅ "The Bottom Line After 50+ Experiments"

**Structure:**
1. Numbered list of 3-5 key insights
2. Each with specific metric or example
3. Mention biggest surprise or unexpected finding
4. Clear next steps for readers

**Example:**
```markdown
## What Actually Matters (After 100+ Tests)

1. **Worker count sweet spot**: 12 workers gave 680 req/s vs 340 at 4 workers
2. **Memory is the bottleneck**: CPU stayed at 45% while RAM maxed out
3. **Validation catches 90% of issues**: Automated checks saved 20+ hours

The biggest surprise was [unexpected finding]. I expected [X] but found [Y]
because [reason].

**If you're implementing this**: Start with [specific step]. Focus on [critical
factor] before optimizing [less critical factor]. And test [specific scenario]
early—I learned that lesson the hard way.
```

---

## Validation Workflow

### 1. Check Humanization Score

```bash
python scripts/blog-content/humanization-validator.py --post src/posts/YYYY-MM-DD-slug.md
```

**Interpreting results:**

```
Score: 85/100 - PASS ✅

VIOLATIONS (0)
(none)

WARNINGS (1)
  [LOW] long_sentences
    Average sentence length: 22 words (max: 20)

PASSED CHECKS (6)
  ✓ first_person: Found 15 occurrences
  ✓ uncertainty: Found 8 occurrences
  ✓ specificity: Found 23 measurements
  ✓ trade_offs: Found 12 occurrences
    Depth Score: 8/10 (Very Good: Multi-option evaluation with quantified comparisons)
  ✓ concrete_details: Found 6 code blocks
  ✓ measurement_richness: 23 total measurements (+10 bonus points)
    Breakdown:
      - Percentages: 5
      - Performance Metrics: 8
      - Hardware Specs: 6
      - Time Measurements: 4
```

**What to fix:**
- **Score <75**: Missing required elements—check violations
- **Score 75-84**: Good, but could add more measurements or failure narratives
- **Score 85-94**: Excellent, ready to publish
- **Score 95+**: Outstanding, you've mastered the humanization patterns

### 2. Verify Citation Hyperlinks

```bash
python scripts/blog-research/check-citation-hyperlinks.py
```

**Requirements:**
- ALL citations must include clickable hyperlinks
- Links must point to arXiv, DOI, or authoritative sources
- No "studies show..." without links

### 3. Final Quality Checks

```bash
# Generate images
python scripts/blog-images/update-blog-images.py
python scripts/blog-images/generate-blog-hero-images.py

# Optimize images
bash scripts/optimize-blog-images.sh

# Check for broken links
# (Add your link checker command here)
```

---

## Tips for High Scores (85-95/100)

### 1. Measurements Are Gold (Target: 10+)

Track every quantitative detail from your testing:
- Hardware: CPU model, RAM amount, GPU
- Performance: req/s, latency, throughput
- Time: startup time, response time, duration
- Versions: software versions, API versions
- Percentages: improvements, success rates
- Comparisons: A vs B, before vs after

### 2. Failure Narratives Are Powerful (Bonus: +5 to +10)

Share at least one:
- Debugging story with time cost
- Mistake you made and lesson learned
- Unexpected challenge and how you solved it
- Configuration error and its impact

### 3. Deep Trade-off Analysis (Bonus: +5 to +10)

Test 3+ options with metrics:
- List each option with quantified pros/cons
- Include performance, memory, cost trade-offs
- Provide context-dependent recommendations
- Explain constraints that influenced choices

### 4. Write Like You Talk

Read your draft aloud:
- If it sounds like a textbook, simplify
- If you'd never say it in conversation, rewrite
- Add "I think", "probably", "in my experience"
- Break up long sentences

### 5. Cut the Formality

Replace:
- "utilize" → "use"
- "leverage" → "use"
- "implement" → "build" or "add"
- "facilitate" → "help" or "enable"

### 6. Be Specific, Not Generic

Replace:
- "fast performance" → "340 req/s on my i9-9900K"
- "good results" → "73% improvement over baseline"
- "recent testing" → "3 months of testing from June to September 2025"

---

## Common Mistakes

### ❌ Mistake 1: Using Em Dashes

```markdown
BAD: "The system is fast—really fast—and scales well."
GOOD: "The system is fast (really fast) and scales well."
GOOD: "The system is fast. Really fast. And it scales well."
```

### ❌ Mistake 2: Generic Conclusions

```markdown
BAD: "In conclusion, this approach offers many benefits..."
GOOD: "After 6 months of testing, the 12-worker configuration gave the best balance..."
```

### ❌ Mistake 3: Unbacked Claims

```markdown
BAD: "This dramatically improves performance."
GOOD: "This reduced latency from 340ms to 85ms—a 75% improvement."
```

### ❌ Mistake 4: Missing Context

```markdown
BAD: "I tested different configurations."
GOOD: "Over 3 months, I tested 4 different worker configurations (4, 8, 12, 16) on my Intel i9-9900K with 64GB RAM."
```

### ❌ Mistake 5: No Failure Narratives

```markdown
BAD: "I implemented the solution successfully."
GOOD: "I spent 6 hours debugging crashes before discovering I'd set memory_limit to 6MB instead of 6GB. One typo, one lost weekend."
```

---

## Quick Reference: Scoring Breakdown

| Element | Min Required | Bonus Available | How to Get Bonus |
|---------|-------------|-----------------|------------------|
| First-person | 1+ occurrences | - | "I tested", "my homelab" |
| Uncertainty | 1+ occurrences | - | "probably", "depends on", "might" |
| Measurements | 1+ occurrences | +10 points | Include 10+ quantified metrics |
| Trade-offs | 1+ occurrences | +10 points | Test 3+ options with metrics |
| Concrete details | 2+ occurrences | - | Code blocks, configs, commands |
| Failure narratives | Not required | +10 points | Debugging stories with time costs |

**Total possible:** 100 base + 30 bonus = 130 (capped at 110)

**Target ranges:**
- **75-84**: Good, ready to publish
- **85-94**: Excellent, well-crafted
- **95+**: Outstanding, exemplary

---

## Getting Help

### Validation Issues

If your score is below 75:

1. Check violations section for specific issues
2. Review the humanization checklist in the template
3. Add missing required elements (first-person, measurements, trade-offs)
4. Remove AI-tells (em dashes, semicolons, generic conclusions)

### Questions About Template

See also:
- `/docs/guides/HUMANIZATION_QUICK_REFERENCE.md` - One-page cheat sheet
- `CLAUDE.md` - Blog post creation guidelines (comprehensive)
- `/scripts/blog-content/humanization-patterns.yaml` - Scoring patterns

### Stuck on a Section

Each template section includes:
- Purpose explanation
- What to include
- Example patterns
- Why it works

Refer to these guides or ask: "How do I write a compelling [section name] for a post about [topic]?"

---

## Success Stories

**Phase 1 validation results** (October 2025):
- Average score: 87.3/100 (excellent)
- 48 of 48 posts scored ≥75/100
- Highest score: 96/100 (vulnerability management post)

**What made the difference:**
1. Rich measurements (10-20+ per post)
2. Multi-option trade-off analysis
3. Personal failure narratives
4. Specific hardware/software versions
5. Conversational tone with uncertainty

---

## Next Steps

1. Copy the template for your next post
2. Write following the section guidance
3. Run the humanization validator
4. Aim for 85+ score on first draft
5. Iterate based on feedback

**Remember:** The template is a guide, not a straitjacket. Adapt it to your topic, but keep the humanization principles: be personal, be specific, be honest, and share what you actually learned.
