from typing import Dict
from textual.containers import Container
from textual.widgets import Static

from pages.base import BasePage


class HomePage(BasePage):
    """Home page of the website."""

    def __init__(self, config: Dict, *args, **kwargs):
        super().__init__(config, "Home", *args, **kwargs)

    def compose_content(self):
        """Create the home page content."""
        site_title = self.config["site"].get("title", "William Zujkowski")
        site_desc = self.config["site"].get(
            "description", "Personal website and blog"
        )
        
        with Container(classes="page-content") as container:
            yield Static(
                f"[b]Welcome to {site_title}'s Website[/b]",
                classes="home-welcome"
            )
            
            yield Static(
                """This is a personal website built with Textual, a powerful Text User Interface (TUI) framework for Python.
                
                Navigate using the sidebar or keyboard shortcuts (shown in the footer).
                
                [b]Features:[/b]
                - Blog posts with Markdown support
                - Links to various resources and profiles
                - Clean, responsive terminal-friendly design
                
                This site can be viewed interactively in a terminal or as a static website on GitHub Pages.
                """,
                classes="home-intro"
            )
            
            # Developer information
            yield Static(
                """[b]About the Developer[/b]
                
                I am a software developer with a passion for Python, web technologies, and terminal-based user interfaces.
                
                My interests include:
                - Python development
                - Terminal user interfaces
                - Web technologies
                - Open source software
                
                Feel free to explore this site to learn more about my work and interests.
                """,
                classes="home-intro"
            )
        
        return container
