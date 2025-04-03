from typing import Dict

from pages.markdown_page import MarkdownPage


class LinksPage(MarkdownPage):
    """Links page showing various resources and social links."""

    def __init__(self, config: Dict, *args, **kwargs):
        # Use MarkdownPage to render content from markdown file
        super().__init__(
            config=config, 
            page_id="links",
            title="Links", 
            markdown_path="content/pages/links/index.md",
            *args, **kwargs
        )
