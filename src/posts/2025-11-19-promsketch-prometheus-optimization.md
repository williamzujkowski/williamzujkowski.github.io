---
title: "PromSketch: What Sketch Algorithms Can and Cannot Do for Prometheus"
description: "PromSketch accelerates *_over_time window aggregations by compiling into Prometheus as a library. What it covers, what it doesn't, and why the distinction matters."
author: "William Zujkowski"
date: 2025-11-19
tags: [prometheus, monitoring, observability, performance, grafana, homelab, optimization]
post_type: tutorial
---

# PromSketch: What Sketch Algorithms Can and Cannot Do for Prometheus

PromQL queries fall over on high-cardinality metrics, and the failure mode is familiar to anyone running a homelab Prometheus: the dashboard takes longer to load than the incident it was supposed to help diagnose. Every panel is a full scan over a window, every scan touches every matching series, and the cost grows with cardinality whether or not you actually needed sample-level precision.

[PromSketch](https://arxiv.org/abs/2505.10560) (PVLDB vol. 18) is a research answer to that. It is worth understanding precisely, because it is narrower than the pitch implies and the narrowness is the interesting part.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/promsketch.png'); width: min(240px, 64%); aspect-ratio: 400/248; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">the shape kept, the detail dropped</p>

## What it actually is

Not a proxy. Not a drop-in replacement. Not something you put between Grafana and Prometheus.

PromSketch is a **Go library you compile into a patched Prometheus** — the paper describes it as "a standalone module that can be integrated into Prometheus and VictoriaMetrics." The [upstream repository](https://github.com/ProjectASAP/promsketch) is source files and no server: no Dockerfile, no published image, no HTTP handler, no listening port. There is nothing to `docker run`.

This matters because the obvious mental model — a caching layer you drop in front of your existing stack — is wrong in a way that wastes an afternoon. If you want to try it, you are building a patched Prometheus from source, and that is the actual cost of adoption.

## The function set is the whole story

PromSketch does not accelerate PromQL generally. It accelerates a specific, enumerable list of window aggregations, and its dispatch table is the honest documentation:

```go
var funcSketchMap = map[string]([]SketchType){
	"avg_over_time":      {USampling},
	"count_over_time":    {USampling},
	"entropy_over_time":  {EHUniv},
	"max_over_time":      {EHKLL},
	"min_over_time":      {EHKLL},
	"stddev_over_time":   {USampling},
	"stdvar_over_time":   {USampling},
	"sum_over_time":      {USampling},
	"sum2_over_time":     {USampling},
	"distinct_over_time": {EHUniv},
	"l1_over_time":       {EHUniv},
	"l2_over_time":       {EHUniv},
	"quantile_over_time": {EHKLL},
}
```

Read what is *not* in that map. No `rate`. No `histogram_quantile` — the string appears nowhere in the codebase. No `sum … by`, no `topk`, no `count`, no `avg`.

That rules out most of what a typical Grafana dashboard is made of. The canonical slow panel — `histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))` — is untouched by PromSketch, because every function in it is outside the set. If your dashboards are built the usual way on histogram buckets and `rate`, this tool does nothing for them.

Where it does apply is single-series window statistics over long ranges: `quantile_over_time` on a raw latency gauge, `distinct_over_time` for cardinality estimates, `entropy_over_time` for distribution shift. Those are genuinely expensive and genuinely sketchable.

## The algorithms, correctly named

Quantiles go through **EHKLL** — an Exponential Histogram wrapping a KLL sketch — not DDSketch. There is a DDSketch variant in the source but it is commented out (`// ehdd *ExpoHistogramDD`), which is a useful reminder that reading a paper's related-work section is not the same as reading its code.

The exponential histogram is the part that earns its keep. Sliding-window aggregation normally means either keeping every sample in the window or recomputing from scratch; an EH keeps buckets at exponentially increasing age granularity, so old data is summarised coarsely and recent data finely, at logarithmic space in the window length. The KLL sketch then answers rank queries within that structure.

**Count-Min Sketch** shows up in this family too, and it is worth being precise about its guarantee, because it is routinely overstated. CMS uses O((1/ε)·log(1/δ)) space — **independent of stream length**, not `O(log n)` — and gives a *one-sided additive overestimate* bounded by εN with probability 1−δ. It never undercounts and it has no multiplicative error bound. "Under 1% error" is not a thing CMS promises.

## What accuracy you are trading

The paper reports **at most 5% average error** across the statistics it evaluates, against speedups of up to two orders of magnitude. Take the 5% seriously rather than assuming the good case: an approximate P99 that is 5% off is fine for a dashboard trend line and is not fine for an SLO you are paying out against.

The general shape of the trade: sketches are the right tool when you are looking at a curve, and the wrong tool when a specific number has consequences. Most dashboards are the former and most alerts are the latter, which suggests keeping exact queries in the alerting path even if you sketch the visualisation.

## Cheaper things to try first

PromSketch is a research prototype under GPL-3.0 that requires building Prometheus from source. Before that, the boring options usually win:

**Recording rules.** The most under-used feature in Prometheus. A recording rule evaluates an expensive expression on the scrape interval and writes the result as a new series — so the dashboard queries one pre-computed series instead of aggregating thousands at render time. The storage cost is one series per rule, which is kilobytes, and it works today with no patched binary. If your dashboards are slow and you have not done this, do this.

**Reduce cardinality at the source.** Most high-cardinality problems are a label that should never have existed — a request ID, a full URL path, a pod name in a metric that outlives the pod. `metric_relabel_configs` at scrape time is cheaper than any query-side optimisation, because the samples never get written.

**Thanos or Cortex downsampling**, if you already run them. Worth correcting a common misconception: downsampling *adds* 5m and 1h resolutions alongside the raw blocks — it does not delete your recent data. The cost is extra storage and a multi-component deployment, not lost fidelity.

**VictoriaMetrics**, which the PromSketch paper itself uses as an integration target and which is substantially more storage-efficient than Prometheus before any sketching is involved.

## Where this leaves it

Sketch-based approximation is a real idea with a real implementation behind a real paper, and it is aimed at a narrower target than the framing usually suggests: long-window statistics over individual series, in a patched binary you build yourself, at up to 5% error.

If your slow queries are `quantile_over_time` over hours of raw samples, this is aimed directly at you. If they are `histogram_quantile` over `rate` of bucket series — which is how most people write them — it is not, and no amount of deployment effort will change that. Checking which of those you have takes about a minute and saves the afternoon.

## Further Reading

- [PromSketch: Efficient and Accurate Sketch-based Query Serving for Metric Monitoring](https://arxiv.org/abs/2505.10560) — the paper, PVLDB vol. 18
- [ProjectASAP/promsketch](https://github.com/ProjectASAP/promsketch) — the implementation (GPL-3.0)
- [An Improved Data Stream Summary: The Count-Min Sketch and its Applications](https://doi.org/10.1016/j.jalgor.2003.12.001) — Cormode & Muthukrishnan
- [DDSketch: A Fast and Fully-Mergeable Quantile Sketch with Relative-Error Guarantees](https://arxiv.org/abs/1908.10693) — Masson, Rim & Lee
- [Gorilla: A Fast, Scalable, In-Memory Time Series Database](https://www.vldb.org/pvldb/vol8/p1816-teller.pdf) — the compression scheme Prometheus's TSDB descends from
- [Prometheus recording rules](https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/) — do this first
