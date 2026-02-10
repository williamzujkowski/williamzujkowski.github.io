---
title: "From RouteLLM to Contextual Bandits: How Research Papers Shaped My Model Router"
date: "2026-01-15"
lastUpdate: "2026-01-15"
description: "How I went from naive round-robin model selection to a five-stage routing pipeline backed by RouteLLM, TOPSIS, and LinUCB research. The failures that led to each improvement."
author: "William Zujkowski"
tags: [ai, machine-learning, open-source, orchestration, research]
image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=630"
imageAlt: "Data visualization dashboard showing routing metrics and model performance"
readingTime: "10 min read"
---

I spent three months building model routers that didn't work before I started reading the papers. Round-robin was unfair. Random selection was wasteful. Static scoring was brittle. Every approach I tried had a failure mode that became obvious only after I deployed it against real tasks in my homelab.

This post walks through the research that fixed each problem, from [RouteLLM's](https://arxiv.org/abs/2406.18510) cost-quality tradeoff to [LinUCB's](https://arxiv.org/abs/2508.21141) adaptive learning. If you're building any kind of multi-model system, these papers probably save you the same months of trial and error.

## The Naive Phase: Why Simple Approaches Fail

### Round-Robin

My first router was embarrassingly simple. Tasks came in, models took turns. Claude got task 1, Gemini got task 2, Codex got task 3, repeat.

This broke immediately. A [security analysis](/posts/ai-new-frontier-cybersecurity/) task would land on whichever model was "next," regardless of capability. Codex got architecture reviews. Claude got simple code generation. The results were mediocre across the board because no model was getting the tasks it was good at.

I measured this: round-robin produced satisfactory results roughly 45% of the time. Not terrible, but not worth the infrastructure.

### Random Selection

I tried weighted random next. Give Claude 50% of tasks, Gemini 30%, Codex 20%. Better than round-robin because the weights roughly matched capability breadth, but still dumb. A research task had the same 50% chance of going to Claude whether it was a broad literature survey (Gemini's strength) or an architecture analysis (Claude's strength).

Satisfactory results climbed to maybe 55%. Still not enough to justify the complexity over just using Claude for everything.

### Static Scoring

Third attempt: score each model on dimensions like "code quality," "research breadth," "security analysis," and route based on task keywords. If the task mentioned "security," send it to the model with the highest security score.

This worked better at first. Maybe 65% satisfactory. But the scores were hand-tuned numbers I made up based on my experience. They didn't account for [context window constraints](/posts/context-windows-llms-memory-shapes-ai/), cost differences, or the fact that model capabilities change with every release. Every time a model got updated, my static scores were wrong.

I probably spent 40 hours tuning those weights manually before I realized I was solving a problem that researchers had already solved.

## The RouteLLM Wake-Up Call

The [RouteLLM paper](https://arxiv.org/abs/2406.18510) (Ong et al.) changed my thinking completely. Their key finding: you can route between a strong model and a weak model using a learned classifier, cutting costs by 85% while maintaining 95% of the quality. They trained on preference data from Chatbot Arena to predict which model would give a better response for a given query.

I couldn't use their exact approach. They optimized for a two-model strong/weak pair, and I had three models with overlapping capabilities. But the insight was transferable: **model selection is a classification problem with learnable features, not a static lookup table.**

This led me to think about the problem differently. Instead of hand-tuning scores, I needed a system that could:
1. Eliminate models that literally can't handle the task (context too small, missing capabilities)
2. Score remaining models on multiple dimensions simultaneously
3. Learn from outcomes over time

That became the three core stages of my router.

## Stage 1-2: Elimination and Budget Awareness

The first two stages are simple. The Budget Router checks billing mode. If you're on a monthly subscription (`plan` mode), cost is irrelevant, so route to the strongest model. If you're paying per token (`api` mode), cost factors into later scoring. This was inspired by RouteLLM's insight that the cost-quality tradeoff is the fundamental routing decision.

The Zero Router eliminates impossible matches. If a task needs 100K tokens of context and a model maxes at 32K, it's out. No fancy math needed. I was surprised how often this stage catches problems. Roughly 15% of tasks get at least one model eliminated here.

## Stage 3: TOPSIS Multi-Criteria Decision Analysis

For the scoring stage, I found the [MoMA framework](https://arxiv.org/abs/2509.07571), which applies TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) to model selection. TOPSIS is a multi-criteria decision method from operations research. You define criteria (quality, speed, cost, context fit), weight them, and the algorithm ranks alternatives by their geometric distance to the ideal solution.

What I liked about TOPSIS over simpler scoring: it handles tradeoffs naturally. A model that's slightly worse on quality but much cheaper gets ranked appropriately depending on the weights. Static scoring treats each dimension independently, so you can't express "I'll accept 10% less quality for 50% less cost" without ugly heuristics.

My TOPSIS implementation considers:
- **Quality score** per task category (code, research, security, architecture)
- **Context window utilization** (how well the model's window fits the task)
- **Speed** (tokens per second, approximate)
- **Cost** (when in API billing mode)

The whole computation takes under 5ms for 6-8 candidate models. TOPSIS is O(n*m) where n is models and m is criteria. With 8 models and 4 criteria, that's 32 operations plus some square roots. Not a bottleneck.

One thing the MoMA paper didn't address that I needed: the weights themselves should adapt. A user who never cares about cost should have different weights than one who's budget-constrained. I handle this with a Preference Router stage (Stage 3 in my pipeline) that adjusts TOPSIS weights based on user preferences and task hints before TOPSIS runs.

## Stage 4: LinUCB Contextual Bandits

The static stages (elimination, TOPSIS) handle maybe 80% of routing decisions well. But they can't learn. If Claude consistently produces better security reviews than Gemini despite similar quality scores, the static router doesn't notice.

The [PILOT paper](https://arxiv.org/abs/2508.21141) introduced me to contextual bandits for LLM routing. LinUCB (Li et al., applied to LLMs by PILOT) treats model selection as an explore/exploit problem. Each task is a "context" with features (category, length, complexity). Each model is an "arm" that produces a reward (success/failure). LinUCB learns a linear relationship between context features and expected reward for each arm.

The exploration-exploitation tradeoff is what makes this better than just tracking historical success rates. If Claude has a 90% success rate on security tasks but Gemini has only been tried twice, LinUCB will occasionally try Gemini to see if it's actually better. The Upper Confidence Bound ensures exploration happens naturally without a separate exploration phase.

I was worried this would be slow. It's not. LinUCB's update step is a matrix operation, but with 6-8 models and maybe 10 context features, the matrix is tiny. The entire bandit computation adds roughly 1ms to routing.

The feedback loop works like this: every task execution produces an outcome. A `computeQualityReward()` function converts the outcome into a 0-1 reward signal. That reward updates the LinUCB model for the arm (model) that was selected. Over time, the weights converge.

I'm still collecting data on how much LinUCB improves over static TOPSIS alone. My rough estimate is 10-15% improvement in task satisfaction after about 200 tasks, but I haven't run a proper A/B test yet. The [SATER paper](https://arxiv.org/abs/2510.05164) suggests confidence-aware routing can improve accuracy by 20-30%, but they tested on different benchmarks than what I'm measuring.

## What Didn't Make the Cut

Not every paper I read was useful. A few approaches I tried and discarded:

**Preference-trained classifiers** (the original RouteLLM approach): Training a classifier requires labeled preference data I didn't have. Chatbot Arena data doesn't transfer well to task routing because the tasks are different. I'd need thousands of labeled task-model-outcome pairs to train a good classifier.

**Cascade routing** ([OptiRoute](https://arxiv.org/abs/2502.16696)): Try a cheap model first, escalate to expensive if it fails. Good for cost optimization, but adds latency (two model calls instead of one) and the "did it fail?" check is itself an LLM call. Not worth it for my use case where the models are roughly similar in cost.

**Cross-attention routing** ([arXiv:2509.09782](https://arxiv.org/abs/2509.09782)): Uses the task prompt's attention patterns to select models. Interesting research, but requires access to model internals that I don't have through CLI interfaces.

## The Full Pipeline

The final router runs five stages in sequence:

1. **Budget Router** - Cost-aware or cost-ignored routing
2. **Zero Router** - Eliminate impossible matches
3. **Preference Router** - Adjust weights from user/task hints
4. **TOPSIS Router** - Multi-criteria scoring
5. **LinUCB Bandit** - Adaptive learning layer

Total latency: under 10ms. The routing decision is effectively free compared to the 2-30 seconds a model call takes.

If I were starting over, I'd probably skip the Preference Router and fold its logic into TOPSIS weight adjustment. Three of the five stages (Budget, Zero, Preference) are essentially pre-processing for TOPSIS. But the staged approach makes each component testable in isolation, and the 193 pipeline tests I've written validate each stage independently. I'd call that a worthwhile tradeoff.

## Papers Referenced

- [RouteLLM: Learning to Route LLMs](https://arxiv.org/abs/2406.18510) (Ong et al.) - Cost-quality routing with preference-trained classifiers
- [MoMA: Multi-objective Model Selection](https://arxiv.org/abs/2509.07571) - TOPSIS for LLM routing
- [PILOT: Practical LLM Routing](https://arxiv.org/abs/2508.21141) - LinUCB contextual bandits for model selection
- [SATER: Confidence-Aware Routing](https://arxiv.org/abs/2510.05164) - Difficulty estimation for routing decisions
- [OptiRoute: Cost-Efficient LLM Routing](https://arxiv.org/abs/2502.16696) - Cascade routing approach
- [Cross-Attention Routing](https://arxiv.org/abs/2509.09782) - Attention-based model selection

The [nexus-agents repository](https://github.com/williamzujkowski/nexus-agents) implements the full pipeline. The routing code lives in `src/cli-adapters/composite-router.ts` and the bandit in `src/cli-adapters/linucb-bandit.ts`.
