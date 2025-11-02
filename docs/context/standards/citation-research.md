---
title: Citation & Research Standards
category: standards
priority: HIGH
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 1800
load_when:
  - Creating blog posts
  - Adding citations
  - Research validation
  - Fact-checking claims
dependencies:
  - technical/research-automation
tags: [citations, research, sources, credibility, validation]
---

# Citation & Research Standards

## Module Metadata
- **Category:** standards
- **Priority:** HIGH
- **Load frequency:** Every blog post requiring research
- **Dependencies:** technical/research-automation

## Purpose
This module establishes the NO FABRICATION rule and defines research verification processes, open-access research platforms, citation formatting standards, and automated validation workflows for all technical claims.

## When to Load This Module
- **Creating blog posts** - Add sources from start
- **Adding citations** - Format properly with hyperlinks
- **Research validation** - Verify claims before publishing
- **Fact-checking** - Use Playwright automation

## Quick Reference

| Element | Standard | Example |
|---------|----------|---------|
| Primary Source | Original research paper or official docs | arXiv, NIST, RFCs |
| Secondary Validation | Additional supporting sources | 2-3 more reputable sources |
| Citation Format | Inline with working hyperlink | `[Study shows 73%](https://arxiv.org/abs/...)` |
| Publication Date | Within 2 years preferred | Check recency |
| Methodology Context | Include sample size, limitations | Always provide context |

**Red Flags to Avoid:**
- ❌ "Studies show..." without citation
- ❌ Specific percentages without source
- ❌ "It's well known that..." without evidence
- ❌ Technical specifications without verification
- ❌ Historical claims without references
- ❌ Performance metrics without methodology

---

## ABSOLUTE RULE: NO FABRICATION

**NEVER make up information, statistics, or claims. ALWAYS back statements with reputable sources.**

**Why it matters:** No citations = no credibility. Readers can verify your claims.

---

## Research Verification Process

### 1. Claim Identification
Scan content for factual claims, statistics, technical statements

### 2. Source Validation
Every claim MUST have a reputable source

### 3. Citation Integration
Properly cite all sources inline and in references

### 4. Fact Checking
Use Playwright to verify claims against authoritative sources

---

## Open-Access Research Platforms

### Primary Research Sources

1. **[arXiv](https://arxiv.org/)** - Preprints in physics, mathematics, computer science, quantitative biology, quantitative finance, statistics, electrical engineering and systems science, and economics

2. **[Zenodo](https://zenodo.org/)** - General-purpose open repository by CERN with DOI assignment

3. **[CORE](https://core.ac.uk/)** - Aggregates 250+ million open-access papers with API access

4. **[Preprints.org](https://www.preprints.org/)** - Multi-disciplinary preprints with moderation

5. **[Research Square](https://www.researchsquare.com/)** - Springer Nature integrated preprints

6. **[SciPost](https://scipost.org/)** - Community-driven peer review in physics

### Domain-Specific Sources

**Security:**
- NIST (nist.gov)
- OWASP (owasp.org)
- SANS (sans.org)
- CVE/NVD databases (cve.mitre.org, nvd.nist.gov)
- Security advisories (vendor-specific)

**AI/ML:**
- Papers with Code (paperswithcode.com)
- Google AI Research (ai.google/research)
- OpenAI Research (openai.com/research)
- Hugging Face papers (huggingface.co/papers)

**Cloud/DevOps:**
- CNCF resources (cncf.io)
- AWS/Azure/GCP documentation (official docs)
- HashiCorp guides (hashicorp.com/resources)

**Networking:**
- RFCs (ietf.org/rfc)
- Cisco documentation (cisco.com/c/en/us/support)
- Cloudflare Learning Center (cloudflare.com/learning)

**Linux/Kernel:**
- kernel.org documentation
- LWN.net (lwn.net)
- Red Hat resources (redhat.com/en/resources)

---

## Research Integration Workflow

### For Every Blog Post

#### 1. Pre-Writing Research
```python
# Use scripts/research-validator.py
python scripts/blog-research/research-validator.py --post "post-title" --check-claims
```

#### 2. Claim Validation with Playwright
```python
# Search academic sources
python scripts/blog-research/academic-search.py --query "specific claim" --sources "arxiv,zenodo,core"
```

#### 3. Source Citation Format - MANDATORY HYPERLINKS

**ALL citations MUST include clickable hyperlinks to sources**

**Inline Format:**
```markdown
[Study shows 73% improvement](https://arxiv.org/abs/2024.xxxxx)
```

**Reference Format:**
```markdown
1. **[Paper Title](https://doi.org/10.xxxx/xxxxx)** (Year)
   - Author names
   - *Journal/Conference Name*
```

**Links MUST point to:**
- arXiv, PubMed Central, or open-access versions
- DOI links (https://doi.org/10.xxxx/xxxxx)
- Official publisher/organization pages

**NEVER cite without a working hyperlink to the source**

#### 4. Visual Evidence
- Extract figures/charts from papers (with permission/citation)
- Create original diagrams based on research data
- Include methodology visualizations

---

## Content Quality Standards

### Every Technical Claim Needs

1. **Primary source** - Original research paper or official documentation
2. **Secondary validation** - Additional supporting sources (2-3)
3. **Context** - Methodology, sample size, limitations
4. **Recency check** - Publication dates within 2 years preferred

### Red Flags to Avoid

- ❌ "Studies show..." without citation
- ❌ Specific percentages without source
- ❌ "It's well known that..." without evidence
- ❌ Technical specifications without verification
- ❌ Historical claims without references
- ❌ Performance metrics without methodology

---

## Automated Research Validation

### Automated Validation Scripts

The following scripts enforce citation quality standards:
- `research-validator.py` - Scan for unsupported claims
- `academic-search.py` - Search arXiv, Zenodo, CORE
- `add-academic-citations.py` - Auto-add citations
- `check-citation-hyperlinks.py` - Validate links

**Complete usage guide:** [research-automation.md](../technical/research-automation.md#scripts-for-research-integrity)

---

## Research-Backed Content Structure

### Optimal Blog Post Format

1. **Introduction** - Set context with cited background
2. **Literature Review** - Brief overview of existing research
3. **Core Content** - Main points with supporting evidence
4. **Case Studies** - Real examples with sources
5. **Data Visualization** - Charts/graphs from research
6. **Limitations** - Acknowledge gaps or contradictions
7. **Future Directions** - Based on research trends
8. **References** - Complete citation list

---

## Playwright Research Automation

Use Playwright to automate research validation across academic databases.

**Capabilities:**
- Multi-source search (arXiv, Zenodo, CORE, Google Scholar)
- Technical specification verification
- Screenshot evidence collection

**Complete guide:** [research-automation.md](../technical/research-automation.md#playwright-research-automation)

---

## Pre-Publication Checklist

### Run Before Committing

```bash
# Validate all citations
python scripts/blog-research/check-citation-hyperlinks.py

# Check for uncited claims
python scripts/blog-research/research-validator.py --post src/posts/[file].md
```

### Verify Checklist

- [ ] All factual claims have citations with working hyperlinks
- [ ] Statistics include methodology and source
- [ ] Technical specs verified against official docs
- [ ] At least 3 reputable sources per major point
- [ ] No outdated information (check publication dates)
- [ ] Opposing viewpoints acknowledged
- [ ] Limitations clearly stated
- [ ] Visual aids properly attributed
- [ ] References section complete
- [ ] Playwright verification completed

---

## Cross-References

### Related Modules
- [technical/research-automation](../technical/research-automation.md) - Research script details (when implemented)
- [workflows/blog-writing](../workflows/blog-writing.md) - Blog post creation workflow
- [standards/humanization-standards](humanization-standards.md) - Content authenticity

### External References
- **Research Validator:** `scripts/blog-research/research-validator.py`
- **Academic Search:** `scripts/blog-research/academic-search.py`
- **Citation Checker:** `scripts/blog-research/check-citation-hyperlinks.py`

---

## Examples

### Example 1: Properly Cited Technical Claim

```markdown
K3s reduces memory footprint by 50% compared to full Kubernetes
([Rancher Labs, 2023](https://rancher.com/docs/k3s/latest/en/architecture/)).
In my homelab testing, K3s used 512MB RAM vs Kubernetes' 2GB minimum
([Official Kubernetes docs](https://kubernetes.io/docs/setup/), verified 2024-10-15).
```

**Analysis:** Primary source (Rancher docs), secondary validation (Kubernetes docs), personal testing confirmation, working hyperlinks, dates verified.

### Example 2: Research-Backed Statistics

```markdown
According to NIST's 2024 vulnerability report, 73% of CVEs in container
images result from outdated dependencies ([NIST NVD, 2024](https://nvd.nist.gov/vuln/statistics)).
This aligns with my Wazuh scanning results: 178 CVEs detected across 47
containers, with 127 (71%) attributed to stale packages.
```

**Analysis:** Official NIST source with working link, personal data confirms trend, percentages calculated from concrete measurements.

---

## Common Pitfalls

### Pitfall 1: Citing Without Verification
**Problem:** Copying citations from other sources without checking links
**Solution:** Click every link, verify it loads correct content
**Prevention:** Use `check-citation-hyperlinks.py` before committing

### Pitfall 2: Over-Reliance on Secondary Sources
**Problem:** Citing blog posts about research instead of original papers
**Solution:** Find the original paper, cite that directly
**Prevention:** Always trace claims back to primary sources

### Pitfall 3: Missing Context
**Problem:** Citing statistics without methodology or sample size
**Solution:** Include "tested with X samples over Y time period"
**Prevention:** Read the methods section of papers before citing

---

## Validation

### Citation Validation Commands

```bash
# Check all citation links work
python scripts/blog-research/check-citation-hyperlinks.py

# Validate claims have sources
python scripts/blog-research/research-validator.py --post src/posts/example.md

# Search for additional sources
python scripts/blog-research/academic-search.py --query "specific claim" --sources "arxiv,zenodo,core"
```

### Expected Output

```
Citation Validation Report
==========================
Post: src/posts/2025-11-01-example-post.md

Links Checked: 15
Working Links: 15
Broken Links: 0

Claims Verified: 23
Sourced Claims: 23
Unsourced Claims: 0

Citation Quality:
- Primary sources: 12 (52%)
- Secondary sources: 11 (48%)
- Average publication age: 1.2 years
- Domain diversity: 8 unique sources

Status: PASS ✓
```

---

## Changelog

### Version 1.0.0 (2025-11-01)
- Initial extraction from CLAUDE.md v3.0.0
- NO FABRICATION rule documented
- Open-access research platforms listed
- Research integration workflow defined
- Automated validation scripts included
- Citation formatting standards established

---

## Maintenance Notes

**Review Schedule:** Quarterly
**Last Review:** 2025-11-01
**Next Review:** 2026-02-01
**Maintainer:** Research quality agent

**Update Triggers:**
- New research platforms added
- Citation standards change
- Validation scripts updated
- Domain-specific source lists expand

---

**Parent Index:** [../../INDEX.yaml](../../INDEX.yaml)
**Category Index:** [../index.md](../index.md)
