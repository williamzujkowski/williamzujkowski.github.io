# LLM VRAM Claims Audit - 2025-11-13

## Critical Issue Summary

**Hardware Reality:** RTX 3090 has 24GB VRAM (not 80GB)

**Problem:** Multiple claims about running 70B models that require 40GB+ VRAM on 24GB hardware

## Technical Inaccuracies Found

### 1. uses.md (CRITICAL)

**Line 25:**
```
"11GB VRAM on my old 2080 Ti wasn't enough for the 70B parameter models I wanted to run"
```
- Implies 3090's 24GB is enough for 70B models
- **FALSE**: 70B Q4_K_M needs ~40GB VRAM

**Line 239:**
```
"Models I actually run: Llama 3.1 70B (quantized to Q4_K_M, ~40GB)"
```
- Claims to run 40GB model on 24GB GPU
- **IMPOSSIBLE** without offloading

**Line 245:**
```
"Q4 quantization reduces quality slightly but fits in VRAM"
```
- Implies 70B Q4 fits in 24GB VRAM
- **FALSE**: 40GB ≠ 24GB

### 2. 2025-10-29-privacy-first-ai-lab-local-llms.md (CRITICAL)

**Line 5 (frontmatter):**
```
"run Llama 3.1 70B on RTX 3090"
```

**Line 34:**
```
"Here's what running a 70B parameter model on my RTX 3090 actually involves: 80GB of VRAM maxed out"
```
- Claims RTX 3090 has 80GB VRAM
- **IMPOSSIBLE**: RTX 3090 has 24GB VRAM

**Line 279:**
```
"Running everything locally means I'm limited to models that fit in 80GB VRAM"
```
- Again claims 80GB VRAM
- **FALSE**: Should be 24GB

**Line 143:**
```
"My RTX 3090 runs 70B models with tool use"
```
- Implies 70B fits in 24GB
- **Requires offloading** not mentioned

### 3. 2025-06-25-local-llm-deployment-privacy-first.md

**Line 26:**
```
"I run Llama 2 70B on my RTX 4090"
```
- RTX 4090 also has 24GB VRAM

**Line 108 (table):**
```
| 70B params | 40-80 GB | 128 GB | 150 GB | Llama 2 70B |
```
- Correctly states 70B needs 40-80GB VRAM
- **Contradicts** claims of running on 24GB GPU

**Line 115:**
```
"NVIDIA RTX 4090 (24GB VRAM)"
```
- Correctly lists VRAM
- **Contradicts** running 70B claim above

### 4. 2024-11-15-gpu-power-monitoring-homelab-ml.md

**Line 40:**
```
"GPU: NVIDIA RTX 3090 (24GB VRAM)"
```
- Correctly lists VRAM

**Line 86:**
```
"Llama 3.1 70B (Q4 quantized): 347W average"
```
- Mentions running 70B quantized

**Line 90:**
```
"The quantized 70B model I ran (Q4_K_M quantization) fit entirely in VRAM"
```
- Claims 70B Q4 fits in 24GB
- **FALSE**: Q4_K_M 70B needs ~40GB

## Actual Model Sizes for 24GB VRAM

### Models That Actually Fit:

| Model Size | Q8 Quantization | Q4 Quantization | Fits 24GB? |
|-----------|----------------|----------------|------------|
| 7B | ~7GB | ~4GB | ✅ Easily |
| 13B | ~13GB | ~7GB | ✅ Comfortably |
| 33B-34B | ~33GB | ~18-20GB | ✅ With Q4 |
| 70B | ~70GB | ~38-42GB | ❌ Requires offloading |

### Reality for 70B Models on 24GB VRAM:

**Options:**
1. **Offloading to System RAM:** Load part of model in VRAM, rest in RAM (slow, but works)
2. **More aggressive quantization:** Q3 or Q2 (significant quality loss, still marginal fit)
3. **Smaller models:** Use 33B-34B instead (realistic for 24GB)

**Performance Reality:**
- 70B with offloading: ~2-10 tokens/second (vs 20-40 without offloading)
- Requires 64GB+ system RAM for offloading buffer
- Memory bandwidth becomes severe bottleneck

## Recommendations

### Immediate Fixes Needed:

1. **uses.md:** Correct to realistic model sizes (7B, 13B, 33B) or explain offloading
2. **privacy-first-ai-lab-local-llms.md:** Fix 80GB VRAM claim (should be 24GB), explain offloading
3. **local-llm-deployment-privacy-first.md:** Remove RTX 4090 70B claim or add offloading context
4. **gpu-power-monitoring-homelab-ml.md:** Add footnote about offloading for 70B

### Honest Framing Options:

**Option A - Be Honest About Offloading:**
```markdown
"With 24GB VRAM, I can run 7B-34B models fully in GPU memory. For 70B models,
I use CPU offloading (loads part of model in system RAM), which works but runs
2-5x slower (~4-8 tokens/second vs 20+ for GPU-only inference). Realistic for
experimentation, not for production use."
```

**Option B - Focus on What Actually Fits:**
```markdown
"RTX 3090's 24GB VRAM handles 7B-34B models comfortably. I primarily use:
- Llama 3.1 8B: Fast, efficient, good for most tasks
- Mistral 7B: Excellent quality-to-size ratio
- CodeLlama 34B: Best coding model that fits fully in VRAM (Q4 quantization)
- Qwen 2.5 Coder 32B: Strong alternative to CodeLlama

For tasks requiring 70B models, I use API access or accept slower CPU-offloaded inference."
```

**Option C - Hardware Upgrade Path (if true):**
```markdown
"Planning upgrade to dual RTX 4090s (48GB combined) or H100 (80GB) for native 70B inference.
Current RTX 3090 (24GB) handles 7B-34B models well but requires offloading for 70B."
```

## Technical Accuracy Standards

All LLM claims must:
1. ✅ Match actual hardware specs (RTX 3090 = 24GB VRAM, not 80GB)
2. ✅ Distinguish between full VRAM fit vs offloading
3. ✅ Provide realistic performance metrics for actual configuration
4. ✅ Explain trade-offs honestly (speed, quality, memory usage)
5. ✅ Avoid exaggerating capabilities beyond hardware limits

## Action Items

- [ ] Fix uses.md AI section (PRIMARY FIX)
- [ ] Fix privacy-first-ai-lab 80GB VRAM claims
- [ ] Audit all 43 AI/LLM blog posts for similar issues
- [ ] Add performance metrics section with realistic numbers
- [ ] Document offloading strategy if actually used
- [ ] Create "Model Selection Guide" for 24GB VRAM
