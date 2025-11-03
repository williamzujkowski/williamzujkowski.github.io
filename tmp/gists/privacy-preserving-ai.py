import re
from typing import Dict, Any

class PrivacyPreservingAI:
    """Detect and redact PII before processing."""

    def __init__(self):
        self.pii_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
        }
        self.compiled_patterns = {
            key: re.compile(pattern) for key, pattern in self.pii_patterns.items()
        }

    def detect_pii(self, text: str) -> Dict[str, int]:
        """Detect PII in text."""
        findings = {}
        for pii_type, pattern in self.compiled_patterns.items():
            matches = pattern.findall(text)
            if matches:
                findings[pii_type] = len(matches)
        return findings

    def redact_pii(self, text: str) -> str:
        """Remove PII from text."""
        redacted = text
        for pii_type, pattern in self.compiled_patterns.items():
            redacted = pattern.sub(f'[{pii_type.upper()}_REDACTED]', redacted)
        return redacted

    def process_safely(self, data: Any) -> Any:
        """Process data with PII protection."""
        if isinstance(data, str):
            findings = self.detect_pii(data)
            if findings:
                print(f"Warning: PII detected: {findings}")
                return self.redact_pii(data)

        processed_data = data
        return processed_data
