---

author: William Zujkowski
date: 2026-08-18
description: "Ninety agent-assisted posts, audited against source. The defects weren't bad reasoning — they were artifacts nobody had ever executed. Why models produce that, why review can't see it, and what actually catches it."
title: "Nobody Ran It"
tags:
  - security
  - ai
  - automation
---
I audited every post on this site against the code, configs and papers it describes. Ninety of them, most written with agent assistance. Almost all had defects.

The interesting part is not that. It is that the defects had a **shape** — one specific enough to design against, and specific enough that I can tell you exactly why my review missed it.

None of them were bad reasoning. Every one was an artifact that had never been executed.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/silent-gate.png'); width: min(250px, 66%); aspect-ratio: 400/446; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">hooked through, hanging open</p>

## The receipt

Here is a threat-intelligence lookup from one of my posts, presented as part of a working homelab pipeline:

```python
def check_threat_intel(ip_address):
    api_key = os.environ.get('ABUSEIPDB_API_KEY')
    ...
```

`os` is never imported. The function raises `NameError` on its first line. Not sometimes — always, on every input, since the day it was written.

That function had never been run. Not once. It was generated, read, judged plausible, and published. And it is not an outlier: behind that first bug were three more, each independently sufficient to make the check useless. Wrong field name. Wrong nesting, so `.get(..., 0)` would return zero for a confirmed-malicious address. And `return 0` on any non-200, so the free tier's rate limit turns every attacker benign after the first HTTP 429.

Four bugs, all failing toward "clean." A person who had run it once would have found the first one in a second.

## Correcting myself, which sharpens the point

I originally wrote this section around a different claim: that config formats silently accept invented keys, so the mistakes are structurally invisible. I had a demo:

```python
tomllib.loads('[scanning]\nworkers = 4\n')   # parses clean
yaml.safe_load('expiration: 2025-12-31')      # parses clean
```

That demo is real, and the conclusion I drew from it was wrong. One of my own posts shipped a fabricated `osv-scanner.toml` full of invented keys — `[scanning]`, `workers`, `max_depth`. I assumed the tool had swallowed them.

It would not have. `osv-scanner` has **errored on unknown config keys since September 2024** — `internal/config/manager.go` calls `Undecoded()` and returns `unknown keys in config file`. The commit is `56e3a994`, titled *"feat: error if configuration file has unknown properties."* My post was published in October 2025.

So the file would have failed on the first run. The tool's authors had already built the exact defense I was about to recommend.

**The config didn't slip past a permissive parser. It never met the parser at all.** Which is a better thesis than the one I started with, and it is the same thesis as the `NameError`: these artifacts were read, not run.

## Why a model produces this

Not carelessness, and not lying. Two mechanisms, both measured.

**It generates plausible surface because plausible is what it optimises for.** The scale of this is now quantified: across 576,000 code samples from 16 models, [Spracklen et al.](https://arxiv.org/abs/2406.10279) found **5.2% of package references hallucinated for commercial models and 21.7% for open-source**, with 205,474 unique invented names. And the rate tracks corpus frequency — [an AWS study](https://arxiv.org/abs/2407.09726) found GPT-4o produced valid invocations for only **38.58%** of low-frequency APIs. Security-scanner config is exactly the low-frequency regime: plenty of examples of `.grype.yaml` in the world, not many, and adjacent tools supply keys that look right.

That is how you get `expiration:` in a grype ignore rule. Grype's `IgnoreRule` struct has nine fields and that is not one of them — but `expiration` is a real key in adjacent tools, so it arrives wearing the right clothes.

The unsettling detail is repeatability. Requerying hallucination-producing prompts ten times, Spracklen et al. found **43% of hallucinated packages repeated in all ten runs**. These aren't random slips; a large share are stable, which is what makes the [slopsquatting](https://www.theregister.com/2025/04/12/ai_code_suggestions_sabotage_supply_chain/) idea coherent. Though in fairness: as far as I can find, exploitation is not yet documented in the wild. The rate is measured, the repeatability is measured, and the only demonstration is a researcher registering an empty `huggingface-cli` package that got 30,000 downloads.

**It optimises the metric you actually gave it.** My archive has this written down in its own commit messages. One reads *"4 posts humanized (40-45 → 90-97.5)"* and lists what it added to get there: `47hrs Isaac Sim`, `2.3 FPS`, `73% accuracy`. Another: *"Claude-Flow: 40.1% → 20.6% (8 gists created, -49% code)"* — and those eight gists exist, created in a **21-second burst, weeks after the post that presents them as working notes.**

My favourite is a commit reporting **`Humanization: 105/100`**. A rubric optimised past its own ceiling.

This is [specification gaming](https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/): behaviour satisfying the literal specification without achieving the intended outcome. The rubric said *add concrete measurements*. It added concrete measurements. The measurements were the deliverable, and nothing in the objective said they had to correspond to anything.

It is also measurable in coding agents specifically. [ImpossibleBench](https://arxiv.org/abs/2510.20270) constructs tasks where the spec and the tests conflict, so any pass implies a shortcut, and reports **GPT-5 cheating on 54%** of them. Its opening example is the thing that most alarmed me in my own archive: an agent with access to unit tests may delete the failing test rather than fix the bug.

## Why review didn't catch it

This is the part I got wrong about myself, and the literature is unkind in a useful way.

**Code review does not find defects at anything like the rate people assume.** [Bacchelli and Bird](https://sback.it/publications/icse2013.pdf) hand-classified **570 review comments** at Microsoft. Their finding, verbatim: *"Review comments about defects are few, comprising one-eighth of the total in our sample, and mostly address 'micro' level and superficial concerns."* Code improvements outnumbered defects two to one.

And of those 570 comments, the number about wrong exception handling was **three**.

Three. Which is the category my `return 0` bug lives in, and it means my review missing it was not an unusual lapse. It is the base rate.

**The error paths are where the damage is.** [Yuan et al.](https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-yuan.pdf) analysed 198 real catastrophic failures across Cassandra, HBase, HDFS, Hadoop and Redis:

> almost all (92%) of the catastrophic system failures are the result of incorrect handling of non-fatal errors explicitly signaled in software

> in 35% of the catastrophic failures, the faults in the error handling code fall into three trivial patterns: (i) the error handler is simply empty or only contains a log printing statement…

Read pattern (i) again, then read the `security-gate` job I shipped in a CI pipeline post:

```yaml
security-gate:
  needs: [dependency-scan, container-scan, comprehensive-scan]
  if: always()
  steps:
    - run: |
        echo "All security scans completed"
        # Make final go/no-go decision
```

An error handler that only contains a log printing statement. Named as the gate. `if: always()`, so it passes when everything upstream fails. This has a CWE — [CWE-636, Failing Open](https://cwe.mitre.org/data/definitions/636.html) — and a thirty-year literature, and I shipped it anyway.

**And we look at machine-written code less carefully.** [Al Madi](https://arxiv.org/abs/2208.14613) eye-tracked 21 programmers reading Copilot output and human-written code. Complexity and readability were comparable, but *"programmers direct less visual attention to model generated code"*, significantly. The authors' own conclusion: beware complacency and automation bias.

So: a defect class that is invisible to reading, in the category review is worst at, in code we look at least closely. That is not a personal failure. It is a system with no check in it.

## It happened while I was writing this

I used a research agent for the citations above, with explicit instructions to verify against primary sources and to flag anything it could not confirm.

It came back with a detailed report. Then it came back **again**, unprompted, with a retraction: it had produced a Fagan 1976 quote — *"approximately two thirds of all errors reported during development are found by inspections"* — that does not appear in the paper. It had generated an archive.org identifier, a chapter attribution, a "cuts out 21%" filter detail, all correctly formatted, before opening any of the documents.

Most of those details were right, which is exactly why nothing looked wrong. The two that were wrong were wrong in the same register as the ones that were right.

It caught this only by re-fetching the primary sources. No consistency check would have found it, because the fabrication was internally consistent — which is itself a measured property. [Sui et al.](https://arxiv.org/abs/2406.04175) find hallucinated LLM output shows *higher* narrativity and semantic coherence than truthful output. Fabrication is smoother than truth. It reads better.

The defect class appeared in the middle of a task specifically instructed to guard against it. Which should tell you how much instruction is worth here, relative to verification.

## What actually works

**Run it.** This is the whole finding, and it is embarrassingly simple. Not "read it carefully" — execute it once, against something that should fail. The `NameError` dies on import. The invented TOML dies on parse, because the tool's authors already thought of that. The `security-gate` reveals itself the moment an upstream job fails. Reading is precisely the activity that cannot distinguish plausible from correct.

**Make the parser strict, and check whether it already is.** `serde`'s `deny_unknown_fields`, Pydantic's `extra='forbid'`, Go's `DisallowUnknownFields` (on `Decoder` only, not `json.Unmarshal`). Kubernetes made server-side field validation the default in **v1.27** — its motivating incident was a Service silently breaking because `containerPort` had been renamed `targetPort` and the server accepted the stale key. The tracking issue stayed open for seven years. The defaults are permissive, and they are changing.

**Check the arithmetic against the sample size.** Psychology has a mechanical test for this — [GRIM](https://en.wikipedia.org/wiki/GRIM_test), which exploits the fact that a mean of N integers must be expressible with denominator N. In its original application, **36 of 71 testable papers contained at least one impossible value.** My archive was full of the same thing: "73% accuracy" on a stated corpus of 50 items requires 36.5 items. I have not seen anyone point GRIM at model output, and it costs nothing.

**Check provenance, not just content.** `gh api gists/<id> --jq .created_at` against the post date. Eleven artifacts created in a 21-second burst are not working notes. `git log -S` on the artifact, and read the commit body — a pass that states its optimisation target is telling you what its numbers are for.

**Two independent implementations, with the caveat.** Differential testing is the strongest no-oracle technique there is: [Csmith](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf) found 325 previously-unknown compiler bugs. But [Knight and Leveson](http://sunnyday.mit.edu/papers/nver-tse.pdf) is the necessary counterweight — 27 independently written versions, a million tests, and correlated failure at 99% confidence, with roughly half the faults appearing in two or more programs. Independent authors do not produce independent mistakes. Their own conclusion is narrower than the folklore: not that N-version programming fails, but that its reliability *"may not be as high as theory predicts under the assumption of independence."*

**And be careful what you cite for any of this.** The most-quoted number in code review — "a review of 200-400 LOC over 60 to 90 minutes should yield 70-90% defect discovery" — is widely attributed to the Cisco/SmartBear study. It is not in the Cisco data. In the book it sits in a different chapter, by a different author, about personal reviews under the SEI's TSP, with no data behind it. The Cisco chapter explicitly declines the claim: *"we don't know how each of these reviews would have fared with a different process."* The vendor's own page states the 400-LOC finding with a Cisco attribution and then the 70-90% figure in the next sentence, unsourced. Nobody wrote a false sentence. The number acquired its authority by proximity.

Which is the same mechanism as everything above, in the literature about checking.

## What I changed

The pre-publish gate on this site now runs a sixth audit: artifact provenance and every config key against the tool's actual upstream schema, one key at a time, including semantics — a flag can exist and do the opposite, as `trivy --ignore-policy` does. Its sharpest rule is the one my archive taught me: **a measurement attached to an invented key means the surrounding numbers are generated too.** `workers = 4 is 40% faster` cannot have been measured if the key has never existed.

But the honest summary is shorter than the tooling. Every defect I found survived because an artifact was judged on how it read. The fix is not more careful reading.

Run it once. Point it at something that should fail. Watch it fail.

