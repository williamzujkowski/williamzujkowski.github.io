# Style Validation Test Plan

**Status**: Active
**Version**: 1.0.0
**Last Updated**: 2025-10-26
**Owner**: Tester Agent (Hive Mind Swarm)

## Executive Summary

This document defines comprehensive test criteria for validating style updates across CLAUDE.md and blog posts, focusing on Smart Brevity compliance, "polite Linus" tone, and healthy AI skepticism. Tests are designed for both automated validation and manual review.

---

## 1. Smart Brevity Compliance Tests

### 1.1 Structural Tests (Automated)

**BLUF (Bottom Line Up Front) Detection**
- **Test ID**: SB-01
- **Category**: Structure
- **Automation**: Yes
- **Pass Criteria**:
  - First paragraph contains main point
  - Key insight within first 100 words
  - Clear action/conclusion in opening

**Test Script**:
```python
def test_bluf_compliance(content):
    """Validate BLUF structure in document opening."""
    first_para = extract_first_paragraph(content)

    checks = {
        "word_count": len(first_para.split()) <= 100,
        "has_key_insight": contains_main_claim(first_para),
        "clarity_score": calculate_clarity(first_para) >= 0.7
    }

    return all(checks.values()), checks
```

**Bullet Point Usage**
- **Test ID**: SB-02
- **Category**: Structure
- **Automation**: Yes
- **Pass Criteria**:
  - Complex lists use bullets
  - Minimum 3 items per bullet group
  - Maximum 7 items per group (cognitive limit)
  - Parallel structure maintained

**Test Script**:
```python
def test_bullet_usage(content):
    """Validate bullet point structure and usage."""
    bullet_groups = extract_bullet_lists(content)

    violations = []
    for group in bullet_groups:
        if len(group) < 3:
            violations.append(f"Group too short: {len(group)} items")
        if len(group) > 7:
            violations.append(f"Group too long: {len(group)} items")
        if not has_parallel_structure(group):
            violations.append("Non-parallel structure detected")

    return len(violations) == 0, violations
```

**Heading Hierarchy**
- **Test ID**: SB-03
- **Category**: Structure
- **Automation**: Yes
- **Pass Criteria**:
  - Proper H1 → H2 → H3 progression
  - No skipped levels
  - Descriptive, action-oriented headings

**Test Script**:
```python
def test_heading_hierarchy(content):
    """Validate markdown heading structure."""
    headings = extract_headings(content)

    violations = []
    prev_level = 0

    for heading in headings:
        level = heading.count('#')
        if level - prev_level > 1:
            violations.append(f"Skipped level: H{prev_level} → H{level}")
        if not is_descriptive(heading.text):
            violations.append(f"Vague heading: {heading.text}")
        prev_level = level

    return len(violations) == 0, violations
```

### 1.2 Content Length Tests (Automated)

**Paragraph Length**
- **Test ID**: SB-04
- **Category**: Brevity
- **Automation**: Yes
- **Pass Criteria**:
  - Average paragraph: 3-5 sentences
  - Maximum paragraph: 8 sentences
  - Technical sections may exceed with justification

**Test Script**:
```python
def test_paragraph_length(content):
    """Check paragraph length compliance."""
    paragraphs = extract_paragraphs(content)

    stats = {
        "total": len(paragraphs),
        "overlength": [],
        "average_sentences": 0
    }

    for i, para in enumerate(paragraphs):
        sentence_count = count_sentences(para)
        stats["average_sentences"] += sentence_count

        if sentence_count > 8:
            stats["overlength"].append({
                "index": i,
                "count": sentence_count,
                "excerpt": para[:100]
            })

    stats["average_sentences"] /= len(paragraphs)

    pass_test = len(stats["overlength"]) == 0
    return pass_test, stats
```

**Sentence Complexity**
- **Test ID**: SB-05
- **Category**: Brevity
- **Automation**: Yes
- **Pass Criteria**:
  - Average words per sentence: 15-20
  - Maximum words per sentence: 30
  - Flesch Reading Ease: 60+ (standard)

**Test Script**:
```python
def test_sentence_complexity(content):
    """Analyze sentence complexity metrics."""
    sentences = extract_sentences(content)

    metrics = {
        "avg_words": sum(len(s.split()) for s in sentences) / len(sentences),
        "max_words": max(len(s.split()) for s in sentences),
        "flesch_score": calculate_flesch_reading_ease(content),
        "complex_sentences": []
    }

    for s in sentences:
        word_count = len(s.split())
        if word_count > 30:
            metrics["complex_sentences"].append({
                "words": word_count,
                "text": s[:100]
            })

    pass_test = (
        metrics["avg_words"] <= 20 and
        metrics["flesch_score"] >= 60 and
        len(metrics["complex_sentences"]) == 0
    )

    return pass_test, metrics
```

---

## 2. "Polite Linus" Tone Tests

### 2.1 Directness Detection (Manual + Automated)

**Technical Precision**
- **Test ID**: PL-01
- **Category**: Tone
- **Automation**: Partial
- **Pass Criteria**:
  - Technical terms used correctly
  - No unnecessary jargon
  - Precise language for specifications

**Automated Check**:
```python
def test_technical_precision(content):
    """Detect vague technical language."""
    vague_phrases = [
        "stuff", "things", "basically", "kind of",
        "sort of", "maybe", "possibly", "probably"
    ]

    violations = []
    for phrase in vague_phrases:
        if phrase.lower() in content.lower():
            context = extract_context(content, phrase, 50)
            violations.append({
                "phrase": phrase,
                "context": context
            })

    return len(violations) == 0, violations
```

**Manual Review Checklist**:
- [ ] Technical claims are specific and verifiable
- [ ] No hedge words in critical instructions
- [ ] Specifications use concrete values

**Constructive Criticism**
- **Test ID**: PL-02
- **Category**: Tone
- **Automation**: Manual
- **Pass Criteria**:
  - Criticisms include actionable fixes
  - Solutions provided with problems
  - Respectful language maintained

**Manual Review Checklist**:
- [ ] Every "don't do X" paired with "do Y instead"
- [ ] Explanations provided for restrictions
- [ ] No inflammatory language
- [ ] Assumes competence, not incompetence

**Authority Balance**
- **Test ID**: PL-03
- **Category**: Tone
- **Automation**: Manual
- **Pass Criteria**:
  - Strong directives where safety-critical
  - Flexible guidance for preferences
  - Clear distinction between MUST/SHOULD/MAY

**Manual Review Checklist**:
- [ ] Safety-critical rules use MUST
- [ ] Best practices use SHOULD
- [ ] Options use MAY or "consider"
- [ ] Rationale provided for all MUST directives

### 2.2 Politeness Metrics (Automated)

**Aggressive Language Detection**
- **Test ID**: PL-04
- **Category**: Tone
- **Automation**: Yes
- **Pass Criteria**:
  - No inflammatory terms
  - No dismissive language
  - No personal attacks

**Test Script**:
```python
def test_aggressive_language(content):
    """Detect potentially aggressive phrasing."""
    aggressive_patterns = [
        r'\b(stupid|dumb|idiotic)\b',
        r'\b(obviously|clearly|trivially)\b',  # Condescending
        r'\b(just|simply|merely)\b.*\bhow\b',  # Dismissive
        r'RTFM',
        r'What were you thinking',
        r'Are you kidding'
    ]

    violations = []
    for pattern in aggressive_patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            violations.append({
                "pattern": pattern,
                "match": match.group(),
                "context": extract_context(content, match.start(), 100)
            })

    return len(violations) == 0, violations
```

**Positive Framing**
- **Test ID**: PL-05
- **Category**: Tone
- **Automation**: Partial
- **Pass Criteria**:
  - Prefer positive instructions over prohibitions
  - Ratio of "do X" to "don't do Y": 2:1 minimum

**Test Script**:
```python
def test_positive_framing(content):
    """Analyze positive vs negative instruction ratio."""
    positive_patterns = [r'\b(do|use|prefer|recommend|try)\b']
    negative_patterns = [r'\b(don\'t|never|avoid|stop)\b']

    positive_count = sum(
        len(re.findall(p, content, re.IGNORECASE))
        for p in positive_patterns
    )
    negative_count = sum(
        len(re.findall(p, content, re.IGNORECASE))
        for p in negative_patterns
    )

    ratio = positive_count / negative_count if negative_count > 0 else float('inf')

    return ratio >= 2.0, {
        "positive": positive_count,
        "negative": negative_count,
        "ratio": ratio
    }
```

---

## 3. AI Skepticism Detection Tests

### 3.1 AI Capability Claims (Manual)

**Overclaiming Detection**
- **Test ID**: AS-01
- **Category**: AI Skepticism
- **Automation**: Manual
- **Pass Criteria**:
  - No claims of AGI or sentience
  - Accurate representation of limitations
  - Clear scope boundaries

**Manual Review Checklist**:
- [ ] AI described as tool, not autonomous agent
- [ ] Limitations acknowledged
- [ ] Failure modes discussed
- [ ] Human oversight emphasized
- [ ] No anthropomorphization

**Evidence Requirements**
- **Test ID**: AS-02
- **Category**: AI Skepticism
- **Automation**: Partial
- **Pass Criteria**:
  - AI performance claims cite benchmarks
  - Comparisons include methodology
  - Results reproducible

**Automated Check**:
```python
def test_ai_evidence_requirements(content):
    """Check if AI claims include citations."""
    ai_claim_patterns = [
        r'AI (achieves|performs|solves|completes)',
        r'model (achieves|performs|solves|completes)',
        r'\d+% (accuracy|precision|recall|improvement)'
    ]

    violations = []
    for pattern in ai_claim_patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            context = extract_context(content, match.start(), 200)
            has_citation = has_citation_nearby(content, match.start(), 200)

            if not has_citation:
                violations.append({
                    "claim": match.group(),
                    "context": context,
                    "missing": "citation"
                })

    return len(violations) == 0, violations
```

### 3.2 Balanced Perspective (Manual)

**Trade-offs Discussion**
- **Test ID**: AS-03
- **Category**: AI Skepticism
- **Automation**: Manual
- **Pass Criteria**:
  - Benefits paired with drawbacks
  - Cost analysis included
  - Alternative approaches mentioned

**Manual Review Checklist**:
- [ ] Every AI solution includes cost analysis (tokens, compute, time)
- [ ] Failure cases documented
- [ ] Traditional alternatives acknowledged
- [ ] When AI is NOT the right tool is discussed

**Hype Avoidance**
- **Test ID**: AS-04
- **Category**: AI Skepticism
- **Automation**: Partial
- **Pass Criteria**:
  - No revolutionary/game-changing claims without evidence
  - Accurate technical terminology
  - Measured language about impact

**Automated Check**:
```python
def test_hype_detection(content):
    """Detect hyperbolic AI claims."""
    hype_phrases = [
        "game-changing", "revolutionary", "unprecedented",
        "will change everything", "solves all", "never seen before",
        "industry disruption", "paradigm shift"
    ]

    violations = []
    for phrase in hype_phrases:
        if phrase.lower() in content.lower():
            context = extract_context(content, phrase, 150)
            has_evidence = has_citation_nearby(content, context, 300)

            violations.append({
                "phrase": phrase,
                "context": context,
                "has_evidence": has_evidence
            })

    # Only fail if hype lacks evidence
    unsupported = [v for v in violations if not v["has_evidence"]]
    return len(unsupported) == 0, violations
```

---

## 4. Content Accuracy Tests

### 4.1 Citation Validation (Automated)

**Citation Coverage**
- **Test ID**: CA-01
- **Category**: Accuracy
- **Automation**: Yes
- **Pass Criteria**:
  - 90%+ claims have citations
  - All statistics cited
  - All technical specs verified

**Test Script**:
```python
def test_citation_coverage(content):
    """Validate citation coverage for claims."""
    claims = extract_factual_claims(content)
    citations = extract_citations(content)

    uncited_claims = []
    for claim in claims:
        if not has_nearby_citation(content, claim, distance=300):
            uncited_claims.append({
                "claim": claim.text,
                "type": claim.type,
                "context": claim.context
            })

    coverage = (len(claims) - len(uncited_claims)) / len(claims)

    return coverage >= 0.90, {
        "total_claims": len(claims),
        "cited_claims": len(claims) - len(uncited_claims),
        "coverage": coverage,
        "uncited": uncited_claims
    }
```

**Link Validation**
- **Test ID**: CA-02
- **Category**: Accuracy
- **Automation**: Yes
- **Pass Criteria**:
  - All external links functional
  - DOI links preferred for papers
  - Archive links for volatile sources

**Test Script**:
```python
async def test_link_validation(content):
    """Validate all hyperlinks in content."""
    links = extract_links(content)

    results = {
        "total": len(links),
        "working": [],
        "broken": [],
        "redirected": []
    }

    async with aiohttp.ClientSession() as session:
        for link in links:
            try:
                async with session.head(link.url, timeout=10) as response:
                    if response.status == 200:
                        results["working"].append(link.url)
                    elif 300 <= response.status < 400:
                        results["redirected"].append({
                            "original": link.url,
                            "status": response.status
                        })
                    else:
                        results["broken"].append({
                            "url": link.url,
                            "status": response.status,
                            "context": link.context
                        })
            except Exception as e:
                results["broken"].append({
                    "url": link.url,
                    "error": str(e),
                    "context": link.context
                })

    return len(results["broken"]) == 0, results
```

### 4.2 Technical Accuracy (Manual)

**Code Validation**
- **Test ID**: CA-03
- **Category**: Accuracy
- **Automation**: Partial
- **Pass Criteria**:
  - Code snippets are syntactically valid
  - Examples are runnable
  - Output matches descriptions

**Manual Review Checklist**:
- [ ] Copy code to IDE and verify syntax
- [ ] Run examples and verify output
- [ ] Check for deprecated functions
- [ ] Validate configuration examples

**Hardware/Software References**
- **Test ID**: CA-04
- **Category**: Accuracy
- **Automation**: Manual
- **Pass Criteria**:
  - Hardware specs match /uses/ page
  - Software versions accurate
  - No fabricated details

**Manual Review Checklist**:
- [ ] Cross-reference hardware with src/pages/uses.md
- [ ] Verify software versions against actual installs
- [ ] Confirm homelab configurations are accurate

---

## 5. Build & Integration Tests

### 5.1 Site Build Tests (Automated)

**Eleventy Build**
- **Test ID**: BI-01
- **Category**: Build
- **Automation**: Yes
- **Pass Criteria**:
  - Site builds without errors
  - All templates render
  - No broken internal links

**Test Script**:
```bash
#!/bin/bash
# test_build.sh

echo "Running Eleventy build test..."

# Clean previous build
rm -rf _site

# Build site
npm run build 2>&1 | tee build.log

# Check for errors
if grep -q "ERROR" build.log; then
    echo "❌ Build failed with errors"
    grep "ERROR" build.log
    exit 1
fi

# Validate output directory
if [ ! -d "_site" ]; then
    echo "❌ Build output directory missing"
    exit 1
fi

# Check for essential files
essential_files=(
    "_site/index.html"
    "_site/posts/index.html"
    "_site/feed.xml"
    "_site/sitemap.xml"
)

for file in "${essential_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing essential file: $file"
        exit 1
    fi
done

echo "✅ Build test passed"
exit 0
```

**Internal Link Check**
- **Test ID**: BI-02
- **Category**: Build
- **Automation**: Yes
- **Pass Criteria**:
  - No 404s for internal links
  - Asset paths resolve correctly

**Test Script**:
```python
def test_internal_links(site_dir="_site"):
    """Validate internal links in built site."""
    violations = []

    html_files = glob.glob(f"{site_dir}/**/*.html", recursive=True)

    for html_file in html_files:
        with open(html_file, 'r') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Check all internal links
        for link in soup.find_all('a', href=True):
            href = link['href']

            # Skip external links
            if href.startswith('http'):
                continue

            # Resolve relative path
            target = resolve_link_path(html_file, href, site_dir)

            if not os.path.exists(target):
                violations.append({
                    "source": html_file,
                    "link": href,
                    "target": target,
                    "text": link.get_text()
                })

    return len(violations) == 0, violations
```

### 5.2 Performance Tests (Automated)

**Page Load Time**
- **Test ID**: BI-03
- **Category**: Build
- **Automation**: Yes
- **Pass Criteria**:
  - LCP < 2.5s
  - FID < 100ms
  - CLS < 0.1

**Test Script**:
```javascript
// test_performance.js
const lighthouse = require('lighthouse');
const chromeLauncher = require('chrome-launcher');

async function testPerformance(url) {
    const chrome = await chromeLauncher.launch({chromeFlags: ['--headless']});
    const options = {
        logLevel: 'info',
        output: 'json',
        onlyCategories: ['performance'],
        port: chrome.port
    };

    const runnerResult = await lighthouse(url, options);
    await chrome.kill();

    const metrics = runnerResult.lhr.audits;

    const results = {
        lcp: metrics['largest-contentful-paint'].numericValue,
        fid: metrics['max-potential-fid'].numericValue,
        cls: metrics['cumulative-layout-shift'].numericValue,
        score: runnerResult.lhr.categories.performance.score
    };

    const passed = (
        results.lcp < 2500 &&
        results.fid < 100 &&
        results.cls < 0.1
    );

    return { passed, results };
}

module.exports = { testPerformance };
```

---

## 6. Test Execution Strategy

### 6.1 Pre-Commit Tests (Local)

Run before each commit:
```bash
# Automated structural tests
python scripts/testing/test_smart_brevity.py --file CLAUDE.md
python scripts/testing/test_tone_compliance.py --file CLAUDE.md

# Build validation
npm run test

# Manual checklist review
# - Review "Polite Linus" tone manually
# - Validate AI skepticism in new content
```

### 6.2 CI/CD Pipeline Tests (Automated)

GitHub Actions workflow:
```yaml
name: Style Validation

on: [push, pull_request]

jobs:
  style-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install dependencies
        run: |
          npm ci
          pip install -r requirements-test.txt

      - name: Smart Brevity Tests
        run: python scripts/testing/test_smart_brevity.py --all

      - name: Tone Compliance Tests
        run: python scripts/testing/test_tone_compliance.py --all

      - name: Citation Validation
        run: python scripts/blog-research/check-citation-hyperlinks.py

      - name: Build Test
        run: npm run build

      - name: Link Validation
        run: python scripts/link-validation/link-validator.py

      - name: Performance Test
        run: npm run test:performance
```

### 6.3 Manual Review Schedule

**Weekly Review** (Every Monday):
- Review 5 random blog posts for tone compliance
- Check CLAUDE.md for clarity and structure
- Validate AI skepticism in recent content

**Monthly Audit** (First of month):
- Full sweep of all documentation
- Update test thresholds based on improvements
- Review and refine manual checklists

### 6.4 Test Reporting

Generate automated report:
```python
def generate_test_report(results):
    """Generate comprehensive test report."""
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_tests": len(results),
            "passed": sum(1 for r in results if r.passed),
            "failed": sum(1 for r in results if not r.passed),
            "pass_rate": None
        },
        "categories": {},
        "violations": [],
        "recommendations": []
    }

    report["summary"]["pass_rate"] = (
        report["summary"]["passed"] / report["summary"]["total"]
    )

    # Group by category
    for result in results:
        category = result.category
        if category not in report["categories"]:
            report["categories"][category] = {
                "total": 0,
                "passed": 0,
                "failed": 0
            }

        report["categories"][category]["total"] += 1
        if result.passed:
            report["categories"][category]["passed"] += 1
        else:
            report["categories"][category]["failed"] += 1
            report["violations"].append({
                "test_id": result.test_id,
                "category": category,
                "details": result.details
            })

    # Generate recommendations
    for category, stats in report["categories"].items():
        if stats["failed"] > 0:
            report["recommendations"].append({
                "category": category,
                "priority": "high" if stats["failed"] > 5 else "medium",
                "action": f"Review {stats['failed']} violations in {category}"
            })

    return report
```

---

## 7. Success Metrics

### 7.1 Quantitative Targets

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Smart Brevity Compliance | 95% | TBD | 🔄 |
| Tone Violations | <5 per month | TBD | 🔄 |
| Citation Coverage | 90%+ | 90%+ | ✅ |
| Build Success Rate | 100% | 100% | ✅ |
| Link Validity | 100% | 100% | ✅ |
| Performance Score | >95 | 95+ | ✅ |

### 7.2 Qualitative Goals

- Documentation feels welcoming yet authoritative
- Technical precision without condescension
- AI capabilities accurately represented
- Readers trust accuracy and completeness
- Content accessible to beginners and experts

---

## 8. Test Maintenance

### 8.1 Test Updates

Tests should evolve as style guidelines mature:
- Add new patterns as they emerge
- Refine thresholds based on actual usage
- Remove tests that don't add value
- Document test rationale

### 8.2 False Positive Handling

When tests flag valid content:
1. Review the flagged content manually
2. If content is correct, document why
3. Update test to handle similar cases
4. Add to allowlist if pattern is acceptable

### 8.3 Test Coverage Expansion

Priority areas for new tests:
- Accessibility compliance (WCAG AA)
- Mobile responsiveness validation
- SEO optimization checks
- Security best practices validation

---

## Appendices

### A. Test Script Locations

```
scripts/testing/
├── test_smart_brevity.py       # Structural tests
├── test_tone_compliance.py     # Tone analysis
├── test_ai_skepticism.py       # AI claim validation
├── test_citations.py           # Citation coverage
├── test_build.sh               # Build validation
└── test_performance.js         # Performance metrics
```

### B. Manual Review Checklists

Stored in: `docs/testing/manual-checklists/`
- polite-linus-review.md
- ai-skepticism-review.md
- technical-accuracy-review.md

### C. Test Data Fixtures

Stored in: `tests/fixtures/`
- good-examples/ (content that passes all tests)
- bad-examples/ (content that should fail specific tests)
- edge-cases/ (boundary conditions)

---

## Document History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-10-26 | Initial comprehensive test plan | Tester Agent |

---

**Next Review**: 2025-11-26
**Feedback**: Store improvements in hive memory under `hive/testing/feedback`
