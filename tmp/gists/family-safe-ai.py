from typing import Callable, Any

class FamilySafeAI:
    """Content filtering wrapper for AI models to ensure kid-safe outputs."""

    def __init__(self):
        self.load_safety_filters()

    def load_safety_filters(self):
        """Load content safety filters."""
        self.unsafe_categories = [
            'violence', 'hate', 'sexual', 'harassment',
            'self-harm', 'dangerous_content'
        ]
        # In production, integrate with content moderation APIs
        # like OpenAI Moderation API or Azure Content Safety

    def is_appropriate_for_kids(self, text: str) -> tuple[bool, str]:
        """Check if AI output is appropriate for children."""
        # Simplified check - in production use proper content moderation API
        inappropriate_keywords = [
            'violence', 'weapon', 'hate', 'explicit'
        ]

        text_lower = text.lower()
        for keyword in inappropriate_keywords:
            if keyword in text_lower:
                return False, f"Content flagged: {keyword}"

        return True, "Content approved"

    def safe_generate(self, model_generate: Callable, prompt: str, **kwargs) -> Any:
        """Wrap model generation with safety checks."""
        # Pre-check prompt
        is_safe, reason = self.is_appropriate_for_kids(prompt)
        if not is_safe:
            return f"This prompt cannot be processed: {reason}"

        # Generate response
        response = model_generate(prompt, **kwargs)

        # Post-check response
        is_safe, reason = self.is_appropriate_for_kids(response)
        if not is_safe:
            return "I cannot provide that response as it may not be appropriate."

        return response
