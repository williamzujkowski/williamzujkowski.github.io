---
title: "The Command Said It Worked"
date: 2026-10-08
draft: false
author: William Zujkowski
description: "Five commands this site published reported success while doing nothing. A small container lab reproduces four, and the cheap defense is running each command once where it must fail."
tags:
  - security
  - linux
  - homelab
  - devops
---

On September 24 I merged [a pull request](https://github.com/williamzujkowski/williamzujkowski.github.io/pull/658) that corrected eight defects across six posts on this site. Four of the eight share a shape. You copy the command, run it, and get exit status 0 and no error. Then you move on, because nothing told you not to, and whatever the command was meant to do has not happened. A fifth command of the same kind, in the Wazuh post, did not make it into that pull request. It is corrected alongside this one.

This post is the catalogue, plus a [small lab](https://github.com/williamzujkowski/research-labs/tree/ea153aa2d92af0a6c3ce408ac6f5277f179eebf0/labs/exit-status) that reproduces four of the five in a container. It ends with the habit I'd use to stop publishing more of them: before a command goes into a post, run it once in a situation where it has to fail, and watch whether it says so.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/sad-extinguisher.png'); width: min(260px, 66%); aspect-ratio: 440/422; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">Inspected. Passed. Mostly decorative.</p>

<div class="flow" role="group" aria-label="One exit status, two outcomes the reader cannot tell apart">
  <div class="flow-node">Reader runs the published command</div>
  <div class="flow-node is-gate"><b>Exit status 0</b><i>no error printed</i></div>
  <div class="flow-branch" role="group" aria-label="What actually happened">
    <div class="flow-leg" data-branch="Worked" role="group" aria-label="Worked"><div class="flow-node is-good"><b>backup.gpg</b><i>131 bytes of ciphertext</i></div></div>
    <div class="flow-leg" data-branch="Did nothing" role="group" aria-label="Did nothing"><div class="flow-node is-bad"><b>backup.gpg</b><i>0 bytes</i></div></div>
  </div>
  <div class="flow-node">Reader moves on either way</div>
</div>

## Five ways to succeed at nothing

Every one of these exits 0:

| Published command | What actually happened | What reports the failure |
| --- | --- | --- |
| `set -e`, then `suricata-update ... \| tee log` | A failed update is ignored; the pipeline's status is `tee`'s | `set -o pipefail` |
| `gpg --symmetric ... seeds.txt > backup.gpg` | `backup.gpg` is empty; the ciphertext is in `seeds.txt.gpg` | `--output backup.gpg`, then decrypt it |
| `pihole -a adlist add <url>` on v6 | Help text printed; no list added | Nothing at the CLI; check the Lists page |
| `curl -sO <url>` that answers 403 | The XML error is saved as `docker-compose.yml` | `curl -f` exits 22 |
| `iptables -I DOCKER-USER ... --dport 22 -j DROP` | The rule sits in a chain container-to-host traffic never enters | An `INPUT` rule on the container's bridge (`docker0` is only the default one), not yet verified |

None of these is obscure, and none of them is new. Each one is behavior that the tool's documentation or source states plainly, and that someone, in this case me, did not check.

The history makes that sharper. Two of the four commands were not in the posts as first published. The Pi-hole line arrived on 4 September 2026 in [#544](https://github.com/williamzujkowski/williamzujkowski.github.io/pull/544), a pass correcting that post's blocklist instructions. The `DOCKER-USER` rule arrived on 17 August 2026 in [#470](https://github.com/williamzujkowski/williamzujkowski.github.io/pull/470), another correction batch. The Suricata pipeline is older, but on 4 September 2026 [#538](https://github.com/williamzujkowski/williamzujkowski.github.io/pull/538), a pass removing a fabricated procedure from that post, added the comment calling `set -e` "the check that matters". So the reply to "it's all in BashFAQ" is that these were not stale posts left behind by the manuals. Each came from a pass whose job was to fix the post, and each left a command that one failing run would have exposed.

**The pipeline.** The [Suricata post](/posts/2025-08-25-network-traffic-analysis-suricata-homelab) wrapped its rule update in `set -e` and called that "the check that matters". The [Bash manual](https://www.gnu.org/software/bash/manual/html_node/Pipelines.html) is plain about it: "The exit status of a pipeline is the exit status of the last command in the pipeline, unless the pipefail option is enabled." The last command was `tee`, which is very good at writing logs and has no opinion on what is in them. Greg Wooledge's [BashFAQ/105](https://mywiki.wooledge.org/BashFAQ/105) has carried the same warning for years: "Using a pipe makes no difference, as only the rightmost process is considered."

**The backup.** The [Bitwarden post](/posts/2025-09-01-self-hosted-bitwarden-migration-guide) told you to encrypt your TOTP seeds with a shell redirect. Given an input file and no `--output`, gpg names its own output by appending `.gpg` to the input name; that logic is `open_outfile` in [GnuPG 2.4.7's `g10/openfile.c`](https://github.com/gpg/gnupg/blob/gnupg-2.4.7/g10/openfile.c). The shell has already created `backup.gpg` for the redirect, and nothing ever writes to it. The plaintext stays where it was. Of the five, this is the one that fails on the worst possible day, because nobody opens a disaster-recovery file until there is a disaster.

**The blocklists.** The [Raspberry Pi post](/posts/2025-03-10-raspberry-pi-security-projects) used `pihole -a adlist add`, the v5 syntax, added eighteen months after [Pi-hole v6.0](https://github.com/pi-hole/pi-hole/releases/tag/v6.0) shipped on 18 February 2025. Its dispatcher has no `-a` case, so the argument falls through to `*) helpFunc`, and [`helpFunc` ends in `exit 0`](https://github.com/pi-hole/pi-hole/blob/2d81552f9f16fb5e12df31069078b43f0e826c3b/pihole#L460-L511). v6.4.3, the latest release on October 1, behaves the same way. The reader sees a screen of usage text, which looks enough like output to pass for it, then runs `pihole -g` and rebuilds gravity without either list.

**The download.** The [Wazuh post](/posts/2025-11-05-siem-homelab-wazuh-graylog-comparison) fetched its compose file with `curl -sO` from a URL that answers 403 with an XML `AccessDenied` body. It answered 403 when checked on October 1, and so did every Wayback Machine capture of that URL, the earliest from December 2025. Whether it ever served a compose file before then, the evidence does not say. The [curl manual](https://curl.se/docs/manpage.html) states the default without apology: "By default, curl does not consider HTTP response codes to indicate failure." So the error page is saved under the name you asked for, and curl exits 0. The failure does surface one step later: `docker compose config` on that 111-byte file stops with a YAML error and exits 1. The error points at the compose file, though, not at the download that wrote it.

**The firewall rule.** The [Docker hardening post](/posts/2025-12-17-docker-container-hardening-homelab) put a container-to-host SSH block in `DOCKER-USER`. Docker's [iptables documentation](https://docs.docker.com/engine/network/firewall-iptables/) says that in the `FORWARD` chain, Docker adds rules that "unconditionally jump to the DOCKER-USER, DOCKER-FORWARD and DOCKER-INGRESS chains", and the [iptables man page](https://ipset.netfilter.org/iptables.man.html) describes `INPUT` as the chain "for packets destined to local sockets". A container connecting to the host is local delivery, so the rule never sees it. The pull request records a measurement: the connection still succeeded and the counter did not move. The lab does not rerun that one; it needs `NET_ADMIN`, which the container deliberately lacks. Treat it as a source finding. The corrected post moves the rule to `INPUT -i docker0`, and that fix has not been run either. `docker0` is only the default bridge; Compose networks get their own `br-` interfaces. Verifying it takes the same negative control: put the `INPUT` rule on the container's actual bridge, try the connection again, and confirm it now fails and the rule's counter moves.

The same pull request fixed two inversions that belong to a different family. A [Vaultwarden](/posts/2025-09-01-self-hosted-bitwarden-migration-guide) comment implied that `DISABLE_ADMIN_TOKEN` would switch off the admin panel. Vaultwarden's [own template](https://github.com/dani-garcia/vaultwarden/blob/061694d0cb3bbf5d4c7e920c892824f0020cff83/.env.template#L451-L453) says "Enable this to bypass the admin panel security. This option is only meant to be used with the use of a separate auth layer in front." Set without that auth layer, it does the opposite of what the comment implied. The [eBPF post](/posts/2025-07-01-ebpf-security-monitoring-practical-guide) expected `apparmor_restrict_unprivileged_userns` to read 0, when [Ubuntu's announcement](https://ubuntu.com/blog/ubuntu-23-10-restricted-unprivileged-user-namespaces) uses 1 to turn the restriction on and 0 to disable it. Neither involves a failing command. They share the useful property that nothing errors.

## What the lab showed

The lab runs each published shape beside a corrected form in a digest-pinned Debian container: no network, read-only root, no capabilities, non-root user. The curl cases hit a throwaway HTTP server on the container's loopback that returns a synthetic 403. The Pi-hole cases run upstream's dispatcher, fetched by commit and hash-checked, with the three helper files it sources replaced by empty stubs, so only the argument handling executes.

The [October 1 run](https://github.com/williamzujkowski/research-labs/tree/ea153aa2d92af0a6c3ce408ac6f5277f179eebf0/docs/evidence/exit-status-2026-10-01) used bash 5.2.37, GnuPG 2.4.7 and curl 8.14.1. All 17 cases matched their stated expectations:

- `set -e; false | tee out.log; echo REACHED` printed `REACHED` and exited 0. With `pipefail` it exited 1.
- The redirect left `backup.gpg` at 0 bytes and wrote 131 bytes to `seeds.txt.gpg`. Decrypting the empty file exited 2. With `--output`, the file held 131 bytes and decrypted to the original.
- `curl -sO` exited 0 and saved the 111-byte error. `curl -fsSO` exited 22 and saved nothing. `--fail-with-body` exited 22 and kept the body for inspection.
- `pihole -a adlist add` exited 0 on v6.0 and v6.4.3, with output byte-identical to `pihole --help`.

These are four behaviors of specific tool versions. They say nothing about how often such commands appear in other people's instructions.

## Why nothing caught them

This site runs a link checker, a build and a set of audits on every change. None of them flagged any of the five.

The link checker did see the Wazuh URL. Its classifier files a 403 as `restricted`, an advisory result, because publishers answer bots with 403 all the time and alarming on each one would bury real breakage. That is a sensible design for citations. It also means a link checker cannot tell a bot challenge from an object that does not exist, and the curl command depended on exactly that difference. The other four commands contain no URL worth checking.

The build renders code fences as text and executes nothing. A shell linter does slightly better. [ShellCheck](https://www.shellcheck.net/) 0.11.0, run over the four original shell snippets, reported nothing for any of them with default checks. With every optional check enabled, it flagged the pipeline (SC2312, severity info) and nothing else. ShellCheck cannot know how gpg names files, what an HTTP server will answer, or which subcommands Pi-hole removed in February 2025. Nor should it.

## Run it where it must fail

The defense is cheap and unglamorous. Before a command goes into a post, run it once in a situation where it has to fail, and confirm it reports the failure. If it reports success, the instructions need a check that does not depend on the exit status.

```sh
# Negative control for the pipeline guard: make the first command fail
bash -c 'set -eo pipefail; false | tee /dev/null; echo REACHED'; echo "exit=$?"
# Verify the backup by restoring it, not by trusting gpg's exit status
gpg --decrypt backup.gpg | cmp - seeds.txt && echo "backup restores"
```

The second half matters as much as the first. A restore check you have never seen fail is a label, so run it once against an empty file and watch it complain. Against an empty `backup.gpg` it prints `cmp: EOF on - which is empty` and exits 1. That pipeline gets away without `pipefail` for a boring reason: the command that decides is the last one. Run it before you shred `seeds.txt`; afterwards there is nothing to compare against.

The corrected forms have limits of their own. BashFAQ/105 shows `set -e -o pipefail` stopping a script only sometimes on `somecmd | head -n1`, depending on whether the output outgrows the pipe buffer. The curl manual says `--fail` "is not fail-safe", especially around 401 and 407 responses. And the v6 `pihole` command has no subcommand that adds a list (its `api` subcommand only sends GET requests), so the honest instruction is to add it in the web interface or with a `POST` to [`/api/lists`](https://github.com/pi-hole/FTL/blob/0bf029baf174f65852a0e598bf4efa436e5cda9c/src/api/docs/content/specs/lists.yaml), then look at the list and see it there.

None of that is novel. The Bash manual, the curl manual and the BashFAQ all said it first. What this adds is a catalogue from one site that published all five, and a lab you can rerun.

## Try it

From a POSIX shell with Git and Docker:

```sh
git clone https://github.com/williamzujkowski/research-labs.git
cd research-labs
git checkout ea153aa2d92af0a6c3ce408ac6f5277f179eebf0
./scripts/exit-status-lab.sh test
mkdir -p results
./scripts/exit-status-lab.sh run > results/exit-status.json
```

The build fetches a pinned base image, curl and gnupg from a fixed Debian snapshot, and the two Pi-hole scripts by commit hash. The run itself is offline. Exit 3 means a case did not match its expectation, and the JSON still records what happened.

The [scanning-pipeline post](/posts/2025-10-06-automated-security-scanning-pipeline) made the same point about CI: a job that echoes a string and exits 0 is not a gate. It turns out to hold one level down, for the commands inside the job, and for the ones I told readers to type.
