"""URL origin and deployment ownership shared by online and offline checks."""
from urllib.parse import SplitResult, urljoin, urlsplit

DEFAULT_SITE = "https://williamzujkowski.github.io"
# Project Pages share our origin but have independent deployment artifacts.
EXTERNAL_PROJECT_PREFIXES = ("/remarque/",)


def origin(url: str) -> tuple[str, str | None, int | None]:
    parts = urlsplit(url)
    port = parts.port if parts.port is not None else {"https": 443, "http": 80}.get(parts.scheme)
    return parts.scheme.lower(), parts.hostname, port


def normalize_dot_segments(path: str) -> str:
    """Normalize browser URL dot segments without decoding encoded separators."""
    output: list[str] = []
    segments = path.split("/")
    for index, segment in enumerate(segments):
        # WHATWG special URLs recognize mixed literal/percent-encoded dots,
        # but %2F remains part of its segment rather than becoming a slash.
        dots = segment.lower().replace("%2e", ".")
        if dots in (".", ".."):
            if dots == ".." and len(output) > 1:
                output.pop()
            if index == len(segments) - 1:
                output.append("")
        else:
            output.append(segment)
    return "/".join(output)


def classify_site_url(url: str, site: str = DEFAULT_SITE) -> tuple[str, SplitResult]:
    """Return local/project/external ownership and the normalized URL parts.

    Relative references are local unless they resolve into a separate project
    deployment. Malformed URLs raise ValueError for the caller to report.
    """
    absolute = urljoin(urljoin(site, "/"), url)
    parts = urlsplit(absolute)
    parts = parts._replace(path=normalize_dot_segments(parts.path))
    if origin(absolute) != origin(site):
        return "external", parts
    if any(parts.path == prefix.rstrip("/") or parts.path.startswith(prefix)
           for prefix in EXTERNAL_PROJECT_PREFIXES):
        return "project", parts
    return "local", parts
