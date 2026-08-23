#!/bin/bash
# Pi-hole VLAN-Specific DNS Filtering
#
# Source: https://williamzujkowski.github.io/posts/zero-trust-vlan-segmentation-homelab/
# Purpose: Apply different DNS blocklists per VLAN, and actually force IoT
#          devices onto Pi-hole instead of their hardcoded resolvers.
# Requires: Pi-hole v6 (checked against v6.4.3), root on the Pi-hole host,
#           and a firewall you control on the inter-VLAN gateway.
#
# Illustrative excerpt, not a turnkey script -- substitute your own VLANs,
# interfaces and domains.
#
# This replaces an earlier version that was wrong in four ways, all of which
# are worth stating because each one FAILS SILENTLY:
#
#   1. It wrote a hosts-format blocklist to /etc/pihole/iot-blocklist.list.
#      Pi-hole never reads that path. v6 emits `hostsdir=/etc/pihole/hosts`
#      (FTL src/config/dnsmasq_config.c), so a hosts file has to live in that
#      DIRECTORY to be loaded at all.
#   2. It used `bogus-nxdomain=` to "block DNS requests to external
#      resolvers". That is not what the directive does. dnsmasq(8):
#      "Transform replies which contain the specified address or subnet into
#      'No such domain' replies." It rewrites ANSWERS, so it blocks nothing
#      outbound -- and pointing it at 8.8.8.8/1.1.1.1 NXDOMAINs dns.google
#      and one.one.one.one for every client on the network.
#   3. It wrote conditional forwarding into /etc/dnsmasq.d/. In v6 that
#      directory is only read when `misc.etc_dnsmasq_d` is enabled, and its
#      default is false (FTL src/config/config.c: `.d.b = false`).
#   4. It ended with `pihole restartdns`, which v6 removed.

set -euo pipefail

IOT_IFACE="eth1.40"          # the IoT VLAN interface on the gateway
PIHOLE_IP="10.0.30.5"

# ---------------------------------------------------------------------------
# 1. Block telemetry domains.
#
# Use the CLI so the entries land in Pi-hole's gravity database, where the
# web UI and Group Management can see them. `--wild` covers subdomains.
# ---------------------------------------------------------------------------
pihole deny \
  phone-home.camera-vendor.com \
  telemetry.iot-vendor.com \
  stats.smart-device.com

pihole deny --wild tracking.xiaomi.com analytics.tp-link.com

# Per-VLAN scoping is Group Management, not a per-VLAN file: create a group,
# assign the IoT clients to it by IP or MAC, and attach these deny entries to
# that group. There is no supported way to bind a blocklist file to a subnet.

# ---------------------------------------------------------------------------
# 2. Local DNS records, if you need them.
#
# v6's custom list is /etc/pihole/hosts/custom.list, and everything else in
# /etc/pihole/hosts is loaded too via hostsdir=. This is the only place a
# hosts-format file does anything.
# ---------------------------------------------------------------------------
cat > /etc/pihole/hosts/vlan-local.list <<'HOSTS'
10.0.30.5 dns.lab.home
10.0.10.5 mgmt.lab.home
HOSTS

# ---------------------------------------------------------------------------
# 3. Conditional forwarding.
#
# Supported route in v6 is `misc.dnsmasq_lines` in pihole.toml (or the web
# UI's "Additional dnsmasq settings"), NOT a file in /etc/dnsmasq.d.
# ---------------------------------------------------------------------------
pihole-FTL --config misc.dnsmasq_lines '[
  "server=/lab.home/10.0.30.5",
  "server=/mgmt.home/10.0.10.5",
  "server=/servers.home/10.0.30.5"
]'

# ---------------------------------------------------------------------------
# 4. Actually force IoT devices onto Pi-hole.
#
# This is a FIREWALL job, on the gateway -- DNS has no mechanism to refuse
# queries it never receives. Redirect port 53 to Pi-hole and drop DoT so a
# device cannot simply bypass you on 853.
# ---------------------------------------------------------------------------
iptables -t nat -A PREROUTING -i "$IOT_IFACE" -p udp --dport 53 \
  ! -d "$PIHOLE_IP" -j DNAT --to-destination "$PIHOLE_IP:53"
iptables -t nat -A PREROUTING -i "$IOT_IFACE" -p tcp --dport 53 \
  ! -d "$PIHOLE_IP" -j DNAT --to-destination "$PIHOLE_IP:53"

# DNS-over-TLS. DoH rides on 443 and cannot be separated by port alone --
# blocking it needs a resolver blocklist or SNI filtering.
iptables -A FORWARD -i "$IOT_IFACE" -p tcp --dport 853 -j REJECT

# ---------------------------------------------------------------------------
# 5. Apply.
# ---------------------------------------------------------------------------
pihole reloadlists   # `restartdns` was removed in v6

echo "VLAN-specific DNS filtering configured"
