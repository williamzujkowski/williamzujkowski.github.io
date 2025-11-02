---
title: Research Automation Tools
category: technical
priority: MEDIUM
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 1500
load_when:
  - Adding citations
  - Research validation
  - Running academic searches
dependencies:
  - standards/citation-research
tags: [research, automation, playwright, citations]
---

# Research Automation Tools

This document describes the research automation workflow, academic search tools, and citation validation systems.

## Research Integration Workflow

### For Every Blog Post

Follow this 4-step research integration process:

**1. Pre-Writing Research**
```python
# Validate research claims before writing
python scripts/blog-research/research-validator.py --post "post-title" --check-claims
```

**What it does:**
- Scans post for factual claims
- Identifies claims requiring sources
- Suggests search terms for validation

**2. Claim Validation with Playwright**
```python
# Search academic sources for supporting research
python scripts/blog-research/academic-search.py --query "specific claim" --sources "arxiv,zenodo,core"
```

**What it does:**
- Searches arXiv, Zenodo, CORE databases
- Returns papers with DOI/arXiv links
- Ranks results by relevance
- Extracts abstracts and metadata

**3. Source Citation Format**

See [Citation Format Standards](../standards/citation-research.md#source-citation-format---mandatory-hyperlinks) for complete formatting guidance including inline citations, reference section format, and hyperlink requirements.

**4. Visual Evidence**
- Extract figures/charts from papers (with permission/citation)
- Create original diagrams based on research data
- Include methodology visualizations

## Content Quality Standards

### Every Technical Claim Needs

- **Primary source**: Original research paper or official documentation
- **Secondary validation**: Additional supporting sources
- **Context**: Methodology, sample size, limitations
- **Recency check**: Publication dates within 2 years

### Red Flags to Avoid

For citation quality standards and red flags to avoid, see [citation-research.md](../standards/citation-research.md#content-quality-standards).

## Automated Research Validation

### Scripts for Research Integrity

**Validate research claims:**
```bash
python scripts/blog-research/research-validator.py --post src/posts/example.md
```

**Search academic sources:**
```bash
python scripts/blog-research/academic-search.py --query "quantum computing" --sources "arxiv,zenodo,core"
```

**Add academic citations:**
```bash
python scripts/blog-research/add-academic-citations.py --post src/posts/example.md
```

**Check citation hyperlinks:**
```bash
python scripts/blog-research/check-citation-hyperlinks.py
```

### Research Validator Features

**Capabilities:**
- Scan posts for unsupported claims
- Extract statistics and technical specifications
- Identify statements requiring citations
- Generate search queries for validation
- Track citation coverage percentage

**Usage:**
```bash
# Check specific post
python scripts/blog-research/research-validator.py --post src/posts/2025-10-29-example.md

# Batch check all posts
python scripts/blog-research/research-validator.py --batch

# Generate report
python scripts/blog-research/research-validator.py --batch --report
```

**Output example:**
```
Post: 2025-10-29-example.md
Citation coverage: 73% (8/11 claims)

Unsupported claims:
- "K3s uses 75% less memory than Kubernetes" (line 42)
- "EPSS prioritization reduces triage time by 60%" (line 87)
- "CVE-2024-1234 affects 40% of containers" (line 156)

Suggested searches:
- "K3s memory usage vs Kubernetes benchmark"
- "EPSS vulnerability prioritization study"
- "CVE-2024-1234 affected systems statistics"
```

## Research-Backed Content Structure

### Optimal Blog Post Format

1. **Introduction**: Set context with cited background
2. **Literature Review**: Brief overview of existing research
3. **Core Content**: Main points with supporting evidence
4. **Case Studies**: Real examples with sources
5. **Data Visualization**: Charts/graphs from research
6. **Limitations**: Acknowledge gaps or contradictions
7. **Future Directions**: Based on research trends
8. **References**: Complete citation list

## Playwright Research Automation

### Capabilities

**Use Playwright for:**
- Searching academic databases (arXiv, Zenodo, CORE, Google Scholar)
- Verifying technical specifications (official docs)
- Checking latest documentation versions
- Finding recent research papers
- Validating statistical claims
- Screenshot evidence collection

### Academic Search Script

**Primary tool:** `scripts/blog-research/academic-search.py`

**Features:**
- Multi-source search (arXiv, Zenodo, CORE)
- Parallel search across databases
- Result ranking by relevance
- DOI/arXiv link extraction
- Abstract and metadata retrieval

**Usage:**
```bash
# Single source search
python scripts/blog-research/academic-search.py --query "quantum computing" --sources "arxiv"

# Multi-source search
python scripts/blog-research/academic-search.py --query "LLM optimization" --sources "arxiv,zenodo,core"

# Limit results
python scripts/blog-research/academic-search.py --query "K3s kubernetes" --sources "arxiv" --limit 10
```

**Output format:**
```json
{
  "query": "quantum computing",
  "sources": ["arxiv", "zenodo", "core"],
  "results": [
    {
      "title": "Quantum Error Correction Advances",
      "authors": ["Smith, J.", "Doe, A."],
      "url": "https://arxiv.org/abs/2024.12345",
      "doi": "10.48550/arXiv.2024.12345",
      "abstract": "...",
      "published": "2024-10-15",
      "relevance_score": 0.95
    }
  ]
}
```

### Example Research Flow

**Complete workflow:**
```python
# 1. Identify claims needing validation
async def research_claim(claim):
    sources = ['arxiv', 'zenodo', 'core', 'scholar.google.com']
    results = []

    # 2. Search multiple sources in parallel
    for source in sources:
        results.extend(await search_source(source, claim))

    # 3. Validate and rank sources
    return validate_and_rank_sources(results)

# 4. Add citations to post
# (Use add-academic-citations.py)
```

## Validation

Before publishing, run the pre-publication checklist from [citation-research.md](../standards/citation-research.md#pre-publication-checklist).

**Additional technical checks:**
```bash
# Verify citation link format
grep -E '\[.*\]\(https?://.*\)' src/posts/[file].md
```

## Research Platform Integration

This module uses the platforms listed in [citation-research.md](../standards/citation-research.md#open-access-research-platforms):
- **Primary sources:** arXiv, Zenodo, CORE, Preprints.org, Research Square, SciPost
- **Domain-specific:** NIST, OWASP, SANS, RFCs, CNCF, kernel.org, LWN.net, etc.

The scripts below integrate with these platforms via Playwright automation.

## Citation Hyperlink Validation

### Check Citation Hyperlinks Script

**Tool:** `scripts/blog-research/check-citation-hyperlinks.py`

**What it does:**
- Extracts all citation links from blog posts
- Validates each URL returns HTTP 200
- Identifies broken links
- Suggests replacements (Wayback Machine, DOI redirects)
- Generates repair report

**Usage:**
```bash
# Check all posts
python scripts/blog-research/check-citation-hyperlinks.py

# Check specific post
python scripts/blog-research/check-citation-hyperlinks.py --post src/posts/example.md

# Auto-repair broken links
python scripts/blog-research/check-citation-hyperlinks.py --auto-repair
```

**Output:**
```
Checking citations in 56 posts...

✓ 312 working links
✗ 3 broken links

Broken links:
1. src/posts/2025-01-15-k3s.md:42
   Link: https://example.com/paper
   Status: 404
   Suggestion: https://web.archive.org/web/*/https://example.com/paper

2. src/posts/2025-03-22-epss.md:87
   Link: https://doi.org/10.xxxx/broken
   Status: 404
   Suggestion: Search arXiv for "EPSS prioritization"

Report saved to: reports/citation-link-check-2025-11-01.json
```

## Troubleshooting

### Academic Search Not Finding Papers

**Check:**
1. Query is specific enough
2. Spelling is correct
3. Source is appropriate for topic
4. Paper is publicly available

**Alternative approach:**
```bash
# Try broader search
python scripts/blog-research/academic-search.py --query "broad topic" --sources "arxiv,zenodo,core"

# Then narrow with grep
python scripts/blog-research/academic-search.py --query "quantum" | grep "error correction"
```

### Citation Validator False Positives

**Scenario**: Validator flags claim that has citation.

**Check:**
1. Citation is inline (within same paragraph)
2. Link is working (not 404)
3. Citation format matches expected pattern

### Playwright Search Timeout

**Increase timeout:**
```python
# In academic-search.py
page.set_default_timeout(60000)  # 60 seconds
```

## Related Documentation

- **Citation Standards**: `docs/context/standards/citation-research.md`
- **Blog Writing**: `docs/context/workflows/blog-writing.md`
- **Script Catalog**: `docs/context/technical/script-catalog.md`
