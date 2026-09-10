#!/usr/bin/env python3
"""Emit the daily monitor's confirmed-broken counts; network findings are advisory."""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from site_urls import classify_site_url


def summarize(results: list[dict]) -> dict:
    internal = external = 0
    for result in results:
        if result.get("status") != "broken":
            continue
        try:
            url = result.get("url")
            if not isinstance(url, str) or not url.strip():
                raise ValueError("Missing or invalid URL in confirmed-broken result")
            owner, _ = classify_site_url(url)
        except ValueError:
            # A malformed confirmed-broken URL must not disappear from alarms.
            owner = "external"
        if owner == "local":
            internal += 1
        else:
            external += 1
    total = len(results)
    broken = internal + external
    return {
        "broken_count": broken,
        "total_count": total,
        "broken_percent": f"{broken / total * 100 if total else 0:.1f}",
        "internal_broken": internal,
        "external_broken": external,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("validation.json"))
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        counts = summarize(data["results"])
        if output := os.environ.get("GITHUB_OUTPUT"):
            with Path(output).open("a", encoding="utf-8") as file:
                file.writelines(f"{key}={value}\n" for key, value in counts.items())
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Cannot summarize link validation: {error}", file=sys.stderr)
        return 1

    total = counts["total_count"]
    print(f"Total links: {total}")
    print(f"Internal broken: {counts['internal_broken']}")
    print(f"External broken: {counts['external_broken']} (advisory)")
    print(f"Overall: {counts['broken_count']}/{total} ({counts['broken_percent']}%)")
    if counts["internal_broken"]:
        print("NOTE: Own-deployment failures are checked authoritatively against dist/ "
              "by internal-link-check.py in a11y.yml.")
    external_percent = counts["external_broken"] / total * 100 if total else 0
    print(f"External failures: {counts['external_broken']} ({external_percent:.1f}% of all links)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
