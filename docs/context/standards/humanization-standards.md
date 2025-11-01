---
title: Humanization Standards & Validation
category: standards
priority: HIGH
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 2500
load_when:
  - Creating blog posts
  - Refining existing posts
  - Pre-commit validation
  - Content review
dependencies:
  - core/enforcement
  - workflows/blog-writing
tags: [humanization, validation, tone, voice, authenticity]
---

# Humanization Standards & Validation

## Module Metadata
- **Category:** standards
- **Priority:** HIGH
- **Load frequency:** Every blog post operation
- **Dependencies:** core/enforcement, workflows/blog-writing

## Purpose
This module defines the 7-phase humanization methodology and validation standards that ensure all blog content sounds authentically human, not AI-generated. Includes pre-commit enforcement, scoring tiers, and validator v2.0 documentation.

## When to Load This Module
- **Creating new blog posts** - Apply humanization from start
- **Refining existing posts** - Transform AI-like content
- **Pre-commit validation** - Automated quality gates
- **Content review** - Assess portfolio quality

## Quick Reference

| Scoring Tier | Score Range | Action Required | Effort |
|--------------|-------------|-----------------|--------|
| Failing | 0-59 | Full 7-phase refinement | 2-4 hours |
| Needs Improvement | 60-74 | Targeted refinement (3-5 phases) | 1-2 hours |
| Good | 75-89 | Polish to excellent tier | 30-60 min |
| Excellent | 90-100 | Maintain, minimal tweaks | 10-15 min |

**Minimum Requirements:**
- ≥75/100 to pass pre-commit validation
- ≥90/100 for excellent tier (target for all posts)
- 0 high-severity violations (em dashes, semicolons, AI phrases)
- 8+ first-person statements
- 6+ uncertainty phrases
- 10+ trade-off discussions
- 15+ concrete measurements

---

## Overview

This blog uses a proven 7-phase humanization methodology to ensure all content sounds authentically human, not AI-generated. The system has been battle-tested across 6+ batches of post refinements, achieving a **48.8% → 94.5% passing rate** transformation.

**Key Achievements:**
- 52 of 55 posts (94.5%) now pass humanization validation (≥75/100)
- 40 posts (72.7%) achieve excellent scores (≥90/100)
- 20 posts (36.4%) reach perfect scores (100/100)
- Zero new AI-tell violations introduced
- Maintained 100% NDA compliance throughout

**Enforcement:**
Pre-commit hooks automatically validate all blog posts using `humanization-validator.py`. Posts scoring <75/100 are **rejected** until refined. See `.git/hooks/pre-commit` for implementation.

---

## Humanization Validator v2.0

**Version:** 2.0.0 (October 2025)
**Performance:** 155x faster with batch processing (0.74s for 57 posts)
**Scoring:** Enhanced with measurement bonuses (up to +10 points)
**Location:** `scripts/blog-content/humanization-validator.py`

### Quick Commands

```bash
# Single post validation
python scripts/blog-content/humanization-validator.py --post src/posts/example.md

# Batch validate all posts (FAST!)
python scripts/blog-content/humanization-validator.py --batch

# Find posts needing attention
python scripts/blog-content/humanization-validator.py --batch --filter-below 90

# Save monthly report
python scripts/blog-content/humanization-validator.py --batch --save-report reports/monthly-$(date +%Y-%m).json

# Compare with last month
python scripts/blog-content/humanization-validator.py --batch --compare reports/monthly-2025-09.json
```

### New Features in v2.0

#### 1. Measurement Detection (+10 bonus for 10+ measurements)

Automatically detects 8 types of concrete measurements:

- **Percentages:** "73% improvement", "25.5% faster"
- **Multipliers:** "2.1x faster", "4x speedup"
- **Comparisons:** "X vs Y", "from 100ms to 50ms"
- **Performance:** "3.2 seconds", "1,000 req/s"
- **Hardware:** "64GB RAM", "Intel i9-9900K", "RTX 3090"
- **Time:** "3 hours", "2 weeks", "5 minutes"
- **Data Sizes:** "48,000 lines", "12 projects"
- **Experimental:** "tested with 50 samples", "measured over 3 months"

**Bonus Scoring:** +5 for 5-9 measurements, +10 for 10+

**Why it matters:** Measurements prove you did the work. Generic posts say "faster," specific posts say "73% faster after 3 weeks testing."

#### 2. Failure Narrative Scoring (0-10 subscore)

Detects authentic failure stories across 6 categories:

- Bug admissions, debugging stories, learning from failure
- Time costs, explicit mistakes, recovery narratives
- Weighted scoring (debugging: 2.0x, admissions: 1.5x)

**Example patterns detected:**
```markdown
✅ "I spent 6 hours debugging this issue..."
✅ "The first fix made it worse..."
✅ "After 4 failed attempts, I discovered..."
✅ "This mistake cost me 2 days..."
```

**Why it matters:** Only humans make mistakes. Admitting failures proves authenticity.

#### 3. Trade-off Depth Analysis (0-11 depth score)

Analyzes trade-off discussion quality:

- Multi-option evaluation (tested 4, 8, 12, 16 heads)
- Constraint discussion, nuanced conclusions
- Quantified comparisons, context-dependent recommendations

**Example patterns detected:**
```markdown
✅ "K3s uses 512MB RAM vs Kubernetes' 2GB minimum."
✅ "This works for edge deployments. But production needs full K8s."
✅ "Tested 4, 8, 12, 16 attention heads. 8 performed best for my use case."
```

**Why it matters:** AI overstates benefits. Humans acknowledge costs.

#### 4. Uncertainty Patterns (expanded to 25)

Now detects 25 uncertainty markers:

- Hedging: "might be", "could be", "tends to"
- Caveats: "in my experience", "Your mileage may vary"
- Admissions: "I'm not sure if", "unclear whether"
- Future: "will probably", "might eventually"

**Why it matters:** AI generates absolute statements. Humans express uncertainty.

#### 5. Batch Processing (155x faster)

- Parallel processing with multiprocessing
- Progress indicators with ETA
- Multiple output formats (summary, JSON, detailed)
- Report comparison for trend analysis

**Performance comparison:**
- **v1.0 (sequential):** 115 seconds for 57 posts
- **v2.0 (batch):** 0.74 seconds for 57 posts
- **Speedup:** 155x faster

---

## The 7-Phase Humanization Framework

This section provides a condensed overview of each phase. For complete methodology with examples and swarm orchestration patterns, see batch completion reports in `docs/reports/`.

### Phase 1: AI-Tell Removal

**Objective:** Eliminate punctuation and language patterns that signal AI authorship

**Target:** 0 violations

**Key Patterns to Remove:**
- **Em dashes (—):** Replace with commas or split into two sentences
- **Semicolons (;):** Use periods (except in code blocks)
- **AI phrases:** "in conclusion," "overall," "in summary," "therefore"
- **Hype words:** "exciting," "remarkable," "revolutionary," "cutting-edge"
- **Corporate jargon:** "leverage" → "use," "utilize" → "use," "facilitate" → "help"

**Quick Check:**
```bash
grep -E "—|;|in conclusion|overall|leverage|exciting" src/posts/[file].md
```

**Why it matters:** These tells are the fastest way readers identify AI-generated content. Eliminate first.

---

### Phase 2: Personal Voice Addition

**Objective:** Ground content in authentic personal experience

**Target:** 8+ first-person statements throughout post

**Required Elements:**
- First-person narrative: "I tested," "I discovered," "I tried"
- Homelab stories: 5-7 specific experiments or incidents
- Personal framing: "In my homelab," "My setup," "My experience with"

**Examples:**
```markdown
✅ "I tested K3s on 3 Raspberry Pi 4s over 2 weeks."
✅ "My RTX 3090 handled 22.1GB VRAM during inference."
✅ "I made the mistake of skipping input validation."
```

**Distribution:** Every major section should include personal narrative.

**Why it matters:** Generic advice sounds AI-generated. Personal stories prove you've done the work.

---

### Phase 3: Concrete Measurement Addition

**Objective:** Replace vague claims with specific, verifiable metrics

**Target:** 15+ specific measurements per post

**Measurement Types:**
- **Technical metrics:** "22.1GB VRAM," "147ms latency," "3.2TB storage"
- **Time investments:** "Took 17 minutes to compile," "2 hours debugging PATH issues"
- **Iteration counts:** "After 4 failed attempts," "Tested 312 CVEs," "87 violations found"
- **Quantified outcomes:** "73% improvement," "178 CVEs detected," "Reduced scan time from 147s to 12s"

**Examples:**
```markdown
✅ "K3s uses 512MB RAM vs Kubernetes' 2GB minimum."
✅ "Scanned 178 CVEs across 47 containers in 8 seconds."
✅ "First test failed. Second crashed after 23 minutes. Third worked."
```

**Pattern:** Every major claim needs a number. No vague "faster" or "better" without data.

**Why it matters:** Specific measurements prove you tested this yourself, not just summarized documentation.

---

### Phase 4: Uncertainty Addition

**Objective:** Demonstrate nuanced thinking by acknowledging knowledge gaps

**Target:** 6-8+ natural uncertainty markers per post

**Uncertainty Patterns:**
- **Probabilistic language:** "probably," "likely," "might," "seems to"
- **Conditional statements:** "depends on," "in my case," "at least in my testing"
- **Honest caveats:** "I think," "I'm not certain," "YMMV" (your mileage may vary)

**Placement Strategy:**
- After technical claims: "This probably depends on your kernel version."
- During recommendations: "K3s likely works better for edge deployments."
- In conclusions: "These results seem consistent, but more testing needed."

**Examples:**
```markdown
✅ "Your mileage may vary depending on hardware."
✅ "This probably works on most distributions, but I tested on Ubuntu 24.04."
✅ "Seems like DNS caching was the issue, though I'm not certain."
```

**Why it matters:** AI generates absolute statements. Humans express uncertainty.

---

### Phase 5: Failure Narrative Addition

**Objective:** Share authentic failures to build credibility and provide learning value

**Target:** 5-7 genuine failure stories per post

**Failure Story Structure:**
1. **What I tried:** Specific action taken
2. **What broke:** Concrete consequence
3. **How I fixed it:** Solution and iteration count
4. **Lesson learned:** Takeaway for readers

**Example Pattern:**
```markdown
✅ "I tried privileged containers for quick testing.
   Bad idea. Container escaped to host in 3 minutes.
   Took 4 attempts to configure AppArmor profiles correctly.
   Now I test in isolated VMs first."
```

**Failure Categories:**
- Configuration mistakes
- Security incidents (in homelab)
- Performance degradations
- Time wasted on wrong approaches
- Breaking changes during upgrades

**Why it matters:** Only humans make mistakes. Sharing failures proves authenticity.

---

### Phase 6: Trade-off Discussion Addition

**Objective:** Demonstrate balanced expertise by acknowledging costs and limitations

**Target:** 10+ balanced perspective statements per post

**Trade-off Formula:** `[Benefit] yet/but/however [Cost]`

**Examples:**
```markdown
✅ "K3s reduces RAM usage, yet requires SQLite expertise."
✅ "Container security improves with AppArmor. But profiles break frequently."
✅ "EPSS prioritization saves time. However, API rate limits slow automation."
```

**Trade-off Connectors:**
- "but," "yet," "however," "though," "still"
- "on the other hand," "the downside is," "the problem with"
- "doesn't work well for," "struggles with," "limitation is"

**Distribution:** Every recommendation should include at least one trade-off.

**Why it matters:** AI overstates benefits. Humans acknowledge costs.

---

### Phase 7: Final Validation

**Objective:** Verify all humanization requirements are met before publishing

**Target:** ≥75/100 passing score (≥90/100 excellent tier)

**Validation Command:**
```bash
python scripts/blog-content/humanization-validator.py --post src/posts/[file].md
```

**Pre-Commit Enforcement:**
Pre-commit hooks automatically run validation. Posts scoring <75/100 are rejected:
```bash
# .git/hooks/pre-commit runs:
python scripts/blog-content/humanization-validator.py --post "$file" --min-score 75
```

**Validation Checklist:**
- [ ] Zero high-severity violations (em dashes, semicolons, AI phrases)
- [ ] All required patterns present (first-person, uncertainty, measurements, trade-offs)
- [ ] Sentiment score balanced (<1.2 threshold)
- [ ] Sentence variety confirmed (3+ short sentences)
- [ ] Paragraph structure varies

**Why it matters:** Manual review misses patterns. Automated validation catches all AI-tells.

---

## Edge Cases

### Career/NDA-Sensitive Posts
- Lower personal narrative threshold (60-70% vs 80%+)
- Time buffering required ("years ago")
- Homelab substitution for work examples

### Technical Deep-Dives
- Higher measurement requirement (20-30+ vs 15+)
- Academic tone acceptable for precision
- Lower personal narrative (50-60%) if compensated by measurements

### Tutorial/How-To Posts
- Higher failure narrative emphasis (80-90% of sections)
- Every technique needs trade-off
- Personal testing framing for every step

### Security/Vulnerability Posts
- 90-day minimum age for CVE discussion
- CVSS scores contextualized (never score alone)
- Homelab testing attribution required

### Meta/Process Posts
- Inherently personal (90-95% personal narrative)
- Iteration documentation critical
- Self-awareness acceptable
- Lower measurement requirement (8-10 vs 15+)

---

## Cross-References

### Related Modules
- [core/enforcement](../core/enforcement.md) - Pre-commit hook enforcement
- [workflows/blog-writing](../workflows/blog-writing.md) - Blog post creation workflow
- [workflows/blog-transformation](../workflows/blog-transformation.md) - Smart Brevity methodology

### External References
- **Validator Script:** `scripts/blog-content/humanization-validator.py`
- **Pattern Definitions:** `scripts/blog-content/humanization-patterns.yaml`
- **Batch 6 Report:** `docs/reports/batch-6-completion-report.md`
- **Complete Methodology:** `docs/HUMANIZATION_VALIDATION.md`

---

## Examples

### Example 1: Excellent Content (95/100 score)

```markdown
I spent 6 hours debugging this issue and discovered it was a simple
misconfiguration. The performance improved from 340ms to 85ms (4x faster)
once I fixed it. In retrospect, I should have checked the logs first,
but I learned the hard way that assumptions are expensive. Your mileage
may vary depending on your setup.
```

**Analysis:** Contains measurements (6 hours, 340ms→85ms, 4x), failure story (debugging), uncertainty (should have, mileage may vary), first-person (I spent, I discovered).

---

## Common Pitfalls

### Pitfall 1: Over-Bulletizing
**Problem:** Converting entire post to bullets loses narrative flow
**Solution:** Keep 2-3 sentence transitions, preserve storytelling
**Prevention:** Strategic bullet usage, not blanket conversion

### Pitfall 2: Losing Personal Voice
**Problem:** Deleting weak language also removes first-person narrative
**Solution:** Keep "I" statements, humor, transitions
**Prevention:** Target only hedging words, not personal pronouns

### Pitfall 3: Vague BLUF
**Problem:** Opening lacks concrete hook
**Solution:** Start with surprising fact, quantify immediately
**Prevention:** Use "why care?" test before writing

---

## Validation

### Validation Commands

```bash
# Single post validation
python scripts/blog-content/humanization-validator.py --post src/posts/example.md

# Batch validate all posts
python scripts/blog-content/humanization-validator.py --batch

# Find posts below threshold
python scripts/blog-content/humanization-validator.py --batch --filter-below 75

# Generate monthly report
python scripts/blog-content/humanization-validator.py --batch --save-report reports/monthly-$(date +%Y-%m).json

# Compare with previous month
python scripts/blog-content/humanization-validator.py --batch --compare reports/monthly-2025-09.json
```

### Expected Output

```
Score: 82/100 - PASS

VIOLATIONS (1)
  [HIGH] banned_token
    Em dashes are AI-tells. Use commas or split into two sentences.
    Found: 2 occurrence(s)

PASSED CHECKS (6)
  ✓ first_person: Found 8 (required: 1)
  ✓ uncertainty: Found 7 (required: 1)
  ✓ trade_offs: Found 15 (required: 1)
  ✓ specificity: Found 22 (required: 1)
  ✓ concrete_details: Found 7 (required: 2)
  ✓ sentiment_balance: 0.8 (threshold: 1.2)

SCORE BREAKDOWN:
  Base score: 72
  Measurement bonus: +10 (detected 15 measurements)
  Total: 82/100
```

---

## Changelog

### Version 1.0.0 (2025-11-01)
- Initial extraction from CLAUDE.md v3.0.0
- Complete humanization methodology documented
- Validator v2.0 features included
- 7-phase framework condensed
- Edge cases documented
- Pre-commit enforcement explained

---

## Maintenance Notes

**Review Schedule:** Monthly
**Last Review:** 2025-11-01
**Next Review:** 2025-12-01
**Maintainer:** Content quality agent

**Update Triggers:**
- New validator features added
- Scoring thresholds change
- New AI-tell patterns discovered
- Edge case validation adjustments

---

**Parent Index:** [../../INDEX.yaml](../../INDEX.yaml)
**Category Index:** [../index.md](../index.md)
