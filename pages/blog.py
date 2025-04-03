import os
from datetime import datetime
import logging
from pathlib import Path
from typing import Dict, List, Optional
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, MarkdownViewer, Button

from pages.base import BasePage

logger = logging.getLogger("williamzujkowski.github.io.blog")


class BlogPost:
    """Represents a single blog post."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.title = ""
        self.date = None
        self.content = ""
        self._parse_file()
    
    def _parse_file(self):
        """Parse the markdown file to extract metadata and content."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            # Extract title from filename or first heading
            self.title = self.file_path.stem.replace("-", " ").title()
            
            # Try to extract date from filename
            try:
                date_part = self.file_path.stem.split("-")[:3]
                if len(date_part) == 3 and all(part.isdigit() for part in date_part):
                    year, month, day = map(int, date_part)
                    self.date = datetime(year, month, day)
            except (ValueError, IndexError):
                # If we can't parse the date from filename, use file modification time
                self.date = datetime.fromtimestamp(self.file_path.stat().st_mtime)
            
            # Extract content
            self.content = "".join(lines)
            
            # Check for YAML frontmatter
            if self.content.startswith("---"):
                parts = self.content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter = parts[1].strip()
                    self.content = parts[2].strip()
                    
                    # Extract title and date from frontmatter
                    for line in frontmatter.split("\n"):
                        if ":" in line:
                            key, value = line.split(":", 1)
                            key = key.strip().lower()
                            value = value.strip().strip('"').strip("'")
                            
                            if key == "title":
                                self.title = value
                            elif key == "date":
                                try:
                                    self.date = datetime.fromisoformat(value)
                                except ValueError:
                                    pass
        
        except Exception as e:
            logger.error(f"Error parsing blog post {self.file_path}: {e}")
            self.title = self.file_path.name
            self.date = datetime.fromtimestamp(self.file_path.stat().st_mtime)
            self.content = f"Error loading post: {e}"


class BlogPage(BasePage):
    """Blog page showing a list of blog posts and their content."""

    def __init__(self, config: Dict, *args, **kwargs):
        super().__init__(config, "Blog", *args, **kwargs)
        self.posts = []
        
        # Load posts immediately
        self._load_posts()

    def _load_posts(self):
        """Load blog posts from the configured directory."""
        # Get the blog post directory from configuration
        blog_config = self.config.get("blog", {})
        post_dir = blog_config.get("post_dir", "content/posts")
        post_path = Path(post_dir)
        
        # Create the directory if it doesn't exist
        post_path.mkdir(parents=True, exist_ok=True)
        
        # Load all markdown files
        self.posts = []
        try:
            for file_path in sorted(
                post_path.glob("*.md"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            ):
                post = BlogPost(file_path)
                self.posts.append(post)
        
            logger.info(f"Loaded {len(self.posts)} blog posts from {post_dir}")
            
            # Create a placeholder post if no posts exist
            if not self.posts:
                placeholder_path = post_path / "welcome.md"
                if not placeholder_path.exists():
                    with open(placeholder_path, "w", encoding="utf-8") as f:
                        f.write("""---
title: Welcome to My Blog
date: 2023-01-01
---

# Welcome to My Blog

This is a placeholder blog post. You can add more posts by adding markdown files to the `content/posts` directory.

## Markdown Support

This blog supports standard markdown formatting:

- **Bold text** and *italic text*
- Lists and numbered lists
- [Links](https://example.com)
- Code blocks and inline `code`
- And more...

Happy blogging!
""")
                    self.posts.append(BlogPost(placeholder_path))
                    logger.info(f"Created placeholder blog post at {placeholder_path}")
        
        except Exception as e:
            logger.error(f"Error loading blog posts: {e}")
            # Create a default post on error
            self.posts.append(BlogPost(Path("content/posts/error.md")))
    
    def compose_content(self):
        """Create the blog page content."""
        with Container(classes="page-content") as container:
            # Create a sidebar with blog post list
            with Container(classes="blog-sidebar"):
                yield Static("[b]Blog Posts[/b]", classes="blog-sidebar-title")
                
                # Create a list of blog posts
                with Container(classes="blog-post-list"):
                    for i, post in enumerate(self.posts):
                        post_item = Static(
                            f"{post.title}",
                            classes="blog-post-item"
                        )
                        # Store post index for click handling
                        post_item.data = i
                        
                        # Add click handler to show post
                        def make_handler(post_idx):
                            def handler():
                                self.show_post(post_idx)
                            return handler
                        
                        post_item.on_click = make_handler(i)
                        yield post_item
            
            # Display the content container (will be filled when a post is selected)
            self.content_container = Container(classes="blog-content-container")
            yield self.content_container
        
        return container
        
    def on_mount(self):
        """Called when the widget is mounted."""
        super().on_mount()
        # Show the first post initially if available
        if self.posts:
            self.show_post(0)
        else:
            # No posts found
            self.content_container.mount(
                Static(
                    "No blog posts found. Create some markdown files in the content/posts directory.",
                    classes="home-intro"
                )
            )
        
    def show_post(self, post_idx: int):
        """Show the selected blog post."""
        if not self.posts or post_idx >= len(self.posts):
            return
            
        post = self.posts[post_idx]
        
        # Clear current content
        self.content_container.remove_children()
        
        # Add post title
        title = Static(f"[b]{post.title}[/b]", classes="blog-post-title")
        self.content_container.mount(title)
        
        # Add post date if available
        if post.date:
            date_format = self.config.get("blog", {}).get("date_format", "%B %d, %Y")
            date = Static(
                f"Published on {post.date.strftime(date_format)}",
                classes="blog-post-date"
            )
            self.content_container.mount(date)
        
        # Add post content as Markdown
        md_viewer = MarkdownViewer(post.content, classes="markdown-body")
        self.content_container.mount(md_viewer)
        
        # Update highlight in sidebar
        for child in self.query(".blog-post-item"):
            if isinstance(child, Static) and child.data == post_idx:
                child.add_class("active")
            else:
                child.remove_class("active")