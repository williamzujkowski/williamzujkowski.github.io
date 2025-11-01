"""
AlienVault OTX Pulse Integration

Source: https://williamzujkowski.github.io/posts/threat-intelligence-mitre-attack-dashboard/
Purpose: Collects threat intelligence pulses from AlienVault OTX and extracts ATT&CK technique mappings
Prerequisites: OTXv2 Python library
Usage:
    collector = AlienVaultCollector(api_key='YOUR_API_KEY')
    pulses = collector.get_recent_pulses(days_back=7)

License: MIT
"""

import OTXv2
from datetime import datetime, timedelta

class AlienVaultCollector:
    def __init__(self, api_key):
        self.otx = OTXv2.OTXv2(api_key)
        self.pulse_cache = {}

    def get_recent_pulses(self, days_back=7):
        """Fetch recent threat pulses"""
        pulses = self.otx.getall_iter(
            modified_since=(datetime.now() - timedelta(days=days_back))
        )

        attack_mappings = []
        for pulse in pulses:
            # Extract ATT&CK tags
            attack_tags = [tag for tag in pulse.get('tags', [])
                          if tag.startswith('T')]

            if attack_tags:
                attack_mappings.append({
                    'pulse_id': pulse['id'],
                    'name': pulse['name'],
                    'techniques': attack_tags,
                    'indicators': pulse.get('indicators', []),
                    'adversary': pulse.get('adversary', 'Unknown')
                })

        return attack_mappings
