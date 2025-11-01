---
title: NDA Compliance & Content Boundaries
category: core
priority: HIGH
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 1200
load_when:
  - Writing blog posts
  - Creating content mentioning work/career
  - Discussing security topics
  - Referencing professional experience
dependencies: []
tags: [security, privacy, boundaries, nda, career, family]
---

# NDA Compliance & Content Boundaries

## Purpose
This module defines **strict boundaries** for content creation to ensure 100% NDA compliance and personal privacy protection. All blog posts, documentation, and public content MUST adhere to these rules to protect career, clearance, and family safety.

## When to Load This Module
- **Before writing any blog post** - Verify no NDA violations
- **When referencing professional experience** - Use safe patterns only
- **When discussing security topics** - Homelab attribution required
- **When mentioning family** - Privacy protection mandatory

## Quick Reference

### NEVER Discuss
- Current work incidents (minimum 2-3 year buffer)
- Specific government systems or agencies
- Active vulnerabilities at work
- Timeline-specific work events
- Team members or organizational structure

### ALWAYS Use
- "Years ago, I learned..." (vague timeframes)
- "In my homelab..." (personal projects)
- "Research suggests..." (academic framing)
- "A common pattern..." (hypothetical)

---

## Government Work Security Guidelines

**Your clearance and career matter more than a blog post. When in doubt, leave it out.**

### CRITICAL: What NEVER to Discuss

- **Current work incidents** (minimum 2-3 year buffer)
- **Specific government systems**
- **Active vulnerabilities at work**
- **Timeline-specific work events**
- **Team members or organizational structure**

### Safe Pattern Examples

✅ **Safe patterns:**
```markdown
✅ "In my homelab, I discovered X vulnerability in Y."
✅ "Years ago, I worked on systems that faced Z challenge."
✅ "Research shows this attack pattern is common."
```

❌ **Unsafe patterns:**
```markdown
❌ "Last month at work..."
❌ "My current employer uses..."
❌ "We recently discovered..."
```

### Professional Content Guidelines

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

## Personal & Family Information

### ACCURATE FAMILY FACTS

- **Children:** ONE child (son)
- **Son's birthday:** June 11, 2023
- **Current age calculation:** As of November 1, 2025, he is 2 years, 4 months, 21 days old
  - Age formula: `(current_date - June 11, 2023)` in years and months
  - **NEVER claim he is older** - always calculate age from birthdate
  - **NEVER claim multiple children** - singular "son" or "child" only

### When to Mention Parenting (Use Sparingly)

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

### Examples of Appropriate Use

```markdown
✅ "With a toddler at home, my late-night homelab experiments now happen during naptime..."
✅ "Since becoming a parent in 2023, I've prioritized automation to free up time..."
✅ "My Dell R940 rack mount is in the basement - toddler-proofing required relocating it..."
```

### Examples of Overuse/Inappropriate

```markdown
❌ "My kids love watching Raspberry Pi lights blink..." (INACCURATE - one child, age 2)
❌ "Teaching my children about cryptography..." (INACCURATE - he's 2 years old)
❌ "As a father of three..." (INACCURATE - one child)
❌ Using parenting analogies in every single blog post
```

### Humanization Balance

Parenting is ONE humanization element among many. Prioritize:
1. **Homelab stories** (most posts)
2. **Technical failures** (most posts)
3. **Concrete measurements** (every post)
4. **Uncertainty phrases** (every post)
5. **Parenting/time constraints** (occasional, 15-20% of posts)

### Privacy Protection

- NEVER use son's name
- NEVER share photos
- NEVER mention specific locations (daycare, pediatrician, etc.)
- NEVER share detailed schedules or routines that could identify patterns
- Keep references generic: "my son," "toddler," "young child"

---

## Cross-References
- Related modules:
  - Core modules apply to all content creation
- External docs:
  - `docs/ENFORCEMENT.md` - NDA compliance enforcement
  - `content-review-instructions.md` - Content review standards

## Examples

### Example 1: Security Vulnerability Discussion (SAFE)

```markdown
✅ "In my homelab, I tested CVE-2024-1234 (CVSS 9.8) using Metasploit.
    Container escaped to host in 3 minutes. Here's how I hardened it..."
```

### Example 2: Security Vulnerability Discussion (UNSAFE)

```markdown
❌ "Last week at work, we discovered a critical RCE in our production environment.
    The vendor hasn't patched it yet, so I can't share details..."
```

### Example 3: Career Experience (SAFE)

```markdown
✅ "Years ago, I worked on systems that required multi-factor authentication.
    The implementation challenges taught me the importance of user experience..."
```

### Example 4: Career Experience (UNSAFE)

```markdown
❌ "My current role involves securing federal systems.
    We use a combination of X, Y, and Z technologies..."
```

## Common Pitfalls

- **Time buffering insufficient** - Use "years ago," never "last month" or "recently"
- **Specific system mentions** - Use generic terms ("federal systems," not agency names)
- **Active vulnerability discussion** - Only discuss CVEs published ≥90 days ago
- **Work story attribution** - Always frame as homelab experiments
- **Family oversharing** - Maintain privacy boundaries

## Validation

### How to Verify Correct Application

```bash
# 1. Check for work references in blog posts
grep -rE "at work|my employer|current role|we use" src/posts/

# 2. Verify no recent timeline references
grep -rE "last month|recently|this year|current" src/posts/

# 3. Check family information accuracy
grep -rE "kids|children|son|daughter" src/posts/ | grep -v "one child\|son"
```

### Success Criteria
- [ ] Zero mentions of current work incidents
- [ ] No specific government systems or agencies
- [ ] All security discussions attributed to homelab
- [ ] Family references accurate (one son, age calculated correctly)
- [ ] Privacy boundaries maintained
- [ ] Time buffering applied (2-3 year minimum for work stories)

## Changelog
- **2025-11-01**: Initial extraction from CLAUDE.md v3.0.0
