#!/bin/bash
# NetFlow analysis for cross-VLAN traffic
#
# Source: https://williamzujkowski.github.io/posts/zero-trust-vlan-segmentation-homelab/
# Purpose: Spot IoT devices reaching outside their VLAN, and port-scan shapes
# Requires: nfdump on the collector; a NetFlow exporter pointed at it
#
# Illustrative excerpt. Three things in the previous version were wrong:
#
#   1. It opened with `configure` / `set system flow-accounting ...` /
#      `commit` under the heading "Enable NetFlow on UDM Pro". That is
#      EdgeOS syntax; UniFi OS has no configuration mode. Export is set up in
#      the UniFi Network application, or you mirror the uplink instead.
#   2. `nfcapd -T all` does nothing. Current nfcapd prints "Option -T no
#      longer supported and ignored" (src/nfcapd/nfcapd.c) and the man page's
#      SYNOPSIS has no -T at all; extension selection is -X. `-l` is also a
#      legacy alias -- nfcapd logs that it "may get removed in future. Please
#      use -w to set output directory".
#   3. `flags S` does NOT mean SYN-only. nfdump(1): "Flags not mentioned are
#      treated as don't care... In order to get those flows with only the SYN
#      flag set, use the syntax `flags S and not flags AFRPU`". The old
#      port-scan query therefore matched every SYN-ACK too -- i.e. the normal
#      second packet of every successful handshake.
#
# One more, easy to miss: nfdump takes the filter expression AFTER all
# options. The old port-scan line put it in the middle, which only worked
# because glibc's getopt permutes argv; it breaks on BSD and macOS.

set -euo pipefail

FLOWDIR=/var/cache/nfdump
IOT_NET=10.0.40.0/24

# Collector. -w is the output directory; there is no -T.
nfcapd -D -w "$FLOWDIR" -p 2055 -P /var/run/nfcapd.pid

# --- Cross-VLAN traffic: IoT reaching outside its own subnet -----------------
echo "=== Cross-VLAN Traffic Analysis ==="
nfdump -R "$FLOWDIR" -s srcip/bytes -n 20 \
  "src net $IOT_NET and not (dst net $IOT_NET or dst port 53 or dst port 123)"

# --- Top bandwidth consumers ------------------------------------------------
echo "=== Top Bandwidth Consumers ==="
nfdump -R "$FLOWDIR" -s srcip/bytes -n 10

# --- Port-scan shapes: SYN-only, not SYN-ACK --------------------------------
echo "=== Potential Port Scans ==="
nfdump -R "$FLOWDIR" -s srcip -n 10 \
  'flags S and not flags AFRPU and packets < 5'

echo "NetFlow analysis complete"
