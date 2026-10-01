---
title: "The Repository Link That Points at Nobody"
date: 2026-10-29
draft: false
author: William Zujkowski
description: "About one declared repository link in seven no longer cloned anonymously, and for about a fifth of those the GitHub account it names no longer existed."
tags:
  - security
  - supply-chain
  - open-source
  - ethics
---

Most package registries let a publisher type in a source repository URL. npm calls it `repository`, PyPI files it under `project_urls`, RubyGems has `source_code_uri`. For most packages the registry stores it as typed, and a whole class of tooling reads it: OpenSSF Scorecard, deps.dev, and my own [dependency-risk-profiler](https://github.com/williamzujkowski/dependency-risk-profiler/tree/b3fe6e5fe1fba59d2c6d8f5ef92456f252d23fd2), which computes 41.51% of its score's declared weight from whatever repository the package names.

In August that project ran a small, deliberately polite measurement. Take declared GitHub links that no longer clone. Ask GitHub one question about each: does the account in the URL still exist? For 25 of 118 distinct owners, the answer was no. That is about a fifth of the dead links, and roughly 3% of all the declared links sampled. For those packages, the field a scorer reads names an account that, on the day it was checked, nobody held.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/dead-link.png'); width: min(300px, 72%); aspect-ratio: 520/287; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">The sign still sounds very sure of itself.</p>

## Where the numbers come from

The sample came from the project's [cross-ecosystem study](https://github.com/williamzujkowski/dependency-risk-profiler/blob/b3fe6e5fe1fba59d2c6d8f5ef92456f252d23fd2/docs/cross-ecosystem-result.md): 1,000 names per ecosystem, drawn uniformly from each registry's full published name list rather than a popularity ranking. From the packages that declared a usable repository, it subsampled 200 per ecosystem and tried to clone each GitHub link anonymously (769 of the 800 pointed at GitHub). A clone that fails with GitHub's authentication prompt is ambiguous by design. It means private, renamed or deleted, and the response does not say which.

That ambiguity is where the [dangling-links protocol](https://github.com/williamzujkowski/dependency-risk-profiler/blob/b3fe6e5fe1fba59d2c6d8f5ef92456f252d23fd2/docs/dangling-links-protocol.md) starts. It was written down before the run, along with the result that would count as a refutation (fewer than 10% missing owners), and the result is in the [raw output file](https://github.com/williamzujkowski/dependency-risk-profiler/blob/b3fe6e5fe1fba59d2c6d8f5ef92456f252d23fd2/research/results/dangling-links.json).

<div class="flow" role="group" aria-label="How a declared link was classified">
  <div class="flow-node"><b>Declared repository link</b><i>200 per ecosystem, 769 of 800 on GitHub</i></div>
  <div class="flow-node is-gate"><b>Anonymous clone fails with auth</b><i>120 links, 118 distinct owners</i></div>
  <div class="flow-node is-gate"><b>One read-only lookup of the owner</b><i>0 API errors on the counted run</i></div>
  <div class="flow-branch" role="group" aria-label="Lookup outcomes">
    <div class="flow-leg" data-branch="404" role="group" aria-label="404"><div class="flow-node is-bad"><b>25 owners missing</b><i>no account answers to that name</i></div></div>
    <div class="flow-leg" data-branch="200" role="group" aria-label="200"><div class="flow-node"><b>93 owners exist</b><i>private or deleted repo: still ambiguous</i></div></div>
  </div>
</div>

| Ecosystem | Declared links sampled | Failed with auth | Share |
|---|---:|---:|---:|
| npm | 200 | 40 | 20.0% |
| RubyGems | 200 | 39 | 19.5% |
| PyPI | 200 | 31 | 15.5% |
| Packagist | 200 | 10 | 5.0% |
| **All four** | **800** | **120** | **15.0%** |

Across npm, PyPI and RubyGems, roughly one declared link in five or six hit that prompt. Of the 118 owners behind the 120 failing links, 25 returned 404. The point estimate is 21.2%, and at this sample size the 95% interval runs from about 15% to 29%, so "about a fifth" is as precise as the data allows.

The roughly 3% figure needs one more step. Owners were de-duplicated before lookup, so the result counts owners rather than links. With 120 links and 118 owners, the 25 missing owners account for somewhere between 25 and 27 links: 3.1% to 3.4% of the 800 declared links attempted. That range describes this draw, these four ecosystems and a snapshot from mid-August 2026. Namespaces are freed and taken every day.

## "Nobody holds it" is not "anyone can take it"

A 404 from `api.github.com/users/<owner>` says no user or organisation currently answers to that name. It does not say the name is available, or that the old repository path can be recreated. GitHub's own rules make that distinction matter.

When a user renames, [GitHub's documentation](https://docs.github.com/en/account-and-profile/concepts/username-changes) says the old username "becomes available for anyone else to claim", and redirects keep old repository URLs working until "the new owner of your old username creates a repository with the same name". A deleted account's username is [available after 90 days](https://docs.github.com/en/account-and-profile/reference/personal-account-reference).

Against that, GitHub retires some names permanently. The current rule covers public repositories that contain an action listed on GitHub Marketplace, or that had more than 100 clones or more than 100 uses of GitHub Actions in the week before the rename or deletion. For those, GitHub retires the `OWNER/REPOSITORY-NAME` combination, so the same path cannot come back under a new owner. The [2018 announcement](https://github.blog/open-source/maintainers/new-tools-for-open-source-maintainers/) introduced the 100-clone threshold to stop developers "pulling down potentially unsafe packages".

The measurement checked none of that. Some of the 25 may sit behind a retired combination or another restriction this lookup cannot see. What it shows is the size of the pool those protections have to cover. Whether any individual name in it is claimable was deliberately left unknown.

## Deliberately less than it could have measured

The protocol drew the line in one sentence: "A count of freed namespaces is a defensive measurement; a list of claimable ones is a target list."

So the script makes one `GET` per owner, against a public endpoint, with a read-only token. It never checks whether a name can be registered and registers nothing. Its output contains [counts only](https://github.com/williamzujkowski/dependency-risk-profiler/blob/b3fe6e5fe1fba59d2c6d8f5ef92456f252d23fd2/research/cross_ecosystem/dangling.py), by construction, so nobody can lift a list of package or owner names from the artifacts. This post follows the same rule.

The cost of that restraint is a weaker claim. "Owner missing" is an upper bound on "repository path claimable", and the gap between the two is unmeasured. I would rather publish the bound than the list.

## The guard that refused a nearly right answer

The first run checked owners without a token. GitHub's unauthenticated API allows 60 requests an hour, and 59 of the 118 lookups came back as rate-limit errors. The protocol had registered a ceiling: if more than 20% of checks errored, the run would be reported as inconclusive rather than scaled up from the survivors. The script evaluates that ceiling itself, and it fired.

The surviving half would have said 20.3%. The authenticated rerun, with zero errors, said 21.2%. It is tempting to read that as proof the guard was fussy. It reads the other way to me. Rate-limit errors arrive in a block once the allowance runs out, and the owners were looked up in roughly alphabetical order, so the missing half was not a random half. The first run happened to land near the truth, and nothing in it could tell us so.

## Prior art

None of the exposure is news, and the attack has a name. Ladisa and colleagues' [supply-chain attack taxonomy](https://arxiv.org/abs/2204.04008) (IEEE S&P 2023) lists "dangling reference" as AV-501: reusing the identifiers of orphaned projects. Aqua Nautilus [sampled 1.25 million repository names](https://www.aquasec.com/blog/github-dataset-research-reveals-millions-potentially-vulnerable-to-repojacking/) from a June 2019 GHTorrent dump and found 36,983, or 2.95%, vulnerable to repojacking. Checkmarx [reported three of the four known bypasses](https://checkmarx.com/blog/persistent-threat-new-exploit-puts-thousands-of-github-repositories-and-millions-of-users-at-risk/) of the namespace-retirement protection (two in 2022, one disclosed in March 2023 and fixed that September), and counted over 4,000 packages on Packagist, Go, Swift and other managers that use renamed usernames and would be at risk if another bypass turned up.

The closest match is Denis Makrushin's [2025 study](https://makrushin.com/repojacking-github/), which started from the public GitHub dataset and applied the same method to repositories referenced from PyPI and npm. It checked each username against GitHub's signup form and reported 1,363 repositories tied to 986 accounts eligible for re-registration, 426 of them referenced from PyPI or npm, and about 0.03% of everything analysed. That is a stronger test than mine: it measures availability, where this one stops at existence. It is also a far lower rate. His PyPI figure works out to 352 of 293,470 unique repositories, about 0.12%, against roughly 3% here. The units differ twice over. His count is names confirmed claimable, mine is owners merely missing. His denominator is unique repositories, each counted once however many packages point at it, while mine is uniformly drawn packages, which weights the abandoned long tail. I have not reconciled the two, and the gap is a reason to read my 3% as a property of a random package, not of the repositories people actually install from.

What the dependency-risk-profiler run adds is narrower. It starts from a uniform draw of registry packages, carries the denominator through to declared links per ecosystem, and connects the result to tools that compute scores from the field. It is another sighting of the problem, with packages as its denominator where the earlier studies used repositories.

## Packagist, and why a low rate is not immunity

Packagist's dead-link rate was a quarter to a third of the others'. The project's explanation fits [how Packagist works](https://packagist.org/about): a package is submitted as a public repository URL, and new versions are crawled from that repository's tags. A link that carries the installation cannot rot unnoticed. The explanation is plausible, but this study did not test it.

Load-bearing links cut both ways. The Checkmarx write-up names Packagist among the managers where a successful bypass enables package takeover. Fewer dead links there means fewer stale scores. A hijacked one is worse, because it can change what gets installed.

## What a consumer can do

None of this measured an attack, and nothing here says any package was hijacked. It measured how often the input to a class of scorer is a claim that has stopped resolving. Some practical consequences follow:

- **Treat a declared repository as unverified unless something says otherwise.** Scorecard's package-manager mode, for one, [takes npm's `repository.url`](https://github.com/ossf/scorecard/blob/c0c8dea5b436a74d730d35e679a6efa8b6303cf7/cmd/package_managers.go#L127-L147) and strips `git+` and `.git`. Its README is candid that the flags exist "to find a GitHub repo only".
- **Prefer links with provenance.** deps.dev labels every package-to-repository mapping with how it was discovered: [`SLSA_ATTESTATION`, `GO_ORIGIN`, the PyPI and RubyGems publish attestations, or `UNVERIFIED_METADATA`](https://docs.deps.dev/api/v3/). That last value tells you whether the edge you are scoring is a claim. npm's [provenance documentation](https://docs.npmjs.com/generating-provenance-statements) tells publishers that `repository` must match the repository they publish from, and PyPI marks [verified project URLs](https://docs.pypi.org/project_metadata/) for Trusted Publishers.
- **Know when the attestation was made.** PyPI's own documentation warns that verification "occurs when release files are uploaded and is not repeated afterwards". A link verified in 2023 can point at a freed name in 2026. This measurement did not separate verified links from the rest.
- **If you build a scorer, check that the link points back.** A dead link usually makes the repository checks fail outright. The risk is the day the path answers again under a new owner. My suggestion, untested: abstain when the repository was created after the package's first release, or when its manifest does not name the package.

The repository field is a sentence the publisher wrote once. About one time in seven in this sample, an anonymous reader could no longer follow it, and about a fifth of those named an account that no longer existed. The tools that read the field should check whether the sentence is still true.
