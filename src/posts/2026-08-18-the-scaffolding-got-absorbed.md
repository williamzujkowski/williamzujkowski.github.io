---

author: William Zujkowski
date: 2026-08-18
description: "A year ago I wrote up two homegrown workarounds for gaps in AI coding tools. Both gaps have since closed. What replaced them, and what I'd keep."
title: "The Scaffolding Got Absorbed"
tags:
  - ai
  - automation
  - programming
---
In the summer of 2025 I wrote up two things I'd built to work around gaps in AI coding tools. One was a [standards repository with a `CLAUDE.md` router](/posts/2025-07-22-supercharging-claude-cli-with-standards) for giving a model persistent context about how I like to work. The other was [claude-flow](/posts/2025-08-07-supercharging-development-claude-flow), for running several agents against one task.

Both gaps have since closed, from underneath. This is the follow-up, and the short version is that most of what I built has been absorbed into the platform — which is the correct and slightly deflating outcome for a workaround.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/scaffolding.png'); width: min(260px, 68%); aspect-ratio: 400/377; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">the ladder, once the floor arrives</p>

## What changed

**claude-flow is now Ruflo.** `ruvnet/claude-flow` redirects to `ruvnet/ruflo`, and the install is `npx ruflo@latest`. Every `npx claude-flow …` invocation in the old post, and in every other write-up from that period, is dead at the first token.

**The `@load` convention was never implemented, and no longer needs to be.** I wrote a syntax that looked like it addressed a loader and was in fact a polite request to the model. The standards repo's own `CLAUDE.md` now carries a note saying the directive is planned rather than built. In the meantime, Claude Code grew the thing it was imitating.

**Skills replaced the routing problem.** A skill in `.claude/skills/` is a directory with a description, and it loads when the description matches what you're doing. That is conditional context loading with actual dispatch behind it — the mechanism I was gesturing at, implemented properly by people who could change the runtime rather than write a convention on top of it.

**Rules replaced most of the standards documents.** Path-scoped rules in `.claude/rules/` apply to the files they match. "These conventions apply to `src/api/**`" is a frontmatter field now, not a paragraph asking the model to notice which part of the codebase it's in.

**Subagents replaced most of the orchestration layer.** Claude Code spawns subagents natively, with their own context windows. The coordination that needed an external tool a year ago is a tool call.

## What I'd keep

Not all of it was scaffolding.

**Writing standards for a model is still worth doing, and the discipline transferred.** One rule per bullet, imperative mood, rationale on a separate line, sections small enough to quote whole, no cross-references between documents. That shape works whether the delivery mechanism is a skill, a rule file, or a paragraph you paste. It also turns out to be how you write documentation a new colleague can actually use, which I did not expect and probably should have.

**Compliance tagging next to the code has outlasted the tooling around it.** Annotating the function that implements a control, rather than maintaining a spreadsheet that claims it exists, is the durable idea. The mechanism for checking those annotations has changed twice and the practice hasn't.

**Decomposition is still the whole game in multi-agent work.** Agents do not discover that your task splits into five independent pieces. Native subagents changed who runs the pieces; they did not change that you have to identify them. The most useful thing I learned from claude-flow was how much of the value was in the decomposition and how little was in the orchestrator.

## What I got wrong, specifically

Two things, and they're different kinds of wrong.

**I described a convention as a mechanism.** `@load [CS:python + SEC:*]` reads like an API call. It is a string in a file that a model usually honours. I knew that when I wrote it and still described it as an "intelligent router," because the syntax I'd chosen made it easy to think of it that way. The lesson I'd actually pass on: if you build something whose behaviour is "the model usually does this," name it something that can't be mistaken for enforcement. The name shapes what you believe about it later.

**I repeated benchmark numbers I hadn't reproduced.** The 84.8% SWE-Bench figure, the 2.8-4.4x speedup, the 32.3% token reduction — all three are claude-flow's own README bullets. I quoted them in a way that implied measurement, and one of them I attributed to "official leaderboard submissions," which was not where it came from. A vendor's self-reported benchmark is a fine thing to mention and a bad thing to launder through your own byline. Both posts have been corrected.

## The pattern worth noticing

A year is a long time in this space, and the shape of the obsolescence is consistent: **the workarounds that got absorbed were the ones addressing a real gap, and the way you could tell was that the platform eventually built them.** Conditional context loading, path-scoped conventions, parallel agents with separate context — all three were real needs, all three are now features.

Which suggests a reasonable posture toward any tooling of this kind, mine included. Build the thing you need, use it, and expect the good parts to be reimplemented under you within a year or so. That's not wasted effort. But it does argue for keeping the layer thin, writing down *why* you built it rather than only *what* it does, and being unsentimental when the floor rises to meet the ladder.

The standards documents survived all of it. The router on top of them did not.
