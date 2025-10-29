#!/usr/bin/env python3
"""
Portfolio-Wide Humanization Validation
Validates all blog posts and generates comprehensive assessment report.

Usage:
    python validate-all-posts.py --output docs/reports/
    python validate-all-posts.py --format json
    python validate-all-posts.py --threshold 75
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import argparse


def find_all_posts(posts_dir="src/posts"):
    """Find all markdown blog posts."""
    posts_path = Path(posts_dir)
    if not posts_path.exists():
        print(f"Error: Posts directory not found: {posts_dir}")
        sys.exit(1)

    posts = list(posts_path.glob("*.md"))
    # Exclude welcome.md if present
    posts = [p for p in posts if p.name != "welcome.md"]
    return sorted(posts)


def validate_post(post_path, validator_script="scripts/blog-content/humanization-validator.py"):
    """Run humanization validator on a single post."""
    try:
        result = subprocess.run(
            ["python", validator_script, "--post", str(post_path), "--output", "json"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Parse JSON output from stdout (validator now outputs to stdout for JSON)
        output = result.stdout if result.stdout else result.stderr

        # Extract JSON from output (may have ANSI codes)
        json_start = output.find("{")
        json_end = output.rfind("}") + 1

        if json_start >= 0 and json_end > json_start:
            json_str = output[json_start:json_end]
            data = json.loads(json_str)
            # Add post path to result
            data["post"] = str(post_path)
            data["status"] = "PASS" if data["score"] >= 75 else "FAIL"
            return data
        else:
            # Fallback: parse text output for score
            score_line = [line for line in output.split("\n") if "Score:" in line]
            if score_line:
                score_text = score_line[0].split("Score:")[1].strip()
                score = float(score_text.split("/")[0])
                status = "PASS" if "PASS" in score_text else "FAIL"
                return {
                    "post": str(post_path),
                    "score": score,
                    "status": status,
                    "violations": [],
                    "warnings": [],
                    "passed_checks": []
                }

            return None

    except subprocess.TimeoutExpired:
        print(f"Timeout validating {post_path}")
        return None
    except Exception as e:
        print(f"Error validating {post_path}: {e}")
        return None


def categorize_posts(results, threshold=75):
    """Categorize posts by score ranges."""
    categories = {
        "excellent": [],    # 90-100
        "good": [],         # 75-89
        "needs_improvement": [],  # 60-74
        "failing": []       # <60
    }

    for result in results:
        score = result["score"]
        if score >= 90:
            categories["excellent"].append(result)
        elif score >= threshold:
            categories["good"].append(result)
        elif score >= 60:
            categories["needs_improvement"].append(result)
        else:
            categories["failing"].append(result)

    return categories


def generate_markdown_report(results, categories, output_file="docs/reports/portfolio-assessment.md"):
    """Generate comprehensive Markdown report."""
    total = len(results)
    avg_score = sum(r["score"] for r in results) / total if total > 0 else 0

    # Sort by score (lowest first)
    sorted_results = sorted(results, key=lambda x: x["score"])
    bottom_10 = sorted_results[:10]
    top_10 = sorted_results[-10:]

    report = f"""# Portfolio-Wide Humanization Assessment

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Total Posts:** {total}
**Average Score:** {avg_score:.1f}/100
**Validation Threshold:** 75/100

---

## 📊 Executive Summary

### Score Distribution

| Category | Range | Count | Percentage |
|----------|-------|-------|------------|
| **Excellent** | 90-100 | {len(categories['excellent'])} | {len(categories['excellent'])/total*100:.1f}% |
| **Good** | 75-89 | {len(categories['good'])} | {len(categories['good'])/total*100:.1f}% |
| **Needs Improvement** | 60-74 | {len(categories['needs_improvement'])} | {len(categories['needs_improvement'])/total*100:.1f}% |
| **Failing** | <60 | {len(categories['failing'])} | {len(categories['failing'])/total*100:.1f}% |

### Key Insights

- **Passing Rate:** {(len(categories['excellent']) + len(categories['good']))/total*100:.1f}% ({len(categories['excellent']) + len(categories['good'])}/{total} posts ≥75)
- **Average Score:** {avg_score:.1f}/100
- **Range:** {sorted_results[0]['score']:.1f} - {sorted_results[-1]['score']:.1f}
- **Median:** {sorted_results[len(sorted_results)//2]['score']:.1f}/100

---

## 🎯 Bottom 10 Posts (Priority Targets for Batch 3)

| Rank | Post | Score | Status | Key Issues |
|------|------|-------|--------|------------|
"""

    for i, post in enumerate(bottom_10, 1):
        filename = Path(post["post"]).name
        violations = len(post.get("violations", []))
        status = post.get("status", "UNKNOWN")
        report += f"| {i} | `{filename}` | {post['score']:.1f}/100 | {status} | {violations} violations |\n"

    report += f"""
---

## ⭐ Top 10 Posts (Exemplary Quality)

| Rank | Post | Score | Status |
|------|------|-------|--------|
"""

    for i, post in enumerate(reversed(top_10), 1):
        filename = Path(post["post"]).name
        status = post.get("status", "UNKNOWN")
        report += f"| {i} | `{filename}` | {post['score']:.1f}/100 | {status} |\n"

    report += f"""
---

## 📈 All Posts (Sorted by Score)

| Post | Score | Status | Violations | Warnings |
|------|-------|--------|------------|----------|
"""

    for result in sorted_results:
        filename = Path(result["post"]).name
        violations = len(result.get("violations", []))
        warnings = len(result.get("warnings", []))
        status = result.get("status", "UNKNOWN")
        report += f"| `{filename}` | {result['score']:.1f}/100 | {status} | {violations} | {warnings} |\n"

    report += f"""
---

## 🚀 Recommended Actions

### Immediate (This Week)

**Batch 3 Refinement:** Target the bottom 10 posts identified above.

**Expected Improvements:**
- Current avg of bottom 10: {sum(p['score'] for p in bottom_10)/len(bottom_10):.1f}/100
- Target: All posts ≥80/100
- Estimated timeline: 2-3 days (using Batch 2 methodology)

### Medium-Term (Next 2 Weeks)

**Batch 4 Planning:** Address posts in "Needs Improvement" category (60-74 range).

### Long-Term (Next Month)

**Portfolio Maintenance:**
- Monthly validation runs
- Pre-commit hooks to prevent regression
- Continuous improvement of lowest-scoring posts

---

## 📋 Detailed Findings

### Common Violation Patterns

Based on bottom 10 analysis:

"""

    # Analyze common violations
    violation_types = defaultdict(int)
    for post in bottom_10:
        for v in post.get("violations", []):
            v_type = v.get("type", "unknown")
            violation_types[v_type] += 1

    if violation_types:
        report += "| Violation Type | Frequency |\n"
        report += "|----------------|------------|\n"
        for v_type, count in sorted(violation_types.items(), key=lambda x: x[1], reverse=True):
            report += f"| `{v_type}` | {count} |\n"
    else:
        report += "*No detailed violation data available.*\n"

    report += f"""
---

## 🎯 Success Metrics

**Current State:**
- Average Score: {avg_score:.1f}/100
- Passing Rate: {(len(categories['excellent']) + len(categories['good']))/total*100:.1f}%
- Posts ≥90: {len(categories['excellent'])}/{total}

**Target State (After Batch 3):**
- Average Score: ≥85/100
- Passing Rate: ≥80% (45+/56 posts)
- Bottom 10 improved to ≥80/100

---

*Generated by validate-all-posts.py*
*Next assessment: After Batch 3 completion*
"""

    # Write report
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        f.write(report)

    return output_file


def generate_json_output(results, categories, output_file="docs/reports/portfolio-assessment.json"):
    """Generate machine-readable JSON output."""
    total = len(results)
    avg_score = sum(r["score"] for r in results) / total if total > 0 else 0

    sorted_results = sorted(results, key=lambda x: x["score"])
    bottom_10 = [r["post"] for r in sorted_results[:10]]

    output = {
        "generated_at": datetime.now().isoformat(),
        "total_posts": total,
        "average_score": round(avg_score, 1),
        "score_distribution": {
            "excellent": len(categories["excellent"]),
            "good": len(categories["good"]),
            "needs_improvement": len(categories["needs_improvement"]),
            "failing": len(categories["failing"])
        },
        "bottom_10_posts": bottom_10,
        "all_results": results
    }

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)

    return output_file


def main():
    parser = argparse.ArgumentParser(description="Validate all blog posts for humanization quality")
    parser.add_argument("--output", default="docs/reports/", help="Output directory for reports")
    parser.add_argument("--format", choices=["markdown", "json", "both"], default="both", help="Output format")
    parser.add_argument("--threshold", type=int, default=75, help="Passing score threshold")
    parser.add_argument("--posts-dir", default="src/posts", help="Directory containing blog posts")

    args = parser.parse_args()

    print("🔍 Portfolio-Wide Humanization Assessment")
    print("=" * 60)

    # Find all posts
    posts = find_all_posts(args.posts_dir)
    print(f"\n📚 Found {len(posts)} blog posts")

    # Validate each post
    print("\n🧪 Validating posts...")
    results = []
    for i, post in enumerate(posts, 1):
        print(f"  [{i}/{len(posts)}] {post.name}...", end=" ")
        result = validate_post(post)
        if result:
            results.append(result)
            print(f"{result['score']:.1f}/100 - {result.get('status', 'UNKNOWN')}")
        else:
            print("SKIPPED (validation error)")

    if not results:
        print("\n❌ No valid results. Check validator script.")
        sys.exit(1)

    # Categorize
    categories = categorize_posts(results, args.threshold)

    # Generate reports
    print("\n📊 Generating reports...")

    if args.format in ["markdown", "both"]:
        md_file = generate_markdown_report(results, categories,
                                          os.path.join(args.output, "portfolio-assessment.md"))
        print(f"  ✅ Markdown report: {md_file}")

    if args.format in ["json", "both"]:
        json_file = generate_json_output(results, categories,
                                        os.path.join(args.output, "portfolio-assessment.json"))
        print(f"  ✅ JSON report: {json_file}")

    # Summary
    total = len(results)
    avg_score = sum(r["score"] for r in results) / total
    passing = len(categories["excellent"]) + len(categories["good"])

    print("\n" + "=" * 60)
    print("📈 ASSESSMENT COMPLETE")
    print("=" * 60)
    print(f"  Total Posts: {total}")
    print(f"  Average Score: {avg_score:.1f}/100")
    print(f"  Passing Rate: {passing/total*100:.1f}% ({passing}/{total} posts ≥{args.threshold})")
    print(f"  Bottom 10 Avg: {sum(r['score'] for r in sorted(results, key=lambda x: x['score'])[:10])/10:.1f}/100")
    print("=" * 60)

    # Exit code based on passing rate
    if passing / total >= 0.75:  # 75% passing rate
        sys.exit(0)
    else:
        print("\n⚠️  Warning: Less than 75% of posts meet threshold")
        sys.exit(1)


if __name__ == "__main__":
    main()
