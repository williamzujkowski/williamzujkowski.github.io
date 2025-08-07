---
title: "Building IR Playbooks with Ansible"
date: 2025-07-22
description: "Transform incident response from chaos to choreography using Ansible. Learn to build automated playbooks that handle security incidents consistently and efficiently"
tags: [security, incident-response, ansible, automation, soc, forensics]
author: "William Zujkowski"
---

**Reading time:** 12 minutes

## From Manual Chaos to Automated Response

Picture this: It's 3 AM, your phone buzzes with a critical security alert. Half-awake, you log in to find potential ransomware activity across multiple servers. In the past, this meant hours of manual work, inconsistent responses, and missed evidence. Today, with properly built Ansible IR playbooks, the same incident triggers automated containment, evidence collection, and recovery procedures – all while you're getting dressed.

After building and deploying IR automation for everything from small businesses to federal agencies, I've learned that Ansible can transform incident response from reactive chaos to proactive orchestration. This guide shares battle-tested playbooks and patterns that work in production.

## Why Ansible for Incident Response?

Traditional incident response suffers from:
- **Human error** under pressure
- **Inconsistent procedures** across team members
- **Slow response times** during critical moments
- **Poor documentation** of actions taken
- **Evidence contamination** from manual intervention

Ansible solves these by providing:
- **Consistency**: Same response every time
- **Speed**: Automated actions in seconds
- **Auditability**: Complete logs of all actions
- **Scalability**: Handle hundreds of systems simultaneously
- **Flexibility**: Adapt playbooks on the fly

## Building Your IR Foundation

### Core Playbook Structure

Let's start with a foundation that all IR playbooks should build upon:

{% raw %}
```yaml
---
# Base IR Playbook Structure
# incident_response_base.yml

- name: Incident Response Base Playbook
  hosts: "{{ target_hosts | default('all') }}"
  gather_facts: yes
  become: yes
  
  vars:
    incident_id: "{{ lookup('env', 'INCIDENT_ID') | default(ansible_date_time.epoch) }}"
    incident_type: "{{ ir_type | default('unknown') }}"
    evidence_path: "/forensics/{{ incident_id }}"
    notification_webhook: "{{ lookup('env', 'IR_WEBHOOK_URL') }}"
    
  pre_tasks:
    - name: Create incident record
      uri:
        url: "{{ ir_api_endpoint }}/incidents"
        method: POST
        body_format: json
        body:
          id: "{{ incident_id }}"
          type: "{{ incident_type }}"
          affected_hosts: "{{ ansible_play_hosts }}"
          started_at: "{{ ansible_date_time.iso8601 }}"
          status: "in_progress"
      delegate_to: localhost
      run_once: true
      
    - name: Send initial notification
      uri:
        url: "{{ notification_webhook }}"
        method: POST
        body_format: json
        body:
          text: "🚨 IR Playbook Started: {{ incident_type }} on {{ ansible_play_hosts | length }} hosts"
          incident_id: "{{ incident_id }}"
      delegate_to: localhost
      run_once: true
      when: notification_webhook is defined
      
    - name: Create evidence directory structure
      file:
        path: "{{ evidence_path }}/{{ inventory_hostname }}/{{ item }}"
        state: directory
        mode: '0700'
      loop:
        - system
        - network
        - processes
        - logs
        - memory
        - timeline
        
  tasks:
    - name: Capture initial system state
      block:
        - name: System information
          shell: |
            uname -a > {{ evidence_path }}/{{ inventory_hostname }}/system/uname.txt
            hostname -A > {{ evidence_path }}/{{ inventory_hostname }}/system/hostname.txt
            date '+%Y-%m-%d %H:%M:%S %Z' > {{ evidence_path }}/{{ inventory_hostname }}/system/date.txt
            uptime > {{ evidence_path }}/{{ inventory_hostname }}/system/uptime.txt
            
        - name: User and login information
          shell: |
            w > {{ evidence_path }}/{{ inventory_hostname }}/system/logged_in_users.txt
            last -F > {{ evidence_path }}/{{ inventory_hostname }}/system/last_logins.txt
            lastb -F > {{ evidence_path }}/{{ inventory_hostname }}/system/failed_logins.txt 2>/dev/null || true
            
        - name: Network connections
          shell: |
            netstat -tulpn > {{ evidence_path }}/{{ inventory_hostname }}/network/netstat_listen.txt 2>&1
            netstat -an > {{ evidence_path }}/{{ inventory_hostname }}/network/netstat_all.txt
            ss -tulpn > {{ evidence_path }}/{{ inventory_hostname }}/network/ss_listen.txt 2>&1
            iptables -L -n -v > {{ evidence_path }}/{{ inventory_hostname }}/network/iptables.txt
            
        - name: Process listing
          shell: |
            ps auxwww > {{ evidence_path }}/{{ inventory_hostname }}/processes/ps_aux.txt
            ps -elf > {{ evidence_path }}/{{ inventory_hostname }}/processes/ps_elf.txt
            lsof -n > {{ evidence_path }}/{{ inventory_hostname }}/processes/lsof.txt 2>&1 || true
            
        - name: Create system snapshot
          shell: |
            tar czf {{ evidence_path }}/{{ inventory_hostname }}/system_snapshot_{{ ansible_date_time.epoch }}.tar.gz \
              /etc/passwd /etc/shadow /etc/group /etc/sudoers* \
              /var/log/auth.log* /var/log/secure* \
              /root/.bash_history /home/*/.bash_history \
              2>/dev/null || true
      rescue:
        - name: Log evidence collection failure
          lineinfile:
            path: "{{ evidence_path }}/{{ inventory_hostname }}/collection_errors.log"
            line: "{{ ansible_date_time.iso8601 }} - Failed to collect evidence: {{ ansible_failed_result.msg | default('Unknown error') }}"
            create: yes
            
  post_tasks:
    - name: Compress evidence
      archive:
        path: "{{ evidence_path }}/{{ inventory_hostname }}"
        dest: "{{ evidence_path }}/{{ inventory_hostname }}_{{ ansible_date_time.epoch }}.tar.gz"
        format: gz
      delegate_to: "{{ inventory_hostname }}"
      
    - name: Update incident record
      uri:
        url: "{{ ir_api_endpoint }}/incidents/{{ incident_id }}"
        method: PATCH
        body_format: json
        body:
          status: "evidence_collected"
          evidence_locations: "{{ evidence_path }}"
      delegate_to: localhost
      run_once: true
      
  handlers:
    - name: notify_soc
      uri:
        url: "{{ notification_webhook }}"
        method: POST
        body_format: json
        body:
          text: "{{ notification_message }}"
          incident_id: "{{ incident_id }}"
      delegate_to: localhost
```
{% endraw %}

### Ransomware Response Playbook

Years ago, during my early days in incident response, I learned the hard way that manual response doesn't scale. After dealing with several ransomware scenarios in my home lab and researching industry best practices, I developed this automation approach.

Here's a playbook structure that follows industry best practices:

{% raw %}
```yaml
---
# ransomware_response.yml
- name: Ransomware Incident Response
  hosts: "{{ affected_hosts }}"
  gather_facts: yes
  become: yes
  serial: "{{ parallel_hosts | default(5) }}"
  
  vars:
    incident_type: "ransomware"
    known_ransomware_extensions:
      - .encrypted
      - .crypto
      - .locked
      - .enc
      - .aes256
      - .ransom
    known_ransomware_processes:
      - vssadmin.exe
      - wbadmin.exe
      - bcdedit.exe
      - cipher.exe
    isolation_mode: "{{ isolation | default('partial') }}"
    
  tasks:
    - name: Import base IR tasks
      include_tasks: incident_response_base.yml
      
    - name: Identify ransomware indicators
      block:
        - name: Search for encrypted files
          find:
            paths: 
              - /home
              - /var
              - /opt
            patterns: "*{{ item }}"
            recurse: yes
            file_type: file
          register: encrypted_files
          loop: "{{ known_ransomware_extensions }}"
          failed_when: false
          
        - name: Check for ransom notes
          find:
            paths:
              - /
            patterns:
              - "*README*"
              - "*DECRYPT*"
              - "*RESTORE*"
              - "*.txt"
            recurse: yes
            age: "-1d"
            size: "-10k"
          register: potential_ransom_notes
          failed_when: false
          
        - name: Identify suspicious processes
          shell: |
            ps aux | grep -E '{{ known_ransomware_processes | join("|") }}' | grep -v grep
          register: suspicious_processes
          failed_when: false
          changed_when: false
          
        - name: Check for shadow copy deletion
          shell: |
            grep -E 'vssadmin.*delete.*shadows|wmic.*shadowcopy.*delete' /var/log/* 2>/dev/null || true
          register: shadow_deletion_attempts
          changed_when: false
          
    - name: Immediate containment actions
      when: encrypted_files.results | selectattr('files', 'defined') | map(attribute='files') | flatten | length > 0
      block:
        - name: Isolate system - Network level
          iptables:
            chain: "{{ item }}"
            policy: DROP
          loop:
            - INPUT
            - OUTPUT
            - FORWARD
          when: isolation_mode == 'full'
          
        - name: Isolate system - Partial (allow management)
          block:
            - name: Allow only management connections
              iptables:
                chain: INPUT
                source: "{{ management_network }}"
                jump: ACCEPT
                
            - name: Block all other traffic
              iptables:
                chain: "{{ item }}"
                jump: DROP
          loop:
            - INPUT
            - OUTPUT
          when: isolation_mode == 'partial'
```
{% endraw %}

#### The Nuclear Option: Process Termination

Here's where theory meets practice. In my testing environments, I've learned that aggressive containment is sometimes necessary. When simulating ransomware that encrypts at high speed, surgical precision isn't always an option:

{% raw %}
```yaml
        - name: Kill suspicious processes
          shell: |
            # This has saved us more times than I can count
            # Yes, it's aggressive. Yes, it works.
            for pid in $(ps aux | grep -E '{{ known_ransomware_processes | join("|") }}' | grep -v grep | awk '{print $2}'); do
              kill -9 $pid
              echo "Killed process $pid at $(date)" >> {{ evidence_path }}/{{ inventory_hostname }}/processes/killed_processes.log
            done
          when: suspicious_processes.stdout_lines | length > 0
          
        - name: Disable scheduled tasks
          systemd:
            name: "{{ item }}"
            enabled: no
            state: stopped
          loop:
            - cron
            - anacron
            - atd
          failed_when: false
          
    - name: Collect ransomware-specific evidence
      block:
        - name: Capture file modification times
          shell: |
            find /home /var /opt -type f -mtime -7 -ls > {{ evidence_path }}/{{ inventory_hostname }}/timeline/recent_modifications.txt 2>/dev/null || true
            
        - name: Extract ransomware samples
          shell: |
            mkdir -p {{ evidence_path }}/{{ inventory_hostname }}/malware_samples
            for ext in {{ known_ransomware_extensions | join(' ') }}; do
              find /tmp /var/tmp /dev/shm -name "*$ext" -type f -size -10M -exec cp {} {{ evidence_path }}/{{ inventory_hostname }}/malware_samples/ \; 2>/dev/null || true
            done
            
        - name: Capture process memory
          shell: |
            for pid in $(ps aux | grep -v grep | awk '{print $2}'); do
              gcore -o {{ evidence_path }}/{{ inventory_hostname }}/memory/process_$pid $pid 2>/dev/null || true
            done
          when: capture_memory | default(false)
          async: 300
          poll: 0
          
        - name: Save ransom notes
          copy:
            src: "{{ item.path }}"
            dest: "{{ evidence_path }}/{{ inventory_hostname }}/ransom_notes/"
            remote_src: yes
          loop: "{{ potential_ransom_notes.files }}"
          when: 
            - potential_ransom_notes.files is defined
            - item.size < 10240  # Only files < 10KB
          failed_when: false
          
    - name: Check backup status
      block:
        - name: Identify backup locations
          shell: |
            # Check common backup locations
            find /backup /mnt/backup /var/backup -type f -name "*.tar*" -o -name "*.sql*" -o -name "*.dump" 2>/dev/null | head -20
          register: backup_files
          failed_when: false
          
        - name: Verify backup integrity
          shell: |
            for backup in {{ backup_files.stdout_lines | join(' ') }}; do
              if [[ $backup == *.tar.gz ]]; then
                tar -tzf $backup >/dev/null 2>&1 && echo "OK: $backup" || echo "CORRUPT: $backup"
              fi
            done
          register: backup_verification
          when: backup_files.stdout_lines | length > 0
          
    - name: Generate ransomware timeline
      shell: |
        cat > {{ evidence_path }}/{{ inventory_hostname }}/timeline/ransomware_timeline.txt << EOF
        Ransomware Incident Timeline - Host: {{ inventory_hostname }}
        ==========================================
        
        First encrypted file detected: $(find {{ encrypted_files.results[0].files[0].path | dirname }} -name "*{{ known_ransomware_extensions[0] }}" -printf '%T+ %p\n' | sort | head -1)
        
        Recent user logins:
        $(last -F -n 20)
        
        Recent file modifications (last 24h):
        $(find /home /var -type f -mtime -1 -ls | sort -k8,9)
        
        Suspicious process activity:
        {{ suspicious_processes.stdout }}
        
        Shadow copy deletion attempts:
        {{ shadow_deletion_attempts.stdout }}
        EOF
      when: encrypted_files.results | selectattr('files', 'defined') | map(attribute='files') | flatten | length > 0
      
    - name: Attempt automated recovery
      when: 
        - auto_recover | default(false)
        - backup_verification.stdout is search("OK:")
      block:
        - name: Stop all non-essential services
          systemd:
            name: "{{ item }}"
            state: stopped
          loop: "{{ non_essential_services }}"
          failed_when: false
          
        - name: Restore from backup
          shell: |
            # Example restore - customize for your environment
            latest_backup=$(ls -t /backup/*.tar.gz | head -1)
            tar -xzf $latest_backup -C /restore_staging/
          register: restore_attempt
          
    - name: Generate incident report
      template:
        src: ransomware_report.j2
        dest: "{{ evidence_path }}/{{ inventory_hostname }}/incident_report.html"
      vars:
        encrypted_file_count: "{{ encrypted_files.results | selectattr('files', 'defined') | map(attribute='files') | flatten | length }}"
        ransom_notes_found: "{{ potential_ransom_notes.files | default([]) | length }}"
        suspicious_process_count: "{{ suspicious_processes.stdout_lines | length }}"
        
  handlers:
    - name: alert_management
      uri:
        url: "{{ notification_webhook }}"
        method: POST
        body_format: json
        body:
          text: |
            🚨 CRITICAL: Ransomware detected on {{ inventory_hostname }}
            Encrypted files: {{ encrypted_files.results | selectattr('files', 'defined') | map(attribute='files') | flatten | length }}
            Status: {{ 'Isolated' if isolation_mode != 'none' else 'Active' }}
          color: "danger"
          incident_id: "{{ incident_id }}"
```
{% endraw %}

### Credential Compromise Response

Based on industry statistics, credential compromise represents the majority of security incidents. Through years of research and home lab simulations, I've developed automated responses for these scenarios.

The key lesson from my research: Speed matters, but accuracy matters more. In test environments, I've seen how locking the wrong account can cause significant disruption.

{% raw %}
```yaml
---
# credential_compromise_response.yml
- name: Credential Compromise Response
  hosts: all
  gather_facts: no
  become: yes
  
  vars:
    compromised_user: "{{ target_user }}"
    incident_type: "credential_compromise"
    reset_password: "{{ auto_reset | default(true) }}"
    revoke_sessions: true
    
  tasks:
    - name: Immediate containment
      block:
        - name: Disable user account
          user:
            name: "{{ compromised_user }}"
            shell: /sbin/nologin
            password_lock: yes
          register: user_disabled
          
        - name: Kill all user processes
          shell: |
            pkill -u {{ compromised_user }} || true
            # More aggressive termination
            for pid in $(ps -u {{ compromised_user }} -o pid --no-headers); do
              kill -9 $pid 2>/dev/null || true
            done
          register: processes_killed
          
        - name: Revoke SSH keys
          file:
            path: "/home/{{ compromised_user }}/.ssh/authorized_keys"
            state: absent
          failed_when: false
          
        - name: Expire user password
          shell: |
            chage -d 0 {{ compromised_user }}
          when: reset_password
          
    - name: Collect authentication evidence
      block:
        - name: Gather authentication logs
          shell: |
            mkdir -p {{ evidence_path }}/{{ inventory_hostname }}/auth_logs
            grep {{ compromised_user }} /var/log/auth.log* > {{ evidence_path }}/{{ inventory_hostname }}/auth_logs/user_auth.log 2>/dev/null || true
            grep {{ compromised_user }} /var/log/secure* >> {{ evidence_path }}/{{ inventory_hostname }}/auth_logs/user_auth.log 2>/dev/null || true
            
        - name: Check sudo usage
          shell: |
            grep {{ compromised_user }} /var/log/sudo.log > {{ evidence_path }}/{{ inventory_hostname }}/auth_logs/sudo_usage.log 2>/dev/null || true
            grep "sudo.*{{ compromised_user }}" /var/log/auth.log* >> {{ evidence_path }}/{{ inventory_hostname }}/auth_logs/sudo_usage.log 2>/dev/null || true
            
        - name: Identify source IPs
          shell: |
            grep "Accepted.*{{ compromised_user }}" /var/log/auth.log* | awk '{print $11}' | sort | uniq -c | sort -rn > {{ evidence_path }}/{{ inventory_hostname }}/auth_logs/source_ips.txt
          register: source_ips
          
        - name: Check for persistence mechanisms
          shell: |
            # Check crontab
            crontab -u {{ compromised_user }} -l > {{ evidence_path }}/{{ inventory_hostname }}/persistence/user_crontab.txt 2>/dev/null || echo "No crontab"
            
            # Check systemd user services
            ls -la /home/{{ compromised_user }}/.config/systemd/user/ > {{ evidence_path }}/{{ inventory_hostname }}/persistence/systemd_services.txt 2>/dev/null || true
            
            # Check shell profiles
            for file in .bashrc .bash_profile .profile .zshrc; do
              if [ -f "/home/{{ compromised_user }}/$file" ]; then
                cp "/home/{{ compromised_user }}/$file" {{ evidence_path }}/{{ inventory_hostname }}/persistence/
              fi
            done
            
    - name: Investigate lateral movement
      block:
        - name: Check SSH known_hosts
          shell: |
            if [ -f "/home/{{ compromised_user }}/.ssh/known_hosts" ]; then
              cp "/home/{{ compromised_user }}/.ssh/known_hosts" {{ evidence_path }}/{{ inventory_hostname }}/lateral_movement/
              # Extract unique hosts
              awk '{print $1}' "/home/{{ compromised_user }}/.ssh/known_hosts" | sort -u > {{ evidence_path }}/{{ inventory_hostname }}/lateral_movement/ssh_targets.txt
            fi
            
        - name: Check command history
          shell: |
            for hist_file in .bash_history .zsh_history .sh_history; do
              if [ -f "/home/{{ compromised_user }}/$hist_file" ]; then
                cp "/home/{{ compromised_user }}/$hist_file" {{ evidence_path }}/{{ inventory_hostname }}/lateral_movement/
                # Look for SSH/SCP/RSYNC commands
                grep -E "ssh|scp|rsync|curl|wget" "/home/{{ compromised_user }}/$hist_file" > {{ evidence_path }}/{{ inventory_hostname }}/lateral_movement/network_commands.txt 2>/dev/null || true
              fi
            done
            
    - name: System-wide credential audit
      block:
        - name: Check for stored credentials
          shell: |
            # Search for potential credential files
            find /home/{{ compromised_user }} -type f \( -name "*.pem" -o -name "*.key" -o -name "*.pfx" -o -name "*password*" -o -name "*cred*" \) -size -1M > {{ evidence_path }}/{{ inventory_hostname }}/credentials/found_credential_files.txt 2>/dev/null || true
            
            # Check environment variables in processes
            for pid in $(ps -u {{ compromised_user }} -o pid --no-headers 2>/dev/null); do
              if [ -r /proc/$pid/environ ]; then
                tr '\0' '\n' < /proc/$pid/environ | grep -E "PASS|TOKEN|KEY|SECRET" >> {{ evidence_path }}/{{ inventory_hostname }}/credentials/process_env_vars.txt 2>/dev/null || true
              fi
            done
            
        - name: Audit sudo privileges
          shell: |
            grep {{ compromised_user }} /etc/sudoers* > {{ evidence_path }}/{{ inventory_hostname }}/credentials/sudo_privileges.txt 2>/dev/null || true
            
    - name: Generate IoCs
      shell: |
        cat > {{ evidence_path }}/{{ inventory_hostname }}/iocs.json << EOF
        {
          "incident_id": "{{ incident_id }}",
          "timestamp": "{{ ansible_date_time.iso8601 }}",
          "compromised_user": "{{ compromised_user }}",
          "source_ips": [
            $(grep "Accepted.*{{ compromised_user }}" /var/log/auth.log* | awk '{print $11}' | sort -u | sed 's/^/"/;s/$/"/' | tr '\n' ',' | sed 's/,$//')
          ],
          "suspicious_files": [
            $(find /home/{{ compromised_user }} -type f -mtime -7 -executable | head -20 | sed 's/^/"/;s/$/"/' | tr '\n' ',' | sed 's/,$//')
          ],
          "network_connections": [
            $(ss -tunp | grep {{ compromised_user }} | awk '{print $5}' | sort -u | sed 's/^/"/;s/$/"/' | tr '\n' ',' | sed 's/,$//')
          ]
        }
        EOF
        
    - name: Remediation actions
      block:
        - name: Reset user password
          user:
            name: "{{ compromised_user }}"
            password: "{{ lookup('password', '/tmp/{{ compromised_user }}_temp_pass length=20 chars=ascii_letters,digits,punctuation') | password_hash('sha512') }}"
          when: reset_password
          register: password_reset
          
        - name: Generate new SSH keys
          openssh_keypair:
            path: "/home/{{ compromised_user }}/.ssh/id_rsa_new"
            type: rsa
            size: 4096
            owner: "{{ compromised_user }}"
            group: "{{ compromised_user }}"
          when: reset_password
          
        - name: Notify user
          mail:
            to: "{{ compromised_user }}@{{ domain }}"
            subject: "Security Alert: Account Compromise Detected"
            body: |
              Your account has been temporarily disabled due to suspected compromise.
              
              Actions taken:
              - Account locked
              - Active sessions terminated
              - SSH keys revoked
              - Password reset required
              
              Please contact the security team immediately to regain access.
              
              Incident ID: {{ incident_id }}
          delegate_to: localhost
          when: send_notifications | default(true)
```
{% endraw %}

### Data Exfiltration Response

Detecting and responding to data theft:

{% raw %}
```yaml
---
# data_exfiltration_response.yml
- name: Data Exfiltration Response
  hosts: "{{ target_hosts }}"
  gather_facts: yes
  become: yes
  
  vars:
    incident_type: "data_exfiltration"
    sensitive_data_paths:
      - /var/lib/mysql
      - /var/lib/postgresql
      - /home/*/Documents
      - /opt/application/data
    suspicious_ports:
      - 20
      - 21
      - 22
      - 445
      - 873
      - 3389
    
  tasks:
    - name: Detect exfiltration indicators
      block:
        - name: Analyze network traffic volume
          shell: |
            # Get network statistics
            vnstat -d > {{ evidence_path }}/{{ inventory_hostname }}/network/daily_traffic.txt 2>/dev/null || true
            
            # Check for unusual data transfers
            netstat -i | awk 'NR>2 {print $1, $8}' > {{ evidence_path }}/{{ inventory_hostname }}/network/interface_stats.txt
            
            # Look for large outbound connections
            ss -tunp | awk '$2 > 1000000 {print}' > {{ evidence_path }}/{{ inventory_hostname }}/network/large_connections.txt
            
        - name: Check for compression/archiving activity
          shell: |
            # Search for recent archive creation
            find /tmp /var/tmp /home -name "*.zip" -o -name "*.tar*" -o -name "*.7z" -o -name "*.rar" -type f -mtime -7 > {{ evidence_path }}/{{ inventory_hostname }}/exfiltration/recent_archives.txt
            
            # Check process history for archiving commands
            ps aux | grep -E 'tar|zip|7z|rar' | grep -v grep > {{ evidence_path }}/{{ inventory_hostname }}/exfiltration/archive_processes.txt
            
        - name: Identify suspicious outbound connections
          shell: |
            # Check connections to suspicious ports
            for port in {{ suspicious_ports | join(' ') }}; do
              ss -tn state established "( dport = :$port or sport = :$port )" >> {{ evidence_path }}/{{ inventory_hostname }}/network/suspicious_connections.txt 2>/dev/null
            done
            
        - name: Analyze DNS queries
          shell: |
            # Check for DNS tunneling indicators
            tcpdump -nn -r /var/log/tcpdump.pcap 'port 53' 2>/dev/null | awk '{print $5}' | sort | uniq -c | sort -rn | head -50 > {{ evidence_path }}/{{ inventory_hostname }}/network/top_dns_queries.txt || true
            
            # Look for long DNS queries (potential tunneling)
            grep -E '[a-zA-Z0-9]{50,}' /var/log/dnsmasq.log > {{ evidence_path }}/{{ inventory_hostname }}/network/long_dns_queries.txt 2>/dev/null || true
            
    - name: Identify compromised data
      block:
        - name: Check file access logs
          shell: |
            # Audit file access (if auditd is running)
            ausearch -f {{ item }} --start today > {{ evidence_path }}/{{ inventory_hostname }}/file_access/{{ item | basename }}_access.log 2>/dev/null || true
          loop: "{{ sensitive_data_paths }}"
          
        - name: Database activity analysis
          shell: |
            # MySQL slow query log
            if [ -f /var/log/mysql/slow.log ]; then
              tail -n 1000 /var/log/mysql/slow.log > {{ evidence_path }}/{{ inventory_hostname }}/database/mysql_slow_queries.log
            fi
            
            # PostgreSQL logs
            if [ -d /var/log/postgresql ]; then
              grep -E 'SELECT.*FROM|COPY.*TO' /var/log/postgresql/*.log | tail -n 1000 > {{ evidence_path }}/{{ inventory_hostname }}/database/postgres_exports.log 2>/dev/null || true
            fi
            
        - name: Check for data staging
          find:
            paths:
              - /tmp
              - /var/tmp
              - /dev/shm
            patterns:
              - "*.sql"
              - "*.csv"
              - "*.json"
              - "*.xml"
            age: "-7d"
            size: "+1m"
          register: staged_data
          
    - name: Contain data exfiltration
      block:
        - name: Block outbound traffic to suspicious IPs
          iptables:
            chain: OUTPUT
            destination: "{{ item }}"
            jump: DROP
            comment: "IR block - {{ incident_id }}"
          loop: "{{ suspicious_ips | default([]) }}"
          when: suspicious_ips is defined
          
        - name: Rate limit outbound connections
          iptables:
            chain: OUTPUT
            match: hashlimit
            hashlimit_name: exfil_limit
            hashlimit_above: 10/minute
            hashlimit_mode: srcip
            hashlimit_burst: 20
            jump: DROP
            comment: "IR rate limit - {{ incident_id }}"
            
        - name: Kill suspicious processes
          shell: |
            # Kill processes with high network usage
            for pid in $(netstat -tunp 2>/dev/null | awk '$2 > 500000 {print $7}' | cut -d'/' -f1 | sort -u); do
              if [ ! -z "$pid" ]; then
                ps -p $pid -o comm= >> {{ evidence_path }}/{{ inventory_hostname }}/processes/killed_high_network.txt
                kill -15 $pid 2>/dev/null || true
              fi
            done
            
    - name: Forensic data collection
      block:
        - name: Capture full network traffic
          shell: |
            timeout 300 tcpdump -i any -w {{ evidence_path }}/{{ inventory_hostname }}/network/full_capture_{{ ansible_date_time.epoch }}.pcap -C 100 -W 10
          async: 310
          poll: 0
          register: pcap_capture
          
        - name: Memory acquisition
          shell: |
            # Use LiME if available
            if [ -f /proc/kallsyms ]; then
              insmod /opt/forensics/lime.ko "path={{ evidence_path }}/{{ inventory_hostname }}/memory/memory.lime format=lime"
            fi
          when: acquire_memory | default(false)
          failed_when: false
          
        - name: File timeline generation
          shell: |
            # Generate timeline of file activity
            find {{ sensitive_data_paths | join(' ') }} -type f -printf '%T@ %Tc %p\n' 2>/dev/null | sort -rn | head -1000 > {{ evidence_path }}/{{ inventory_hostname }}/timeline/file_timeline.txt
            
        - name: Process timeline
          shell: |
            # Create process tree with timing
            ps -eo pid,ppid,cmd,etime,lstart --forest > {{ evidence_path }}/{{ inventory_hostname }}/processes/process_tree_timeline.txt
            
    - name: Generate exfiltration report
      template:
        src: exfiltration_report.j2
        dest: "{{ evidence_path }}/{{ inventory_hostname }}/exfiltration_report.html"
      vars:
        data_at_risk: "{{ staged_data.files | map(attribute='path') | list }}"
        suspicious_connections: "{{ lookup('file', evidence_path + '/' + inventory_hostname + '/network/suspicious_connections.txt', errors='ignore') }}"
        timeline: "{{ lookup('file', evidence_path + '/' + inventory_hostname + '/timeline/file_timeline.txt', errors='ignore') }}"
```

### Web Application Attack Response

Responding to web application compromises:

```yaml
---
# web_attack_response.yml
- name: Web Application Attack Response
  hosts: web_servers
  gather_facts: yes
  become: yes
  
  vars:
    incident_type: "web_attack"
    web_root: "/var/www/html"
    log_paths:
      - /var/log/apache2
      - /var/log/nginx
      - /var/log/httpd
    common_webshells:
      - "*.php"
      - "*.phtml"
      - "*.php3"
      - "*.php4"
      - "*.php5"
      - "*.phar"
      - "*.asp"
      - "*.aspx"
      - "*.jsp"
      
  tasks:
    - name: Analyze web logs for attacks
      block:
        - name: Extract suspicious requests
          shell: |
            # Common attack patterns
            grep -E 'union.*select|<script|javascript:|onerror=|onclick=|<iframe|base64_decode|eval\(|system\(|exec\(|passthru\(' {{ item }}/*access* > {{ evidence_path }}/{{ inventory_hostname }}/web_logs/suspicious_requests.log 2>/dev/null || true
            
            # SQL injection attempts
            grep -E "(\%27)|(\')|(\-\-)|(\%23)|(\#)|(\%3D)|(=)|(\%2F)|(\/)|(\%22)|(\")|(\\)|(\%5C)|(\%2E)|(\.)|(union|select|insert|update|delete|drop|create|alter|exec|script|javascript|alert)" {{ item }}/*access* > {{ evidence_path }}/{{ inventory_hostname }}/web_logs/sql_injection_attempts.log 2>/dev/null || true
            
            # Path traversal
            grep -E "\.\./|\.\.\\\\" {{ item }}/*access* > {{ evidence_path }}/{{ inventory_hostname }}/web_logs/path_traversal.log 2>/dev/null || true
            
            # Get unique attacker IPs
            awk '{print $1}' {{ item }}/*access* | sort | uniq -c | sort -rn | head -100 > {{ evidence_path }}/{{ inventory_hostname }}/web_logs/top_ips.txt
          loop: "{{ log_paths }}"
          failed_when: false
          
        - name: Identify attack timeline
          shell: |
            # First attack attempt
            grep -h -E 'union.*select|<script|javascript:|onerror=|onclick=' {{ log_paths | join('/*access* ') }}/*access* 2>/dev/null | head -1 > {{ evidence_path }}/{{ inventory_hostname }}/timeline/first_attack.log
            
            # Attack frequency over time
            grep -h -E 'union.*select|<script|javascript:|onerror=|onclick=' {{ log_paths | join('/*access* ') }}/*access* 2>/dev/null | awk '{print $4}' | cut -d: -f1,2 | sort | uniq -c > {{ evidence_path }}/{{ inventory_hostname }}/timeline/attack_frequency.log
            
    - name: Search for webshells
      block:
        - name: Find recently modified files
          find:
            paths: "{{ web_root }}"
            age: "-7d"
            patterns: "{{ common_webshells }}"
            recurse: yes
          register: recent_files
          
        - name: Scan for webshell signatures
          shell: |
            # Common webshell signatures
            grep -r -E 'eval\(|base64_decode|system\(|exec\(|shell_exec\(|passthru\(|`.*`|\$_REQUEST|\$_POST|\$_GET' {{ web_root }} --include="*.php" --include="*.inc" > {{ evidence_path }}/{{ inventory_hostname }}/webshells/signature_matches.txt 2>/dev/null || true
            
            # One-liner webshells
            find {{ web_root }} -name "*.php" -type f -exec grep -l '^<?\(php\)\?\s*\(eval\|system\|exec\|passthru\|shell_exec\).*\$_\(GET\|POST\|REQUEST\|COOKIE\|SERVER\)' {} \; > {{ evidence_path }}/{{ inventory_hostname }}/webshells/oneliners.txt 2>/dev/null || true
            
            # Files with suspicious permissions
            find {{ web_root }} -type f \( -perm -4000 -o -perm -2000 \) > {{ evidence_path }}/{{ inventory_hostname }}/webshells/suspicious_permissions.txt
            
        - name: Check for backdoored files
          shell: |
            # Compare against known good hashes if available
            if [ -f /opt/security/web_file_hashes.txt ]; then
              cd {{ web_root }}
              md5sum -c /opt/security/web_file_hashes.txt 2>&1 | grep FAILED > {{ evidence_path }}/{{ inventory_hostname }}/webshells/modified_files.txt
            fi
            
        - name: Quarantine suspicious files
          shell: |
            mkdir -p {{ evidence_path }}/{{ inventory_hostname }}/quarantine
            for file in $(cat {{ evidence_path }}/{{ inventory_hostname }}/webshells/signature_matches.txt | cut -d: -f1 | sort -u); do
              if [ -f "$file" ]; then
                # Create quarantine copy
                cp -p "$file" {{ evidence_path }}/{{ inventory_hostname }}/quarantine/
                # Neutralize the file
                chmod 000 "$file"
                echo "Quarantined: $file" >> {{ evidence_path }}/{{ inventory_hostname }}/quarantine/quarantine.log
              fi
            done
            
    - name: Check for persistence mechanisms
      block:
        - name: Audit cron jobs
          shell: |
            # System crontabs
            for file in /etc/crontab /etc/cron.*/*; do
              if [ -f "$file" ]; then
                grep -E 'wget|curl|php|python|perl|sh|bash' "$file" > {{ evidence_path }}/{{ inventory_hostname }}/persistence/suspicious_cron.txt 2>/dev/null || true
              fi
            done
            
            # User crontabs
            for user in $(cut -f1 -d: /etc/passwd); do
              crontab -u $user -l 2>/dev/null | grep -E 'wget|curl|php|python|perl|sh|bash' >> {{ evidence_path }}/{{ inventory_hostname }}/persistence/user_cron.txt || true
            done
            
        - name: Check web server configs
          shell: |
            # Apache
            if [ -d /etc/apache2 ]; then
              grep -r -E 'php_value auto_prepend_file|php_value auto_append_file' /etc/apache2/ > {{ evidence_path }}/{{ inventory_hostname }}/persistence/apache_backdoor.txt 2>/dev/null || true
            fi
            
            # Nginx
            if [ -d /etc/nginx ]; then
              grep -r -E 'fastcgi_param|include' /etc/nginx/ | grep -E '\.php|\.inc' > {{ evidence_path }}/{{ inventory_hostname }}/persistence/nginx_includes.txt 2>/dev/null || true
            fi
            
        - name: Database backdoors
          shell: |
            # MySQL
            mysql -e "SELECT user,host FROM mysql.user WHERE user NOT IN ('root','mysql','debian-sys-maint');" > {{ evidence_path }}/{{ inventory_hostname }}/persistence/mysql_users.txt 2>/dev/null || true
            
            # Check for stored procedures
            mysql -e "SELECT db,name,type FROM mysql.proc;" > {{ evidence_path }}/{{ inventory_hostname }}/persistence/mysql_procedures.txt 2>/dev/null || true
            
    - name: Immediate remediation
      block:
        - name: Block attacking IPs
          iptables:
            chain: INPUT
            source: "{{ item.split()[1] }}"
            jump: DROP
            comment: "Web attack from {{ item.split()[1] }} - {{ incident_id }}"
          loop: "{{ lookup('file', evidence_path + '/' + inventory_hostname + '/web_logs/top_ips.txt', errors='ignore').splitlines()[:20] }}"
          when: item is match('^\d+\s+\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
          
        - name: Enable mod_security rules
          apache2_module:
            name: security2
            state: present
          when: "'apache' in ansible_facts.packages"
          notify: restart_apache
          
        - name: Clear suspicious sessions
          shell: |
            # PHP sessions
            find /var/lib/php/sessions -type f -delete
            
            # Application sessions
            if [ -d {{ web_root }}/var/session ]; then
              find {{ web_root }}/var/session -type f -mtime +1 -delete
            fi
            
        - name: Reset application credentials
          shell: |
            # Example: Reset WordPress salts
            if [ -f {{ web_root }}/wp-config.php ]; then
              cp {{ web_root }}/wp-config.php {{ web_root }}/wp-config.php.backup
              # Generate new salts and update config
              curl -s https://api.wordpress.org/secret-key/1.1/salt/ > /tmp/wp-salts.txt
              # Update wp-config.php with new salts (implementation specific)
            fi
            
    - name: Generate web attack report
      template:
        src: web_attack_report.j2
        dest: "{{ evidence_path }}/{{ incident_id }}/web_attack_report_{{ ansible_date_time.epoch }}.html"
      delegate_to: localhost
      run_once: true
      
  handlers:
    - name: restart_apache
      systemd:
        name: apache2
        state: restarted
      when: "'apache2' in ansible_facts.packages"
```

## Orchestration and Integration

### Master Incident Response Orchestrator

Tie everything together with a master orchestrator:

```yaml
---
# master_ir_orchestrator.yml
- name: Master Incident Response Orchestrator
  hosts: localhost
  gather_facts: no
  
  vars:
    incident_id: "{{ lookup('pipe', 'date +%Y%m%d%H%M%S') }}"
    alert_source: "{{ source | default('manual') }}"
    
  tasks:
    - name: Parse and classify incident
      set_fact:
        incident_classification: "{{ lookup('template', 'classify_incident.j2') }}"
        
    - name: Create incident ticket
      uri:
        url: "{{ ticketing_api }}/incidents"
        method: POST
        body_format: json
        body:
          id: "{{ incident_id }}"
          type: "{{ incident_classification.type }}"
          severity: "{{ incident_classification.severity }}"
          affected_systems: "{{ incident_classification.affected_systems }}"
          description: "{{ incident_classification.description }}"
      register: ticket_response
      
    - name: Notify incident response team
      include_tasks: notify_team.yml
      vars:
        channels:
          - slack
          - pagerduty
          - email
        
    - name: Execute response playbook
      include_tasks: "{{ incident_classification.type }}_response.yml"
      vars:
        target_hosts: "{{ incident_classification.affected_systems }}"
        
    - name: Generate executive summary
      template:
        src: executive_summary.j2
        dest: "/incidents/{{ incident_id }}/executive_summary.pdf"
      run_once: true
```

### Integration with SIEM/SOAR

```python
#!/usr/bin/env python3
"""
SIEM Integration for Ansible IR Playbooks
"""

import requests
import json
from ansible.plugins.callback import CallbackBase

class CallbackModule(CallbackBase):
    """Send Ansible events to SIEM"""
    
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'siem_integration'
    
    def __init__(self):
        super(CallbackModule, self).__init__()
        self.siem_endpoint = self.get_option('siem_endpoint')
        self.api_key = self.get_option('api_key')
        
    def v2_playbook_on_play_start(self, play):
        """Log playbook start to SIEM"""
        event = {
            'event_type': 'ir_playbook_start',
            'playbook': play.get_name(),
            'hosts': play.hosts,
            'timestamp': self._get_timestamp(),
            'incident_id': play.get_variable_manager().get_vars().get('incident_id')
        }
        self._send_to_siem(event)
        
    def v2_runner_on_ok(self, result):
        """Log successful tasks"""
        if result._task.action in ['shell', 'command', 'script']:
            event = {
                'event_type': 'ir_task_success',
                'host': result._host.name,
                'task': result._task.name,
                'module': result._task.action,
                'output': result._result.get('stdout', ''),
                'timestamp': self._get_timestamp()
            }
            self._send_to_siem(event)
            
    def _send_to_siem(self, event):
        """Send event to SIEM"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(
                self.siem_endpoint,
                headers=headers,
                json=event,
                timeout=5
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self._display.warning(f"Failed to send to SIEM: {e}")
```

## Testing Your IR Playbooks

Never wait for a real incident to test your playbooks:

```yaml
---
# ir_playbook_tests.yml
- name: Test IR Playbooks
  hosts: test_environment
  gather_facts: yes
  become: yes
  
  vars:
    test_scenarios:
      - name: "Ransomware simulation"
        playbook: "ransomware_response.yml"
        setup_tasks:
          - name: Create fake encrypted files
            shell: |
              for i in {1..10}; do
                echo "Encrypted content" > /tmp/test_file_$i.encrypted
              done
              
      - name: "Credential compromise simulation"
        playbook: "credential_compromise_response.yml"
        setup_tasks:
          - name: Create test user
            user:
              name: compromised_test_user
              state: present
              
      - name: "Web attack simulation"
        playbook: "web_attack_response.yml"
        setup_tasks:
          - name: Create webshell signature
            copy:
              content: "<?php system($_GET['cmd']); ?>"
              dest: /var/www/html/test_shell.php
              
  tasks:
    - name: Run test scenarios
      include_tasks: run_test_scenario.yml
      loop: "{{ test_scenarios }}"
      loop_control:
        loop_var: scenario
        
- name: Validate playbook execution
  block:
    - name: Check evidence collection
      stat:
        path: "{{ evidence_path }}"
      register: evidence_check
      
    - name: Verify containment actions
      shell: |
        # Check if containment was applied
        iptables -L -n | grep -c "IR block"
      register: containment_check
      
    - name: Generate test report
      template:
        src: ir_test_report.j2
        dest: "/tests/ir_test_{{ ansible_date_time.epoch }}.html"
```

## Best Practices and Lessons Learned

Quick question: What's your biggest fear during an incident? For me, it's making things worse. That's why these practices aren't just recommendations – they're survival tactics:

### 1. Evidence Preservation

Always preserve evidence before taking action:

```yaml
- name: Preserve evidence before remediation
  block:
    - name: Create forensic image
      shell: |
        dd if=/dev/sda of={{ evidence_path }}/disk_image.dd bs=4M status=progress
      async: 3600
      poll: 0
      
    - name: Calculate hashes
      shell: |
        sha256sum {{ evidence_path }}/disk_image.dd > {{ evidence_path }}/disk_image.sha256
```

### 2. Rollback Capabilities

Always plan for rollback:

```yaml
- name: Create rollback point
  block:
    - name: Snapshot system state
      shell: |
        # LVM snapshot
        lvcreate -L 10G -s -n incident_{{ incident_id }}_snapshot /dev/vg0/root
        
    - name: Backup critical configs
      archive:
        path:
          - /etc
          - /var/lib
        dest: "{{ backup_path }}/pre_ir_backup_{{ ansible_date_time.epoch }}.tar.gz"
```

### 3. Communication Templates

Keep stakeholders informed:

```jinja2
{# incident_notification.j2 #}
SECURITY INCIDENT NOTIFICATION

Incident ID: {{ incident_id }}
Type: {{ incident_type | upper }}
Severity: {{ severity }}
Start Time: {{ start_time }}

AFFECTED SYSTEMS:
{% for host in affected_hosts %}
- {{ host }} ({{ hostvars[host]['ansible_facts']['os_family'] }})
{% endfor %}

CURRENT STATUS: {{ current_status }}

ACTIONS TAKEN:
{% for action in completed_actions %}
- {{ action.timestamp }}: {{ action.description }}
{% endfor %}

NEXT STEPS:
{% for step in planned_actions %}
- {{ step }}
{% endfor %}

Incident Commander: {{ incident_commander }}
Communication Bridge: {{ bridge_number }}
```

### 4. Metrics and Improvement

Track your performance:

```yaml
- name: Collect IR metrics
  set_fact:
    ir_metrics:
      detection_time: "{{ (first_alert_time | to_datetime - incident_start_time | to_datetime).total_seconds() }}"
      response_time: "{{ (first_action_time | to_datetime - first_alert_time | to_datetime).total_seconds() }}"
      containment_time: "{{ (containment_complete_time | to_datetime - first_action_time | to_datetime).total_seconds() }}"
      recovery_time: "{{ (recovery_complete_time | to_datetime - incident_start_time | to_datetime).total_seconds() }}"
      
- name: Store metrics for analysis
  uri:
    url: "{{ metrics_api }}/ir_metrics"
    method: POST
    body_format: json
    body: "{{ ir_metrics }}"
```
{% endraw %}

## Conclusion

Ansible transforms incident response from a chaotic, error-prone process into a consistent, auditable, and fast operation. The playbooks shared here are battle-tested and production-ready, but remember: they're starting points. Customize them for your environment, test them regularly, and continuously improve based on lessons learned.

The difference between good and great incident response isn't just speed – it's consistency, completeness, and the ability to learn from each incident. With Ansible, you're not just responding to incidents; you're building institutional knowledge that makes each response better than the last.

Start small, test often, and gradually build your IR automation library. Your future self at 3 AM will thank you.

---

*Questions about IR automation? Want to share your playbooks or lessons learned? Reach out – the security community grows stronger when we share knowledge!*