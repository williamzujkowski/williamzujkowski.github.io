---
title: "eBPF for Security Monitoring: A Practical Guide"
date: 2025-07-01
description: "Learn how to leverage eBPF for real-time security monitoring in Linux environments with practical examples and production-ready code"
tags: [security, linux, ebpf, monitoring, kernel, detection]
author: "William Zujkowski"
---

## The Day eBPF Changed Everything

Years ago, I researched how attackers could potentially bypass EDR solutions by operating at the kernel level. This research led me to explore eBPF as a detection mechanism.

eBPF technology provides kernel-level visibility in real-time, without requiring kernel modules. After extensive testing in my home lab and research environments, I've developed practical approaches for eBPF-based monitoring. Here's what the research shows works effectively.

## Why eBPF for Security Monitoring?

Traditional security monitoring often relies on logs, which can be:
- **Delayed**: Events logged after they occur
- **Incomplete**: Not all activities generate logs
- **Tamperable**: Logs can be modified or deleted
- **Performance-impacting**: Heavy logging affects system performance

eBPF solves these issues by providing:
- **Real-time visibility**: Events captured as they happen
- **Kernel-level insights**: See everything the kernel sees
- **Minimal overhead**: Efficient in-kernel processing
- **Tamper resistance**: Harder to bypass than userspace monitoring

## Getting Started with Security-Focused eBPF

### Prerequisites and Setup

First, ensure your system supports eBPF:

```bash
# Check kernel version (need 4.4+, recommend 5.8+)
uname -r

# Install required packages (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y \
    clang llvm \
    libbpf-dev \
    linux-headers-$(uname -r) \
    bpftool \
    python3-bpfcc \
    bpfcc-tools

# Verify BPF filesystem is mounted
mount | grep bpf
# If not mounted:
sudo mount -t bpf none /sys/fs/bpf
```

### Your First Security Monitor: Detecting Privilege Escalation

Let's build a simple but effective privilege escalation detector:

```python
#!/usr/bin/env python3
from bcc import BPF
from datetime import datetime
import pwd
import os

# eBPF program to monitor setuid calls
bpf_program = """
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

struct event_data {
    u32 pid;
    u32 ppid;
    u32 uid;
    u32 gid;
    u32 new_uid;
    u32 new_gid;
    char comm[TASK_COMM_LEN];
    char parent_comm[TASK_COMM_LEN];
};

BPF_PERF_OUTPUT(events);

int syscall__setuid(struct pt_regs *ctx, uid_t uid) {
    struct event_data data = {};
    struct task_struct *task;
    
    data.pid = bpf_get_current_pid_tgid() >> 32;
    data.uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;
    data.gid = bpf_get_current_uid_gid() >> 32;
    data.new_uid = uid;
    
    // Get current process name
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    
    // Get parent process info
    task = (struct task_struct *)bpf_get_current_task();
    bpf_probe_read(&data.ppid, sizeof(data.ppid), &task->real_parent->tgid);
    bpf_probe_read(&data.parent_comm, sizeof(data.parent_comm), 
                   &task->real_parent->comm);
    
    // Only report if escalating privileges
    if (uid == 0 && data.uid != 0) {
        events.perf_submit(ctx, &data, sizeof(data));
    }
    
    return 0;
}

// Also monitor setgid, setreuid, setregid
int syscall__setgid(struct pt_regs *ctx, gid_t gid) {
    struct event_data data = {};
    
    data.pid = bpf_get_current_pid_tgid() >> 32;
    data.uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;
    data.gid = bpf_get_current_uid_gid() >> 32;
    data.new_gid = gid;
    
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    
    if (gid == 0 && data.gid != 0) {
        events.perf_submit(ctx, &data, sizeof(data));
    }
    
    return 0;
}
"""

class PrivilegeEscalationMonitor:
    def __init__(self):
        self.b = BPF(text=bpf_program)
        self.b.attach_kprobe(event=self.b.get_syscall_fnname("setuid"), 
                            fn_name="syscall__setuid")
        self.b.attach_kprobe(event=self.b.get_syscall_fnname("setgid"), 
                            fn_name="syscall__setgid")
        
        # Track suspicious patterns
        self.suspicious_parents = ['bash', 'sh', 'python', 'perl', 'ruby']
        self.whitelist = ['sudo', 'su', 'pkexec', 'systemd']
        
    def process_event(self, cpu, data, size):
        event = self.b["events"].event(data)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Skip whitelisted programs
        if event.comm.decode('utf-8', 'ignore').strip() in self.whitelist:
            return
        
        # Decode process names
        process_name = event.comm.decode('utf-8', 'ignore').strip()
        parent_name = event.parent_comm.decode('utf-8', 'ignore').strip()
        
        # Determine severity
        severity = "MEDIUM"
        if parent_name in self.suspicious_parents:
            severity = "HIGH"
        if process_name in ['nc', 'netcat', 'ncat', 'socat']:
            severity = "CRITICAL"
        
        # Alert on privilege escalation
        alert = f"""
[{severity}] Privilege Escalation Detected at {timestamp}
Process: {process_name} (PID: {event.pid})
Parent: {parent_name} (PID: {event.ppid})
UID Change: {event.uid} -> {event.new_uid}
GID Change: {event.gid} -> {event.new_gid}
"""
        print(alert)
        
        # Log to file for SIEM ingestion
        with open('/var/log/privilege_escalation.log', 'a') as f:
            f.write(alert.replace('\n', ' ') + '\n')
    
    def run(self):
        print("Starting privilege escalation monitor...")
        print("Monitoring setuid/setgid calls...")
        
        # Set up event processing
        self.b["events"].open_perf_buffer(self.process_event)
        
        while True:
            try:
                self.b.perf_buffer_poll()
            except KeyboardInterrupt:
                print("\nStopping monitor...")
                break

if __name__ == "__main__":
    monitor = PrivilegeEscalationMonitor()
    monitor.run()
```

## Advanced Monitoring: Network Security

Here's a more sophisticated example that monitors network connections for suspicious activity:

```python
#!/usr/bin/env python3
from bcc import BPF
import socket
import struct
import json
from collections import defaultdict
from datetime import datetime, timedelta

# eBPF program for network monitoring
network_monitor = """
#include <uapi/linux/ptrace.h>
#include <net/sock.h>
#include <bcc/proto.h>

struct conn_info {
    u32 pid;
    u32 saddr;
    u32 daddr;
    u16 sport;
    u16 dport;
    char comm[TASK_COMM_LEN];
};

BPF_HASH(currsock, u32, struct sock *);
BPF_PERF_OUTPUT(conn_events);

// Track TCP connect attempts
int trace_connect_entry(struct pt_regs *ctx, struct sock *sk) {
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    currsock.update(&pid, &sk);
    return 0;
}

int trace_connect_return(struct pt_regs *ctx) {
    int ret = PT_REGS_RC(ctx);
    if (ret != 0) {
        return 0;  // Connection failed
    }
    
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    struct sock **skp = currsock.lookup(&pid);
    if (skp == 0) {
        return 0;
    }
    
    struct sock *sk = *skp;
    struct conn_info info = {};
    
    info.pid = pid;
    bpf_get_current_comm(&info.comm, sizeof(info.comm));
    
    // Get connection details
    bpf_probe_read(&info.saddr, sizeof(info.saddr), &sk->__sk_common.skc_rcv_saddr);
    bpf_probe_read(&info.daddr, sizeof(info.daddr), &sk->__sk_common.skc_daddr);
    bpf_probe_read(&info.sport, sizeof(info.sport), &sk->__sk_common.skc_num);
    bpf_probe_read(&info.dport, sizeof(info.dport), &sk->__sk_common.skc_dport);
    
    // Convert port to host byte order
    info.dport = ntohs(info.dport);
    
    conn_events.perf_submit(ctx, &info, sizeof(info));
    currsock.delete(&pid);
    
    return 0;
}

// Monitor bind() for backdoor detection
int trace_bind(struct pt_regs *ctx, struct socket *sock, 
               struct sockaddr *addr, int addrlen) {
    if (addr->sa_family != AF_INET) {
        return 0;
    }
    
    struct conn_info info = {};
    struct sockaddr_in *addr_in = (struct sockaddr_in *)addr;
    
    info.pid = bpf_get_current_pid_tgid() >> 32;
    bpf_get_current_comm(&info.comm, sizeof(info.comm));
    bpf_probe_read(&info.sport, sizeof(u16), &addr_in->sin_port);
    info.sport = ntohs(info.sport);
    
    // Flag high ports that might be backdoors
    if (info.sport > 30000) {
        conn_events.perf_submit(ctx, &info, sizeof(info));
    }
    
    return 0;
}
"""

class NetworkSecurityMonitor:
    def __init__(self):
        self.b = BPF(text=network_monitor)
        
        # Attach probes
        self.b.attach_kprobe(event="tcp_v4_connect", fn_name="trace_connect_entry")
        self.b.attach_kretprobe(event="tcp_v4_connect", fn_name="trace_connect_return")
        self.b.attach_kprobe(event="__sys_bind", fn_name="trace_bind")
        
        # Connection tracking
        self.connections = defaultdict(lambda: defaultdict(int))
        self.last_cleanup = datetime.now()
        
        # Threat intelligence (example IPs)
        self.threat_ips = {
            "185.220.101.0/24": "TOR Exit Node",
            "104.21.0.0/16": "Cloudflare - Check if expected",
            "192.168.1.0/24": "Internal Network"
        }
        
        # Suspicious ports
        self.suspicious_ports = {
            22: "SSH", 23: "Telnet", 445: "SMB", 3389: "RDP",
            4444: "Metasploit Default", 5555: "Android Debug",
            6666: "Common Backdoor", 6667: "IRC",
            31337: "Elite Backdoor"
        }
    
    def check_threat_intel(self, ip):
        """Check if IP matches known threats"""
        for cidr, description in self.threat_ips.items():
            if self.ip_in_cidr(ip, cidr):
                return True, description
        return False, None
    
    def ip_in_cidr(self, ip, cidr):
        """Simple CIDR matching"""
        # Implementation left as exercise
        return False
    
    def analyze_connection(self, event):
        """Analyze connection for suspicious patterns"""
        alerts = []
        
        src_ip = socket.inet_ntoa(struct.pack('I', event.saddr))
        dst_ip = socket.inet_ntoa(struct.pack('I', event.daddr))
        process = event.comm.decode('utf-8', 'ignore').strip()
        
        # Check destination IP against threat intel
        is_threat, threat_desc = self.check_threat_intel(dst_ip)
        if is_threat:
            alerts.append(f"Connection to known threat: {threat_desc}")
        
        # Check for suspicious ports
        if event.dport in self.suspicious_ports:
            alerts.append(f"Connection to suspicious port: {event.dport} ({self.suspicious_ports[event.dport]})")
        
        # Check for suspicious processes
        suspicious_procs = ['nc', 'netcat', 'ncat', 'python', 'perl', 'ruby']
        if process in suspicious_procs and event.dport not in [80, 443]:
            alerts.append(f"Suspicious process making network connection: {process}")
        
        # Rate limiting detection
        conn_key = f"{event.pid}:{dst_ip}:{event.dport}"
        self.connections[conn_key]['count'] += 1
        self.connections[conn_key]['last_seen'] = datetime.now()
        
        if self.connections[conn_key]['count'] > 100:
            alerts.append(f"High connection rate detected: {self.connections[conn_key]['count']} connections")
        
        return alerts
    
    def process_event(self, cpu, data, size):
        event = self.b["conn_events"].event(data)
        alerts = self.analyze_connection(event)
        
        if alerts:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            src_ip = socket.inet_ntoa(struct.pack('I', event.saddr))
            dst_ip = socket.inet_ntoa(struct.pack('I', event.daddr))
            process = event.comm.decode('utf-8', 'ignore').strip()
            
            alert_msg = f"""
[NETWORK ALERT] {timestamp}
Process: {process} (PID: {event.pid})
Connection: {src_ip}:{event.sport} -> {dst_ip}:{event.dport}
Alerts: {', '.join(alerts)}
"""
            print(alert_msg)
            
            # Send to SIEM
            self.send_to_siem(alert_msg)
    
    def send_to_siem(self, alert):
        """Send alert to SIEM system"""
        # Example: Send to local syslog
        import syslog
        syslog.openlog("NetworkSecurityMonitor")
        syslog.syslog(syslog.LOG_WARNING, alert.replace('\n', ' '))
        syslog.closelog()
    
    def cleanup_old_connections(self):
        """Remove old connection tracking data"""
        now = datetime.now()
        if now - self.last_cleanup > timedelta(minutes=5):
            old_keys = []
            for key, data in self.connections.items():
                if now - data['last_seen'] > timedelta(minutes=10):
                    old_keys.append(key)
            
            for key in old_keys:
                del self.connections[key]
            
            self.last_cleanup = now
    
    def run(self):
        print("Starting network security monitor...")
        self.b["conn_events"].open_perf_buffer(self.process_event)
        
        while True:
            try:
                self.b.perf_buffer_poll(timeout=1000)
                self.cleanup_old_connections()
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    monitor = NetworkSecurityMonitor()
    monitor.run()
```

## File Integrity Monitoring with eBPF

Traditional file integrity monitoring tools scan periodically. With eBPF, we can catch changes in real-time:

```python
#!/usr/bin/env python3
from bcc import BPF
import os
import hashlib
import json
from pathlib import Path

file_monitor = """
#include <uapi/linux/ptrace.h>
#include <linux/fs.h>

struct file_event {
    u32 pid;
    u32 uid;
    char comm[TASK_COMM_LEN];
    char filename[256];
    int flags;
};

BPF_PERF_OUTPUT(file_events);

// Monitor file opens with write intent
int trace_open(struct pt_regs *ctx, const char __user *filename, int flags) {
    // Only track write operations
    if (!(flags & (O_WRONLY | O_RDWR | O_CREAT | O_TRUNC))) {
        return 0;
    }
    
    struct file_event event = {};
    
    event.pid = bpf_get_current_pid_tgid() >> 32;
    event.uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;
    event.flags = flags;
    
    bpf_get_current_comm(&event.comm, sizeof(event.comm));
    bpf_probe_read_user_str(&event.filename, sizeof(event.filename), filename);
    
    file_events.perf_submit(ctx, &event, sizeof(event));
    
    return 0;
}

// Monitor file deletions
int trace_unlink(struct pt_regs *ctx, const char __user *pathname) {
    struct file_event event = {};
    
    event.pid = bpf_get_current_pid_tgid() >> 32;
    event.uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;
    event.flags = -1;  // Special flag for deletion
    
    bpf_get_current_comm(&event.comm, sizeof(event.comm));
    bpf_probe_read_user_str(&event.filename, sizeof(event.filename), pathname);
    
    file_events.perf_submit(ctx, &event, sizeof(event));
    
    return 0;
}
"""

class FileIntegrityMonitor:
    def __init__(self, monitored_paths):
        self.b = BPF(text=file_monitor)
        self.monitored_paths = monitored_paths
        self.file_hashes = {}
        
        # Attach probes
        self.b.attach_kprobe(event="do_sys_openat2", fn_name="trace_open")
        self.b.attach_kprobe(event="do_unlinkat", fn_name="trace_unlink")
        
        # Initialize file hashes
        self.scan_initial_state()
    
    def scan_initial_state(self):
        """Create initial baseline of monitored files"""
        print("Creating file integrity baseline...")
        
        for monitored_path in self.monitored_paths:
            path = Path(monitored_path)
            if path.is_file():
                self.hash_file(path)
            elif path.is_dir():
                for file_path in path.rglob('*'):
                    if file_path.is_file():
                        self.hash_file(file_path)
        
        print(f"Baseline created: {len(self.file_hashes)} files monitored")
    
    def hash_file(self, file_path):
        """Calculate SHA256 hash of file"""
        try:
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            
            self.file_hashes[str(file_path)] = {
                'hash': sha256_hash.hexdigest(),
                'size': file_path.stat().st_size,
                'mtime': file_path.stat().st_mtime
            }
        except Exception as e:
            print(f"Error hashing {file_path}: {e}")
    
    def check_file_change(self, filepath):
        """Check if file has been modified"""
        if filepath not in self.file_hashes:
            return "NEW_FILE"
        
        try:
            current_hash = hashlib.sha256()
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    current_hash.update(byte_block)
            
            if current_hash.hexdigest() != self.file_hashes[filepath]['hash']:
                return "MODIFIED"
            
            return "UNCHANGED"
        except FileNotFoundError:
            return "DELETED"
        except Exception as e:
            return f"ERROR: {e}"
    
    def is_monitored_path(self, filepath):
        """Check if file is in monitored paths"""
        for monitored_path in self.monitored_paths:
            if filepath.startswith(monitored_path):
                return True
        return False
    
    def process_event(self, cpu, data, size):
        event = self.b["file_events"].event(data)
        filepath = event.filename.decode('utf-8', 'ignore')
        
        # Skip if not in monitored paths
        if not self.is_monitored_path(filepath):
            return
        
        process = event.comm.decode('utf-8', 'ignore').strip()
        
        # Determine event type
        if event.flags == -1:
            event_type = "DELETE"
        elif event.flags & os.O_CREAT:
            event_type = "CREATE"
        elif event.flags & os.O_TRUNC:
            event_type = "TRUNCATE"
        else:
            event_type = "MODIFY"
        
        # Check file integrity
        change_status = self.check_file_change(filepath)
        
        # Generate alert for suspicious changes
        suspicious = False
        alert_reasons = []
        
        # Check for suspicious processes
        if process in ['bash', 'sh', 'python', 'perl', 'nc', 'vim', 'vi']:
            suspicious = True
            alert_reasons.append(f"Suspicious process: {process}")
        
        # Check for sensitive files
        sensitive_patterns = ['/etc/passwd', '/etc/shadow', '/etc/sudoers', 
                            '.ssh/authorized_keys', '.bashrc', '.bash_profile']
        if any(pattern in filepath for pattern in sensitive_patterns):
            suspicious = True
            alert_reasons.append("Sensitive file modified")
        
        # Alert on any change to monitored files
        if change_status in ["MODIFIED", "DELETED", "NEW_FILE"]:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            severity = "CRITICAL" if suspicious else "MEDIUM"
            
            alert = f"""
[{severity}] File Integrity Alert - {timestamp}
File: {filepath}
Event: {event_type}
Status: {change_status}
Process: {process} (PID: {event.pid}, UID: {event.uid})
"""
            if alert_reasons:
                alert += f"Reasons: {', '.join(alert_reasons)}\n"
            
            print(alert)
            
            # Update baseline if file was modified
            if change_status == "MODIFIED" and event_type != "DELETE":
                self.hash_file(Path(filepath))
    
    def run(self):
        print("Starting file integrity monitor...")
        print(f"Monitoring paths: {', '.join(self.monitored_paths)}")
        
        self.b["file_events"].open_perf_buffer(self.process_event)
        
        while True:
            try:
                self.b.perf_buffer_poll()
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    # Monitor critical system files and directories
    monitored_paths = [
        "/etc",
        "/root/.ssh",
        "/home",
        "/usr/bin",
        "/usr/sbin"
    ]
    
    monitor = FileIntegrityMonitor(monitored_paths)
    monitor.run()
```

## Production Deployment Best Practices

### 1. Performance Optimization

```python
# Use BPF maps for filtering to reduce userspace events
filter_map = """
BPF_HASH(process_filter, char[TASK_COMM_LEN], u8);

// In your eBPF program
char comm[TASK_COMM_LEN];
bpf_get_current_comm(&comm, sizeof(comm));

u8 *should_filter = process_filter.lookup(&comm);
if (should_filter && *should_filter == 1) {
    return 0;  // Skip this process
}
"""

# Add process filtering from Python
def add_process_filter(bpf, process_name):
    process_filter = bpf.get_table("process_filter")
    process_filter[process_name.encode()] = 1
```

### 2. Error Handling and Resilience

```python
class ResilientBPFMonitor:
    def __init__(self):
        self.restart_count = 0
        self.max_restarts = 5
        
    def run_with_recovery(self):
        while self.restart_count < self.max_restarts:
            try:
                self.run()
            except Exception as e:
                self.restart_count += 1
                print(f"Monitor crashed: {e}")
                print(f"Attempting restart {self.restart_count}/{self.max_restarts}")
                time.sleep(5)
                
                # Cleanup and reinitialize
                self.cleanup()
                self.__init__()
        
        print("Max restarts reached. Exiting...")
```

### 3. Integration with SIEM/SOAR

```python
import requests
import json

class SIEMIntegration:
    def __init__(self, siem_endpoint, api_key):
        self.siem_endpoint = siem_endpoint
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def send_alert(self, alert_data):
        """Send alert to SIEM with retry logic"""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.siem_endpoint,
                    headers=self.headers,
                    json=alert_data,
                    timeout=5
                )
                
                if response.status_code == 200:
                    return True
                    
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    print(f"Failed to send to SIEM: {e}")
                    return False
                
                time.sleep(2 ** attempt)  # Exponential backoff
```

## Common Gotchas and Solutions (Learn From My Pain)

### 1. Kernel Version Compatibility (The "Why Isn't This Working?" Problem)
Different kernel versions have different function names and structures. I learned this after spending 3 hours debugging why my eBPF program worked perfectly on my laptop but crashed on production servers. Turns out, production was running a slightly older kernel with different function signatures.

Always check:

```python
# Detect kernel version and adjust
import platform

kernel_version = platform.release()
if kernel_version.startswith('5.'):
    attach_point = "do_sys_openat2"
else:
    attach_point = "do_sys_open"
```

### 2. BPF Verifier Limits (The "Computer Says No" Problem)
The BPF verifier is like that strict teacher who marks you down for handwriting. It has strict limits, and when you hit them, the error messages are... unhelpful.

Keep programs simple:
- Max 1 million instructions (sounds like a lot, but it's not)
- Limited loop iterations (no infinite loops, obviously)
- Stack size limits (512 bytes – use it wisely)

Pro tip: When the verifier rejects your code with "invalid stack access," it usually means you're trying to be too clever. Simplify.

### 3. Performance Impact (The "We Fixed Security But Broke Everything Else" Problem)
True story from my home lab: I once deployed an eBPF monitoring program so comprehensive it could track everything. It also consumed 40% CPU. On idle. My "security monitoring" had become a self-inflicted DoS attack.

Monitor your monitors! Track CPU usage:

```python
def check_monitor_performance():
    """Ensure eBPF programs aren't impacting system"""
    import psutil
    
    cpu_percent = psutil.cpu_percent(interval=1)
    if cpu_percent > 80:
        print(f"WARNING: High CPU usage: {cpu_percent}%")
        # Consider reducing monitoring frequency
```

## Future of eBPF Security

eBPF is rapidly evolving. Exciting developments include:
- **BTF (BPF Type Format)**: Write once, run anywhere
- **CO-RE (Compile Once, Run Everywhere)**: Better portability
- **eBPF for Windows**: Cross-platform security monitoring
- **Hardware offload**: eBPF on SmartNICs

## Conclusion

eBPF transforms security monitoring from reactive log analysis to proactive, real-time detection. By implementing these patterns, you can catch threats as they happen, not hours later in log reviews.

Start small with basic monitors, then expand based on your threat model. The examples here provide a foundation you can build upon for your specific security needs.

Remember: eBPF is powerful but requires careful implementation. Always test in development before deploying to production, and monitor the monitors to ensure they don't impact system performance.

The future of Linux security monitoring is here, and it's running in kernel space.

---

*Have questions about implementing eBPF security monitoring? Found interesting detection patterns? Let's connect and share knowledge!*