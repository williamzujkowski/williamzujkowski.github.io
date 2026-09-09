#!/usr/bin/env python3
"""Check built HTML references and anchors offline, including relative URLs.

HTML parsing handles normal quoting/entity forms. URLs resolve against each
page and its first <base href>, just as authored links do in a browser. External
origins remain the scheduled network check's responsibility. Files and symlink
targets must stay inside dist; an empty build cannot pass.
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urljoin, urlsplit

DEFAULT_SITE = "https://williamzujkowski.github.io"
# GitHub project Pages share this origin but are deployed from other repos.
# These URLs belong to the network checker, not this dist tree. Match a whole
# path segment so a missing /remarque-other/ route is still a local failure.
EXTERNAL_PROJECT_PREFIXES = ("/remarque/",)


class Document(HTMLParser):
    def __init__(self, html: str):
        super().__init__(convert_charrefs=True)
        self.references: list[str] = []
        self.ids: set[str] = set()
        self.base: str | None = None
        self.text_only: str | None = None
        self.template_depth = 0
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        if self.text_only:
            return
        if tag in ("textarea", "title"):
            self.text_only = tag
        if self.template_depth:
            if tag == "template":
                self.template_depth += 1
            return
        if tag == "template":
            self.template_depth = 1
        # Browsers use the first occurrence of a duplicate attribute.
        values = {}
        for key, value in attrs:
            values.setdefault(key, value)
        if values.get("id") is not None:
            self.ids.add(values["id"])
        if tag == "a" and values.get("name") is not None:
            self.ids.add(values["name"])
        if tag == "base":
            if self.base is None and values.get("href") is not None:
                self.base = values["href"]
            return
        for key in ("href", "src"):
            if values.get(key) is not None:
                self.references.append(values[key])

    def handle_endtag(self, tag):
        if self.text_only:
            if tag == self.text_only:
                self.text_only = None
        elif tag == "template" and self.template_depth:
            self.template_depth -= 1


def origin(url: str) -> tuple[str, str | None, int | None]:
    parts = urlsplit(url)
    return parts.scheme.lower(), parts.hostname, parts.port or {"https": 443, "http": 80}.get(parts.scheme)


def page_url(site: str, page: Path, dist: Path) -> str:
    path = page.relative_to(dist).as_posix()
    if page.name == "index.html":
        path = path.removesuffix("index.html")
    return urljoin(site, "/" + quote(path))


def resolve(dist: Path, path: str) -> Path | None:
    """Map a URL path to a served file without accepting files outside dist."""
    rel = unquote(path).lstrip("/") or "index.html"
    candidates = [dist / rel]
    if not rel.endswith(".html"):
        # Astro's logical /404/ canonical is emitted as 404.html.
        candidates += [dist / rel / "index.html", dist / (rel.rstrip("/") + ".html")]
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
            if resolved.is_relative_to(dist) and resolved.is_file():
                return resolved
        except (OSError, RuntimeError, ValueError):
            continue
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", type=Path, default=Path("astro-site/dist"))
    parser.add_argument("--site-url", default=DEFAULT_SITE, help="published site's HTTP(S) origin")
    parser.add_argument("--quiet", action="store_true", help="omit successful check counts")
    args = parser.parse_args()
    try:
        site_origin = origin(args.site_url)
        if site_origin[0] not in ("http", "https") or not site_origin[1]:
            raise ValueError("expected an HTTP(S) site URL")
    except ValueError as error:
        parser.error(str(error))

    dist = args.dist.resolve()
    if not dist.is_dir():
        print(f"ERROR: dist not found at {dist}. Run `pnpm build` first.", file=sys.stderr)
        return 1
    pages = sorted(dist.rglob("*.html"))
    if not pages:
        print(f"ERROR: no HTML under {dist}. An empty walk is not a clean pass.", file=sys.stderr)
        return 1

    documents: dict[Path, Document] = {}
    failures: dict[str, list[str]] = defaultdict(list)
    checked_links = checked_anchors = external_project_links = 0

    def document(path: Path) -> Document:
        if path not in documents:
            documents[path] = Document(path.read_text(encoding="utf-8", errors="replace"))
        return documents[path]

    for page in pages:
        url = page_url(args.site_url, page, dist)
        here = urlsplit(url).path
        if not page.resolve().is_relative_to(dist):
            failures[here].append("HTML file resolves outside dist")
            continue
        doc = document(page)
        try:
            base = urljoin(url, doc.base) if doc.base is not None else url
        except ValueError:
            failures[here].append(f"invalid base URL {doc.base}")
            continue
        for raw in doc.references:
            value = raw.strip()
            if not value:
                continue
            try:
                target_url = urljoin(base, value)
                if origin(target_url) != site_origin:
                    continue
                parts = urlsplit(target_url)
            except ValueError:
                failures[here].append(f"invalid URL {value}")
                continue
            if any(parts.path == prefix.rstrip("/") or parts.path.startswith(prefix)
                   for prefix in EXTERNAL_PROJECT_PREFIXES):
                external_project_links += 1
                continue
            checked_links += 1
            target = resolve(dist, parts.path)
            if target is None:
                failures[here].append(f"dead path  {value}")
                continue
            if parts.fragment:
                checked_anchors += 1
                fragment = unquote(parts.fragment)
                # HTML defines #top as the top of the document when no ID matches.
                if fragment.lower() != "top" and fragment not in document(target).ids:
                    failures[here].append(f"dead anchor {value}")

    total = sum(len(values) for values in failures.values())
    if not args.quiet:
        print(f"internal-link-check: {len(pages)} pages, {checked_links} links, {checked_anchors} anchors")
        print(f"Other deployments (excluded from offline check): {external_project_links} references")
    if not failures:
        print("All internal links and anchors resolve.")
        return 0
    print(f"\n{total} broken internal reference(s) across {len(failures)} page(s):\n")
    for source in sorted(failures):
        print(f"  {source}")
        for failure in sorted(set(failures[source])):
            print(f"      {failure}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
