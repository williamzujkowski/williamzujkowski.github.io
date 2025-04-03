from typing import Dict, List
from textual.containers import Container, Vertical
from textual.widgets import Static
import logging

logger = logging.getLogger("williamzujkowski.github.io.navigation")


class NavigationSidebar(Container):
    """Navigation sidebar for the website."""

    def __init__(self, config: Dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.id = "navigation-sidebar"

    def compose(self):
        """Compose the navigation sidebar."""
        # Get site title from configuration
        site_title = self.config["site"].get("title", "William Zujkowski")
        yield Static(f"[b]{site_title}[/b]", classes="nav-title")

        # Create navigation items from configuration
        with Vertical(id="nav-items"):
            nav_items = self.config.get("navigation", {}).get("items", [])
            if not nav_items:
                nav_items = [
                    {"name": "Home", "path": "home", "icon": "🏠"},
                    {"name": "Links", "path": "links", "icon": "🔗"},
                    {"name": "Blog", "path": "blog", "icon": "📝"},
                ]

            for item in nav_items:
                name = item.get("name", "")
                path = item.get("path", "")
                icon = item.get("icon", "")

                if not name or not path:
                    continue

                nav_item = Static(
                    f"{icon} {name}",
                    classes="nav-item",
                    id=f"nav-{path}",
                )
                nav_item.data = path  # Store the path for use in callbacks

                # Add click handler to switch pages
                def make_handler(path):
                    def handler():
                        self.app.action_show_page(path)
                    return handler

                nav_item.on_click = make_handler(path)
                yield nav_item
