---

author: William Zujkowski
date: 2025-04-10
description: "Secure personal AI experiments with model isolation and network segmentation—protect LLM deployments using privacy controls and threat modeling."
title: 'Securing Your Personal AI/ML Experiments: A Practical Guide'
tags:
  - ai
  - homelab
  - llm
  - machine-learning
  - privacy
  - security
---
## The AI Revolution Hits Home

I run local models in my [homelab](/posts/2025-04-24-building-secure-homelab-adventure) on an RTX 3090. Twenty-four gigabytes sets a real ceiling: a 4-bit 32B model fits with room for context, and a 70B does not — 70 billion parameters at half a byte each is 35 GB of weights before you have loaded a single token of KV cache. It took me embarrassingly long to stop treating it like a chatbot and start treating it like what it actually is: a process with network access, disk access, and occasionally opinions about running arbitrary code. Running [AI experiments](/posts/2025-06-25-local-llm-deployment-privacy-first) at home created unique security and privacy challenges I didn't anticipate. This post shares practical approaches to securing personal AI/ML deployments, learned through successes and carefully contained failures.

**Key takeaway:** Model isolation, [network segmentation](/posts/2025-09-08-zero-trust-vlan-segmentation-homelab), and privacy controls turn experimental AI systems into production-safe infrastructure.


## Requirements

To run the code examples in this post, you'll need to install the following packages:

```bash
pip install cryptography keyring psutil torch nvidia-ml-py
```

Or create a `requirements.txt` file:

```text
cryptography
keyring
psutil
torch
nvidia-ml-py
```

## Why Security Matters for Personal AI Projects

Five critical risks demand attention:

- **Data Privacy**: AI models memorize training data, including personal information
- **Resource Hijacking**: ML workloads attract cryptominers (GPU-intensive = high-value targets)
- **Model Poisoning**: Compromised models generate harmful content
- **Network Security**: AI experiments require internet connectivity, expanding attack surface
- **Family Safety**: Kids using AI tools need additional safeguards

## Setting Up a Secure AI Sandbox

### Isolated Environment is Key

My first rule: AI experiments run in isolation.

This approach adds operational complexity, trading convenience for security. But isolation prevents one compromised experiment from cascading across your network — and a compromised experiment with 24GB of VRAM and no rate limit is not something you want loose.

🔖 [Secure AI sandbox isolation setup ↗](https://gist.github.com/williamzujkowski/d8ad8f2e7cb5431e0def2c94283d4ce5)

### Network Segmentation for AI Workloads

AI experiments get their own VLAN with strict firewall rules:

🔖 [AI workload VLAN segmentation rules ↗](https://gist.github.com/williamzujkowski/6eaf1ebe4f96aad330fc23fc5b57c671)

## Securing Local LLM Deployments

Running LLMs locally (like LLaMA or Mistral) requires special consideration:

### Model loading is the dangerous part

The thing to understand before writing any of this: **`torch.load` unpickles, and
unpickling is arbitrary code execution.** PyTorch flipped the default to
`weights_only=True` in 2.6 precisely because the unconstrained unpickler can call
arbitrary functions. A downloaded checkpoint from a stranger is a program, not
data.

Two rules follow.

**Prefer safetensors.** The format exists specifically because this problem
exists. If a torch checkpoint is unavoidable, pass `weights_only=True` explicitly
rather than relying on your installed version's default.

**Make hash verification fail closed.** This is the trap worth flagging loudly,
because it is easy to write and looks correct:

```python
expected = trusted_hashes.get(model_path.name)
if expected and computed != expected:      # wrong
    raise ValueError("checksum mismatch")
return True
```

An unknown model has no entry, so `expected` is `None`, the comparison is
skipped, and the function returns success. If the hash file does not exist at
all, *every* model verifies. A checker that passes everything it does not
recognise is worse than no checker, because you stop looking at that step. The
correct shape:

```python
expected = trusted_hashes.get(model_path.name)
if expected is None:
    raise ValueError(f"No trusted hash on record for {model_path.name}")
if computed != expected:
    raise ValueError(f"Checksum mismatch for {model_path.name}")
```

The same applies to path handling: resolve against a base directory and check
containment (`Path(base).resolve()`, then `is_relative_to`). String-replacing
`../` does not work, because `....//` collapses back to `../` after one pass.

### Prompt injection: what you can and cannot do about it

There is no reliable filter-based defence against prompt injection. A blocklist
of phrases like "ignore previous instructions" is defeated by paraphrase,
translation, base64, or simply not using those words — and it produces immediate
false positives, since a blocklist containing "system prompt" refuses anyone who
asks what a system prompt is.

An input filter also only ever sees the user's prompt. The variety that actually
threatens a homelab RAG setup is **indirect** injection, arriving in a retrieved
document, a fetched web page, or a tool's output. Nothing inspecting the user's
typing sees it at all.

So treat this as an architecture problem rather than a filtering one, which is
also [OWASP's position](https://owasp.org/www-project-top-10-for-large-language-model-applications/):

- The model gets no credentials worth stealing.
- The model's network egress is restricted, so an injected instruction has
  nowhere to send anything.
- Any tool with a consequential side effect requires human confirmation.
- All model output is treated as untrusted input to whatever consumes it.

A phrase blocklist is still worth having as a crude tripwire that tells you
someone is probing. Do not mistake it for a control.

## Monitoring AI Resource Usage

AI workloads can consume significant resources. Here's how I monitor them:

🔖 [AI resource usage monitoring scripts ↗](https://gist.github.com/williamzujkowski/328c43577820c92437ed40c58e276ae8)

## Data Privacy in AI Experiments

### Preventing Data Leakage

When experimenting with AI, especially when using family photos or documents:

🔖 [AI experiment data leakage prevention workflow ↗](https://gist.github.com/williamzujkowski/271230bd22778b63d2645fb63570b3bf)

### Secure API Key Management

For cloud AI services, proper API key management is essential:

🔖 [Secure AI API key management examples ↗](https://gist.github.com/williamzujkowski/9321cf345abbe8ae554d4d106645a0db)

## Family-Safe AI Guidelines

When kids want to experiment with AI, additional safeguards are needed:

### Content Filtering for AI Outputs

🔖 [Family-safe AI output filtering examples ↗](https://gist.github.com/williamzujkowski/cda8c25a0a3b3596aa38207ad76769a8)

## Lessons Learned

### 1. Start Small and Isolated

Begin with small experiments in completely isolated environments.
Scale up only after understanding security implications.

Perfect isolation isn't always practical — a model that can't download itself or call out for updates is a decorative object, not a deployment. I've made compromises when connectivity was needed for model downloads or API calls.

### 2. Monitor Everything

AI workloads behave unexpectedly.
Thorough monitoring catches issues early.

Distinguishing between legitimate spikes and actual problems is more art than science.

### 3. Version Control for Models

Track model versions and their sources.
Know exactly what you're running.

### 4. Regular Security Audits

AI tools evolve rapidly.
Regular security reviews are essential.

I'm still figuring out the right cadence for these audits.

### 5. Educate Family Members

Help family understand AI privacy implications.
My family now asks before sharing personal info with any AI tool.

## Tools and Resources

Essential tools for secure AI experimentation:

- **Docker/Podman**: Container isolation
- **[LocalAI](/posts/2025-10-29-privacy-first-ai-lab-local-llms)**: Run LLMs locally
- **Ollama**: easy local model management — but it binds with **no authentication** by default, so keep it on localhost or behind something that authenticates. [CVE-2024-37032](https://nvd.nist.gov/vuln/detail/CVE-2024-37032) (path traversal to RCE, CVSS 8.8) was fixed in 0.1.34; do not run older than that
- **Netdata**: Real-time performance monitoring

## Future Plans

My upcoming AI security projects:

- Federated learning setup for family devices
- Homomorphic encryption for sensitive data processing
- Local voice assistant with privacy guarantees
- AI-powered security monitoring for the homelab itself

## Conclusion

Running AI experiments at home requires the right safeguards.
Proper isolation, monitoring, and privacy controls let you explore AI frontiers while keeping family data safe.

In the AI age, we're securing thoughts, conversations, and creative outputs—not just networks and devices.

But AI promises aren't always delivered.
Model accuracy degrades with subtle input changes.
Privacy controls add overhead that slows inference.
Perfect isolation conflicts with practical usability.

When properly secured, AI becomes a powerful tool for learning and creativity rather than a privacy risk. The trade-offs are worth it.



## Further Reading

For more in-depth information on the topics covered in this post:

- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [arXiv AI Research](https://arxiv.org/list/cs.AI/recent)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)


---

*Building your own secure AI lab? Hit me up – I love exchanging ideas about making AI both powerful and privacy-preserving!*
