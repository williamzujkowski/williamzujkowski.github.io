#!/usr/bin/env python3
"""
SCRIPT: scripts/blog-audit/batch.py
PURPOSE: Run the static portion of blog-pre-publish across many posts at once.
CATEGORY: blog_audit
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2026-05-09

DESCRIPTION:
    Mechanical companion to the interactive `blog-pre-publish` Skill. Runs the
    two static audits — blog-overlap and blog-llm-tells — across every post
    matching a glob, in seconds. Skips factcheck (needs network), nda-check
    and argument-shape (need LLM judgment).

    Use this for:
    - bulk pre-publish dry runs across the archive
    - regression testing after refining a skill's thresholds
    - generating per-post finding counts for a CI report

    For the full five-skill audit on a single post, invoke the
    `blog-pre-publish` Skill.

USAGE:
    # Audit every post matching the default glob (src/posts/*.md):
    python3 scripts/blog-audit/batch.py

    # Audit a specific year:
    python3 scripts/blog-audit/batch.py --glob 'src/posts/2026-*.md'

    # Audit a single post:
    python3 scripts/blog-audit/batch.py --glob 'src/posts/2026-05-07-*.md'

    # JSON output for CI consumption:
    python3 scripts/blog-audit/batch.py --json > audit.json

THRESHOLDS:
    Calibrated to this blog's empirical voice (TTR 0.41–0.52 across 13 posts,
    mean ~0.46). See ~/.claude/skills/blog-llm-tells/SKILL.md for the full
    threshold rationale.
"""

import argparse, json, re, statistics, sys
from pathlib import Path
from collections import defaultdict


REPO = Path(__file__).resolve().parent.parent.parent
DEFAULT_GLOB = "src/posts/*.md"

STOPWORDS = set("the a an of to in is are was were and or but that this it on at "
                "for with as be by from has have not how what when where why".split())

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

ABBR = ["mr.", "dr.", "e.g.", "i.e.", "vs.", "etc.", "v.", "fig.", "no.",
        "ph.d.", "u.s.", "u.k."]

REGISTRIES = ("npm", "pypi", "rubygems", "cargo", "crates.io", "maven", "nuget",
              "pip ", "go module")

# This-blog-calibrated TTR thresholds (default for src/posts/)
TTR_THRESH_BLOG = (0.50, 0.45, 0.40, 0.35)  # rich, ok, thin (LOW), very-thin (MED), HIGH


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}, text, 0
    fm = {}
    for line in m.group(1).split("\n"):
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"').strip("'")
    tag_match = re.search(r"^tags:\s*\[(.*?)\]", m.group(1), re.MULTILINE)
    if tag_match:
        fm["tags"] = [t.strip().strip('"').strip("'") for t in tag_match.group(1).split(",")]
    fm_end = text[:m.end()].count("\n") + 1
    return fm, text[m.end():], fm_end


def strip_code(s):
    s = re.sub(r"```.*?```", " ", s, flags=re.DOTALL)
    return re.sub(r"`[^`\n]+`", " ", s)


def is_npm_ecosystem(line, match_pos, match_len):
    """True if 'ecosystem' match is in a registry context (npm, pypi, etc.)."""
    before = line[max(0, match_pos - 30):match_pos].lower()
    after = line[match_pos + match_len:match_pos + match_len + 30].lower()
    return any(reg in before or reg in after for reg in REGISTRIES)


def split_sentences(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"(\d)\.(\d)", r"\1<DOT>\2", text)
    for ab in ABBR:
        text = re.sub(re.escape(ab), ab.replace(".", "<DOT>"), text, flags=re.IGNORECASE)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"\(\*\-\#])", text)
    return [p.replace("<DOT>", ".").strip() for p in parts if p.strip()]


def classify_bold(line):
    """Return list of 'structural' or 'scattered' for each bold span on the line."""
    rs = line.strip()
    bolds = list(re.finditer(r"\*\*[^*\n]+\*\*", line))
    out = []
    for b in bolds:
        # bullet-list lead-in
        if rs.startswith(("-", "*")) and b.start() <= 4:
            out.append("structural")
            continue
        # numbered-list lead-in
        if re.match(r"^\d+\.\s+", rs) and b.start() <= 6:
            out.append("structural")
            continue
        # standalone bold line (subsection header or thesis pivot)
        if re.match(r"^\*\*[^*]+\*\*[:\s]*$", rs):
            out.append("structural")
            continue
        # paragraph-leading bold
        if b.start() == 0 and "." in line[b.end():b.end() + 2]:
            out.append("structural")
            continue
        out.append("scattered")
    return out


def overlap_signals(text, fm):
    sigs = defaultdict(int)
    for t in (fm.get("tags") or []):
        sigs[t.lower()] += 3
    for w in re.findall(r"\b[A-Za-z][a-zA-Z-]{2,}\b", fm.get("title", "")):
        if w.lower() not in STOPWORDS:
            sigs[w.lower()] += 3
    for h2 in re.findall(r"^##\s+(.+)$", text, re.MULTILINE):
        for w in re.findall(r"\b[A-Za-z][a-zA-Z-]{2,}\b", h2):
            if w.lower() not in STOPWORDS:
                sigs[w.lower()] += 2
    for m in re.finditer(r"\b([A-Z][a-z]+(?:[\s_-][A-Z][a-z]+){0,3})\b", text):
        ent = m.group(1).lower()
        if ent not in STOPWORDS and len(ent) > 4:
            sigs[ent] += 2
    for m in re.finditer(r"`([^`\n]{4,40})`", text):
        sigs[m.group(1).lower().strip()] += 1
    return sigs


def jaccard_weighted(a, b):
    inter = sum(min(a[k], b[k]) for k in set(a) & set(b))
    union = sum(max(a.get(k, 0), b.get(k, 0)) for k in set(a) | set(b))
    return inter / union if union else 0


def audit_post(post_path, all_signals):
    text = post_path.read_text()
    fm, body, fm_end = parse_frontmatter(text)
    lines = text.split("\n")
    body_lines = lines[fm_end:]

    bib_idx = next((i for i, line in enumerate(body_lines)
                    if "Sources used in this post" in line or "## References" in line), None)
    if bib_idx is not None:
        body_lines = body_lines[:bib_idx]
    body = "\n".join(body_lines)
    body_no_code = strip_code(body)

    # Sentence-length variance (burstiness)
    sentences = split_sentences(body_no_code)
    sentence_lens = [len(re.findall(r"\b\w+\b", s)) for s in sentences
                     if len(re.findall(r"\b\w+\b", s)) > 0]
    sd_sl = statistics.stdev(sentence_lens) if len(sentence_lens) > 1 else 0

    words = [w.lower() for w in re.findall(r"\b[a-zA-Z]+\b", body_no_code)]
    total_w = len(words)

    if total_w <= 1500:
        ttr = len(set(words)) / total_w if total_w else 0
    else:
        ttrs = [len(set(words[s:s + 1000])) / 1000
                for s in range(0, total_w - 1000, 100)]
        ttr = statistics.mean(ttrs) if ttrs else 0

    # Banned words (with context exceptions)
    banned_hits = []
    for ln_idx, raw in enumerate(body_lines, fm_end + 1):
        if raw.strip().startswith(">"):
            continue
        line_no_code = strip_code(raw)
        for word in BANNED:
            for m in re.finditer(r"\b" + re.escape(word) + r"\b", line_no_code, re.IGNORECASE):
                if word == "ecosystem" and is_npm_ecosystem(line_no_code, m.start(), len(m.group(0))):
                    continue
                if word == "harness":
                    nearby = line_no_code[max(0, m.start() - 15):m.end() + 20].lower()
                    if any(t in nearby for t in ("test", "playwright", "pytest", "cypress",
                                                  "persona", "aegis", "qemu", "ovmf", "docker")):
                        continue
                if word == "navigate":
                    after = line_no_code[m.end():m.end() + 20]
                    if re.search(r"^\s+(to\s+)?[/~.]", after):
                        continue
                if word == "leverage":
                    after_words = line_no_code[m.end():m.end() + 40].split()[:4]
                    if any(re.match(r"^[A-Z][a-zA-Z]+", w) for w in after_words):
                        continue
                    if "`" in line_no_code[m.end():m.end() + 30]:
                        continue
                banned_hits.append((ln_idx, word))

    # Phrasal patterns (HIGH severity)
    phrasal_hits = []
    for ln_idx, raw in enumerate(body_lines, fm_end + 1):
        if raw.strip().startswith(">"):
            continue
        line_no_code = strip_code(raw)
        for pat, name in PHRASAL:
            for m in re.finditer(pat, line_no_code, re.IGNORECASE):
                phrasal_hits.append((ln_idx, name))

    # Em-dash count (raw — classification is for the SKILL.md author judgment)
    em_count = sum(len(re.findall(r"—", strip_code(raw))) for raw in body_lines)
    em_per_100 = em_count / (len(body_lines) / 100) if body_lines else 0

    # Bold density (scattered only, structural suppressed)
    structural_bolds = scattered_bolds = 0
    for raw in body_lines:
        cls = classify_bold(raw)
        structural_bolds += cls.count("structural")
        scattered_bolds += cls.count("scattered")
    scattered_per_100L = (scattered_bolds / len(body_lines) * 100) if body_lines else 0

    # Passive voice
    passive_re = re.compile(r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+\s+){0,2}(\w+ed|\w+en)\b",
                            re.IGNORECASE)
    passive_hits = total_clauses = 0
    for raw in body_lines:
        line_no_code = strip_code(raw)
        if not line_no_code.strip():
            continue
        total_clauses += len(re.split(r"[,;]", line_no_code))
        passive_hits += len(passive_re.findall(line_no_code))
    passive_pct = (passive_hits / total_clauses * 100) if total_clauses else 0

    trans_count = sum(len(re.findall(r"\b" + w + r"\b", body_no_code, re.IGNORECASE))
                      for w in TRANSITIONS)
    trans_per_100w = (trans_count / total_w * 100) if total_w else 0

    # Trailing-summary Jaccard
    title = fm.get("title", "")
    sw = set("the a an of to in is are was were and or but that this it on at for "
             "with as be by from has have not".split())

    def to_set(s):
        return set(w.lower() for w in re.findall(r"\b[a-zA-Z]{3,}\b", s)) - sw

    first_para = []
    for ln in body_lines:
        if ln.strip():
            first_para.append(ln)
            if sum(len(p.split()) for p in first_para) > 50:
                break
    last_para = []
    for ln in reversed(body_lines):
        if ln.strip():
            last_para.insert(0, ln)
            if len(last_para) > 4:
                break
    fset = to_set(title + " " + " ".join(first_para))
    lset = to_set(" ".join(last_para))
    jaccard = len(fset & lset) / len(fset | lset) if (fset | lset) else 0

    # Classify findings
    findings = {"H": [], "M": [], "L": []}
    for ln, name in phrasal_hits:
        findings["H"].append((name, ln))
    if jaccard > 0.4:
        findings["H"].append(("trailing-summary", f"jaccard={jaccard:.2f}"))
    for ln, word in banned_hits:
        findings["M"].append((f"banned:{word}", ln))
    if sd_sl < 4:
        findings["H"].append(("burstiness", f"SD={sd_sl:.1f}"))
    elif sd_sl < 6:
        findings["M"].append(("burstiness", f"SD={sd_sl:.1f}"))

    # TTR (this-blog calibrated thresholds)
    rich, ok, thin_low, very_thin = TTR_THRESH_BLOG
    if ttr < very_thin:
        findings["H"].append(("TTR", f"{ttr:.2f}"))
    elif ttr < thin_low:
        findings["M"].append(("TTR", f"{ttr:.2f}"))
    elif ttr < ok:
        findings["L"].append(("TTR", f"{ttr:.2f}"))

    if em_per_100 > 8:
        findings["L"].append(("em-dash-density", f"{em_per_100:.1f}/100L  (audit dramatic vs functional)"))
    if scattered_per_100L > 8:
        findings["M"].append(("scattered-bold", f"{scattered_bolds} bolds, {scattered_per_100L:.1f}/100L"))
    elif scattered_per_100L > 4:
        findings["L"].append(("scattered-bold", f"{scattered_bolds} bolds, {scattered_per_100L:.1f}/100L"))
    if passive_pct > 15:
        findings["M"].append(("passive", f"{passive_pct:.0f}%"))
    if trans_per_100w > 2.0:
        findings["M"].append(("transitions", f"{trans_per_100w:.2f}/100w"))

    # Overlap
    target_sigs = overlap_signals(body, fm)
    target_tags = set(fm.get("tags") or [])
    overlap_results = []
    for other_path, other_sigs, other_tags, other_text in all_signals:
        if other_path == post_path:
            continue
        score = jaccard_weighted(target_sigs, other_sigs)
        if len(target_tags & other_tags) >= 2:
            score += 0.10
        slug = other_path.stem
        linked = bool(re.search(rf"/posts/{re.escape(slug)}", text))
        if score >= 0.20:
            overlap_results.append((score, other_path.name, linked))
    overlap_results.sort(reverse=True)

    return {
        "name": post_path.name,
        "lines": len(body_lines),
        "words": total_w,
        "sentences": len(sentence_lens),
        "metrics": {
            "sd": round(sd_sl, 1),
            "ttr": round(ttr, 2),
            "em_per_100": round(em_per_100, 1),
            "structural_bolds": structural_bolds,
            "scattered_bolds": scattered_bolds,
            "scattered_per_100L": round(scattered_per_100L, 1),
            "passive_pct": round(passive_pct, 1),
            "trans_per_100w": round(trans_per_100w, 2),
            "trailing_jaccard": round(jaccard, 2),
        },
        "findings": findings,
        "overlap": [(round(s, 2), n, l) for s, n, l in overlap_results],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    ap.add_argument("--glob", default=DEFAULT_GLOB,
                    help=f"glob pattern relative to repo root (default: {DEFAULT_GLOB})")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of table")
    args = ap.parse_args()

    targets = sorted((REPO).glob(args.glob))
    if not targets:
        print(f"No posts matched {args.glob}", file=sys.stderr)
        sys.exit(1)

    # Build all-posts signals once (overlap needs them)
    all_signals = []
    for p in sorted((REPO / "src" / "posts").glob("*.md")):
        if not p.is_file() or p.name == "welcome.md":
            continue
        txt = p.read_text()
        fm, body, _ = parse_frontmatter(txt)
        all_signals.append((p, overlap_signals(body, fm),
                            set(fm.get("tags") or []), txt))

    results = [audit_post(t, all_signals) for t in targets]

    if args.json:
        print(json.dumps(results, indent=2))
        return

    print(f"\n{'POST':<70} {'W':>5} {'SD':>5} {'TTR':>5} {'EM':>5} {'BLD':>5} "
          f"{'H':>3} {'M':>3} {'L':>3} {'OVL':>3}")
    print("=" * 120)
    for r in results:
        H, M, L = len(r["findings"]["H"]), len(r["findings"]["M"]), len(r["findings"]["L"])
        OVL = sum(1 for s, _, linked in r["overlap"] if not linked)
        m = r["metrics"]
        print(f"{r['name'][:67]:<70} {r['words']:>5} {m['sd']:>5} {m['ttr']:>5} "
              f"{m['em_per_100']:>5} {m['scattered_per_100L']:>5} "
              f"{H:>3} {M:>3} {L:>3} {OVL:>3}")

    print("\n=== Per-post HIGH/MED findings ===")
    any_findings = False
    for r in results:
        if r["findings"]["H"] or r["findings"]["M"] or any(not l for _, _, l in r["overlap"]):
            any_findings = True
            print(f"\n{r['name']}:")
            for name, line in r["findings"]["H"]:
                print(f"  HIGH  {name}  {line}")
            for name, line in r["findings"]["M"]:
                print(f"  MED   {name}  {line}")
            for s, n, linked in r["overlap"]:
                if not linked:
                    tier = "STRONG" if s >= 0.40 else "MODERATE"
                    print(f"  OVERLAP {tier}  {s:.2f}  {n}  (NOT LINKED)")
    if not any_findings:
        print("Clean across all audited posts.")


if __name__ == "__main__":
    main()
