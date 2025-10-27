# Blog Post Refactoring Template

Use this template for every post refactoring to ensure consistency and quality.

---

## Post Information

**Filename**: [filename.md]
**Current Word Count**: [X words]
**Target Word Count**: [Y words] ([Z]% reduction)
**Compliance Score**: [X/100] → Target: ≥80/100
**Priority Tier**: [1/2/3]

**Violations Identified**:
- [ ] Missing BLUF
- [ ] Excessive weak language ([N] instances)
- [ ] Insufficient bullets ([N] < 10)
- [ ] Long paragraphs (avg [N] sentences)
- [ ] Missing AI skepticism (for AI posts)

---

## Refactoring Checklist

### Phase 1: Analysis (5 minutes)

- [ ] Read entire post
- [ ] Identify main argument/value proposition
- [ ] Note sections that can be condensed
- [ ] List weak language patterns to fix
- [ ] Check if AI-related (needs skepticism)
- [ ] Verify citations are present

### Phase 2: Structure (15-30 minutes)

#### BLUF Addition
- [ ] Write 2-3 sentence BLUF
- [ ] Format: "One big thing. How it works. Why it matters."
- [ ] Place immediately after frontmatter
- [ ] Verify word count ≤60 words

**Example BLUF**:
```markdown
Progressive loading cuts LLM tokens by 98%. Load context on-demand based on
file types and task requirements. Saves costs, reduces latency, maintains accuracy.
```

#### Section Restructuring
- [ ] Ensure clear H2/H3 hierarchy
- [ ] Add "Why it matters" subsections where needed
- [ ] Identify paragraphs → bullet conversions
- [ ] Move examples to dedicated sections

### Phase 3: Language Cleanup (15-20 minutes)

#### Remove Weak Language
**Find and replace patterns**:

| Weak | Strong |
|------|--------|
| should | must (requirements) OR omit (suggestions) |
| could | can OR will/won't |
| might | may OR will/won't |
| perhaps | [delete or be specific] |
| maybe | [delete or be specific] |
| possibly | [delete or be specific] |
| essentially | [delete] |
| basically | [delete] |
| actually | [delete] |
| generally | [delete or be specific] |
| typically | [delete or be specific] |
| very | [delete or find stronger word] |
| really | [delete or find stronger word] |
| quite | [delete] |
| rather | [delete] |

#### Remove Throat-Clearing
**Delete these patterns**:
- "In this post, I will..."
- "In this section, we'll discuss..."
- "It is important to note that..."
- "Let me explain..."
- "Let's dive into..."
- "As I/we mentioned..."

**Before**:
```markdown
In this section, I will discuss how to implement zero trust architecture.
It is important to note that this requires careful planning.
```

**After**:
```markdown
Implementing zero trust requires careful planning. Start with network segmentation.
```

### Phase 4: Content Transformation (30-45 minutes)

#### Paragraphs → Bullets
**Convert verbose paragraphs to concise bullets**:

**Before**:
```markdown
There are several key advantages to using this approach. First, it reduces
complexity by eliminating unnecessary components. Second, it improves
performance by optimizing resource usage. Third, it enhances security
through better isolation.
```

**After**:
```markdown
**Advantages**:
• Reduces complexity—eliminates unnecessary components
• Improves performance—optimizes resource usage
• Enhances security—better isolation
```

**Target**: 15-20 bullets total per post

#### Add Comparative Sections
For technical posts, add "What Works / What Doesn't":

```markdown
## What Works / What Doesn't

**Works**:
✅ Specific success pattern with context
✅ Another proven approach
✅ Third validated method

**Doesn't work**:
❌ Common failure mode and why
❌ Another pitfall to avoid
❌ Third anti-pattern

**Why**: [Brief 1-2 sentence explanation]
```

### Phase 5: AI Skepticism (AI posts only, 15-20 minutes)

#### Add Reality Check Section
**For all AI/ML posts, include**:

```markdown
## Reality Check

**The hype**: [What marketing/vendors claim]

**The truth**: [What actually works in practice]

**Limitations**:
• Known failure mode 1 (with specific example)
• Known failure mode 2 (with specific example)
• Known failure mode 3 (with specific example)

**When to use**: [Specific scenarios where this works]

**When NOT to use**: [Specific scenarios to avoid]

**Reproducibility**: [Link to code/data or explain verification method]
```

#### Fix Anthropomorphization
**Replace AI-as-human language**:

| Anthropomorphic | Accurate |
|-----------------|----------|
| AI thinks | Model predicts |
| AI understands | Model processes |
| AI knows | Model is trained on |
| AI learns | Model adjusts weights based on |
| AI decides | Model classifies/selects |
| AI wants | Model optimizes for |
| AI believes | Model outputs |

#### Add Benchmark Context
**Never cite bare statistics**:

**Before**:
```markdown
The model achieves 95% accuracy.
```

**After**:
```markdown
The model achieves 95% accuracy on GLUE benchmark (sample size: 10K examples,
task: sentiment classification, baseline: 87%). Note: Performance degrades
to 78% on domain-shifted data.
```

### Phase 6: Technical Accuracy (10-15 minutes)

- [ ] Verify all code blocks still valid
- [ ] Check all citations still work
- [ ] Ensure image references correct
- [ ] Validate technical claims against sources
- [ ] Test example commands if present

### Phase 7: Final Polish (10 minutes)

#### Word Count Check
- [ ] Count final words: [X words]
- [ ] Verify ≥1,400 words (minimum for 6-minute read)
- [ ] Verify reduction meets target ([Y]%)

#### Compliance Validation
- [ ] BLUF present and concise
- [ ] Weak language <5 instances
- [ ] Bullets ≥10 total
- [ ] Paragraphs average ≤5 sentences
- [ ] AI skepticism present (for AI posts)

#### Reading Flow
- [ ] Read entire post aloud
- [ ] Check for awkward transitions
- [ ] Verify examples support main points
- [ ] Ensure conclusion reinforces BLUF

---

## Before/After Metrics

Document improvements:

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Word count | [X] | [Y] | [Z]% reduction |
| Compliance score | [X]/100 | [Y]/100 | +[Z] points |
| Weak language | [X] instances | [Y] instances | -[Z] instances |
| Bullet count | [X] | [Y] | +[Z] bullets |
| Paragraph avg | [X] sentences | [Y] sentences | -[Z] sentences |
| BLUF | ❌ | ✅ | Added |
| AI skepticism | ❌ | ✅ | Added |

---

## Common Patterns to Fix

### Pattern 1: Verbose Introductions
**Before**:
```markdown
I remember when I first started exploring this topic. It was fascinating
to discover all the different approaches and methodologies that people
have developed over the years. In this post, I want to share what I've
learned about...
```

**After**:
```markdown
[Direct BLUF about the topic]
```

### Pattern 2: Apologetic Language
**Before**:
```markdown
This might not work for everyone, but you could try this approach if you
want. It's just one possible solution among many.
```

**After**:
```markdown
This approach works for X scenario. Use it when Y condition exists.
```

### Pattern 3: Vague Claims
**Before**:
```markdown
Studies show that this technique can improve performance significantly.
Many researchers have found positive results.
```

**After**:
```markdown
[Stanford 2024 study](https://...) shows 23% latency reduction (N=1,000 trials,
p<0.01). Reproducible with [this setup](https://...).
```

### Pattern 4: Buried Lessons
**Before**:
```markdown
Throughout this project, I learned several things. The first thing I
learned was... Another thing that became apparent was... I also discovered...
```

**After**:
```markdown
## Lessons Learned

• Specific lesson 1 with outcome
• Specific lesson 2 with outcome
• Specific lesson 3 with outcome
```

---

## Quality Gates

**Do NOT proceed to next phase until current phase passes**:

✅ **Phase 1**: Clear understanding of post value proposition
✅ **Phase 2**: BLUF written and approved, structure clear
✅ **Phase 3**: All weak language removed or justified
✅ **Phase 4**: Paragraph→bullet conversions complete
✅ **Phase 5**: AI skepticism section complete (if applicable)
✅ **Phase 6**: Technical accuracy verified
✅ **Phase 7**: All metrics meet targets

---

## Example: Full Refactoring

### Before (Tier 1 Post)
```markdown
---
title: "Understanding Prompt Engineering"
date: 2024-04-19
---

I remember my first attempts at prompt engineering. It was really quite
challenging to figure out how to get the model to understand what I wanted.
In this post, I will discuss the various techniques that you should consider
when working with LLMs.

Prompt engineering is essentially about learning how to communicate effectively
with AI systems. Basically, you need to provide clear instructions. This is
something that could potentially improve your results significantly.

There are several approaches you might want to try. First, you could use
role-based prompting. This is where you tell the AI to act as a specific
character or expert. Another thing you could do is provide examples of what
you want. This generally helps the model understand the pattern.
```

**Metrics**: 140 words, 0 bullets, compliance: 40/100

### After (Smart Brevity)
```markdown
---
title: "Mastering Prompt Engineering: Programming with Words"
date: 2024-04-19
---

Prompt engineering is programming with words. Master these patterns to control
LLM outputs. Get 10x better results with structured prompts.

## Core Patterns

**Role-based prompting**:
• Define expertise: "You are a Python expert reviewing code"
• Set constraints: "Focus on security, ignore style"
• Specify format: "Return JSON with findings array"

**Few-shot examples**:
• Show 2-3 input→output pairs
• Model infers pattern
• Works for classification, transformation, generation

**Chain-of-thought**:
• Force reasoning steps: "Let's think step by step"
• Improves accuracy on complex tasks
• Increases token usage 2-3x

## What Works / What Doesn't

**Works**:
✅ Specific constraints: "Max 100 words" beats "Be concise"
✅ Examples: Show don't tell
✅ Temperature=0 for consistency

**Doesn't work**:
❌ Vague instructions: "Be creative"
❌ Assuming context: Model has no memory between calls
❌ Over-prompting: >500 words rarely helps

**Why**: LLMs pattern-match. Give clear patterns.

## Reality Check

**The hype**: "Prompt engineering replaces programming"

**The truth**: Prompting is programming—just a different interface. Same
debugging required.

**Limitations**:
• Inconsistent outputs—same prompt ≠ same result
• Hallucinations—model invents plausible-sounding nonsense
• Context limits—can't process infinite examples

**When NOT to use**: Deterministic tasks (use code), high-stakes decisions
(verify everything), real-time systems (latency varies).

## Lessons Learned

• Start simple—add complexity only when needed
• Version your prompts—track what works
• Validate outputs—never trust blindly

## Further Reading

• [OpenAI Prompt Engineering Guide](https://...)
• [Anthropic Prompt Library](https://...)
• [Prompt Papers Collection](https://...)
```

**Metrics**: 280 words (2x), 18 bullets, compliance: 90/100

**Improvements**:
- Added BLUF
- Converted paragraphs to bullets
- Removed all weak language
- Added AI skepticism section
- Added "What Works/Doesn't" section
- Doubled value in 2x words (original was 1,879 words with less content)

---

## Refactoring Notes

Use this section to document:
- Specific challenges encountered
- Decisions made (and why)
- Content moved or removed
- Citations added or updated
- Images adjusted

---

**End of Refactoring Template**

**Usage**: Copy this template for each post, fill in the blanks, follow the checklist.
