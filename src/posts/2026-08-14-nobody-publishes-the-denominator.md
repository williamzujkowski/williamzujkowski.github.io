---
title: "Nobody States Their Denominator"
date: 2026-08-14
description: "npm's own replication database says 4,288,093 packages. The aggregator most supply-chain research runs on says 5,732,659. The gap is retained unpublish tombstones, and sampling from the wrong side moves a headline number by sixteen points."
tags:
- security
- supply-chain
- open-source
- vulnerability-management
---

I'm censusing eleven package registries. Not the important packages — all of them, including the several million nobody has ever depended on. Sample a few thousand from each, then report what fraction declares a source repository, what fraction of those links still resolve, what fraction has one maintainer, what fraction was published once and never touched again.

Before you can sample a population you have to count it. So the first question was the boring one, and it turned out not to have an agreed answer: on npm the two best sources differ by more than the entire contents of PyPI.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/counted-anyway.png'); width: min(320px, 76%); aspect-ratio: 420/209; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">unpublished, and still on the tally</p>

## Why count the boring four million

The obvious objection first, because it's the one that decides whether any of this matters.

Everyone who measures open-source health measures the head. The Linux Foundation's [Census III](https://www.linuxfoundation.org/research/census-iii) ranks the most-used packages. Andrew Nesbitt's [Weekend at Bernie's](https://nesbitt.io/2026/05/08/weekend-at-bernies.html) took 8,606 packages resolving to 5,874 distinct repositories and found 12.1% dead, 20.2% dormant, and 18.9% unknown. Those are good studies and they answer the question most people have: what are we all standing on?

They didn't overlook the tail. They excluded it, deliberately, and a reasonable person can argue the excluded part is mostly typosquats, tutorial leftovers, generated SDKs and abandoned experiments — in which case measuring it precisely is precision applied to garbage.

Two reasons I think it's worth counting anyway. **Attackers shop in the tail, not the head** — a name with no dependents and a dead maintainer is the cheap end of the supply chain, and its value to an attacker doesn't depend on its download count. And **claims computed from the head circulate as claims about the whole population.** "X% of open source is unmaintained" gets quoted without its frame roughly every week. You cannot know whether the head is representative until somebody measures the rest, and nobody has.

That's the argument. If you don't buy it, the rest of this post is a story about counting things badly, which is at least a shorter commitment.

## Two counts, one registry

npm's own replication database, `replicate.npmjs.com/_all_docs`, enumerated **4,288,093** package names when I ran it on 14 August 2026. Enumerating [ecosyste.ms](https://ecosyste.ms/) — the cross-registry index a great deal of supply-chain research runs on, mine included — gave **5,732,659**. Both numbers drift daily; npm's `doc_count` moved by 91 during a 41-minute window, and a later run of my own enumerator returned 4,288,186.

Neither is a number either party publishes as gospel, and that matters. ecosyste.ms's own API reports 5,731,796 or 5,728,700 depending on which endpoint you ask, a self-disagreement of about 3,000 that rules out quoting either as exact. The 5,732,659 is my enumeration of their list, not their published figure.

**This gap is not news.** Socket [reported it in their 2023 retrospective](https://socket.dev/blog/2023-npm-retrospective): they had ingested "almost four million packages" against npm's "more than 2.5 million live packages," and named the cause correctly — "many packages end up getting removed from the registry." They also counted 1,241,583 versions unpublished in that year alone. The [npm-follower](https://arxiv.org/abs/2308.12545) dataset (Pinckney, Cassano, Guha and Bell, ESEC/FSE 2023) was built partly around the same problem, noting that packages deleted from npm "can not be scraped" after the fact, and archiving over 330,000 deleted versions in ten months.

So removals were the known answer. What nobody published is the **shape** of the gap, and it isn't the shape everyone assumes.

<figure class="arch-fig">
<div class="arch" role="group" aria-label="How the two npm frames decompose into three disjoint zones">
  <section class="arch-tier" data-label="Only in npm's _all_docs" role="group" aria-label="Only in npm's _all_docs"><span class="arch-chip is-warn"><b>189,237</b><i>live packages with no row in the aggregator</i></span></section>
  <section class="arch-tier" data-label="In both" role="group" aria-label="In both"><span class="arch-chip is-primary"><b>4,098,856</b><i>the packages everyone agrees exist</i></span></section>
  <section class="arch-tier" data-label="Only in ecosyste.ms" role="group" aria-label="Only in ecosyste.ms"><span class="arch-chip is-warn"><b>1,633,803</b><i>~89% tombstones: a name, and nothing behind it</i></span></section>
</div>
<figcaption>Three disjoint zones. The totals differ by 1,444,566, which is the two differences netted — not a single one-directional gap.</figcaption>
</figure>

The assumption worth killing is that the aggregator is a **superset**: it has everything npm has, plus some stale rows. It isn't. **189,237 packages that are live on npm right now have no row in it.**

Some of that is ordinary ingestion lag, and any continuously-syncing index of 5.7 million names will show some. I checked whether lag explains all of it, because if the npm-only zone skewed heavily recent that would be the boring answer. It doesn't — some of those packages were published months ago. So the honest description is retention *plus* lag, running in opposite directions, and 4.4% behind is a lag figure for a small nonprofit syncing a registry this size, not a defect.

That still changes the arithmetic, because the two zones don't cancel.

I didn't trust the enumeration on its own — an enumeration that silently drops rows produces exactly this shape. So I re-estimated both differences a second way, by uniform random draw, in a way that doesn't depend on either enumeration being complete. Eco-only came back 30% [25.7, 34.7], npm-only 3% [1.7, 5.2], with both enumerated figures inside their intervals.

## The mechanism is tombstones

Draw 400 ecosyste.ms names at random and ask npm about each. 280 come back as live packages. 13 are properly gone — HTTP 404, no document at all. The other **107 are tombstones**.

When a package is unpublished, npm deletes the CouchDB document, so the name drops out of `_all_docs`. But `registry.npmjs.org` still answers for it — HTTP 200, with a body containing `_id`, `name`, and `time.unpublished`. No versions. No repository. No licence. No maintainers.

<figure>
<div class="flow" role="group" aria-label="What happens to a package name after it is unpublished">
  <div class="flow-node"><b>Package unpublished</b><i>author or npm removes it</i></div>
  <div class="flow-node is-bad"><b>CouchDB doc deleted</b><i>name leaves <code>_all_docs</code></i></div>
  <div class="flow-node"><b>Registry still answers</b><i>HTTP 200, stub body</i></div>
  <div class="flow-node is-bad"><b>Aggregator keeps the row</b><i>marked, not removed</i></div>
  <div class="flow-node is-bad"><b>Counted as a package</b><i>with no metadata to read</i></div>
</div>
<figcaption>An unpublished name survives as a 200 with nothing behind it. Both a status-code check and a row count will tell you it is a package.</figcaption>
</figure>

I can't find this documented anywhere. npm's [unpublish docs](https://docs.npmjs.com/unpublishing-packages-from-the-registry/) say only that the package "will be unable to be installed"; the replication API docs say it differs from the public registry API without saying how. If someone can point me at the spec, I'd genuinely like to read it.

The rows I checked on the aggregator side were **marked, not removed**, and keeping them is a defensible choice for an archive. It may be the more useful one: "this name used to be a package and now isn't" is exactly the information npm-follower was built to preserve, because it's unrecoverable once deleted. It is simply the wrong list to divide by.

There's a second artifact running the *other* direction, inside the frame I chose. npm's [unpublish policy](https://blog.npmjs.org/post/141905368000/changes-to-npms-unpublish-policy) says that when every version of a package is removed, the name is replaced with a **security placeholder** pointing at `github.com/npm/security-holder`, so it can't be squatted. Those are live rows in `_all_docs` carrying a real repository field — all of them the same one. They'd score as "declares a source repository," inflating the metric in the opposite direction from tombstones. They have to be excluded by name, and any census that doesn't say whether it did is hiding a second frame problem behind the first.

## Why this is worth sixteen points

The census reads the repository claim from raw registry metadata, deliberately, because aggregators normalise that field and normalisation hides the thing I'm measuring. The prior it's calibrated against is **42.4% of npm packages declaring no repository**, from a uniform sample of n=2,000 (±2.2 points) drawn in August 2026.

That prior has a frame too, and I should state it rather than repeat this post's own mistake: it was drawn from `all-the-package-names` — a third list, with a third answer — under an eligibility rule requiring a resolvable registry document, with ineligible draws replaced. Which is lucky, because the filter makes it a base rate among packages that actually resolve, and that is exactly the input the calculation below needs.

Now sample from the aggregator's list instead. **26.75% of your draws are tombstones**, each scoring as "no repository declared" — correctly, in that the field really is missing, and uselessly, in that it was never a package. Another 3.25% are 404s: no document, nothing to read, and *not* an answer. Those come out of the denominator rather than getting a default written into them, which is the whole point of the exercise.

```
tombstones          0.2675 / (1 − 0.0325)          = 0.2765
live, at the prior  (0.70 / (1 − 0.0325)) × 0.424  = 0.3068
                                            total  = 0.5833
```

**42.4% becomes 58.3%.** Sixteen points, manufactured by which list you sampled from, on rows that aren't packages.

The exact figure moves a little with how you treat the 404s — 15.4 points if you fold them in with the living, 16.4 if you let them score as missing repositories. That the answer is sixteen-ish under every defensible treatment is the useful part. What isn't defensible is the version I published here a day ago, which used the eco-only share (28.5%) as though it were the tombstone rate and quietly let the 404s count as "no repository declared" — writing a default into the one state the schema exists to protect. Same headline, wrong working, and wrong in the direction that flattered me. [The correction is in the repo.](https://github.com/williamzujkowski/oss-census)

And the error is directional rather than random. Dead packages are the ones most likely to carry a dead repository claim, so the bias runs *into* the metric and in the flattering direction — larger than most effects a study like this is trying to detect.

Nesbitt named this failure mode in [The Mismeasure of Open Source](https://nesbitt.io/2026/05/09/the-mismeasure-of-open-source.html): the absence of a signal gets written into the cell as a zero rather than as "unknown," so a project that lacks an attribute and a project nobody could measure come out identical. A tombstone is that bug wearing a package's name.

So the census records three states, not two: measured, measured-and-absent, and not answerable. Nothing in the schema lets you write a default into the third. It sounds pedantic right up until 3.25% of your sample *is* the third one and moving it moves your headline by a point.

## A 200 is not proof of existence

The natural fix, once you know tombstones exist, is to filter them out. Ask the registry whether each name is real, keep the ones that are.

Write that check the obvious way — 200 means it's there — and it reports all 1,633,803 eco-only names as live, which would mean npm's own replication database is missing 28% of npm. You would then go and file a bug against CouchDB.

The registry isn't lying. It's answering a different question than the one you think you asked: not "does this package exist" but "do I have a document at this key." The census records document *shape*, never status codes.

Filtering on the aggregator's `status` field doesn't rescue it either, and here I can do better than the anecdote I published first. On a sample of npm rows, `status` carries `"unpublished"` on most dead rows, so it's populated and it's useful. But the schema declares it only as nullable with no enumerated values, and the `?status=` query parameter appears to be ignored: `status=unpublished` and `status=active` returned identical mixes. It's a field you can read, not a filter you can build a population on.

## Endpoints that hand you a plausible wrong number

The same class of problem showed up everywhere once I went looking, and it always wears an HTTP 200. These are endpoint defaults rather than registries misreporting themselves, which is a duller headline and a more useful warning.

| endpoint | what it does | what you'd conclude |
|---|---|---|
| MetaCPAN `_search` | `hits.total` caps without `track_total_hits` | **CPAN has 10,000 distributions** (real: 41,743) |
| NuGet `query` | returns an empty array past a `skip` bound | **NuGet has 4,000 packages** |
| Maven `solrsearch` | `rows=500` silently returns 20 docs | your harvester runs 25× slower than you think |
| Hex `/api/packages` | `per_page=1000` returns 100 | — page size only; its count is correct |

The MetaCPAN one is the nastiest, because **10,000 is a completely believable number of Perl distributions**. It's wrong by 4.2×. In fairness the cap isn't MetaCPAN's invention — it's Elasticsearch's documented default since 7.0, and Elasticsearch normally warns you by returning `{"value": 10000, "relation": "gte"}`. MetaCPAN's v1 compatibility layer flattens that to a bare integer, so the field that would have told you arrives stripped. Add `track_total_hits` and the same query returns 41,743.

So the harvester now treats a short page as a failure rather than a result. If you asked for 500 rows and got 20, that's an error. The only way to accept a short final page is to prove it's the last one: a server-declared total reached exactly, a null cursor, or an exhaustion probe. There's deliberately no escape hatch for "the page was just short": that's the thing being caught.

Then the quieter version of the same bug: **paging that returns the right number of rows and the wrong rows.** A first enumeration of ecosyste.ms's `package_names` endpoint came back with 323,887 rows holding 256,522 distinct names — 21% duplicates, from offset paging over an unstable sort. Every duplicate is also a name that never got served, so the result was silently incomplete in both directions while looking complete. Passing an explicit sort fixes it entirely. This is an endpoint property, not a defect in anyone's data, and the rule it teaches is portable: **assert that distinct-count equals row-count, every time.**

## When there is no frame to fix

Go was going to be the twelfth registry. It doesn't have one. It has `index.golang.org`, an append-only log of module versions the public proxy has been asked for, which sounds close enough until you draw from it. Rows are `(path, version)` pairs, so you draw a version and not a module — distinct paths ran 15–68% of rows depending on the slice, and one path took 204 of 2,000. The log also contains things nobody published: one rewriting mirror host was 8.7% of a slice, because somebody fetched a project through a corporate proxy and every version got re-indexed under the proxy's hostname. Machine-generated SDKs were 20.8% of another. A mailing-list archive appears as a module.

The timestamp semantics don't help, though in fairness Go documents them — the index says plainly that its timestamp is when a version was first cached by the proxy, not when it was published. That's fine until you use it as a publish date.

So "one-shot publish" has no definition in Go. A single row means the module was asked for once, equally consistent with a one-version module and a fifty-version module somebody fetched once. Go goes in a labelled appendix, measured as what it is: a demand log. Worth publishing on its own terms, worth nothing to the cross-registry numbers.

## What I did about it

I committed the protocol to git before sampling a single package. It named ecosyste.ms as the primary frame. It also required a frame audit per registry, with the explicit power to overrule the protocol.

The audit used that power. The aggregator lost the denominator job, and npm is now sampled from `_all_docs` with security-holder placeholders excluded. Maven's frame looks backwards — Central's search index appears to hold 47,289 *more* packages than the aggregator while being weeks *older* — though that one is still open: the audit passed Maven conditionally, and until the count is settled against the full Nexus index neither number is validated. Several counts I'd written down as registry figures were aggregator figures I'd mislabelled.

Every one of those was cheap because nothing had been sampled yet. The same corrections after publication would each have been a retraction, which, as the sixteen-points section records, is not a hypothetical.

One thing I won't publish: the list. Diffing the two sources yields something close to a register of once-used npm names that no longer resolve, and npm only blocks republishing for 24 hours. The security-holder policy covers the packages npm removed, not every name an author dropped. Rates and mechanisms are a defensive contribution; the names are a target list, so the census publishes counts and the diff stays on my disk.

None of this is new as a concern, and pretending otherwise would be its own kind of frame error. Sampling and population validity in software-engineering research have a literature — [Baltes and Ralph](https://arxiv.org/pdf/2002.07764) on sampling, [Molléri](https://arxiv.org/abs/2404.15093) on who is actually being studied. What I can add is a worked instance with a number attached, in an ecosystem where the frame is a URL you can go and fetch.

The actual census numbers come later, once packages have been sampled. The protocol, the audits, and the code are public at [oss-census](https://github.com/williamzujkowski/oss-census), including the amendment where I had to write down that I'd picked the wrong list, and the correction where I got my own arithmetic wrong in this post's favour.

**The frame decides the finding, and it does so before you write a line of analysis.** Reproduce this census the obvious way — one uniform API, one weekend — and you'd get an answer that differs from mine in a known direction by a known amount, and nothing in your pipeline would tell you.
