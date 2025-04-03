from typing import Dict
from textual.containers import Container
from textual.widgets import Static

from pages.base import BasePage


class PlaceholderPage(BasePage):
    """Placeholder page for future content."""

    def __init__(self, title: str, config: Dict, *args, **kwargs):
        super().__init__(config, title, *args, **kwargs)

    def compose_content(self):
        """Create the placeholder page content."""
        with Container(classes="page-content") as container:
            yield Static(
                f"""[b]This page ({self.title}) is under construction[/b]
                
                This is a placeholder for future content. Check back later for updates!
                
                To add content to this page, edit the corresponding module in the 'pages' directory.
                """,
                classes="placeholder-container"
            )
        
        return container
