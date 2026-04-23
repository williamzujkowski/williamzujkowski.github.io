# Agent Instructions

**Status:** Authoritative
**Last Updated:** 2026-04-22
**Project:** Personal website and technical blog (Astro 6 + Svelte 5 + Tailwind CSS 4)

This file is the canonical guidance for AI coding agents working in this repo (Claude Code, Codex, Cursor, Aider, etc.). Harness-specific entry points (e.g. `CLAUDE.md`) import this file — edit here, not there.

Additional rules: `@.rules/nexus-agents.md`

---

## Quick Start

```bash
cd astro-site
npm install
npm run dev          # Dev server at localhost:4321
npm run build        # Production build → dist/
npm run preview      # Preview production build
npm run check        # Astro type checking
```

**Prerequisites:** Node.js 22+, npm, Git. Python 3.11+ and [UV](https://docs.astral.sh/uv/) for link validation scripts only.

---

## Project Structure

```
├── astro-site/                # Website source (Astro 6 + Svelte 5)
│   ├── src/
│   │   ├── components/        # Svelte & Astro components
│   │   ├── content/blog/      # Blog posts (Markdown, content collections)
│   │   ├── layouts/           # Page layouts (BaseLayout.astro)
│   │   ├── pages/             # Route pages
│   │   └── styles/            # Global CSS (Tailwind 4)
│   ├── public/                # Static assets
│   ├── astro.config.mjs       # Astro configuration
│   └── package.json           # Node.js dependencies
├── scripts/                   # Link validation CI pipeline (8 Python scripts)
│   ├── lib/logging_config.py  # Shared logging module
│   └── link-validation/       # Citation and link health checking
├── tests/unit/                # Unit tests (JS)
├── docs/                      # Research and link validation docs
├── .github/workflows/         # CI/CD (4 workflows)
└── nexus-agents.yaml          # AI agent orchestration config
```

---

## Core Principles

### NDA Compliance

**Golden rules:**
- NEVER discuss current or recent work incidents (2-3 year minimum buffer)
- ALWAYS use homelab attribution for technical examples
- NEVER reference specific government systems or agencies
- ALWAYS time-buffer work references ("years ago I worked on...")

**Safe patterns:**
```markdown
"In my homelab, I discovered X vulnerability in Y."
"Years ago, I worked on systems that faced Z challenge."
"Research shows this attack pattern is common."
```

**Unsafe patterns:**
```markdown
"Last month at work..."
"My current employer uses..."
"We recently discovered..."
```

### Writing Style

**"Polite Linus Torvalds" style for all technical writing.**

- Technical precision without explanation bloat
- Direct, casual-professional tone (engineer-to-engineer)
- Active voice, short sentences (avg <20 words)
- Zero tolerance for fluff and decorative punctuation
- Results-oriented language ("Show me the code")

**Prohibited:** Semicolons for sophistication, em-dashes for dramatic pauses, rhetorical questions, corporate hedging ("arguably", "potentially"), academic formality ("furthermore", "moreover"), filler phrases ("in order to" -> "to").

**Quality test:** If it sounds like "engineer explaining facts to another engineer" -> correct. If it sounds like TED talk/textbook/marketing -> wrong.

### Technical Authority & Security Expertise

**Author background:** Senior security engineer with system/network administration foundation.

**Technical depth required:**
- System-level: network protocols, OS internals, infrastructure security, virtualization, hardware
- Security: vulnerability assessment, incident response, forensics, architecture, compliance (NIST, CIS, DISA STIGs), threat modeling

**Credibility markers (NDA-compliant):**
- "Years of system administration taught me..." (vague timeframe)
- "After managing enterprise networks..." (no employer details)
- "In production environments, I've seen..." (no work specifics)
- "Homelab testing confirmed industry patterns..." (safe attribution)

**Security best practices in examples:**
- Least privilege (not root unless necessary)
- Defense in depth (multiple security layers)
- Fail-secure defaults (deny-by-default)
- Input validation and sanitization
- Secure credential management (never hardcoded secrets)

### Code Block Quality

**Decision framework:**
- **KEEP inline (<15 lines):** Teaches core concept, context-critical, complete and runnable
- **EXTRACT to gist (>20 lines):** Complete implementations, reference material, reusable
- **DELETE (any length):** Truncated pseudocode, redundant with official docs, better as prose/diagram

### File Organization

**NEVER save working files to the root folder.**

| Directory | Purpose |
|-----------|---------|
| `astro-site/src/` | Website source code |
| `scripts/link-validation/` | Link validation Python scripts |
| `tests/` | Test files |
| `docs/` | Documentation |

### Content Standards

- Blog posts require frontmatter: title, date, description, tags
- Citations required for technical claims (target 90%+ coverage)
- Hero images for all posts
- SEO: canonical URLs, Open Graph, Twitter Cards, structured data

---

## CI/CD Workflows

| Workflow | Purpose |
|----------|---------|
| `deploy.yml` | Build and deploy to GitHub Pages on push to main |
| `compliance-monitor.yml` | Build validation, Lighthouse, accessibility, HTML validation, security scan |
| `citation-validation.yml` | Citation coverage and link validation for blog posts |
| `link-monitor.yml` | Scheduled link health monitoring and repair |

---

## Python Scripts (Link Validation Only)

All Python scripts are in `scripts/link-validation/` with shared logging from `scripts/lib/logging_config.py`.

Dependencies managed via `pyproject.toml` (3 deps: aiohttp, certifi, tqdm). Install with `uv sync`.

---

## Key Configuration

- **Astro:** `astro-site/astro.config.mjs` (integrations, prefetch, syntax highlighting)
- **TypeScript:** `astro-site/tsconfig.json` (strict mode, path aliases)
- **Tailwind CSS:** CSS-only config via `@tailwindcss/vite` plugin
- **Content schemas:** `astro-site/src/content.config.ts` (Zod validation)

---

## Standards

- **Standards repo:** https://github.com/williamzujkowski/standards
- **Compliance:** NDA 100%, political neutrality 100%, personal focus 100%
- **Pre-commit:** Build validation on Astro file changes
- **CI:** GitHub Actions enforce standards on all pushes and PRs
