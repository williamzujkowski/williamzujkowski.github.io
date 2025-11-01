"""
Threat Data Visualization Module

Source: https://williamzujkowski.github.io/posts/threat-intelligence-mitre-attack-dashboard/
Purpose: Creates interactive heatmaps and timelines of MITRE ATT&CK technique frequency
Prerequisites: plotly
Usage:
    visualizer = ThreatVisualizer(threat_data)
    heatmap_fig = visualizer.create_attack_heatmap()
    timeline_fig = visualizer.create_threat_timeline(alerts)

License: MIT
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots

class ThreatVisualizer:
    def __init__(self, threat_data):
        self.threat_data = threat_data

    def create_attack_heatmap(self):
        """Create heatmap of technique frequency"""
        tactics = []
        techniques = []
        frequencies = []

        for tactic, tech_list in self.threat_data.items():
            for technique in tech_list:
                tactics.append(tactic)
                techniques.append(technique['name'])
                frequencies.append(technique.get('frequency', 0))

        fig = go.Figure(data=go.Heatmap(
            x=tactics,
            y=techniques,
            z=frequencies,
            colorscale='Reds',
            showscale=True
        ))

        fig.update_layout(
            title='MITRE ATT&CK Technique Frequency',
            xaxis_title='Tactics',
            yaxis_title='Techniques',
            height=800
        )

        return fig

    def create_threat_timeline(self, alerts):
        """Create timeline of threat activity"""
        fig = go.Figure()

        for alert in alerts:
            fig.add_trace(go.Scatter(
                x=[alert['timestamp']],
                y=[alert['severity']],
                mode='markers+text',
                name=alert['source'],
                text=alert['description'],
                marker=dict(
                    size=alert['severity'] * 5,
                    color=self.get_color_by_severity(alert['severity'])
                )
            ))

        fig.update_layout(
            title='Threat Activity Timeline',
            xaxis_title='Time',
            yaxis_title='Severity',
            showlegend=True
        )

        return fig

    def get_color_by_severity(self, severity):
        """Map severity to color"""
        colors = {
            1: 'blue',
            2: 'yellow',
            3: 'orange',
            4: 'red'
        }
        return colors.get(severity, 'gray')
