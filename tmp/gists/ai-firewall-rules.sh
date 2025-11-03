#!/bin/bash
# Dream Machine Professional firewall rules for AI VLAN
# Network segmentation for AI workloads

# AI VLAN Configuration
AI_VLAN="10.0.50.0/24"
INTERNAL_REPO="10.0.10.5"

# Allow: AI VLAN -> Internal model repository
iptables -A FORWARD -s $AI_VLAN -d $INTERNAL_REPO -j ACCEPT

# Allow: AI VLAN -> Specific whitelisted APIs (OpenAI, Hugging Face)
iptables -A FORWARD -s $AI_VLAN -d api.openai.com -j ACCEPT
iptables -A FORWARD -s $AI_VLAN -d huggingface.co -j ACCEPT

# Block: AI VLAN -> Home network
iptables -A FORWARD -s $AI_VLAN -d 10.0.1.0/24 -j DROP

# Block: AI VLAN -> Management network
iptables -A FORWARD -s $AI_VLAN -d 10.0.0.0/24 -j DROP

# Log: All AI VLAN traffic for monitoring
iptables -A FORWARD -s $AI_VLAN -j LOG --log-prefix "AI-VLAN: "
