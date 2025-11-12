---
title: NDA Compliance & Content Boundaries
category: core
priority: HIGH
version: 2.0.0
last_updated: 2025-11-11
estimated_tokens: 3500
load_when:
  - Writing blog posts
  - Creating content mentioning work/career
  - Discussing security topics
  - Referencing professional experience
  - Demonstrating senior-level expertise
  - Establishing technical credibility
dependencies: [standards/writing-style.md]
tags: [security, privacy, boundaries, nda, career, family, expertise, attribution, senior-engineer]
---

# NDA Compliance & Content Boundaries

## Purpose
This module defines **strict boundaries** for content creation to ensure 100% NDA compliance and personal privacy protection. All blog posts, documentation, and public content MUST adhere to these rules to protect career, clearance, and family safety.

## When to Load This Module
- **Before writing any blog post** - Verify no NDA violations
- **When referencing professional experience** - Use safe patterns only
- **When discussing security topics** - Homelab attribution required
- **When mentioning family** - Privacy protection mandatory

## Quick Reference

### NEVER Discuss
- Current work incidents (minimum 2-3 year buffer)
- Specific government systems or agencies
- Active vulnerabilities at work
- Timeline-specific work events
- Team members or organizational structure

### ALWAYS Use
- "Years ago, I learned..." (vague timeframes)
- "In my homelab..." (personal projects)
- "Research suggests..." (academic framing)
- "A common pattern..." (hypothetical)

---

## Government Work Security Guidelines

**Your clearance and career matter more than a blog post. When in doubt, leave it out.**

### CRITICAL: What NEVER to Discuss

- **Current work incidents** (minimum 2-3 year buffer)
- **Specific government systems**
- **Active vulnerabilities at work**
- **Timeline-specific work events**
- **Team members or organizational structure**

### Safe Pattern Examples

✅ **Safe patterns:**
```markdown
✅ "In my homelab, I discovered X vulnerability in Y."
✅ "Years ago, I worked on systems that faced Z challenge."
✅ "Research shows this attack pattern is common."
```

❌ **Unsafe patterns:**
```markdown
❌ "Last month at work..."
❌ "My current employer uses..."
❌ "We recently discovered..."
```

### Professional Content Guidelines

**Do Share:**
- Professional challenges and wins (from years ago)
- Learning struggles and breakthroughs (personal projects)
- Creative process (home lab/research)
- Book and media recommendations
- Opinions on industry trends
- Historical lessons learned (appropriately aged)
- Personal research and experiments

**Don't Share:**
- Current or recent work incidents
- Specific government agency details
- Active security measures or controls
- Ongoing investigations or issues
- Current vulnerabilities or threats at work
- Specific systems or technologies in use
- Team member details or roles
- Timeline-specific work events
- Employer confidential information
- Others' stories without permission
- Financial specifics
- Personal relationship details (beyond basics)

---

## Personal & Family Information

### ACCURATE FAMILY FACTS

- **Children:** ONE child (son)
- **Son's birthday:** June 11, 2023
- **Current age calculation:** As of November 1, 2025, he is 2 years, 4 months, 21 days old
  - Age formula: `(current_date - June 11, 2023)` in years and months
  - **NEVER claim he is older** - always calculate age from birthdate
  - **NEVER claim multiple children** - singular "son" or "child" only

### When to Mention Parenting (Use Sparingly)

✅ **Appropriate contexts:**
- Time management discussions: "With a toddler, homelab time is usually after bedtime..."
- Work-life balance: "Running security scans overnight since my son's bedtime is 7:30 PM..."
- Learning/teaching parallels: "Teaching my son to walk reminds me of debugging - iteration and patience..."
- Power consumption concerns: "Since my son was born, I'm more conscious of homelab energy costs..."
- Noise considerations: "Moved the server rack to avoid waking my son..."

❌ **Avoid overuse:**
- Don't mention in EVERY post (target: 1 in 5-7 posts maximum)
- Don't force parenting analogies into unrelated technical content
- Don't share identifying details (name, photos, specific routines beyond general statements)
- Don't make parenting the central narrative unless directly relevant

### Examples of Appropriate Use

```markdown
✅ "With a toddler at home, my late-night homelab experiments now happen during naptime..."
✅ "Since becoming a parent in 2023, I've prioritized automation to free up time..."
✅ "My Dell R940 rack mount is in the basement - toddler-proofing required relocating it..."
```

### Examples of Overuse/Inappropriate

```markdown
❌ "My kids love watching Raspberry Pi lights blink..." (INACCURATE - one child, age 2)
❌ "Teaching my children about cryptography..." (INACCURATE - he's 2 years old)
❌ "As a father of three..." (INACCURATE - one child)
❌ Using parenting analogies in every single blog post
```

### Humanization Balance

Parenting is ONE humanization element among many. Prioritize:
1. **Homelab stories** (most posts)
2. **Technical failures** (most posts)
3. **Concrete measurements** (every post)
4. **Uncertainty phrases** (every post)
5. **Parenting/time constraints** (occasional, 15-20% of posts)

### Privacy Protection

- NEVER use son's name
- NEVER share photos
- NEVER mention specific locations (daycare, pediatrician, etc.)
- NEVER share detailed schedules or routines that could identify patterns
- Keep references generic: "my son," "toddler," "young child"

---

## Senior Engineer Attribution Patterns

### Purpose
Demonstrate technical depth and senior-level expertise without violating NDA or revealing current work details. These patterns allow credible attribution of experience while maintaining strict privacy boundaries.

### When to Use This Section
- Establishing technical credibility in blog posts
- Referencing professional expertise safely
- Demonstrating system/network administration knowledge
- Sharing security engineering insights

### CRITICAL: Experience Framing Rules

**Core principle:** Attribute expertise to PAST roles, HOMELAB experiments, or RESEARCH, never current work.

**Safe timeframe patterns:**
```markdown
✅ "With 15+ years in security engineering..."
✅ "Over a decade of system administration experience has shown..."
✅ "Years of network engineering work taught me..."
✅ "Throughout my career spanning [timeframe], I've learned..."
```

**Unsafe recent references:**
```markdown
❌ "In my current senior engineer role..."
❌ "Last year at work, I architected..."
❌ "My team recently implemented..."
❌ "As a senior security engineer at [employer], I..."
```

### Senior Security Engineer Attribution

**DO demonstrate expertise through:**

1. **Aggregate experience statements** (no specific incidents)
   ```markdown
   ✅ "Over 15 years of security engineering, I've seen authentication bypass attacks evolve from simple SQL injection to sophisticated token manipulation."

   ✅ "Throughout my career, network segmentation failures consistently stem from the same root cause: assuming Layer 3 boundaries prevent lateral movement."

   ✅ "Senior security roles teach you one truth: preventive controls fail less than detective controls, but both fail eventually."
   ```

2. **Homelab validation of professional patterns** (attribution shift)
   ```markdown
   ✅ "In my homelab, I replicated a privilege escalation pattern I've seen across multiple environments over the years. Kubernetes RBAC misconfigurations follow predictable patterns..."

   ✅ "Years of experience showed me firewalls are often misconfigured. I validated this in my homelab by testing 12 common rulesets - 83% had shadowed rules that never matched traffic."
   ```

3. **Research-backed professional observations** (academic framing)
   ```markdown
   ✅ "Research from [source] aligns with what I've observed professionally: 70% of breaches exploit known vulnerabilities older than 2 years. My homelab testing confirmed patch deployment delays create predictable windows..."

   ✅ "Academic literature on lateral movement matches patterns I've studied: attackers spend 200+ days in networks not because detection is impossible, but because baselines are missing. I tested this hypothesis in my homelab..."
   ```

4. **Lessons learned (time-buffered, genericized)**
   ```markdown
   ✅ "Years ago, I worked on systems where multi-factor authentication rollout took 18 months. The technical implementation took 2 weeks - the remaining time was change management. Lesson: security engineering is 20% technical, 80% organizational."

   ✅ "Early in my career, I learned incident response plans fail at first contact with reality. I've since built homelab scenarios to test response automation..."
   ```

**DON'T reveal current work:**
```markdown
❌ "In my current senior engineer role, I recently discovered a critical SSRF vulnerability in our API gateway."

❌ "Last quarter, I architected a zero-trust network for [employer] using Cloudflare Access and WireGuard."

❌ "My team's security roadmap for 2025 includes implementing SIEM correlation rules for..."

❌ "As senior security engineer at [agency], I'm responsible for securing 500+ endpoints against..."
```

### System/Network Administration Context

**Safe patterns for demonstrating sysadmin expertise:**

1. **Infrastructure scale references** (generic, homelab-comparable)
   ```markdown
   ✅ "I've administered networks ranging from 10-node homelabs to enterprise environments with 1,000+ endpoints. Monitoring strategies scale differently..."

   ✅ "Managing systems at scale taught me automation isn't optional. My homelab deployment pipeline (Ansible + GitOps) mirrors patterns from larger environments."

   ✅ "Years of sysadmin work showed me backup verification matters more than backup execution. My homelab tests restoration monthly..."
   ```

2. **Technology stack experience** (vendor-neutral, not work-specific)
   ```markdown
   ✅ "I've worked with virtualization platforms from VMware to Proxmox to KVM. My homelab runs Proxmox because..."

   ✅ "Network administration across Cisco, Juniper, and open-source stacks taught me vendor lock-in risks. My homelab uses pfSense and VyOS to maintain flexibility..."

   ✅ "Storage architecture experience spans SAN, NAS, and hyperconverged systems. My homelab Dell R940 runs TrueNAS to test ZFS replication..."
   ```

3. **Operational lessons** (time-buffered, lessons-focused)
   ```markdown
   ✅ "Years ago, I learned monitoring alerts need 3 tiers: informational (log only), warning (ticket), critical (page). My homelab Prometheus setup mirrors this..."

   ✅ "Early in my career, a production outage taught me the value of graceful degradation. I've since built homelab services with circuit breakers and fallback modes..."

   ✅ "Network troubleshooting experience taught me to trust packet captures over assumptions. My homelab runs persistent tcpdump for post-incident analysis..."
   ```

4. **Architecture decisions** (homelab attribution required)
   ```markdown
   ✅ "Professional experience showed me hub-and-spoke VPN topologies don't scale. My homelab tests full-mesh WireGuard for comparison..."

   ✅ "I've seen DNS resolution failures cause cascading outages across multiple environments. My homelab runs split-horizon DNS with Unbound for resilience testing..."

   ✅ "Years of managing certificate lifecycles taught me automation prevents expiration incidents. My homelab uses cert-manager for Let's Encrypt rotation..."
   ```

**DON'T reveal work infrastructure:**
```markdown
❌ "My agency's network consists of 50 VLANs segmented by classification level..."

❌ "We recently migrated 200 servers from VMware to AWS EC2..."

❌ "Last month, I configured our new Palo Alto firewall with these specific rules..."

❌ "My current employer runs a 3-tier architecture with F5 load balancers and..."
```

### Technical Depth Demonstration Patterns

**Pattern 1: Expertise → Homelab Validation**

Frame professional knowledge as hypothesis, test in homelab:

```markdown
✅ "Professional experience suggested IPsec overhead impacts VoIP quality.
    I validated this in my homelab by running RTP streams through WireGuard (baseline),
    IPsec (26% jitter increase), and OpenVPN (41% jitter increase).
    Measurements confirmed: WireGuard's reduced overhead benefits real-time protocols."
```

**Pattern 2: Years of Experience → Research Citation**

Combine career length with academic backing:

```markdown
✅ "Over 15 years in security engineering, I've observed that most organizations
    patch critical vulnerabilities within 30 days but ignore medium-severity CVEs for months.
    Research from [Cyentia Institute] confirms this: CVSS 9+ patches in 21 days median,
    CVSS 5-7 patches in 120+ days. I tested this hypothesis in my homelab..."
```

**Pattern 3: Past Role → Current Homelab Application**

Explicitly separate past work from current experiments:

```markdown
✅ "Years ago, I worked on systems requiring FIPS 140-2 compliance.
    The configuration complexity was significant - cryptographic module validation,
    approved algorithms, key management requirements.
    I've since replicated FIPS-compliant SSH configurations in my homelab to understand
    the performance impact: 18% throughput reduction compared to ChaCha20-Poly1305."
```

**Pattern 4: Industry Observation → Personal Testing**

Generalize professional observations, attribute testing to homelab:

```markdown
✅ "Industry reports show container escape vulnerabilities increase year-over-year.
    I tested 5 recent CVEs in my homelab: 3 required privileged containers (preventable),
    2 exploited kernel vulnerabilities (requires host patching).
    Lesson: container security is 60% configuration, 40% kernel hardening."
```

### Credibility Markers (NDA-Compliant)

**Safe ways to establish senior-level expertise:**

1. **Certifications and public credentials**
   ```markdown
   ✅ "CISSP and OSCP certifications provided frameworks, but real-world experience showed me..."
   ✅ "Academic research in [field] combined with professional experience suggests..."
   ```

2. **Conference talks and publications** (if public)
   ```markdown
   ✅ "In a previous conference talk on [topic], I discussed..."
   ✅ "Research I published on [platform] explored..."
   ```

3. **Open-source contributions** (public repositories only)
   ```markdown
   ✅ "Contributing to [public project] taught me..."
   ✅ "My open-source work on [GitHub project] demonstrated..."
   ```

4. **Career timeline (vague, no employer names)**
   ```markdown
   ✅ "Over 15+ years spanning network engineering, systems administration, and security roles..."
   ✅ "Throughout my career from junior sysadmin to senior security engineer..."
   ```

5. **Industry observation + homelab validation**
   ```markdown
   ✅ "Professional experience across multiple organizations showed me [pattern]. I validated this in my homelab by..."
   ```

**NEVER use:**
```markdown
❌ Current employer names or agency identifiers
❌ Specific project codenames or system names
❌ Current role responsibilities or team structure
❌ Recent work accomplishments or ongoing initiatives
❌ Clearance level or access details
```

### Cross-Reference: CLAUDE.md Section 4.5.1

This module extends CLAUDE.md Section 4.5.1 (Writing Style) with NDA-safe patterns for demonstrating technical authority. When writing blog posts:

1. **Load this module (nda-compliance.md)** for attribution patterns
2. **Load writing-style.md** for tone and structure
3. **Combine both:** Technical depth (this module) + Polite Linus Torvalds tone (writing-style)

**Example combining both modules:**
```markdown
✅ "Over 15 years in security engineering, I've learned one truth: preventive controls fail.
    Not sometimes - always. The question isn't 'if' but 'when' and 'how badly.'

    I tested this in my homelab by deploying 5 layers of preventive controls
    (network segmentation, AppArmor, SELinux, firewall rules, RBAC).
    Then I ran Metasploit's Eternalblue exploit against a vulnerable Windows VM.

    Result: 4 of 5 controls bypassed in under 10 minutes. Only network segmentation held.

    Lesson: Defense in depth works, but only if each layer actually blocks different attack vectors.
    Most organizations stack controls that fail the same way."
```

**Why this works:**
- **NDA-safe:** Attributes expertise to homelab testing, not current work
- **Technical depth:** Specific tools (Metasploit, Eternalblue), measurable results (4/5 bypassed, <10 min)
- **Senior-level insight:** "Preventive controls fail" - pattern recognition from years of experience
- **Polite Linus tone:** Direct, casual-professional, results-oriented ("Not sometimes - always")

---

## Cross-References
- Related modules:
  - Core modules apply to all content creation
  - `standards/writing-style.md` - Tone and structure (combine with attribution patterns)
  - `workflows/blog-writing.md` - Content creation workflow
- External docs:
  - `docs/ENFORCEMENT.md` - NDA compliance enforcement
  - `CLAUDE.md` Section 4.5.1 - Writing style integration
  - `content-review-instructions.md` - Content review standards

## Examples

### Example 1: Security Vulnerability Discussion (SAFE)

```markdown
✅ "In my homelab, I tested CVE-2024-1234 (CVSS 9.8) using Metasploit.
    Container escaped to host in 3 minutes. Here's how I hardened it..."
```

### Example 2: Security Vulnerability Discussion (UNSAFE)

```markdown
❌ "Last week at work, we discovered a critical RCE in our production environment.
    The vendor hasn't patched it yet, so I can't share details..."
```

### Example 3: Career Experience (SAFE)

```markdown
✅ "Years ago, I worked on systems that required multi-factor authentication.
    The implementation challenges taught me the importance of user experience..."
```

### Example 4: Career Experience (UNSAFE)

```markdown
❌ "My current role involves securing federal systems.
    We use a combination of X, Y, and Z technologies..."
```

## Common Pitfalls

### General NDA Violations
- **Time buffering insufficient** - Use "years ago," never "last month" or "recently"
- **Specific system mentions** - Use generic terms ("federal systems," not agency names)
- **Active vulnerability discussion** - Only discuss CVEs published ≥90 days ago
- **Work story attribution** - Always frame as homelab experiments
- **Family oversharing** - Maintain privacy boundaries

### Senior Engineer Attribution Pitfalls
- **Current role expertise** - Never say "In my current senior engineer role..." (time-buffer to past)
- **Specific employer accomplishments** - Don't reference recent work projects by name
- **Team structure details** - Avoid "my team," "our security program," "we implemented"
- **Missing homelab attribution** - Professional observations MUST be tested/validated in homelab
- **Clearance references** - Never mention clearance level, classification, or access details
- **Recent timeline creep** - "Last year" or "2024" reveals current work (use "years ago")
- **Employer-specific tech stacks** - Don't say "My agency uses X vendor" (say "I've worked with X")
- **Implied current authority** - Avoid "I'm responsible for" (say "I've managed" or "I've worked on")

## Validation

### How to Verify Correct Application

```bash
# 1. Check for work references in blog posts
grep -rE "at work|my employer|current role|we use|my team" src/posts/

# 2. Verify no recent timeline references
grep -rE "last month|recently|this year|current|last quarter" src/posts/

# 3. Check family information accuracy
grep -rE "kids|children|son|daughter" src/posts/ | grep -v "one child\|son"

# 4. Verify homelab attribution for expertise demonstrations
grep -rE "In my (current|senior) (engineer|role)|at \[employer\]" src/posts/

# 5. Check for safe experience framing patterns
grep -rE "years of experience|over .* years|throughout my career" src/posts/

# 6. Verify no employer or agency identifiers
grep -rE "agency|clearance level|classified|employer name" src/posts/
```

### Success Criteria
- [ ] Zero mentions of current work incidents
- [ ] No specific government systems or agencies
- [ ] All security discussions attributed to homelab
- [ ] Family references accurate (one son, age calculated correctly)
- [ ] Privacy boundaries maintained
- [ ] Time buffering applied (2-3 year minimum for work stories)
- [ ] Senior expertise demonstrated via safe patterns (aggregate experience, homelab validation, research citations)
- [ ] No current employer names, project codenames, or clearance details
- [ ] Technical depth attributed to past roles, homelab, or research (not current work)
- [ ] Experience framing uses vague timeframes ("15+ years", "throughout career") not specific dates

## Changelog
- **2025-11-11**: v2.0.0 - Added "Senior Engineer Attribution Patterns" section
  - Experience framing rules (safe/unsafe timeframes)
  - Security engineer attribution patterns (4 demonstration methods)
  - System/network administration context guidelines
  - Technical depth demonstration patterns (4 proven patterns)
  - Credibility markers (5 NDA-compliant methods)
  - Cross-reference with writing-style.md integration
  - Enhanced validation checks and success criteria
  - Senior engineer attribution pitfalls
- **2025-11-01**: v1.0.0 - Initial extraction from CLAUDE.md v3.0.0
