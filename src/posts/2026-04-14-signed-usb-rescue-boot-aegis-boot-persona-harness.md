---
title: "Signed USB Rescue Boot: aegis-boot and the QEMU+OVMF Persona Harness"
date: 2026-04-14
description: "A UEFI-Secure-Boot-preserving rescue USB for any ISO, and the companion QEMU harness that validates it against ~100 hardware personas without physical Frameworks, ThinkPads, or Dells on a lab bench."
tags: [security, firmware, rust, homelab, uefi]
image: https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200&h=630
imageAlt: "Close-up of motherboard circuitry with capacitors and traces"
author: William Zujkowski
---

There's a specific pain in being the "family IT person" with Secure Boot enabled on every machine. You get a call, you need to boot a rescue distro, you want to keep Secure Boot enforcing, and your options are: (a) disable Secure Boot for 30 minutes and forget to re-enable it, (b) enroll a shared MOK that effectively trusts every kernel Ventoy ever boots, or (c) pick one specific ISO and dd it onto a stick. None of those are defensible positions.

[aegis-boot](https://github.com/williamzujkowski/aegis-boot) is option (d): a signed UEFI rescue environment that lets you drop any `.iso` onto a data partition and `kexec` into it, with kernel-level signature verification keeping the chain of trust intact. [aegis-hwsim](https://github.com/williamzujkowski/aegis-hwsim) is the companion project that simulates ~100 real-hardware configurations in QEMU so I can validate the full flow without waiting on physical Framework / ThinkPad / Dell / HP hardware to arrive.

Both are Rust. Both ship CI that actually exercises the full pipeline. Both exist because years of system administration taught me that "works on my laptop" is the least interesting claim a tool can make about UEFI.

## What aegis-boot actually does

The operator flow is five steps:

1. Flash the aegis-boot image to a USB stick (`aegis-boot flash` or `dd`).
2. Drop `.iso` files onto the `AEGIS_ISOS` partition.
3. Boot the stick on any UEFI machine with Secure Boot enabled.
4. A minimal ratatui TUI lists the available ISOs.
5. `kexec_file_load(2)` hands off to the selected ISO's kernel.

The boot chain is where the engineering lives:

```
UEFI firmware
  → shim (Microsoft-signed)
    → grub (Canonical-signed)
      → rescue kernel (signed)
        → our initramfs
          → rescue-tui
            → kexec_file_load
              → selected ISO's kernel
```

Every link in that chain has a signature verification. The rescue kernel is built with `KEXEC_SIG=y`, so `kexec_file_load` refuses unsigned target kernels. If the operator drops an ISO whose kernel isn't signed by a key the operator's MOK trusts, aegis-boot prints a specific `mokutil --import` command for the signing key. Not "disable Secure Boot." Not "use a different tool." Enroll this specific key, reboot, try again.

## How it differs from Ventoy

Ventoy is a lovely tool. I've used it for years. It works by shipping a grub-based loader that gets signed with a shared MOK across all Ventoy installations. Once you enroll that MOK, every Ventoy stick boots every kernel it hosts. One trust decision, permanent, global.

That's not a Secure Boot threat model. That's a "Secure Boot is enabled" threat model. The difference matters if you're trying to minimize the blast radius of a compromised ISO.

aegis-boot's trust model is per-ISO key enrollment. You enroll the Alpine signing key, Alpine kernels boot. You don't enroll the random-distro key, that distro's kernels get rejected with a clear error. The tradeoff is an extra `mokutil --import` for each new distro you want to boot. The payoff is that adding a new distro doesn't implicitly trust every kernel Ventoy has ever signed.

## The persona problem

aegis-boot's testable surface is the Linux-visible part of a laptop: DMI/SMBIOS strings, Secure Boot posture (MS-enrolled / custom-PK / setup-mode / disabled), TPM 1.2 or 2.0 presence, kernel lockdown mode. On real hardware, these vary across every machine. A 2018 ThinkPad with TPM 1.2 and a custom PK, a 2024 Framework with MS-enrolled keys and TPM 2.0 — different test cases, different failure modes.

The naive approach is a hardware lab. Buy one of each, rack them, automate them with serial consoles and power switches. [LAVA](https://docs.lavasoftware.org) and [labgrid](https://github.com/labgrid-project/labgrid) both do this well. Neither is cheap.

aegis-hwsim takes the other approach: parameterize QEMU + OVMF + swtpm over YAML fixtures that match real shipping laptops. Each persona is a file like this:

```yaml
name: framework-laptop-12gen
dmi:
  sys_vendor: Framework
  product_name: Laptop (12th Gen Intel Core)
  bios_vendor: INSYDE Corp.
secure_boot:
  posture: ms-enrolled
  ovmf_variant: OVMF_CODE_4M.ms.fd
tpm:
  version: 2.0
  swtpm_socket: /tmp/swtpm-framework.sock
kernel_lockdown: integrity
quirks:
  - framework-ec-key-passthrough
```

The harness loads the fixture, constructs the right QEMU invocation (DMI strings via `-smbios type=0/1/2/3/4/17`, OVMF variant path, swtpm socket), boots aegis-boot through the full chain, and asserts the expected behavior. CI runs the matrix on every PR:

```
personas (11)  ×  scenarios (N)  →  coverage grid
```

The 11 shipped personas include Framework Laptop 12th gen, Dell XPS 13 9320, Lenovo ThinkPad X1 Carbon Gen 11, HP EliteBook 845 G10, ASUS Zenbook 14 OLED, plus five QEMU-specific corner cases (custom-PK, setup-mode, Secure Boot disabled, no-TPM smoke, generic minimal).

## Why QEMU isn't enough

QEMU's `-smbios` flag spoofs the DMI strings the kernel reads from `/sys/class/dmi/id/`. Great for testing vendor-detection logic. It does not spoof the ACPI SSDT tables, PCI IDs, or embedded controller quirks that actually drive `thinkpad_acpi` or `dell-laptop` kernel module behavior.

[fwupd's QEMU CI](https://github.com/fwupd/fwupd) and the LVFS empirical data from Richard Hughes and Mario Limonciello puts QEMU's coverage of capsule-flow bugs at roughly 60-70%. The remaining 30-40% are EC-specific, firmware-vendor-specific, reproducible only on metal.

aegis-boot's scope is narrower than fwupd's — we're testing the USB rescue-stick signed-chain flow, not capsule updates. My estimate is ~80% of aegis-boot's testable failure modes reproduce in aegis-hwsim. The remaining ~20% require physical hardware shakedown, which is what [aegis-boot#51](https://github.com/williamzujkowski/aegis-boot/issues/51) tracks for v1.0.0.

This is a known limitation, called out in both READMEs. The thing aegis-hwsim buys you is fast iteration on the 80%. Writing a new aegis-boot feature, validating it against 11 personas, seeing the matrix go green in CI — that's a tight loop. Adding "ship it on a physical Framework and retest" to every feature would kill the cadence.

## What LAVA already told me

The LAVA project documented something they learned from years of running a deployment lab: "UEFI automation proved to be unworkable in automation due to complexity of the sequences and the changes in error handling between levels of the same menus."

That's a validated dead end. Vendor-specific UEFI UI — Lenovo's blue-screen MOK Manager, Dell's F12 boot menu, HP's Fast Boot timing — doesn't automate reliably. Every firmware update shifts the sequence. Every vendor does it differently.

aegis-hwsim deliberately scopes UEFI UI out. It tests the Linux-visible surface, which is stable and documented. For the firmware-UI part of the flow, we rely on operator documentation: "enter BIOS, enable Secure Boot, set boot priority, save and exit." No attempt to script the BIOS itself.

That scoping decision is where most test harness projects fail — they try to validate everything, the UEFI UI becomes a tar pit, and the project stalls. Keeping the persona matrix to the Linux surface kept aegis-hwsim shipping.

## The "signed boot, any ISO" design decision

A competing design for aegis-boot would have been to ship a known-good ISO catalog — "here are the 20 distros this tool supports." That's what most vendor rescue USBs do.

The problem is that my actual rescue scenarios are weird. An old Debian I can't find on any mirror. A custom SystemRescue build with a specific driver included. Alpine with a patched initramfs for a specific recovery task. A catalog doesn't help.

aegis-boot went the other direction: any signed kernel, any operator-trusted signing key, any distro. The operator owns the trust decision. The tool does the signature verification. When the ISO's kernel isn't trusted, we produce the specific enrollment command rather than failing opaquely.

This mirrors what the TPM and Secure Boot specs actually say the operator should do. Shared MOKs are a shortcut that defeats the point. Per-distro enrollment is more work for the operator but matches the threat model.

## Current state

**aegis-boot v0.13.0** ships with:

- Five operator subcommands: `doctor` (validate a flashed stick), `recommend` (suggest per-distro MOK enrollment), `fetch` (download + verify an ISO), `attest list`, `attest show`.
- Cosign-signed prebuilt binaries.
- A Homebrew tap.
- Attestation receipts on every flash — a Sigstore-style log of what image was flashed, what ISO catalog was included, what keys were enrolled.
- Real-hardware shakedown validated on Alpine + Ubuntu under Secure Boot enforcing ([aegis-boot#109](https://github.com/williamzujkowski/aegis-boot/issues/109)).

**aegis-hwsim** is in Phase 1: CI exercises the full QEMU + OVMF + swtpm pipeline against the 11-persona library on every PR via the `qemu-boots-ovmf` smoke scenario. The roadmap adds more scenarios (MOK enrollment, kexec signature rejection, attestation roundtrip) and more personas (older ThinkPads with TPM 1.2, non-x86 reference platforms).

v1.0.0 for aegis-boot is gated on a multi-vendor physical shakedown per [aegis-boot#51](https://github.com/williamzujkowski/aegis-boot/issues/51). I'll post a follow-up once that clears.

## Numbers

| Metric | aegis-boot | aegis-hwsim |
|--------|-----------:|------------:|
| Lines of Rust | ~18,000 | ~3,500 |
| Test count | 340+ | 50+ |
| CI workflows | 11 | 4 |
| Real-hardware validation points | 6+ distros × Alpine/Ubuntu boots | n/a (QEMU) |
| Shipped personas | n/a | 11 |
| Persona × scenario coverage grid | n/a | ~80% of testable flow |
| Boot chain verification points | 4 signatures | 4 (matches aegis-boot) |

## What I'd tell a past-me

**Don't build the hardware lab first.** Spin up the QEMU harness before buying a single laptop. You'll discover 80% of your bugs against simulated personas. The remaining 20% that need real hardware are worth waiting for, but starting with the cheap test infrastructure lets you iterate fast on the logic.

**Per-distro MOK enrollment is the feature, not the bug.** I spent time early on trying to make the enrollment flow automatic. It shouldn't be. The operator is the trust anchor. Making them explicitly enroll a signing key per distro is how you keep the threat model honest.

**Scope out the UEFI UI.** LAVA already documented this dead end. Any effort spent on vendor-specific BIOS automation is a loss. Document the operator steps, test the Linux surface, ship.

**Rust for the runtime, YAML for the fixtures.** The persona library doesn't need to be code. YAML loaders are easy in Rust via `serde`. Keeping the fixtures as data means non-Rust-writing operators can contribute new personas with `git add personas/my-laptop.yaml`.

## Try it

- [aegis-boot v0.13.0](https://github.com/williamzujkowski/aegis-boot/releases/latest) — signed prebuilt binaries. Install one-liner in the README.
- [aegis-hwsim](https://github.com/williamzujkowski/aegis-hwsim) — clone, `cargo test`, add a persona.

If you own a laptop that isn't in the persona library and aegis-boot passes its shakedown on it, I'd love the persona contribution. A YAML file with your DMI strings, Secure Boot posture, and TPM version is the minimum viable pull request.

Security hygiene is a running thread across everything I've shipped this month. The OSSF Scorecard work, CVE patching, and CodeQL cleanup on nexus-agents lives in the [modularization post](/posts/nexus-agents-april-month-of-modularization/). Same posture, different layer of the stack.
