# Blog-audit frontmatter parser migration

Issue #615 evaluated the advisory batch audit's regular-expression YAML subset.
The migration uses pinned PyYAML 6.0.3 with a `SafeLoader` subclass that rejects
duplicate mapping keys and non-string keys. Astro still owns the complete content
schema and publication path. The audit validates the fields it consumes: `title`
must be a string, and `tags` must be a list of strings when present.

## Corpus comparison

Compared the implementation at baseline commit `9091b14` with the new parser
against all 96 Markdown posts in that checkout on 2026-09-13. Both parsers received
the same original file text. All body slices and body-start line offsets matched.
All tag lists matched. Four titles changed only by correctly decoding YAML's
doubled apostrophe inside a single-quoted string:

- `2024-01-08-writing-secure-code-developers-guide.md`
- `2024-01-18-demystifying-cryptography-beginners-guide.md`
- `2024-07-16-sustainable-computing-carbon-footprint.md`
- `2024-10-03-quantum-computing-defense.md`

Every post contains `title`, `date`, `description`, and `tags`. Optional metadata
counts are `author` 60, `post_type` 8, `series` and `seriesOrder` 7 each,
`readingTime` 5, `lastUpdate` 4, `reading_time` 3, and `draft` 2. Tags use 64 block
sequences and 32 flow sequences. Titles use 16 plain, 41 double-quoted, and 39
single-quoted values. Descriptions use 36 plain, 59 double-quoted, and one
single-quoted value. Comments inside tag blocks are covered by regressions.

The old helper returned most scalar values as strings. The new loader uses YAML
types for dates, booleans, and integers; the audit does not consume those fields.
It does not claim schema parity with Astro.

## Dependency and failure behavior

PyYAML is now an explicit pinned runtime dependency in `pyproject.toml`, with
distribution hashes in `uv.lock`. Use `uv run python scripts/blog-audit/batch.py`
or install the declared dependencies with `uv sync`. This adds one package to the
Python environment instead of importing a transitive Node dependency or extending
the hand-written YAML parser. The pin is part of normal dependency maintenance.

The loader accepts quoted commas, escaped/doubled quotes, multiline strings, and
ordinary aliases. It rejects Python object tags and unknown custom tags, duplicate
keys even inside nested mappings, and invalid title/tag types. Recursive aliases
cannot bypass those field type checks. YAML merge keys are deliberately rejected;
there is no implicit override policy for frontmatter. PyYAML's YAML 1.1 scalar
resolution also means values such as `yes` and `on` must be quoted when intended
as text. Invalid metadata fails the audit with source-path context instead of
silently returning incomplete overlap signals.

Missing or unclosed frontmatter retains the existing empty-metadata/original-body
fallback. Empty closed frontmatter now preserves its body offset correctly, and
a line beginning `---something` no longer masquerades as a closing delimiter.
These extraction rules do not replace Astro's required-field validation.

## Validation and cost

The focused extraction suite has 35 passing cases covering the existing prose
and line-number checks plus YAML quoting, multiline/CRLF input, duplicates,
unsafe tags, aliases, type errors, empty delimiters, and audit failure behavior.
The full batch audit completed successfully and emitted JSON for all 96 posts.

A local timing loop parsed all 96 files ten times with each implementation:
mean elapsed time per corpus was 0.0042 seconds for the old subset and 0.0987
seconds for safe YAML loading. These are local author-tool timings, not a portable
benchmark. The added parsing cost is acceptable for an advisory audit that also
performs corpus-wide overlap analysis; it buys standard scalar/collection parsing
and explicit failure behavior without another bespoke syntax layer.
