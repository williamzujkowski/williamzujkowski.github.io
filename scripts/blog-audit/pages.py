#!/usr/bin/env python3
"""
SCRIPT: scripts/blog-audit/pages.py
PURPOSE: Voice scrub for non-post Astro pages (about, now, index, etc.).
CATEGORY: blog_audit
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2026-05-09

DESCRIPTION:
    Companion to scripts/blog-audit/batch.py for non-post pages.

    The blog has a handful of non-post pages (.astro files under
    astro-site/src/pages/) that have real prose: about, now, index, projects,
    uses, 404. They are subject to the same AGENTS.md voice rules as blog
    posts but have a different shape (JSX wrapper around prose) and a
    different threat model (the about page intentionally names the current
    employer; the now page is intentionally about current work).

    This script strips the JSX/Astro scaffolding to extract the prose, then
    runs the voice-only portion of the audit:

      - banned-word scan (with the same context exceptions as batch.py)
      - phrasal patterns ("It's not just X, it's Y", etc.)
      - em-dash density
      - scattered-bold density
      - passive voice
      - transition-word density

    SKIPPED (intentionally, because they don't apply):
      - NDA contextual check (about/now have intentional current-work attribution)
      - argument-shape (these aren't argumentative essays)
      - overlap (cross-page topic overlap isn't meaningful here)
      - TTR (these pages are too short for meaningful TTR; results would be noise)
      - factcheck (separate concern; do via the blog-factcheck Skill if needed)

USAGE:
    # Audit every .astro page (default):
    python3 scripts/blog-audit/pages.py

    # Audit a specific file:
    python3 scripts/blog-audit/pages.py --file astro-site/src/pages/about.astro

    # JSON output:
    python3 scripts/blog-audit/pages.py --json
"""

import argparse, json, re, statistics, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
DEFAULT_DIR = "astro-site/src/pages"

BANNED = ["delve", "leverage", "utilize", "navigate", "ecosystem", "landscape",
          "robust", "comprehensive", "seamless", "cutting-edge", "revolutionary",
          "game-changer", "furthermore", "moreover", "additionally", "indeed",
          "essentially", "fundamentally", "ultimately", "tapestry", "vibrant",
          "intricate", "myriad", "plethora", "multifaceted", "embark",
          "unleash", "empower", "harness", "elevate", "foster"]

PHRASAL = [
    (r"it'?s not just \w+,? it'?s \w+", "it's-not-just-X"),
    (r"not only \w+ but \w+", "not-only-but"),
    (r"in today'?s \w+ (world|landscape|era)", "in-today's-X"),
    (r"it'?s important to note that", "it's-important-to-note"),
    (r"in conclusion[,:]", "in-conclusion"),
]

TRANSITIONS = ["however", "therefore", "thus", "moreover", "furthermore",
               "additionally", "consequently", "nonetheless", "nevertheless"]

REGISTRIES = ("npm", "pypi", "rubygems", "cargo", "crates.io", "maven", "nuget",
              "pip ", "go module")


def strip_astro_to_prose(text):
    """Strip Astro/JSX scaffolding, return prose lines with original line numbers.

    Returns a list of (line_number, prose_text) tuples. Line numbers refer
    to positions in the ORIGINAL file so findings can be reported back at
    the location an editor would see.
    """
    lines = text.split("\n")

    # Skip the leading frontmatter import block (--- ... ---)
    fm_end = 0
    if lines and lines[0].strip() == "---":
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == "---":
                fm_end = i + 1
                break

    out = []
    in_code = False
    for i, raw in enumerate(lines[fm_end:], fm_end + 1):
        # Track fenced code blocks (rare in .astro but defensive)
        if raw.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue

        # Skip pure-import lines or pure-JSX-tag lines (no prose to audit)
        stripped = raw.strip()
        if not stripped:
            continue
        # Skip lines that are *only* tags / variable references
        # e.g.  <BaseLayout title="About">  or  </BaseLayout>  or  <h2>About</h2>
        # but KEEP lines that have text inside the tags

        # Strip Astro template expressions {...} that aren't prose
        line = re.sub(r"\{[^{}]*\}", "", raw)
        # Strip HTML/JSX comments
        line = re.sub(r"<!--.*?-->", "", line)
        line = re.sub(r"\{/\*.*?\*/\}", "", line)
        # Strip <script> and <style> blocks (rare inline; defensive)
        line = re.sub(r"<script[^>]*>.*?</script>", "", line, flags=re.DOTALL)
        line = re.sub(r"<style[^>]*>.*?</style>", "", line, flags=re.DOTALL)
        # Strip JSX tags but keep inner text. Preserve **bold** markers since
        # those are markdown-style bold inside the JSX.
        line = re.sub(r"<[^>]+>", "", line)
        # Collapse whitespace
        line = re.sub(r"\s+", " ", line).strip()

        if line and len(line) > 4:  # ignore very short residuals
            out.append((i, line))

    return out


def is_npm_ecosystem(line, match_pos, match_len):
    before = line[max(0, match_pos - 30):match_pos].lower()
    after = line[match_pos + match_len:match_pos + match_len + 30].lower()
    return any(reg in before or reg in after for reg in REGISTRIES)


def audit_page(page_path):
    text = page_path.read_text()
    prose_lines = strip_astro_to_prose(text)
    prose = "\n".join(p for _, p in prose_lines)
    words = [w.lower() for w in re.findall(r"\b[a-zA-Z]+\b", prose)]
    total_w = len(words)

    findings = {"H": [], "M": [], "L": []}

    # Banned words (with context exceptions)
    for ln_idx, line in prose_lines:
        for word in BANNED:
            for m in re.finditer(r"\b" + re.escape(word) + r"\b", line, re.IGNORECASE):
                if word == "ecosystem" and is_npm_ecosystem(line, m.start(), len(m.group(0))):
                    continue
                if word == "harness":
                    nearby = line[max(0, m.start() - 15):m.end() + 20].lower()
                    if any(t in nearby for t in ("test", "playwright", "pytest", "cypress",
                                                  "persona", "aegis", "qemu", "ovmf", "docker")):
                        continue
                if word == "navigate":
                    after = line[m.end():m.end() + 20]
                    if re.search(r"^\s+(to\s+)?[/~.]", after):
                        continue
                if word == "leverage":
                    after_words = line[m.end():m.end() + 40].split()[:4]
                    if any(re.match(r"^[A-Z][a-zA-Z]+", w) for w in after_words):
                        continue
                findings["M"].append((f"banned:{word}", ln_idx, line[:80]))

    # Phrasal patterns (HIGH severity)
    for ln_idx, line in prose_lines:
        for pat, name in PHRASAL:
            for m in re.finditer(pat, line, re.IGNORECASE):
                findings["H"].append((name, ln_idx, line[:80]))

    # Em-dash count (raw)
    em_count = sum(line.count("—") for _, line in prose_lines)
    em_per_100 = em_count / (len(prose_lines) / 100) if prose_lines else 0
    if em_per_100 > 8:
        findings["M"].append(("em-dash density", -1, f"{em_per_100:.1f}/100L ({em_count} total)"))
    elif em_per_100 > 4:
        findings["L"].append(("em-dash density", -1, f"{em_per_100:.1f}/100L ({em_count} total)"))

    # Bold density (markdown-style **...** that survived the JSX strip)
    bold_count = sum(len(re.findall(r"\*\*[^*\n]+\*\*", line)) for _, line in prose_lines)
    bold_per_100L = (bold_count / len(prose_lines) * 100) if prose_lines else 0
    if bold_per_100L > 8:
        findings["M"].append(("bold-density", -1, f"{bold_count} bolds, {bold_per_100L:.1f}/100L"))
    elif bold_per_100L > 4:
        findings["L"].append(("bold-density", -1, f"{bold_count} bolds, {bold_per_100L:.1f}/100L"))

    # Passive voice (rough)
    passive_re = re.compile(r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+\s+){0,2}(\w+ed|\w+en)\b",
                            re.IGNORECASE)
    passive_hits = total_clauses = 0
    for _, line in prose_lines:
        total_clauses += len(re.split(r"[,;]", line))
        passive_hits += len(passive_re.findall(line))
    passive_pct = (passive_hits / total_clauses * 100) if total_clauses else 0
    if passive_pct > 15:
        findings["M"].append(("passive", -1, f"{passive_pct:.0f}%"))
    elif passive_pct > 10:
        findings["L"].append(("passive", -1, f"{passive_pct:.0f}%"))

    # Transition density
    trans_count = sum(len(re.findall(r"\b" + w + r"\b", prose, re.IGNORECASE)) for w in TRANSITIONS)
    trans_per_100w = (trans_count / total_w * 100) if total_w else 0
    if trans_per_100w > 2.0:
        findings["M"].append(("transitions", -1, f"{trans_per_100w:.2f}/100w"))

    return {
        "name": page_path.relative_to(REPO).as_posix(),
        "prose_lines": len(prose_lines),
        "words": total_w,
        "metrics": {
            "em_per_100": round(em_per_100, 1),
            "bold_per_100L": round(bold_per_100L, 1),
            "passive_pct": round(passive_pct, 1),
            "trans_per_100w": round(trans_per_100w, 2),
        },
        "findings": findings,
    }


def main():
    ap = argparse.ArgumentParser(description="Voice scrub for non-post Astro pages.")
    ap.add_argument("--file", help="audit a single file (path relative to repo root)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.file:
        targets = [REPO / args.file]
    else:
        targets = sorted((REPO / DEFAULT_DIR).glob("*.astro"))

    if not targets:
        print("No .astro pages found.", file=sys.stderr)
        sys.exit(1)

    results = [audit_page(t) for t in targets]

    if args.json:
        print(json.dumps(results, indent=2))
        return

    print(f"\n{'PAGE':<45} {'WORDS':>5} {'EM':>5} {'BLD':>5} {'PASV':>5} "
          f"{'H':>3} {'M':>3} {'L':>3}")
    print("=" * 95)
    for r in results:
        H, M, L = len(r["findings"]["H"]), len(r["findings"]["M"]), len(r["findings"]["L"])
        m = r["metrics"]
        print(f"{r['name'][:42]:<45} {r['words']:>5} {m['em_per_100']:>5} "
              f"{m['bold_per_100L']:>5} {m['passive_pct']:>5} "
              f"{H:>3} {M:>3} {L:>3}")

    print("\n=== Per-page findings ===")
    any_findings = False
    for r in results:
        for sev_key, sev_label in (("H", "HIGH"), ("M", "MED"), ("L", "LOW")):
            for name, ln, detail in r["findings"][sev_key]:
                if not any_findings:
                    print()
                any_findings = True
                line_str = f"L{ln}" if ln > 0 else "—"
                print(f"  {sev_label:5} {r['name'][:42]:<45} {line_str:>5}  {name:25} {detail[:80]}")
    if not any_findings:
        print("Clean across all audited pages.")


if __name__ == "__main__":
    main()
