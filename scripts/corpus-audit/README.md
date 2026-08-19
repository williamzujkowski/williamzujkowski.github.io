# Corpus audit scripts

Measurement code behind [Nobody Ran It](../../src/posts/2026-08-18-checks-that-pass-for-the-wrong-reason.md).
Both are here so the numbers in that post can be reproduced or refuted.

## `grim_check.py` — GRIM-style arithmetic check

Tests whether a stated percentage is reachable on its stated denominator.

```bash
python3 scripts/corpus-audit/grim_check.py 'src/posts/*.md'
```

**Result on this corpus: 10 tightly-bound pairs, 0 violations** — the same
before and after the 2026 audit. This is a negative result and the script is
kept as evidence for it.

Two earlier versions are described in the post and are *not* kept, because both
were wrong in instructive ways: a proximity heuristic that flagged 309 of 619
pairs (reading the `7` in "Mistral 7B" as a denominator), and an "of"-binding
version that cross-paired figures within a sentence. Only bind a figure to its
immediate neighbour.

The reason the check finds nothing: in this corpus the denominator is usually
*derived* from a described experiment rather than stated. "12 participants × 10
videos" never appears as "120" anywhere on the page.

## `provenance.py` — model attribution and defect markers

Reads the creating commit for each post, extracts the model from the
`Co-Authored-By` trailer, and computes objective markers: numeric claims per
citation, placeholder identifiers, and citations dated after the post.

```bash
git archive <pre-audit-sha> src/posts | tar -x -C /tmp/pre
python3 scripts/corpus-audit/provenance.py
```

Run it against a **pre-audit** tree. Against the current tree the corrections
have already removed what it looks for.

**Caveat that matters more than the output:** model version is perfectly
confounded with calendar time in this corpus — every 2025 post carries an
unversioned trailer, every 2026 post a versioned one. Tooling and author
practice changed over the same window. The script measures a difference between
cohorts; it cannot attribute one.
