---
title: "Search Is Part of the Static Build"
date: 2026-09-08
description: "How this site's Pagefind search works, why a 210-page index can obscure 92 posts, and the small changes that would make the archive easier to use."
tags: [web-development, accessibility, open-source]
author: William Zujkowski
draft: true
---

This site's search engine is a directory of generated files. Astro builds the pages, Pagefind indexes their HTML, and a Svelte dialog lets the browser search them. The index goes to GitHub Pages with everything else. There is no search service to restart, which is a modest but reliable pleasure.

The arrangement suits a technical blog: publish a post, rebuild the site, update the searchable archive. [Pagefind is designed for that sequence](https://pagefind.app/docs/). Its input is the finished site, so it does not need a second copy of the content model.

During an agent-assisted review on September 8, I looked at what that arrangement actually gives readers. The useful finding was about the index's contents. Searching for `ebpf` found the relevant article first, then spent the rest of the visible results showing different shelves containing the same article.

## The search engine travels with the pages

The [build script](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/875cc84036070b64b7b8ebca820d6e7b04552083/astro-site/package.json#L10) runs Astro and then Pagefind against `dist`. The resulting HTML and search assets are one deployment.

<div class="flow" role="group" aria-label="Static site search from build to reader">
  <div class="flow-node"><b>Astro build</b><i>Posts become HTML pages</i></div>
  <div class="flow-node"><b>Pagefind indexing</b><i>Selected HTML becomes search data</i></div>
  <div class="flow-node"><b>Static hosting</b><i>Pages and index ship together</i></div>
  <div class="flow-node"><b>Reader searches</b><i>Browser loads matching results</i></div>
</div>

The [Svelte component](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/875cc84036070b64b7b8ebca820d6e7b04552083/astro-site/src/components/Search.svelte#L77) imports Pagefind when a search needs it. It waits for at least two characters, debounces input by 200 milliseconds, then loads details for the first eight matches. Those are implementation settings, not measured performance claims.

Pagefind separates finding matches from fetching their result data. Its [API documentation](https://pagefind.app/docs/api/) shows the same pattern: call `search()`, select results, then await each result's `data()` function. A reader who never searches does not trigger this component's Pagefind import.

I also use Pagefind in [US Code Tracker](/posts/2026-04-02-building-us-code-tracker-law-as-git-history/). [Tsundoku](/posts/2026-02-23-building-tsundoku-digital-bookshelf/) uses a different, custom JSON index. Static search describes where the work happens; it does not prescribe one implementation.

## Which pages belong in the answer?

At the reviewed source revision, `875cc8403607`, a local production build indexed **210 pages**, while the published-post count was **92**. That difference alone is not a defect. About pages and project descriptions can be useful answers too.

The live `ebpf` query made the distinction concrete. It returned 17 matches. The component showed these first eight:

| Position | Destination | What the reader gets |
|---|---|---|
| 1 | The eBPF article | The explanation they searched for |
| 2 | `/tags/ebpf/` | An article listing |
| 3 | `/tags/kernel/` | Another listing |
| 4 | `/tags/threat-detection/` | Another listing |
| 5 | `/tags/linux/` | Another listing |
| 6 | `/tags/monitoring/` | Another listing |
| 7 | `/tags/security/` | Another listing |
| 8 | `/posts/` | The archive |

That is one query, observed during this review, rather than a relevance benchmark. The first result is good. The remaining visible space offers seven ways to resume browsing.

The cause is visible in the [shared layout](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/875cc84036070b64b7b8ebca820d6e7b04552083/astro-site/src/layouts/BaseLayout.astro#L299): every page using it gets `data-pagefind-body` on its main content. This correctly leaves the masthead and footer outside the searchable body. It also makes tag listings and the archive eligible.

[Pagefind's indexing controls](https://pagefind.app/docs/indexing/) let the author choose that boundary. Once any page uses `data-pagefind-body`, pages without the attribute are excluded. Individual sections can also use `data-pagefind-ignore`.

My proposed default is to index articles and selected standalone pages, with tag listings remaining navigation. That needs checking against representative searches before changing the layout. Someone searching for a broad topic may want a collection; someone searching for a specific command probably wants the paragraph containing it.

## A small interface still has moving parts

The dialog owns its own timers, asynchronous requests and focus handling. Static hosting does not simplify those responsibilities.

The review reproduced a stale-result case by delaying a mocked Pagefind response: start a search for `security`, reduce the input to `e`, then let the earlier response finish. Results for `security` appear beneath the shorter input. The [current search function](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/875cc84036070b64b7b8ebca820d6e7b04552083/astro-site/src/components/Search.svelte#L91) clears a pending timer, but already-running work can still assign results.

The proposed fix is to give each query a generation number and reject completions belonging to an older generation. Clearing the query or closing the dialog must invalidate that work too. Debouncing reduces how often searches start; it does not make their completion order predictable.

A second reproduced sequence involved focus: click Search, press Ctrl+K while it is already open, then Escape. The main page remained `inert`. The repeated open replaced the component's record of elements it needed to restore. Guarding an already-open dialog is a small change with a very visible consequence.

The [WAI modal-dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) describes the intended experience: focus enters the dialog, stays inside while it is modal, and normally returns to its trigger when it closes. The page also needs to become usable again. A beautifully focused button is limited consolation when the article beside it has retired.

## What I want the next version to do

These are proposed changes, not fixes shipped in the reviewed version. I want search results to spend more space on articles, old requests to stay old, and an unavailable index to produce a useful error instead of looking like an empty archive.

Verification should include a real query against the built index, a query with no matches, delayed responses, and repeated keyboard opening and closing. Index selection also needs a few deliberately different queries: a project name, a narrow technical term, and a broad subject.

The existing architecture can support all of that. The next improvement is choosing what belongs in its answers and making the small interface dependable enough to get readers there.
