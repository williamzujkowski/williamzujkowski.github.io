---
title: "live-coding-music-mcp: Handing Claude a Browser and a Drum Machine"
date: 2026-06-11
description: "An MCP server that lets Claude live-code music in Strudel through a real, visible Chromium browser — no mocked audio API. What it does, what broke while I built it, and the engineering that came out of my first real browser-automation project."
tags: [typescript, mcp, ai, music, playwright]
author: William Zujkowski
---

live-coding-music-mcp is what happens when you hand a language model a browser and a drum machine and step out for coffee. Concretely: it's an MCP server that lets Claude write and play algorithmic music in Strudel, the live-coding language where you type `sound("bd hh sd hh")` and a beat falls out. It does this by driving the real Strudel site in a real, visible Chromium window — no mocked audio API. Claude types a pattern into the editor, the browser makes actual noise.

It was also my first serious attempt at browser automation from an LLM, which mostly means it was my first tour of the many ways a browser can let you down. I wanted to see whether a model could do something closer to live coding, hands on the instrument, than to the usual trick of prompting a black box for a finished track. Short answer: yes, once you stop treating the browser as a tidy API and start treating it as the temperamental analog synth it actually is.

## What it actually does

Point Claude at it and ask for a techno beat, and here's roughly what happens: a Chromium window opens — visibly, because this is meant to be watched, not hidden — and lands on strudel.cc. Claude calls `init`, then `compose({ style: "techno" })`, and a pattern lands in the CodeMirror editor and starts playing through your speakers. No audio file gets generated somewhere and handed back; the sound comes out of the same browser tab you're looking at, in real time, because that's the same tab running the same code a human would type by hand:

```javascript
setcpm(130)
stack(
  s("bd*4").gain(0.9),
  s("~ cp ~ cp").room(0.2),
  s("hh*16").gain(0.4).pan(sine.range(-0.5, 0.5)),
  note("c2 c2 eb2 c2").s("sawtooth").cutoff(800)
).swing(0.05)
```

From there it's genuinely a conversation. Ask for a walking bassline in F and it appends `note("g2 c2 f2").s("sine").gain(0.7)` to the stack. Ask it to analyze what's playing and it reads real FFT output off the Web Audio graph — bass, mid, treble, tempo, key — and reports back that the mix is bass-heavy, which for a techno pattern is not exactly a shocking diagnosis but is at least an honest one, because nothing about it was faked. Twenty-seven tools cover pattern editing, transforms (transpose, humanize, euclidean rhythms), playback, MIDI import/export, and eight genre templates, and every one of them is enum-parameterized — `edit_pattern({ mode })`, `transform({ op })` — rather than one tool per verb. More on why that matters in a minute.

## My first real browser-automation project

I'd [built MCP servers before](/posts/2025-07-29-building-mcp-standards-server), but always ones that stayed inside a documentation-and-code sandbox — read a file, run a lint, return text. This was the first time I'd handed a model a live browser tab and asked it to actually operate something inside it, and a browser turns out to be a much less cooperative instrument than a REST API.

The first surprise was how much of the work is just getting the browser to admit it's ready. Strudel loads CodeMirror asynchronously, initializes its own audio graph, and only then becomes something you can safely type into. Typing character-by-character into the editor like a human — Playwright supports this, and it's the obvious first thing to try — works but is slow and occasionally drops keystrokes on longer patterns. The fix was to stop simulating a human and use the editor's own write path instead: `strudelMirror.editor.dispatch(...)`, CodeMirror's own transaction API for mutating editor state. It's about 80% faster than typing, and more importantly it's the actual documented way to mutate that editor's state, not a workaround. Finding that call meant reading Strudel's own source rather than guessing at DOM selectors, which is a very ordinary lesson that nonetheless took me an embarrassing number of `page.type()` calls to learn.

The second surprise was audio analysis. Feeding a mock a number and having it hand the same number back is not analysis, it's an assertion with extra steps, and I wanted the real thing: actual FFT spectrum sampling, tempo detection from onsets, key detection via Krumhansl-Schmuckler pitch-class correlation. All of that works, and against a visible browser window with real audio output it works well. Run it headless, though, and tempo detection gets noticeably less reliable: the browser's audio pipeline behaves differently without a compositor actually painting frames, and onset detection is sensitive to that. The README's performance table notes tempo detection is "degraded under headless audio," and that line isn't hedging, it's a lab note. Real audio from a real browser is a harder signal to reason about than a canned number, which is obvious in hindsight and was not obvious to me three cycles into a debugging session at 1am.

The test suite reflects that split honestly: `src/__tests__/utils/MockPlaywright.ts` gives unit tests a `MockPage` with fake `click`/`type`/`waitForFunction` so most of the suite doesn't need a real Chromium process, and the 20 tests that do talk to an actual browser are skipped in CI and run locally instead. Out of 1,709 tests total, that's a small, deliberate split: the mock exists so the other 1,689 don't have to launch a browser, not because the real browser path is something to avoid.

## The parts I'm genuinely proud of

Version 3.0 shipped 17 tool mergers behind a deprecation window: `write`/`append`/`insert`/`replace`/`clear` collapsed into `edit_pattern({ mode })`, `play`/`pause`/`stop` into `playback({ action })`, and so on, with the old names kept as forwarding aliases so nothing broke mid-migration. That left `tools/list` at 84 entries: 26 real tools plus 58 aliases pointing at them, which is a lot of ways to ask a model to make the same decision. Version 4.0.0 deleted every alias in one pass (#178): 1,114 net fewer lines across 43 files, `tools/list` back down to 26 (27 today, after MIDI import/export landed). Nothing was removed except the redundancy — every alias had a direct replacement — but an MCP tool list is the entire menu an LLM reasons over at decision time, and a shorter menu with the same dishes is just a better menu. Fewer things to misread beats more things to be clever about, every time.

Multi-session support followed the same instinct in a different direction. Every browser-touching tool takes an optional `session_id`, and named sessions get their own `StrudelController`, their own Chromium page, their own undo stack, their own audio-capture service — not a shared object with a session field bolted on. `SessionManager` caps things at five concurrent sessions and evicts anything idle for 30 minutes, mostly so a jazz progression in one session and a techno beat in another can't quietly bleed into each other's history. It's a small thing. It also means "compose two tracks at once" is a feature rather than a bug report waiting to happen.

## What this is, plainly

This is a beta, single-maintainer fan project, unaffiliated with Strudel, with no authentication — the server trusts whoever's talking to it, which is fine for a local MCP tool and would be a terrible idea anywhere else. Pattern content does get some real validation before it runs (gain capped at 2.0 so it doesn't blow out your speakers, eval blocks rejected, path traversal blocked in the on-disk pattern store), but that's a secondary layer, not the point of the project.

And yes, the Chromium launch passes `--no-sandbox` and `--disable-setuid-sandbox`. Chrome's OS-level sandbox wants privileges Docker doesn't hand out by default, and this project ships a Dockerfile, so the flag is there for the boring container reason rather than for any more interesting one. I'm not going to pretend that's a triumph of secure-by-default engineering, it's the same trade every containerized Chrome instance makes, but it's also not the story here. The story is that a model can sit down at an actual instrument and play it, badly at first and then less badly, and that turned out to be more fun to build than I expected.

## Sources

- [live-coding-music-mcp repository](https://github.com/williamzujkowski/live-coding-music-mcp)
- [live-coding-music-mcp README — Architecture, Security, Multi-Session sections](https://github.com/williamzujkowski/live-coding-music-mcp/blob/main/README.md)
- [live-coding-music-mcp CHANGELOG — v4.0.0 alias removal (#178) and v3.0.0 multi-session (#108)](https://github.com/williamzujkowski/live-coding-music-mcp/blob/main/CHANGELOG.md)
- [StrudelController.ts — the Chromium launch args (`--no-sandbox`, `--disable-setuid-sandbox`) and the `strudelMirror.editor.dispatch` write path](https://github.com/williamzujkowski/live-coding-music-mcp/blob/main/src/StrudelController.ts)
- [Strudel — the live-coding pattern language this project drives](https://strudel.cc/)
