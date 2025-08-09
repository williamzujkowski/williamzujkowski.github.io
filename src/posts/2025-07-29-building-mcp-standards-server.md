---
title: 'Down the MCP Rabbit Hole: Building a Standards Server'
date: 2025-07-29
tags:
- ai
- mcp
- development
- open-source
description: 'The ongoing saga of turning my standards repository into an MCP server.
  Spoiler: It''s working, mostly, and I''ve only rewritten it three times.'
---
## When Good Ideas Get Complicated

Remember last week when I was all excited about my standards repository? Well, I made the classic developer mistake: "You know what would make this better? If I rebuilt it from scratch with a completely different architecture!"

Enter the Model Context Protocol (MCP) – Anthropic's new way for LLMs to interact with external tools. The idea was simple: instead of copying CLAUDE.md into every project, why not serve the standards directly to Claude through MCP?

Three weeks and several rewrites later, I have [github.com/williamzujkowski/mcp-standards-server](https://github.com/williamzujkowski/mcp-standards-server). It works! Mostly. When Redis is happy. And the moon is in the right phase.

## The Original Vision vs Reality

### What I Planned (Week 1)

"I'll just wrap my standards in an MCP server. How hard could it be?"

```python
# My naive first attempt
class StandardsServer:
    def __init__(self):
        self.standards = load_standards()  # Easy!
    
    def get_standard(self, name):
        return self.standards[name]  # Done!
```

### What Actually Happened (Week 3)

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
Started with stdio communication. Just pipe standards in and out. Clean, simple, working.

Then I thought: "But what about caching?"

### Version 2: "Add Some Redis"
Added Redis for caching. Now I had two problems: cache invalidation and Redis connection management.

Then I thought: "But what about semantic search?"

### Version 3: "ChromaDB Will Fix Everything"
Added ChromaDB for vector search. Now I had three problems: embeddings, vector storage, and "why is my laptop fan screaming?"

Then I thought: "But what about multi-language support?"

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

The rule engine is actually pretty clever:

```python
context = {
    "project_type": "web_application",
    "framework": "react",
    "requirements": ["accessibility", "performance"]
}

# Automatically loads: react-18-patterns, wcag-2.1, performance-optimization
standards = engine.evaluate(context)
```

No more manual standard selection. The system figures out what you need based on your project context.

### Multi-Language Code Analysis

This turned out surprisingly useful:

```bash
mcp-standards validate src/ --language auto
# Detects Python, finds 3 PEP-8 violations
# Detects JavaScript, suggests ES6 improvements
# Generates fix patches automatically
```

### Token Optimization That Actually Matters

Compressed formats that reduce token usage by 70-90%:

```python
# Full standard: 5000 tokens
# Compressed: 500 tokens
# Reference only: 50 tokens

standard = get_standard("react-patterns", format="compressed")
```

## The Struggles (Learning Moments)

### Redis Is Not Your Friend at 3 AM

Spent two days debugging why standards weren't caching. Turns out Redis was silently failing because I exceeded memory limits. My "temporary" cache was storing everything forever.

**Lesson learned**: TTLs exist for a reason. Use them.

### Vector Databases Are Hungry

ChromaDB ate 4GB of RAM just to index my standards. For 25 documents. That's 160MB per document for... searching text.

**Lesson learned**: Sometimes grep is enough. Not everything needs AI.

### The MCP Protocol Is Still Evolving

Halfway through development, the MCP spec changed. My perfectly working server suddenly wasn't.

**Lesson learned**: Pin your dependencies when working with beta protocols.

## Unexpected Discoveries

### The Web UI Nobody Asked For

Started building a "quick" debugging interface. Ended up with a full React app:

```bash
cd web && ./start.sh
# Full standards browser at localhost:3000
# Real-time WebSocket updates
# Rule testing playground
```

I use it more than the CLI now. Sometimes procrastination produces useful things.

### Performance Benchmarking Addiction

Built benchmarking tools to prove my server was fast. Discovered it wasn't. Spent a week optimizing. Now I have graphs!

```bash
python benchmarks/run_benchmarks.py
# Standard retrieval: 12ms average
# Semantic search: 89ms average  
# Rule evaluation: 3ms average
```

Nobody asked for these metrics. But they're pretty.

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

My "simple wrapper" became a distributed system with caching, vector search, and web UI. Next time: actually keep it simple.

### Perfect Is the Enemy of Deployed

Version 1 worked fine. Versions 2-4 added complexity for marginal gains. Should have shipped v1 and iterated.

### Tools Shape Solutions

Having Redis available made me add caching everywhere. Having ChromaDB made me add semantic search to everything. Just because you can doesn't mean you should.

## What's Next (The Roadmap I'll Probably Ignore)

**The Realistic List:**
- Fix the Redis connection issues (week 5 of saying this)
- Write actual documentation
- Add integration tests that actually test integration
- Simplify the architecture (ha!)

**The Dream List:**
- VS Code extension
- Direct Claude Desktop integration  
- Distributed standards federation
- GraphQL API

## Try It Yourself (At Your Own Risk)

If you're brave enough:

```bash
# The optimistic quick start
pip install mcp-standards-server
mcp-standards serve --stdio

# The realistic setup
git clone https://github.com/williamzujkowski/mcp-standards-server.git
cd mcp-standards-server
python -m venv venv && source venv/bin/activate
pip install -e .
# Fix 17 dependency conflicts
# Install Redis
# Sacrifice a keyboard to the demo gods
python -m src
```

Fair warning: This is very much a work in progress. It works, but "works" is doing some heavy lifting here.

## The Real Talk

This project taught me something important: The gap between "working prototype" and "production ready" is vast. My standards repository was immediately useful. This MCP server is technically superior but practically inferior – it's harder to install, easier to break, and solves problems that might not exist.

But I learned a ton:
- How MCP actually works (and doesn't)
- Redis patterns I'll never use again
- Why simple solutions often win
- That scope creep is my superpower and weakness

Will I keep working on it? Absolutely. Will it ever be "done"? Absolutely not.

That's the beauty of side projects – they're never finished, just in various states of "good enough for now."

## The Bottom Line

Building an MCP server for my standards was like using a sledgehammer to hang a picture. It works, the picture is hung, but there's also a hole in the wall and my neighbors are asking questions.

But hey, it's MY hole in the wall, and I learned how to use a sledgehammer.

Sometimes that's enough.

---

*Want to contribute? The code is at [github.com/williamzujkowski/mcp-standards-server](https://github.com/williamzujkowski/mcp-standards-server). Issues and PRs welcome. Especially if you know why Redis keeps disconnecting.*

*Or just use the original standards repo. It still works great and doesn't require Redis.*