from pathlib import Path
from typing import Dict, Optional
from textual.containers import Container
from textual.widgets import MarkdownViewer, Static

from pages.base import BasePage


class MarkdownPage(BasePage):
    """Base class for pages that render Markdown content."""

    def __init__(
        self, 
        config: Dict, 
        page_id: str,
        title: Optional[str] = None, 
        markdown_path: Optional[str] = None,
        *args, 
        **kwargs
    ):
        """Initialize the markdown page.
        
        Args:
            config: Site configuration dictionary
            page_id: Identifier for this page (e.g., 'home', 'links')
            title: Page title (optional, will be derived from page_id if not provided)
            markdown_path: Path to the markdown file (optional)
            *args, **kwargs: Additional arguments passed to parent class
        """
        self.page_id = page_id
        title = title or page_id.title()
        super().__init__(config, title, *args, **kwargs)
        
        # Determine markdown path if not provided
        if markdown_path is None:
            # Default path is content/pages/{page_id}/index.md
            markdown_path = f"content/pages/{page_id}/index.md"
        
        self.markdown_path = Path(markdown_path)
        self.content_text = self._load_markdown()

    def _load_markdown(self) -> str:
        """Load markdown content from file."""
        try:
            if not self.markdown_path.exists():
                return f"# Page Not Found\n\nThe content for {self.title} could not be found at {self.markdown_path}."
            
            with open(self.markdown_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Handle frontmatter if present
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    # There is frontmatter - extract content
                    frontmatter = parts[1].strip()
                    content = parts[2].strip()
                    
                    # Extract title if present
                    for line in frontmatter.split("\n"):
                        if ":" in line:
                            key, value = line.split(":", 1)
                            key = key.strip().lower()
                            value = value.strip().strip('"').strip("'")
                            
                            if key == "title":
                                self.title = value
            
            return content
        except Exception as e:
            return f"# Error\n\nFailed to load markdown content: {e}"

    def compose_content(self):
        """Create the page content using MarkdownViewer."""
        with Container(classes="page-content") as container:
            # Use MarkdownViewer to render the markdown content
            yield MarkdownViewer(self.content_text, classes="markdown-body")
        
        return container