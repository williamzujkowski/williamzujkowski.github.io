---
title: Blog Post Creation - LLM Quick Start Checklist
category: workflows
priority: HIGH
version: 1.0.0
last_updated: 2025-11-13
estimated_tokens: 800
---

# Blog Post Creation - Quick Start Checklist for LLMs

**Purpose:** Ensure all LLMs follow the correct sequence when creating blog posts.

---

## ⚠️ MANDATORY LOADING SEQUENCE

**Creating a new blog post requires loading modules in THIS EXACT ORDER:**

### Step 1: Core Foundation (MANDATORY)
```bash
Read docs/context/core/enforcement.md
Read docs/context/core/nda-compliance.md
```
**Why:** Safety checks, NDA compliance, basic rules

### Step 2: Topic Selection (MANDATORY)
```bash
Read docs/context/workflows/blog-topic-selection.md
```
**Why:** Validates topic fills gaps, scores topic, checks format diversity

**ACTION REQUIRED:**
- [ ] Score topic using 5-criteria system (0-5 each)
- [ ] Verify score ≥15/25 (minimum to proceed)
- [ ] Confirm fills critical gap OR introduces new format
- [ ] Check NDA compliance (homelab only, no work)
- [ ] Validate against content mix ratios (75/25 evergreen-trending)

**If topic scores <15/25 → STOP, choose different topic**

### Step 3: Writing Process (MANDATORY)
```bash
Read docs/context/workflows/blog-writing.md
Read docs/context/standards/writing-style.md
```
**Why:** Writing workflow, tone/voice standards

---

## 🎯 Topic Scoring System (Required)

**Score each criterion 0-5:**

| Criterion | Score | Notes |
|-----------|-------|-------|
| Personal Experience (must be 4+) | __/5 | Homelab tested, unique insights? |
| Audience Value (must be 3+) | __/5 | Solves problems, teaches skills? |
| Search Potential (nice to have 3+) | __/5 | Volume >100, difficulty <60? |
| Evergreen Longevity (prefer 4+) | __/5 | Relevant 2+ years? |
| Unique Angle (must be 3+) | __/5 | Different from existing content? |
| **TOTAL** | __/25 | **Minimum 15 required** |

---

## 🔴 Content Gaps to Fill (Priority)

**These topics need MORE posts (choose from these first):**

1. **Cloud Security** (2 posts → need 6+ more)
2. **Container Security** (3 posts → need 7+ more)
3. **Monitoring & Observability** (3 posts → need 5+ more)
4. **Python Automation** (3 posts → need 5+ more)

**Missing Formats (introduce these):**
- Multi-part series (0 → need some!)
- Tool comparisons (minimal → need more!)
- Failure stories (minimal → need more!)
- Beginner guides (few → need more!)

---

## ✅ Pre-Writing Validation

**Before starting to write, confirm:**

- [ ] Topic scored ≥15/25
- [ ] Fills identified gap OR introduces new format
- [ ] 100% homelab/public knowledge (no work/NDA content)
- [ ] Can test/demo in personal environment
- [ ] Readers can reproduce with similar hardware
- [ ] Evergreen (relevant 18+ months) OR trending (quota <25%)
- [ ] 10+ credible sources identified for citations
- [ ] Time budget reasonable (research + write + test)

---

## 📊 Content Mix Tracking

**Current Target: 75/25 Evergreen-Trending**

**Monthly quota (4 posts/month):**
- Week 1: Deep technical guide (evergreen, gap-filler)
- Week 2: Practical implementation (evergreen, hands-on)
- Week 3: Tool review/comparison (evergreen, new format)
- Week 4: Trending topic OR failure story (mixed)

**If this month already has 1 trending post → this post must be evergreen**

---

## 🚫 Common Mistakes to Avoid

❌ **Don't:**
- Start writing without loading blog-topic-selection.md
- Choose topic without scoring it
- Ignore content gaps (writing only comfortable topics)
- Reference work scenarios (NDA violation!)
- Exaggerate capabilities (e.g., "runs 70B on 24GB")
- Skip testing commands before publishing

✅ **Do:**
- Follow mandatory loading sequence
- Score topic honestly (reject if <15/25)
- Fill critical gaps first
- Frame everything through homelab lens
- Test all technical claims in personal environment
- Include 10+ citations from credible sources

---

## 📝 Quick Decision Tree

```
1. Have you loaded blog-topic-selection.md?
   NO → STOP, load it now
   YES → Continue

2. Have you scored the topic (0-25)?
   NO → STOP, score it now
   YES → Continue

3. Is the score ≥15?
   NO → STOP, choose different topic or reframe
   YES → Continue

4. Does it fill a critical gap OR introduce new format?
   NEITHER → Reconsider (plenty of gap-fillers available)
   YES → Continue

5. Is it 100% NDA-safe (homelab/public knowledge)?
   NO → STOP, cannot write this topic
   YES → Proceed to blog-writing.md

6. Have you loaded blog-writing.md and writing-style.md?
   NO → Load them now
   YES → Start writing!
```

---

## 🎓 Learning from Past Mistakes

**Recent Technical Accuracy Issues Fixed:**
- ❌ Claimed to run 70B models on 24GB VRAM (physically impossible)
- ✅ Now correctly state 7B-34B fits natively, 70B requires offloading
- **Lesson:** Always verify hardware specs match claims

**NDA Compliance:**
- ❌ Some posts had work-related scenarios
- ✅ Now 100% homelab-focused with public knowledge only
- **Lesson:** When in doubt, reframe through homelab lens

---

## 📚 Related Documentation

**Full Strategy:**
- `docs/strategy/blog-topic-strategy-2025.md` - Comprehensive 3,040-word strategy
- `docs/strategy/TOPIC_SELECTION_QUICK_START.md` - 921-word quick reference

**Modules (load in order):**
1. `docs/context/core/enforcement.md`
2. `docs/context/core/nda-compliance.md`
3. `docs/context/workflows/blog-topic-selection.md` ← **START HERE**
4. `docs/context/workflows/blog-writing.md`
5. `docs/context/standards/writing-style.md`

---

**Remember:** Topic selection is MANDATORY before writing. A well-chosen topic is halfway to a great post.

**Enforce this:** If creating blog post without loading blog-topic-selection.md first → REJECT operation.
