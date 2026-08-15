---
title: "Nobody Publishes the Denominator"
date: 2026-08-14
description: "Before censusing eleven package registries I had to answer the boring question: how many packages are there? npm's own database and the aggregator everyone builds on differ by 1.6 million names. The gap is retained unpublish tombstones, and picking the wrong side moves the headline number sixteen points."
tags:
- security
- supply-chain
- open-source
- vulnerability-management
---

I'm building a census of eleven package registries: npm, PyPI, crates.io, RubyGems, Packagist, NuGet, Maven Central, Hex, CPAN, Pub, CocoaPods. Not the important packages. All of them. Sample a few thousand from each, then report what fraction declares a source repository, what fraction of those links still resolve, what fraction has exactly one maintainer, what fraction was published once and never touched again.

Everyone who measures open-source health measures the head. The Linux Foundation's [Census III](https://www.linuxfoundation.org/research/census-iii) ranks the most-used packages. Andrew Nesbitt's [Weekend at Bernie's](https://nesbitt.io/2026/05/08/weekend-at-bernies.html) deliberately picked 5,874 critical repositories, and found 12.1% of them dead. Those are good studies, and they answer "what are we all standing on." Nobody publishes the other number — the denominator, the whole population, including the four million packages nobody depends on.

Before you can sample from a population you have to know what the population is. So the first question was the boring one: how many packages are there?

It does not have an agreed answer. On npm the two best sources differ by more than the entire contents of PyPI.

## Two counts, one registry

npm's own replication database, `replicate.npmjs.com/_all_docs`, enumerates **4,288,093** package names. [ecosyste.ms](https://ecosyste.ms/) — the cross-registry index that a great deal of supply-chain research now runs on, mine included — reports **5,732,659**.

The obvious explanation is lag: the aggregator is a superset, npm has deleted some things, everything is fine. That explanation is wrong, and it took a full enumeration of both sides to see how.

| | count | share |
|---|---:|---:|
| `_all_docs` | 4,288,093 | |
| ecosyste.ms | 5,732,659 | |
| in ecosyste.ms, **absent from npm** | 1,633,803 | 28.5% of ecosyste.ms |
| in npm, **absent from ecosyste.ms** | 189,237 | 4.4% of npm |

That second row is the one that kills the simple story. If the aggregator were merely a stale superset, it would be zero. Instead 189,237 packages that are live on npm right now are missing from it, and the two differences net out to the headline gap, which is exactly why comparing the totals looks like ordinary lag and isn't.

I didn't trust the enumeration on its own, because an enumeration that silently drops rows produces this same shape. So both differences were re-estimated a second way, by uniform random draw against neither list: eco-only 30.00% [25.72, 34.66], npm-only 3.00% [1.72, 5.17]. Both exact figures land inside their intervals. The difference is real, not an artifact of how I counted.

## The mechanism is tombstones

Draw 400 ecosyste.ms names at random and ask npm about each one. 280 come back as live packages. 13 are properly gone. The other **107 are tombstones**, and they are the interesting case.

When a package is unpublished, npm deletes the CouchDB document, so the name drops out of `_all_docs`. But `registry.npmjs.org` still answers for it — with HTTP 200, and a body containing `_id`, `name`, and `time.unpublished`. No versions. No repository. No licence. No maintainers.

<figure>
<div class="flow" role="group" aria-label="What happens to a package name after it is unpublished">
  <div class="flow-node"><b>Package unpublished</b><i>author or npm removes it</i></div>
  <div class="flow-node is-bad"><b>CouchDB doc deleted</b><i>name leaves <code>_all_docs</code></i></div>
  <div class="flow-node"><b>Registry still answers</b><i>HTTP 200, stub body</i></div>
  <div class="flow-node is-bad"><b>Aggregator keeps the row</b><i>marked, never removed</i></div>
  <div class="flow-node is-bad"><b>Counted as a package</b><i>with no metadata to read</i></div>
</div>
<figcaption>An unpublished name survives as a 200 with nothing behind it. Both a status-code check and a row count will tell you it is a package.</figcaption>
</figure>

ecosyste.ms never removes the row. It marks it and keeps counting it. That is a perfectly defensible thing for an archive to do — arguably the right thing, since "this name used to be a package and now isn't" is real information you cannot recover once it's deleted. It is simply the wrong number to divide by.

## Why this is worth sixteen points

Here is the part that turned a plumbing detail into a decision I had to make in writing, in advance.

The census reads the repository claim from raw registry metadata, on purpose, because aggregators normalise that field and normalisation hides the thing I'm trying to measure. A prior npm sample put "no repository declared" at **42.4%**.

Now sample from the aggregator's frame instead. 28.5% of your draws are tombstones. A tombstone has no repository field, so every one of them scores as "no repository declared" — correctly, in the sense that the field really is missing, and uselessly, in the sense that it was never a package.

```
0.285 + (0.715 × 0.424) = 0.588
```

**42.4% becomes 58.8%.** Sixteen points, manufactured entirely by which list you sampled from, on rows that aren't packages. No bug, no typo, nothing you'd catch in review — just a number that came out higher than the truth because of a choice most papers don't state.

And the error is directional rather than random. Dead packages are the ones most likely to carry a dead repository claim, so the bias runs *into* the metric, in the flattering direction, at a magnitude larger than most effects a study like this is trying to detect.

Nesbitt named this failure mode in [The Mismeasure of Open Source](https://nesbitt.io/2026/05/09/the-mismeasure-of-open-source.html): the absence of a signal gets recorded as a low value instead of an unknown, so a project that lacks an attribute and a project nobody measured come out identical. A tombstone is that bug wearing a package's name. Its repository field really is missing. It was never a package.

That's why the census records three states rather than two — measured, measured-and-absent, and not answerable — with no way to write a default into the third. It sounds pedantic right up until 28.5% of your sample is the third one.

## A 200 is not proof of existence

The natural fix, once you know tombstones exist, is to filter them out. Ask the registry whether each name is real and keep the ones that are.

Write that check the obvious way — 200 means it's there — and it reports all 1,633,803 eco-only names as live, which would mean npm's own replication database is missing a quarter of npm. You would then go and file a bug against CouchDB.

The registry is not lying. It's answering a different question than the one you think you asked: not "does this package exist" but "do I have a document at this key." The census now records document *shape*, never status codes.

Filtering on the aggregator's own `status` field may not rescue it either, though here I'm on thinner evidence: a spot check of three dead PyPI rows found two carrying `status: null`. Three rows is an anecdote, not a rate. It was enough to stop me relying on the field without measuring it first, which is the only claim I'll make for it.

## Four registries lie about their own size

The same class of problem showed up everywhere once I went looking, and it always wears an HTTP 200.

| endpoint | what it does | the plausible wrong answer |
|---|---|---:|
| MetaCPAN `_search` | caps `hits.total` without `track_total_hits` | **10,000** (real: 41,743) |
| Maven `solrsearch` | `rows=500` silently returns 20 docs | 20 |
| NuGet query | empty array past a `skip` bound | 0 |
| Hex | ignores `per_page` | 20 |

The MetaCPAN one is the nastiest, because **10,000 is a completely believable number of Perl distributions**. It's wrong by 4.2×. Nothing in the response says so. Add `track_total_hits: true` and the same query returns 41,743.

So the harvester now treats a short page as a failure rather than a result. If you asked for 500 rows and got 20, that's an error, and the only way to accept a short final page is to prove it's the last one — a server-declared total reached exactly, a null cursor, or an exhaustion probe. There is deliberately no way to satisfy that check by saying "well, the page was short," which is the condition it exists to catch.

There's a quieter cousin, too: paging that returns the right *number* of rows and the wrong rows. A first crates.io enumeration came back with 323,887 rows holding 256,522 distinct names — 21% duplicates, from offset paging over an unstable sort. Every duplicate is also a name that never got served, so the enumeration was silently incomplete in both directions while looking complete. Passing an explicit sort fixes it entirely. Assert that distinct-count equals row-count, always.

## Sometimes the frame can't be fixed

Go was going to be the twelfth registry. It isn't, and working out why was the most interesting afternoon of the project.

Go has no registry. It has `index.golang.org`, an append-only log of module versions the public proxy has been asked for. That sounds close enough to a package list until you measure it:

- Rows are `(path, version)` pairs, so drawing a row draws a **version**, not a module. Distinct paths were 15–68% of rows depending on the slice. One path took 204 of 2,000.
- The log contains things nobody published. One rewriting mirror host was 8.7% of a slice, because somebody fetched a project through a corporate proxy and every version got re-indexed under the proxy's hostname. Machine-generated SDKs were 20.8% of another. A mailing-list archive appears as a module.
- `Timestamp` is **first-fetch, not publish**. The log's opening rows are 2018-dated pseudo-versions all stamped with the index's 2019 origin date, which is what you'd expect from a log that started by recording whatever people asked for first.
- Modules nobody ever fetched through the public proxy have no row at all, and you cannot bound that exclusion from inside the log.

So "one-shot publish" and "release cadence" have no definition in Go. A single row means the module was asked for once — equally consistent with a one-version module and a fifty-version module somebody fetched once.

Go goes in a labelled appendix, measured as what it actually is: a demand log. That's a genuinely novel thing to publish, and it contributes to none of the cross-registry numbers.

## What I did about it

The protocol for this census was committed to git before any package was sampled, which is the entire reason this story has a happy ending instead of a retraction. It named ecosyste.ms as the primary frame. It also required a frame audit per registry, with the explicit power to overrule the protocol.

The audit used that power three times: the aggregator lost the denominator job, Maven's frame turned out to be backwards (Central's own index holds 47,289 *more* packages while being nine weeks *older*), and Go was demoted. Several counts I'd written down as registry figures were aggregator figures I'd mislabelled — RubyGems is 195,967, not 210,512; CPAN's index holds 267,995 *module* rows against roughly 41,743 distributions.

Every one of those was cheap to fix because nothing had been sampled yet. The same corrections after publication would each have been a retraction.

None of this is a criticism of ecosyste.ms, which is doing something genuinely valuable and which the census still depends on for reverse dependencies, funding links, advisories, and PyPI maintainer counts, none of which exist anywhere else in uniform form. Retaining unpublished packages is the right call for an archive and the wrong call for a denominator. Those are different jobs.

The lesson I'd hand to anyone doing this kind of work: **the frame decides the finding, and it does so before you write a line of analysis.** Reproduce this census the obvious way, from one uniform API in a weekend, and you'd get an answer that differs from mine in a known direction by a known amount, and nothing in your pipeline would tell you.

The actual census numbers come later, once packages have been sampled. The protocol, the audits, and the code are public at [oss-census](https://github.com/williamzujkowski/oss-census), including the amendment where I had to write down that I'd picked the wrong list.
