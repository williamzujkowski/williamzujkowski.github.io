# Blog Post Template - Quick Start

**Time to first draft**: 5 minutes setup + 2-3 hours writing = Your best post yet

---

## 🚀 Three Steps to 85+ Score

### 1. Copy Template (30 seconds)

```bash
# Replace YYYY-MM-DD and slug with your details
cp src/templates/blog-post-template.md src/posts/2025-10-29-my-topic-slug.md
```

### 2. Fill In While Following Guidance (2-3 hours)

Open the file in your editor. You'll see:
- ✅ Section headings with guidance
- ✅ Example patterns to follow
- ✅ Inline checklist reminding you what to include
- ✅ Comments explaining "why" for each element

**Write naturally**, following the examples. The template keeps you on track.

### 3. Validate and Publish (10 minutes)

```bash
# Check your score (target: ≥75, excellent: ≥85)
python scripts/blog-content/humanization-validator.py \
  --post src/posts/2025-10-29-my-topic-slug.md

# Generate images
python scripts/blog-images/update-blog-images.py
python scripts/blog-images/generate-blog-hero-images.py
bash scripts/optimize-blog-images.sh

# Commit and push
git add src/posts/2025-10-29-my-topic-slug.md
git commit -m "feat: Add post about [topic]"
git push origin main
```

---

## 🎯 The Magic Formula

```
Required Elements (5)
  + 10+ Measurements
  + 1+ Failure Story
  + 3+ Options Tested
  - Zero AI-Tells
  = 85-95/100 Score
```

---

## ✅ While Writing, Include:

### Required (must have ≥1 each):
- [x] "I tested..." / "my homelab" (first-person)
- [x] "probably" / "depends on" (uncertainty)
- [x] "64GB RAM" / "v2.3.1" / "took 3 hours" (measurements)
- [x] "trade-off" / "but" / "limitation" (balanced view)
- [x] Code blocks / "for example" (concrete details)

### Bonus (high value):
- [x] 10+ quantified metrics (hardware, time, percentages)
- [x] 1 debugging story with time cost ("spent 6 hours...")
- [x] 3+ options tested with metrics ("4 workers: 340 req/s, 8 workers: 520 req/s...")

### Avoid:
- [ ] Em dashes (—) → use commas or parentheses
- [ ] Semicolons in narrative → use periods
- [ ] "In conclusion" → use specific heading instead
- [ ] "revolutionary" without proof → show metrics

---

## 📊 What to Expect

**Phase 1 results** (48 posts using similar approach):
- Average score: **87.3/100** ⭐
- Pass rate: **100%** (all ≥75/100)
- Excellent rate: **85%** (≥85/100)

**Your first post with template**:
- Expect: **80-90/100** on first draft
- Time saved: **2-3 hours** vs. writing without template
- Revisions needed: **Minimal** (maybe 1 round)

---

## 🆘 Need Help?

### Stuck on a section?
- **Quick patterns**: See `/docs/guides/HUMANIZATION_QUICK_REFERENCE.md`
- **Detailed examples**: See `/docs/guides/USING_POST_TEMPLATE.md`
- **Full standards**: See `CLAUDE.md`

### Score below 75?
- Check validator output for specific violations
- Add missing required elements
- Remove AI-tells (em dashes, semicolons, "In conclusion")
- Add 5-10 more measurements from your testing

### Not sure what counts as a measurement?
**Counts**: version numbers, dates, percentages, hardware specs, time durations, before/after metrics, req/s, latency, memory usage, CPU models, anything quantified

**Example rich paragraph** (12 measurements):
```
On my Intel i9-9900K with 64GB RAM and RTX 3090, I tested Python 3.11.2
with Docker v24.0.5 over 3 months starting June 2025. Cold start took
12-15 seconds, with throughput of 340-520 req/s at 45-60% CPU and stable
4-6GB memory usage—a 73% improvement over the baseline.
```

---

## 💡 Pro Tips

1. **Track measurements as you test**: Keep a notepad with versions, times, metrics
2. **Share at least one mistake**: "I spent X hours because I forgot Y"
3. **Test 3+ options**: Document the metrics for each
4. **Read aloud**: If it sounds like a textbook, simplify
5. **Be specific**: "340 req/s" not "fast", "6 hours" not "a while"

---

## 📚 Full Documentation

- **Template**: `/src/templates/blog-post-template.md`
- **Usage Guide**: `/docs/guides/USING_POST_TEMPLATE.md` (detailed, 568 lines)
- **Quick Reference**: `/docs/guides/HUMANIZATION_QUICK_REFERENCE.md` (one-page)
- **System Overview**: `/docs/guides/TEMPLATE_SYSTEM_OVERVIEW.md`
- **Master Standards**: `CLAUDE.md`

---

## ✨ Remember

The template works because it helps you:
1. Include all required humanization elements
2. Track and share real measurements from testing
3. Admit failures and share lessons learned
4. Compare multiple options with quantified trade-offs
5. Write conversationally, not formally

**Result**: Authentic content that scores 80-90/100 because it captures real experience through structured storytelling.

**Now go write something awesome!** 🚀
