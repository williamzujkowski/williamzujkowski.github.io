---
title: "Aegis Boot"
description: "A signed UEFI Secure Boot rescue environment: pick any ISO from a USB stick's data partition and kexec into it without leaving the chain of trust. Per-ISO trust decisions instead of Ventoy's one-shared-key shortcut."
url: "https://github.com/aegis-boot/aegis-boot"
category: "security"
tags: ["rust", "uefi", "secure-boot", "kexec", "cli"]
featured: false
status: "active"
order: 7
---

Boot chain: signed shim, signed GRUB, a rescue kernel, then `kexec_file_load` into the operator's chosen ISO — Secure Boot's signature checks stay intact the whole way down. Unsigned kernels are refused outright rather than silently trusted.
