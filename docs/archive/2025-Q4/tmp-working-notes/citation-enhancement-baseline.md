# Citation Enhancement Baseline Report

**Date:** 2025-11-11
**Posts Analyzed:** 14 (with References sections)
**Total Citations:** 199 (38 DOI + 161 arXiv inline references)

## Overview

### Current State
- Posts with citations: 14/63 (22.2%)
- Average citations per post (with References): 14.21
- **Unique** DOI citations: 25 (12.6% of unique)
- **Unique** arXiv citations: 104 (52.3% of unique)
- Total inline references: 199 (includes duplicates)
- DOI inline references: 38 (19.1%)
- arXiv inline references: 161 (80.9%)

### Citation Distribution

**Top Cited Posts:**
1. `transformer-architecture-deep-dive`: 15 citations (0 DOI, 15 arXiv)
2. `threat-intelligence-mitre-attack-dashboard`: 12 citations (12 DOI, 0 arXiv)
3. `progressive-context-loading-llm-workflows`: 11 citations (0 DOI, 11 arXiv)
4. `running-llama-raspberry-pi-pipeload`: 11 citations (0 DOI, 11 arXiv)
5. `vulnerability-prioritization-epss-kev`: 10 citations (2 DOI, 8 arXiv)
6. `iot-security-homelab-owasp`: 10 citations (10 DOI, 0 arXiv)
7. `post-quantum-cryptography-homelab`: 9 citations (2 DOI, 7 arXiv)

**Posts with Empty References Sections:**
- `vulnerability-management-scale-open-source`: Has References section but no DOI/arXiv (uses other sources)
- `blockchain-beyond-cryptocurrency`: Has References section but no DOI/arXiv (uses other sources)
- `zero-trust-security-principles`: Has References section but no DOI/arXiv (uses other sources)

## Quality Issues Found

### 1. DOI Format Inconsistency

**Formats found:**
- `https://doi.org/...`: 38 occurrences ✅ (preferred format, 100% HTTPS)
- `http://doi.org/...`: 0 occurrences ✅ (no HTTP upgrades needed)
- `*DOI: 10.xxxx/...`: 1 occurrence ⚠️ (needs URL conversion)
  - Location: `src/posts/2024-06-25-designing-resilient-systems.md:15`
  - Citation: NIST SP 800-207 - `*DOI: 10.6028/NIST.SP.800-207*`
- Plain `10.xxxx/...`: 0 occurrences ✅ (none found)

**Priority:** LOW (only 1 citation needs conversion)
**Affected posts:** 1 (`designing-resilient-systems.md`)
**Fix effort:** 5 min (manual conversion)

### 2. Broken Citations

**arXiv URL Issues:**
- 1 broken arXiv URL found: `https://arxiv.org/abs/` (empty ID)
- Location: Need to identify specific post

**Priority:** HIGH (broken link prevents access)
**Fix effort:** 10 min (find and fix)

### 3. Duplicate Citations

**DOI duplicates found:**
Top 10 most duplicated DOI prefixes:
- `10.1145/3*`: 8 occurrences
- `10.1007/s*`: 5 occurrences
- `10.1109/T*`: 4 occurrences
- `10.1016/j*`: 4 occurrences
- `10.1037/0*`: 3 occurrences
- `10.1007/9*`: 3 occurrences

**arXiv duplicates found:**
Top 20 most cited arXiv papers:
- `2409.04040`: 6 occurrences
- `2409.04249`: 5 occurrences
- `2409.13139`: 4 occurrences
- `2503.20020`: 3 occurrences
- `2501.06706`: 3 occurrences
- `2411.06382`: 3 occurrences
- `2402.13753`: 3 occurrences
- `2303.08774`: 3 occurrences
- `2210.17323`: 3 occurrences
- `2005.14165`: 3 occurrences
- `1906.08935`: 3 occurrences
- 9 papers cited 2 times each

**Priority:** MEDIUM
**Impact:** Citations are valid, just redundant across posts (common foundational papers)
**Fix effort:** 0 min (documentation only, not an error)

### 4. arXiv/DOI Balance

**Posts with 100% arXiv (no DOI citations):**
1. `transformer-architecture-deep-dive`: 0 DOI, 15 arXiv
2. `progressive-context-loading-llm-workflows`: 0 DOI, 11 arXiv
3. `running-llama-raspberry-pi-pipeload`: 0 DOI, 11 arXiv
4. `llm-agent-homelab-incident-response`: 0 DOI, 5 arXiv
5. `gvisor-container-sandboxing-security`: 0 DOI, 4 arXiv
6. `high-performance-computing`: 0 DOI, 4 arXiv
7. `ethics-large-language-models`: 0 DOI, 1 arXiv

**Posts with 100% DOI (no arXiv citations):**
1. `iot-security-homelab-owasp`: 10 DOI, 0 arXiv
2. `threat-intelligence-mitre-attack-dashboard`: 12 DOI, 0 arXiv

**Posts with balanced citations:**
1. `vulnerability-prioritization-epss-kev`: 2 DOI, 8 arXiv (1:4 ratio)
2. `post-quantum-cryptography-homelab`: 2 DOI, 7 arXiv (1:3.5 ratio)

**Priority:** MEDIUM
**Impact:** arXiv is valid for preprints (especially AI/ML topics), but peer-reviewed DOI preferred when available
**Fix effort:** Manual review required (30-60 min per post), may not have DOI alternatives

### 5. Citation Coverage Gap

**Discovery:** 3 posts have References sections but NO DOI/arXiv citations
- `vulnerability-management-scale-open-source`: Uses .gov, GitHub, other sources
- `blockchain-beyond-cryptocurrency`: Uses whitepapers, case studies, .org sources
- `zero-trust-security-principles`: Uses .gov, vendor docs, NIST publications

**Priority:** LOW
**Impact:** These posts cite government/industry sources appropriately (NIST, CISA, etc.)
**Fix effort:** 0 min (not an error, appropriate sourcing)

## Implementation Recommendations

### Phase A: Critical Fixes (P0) - 15 min

**1. Fix Broken arXiv URL**
- Find post with `https://arxiv.org/abs/)` (empty ID)
- Identify correct arXiv ID from context
- Update citation

**Effort:** 10 min

**2. Convert DOI: Prefix to URL**
- Convert 1 citation in `designing-resilient-systems.md`
- From: `*DOI: 10.6028/NIST.SP.800-207*`
- To: `[DOI: 10.6028/NIST.SP.800-207](https://doi.org/10.6028/NIST.SP.800-207)`

**Effort:** 5 min

### Phase B: Documentation (P1) - 15 min

**3. Duplicate Citation Report**
- Document most-cited papers (informational)
- Useful for identifying foundational literature
- No fixes required (duplicates are valid)

**Effort:** 15 min (report generation)

### Phase C: Manual Review (P2) - Deferred

**4. arXiv/DOI Balance Review**
- Research if peer-reviewed DOI versions exist for highly-cited arXiv papers
- Focus on papers with 3+ citations (14 candidates)
- Update citations where applicable

**Decision:** DEFER to future work (requires manual research per citation)
**Effort:** 30-60 min per post (7 posts = 3.5-7 hours total)

## Estimated Effort

### Minimum Viable (P0):
- Fix broken arXiv URL: 10 min
- Convert DOI: prefix: 5 min
- **Total P0:** 15 min ✅

### Full Enhancement (P0 + P1):
- P0 tasks: 15 min
- Duplicate report: 15 min
- **Total P0+P1:** 30 min ✅

### Complete (P0 + P1 + P2):
- P0+P1 tasks: 30 min
- arXiv/DOI balance review: 3.5-7 hours (7 posts)
- **Total:** 4-7.5 hours ❌ (exceeds budget)

**Recommendation:** Focus on P0 (15 min) + P1 (15 min) = 30 min total to stay within 2-3h budget.

## Priority Ranking

1. **P0 - Fix Broken arXiv URL** (HIGH impact, critical)
   - Effort: 10 min
   - Impact: Prevents 404 error
   - Automated: NO (requires context research)

2. **P0 - Convert DOI: Prefix** (LOW impact, quick fix)
   - Effort: 5 min
   - Impact: Consistency (1 citation)
   - Automated: YES

3. **P1 - Duplicate Detection Report** (MEDIUM impact, informational)
   - Effort: 15 min
   - Impact: Documentation/awareness of foundational papers
   - Automated: YES

4. **P2 - arXiv/DOI Balance** (MEDIUM impact, extensive manual work)
   - Effort: 3.5-7 hours
   - Impact: Improved source quality (7 posts)
   - Automated: NO (requires per-paper research)

## Discovery: Discrepancies from TODO.md Claims

**Claim:** "13/63 posts have References sections (20.6%)"
**Actual:** 14/63 posts have References sections (22.2%)
**Discrepancy:** +1 post (7.7% error)

**Claim:** "Total citations: 159 (12.23 avg for cited posts)"
**Actual:** Total citations: 199 inline (14.21 avg) OR 129 unique (9.21 avg)
**Discrepancy:** Definition ambiguity (inline vs unique)

**Claim:** "DOI citations: 38 (23.9%)"
**Actual:** DOI citations: 38 inline (19.1% of 199) OR 25 unique (19.4% of 129)
**Discrepancy:** Percentage calculation differs based on denominator

**Claim:** "arXiv citations: 182 (114.5% - some over-indexing)"
**Actual:** arXiv citations: 161 inline (80.9%) OR 104 unique (80.6%)
**Discrepancy:** -21 inline citations (-11.5% error), percentage was miscalculated

**Resolution:** Use inline counts (199 total, 38 DOI, 161 arXiv) for consistency with prior research.

## Next Steps for Coder

### Immediate (P0) - 15 min

1. **Find broken arXiv URL:**
   ```bash
   grep -n "https://arxiv.org/abs/)" src/posts/*.md
   ```
   - Identify post and context
   - Research correct arXiv ID
   - Fix citation

2. **Convert DOI: prefix in designing-resilient-systems.md:**
   - Line 15: NIST SP 800-207 citation
   - Convert to markdown link format

### Optional (P1) - 15 min

3. **Generate duplicate citation report:**
   - Create list of most-cited papers
   - Identify foundational literature
   - Document for future reference

### Future Work (P2) - Deferred

4. **arXiv/DOI balance review:**
   - 7 posts with 100% arXiv
   - Research peer-reviewed alternatives
   - Update where applicable

## Success Criteria

- ✅ Broken arXiv URL fixed (1 citation)
- ✅ DOI: prefix converted to URL format (1 citation)
- ✅ Build passes after changes
- ✅ Pre-commit validation passes
- ✅ Total effort ≤30 min (P0+P1)

## Deliverables

1. ✅ `tmp/citation-enhancement-baseline.md` (this file)
2. ✅ `tmp/posts-with-citations.txt` (14 posts identified)
3. ✅ `tmp/doi-urls-clean.txt` (25 unique DOI citations)
4. ✅ `tmp/arxiv-urls-clean.txt` (104 unique arXiv citations)
5. ✅ `tmp/doi-duplicates.txt` (duplicate DOI analysis)
6. ✅ `tmp/arxiv-duplicates.txt` (duplicate arXiv analysis)
7. ✅ `tmp/citation-balance.txt` (citation counts by post)
8. ✅ Priority ranking (P0-P2)
9. ✅ Discrepancy report (TODO.md corrections)

---

**CONCLUSION:** Citation quality is HIGH overall. Only 2 issues found (1 broken arXiv URL, 1 DOI: prefix). Total fix effort: 15 min (P0 only). No automated script needed - manual fixes are faster.
