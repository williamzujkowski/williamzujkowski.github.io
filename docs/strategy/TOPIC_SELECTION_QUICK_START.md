# Blog Topic Selection - Quick Start Guide

**For:** William's Security/Homelab Blog
**Last Updated:** 2025-11-13
**See Full Strategy:** `blog-topic-strategy-2025.md`

---

## TL;DR: What You Need to Know

**Current State:**
- 62 posts published (strong foundation ✅)
- Top topics: security (32), ai (23), homelab (21)
- **GAPS:** cloud (2), containers (3), monitoring (3), tool reviews (minimal)

**Target State (12 months):**
- 110 total posts (48 new in 2026)
- 75/25 evergreen-trending ratio
- 4 posts/month consistent cadence
- Fill all critical gaps

---

## Quick Decision Framework

### Can I Write This Post?

```
1. ✅ Personal homelab experience? (not work)
2. ✅ Can test/demo in my environment?
3. ✅ Unique angle or deeper than existing content?
4. ✅ Readers can reproduce?
5. ✅ Passes NDA compliance?
```

**If all YES → Write it!**

---

## Critical Gaps to Fill (Priority 1)

### 🔴 Cloud Security (2 posts → target 8-10)
- AWS IAM deep dives
- Azure/GCP security
- Multi-cloud management
- Cost optimization through security

### 🔴 Container Security (3 posts → target 10-12)
- Docker hardening
- K8s RBAC & network policies
- Service mesh security
- Image scanning comparisons

### 🔴 Monitoring & Observability (3 posts → target 8-10)
- Prometheus setup & tuning
- Grafana dashboard guides
- Loki log aggregation
- Distributed tracing

### 🔴 Python Security Automation (3 posts → target 8-10)
- Script library walkthroughs
- Testing with pytest
- API integrations
- Performance optimization

---

## New Content Formats to Try

### 1. Multi-Part Series
- "Building a SOC Lab" (6 parts)
- "Zero to Hero: Kubernetes" (4 weeks)
- "Securing Your Homelab" (10 parts)

### 2. Tool Comparisons
- SIEM: Wazuh vs Splunk vs ELK
- IDS/IPS: Suricata vs Snort vs Zeek
- Password Managers: Bitwarden vs 1Password vs KeePass

### 3. Failure Stories
- "How I DDoS'd My Homelab"
- "5 Costly Security Misconfigurations"
- "When Automation Goes Wrong"

### 4. Beginner Guides
- "Your First Security Lab: $200 Budget"
- "Networking Basics for Homelab"
- "Understanding Logs"

---

## Monthly Publishing Schedule

**Target: 4 posts/month (1 per week)**

- **Week 1:** Deep technical guide (evergreen)
- **Week 2:** Practical implementation (evergreen)
- **Week 3:** Tool review/comparison (evergreen)
- **Week 4:** Trending topic OR failure story (mixed)

---

## Topic Scoring System

**Score each idea 0-5 on:**
1. Personal Experience (must be 4+)
2. Audience Value (must be 3+)
3. Search Potential (nice to have 3+)
4. Evergreen Longevity (prefer 4+)
5. Unique Angle (must be 3+)

**Minimum: 15/25 to proceed**

---

## Next 30 Days Action Plan

### Week 1: Planning
- [ ] Review full strategy doc (`blog-topic-strategy-2025.md`)
- [ ] Create content calendar for Q1 2026
- [ ] Choose 4 topics from critical gaps

### Week 2: Research
- [ ] Outline first cloud security post
- [ ] Test setup in homelab
- [ ] Gather citations/sources

### Week 3: Writing
- [ ] Draft first post (2,500+ words)
- [ ] Include 10+ citations
- [ ] Test all commands/code

### Week 4: Publishing
- [ ] Publish first gap-filling post
- [ ] Promote on social media
- [ ] Plan next 3 posts

---

## Quick Topic Ideas (Start Here)

### Cloud Security
1. AWS IAM Deep Dive: Beyond Basic Roles
2. S3 Security: Lessons from Public Bucket Failures
3. Multi-Cloud Security: Managing AWS + Azure

### Container Security
1. Docker Security Hardening: 20 Best Practices
2. Kubernetes RBAC: Practical Implementation
3. Container Escape Scenarios: Testing in Homelab

### Monitoring
1. Prometheus Architecture: Homelab Setup
2. Grafana Dashboards: From Zero to Hero
3. Alert Fatigue: Lessons from Over-Monitoring

### Python Automation
1. Python Script Library Tour: 37 Utilities Explained
2. Building a Vulnerability Scanner in Python
3. Pytest for Security Scripts: TDD Approach

### Tool Comparisons
1. SIEM Solutions: Wazuh vs Splunk vs ELK
2. Backup Solutions: restic vs Borg vs Kopia
3. VPN Technologies: WireGuard vs OpenVPN vs Tailscale

---

## Content Quality Checklist

Before publishing, verify:

- [ ] **NDA Safe:** 100% homelab or public knowledge
- [ ] **Tested:** All commands/code work in my environment
- [ ] **Accurate:** Hardware specs match uses.md
- [ ] **Cited:** 10+ credible sources with links
- [ ] **Readable:** "Polite Linus Torvalds" style
- [ ] **Reproducible:** Readers can follow along
- [ ] **Length:** 2,500+ words for technical content
- [ ] **Tags:** 3-5 relevant tags
- [ ] **Images:** Hero image + screenshots

---

## Quarterly Themes

**Q1:** Foundations & Fundamentals (fill gaps)
**Q2:** Advanced Implementations (multi-part series)
**Q3:** Tool Evaluations & Comparisons (reviews)
**Q4:** Year in Review & Future Trends (retrospectives)

---

## Resources

- **Full Strategy:** `docs/strategy/blog-topic-strategy-2025.md`
- **Topic Analyzer:** `scripts/analysis/topic-distribution-analyzer.py`
- **Content Guide:** `docs/guides/content-review-instructions.md`
- **Writing Style:** `docs/context/standards/writing-style.md`
- **NDA Compliance:** `docs/context/core/nda-compliance.md`

---

## Key Metrics to Track

**Monthly:**
- Posts published (target: 4)
- Organic traffic growth
- Average engagement time
- Newsletter signups

**Quarterly:**
- Gap closure progress
- Search rankings
- Backlinks generated
- Audience feedback

---

## Common Pitfalls to Avoid

❌ **Don't:**
- Write about work incidents (NDA!)
- Copy commands without testing
- Exaggerate hardware capabilities (learned this!)
- Chase every trending topic
- Publish without citations

✅ **Do:**
- Focus on homelab experiments
- Test everything before publishing
- Be honest about limitations/failures
- Balance evergreen and trending (75/25)
- Cite academic sources

---

**Remember:** Quality > Quantity. One excellent post per week beats four mediocre ones.

**Start small:** Pick ONE topic from critical gaps. Research, test, write, publish. Repeat.
