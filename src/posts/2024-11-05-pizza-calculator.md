---

date: 2024-05-26
author: William Zujkowski
description: "A Saturday afternoon coding project that taught me more about assumptions than algorithms."
title: 'The Pizza Calculator: A Weekend Project in Humility'
tags:
  - programming
  - homelab
  - tutorial
image: "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=1200&h=630"
imageAlt: "Fresh pizza with melted cheese on a wooden board"

---
Years ago, I was at a weekend hackathon that ran long. We'd been coding for twelve hours when someone suggested ordering pizza. Twenty minutes later, three pizzas arrived for eight hungry developers. What followed was a surprisingly tense negotiation over slice allocation that probably cost us more productivity than the original bug.

That experience stuck with me. Fast forward to October 2024, and I found myself in a similar situation at home. My wife and I were ordering pizza and arguing about whether two 12-inch pizzas ($14.99 each) were a better deal than one 18-inch ($24.99). I opened VS Code and spent the next two hours building a calculator to settle it.

Spoiler: the 18-inch wins by a mile. Area scales with the square of the radius, so an 18-inch pizza has about 254 square inches versus 226 total for two 12-inch pizzas — and costs $5 less. Math doesn't lie.

## The Code

The first version was dead simple. A single HTML file, no frameworks, no build tools:

```javascript
function calculatePizzaOrder(team, duration, intensity) {
  const slicesPerPerson = 2.8;
  const slicesPerPizza = 8;

  // My first version forgot to account for this!
  const adjustmentFactor = intensity > 0.7 ? 1.2 : 1.0;

  const totalSlices = team.size * slicesPerPerson * adjustmentFactor;
  const pizzasNeeded = Math.ceil(totalSlices / slicesPerPizza);

  return {
    pizzas: pizzasNeeded,
    costPerPerson: (pizzasNeeded * 24.99) / team.size,
    slicesPerPerson: (pizzasNeeded * slicesPerPizza) / team.size
  };
}
```

I learned the hard way to always round up (`Math.ceil`). Pizzas are never perfectly circular, slice counts vary by 10-15% depending on how the pizzeria cuts them, and nobody has ever complained about leftover pizza.

## Where It All Fell Apart

Two weeks later, I got my first real-world test: ordering for a gathering of 6 people. The calculator said 2 large pizzas would be perfect. I confidently ordered exactly that.

We ran out in 45 minutes.

Turns out I had hardcoded `slicesPerPerson` at 2.8, which is reasonable for an office lunch where pizza is a side act. At a social gathering where pizza *is* the meal? People eat way more. I quickly added a "meal type" selector to the next version.

## What I Actually Learned

The pizza calculator is a toy, but it taught me something real: **the algorithm was never the hard part.** The math was sound from day one. What I got wrong was the assumptions feeding into it.

This is the same lesson that shows up everywhere in software:
- Your load test passes because the test data doesn't match production patterns
- Your monitoring catches every alert except the one that matters at 2 AM
- Your security controls work perfectly until a real user finds them inconvenient

The gap between "works in theory" and "works in practice" is almost always about context, not code. My pizza calculator was mathematically correct and practically useless until I started accounting for how people actually behave.

I still use the calculator. Version 3 has inputs for meal type, time of day, and whether there are teenagers present (a 1.5x multiplier, minimum). It's still just a single HTML file. Some problems don't need React.
