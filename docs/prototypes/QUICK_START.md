# Optimization Prototypes: Quick Start Guide

**For**: Developers and LLMs
**Purpose**: Get started with optimization prototypes in 5 minutes

## TL;DR

Run all analyses and generate reports:

```bash
# 1. MANIFEST.json optimization
uv run python3 scripts/utilities/manifest-optimizer.py --compare

# 2. Context loading analysis
uv run python3 scripts/utilities/context-loader.py --coverage

# 3. Script consolidation
uv run python3 scripts/utilities/script-consolidator.py --plan

# 4. Comprehensive benchmarks
uv run python3 scripts/utilities/optimization-benchmark.py --all

# 5. Start token monitoring
uv run python3 scripts/utilities/token-usage-monitor.py --start-session my-session
```

All reports generated in `docs/prototypes/*/`

---

## 1. MANIFEST.json Optimizer

**What it does**: Analyzes current MANIFEST.json and proposes optimized structure

### Quick Commands

```bash
# Analyze current structure
uv run python3 scripts/utilities/manifest-optimizer.py --analyze

# Generate optimized version + comparison report
uv run python3 scripts/utilities/manifest-optimizer.py --compare --optimize

# Custom output directory
uv run python3 scripts/utilities/manifest-optimizer.py --all --output-dir /path/to/output
```

### Expected Output

```
=== MANIFEST ANALYSIS ===
Total tokens: 29,588
Total files: 593

Optimization targets:
  - inventory (86.8%)

✓ Comparison report: docs/prototypes/manifest-optimization/optimization-analysis.md
```

### What You Get

- **Analysis**: Current token usage breakdown
- **Optimized MANIFEST**: 99% token reduction prototype
- **Comparison report**: Before/after analysis
- **Migration plan**: Step-by-step implementation guide

**Use case**: Understanding MANIFEST.json overhead

---

## 2. Context Loader

**What it does**: Shows which context modules to load for different tasks

### Quick Commands

```bash
# See all task patterns
uv run python3 scripts/utilities/context-loader.py --coverage

# Analyze specific task
uv run python3 scripts/utilities/context-loader.py --task blog-writing

# Generate loading script
uv run python3 scripts/utilities/context-loader.py --task blog-writing --generate-script

# Interactive mode (best for exploration)
uv run python3 scripts/utilities/context-loader.py --interactive
```

### Expected Output

```
=== TASK COVERAGE ANALYSIS ===

blog-writing:
  Required tags: blog, nda, humanization
  Matching modules: 4
  Coverage score: 133.3%
  Token budget: 15,000
```

### What You Get

- **Task patterns**: 8 common task types
- **Module recommendations**: Which modules to load
- **Token budgets**: Expected token usage per task
- **Loading scripts**: Executable bash scripts for optimal loading

**Use case**: Optimizing context loading for specific operations

---

## 3. Script Consolidator

**What it does**: Identifies duplicate functionality across scripts

### Quick Commands

```bash
# Analyze duplication
uv run python3 scripts/utilities/script-consolidator.py --analyze

# Generate consolidation plan
uv run python3 scripts/utilities/script-consolidator.py --plan

# Create example consolidated scripts
uv run python3 scripts/utilities/script-consolidator.py --consolidate
```

### Expected Output

```
=== SCRIPT ANALYSIS ===

Total scripts: 60
Total lines: 24,626

Consolidation opportunities: 3

  [HIGH] link-validator-unified
    Scripts: 7
    Line reduction: 2,180
```

### What You Get

- **Duplication analysis**: Where code is duplicated
- **Consolidation plan**: Detailed migration roadmap
- **Example scripts**: Working prototypes of consolidated scripts
- **Impact estimate**: Line reduction and maintenance improvements

**Use case**: Reducing script maintenance burden

---

## 4. Token Usage Monitor

**What it does**: Tracks token usage in real-time with recommendations

### Quick Commands

```bash
# Start session
uv run python3 scripts/utilities/token-usage-monitor.py --start-session blog-post-1

# Log operation (during session)
uv run python3 scripts/utilities/token-usage-monitor.py \
  --log "read MANIFEST.json" \
  --tokens 2500 \
  --session blog-post-1

# End session (generates report)
uv run python3 scripts/utilities/token-usage-monitor.py --end-session blog-post-1

# Get recommendations
uv run python3 scripts/utilities/token-usage-monitor.py --recommend
```

### Example Session

```bash
# 1. Start
uv run python3 scripts/utilities/token-usage-monitor.py --start-session demo

# 2. Log some operations
uv run python3 scripts/utilities/token-usage-monitor.py --log "read MANIFEST.json" --tokens 29588 --session demo
uv run python3 scripts/utilities/token-usage-monitor.py --log "read CLAUDE.md" --tokens 7372 --session demo
uv run python3 scripts/utilities/token-usage-monitor.py --log "write blog post" --tokens 5000 --session demo

# 3. End session
uv run python3 scripts/utilities/token-usage-monitor.py --end-session demo

# 4. View recommendations
uv run python3 scripts/utilities/token-usage-monitor.py --recommend
```

### What You Get

- **Session reports**: Detailed breakdown of token usage
- **Historical analysis**: Trends over time
- **Automatic recommendations**: What to optimize next
- **Category breakdown**: Where tokens are being spent

**Use case**: Understanding where tokens are being used

---

## 5. Optimization Benchmark

**What it does**: Comprehensive before/after comparison of all optimizations

### Quick Commands

```bash
# Run all benchmarks
uv run python3 scripts/utilities/optimization-benchmark.py --all

# Run specific benchmark
uv run python3 scripts/utilities/optimization-benchmark.py --benchmark manifest

# Just generate report
uv run python3 scripts/utilities/optimization-benchmark.py --report
```

### Expected Output

```
=== RUNNING ALL BENCHMARKS ===

✓ manifest_optimization
✓ context_loading
✓ script_consolidation
✓ token_monitoring

✓ Report: docs/prototypes/benchmarks/optimization-comparison-report.md
```

### What You Get

- **Comprehensive comparison**: All 4 optimizations analyzed
- **ROI analysis**: Token savings, performance improvements
- **Implementation roadmap**: Phased rollout plan
- **Risk assessment**: Migration complexity and risks
- **Success metrics**: How to measure success

**Use case**: Understanding total optimization impact

---

## Common Workflows

### Workflow 1: "I want to understand token usage"

```bash
# 1. Run comprehensive benchmark
uv run python3 scripts/utilities/optimization-benchmark.py --all

# 2. Read the report
cat docs/prototypes/benchmarks/optimization-comparison-report.md

# 3. Start monitoring
uv run python3 scripts/utilities/token-usage-monitor.py --start-session baseline
```

**Time**: 5 minutes
**Output**: Complete understanding of optimization opportunities

### Workflow 2: "I want to optimize MANIFEST.json"

```bash
# 1. Analyze current state
uv run python3 scripts/utilities/manifest-optimizer.py --analyze

# 2. Generate optimized version
uv run python3 scripts/utilities/manifest-optimizer.py --optimize

# 3. Review comparison
cat docs/prototypes/manifest-optimization/optimization-analysis.md

# 4. Implement (follow migration steps in report)
```

**Time**: 15 minutes analysis + implementation
**Output**: 99% token reduction plan

### Workflow 3: "I want to reduce script duplication"

```bash
# 1. Analyze duplication
uv run python3 scripts/utilities/script-consolidator.py --analyze

# 2. Generate plan
uv run python3 scripts/utilities/script-consolidator.py --plan

# 3. Create example consolidated scripts
uv run python3 scripts/utilities/script-consolidator.py --consolidate

# 4. Review plan
cat docs/prototypes/script-consolidation/consolidation-plan.md
```

**Time**: 10 minutes analysis + phased implementation
**Output**: 21.8% line reduction plan

### Workflow 4: "I want to optimize context loading for a task"

```bash
# 1. See all tasks
uv run python3 scripts/utilities/context-loader.py --coverage

# 2. Analyze specific task
uv run python3 scripts/utilities/context-loader.py --task blog-writing

# 3. Generate loading script
uv run python3 scripts/utilities/context-loader.py --task blog-writing --generate-script

# 4. Use the loading script
bash docs/prototypes/context-loading/load-blog-writing.sh
```

**Time**: 2 minutes
**Output**: Optimal module loading for task

---

## Output Locations

All prototypes generate output in organized directories:

```
docs/prototypes/
├── manifest-optimization/
│   ├── optimization-analysis.md           # Comparison report
│   ├── MANIFEST.optimized.json            # Optimized manifest
│   └── docs/manifests/                    # Lazy-loaded metadata
├── context-loading/
│   └── load-{task}.sh                     # Loading scripts
├── script-consolidation/
│   ├── consolidation-plan.md              # Migration plan
│   └── {consolidated-script}.py           # Example scripts
├── benchmarks/
│   ├── optimization-comparison-report.md  # Full comparison
│   └── benchmark-results.json             # Raw data
├── PROTOTYPE_SUMMARY.md                   # This summary
└── QUICK_START.md                         # This guide

docs/metrics/
└── token-usage/
    ├── sessions.json                      # Monitoring sessions
    ├── usage-log.jsonl                    # Operation log
    └── session-{id}.md                    # Session reports
```

---

## Tips & Tricks

### For LLMs

1. **Start with benchmarks**: Run `optimization-benchmark.py --all` to get the big picture
2. **Use interactive mode**: `context-loader.py --interactive` for exploration
3. **Monitor sessions**: Wrap operations in monitoring sessions to track token usage
4. **Read reports**: Generated markdown reports are human-readable and comprehensive

### For Developers

1. **Run all analyses**: Execute all 5 commands in TL;DR to get complete picture
2. **Review reports**: All generated reports are in `docs/prototypes/`
3. **Low-hanging fruit**: Start with token monitoring (zero risk)
4. **Phased approach**: Implement optimizations incrementally

### Troubleshooting

**Problem**: Script fails to run
```bash
# Ensure UV is installed and up to date
uv --version

# Sync dependencies
uv sync
```

**Problem**: Output directory doesn't exist
```bash
# All scripts create directories automatically, but you can specify:
--output-dir /path/to/custom/output
```

**Problem**: Can't find generated reports
```bash
# All reports are in docs/prototypes/{category}/
ls -R docs/prototypes/
```

---

## Next Steps

After running prototypes:

1. **Review reports**: Read generated markdown files in `docs/prototypes/`
2. **Validate findings**: Check if estimates match your experience
3. **Plan implementation**: Use phased rollout in benchmark report
4. **Start monitoring**: Deploy token monitoring first (zero risk)
5. **Iterate**: Use monitoring data to refine optimizations

---

## Performance Expectations

### MANIFEST.json Optimizer
- **Runtime**: <5 seconds
- **Output size**: ~50 KB (report + optimized files)
- **Memory**: Minimal

### Context Loader
- **Runtime**: <2 seconds
- **Output size**: ~20 KB per task
- **Memory**: Minimal

### Script Consolidator
- **Runtime**: ~10 seconds (60 scripts)
- **Output size**: ~100 KB (plan + examples)
- **Memory**: Low

### Token Monitor
- **Runtime**: <1 second per operation
- **Storage**: ~1 KB per operation logged
- **Memory**: Minimal

### Optimization Benchmark
- **Runtime**: <5 seconds
- **Output size**: ~200 KB (all reports)
- **Memory**: Minimal

All prototypes are lightweight and fast.

---

## Support

For questions or issues:

1. **Read reports**: Most questions answered in generated reports
2. **Check PROTOTYPE_SUMMARY.md**: Comprehensive overview
3. **Run with --help**: All scripts have detailed help
4. **Review source**: Scripts are heavily documented

**All prototypes are in**: `scripts/utilities/optimization-*.py`

---

**Last updated**: 2025-11-01
**Status**: Production-ready prototypes
