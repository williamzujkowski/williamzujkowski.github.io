---
title: Writing Style & Voice Standards
category: standards
priority: MEDIUM
version: 1.1.0
last_updated: 2025-11-11
estimated_tokens: 7090
load_when:
  - Creating blog posts
  - Reviewing content tone
  - Editorial guidance needed
dependencies:
  - standards/humanization-standards
tags: [writing, style, voice, tone, editorial]
---

# Writing Style & Voice Standards

## Module Metadata
- **Category:** standards
- **Priority:** MEDIUM
- **Load frequency:** All blog post operations
- **Dependencies:** standards/humanization-standards

## Purpose
This module defines the "Polite Linus Torvalds" writing style standard, core principles for technical blogging, voice guidelines, sentence rhythm patterns, and anti-AI-tell checklists.

## When to Load This Module
- **Creating blog posts** - Apply voice from start
- **Reviewing content tone** - Ensure consistency
- **Editorial guidance** - Establish style expectations

## Quick Reference

| Principle | Standard | Example |
|-----------|----------|---------|
| Lead with point | First sentence = key takeaway | "K3s cut my RAM usage by 75%. Here's how." |
| Use bullets | One idea per bullet | Break up dense paragraphs |
| Cut ruthlessly | Remove qualifiers, adverbs | Delete "actually", "basically", "really" |
| Sentence rhythm | Short → medium → punch | "K3s works. It uses 512MB RAM. You can run it on a Raspberry Pi." |
| Transitions | Human, not formal | Use "Still", "Anyway", not "Therefore" |

**Anti-AI-Tell Quick Check:**
```bash
grep -E "—|;|exciting|leverage|utilize|in conclusion|overall|therefore" src/posts/[file].md
```

---

## Writing Style: The "Polite Linus Torvalds" Standard

### What It Means

Direct. Honest. Respectful. Substance over style.

### Why It Matters

This blog shares real technical work, not corporate marketing. Readers want clarity, not fluff.

---

## Core Principles

### Lead with the Point

- First sentence = most important takeaway
- No throat-clearing
- No "In this post, I will discuss..."

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

### Use Bullets Liberally

- One idea per bullet
- Short sentences
- White space is your friend

### Cut Ruthlessly

- Remove qualifiers: "actually," "basically," "essentially"
- Delete adverbs: "very," "really," "quite"
- Kill corporate speak: "leverage," "synergy," "paradigm"

---

## "Why It Matters" Sections

Every major claim needs context:

```markdown
**Why it matters:** [One sentence explaining impact]
```

**Example:**
```markdown
K3s uses 512MB RAM vs Kubernetes' 2GB minimum.

**Why it matters:** You can run production-grade orchestration
on a Raspberry Pi without sacrificing features.
```

---

## Sentence Rhythm and Cadence

### Pattern: Short → Medium → Punch

**Examples:**
- "K3s works. It uses 512MB RAM. You can run it on a Raspberry Pi." (5-8-10 words)
- "The first test failed. Took 20 minutes to debug. Turns out I forgot sudo." (4-5-8 words)

### Avoid AI Patterns

- ❌ Perfectly parallel structures: "This improves X. This enhances Y. This optimizes Z."
- ✅ Break rhythm: "This improves X. Y gets better too. Z? Still working on it."

### Use Minimal Conjunctions

- ❌ "I tested the system, and it worked, but the performance was slow."
- ✅ "I tested the system. It worked. Performance was slow."

### Add Transitions Like a Human

**Use:** "Still," "Anyway," "That's fine," "Turns out"

**Avoid:** "Therefore," "Hence," "In conclusion," "Overall"

---

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

---

## Anti-AI-Tells Checklist

**Quick reference table:**

| Category | Remove | Replace With |
|----------|--------|--------------|
| **Punctuation** | Em dashes (—), semicolons (;) | Short sentences or commas |
| **Transitions** | "In conclusion," "Overall," "Therefore" | "Anyway," "That's the gist," "Still" |
| **Emotion** | "exciting," "remarkable," "thrilled" | "useful," "surprising," or remove |
| **Vocabulary** | "utilize," "leverage," "paradigm" | "use," "try," "model" |

**Quick validation:**
```bash
# Check for AI tells in your post
grep -E "—|;|exciting|leverage|utilize|in conclusion|overall|therefore" src/posts/[file].md
```

**Complete Phase 1 methodology:** See [humanization-standards.md](humanization-standards.md#phase-1-ai-tell-removal) for full requirements, patterns, and enforcement rules.

---

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

---

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

---

## Blog Post Structure Template

1. **Hook**: Start with story, question, or interesting fact
2. **Context**: Why writing about this now
3. **Main Content**: Core information
4. **Personal Reflection**: What this means personally
5. **Invitation**: Question or thought for readers

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

---

## Remember

- Perfect is the enemy of published
- Voice will evolve—that's good
- Not every post needs to be epic
- It's okay to have opinions
- Writing gets easier with practice

---

## Humanization Techniques

**Complete methodology:** See [humanization-standards.md](humanization-standards.md#the-7-phase-humanization-framework) for the authoritative 7-phase framework including:
- Personal voice addition techniques (Phase 2: 8+ first-person statements)
- Concrete measurement patterns (Phase 3: 15+ measurements, 8 types)
- Uncertainty markers (Phase 4: 25 patterns)
- Failure narrative structure (Phase 5: 5-7 stories)
- Trade-off discussion formulas (Phase 6: 10+ balanced statements)
- Edge case handling (NDA-sensitive, technical deep-dives, tutorials)

**Quick reference techniques:**

| Technique | Example | Use When |
|-----------|---------|----------|
| **Hesitation** | "At first I thought it was DNS. It wasn't." | Debugging stories |
| **Reflection** | "Looking back, that assumption was wrong." | Lessons learned |
| **Micro-failure** | "The first fix made it worse." | Tutorials |
| **Concrete detail** | "Took 17 minutes to compile." | Technical posts |
| **Temporal anchor** | "As of October 2025…" | Current state |
| **Contradiction** | "I hate YAML. But it works." | Opinions |

---

## Cross-References

### Related Modules
- [standards/humanization-standards](humanization-standards.md) - 7-phase humanization methodology
- [workflows/blog-writing](../workflows/blog-writing.md) - Blog post creation workflow
- [workflows/blog-transformation](../workflows/blog-transformation.md) - Smart Brevity methodology

### External References
- **Humanization Validator:** `scripts/blog-content/humanization-validator.py`
- **Pattern Definitions:** `scripts/blog-content/humanization-patterns.yaml`

---

## Examples

### Example 1: Excellent Writing Style (Polite Linus)

```markdown
Docker cut my homelab deployment time by 70%. Here's what worked and what didn't.

The first approach failed. I tried Docker Swarm. Too complex for 3 nodes.

K3s worked better. Installed in 5 minutes. Uses 512MB RAM vs Kubernetes' 2GB minimum.

**Why it matters:** You can run production-grade orchestration on a Raspberry Pi
without sacrificing features.

Your mileage may vary. I tested on Ubuntu 24.04 with 64GB RAM. Still, K3s
handles my 47 containers without breaking a sweat.
```

**Analysis:** Direct opening, sentence rhythm varies (short/medium/long), first-person narrative, concrete measurements (70%, 5 minutes, 512MB), trade-off acknowledged (complex for 3 nodes), uncertainty marker (your mileage may vary), personal context (my testing).

**See also:** [humanization-standards.md](humanization-standards.md#examples) for additional examples with validation scoring breakdowns.

---

## Common Pitfalls

### Pitfall 1: Corporate Voice Creep
**Problem:** Using "leverage," "utilize," "synergize" in technical writing
**Solution:** Find/replace with "use," "try," "combine"
**Prevention:** Run anti-AI-tell check before committing

### Pitfall 2: Perfect Parallel Structures
**Problem:** "This improves X. This enhances Y. This optimizes Z."
**Solution:** Break rhythm: "This improves X. Y gets better too. Z? Still working on it."
**Prevention:** Vary sentence length and structure intentionally

### Pitfall 3: Missing Personal Voice
**Problem:** Generic technical documentation tone
**Solution:** Add first-person narrative, homelab stories, failures
**Prevention:** Apply Phase 2 of humanization methodology

---

## Validation

### Style Validation Checklist

- [ ] No em dashes (—) or semicolons (;) outside code blocks
- [ ] No AI transitions ("in conclusion," "overall," "therefore")
- [ ] No corporate jargon ("leverage," "utilize," "facilitate")
- [ ] Sentence rhythm varies (not all same length)
- [ ] First-person narrative present (8+ "I" statements)
- [ ] Concrete details included (measurements, timestamps)
- [ ] Uncertainty markers present (6+ "probably," "might," etc.)
- [ ] Trade-offs acknowledged (10+ balanced statements)

### Validation Commands

**Complete validation workflow:** See [humanization-standards.md](humanization-standards.md#validation) for full command reference, expected output, and score interpretation.

```bash
# Check for AI tells (quick)
grep -E "—|;|exciting|leverage|utilize|in conclusion|overall|therefore" src/posts/[file].md
```

---

## Changelog

### Version 1.1.0 (2025-11-11)
- **Consolidation with humanization-standards.md:** Replaced duplicate content with cross-references
  - Anti-AI-Tell Checklist: Kept quick reference table + added cross-reference to Phase 1 methodology
  - Humanization Techniques: Enhanced cross-reference with specific phase targets
  - Example Analysis: Added cross-reference to additional examples
- Updated estimated_tokens from 2000 to 7090 (accurate measurement)
- Token savings: ~370 tokens via consolidation (reduced duplication by ~5%)
- Established clear ownership: writing-style = editorial voice, humanization-standards = validation methodology

### Version 1.0.0 (2025-11-01)
- Initial extraction from CLAUDE.md v3.0.0
- "Polite Linus Torvalds" standard documented
- Core principles established
- Sentence rhythm patterns defined
- Anti-AI-tell checklist included
- Healthy AI skepticism section added

---

## Maintenance Notes

**Review Schedule:** Quarterly
**Last Review:** 2025-11-01
**Next Review:** 2026-02-01
**Maintainer:** Editorial quality agent

**Update Triggers:**
- New AI-tell patterns discovered
- Voice evolution (gradual)
- Reader feedback on tone
- New anti-pattern identification

---

**Parent Index:** [../../INDEX.yaml](../../INDEX.yaml)
**Category Index:** [../index.md](../index.md)
