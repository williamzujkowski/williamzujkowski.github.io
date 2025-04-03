from typing import Dict, Optional
from textual.containers import Container, ScrollableContainer
from textual.widgets import Static


class BasePage(Container):
    """Base class for all pages in the application."""

    def __init__(self, config: Dict, title: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.title = title or self.__class__.__name__.replace("Page", "")

    def compose_title(self) -> Static:
        """Create the page title widget."""
        return Static(f"[b]{self.title}[/b]", classes="page-title")

    def compose_content(self):
        """Create the page content container.
        
        This should be overridden by subclasses.
        """
        with Container(classes="page-content") as container:
            pass
        return container
    
    def compose(self):
        """Compose the page layout."""
        with ScrollableContainer(classes="page-container"):
            yield self.compose_title()
            content = self.compose_content()
            if hasattr(content, "__iter__") and not isinstance(content, (str, bytes)):
                for widget in content:
                    if widget is not None:
                        yield widget
            elif content is not None:
                yield content
