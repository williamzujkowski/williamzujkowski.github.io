from pathlib import Path
from typing import Dict, Optional
from textual.containers import Container
from textual.widgets import MarkdownViewer

from pages.markdown_page import MarkdownPage


class PlaceholderPage(MarkdownPage):
    """Placeholder page for future content."""

    def __init__(self, title: str, config: Dict, *args, **kwargs):
        # Handle the case where title is dynamic
        page_id = title.lower().replace(" ", "_")
        
        # Check if there's a markdown file for this page
        markdown_path = f"content/pages/{page_id}/index.md"
        
        # If the contact page is requested, use that content
        if page_id == "contact":
            markdown_path = "content/pages/contact/index.md"
        
        # If a specific file doesn't exist, create a default placeholder content
        if not Path(markdown_path).exists():
            default_content = f"""---
title: {title}
---

# {title}

This page is currently under construction.

Please check back later for updates!

To add content to this page, create a markdown file at `{markdown_path}`.
"""
            # Use base implementation with provided content
            super().__init__(
                config=config,
                page_id=page_id,
                title=title,
                *args, **kwargs
            )
            self.content_text = default_content
        else:
            # Use the existing markdown file
            super().__init__(
                config=config,
                page_id=page_id,
                title=title,
                markdown_path=markdown_path,
                *args, **kwargs
            )
