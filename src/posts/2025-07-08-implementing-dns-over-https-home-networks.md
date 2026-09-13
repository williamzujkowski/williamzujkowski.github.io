---
author: William Zujkowski
date: 2025-07-08
description: Choose where DNS-over-HTTPS belongs in a home network, distinguish browser and Pi-hole upstream encryption, and check fallback behavior.
title: Implementing DNS-over-HTTPS (DoH) for Home Networks
tags:
  - cryptography
  - homelab
  - networking
  - privacy
  - security
---

DNS-over-HTTPS carries DNS queries inside HTTPS. For a home network, the useful question is where that encrypted connection begins. A browser talking directly to a remote resolver and Pi-hole forwarding through a local proxy protect different parts of the path. The protocol is defined in [RFC 8484](https://www.rfc-editor.org/rfc/rfc8484.html).

Draw that path before changing settings. A padlock is easier to understand when you know which door it belongs to.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/dns-doh.png'); width: min(360px, 85%); aspect-ratio: 400/342; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">DNS, now wearing a coat</p>

**Correction, September 13, 2026:** The earlier version included incomplete deployment scripts, invalid Python dependency instructions, and personal deployment and latency claims without retained supporting evidence. Those have been removed. This article now explains the architecture and the checks a deployment needs. Cloudflare also announced that new releases would remove `cloudflared proxy-dns` beginning February 2, 2026; the old installation advice is no longer suitable for a new setup. That change was announced after this post's original date. [Cloudflare's November 2025 announcement](https://developers.cloudflare.com/changelog/post/2025-11-11-cloudflared-proxy-dns/).

## What DoH protects

DoH encrypts the exchange between a DoH client and its selected resolver, with HTTPS authenticating that resolver's identity. An observer outside that encrypted connection cannot simply read the DNS message from the wire. The resolver still receives the query, and encryption does not erase traffic-analysis signals. Nor does it establish that the resolver's answer is trustworthy in every respect. [RFC 8484, privacy and security considerations](https://www.rfc-editor.org/rfc/rfc8484.html#section-8).

Treat resolver choice as a trust decision. Consider its query-retention policy, the filtering you want, and what happens when it becomes unavailable. DNS transport encryption and malware filtering are separate properties: DoH specifies how queries travel, not which domains a provider should block. [RFC 8484, server selection](https://www.rfc-editor.org/rfc/rfc8484.html#section-3).

## Browser DoH: encryption starts at the application

A browser configured to use a remote DoH provider sends the applicable lookups from that browser to that provider over HTTPS. Its setting does not establish the DNS behavior of the other applications on the machine. Firefox's implementation also distinguishes ordinary lookups from excluded names and special requests. [Mozilla's implementation notes, June 2024 revision](https://github.com/mozilla-firefox/firefox/blob/ce8560edadf1e29fd9646be1fb3cfaa9b4e0d7b1/netwerk/docs/dns/dns-over-https-trr.md).

The fallback choice matters. In those documented Firefox settings, `network.trr.mode = 2` means DoH first, with ordinary DNS available on failure. Mode `3` means DoH only for requests using that mode; excluded names and special requests still need separate attention. Calling either setting “all DNS encrypted” would hide the exceptions. The same [Mozilla notes](https://github.com/mozilla-firefox/firefox/blob/ce8560edadf1e29fd9646be1fb3cfaa9b4e0d7b1/netwerk/docs/dns/dns-over-https-trr.md#implementation) describe the fallback and exclusions.

For a homelab with Pi-hole, make the routing choice deliberate. A browser sending a lookup directly to an external provider has taken a path around the local resolver, so Pi-hole cannot apply its local filtering to that lookup. That follows from the two different paths; it is not a defect in HTTPS.

## Pi-hole with an encrypted upstream

The Pi-hole arrangement documented before this post's original date uses `dnscrypt-proxy` as a local upstream service. Pi-hole accepts ordinary DNS from clients and forwards requests to the proxy, which can send them to a selected DoH resolver. This is an upstream proxy arrangement, not a client-facing DoH server. [Pi-hole's March 2025 guide](https://github.com/pi-hole/docs/blob/7ca1c7b7aae00f0cb175c9b6ef02fe53ab2092e9/docs/guides/dns/dnscrypt-proxy.md).

<div class="flow" role="group" aria-label="Pi-hole upstream DNS path; HTTPS begins at the local proxy">
  <div class="flow-node"><b>Home device</b><i>Ordinary DNS to Pi-hole</i></div>
  <div class="flow-node"><b>Pi-hole</b><i>DNS to a loopback listener</i></div>
  <div class="flow-node"><b>dnscrypt-proxy</b><i>HTTPS to the selected DoH resolver</i></div>
  <div class="flow-node"><b>Upstream resolver</b><i>Receives the query</i></div>
</div>

In that layout, the local network hop remains ordinary DNS. The proxy-to-upstream hop is encrypted. Running both local services on one host makes their intervening connection a loopback connection; it does not retroactively encrypt the device-to-Pi-hole traffic.

The historical guide separates Pi-hole's port 53 listener from the proxy's loopback port 5053, then points Pi-hole at `127.0.0.1#5053`. It also removes other upstream selections. Those details explain the topology; they are not a complete installation recipe for every distribution. Package defaults, service activation, and resolver lists need checking against the installed versions. [Historical configuration](https://github.com/pi-hole/docs/blob/7ca1c7b7aae00f0cb175c9b6ef02fe53ab2092e9/docs/guides/dns/dnscrypt-proxy.md#configuring-dnscrypt-proxy).

**Current installation reference, checked September 2026:** Pi-hole maintains a [dnscrypt-proxy guide](https://docs.pi-hole.net/guides/dns/dnscrypt-proxy/) with its current package and service assumptions. Follow that maintained procedure for a compatible system, and verify the selected upstream uses DoH if that is the transport you intend. The [old cloudflared guide](https://docs.pi-hole.net/guides/dns/cloudflared/) now advises against new installations using its removed proxy feature.

## Check the path and the failure case

A successful lookup proves that an answer arrived. It does not identify every hop or demonstrate that fallback was encrypted. For a change on your own homelab network, use the documented routing and fallback behavior to build a small acceptance checklist:

| Check | Evidence to collect |
| --- | --- |
| Resolver path | Browser or operating-system DNS settings, Pi-hole upstream settings, and the proxy's selected server. |
| Actual transport | Service logs and a scoped capture on the relevant interfaces during a test lookup; identify local DNS separately from the upstream HTTPS connection. |
| Failure behavior | In a controlled test, make the selected upstream unavailable and record whether resolution fails, retries, or uses another path. Restore the setup afterwards. |
| Local names | Resolve a known homelab name and check which resolver answered it. |
| Filtering | If filtering is part of the design, use the chosen service's documented test case and confirm that the query actually reaches it. |

These are proposed checks, not results from a retained experiment. A packet capture also needs context: the presence of HTTPS traffic alone does not prove every query used the intended resolver. Firefox's [fallback documentation](https://github.com/mozilla-firefox/firefox/blob/ce8560edadf1e29fd9646be1fb3cfaa9b4e0d7b1/netwerk/docs/dns/dns-over-https-trr.md#implementation) gives one concrete reason to test failure as well as success.

Measure latency separately if it affects your decision. Record the resolver, cache state, connection reuse, network conditions, and failed requests alongside timings.

Start with one device and one explicit resolver path. Expand the setup once both the successful lookup and the failure case behave as intended. The useful outcome is knowing where DNS goes, including when the preferred route stops working.
