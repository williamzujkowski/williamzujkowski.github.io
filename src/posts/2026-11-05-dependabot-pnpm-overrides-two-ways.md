---
title: "The Override Was Still in package.json"
date: 2026-11-05
draft: false
author: William Zujkowski
description: "A one-line pnpm override kept this site off a vulnerable fflate. Dependabot's lockfiles lost it in two ways, and only one of them failed the build."
tags:
  - security
  - supply-chain
  - npm
  - devops
---

A pnpm override is one line in `package.json` that tells the package manager to ignore what a dependency asked for. This site has exactly one: `"satori>fflate": "0.7.5"`. Satori, the library that draws the social cards, pins `fflate` to exactly 0.7.3, and 0.7.3 is affected by [GHSA-px8p-9vwx-vf98](https://github.com/advisories/GHSA-px8p-9vwx-vf98). The override swaps in the patched release for satori and nobody else.

The line sits in `package.json`, where it is easy to read and review. The decision it makes is recorded in `pnpm-lock.yaml`, a file that Dependabot rewrites every week. Since the override arrived, every Dependabot lockfile in this repository has lost it in two ways. One fails every check that installs dependencies. The other moves satori back to the vulnerable version, and no error mentions it.

<!-- DOODLE: a sticky note on a blueprint being fed through a photocopier; the copy slides out the other side without the note, and a small builder is already reaching for the copy -->

## A fix for a function nobody calls

First, the stakes, because they are smaller than the advisory's CVSS 3.1 score of 7.5 suggests. GitHub itself rates it medium, with a CVSS 4.0 score of 6.6. The advisory describes an infinite loop in fflate's `unzipSync()` when it parses a malformed ZIP64 archive. It lists `>= 0.7.0, < 0.7.5` as affected on the 0.7 line. When the alert arrived, [issue #563](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/563) checked the installed source: satori imports `inflateSync`, not `unzipSync`, and this site runs satori only at build time, on fonts from its own repository. A fresh install of satori 0.33.4 still imports only that one function from fflate.

So the override guards against a bug in a function this site never calls, which is the best kind of vulnerability to lose control of. That makes it a cheap test subject. Nothing below put a reader at risk. The mechanism is the same one you would use for a bug that did matter, and that is the reason to examine it.

## The loud half

From August 25 on, every Dependabot pull request that touched the lockfile failed all five site checks, each within thirty seconds of starting, with this error:

```text
ERR_PNPM_LOCKFILE_CONFIG_MISMATCH  Cannot proceed with the frozen installation.
The current "overrides" configuration doesn't match the value found in the lockfile
```

The bot had written a lockfile without its top-level `overrides:` block, while `package.json` still declared it. `pnpm install --frozen-lockfile` compares the two and refuses. The message is accurate, but it does not say what produced the lockfile or how to fix it.

The onset is odd. On August 23, [#523](https://github.com/williamzujkowski/williamzujkowski.github.io/pull/523) and [#524](https://github.com/williamzujkowski/williamzujkowski.github.io/pull/524) arrived with the header intact, as had #446 and #482 before them. Two days later [#530](https://github.com/williamzujkowski/williamzujkowski.github.io/pull/530) arrived without it. Between those, this repository's `package.json` changed only in dependency versions and `dependabot.yml` didn't change at all. Whatever changed, it wasn't on this side. The same error class is not new upstream, either: [dependabot-core#13036](https://github.com/dependabot/dependabot-core/issues/13036), open since September 2025, reports Dependabot dropping `injectWorkspacePackages` from a pnpm lockfile's settings, with the same `ERR_PNPM_LOCKFILE_CONFIG_MISMATCH`.

My first diagnosis was wrong. [PR #533](https://github.com/williamzujkowski/williamzujkowski.github.io/pull/533) blamed a duplicated `overrides` block in `package.json` and removed it. Dependabot opened [#537](https://github.com/williamzujkowski/williamzujkowski.github.io/pull/537) 3 minutes 43 seconds after that merge, without the duplicate, and it failed identically. The duplicate was dead config and deserved to go. It was not the cause.

## The silent half

The satori override arrived on September 8. Since then Dependabot has written six lockfiles across four pull requests: the original commit on [#564](https://github.com/williamzujkowski/williamzujkowski.github.io/pull/564) (`d0160c5`), #635, #662, and three versions of [#638](https://github.com/williamzujkowski/williamzujkowski.github.io/pull/638), the bot force-pushing it twice more after the fix below had merged. In all six, the header is missing and so is the override's effect:

```text
satori@0.33.4:                       # 0.33.5 in #662
  fflate: 0.7.3                      # main has 0.7.5
'@shuding/opentype.js@1.4.0-beta.0':
  fflate: 0.7.5
```

That second entry matters. Satori depends on `@shuding/opentype.js`, which depends on fflate `^0.7.3`, and in these lockfiles it kept 0.7.5. A check that asks whether the patched version is present passes. The patched version is present. It just isn't the one satori loads.

The earlier record held a misleading piece of evidence too. Issue [#540](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/540) originally argued that the bot applied overrides correctly and only failed to save the header. Its proof was `fast-uri` 3.1.7 in #537's tree, which the issue said "can only be there because of the `^3.1.6` override". The npm registry shows 3.1.7 [published on September 2](https://registry.npmjs.org/fast-uri), two days before #537. It was already the newest 3.x release, so a fresh resolution would have chosen it with or without the override. That observation could not tell an applied override from an irrelevant one.

## The loud half is what protects you

The red build is useful as long as the repair is a real regeneration. The trouble starts when someone takes the error message literally and only restores the missing header.

To see what pnpm does with each case, I built a [small lab](https://github.com/williamzujkowski/research-labs/tree/RESEARCH_LABS_COMMIT/labs/pnpm-override-drift) with one manifest (satori 0.33.4 plus the override) and three lockfiles, run offline against pnpm 10.33.0. The `no-header` file is a simulation. It was made by resolving once without the override and then restoring the manifest, which reproduces the missing header and both fflate edges from the real bot lockfiles. It does not run Dependabot. `header-only` is that file with the three-line `overrides:` block pasted back in.

| Check | faithful | no-header | header-only |
| --- | --- | --- | --- |
| `overrides:` header present | pass | **fail** | pass |
| `fflate@0.7.5` present anywhere | pass | pass | pass |
| `pnpm install --frozen-lockfile` | pass | **fail** | pass, links satori to 0.7.3 |
| `pnpm install --lockfile-only` changes the lockfile | no | yes, restores 0.7.5 | no |
| `pnpm dedupe --check` | pass | **fail** | **fail** |
| satori's fflate edge equals the override | pass | **fail** | **fail** |

The third column is the one to remember. With the header restored, the frozen install exits 0 and links fflate 0.7.3 under satori. Running `pnpm install --lockfile-only` on that file changes nothing, so regenerating the lockfile and diffing it passes too. The [pnpm docs](https://pnpm.io/10.x/cli/install#--frozen-lockfile) say a frozen install fails "if the lockfile is out of sync with the manifest". In this run, the check compared the recorded override settings and did not re-check the edge the override controls. That is a fair design for a tool that expects to have written its own lockfile. Hand-spliced YAML falls outside that expectation.

<div class="flow" role="group" aria-label="Two ways to repair a Dependabot lockfile that lost its overrides">
  <div class="flow-node"><b>Bot lockfile</b><i>no overrides header; satori on fflate 0.7.3</i></div>
  <div class="flow-node is-gate"><b>Frozen install refuses</b><i>ERR_PNPM_LOCKFILE_CONFIG_MISMATCH</i></div>
  <div class="flow-branch" role="group" aria-label="Repair choices">
    <div class="flow-leg" data-branch="Regenerate" role="group" aria-label="Regenerate with pnpm"><div class="flow-node is-good"><b>Header and edge restored</b><i>satori back on 0.7.5</i></div></div>
    <div class="flow-leg" data-branch="Paste header" role="group" aria-label="Restore only the header"><div class="flow-node is-bad"><b>Frozen install green</b><i>satori still on 0.7.3</i></div></div>
  </div>
</div>

`pnpm dedupe --check` catches both bad files in the lab, and pnpm documents it as exiting nonzero ["if changes are possible"](https://pnpm.io/10.x/cli/dedupe). It is less useful on a real dependency tree. Against this site's own lockfile it also fails on `main`, flagging ordinary duplicates such as two vite versions. A gate that is already red tells you nothing new.

`pnpm audit --prod` also flags both bad files in a scratch run, reporting the path `.>satori>fflate`. It works here because an advisory exists for this exact package. The edge check works for any override, including one written for a reason no advisory database knows about.

## Check the edge, not the line

The repository now runs [`scripts/ci/check-lockfile-overrides.py`](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/main/scripts/ci/check-lockfile-overrides.py) before the frozen install. It reads both files and asserts two things: the header matches `package.json`, and for every `parent>child` override, the version the parent actually resolves is at least the override's version. It uses only Python's standard library, so it needs nothing installed, and it can only add a failure. On September 29, Dependabot opened #662, and the check reported both defects:

```text
- pnpm-lock.yaml has no `overrides:` block, but package.json declares 1: satori>fflate.
- RESOLUTION REGRESSED: satori resolves fflate to 0.7.3, below the overridden 0.7.5. The `overrides:` header alone does not catch this.
```

The fix it prints is `cd astro-site && pnpm install --lockfile-only`. In the lab, that command restores the header and 0.7.5, but only when the header is missing. Run it on a file whose header was already pasted back and it changes nothing, as the table shows. The repair for that file is to discard it, start again from the untouched bot lockfile or from `main`'s, and then regenerate. The order matters. Regenerate first, then confirm the edge.

## Nine of the ten were doing nothing

While building that check, the repository measured its override block instead of assuming it worked. [The commit](https://github.com/williamzujkowski/williamzujkowski.github.io/commit/38e324bf60183d7cbd53255b7428a16ee90b0892) records ten entries. Two, `uuid` and `dompurify`, named packages that were not in the tree at all. Seven were floors or ranges, such as `vite: '>=8.0.13'` and `fast-uri: ^3.1.6`, that natural resolution already satisfied. Only `satori>fflate` changed the result. The other nine were removed.

The way pnpm [matches overrides](https://pnpm.io/10.x/settings#overrides) explains how an entry can parse cleanly and still change nothing. An override does not inspect the resolved version. It rewrites a request before resolution starts. In [pnpm 10.33.0's source](https://github.com/pnpm/pnpm/blob/v10.33.0/hooks/read-package-hook/src/createVersionsOverrider.ts), a key such as `yaml@<2.8.3` applies wherever a dependent's declared range [intersects](https://github.com/pnpm/pnpm/blob/v10.33.0/hooks/read-package-hook/src/isIntersectingRange.ts) `<2.8.3`. A `parent>child` key applies only inside packages whose name and version match the parent selector. So `yaml@<2.8.3: '>=2.8.3'` still turns a `^2.0.0` request into `>=2.8.3`. If the newest `^2.0.0` release is already above the floor, the tree comes out the same either way. pnpm gives no warning because nothing is wrong. These were CVE pins written when the CVEs were current. Upstream fixed them and the pins stayed, like a wet-paint sign on a wall that dried months ago.

Removing them did give something up. A floor that changes nothing today can still block a future downgrade. The commit describes the choice as shrinking "the surface the bot can silently re-resolve from 10 pins to 1".

## What this does and doesn't show

The upstream report, [dependabot-core#16232](https://github.com/dependabot/dependabot-core/issues/16232), is filed from this repository with the manifests, lockfiles and failing run. It was still open with no replies when I checked on October 1. The hosted updater's pnpm version and code path are unknown. The evidence is one repository, one parent-scoped override and pnpm lockfile v9. It does not show how Dependabot treats a bare override. The lab demonstrates pnpm's behaviour on lockfiles shaped like the bot's, not the bot's own code.

My conclusion is narrower than "don't use Dependabot". An override is a security control stored in a file that a bot regenerates. If the only check is whether the override line exists, the control can disappear without anyone noticing. Check the edge it is supposed to change, using the resolved version the parent actually gets. If you use a cooldown and a frozen install, as I argued in [Patch Fast, Pull Slow](/posts/2026-05-07-patch-fast-pull-slow-defending-copy-fail-shai-hulud), both still help. Neither one checks this edge.
