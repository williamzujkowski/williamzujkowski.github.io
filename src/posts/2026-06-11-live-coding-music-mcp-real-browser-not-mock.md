---
title: "Wiring an LLM to a Real Browser, Not a Mock: Lessons from an MCP Music Server"
date: 2026-06-11
description: "live-coding-music-mcp lets Claude drive Strudel.cc through real Playwright automation, not a mocked API. The interesting engineering isn't the music theory — it's narrowing what an LLM-controlled browser session can reach."
tags: [typescript, mcp, ai, security, music]
author: William Zujkowski
---

[live-coding-music-mcp](https://github.com/williamzujkowski/live-coding-music-mcp) is an **unofficial fan project**, not affiliated with or endorsed by [Strudel](https://codeberg.org/uzu/strudel), the live-coding pattern language it drives. It's a Model Context Protocol server that gives Claude 27 tools for composing, editing, and playing algorithmic music through [Strudel.cc](https://strudel.cc/): pattern generation across eight genres, music-theory helpers, audio analysis, MIDI import/export. Status is Beta, 1709 tests, 86.32% statement coverage, explicitly marked "Not Production-Ready." I built it to see whether an LLM could do something closer to actual live coding than to prompting a black box for a song file.

The part worth writing about isn't the music. It's that Claude isn't calling a mocked "generate audio" API: it's driving a real, visible Chromium instance through a real web app, and every decision in the codebase's hardening work traces back to that one fact. I've [written before](/posts/2025-07-29-building-mcp-standards-server) about an MCP server that stayed inside a documentation-and-code sandbox; this one hands the model a live browser tab, which is a different risk category entirely.

## Driving the actual Strudel runtime

Most "AI makes music" demos work by having the model call a synthesis API that returns audio bytes. This project does something more literal: `StrudelController` launches Chromium with Playwright, navigates to `https://strudel.cc/`, waits for the CodeMirror editor to initialize, and then drives it directly through `strudelMirror.editor.dispatch(...)` — the same programmatic API the site's own UI uses internally, not keyboard-event simulation. That's about 80% faster than typing character-by-character, and it means the "pattern" Claude writes is executing inside the actual Strudel runtime, with actual audio coming out of Web Audio API nodes that `AudioAnalyzer` samples for real FFT spectrum, tempo detection, and Krumhansl-Schmuckler key detection. When the README says tempo detection "degrades under headless audio," that's not hedging: it's an honest admission that analyzing real audio from a real (optionally invisible) browser tab is harder than analyzing a number a mock returned.

The test suite draws the line explicitly: `src/__tests__/utils/MockPlaywright.ts` implements a `MockPage` with fake `click`/`type`/`waitForFunction` methods so unit tests don't need a real browser, and browser-dependent specs are skipped in CI (20 of them, gated behind an actual Playwright install). That split is the right call for a test suite, but it means the mock only exists at the test boundary. The browser-touching tools always drive the real thing, and "real thing" here means an LLM has standing access to launch and control a Chromium process that auto-accepts media-stream permission prompts (`--use-fake-ui-for-media-stream`) and plays audio without a user gesture (`--autoplay-policy=no-user-gesture-required`). Strudel produces sound, so those flags are load-bearing, not incidental.

That access is not sandboxed the way the README implies. The Security section states "Playwright runs Chromium in sandbox mode," but the actual launch call passes `--no-sandbox` and `--disable-setuid-sandbox` alongside `--disable-gpu`:

```typescript
this.browser = await chromium.launch({
  headless: this.isHeadless,
  args: [
    '--use-fake-ui-for-media-stream',
    '--autoplay-policy=no-user-gesture-required',
    '--disable-dev-shm-usage',
    '--no-sandbox',
    '--disable-setuid-sandbox',
    // other args omitted
```

`--no-sandbox` is common in containerized CI because Chrome's OS-level sandbox needs privileges Docker doesn't grant by default, and this project does ship a Dockerfile. So the flag is very likely there for that reason, not carelessness. But it's the opposite of what the README's security claim says, and for a tool whose entire premise is "let an LLM drive a real browser," that's exactly the line that should say precisely what protects what. Real automation earns real scrutiny; a security section is only as good as its accuracy against the actual launch args.

## The v4 story: fewer tools is a security property, not just tidiness

Version 3.0 shipped 17 tool mergers behind a deprecation window — `write`/`append`/`insert`/`replace`/`clear` collapsed into `edit_pattern({ mode })`, `play`/`pause`/`stop` into `playback({ action })`, and so on, with the old single-verb names kept as deprecated forwarding aliases. `tools/list` sat at 84 entries: 26 consolidated tools plus 58 aliases quietly pointing at them. Version 4.0.0 deleted all 58 aliases (#178). `tools/list` dropped to 26 — it sits at 27 on main today, after MIDI import/export landed. Net change from the deletion: about 1,100 fewer lines across 43 files — the tool definitions, their case-branch handlers, and the per-module "legacy aliases still forward" test blocks all gone at once.

The framing that matters here isn't code cleanliness, it's protocol surface area. An MCP tool list is the entire interface an LLM has to reason about at decision time: every extra tool is one more thing the model can pick wrong, one more code path that has to independently validate its inputs, one more place a schema can drift out of sync with its sibling. Having `play`, `stop`, `pause` *and* `playback({ action: "play" | "stop" | "pause" })` covering the same mutation isn't redundancy for redundancy's sake: it's two independent implementations of the same trust boundary that both have to stay correct forever. Deleting the 58 aliases didn't remove functionality; every one of them had a direct enum-parameterized replacement. It removed 58 opportunities for the smaller of two implementations to be the one with the bug, and 58 extra entries an LLM had to disambiguate between on every tool-selection decision. Fewer tools, same capability, smaller error surface: that's a security argument even though nothing about it reads like one.

## Per-session isolation: the same idea, applied to browser state

Multi-session support (#108, landed in 3.0.0) gives every browser-touching tool an optional `session_id`. Named sessions get their own `StrudelController` instance (their own Chromium page), their own undo/redo/history stack, and their own `AudioCaptureService` — genuinely separate objects, not a shared controller with a session-ID field threaded through it. `SessionManager` caps concurrency at 5 sessions and evicts idle ones after 30 minutes.

That's the same principle the tool-count reduction is chasing, aimed at a different axis. Tool consolidation narrows what a single call can do; session isolation narrows what one conversation's state can leak into another's. If Claude is composing a techno beat in session A and a jazz progression in session B, a bug in one session's `edit_pattern` call shouldn't be able to corrupt the other session's pattern history or bleed audio between the two `AudioCaptureService` instances. For a local single-user MCP server this isn't multi-tenant security in the traditional sense: there's explicitly no authentication, and the README says so plainly under "Known Limitations." It's closer to a discipline you'd apply to any system where one execution context shouldn't be able to touch another's resources by accident, applied here because an LLM juggling multiple simultaneous "sessions" in one long conversation is a real failure mode, not a hypothetical one.

## What this doesn't claim

This is a beta, unofficial, single-maintainer fan project with no authentication and an explicit "not production-ready" label. I'm not arguing it's hardened software. The pattern-content validation is genuinely there (gain capped at 2.0 to protect speakers, eval blocks rejected, path traversal blocked in the JSON pattern store), but it's a secondary layer. The structural safety work — the work that actually shows up as deleted code and isolated objects rather than as a validation function — is concentrated on narrowing what the LLM-controlled browser session can reach and how many ways it can reach it, not on filtering the music itself. If a future version reintroduces a large single-verb tool surface, or drops per-session isolation for a shared controller "to simplify," that would be the regression to watch for, not a new pattern-validation gap.

## Sources

- [live-coding-music-mcp repository](https://github.com/williamzujkowski/live-coding-music-mcp)
- [live-coding-music-mcp README — Architecture, Security, Multi-Session sections](https://github.com/williamzujkowski/live-coding-music-mcp/blob/main/README.md)
- [live-coding-music-mcp CHANGELOG — v4.0.0 alias removal (#178) and v3.0.0 multi-session (#108)](https://github.com/williamzujkowski/live-coding-music-mcp/blob/main/CHANGELOG.md)
- [StrudelController.ts — the Chromium launch args (`--no-sandbox`, `--disable-setuid-sandbox`) and the `strudelMirror.editor.dispatch` write path](https://github.com/williamzujkowski/live-coding-music-mcp/blob/main/src/StrudelController.ts)
- [Strudel — the live-coding pattern language this project drives](https://strudel.cc/)
