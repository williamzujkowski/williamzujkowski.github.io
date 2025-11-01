# VLAN Segmentation Troubleshooting Guide

Source: https://williamzujkowski.github.io/posts/zero-trust-vlan-segmentation-homelab/

## Common Issues and Solutions

### 1. Device Can't Get IP Address

**Symptoms:** Device connects but gets 169.254.x.x address

**Diagnosis:**
```bash
# Check DHCP server is running
systemctl status isc-dhcp-server

# View DHCP leases
cat /var/lib/dhcp/dhcpd.leases

# Check DHCP logs
tail -f /var/log/syslog | grep dhcp
```

**Solutions:**
- Verify VLAN is correctly configured on switch port
- Check DHCP pool isn't exhausted
- Ensure DHCP relay is configured if server is on different VLAN

### 2. Can't Access Devices on Same VLAN

**Symptoms:** Devices on same VLAN can't communicate

**Diagnosis:**
```bash
# Verify switch port VLAN assignment
show vlan brief

# Check if port is in correct VLAN
show interfaces switchport

# Test layer 2 connectivity
arping -I eth0 10.0.40.100
```

**Solutions:**
- Verify all ports are in correct VLAN
- Check for PVLAN isolation if enabled
- Ensure switch port mode is correct (access vs trunk)

### 3. Cross-VLAN Communication Doesn't Work

**Symptoms:** Can't reach devices on other VLANs even when allowed

**Diagnosis:**
```bash
# Check firewall rules
iptables -L -v -n | grep 10.0.40

# Verify routing is enabled
sysctl net.ipv4.ip_forward

# Test with tcpdump
tcpdump -i eth1.40 icmp
```

**Solutions:**
- Verify firewall rules are in correct order
- Check that inter-VLAN routing is enabled
- Ensure gateway IPs are correctly configured

### 4. VLAN Hopping Security Concerns

**Symptoms:** Devices can access VLANs they shouldn't

**Diagnosis:**
```bash
# Check for trunk ports on access ports
show interfaces trunk

# Verify native VLAN is disabled or unused
show vlan id 1

# Check for double tagging vulnerabilities
tcpdump -vv -i eth0 vlan
```

**Solutions:**
- Disable unused VLAN 1
- Set all access ports to explicit access mode
- Disable DTP (Dynamic Trunking Protocol)

### 5. Performance Issues

**Symptoms:** Slow network performance across VLANs

**Diagnosis:**
```bash
# Check CPU usage on router/firewall
top

# Monitor interface errors
netstat -i

# Test bandwidth
iperf3 -s  # on server
iperf3 -c 10.0.30.100  # on client
```

**Solutions:**
- Enable hardware offloading if available
- Reduce firewall logging on high-volume rules
- Consider faster routing hardware

## Quick Diagnostic Commands

```bash
# Show all VLANs
show vlan brief

# Show VLAN on specific port
show interfaces gi0/1 switchport

# Show IP routing table
show ip route

# Display firewall rule hits
iptables -L -v -n --line-numbers

# Check connectivity matrix
bash vlan-connectivity-tests.sh

# Monitor real-time traffic
tcpdump -i eth1 -n vlan

# View NetFlow statistics
nfdump -R /var/cache/nfdump -s srcip/bytes -n 20
```

## Log Locations

- **Firewall logs:** `/var/log/firewall.log`
- **DHCP logs:** `/var/log/syslog` (filter by dhcp)
- **DNS logs:** `/var/log/pihole.log`
- **System logs:** `/var/log/messages` or `/var/log/syslog`
- **NetFlow data:** `/var/cache/nfdump/`

## Testing Methodology

1. **Layer 2 Testing** (same VLAN):
   - Ping test
   - ARP resolution
   - MAC address table

2. **Layer 3 Testing** (cross-VLAN):
   - Routing table verification
   - Gateway reachability
   - Firewall rule validation

3. **Application Testing**:
   - Port-specific connectivity
   - DNS resolution
   - Service availability

## Recovery Procedures

### Lost Management Access

1. Connect via console cable
2. Reset VLAN configuration to defaults
3. Reconfigure VLANs from scratch
4. Test each VLAN before proceeding

### Suspected Breach

1. Isolate affected VLAN immediately
2. Review firewall logs for violations
3. Check NetFlow for unusual patterns
4. Scan for unauthorized devices
5. Reset compromised device credentials

## Monitoring Best Practices

1. Enable logging on all block rules
2. Set up alerts for cross-VLAN violations
3. Regular review of DHCP leases
4. Monitor bandwidth per VLAN
5. Periodic security audits with nmap

---

For additional help, see the full blog post or consult vendor documentation for your specific hardware.
