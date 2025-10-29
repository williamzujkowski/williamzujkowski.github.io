# Humanization Quick Reference Card

**Purpose**: One-page cheat sheet for writing authentic, human-sounding blog posts that score 85-95/100.

**Target**: ≥75/100 (passing), ≥85/100 (excellent), ≥95/100 (outstanding)

---

## 🎯 The Formula for 85+ Scores

```
Required Elements (must have ≥1 each)
  + Measurements (target: 10+ for +10 bonus)
  + Failure Narratives (any = +5 to +10 bonus)
  + Deep Trade-offs (3+ options with metrics = +5 to +10 bonus)
  - AI-tells (em dashes, semicolons, generic conclusions)
  = 85-95/100 score
```

---

## ✅ Required Elements (Must Have)

### 1. First-Person Narrative (min: 1)
- "I tested", "I discovered", "I learned"
- "my homelab", "my setup", "my experience"
- "I spent 6 hours debugging..."

### 2. Uncertainty Markers (min: 1)
- "probably", "likely", "might", "seems to"
- "depends on", "your mileage may vary"
- "in my experience", "at least in my testing"

### 3. Specific Measurements (min: 1)
- Version numbers: "Python 3.11.2"
- Dates: "2025-07-15"
- Performance: "340ms → 85ms (75% improvement)"
- Hardware: "Intel i9-9900K, 64GB RAM, RTX 3090"
- Time: "took 3 hours", "over 6 months"

### 4. Trade-off Discussion (min: 1)
- "trade-off", "downside", "limitation", "caveat"
- "but", "however", "on the other hand"
- "better for X but worse for Y"

### 5. Concrete Details (min: 2)
- Code blocks with comments
- Configuration examples
- "Here's how", "For example", "In practice"

---

## 🚀 Bonus Scoring (High-Value Additions)

### +10 Points: 10+ Measurements
Track everything from your testing:
- **Hardware**: CPU, RAM, GPU models
- **Performance**: req/s, latency, throughput
- **Time**: startup, response, duration
- **Versions**: software, API versions
- **Percentages**: improvements, rates
- **Comparisons**: before/after, A vs B

**Example with 12 measurements:**
```
On my Intel i9-9900K with 64GB RAM and RTX 3090, I tested Python 3.11.2
with Docker v24.0.5. Cold start took 12-15 seconds, with throughput of
340-520 req/s at 45-60% CPU and 4-6GB memory. This is a 73% improvement
over the 2.1x slower baseline from June 2025 testing.
```
(Counted: i9-9900K, 64GB, RTX 3090, 3.11.2, 24.0.5, 12-15s, 340-520 req/s, 45-60%, 4-6GB, 73%, 2.1x, June 2025 = 12)

### +5-10 Points: Failure Narratives
Share debugging stories with time costs:
- "I spent 6 hours debugging [issue]..."
- "I forgot to [critical step] which cost me..."
- "Looking back, I should have [better approach]..."
- "This taught me to always [lesson]..."

**Example failure narrative:**
```
I completely forgot to set memory_limit in the config, which cost me
an entire Saturday of debugging. The system would crash every 6 hours
with cryptic OOM errors. After 8 hours of profiling, I discovered I'd
left it at the default 512MB instead of the recommended 4GB. One missing
line, one lost weekend. Now I always validate configs with `--dry-run`
before deploying.
```

### +5-10 Points: Deep Trade-off Analysis
Test 3+ options with quantified metrics:
- List each option tested
- Include specific metrics for each
- Explain performance vs. X trade-offs
- Give context-dependent recommendations

**Example multi-option analysis:**
```
I tested four worker configurations:

1. **4 workers**: 12s startup, 340 req/s, 2GB RAM
2. **8 workers**: 18s startup, 520 req/s, 4GB RAM (balanced)
3. **12 workers**: 25s startup, 680 req/s, 8GB RAM (best throughput)
4. **16 workers**: 28s startup, 710 req/s, 12GB RAM (diminishing returns)

Trade-off: Speed vs. memory. With 12 workers, you get 2x the throughput
of 4 workers but use 4x the RAM. For systems with <16GB, stick with 8.
For high-traffic with memory to spare, 12 is the sweet spot.
```

---

## 🚫 Avoid: AI-Tells (Score Penalties)

### Punctuation (-5 each)
- ❌ Em dashes (—) → Use commas or parentheses
- ❌ Semicolons in narrative → Use periods or commas

### Transitions (-5 to -10 each)
- ❌ "In conclusion"
- ❌ "Overall"
- ❌ "To summarize"
- ❌ "Looking ahead"

### Hype Words (-5 to -10 each)
- ❌ "revolutionary", "game-changing", "cutting-edge" (without specifics)
- ❌ "amazing", "remarkable", "seamless"
- ❌ "exciting", "fantastic", "incredible"

### Corporate Jargon (-2.5 each)
- ❌ "leverage" → "use"
- ❌ "utilize" → "use"
- ❌ "facilitate" → "help" or "enable"
- ❌ "implement" → "build" or "add"

---

## 📝 Quick Writing Patterns

### Opening Hook (Authentic)
```
✅ "Years ago, I spent 6 hours debugging [specific issue]. Turned out
   I'd [specific mistake]. This taught me [specific lesson]..."

❌ "Today we'll explore the fascinating world of [generic topic]..."
```

### Adding Measurements
```
✅ "On my Intel i9-9900K with 64GB RAM, cold start took 12-15 seconds..."

❌ "The system starts quickly and performs well..."
```

### Trade-offs
```
✅ "Approach A is 2x faster (340ms vs 680ms) but uses 50% more memory
   (6GB vs 4GB). For memory-constrained systems, use B..."

❌ "Both approaches have pros and cons depending on your needs..."
```

### Failure Narratives
```
✅ "I completely forgot to [action], which cost me 4 hours of debugging.
   The error message was cryptic: [actual error]. After [process], I
   discovered [root cause]..."

❌ "I encountered some issues but eventually got it working..."
```

### Uncertainty/Caveats
```
✅ "This probably works for most cases, but your mileage may vary
   depending on [factor]. In my testing on [hardware], I saw [results]..."

❌ "This solution works for all scenarios and provides optimal results..."
```

### Conclusions
```
✅ "Key Lessons from 6 Months of Testing"
   "What I'd Do Differently Next Time"

❌ "In conclusion, we've explored..."
```

---

## 🎯 Target Metrics by Section

| Section | Measurements | First-Person | Trade-offs | Time to Write |
|---------|-------------|--------------|-----------|---------------|
| Opening Hook | 1-2 | 3-5 | 0 | 10 min |
| Context | 2-3 | 2-3 | 0-1 | 10 min |
| Core Content | 5-10 | 5-8 | 2-3 | 30-45 min |
| Trade-offs | 5-10 | 3-5 | 5-10 | 20-30 min |
| Challenges | 2-3 | 5-8 | 1-2 | 15-20 min |
| Implementation | 3-5 | 2-3 | 1-2 | 20-30 min |
| Conclusion | 0-2 | 1-2 | 0-1 | 10 min |

**Total target**: 20-35 measurements, 20-35 first-person, 10-20 trade-offs

---

## 🔍 Validation Checklist

Before running validator:

**Required Elements:**
- [ ] 1+ first-person statements ("I tested", "my homelab")
- [ ] 1+ uncertainty markers ("probably", "depends on")
- [ ] 1+ specific measurements (versions, metrics, dates)
- [ ] 1+ trade-off discussions ("but", "limitation", "downside")
- [ ] 2+ concrete details (code blocks, "for example")

**Bonus Elements (high-value):**
- [ ] 10+ measurements (hardware, performance, time, versions)
- [ ] 1+ failure narrative with time cost and lesson learned
- [ ] 3+ options tested with quantified trade-offs

**Avoid:**
- [ ] No em dashes (—) in narrative text
- [ ] No semicolons outside code blocks
- [ ] No "In conclusion", "Overall", "To summarize"
- [ ] No hype words without backing ("revolutionary", "game-changing")

---

## 🚀 Validation Commands

```bash
# Check humanization score (target: ≥75)
python scripts/blog-content/humanization-validator.py \
  --post src/posts/YYYY-MM-DD-slug.md

# Verify citation hyperlinks
python scripts/blog-research/check-citation-hyperlinks.py

# Generate and optimize images
python scripts/blog-images/update-blog-images.py
python scripts/blog-images/generate-blog-hero-images.py
bash scripts/optimize-blog-images.sh
```

---

## 📊 Score Interpretation

| Score | Status | What It Means | Action |
|-------|--------|---------------|--------|
| 95-110 | Outstanding | Exemplary humanization | Ready to publish |
| 85-94 | Excellent | Well-crafted, authentic | Ready to publish |
| 75-84 | Good | Passes validation | Consider adding failure narrative |
| 65-74 | Needs work | Close but not quite | Add measurements or trade-offs |
| <65 | Needs revision | Too AI-like | Add required elements, remove AI-tells |

---

## 💡 Pro Tips

1. **Write conversationally**: Read aloud—if it sounds like a textbook, simplify
2. **Track everything**: Note every measurement during testing (versions, times, metrics)
3. **Share failures**: Vulnerability builds trust and scores highly
4. **Test multiple options**: 3+ with metrics = deep trade-off analysis bonus
5. **Be specific**: Replace "fast" with "340 req/s on my i9-9900K"
6. **Use parentheses**: Instead of em dashes for asides
7. **Add caveats**: "depends on", "your mileage may vary", "in my experience"
8. **Cut formality**: "use" not "utilize", "help" not "facilitate"

---

## 📚 See Also

- **Full template**: `/src/templates/blog-post-template.md`
- **Detailed guide**: `/docs/guides/USING_POST_TEMPLATE.md`
- **Validator patterns**: `/scripts/blog-content/humanization-patterns.yaml`
- **Blog standards**: `CLAUDE.md` (sections on blog post requirements)

---

## 🎓 Remember

**Authentic content comes from:**
- Real testing (measurements prove it)
- Honest mistakes (failures humanize it)
- Thoughtful comparisons (trade-offs show nuance)
- Conversational tone (write like you talk)

**The goal isn't to game the validator—it's to write content that genuinely helps readers through your authentic experience.**

Target 85+ and you'll consistently create content that sounds human because it comes from human experience.
