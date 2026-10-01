# "The Command Said It Worked": research note, October 1, 2026

Post: `src/posts/2026-10-08-the-command-said-it-worked.md` (scheduled 2026-10-08,
`draft: false`). Status: drafted, self-reviewed, built and audited; lab committed on
an unpushed research-labs branch. The post links the lab at the placeholder
`RESEARCH_LABS_COMMIT`, which must be replaced with the merged commit.

Companion change on the same website branch: a separate commit corrects the Wazuh
post's `curl -sO` download (`src/posts/2025-11-05-siem-homelab-wazuh-graylog-comparison.md`).
The new post states that correction happens "alongside this one"; if that commit is
dropped, the post's first paragraph and the "download" paragraph must change.

## Question and thesis

Reader question: which published ops/security commands fail while reporting
success, and what cheap habit catches them before publication?

Thesis: the defect that hurts readers is the command that exits 0 without doing its
job; link checking, the build and default linting do not see it; running each
command once where it must fail (a negative control), and checking effects rather
than exit status, does. What would weaken it: a static or CI check that flags these
shapes without execution. ShellCheck `-o all` catches one of four (recorded below).

## Lab

- Repository: `~/git/research-labs`, worktree
  `<scratchpad>/post1/rl`, branch `lab/exit-status` (not pushed).
- Commits (pre-rebase): `70619f6` (lab), `f2e29de` (retained run), `0b2335e`
  (ShellCheck cross-check), `1c91cd6` (article-snippet run). Root later rebased the
  branch onto research-labs main for PR #4; SHAs changed, content did not.
- Entry point: `./scripts/exit-status-lab.sh test|run`.
- Container: `python:3.12-slim@sha256:78387bc3...` plus curl and gnupg from Debian
  snapshot `20260824T000000Z`; Pi-hole dispatcher fetched at commits `2d81552`
  (v6.0) and `f47b8ed` (v6.4.3), SHA-256 checked. Runtime: `--network none`,
  read-only root, `--cap-drop ALL`, UID 65532, 1 CPU, 256 MiB, 64 PIDs, 300 s.
- Run 2026-10-01 (~04:50 UTC), clean commit `70619f6`, image
  `sha256:98dd86c7...`. 17/17 cases matched; 6/6 tests passed.
  Tool versions: bash 5.2.37, GnuPG 2.4.7, curl 8.14.1, Python 3.12.14.
- Raw outputs: `docs/evidence/exit-status-2026-10-01/{observations.json,tests.txt,
  shellcheck-0.11.0.txt,post-snippets.txt}` in the lab branch.
- Not run: the `DOCKER-USER` case (needs `NET_ADMIN`). Source finding only.
- First build attempt and all later builds succeeded; no failed runs to record.
  An earlier run during development (dirty tree) also matched 17/17; it is
  not retained because the clean-commit run supersedes it.

## Sources (accessed 2026-10-01)

| Source | Locator | Used for |
| --- | --- | --- |
| PR #658 "fix(content): correct security advice that made readers less safe", W. Zujkowski, merged 2026-09-24T13:24:08Z | https://github.com/williamzujkowski/williamzujkowski.github.io/pull/658, commit `0e19776` | The catalogue; DOCKER-USER measurement claim |
| GNU Bash Reference Manual, "Pipelines" | https://www.gnu.org/software/bash/manual/html_node/Pipelines.html | Quoted pipeline exit status sentence |
| GNU Bash Reference Manual, "The Set Builtin" | https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html | `-e` ignores non-last pipeline commands (background) |
| Greg Wooledge et al., BashFAQ/105 | https://mywiki.wooledge.org/BashFAQ/105 | Quoted "Using a pipe makes no difference..."; `somecmd \| head -n1` pipe-buffer caveat |
| curl man page (curl.se, current) | https://curl.se/docs/manpage.html, `--fail`, `--fail-with-body` | Quoted "By default, curl does not consider HTTP response codes to indicate failure"; "not fail-safe ... 401 and 407" |
| GnuPG manual, GPG Input and Output | https://www.gnupg.org/documentation/manuals/gnupg/GPG-Input-and-Output.html | `--output`: "To write to stdout use - as the filename." |
| GnuPG 2.4.7 source, `g10/openfile.c` `open_outfile`; `common/iobuf.c` `iobuf_is_pipe_filename` | https://github.com/gpg/gnupg/blob/gnupg-2.4.7/g10/openfile.c (lines ~182-260) | Output name = input + `.gpg` unless stdin/`-` or `--output` |
| Pi-hole `pihole` at v6.0 commit `2d81552` (2025-02-18) | https://github.com/pi-hole/pi-hole/blob/2d81552f9f16fb5e12df31069078b43f0e826c3b/pihole L460-511, L519-552 | No `-a` case; `*) helpFunc`; `helpFunc` ends `exit 0` |
| Pi-hole `pihole` at v5.18.4 tag | raw file, L542 and L579 | v5 had `"-a" \| "admin"` → `webpageFunc` |
| Pi-hole release v6.0 (published 2025-02-18T17:29:35Z); v6.4.3 latest (2026-07-06) | GitHub releases API | Dates |
| Pi-hole `advanced/Scripts/api.sh` at `f47b8ed` | `apiFunc` → `GetFTLData` (`-X GET`) | `pihole api` only GETs |
| Pi-hole FTL `lists.yaml` at `0bf029b` | https://github.com/pi-hole/FTL/blob/0bf029baf174f65852a0e598bf4efa436e5cda9c/src/api/docs/content/specs/lists.yaml | `POST /api/lists` "Add new list" |
| Docker docs, "Docker with iptables" | https://docs.docker.com/engine/network/firewall-iptables/ | Quoted FORWARD → DOCKER-USER jump |
| iptables(8) man page (netfilter.org mirror) | https://ipset.netfilter.org/iptables.man.html | Quoted INPUT "for packets destined to local sockets" |
| Vaultwarden `.env.template` at `061694d` | https://github.com/dani-garcia/vaultwarden/blob/061694d0cb3bbf5d4c7e920c892824f0020cff83/.env.template#L451-L453 | Quoted DISABLE_ADMIN_TOKEN comment |
| Ubuntu blog, "Restricted unprivileged user namespaces are coming to Ubuntu 23.10" | https://ubuntu.com/blog/ubuntu-23-10-restricted-unprivileged-user-namespaces | `=1` turns on, `=0` disables |
| Wazuh 4.9 Docker deployment guide | https://documentation.wazuh.com/4.9/deployment-options/docker/wazuh-container.html | Corrected Wazuh install steps |
| wazuh-docker v4.9.2 `single-node/docker-compose.yml` (tag commit `574c7b0`) | raw file | No `WAZUH_*_RAM` variables; `OPENSEARCH_JAVA_OPTS` |
| Live check of `https://packages.wazuh.com/4.9/docker-compose.yml` | `curl -sS -w '%{http_code} %{content_type} %{size_download}'` → `403 application/xml 111`, 2026-10-01T04:44Z | 403 claim, 111 bytes |
| Wayback CDX for that URL | `web.archive.org/cdx/search/cdx?url=...` → 4 captures 2025-12-17..2026-06-18, all 403 | "every capture ... 403" |
| Site link validator source | `scripts/link-validation/link-validator.py` `classify_http_status` (403 → `restricted`); extractor run found the Wazuh URL | "link checker did see ... restricted" |

## Claim ledger

| Proposed claim | Kind | Evidence and locator | Scope/caveat | Status |
| --- | --- | --- | --- | --- |
| PR corrected eight defects across six posts, merged Sept 24 | source finding | PR #658 body ("Eight defects across six posts"), mergedAt 2026-09-24 | Squash commit message says "Seven defects" but lists 8; post follows the PR body and the enumerated list | verified |
| Four of the eight share the exit-0 shape | inference | PR items 2, 5, 6, 8 | Item 8 exits 0 on insertion; the rule is ineffective rather than the command failing | verified |
| Wazuh `curl -sO` case not in #658 | source finding | `git show 0e19776 --stat` (Wazuh post absent); post line 83 pre-fix | Found in the same audit per author memory; not in any public issue | verified |
| Bash pipeline quote | source finding | Bash manual Pipelines | — | verified (exact text) |
| BashFAQ quote and head/pipe-buffer caveat | source finding | BashFAQ/105 | — | verified (exact text) |
| gpg writes input+`.gpg`, redirect target empty | source finding + our observation | openfile.c; observations.json `gpg-redirect` (0 / 131 bytes) | GnuPG 2.4.7; batch passphrase flags added | verified |
| Pi-hole v6.0 released 2025-02-18; the v5 line was added about 18 months later | source finding | releases API; commit `97deac2` | An earlier draft said "twenty days before that post" (the post's date), wrong in substance; corrected | verified |
| Pi-hole line added 2026-09-04 (#544); DOCKER-USER rule added 2026-08-17 (#470); "the check that matters" comment added 2026-09-04 (#538); the pipeline itself from `c1f4b10` (2025-11-11) | source finding | pickaxe log search on each post: `97deac2`, `7fac896`, `ac0f499`, `c1f4b10` | gpg redirect came from `05b5061` (2025-11-15), not a correction pass | verified |
| `docker compose config` on the 111-byte body fails with a YAML error, exit 1 | our observation | Docker Compose v5.5.1, scratch dir, 2026-10-01: `yaml: construct errors: line 1: cannot construct !!str ... into cli.named`, exit=1 | Independent reviewer reported the same | verified |
| Wazuh: `vm.max_map_count=262144` prerequisite; default admin/SecretPassword; OpenSearch root response contains `cluster_name` | source finding | Wazuh 4.9 docker-installation page; wazuh-container page and compose `INDEXER_PASSWORD`; OpenSearch quickstart example response | Not executed | verified |
| v6 dispatcher falls to helpFunc, exit 0; v6.4.3 same | source + observation | pihole L519-552; observations `pihole-*` (exit 0, stdout hash equal to `--help`) | Helpers stubbed; v6.4.3 prints one stderr line from the stub | verified |
| `pihole` v6 has no list-adding subcommand; `api` only GETs | source finding | v6.4.3 helpFunc and dispatch; api.sh `apiFunc`→`GetFTLData` | — | verified |
| URL answers 403, 111-byte XML; Wayback captures all 403 | our observation | live curl 2026-10-01; CDX listing | Cannot prove it never served 200 before 2025-12-17 | verified (bounded) |
| curl default quote; `--fail` not fail-safe 401/407 | source finding | curl man page | Current man page, not 8.14.1-specific | verified |
| curl `-sO` exit 0 saves body; `-fsSO` exit 22 no file; `--fail-with-body` 22 keeps body | our observation | observations `curl-*` | Loopback synthetic server, curl 8.14.1 | verified |
| Docker FORWARD jumps to DOCKER-USER; INPUT is local delivery | source finding | Docker docs; iptables(8) | Not executed by this lab | verified |
| PR records connection succeeded, counter did not move | source finding | PR #658 item 8 | No raw output retained in the website repo | partial (reported, not re-run) |
| Vaultwarden template quote | source finding | `.env.template` L451-453 at `061694d` | — | verified |
| Ubuntu: 1 turns restriction on, 0 disables | source finding | Ubuntu blog | Post does not claim the default value | verified |
| 17/17 cases matched; listed values | our observation | observations.json | One run, one host | verified |
| Link checker classifies 403 as `restricted` (advisory) and extracts the Wazuh URL | source finding + observation | link-validator.py; link-extractor run (URL present) | Did not inspect historical link-monitor runs | verified |
| None of the site's gates flagged the five | inference | posts built and published; 403→restricted; no issue mentions `packages.wazuh.com` (gh search) | Absence of a flag in history not exhaustively audited | partial |
| ShellCheck default silent; `-o all` flags only the pipeline (SC2312 info) | our observation | `shellcheck-0.11.0.txt` | Host ShellCheck 0.11.0, not pinned in the lab | verified |
| Post's inline gpg/cmp snippet: `backup restores` / `cmp: EOF on - which is empty`, exit 1 | our observation | `post-snippets.txt` | Batch passphrase flags added | verified |

## Commands run (website side)

- `gh pr view 658 --json title,body,mergedAt,url`; `git show 0e19776`.
- `uv run python scripts/link-validation/link-extractor.py --posts-dir src/posts --output <scratch>/links.json` (1544 links; Wazuh URL present).
- `cd astro-site && pnpm install --frozen-lockfile && PUBLICATION_AS_OF=2026-10-08T00:00:00Z pnpm build` → exit 0.
- `pnpm run audit` → exit 0 ("All pairs meet APCA draft targets").
- Playwright screenshots of the flow and table at 390 px and 1280 px, light and dark
  colour schemes: no page-level horizontal overflow.

## Overlap check

Searches: `rg -i 'pipefail|exit status|exit code|exits? 0|negative control|fail-with-body'`
over `src/posts` and `docs/shelved-drafts`; `gh issue list --state all --search`
for "exit status", "pipefail", "exit 0", "negative control"; `gh search issues`
for `packages.wazuh.com`.

- `2025-10-06-automated-security-scanning-pipeline.md`: moderate. Same idea at the
  CI-job level (an echoing gate that exits 0). Cross-linked in the close.
- The six corrected posts (#658) and the Wazuh post: they carry the individual
  corrections; this post is the cross-cutting catalogue and lab. Linked.
- `docs/shelved-drafts/2026-08-18-checks-that-pass-for-the-wrong-reason.md`: weak; a
  stub replaced by another post.
- Issues #511, #645, #647, #660 (site tooling that passes for the wrong reason):
  moderate in theme, different subject (the repo's gates, not published commands). Not
  linked; root may choose to.
- No strong overlap found. Posts by the four parallel writers were not visible.

## Layer-1 review coverage

| Stage | Status | Notes |
| --- | --- | --- |
| blog-overlap | completed | See above. |
| blog-factcheck | completed | 21 claims in the ledger; 2 partial (bounded in the post's wording). Internal links all to posts dated before 2026-10-08. |
| blog-llm-tells | manual | Read in full. Zero em dashes. Removed an inaccurate `-s` aside and a "documented" overclaim; changed a 4-column table to 3 for phone width. American spelling to match the archive (40 vs 6 posts). |
| blog-nda-check | completed | No employer, incident or agency references. First person limited to William's own PR/posts. ShellCheck and URL checks phrased impersonally because they were run by the drafting agent. |
| blog-argument-shape | completed | Thesis in para 2 and "Run it where it must fail". Strongest objection (a linter could catch it) answered with retained ShellCheck output; corrected forms' own limits stated (pipefail/head, `--fail` 401/407). No prevalence claim. |
| blog-visuals | manual | One `.flow` (roles/labels per contract), one table. Rendered at 390/1280 px light/dark, no overflow. `data-theme-deck` variants not checked. Doodle left as a `<!-- DOODLE -->` TODO. |
| blog-artifact-check | completed | Every command/flag checked against upstream source or executed: lab cases, both inline snippets, Pi-hole `-a`/`api`/`/api/lists`, Wazuh replacement steps against the 4.9 guide (Wazuh steps not executed). |

## Limitations

- One run on one host; tool behaviors are version-specific.
- The Pi-hole cases execute only the dispatcher with stubbed helpers.
- The DOCKER-USER case is a source finding; the PR's measurement has no retained raw output.
- The Wazuh replacement steps follow the vendor guide but were not executed.
- No claim about how common these defects are outside this site.
- The Wazuh post contains other claims (benchmark timings) not reviewed here.
- The Docker hardening post still recommends `INPUT -i docker0` as verified-looking
  advice; the new post says it is unrun and bridge-specific, but that post itself was
  not edited.

## Independent review (2026-10-01)

Two reviews arrived via root: Claude (HOLD; independently re-ran the lab at the
pre-rebase commit `1c91cd6` on 2026-10-01 and reproduced 6/6 tests and 17/17 cases)
and Gemini 3.1 Pro. Each item was checked against source before editing.

| Item | Verification | Action |
| --- | --- | --- |
| "Twenty days before that post" false in substance | Pickaxe search: Pi-hole line `97deac2` (#544, 2026-09-04); DOCKER-USER `7fac896` (#470, 2026-08-17); comment `ac0f499` (#538, 2026-09-04) | Applied with one precision change: the Suricata pipeline predates the 2026 passes (`c1f4b10`, 2025-11-11) and #538 added the comment vouching for it, so the post says two of the four were introduced by correction passes and a third pass vouched for the pipeline, not "three of the four arrived" |
| INPUT fix never run; `docker0` is only the default bridge | Docker post's corrected block uses `-i docker0`; no retained run | Applied: table cell and paragraph say "not verified" and describe the negative control. The Docker post itself is unchanged (flagged to root) |
| Compose fails loudly one step later; scope the pre-December-2025 history | Reproduced `docker compose config` exit 1 (ledger) | Applied both |
| Vaultwarden quote incomplete | Template L451-452 at `061694d` | Applied: full two-sentence quote |
| Wazuh prerequisite; health check that cannot pass on a 401 | Wazuh docker-installation page; compose credentials; OpenSearch example response | Applied to the Wazuh post (steps still not executed) |
| Compare before shredding `seeds.txt` | The check needs the plaintext | Applied |
| Record the independent reproduction | Reported by root | Applied (this section) |

No item was rejected.
