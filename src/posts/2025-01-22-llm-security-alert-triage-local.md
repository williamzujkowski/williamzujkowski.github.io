---
title: "LLM-Powered Security Alert Triage with Local Models"
description: "Automate security alert analysis using local LLMs (Ollama) for privacy-preserving incident response. Reduce alert fatigue with AI-powered triage without cloud dependencies."
author: "William Zujkowski"
date: 2025-11-20
tags: [llm, security, incident-response, automation, ollama, homelab, python, ai]
post_type: tutorial
---

SOC teams field an average of 4,484 alerts a day ([Vectra AI, 2023 State of Threat Detection](https://www.vectra.ai/resources/2023-state-of-threat-detection)) — that's the team total, not per analyst. I automated 78% of triage decisions using local LLMs running on Ollama. No cloud API calls, no data exfiltration. Llama 3.1 (8B parameter model) classifies alert severity, correlates events, and generates incident summaries entirely in my homelab.

Here's how local LLM triage reduces alert fatigue while preserving data privacy.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/alert-triage.png'); width: min(230px, 60%); aspect-ratio: 400/322; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">which alarm actually matters</p>

## The Alert Fatigue Problem

Security tools generate thousands of alerts. Analysts manually triage each one: real threat or false positive? Investigations take 45 minutes average. Vectra puts false positives at 83% of alerts.

**Alert volume breakdown (my homelab, 7 days):**

- **Wazuh SIEM:** 2,847 alerts (brute force, file changes, malware detection)
- **Suricata IDS:** 1,923 alerts (network anomalies, port scans, suspicious traffic)
- **Fail2ban:** 1,156 alerts (SSH attacks, HTTP probes)
- **ClamAV:** 78 alerts (malware signatures)
- **Total:** 6,004 alerts per week = **858 alerts/day**

**Analyst workload:** 6,004 alerts × 3 minutes triage = **300 hours/week** (impossible for a single admin, by a wide margin).

**What I needed:** Automated first-pass triage. LLM reads alert, classifies severity, suggests investigation steps. Humans review only high-priority items.

## Local LLMs: Privacy-Preserving AI

Cloud LLM APIs (OpenAI, Anthropic, Google) send data to third-party servers. Security alerts contain sensitive info: IP addresses, user

names, internal network topology. Local LLM inference keeps all data in homelab.

**Ollama advantages:**

- **Privacy:** All inference runs locally (no cloud API calls)
- **Cost:** Zero per-request fees (vs $0.03-0.15/1K tokens for GPT-4)
- **Speed:** 15-40 tokens/second on consumer GPUs
- **Offline:** Works without internet connectivity
- **Control:** Choose models (Llama 3.1, Mistral, Qwen)

**Ollama architecture:**

<div class="flow" role="group" aria-label="Ollama alert triage architecture">
  <div class="flow-node"><b>Security Alerts</b><i>Wazuh / Suricata JSON</i></div>
  <div class="flow-node"><b>Alert Processor</b><i>Python prompt</i></div>
  <div class="flow-node"><b>Ollama Server</b><i>local LLM; NVIDIA GPU inference, 8GB VRAM</i></div>
  <div class="flow-node"><b>SQLite</b><i>alert DB classification</i></div>
  <div class="flow-parallel" role="group" aria-label="Runs in parallel">
    <div class="flow-node is-bad"><b>Slack Notification</b><i>high priority</i></div>
    <div class="flow-node"><b>Grafana Dashboard</b><i>all alerts</i></div>
  </div>
</div>

**How it works:**

1. **Alert ingestion:** Python script polls Wazuh/Suricata APIs every 60 seconds
2. **Prompt generation:** Convert alert JSON to natural language prompt
3. **LLM inference:** Ollama processes prompt using Llama 3.1 (8B)
4. **Classification:** LLM outputs severity (Critical/High/Medium/Low) + reasoning
5. **Action:** High-severity alerts → Slack notification, all alerts logged to database

**Privacy guarantee:** inference never leaves the homelab. Note the Slack notification path does ship alert descriptions to a third party — swap it for an on-prem notifier if that matters to you. LLM runs on local GPU, no external API calls.

## Implementation: Ollama + Python Automation

I deployed Ollama on dedicated VM with NVIDIA RTX 3060 (12GB VRAM). Python script orchestrates alert processing and LLM inference.

**Ollama installation:**

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Download Llama 3.1 (8B parameter model, 4.7GB)
ollama pull llama3.1:8b

# Verify model loaded
ollama list

# Test inference
ollama run llama3.1:8b "Classify this security alert: SSH login from 192.168.1.100"
```

**Alert triage script:** https://gist.github.com/williamzujkowski/c501bf21bf504d84fa21edb3688da814

**Key components:**

**1. Alert retrieval (Wazuh API):**

```python
import requests

def get_recent_alerts(hours=1):
    """Fetch alerts from Wazuh API."""
    url = "https://wazuh-manager:55000/security/alerts"
    headers = {"Authorization": "Bearer <token>"}
    params = {
        "limit": 100,
        "time_range": f"{hours}h",
        "sort": "-timestamp"
    }

    response = requests.get(url, headers=headers, params=params, verify=True)
    return response.json()["data"]["alerts"]
```

**2. Prompt engineering for security context:**

```python
def create_triage_prompt(alert):
    """Generate LLM prompt from alert JSON."""
    prompt = f"""You are a security analyst triaging alerts. Classify this alert:

**Alert Details:**
- Rule: {alert['rule']['description']}
- Level: {alert['rule']['level']}
- Source IP: {alert.get('data', {}).get('srcip', 'N/A')}
- Timestamp: {alert['timestamp']}
- Full message: {alert.get('full_log', '')}

**Your task:**
1. Classify severity: Critical, High, Medium, or Low
2. Explain reasoning (2-3 sentences)
3. Suggest next investigation step

**Format response as JSON:**
{% raw %}{{
  "severity": "High",
  "reasoning": "SSH brute force from external IP with 50 failed attempts",
  "next_step": "Block source IP, review SSH logs for successful logins"
}}{% endraw %}
"""
    return prompt
```

**3. LLM inference via Ollama API:**

```python
import ollama

def classify_alert(prompt):
    """Send prompt to local Ollama LLM."""
    response = ollama.chat(
        model='llama3.1:8b',
        messages=[{
            'role': 'user',
            'content': prompt
        }],
        options={
            'temperature': 0.1,  # Low temperature for consistent classification
            'top_p': 0.9
        }
    )

    return response['message']['content']
```

**4. Automated action based on classification:**

```python
def process_alert(alert):
    """Triage alert using LLM, take action based on severity."""
    # Generate prompt
    prompt = create_triage_prompt(alert)

    # Get LLM classification
    classification = classify_alert(prompt)
    result = json.loads(classification)

    # Log to database
    log_alert(alert, result)

    # High-severity alerts trigger notifications
    if result['severity'] in ['Critical', 'High']:
        send_slack_notification(
            title=f"{result['severity']}: {alert['rule']['description']}",
            message=result['reasoning'],
            action=result['next_step']
        )

    return result
```

**Complete automation script:** https://gist.github.com/williamzujkowski/c501bf21bf504d84fa21edb3688da814

## Triage Results: 78% Automation Rate

I ran the LLM triage system for 30 days on my homelab alerts. It classified 91.1% of sampled alerts correctly, and 22% still needed a human look.

**Classification accuracy (1,500 alerts sampled):**

| Alert Type | Total | LLM Correct | Accuracy |
|------------|-------|-------------|----------|
| SSH brute force | 450 | 442 | 98.2% |
| Port scan | 380 | 365 | 96.1% |
| Malware detection | 92 | 88 | 95.7% |
| File integrity change | 234 | 198 | 84.6% |
| Network anomaly | 188 | 132 | 70.2% |
| Web attack (SQL injection) | 156 | 142 | 91.0% |
| **Overall** | **1,500** | **1,367** | **91.1%** |

**Why network anomalies had lower accuracy:** Legitimate traffic patterns (VPN reconnects, DNS queries) flagged as anomalies. LLM lacks context on expected behavior. Improved with retrieval context (see RAG, below).

**False positives/negatives:**

- **False positives:** 8.9% (133 alerts) - LLM marked low-severity events as high (e.g., routine software updates flagged as malware)
- **False negatives:** 0.7% (11 alerts) - LLM missed critical alerts (privilege escalation buried in verbose logs)

**Time savings:** 1,367 alerts triaged automatically × 3 min/alert = **68.4 hours saved/month**. Manual review required for 22% (297 alerts) = **14.9 hours/month**. Net reduction: **78% time savings**.

## Advanced: RAG for Alert Context

Large Language Models benefit from context. Retrieval-Augmented Generation (RAG) provides LLM with historical alert data and threat intelligence.

**RAG architecture:**

<div class="flow" role="group" aria-label="RAG alert context pipeline">
  <div class="flow-node">New Alert</div>
  <div class="flow-node"><b>Vector DB</b><i>Chroma query; 30 days historical alert embeddings</i></div>
  <div class="flow-node"><b>Context Builder</b><i>similar alerts + MISP / OTX IOCs</i></div>
  <div class="flow-node"><b>Ollama LLM</b><i>enriched prompt</i></div>
  <div class="flow-node"><b>Triage Decision</b><i>classification</i></div>
</div>

**How RAG improves triage:**

1. **Alert arrives:** "SSH login from 203.0.113.5"
2. **Vector search:** Find similar historical alerts (same source IP, similar timestamp pattern)
3. **Context retrieval:** Previous alerts show 203.0.113.5 = VPN endpoint (false positive likely)
4. **Enriched prompt:** Include context in LLM prompt: "Previous 10 logins from this IP were legitimate VPN connections"
5. **Better classification:** LLM correctly classifies as Low severity (routine VPN login)

**Implementation using ChromaDB:**

```python
import chromadb
from chromadb.utils import embedding_functions

# Initialize vector database
client = chromadb.Client()
collection = client.create_collection(
    name="alert_history",
    embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction()
)

# Add historical alerts to vector DB
for alert in historical_alerts:
    collection.add(
        documents=[alert['full_log']],
        metadatas=[{'severity': alert['severity'], 'src_ip': alert['src_ip']}],
        ids=[alert['id']]
    )

# Retrieve similar alerts for new alert
def get_similar_alerts(new_alert, limit=5):
    """Find historically similar alerts using vector similarity."""
    results = collection.query(
        query_texts=[new_alert['full_log']],
        n_results=limit
    )
    return results['documents'][0]

# Enrich prompt with context
def create_rag_prompt(alert):
    """Generate prompt with RAG context."""
    similar = get_similar_alerts(alert)
    context = "\n".join([f"- {s}" for s in similar])

    prompt = f"""Classify this alert. Consider similar historical alerts:

**Current Alert:**
{alert['full_log']}

**Similar Historical Alerts:**
{context}

**Classification:** ...
"""
    return prompt
```

**RAG impact:** Accuracy on network anomaly alerts improved from 70.2% to 94.8% — that category was the weakest before retrieval, which is why it moved most.

**RAG implementation:** https://gist.github.com/williamzujkowski/81c7b4914517758e7a7fdc0c61aeb699

## Performance: LLM Inference Speed

Local LLM inference speed depends on hardware. I tested Llama 3.1 (8B) on different configurations.

**Hardware benchmarks:**

| Hardware | Tokens/Second | Alert Triage Time | Cost |
|----------|---------------|-------------------|------|
| NVIDIA RTX 4090 (24GB) | 85 tokens/sec | 0.8 seconds | $1,600 |
| NVIDIA RTX 3060 (12GB) | 38 tokens/sec | 1.9 seconds | $300 |
| CPU only (16-core Xeon) | 4 tokens/sec | 18 seconds | $0 (existing) |
| M1 Mac (8GB unified) | 22 tokens/sec | 3.2 seconds | $1,000 |

**My setup:** RTX 3060 (12GB VRAM) handles 38 tokens/second. Average triage prompt = 250 tokens input + 100 tokens output = 350 tokens total. Processing time: 350 / 38 = **9.2 seconds per alert**.

**Throughput:** 858 alerts/day ÷ 86,400 seconds/day = 0.01 alerts/second. LLM can handle 0.11 alerts/second (38 tokens/sec ÷ 350 tokens). **Headroom: 11x current load.**

**Optimization:** Batch processing 10 alerts concurrently reduces per-alert overhead to 1.9 seconds (5x speedup).

## Research: AI-Augmented SOC

Academic research validates LLM effectiveness for security operations. Several 2025 surveys discuss production viability.

**Key findings:**

1. **Survey on LLM SOC Applications** (arXiv:2509.10858, September 2025)
   - LLMs show strong potential in log summarization, alert triage, threat intelligence, incident response
   - Notes LLM potential for faster alert triage, without reporting a specific time-reduction figure
   - Challenges: prompt injection, excessive agency, hallucination risks

2. **Autonomous Incident Response** (arXiv:2508.10677, August 2025)
   - RAG-based framework using CTI (Cyber Threat Intelligence) integration
   - Automated IR playbook generation from threat intel databases
   - Evaluated with LLM-as-judge metrics; mentions Azure only in passing, with no reported production accuracy figure

3. **Lightweight LLMs for IR** (2025 research)
   - Smaller fine-tuned models + RAG achieve **22% faster recovery** than frontier models
   - Reduced ineffective actions through decision-theoretic planning
   - Lower hallucination rates with retrieval-augmented approaches

**My implementation aligns with research:** Local LLM + RAG + decision thresholds for automated triage. I have no published automation-rate benchmark to compare this against; the surveys I found report no specific figure.

**Citations:**

- [Large Language Models for Security Operations Centers](https://arxiv.org/abs/2509.10858) - arXiv:2509.10858, comprehensive SOC automation survey
- [Advancing Autonomous Incident Response](https://arxiv.org/html/2508.10677v1) - arXiv:2508.10677, RAG-based IR automation

## Limitations and Trade-Offs

**Challenge 1: Model hallucination**

- **Problem:** LLMs occasionally invent facts (claims IP is known attacker when it's not)
- **Impact:** 8.9% false positive rate from hallucinated threat intel
- **Mitigation:** Confidence scores, human review for Critical/High severity, RAG grounding

**Challenge 2: Context window limits**

- **Problem:** Ollama's default `num_ctx` is 2048 tokens regardless of what the model supports
- **Impact:** long log files are silently truncated unless you raise it — Llama 3.1 8B itself handles 128K
- **Mitigation:** Summarize logs before LLM processing, use sliding window for large files

**Challenge 3: Domain-specific knowledge**

- **Problem:** General-purpose LLMs lack security expertise (miss advanced persistent threat patterns)
- **Impact:** Lower accuracy on complex attacks (APT, zero-days)
- **Mitigation:** Fine-tune on security-specific dataset (MISP, AlienVault OTX)

**Challenge 4: GPU requirements**

- **Problem:** 8B model needs roughly 6GB of VRAM at 4-bit
- **Impact:** Not feasible on low-end hardware (CPU-only inference roughly 9.5x slower)
- **Mitigation:** Use smaller models (Llama 3.2 1B or 3B), quantization (4-bit reduces VRAM 75%)

**What I learned:** Start with small model (1B-3B parameters), validate on historical alerts, scale up if accuracy insufficient. Don't over-engineer: 91% accuracy good enough for first-pass triage.

## Further Reading

**Research papers:**

- [Large Language Models for Security Operations Centers: A Comprehensive Survey](https://arxiv.org/abs/2509.10858) - arXiv:2509.10858, SOC automation with LLMs
- [Advancing Autonomous Incident Response: Leveraging LLMs and CTI](https://arxiv.org/html/2508.10677v1) - arXiv:2508.10677, RAG-based incident response
- [AI-Augmented SOC: A Survey of LLMs and Agents](https://www.mdpi.com/2624-800X/5/4/95) - MDPI 2024, comprehensive LLM SOC survey

**LLM deployment:**

- [Ollama](https://ollama.com/) - Local LLM deployment platform
- [Llama 3.1 Model Card](https://github.com/meta-llama/llama-models) - Meta's open-source LLM
- [ChromaDB](https://www.trychroma.com/) - Vector database for RAG

**Security automation:**

- [Wazuh API Documentation](https://documentation.wazuh.com/current/user-manual/api/reference.html) - SIEM API integration
- [Suricata JSON Output](https://docs.suricata.io/en/latest/output/eve/index.html) - IDS alert format
- [MISP Threat Intel Platform](https://www.misp-project.org/) - Open-source threat intelligence

**Prompt engineering:**

- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering) - Best practices (applies to Llama too)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction) - LLM orchestration framework

**Implementation examples:**

- **Alert triage script:** https://gist.github.com/williamzujkowski/c501bf21bf504d84fa21edb3688da814
- **RAG implementation:** https://gist.github.com/williamzujkowski/81c7b4914517758e7a7fdc0c61aeb699
- **Complete automation:** https://gist.github.com/williamzujkowski/c501bf21bf504d84fa21edb3688da814

---

**Deploy local LLM triage for your alerts.** Install Ollama, download Llama 3.1, point it at your SIEM. Start with read-only mode (classify but don't act), validate accuracy, then enable automated actions.

Most alert fatigue comes from manual triage of obvious false positives. LLMs excel at pattern recognition: "SSH login from office IP during business hours = probably legitimate." In my homelab, 78% of alerts now self-triage. I investigate the interesting 22%.
