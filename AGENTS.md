# Agent Instructions

**Status:** Authoritative
**Last Updated:** 2026-04-22
**Project:** Personal website and technical blog (Astro 6 + Svelte 5 + hand-written CSS / Remarque design tokens)

This file is the canonical guidance for AI coding agents working in this repo (Claude Code, Codex, Cursor, Aider, etc.). Harness-specific entry points (e.g. `CLAUDE.md`) import this file — edit here, not there.

Additional rules: `@.rules/nexus-agents.md`

---

## Quick Start

```bash
cd astro-site
pnpm install
pnpm dev             # Dev server at localhost:4321
pnpm build           # Production build → dist/
pnpm preview         # Preview production build
pnpm check           # Astro type checking
```

**Prerequisites:** Node.js 22+, pnpm, Git. Python 3.11+ and [UV](https://docs.astral.sh/uv/) for link validation scripts only. The repo is pnpm-only (`astro-site/pnpm-lock.yaml`); CI and the pre-commit hook both run `pnpm`.

---

## Project Structure

```
├── src/                       # Content collections (loaded by astro-site)
│   ├── posts/                 # Blog posts (Markdown) — astro-site/src/content.config.ts globs ../src/posts
│   └── projects/              # Project entries (Markdown)
├── astro-site/                # Website source (Astro 6 + Svelte 5)
│   ├── src/
│   │   ├── components/        # Svelte & Astro components
│   │   ├── content.config.ts  # Content collection schemas (points at ../src/posts, ../src/projects)
│   │   ├── layouts/           # Page layouts (BaseLayout.astro)
│   │   ├── pages/             # Route pages
│   │   └── styles/            # Global CSS (hand-written; Remarque design tokens)
│   ├── public/                # Static assets
│   ├── astro.config.mjs       # Astro configuration
│   └── package.json           # Node.js dependencies (pnpm)
├── scripts/                   # Python tooling
│   ├── lib/logging_config.py  # Shared logging module
│   ├── link-validation/       # Citation and link health checking (7 scripts)
│   └── blog-audit/            # Blog audit helpers
├── docs/                      # Research and link validation docs
├── .github/workflows/         # CI/CD (7 workflows)
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

**"Polite Linus Torvalds, with a pulse" — precise and direct, but genuinely funny.**

The old rule was right about precision and wrong to strip out the personality. Keep every precise thing; add the wit that makes a post worth reading twice.

**Keep (non-negotiable):**
- Technical precision without explanation bloat
- Active voice; vary sentence length (mostly short, the occasional long one for rhythm)
- Zero corporate hedging ("arguably", "potentially"), zero academic formality ("furthermore", "moreover"), zero filler ("in order to" -> "to")
- Results-oriented: show the thing, then say what you learned

**Add (the pulse):**
- **Dry wit through observation, not jokes bolted on.** The funny comes from noticing something true and stating it deadpan. If a line would survive being cut and the sentence is worse without it, keep it. If it's a joke for its own sake, cut it.
- **Understatement over enthusiasm.** "The browser had opinions about this" beats "it was SO frustrating!!"
- **Apt, unexpected analogies.** A moody API is a temperamental analog synth. Use sparingly; one good image beats five.
- **Self-aware first person.** The story of building the thing, including the parts that went sideways, told without self-flagellation. Warm about your own projects, not a roast.
- **Register: dry British humor with an American bent** — sardonic when something earns it, never mean; a bit absurdist in small, earned doses.

**Lead with what the thing IS.** For project posts especially: introduce it, make the reader want it, tell the story of building it, *then* get into the sharp technical or security details. Don't open a "here's a fun thing I built" post like a threat-model doc.

**Still prohibited:** exclamation-mark enthusiasm, memes/references that will date, quirk that obscures the technical point, TED-talk uplift, three-item parallelism as a crutch, "it's not X, it's Y" as a reflex.

**Em-dashes:** allowed for a genuine parenthetical aside, banned for manufactured drama. If the dash is doing comic timing or clarifying an aside, fine. If it's there to sound profound, cut it.

**Quality test:** If it reads like a sharp engineer being honest and a little funny about their own work -> correct. If it reads like a TED talk, a marketing page, or a robot performing whimsy -> wrong.

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
- Social images are generated per post at build time (`/og/<slug>.png`) — no hero-image frontmatter
- SEO: canonical URLs, Open Graph, Twitter Cards, structured data

---

## Content QA pipeline

Four layers, each owning a distinct concern. When adding a new check,
pick the layer that matches the latency, cost, and feedback profile.
The Layer-1 skills live in `.claude/skills/blog-*/` (tracked in git).

```
┌─ 1. Pre-publish (interactive, author-invoked via Skill tool) ─────┐
│   blog-pre-publish runs:                                          │
│     blog-overlap        → topic overlap with prior posts          │
│     blog-factcheck      → semantic verification of cited claims   │
│     blog-llm-tells      → voice/prose LLM-tell scrub              │
│     blog-nda-check      → contextual NDA-compliance               │
│     blog-argument-shape → thesis + evidence + falsifiability      │
└───────────────────────────────────────────────────────────────────┘
                            │ author commits
                            ▼
┌─ 2. Pre-commit (synchronous, blocking) ───────────────────────────┐
│   .git/hooks/pre-commit                                           │
│     pnpm run build (only when astro-site/ or src/ files changed)  │
└───────────────────────────────────────────────────────────────────┘
                            │ author pushes
                            ▼
┌─ 3. On push / PR (every commit, blocking) ────────────────────────┐
│   deploy.yml             → build + deploy to GitHub Pages         │
│   audits.yml             → Remarque design audits                 │
│                            (contrast, typography, color tokens,   │
│                            APCA-advisory)                         │
│   a11y.yml               → axe-playwright accessibility           │
│   compliance-monitor.yml → Lighthouse, HTML validation,           │
│                            citation coverage %, NDA pattern grep, │
│                            Trivy + Gitleaks + pip-audit           │
│   tests.yml              → pytest for scripts/link-validation     │
│                            (only on scripts/** changes)           │
└───────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─ 4. Scheduled (cron) ─────────────────────────────────────────────┐
│   link-monitor.yml       → daily 03:00 UTC + on PR to             │
│                            src/posts/**: external link health,    │
│                            via scripts/link-validation/ pipeline. │
│                            Auto-PRs high-confidence repairs.      │
│   citation-validation.yml → weekly Mon 09:00 UTC: deeper          │
│                            citation link audit; opens tracking    │
│                            issue on broken citations.             │
└───────────────────────────────────────────────────────────────────┘
```

### Concern-to-layer ownership table

| Concern | Owner | Why |
|---------|-------|-----|
| Voice / LLM tells | Layer 1 (`blog-llm-tells`) | Author-time judgment call, not blocking |
| Citation accuracy (semantic) | Layer 1 (`blog-factcheck`) | Requires LLM to compare claim vs source page |
| Citation link health (HTTP) | Layer 4 (`link-monitor.yml`) | Cheap, automated, scales |
| Topic overlap with prior posts | Layer 1 (`blog-overlap`) | Author decides refinement vs new arg |
| Thesis / evidence / falsifiability | Layer 1 (`blog-argument-shape`) | Author-time editorial judgment |
| Build correctness | Layer 2 (pre-commit) | Fast, blocks bad commits |
| Astro design tokens | Layer 3 (`audits.yml`) | Per-commit, blocks broken design |
| Accessibility | Layer 3 (`a11y.yml`) | Per-commit, axe-playwright |
| Lighthouse / HTML validation | Layer 3 (`compliance-monitor.yml`) | Per-commit, advisory |
| NDA enforcement (mechanical) | Layer 3 (`compliance-monitor.yml`) | Per-commit grep, 13 phrases — ADVISORY by design: 7 of the 13 (e.g. "in production", "sensitive", "government") appear in legitimate prose across 20-30 existing posts, so blocking would red every build. The contextual Layer-1 `blog-nda-check` is the real gate. |
| NDA enforcement (contextual) | Layer 1 (`blog-nda-check`) | Author-time LLM judgment: tense, scale revelations, implicit current-engagement, gov-agency context — beyond what grep can catch |
| Citation coverage % | Layer 3 (`compliance-monitor.yml`) | Per-commit metric, advisory |
| Security scans (Trivy, Gitleaks, pip-audit) | Layer 3 (`compliance-monitor.yml`) | Per-commit |

### Anti-patterns to avoid

- **Don't add a check in Layer 1 that already exists in Layer 3.** Voice
  scrub is a Layer-1 concern (author judgment); NDA pattern enforcement
  is a Layer-3 concern (mechanical, blocks publish).
- **Don't add a check in Layer 3 that's already in Layer 4.** External
  link checking belongs in Layer 4; running it on every push wastes CI.
- **Don't add a check in Layer 1 that requires CI access.** Skills are
  interactive and depend on the author running them. Anything that must
  run on every commit belongs in Layer 2 or 3.

### Workflow detail

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `deploy.yml` | push/dispatch | Build and deploy to GitHub Pages |
| `audits.yml` (Remarque) | push/PR | Design tokens, contrast, typography floor |
| `a11y.yml` (axe-playwright) | push/PR | Accessibility test suite |
| `compliance-monitor.yml` | push/PR/daily | Lighthouse, HTML validation, citation coverage, NDA pattern grep, Trivy/Gitleaks/pip-audit |
| `link-monitor.yml` | daily/dispatch + PR on `src/posts/**` | External link health via Python pipeline; auto-PRs repairs |
| `citation-validation.yml` | weekly/dispatch | Deeper weekly citation audit; opens tracking issue |
| `tests.yml` | push/PR on `scripts/**`, dispatch | Python pytest gate for the link-validation pipeline |

---

## Python Scripts (Link Validation Only)

All Python scripts are in `scripts/link-validation/` with shared logging from `scripts/lib/logging_config.py`.

Dependencies managed via `pyproject.toml` (3 deps: aiohttp, certifi, tqdm). Install with `uv sync`.

---

## Key Configuration

- **Astro:** `astro-site/astro.config.mjs` (integrations, prefetch, syntax highlighting)
- **TypeScript:** `astro-site/tsconfig.json` (strict mode, path aliases)
- **Styling:** Hand-written CSS with Remarque design tokens in `astro-site/src/styles/` (no Tailwind)
- **Content schemas:** `astro-site/src/content.config.ts` (Zod validation)

---

## Standards

- **Standards repo:** https://github.com/williamzujkowski/standards
- **Compliance:** NDA 100%, political neutrality 100%, personal focus 100%
- **Pre-commit:** Build validation on Astro file changes
- **CI:** GitHub Actions enforce standards on all pushes and PRs
