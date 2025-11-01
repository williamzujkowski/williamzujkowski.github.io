"""
Threat Alerting Module

Source: https://williamzujkowski.github.io/posts/threat-intelligence-mitre-attack-dashboard/
Purpose: Automated alerting for high-priority threats with email notifications
Prerequisites: smtplib
Usage:
    config = {'smtp_server': 'smtp.gmail.com', 'smtp_port': 587,
              'sender_email': 'alerts@example.com', 'recipients': ['admin@example.com'],
              'priority_techniques': ['T1566', 'T1210', 'T1190']}
    alerting = ThreatAlerting(config)
    alerts = alerting.check_alerts(new_threats)

License: MIT
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class ThreatAlerting:
    def __init__(self, config):
        self.smtp_server = config['smtp_server']
        self.smtp_port = config['smtp_port']
        self.sender = config['sender_email']
        self.recipients = config['recipients']
        self.priority_techniques = config['priority_techniques']

    def check_alerts(self, new_threats):
        """Check for high-priority threats"""
        alerts = []

        for threat in new_threats:
            # Check against priority techniques
            if any(tech in self.priority_techniques
                   for tech in threat.get('techniques', [])):
                alerts.append(self.create_alert(threat))

            # Check for ransomware indicators
            if threat.get('ransomware_use'):
                alerts.append(self.create_critical_alert(threat))

        return alerts

    def create_alert(self, threat):
        """Create standard alert"""
        return {
            'level': 'WARNING',
            'timestamp': datetime.now(),
            'threat': threat,
            'message': f"Detected activity matching technique {threat['techniques']}"
        }

    def create_critical_alert(self, threat):
        """Create critical alert"""
        return {
            'level': 'CRITICAL',
            'timestamp': datetime.now(),
            'threat': threat,
            'message': f"CRITICAL: Ransomware-related activity detected: {threat.get('cve')}"
        }

    def send_alert_email(self, alert):
        """Send email notification for critical alerts"""
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"[{alert['level']}] Threat Intelligence Alert"
        msg['From'] = self.sender
        msg['To'] = ', '.join(self.recipients)

        html_body = self.format_alert_html(alert)
        msg.attach(MIMEText(html_body, 'html'))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.send_message(msg)

    def format_alert_html(self, alert):
        """Format alert as HTML email"""
        return f"""
        <html>
        <body>
            <h2 style="color: {'red' if alert['level'] == 'CRITICAL' else 'orange'};">
                {alert['level']} Alert
            </h2>
            <p><strong>Timestamp:</strong> {alert['timestamp']}</p>
            <p><strong>Message:</strong> {alert['message']}</p>
            <p><strong>Threat Details:</strong> {alert['threat']}</p>
        </body>
        </html>
        """
