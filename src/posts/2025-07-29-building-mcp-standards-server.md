---

date: 2025-07-29
description: "Build MCP standards server for Claude AI—implement Model Context Protocol for intelligent code standards and context-aware workflows."
images:
  hero:
    alt: 'Down the MCP Rabbit Hole: Building a Standards Server - Hero Image'
    caption: 'Visual representation of Down the MCP Rabbit Hole: Building a Standards Server'
    height: 630
    src: /assets/images/blog/hero/2025-07-29-building-mcp-standards-server-hero.jpg
    width: 1200
  inline: []
  og:
    alt: 'Down the MCP Rabbit Hole: Building a Standards Server - Social Media Preview'
    src: /assets/images/blog/hero/2025-07-29-building-mcp-standards-server-og.jpg
title: 'Down the MCP Rabbit Hole: Building a Standards Server'
tags:
  - ai
  - mcp
  - open-source
  - programming

---
## Bottom Line Up Front

I built a standards server that was supposed to be a simple wrapper around my documentation repository. Three weeks later, I had written 6,000 lines of code across 47 components, implementing Redis caching, vector search, six different language analyzers, 88 tests, and a React UI.

For a read-only documentation server. That I'm the only user of.

This is a case study in scope creep, premature optimization, and what happens when you let "one more feature" become your guiding principle. The irony? Version 1 worked perfectly fine at 200 lines of code.

But here's the thing: personal projects are where we learn by overdoing it, by making every mistake in the book when the stakes are low. This post walks through the evolution from working prototype to over-engineered monstrosity, examining the classic developer pitfalls I hit along the way, including tool-driven architecture, the seduction of sophisticated patterns, and the massive gap between "it works" and "it's production ready."

**The Numbers**: Version 1 (200 lines, 2 hours, functional) → Version 4 (6,000+ lines, 3 weeks, questionably necessary). Redis cache with 30-minute TTL for documentation that changes once a month. Vector search implementation for 50 markdown files. Six language-specific analyzers for standards that are 90% YAML. This isn't a success story: it's a cautionary tale about knowing when good enough is perfect.

## When Good Ideas Get Complicated

Remember last week when I was all excited about my standards repository? Well, I made the classic developer mistake: "You know what would make this better? If I rebuilt it from scratch with a completely different architecture!"

Enter the [Model Context Protocol (MCP)](https://docs.claude.com/en/docs/mcp) – Anthropic's new way for LLMs to interact with external tools. The idea was simple: instead of copying CLAUDE.md into every project, why not serve the standards directly to Claude through MCP? This server became a key component of my broader workflow when [supercharging development with Claude-Flow](/posts/2025-08-07-supercharging-development-claude-flow), enabling dynamic standards integration across multiple projects.

Three weeks and several rewrites later, I have [github.com/williamzujkowski/mcp-standards-server](https://github.com/williamzujkowski/mcp-standards-server). It works! Mostly. When Redis is happy. And the moon is in the right phase.

## The Original Vision vs Reality

### What I Planned (Week 1)

"I'll wrap my standards in an MCP server. How hard could it be?"

```python
# My naive first attempt
class StandardsServer:
    def __init__(self):
        self.standards = load_standards()  # Easy!
    
    def get_standard(self, name):
        return self.standards[name]  # Done!
```

### The Reality (Week 3)

```python
# Current reality - 6000+ lines of code later
class MCPStandardsServer:
    def __init__(self):
        self.rule_engine = RuleEngine()
        self.semantic_search = HybridVectorStorage()
        self.cache_layer = RedisL1L2Cache()
        self.analyzers = MultiLanguageAnalyzerFactory()
        self.compliance_mapper = NISTComplianceEngine()
        self.token_optimizer = CompressionStrategy()
        # ... 47 more components
```

Yeah, it got away from me a bit.

## The Architecture Journey

### Version 1: "Keep It Simple"
I started with stdio communication. Just pipe standards in and out. Clean, simple, working.

Then I thought: "What about caching?"

### Version 2: "Add Some Redis"
Added Redis for caching. Now I had two problems: cache invalidation and Redis connection management.

Then I thought: "What about semantic search?"

### Version 3: "ChromaDB Will Fix Everything"
Added ChromaDB for vector search. Now I had three problems: embeddings, vector storage, and "why is my laptop fan screaming?"

Then I thought: "What about multi-language support?"

### Version 4: "The Kitchen Sink"
Current state. It has:
- 6 language analyzers (Python, JS, Go, Java, Rust, TypeScript)
- 25 comprehensive standards (up from my original 10)
- Redis L1/L2 caching architecture
- Semantic search with boolean operators
- NIST compliance mapping
- A React web UI (because why not?)
- Performance benchmarking
- 88 integration tests

I may have overdone it.

## What Actually Works (The Good Parts)

Despite my scope creep, some genuinely useful stuff emerged:

### Intelligent Standard Selection

Context-aware rule engine eliminates manual standard selection:

```python
context = {
    "project_type": "web_application",
    "framework": "react",
    "requirements": ["accessibility", "performance"]
}

# Automatically loads: react-18-patterns, wcag-2.1, performance-optimization
standards = engine.evaluate(context)
```

**Capabilities:**
- Analyzes project structure and dependencies
- Maps requirements to relevant standards automatically
- Loads 3-5 standards per project (vs. 25 total available)
- Eliminates guesswork about which standards apply
- Adapts recommendations based on framework versions

### Multi-Language Code Analysis

Automatic language detection with fix generation:

```bash
mcp-standards validate src/ --language auto
# Detects Python, finds 3 PEP-8 violations
# Detects JavaScript, suggests ES6 improvements
# Generates fix patches automatically
```

**Features:**
- Supports 6 languages: Python, JavaScript, Go, Java, Rust, TypeScript
- Auto-detects language from file extensions and syntax
- Provides violation explanations with line numbers
- Generates `.patch` files for automatic fixes
- Integrates with pre-commit hooks

### Token Optimization That Actually Matters

Compressed formats reduce LLM token costs by 70-90%. This optimization strategy builds on the principles I discuss in my guide to [progressive context loading for LLM workflows](/posts/2025-10-17-progressive-context-loading-llm-workflows), where efficient token management becomes critical for complex projects:

```python
# Full standard: 5000 tokens
# Compressed: 500 tokens
# Reference only: 50 tokens

standard = get_standard("react-patterns", format="compressed")
```

**Compression strategies:**
- Bullet-point summaries (500 tokens, 90% reduction)
- Reference-only mode (50 tokens, 99% reduction)
- Dynamic expansion: Request details only when needed
- Saves ~$0.15 per standard load at current API pricing

## The Struggles (Learning Moments)

### Redis Is Not Your Friend at 3 AM

I spent two frustrating days tracking down silent cache failures before I realized I'd configured Redis with a noeviction policy. My "temporary" cache was storing everything indefinitely.

**The Problem:**
- Spent 2 days debugging silent cache failures
- Redis exceeded memory limits (maxmemory policy: noeviction)
- "Temporary" cache stored everything indefinitely
- 200MB cached data for documentation that changes monthly
- Cache hit rate: 99% (because nothing ever expired)

**The Fix:**
- Added 30-minute TTL on all cache entries
- Reduced maxmemory from 512MB to 64MB
- Implemented [LRU eviction policy](https://redis.io/docs/latest/develop/reference/eviction/)
- Result: Memory usage dropped 87%, performance unchanged

**Lesson learned**: TTLs exist for a reason. Use them.

### Vector Databases Are Hungry

**The Absurdity:**
- [ChromaDB](https://docs.trychroma.com) consumed 4GB RAM for 25 markdown documents
- 160MB per document for semantic search
- Index generation: 47 seconds
- Query latency: 89ms average
- Alternative: `grep -r "pattern" docs/` → 12ms

**The Reality Check:**
- Total corpus size: 250KB of text
- Vector embeddings: 1,536 dimensions per chunk
- Overhead ratio: 16,000:1 (storage vs. original text)
- Use cases requiring semantic search: 0

**Lesson learned**: Sometimes grep is enough. Not everything needs AI.

### The MCP Protocol Is Still Evolving

**The Breaking Change:**
- MCP spec 0.3 → 0.4 changed `tools` structure
- Server worked perfectly on Friday
- Monday: All tool calls failed with cryptic errors
- Anthropic docs: "We simplified the schema!"
- My perfectly working implementation: Broken

**The Recovery:**
- 6 hours rewriting tool definitions
- Updated SDK dependencies
- Rewrote 88 tests
- Added version checking middleware
- Now: Server checks MCP protocol version on startup

**Lesson learned**: Pin your dependencies when working with beta protocols. Check breaking change logs religiously.

## Unexpected Discoveries

### The Web UI Nobody Asked For

"Quick" debugging interface → Full React application:

```bash
cd web && ./start.sh
# Full standards browser at localhost:3000
# Real-time WebSocket updates
# Rule testing playground
```

**What Started as a 2-Hour Debug Tool:**
- Interactive standards browser with search
- Real-time [WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) updates when standards change
- Rule testing playground with live validation
- Syntax highlighting for code examples
- Mobile-responsive design (because of course)
- Dark mode toggle (essential)
- 50+ components, 3,000 lines of [React](https://react.dev/reference/react/hooks)

**The Irony**: I use this more than the CLI now. Sometimes procrastination produces useful things.

### Performance Benchmarking Addiction

Built tools to prove server speed. Discovered it was slow. Spent a week optimizing. Now: graphs!

```bash
python benchmarks/run_benchmarks.py
# Standard retrieval: 12ms average
# Semantic search: 89ms average
# Rule evaluation: 3ms average
```

**Optimization Journey:**
- Initial measurements: 340ms average retrieval (embarrassing)
- Profiled with cProfile: 85% time in JSON parsing
- Added [msgpack serialization](https://msgpack.org): 180ms (47% faster)
- Implemented response caching: 45ms (75% faster)
- Final optimization: Lazy-load standard details: 12ms (96% faster)
- Time invested: 1 week
- Users who care about 12ms vs 45ms: 0 (only me)

**The Graphs**: Created dashboards tracking latency percentiles, cache hit rates, memory usage over time. Nobody asked for these metrics. But they're pretty.

## Current State: "It Works on My Machine"

The honest status:

✅ **What's Working:**
- MCP server starts and serves standards
- 25 standards available and searchable
- CLI works (mostly)
- Tests pass (when Redis is running)
- Web UI loads (in Chrome)

⚠️ **What's Flaky:**
- Redis randomly disconnects
- Web UI websocket reconnection
- Performance under load (untested with >1 user)
- The documentation

❌ **What's Broken:**
- Windows support (WSL2 or suffer)
- The release automation I spent 3 days on
- My sleep schedule

## Lessons Learned (So Far)

### Start Smaller Than You Think

**The Evolution:**
- Week 1: "Simple wrapper" (200 lines, 1 file)
- Week 2: Added caching (1,200 lines, 8 files)
- Week 3: Added vector search (3,800 lines, 23 files, 4GB RAM)
- Week 4: Added web UI (6,000+ lines, 47 components)

**What I Should Have Done:**
- Ship Version 1
- Get feedback
- Add features based on actual needs, not hypothetical ones
- Iterate based on real usage

**The Reality**: Built for an audience of one (me). Over-engineered for problems I don't have.

### Perfect Is the Enemy of Deployed

**Version Comparison:**
- **Version 1**: 200 lines, works, deployed, useful
- **Version 2**: 1,200 lines, faster caching, zero users noticed
- **Version 3**: 3,800 lines, semantic search, solves no real problems
- **Version 4**: 6,000 lines, full UI, impressive demos, occasional Redis crashes

**Value Added Per Version:**
- V1 → V2: Marginal (caching saves 50ms on repeated queries)
- V2 → V3: Negative (added complexity, solved nothing)
- V3 → V4: Mixed (UI is useful, but could have been separate project)

**Lesson**: Should have shipped V1 three weeks ago. Iterated based on real feedback.

### Tools Shape Solutions

**The Pattern I Fell Into:**
- Had Redis → Added caching to everything
- Had ChromaDB → Added vector search everywhere
- Had React experience → Built unnecessary UI
- Had time → Spent it adding features instead of shipping

**Tools That Influenced Architecture:**
- Redis: L1/L2 cache architecture (for 25 files)
- ChromaDB: Semantic search (for text searchable by grep)
- React: Full web UI (for debugging tool)
- [Python async](https://docs.python.org/3/library/asyncio.html): Everything became async (unnecessary complexity)

**The Trap**: "I have this hammer, so everything looks like a nail." Technology-driven architecture instead of problem-driven. Classic [scope creep](https://www.pmi.org/learning/library/top-five-causes-scope-creep-6675) in action.

## What's Next (The Roadmap I'll Probably Ignore)

**The Realistic List:**
- Fix the Redis connection issues (week 5 of saying this)
- Write actual documentation
- Add integration tests that test integration
- Simplify the architecture (ha!)

**The Dream List:**
- VS Code extension
- Direct Claude Desktop integration  
- Distributed standards federation
- GraphQL API

## Try It Yourself (At Your Own Risk)

If you're brave enough to try this server, you might also want to explore my simpler (and more practical) approach to [supercharging Claude CLI with standards](/posts/2025-07-22-supercharging-claude-cli-with-standards) that doesn't require Redis or ChromaDB:

**AI skepticism note:** MCP is bleeding-edge technology from Anthropic. The spec changes. The libraries break. The examples in the docs don't always work. Building production systems on top of experimental protocols is a recipe for midnight debugging sessions.

```bash
# The optimistic quick start
pip install mcp-standards-server
mcp-standards serve --stdio

# The realistic setup
git clone [https://github.com/williamzujkowski/mcp-standards-server.git](https://github.com/williamzujkowski/mcp-standards-server.git)
cd mcp-standards-server
python -m venv venv && source venv/bin/activate
pip install -e .
# Fix 17 dependency conflicts
# Install Redis
# Sacrifice a keyboard to the demo gods
python -m src
```

Fair warning: This is a work in progress. It works, but "works" is doing some heavy lifting here.

## The Real Talk

This project taught me something important: The gap between "working prototype" and "production ready" is vast. My standards repository was immediately useful. This MCP server is technically superior and practically inferior. It's harder to install, easier to break, and solves problems that don't exist.

**The honest assessment:** This is over-engineering as a learning exercise. The first version (200 lines) worked fine. The current version (6,000+ lines) is more impressive and less useful. Sometimes the best code is the code you don't write.

But I learned a ton:
- How MCP works (and doesn't)
- Redis patterns I'll never use again
- Why simple solutions often win
- That scope creep is my superpower and weakness

Will I keep working on it? Absolutely. Will it ever be "done"? Absolutely not.

That's the beauty of side projects – they're never finished, only in various states of "good enough for now."

## The Bottom Line

Building an MCP server for my standards was like using a sledgehammer to hang a picture. It works, the picture is hung, but there's also a hole in the wall and my neighbors are asking questions.

But hey, it's MY hole in the wall, and I learned how to use a sledgehammer. I tested every feature, broke things multiple times, and rebuilt them better each iteration.

Sometimes that's enough.

---

*Want to contribute? The code is at [github.com/williamzujkowski/mcp-standards-server](https://github.com/williamzujkowski/mcp-standards-server). Issues and PRs welcome. Especially if you know why Redis keeps disconnecting.*

*Or use the original standards repo. It still works great and doesn't require Redis.*