from typing import Dict, List
from textual.containers import Container
from textual.widgets import Static

from pages.base import BasePage


class LinksPage(BasePage):
    """Links page showing various resources and social links."""

    def __init__(self, config: Dict, *args, **kwargs):
        super().__init__(config, "Links", *args, **kwargs)

    def compose_content(self):
        """Create the links page content."""
        with Container(classes="page-content") as container:
            yield Static(
                """Below are links to various resources, social profiles, and projects.
                Links are organized by category for easier navigation.
                """,
                classes="home-intro"
            )
            
            # Get link configuration
            links_config = self.config.get("links", {})
            groups = links_config.get("groups", [])
            links = links_config.get("items", [])
            
            # Organize links by group
            grouped_links = {}
            for link in links:
                group = link.get("group", "Uncategorized")
                if group not in grouped_links:
                    grouped_links[group] = []
                grouped_links[group].append(link)
            
            # Display link groups
            for group in groups:
                group_name = group.get("name", "Uncategorized")
                group_icon = group.get("icon", "")
                
                if group_name not in grouped_links:
                    continue
                    
                with Container(classes="link-group") as group_container:
                    yield Static(
                        f"{group_icon} [b]{group_name}[/b]",
                        classes="link-group-title"
                    )
                    
                    # Add links for this group
                    for link in grouped_links[group_name]:
                        link_name = link.get("name", "")
                        link_url = link.get("url", "#")
                        link_icon = link.get("icon", "")
                        link_desc = link.get("description", "")
                        
                        yield Static(
                            f"{link_icon} [link={link_url}]{link_name}[/link]",
                            classes="link-item"
                        )
                        
                        if link_desc:
                            yield Static(
                                f"{link_desc}",
                                classes="link-description"
                            )
                
                yield group_container
        
        return container
