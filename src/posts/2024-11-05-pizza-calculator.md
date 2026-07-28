---
date: 2024-11-05
author: William Zujkowski
description: "I asked an early LLM to build a pizza calculator to find out whether it could write working code. It could. Then it kept adding features nobody asked for, and I made the mistake of encouraging it."
title: 'PizzaOps: How a Dumb LLM Experiment Became a Distributed System'
tags:
  - programming
  - homelab
  - tutorial
---
This was one of the first things I ever built with a large language model, back when "can it actually write working code?" was still a live question and not a settled one. I did not have a problem that needed solving. I had a Saturday, a new toy, and a hunch that "write me a pizza calculator" was a suitably low-stakes way to find out whether the thing could program. It could. That should have been the end of it.

It was not the end of it. Because when I asked for a pizza calculator, I got a pizza calculator — and then, unprompted, I got a slices-per-person multiplier. Then an adjustment factor for "event intensity." Then a code comment reminding me to account for teenagers. I had not mentioned teenagers. At no point in the conversation had teenagers come up. The model simply knew, the way you know, that teenagers change the math.

```javascript
function provision({ consumers, intensity, teenagers }) {
  const SLICES_PER_PIZZA = 8;
  let perPerson = 2.8 * (1 + 0.4 * intensity);
  if (teenagers) perPerson *= 1.5; // the model insisted. it was right.
  const units = Math.ceil((consumers * perPerson) / SLICES_PER_PIZZA);
  return Math.max(1, units); // you always round up. dignity does not divide.
}
```

Buried in all of this was a single genuinely correct piece of geometry, which I want to state plainly because it is the only useful sentence in the entire post: **an 18-inch pizza is more pizza than two 12-inch pizzas, and it usually costs less.** Area is πr². A 12-inch pizza is about 113 square inches; two of them, 226. An 18-inch is 254. The big one wins on area, wins on price, wins on the only axes that matter. This is not a preference. It is a theorem.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/pizza-calculator.png'); width: min(340px, 80%); aspect-ratio: 500/369; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">the 18-inch, vindicated</p>

## Where it went off the rails

I should have stopped there. Instead, some time later, I did the responsible thing and rebuilt the toy as an enterprise platform.

It has a control plane. It has a status page. It has a hunger-consensus quorum, an SLA measured in slices per consumer, a live p99 latency figure that measures nothing, and an Anchovy Isolation Chamber that is — by design — permanently isolated. It computes the exact same 18-inch geometry it always did, now wrapped in enough observability to satisfy an auditor who never asked to be here. I named it **PizzaOps**. It is genuinely functional. I am not going to talk you out of it.

**→ [PizzaOps™: the platform, in production](/pizza-ops/)**

## The one real incident

The original calculator did ship one true production failure. It told me two large pizzas would comfortably feed six people. I ordered exactly that, with confidence. We ran out in forty-five minutes.

The model had quietly assumed pizza was a side dish. At the gathering in question, pizza was the entire personality of the evening. This is now logged as SEV-1: *demand exceeded modeled capacity; root cause, optimism.* The fix was a "meal class" selector, which is a polite way of saying I taught the calculator the difference between a snack and a commitment.

## What I learned

Nothing. I learned nothing.

The math was correct the day it was written and it is correct now. Every feature that arrived after it — the multipliers, the meal classes, the quorum, the entire control plane — was decoration, and the decoration eventually became infrastructure. There is no lesson here. There is only pizza, and the calculator that pizza deserves.

Enjoy the calculator. Do not taunt the oven.
