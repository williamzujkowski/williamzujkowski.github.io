# Phase 6: Implementation Decision Tree

**Quick Reference Guide for Phase 6 Execution**

---

## Decision Flow

```
START: Portfolio at 98.2% passing (56/57), avg 105.4/100
│
├─> Q1: Is CLAUDE.md up-to-date with validator v2.0?
│   ├─> NO  → [P1.1] Update CLAUDE.md (30-45 min) ⭐⭐⭐
│   └─> YES → Skip to Q2
│
├─> Q2: Are all posts passing (≥75/100)?
│   ├─> NO  → [P1.2] Fix failing posts (2-4 hrs/post) ⭐⭐⭐
│   └─> YES → Skip to Q3
│
├─> Q3: Is monthly validation automated?
│   ├─> NO  → [P2.1] Deploy monthly cron (45-60 min) ⭐⭐
│   └─> YES → Skip to Q4
│
├─> Q4: Does new post template exist?
│   ├─> NO  → [P2.2] Create template (20-30 min) ⭐⭐
│   └─> YES → Skip to Q5
│
├─> Q5: Is P1+P2 stable for 2+ weeks?
│   ├─> NO  → WAIT 2 weeks, monitor
│   └─> YES → Continue to Q6
│
├─> Q6: Do you need regression alerts?
│   ├─> YES → [P3.1] Implement regression detector (45-60 min) ⭐
│   └─> NO  → Skip to Q7
│
├─> Q7: Do you want weekly summaries?
│   ├─> YES → [P3.2] Deploy weekly cron (30-45 min) ⭐
│   └─> NO  → Skip to Q8
│
└─> Q8: Do you need visual dashboard?
    ├─> YES → [P4] Build dashboard (2-3 hrs) - DEFER
    └─> NO  → DONE: Maintenance system complete
```

---

## Priority Matrix

```
IMPACT vs EFFORT

High Impact  │ P1.1 CLAUDE.md    │ P2.1 Monthly Cron
             │ P1.2 Fix Failing  │ P2.2 Template
             │ (30-45 min)       │ (45-60 min)
             │ (2-4 hrs)         │ (20-30 min)
─────────────┼───────────────────┼─────────────────────
             │                   │ P3.1 Regression
Medium Impact│                   │ P3.2 Weekly Summary
             │                   │ (45-60 min)
             │                   │ (30-45 min)
─────────────┼───────────────────┼─────────────────────
             │                   │ P4 Dashboard
Low Impact   │                   │ (2-3 hrs)
             │                   │ [DEFER]
─────────────┴───────────────────┴─────────────────────
             Low Effort (0-1 hr)  Med-High Effort (1-4 hrs)
```

**Legend:**
- ⭐⭐⭐ = P1 Critical (must do)
- ⭐⭐ = P2 High (should do)
- ⭐ = P3 Medium (nice to have)
- No stars = P4 Low (defer)

---

## Task Dependencies

```
Independent (Parallel Execution):
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ P1.1 CLAUDE.md   │  │ P2.2 Template    │  │ P2.1 Monthly Cron│
│ (30-45 min)      │  │ (20-30 min)      │  │ (45-60 min)      │
└──────────────────┘  └──────────────────┘  └────────┬─────────┘
                                                      │
                                                      ▼
Sequential (After Monthly Cron):                ┌────────────────┐
                                                │ P3.1 Regression│
Can Start Immediately:                          │ (45-60 min)    │
┌──────────────────┐                           └────────────────┘
│ P1.2 Fix Failing │
│ (2-4 hrs/post)   │
└──────────────────┘

Independent (Optional):
┌──────────────────┐
│ P3.2 Weekly Sum. │
│ (30-45 min)      │
└──────────────────┘

Deferred Indefinitely:
┌──────────────────┐
│ P4 Dashboard     │
│ (2-3 hrs)        │
└──────────────────┘
```

---

## Execution Strategy

### Recommended: P1 + P2 Only (5-8 hours)

**Week 1-2: P1 Critical**
```
Day 1-2:  Update CLAUDE.md (30-45 min)
Day 3-7:  Fix failing post (2-4 hrs)
         └─> Validate: 100% passing rate
```

**Week 2-4: P2 Automation**
```
Day 8-10: Create template (20-30 min)
Day 11-14: Deploy monthly cron (45-60 min)
          └─> Test manually
          └─> Schedule cron job
          └─> Monitor first run
```

**Week 4+: Monitor & Sustain**
```
Month 1:  Active monitoring (daily log checks)
Month 2-3: Close monitoring (weekly reviews)
Month 4+:  Maintenance mode (quarterly reviews)
```

---

## What to Skip

### ❌ DO NOT IMPLEMENT (Low ROI)

**P4: Portfolio Dashboard**
- **Reason:** 2-3 hours for visual appeal only
- **Alternative:** CLI commands provide sufficient data
- **Decision:** Defer indefinitely

**P3 (Until P2 Stable):**
- **Reason:** Need 2 weeks to validate P2 automation
- **Decision:** Wait, then reassess

---

## Success Checkpoints

### ✅ After P1 (Week 1-2)
- [ ] CLAUDE.md section 2,500-3,000 words complete
- [ ] All 57 posts passing (100% rate)
- [ ] Validator v2.0 fully documented
- [ ] Zero NDA violations in career post

### ✅ After P2 (Week 2-4)
- [ ] Monthly cron deployed and scheduled
- [ ] First monthly report generated
- [ ] Template validated on test post (80-90/100)
- [ ] Zero manual overhead achieved

### ✅ After 1 Month
- [ ] Cron ran successfully on 1st of month
- [ ] Report saved to `reports/monthly/`
- [ ] No regressions detected
- [ ] Passing rate sustained ≥95%

### ✅ After 3 Months
- [ ] 3 monthly reports generated
- [ ] Automation proven stable
- [ ] Template used for any new posts
- [ ] Zero manual intervention required

---

## Common Questions

### Q: Should I implement P3 (regression alerts) now?
**A:** NO. Wait 2 weeks to validate P2 stable first.

### Q: Do I need the portfolio dashboard?
**A:** NO. CLI commands provide sufficient monitoring. Dashboard is visual appeal only (2-3 hrs effort, low ROI).

### Q: What if a post fails after P1?
**A:** Pre-commit hook will reject commits. Fix immediately using 7-phase methodology from unified guide.

### Q: How often should I run manual reviews?
**A:**
- **Month 1:** Daily log checks (5 min)
- **Month 2-3:** Weekly reviews (10 min)
- **Month 4+:** Quarterly deep-dives (1-2 hrs)

### Q: What's the minimum to sustain quality?
**A:** P1 + P2 only. Monthly cron automates monitoring, template ensures new posts start strong.

---

## Quick Commands Reference

### Check Portfolio Health
```bash
# Quick summary
python scripts/blog-content/humanization-validator.py --batch --format summary

# Find failing posts
python scripts/blog-content/humanization-validator.py --batch --filter-below 75

# Generate monthly report
python scripts/blog-content/humanization-validator.py --batch --save-report reports/monthly/validation-$(date +%Y-%m-%d).json
```

### Test Monthly Cron
```bash
# Manual execution (test before scheduling)
bash scripts/blog-content/monthly-validation.sh

# Check logs
tail -f logs/monthly-validation.log
```

### Use Template
```bash
# Copy template for new post
cp docs/TEMPLATES/blog-post-template.md src/posts/YYYY-MM-DD-slug.md

# Validate after writing
python scripts/blog-content/humanization-validator.py --post src/posts/YYYY-MM-DD-slug.md
```

---

## Risk-Based Decision Making

### If Time-Constrained (2-3 hours only)
**Priority:** P1.1 CLAUDE.md + P2.2 Template
- **Why:** Documentation ensures future LLMs know v2.0 features
- **Why:** Template provides proactive quality for new posts
- **Skip:** P1.2 (failing post fix) can wait, pre-commit blocks bad commits anyway

### If Quality-Focused (4-6 hours)
**Priority:** P1 (CLAUDE.md + Fix Failing) + P2.2 Template
- **Why:** Achieve 100% passing rate
- **Why:** Complete documentation
- **Why:** Proactive template for new posts
- **Skip:** P2.1 (monthly cron) can be added later

### If Automation-Focused (3-4 hours)
**Priority:** P1.1 CLAUDE.md + P2 (Cron + Template)
- **Why:** Zero manual overhead achieved
- **Why:** Documentation complete
- **Skip:** P1.2 (failing post) is 1/57, pre-commit protects anyway

---

## Final Recommendation

### ✅ IMPLEMENT
1. **P1.1 CLAUDE.md** (30-45 min) → Document v2.0
2. **P1.2 Fix Failing Post** (2-4 hrs) → 100% passing rate
3. **P2.1 Monthly Cron** (45-60 min) → Automated monitoring
4. **P2.2 Template** (20-30 min) → Proactive quality

**Total:** 5-8 hours over 2-4 weeks

### ⏸️ DEFER
1. **P3 Regression Alerts** → Wait 2 weeks, validate P2 stable
2. **P3 Weekly Summaries** → Optional enhancement
3. **P4 Dashboard** → Indefinitely (CLI sufficient)

---

**Next Step:** Review with stakeholder, approve P1+P2, begin implementation.
