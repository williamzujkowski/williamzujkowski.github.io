from typing import Dict

from pages.markdown_page import MarkdownPage


class HomePage(MarkdownPage):
    """Home page of the website."""

    def __init__(self, config: Dict, *args, **kwargs):
        # Use MarkdownPage to render content from markdown file
        super().__init__(
            config=config, 
            page_id="home",
            title="Home", 
            markdown_path="content/pages/home/index.md",
            *args, **kwargs
        )
