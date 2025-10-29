# Batch 4 Execution Checklist

**Status:** READY
**Timeline:** 4-6 hours
**Target:** 10 posts (25-45/100 range)

---

## ⏱️ Quick Start (5 min)

- [ ] **Read:** Executive Summary (`/docs/BATCH_4_EXEC_SUMMARY.md`)
- [ ] **Review:** Batch 3 patterns (`/docs/BATCH_3_COMPLETION_SUMMARY.md`)
- [ ] **Check:** NDA guidelines in CLAUDE.md (for Post 8)
- [ ] **Verify:** `/uses/` page for homelab hardware
- [ ] **Time:** Allocate 4-6 hours uninterrupted

---

## 📋 Wave 1 Checklist (2-3 hours)

### Pre-Wave 1 (5 min)

- [ ] Create TODO list with Posts 1-6
- [ ] Open 6 terminal windows or tmux panes
- [ ] Have humanization-validator.py ready
- [ ] Note commit message template

### Spawn Agents (5 min)

**Group A (Posts 1-3):**
- [ ] Agent 1: `2024-05-14-ai-new-frontier-cybersecurity.md` (25/100, 5 violations)
- [ ] Agent 2: `2024-01-30-securing-cloud-native-frontier.md` (27.5/100, 5 violations)
- [ ] Agent 3: `2024-08-02-quantum-computing-leap-forward.md` (30/100, 4 violations)

**Group B (Posts 4-6):**
- [ ] Agent 4: `2024-11-05-pizza-calculator.md` (32.5/100, 2 violations) *Quick win*
- [ ] Agent 5: `2024-02-22-open-source-vs-proprietary-llms.md` (35/100, 6 violations)
- [ ] Agent 6: `2024-07-09-zero-trust-architecture-implementation.md` (35/100, 6 violations)

### Agent Instructions Template

For each agent, provide:
```
Fix [filename]:
1. Remove all em dashes (—) - Priority #1
2. Add personal homelab story opening
3. Replace vague timestamps with specific dates (2019-2024)
4. Add concrete measurements (from /uses/ for hardware)
5. Add 5+ uncertainty statements (probably, typically, roughly)
6. Add 2-3 failure/surprise narratives
7. Validate with humanization-validator.py
8. Target: ≥80/100, ideally ≥90/100
```

### Monitor Progress (90-120 min)

- [ ] Check agent outputs every 15-20 min
- [ ] Answer questions or provide clarifications
- [ ] Verify no conflicts between agents

### Validation (15 min)

For each post:
- [ ] Post 1: Run `python scripts/blog-content/humanization-validator.py src/posts/2024-05-14-ai-new-frontier-cybersecurity.md`
- [ ] Post 2: Run `python scripts/blog-content/humanization-validator.py src/posts/2024-01-30-securing-cloud-native-frontier.md`
- [ ] Post 3: Run `python scripts/blog-content/humanization-validator.py src/posts/2024-08-02-quantum-computing-leap-forward.md`
- [ ] Post 4: Run `python scripts/blog-content/humanization-validator.py src/posts/2024-11-05-pizza-calculator.md`
- [ ] Post 5: Run `python scripts/blog-content/humanization-validator.py src/posts/2024-02-22-open-source-vs-proprietary-llms.md`
- [ ] Post 6: Run `python scripts/blog-content/humanization-validator.py src/posts/2024-07-09-zero-trust-architecture-implementation.md`

**Pass Criteria:** All posts ≥80/100, zero high-severity violations

### Build Test (2 min)

- [ ] Run `npm run build`
- [ ] Verify build passes (target: <5s)
- [ ] Check for any errors or warnings

### Commit Wave 1 (3 min)

```bash
git add src/posts/2024-05-14-ai-new-frontier-cybersecurity.md
git add src/posts/2024-01-30-securing-cloud-native-frontier.md
git add src/posts/2024-08-02-quantum-computing-leap-forward.md
git add src/posts/2024-11-05-pizza-calculator.md
git add src/posts/2024-02-22-open-source-vs-proprietary-llms.md
git add src/posts/2024-07-09-zero-trust-architecture-implementation.md

git commit -m "feat(blog): Batch 4 Wave 1 - humanize 6 posts (25-35 range)

- AI New Frontier Cybersecurity: 25 → ≥80/100
- Securing Cloud Native Frontier: 27.5 → ≥80/100
- Quantum Computing Leap Forward: 30 → ≥80/100
- Pizza Calculator: 32.5 → ≥80/100 (quick win)
- Open Source vs Proprietary LLMs: 35 → ≥80/100
- Zero Trust Architecture Implementation: 35 → ≥80/100

Applied Batch 3 patterns: em dash removal, personal stories,
concrete timestamps, uncertainty statements, failure narratives.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

- [ ] Commit created
- [ ] Push to remote (optional, or wait until end)

---

## 📋 Wave 2 Checklist (1-2 hours)

### Pre-Wave 2 (5 min)

- [ ] Update TODO list with Posts 7-10
- [ ] Open 4 terminal windows or tmux panes
- [ ] Coffee/water break
- [ ] Review Wave 1 learnings

### Spawn Agents (5 min)

- [ ] Agent 7: `2024-12-03-context-windows-llms.md` (40/100, 4 violations)
- [ ] Agent 8: `2024-10-22-ai-edge-computing.md` (40/100, 4 violations) ⚠️ **NDA RISK**
- [ ] Agent 9: `2024-02-09-deepfake-dilemma-ai-deception.md` (42.5/100, 3 violations)
- [ ] Agent 10: `2024-09-09-embodied-ai-teaching-agents.md` (45/100, 3 violations)

### Agent 8 Special Instructions (NDA Critical)

```
Fix ai-edge-computing.md:

⚠️ CRITICAL NDA REQUIREMENTS:
- Remove ANY current/recent work references
- Use ONLY "years ago" (2019-2021) timeframes
- Keep stories GENERIC and HYPOTHETICAL
- Focus on HOMELAB and PERSONAL learning
- Reference CLAUDE.md "Government Work Security Guidelines"

NEVER use patterns like:
❌ "Last week/month at work..."
❌ "We recently had an incident..."
❌ "My current employer..."
❌ "In our production environment..."

USE patterns like:
✅ "Years ago, I learned..."
✅ "In my home lab, I discovered..."
✅ "While researching [topic], I found..."
✅ "A common scenario in security is..." (hypothetical)

Then apply standard humanization:
1. Remove em dashes
2. Add concrete timestamps (2019-2021 only)
3. Add uncertainty statements
4. Add homelab testing stories
5. Validate with humanization-validator.py
```

### Monitor Progress (45-60 min)

- [ ] Check agent outputs every 15 min
- [ ] **CRITICAL:** Manually review Post 8 for NDA violations before validation
- [ ] Answer questions or provide clarifications

### Manual NDA Review (Post 8) - 10 min ⚠️

- [ ] Open `src/posts/2024-10-22-ai-edge-computing.md`
- [ ] Search for forbidden patterns: "recent", "current", "last week/month", "employer", "production"
- [ ] Verify all timestamps are 2019-2021 or earlier
- [ ] Confirm stories are generic/hypothetical or homelab-specific
- [ ] Check no specific government agency or team details
- [ ] Verify no active security measures or controls mentioned

**If ANY violations found:** Reject Post 8, have agent rewrite sections

### Validation (10 min)

For each post:
- [ ] Post 7: Run `python scripts/blog-content/humanization-validator.py src/posts/2024-12-03-context-windows-llms.md`
- [ ] Post 8: Run `python scripts/blog-content/humanization-validator.py src/posts/2024-10-22-ai-edge-computing.md`
- [ ] Post 9: Run `python scripts/blog-content/humanization-validator.py src/posts/2024-02-09-deepfake-dilemma-ai-deception.md`
- [ ] Post 10: Run `python scripts/blog-content/humanization-validator.py src/posts/2024-09-09-embodied-ai-teaching-agents.md`

**Pass Criteria:** All posts ≥80/100, zero high-severity violations, Post 8 NDA-clean

### Build Test (2 min)

- [ ] Run `npm run build`
- [ ] Verify build passes (target: <5s)
- [ ] Check for any errors or warnings

### Commit Wave 2 (3 min)

```bash
git add src/posts/2024-12-03-context-windows-llms.md
git add src/posts/2024-10-22-ai-edge-computing.md
git add src/posts/2024-02-09-deepfake-dilemma-ai-deception.md
git add src/posts/2024-09-09-embodied-ai-teaching-agents.md

git commit -m "feat(blog): Batch 4 Wave 2 - humanize 4 posts (40-45 range)

- Context Windows LLMs: 40 → ≥80/100
- AI at the Edge Computing: 45 → ≥90/100 (safe replacement)
- Deepfake Dilemma AI Deception: 42.5 → ≥80/100
- Embodied AI Teaching Agents: 45 → ≥80/100

Applied Batch 3 patterns + NDA guidelines for career reflection post.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

- [ ] Commit created
- [ ] Push to remote

---

## 📊 Post-Execution (1 hour)

### Portfolio Re-assessment (15 min)

```bash
cd /home/william/git/williamzujkowski.github.io
python scripts/blog-content/validate-all-posts.py
```

- [ ] Generate updated `docs/reports/portfolio-assessment.md`
- [ ] Check portfolio average: Target ≥78/100
- [ ] Check passing rate: Target ≥76% (42/55)
- [ ] Check excellent posts: Target ≥22/55 (40%)
- [ ] Check failing posts: Target ≤13/55 (23.6%)

### Actual vs Projected Analysis (10 min)

Compare actual results to projections:

| Metric | Projected | Actual | Δ | Status |
|--------|-----------|--------|---|--------|
| Batch 4 Avg | ≥85/100 | _____ | _____ | _____ |
| Portfolio Avg | 78.5/100 | _____ | _____ | _____ |
| Passing Rate | 76.4% (42/55) | _____ | _____ | _____ |
| Excellent Posts | 24-26/55 | _____ | _____ | _____ |
| Timeline | 4-6 hours | _____ | _____ | _____ |

### Completion Report (30 min)

Create `docs/BATCH_4_COMPLETION_SUMMARY.md` with:

- [ ] Executive summary (metrics, success rate)
- [ ] Per-post improvements table (before/after scores)
- [ ] Common patterns fixed (em dashes, timestamps, etc.)
- [ ] Portfolio impact analysis (score distribution shift)
- [ ] Learnings for Batch 5
- [ ] Recommendations for next steps

### Batch 5 Planning (15 min)

Based on results, choose path:

**If passing rate ≥76%:** (Expected)
- [ ] Plan Batch 5: Target remaining 13 failing posts
- [ ] Expected: 1 day execution, +65-75 avg improvement
- [ ] Goal: Achieve 85-90% passing rate (47-50/55)

**If passing rate ≥80%:** (Best case)
- [ ] Pivot to content generation (test methodology on new posts)
- [ ] Create 2-3 new posts with humanization-first approach
- [ ] Validate greenfield effectiveness

**If passing rate <75%:** (Contingency)
- [ ] Analyze what went wrong
- [ ] Adjust methodology if needed
- [ ] Consider targeting 60-74 range (borderline posts) next

---

## ✅ Final Success Criteria

### Minimum (PASS)
- [ ] All 10 posts ≥80/100
- [ ] Zero high-severity violations
- [ ] Zero NDA violations (Post 8)
- [ ] Portfolio average ≥76/100
- [ ] Passing rate ≥70% (39/55)
- [ ] Build passes

### Target (SUCCESS)
- [ ] 9-10 posts ≥90/100
- [ ] Portfolio average ≥78/100
- [ ] Passing rate ≥76% (42/55)
- [ ] 24-26 excellent posts (≥90/100)
- [ ] 13 or fewer failing posts
- [ ] Completed in 4-6 hours

### Stretch (EXCELLENCE)
- [ ] All 10 posts = 100/100
- [ ] Portfolio average ≥80/100
- [ ] Passing rate ≥80% (44/55)
- [ ] 26+ excellent posts
- [ ] 10 or fewer failing posts
- [ ] Completed in <4 hours

---

## 📋 Common Issues & Solutions

### Issue: Agent gets stuck on complex technical section
**Solution:**
- Provide specific homelab example from `/uses/`
- Reference concrete testing experience
- Simplify without dumbing down

### Issue: Post 8 has NDA violation
**Solution:**
- Reject agent output
- Provide specific rewrite: "In 2019, during a personal research project..."
- Remove all work-specific references

### Issue: Em dashes remain after fix
**Solution:**
- Search file: `grep "—" filename.md`
- Replace all: `sed -i 's/—/,/g' filename.md` (or `. ` or ` ` depending on context)

### Issue: Validation score below 80/100
**Solution:**
- Re-run validator with verbose: `python ... --verbose`
- Identify specific violations
- Apply targeted fixes
- Re-validate

### Issue: Build fails
**Solution:**
- Check error message
- Usually frontmatter syntax error
- Verify YAML validity
- Fix and rebuild

---

## 🎯 Time Budget

| Activity | Planned | Actual | Notes |
|----------|---------|--------|-------|
| **Wave 1** | 2-3 hours | _____ | 6 posts |
| **Wave 2** | 1-2 hours | _____ | 4 posts |
| **Validation** | 30 min | _____ | Portfolio re-assessment |
| **Documentation** | 30 min | _____ | Completion report |
| **Buffer** | 1 hour | _____ | Unexpected issues |
| **TOTAL** | 4-6 hours | _____ | |

---

## 📚 Quick Reference

**Full Plan:** `/docs/BATCH_4_PLAN.md`
**Summary:** `/docs/BATCH_4_EXEC_SUMMARY.md`
**Comparison:** `/docs/BATCH_4_COMPARISON.md`
**Batch 3 Report:** `/docs/BATCH_3_COMPLETION_SUMMARY.md`
**Validator:** `/scripts/blog-content/humanization-validator.py`
**CLAUDE.md:** `/CLAUDE.md` (NDA guidelines)
**Uses Page:** `/src/pages/uses.md` (homelab hardware)

---

**Start Time:** _____
**Wave 1 Complete:** _____
**Wave 2 Complete:** _____
**End Time:** _____
**Total Duration:** _____

**Status:** ⏸️ PENDING → ▶️ IN PROGRESS → ✅ COMPLETE

---

**Last Updated:** 2025-10-28
**Ready to Execute:** ✅ YES
