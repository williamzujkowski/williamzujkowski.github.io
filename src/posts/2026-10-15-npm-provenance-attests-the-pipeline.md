---
title: "Provenance Attests the Pipeline, Not the Intent"
date: 2026-10-15
draft: false
author: William Zujkowski
description: "Three 2026 npm compromises shipped malware with valid provenance. Only one of them is visible in the signed fields, and a fourth shows what provenance does catch."
tags:
  - security
  - supply-chain
  - npm
---

npm provenance is a signed note stapled to a package. It says which repository, workflow file, git ref and commit built this exact tarball, and a Sigstore certificate vouches for the note. With [trusted publishing](https://docs.npmjs.com/trusted-publishers), a GitHub Actions job publishes using a short-lived OIDC credential instead of a stored token, and the provenance comes for free. It is one of the better things to happen to the npm registry in years. It also does exactly what it says, which turns out to be less than a green checkmark implies.

On October 1 I installed two deprecated, known-malicious versions into a throwaway container with install scripts disabled: `@injectivelabs/sdk-ts@1.20.21` and `autotel-audit@0.1.15`. Then I ran `npm audit signatures`. Then I swapped in the clean versions published just before each one and ran it again. Don't repeat this at home: reading the attestation, as shown further down, gives the same evidence without installing anything. Apart from the elapsed time (7s here for the malicious pair, 6s for the clean one), both runs printed the same thing:

```text
audited 216 packages in 7s
216 packages have verified registry signatures
85 packages have verified attestations
```

Exit code 0 both times. Both malicious versions carry attestations, and none was reported invalid. The check was right: it verified that each tarball came from the pipeline its certificate names, and each one did.

<!-- DOODLE: a pristine, wax-sealed shipping label on a crate, with a raccoon visibly inside the crate peering out through the slats; the seal is perfect, the contents are not -->

## What provenance was ever promised to mean

Careful sources never sold this as a malware check. npm's [provenance documentation](https://docs.npmjs.com/generating-provenance-statements) says that provenance "does not guarantee the package has no malicious code", and offers instead "a verifiable link to the package's source code and build instructions". The now-retired [SLSA v1.0 threat model](https://slsa.dev/spec/v1.0/threats), whose provenance format npm emits, is blunter. It defines a source threat as a change "that does not reflect the intent of the software producer", including one from an authorized individual, and then says: "SLSA v1.0 does not address source threats." Submitting an unauthorized change and compromising the source repository are both listed as threats v1.0 "does not address". The current [v1.2 threat model](https://slsa.dev/spec/v1.2/threats) adds a Source track that names this exact case, "Adversary directly pushes a change to a git repo’s main branch", and answers it with two-party review of the source, not with build provenance. It also says a malicious producer "cannot be directly mitigated through SLSA controls."

So nobody lied. The gap is between the claim and the feeling. A verified attestation reads like an endorsement, and what it actually certifies is narrower: this artifact came out of this pipeline. If an attacker can make the pipeline run, the certificate is accurate and the package is malware.

## Three ways into the pipeline

This started as a side question in my [dependency-risk-profiler issue #335](https://github.com/williamzujkowski/dependency-risk-profiler/issues/335) in August, while I was testing whether provenance could be a risk signal. (It couldn't. That is a separate, duller story.) In that August record (raw data not retained), the malicious versions whose attestations were still readable came from just three independent victims. On October 1 I re-fetched and decoded whatever survives.

| Case | How the code got into the pipeline | Signed ref | Trigger | Looks unusual? |
|---|---|---|---|---|
| jagreehal packages, 4 June | Orphan commits on new `snapshot-<hex>` branches, each adding its own `release.yml` | `refs/heads/snapshot-e8ed3490` and similar | `push` | Yes |
| `@injectivelabs/sdk-ts@1.20.21`, 8 July | Commits pushed to `master` from a maintainer account | `refs/heads/master` | `push` | No |
| `keyv@6.0.0`, 4 August | Commits on `main` from the compromised maintainer GitHub account, then a release | `refs/tags/v6.0.0` (August record; bundle now gone) | `release` | No |

**The jagreehal burst.** Between 00:25:27 and 00:30:21 UTC on 4 June, at least 280 versions of 53 packages maintained by the npm account `jagreehal` were published. (That counts packages npm search still lists; anything removed wholesale is invisible to it.) 204 of them are no longer on the registry. The 76 that remain all carry a provenance attestation, an npm deprecation notice and a 157-byte `binding.gyp` at the package root (the payload mechanism [StepSecurity described](https://www.stepsecurity.io/blog/binding-gyp-npm-supply-chain-attack-spreads-like-worm)). Every one's registry SHA-512 matches its attestation's subject digest. The provenance names seven genuine repositories, with the runs and commits to match. Each commit has no parent and touches exactly two files: `.github/workflows/release.yml` and `_index.js`.

**Injective.** The malicious 1.20.21 was built by `.github/workflows/publish.yaml` from `refs/heads/master` on a `push`, exactly like the clean 1.20.20 the previous day. The attested commit is in `master`'s history today. [StepSecurity's analysis](https://www.stepsecurity.io/blog/injective-npm-supply-chain-attack-18-packages-backdoored-to-steal-crypto-wallet-keys) traces the commits to an existing maintainer account and the publish to the repository's own trusted-publisher pipeline. In the signed provenance, the two releases differ only in tarball digest, commit hash and run ID. None of those fields tells you which one to trust. Injective published a clean 1.20.23 49 minutes later.

**keyv.** [Socket](https://socket.dev/blog/popular-npm-packages-in-the-keyv-and-cacheable-namespaces-compromised-in-active-supply-chain) reports the maintainer account was compromised, and [Endor Labs](https://www.endorlabs.com/learn/npm-malware-compromises-keyv-and-cacheable-with-500m-weekly-downloads-and-spreads-to-hundreds-of-packages) says the first wave went out "through the project's legitimate GitHub Actions OIDC trusted publishing pipeline after a commit to `main`", with "valid npm signatures and SLSA provenance." keyv's [release workflow at the time](https://github.com/jaredwray/keyv/blob/90109616a94f6774c172c5f457b2195d5801d508/.github/workflows/release.yaml) ran on `release: published` (or a manual `workflow_dispatch`), and its publish job already named a GitHub environment, as it still did at the attacker's release commit. Whatever rules that environment had, they did not stop a release made from the maintainer's own account. [Snyk's write-up](https://snyk.io/blog/inside-keyv-npm-compromise-preinstall-malware-trusted-provenance-ide-hooks/) puts the boundary precisely: "provenance can faithfully attest a build whose source or workflow context has already been compromised." Socket's is shorter: "provenance attests build integrity, not source integrity."

## Why an orphan branch could publish

npm's trusted-publisher configuration asks for an owner, a repository and a workflow filename, plus an optional environment name. It does not ask for a branch.

<div class="flow" role="group" aria-label="How a workflow on an attacker branch obtains a publish credential">
  <div class="flow-node"><b>Push access to the repository</b><i>a stolen account or token is enough</i></div>
  <div class="flow-node"><b>New orphan branch</b><i>carries its own copy of release.yml</i></div>
  <div class="flow-node"><b>That copy runs on push</b><i>main's branch filter is in main's copy</i></div>
  <div class="flow-node is-gate"><b>npm trusted publisher check</b><i>repository and workflow filename match</i></div>
  <div class="flow-node is-bad"><b>Publish accepted</b><i>Sigstore certificate names the snapshot ref</i></div>
</div>

The pre-incident `release.yml` on autotel's `main` [triggered only on pushes to `main`](https://github.com/jagreehal/autotel/blob/35a8a119f3e0dc0e5374e928efd4c91abce24fac/.github/workflows/release.yml). That filter lives inside the file. A push to another branch runs that branch's copy of the file, and the attacker wrote that copy. Nothing in npm's configuration asks which branch the copy came from. [Corgea documented the same move](https://corgea.com/research/redhat-cloud-services-npm-miasma-shai-hulud-worm) against Red Hat Cloud Services packages compromised on 1 June: orphan commits, a release workflow "triggered on attacker-controlled branch pushes", valid provenance at the end.

The fix the maintainer adopted is the one GitHub supports for exactly this. autotel's [current release workflow](https://github.com/jagreehal/autotel/blob/f5cf12a4bd8b859ea43785af1ea46cb50d406564/.github/workflows/release.yml) pairs npm's "Environment name" setting with a `release` environment restricted to `main` and gated on a required reviewer, so "a workflow running from any other branch cannot obtain the OIDC claim npm requires." GitHub's [environment docs](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments) describe those deployment-branch rules and required reviewers. The gate is only as independent as its reviewer. If the account an attacker holds can also approve the deployment, the environment adds a click rather than a check, so the reviewer has to be a second person.

## What a consumer can actually check

Provenance is still evidence, as long as you read more than whether it verified. After `npm audit signatures` has verified the bundle, the signed provenance statement tells you where the build came from:

```sh
curl -s https://registry.npmjs.org/-/npm/v1/attestations/autotel-audit@0.1.15 \
  | jq -r '.attestations[] | select(.predicateType == "https://slsa.dev/provenance/v1")
           | .bundle.dsseEnvelope.payload' | base64 -d \
  | jq -c '.predicate.buildDefinition | {ref: .externalParameters.workflow.ref,
           workflow: .externalParameters.workflow.path,
           trigger: .internalParameters.github.event_name,
           commit: .resolvedDependencies[0].digest.gitCommit}'
```

For 0.1.15 that prints `refs/heads/snapshot-e8ed3490`; for the clean 0.1.14, `refs/heads/main`. The same values appear in the Fulcio certificate as the Source Repository Ref and Build Trigger extensions. Four checks follow from those fields:

- **Ref against the project's habit.** A release from `snapshot-e8ed3490` when every previous one came from `main` or a `v*` tag is worth a pause. This catches the jagreehal case.
- **Commit ancestry.** GitHub's compare API reports "No common ancestor" between autotel's `main` and the attested orphan commit. A release commit that is not in the default branch's history has some explaining to do.
- **Trigger against the project's habit.** A project that releases on `release` events suddenly publishing on `push` is a change worth noticing.
- **Attestation disappearing.** `cline@2.3.0` was published with a [stolen npm token](https://github.com/cline/cline/security/advisories/GHSA-9ppg-jx86-fqw7). Its neighbours 2.2.3 and 2.4.0 carry attestations; 2.3.0 carries none. npm only issues provenance from a supported CI runner, so a token that bypasses CI also bypasses provenance. A downgrade from attested to unattested is a cheap signal, and here it was the right one.

Run those against the three cases and they catch one of them. Injective, and keyv by its August record, pass every field-level check, because the attacker went through the usual release path. (keyv's release commit, ee2681a9, now shows as diverged from `main`, so the ancestry check would flag it today, well after the fact.) That is the existence claim, at n=3: valid provenance on malware that the signed fields cannot distinguish from an ordinary release.

## Why this is three cases and not a rate

I would like to tell you what fraction of compromised npm releases carry valid provenance. The data will not support it. In the August measurement recorded in #335, 5,457 of the 5,573 malicious versions listed in Datadog's [malicious-software-packages dataset](https://github.com/DataDog/malicious-software-packages-dataset) could no longer be read, because npm removes them. The survivors are selected on "npm has not removed it yet", which may well correlate with how the version was published, so the attested share among them describes the survivors, not the attacks.

The attestation endpoint does not help with the missing ones. In August, `keyv@6.0.0`'s attestation still returned 200 after the version was removed. On October 1 the same URL returns 404, as do the four removed ai-sdk-ollama versions from the jagreehal burst. A 404 can mean "never attested" or "purged", and the response does not say which.

Mirrors are worse. Asking npmmirror for the removed `@antv/dumi-theme-antv@0.9.4` returns a document labelled 0.9.4 whose tarball URL and SHA-1 are 0.8.4's. Measure from that without checking the hash and you have fabricated a result with full confidence. Removal is the registry doing its job; it just also decides which evidence survives.

## Where that leaves provenance

Keep it on. Provenance gave the cline publish a mechanical tell, and it made the jagreehal publishes look odd to anyone who read the ref. It is also the reason I could reconstruct any of this months later: the certificates still name the exact run and commit, even though the snapshot branches are gone.

Just read it as a receipt. On the consuming side, record the ref and trigger each dependency normally publishes from, and treat a change or a missing attestation as a reason to hold the update. Holding new versions for a few days, as in [Patch Fast, Pull Slow](/posts/2026-05-07-patch-fast-pull-slow-defending-copy-fail-shai-hulud), gives the people who do read refs time to notice. On the publishing side, the controls that address the intent gap sit before the pipeline: an environment limited to the release branch, with a reviewer who is not the person pushing, or npm's [staged publishing](https://docs.npmjs.com/staged-publishing), which holds a CI publish until a maintainer approves it with npm two-factor authentication. The [trivy-action compromise](/posts/2026-03-21-trivy-supply-chain-compromise-ai-assisted-investigation) showed CI as the place secrets leak from. Trusted publishing makes CI the place releases come from, which raises the price of the same accounts. A signature tells you who handled the package. Whether they should have is a separate question.

The October 1 measurements, scripts and decoded certificate fields are in the [research note](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/main/docs/research/2026-10-01-npm-provenance-pipeline-not-intent.md). The August figures are as recorded in #335, whose raw data was not kept.
