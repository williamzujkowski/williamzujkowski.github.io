# npm provenance attests the pipeline, not the intent: evidence record

**Post:** `src/posts/2026-10-22-npm-provenance-attests-the-pipeline.md` (scheduled 2026-10-22)
**Evidence captured:** 2026-10-01, 04:45Z to 05:40Z, from public endpoints only.
**Origin:** [dependency-risk-profiler #335](https://github.com/williamzujkowski/dependency-risk-profiler/issues/335)
(opened and measured 2026-08-11). The August raw data for #335 was not retained in
that repository, so every number in the post except the two #335 figures named below
was re-measured on 2026-10-01.

## Claim strength

Existence and mechanism, n=3 independent victims (jagreehal, Injective, keyv), plus one
counter-example (cline). Not a rate. The #335 figures 80/116 (69.0%) and 30/32 (93.8%)
are deliberately absent from the post.

## Sources

| Source | Author / publisher | URL | Date | Accessed |
|---|---|---|---|---|
| Generating provenance statements | npm Docs | https://docs.npmjs.com/generating-provenance-statements | live page | 2026-10-01 |
| Trusted publishing for npm packages | npm Docs | https://docs.npmjs.com/trusted-publishers | live page | 2026-10-01 |
| Staged publishing for npm packages | npm Docs | https://docs.npmjs.com/staged-publishing | live page | 2026-10-01 |
| Verifying ECDSA registry signatures | npm Docs | https://docs.npmjs.com/verifying-registry-signatures | live page | 2026-10-01 |
| Threats & mitigations, SLSA v1.0 (status: retired) | SLSA / OpenSSF | https://slsa.dev/spec/v1.0/threats | v1.0 | 2026-10-01 |
| Threats & mitigations, SLSA v1.2 | SLSA / OpenSSF | https://slsa.dev/spec/v1.2/threats | v1.2 | 2026-10-01 |
| Deployments and environments | GitHub Docs | https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments | live page | 2026-10-01 |
| Miasma npm Supply Chain Attack: Self-Spreading Worm via Phantom Gyp | StepSecurity (Sai Likhith) | https://www.stepsecurity.io/blog/binding-gyp-npm-supply-chain-attack-spreads-like-worm | 2026-06-03 | 2026-10-01 |
| Injective npm Supply Chain Attack: 18 Packages Backdoored to Steal Crypto Wallet Keys | StepSecurity | https://www.stepsecurity.io/blog/injective-npm-supply-chain-attack-18-packages-backdoored-to-steal-crypto-wallet-keys | July 2026 | 2026-10-01 |
| Popular npm Packages in the keyv and Cacheable Namespaces Compromised | Socket Research Team | https://socket.dev/blog/popular-npm-packages-in-the-keyv-and-cacheable-namespaces-compromised-in-active-supply-chain | 2026-08-04 | 2026-10-01 |
| NPM Malware Compromises keyv and cacheable | Endor Labs | https://www.endorlabs.com/learn/npm-malware-compromises-keyv-and-cacheable-with-500m-weekly-downloads-and-spreads-to-hundreds-of-packages | Aug 2026 | 2026-10-01 |
| Inside the keyv npm Supply Chain Compromise (consulted, not cited) | Snyk | https://snyk.io/blog/inside-keyv-npm-compromise-preinstall-malware-trusted-provenance-ide-hooks/ | Aug 2026 | 2026-10-01 |
| Miasma poisoned Red Hat Cloud Services npm packages through trusted publishing | Corgea Research | https://corgea.com/research/redhat-cloud-services-npm-miasma-shai-hulud-worm | 2026-06-02 | 2026-10-01 (WebFetch; curl returns 403) |
| GHSA-9ppg-jx86-fqw7, unauthorized npm publish of cline@2.3.0 | Cline maintainers | https://github.com/cline/cline/security/advisories/GHSA-9ppg-jx86-fqw7 | 2026-02-17 | 2026-10-01 |
| malicious-software-packages-dataset | Datadog | https://github.com/DataDog/malicious-software-packages-dataset | (as used in #335, Aug 2026) | 2026-10-01 (existence) |
| keyv release workflow before the incident | jaredwray/keyv @ `90109616a94f` | https://github.com/jaredwray/keyv/blob/90109616a94f6774c172c5f457b2195d5801d508/.github/workflows/release.yaml | last commit before 2026-08-04T09:00Z | 2026-10-01 |
| autotel release workflow before / after | jagreehal/autotel @ `35a8a119` / `f5cf12a4` | see post links | 2026-06-03 / 2026-10-01 | 2026-10-01 |

All quoted phrases were string-matched against the fetched page text by
`2026-10-01-npm-provenance-quotecheck.py` (all FOUND except Corgea, which blocks curl;
Corgea's phrase "triggered on attacker-controlled branch pushes" and the 1 June date were
confirmed by two separate WebFetch reads). Earlier prior art for the thesis exists and is
cited rather than claimed: Socket ("provenance attests build integrity, not source
integrity"), Corgea and Snyk all make the same point about these incidents.

## Claim ledger

| Proposed claim | Kind | Evidence and locator | Scope / caveat | Status |
|---|---|---|---|---|
| `npm audit signatures` output is identical (counts, exit 0) for malicious sdk-ts 1.20.21 + autotel-audit 0.1.15 and clean 1.20.20 + 0.1.14 | our observation | Container run below: both print 216 registry signatures / 85 attestations, EXIT=0; only elapsed time differs (7s vs 6s) | Per-package inclusion inferred: both malicious versions have `dist.attestations` in the packument and no invalid attestation was reported | verified |
| npm docs: provenance "does not guarantee the package has no malicious code" | source finding | npm provenance page | live page | verified |
| SLSA v1.0 source-threat definition and "does not address source threats" | source finding | slsa.dev v1.0 threats, Source threats intro, (A), (B) | v1.0 is retired; v1.2 quote added | verified |
| SLSA v1.2: producer threat "cannot be directly mitigated through SLSA controls" | source finding | slsa.dev v1.2 threats, (A) Producer | | verified |
| Only 3 independent victims among attested malicious versions | in-repo record | #335 comment 2026-08-11 (30 packages, 3 owners) | Aug 2026 measurement; raw not retained | recorded, not re-run |
| jagreehal burst: ≥280 versions / 53 packages, 00:25:27–00:30:21Z 4 June; 204 removed; 76 present | our observation | results.json `jagreehal_window_scan`, filter time in [00:25, 00:31) | Package list from npm search `maintainer:jagreehal` (135 packages); wholly-removed packages invisible, hence "at least" | verified |
| All 76 present: attested, deprecated, root 157-byte binding.gyp, sha512 == attestation subject | our observation | results.json `jagreehal_burst_present_tarball_check` | Tarballs listed in memory, never extracted; deleted after | verified |
| 7 repos; each attested commit has 0 parents and touches only `.github/workflows/release.yml` and `_index.js` | our observation | `gh api repos/jagreehal/<repo>/commits/<sha>` for all 7 SHAs | | verified |
| Attacker workflow triggers on `push` with `id-token: write`; main's pre-incident copy filtered `branches: [main]` | our observation | contents API at 28a85158 and 35a8a119 | Workflow body deliberately not reproduced | verified |
| Snapshot ref vs main ref in autotel-audit 0.1.15 vs 0.1.14 provenance and certificate | our observation | certificate_fields_text + jq snippet output | | verified |
| `main` and the orphan commit: "No common ancestor" | our observation | `gh api repos/jagreehal/autotel/compare/main...28a85158…` → 404 with that message | | verified |
| Injective 1.20.21 and 1.20.20: same workflow/ref/trigger; differ in digest, commit, run | our observation | decoded predicates + cert extensions | | verified |
| Injective attested commit is in master's history | our observation | compare 5486f13e...master → status "ahead" by 174 | as of 2026-10-01 | verified |
| Injective clean 1.20.23 published 49 min after 1.20.21 | our observation | packument time: 20:59:28.362Z → 21:48:03.717Z = 48m35s | | verified |
| keyv: compromised maintainer account; trusted publishing; valid provenance | source finding | Socket, Endor (quotes string-matched) | attestation now 404, cannot re-decode | verified (secondary) |
| keyv: `v6.0.0` tag, `release` trigger | in-repo record + source | #335 comment; release.yaml at 90109616 has `release: types: [published]` | tag and release now 404 | partial |
| keyv publish job named `environment: release`, also at attacker commit ee2681a9 | our observation | contents API at 90109616 and ee2681a9 (line 76) | environment's protection rules are not public | verified |
| autotel's current workflow: environment restricted to main + required reviewer | our observation (author's comment) | release.yml @ f5cf12a4, comment block above `environment: release` | Rules described by the maintainer's comment; settings themselves not visible | verified as quoted |
| npm trusted publisher fields: workflow filename required, environment optional; no branch field | source finding | npm trusted-publishers page | live page | verified |
| cline 2.3.0: stolen npm token; no attestation; 2.2.3 and 2.4.0 attested | source finding + our observation | GHSA; packument `dist.attestations` | | verified |
| 5,457 of 5,573 malicious versions unreadable in Aug | in-repo record | #335 comment 2026-08-11 | raw not retained; scoped as "the August measurement recorded in #335" | recorded, not re-run |
| keyv@6.0.0 attestation 200 in Aug, 404 on 2026-10-01 | in-repo record + our observation | #335; curl 404 at 04:45Z | | verified |
| four removed ai-sdk-ollama burst versions → 404 | our observation | curl, 0.13.1 / 1.1.1 / 2.2.1 / 3.8.5 | | verified |
| npmmirror returns 0.8.4's tarball and shasum for 0.9.4 | our observation | `registry.npmmirror.com/@antv/dumi-theme-antv/0.9.4` → version "0.9.4", tarball `…-0.8.4.tgz`, shasum dc70ba68… = npmjs 0.8.4 shasum; 0.9.4 absent from npmjs | | verified |
| npm only issues provenance from supported CI runners | source finding | npm provenance + trusted-publishers pages (supported providers, cloud-hosted runners) | | verified |

## Commands run (2026-10-01)

- `curl https://registry.npmjs.org/-/npm/v1/attestations/<pkg>@<ver>` for keyv 6.0.0 (404),
  sdk-ts 1.20.20/1.20.21 (200), cline 2.3.0 (404), ai-sdk-ollama 0.13.1/1.1.1/2.2.1/3.8.5/3.8.6 (404), 3.8.4 (200).
- `python3 2026-10-01-npm-provenance-scan.py` (run from a scratch dir holding `raw/search_jag.json`
  from `registry.npmjs.org/-/v1/search?text=maintainer:jagreehal&size=250`): 305 versions in
  2026-06-03..06-06, 100 present.
- `python3 2026-10-01-npm-provenance-gypcheck.py`: 76 checked, 76 binding.gyp (157 bytes),
  76 deprecated, 76 digest matches.
- `uv run --no-project --with cryptography python 2026-10-01-npm-provenance-certdump.py …`:
  Fulcio extension values recorded in the results JSON.
- Container (image `node@sha256:4d676821dff059fd00d277ee4261ef34ea712317fed0737c03941481b5760c96`,
  `node:22-bookworm-slim`, npm 10.9.8): `--user node --read-only --tmpfs /tmp --cap-drop ALL
  --security-opt no-new-privileges --memory 2g`; `npm install --ignore-scripts --legacy-peer-deps`
  then `npm audit signatures`, malicious pair then clean pair. Network was needed for the
  registry. `--ignore-scripts` suppresses the implicit node-gyp build, so the binding.gyp
  payload never ran. Container discarded.
- `gh api` reads of commits, compare, contents and workflow runs for jagreehal/*,
  InjectiveLabs/injective-ts and jaredwray/keyv.
- `sigstore verify github` (sigstore-python 4.5.0) was attempted and failed with "in-toto
  statement has no subject for digest": npm subjects carry only sha512, the CLI hashes sha256.
  Cryptographic verification therefore rests on `npm audit signatures`.

Raw outputs: `2026-10-01-npm-provenance-results.json`. Malicious tarballs were downloaded to
scratch for listing only and deleted.

## Research-labs placement

Not applicable. research-labs' AGENTS.md forbids live targets, network services and untrusted
inputs; this evidence is reads of the live public registry and of known-malicious tarballs.
Scripts and raw output are kept here instead, following the 2026-09-11 page-cache precedent.

## Limitations

- n=3 victims; the survivors are selected by npm's removals. No rate is claimed.
- The keyv bundle could not be re-decoded (404 since August). keyv's mechanism rests on #335's
  August record and three vendor write-ups.
- "Triggering actor = maintainer's own account" (#335) is not repeated in the post; the post
  uses Socket's "maintainer account was compromised" instead.
- A claim from session notes that GitHub's workflow-run list omits runs whose triggering tag was
  deleted was dropped: it is not recorded in #335 and could not be re-tested without a run ID.
  Observed only: on 2026-10-01 the list endpoint shows zero `release.yaml` runs for keyv in
  2026-08-01..06 and zero runs for head SHA ee2681a9; the `v6.0.0` tag and release are 404.
- Whether the environment protection rules in keyv existed is not public.
- The Injective run 28975012939 concluded `failure` per the API although the publish succeeded;
  not explored, not in the post.

## Overlap check

- `rg -i 'provenance|attestation|trusted publish|sigstore|slsa|oidc' src/posts docs/shelved-drafts`:
  no post covers npm provenance. `docs/shelved-drafts/2026-08-01-dependency-risk-leading-indicators.md`
  promoted "provenance posture" as a leading indicator and was shelved on the #328 measurement
  (README row: 12.72% vs 12.5%, p=0.97). The new post does not revive that claim.
- `2026-05-07-patch-fast-pull-slow-defending-copy-fail-shai-hulud.md` (published): moderate; npm
  worms and dependency cooldowns, no provenance discussion. Cross-linked from the close for the
  hold-new-versions advice.
- `2026-03-21-trivy-supply-chain-compromise-ai-assisted-investigation.md` (published): weak to
  moderate; CI as a credential-theft target. Cross-linked in the close.
- `gh issue list --state all --search provenance` / `"trusted publishing"` and
  `gh pr list --state all --search provenance` in this repo: no matching proposal or post.
- Verdict: distinct contribution (decoded fields across three routes, the identical consumer
  check output, measurement traps). External prior art for the thesis is cited.

## Layer-1 review coverage

| Stage | Status | Evidence |
|---|---|---|
| blog-overlap | completed | section above |
| blog-factcheck | completed | claim ledger; quote checker; every number recomputed from raw files on 2026-10-01. Fixed during review: "four ai-sdk-ollama 404s" (only one had been fetched, then all four were), "binds to filename" misattributed to Corgea (rewritten as our reading of npm's config fields), "gone within the hour" (1.20.21 is still on npm, deprecated; replaced with the 1.20.23 timing), "280 versions" made "at least", "Both runs printed the same thing" qualified for elapsed time, "certificates name refs deleted by attackers" (runs still exist; rewritten) |
| blog-llm-tells | manual | Read in full for hedging, stock contrasts, triple parallelism and closing summaries. Removed one "strong signal" overclaim and a non-sequitur cross-link. Remaining "not X, but Y" uses are the thesis itself (title, Socket quote, final line), kept deliberately. No exclamation marks; em dashes: none. |
| blog-nda-check | completed | No employer or work references. All first person refers to recorded work in dependency-risk-profiler #335 and the 2026-10-01 measurements here. Victims named only as projects / npm account handles already public in vendor write-ups; no individual is blamed; the autotel fix is credited to the maintainer. |
| blog-argument-shape | completed | Thesis: "If an attacker can make the pipeline run, the certificate is accurate and the package is malware." Evidence: 3 decoded cases + audit-signatures demo + docs. Strongest objection (provenance never claimed this) is answered in section 2. Disconfirming result: a field-level check that separates the Injective or keyv publishes from their clean neighbours. Close follows: keep it, read the ref, gate before the pipeline. |
| blog-visuals | manual | One `.flow` (5 nodes, role=group + aria-label, no blank lines, escaped text); one Markdown table. Doodle left as `<!-- DOODLE -->` TODO for root. Rendered review in browser not performed; build + `pnpm run audit` results recorded in the final report. |
| blog-artifact-check | completed | The jq snippet was executed against autotel-audit 0.1.15 and 0.1.14 and prints the values the post quotes. Field names checked against the actual decoded predicate (`buildDefinition.externalParameters.workflow.{ref,path}`, `internalParameters.github.event_name`, `resolvedDependencies[0].digest.gitCommit`). Certificate extension names from Fulcio OIDs 1.3.6.1.4.1.57264.1.14 and .1.20. No gists. |
