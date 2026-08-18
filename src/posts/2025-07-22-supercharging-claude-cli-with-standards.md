---

date: 2025-07-22
description: "A CLAUDE.md is a prompt, not a loader. What a standards repository can and cannot enforce, and where the real enforcement has to live."
title: Exploring Claude CLI Context and Compliance with My Standards Repository
tags:
  - ai
  - compliance
  - professional-development
  - programming
---
## The problem: AI tools that forget everything

Every new session starts from nothing. You explain your coding style again. You paste the same security requirements. You get suggestions that contradict last week's suggestions, and the only thing keeping any of it consistent is your own memory.

So I built [github.com/williamzujkowski/standards](https://github.com/williamzujkowski/standards) — an MIT-licensed collection of development standards written to be read by a model rather than a person — and wired it into my projects through a `CLAUDE.md`. This sits alongside [progressive context loading](/posts/2025-10-17-progressive-context-loading-llm-workflows) and [prompt engineering](/posts/2024-04-19-mastering-prompt-engineering-llms) as one more attempt at the same problem: getting a model to behave consistently without re-explaining yourself.

It works, with a large asterisk that took me a while to accept and which is most of what this post is about.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/cli-standards.png'); width: min(320px, 80%); aspect-ratio: 400/136; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">the CLI, with house rules</p>

## The asterisk: `CLAUDE.md` is a prompt, not a router

I described this to myself for months as an "intelligent router" that detects what you're working on and loads the relevant standards. That is a flattering description of what happens, and it is wrong.

`CLAUDE.md` is a file the model reads at the start of a session. That's the whole mechanism. When I write:

```markdown
@load [CS:python + TS:pytest + SEC:*]
```

nothing parses that. There is no matching engine, no context detection, no dispatch. It is a convention I have asked the model to follow, expressed in a syntax that *looks* like an API because I found that shape easier to think in. The model usually follows it. "Usually" is doing real work in that sentence.

My own repository is explicit about this — `docs/core/CLAUDE.md` carries the note that the `@load` directive and its semantic loading syntax are planned rather than implemented, with the current version relying on a loader script. I wrote the aspirational syntax first and the honest note second, which is a fair summary of how this kind of project goes.

The one genuine mechanism in Claude Code is `@path/to/file`, which imports a file's contents. That is a real feature and it is less magical than it sounds: it is textual inclusion, and the included text costs tokens like any other.

**Why this matters if you are copying the pattern.** A convention the model follows most of the time is genuinely useful and is not a control. If something must happen every time — a licence header, a security review, a compliance tag — it cannot live in a prompt. It has to live somewhere that fails the build.

## On the token argument

The pitch for this pattern is usually token savings: replace a wall of pasted standards with a short reference.

The short reference *is* short. But the standards it points at still get read into context when they are actually needed, and `CODING_STANDARDS.md` on its own is around 23KB. So the saving is not "5,000 tokens became 100." The saving is in the standards you *don't* load on a given task — you pull the Python and testing conventions for a Python change and leave the frontend ones alone.

That is a real benefit and a much more modest one than a percentage implies. I would be sceptical of any headline figure here, including one of mine: the number depends entirely on what you compare against, and the tempting baseline — "loading every standard at once" — is a thing nobody does.

## NIST control tagging

The part I have found most durable is compliance tagging. Working against NIST 800-53r5 has come up repeatedly over the years, and having the control mapping live next to the code rather than in a spreadsheet is the difference between compliance being a document and being a property of the repository.

The repo ships `scripts/setup-nist-hooks.sh`, which installs a pre-commit hook that checks for control annotations:

```bash
git clone https://github.com/williamzujkowski/standards
./standards/scripts/setup-nist-hooks.sh
```

Tag the code where the control is actually implemented — in a comment next to the function that does the work, not in a header block at the top of the file. The value is that a reviewer reading the authentication path sees which control it satisfies, and notices when a change breaks that relationship.

## The pre-commit lesson worth keeping

I set up that hook feeling quite pleased with myself, then found I could sail straight past it:

```bash
git commit --no-verify
```

My first instinct was to close the hole from inside the hook. You cannot. `--no-verify` skips the pre-commit hook *entirely* — the hook process never starts, so nothing it might do on the way out can matter. There is no exit code that runs when the code doesn't run.

This is obvious in retrospect and it was not obvious to me at the time, and I suspect I am not alone, because "add a pre-commit hook" is the standard advice for enforcing almost anything.

**Client-side hooks are a convenience for the person running them. They are not enforcement.** Real enforcement is server-side, and there are three places to put it:

- a `pre-receive` hook on the remote, which cannot be bypassed by the client
- a required CI status check, so a PR cannot merge until validation passes
- branch protection, so nobody pushes to the default branch directly

The pre-commit hook is still worth having. It gives you the fast feedback loop, catching problems in the two seconds after you type `git commit` rather than five minutes later in CI. Just don't mistake the convenience for the control — which is the same mistake, in a different costume, as mistaking a prompt for a router.

## What I would tell someone starting this

**Write the standards as if a model will read them, because one will.** Short declarative rules, one concept per heading, no cross-references that require holding two documents in your head at once. The documents that work well for a model turn out to be the ones that work well for a new colleague.

**Keep the `CLAUDE.md` short.** Mine drifts toward bloat every time I add a rule for an edge case, and a long instruction file is one the model follows less reliably, not more — the rules compete for attention with each other and with your actual request.

**Put anything load-bearing where it fails the build.** Everything else is a strong suggestion, and strong suggestions are fine as long as you know which category a given rule is in.

**Expect to throw away the enforcement layer.** I rewrote mine repeatedly, and the versions that survived were the ones that checked fewer things more reliably.

## Where this pattern has gone since

Written in July 2025, and the ground has moved. Claude Code now has first-class **Skills** (`.claude/skills/`), path-scoped **rules**, **hooks**, and **subagents** — which between them cover most of what the `@load` convention was reaching for, with actual dispatch behind them rather than a hopeful convention.

The standards repository itself has since refactored toward a skills-based layout. If you are building this today, start there rather than from the syntax in this post. The underlying idea holds up: give the model your standards once, in a form it can use, and stop re-explaining yourself. The specific mechanism I reached for has been replaced by better ones, which is the normal and desirable outcome for a workaround.
