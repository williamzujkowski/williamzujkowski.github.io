# Mermaid Diagram Templates

This directory contains reusable Mermaid diagram templates for blog posts.

## Purpose

- **Consistency:** Ensure similar diagrams follow the same structure
- **Efficiency:** Start with proven templates instead of creating from scratch
- **Guidance:** Provide visual examples for common architectural patterns

## Template Catalog

### 1. Threat Actor Security Template

**File:** `templates/threat-actor-security-template.mmd`

**Use for:**
- Security architecture posts
- Threat modeling discussions
- Cybersecurity tutorials
- Defense-in-depth explanations

**Features:**
- Threat actor categorization
- Attack vector mapping
- Target asset identification
- Defense layer visualization

**Color scheme:** Blue/Red gradient (security topics)

**Usage count:** 10 existing posts

---

### 2. ML/AI Data Pipeline Template

**File:** `templates/ml-data-pipeline-template.mmd`

**Use for:**
- Machine learning posts
- AI model training guides
- LLM fine-tuning tutorials
- MLOps discussions

**Features:**
- Complete data pipeline flow
- Training loop visualization
- Evaluation metrics tracking
- Deployment and monitoring

**Color scheme:** Purple/Pink gradient (AI/ML topics)

**Usage count:** 14 existing posts

---

### 3. Cloud Frontend Architecture Template

**File:** `templates/cloud-frontend-template.mmd`

**Use for:**
- Cloud deployment guides
- Infrastructure architecture posts
- Full-stack application tutorials
- System design discussions

**Features:**
- Frontend layer (CDN, static assets)
- API gateway with authentication
- Application layer (cache, queue)
- Data layer (database, storage)
- Monitoring and observability

**Color scheme:** Sky Blue/Teal gradient (cloud topics)

**Usage count:** 3 existing posts

---

## How to Use Templates

### Step 1: Choose Template

Review templates in `diagrams/templates/` and select the pattern that matches your post topic.

### Step 2: Copy Template

Copy the Mermaid diagram code from the template file into your blog post.

### Step 3: Customize

Modify the template for your specific use case:
- Update node labels
- Add/remove components
- Adjust relationships (arrows)
- Change subgraph titles
- Customize for your architecture

### Step 4: Validate

Ensure your diagram renders correctly:
- Check syntax with Mermaid Live Editor (https://mermaid.live/)
- Preview in local development (`npm run serve`)
- Verify mobile responsiveness

### Step 5: Document

If you create a new reusable pattern, consider adding it to `templates/` for future posts.

---

## Diagram Style Guide

### Color Consistency

Use these color gradients for different topics:

- **Security:** Blue/Red (#1e3a8a → #dc2626)
- **AI/ML:** Purple/Pink (#7c3aed → #ec4899)
- **Cloud:** Sky Blue/Teal (#0ea5e9 → #10b981)
- **Blockchain:** Amber/Emerald (#f59e0b → #10b981)
- **Quantum:** Violet/Blue (#8b5cf6 → #3b82f6)
- **DevOps:** Green/Blue (#10b981 → #3b82f6)

### Naming Conventions

- **Node IDs:** CamelCase (e.g., `DataPipeline`, `ThreatActor`)
- **Labels:** Descriptive phrases in square brackets (e.g., `[External Attackers]`, `[Raw Data]`)
- **Subgraphs:** Title case with quotes (e.g., `subgraph "Data Pipeline"`)

### Layout Preferences

- **Top-down (`graph TB` or `graph TD`):** Architecture diagrams, hierarchies, layer models
- **Left-right (`graph LR`):** Workflows, pipelines, sequential processes
- **Flowchart (`flowchart LR` or `flowchart TD`):** Decision trees, process flows

### Complexity Targets

- **Simple diagrams:** ≤20 lines (ideal for quick illustration)
- **Moderate diagrams:** 20-40 lines (acceptable for most posts)
- **Complex diagrams:** 40-50 lines (consider simplification)
- **Very complex:** ≥50 lines (split into multiple diagrams)

**Rule:** If your diagram exceeds 50 lines, split it into multiple diagrams or simplify.

---

## Inline vs Reference-Based

**Current strategy: All diagrams stay inline within blog posts.**

**Rationale:**
- Diagrams provide essential visual context
- Inline placement improves reader comprehension
- Minimal maintenance burden (diagrams rarely change)
- Plain Markdown compatibility preserved

**Templates are copy-paste starting points, not centralized includes.**

---

## Future Expansion

As new common patterns emerge, consider adding templates for:

- Network topology diagrams (VLAN segmentation, firewall rules)
- CI/CD pipeline architectures
- Microservices architectures
- Event-driven architectures
- Blockchain consensus mechanisms
- Quantum circuit diagrams

**Contribution criteria:**
- Pattern used in 3+ existing posts
- Template provides 80%+ of structure
- Customization straightforward for most use cases

---

## Tools and Resources

### Mermaid Resources

- **Mermaid Live Editor:** https://mermaid.live/
- **Official Documentation:** https://mermaid.js.org/
- **Syntax Cheatsheet:** https://jojozhuang.github.io/tutorial/mermaid-cheat-sheet/

### Diagram Generation Tools

- **PlantUML to Mermaid converter:** https://plantuml-to-mermaid.com/
- **Draw.io to Mermaid:** Manual conversion required
- **Excalidraw to Mermaid:** Manual conversion required

### Validation

Test diagrams before publishing:
```bash
# Local development preview
npm run serve

# Check diagram syntax
# Use Mermaid Live Editor: https://mermaid.live/
```

---

## Analysis Report

For complete analysis of existing Mermaid diagrams across all blog posts, see:

**Report:** `docs/reports/mermaid-diagram-analysis-report.md`

**Key findings:**
- 49 posts contain Mermaid diagrams (86.0% of blog)
- 65 total diagrams
- 15 large diagrams (≥30 lines)
- 3 common patterns (27 posts use duplicate structures)

**Recommendation:** DEFER centralization until 80+ posts or 100+ diagrams

---

**Last updated:** 2025-11-01
**Maintained by:** Code Implementation Agent
