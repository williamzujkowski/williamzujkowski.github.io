# Instructions for Creating GitHub Gists

These gists need to be created manually at https://gist.github.com/

For each file below, create a gist with the specified filename and description.

## Gist 1: Docker Compose Configuration
- **Filename**: `ai-docker-compose.yml`
- **Description**: Docker Compose configuration for isolated AI experiment environment with network isolation and resource limits
- **Tags**: docker, ai, security, homelab
- **Content**: `/home/william/git/williamzujkowski.github.io/tmp/gists/ai-docker-compose.yml`

## Gist 2: Firewall Rules
- **Filename**: `ai-firewall-rules.sh`
- **Description**: Network segmentation firewall rules for AI VLAN using iptables
- **Tags**: security, networking, ai, firewall
- **Content**: `/home/william/git/williamzujkowski.github.io/tmp/gists/ai-firewall-rules.sh`

## Gist 3: Secure Model Loader
- **Filename**: `secure-model-loader.py`
- **Description**: Verify ML model integrity with checksums before loading to prevent tampering
- **Tags**: python, security, ai, machine-learning
- **Content**: `/home/william/git/williamzujkowski.github.io/tmp/gists/secure-model-loader.py`

## Gist 4: Prompt Security Filter
- **Filename**: `prompt-security-filter.py`
- **Description**: Detect and block prompt injection attempts in LLM applications
- **Tags**: python, security, ai, llm, prompt-injection
- **Content**: `/home/william/git/williamzujkowski.github.io/tmp/gists/prompt-security-filter.py`

## Gist 5: AI Resource Monitor
- **Filename**: `ai-resource-monitor.py`
- **Description**: Monitor GPU and CPU usage for AI workloads to detect anomalous behavior
- **Tags**: python, monitoring, ai, security
- **Content**: `/home/william/git/williamzujkowski.github.io/tmp/gists/ai-resource-monitor.py`

## Gist 6: Privacy Preserving AI
- **Filename**: `privacy-preserving-ai.py`
- **Description**: Detect and redact PII (email, phone, SSN, credit card) before AI processing
- **Tags**: python, privacy, ai, pii, security
- **Content**: `/home/william/git/williamzujkowski.github.io/tmp/gists/privacy-preserving-ai.py`

## Gist 7: Secure API Manager
- **Filename**: `secure-api-manager.py`
- **Description**: Securely store and retrieve API keys using encryption and system keyring
- **Tags**: python, security, api, encryption
- **Content**: `/home/william/git/williamzujkowski.github.io/tmp/gists/secure-api-manager.py`

## Gist 8: Family Safe AI
- **Filename**: `family-safe-ai.py`
- **Description**: Content filtering wrapper for AI models to ensure kid-safe outputs
- **Tags**: python, ai, content-moderation, family-safety
- **Content**: `/home/william/git/williamzujkowski.github.io/tmp/gists/family-safe-ai.py`

---

## After Creating Gists

Once you create each gist, you'll get a URL like:
`https://gist.github.com/williamzujkowski/[hash]`

Save these URLs - you'll need them to update the blog post with gist embeds.

The embed format is:
```html
<script src="https://gist.github.com/williamzujkowski/[hash].js"></script>
```

**Example placeholders for blog post update:**
```
GIST_1_HASH = [hash from Docker Compose gist]
GIST_2_HASH = [hash from firewall rules gist]
GIST_3_HASH = [hash from secure model loader gist]
GIST_4_HASH = [hash from prompt security filter gist]
GIST_5_HASH = [hash from AI resource monitor gist]
GIST_6_HASH = [hash from privacy preserving AI gist]
GIST_7_HASH = [hash from secure API manager gist]
GIST_8_HASH = [hash from family safe AI gist]
```
