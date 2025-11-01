# Phase 6.5: Static Page Humanization - Quick Reference

**Version:** 1.0.0 | **Date:** 2025-10-29 | **Status:** AGENT EXECUTION GUIDE

---

## Mission Brief

Transform 4 static pages from corporate-sounding to authentically personal using proven humanization principles from blog posts (104.2/100 avg score). Maintain NDA compliance and professional credibility.

**Target:** All pages achieve 85-95+ humanization scores through first-person narratives, specific measurements, failure stories, and conversational tone.

---

## Agent Assignments

| Agent | Page | File | Priority | Time | Score Target |
|-------|------|------|----------|------|--------------|
| **1** | Home | `src/index.njk` | P1 | 2h | 85+ |
| **2** | About | `src/pages/about.md` | P1 | 3-4h | 90+ |
| **3** | Uses | `src/pages/uses.md` | P2 | 2-3h | 85+ |
| **4** | Resources | `src/pages/resources.md` | P3 | 1-2h | 95+ |

---

## The 5 Core Principles

### 1. First-Person Authenticity
- **Use:** I/me/my throughout
- **Avoid:** Third person, "one might", corporate passive voice
- **Example:** "I implement Zero-Trust" NOT "Zero-Trust architectures are implemented"

### 2. Specific Over Generic
- **Add:** Dates (2024-10-29), versions (v2.3.1), numbers (64GB, 100k assets)
- **Avoid:** "Recently", "modern tools", "many years"
- **Example:** "Dell R940 with 64GB RAM, built 2019" NOT "powerful server"

### 3. Uncertainty & Nuance
- **Use:** "Probably", "in my experience", "seems to", "depends on"
- **Avoid:** Absolute statements, "definitely", "always works"
- **Example:** "This works well for me, though it depends on..." NOT "This is the best approach"

### 4. Failure as Learning
- **Add:** Specific struggle stories with lessons
- **Include:** What broke, how long it took, what you learned
- **Example:** "I spent 6 hours debugging YAML before realizing..." NOT just "configured successfully"

### 5. Conversational Tone
- **Use:** Contractions, humor, real talk
- **Avoid:** Corporate jargon, buzzwords, overly formal language
- **Example:** "Tools that actually work" NOT "leveraging cutting-edge solutions"

---

## NDA Compliance Rules (CRITICAL)

### ✅ SAFE Patterns

```
✓ "Years ago, I learned..."
✓ "In my experience..."
✓ "While researching [topic]..."
✓ "A common scenario in security..."
✓ "During the Log4j crisis in 2021..." (public event)
✓ "At a federal health agency..." (generic)
```

### ❌ FORBIDDEN Patterns

```
✗ "Last week at work..."
✗ "We recently had an incident..."
✗ "My current employer..."
✗ "In our production environment..."
✗ "Last month at Cloud.gov..."
✗ Specific ongoing projects or current incidents
```

### 🚨 When In Doubt

- Make it generic or hypothetical
- Focus on homelab and personal projects
- Use "years ago" for work stories
- Describe role/actions, not agency specifics

---

## Humanization Scoring Cheat Sheet

### ⬆️ Increases Score

**First-Person (+5 each, max +15):**
- I/me/my used naturally throughout

**Measurements (+1 each, bonus at 10+):**
- Dates: 2024-10-29, October 2024
- Versions: v2.3.1, Python 3.11
- Numbers: 64GB, 100k, $3,000
- Time: "6 hours", "2 years"

**Failure Stories (+10 each, max +30):**
- Specific debugging struggles
- "I tried X, learned Y"
- Costs of learning ("$5k in mistakes")

**Trade-Offs (+5 each, max +15):**
- "X vs Y" comparisons
- Honest pros and cons
- "Depends on use case"

**Uncertainty (+5 total):**
- "Probably", "seems to", "in my case"

### ⬇️ Decreases Score

**AI Tells (-5 to -10 each):**
- Em dashes (—) in prose
- Semicolons outside code
- "Moreover", "Furthermore"

**Corporate Jargon (-5 each):**
- "Leverage", "utilize", "synergy"
- "Cutting-edge", "game-changing"
- "Best practices" (without context)

**Overly Formal (-3 each):**
- Passive voice unnecessarily
- Complex vocabulary when simple works

---

## Quick Transformation Guide

### Before → After Examples

**Generic to Specific:**
```
Before: "Modern security tools"
After:  "Wazuh 4.5.2 running on my Dell R940"
```

**Third to First Person:**
```
Before: "Security engineering focuses on..."
After:  "I focus on security engineering because..."
```

**Success to Failure Learning:**
```
Before: "Built a comprehensive homelab"
After:  "Started with a $50 Pi, killed an eBay server with bad power,
         learned about 208V the expensive way, now running a Dell R940.
         $3k equipment, $5k in learning experiences."
```

**Absolute to Nuanced:**
```
Before: "This is the best approach"
After:  "This works well for me, though it depends on your priorities.
         Your mileage may vary."
```

---

## Page-Specific Targets

### Agent 1: Home Page (src/index.njk)

**Focus Areas:**
- Hero text (lines 20-34): Add 15+ years, YAML debugging story
- AI Journey (lines 48-66): Add 1995 date, 30 years later, federal context
- What I Do cards (lines 139-194): Add anecdote to each (20-30 words)

**Key Additions:**
- First-person instances: 8+
- Measurements: 6+ (dates, numbers, specs)
- Failure narratives: 2+
- Remove ALL corporate jargon

---

### Agent 2: About Page (src/pages/about.md)

**Focus Areas:**
- Opening (lines 11-20): Reality of the job, good days vs bad days
- Journey (lines 22-31): Expand to 300-400 words with progression
  - 2005: IT consulting (toolbar virus story)
  - 2010: NIH (didn't know what I was doing)
  - 2015: Vulnerability management scale
  - 2023: Cloud.gov
- Impact stories (lines 90-136): Transform into narratives
  - Log4j: December 9, 2021, 11:45 PM, 3-week sprint
  - Each story: 80-100 words
- Philosophy (lines 139-176): Replace with failure examples
  - SSH tunnel story, API key commits, "my failures specifically"

**Key Additions:**
- First-person instances: 30+
- Measurements: 10+ (dates, times, counts)
- Failure narratives: 4+ detailed stories
- Career honesty about learning

---

### Agent 3: Uses Page (src/pages/uses.md)

**Focus Areas:**
- Hardware (lines 16-38): Add context to each item
  - Workstation: RAM regret, 2019 build date
  - Framework: Coffee incident, repairability win
  - Homelab story: $50 Pi → R940 progression, $3k+$5k costs
- Software (lines 46-62): Add discovery stories
  - Ghostty: Oct 2024 switch from Alacritty
  - VS Code: 2018 vim attempt, 3 weeks, pairing pain
  - Tokyo Night: Tested 847 themes (maybe 20)
- Trade-offs (lines 64-83): Wazuh vs alternatives
  - vs ELK, vs Splunk, vs OSSEC
  - Honest downsides
- Principles (lines 157-164): Expand each to 3-4 sentences
  - CentOS betrayal, Bitwarden choice, "future me yelling"

**Key Additions:**
- First-person instances: 20+
- Measurements: 15+ (versions, dates, specs)
- Trade-offs: 5+ tool comparisons
- Failure narratives: 3+
- "Why" context for every major tool

---

### Agent 4: Resources Page (src/pages/resources.md)

**Focus Areas:**
- Hot Right Now (lines 44-104): Add versions and dates
  - Slim.AI: v1.40.5, Oct 2024
  - Tailscale: v1.54.1, 2:07 connection time
- Learning Paths: Add hour estimates
  - Week 1-2: 15-20 hours
  - Month 2: "eat your evenings"
- Book Recommendations (lines 433-499): Add when read
  - Web App Handbook: 2012, re-read schedule
  - Each book: specific takeaway
- Learning Platforms (lines 501-620): Add dates and progression
  - THM: 3-6 months, specific paths
  - HTB: Starting Point, forum/Discord value
- Tools: Add version numbers throughout

**Key Additions:**
- Measurements: 10+ more
- All tools have versions
- Personal anecdotes have dates
- Maintain current high score (85+)

---

## Self-Validation Checklist

Before submitting your work, verify:

### Content Quality
- [ ] Read your changes aloud (sounds natural?)
- [ ] First-person perspective throughout
- [ ] Specific measurements added (dates, versions, numbers)
- [ ] At least 2+ failure stories with lessons
- [ ] Trade-offs discussed honestly
- [ ] Conversational tone, no corporate jargon
- [ ] Humor enhances, not detracts

### NDA Compliance
- [ ] No "last week/month" or "recently" with work
- [ ] No current employer specifics
- [ ] No ongoing projects or incidents
- [ ] All work stories are "years ago" or generic
- [ ] Homelab/personal projects emphasized

### Technical
- [ ] No HTML/CSS structure changes
- [ ] Preserve existing classes and IDs
- [ ] Links still work (check internal refs)
- [ ] No syntax errors (build test)

### Validation Commands
```bash
# Run humanization validator
python scripts/blog-content/humanization-validator.py --post [your-file]

# Build test
npm run build

# Visual check
npm run serve
# Open http://localhost:8080 and review your page
```

---

## Common Pitfalls to Avoid

### ❌ Don't Do This

**Over-casual:**
```
"lol this broke everything and I was like wtf"
```

**Under-specific:**
```
"I use modern security tools for monitoring"
```

**NDA violation:**
```
"Last month at Cloud.gov, we discovered a vulnerability in..."
```

**Corporate jargon:**
```
"Leveraging cutting-edge solutions to optimize security posture"
```

**AI tells:**
```
"Moreover, the implementation—while complex—yielded exceptional results; furthermore..."
```

### ✅ Do This Instead

**Conversational professional:**
```
"I spent 6 hours debugging this before realizing the issue"
```

**Specific and measured:**
```
"I run Wazuh 4.5.2 on Ubuntu 24.04 for security monitoring"
```

**Safe work reference:**
```
"Years ago, I learned that vulnerability management requires more communication than technical skill"
```

**Plain language:**
```
"Building security controls that actually work and don't annoy developers"
```

**Natural flow:**
```
"After trying multiple approaches, I found that this method works well for most homelab scenarios. Your mileage may vary depending on your setup."
```

---

## Time Management

### Estimated Timeline Per Agent

**Agent 1 (Home):** 2 hours
- Setup & reading: 30 min
- Hero + AI Journey: 45 min
- What I Do cards: 30 min
- Self-validation: 15 min

**Agent 2 (About):** 3-4 hours
- Setup & reading: 30 min
- Opening rewrite: 30 min
- Journey expansion: 90 min
- Impact stories: 60 min
- Philosophy rebuild: 45 min
- Self-validation: 15 min

**Agent 3 (Uses):** 2-3 hours
- Setup & reading: 30 min
- Hardware context: 45 min
- Software stories: 45 min
- Trade-offs section: 30 min
- Principles expansion: 30 min
- Self-validation: 15 min

**Agent 4 (Resources):** 1-2 hours
- Setup & reading: 20 min
- Add versions/dates: 45 min
- Book timestamps: 20 min
- Platform details: 20 min
- Self-validation: 15 min

### Check-In Schedule

- **T+0h:** Kickoff (confirm receipt)
- **T+1h:** Initial progress report
- **T+4h:** Mid-point review (share drafts)
- **T+6-8h:** Final drafts ready

---

## Support & Questions

### If You Get Stuck

**NDA Concerns:**
- Make it generic or homelab-focused
- Use "years ago" for work stories
- When in doubt, ask before proceeding

**Voice Questions:**
- Reference blog posts for tone examples
- Read section aloud - does it sound natural?
- Check quick reference examples above

**Technical Issues:**
- Build errors: Check HTML syntax
- Link problems: Verify file paths
- Responsive issues: Preserve existing classes

### Communication Format

```
Agent [N] - [HH:MM]
Page: [Home|About|Uses|Resources]
Status: [in_progress|blocked|complete]
Progress: [description]
Issues: [any concerns]
Next: [next actions]
```

---

## Success Criteria Summary

| Metric | Target | How to Check |
|--------|--------|--------------|
| Humanization Score | 85-95+ | Run validator script |
| First-Person | 60+ total | Count I/me/my |
| Measurements | 45+ total | Count dates/versions/numbers |
| Failure Stories | 10+ total | Count specific struggles |
| Trade-Offs | 8+ total | Count balanced discussions |
| NDA Compliance | 100% | Grep for risky patterns |
| Build Success | 0 errors | `npm run build` |
| Mobile Responsive | No scroll | Test 375px/768px/1440px |

---

## Final Reminders

1. **Read the full strategy document** (PHASE6.5_STATIC_PAGES_STRATEGY.md) before starting
2. **NDA compliance is non-negotiable** - when in doubt, make it generic
3. **Voice consistency matters** - match the conversational professional tone of blog posts
4. **Specific beats generic** - dates, versions, numbers make it real
5. **Failures teach** - share struggles and lessons learned
6. **Test your work** - run validator, build, and visual check
7. **Professional credibility first** - humor and honesty should enhance, not detract

---

**You've got this. Make these pages feel like a real person wrote them—because they should.**

---

**Document Version:** 1.0.0
**For Questions:** Check main strategy document or ask in check-in
**Status:** READY FOR AGENT EXECUTION
