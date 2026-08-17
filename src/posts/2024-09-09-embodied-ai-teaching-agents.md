---

date: 2025-05-14
description: A robot given an ambiguous instruction usually guesses. New work trains agents to ask a clarifying question instead, using LLM-generated rewards.
title: 'Teaching AI Agents to Ask for Help: A Breakthrough in Human-Robot Interaction'
tags:
  - ai
  - llm
  - robotics
---
Ask a household robot to "pick up the small container" when three containers are on the table and it will pick one. Not the right one, particularly — just one. It will not ask which you meant, because nothing in how it was trained rewards asking.

That gap is small to describe and awkward to close. A person handed the same instruction resolves it in about a second: *"the blue one or the glass one?"* The question is cheap, targeted, and ends the ambiguity. Getting a robot to produce that question at the right moment — and only at the right moment — turns out to be a research problem in its own right.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/teaching-agents.png'); width: min(190px, 52%); aspect-ratio: 400/389; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">a robot that knows to ask</p>

## Three bad options

Faced with an under-specified instruction, an embodied agent generally does one of three things, and all three are unsatisfying.

It **guesses** from some internal heuristic, which is fine when it happens to be right and opaque when it isn't. It **asks for the whole instruction again**, which is the conversational equivalent of "what?" and puts the entire burden back on the person. Or it **refuses**, demanding more specificity up front and making the human do the disambiguation work that the robot is standing right next to the answer for.

None of these is what a competent collaborator does. Ask a colleague for "the report on the shared drive" when there are four, and you get a question that resolves exactly the missing bit: "the quarterly analysis or the customer survey?" That targeted narrowing is most of what makes human collaboration efficient, and it is exactly the behaviour missing from instruction-following robots.

## Ask-to-Act

Ramrakhya and colleagues at Georgia Tech and Meta FAIR set this up as a benchmark task they call **Ask-to-Act** ([arXiv 2504.00907](https://arxiv.org/abs/2504.00907)). An agent is given a single- or multi-object rearrangement task in a home environment, with a deliberately under-specified instruction, and has to navigate under partial observability — it cannot see the whole scene at once, so some ambiguity is only discoverable by moving.

The requirement is stated carefully: the agent must ask **minimal yet relevant** clarification questions. Both halves matter. An agent that asks about everything is worse than one that guesses, because it converts a fast wrong answer into a slow annoying one. The task is not "ask more questions"; it is "know which single question is load-bearing."

This decomposes into four capabilities the agent has to have at once: notice that the instruction is under-determined *given what it can currently see*, generate a question that targets the specific ambiguity, fold the answer back into its plan, and then act. The architecture inherits from Vision-Language-Action models, and the multimodal-context handling has the same foundations discussed in [transformer architecture](/posts/2024-03-20-transformer-architecture-deep-dive).

## LLM-generated rewards

The training approach is the part I find most interesting, and it addresses a problem that would otherwise make this intractable.

Training a policy to ask good questions normally needs a large corpus of human-annotated ambiguous scenarios — someone deciding, thousands of times, whether a given question was the right one to ask in a given scene. That annotation cost is what stops most work of this kind before it starts.

Instead, they fine-tune multimodal LLMs as VLA policies using **online reinforcement learning with LLM-generated rewards**. The language model judges whether a question was relevant and helpful, and that judgement becomes the reward signal. No human demonstration corpus, no hand-engineered reward function.

Using a language model to grade the behaviour of a language-model-derived policy invites obvious objections about the grader inheriting the same blind spots as the thing it grades. The empirical answer is whether the resulting policy works, and it does — but it is worth being clear that the reward signal here is a model's opinion, not ground truth.

## The results, stated as the paper states them

The RL-finetuned model beat every baseline — including zero-shot GPT-4o and supervised fine-tuned MLLMs — by **10.4 to 16.5%**, and generalised to novel scenes and tasks. The authors describe it as the first demonstration of adapting MLLMs into VLA agents that can both act and ask for help, trained with LLM-generated rewards under online RL.

Ten to sixteen points over a zero-shot GPT-4o baseline is a real result and a modest one. It is worth resisting the urge to inflate it, because the interesting claim is not the size of the margin — it is that the behaviour was learned at all without an annotation corpus, and that it held up on scenes and instruction types the policy had not trained on. Generalisation is the part that suggests the model picked up something about clarification-seeking rather than memorising which scenes are ambiguous.

## Where this would matter

**Healthcare.** "Which medication: the pain reliever, the antibiotic, or the blood pressure medication?" is obviously preferable to a guess. It is also the setting where the gap between a benchmark result and a deployable system is widest, and where a 10-16 point improvement over GPT-4o is nowhere near the bar.

**Education.** Tutoring systems that detect an ambiguous student question and ask before answering, rather than confidently addressing the wrong interpretation. This is closer to shipping than the robotics cases because the cost of a bad clarification is an extra exchange, not a physical error.

**Industrial settings.** "To what torque specification?" beats applying a default. The determinism bar in manufacturing is higher than a learned clarification policy currently clears, but the failure mode — stop and ask — is at least the safe direction to fail in.

**Accessibility.** Assistive robots supporting people whose communication may itself be non-standard is arguably the application with the most value and the highest cost of getting it wrong. Both facts follow from the same property: the user may not be able to easily correct a robot that guessed.

## The unresolved parts

**Question overload.** The paper's "minimal yet relevant" framing names the tension but does not dissolve it. There is a threshold between an agent that asks too rarely and one that asks constantly, and where it sits probably depends on the person, the task, and how expensive a mistake is. A robot that checks in every thirty seconds will get switched off no matter how relevant each individual question was.

**Cultural variation.** Norms around question-asking differ substantially — directness, deference, how acceptable it is to interrupt. A clarification policy trained on one set of interaction norms is not obviously portable, and I have not seen this addressed anywhere in the current work.

**Modality.** Speech is not always the efficient channel. Pointing at two objects and raising an eyebrow resolves the container ambiguity faster than any sentence, and a robot with an arm already has the hardware to do it.

**Simulation to deployment.** The benchmark runs in home-environment scenes with an agent navigating under partial observability. The distance between that and a physical robot in an actual kitchen — real lighting, real clutter, real objects that were not in any asset library — remains the standing hard problem in robotics, and nothing here claims to have closed it.

## Why it's worth watching

Most of the work on embodied agents is about making them more capable at executing what they're told. This is about making them better at noticing when they haven't been told enough — which is a different skill, and one that gets more valuable as the agents get more capable, not less. An incompetent robot that guesses wrong is an annoyance. A highly capable one that guesses wrong, quickly and confidently, is a hazard.

Acknowledging uncertainty and resolving it through dialogue is so routine in humans that it barely registers as a skill. Getting it into artificial agents is turning out to be a genuine research programme, and the fact that it can be trained without an annotation corpus makes it a much more tractable one than it looked a year ago. It also connects to a broader theme in [AI learning with limited resources](/posts/2024-05-30-ai-learning-resource-constrained): the constraint that shapes the method is usually the cost of supervision, not the cost of compute.

---

*The [Embodied AI Workshop at CVPR](https://embodied-ai.org/) is the best single venue for tracking this area.*

## Sources

1. **[Grounding Multimodal LLMs to Embodied Agents that Ask for Help with Reinforcement Learning](https://arxiv.org/abs/2504.00907)** (2025)
   - Ramrakhya, Chang, Puig, Desai, Kira & Mottaghi — Georgia Tech and Meta FAIR
   - Introduces the Ask-to-Act task; RL-finetuned MLLM beats all baselines by 10.4-16.5%

2. **[Learning to Navigate in Complex Environments](https://arxiv.org/abs/1611.03673)** (2017)
   - Mirowski et al., DeepMind — *ICLR 2017*

3. **[RoboNet: Large-Scale Multi-Robot Learning](https://arxiv.org/abs/1910.11215)** (2019)
   - Dasari et al. — *CoRL 2019*

### Simulation platforms

- **[NVIDIA Isaac Sim](https://developer.nvidia.com/isaac-sim)** - robotics simulation platform
- **[Unity ML-Agents](https://github.com/Unity-Technologies/ml-agents)** - game engine for AI training
- **[Gymnasium](https://gymnasium.farama.org/)** - reinforcement learning toolkit (successor to OpenAI Gym)
- **[MuJoCo](https://mujoco.org/)** - physics simulation for robotics

### Cognitive architecture

- **The Society of Mind** - Marvin Minsky, Simon & Schuster, 1986
