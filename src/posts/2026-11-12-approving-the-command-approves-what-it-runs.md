---
title: "Approving the Command Approves What It Runs"
date: 2026-11-12
draft: false
author: William Zujkowski
description: "A permission rule matches the command an agent types. A small lab traces what one approved npm install then started and wrote, with and without a sandbox."
tags:
  - security
  - ai
  - supply-chain
  - npm
---

The [approval-scope lab](https://github.com/williamzujkowski/research-labs/tree/6540fc4b645d8c74b0240254af92d25d79ac7232/labs/approval-scope) is one synthetic JavaScript project and one command a coding agent might ask to run: `npm install`. The project's `postinstall` and `prepare` scripts, and a dependency's own `postinstall`, each write a marker file and nothing else. The `prepare` script also installs a git pre-commit hook, the way hook managers such as simple-git-hooks do.

Under `strace -f`, that one command started three lifecycle scripts. They wrote markers inside the project and in a directory beside it, and left a hook in `.git/hooks`. A later `git commit` ran the hook. npm's own output named two of the three scripts; the dependency's ran without a word.

None of that is a bug. npm documents every step of it. What interested me is the approval. A permission rule such as `Bash(npm install *)` names a command, and the command turned out to be the front door of a fairly large house.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/stamped-box.png'); width: min(260px, 66%); aspect-ratio: 420/457; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">Approved. All of it, apparently.</p>

<div class="flow" role="group" aria-label="What one approved install command ran in the lab">
  <div class="flow-node is-gate"><b>Approved text</b><i>npm install</i></div>
  <div class="flow-parallel" role="group" aria-label="Lifecycle scripts the install started">
    <div class="flow-node is-bad"><b>Dependency postinstall</b><i>not shown by npm</i></div>
    <div class="flow-node"><b>Project postinstall</b><i>markers in and out</i></div>
    <div class="flow-node"><b>Project prepare</b><i>installs a git hook</i></div>
  </div>
  <div class="flow-node is-gate"><b>Next approved text</b><i>git commit</i></div>
  <div class="flow-node is-bad"><b>Hook runs</b><i>writes its own marker; neither rule named it</i></div>
</div>

## What the rule matches

Claude Code is explicit about this. Its [permissions documentation](https://code.claude.com/docs/en/permissions#bash-rule-limits) says a Bash rule "matches the command text Claude writes" and that a deny or ask rule "isn't a security boundary around the program." The same page says Read and Edit deny rules don't cover "arbitrary subprocesses that read or write files indirectly, like a Python or Node script that opens files itself," and sends you to the sandbox for OS-level enforcement. Its wildcard rules also mean a trailing ` *` matches the bare command, and the `*` stands in for any text. So `Bash(npm install *)` approves `npm install`, `npm install --ignore-scripts` and `npm install` followed by whatever package name the agent types next.

The rule is honest about its scope. The trouble is how the decision reads afterwards. Approving `npm install` sounds like approving an install. What it authorizes is whatever the project's manifest, and every dependency's manifest, says happens during one.

## What ran

Each arm copies the fixture into a fresh git repository, runs one install under `strace -f`, then runs `git commit` the same way. The [retained run](https://github.com/williamzujkowski/research-labs/blob/6540fc4b645d8c74b0240254af92d25d79ac7232/docs/evidence/approval-scope-2026-10-01/plain.json) used npm 10.9.8, pnpm 10.33.0 (always with `--frozen-lockfile`), Node 22 and git 2.39.5, offline, nonroot, with capabilities dropped.

| Command | Scripts run (named in output) | Marker outside | Hook fired at commit |
| --- | --- | --- | --- |
| Each install with `--ignore-scripts` | 0 | no | no |
| `npm install`, `npm ci` | 3 (2) | yes | yes |
| npm with `--foreground-scripts` | 3 (3) | yes | yes |
| `pnpm install` | 2 (2) | yes | yes |
| pnpm, dependency allowlisted | 3 (3) | yes | yes |

The `--ignore-scripts` controls ran first, and the harness refuses to continue if a control exits non-zero, goes untraced, or shows any script or marker. A positive arm through the same tracer finds all three scripts, and hand-planted defects in the trace parser turn its tests red.

The quiet one is npm's dependency script. npm's [`foreground-scripts`](https://docs.npmjs.com/cli/v10/using-npm/config#foreground-scripts) setting exists to run installed packages' build scripts "in the foreground process, sharing standard input, output, and error with the main npm process." With it, the dependency's command appears in the output. Without it, the output said `added 1 package` and nothing about the script.

pnpm changed its default in 10.0.0. The [release notes](https://github.com/pnpm/pnpm/releases/tag/v10.0.0) say "Lifecycle scripts of dependencies are not executed during installation by default". The dependency's script did not run, and pnpm printed a warning naming the package it skipped. The project's own `postinstall` and `prepare` still ran, as they should: they belong to the project, and the project is the thing you cloned.

## Old news, new button

Nobody who has read npm's [scripts page](https://docs.npmjs.com/cli/v10/using-npm/scripts) will be surprised by any of this. It lists `preinstall` through `postprepare` for both `npm install` and `npm ci`, and `ignore-scripts` is an ordinary documented setting. What changed is who presses the button, and what the button's label tells them.

Zhang and six co-authors call it [approval laundering](https://arxiv.org/html/2609.28586v1) (arXiv 2609.28586v1, a September 2026 preprint): a durable record "faithfully names the entry invocation yet omits effects exercised within its workflow." Their opening case is the same shape as this lab: an agent requested approval for `pnpm --dir <fixed-sha-workspace> install --frozen-lockfile` in Vite, and the approved install invoked `postinstall` (simple-git-hooks, per their transcript) and wrote a workspace file, `node_modules/.modules.yaml`. Across 111 approval/trace pairs, records that omitted at least one observed effect fell from 40 when read as explicit fields to 17 with command semantics, and to 13 when their post hoc analysis added metadata that was available at decision time. They disclosed the product-specific findings to Anthropic, GitHub and Alibaba. The paper says it ships no artifact, so this lab is a smaller, independent look at the mechanism, not a reproduction of their benchmark.

Their proposed fix binds predicted effects into the approval record before the decision, and they demonstrate it through a Claude Code `PreToolUse` hook. I didn't build that. I measured the layer that already exists.

## The sandbox sees the children

Unlike a rule, Claude Code's [sandbox](https://code.claude.com/docs/en/sandboxing) applies to shell commands "and the processes they start." By default it allows writes to the working directory and "a per-user temp directory," and keeps [protected paths](https://code.claude.com/docs/en/sandboxing#protected-paths) write-denied inside them, including "`hooks` and `config` inside `.git`."

I ran the installs inside [`@anthropic-ai/sandbox-runtime`](https://github.com/anthropics/sandbox-runtime) 0.0.78, the open-source package those docs say the sandbox is built on, with settings that mirror the documented defaults. This is the runtime on its own, not Claude Code, which computes its own configuration on top. It ran inside Docker with seccomp and AppArmor relaxed, in the runtime's `enableWeakerNestedSandbox` mode, which its README says "considerably weakens security"; and the lab allowed writes to all of `/tmp`, wider than the documented per-user temp directory. Every script still ran. Markers inside the project were written. The marker beside the project and the hook both failed with `EROFS`, and the next `git commit` ran nothing ([sandbox evidence](https://github.com/williamzujkowski/research-labs/blob/6540fc4b645d8c74b0240254af92d25d79ac7232/docs/evidence/approval-scope-2026-10-01/sandbox.json)).

So the sandbox constrains where effects land, not whether code runs. Writes inside the project stay allowed by design, and the project is what you run next: `node_modules`, the build scripts, anything a `postinstall` chose to edit.

Two documented defaults decide whether you get even that. The sandbox is off until you enable it. And "if the sandbox can't start because a dependency is missing or the platform is unsupported, Claude Code runs commands without sandboxing," unless `sandbox.failIfUnavailable` is set. In the lab, with bubblewrap installed but user namespaces refused, the runtime exited with an error and the install never started; Claude Code's fallback is documented for a missing dependency or unsupported platform, which this did not test.

One design choice is worth noticing. With the sandbox on and `autoAllowBashIfSandboxed` at its default of `true`, sandboxed commands skip the whole-tool prompt (content-scoped ask rules still prompt); the permissions page says "the sandbox boundary substitutes for that whole-tool prompt." For this problem that is the right trade. A boundary can be described before anything runs. A command's consequences mostly can't.

## The same gap, one layer up

Agent frameworks show the pattern in a different place. Khan's [*Stop Means Stop*](https://arxiv.org/abs/2607.14166v3) (arXiv 2607.14166v3, preprint, [MIT artifact](https://github.com/sajjadanwar0/soundgate-paper)) finds that an approval gate pauses its own branch while a sibling's side effect commits during the pause, in every framework that ships a pre-execution gate: five of the six it tested. In a 1,000-workflow sweep on LangGraph, effects in the same superstep as the gate leaked 577 times out of 577; effects in later supersteps leaked 0 of 331. The author is careful: "Whether any individual gap is a bug or a deliberate design is for maintainers to say." I did not reproduce it. It is the same lesson, though: an approval covers what it names.

## What to put in the rule

Approve the form that runs nothing. An exact rule such as `Bash(npm ci --ignore-scripts)` grants less than `Bash(npm install *)`, and a package that needs its build step becomes a separate, named decision. On pnpm 10 the allowlist (`onlyBuiltDependencies`) already is that decision, so review changes to it like code. Root scripts still run either way, so read `scripts` in `package.json` before approving any install in a repository you didn't write. My [agent-controls post](/posts/2026-07-23-agent-controls-as-oscal) deferred human-approval gates; this is the first concrete rule I'd write for one.

To see what an install would run without running it, install with scripts off and ask npm for every package declaring one of the seven scripts `npm install` runs:

```sh
npm ci --ignore-scripts
npm query ':attr(scripts, [preinstall]), :attr(scripts, [install]), :attr(scripts, [postinstall]), :attr(scripts, [prepublish]), :attr(scripts, [preprepare]), :attr(scripts, [prepare]), :attr(scripts, [postprepare])'
```

On the fixture that returns the project and `node_modules/canary-dep`, with their scripts. It reads declared scripts only: the same scripts page says npm defaults a package's `install` to `node-gyp rebuild` when it ships a `binding.gyp` and defines no `install` or `preinstall` script of its own. To see what an approval actually ran, trace it and keep the successful `sh -c` launches:

```sh
strace -f -qq -s 4096 -e trace=execve -o install.trace npm ci
grep '"-c", .* = 0$' install.trace | grep -oE '"-c", "([^"\\]|\\.)*"'
```

That printed exactly the three scripts in the lab. The `= 0` filter drops the failed `PATH` lookups that otherwise repeat each line several times, `-s 4096` stops strace cutting strings at its default 32 characters, and the pattern keeps a script containing escaped quotes whole. After any install, look in `.git/hooks`. An approved `git commit` runs whatever hook is there. Per [githooks](https://git-scm.com/docs/githooks), `--no-verify` skips `pre-commit` and `commit-msg` only; `prepare-commit-msg` "is not suppressed by the --no-verify option," and `post-commit` still runs.

Then turn the sandbox on, with `failIfUnavailable`, so the layer that sees children is the one doing the containing. My [sandbox survey](/posts/2026-07-02-agentic-ai-sandbox-secret-proxying-gap) covers what it doesn't do for secrets, and [*Provenance Attests the Pipeline, Not the Intent*](/posts/2026-10-15-npm-provenance-attests-the-pipeline) makes the matching point about signatures.

## Limits

One fixture, one dependency and one hook pattern, on linux/amd64 with no network, so network effects are out of scope. The sandbox arms needed relaxed seccomp and AppArmor for bubblewrap and the runtime's `enableWeakerNestedSandbox` mode, which binds the existing `/proc`; the filesystem rules measured here are the same mechanism, process isolation is not, and the lab says nothing about it. No agent and no Claude Code binary ran, so nothing here measures what a permission prompt displays. A real hook manager may fail or warn where these payloads catch their own errors.

Against the falsifier in the [proposal](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/673): the permission layer, by its documented design, neither constrains nor surfaces the transitive effects. That is a reading of the documentation: the proposal suggested testing a real harness, and this lab did not. sandbox-runtime, run standalone, constrained two of the three places they landed and left the third, the project itself, writable. Nothing surfaced the dependency's script in npm's default output.

The command line is the part of an install you already knew.
