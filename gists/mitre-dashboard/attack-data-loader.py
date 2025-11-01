"""
MITRE ATT&CK Data Loader with STIX Processing

Source: https://williamzujkowski.github.io/posts/threat-intelligence-mitre-attack-dashboard/
Purpose: Fetches and processes MITRE ATT&CK Enterprise matrix data from GitHub
Prerequisites: requests, stix2
Usage:
    loader = ATTACKDataLoader()
    technique_map = loader.load_attack_data()

License: MIT
"""

import requests
from stix2 import MemoryStore, Filter

class ATTACKDataLoader:
    def __init__(self):
        self.attack_url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
        self.memory_store = None

    def load_attack_data(self):
        """Load MITRE ATT&CK Enterprise matrix"""
        response = requests.get(self.attack_url)
        attack_data = response.json()

        # Create STIX memory store
        self.memory_store = MemoryStore(stix_data=attack_data["objects"])

        # Extract techniques
        techniques = self.memory_store.query([
            Filter("type", "=", "attack-pattern")
        ])

        return self.process_techniques(techniques)

    def process_techniques(self, techniques):
        """Process and categorize techniques by tactic"""
        technique_map = {}

        for technique in techniques:
            if hasattr(technique, 'kill_chain_phases'):
                for phase in technique.kill_chain_phases:
                    tactic = phase.phase_name.replace('-', ' ').title()

                    if tactic not in technique_map:
                        technique_map[tactic] = []

                    technique_map[tactic].append({
                        'id': technique.external_references[0].external_id,
                        'name': technique.name,
                        'description': technique.description
                    })

        return technique_map
