---
title: Senior Engineer Content Validation Checklist
category: checklists
version: 1.0.0
created: 2025-11-11
last_updated: 2025-11-11
purpose: Pre-publication validation for senior security engineer content quality
related_modules:
  - docs/context/core/nda-compliance.md
  - docs/context/standards/writing-style.md
  - docs/context/standards/humanization-standards.md
  - docs/context/standards/blog-patterns.md
tags: [validation, quality-control, senior-engineer, content-review, pre-publication]
---

# Senior Engineer Content Validation Checklist

**Purpose:** Comprehensive validation checklist for ensuring blog posts meet senior security engineer content quality standards before publication.

**Usage:** Run through this checklist during final review phase after content creation and automated validation.

**Time estimate:** 15-25 minutes for thorough review

**Automation:** Some checks have bash commands for quick validation. Manual review required for nuanced assessment.

---

## 1. Technical Accuracy Validation

### 1.1 Version Verification

- [ ] **All version numbers verified against official documentation**
  ```bash
  # Extract version numbers from post
  grep -oE "v?[0-9]+\.[0-9]+(\.[0-9]+)?" src/posts/[file].md | sort -u
  ```
  - Cross-reference each version with official release notes
  - Verify compatibility claims (e.g., "works on Ubuntu 22.04+")
  - Check if versions are current or explicitly dated

- [ ] **Command syntax tested in actual environment**
  - Copy all command blocks to test environment
  - Verify output matches claims in post
  - Check for typos in flags, paths, or arguments

- [ ] **Breaking changes documented with version context**
  - If discussing migration: "Changed in version X.Y"
  - If syntax deprecated: "Before v3.0, you used..."
  - If feature removed: "As of v4.2, X is no longer supported"

### 1.2 Performance Claims

- [ ] **Performance metrics backed by actual measurements**
  ```bash
  # Check for unsubstantiated performance claims
  grep -E "faster|slower|better|worse|improved|optimized" src/posts/[file].md
  ```
  - Every "faster" claim has quantified data (e.g., "73% faster")
  - Every comparison includes baseline (e.g., "vs standard approach")
  - Measurements include test conditions (hardware, dataset size, duration)

- [ ] **No vendor specs without independent verification**
  - Marketing claims (e.g., "10x faster!") verified in homelab
  - Benchmark methodology disclosed
  - Reproducibility information provided

- [ ] **Resource measurements specific and realistic**
  ```bash
  # Verify resource measurements present
  grep -E "[0-9]+(GB|MB|KB|ms|seconds|minutes|hours|CPU|RAM|VRAM)" src/posts/[file].md | wc -l
  ```
  - Expected: 15+ concrete measurements per post
  - RAM usage realistic (not "uses 1KB RAM for full OS")
  - Time measurements honest (not "installed in 5 seconds" for complex systems)

### 1.3 System Architecture Context

- [ ] **Architecture decisions explained with reasoning**
  - Not just "use Docker" but "Docker because X, not Podman because Y"
  - Trade-offs acknowledged (see Section 3.5)
  - Alternative approaches mentioned

- [ ] **Environment specifications provided**
  ```bash
  # Check for environment context
  grep -iE "ubuntu|debian|centos|rhel|fedora|kernel|hardware|CPU|GPU" src/posts/[file].md
  ```
  - OS distribution and version specified
  - Kernel version if relevant to topic
  - Hardware specs if performance-related

- [ ] **Integration challenges discussed**
  - Tool compatibility issues mentioned
  - Version conflicts documented
  - Workarounds explained with rationale

---

## 2. Security Best Practices Verification

### 2.1 Vulnerability Discussion

- [ ] **CVEs cited with 90-day minimum age**
  ```bash
  # Extract CVE references
  grep -oE "CVE-[0-9]{4}-[0-9]{4,}" src/posts/[file].md
  ```
  - Check publication date of each CVE (use cve.mitre.org or nvd.nist.gov)
  - Verify 90+ day gap between CVE publication and blog post
  - Reasoning: Avoid discussing active 0-days or recent organizational vulnerabilities

- [ ] **CVSS scores contextualized, not used alone**
  - CVSS score ALWAYS accompanied by:
    - EPSS probability (if applicable)
    - Exploitability assessment
    - Environmental factors (e.g., "9.8 but requires local access")
  - Never: "CRITICAL 9.8, patch immediately"
  - Always: "CVSS 9.8, EPSS 0.3% exploitation probability, context matters"

- [ ] **Security claims tested in homelab**
  ```bash
  # Check for homelab attribution
  grep -iE "homelab|tested|my environment|my setup" src/posts/[file].md | wc -l
  ```
  - Expected: 5-7 homelab references per post
  - All security configurations verified personally
  - No untested "best practices" copied from vendor docs

### 2.2 Threat Model Clarity

- [ ] **Threat model explicitly defined for security advice**
  - Who is the attacker? (script kiddie, APT, insider)
  - What are they targeting? (data, availability, credentials)
  - What constraints exist? (network access, authentication required)

- [ ] **Attack surface analysis realistic**
  - Not: "This makes you unhackable"
  - Yes: "This reduces attack surface by eliminating X exposure"

- [ ] **Defense-in-depth acknowledged**
  - Security measures presented as layers, not silver bullets
  - Failure modes discussed (see Section 3.4)

### 2.3 Common Security Mistake Patterns

- [ ] **No oversimplified security advice**

  **Anti-patterns to remove:**

  | ❌ Oversimplification | ✅ Nuanced Alternative |
  |----------------------|------------------------|
  | "Just use AppArmor for container security" | "AppArmor provides MAC for containers. But profiles break during upgrades. I maintain 23 custom profiles—each took 3-4 iterations. Test in staging first." |
  | "Enable HTTPS and you're secure" | "HTTPS encrypts transport. Doesn't prevent SQLi, SSRF, or credential stuffing. It's table stakes, not a security strategy." |
  | "This CVE is CRITICAL, patch immediately" | "CVSS 9.8 measures theoretical severity. EPSS shows 0.3% exploitation probability. Still patch, but context matters for prioritization." |
  | "Use strong passwords" | "20+ character passwords generated via password manager. Protect manager with U2F key. Passwords alone insufficient without MFA." |

  ```bash
  # Check for oversimplified security claims
  grep -iE "just use|simply|easy|secure|unhackable|bulletproof" src/posts/[file].md
  ```

- [ ] **Cryptography discussion accurate**
  - Algorithm names spelled correctly (ChaCha20-Poly1305, not "ChaCha")
  - Key sizes appropriate for algorithm (AES-256, not AES-512)
  - No homebrew crypto recommendations
  - Library recommendations current (e.g., libsodium, not ancient OpenSSL)

- [ ] **Compliance context provided**
  - If mentioning compliance: specify framework (e.g., NIST 800-53, PCI-DSS)
  - No blanket "compliant" claims without audit evidence
  - Homelab ≠ production compliance (acknowledge difference)

---

## 3. NDA Compliance Check

**Reference:** `docs/context/core/nda-compliance.md`

### 3.1 Time Buffering

- [ ] **No current or recent work incidents (2-3 year minimum buffer)**
  ```bash
  # Check for time-sensitive work references
  grep -iE "at work|my employer|current role|recently|last month|this year|2024|2025" src/posts/[file].md
  ```
  - **Safe:** "Years ago, I worked on systems that faced Z challenge."
  - **Unsafe:** "Last month at work, we discovered..."

- [ ] **All work stories time-buffered or homelab-attributed**
  - Work experience: Use "years ago" framing
  - Recent experiments: Attribute to homelab
  - Security incidents: Homelab testing only

### 3.2 Attribution Patterns

- [ ] **Homelab attribution for technical examples**
  ```bash
  # Verify homelab attribution present
  grep -iE "in my homelab|my setup|my raspberry pi|my dell r940|my testing" src/posts/[file].md | wc -l
  ```
  - Expected: 5-7+ homelab references per technical post
  - No ambiguous "we" or "our environment" (implies work)
  - Specific hardware mentioned (Dell R940, Raspberry Pi 4, RTX 3090)

- [ ] **No specific government systems or agencies**
  ```bash
  # Check for prohibited references (customize pattern based on your background)
  grep -iE "agency|federal system|classified|clearance|government" src/posts/[file].md
  ```
  - Generic terms only: "federal systems," "government sector"
  - No agency acronyms or specific program names
  - No clearance level mentions

### 3.3 Family Privacy

- [ ] **Family references accurate (one son, age calculated correctly)**
  ```bash
  # Check family references for accuracy
  grep -iE "kids|children|son|daughter|family" src/posts/[file].md
  ```
  - **Accurate:** "one child," "my son" (born June 11, 2023)
  - **Inaccurate:** "my kids," "children," "father of three"
  - Age calculation: As of 2025-11-11, son is 2 years, 5 months old

- [ ] **Privacy boundaries maintained**
  - NEVER use son's name
  - NEVER share photos
  - NEVER mention specific locations (daycare, pediatrician)
  - Keep references generic: "my son," "toddler," "young child"

- [ ] **Parenting mentions used sparingly (15-20% of posts maximum)**
  - Not every post needs parenting analogy
  - Avoid forced connections to unrelated technical content
  - Appropriate contexts: time management, work-life balance, noise/power considerations

### 3.4 Safe vs Unsafe Patterns

**Quick validation:**

```bash
# Check for unsafe patterns
grep -E "at work|we use|current role|my employer|recent|last week|this month" src/posts/[file].md

# Verify safe patterns present
grep -E "in my homelab|years ago|research shows|common pattern|I tested" src/posts/[file].md
```

**✅ Safe patterns:**
- "In my homelab, I discovered X vulnerability in Y."
- "Years ago, I worked on systems that required multi-factor authentication."
- "Research shows this attack pattern is common."
- "A common challenge with containerization is..."

**❌ Unsafe patterns:**
- "Last month at work..."
- "My current employer uses..."
- "We recently discovered..."
- "Our team implemented..."

---

## 4. Authority Signal Validation

**Reference:** `docs/context/standards/writing-style.md` (Technical Authority Standards section)

### 4.1 Senior Engineer Voice

- [ ] **Complexity acknowledged without oversimplifying**
  - Not: "Docker is easy to use"
  - Yes: "Docker simplifies deployment. But storage gets messy—overlay2 vs devicemapper trade-offs matter."

- [ ] **Vendor claims questioned with technical objections**
  - Not: "Product X is 10x faster (according to vendor)"
  - Yes: "Vendor claims 10x speedup. I tested: 2.3x in my environment. Methodology differs."

- [ ] **Multiple failure modes referenced from experience**
  ```bash
  # Check for failure narrative presence
  grep -iE "failed|broke|mistake|wrong|bug|issue|problem|crashed" src/posts/[file].md | wc -l
  ```
  - Expected: 5-7+ failure references per post
  - Demonstrates real-world testing, not just theory

### 4.2 Depth Indicators

- [ ] **Assumes sysadmin background (no basic networking/Linux explanations)**

  **Don't explain:**
  - Basic networking (TCP/IP, DNS, routing)
  - Linux fundamentals (package management, systemd, permissions)
  - Container basics (Docker images, registries)
  - Common security concepts (CVEs, CVSS, authentication vs authorization)

  **Do explain:**
  - Non-obvious behavior (kernel quirks, edge cases)
  - Advanced configurations (performance tuning, security hardening)
  - Integration challenges (tool compatibility, version conflicts)

- [ ] **Architecture decisions include reasoning**
  - Every "use X" recommendation includes "because Y, not Z because..."
  - Trade-offs explicit (see Section 3.5)
  - Context-dependent advice (e.g., "for edge deployments" vs "production clusters")

- [ ] **Differentiates theory vs production reality**
  - Not: "This should work"
  - Yes: "In theory, X. In production, I encountered Y. Workaround: Z."

### 4.3 Time Investment Signals

- [ ] **Debugging time quantified**
  ```bash
  # Check for time investment mentions
  grep -oE "[0-9]+ (hours?|days?|weeks?|minutes?)" src/posts/[file].md | wc -l
  ```
  - Expected: 8+ time references
  - Examples: "spent 6 hours debugging," "took 3 weeks to optimize," "17 minutes to compile"

- [ ] **Iteration counts explicit**
  - "After 4 failed attempts..."
  - "Tested 8, 12, 16 attention heads..."
  - "Third configuration finally worked"

- [ ] **Multiple approaches documented**
  - Not: "Use approach X"
  - Yes: "Tried A (failed), then B (slow), settled on C (works but limited)"

---

## 5. Common Mistake Prevention

### 5.1 AI-Tell Detection

**Reference:** `docs/context/standards/humanization-standards.md` (Phase 1)

- [ ] **Zero em dashes (—) outside code blocks**
  ```bash
  # Check for em dashes (high-severity violation)
  grep -E "—" src/posts/[file].md | grep -v "```"
  ```
  - Replace with commas or split into two sentences

- [ ] **Zero semicolons (;) outside code blocks**
  ```bash
  # Check for semicolons (high-severity violation)
  grep -E ";" src/posts/[file].md | grep -v "```"
  ```
  - Use periods instead

- [ ] **Zero AI transition phrases**
  ```bash
  # Check for AI-tell phrases
  grep -iE "in conclusion|overall|in summary|therefore|hence|thus|moreover|furthermore" src/posts/[file].md
  ```
  - Replace with human transitions: "Anyway," "That said," "Still," "Turns out"

- [ ] **Zero corporate buzzwords**
  ```bash
  # Check for corporate jargon
  grep -iE "leverage|utilize|synergy|paradigm|facilitate|optimize" src/posts/[file].md
  ```
  - Replace: "leverage" → "use," "utilize" → "use," "facilitate" → "help"

### 5.2 Personal Voice Requirements

**Reference:** `docs/context/standards/humanization-standards.md` (Phase 2)

- [ ] **8+ first-person statements throughout post**
  ```bash
  # Count first-person statements
  grep -oE "I (tested|tried|discovered|found|spent|built|deployed|configured|debugged)" src/posts/[file].md | wc -l
  ```
  - Distribution: Every major section includes personal narrative
  - Not clustered in one paragraph

- [ ] **5-7+ homelab stories**
  ```bash
  # Count homelab references
  grep -iE "in my homelab|my setup|my raspberry pi|my dell|my rtx" src/posts/[file].md | wc -l
  ```
  - Specific hardware mentioned (not generic "my server")
  - Real experiments described

### 5.3 Measurement Requirements

**Reference:** `docs/context/standards/humanization-standards.md` (Phase 3)

- [ ] **15+ concrete measurements**
  ```bash
  # Run humanization validator measurement detection
  uv run python scripts/blog-content/humanization-validator.py --post src/posts/[file].md | grep "measurements"
  ```
  - Types: percentages, multipliers, comparisons, performance, hardware, time, data sizes
  - Examples: "73% faster," "2.1x speedup," "512MB RAM," "3 hours debugging"

### 5.4 Uncertainty Markers

**Reference:** `docs/context/standards/humanization-standards.md` (Phase 4)

- [ ] **6-8+ uncertainty phrases**
  ```bash
  # Check uncertainty patterns
  grep -iE "probably|likely|might|seems|your mileage may vary|in my case|depends on|I think" src/posts/[file].md | wc -l
  ```
  - Distributed throughout post (not clustered)
  - Natural placement after technical claims

### 5.5 Trade-off Balance

**Reference:** `docs/context/standards/humanization-standards.md` (Phase 6)

- [ ] **10+ balanced perspective statements**
  ```bash
  # Check for trade-off connectors
  grep -iE " but | yet | however | though | still |on the other hand|downside|limitation" src/posts/[file].md | wc -l
  ```
  - Formula: `[Benefit] yet/but/however [Cost]`
  - Examples:
    - "K3s reduces RAM usage, yet requires SQLite expertise."
    - "AppArmor improves security. But profiles break during upgrades."
    - "EPSS saves time. However, API rate limits slow automation."

---

## 6. Automated Validation

### 6.1 Humanization Validator

```bash
# Run comprehensive humanization validation
uv run python scripts/blog-content/humanization-validator.py --post src/posts/[file].md
```

**Expected output:**
- **Score:** ≥75/100 to pass (≥90/100 excellent tier)
- **Zero high-severity violations** (em dashes, semicolons, AI phrases)
- **All required patterns present** (first-person, uncertainty, measurements, trade-offs)

**Scoring tiers:**

| Score | Tier | Action Required | Effort |
|-------|------|-----------------|--------|
| 0-59 | Failing | Full 7-phase refinement | 2-4 hours |
| 60-74 | Needs Improvement | Targeted refinement (3-5 phases) | 1-2 hours |
| 75-89 | Good | Polish to excellent tier | 30-60 min |
| 90-100 | Excellent | Maintain, minimal tweaks | 10-15 min |

### 6.2 Build Validation

```bash
# Test build without deploying
npm run build
```

- [ ] **Build completes without errors**
- [ ] **Zero Eleventy warnings**
- [ ] **Frontmatter YAML valid**

### 6.3 Metadata Validation

```bash
# Validate post metadata
uv run python scripts/blog-content/metadata-validator.py --post src/posts/[file].md
```

- [ ] **Required fields present:** title, date, author, tags, description
- [ ] **Date format correct:** YYYY-MM-DD
- [ ] **Tags appropriate:** 3-7 tags, lowercase, hyphenated
- [ ] **Description length:** 120-160 characters (SEO optimal)

### 6.4 Link Validation

```bash
# Check for broken links
uv run python scripts/blog-content/link-validator.py --post src/posts/[file].md
```

- [ ] **All external links return 200 status**
- [ ] **All internal links resolve to existing pages**
- [ ] **Citation links include DOI or arXiv when available**

---

## 7. Final Review Checklist

### 7.1 Content Quality

- [ ] **Opening hook compelling** (surprising fact, concrete measurement, personal story)
- [ ] **BLUF (Bottom Line Up Front) in first 2 sentences**
- [ ] **Sentence rhythm varies** (short → medium → punch pattern)
- [ ] **Paragraphs 2-4 sentences** (not walls of text)
- [ ] **Code blocks earn their place** (see Section 7.3)
- [ ] **Citations present** (10+ for research-heavy posts, 3+ minimum)

### 7.2 Readability

- [ ] **Scannable structure** (headings, bullets, white space)
- [ ] **Technical jargon defined or linked** (on first use)
- [ ] **Acronyms spelled out** (on first use, e.g., "EPSS (Exploit Prediction Scoring System)")
- [ ] **Active voice predominant** (passive voice <20%)

### 7.3 Code Block Quality

**Reference:** `docs/STANDARDS/CODE_BLOCK_CONTENT_STANDARDS.md`

- [ ] **Code ratio within threshold for post type**
  ```bash
  # Calculate code ratio
  uv run python scripts/blog-content/code-ratio-calculator.py --post src/posts/[file].md --post-type-aware
  ```

  | Post Type | Total Code Ratio | Actual Code Ratio | Threshold |
  |-----------|-----------------|-------------------|-----------|
  | Tutorial | <35% | <30% | Step-by-step needs examples |
  | Conceptual | <25% | <20% | Diagrams + light code |
  | Experience | <20% | <15% | Lessons > implementation |
  | DIAGRAM-HEAVY | <60%* | <10% | *If >80% Mermaid educational |

- [ ] **Inline code blocks (<15 lines) teach core concepts**
  - Context-critical (interrupting flow to visit gist breaks learning)
  - Complete and runnable (or clearly labeled as simplified)
  - Cannot be better expressed as diagram/prose

- [ ] **Extracted to gist (>20 lines) for reference material**
  - Complete implementations readers will copy-paste
  - Reusable across projects (not post-specific examples)
  - Latest version maintenance valuable

- [ ] **No truncated pseudocode** ("# ... additional implementation")
  - Incomplete code converted to prose or deleted
  - No "rest left as exercise" unless tutorial

### 7.4 SEO & Metadata

- [ ] **URL slug descriptive and concise** (50-60 characters)
- [ ] **Meta description compelling** (120-160 characters)
- [ ] **Title accurate and benefit-focused** (not clickbait)
- [ ] **Image alt text descriptive** (for accessibility and SEO)
- [ ] **Heading hierarchy logical** (H1 → H2 → H3, no skipping levels)

---

## 8. Pre-Commit Enforcement

**Reference:** `docs/context/core/enforcement.md`

### 8.1 Automated Checks

Pre-commit hooks run automatically. These checks will **block commit** if failed:

```bash
# Pre-commit hook runs:
# 1. Humanization validation (≥75/100 required)
# 2. Metadata validation (required fields, date format)
# 3. MANIFEST.json currency check
# 4. Build test (npm run build must succeed)
```

### 8.2 Manual Pre-Flight

Before attempting commit, manually verify:

- [ ] **Ran humanization validator** and score ≥75/100
- [ ] **Tested build locally** (`npm run build`)
- [ ] **Reviewed git diff** for unintended changes
- [ ] **Updated MANIFEST.json** if new files created

### 8.3 Commit Message Standards

```bash
# Commit message format
git commit -m "feat: add blog post about [topic]

- [Summary of key points]
- [Technical focus]
- Score: [humanization score]/100"
```

**Conventional commit prefixes:**
- `feat:` - New blog post
- `fix:` - Bug fix, broken link repair
- `refactor:` - Content refinement, humanization improvements
- `docs:` - Documentation updates
- `chore:` - Maintenance tasks

---

## 9. Post-Publication Validation

### 9.1 Live Site Checks

- [ ] **Page loads without errors** (check browser console)
- [ ] **Mobile responsive** (test on phone or dev tools)
- [ ] **Gists render correctly** (if embedded)
- [ ] **Mermaid diagrams render** (v10+ syntax)
- [ ] **Images load** (check all screenshots, diagrams)

### 9.2 Performance

```bash
# Run Lighthouse audit (requires deployed site)
npx lighthouse https://williamzujkowski.com/posts/[slug]/ --view
```

- [ ] **Performance score ≥90**
- [ ] **Accessibility score ≥90** (WCAG AA compliance)
- [ ] **Best Practices score ≥90**
- [ ] **SEO score ≥90**

### 9.3 Cross-Browser Testing

- [ ] **Chrome/Edge** (Chromium engine)
- [ ] **Firefox** (Gecko engine)
- [ ] **Safari** (WebKit engine, if available)

---

## 10. Monthly Audit Checklist

**Frequency:** First week of each month

### 10.1 Portfolio Review

```bash
# Run batch humanization validation
uv run python scripts/blog-content/humanization-validator.py --batch --save-report reports/monthly-$(date +%Y-%m).json

# Compare with previous month
uv run python scripts/blog-content/humanization-validator.py --batch --compare reports/monthly-$(date +%Y-%m-%d).json
```

- [ ] **≥90% posts score ≥75/100** (passing threshold)
- [ ] **≥70% posts score ≥90/100** (excellent tier)
- [ ] **Zero high-severity violations** (em dashes, semicolons)

### 10.2 Accuracy Audit

**Reference:** Session 20-22 pattern (audit-first prevents 30+ min waste)

- [ ] **TODO.md accuracy verified** (no false positives/negatives)
- [ ] **MANIFEST.json current** (last_validated within 30 days)
- [ ] **Citation links still valid** (no 404s)
- [ ] **Version claims current** (flag outdated version references)

### 10.3 Standards Drift Prevention

- [ ] **Exaggeration creep check** (verify quantified claims still accurate)
- [ ] **NDA compliance review** (ensure no work references introduced)
- [ ] **Documentation accuracy** (CLAUDE.md stats match reality)

---

## Appendix A: Quick Reference Commands

```bash
# === VALIDATION SUITE ===

# 1. Humanization validation (comprehensive)
uv run python scripts/blog-content/humanization-validator.py --post src/posts/[file].md

# 2. Code ratio calculation (post-type aware)
uv run python scripts/blog-content/code-ratio-calculator.py --post src/posts/[file].md --post-type-aware

# 3. Metadata validation
uv run python scripts/blog-content/metadata-validator.py --post src/posts/[file].md

# 4. Link validation
uv run python scripts/blog-content/link-validator.py --post src/posts/[file].md

# 5. Build test
npm run build

# === PATTERN DETECTION ===

# AI-tells (em dashes, semicolons, AI phrases)
grep -E "—|;|in conclusion|overall|leverage|exciting" src/posts/[file].md | grep -v "```"

# NDA violations (work references, recent timelines)
grep -E "at work|we use|current role|recently|last month|this year" src/posts/[file].md

# Authority signals (first-person, homelab, measurements)
grep -E "I (tested|tried|discovered|spent)|in my homelab|[0-9]+(GB|MB|hours|minutes|%)" src/posts/[file].md | wc -l

# Uncertainty markers
grep -iE "probably|likely|might|seems|your mileage may vary|depends on" src/posts/[file].md | wc -l

# Trade-off balance
grep -iE " but | yet | however | though |downside|limitation" src/posts/[file].md | wc -l

# === BATCH OPERATIONS ===

# Batch humanization validation
uv run python scripts/blog-content/humanization-validator.py --batch

# Find posts below threshold
uv run python scripts/blog-content/humanization-validator.py --batch --filter-below 75

# Monthly report with comparison
uv run python scripts/blog-content/humanization-validator.py --batch --save-report reports/monthly-$(date +%Y-%m).json --compare reports/monthly-2025-10.json
```

---

## Appendix B: Common Violation Fixes

### B.1 Em Dash Removal

**Before:**
```markdown
Docker simplifies deployment—but storage gets messy.
```

**After:**
```markdown
Docker simplifies deployment. But storage gets messy.
```

### B.2 Semicolon Elimination

**Before:**
```markdown
K3s uses 512MB RAM; Kubernetes uses 2GB minimum.
```

**After:**
```markdown
K3s uses 512MB RAM. Kubernetes uses 2GB minimum.
```

### B.3 AI Phrase Replacement

**Before:**
```markdown
In conclusion, containerization offers significant benefits.
Moreover, it simplifies deployment workflows.
```

**After:**
```markdown
Anyway, containerization helps.
It simplifies deployment too.
```

### B.4 Corporate Jargon Elimination

**Before:**
```markdown
We can leverage Docker to facilitate rapid deployment and
optimize resource utilization across our infrastructure paradigm.
```

**After:**
```markdown
Use Docker for faster deployment and better resource management.
```

### B.5 Adding Personal Voice

**Before:**
```markdown
Docker is a containerization platform that simplifies deployment.
```

**After:**
```markdown
I tested Docker in my homelab for 3 weeks. Deployment time dropped
from 2 hours to 17 minutes. Still, storage configuration took
6 hours to get right.
```

### B.6 Quantifying Vague Claims

**Before:**
```markdown
This approach is much faster and uses less memory.
```

**After:**
```markdown
This approach is 73% faster (2.3s vs 8.1s) and uses 41% less RAM
(512MB vs 870MB). Tested on Ubuntu 24.04 with Intel i9-9900K.
```

---

## Appendix C: Related Documentation

### Core Standards Modules
- **`docs/context/core/nda-compliance.md`** - NDA compliance rules and safe patterns
- **`docs/context/core/enforcement.md`** - Pre-commit enforcement rules
- **`docs/context/standards/writing-style.md`** - "Polite Linus Torvalds" voice standards
- **`docs/context/standards/humanization-standards.md`** - 7-phase humanization methodology
- **`docs/context/standards/blog-patterns.md`** - SEO, internal linking, content patterns

### Validation Scripts
- **`scripts/blog-content/humanization-validator.py`** - Comprehensive humanization scoring
- **`scripts/blog-content/code-ratio-calculator.py`** - Code block ratio calculation
- **`scripts/blog-content/metadata-validator.py`** - Frontmatter validation
- **`scripts/blog-content/link-validator.py`** - Broken link detection

### Quality Standards
- **`docs/STANDARDS/CODE_BLOCK_CONTENT_STANDARDS.md`** - Code block quality guidelines
- **`docs/HUMANIZATION_VALIDATION.md`** - Complete humanization methodology
- **`CLAUDE.md`** - Master configuration and routing architecture

---

## Changelog

### Version 1.0.0 (2025-11-11)
- **Initial creation** - Comprehensive senior engineer content validation checklist
- **10 main sections:**
  1. Technical accuracy validation (versions, performance, architecture)
  2. Security best practices verification (CVEs, threat models, common mistakes)
  3. NDA compliance check (time buffering, attribution, family privacy)
  4. Authority signal validation (senior voice, depth, time investment)
  5. Common mistake prevention (AI-tells, personal voice, measurements)
  6. Automated validation (humanization, build, metadata, links)
  7. Final review checklist (content quality, readability, code blocks, SEO)
  8. Pre-commit enforcement (automated checks, manual pre-flight, commit standards)
  9. Post-publication validation (live site, performance, cross-browser)
  10. Monthly audit checklist (portfolio review, accuracy, standards drift)
- **3 appendices:**
  - Appendix A: Quick reference bash commands for all validation checks
  - Appendix B: Common violation fixes with before/after examples
  - Appendix C: Related documentation and cross-references
- **Bash validation commands:** 25+ automated checks for quick verification
- **Cross-references:** Links to all relevant standards modules
- **Production-ready:** Designed for 15-25 minute pre-publication review

---

**Maintainer:** Content quality agent
**Review Schedule:** Quarterly
**Next Review:** 2026-02-11
**Usage:** Run through this checklist before publishing any blog post

---

**Parent:** [docs/checklists/](../checklists/)
**Related:** [CLAUDE.md](../../CLAUDE.md), [docs/context/INDEX.yaml](../context/INDEX.yaml)
