---
title: "Implementing DNS-over-HTTPS (DoH) for Home Networks"
date: 2025-07-08
description: "Complete guide to deploying DNS-over-HTTPS on your home network for enhanced privacy and security, with multiple implementation approaches"
tags: [security, networking, dns, privacy, homelab, encryption]
author: "William Zujkowski"
---

**Reading time:** 9 minutes

## The ISP Letter That Started Everything

A few years back, I became aware that many ISPs monetize DNS query data for targeted advertising. This privacy concern motivated me to research DNS-over-HTTPS implementations.

After implementing DoH on my personal home network, I've achieved complete DNS privacy. The ISP only sees encrypted HTTPS traffic, protecting browsing patterns from commercial exploitation.

If you're tired of being the product, here's how to take back control of your DNS privacy. It's easier than you think, and I'll show you three different ways to do it.

## Understanding the DNS Privacy Problem

Traditional DNS has several privacy and security issues:

1. **Plain Text Queries**: ISPs and network observers see all DNS lookups
2. **DNS Hijacking**: Malicious actors can redirect your traffic
3. **ISP Monetization**: Many ISPs sell DNS query data
4. **Censorship**: DNS blocking is a common censorship technique
5. **Man-in-the-Middle**: Unencrypted DNS is vulnerable to tampering

DNS-over-HTTPS solves these by:
- Encrypting all DNS queries with HTTPS
- Authenticating the DNS server
- Hiding DNS queries from network observers
- Preventing DNS-based censorship and filtering

## Implementation Approaches

I'll cover three approaches, from simple to advanced:

1. **Device-Level**: Configure individual devices
2. **Router-Level**: Protect your entire network
3. **Self-Hosted**: Maximum control and privacy

## Approach 1: Device-Level DoH

### Browser Configuration

Most modern browsers support DoH natively:

**Firefox:**
```javascript
// about:config settings
network.trr.mode = 2  // Enable DoH with fallback
network.trr.uri = "https://cloudflare-dns.com/dns-query"
network.trr.bootstrapAddress = "1.1.1.1"
```

**Chrome/Edge:**
```
Settings → Privacy and Security → Security → Use secure DNS
Select provider or enter custom: https://dns.google/dns-query
```

### System-Wide DoH on Linux

For system-wide protection, I use `cloudflared`:

```bash
# Install cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Configure as DNS proxy
sudo mkdir -p /etc/cloudflared/
cat << EOF | sudo tee /etc/cloudflared/config.yml
proxy-dns: true
proxy-dns-port: 5053
proxy-dns-upstream:
  - https://1.1.1.1/dns-query
  - https://1.0.0.1/dns-query
EOF

# Create systemd service
sudo cloudflared service install
sudo systemctl start cloudflared

# Configure system to use local DoH proxy
sudo bash -c 'cat << EOF > /etc/systemd/resolved.conf.d/cloudflared.conf
[Resolve]
DNS=127.0.0.1:5053
DNSStubListener=no
EOF'

sudo systemctl restart systemd-resolved
```

### Windows DoH Setup

Windows 11 has native DoH support:

```powershell
# Enable DoH for network adapter
netsh dns add encryption server=1.1.1.1 dohtemplate=https://cloudflare-dns.com/dns-query
netsh dns add encryption server=8.8.8.8 dohtemplate=https://dns.google/dns-query

# Configure network adapter to use DoH
# GUI: Settings → Network → Ethernet/WiFi → DNS server assignment → Manual
# Set preferred DNS encryption to "Encrypted only"
```

## Approach 2: Router-Level DoH

Protecting your entire network requires a DoH-capable router or custom firmware.

### Using pfSense

pfSense doesn't natively support DoH, but we can use a clever workaround:

```bash
# Install required packages in pfSense
pkg install dnscrypt-proxy2

# Configure dnscrypt-proxy for DoH
cat > /usr/local/etc/dnscrypt-proxy/dnscrypt-proxy.toml << 'EOF'
server_names = ['cloudflare', 'google', 'quad9-doh']
listen_addresses = ['127.0.0.1:5353']
max_clients = 250

[query_log]
file = '/var/log/dnscrypt-proxy/query.log'
format = 'tsv'

[sources]
[sources.'public-resolvers']
urls = ['https://raw.githubusercontent.com/DNSCrypt/dnscrypt-resolvers/master/v3/public-resolvers.md']
cache_file = '/var/cache/dnscrypt-proxy/public-resolvers.md'
minisign_key = 'RWQf6LRCGA9i53mlYecO4IzT51TGPpvWucNSCh1CBM0QTaLn73Y7GFO3'

[static]
[static.'cloudflare']
stamp = 'sdns://AgEAAAAAAAAAAAAOZG5zLmNsb3VkZmxhcmUuY29tCi9kbnMtcXVlcnk'

[static.'google']
stamp = 'sdns://AgEAAAAAAAAAAAAADGRucy5nb29nbGUuY29tCi9kbnMtcXVlcnk'

[static.'quad9-doh']
stamp = 'sdns://AgEAAAAAAAAAAAAADHF1YWQ5Lm5ldDo0NDMKL2Rucy1xdWVyeQ'
EOF

# Enable service
sysrc dnscrypt_proxy_enable="YES"
service dnscrypt-proxy start

# Configure pfSense DNS
# GUI: System → General Setup
# DNS Servers: 127.0.0.1:5353
# Uncheck "Allow DNS server list to be overridden"
```

### OpenWrt with DoH

OpenWrt makes DoH implementation straightforward:

```bash
# Install packages
opkg update
opkg install https-dns-proxy luci-app-https-dns-proxy

# Configure DoH providers
uci set https-dns-proxy.@https-dns-proxy[0].bootstrap_dns='1.1.1.1,8.8.8.8'
uci set https-dns-proxy.@https-dns-proxy[0].resolver_url='https://cloudflare-dns.com/dns-query'
uci set https-dns-proxy.@https-dns-proxy[0].listen_addr='127.0.0.1'
uci set https-dns-proxy.@https-dns-proxy[0].listen_port='5053'
uci commit https-dns-proxy

# Restart services
/etc/init.d/https-dns-proxy restart
/etc/init.d/dnsmasq restart

# Configure dnsmasq to use DoH proxy
uci set dhcp.@dnsmasq[0].server='127.0.0.1#5053'
uci commit dhcp
/etc/init.d/dnsmasq restart
```

## Approach 3: Self-Hosted DoH Server

For maximum privacy and control, run your own DoH server:

### Pi-hole with DoH

Transform Pi-hole into a DoH server:

```bash
# Install Pi-hole (if not already installed)
curl -sSL https://install.pi-hole.net | bash

# Install cloudflared for DoH upstream
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64
sudo mv cloudflared-linux-arm64 /usr/local/bin/cloudflared
sudo chmod +x /usr/local/bin/cloudflared

# Create cloudflared user
sudo useradd -s /usr/sbin/nologin -r -M cloudflared

# Configure cloudflared
sudo mkdir -p /etc/cloudflared
cat << EOF | sudo tee /etc/cloudflared/config.yml
proxy-dns: true
proxy-dns-port: 5053
proxy-dns-upstream:
  - https://1.1.1.1/dns-query
  - https://1.0.0.1/dns-query
  - https://dns.quad9.net/dns-query
  - https://dns.google/dns-query
EOF

# Create systemd service
cat << EOF | sudo tee /etc/systemd/system/cloudflared.service
[Unit]
Description=cloudflared DNS over HTTPS proxy
After=network.target
Before=pihole-FTL.service

[Service]
Type=simple
User=cloudflared
Group=cloudflared
ExecStart=/usr/local/bin/cloudflared --config /etc/cloudflared/config.yml
Restart=on-failure
RestartSec=10
KillMode=process

[Install]
WantedBy=multi-user.target
EOF

# Start cloudflared
sudo systemctl enable cloudflared
sudo systemctl start cloudflared

# Configure Pi-hole to use cloudflared
# Web UI: Settings → DNS → Upstream DNS Servers
# Custom 1: 127.0.0.1#5053
# Uncheck all other DNS servers
```

### Advanced: DoH Server with nginx

Serve DoH directly to clients using nginx and dnsdist:

```bash
# Install required packages
sudo apt-get update
sudo apt-get install -y nginx dnsdist certbot python3-certbot-nginx

# Configure dnsdist
cat << 'EOF' | sudo tee /etc/dnsdist/dnsdist.conf
-- Listen for DoH
addDOHLocal("127.0.0.1:8053", nil, nil, "/dns-query", {serverTokens="", customResponseHeaders={["cache-control"]="max-age=10"}})

-- Backend DNS servers (Pi-hole)
newServer({address="127.0.0.1:53", pool="default"})

-- Policy
setServerPolicy(firstAvailable)

-- Cache
pc = newPacketCache(10000, {maxTTL=86400, minTTL=0, temporaryFailureTTL=60, staleTTL=60, dontAge=false})
getPool(""):setCache(pc)

-- Security
setACL({'0.0.0.0/0', '::/0'})
addACL('192.168.0.0/16')
addACL('10.0.0.0/8')
addACL('172.16.0.0/12')

-- Logging
addAction(AllRule(), LogAction("/var/log/dnsdist/dnsdist.log", false, true, false))
EOF

# Configure nginx for DoH
cat << 'EOF' | sudo tee /etc/nginx/sites-available/doh
upstream dnsdist_backend {
    server 127.0.0.1:8053;
}

server {
    listen 443 ssl http2;
    server_name doh.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/doh.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/doh.yourdomain.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    location /dns-query {
        proxy_pass http://dnsdist_backend/dns-query;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # DoH specific headers
        proxy_set_header Content-Type application/dns-message;
        proxy_hide_header X-Powered-By;
        
        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 10s;
        proxy_read_timeout 10s;
    }
    
    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF

# Enable site and restart services
sudo ln -s /etc/nginx/sites-available/doh /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx
sudo systemctl enable dnsdist && sudo systemctl start dnsdist
```

## Monitoring and Validation

### Verify DoH is Working

```bash
# Test using curl
curl -H 'content-type: application/dns-message' \
     --data-binary @<(echo -n 'q80BAAABAAAAAAAAA3d3dwdleGFtcGxlA2NvbQAAAQAB' | base64 -d) \
     https://cloudflare-dns.com/dns-query | hexdump -C

# Test using dog (better than dig for DoH)
dog example.com @https://cloudflare-dns.com/dns-query

# Check for DNS leaks
# Visit: https://dnsleaktest.com
# Should only show your configured DoH provider
```

### Performance Monitoring

```python
#!/usr/bin/env python3
import time
import dns.resolver
import requests
from statistics import mean, stdev

def benchmark_dns(resolver_func, queries, name):
    """Benchmark DNS resolver performance"""
    times = []
    
    for domain in queries:
        start = time.time()
        try:
            resolver_func(domain)
            elapsed = (time.time() - start) * 1000  # ms
            times.append(elapsed)
        except Exception as e:
            print(f"Error resolving {domain}: {e}")
    
    if times:
        print(f"\n{name} Performance:")
        print(f"  Average: {mean(times):.2f}ms")
        print(f"  StdDev: {stdev(times):.2f}ms")
        print(f"  Min: {min(times):.2f}ms")
        print(f"  Max: {max(times):.2f}ms")

def traditional_dns_query(domain):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['8.8.8.8']
    return resolver.resolve(domain, 'A')

def doh_query(domain):
    url = 'https://cloudflare-dns.com/dns-query'
    headers = {'content-type': 'application/dns-message'}
    
    # Build DNS query (simplified)
    import base64
    query = base64.b64decode('q80BAAABAAAAAAAAA3d3dwdleGFtcGxlA2NvbQAAAQAB')
    
    response = requests.post(url, headers=headers, data=query)
    return response.content

# Test domains
test_domains = [
    'google.com', 'facebook.com', 'amazon.com',
    'netflix.com', 'wikipedia.org', 'github.com'
]

# Run benchmarks
benchmark_dns(traditional_dns_query, test_domains, "Traditional DNS")
benchmark_dns(doh_query, test_domains, "DNS-over-HTTPS")
```

### Logging and Analytics

```bash
# Parse dnscrypt-proxy logs
cat << 'EOF' > /usr/local/bin/analyze-doh-logs.sh
#!/bin/bash

LOG_FILE="/var/log/dnscrypt-proxy/query.log"

echo "=== DoH Query Analysis ==="
echo

echo "Top 10 Queried Domains:"
awk '{print $3}' "$LOG_FILE" | sort | uniq -c | sort -rn | head -10

echo -e "\nQueries by Hour:"
awk '{print substr($1,12,2)}' "$LOG_FILE" | sort | uniq -c

echo -e "\nBlocked Queries:"
grep "BLOCKED" "$LOG_FILE" | wc -l

echo -e "\nQuery Types:"
awk '{print $4}' "$LOG_FILE" | sort | uniq -c | sort -rn
EOF

chmod +x /usr/local/bin/analyze-doh-logs.sh
```

## Security Considerations

### 1. DoH Provider Selection

Not all DoH providers are equal. Consider:

```yaml
Provider Comparison:
  Cloudflare (1.1.1.1):
    Privacy: Excellent (audited no-logs policy)
    Performance: Fastest globally
    Features: Malware blocking option (1.1.1.2)
    
  Quad9 (9.9.9.9):
    Privacy: Good (Swiss privacy laws)
    Performance: Good
    Features: Malware blocking by default
    
  Google (8.8.8.8):
    Privacy: Moderate (logs for 24-48h)
    Performance: Excellent
    Features: No filtering
    
  NextDNS:
    Privacy: Good (configurable logging)
    Performance: Good
    Features: Extensive filtering options
```

### 2. Preventing DoH Bypass

Ensure all DNS queries use DoH:

```bash
# iptables rules to force DoH
# Block standard DNS (port 53) except from DoH proxy
iptables -A OUTPUT -p udp --dport 53 -m owner ! --uid-owner cloudflared -j DROP
iptables -A OUTPUT -p tcp --dport 53 -m owner ! --uid-owner cloudflared -j DROP

# Block DNS-over-TLS (port 853)
iptables -A OUTPUT -p tcp --dport 853 -j DROP

# Allow only DoH proxy to make HTTPS connections to DNS providers
iptables -A OUTPUT -p tcp --dport 443 -d 1.1.1.1 -m owner ! --uid-owner cloudflared -j DROP
iptables -A OUTPUT -p tcp --dport 443 -d 8.8.8.8 -m owner ! --uid-owner cloudflared -j DROP
```

### 3. Certificate Pinning

For self-hosted DoH, implement certificate pinning:

```python
import ssl
import hashlib
import base64

class SecureDoHClient:
    def __init__(self, server_url, pin_sha256):
        self.server_url = server_url
        self.pin_sha256 = pin_sha256
    
    def verify_pin(self, cert_der):
        """Verify certificate pin"""
        cert_hash = hashlib.sha256(cert_der).digest()
        cert_pin = base64.b64encode(cert_hash).decode('utf-8')
        
        return cert_pin == self.pin_sha256
    
    def create_secure_context(self):
        """Create SSL context with pinning"""
        context = ssl.create_default_context()
        
        def verify_callback(conn, cert, errno, depth, ok):
            if depth == 0:  # Server certificate
                cert_der = cert.to_cryptography().public_bytes(
                    serialization.Encoding.DER
                )
                if not self.verify_pin(cert_der):
                    return False
            return ok
        
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        context.verify_callback = verify_callback
        
        return context
```

## Troubleshooting Common Issues

### 1. Slow Initial Queries

```bash
# Implement DNS caching
# For dnsmasq
echo "cache-size=10000" >> /etc/dnsmasq.conf
echo "min-cache-ttl=3600" >> /etc/dnsmasq.conf

# For systemd-resolved
[Resolve]
Cache=yes
CacheLimit=2048
```

### 2. Connection Timeouts

```bash
# Increase timeout values
# cloudflared config
timeout: 10s
max-upstream-conns: 5

# Multiple upstream servers for redundancy
proxy-dns-upstream:
  - https://1.1.1.1/dns-query
  - https://1.0.0.1/dns-query
  - https://dns.quad9.net/dns-query
```

### 3. Corporate Network Compatibility

Some corporate networks block DoH. Implement fallback:

```bash
# Detect corporate network and adjust
if ping -c 1 corp-gateway.local > /dev/null 2>&1; then
    echo "Corporate network detected, using standard DNS"
    systemctl stop cloudflared
else
    systemctl start cloudflared
fi
```

## Advanced Configurations

### Load Balancing Multiple DoH Providers

```nginx
upstream doh_providers {
    server 1.1.1.1:443 weight=3;
    server dns.google:443 weight=2;
    server dns.quad9.net:443 weight=1;
    keepalive 32;
}
```

### Geo-based DoH Selection

```python
def select_doh_provider(client_ip):
    """Select optimal DoH provider based on location"""
    # Simplified geo-detection
    if client_ip.startswith('192.168.'):
        return "https://local-doh.home.arpa/dns-query"
    elif is_asian_ip(client_ip):
        return "https://dns.google/dns-query"  # Better in Asia
    else:
        return "https://cloudflare-dns.com/dns-query"  # Global default
```

## The Bottom Line: Is DoH Worth It?

After running DoH for years, here's what changed for me:

**The Good:**
- ISP can't sell my browsing habits anymore (take that, "anonymous" marketing data)
- No more DNS hijacking to ISP "search assistance" pages
- Kids' devices automatically protected from DNS-based malware
- That warm fuzzy feeling of actual privacy

**The Annoying:**
- Some corporate networks break (had to create a work profile that disables DoH)
- Slightly slower initial connections (we're talking 10-20ms)
- Explaining to family why "the internet is broken" when DoH server is down
- Captive portals at coffee shops require temporary disabling

**My Verdict:** Absolutely worth it. The privacy gains far outweigh the minor inconveniences.

## Your Next Steps

Don't try to boil the ocean. Here's your weekend project path:

1. **Right now (5 minutes):** Enable DoH in your browser. Just do it.
2. **This weekend (2 hours):** Set up Pi-hole with DoH on a Raspberry Pi
3. **Next month:** Configure your router for network-wide protection
4. **Eventually:** Consider self-hosting if you're a control freak like me

Remember: DNS privacy is just one piece of the puzzle. But it's a big piece. Every DNS query you encrypt is data your ISP can't monetize, a profile that can't be built, and a step toward the internet we deserve.

The internet was built on open protocols, but that doesn't mean we have to accept surveillance as the price of connectivity. 

Take back your DNS privacy. This weekend. I'll wait.

---

*Running DoH in production? Hit me up to share experiences and optimization tips. Privacy is a community effort!*