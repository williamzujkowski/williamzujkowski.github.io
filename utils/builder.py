import os
import sys
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import asyncio
from bs4 import BeautifulSoup
import markdown

logger = logging.getLogger("williamzujkowski.github.io.builder")


class StaticSiteBuilder:
    """Builds a static site for GitHub Pages deployment."""

    def __init__(self, config: Dict):
        self.config = config
        self.env_config = config.get("environments", {}).get("production", {})
        self.build_dir = Path(self.env_config.get("build_dir", "build"))
        self.assets_dir = Path(self.env_config.get("assets_dir", "assets"))
        self.minify = self.env_config.get("minify", False)
        self.compression = self.env_config.get("compression", False)

    def build(self):
        """Build the static site."""
        # Create build directory
        self.build_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Building static site in {self.build_dir}")

        # Copy assets
        self._copy_assets()

        # Generate pages
        self._generate_home_page()
        self._generate_links_page()
        self._generate_blog_page()
        self._generate_placeholder_pages()

        # Generate CSS
        self._generate_css()

        # Generate JavaScript helpers
        self._generate_javascript()

        # Create index.html as a copy of home.html
        shutil.copy(self.build_dir / "home.html", self.build_dir / "index.html")

        logger.info(f"Static site built successfully in {self.build_dir}")

    def _copy_assets(self):
        """Copy assets to the build directory."""
        if self.assets_dir.exists():
            assets_build_dir = self.build_dir / "assets"
            assets_build_dir.mkdir(exist_ok=True)

            # Copy all assets
            for item in self.assets_dir.glob("**/*"):
                if item.is_file():
                    rel_path = item.relative_to(self.assets_dir)
                    dest_path = assets_build_dir / rel_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest_path)
                    logger.debug(f"Copied asset: {item} -> {dest_path}")

    def _render_common_elements(self, soup, active_page):
        """Render common elements like header and navigation."""
        # Add meta tags
        head = soup.head
        meta_viewport = soup.new_tag("meta")
        meta_viewport["name"] = "viewport"
        meta_viewport["content"] = "width=device-width, initial-scale=1.0"
        head.append(meta_viewport)

        site_title = self.config["site"].get("title", "William Zujkowski")
        site_desc = self.config["site"].get(
            "description", "Personal website and blog"
        )

        # Add favicon with absolute path
        favicon = soup.new_tag("link")
        favicon["rel"] = "icon"
        favicon["href"] = "/assets/favicon.ico"
        favicon["type"] = "image/x-icon"
        head.append(favicon)

        # Add title
        title_tag = soup.new_tag("title")
        title_tag.string = f"{site_title} - {active_page.title()}"
        head.append(title_tag)

        # Add description
        meta_desc = soup.new_tag("meta")
        meta_desc["name"] = "description"
        meta_desc["content"] = site_desc
        head.append(meta_desc)

        # Create header
        header = soup.new_tag("header")
        header["class"] = "site-header"
        header_title = soup.new_tag("h1")
        header_title.string = site_title
        header.append(header_title)
        soup.body.append(header)

        # Create navigation
        nav = soup.new_tag("nav")
        nav["class"] = "site-nav"
        nav_list = soup.new_tag("ul")

        # Add navigation items
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

            li = soup.new_tag("li")
            a = soup.new_tag("a")
            
            # Use absolute paths from root
            if active_page.startswith("blog/"):
                # If we're in a blog post page, use absolute paths with preceding slash
                a["href"] = f"/{path}.html"
            else:
                a["href"] = f"/{path}.html"

            # Mark active page
            if path == active_page:
                a["class"] = "active"

            a.string = f"{icon} {name}" if icon else name
            li.append(a)
            nav_list.append(li)

        nav.append(nav_list)
        soup.body.append(nav)

        # Create main content container
        main = soup.new_tag("main")
        main["class"] = "site-content"
        soup.body.append(main)

        # Create footer
        footer = soup.new_tag("footer")
        footer["class"] = "site-footer"
        footer_text = soup.new_tag("p")
        current_year = datetime.now().year
        footer_text.string = f"© {current_year} {site_title} - Built with Python and Textual"
        footer.append(footer_text)
        soup.body.append(footer)

        return main  # Return main content container for page-specific content

    def _generate_base_template(self, page_name):
        """Generate a base HTML template for a page."""
        # Use absolute paths for CSS and JavaScript
        css_path = "/styles.css"
        js_path = "/script.js"
            
        html = f"""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <link rel="stylesheet" href="{css_path}">
            <script src="{js_path}" defer></script>
        </head>
        <body class="{page_name}-page">
        </body>
        </html>
        """

        soup = BeautifulSoup(html, "html.parser")
        main_content = self._render_common_elements(soup, page_name)
        return soup, main_content

    def _generate_home_page(self):
        """Generate the home page using markdown content."""
        soup, main_content = self._generate_base_template("home")
        
        # Use markdown content from the content directory
        md_path = Path("content/pages/home/index.md")
        
        # Process markdown content
        try:
            with open(md_path, "r", encoding="utf-8") as f:
                md_content = f.read()
                
            # Handle frontmatter if present
            title = "Home"
            if md_content.startswith("---"):
                parts = md_content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter = parts[1].strip()
                    content = parts[2].strip()
                    
                    # Extract title from frontmatter if present
                    for line in frontmatter.split("\n"):
                        if ":" in line:
                            key, value = line.split(":", 1)
                            key = key.strip().lower()
                            value = value.strip().strip('"').strip("'")
                            
                            if key == "title":
                                title = value
            else:
                content = md_content
            
            # Add page title
            title_el = soup.new_tag("h2")
            title_el["class"] = "page-title"
            title_el.string = title
            main_content.append(title_el)
            
            # Add markdown content
            content_div = soup.new_tag("div")
            content_div["class"] = "markdown-body"
            
            # Convert markdown to HTML
            html_content = markdown.markdown(
                content,
                extensions=["extra", "codehilite", "nl2br"],
            )
            content_div.append(BeautifulSoup(html_content, "html.parser"))
            main_content.append(content_div)
            
        except Exception as e:
            logger.error(f"Error processing markdown for home page: {e}")
            # Fallback to static content
            error_msg = soup.new_tag("div")
            error_msg["class"] = "error-message"
            error_msg.string = f"Error loading home page content: {e}"
            main_content.append(error_msg)

        # Write the file
        with open(self.build_dir / "home.html", "w", encoding="utf-8") as f:
            f.write(str(soup.prettify()))

        logger.info("Generated home page")

    def _generate_links_page(self):
        """Generate the links page using markdown content."""
        soup, main_content = self._generate_base_template("links")
        
        # Use markdown content from the content directory
        md_path = Path("content/pages/links/index.md")
        
        # Process markdown content
        try:
            with open(md_path, "r", encoding="utf-8") as f:
                md_content = f.read()
                
            # Handle frontmatter if present
            title = "Links"
            if md_content.startswith("---"):
                parts = md_content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter = parts[1].strip()
                    content = parts[2].strip()
                    
                    # Extract title from frontmatter if present
                    for line in frontmatter.split("\n"):
                        if ":" in line:
                            key, value = line.split(":", 1)
                            key = key.strip().lower()
                            value = value.strip().strip('"').strip("'")
                            
                            if key == "title":
                                title = value
            else:
                content = md_content
            
            # Add page title
            title_el = soup.new_tag("h2")
            title_el["class"] = "page-title"
            title_el.string = title
            main_content.append(title_el)
            
            # Add markdown content
            content_div = soup.new_tag("div")
            content_div["class"] = "markdown-body"
            
            # Convert markdown to HTML
            html_content = markdown.markdown(
                content,
                extensions=["extra", "codehilite", "nl2br"],
            )
            
            # Enhance the links by adding target="_blank" and rel="noopener noreferrer"
            parsed_html = BeautifulSoup(html_content, "html.parser")
            for a in parsed_html.select('a'):
                a['target'] = '_blank'
                a['rel'] = 'noopener noreferrer'
            
            content_div.append(parsed_html)
            main_content.append(content_div)
            
        except Exception as e:
            logger.error(f"Error processing markdown for links page: {e}")
            # Fallback to link configuration
            error_msg = soup.new_tag("div")
            error_msg["class"] = "error-message"
            error_msg.string = f"Error loading links page content: {e}"
            main_content.append(error_msg)
            
            # Get link configuration and build the page from config as fallback
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
                    
                group_container = soup.new_tag("div")
                group_container["class"] = "link-group"
                
                group_title = soup.new_tag("h3")
                group_title["class"] = "link-group-title"
                group_title.string = f"{group_icon} {group_name}" if group_icon else group_name
                group_container.append(group_title)
                
                # Add links for this group
                link_list = soup.new_tag("ul")
                link_list["class"] = "link-list"
                
                for link in grouped_links[group_name]:
                    link_name = link.get("name", "")
                    link_url = link.get("url", "#")
                    link_icon = link.get("icon", "")
                    link_desc = link.get("description", "")
                    
                    li = soup.new_tag("li")
                    li["class"] = "link-item"
                    
                    a = soup.new_tag("a")
                    a["href"] = link_url
                    a["target"] = "_blank"
                    a["rel"] = "noopener noreferrer"
                    a.string = f"{link_icon} {link_name}" if link_icon else link_name
                    li.append(a)
                    
                    if link_desc:
                        desc = soup.new_tag("p")
                        desc["class"] = "link-description"
                        desc.string = link_desc
                        li.append(desc)
                        
                    link_list.append(li)
                    
                group_container.append(link_list)
                main_content.append(group_container)

        # Write the file
        with open(self.build_dir / "links.html", "w", encoding="utf-8") as f:
            f.write(str(soup.prettify()))

        logger.info("Generated links page")

    def _generate_blog_page(self):
        """Generate the blog page and individual blog post pages."""
        # Get blog configuration
        blog_config = self.config.get("blog", {})
        post_dir = blog_config.get("post_dir", "content/posts")
        post_path = Path(post_dir)
        date_format = blog_config.get("date_format", "%B %d, %Y")
        show_dates = blog_config.get("show_dates", True)

        # Ensure the posts directory exists
        post_path.mkdir(parents=True, exist_ok=True)

        # Create blog index page
        soup, main_content = self._generate_base_template("blog")

        # Add page title
        title = soup.new_tag("h2")
        title["class"] = "page-title"
        title.string = "Blog"
        main_content.append(title)

        # Create post list container
        post_list = soup.new_tag("div")
        post_list["class"] = "blog-list"
        post_list_title = soup.new_tag("h3")
        post_list_title.string = "Blog Posts"
        post_list.append(post_list_title)

        # Create post content container
        post_content = soup.new_tag("div")
        post_content["class"] = "blog-post-content"
        post_content["id"] = "blog-post-content"

        # Get all markdown files
        posts = []
        try:
            for file_path in post_path.glob("*.md"):
                # Parse the post
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Extract title and date
                title = file_path.stem.replace("-", " ").title()
                date = datetime.fromtimestamp(file_path.stat().st_mtime)

                # Check for frontmatter
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        frontmatter = parts[1].strip()
                        content = parts[2].strip()

                        for line in frontmatter.split("\n"):
                            if ":" in line:
                                key, value = line.split(":", 1)
                                key = key.strip().lower()
                                value = value.strip().strip('"').strip("'")

                                if key == "title":
                                    title = value
                                elif key == "date":
                                    try:
                                        date = datetime.fromisoformat(value)
                                    except ValueError:
                                        pass

                # Create post object
                post = {
                    "title": title,
                    "date": date,
                    "content": content,
                    "file_path": file_path,
                    "slug": file_path.stem,
                }
                posts.append(post)

            # Sort posts by date (newest first)
            posts.sort(key=lambda p: p["date"], reverse=True)

            # Create a placeholder post if no posts exist
            if not posts:
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

                    # Parse the placeholder post
                    with open(placeholder_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Add the placeholder post
                    post = {
                        "title": "Welcome to My Blog",
                        "date": datetime(2023, 1, 1),
                        "content": content.split("---", 2)[2].strip(),
                        "file_path": placeholder_path,
                        "slug": "welcome",
                    }
                    posts.append(post)

            # Create post list
            ul = soup.new_tag("ul")
            ul["class"] = "blog-post-list"

            for post in posts:
                li = soup.new_tag("li")
                li["class"] = "blog-post-item"

                # Create link to post page with absolute path
                a = soup.new_tag("a")
                a["href"] = f"/blog/{post['slug']}.html"
                a["onclick"] = f"loadBlogPost('{post['slug']}'); return false;"

                # Add post title and date
                post_title = soup.new_tag("span")
                post_title["class"] = "blog-post-title"
                post_title.string = post["title"]
                a.append(post_title)

                if show_dates and post["date"]:
                    post_date = soup.new_tag("span")
                    post_date["class"] = "blog-post-date"
                    post_date.string = f" ({post['date'].strftime(date_format)})"
                    a.append(post_date)

                li.append(a)
                ul.append(li)

                # Generate individual post page
                self._generate_blog_post_page(post)

            post_list.append(ul)

            # Add post list and content to the main container
            row = soup.new_tag("div")
            row["class"] = "blog-page-layout"
            row.append(post_list)
            row.append(post_content)
            main_content.append(row)

            # If we have posts, add a script to load the first post by default
            if posts:
                script = soup.new_tag("script")
                script.string = f"""
                document.addEventListener('DOMContentLoaded', function() {{ 
                    // Make sure the blog-post-content element exists
                    const contentElement = document.getElementById('blog-post-content');
                    if (contentElement) {{
                        // Only try to load posts if we have the content element
                        // Use absolute path reference, but pass just the slug to the function
                        loadBlogPost('{posts[0]['slug']}');
                    }}
                }});
                """
                soup.body.append(script)

        except Exception as e:
            logger.error(f"Error generating blog page: {e}")
            error_msg = soup.new_tag("p")
            error_msg["class"] = "error-message"
            error_msg.string = f"Error loading blog posts: {e}"
            main_content.append(error_msg)

        # Write the file
        with open(self.build_dir / "blog.html", "w", encoding="utf-8") as f:
            f.write(str(soup.prettify()))

        logger.info("Generated blog page")

    def _generate_blog_post_page(self, post):
        """Generate an individual blog post page."""
        # Create HTML structure from scratch for blog post pages
        html = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <link rel="stylesheet" href="/styles.css">
            <script src="/script.js" defer></script>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title} - William Zujkowski</title>
            <meta name="description" content="Personal website and technology blog">
            <link rel="icon" href="/assets/favicon.ico" type="image/x-icon">
        </head>
        <body class="blog-post-page">
            <header class="site-header">
                <h1>William Zujkowski</h1>
            </header>
            <nav class="site-nav">
                <ul>
                    <li><a href="/home.html">🏠 Home</a></li>
                    <li><a href="/links.html">🔗 Links</a></li>
                    <li><a href="/blog.html">📝 Blog</a></li>
                    <li><a href="/contact.html">✉️ Contact</a></li>
                </ul>
            </nav>
            <main class="site-content">
                <!-- Content will be inserted here -->
            </main>
            <footer class="site-footer">
                <p>© {year} William Zujkowski - Built with Python and Textual</p>
            </footer>
        </body>
        </html>
        """.format(
            title=post["title"],
            year=datetime.now().year
        )
        
        soup = BeautifulSoup(html, "html.parser")
        main_content = soup.select_one("main.site-content")
        
        # Add post title
        title = soup.new_tag("h2")
        title["class"] = "page-title"
        title.string = post["title"]
        main_content.append(title)

        # Add post date if available
        if post["date"]:
            date_format = self.config.get("blog", {}).get("date_format", "%B %d, %Y")
            date = soup.new_tag("p")
            date["class"] = "blog-post-date"
            date.string = f"Published on {post['date'].strftime(date_format)}"
            main_content.append(date)

        # Add post content (convert markdown to HTML)
        content = soup.new_tag("div")
        content["class"] = "markdown-body"
        
        # Convert markdown to HTML
        html_content = markdown.markdown(
            post["content"],
            extensions=["extra", "codehilite"],  # Remove nl2br to prevent unwanted <br/> tags
        )
        
        # Parse the HTML content
        html_soup = BeautifulSoup(html_content, "html.parser")
        
        # Fix links to ensure they open in a new tab with proper security attributes
        for a_tag in html_soup.find_all('a'):
            if a_tag.get('href') and (a_tag['href'].startswith('http://') or a_tag['href'].startswith('https://')):
                a_tag['target'] = '_blank'
                a_tag['rel'] = 'noopener noreferrer'
        
        content.append(html_soup)
        main_content.append(content)

        # Add back link with absolute path
        back_link = soup.new_tag("p")
        back_link["class"] = "back-link"
        a = soup.new_tag("a")
        a["href"] = "/blog.html"
        a.string = "← Back to Blog"
        back_link.append(a)
        main_content.append(back_link)

        # Create blog posts directory
        blog_dir = self.build_dir / "blog"
        blog_dir.mkdir(exist_ok=True)

        # Write the file
        with open(blog_dir / f"{post['slug']}.html", "w", encoding="utf-8") as f:
            f.write(str(soup.prettify()))

        logger.debug(f"Generated blog post page: {post['slug']}.html")

    def _generate_placeholder_pages(self):
        """Generate placeholder pages for future content using markdown content if available."""
        # Get navigation items that might need placeholder pages
        nav_items = self.config.get("navigation", {}).get("items", [])
        for item in nav_items:
            path = item.get("path", "")
            name = item.get("name", "")
            
            # Skip the main pages we've already created
            if path in ["home", "links", "blog"]:
                continue
                
            # Generate a page based on markdown content if available
            soup, main_content = self._generate_base_template(path)
            
            # Check if markdown content exists for this page
            md_path = Path(f"content/pages/{path}/index.md")
            
            if md_path.exists():
                # Process markdown content
                try:
                    with open(md_path, "r", encoding="utf-8") as f:
                        md_content = f.read()
                        
                    # Handle frontmatter if present
                    title = name
                    if md_content.startswith("---"):
                        parts = md_content.split("---", 2)
                        if len(parts) >= 3:
                            frontmatter = parts[1].strip()
                            content = parts[2].strip()
                            
                            # Extract title from frontmatter if present
                            for line in frontmatter.split("\n"):
                                if ":" in line:
                                    key, value = line.split(":", 1)
                                    key = key.strip().lower()
                                    value = value.strip().strip('"').strip("'")
                                    
                                    if key == "title":
                                        title = value
                    else:
                        content = md_content
                    
                    # Add page title
                    title_el = soup.new_tag("h2")
                    title_el["class"] = "page-title"
                    title_el.string = title
                    main_content.append(title_el)
                    
                    # Add markdown content
                    content_div = soup.new_tag("div")
                    content_div["class"] = "markdown-body"
                    
                    # Convert markdown to HTML
                    html_content = markdown.markdown(
                        content,
                        extensions=["extra", "codehilite", "nl2br"],
                    )
                    content_div.append(BeautifulSoup(html_content, "html.parser"))
                    main_content.append(content_div)
                    
                except Exception as e:
                    logger.error(f"Error processing markdown for {path} page: {e}")
                    # Fallback to placeholder content
                    self._add_placeholder_content(main_content, name, path)
            else:
                # No markdown content, use placeholder
                title = soup.new_tag("h2")
                title["class"] = "page-title"
                title.string = name
                main_content.append(title)
                
                self._add_placeholder_content(main_content, name, path)
            
            # Write the file
            with open(self.build_dir / f"{path}.html", "w", encoding="utf-8") as f:
                f.write(str(soup.prettify()))
                
            logger.info(f"Generated page: {path}.html")
    
    def _add_placeholder_content(self, main_content, name, path):
        """Add placeholder content to the main content container."""
        soup = BeautifulSoup("", "html.parser")
        placeholder = soup.new_tag("div")
        placeholder["class"] = "placeholder-container"
        
        heading = soup.new_tag("h3")
        heading.string = f"This page ({name}) is under construction"
        placeholder.append(heading)
        
        text = soup.new_tag("p")
        text.string = "This is a placeholder for future content. Check back later for updates!"
        placeholder.append(text)
        
        tech_note = soup.new_tag("p")
        tech_note.string = f"To add content to this page, create a markdown file at 'content/pages/{path}/index.md'."
        placeholder.append(tech_note)
        
        main_content.append(placeholder)

    def _generate_css(self):
        """Generate CSS for the static site."""
        css = """
        /* Futuristic Cyberpunk Theme */
        :root {
            --primary-color: #0a192f;     /* dark blue */
            --primary-light: #0ff;        /* neon blue */
            --primary-dark: #020c1b;      /* midnight */
            --accent-color: #b967ff;      /* neon purple */
            --accent-light: #fe53bb;      /* neon pink */
            --surface-color: #061121;     /* darker blue */
            --surface-dark: #020c1b;      /* midnight */
            --text-color: #ccd6f6;        /* light slate */
            --text-muted: #8892b0;        /* slate */
            --panel-color: #0a192f;       /* dark blue */
            --panel-dark: #020c1b;        /* midnight */
            --code-bg: #020c1b;           /* midnight */
            --code-color: #64ffda;        /* terminal green */
            --border-radius: 4px;
            --box-shadow: 0 2px 8px rgba(11, 255, 255, 0.2);
            --terminal-green: #64ffda;    /* terminal green */
        }
        
        /* We're always using our cyberpunk theme, no media query needed */
        
        * {
            box-sizing: border-box;
            transition: all 0.3s ease-in-out;
        }
        
        body {
            font-family: 'JetBrains Mono', 'Fira Code', 'Roboto Mono', monospace, -apple-system, BlinkMacSystemFont, "Segoe UI", Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
            line-height: 1.7;
            margin: 0;
            padding: 0;
            color: var(--text-color);
            background-color: var(--surface-color);
            border: 1px solid var(--primary-light);
        }
        
        a {
            color: var(--primary-light);
            text-decoration: none;
            transition: all 0.2s ease-in-out;
            border-bottom: 1px solid var(--primary-light);
            padding: 0 0.1rem;
        }
        
        a:hover {
            color: var(--accent-color);
            border-bottom: 1px solid var(--accent-color);
            text-shadow: 0 0 5px var(--accent-light);
        }
        
        /* Futuristic Header and Footer */
        .site-header {
            background-color: var(--primary-dark);
            color: var(--primary-light);
            padding: 1.5rem 2rem;
            text-align: center;
            border-bottom: 4px solid var(--accent-color);
            box-shadow: 0 0 15px var(--primary-light);
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .site-header h1 {
            margin: 0;
            font-weight: 700;
            text-shadow: 0 0 10px var(--primary-light);
            letter-spacing: 1px;
        }
        
        .site-footer {
            background-color: var(--primary-dark);
            color: var(--primary-light);
            padding: 1.2rem;
            text-align: center;
            border-top: 4px solid var(--accent-color);
            margin-top: 3rem;
            box-shadow: 0 0 15px var(--primary-light);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.9rem;
        }
        
        /* Terminal-inspired elements */
        .terminal-box {
            background-color: var(--panel-dark);
            border: 1px solid var(--primary-light);
            padding: 1.5rem;
            margin: 1.5rem 0;
            box-shadow: inset 0 0 10px rgba(0, 255, 255, 0.2);
        }
        
        .terminal-text {
            color: var(--terminal-green);
            font-family: 'Fira Code', monospace;
            line-height: 1.5;
            margin: 0.5rem 0;
        }
        
        .terminal-prompt {
            padding-left: 1rem;
            border-left: 2px solid var(--primary-light);
        }
        
        /* Digital scan line effect */
        .scanline {
            position: relative;
            overflow: hidden;
            padding: 0.5rem 0;
        }
        
        .scanline:before {
            content: "";
            position: absolute;
            width: 100%;
            height: 2px;
            background-color: var(--primary-light);
            opacity: 0.5;
            animation: scan 2s linear infinite;
        }
        
        @keyframes scan {
            0% { top: 0%; }
            100% { top: 100%; }
        }
        
        /* Animated elements */
        .pulse {
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.6; }
            100% { opacity: 1; }
        }
        
        /* Cyberpunk Navigation */
        .site-nav {
            background-color: var(--primary-color);
            border-bottom: 3px solid var(--accent-color);
            box-shadow: 0 0 10px var(--accent-light);
        }
        
        .site-nav ul {
            display: flex;
            justify-content: center;
            list-style-type: none;
            margin: 0;
            padding: 0;
        }
        
        .site-nav li {
            margin: 0;
            padding: 0;
            position: relative;
        }
        
        .site-nav a {
            display: block;
            padding: 1rem 1.5rem;
            color: var(--text-color);
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease-in-out;
            border-bottom: 3px solid transparent;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
            margin-bottom: -3px;
        }
        
        .site-nav a:hover {
            background-color: var(--primary-dark);
            color: var(--primary-light);
            text-decoration: none;
            border-bottom: 3px solid var(--accent-light);
            text-shadow: 0 0 5px var(--primary-light);
        }
        
        .site-nav a:before {
            content: "";
            position: absolute;
            bottom: 5px;
            left: 0;
            width: 0;
            height: 1px;
            background-color: var(--primary-light);
            transition: width 0.3s ease;
        }
        
        .site-nav a:hover:before {
            width: 100%;
        }
        
        .site-nav a.active {
            background-color: var(--primary-dark);
            color: var(--accent-color);
            border-bottom: 3px solid var(--accent-color);
            text-shadow: 0 0 5px var(--accent-color);
        }
        
        /* Cyberpunk Main content */
        .site-content {
            max-width: 1200px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
            padding: 2rem;
            background-color: var(--surface-color);
            box-shadow: var(--box-shadow);
            border-radius: var(--border-radius);
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
        }
        
        .page-title {
            text-align: center;
            color: var(--accent-color);
            border-bottom: 3px solid var(--accent-light);
            padding-bottom: 0.75rem;
            margin-bottom: 2rem;
            font-size: 2rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 3px;
            text-shadow: 0 0 10px var(--accent-color);
            position: relative;
        }
        
        .page-title:after {
            content: "";
            position: absolute;
            bottom: -3px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 1px;
            background-color: var(--primary-light);
            box-shadow: 0 0 10px var(--primary-light);
        }
        
        /* Cyberpunk Home page */
        .home-welcome {
            text-align: center;
            background-color: var(--primary-dark);
            color: var(--primary-light);
            padding: 2rem;
            border-radius: var(--border-radius);
            margin-bottom: 2rem;
            border: 1px solid var(--primary-light);
            box-shadow: 0 0 15px var(--primary-light);
            position: relative;
            overflow: hidden;
        }
        
        .home-welcome:before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--primary-light), transparent);
            animation: glow 2s linear infinite;
        }
        
        @keyframes glow {
            0% { opacity: 0.3; }
            50% { opacity: 1; }
            100% { opacity: 0.3; }
        }
        
        .home-welcome h3 {
            margin-top: 0;
            font-size: 1.8rem;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: var(--primary-light);
            text-shadow: 0 0 10px var(--primary-light);
        }
        
        .home-intro {
            background-color: var(--panel-color);
            padding: 1.8rem;
            border-radius: var(--border-radius);
            margin-bottom: 2rem;
            border-left: 4px solid var(--accent-color);
            box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.3);
            border: 1px solid var(--accent-light);
            position: relative;
            
            /* Add cyberpunk-style after element */
            &:after {
                content: '';
                position: absolute;
                bottom: 0;
                right: 0;
                width: 50px;
                height: 50px;
                border-right: 2px solid var(--accent-color);
                border-bottom: 2px solid var(--accent-color);
                opacity: 0.7;
            }
        }
        
        /* Futuristic Links page */
        .link-group {
            background-color: var(--panel-color);
            padding: 1.8rem;
            border-radius: var(--border-radius);
            margin-bottom: 2rem;
            border-left: 4px solid var(--accent-color);
            box-shadow: 0 0 15px rgba(185, 103, 255, 0.2);
            transition: transform 0.3s ease-in-out;
            border: 1px solid var(--accent-light);
            position: relative;
            overflow: hidden;
        }
        
        .link-group:before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, transparent 0%, rgba(11, 255, 255, 0.05) 50%, transparent 100%);
            pointer-events: none;
        }
        
        .link-group:hover {
            transform: translateY(-5px);
            box-shadow: 0 0 20px rgba(185, 103, 255, 0.3);
        }
        
        .link-group-title {
            color: var(--accent-color);
            border-bottom: 2px solid var(--accent-light);
            padding-bottom: 0.7rem;
            margin-top: 0;
            font-size: 1.6rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 0 5px var(--accent-color);
        }
        
        .link-list {
            list-style-type: none;
            padding: 0;
            margin-top: 1.5rem;
        }
        
        .link-item {
            margin-bottom: 1.2rem;
            padding: 0.8rem 1rem;
            background-color: var(--surface-color);
            border-radius: var(--border-radius);
            border-left: 4px solid var(--primary-light);
            transition: all 0.3s ease-in-out;
            box-shadow: 0 0 5px rgba(0, 255, 255, 0.2);
            position: relative;
            border: 1px solid transparent;
        }
        
        .link-item:hover {
            background-color: var(--primary-dark);
            border-left-color: var(--accent-color);
            transform: translateX(5px);
            border-color: var(--primary-light);
            box-shadow: 0 0 10px var(--primary-light);
        }
        
        .link-item:before {
            content: "";
            position: absolute;
            left: -4px;
            top: 0;
            height: 100%;
            width: 4px;
            background-color: var(--primary-light);
            opacity: 0.7;
            transition: background-color 0.3s ease-in-out;
        }
        
        .link-item:hover:before {
            background-color: var(--accent-color);
            box-shadow: 0 0 10px var(--accent-color);
        }
        
        .link-description {
            color: var(--text-muted);
            margin: 0.5rem 0 0 1.5rem;
            font-size: 0.9rem;
            font-style: italic;
            border-left: 2px solid var(--accent-light);
            padding-left: 0.5rem;
            font-style: italic;
        }
        
        /* Cyberpunk Blog page */
        .blog-page-layout {
            display: grid;
            grid-template-columns: 1fr 3fr;
            gap: 2rem;
            position: relative;
        }
        
        .blog-page-layout:before {
            content: "";
            position: absolute;
            top: 0;
            left: 50%;
            height: 100%;
            width: 1px;
            background: linear-gradient(to bottom, var(--primary-light), transparent);
            opacity: 0.5;
            pointer-events: none;
        }
        
        @media (max-width: 768px) {
            .blog-page-layout {
                grid-template-columns: 1fr;
            }
            
            .blog-page-layout:before {
                display: none;
            }
        }
        
        .blog-list {
            background-color: var(--panel-color);
            padding: 1.8rem;
            border-radius: var(--border-radius);
            border-left: 4px solid var(--accent-color);
            box-shadow: 0 0 15px rgba(185, 103, 255, 0.2);
            height: fit-content;
            border: 1px solid var(--accent-light);
            position: relative;
            overflow: hidden;
        }
        
        .blog-list:before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, transparent 0%, rgba(11, 255, 255, 0.05) 50%, transparent 100%);
            pointer-events: none;
        }
        
        .blog-post-list {
            list-style-type: none;
            padding: 0;
            margin-top: 1rem;
        }
        
        .blog-post-item {
            margin-bottom: 0.8rem;
            padding: 0.8rem 1rem;
            background-color: var(--surface-color);
            border-radius: var(--border-radius);
            border-left: 4px solid var(--primary-light);
            transition: all 0.3s ease-in-out;
            box-shadow: 0 0 5px rgba(0, 255, 255, 0.2);
            position: relative;
            border: 1px solid transparent;
        }
        
        .blog-post-item:hover {
            background-color: var(--primary-dark);
            border-left-color: var(--accent-color);
            transform: translateX(5px);
            border-color: var(--primary-light);
            box-shadow: 0 0 10px var(--primary-light);
        }
        
        .blog-post-item:before {
            content: "";
            position: absolute;
            left: -4px;
            top: 0;
            height: 100%;
            width: 4px;
            background-color: var(--primary-light);
            opacity: 0.7;
            transition: background-color 0.3s ease-in-out;
        }
        
        .blog-post-item:hover:before {
            background-color: var(--accent-color);
            box-shadow: 0 0 10px var(--accent-color);
        }
        
        .blog-post-title {
            font-weight: 600;
            color: var(--primary-light);
            text-shadow: 0 0 5px var(--primary-light);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .blog-post-date {
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-top: 0.3rem;
            display: inline-block;
            font-style: italic;
            letter-spacing: 1px;
        }
        
        .blog-post-content {
            background-color: var(--panel-color);
            padding: 2rem;
            border-radius: var(--border-radius);
            border-left: 4px solid var(--accent-color);
            box-shadow: 0 0 15px rgba(185, 103, 255, 0.2);
            border: 1px solid var(--accent-light);
            position: relative;
            overflow: hidden;
        }
        
        .blog-post-content:before {
            content: "";
            position: absolute;
            top: 0;
            right: 0;
            width: 50px;
            height: 50px;
            border-top: 2px solid var(--primary-light);
            border-right: 2px solid var(--primary-light);
            opacity: 0.7;
        }
        
        .blog-post-content:after {
            content: "";
            position: absolute;
            bottom: 0;
            left: 0;
            width: 50px;
            height: 50px;
            border-bottom: 2px solid var(--accent-color);
            border-left: 2px solid var(--accent-color);
            opacity: 0.7;
        }
        
        /* Cyberpunk Markdown content */
        .markdown-body {
            line-height: 1.7;
            margin-bottom: 2rem;
            font-family: 'JetBrains Mono', monospace, sans-serif;
            letter-spacing: 0.3px;
        }
        
        .markdown-body h1,
        .markdown-body h2,
        .markdown-body h3,
        .markdown-body h4,
        .markdown-body h5,
        .markdown-body h6 {
            margin-top: 1.8rem;
            margin-bottom: 1rem;
            color: var(--accent-color);
            border-bottom: 1px solid var(--accent-light);
            padding-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-shadow: 0 0 5px var(--accent-color);
        }
        
        .markdown-body h1 {
            color: var(--primary-light);
            text-shadow: 0 0 10px var(--primary-light);
            border-bottom: 2px solid var(--primary-light);
        }
        
        .markdown-body h2 {
            color: var(--accent-color);
            text-shadow: 0 0 5px var(--accent-color);
        }
        
        .markdown-body p {
            margin-bottom: 1.2rem;
        }
        
        .markdown-body a {
            color: var(--primary-light);
            text-decoration: none;
            border-bottom: 1px solid var(--primary-light);
            padding: 0 3px 1px;
            transition: all 0.3s ease;
            position: relative;
            z-index: 1;
        }
        
        .markdown-body a:hover {
            color: var(--accent-color);
            border-color: var(--accent-color);
            text-shadow: 0 0 5px var(--accent-color);
        }
        
        .markdown-body a:before {
            content: "";
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 0;
            background-color: rgba(11, 255, 255, 0.1);
            transition: height 0.3s ease;
            z-index: -1;
        }
        
        .markdown-body a:hover:before {
            height: 100%;
        }
        
        .markdown-body ul, .markdown-body ol {
            padding-left: 2rem;
            margin-bottom: 1.5rem;
        }
        
        .markdown-body li {
            margin-bottom: 0.5rem;
        }
        
        .markdown-body code {
            background-color: var(--code-bg);
            color: var(--terminal-green);
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: 'Fira Code', 'JetBrains Mono', monospace;
            border: 1px solid rgba(100, 255, 218, 0.3);
            text-shadow: 0 0 2px var(--terminal-green);
        }
        
        .markdown-body pre {
            background-color: var(--code-bg);
            padding: 1rem;
            border-radius: var(--border-radius);
            overflow-x: auto;
            margin: 1.5rem 0;
            border: 1px solid var(--primary-light);
            box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.5);
            position: relative;
        }
        
        .markdown-body pre:before {
            content: "</> code";
            position: absolute;
            top: -10px;
            right: 10px;
            background-color: var(--primary-dark);
            color: var(--terminal-green);
            padding: 0 8px;
            font-size: 0.8rem;
            border-radius: 3px;
            border: 1px solid var(--terminal-green);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .markdown-body img {
            max-width: 100%;
            height: auto;
            border-radius: var(--border-radius);
            margin: 1.5rem 0;
            border: 1px solid var(--primary-light);
            box-shadow: 0 0 15px rgba(11, 255, 255, 0.3);
            opacity: 0.9;
            transition: opacity 0.3s ease, transform 0.3s ease;
        }
        
        .markdown-body img:hover {
            opacity: 1;
            transform: scale(1.01);
        }
        
        /* Image captions */
        .image-container {
            margin: 2rem 0;
            text-align: center;
            background-color: var(--panel-dark);
            padding: 1rem;
            border-radius: var(--border-radius);
            border: 1px solid var(--primary-light);
            box-shadow: 0 0 10px rgba(11, 255, 255, 0.2);
        }
        
        .image-caption {
            color: var(--text-muted);
            font-style: italic;
            margin-top: 0.5rem;
            font-size: 0.9rem;
            text-align: center;
        }
        
        .markdown-body blockquote {
            margin: 1.5rem 0;
            padding: 1rem 1.5rem;
            border-left: 4px solid var(--accent-light);
            background-color: var(--panel-dark);
            color: var(--text-muted);
            font-style: italic;
            position: relative;
            border-radius: 0 var(--border-radius) var(--border-radius) 0;
            box-shadow: 0 0 10px rgba(185, 103, 255, 0.1);
        }
        
        .markdown-body blockquote:before {
            content: "\\201C";
            position: absolute;
            top: 0;
            left: 0.5rem;
            font-size: 2rem;
            color: var(--accent-color);
            opacity: 0.5;
            line-height: 1;
        }
        
        /* Terminal-inspired elements with animations */
        .terminal-box {
            background-color: var(--panel-dark);
            border: 1px solid var(--primary-light);
            padding: 1.5rem;
            margin: 1.5rem 0;
            box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.3);
            border-radius: var(--border-radius);
            position: relative;
            overflow: hidden;
        }
        
        .terminal-box:before {
            content: attr(data-terminal-name);
            position: absolute;
            top: -10px;
            left: 10px;
            background-color: var(--primary-dark);
            color: var(--primary-light);
            padding: 0 8px;
            font-size: 0.8rem;
            border-radius: 3px;
            border: 1px solid var(--primary-light);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .terminal-box:after {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: var(--primary-light);
            opacity: 0.3;
            animation: terminalScan 4s linear infinite;
        }
        
        @keyframes terminalScan {
            0% { transform: translateY(0); }
            100% { transform: translateY(100%); }
        }
        
        .terminal-text {
            color: var(--terminal-green);
            font-family: 'Fira Code', monospace;
            line-height: 1.5;
            margin: 0.5rem 0;
            overflow: hidden;
            border-right: 0.15em solid var(--terminal-green);
            white-space: nowrap;
            animation: typing 3.5s steps(40, end), blink-caret 0.75s step-end infinite;
            animation-fill-mode: both;
            width: fit-content;
        }
        
        .terminal-text.delay-1 {
            animation-delay: 0.5s;
        }
        
        .terminal-text.delay-2 {
            animation-delay: 2s;
        }
        
        .terminal-text.delay-3 {
            animation-delay: 3.5s;
        }
        
        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }
        
        @keyframes blink-caret {
            from, to { border-color: transparent }
            50% { border-color: var(--terminal-green) }
        }
        
        .terminal-prompt {
            padding-left: 1rem;
            border-left: 2px solid var(--primary-light);
            position: relative;
            display: flex;
            align-items: center;
        }
        
        .terminal-prompt:before {
            content: ">";
            color: var(--primary-light);
            margin-right: 8px;
            display: inline-block;
        }
        
        .terminal-user-info {
            position: absolute;
            top: -32px;
            right: 10px;
            color: var(--text-muted);
            font-size: 0.8rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .terminal-user-info span {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .terminal-user-info .pulse-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--terminal-green);
            display: inline-block;
            animation: pulse 1.5s infinite;
        }
        
        .markdown-body table {
            width: 100%;
            margin: 1.5rem 0;
            border-collapse: collapse;
            border: 1px solid var(--primary-light);
            box-shadow: 0 0 15px rgba(11, 255, 255, 0.2);
            border-radius: var(--border-radius);
            overflow: hidden;
        }
        
        .markdown-body table th,
        .markdown-body table td {
            padding: 0.75rem;
            text-align: left;
            border: 1px solid var(--primary-light);
        }
        
        .markdown-body table th {
            background-color: var(--primary-dark);
            color: var(--primary-light);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 700;
            text-shadow: 0 0 5px var(--primary-light);
        }
        
        .markdown-body table tr {
            background-color: var(--surface-color);
            transition: background-color 0.3s ease;
        }
        
        .markdown-body table tr:nth-child(even) {
            background-color: var(--panel-dark);
        }
        
        .markdown-body table tr:hover {
            background-color: var(--panel-dark);
        }
        
        .markdown-body ul,
        .markdown-body ol {
            margin-bottom: 1.5rem;
        }
        
        .markdown-body li {
            margin-bottom: 0.5rem;
        }
        
        .markdown-body pre {
            background-color: var(--code-bg);
            color: var(--code-color);
            padding: 1.2rem;
            border-radius: var(--border-radius);
            overflow-x: auto;
            margin: 1.5rem 0;
            box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
        }
        
        .markdown-body code {
            background-color: var(--code-bg);
            color: var(--code-color);
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: 'Fira Code', SFMono-Regular, Consolas, Liberation Mono, Menlo, monospace;
            font-size: 0.9rem;
        }
        
        .markdown-body pre code {
            padding: 0;
            background-color: transparent;
        }
        
        .markdown-body blockquote {
            border-left: 4px solid var(--accent-light);
            padding-left: 1rem;
            margin-left: 0;
            color: var(--text-muted);
            font-style: italic;
        }
        
        /* Enhanced Placeholder pages */
        .placeholder-container {
            text-align: center;
            background-color: var(--panel-color);
            padding: 3.5rem;
            border-radius: var(--border-radius);
            margin: 3rem auto;
            max-width: 800px;
            border-top: 4px solid var(--accent-color);
            box-shadow: var(--box-shadow);
        }
        
        .placeholder-container h3 {
            color: var(--accent-color);
            margin-top: 0;
            font-size: 1.8rem;
        }
        
        /* Enhanced Utility classes */
        .back-link {
            margin-top: 2.5rem;
            display: inline-block;
            padding: 0.6rem 1.2rem;
            background-color: var(--primary-light);
            color: white;
            border-radius: var(--border-radius);
            text-decoration: none;
            transition: all 0.2s ease-in-out;
        }
        
        .back-link a {
            color: white;
            border-bottom: none;
        }
        
        .back-link:hover {
            background-color: var(--accent-color);
            transform: translateX(-3px);
        }
        
        .error-message {
            color: var(--accent-color);
            background-color: rgba(231, 76, 60, 0.1);
            padding: 1.2rem;
            border-radius: var(--border-radius);
            border-left: 4px solid var(--accent-color);
            margin: 1.5rem 0;
        }
        """
        
        # Write the CSS file
        with open(self.build_dir / "styles.css", "w", encoding="utf-8") as f:
            f.write(css)
            
        logger.info("Generated CSS file")

    def _generate_javascript(self):
        """Generate JavaScript for the static site."""
        js = """
        // JavaScript functionality for the static site
        
        // Terminal animation and user info functionality
        async function setupTerminalElements() {
            // Find all terminal boxes
            const terminalBoxes = document.querySelectorAll('.terminal-box');
            
            if (terminalBoxes.length === 0) return;
            
            // Try to get user IP information
            let userInfo = {
                ip: "127.0.0.1",
                city: "localhost",
                country: "local",
                browser: navigator.userAgent.split(' ')[0]
            };
            
            try {
                const response = await fetch('https://api.ipify.org?format=json');
                if (response.ok) {
                    const data = await response.json();
                    userInfo.ip = data.ip;
                    
                    // Try to get location data
                    try {
                        const geoResponse = await fetch(`https://ipapi.co/${data.ip}/json/`);
                        if (geoResponse.ok) {
                            const geoData = await geoResponse.json();
                            userInfo.city = geoData.city || "Unknown";
                            userInfo.country = geoData.country_name || "Unknown";
                        }
                    } catch (e) {
                        console.log('Geo location fetch failed:', e);
                    }
                }
            } catch (e) {
                console.log('IP fetch failed:', e);
            }
            
            // Process each terminal box
            terminalBoxes.forEach((box, index) => {
                // Set unique terminal name
                box.setAttribute('data-terminal-name', `$ terminal-${index + 1}`);
                
                // Add user info to the terminal
                const userInfoDiv = document.createElement('div');
                userInfoDiv.className = 'terminal-user-info';
                userInfoDiv.innerHTML = `
                    <span><div class="pulse-dot"></div>CONNECTED</span>
                    <span>IP: ${userInfo.ip}</span>
                    <span>LOC: ${userInfo.city}, ${userInfo.country}</span>
                    <span>TIME: ${new Date().toLocaleTimeString()}</span>
                `;
                box.appendChild(userInfoDiv);
                
                // Add animation classes to text elements
                const textElements = box.querySelectorAll('.terminal-text');
                textElements.forEach((el, idx) => {
                    // Add sequential animation delay classes
                    if (idx === 0) el.classList.add('delay-1');
                    else if (idx === 1) el.classList.add('delay-2');
                    else el.classList.add('delay-3');
                });
            });
        }
        
        // Function to ensure all navigation links work correctly
        document.addEventListener('DOMContentLoaded', function() {
            // Setup terminal elements with user information
            setupTerminalElements();
            
            // Fix navigation links on blog and blog post pages
            const isBlogPage = window.location.pathname.endsWith('/blog.html');
            const isBlogPostPage = window.location.pathname.includes('/blog/');
            
            // Only apply the fix where needed
            if (isBlogPage || isBlogPostPage) {
                // Get all navigation links
                const navLinks = document.querySelectorAll('.site-nav a');
                
                // Add click handlers that force full page navigation
                navLinks.forEach(link => {
                    if (!link.getAttribute('href').includes('blog')) {
                        link.addEventListener('click', function(e) {
                            // Force a full page navigation
                            window.location.href = this.getAttribute('href');
                            e.preventDefault();
                        });
                    }
                });
            }
        });
        
        // Function to load blog post content via Ajax
        function loadBlogPost(slug) {
            // Always use absolute paths with root
            const basePath = '/blog/';
            
            // Update URL without full navigation
            if (history.pushState) {
                // Always use absolute path from root
                const newUrl = basePath + slug + '.html';
                window.history.pushState({path: newUrl}, '', newUrl);
            }
            
            // Fetch the post content with the correct absolute path
            fetch(basePath + slug + '.html')
                .then(response => response.text())
                .then(html => {
                    // Parse the HTML content
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    
                    // Extract the main content
                    const content = doc.querySelector('.site-content');
                    
                    // Update our page's content area
                    document.getElementById('blog-post-content').innerHTML = content.innerHTML;
                    
                    // Highlight the active post in the list
                    const postItems = document.querySelectorAll('.blog-post-item');
                    postItems.forEach(item => {
                        if (item.querySelector('a').getAttribute('href').includes(slug)) {
                            item.classList.add('active');
                        } else {
                            item.classList.remove('active');
                        }
                    });
                })
                .catch(error => {
                    console.error('Error loading blog post:', error);
                    document.getElementById('blog-post-content').innerHTML = 
                        '<div class="error-message">Error loading blog post: ' + error.message + '</div>';
                });
        }
        
        // Handle browser back/forward navigation
        window.onpopstate = function(event) {
            const path = window.location.pathname;
            
            // Check if we're on a blog post page
            const blogPostMatch = path.match(/^\\/blog\\/([\\w\\-]+)\\.html$/);
            if (blogPostMatch) {
                // We're on a specific post, load it
                loadBlogPost(blogPostMatch[1]);
                return;
            }
            
            // If we navigated away from a blog post, reload the page
            if (path === '/blog.html') {
                window.location.reload();
            }
        };
        
        // Initialize theme toggle based on user preference
        document.addEventListener('DOMContentLoaded', function() {
            // Apply any saved theme preference or respect system preference
            const savedTheme = localStorage.getItem('theme');
            if (savedTheme) {
                document.documentElement.setAttribute('data-theme', savedTheme);
            }
        });
        """
        
        # Write the JavaScript file
        with open(self.build_dir / "script.js", "w", encoding="utf-8") as f:
            f.write(js)
            
        logger.info("Generated JavaScript file")
