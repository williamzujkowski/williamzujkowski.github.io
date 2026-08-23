#!/usr/bin/env python3
"""Verify every internal link and in-page anchor in the built site.

Why this exists (issue #502): `link-monitor.yml`'s only failure condition
counts results whose status is `broken`. Relative paths never reach that
status -- simple-validator hands them to aiohttp, which raises `InvalidURL`,
which is recorded as `needs_manual`. So 182 relative links, about 12% of the
corpus, were structurally exempt from the one classification the gate reads.
A deliberately nonexistent internal post URL was not "broken".

HTTP was the wrong tool. Internal links resolve against files on disk, so
this walks `dist/` and checks them there: deterministic, offline,
sub-second, and able to fail the build -- unlike everything previously
pointed at links.

What it checks:
  * root-relative hrefs (`/posts/x/`) resolve to a file in dist/
  * in-page fragments (`#notes`) match an id or a name in that page
  * cross-page fragments (`/about/#contact`) resolve on the target page

What it deliberately does NOT check: external URLs (that is link-monitor's
job, over the network, and it must stay advisory because the network is not
a property of this commit).
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlsplit

# href/src values. Skips anything with a scheme and protocol-relative URLs.
LINK_RE = re.compile(r'(?:href|src)\s*=\s*"([^"]+)"', re.I)
ID_RE = re.compile(r'\bid\s*=\s*"([^"]+)"', re.I)
NAME_RE = re.compile(r'<a\b[^>]*\bname\s*=\s*"([^"]+)"', re.I)

# Emitted by the build for the search index and similar; not page links.
IGNORE_PREFIXES = ("/pagefind/",)


def page_ids(html: str) -> set[str]:
    return set(ID_RE.findall(html)) | set(NAME_RE.findall(html))


def resolve(dist: Path, path: str) -> Path | None:
    """Map a site-absolute path to the file that serves it, or None."""
    rel = unquote(path).lstrip("/")
    if rel == "":
        rel = "index.html"
    candidates = [dist / rel]
    if not rel.endswith(".html"):
        candidates += [dist / rel / "index.html", dist / (rel + ".html")]
    for c in candidates:
        if c.is_file():
            return c
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dist", type=Path, default=Path("astro-site/dist"))
    ap.add_argument("--quiet", action="store_true", help="only print failures")
    args = ap.parse_args()

    dist: Path = args.dist
    if not dist.is_dir():
        print(f"ERROR: dist not found at {dist}. Run `pnpm build` first.", file=sys.stderr)
        return 1

    pages = sorted(dist.rglob("*.html"))
    if not pages:
        print(f"ERROR: no HTML under {dist}. An empty walk is not a clean pass.", file=sys.stderr)
        return 1

    ids_cache: dict[Path, set[str]] = {}
    failures: dict[str, list[str]] = defaultdict(list)
    checked_links = 0
    checked_anchors = 0

    for page in pages:
        html = page.read_text(encoding="utf-8", errors="replace")
        here = "/" + str(page.relative_to(dist)).removesuffix("index.html").removesuffix("/")

        for raw in LINK_RE.findall(html):
            value = raw.strip()
            if not value or value.startswith(("//", "data:", "mailto:", "tel:")):
                continue
            if urlsplit(value).scheme:
                continue
            if not value.startswith(("/", "#")):
                continue  # genuinely relative; the site does not emit these
            if value.startswith(IGNORE_PREFIXES):
                continue

            parts = urlsplit(value)
            target_page = page
            if parts.path:
                checked_links += 1
                found = resolve(dist, parts.path)
                if found is None:
                    failures[here].append(f"dead path  {value}")
                    continue
                target_page = found

            if parts.fragment:
                checked_anchors += 1
                if target_page not in ids_cache:
                    ids_cache[target_page] = page_ids(
                        target_page.read_text(encoding="utf-8", errors="replace")
                    )
                if unquote(parts.fragment) not in ids_cache[target_page]:
                    failures[here].append(f"dead anchor {value}")

    total = sum(len(v) for v in failures.values())
    if not args.quiet:
        print(
            f"internal-link-check: {len(pages)} pages, {checked_links} links, "
            f"{checked_anchors} anchors"
        )

    if not failures:
        print("All internal links and anchors resolve.")
        return 0

    print(f"\n{total} broken internal reference(s) across {len(failures)} page(s):\n")
    for src in sorted(failures):
        print(f"  {src}")
        for f in sorted(set(failures[src])):
            print(f"      {f}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
