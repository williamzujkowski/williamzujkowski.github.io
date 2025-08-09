---
title: Exploring Claude CLI Context and Compliance with My Standards Repository
date: 2025-07-22
tags:
- ai
- development
- standards
- productivity
description: How I built a comprehensive standards repository that transforms Claude
  CLI into a context-aware development powerhouse with 90% token reduction.
---
## The Problem: AI Tools That Forget Everything

Ever notice how every AI conversation starts from scratch? You explain your project structure, your coding standards, your preferences... again and again. It's like having a brilliant colleague with amnesia.

I was using Claude CLI daily but kept hitting the same frustrations:
- Explaining my coding style every. single. time.
- Getting inconsistent suggestions across sessions
- Watching token counts explode with context
- Copy-pasting the same standards repeatedly

Then I had an idea: What if I could give Claude permanent memory of how I like to work?

## Enter the Standards Repository

I built [github.com/williamzujkowski/standards](https://github.com/williamzujkowski/standards) – a comprehensive collection of development standards designed specifically for LLM consumption. It's not just documentation; it's an AI instruction manual for your projects.

### The Magic: CLAUDE.md

The centerpiece is a file called `CLAUDE.md` that acts as an intelligent router. Drop it in your project, and suddenly Claude understands:

```markdown
# Basic usage in your project
@load [CS:python + TS:pytest + SEC:*]

# Natural language works too
"I need to build a secure API"
→ Automatically loads: CS:api + SEC:auth + TS:integration
```

### Real Example: Setting Up a New Project

Here's how I used it yesterday to bootstrap a new Python service:

```bash
# Step 1: Clone standards to my project
git submodule add https://github.com/williamzujkowski/standards.git .standards

# Step 2: Copy CLAUDE.md to project root
cp .standards/docs/core/CLAUDE.md .

# Step 3: Start Claude CLI
claude chat
```

Then in Claude:

```
Me: I'm building a Python API that handles payment processing. 
    Set up the project structure following the standards.

Claude: I'll set up your payment processing API following the standards. 
        Loading [CS:python + CS:api + SEC:payments + COMPLIANCE:pci]...

        [Creates complete project structure with security controls,
         testing setup, CI/CD pipelines, and NIST compliance tags]
```

The result? A production-ready structure in minutes, not hours.

## The Power of Token Optimization

The real game-changer is the **90% token reduction**. Instead of feeding Claude entire documentation:

```markdown
# Old way (5000+ tokens)
"Here are my Python standards... [wall of text]
 Here are my API patterns... [another wall]
 Here are security requirements... [yet another wall]"

# New way (< 100 tokens)
@load [CS:python + CS:api + SEC:*]
```

Claude knows to reference the full standards without needing them in context every time.

## NIST Compliance Built-In

Since I work in government-adjacent spaces, NIST 800-53r5 compliance is crucial. The standards include automatic control tagging:

```python
# Claude automatically suggests NIST controls
@nist ac-2 "User account management"
class UserAccountManager:
    @nist ia-2 "Multi-factor authentication"
    @nist ia-5 "Authenticator management"
    def authenticate_user(self, credentials):
        # Implementation with security controls
        pass
```

Run the compliance checker:

```bash
./scripts/setup-nist-hooks.sh
git commit -m "Add user auth"
# Pre-commit hook validates NIST tags automatically
```

## My Favorite Features

### 1. Context-Aware Loading

Claude detects what you're working on and loads relevant standards:

```markdown
# Working on React component?
@load context:[auto]
# Automatically loads: FE:react + WD:components + TS:jest

# Fixing a security bug?
@task security_fix
# Loads: SEC:* + TS:regression + CS:error-handling
```

### 2. Project Kickstart

The kickstart prompt is pure magic. Feed it your project idea:

```markdown
Project: Homelab monitoring dashboard
Tech: Python backend, React frontend
Requirements: Real-time metrics, mobile-friendly

[Paste into Claude with kickstart prompt]

Result: Complete implementation plan with:
- Architecture decisions
- Tool recommendations  
- Security considerations
- Testing strategy
- 6-month roadmap
```

### 3. Intelligent Suggestions

Claude now makes connections I wouldn't:

```
You're using Redis for sessions.
Also consider: [rate-limiting, cache-invalidation patterns]
Teams like yours often use: [Redis Sentinel for HA]
Related standard: [CS:caching + SEC:session-management]
```

## Lessons Learned (The Hard Way)

### What Worked

1. **Start small**: I began with just Python standards, expanded gradually
2. **Version everything**: Standards evolve, Git tracks the journey
3. **Real examples**: Abstract standards < concrete code examples
4. **Token counting**: Every character matters for LLM efficiency

### What Didn't

1. **Over-engineering**: My first version had 200+ micro-standards. Too much.
2. **Perfect structure**: Spent weeks organizing. Claude doesn't care about folder beauty.
3. **Forcing adoption**: Team needs to see value before they'll use it

## Setting It Up for Your Projects

Want to try this yourself? Here's my recommended approach:

### Quick Start (5 minutes)

```bash
# 1. Add to existing project
curl -O https://raw.githubusercontent.com/williamzujkowski/standards/master/docs/core/CLAUDE.md

# 2. Tell Claude about it
"Use CLAUDE.md for standards. I'm building [your project type]"

# 3. Watch the magic happen
```

### Full Integration (30 minutes)

```bash
# 1. Clone the standards
git clone https://github.com/williamzujkowski/standards.git

# 2. Run setup script
./standards/scripts/setup-project.sh my-project

# 3. Customize for your needs
# Edit CLAUDE.md with your preferences

# 4. Set up NIST compliance (if needed)
./scripts/setup-nist-hooks.sh
```

## Real-World Impact

Since implementing this system:

- **Setup time**: 2 hours → 15 minutes for new projects
- **Consistency**: Same patterns across all my projects
- **Token usage**: Down 85% on average
- **Compliance**: NIST controls tagged automatically
- **Knowledge transfer**: New team members productive in days, not weeks

## Tips for Claude CLI Power Users

### 1. Create Project-Specific Standards

```markdown
# In your project's CLAUDE.md
project_context:
  style: "Google Python style"
  testing: "pytest with 90% coverage"
  special_rules:
    - "All API endpoints need rate limiting"
    - "Use structured logging everywhere"
```

### 2. Chain Commands Efficiently

```bash
# My typical workflow
claude chat << 'EOF'
@load [CS:python + SEC:*]
@task refactor
Review this module for standards compliance:
$(cat src/payment_processor.py)
Generate improved version with tests.
EOF
```

### 3. Build Your Own Standards

Don't just use mine – fork and customize:

```markdown
# Add your team's conventions
team_standards:
  pr_size: "Max 400 lines"
  commit_style: "Conventional commits"
  review_sla: "24 hours"
```

## The Unexpected Benefits

Beyond the obvious productivity gains, this system has:

1. **Documented tribal knowledge**: Those "oh, we always do X" conversations are now codified
2. **Improved code reviews**: "Does this follow our standards?" → "Run the checker"
3. **Easier onboarding**: Hand new devs the standards repo, they're ready to go
4. **Consistent AI assistance**: Claude gives the same advice every time

## Where It's Heading

I'm working on:

- **VS Code extension**: Real-time standard suggestions while coding
- **GitHub Actions integration**: Automated standards enforcement in PRs
- **Team analytics**: Track which standards get used/violated most
- **LLM fine-tuning**: Train models specifically on your standards

## Try It Yourself

The repository is open source and MIT licensed. Fork it, customize it, make it yours:

[github.com/williamzujkowski/standards](https://github.com/williamzujkowski/standards)

Start small – even just adding a CLAUDE.md with your basic preferences will transform how you work with AI tools.

## The Bottom Line

We're using AI tools wrong if we're explaining the same things repeatedly. These tools should learn our preferences once and apply them consistently.

This standards repository turns Claude CLI from a smart tool into YOUR smart tool – one that knows your style, your requirements, and your way of working.

The future isn't just AI-assisted development; it's AI that actually knows how you like to develop.

---

*Have you built something similar? How do you maintain consistency with AI tools? Drop me a line – I'm always looking for new patterns to steal... I mean, learn from.*