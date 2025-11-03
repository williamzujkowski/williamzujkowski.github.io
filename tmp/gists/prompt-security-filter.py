import re
from typing import List

class PromptSecurityFilter:
    """Detect and block prompt injection attempts."""

    def __init__(self):
        self.blocked_patterns = [
            r"ignore previous instructions",
            r"disregard all prior",
            r"forget everything",
            r"new instructions:",
            r"system prompt",
            r"act as if",
            r"pretend you are",
        ]
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.blocked_patterns]

    def check_injection(self, prompt: str) -> tuple[bool, List[str]]:
        """Check for prompt injection patterns."""
        detected = []
        for pattern in self.compiled_patterns:
            if pattern.search(prompt):
                detected.append(pattern.pattern)

        return len(detected) > 0, detected

    def sanitize(self, prompt: str) -> str:
        """Remove suspicious content from prompts."""
        sanitized = prompt
        for pattern in self.compiled_patterns:
            sanitized = pattern.sub('[FILTERED]', sanitized)

        return sanitized
