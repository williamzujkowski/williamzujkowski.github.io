---
title: Blog Post Transformation Workflow
category: workflows
priority: MEDIUM
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 2000
load_when:
  - Transforming existing posts
  - Smart Brevity refinement
  - Citation enhancement
dependencies:
  - standards/humanization-standards
  - standards/citation-research
tags: [transformation, smart-brevity, refinement]
---

# Blog Post Transformation Workflow

## Module Metadata

**Category:** workflows
**Priority:** MEDIUM
**Load When:** Transforming existing posts, Smart Brevity refinement, citation enhancement
**Dependencies:** standards/humanization-standards, standards/citation-research
**Estimated Size:** ~2,000 tokens

---

## Purpose

This module documents the proven 7-phase Smart Brevity methodology for transforming existing blog posts to meet quality standards (10+ citations, 60+ bullets, 0 weak language, strong BLUF, human tone).

---

## When to Load This Module

**Load this module when:**
- Transforming existing blog posts
- Smart Brevity refinement needed
- Citation enhancement required
- Batch post improvements

**Skip this module if:**
- Creating new posts from scratch (use blog-writing.md)
- Only validating tone (use humanization-standards.md)

---

## Quick Reference

**7 Phases (Time per post: ~2 hours):**
- **A**: Pre-Analysis (15 min)
- **B**: BLUF Creation (15 min)
- **C**: Structure Transformation (40 min)
- **D**: Language Hardening (15 min)
- **E**: Citation Enhancement (20 min)
- **F**: Validation (10 min)
- **G**: Tone Validation (10 min)

**Batch 2 Results:** 2.1 → 11.3 avg citations (+440%), 23.4 → 78.1 avg bullets (+234%)

---

## Overview

For transforming existing blog posts to meet Smart Brevity standards (10+ citations, 60+ bullets, 0 weak language, strong BLUF, human tone), use the proven 7-phase methodology from Batch 2+ (validated on 8 posts, enhanced with human tone validation).

**Complete methodology documented in:** `docs/archive/2025-Q3/batch-2/CLAUDE_MD_UPDATES.md` and `docs/human-tone-integration-plan.md`

---

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

---

## Batch 2 Results (8 Posts)

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Citations | 2.1 avg | 11.3 avg | +440% |
| Bullets | 23.4 avg | 78.1 avg | +234% |
| Weak Language | 9.8 avg | 0.0 | -100% |
| Build Success | 62.5% | 100% | +60% |

---

## Swarm Orchestration Pattern

**For batch transformations (3+ posts), use multi-agent approach:**
- **Planner Agent**: Creates pre-analysis, defines strategy, validates output
- **Researcher Agent**: Finds citations (arXiv, NIST, official docs), validates claims
- **Coder Agent**: Executes transformations, integrates citations, runs validation

**Memory key structure:** `swarm/batch-X/post-Y/{pre-analysis,citations,status,validation-results}`

---

## Key Success Patterns

1. **Pre-analysis prevents scope creep** - Know targets before starting
2. **BLUF works for all post types** - Technical and personal styles both effective
3. **Strategic bulletization preserves voice** - Keep "I" statements, humor, transitions
4. **Citation research improves content** - Beyond just adding links, deepens understanding
5. **Language hardening strengthens** - Remove hedging without sterilizing personality

---

## Common Pitfalls to Avoid

- **Over-bulletizing**: Keep 2-3 sentence transitions, preserve storytelling
- **Losing personal voice**: Delete weak language, NOT first-person narrative
- **Citation overload**: One per major claim, not every sentence
- **Vague BLUF**: Start with surprising fact, quantify immediately, answer "why care?"

---

## Documentation References

- **Complete methodology**: `docs/archive/2025-Q3/batch-2/CLAUDE_MD_UPDATES.md` (40K, comprehensive guide)
- **Lessons learned**: `docs/archive/2025-Q3/batch-2/LESSONS_LEARNED.md` (36K, Batch 2 analysis)
- **Pre-analysis examples**: `docs/archive/2025-Q3/batch-2/pre-analysis/post-[1-8]-pre-analysis.md`
- **Cleanup report**: `docs/archive/2025-Q3/batch-2/CLEANUP_REPORT.md` (organization strategy)

---

## Cross-References

### Related Modules
- [humanization-standards.md](../standards/humanization-standards.md) - Tone validation (Phase G)
- [citation-research.md](../standards/citation-research.md) - Citation enhancement (Phase E)

### External References
- [docs/archive/2025-Q3/batch-2/CLAUDE_MD_UPDATES.md](../../archive/2025-Q3/batch-2/CLAUDE_MD_UPDATES.md) - Complete methodology
- [docs/human-tone-integration-plan.md](../../human-tone-integration-plan.md) - Tone validation

---

## Examples

### Example 1: Complete Transformation Workflow

```bash
# Phase A: Pre-Analysis
python scripts/blog-content/analyze-blog-content.py --post src/posts/example.md > pre-analysis.md

# Phases B-F: Apply transformations
# (manual editing with Smart Brevity principles)

# Phase G: Tone Validation
python scripts/blog-content/humanization-validator.py --post src/posts/example.md

# Result: 90/100 score, 12 citations, 78 bullets, 0 weak language
```

**Explanation:** End-to-end transformation from analysis to validation.

### Example 2: Batch Swarm Orchestration

```javascript
// Spawn 3 agents for parallel execution
Task("Planner", "Pre-analysis for 5 posts")
Task("Researcher", "Find 60 citations (12 per post)")
Task("Coder", "Execute Phases B-F for all posts")

// Memory keys: swarm/batch-3/post-{1-5}/{pre-analysis,citations,status}
// Result: 5 posts refined in ~6 hours vs ~10 hours sequential
```

**Explanation:** Swarm orchestration reduces batch transformation time by 40%.

---

## Common Pitfalls

### Pitfall 1: Skipping Pre-Analysis
**Problem:** Starting transformations without baseline metrics
**Solution:** ALWAYS complete Phase A first
**Prevention:** Create pre-analysis document before any edits

### Pitfall 2: Over-Bulletizing
**Problem:** Converting every sentence to bullets, losing flow
**Solution:** Keep 2-3 sentence transitions between bullet groups
**Prevention:** Preserve storytelling passages with first-person narrative

### Pitfall 3: Ignoring Tone Validation
**Problem:** Smart Brevity complete but content sounds AI-generated
**Solution:** Run Phase G tone validation with humanization-validator.py
**Prevention:** Check for AI tells after every batch transformation

---

## Validation

### How to Verify Correct Application

**Checklist:**
- [ ] Pre-analysis document created (Phase A)
- [ ] BLUF added with quantified impact (Phase B)
- [ ] 60+ bullets with preserved voice (Phase C)
- [ ] 0 weak language instances (Phase D)
- [ ] 10+ reputable citations with hyperlinks (Phase E)
- [ ] Build passes, metrics verified (Phase F)
- [ ] Humanization score ≥75/100 (Phase G)
- [ ] Personal stories and humor preserved

**Commands:**
```bash
# Validate structure and citations
npm run build

# Check humanization score
python scripts/blog-content/humanization-validator.py --post src/posts/[file].md

# Verify citation links
python scripts/blog-research/check-citation-hyperlinks.py
```

---

## Changelog

### Version 1.0.0 (2025-11-01)
- Initial extraction from CLAUDE.md section "Blog Post Transformation: Smart Brevity Methodology"
- Complete 7-phase workflow
- Batch 2 results and success patterns
- Examples and validation added

---

## Maintenance Notes

**Review Schedule:** Quarterly
**Last Review:** 2025-11-01
**Next Review:** 2026-02-01
**Maintainer:** Content Quality Team

---

**Parent Index:** [../../INDEX.yaml](../../INDEX.yaml)
**Category Index:** [../index.md](../index.md)
