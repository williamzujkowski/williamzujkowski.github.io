---
title: "Multiboxing EverQuest on Linux: Deterministic Wine Prefixes and Programmatic Window Layout"
date: 2026-04-12
description: "I left Windows behind for good. Norrath-Native is an IaC-style toolkit that deploys EverQuest on Ubuntu 24.04 with Wine and DXVK, and a growing exploration into what you can actually do with programmatic window management on Linux."
tags: [linux, homelab, devops, gaming, automation]
image: https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=1200&h=630
imageAlt: "Multiple monitors on a desk displaying code and terminal windows"
author: William Zujkowski
---

I don't run Windows anywhere anymore. Every machine in the house is on some flavor of Linux. That was fine for everything except the one hobby I refuse to give up — running three EverQuest clients at once to play a multibox group through the old zones that built the memory.

EverQuest's recent DirectX 11 upgrade broke several things on Linux: aggressive focus stealing that made the first client grab every keystroke from the second, a black-box launcher render bug, and CPU thrashing when more than one client ran at a time. Wine + DXVK plus the right winetricks sequence fixed it, but the setup is fiddly enough that I wrote it down. [Norrath-Native](https://github.com/williamzujkowski/norrath-native) is that write-down turned into an Infrastructure-as-Code toolkit.

And because once you start tiling windows programmatically the rabbit hole goes deep, this is also about what Linux lets you do with window management that I kept assuming was Windows-only territory.

## The deployment shape

The whole project is one `make deploy` away from running:

```bash
git clone https://github.com/williamzujkowski/norrath-native.git
cd norrath-native
make prereqs                    # installs Wine 11.0, DXVK, vulkan-drivers
make deploy                     # builds the Wine prefix idempotently
make launch-multi               # starts 3 instances with 5s stagger
```

`make deploy` is deterministic and idempotent. Run it once, get a working Wine prefix. Run it again, nothing changes. Run it after clobbering the prefix, get the exact same state back. The approach is Ansible-flavored without the Ansible runtime overhead:

- **Wine prefix path is pinned** at `~/.local/share/norrath-native/wineprefix`. No `$WINEPREFIX` surprises.
- **DXVK DLLs are symlinked**, not copied. Upgrading DXVK across installs means `ln -sf`, not rebuild the prefix.
- **winetricks verbs are idempotent**. `corefonts`, `vcrun2019`, `d3dcompiler_47` — all re-runnable. The script checks for each before invoking.
- **Client settings are templated**, not patched. The `eqclient.ini` lives in the repo; `make deploy` copies it in.
- **Multiboxing is a concurrent launcher**, not a separate install. One prefix, N instances.

The key choice that makes this scale: EQ instances run as **native XWayland windows**, not as children of a Wine Virtual Desktop. Virtual Desktop nests windows inside a Wine frame that intercepts focus and steals Alt-Tab. Native XWayland means each client shows up in the window manager's taskbar, gets its own window ID, and responds to `xdotool` / `wmctrl` / `hyprctl` like any other application.

## Why native windows matter

Here's what I can do once each EQ client is a first-class window:

**Tile them programmatically.** A three-instance layout with the main client taking the left 2/3 of my ultrawide monitor and two box clients stacked on the right:

```bash
# Main client: left 2/3, 16:9 aspect
wmctrl -r "EverQuest (Grenlan)" -e "0,0,0,2304,1440"

# Box 1: top-right quarter
wmctrl -r "EverQuest (Box1)"   -e "0,2304,0,1216,720"

# Box 2: bottom-right quarter
wmctrl -r "EverQuest (Box2)"   -e "0,2304,720,1216,720"
```

Four lines. No Windows-specific tooling. This is the thing I genuinely didn't know Linux had sorted out.

**Broadcast keystrokes selectively.** `xdotool search --name "EverQuest (Box1)" key --window $WID F7` sends F7 to just that window without stealing focus. Useful for keep-alive macros on followers.

**Detect focus races.** The DX11 launcher steals focus aggressively during startup. `xprop -spy -root _NET_ACTIVE_WINDOW` emits a line every time focus changes. A tiny monitoring script flags any unexpected focus swap and I can add a workaround.

**Attach different audio outputs per instance.** PulseAudio's `pactl move-sink-input` routes each client's audio to a different sink. Main client to headphones, box clients to the desk speakers.

None of these require root. None require a kernel module. None require me to ship my own WM. They're primitives Linux already has, exposed through CLIs that compose.

## The DX11 black-box launcher workaround

Shortly after the DX11 upgrade, the launcher started rendering as a black rectangle in the Wine prefix. The game itself ran fine — the launcher just couldn't render its buttons. The fix turned out to be `--disable-gpu` on the launcher invocation only:

```bash
wine "$EQ_DIR/LaunchPad.exe" --disable-gpu
```

The launcher is a CEF (Chromium Embedded Framework) app. CEF's GPU-accelerated paint path hit a Wine+DXVK incompatibility on the specific compositor shim it uses. Falling back to the software renderer for just the launcher fixed it. The game itself still uses DXVK for full Vulkan-backed rendering.

This is the kind of thing that lives in `scripts/start_eq.sh` behind a comment. One line of commentary, one flag, three weeks of debugging saved for anyone who comes after.

## Idempotent winetricks

The winetricks sequence is where most Wine-on-Linux guides go wrong. "Install these five winetricks verbs" is a one-shot recipe. It works once, then when you rebuild the prefix six months later you've forgotten the order and half the verbs fail because a later one already ran.

Norrath-Native's `scripts/setup_prefix.sh` is idempotent:

```bash
for verb in corefonts vcrun2019 d3dcompiler_47 dotnet48; do
  if ! winetricks_has_verb "$verb"; then
    winetricks -q "$verb"
  fi
done
```

`winetricks_has_verb` inspects the prefix's `winetricks.log` (yes, winetricks keeps one) to see whether the verb was applied. The script only runs verbs that haven't been applied yet. Re-running the whole setup is safe.

This is the Ansible-style "check mode then converge" pattern applied to Wine. The payoff is that `make deploy` works the same way on a fresh install, after a manual Wine update, or on a friend's machine with a slightly different Wine version. Idempotency compounds.

## Window management as a programmable surface

The thing I keep coming back to in this project is that Linux's window management is weirdly good once you commit to it.

**X11 has xdotool, wmctrl, and xprop** — three tools that cover 90% of any "move this window, focus that window, tell me what's active" scenario.

**Wayland has hyprctl, swaymsg, and the wl-clipboard ecosystem** — different shape, same capabilities. Hyprland's `hyprctl dispatch focuswindow` and `hyprctl dispatch moveactive` are particularly nice because they're documented CLI commands rather than tool-of-last-resort escape hatches.

**Both expose window geometry, title, and process info as shell-queryable data**. `xdotool search --class "eqgame.exe"` returns window IDs. `wmctrl -l -G` dumps geometry for every window. Grepping the output for the pattern you want is a real workflow.

Compare this to Windows, where you need PowerShell and `System.Windows.Automation`, or AutoHotkey, or a custom win32 harness. Linux lets shell scripts do what Windows needs a runtime for.

I'm using Norrath-Native as the excuse to push this further. A [follow-up branch](https://github.com/williamzujkowski/norrath-native) on the repo has experiments with:

- **Per-monitor profiles.** Plug in an external display, have the box clients automatically migrate there.
- **Focus-follows-activity.** The client that just took damage gets focus for the next 5 seconds.
- **Session save/restore.** Kill all clients, rerun with `--restore`, windows come back on the same monitors at the same sizes.

None of this is novel Windows-manager tech. All of it works with primitives Linux already exposes. The exploration is the point.

## The "I'm only using Linux these days" lesson

I switched the house over in stages. Gaming rig first (Proton carries the weight). Laptop next (nothing I do professionally needs Windows). NAS and homelab have been Linux forever. The last holdout was the EQ multiboxing setup, and the moment I finished Norrath-Native, that became a non-issue too.

What surprised me is how much of the friction was in my head. "Wine doesn't handle modern games well" was outdated advice by about three years. "Window management is Windows-native territory" was just wrong. "You need Windows for multiboxing" assumed Windows-specific tooling that turned out to be worse than `wmctrl` + a shell script.

The actual blockers were specific and solvable:

- **DX11 launcher black box** → `--disable-gpu`
- **Focus stealing between instances** → native XWayland windows, not Virtual Desktop
- **CPU thrashing on multi-client** → `ClientCore=-1` (let Wine schedule)
- **DXVK GPU init races on concurrent launch** → 5-second stagger in the launcher script

Every one of those is a three-line fix once you know what it is. The project is the writedown so the next person doesn't re-solve them.

## Numbers

| Metric | Value |
|--------|------:|
| Lines of shell | ~800 across 6 scripts |
| Makefile targets | 12 |
| Tested Ubuntu versions | 24.04 LTS (primary), Mint 22, Pop!_OS 24.04 |
| Concurrent EQ instances | tested to 4, limited by GPU VRAM |
| Cold `make deploy` time | ~8 minutes (mostly Wine prereq install) |
| Warm `make deploy` time | ~12 seconds |
| GPUs tested | Intel Arc A770, AMD RX 7800 XT, NVIDIA RTX 4070 |

## What I'd do differently

**Start with idempotency.** My first version of the deploy script was linear steps. It worked once, then broke when I tried to upgrade DXVK. Rewriting it as idempotent check-then-converge from the start would have saved a week.

**Make the launcher stagger configurable immediately.** The default 5-second stagger works for my GPU. A friend with a slower iGPU needs 10 seconds. This should have been a CLI flag on day one, not day thirty.

**Write the multiboxing doc section first.** Multiboxing is the actual use case. The rest of the tooling exists to serve it. Leading with the multiboxing workflow in the README forced me to design the rest of the tool around it, not retrofit multiboxing onto a single-client deploy.

## Try it

- [Norrath-Native source](https://github.com/williamzujkowski/norrath-native) — Ubuntu 24.04, ~10 minutes from clone to running EQ.
- [Window management scripts](https://github.com/williamzujkowski/norrath-native/tree/main/scripts) — the `wmctrl` / `xdotool` / `hyprctl` snippets I pulled out into reusable helpers.

I'm still using this daily. PRs and issues on `eqclient.ini` tuning, specific distro quirks, or alternate multibox layouts are welcome. The window-management exploration is open-ended — if you've found a clean pattern for Linux window programming I haven't, I'd love to hear about it.
