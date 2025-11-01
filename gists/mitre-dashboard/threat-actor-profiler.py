"""
Threat Actor Profiling Module

Source: https://williamzujkowski.github.io/posts/threat-intelligence-mitre-attack-dashboard/
Purpose: Matches observed techniques to known threat actor TTPs for attribution
Prerequisites: None (uses MITRE groups data)
Usage:
    profiler = ThreatActorProfiler()
    matches = profiler.match_activity_to_actor(['T1566', 'T1027', 'T1055'])

License: MIT
"""

class ThreatActorProfiler:
    def __init__(self):
        self.actor_database = {}
        self.load_actor_profiles()

    def load_actor_profiles(self):
        """Load known threat actor profiles from MITRE"""
        # In production, this would fetch from MITRE's groups STIX data
        self.actor_database = {
            'APT29': {
                'aliases': ['Cozy Bear', 'The Dukes'],
                'techniques': ['T1566', 'T1027', 'T1055', 'T1083'],
                'targets': ['Government', 'Healthcare'],
                'origin': 'Russia'
            },
            'APT28': {
                'aliases': ['Fancy Bear', 'Sofacy'],
                'techniques': ['T1566', 'T1193', 'T1071', 'T1056'],
                'targets': ['Government', 'Defense'],
                'origin': 'Russia'
            },
            'Lazarus Group': {
                'aliases': ['Hidden Cobra'],
                'techniques': ['T1566', 'T1059', 'T1105', 'T1071'],
                'targets': ['Finance', 'Media'],
                'origin': 'North Korea'
            }
        }

    def match_activity_to_actor(self, observed_techniques):
        """Match observed techniques to known actors"""
        matches = []

        for actor, profile in self.actor_database.items():
            overlap = set(observed_techniques) & set(profile['techniques'])

            if len(overlap) >= 2:  # Minimum 2 technique matches
                confidence = len(overlap) / len(profile['techniques'])
                matches.append({
                    'actor': actor,
                    'confidence': confidence,
                    'matched_techniques': list(overlap),
                    'aliases': profile['aliases'],
                    'origin': profile['origin']
                })

        return sorted(matches, key=lambda x: x['confidence'], reverse=True)
