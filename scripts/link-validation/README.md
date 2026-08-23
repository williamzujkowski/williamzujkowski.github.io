# Link validation scripts

The documentation for this pipeline lives at
[`docs/link-validation/README.md`](../../docs/link-validation/README.md),
which describes the seven scripts that actually exist and how
`link-monitor.yml` and `citation-validation.yml` invoke them.

---

This file previously described a consolidated `link-manager.py` with
`validate` / `fix` / `update-citations` / `check-gists` subcommands, and a
"~400 LOC reduction" changelog. **None of it was ever true.** `link-manager.py`
has never existed in this repository, nor have `citation-updater.py` or
`validate-gist-links.py`, which it named as the scripts it replaced. Every
usage example in it was uncopyable, and an agent reading it would have
reached for a tool that is not there.

Replaced with this pointer rather than rewritten, because the accurate
description already existed in `docs/` — two READMEs for one system, one of
them fiction, is the failure mode worth removing (issue #503).
