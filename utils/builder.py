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

        # Add favicon with correct path
        favicon = soup.new_tag("link")
        favicon["rel"] = "icon"
        if active_page.startswith("blog/"):
            favicon["href"] = "../assets/favicon.ico"
        else:
            favicon["href"] = "assets/favicon.ico"
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
            
            # Use absolute paths from root with correct relative paths
            if active_page.startswith("blog/"):
                # If we're in a blog post page, navigate up one level for non-blog pages
                if path != "blog":
                    a["href"] = f"../{path}.html"
                else:
                    a["href"] = f"../blog.html"  # Special case for blog link
            else:
                a["href"] = f"{path}.html"

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
        # Adjust CSS and JavaScript paths for blog posts
        if page_name.startswith("blog/"):
            css_path = "../styles.css"
            js_path = "../script.js"
        else:
            css_path = "styles.css"
            js_path = "script.js"
            
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
        """Generate the home page."""
        soup, main_content = self._generate_base_template("home")

        # Add page title
        title = soup.new_tag("h2")
        title["class"] = "page-title"
        title.string = "Home"
        main_content.append(title)

        # Add welcome message
        welcome = soup.new_tag("div")
        welcome["class"] = "home-welcome"
        welcome_title = soup.new_tag("h3")
        site_title = self.config["site"].get("title", "William Zujkowski")
        welcome_title.string = f"Welcome to {site_title}'s Website"
        welcome.append(welcome_title)
        main_content.append(welcome)

        # Add introduction
        intro = soup.new_tag("div")
        intro["class"] = "home-intro"
        intro_content = soup.new_tag("p")
        intro_content.string = """This is a personal website built with Python and Textual, 
        showcasing a modern terminal-inspired design that works great as both a TUI and a static website."""
        intro.append(intro_content)

        features = soup.new_tag("div")
        features_title = soup.new_tag("h4")
        features_title.string = "Features:"
        features.append(features_title)

        feature_list = soup.new_tag("ul")
        for feature in [
            "Blog posts with Markdown support",
            "Links to various resources and profiles",
            "Clean, responsive web design",
            "Terminal-friendly interface when run as a TUI",
        ]:
            li = soup.new_tag("li")
            li.string = feature
            feature_list.append(li)

        features.append(feature_list)
        intro.append(features)
        main_content.append(intro)

        # Add about section
        about = soup.new_tag("div")
        about["class"] = "home-intro"
        about_title = soup.new_tag("h3")
        about_title.string = "About the Developer"
        about.append(about_title)

        about_content = soup.new_tag("p")
        about_content.string = """I am a software developer with a passion for Python, 
        web technologies, and terminal-based user interfaces."""
        about.append(about_content)

        interests = soup.new_tag("p")
        interests.string = "My interests include:"
        about.append(interests)

        interest_list = soup.new_tag("ul")
        for interest in [
            "Python development",
            "Terminal user interfaces",
            "Web technologies",
            "Open source software",
        ]:
            li = soup.new_tag("li")
            li.string = interest
            interest_list.append(li)

        about.append(interest_list)
        main_content.append(about)

        # Write the file
        with open(self.build_dir / "home.html", "w", encoding="utf-8") as f:
            f.write(str(soup.prettify()))

        logger.info("Generated home page")

    def _generate_links_page(self):
        """Generate the links page."""
        soup, main_content = self._generate_base_template("links")

        # Add page title
        title = soup.new_tag("h2")
        title["class"] = "page-title"
        title.string = "Links"
        main_content.append(title)

        # Add introduction
        intro = soup.new_tag("div")
        intro["class"] = "home-intro"
        intro_content = soup.new_tag("p")
        intro_content.string = """Below are links to various resources, social profiles, and projects.
        Links are organized by category for easier navigation."""
        intro.append(intro_content)
        main_content.append(intro)

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

            group_container = soup.new_tag("div")
            group_container["class"] = "link-group"

            group_title = soup.new_tag("h3")
            group_title["class"] = "link-group-title"
            group_title.string = f"{group_icon} {group_name}"
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

                # Create link to post page
                a = soup.new_tag("a")
                a["href"] = f"blog/{post['slug']}.html"
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
            <link rel="stylesheet" href="../styles.css">
            <script src="../script.js" defer></script>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title} - William Zujkowski</title>
            <meta name="description" content="Personal website and technology blog">
            <link rel="icon" href="../assets/favicon.ico" type="image/x-icon">
        </head>
        <body class="blog-post-page">
            <header class="site-header">
                <h1>William Zujkowski</h1>
            </header>
            <nav class="site-nav">
                <ul>
                    <li><a href="javascript:void(0)" onclick="window.location.href='../home.html'">🏠 Home</a></li>
                    <li><a href="javascript:void(0)" onclick="window.location.href='../links.html'">🔗 Links</a></li>
                    <li><a href="javascript:void(0)" onclick="window.location.href='../blog.html'">📝 Blog</a></li>
                    <li><a href="javascript:void(0)" onclick="window.location.href='../placeholder.html'">✉️ Contact</a></li>
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
            extensions=["extra", "codehilite", "nl2br"],
        )
        content.append(BeautifulSoup(html_content, "html.parser"))
        main_content.append(content)

        # Add back link
        back_link = soup.new_tag("p")
        back_link["class"] = "back-link"
        a = soup.new_tag("a")
        a["href"] = "../blog.html"
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
        """Generate placeholder pages for future content."""
        # Get navigation items that might need placeholder pages
        nav_items = self.config.get("navigation", {}).get("items", [])
        for item in nav_items:
            path = item.get("path", "")
            name = item.get("name", "")
            
            # Skip the main pages we've already created
            if path in ["home", "links", "blog"]:
                continue
                
            # Generate a placeholder page
            soup, main_content = self._generate_base_template(path)
            
            # Add page title
            title = soup.new_tag("h2")
            title["class"] = "page-title"
            title.string = name
            main_content.append(title)
            
            # Add placeholder content
            placeholder = soup.new_tag("div")
            placeholder["class"] = "placeholder-container"
            
            heading = soup.new_tag("h3")
            heading.string = f"This page ({name}) is under construction"
            placeholder.append(heading)
            
            text = soup.new_tag("p")
            text.string = "This is a placeholder for future content. Check back later for updates!"
            placeholder.append(text)
            
            tech_note = soup.new_tag("p")
            tech_note.string = f"To add content to this page, create a new module in the 'pages' directory for {path}."
            placeholder.append(tech_note)
            
            main_content.append(placeholder)
            
            # Write the file
            with open(self.build_dir / f"{path}.html", "w", encoding="utf-8") as f:
                f.write(str(soup.prettify()))
                
            logger.info(f"Generated placeholder page: {path}.html")

    def _generate_css(self):
        """Generate CSS for the static site."""
        css = """
        /* Enhanced Global styles with improved color schemes */
        :root {
            --primary-color: #2c3e50;
            --primary-light: #3498db;
            --primary-dark: #1a2634;
            --accent-color: #e74c3c;
            --accent-light: #f39c12;
            --surface-color: #ecf0f1;
            --surface-dark: #bdc3c7;
            --text-color: #333;
            --text-muted: #7f8c8d;
            --panel-color: #f5f5f5;
            --panel-dark: #dcdcdc;
            --code-bg: #2d2d2d;
            --code-color: #f8f8f2;
            --border-radius: 4px;
            --box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        
        @media (prefers-color-scheme: dark) {
            :root {
                --primary-color: #1a2634;
                --primary-light: #2980b9;
                --primary-dark: #0d1218;
                --accent-color: #e74c3c;
                --accent-light: #f39c12;
                --surface-color: #2c3e50;
                --surface-dark: #34495e;
                --text-color: #ecf0f1;
                --text-muted: #bdc3c7;
                --panel-color: #34495e;
                --panel-dark: #2c3e50;
                --code-bg: #1e1e1e;
                --code-color: #f8f8f2;
                --box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
            }
        }
        
        * {
            box-sizing: border-box;
            transition: all 0.3s ease-in-out;
        }
        
        body {
            font-family: 'Roboto', -apple-system, BlinkMacSystemFont, "Segoe UI", Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
            line-height: 1.7;
            margin: 0;
            padding: 0;
            color: var(--text-color);
            background-color: var(--surface-color);
        }
        
        a {
            color: var(--primary-light);
            text-decoration: none;
            transition: all 0.2s ease-in-out;
            border-bottom: 1px dotted transparent;
        }
        
        a:hover {
            color: var(--accent-color);
            border-bottom: 1px dotted var(--accent-color);
        }
        
        /* Enhanced Header and Footer */
        .site-header {
            background-color: var(--primary-dark);
            color: white;
            padding: 1.5rem 2rem;
            text-align: center;
            border-bottom: 4px solid var(--accent-color);
            box-shadow: var(--box-shadow);
        }
        
        .site-header h1 {
            margin: 0;
            font-weight: 700;
            letter-spacing: 1px;
        }
        
        .site-footer {
            background-color: var(--primary-dark);
            color: white;
            padding: 1.2rem;
            text-align: center;
            border-top: 4px solid var(--accent-color);
            margin-top: 3rem;
            box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
        }
        
        /* Enhanced Navigation */
        .site-nav {
            background-color: var(--primary-color);
            border-bottom: 3px solid var(--accent-color);
            box-shadow: var(--box-shadow);
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
            color: white;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
            border-bottom: none;
            border-bottom: 3px solid transparent;
            margin-bottom: -3px;
        }
        
        .site-nav a:hover {
            background-color: var(--primary-light);
            color: white;
            text-decoration: none;
            border-bottom: 3px solid var(--accent-light);
        }
        
        .site-nav a.active {
            background-color: var(--primary-dark);
            color: white;
            border-bottom: 3px solid var(--accent-color);
        }
        
        /* Enhanced Main content */
        .site-content {
            max-width: 1200px;
            margin: 0 auto;
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
        }
        
        /* Enhanced Home page */
        .home-welcome {
            text-align: center;
            background-color: var(--primary-dark);
            color: white;
            padding: 2rem;
            border-radius: var(--border-radius);
            margin-bottom: 2rem;
            border: none;
            box-shadow: var(--box-shadow);
        }
        
        .home-welcome h3 {
            margin-top: 0;
            font-size: 1.8rem;
            letter-spacing: 0.5px;
        }
        
        .home-intro {
            background-color: var(--panel-color);
            padding: 1.8rem;
            border-radius: var(--border-radius);
            margin-bottom: 2rem;
            border-left: 4px solid var(--accent-color);
            box-shadow: var(--box-shadow);
        }
        
        /* Enhanced Links page */
        .link-group {
            background-color: var(--panel-color);
            padding: 1.8rem;
            border-radius: var(--border-radius);
            margin-bottom: 2rem;
            border-left: 4px solid var(--accent-color);
            box-shadow: var(--box-shadow);
            transition: transform 0.2s ease-in-out;
        }
        
        .link-group:hover {
            transform: translateY(-3px);
        }
        
        .link-group-title {
            color: var(--accent-color);
            border-bottom: 2px solid var(--accent-light);
            padding-bottom: 0.7rem;
            margin-top: 0;
            font-size: 1.6rem;
            font-weight: 700;
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
            transition: all 0.2s ease-in-out;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        }
        
        .link-item:hover {
            background-color: var(--surface-dark);
            border-left-color: var(--accent-color);
            transform: translateX(3px);
        }
        
        .link-description {
            color: var(--text-muted);
            margin: 0.5rem 0 0 1.5rem;
            font-size: 0.9rem;
            font-style: italic;
        }
        
        /* Enhanced Blog page */
        .blog-page-layout {
            display: grid;
            grid-template-columns: 1fr 3fr;
            gap: 2rem;
        }
        
        @media (max-width: 768px) {
            .blog-page-layout {
                grid-template-columns: 1fr;
            }
        }
        
        .blog-list {
            background-color: var(--panel-color);
            padding: 1.8rem;
            border-radius: var(--border-radius);
            border-left: 4px solid var(--accent-color);
            box-shadow: var(--box-shadow);
            height: fit-content;
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
            transition: all 0.2s ease-in-out;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        }
        
        .blog-post-item:hover {
            background-color: var(--surface-dark);
            border-left-color: var(--accent-color);
            transform: translateX(3px);
        }
        
        .blog-post-title {
            font-weight: 600;
        }
        
        .blog-post-date {
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-top: 0.3rem;
            display: inline-block;
        }
        
        .blog-post-content {
            background-color: var(--panel-color);
            padding: 2rem;
            border-radius: var(--border-radius);
            border-left: 4px solid var(--accent-color);
            box-shadow: var(--box-shadow);
        }
        
        /* Enhanced Markdown content */
        .markdown-body {
            line-height: 1.7;
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
        }
        
        .markdown-body p {
            margin-bottom: 1.2rem;
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
        
        // Function to ensure all navigation links work correctly
        document.addEventListener('DOMContentLoaded', function() {
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
            // Determine the correct path for fetching blog posts
            const inBlogDir = window.location.pathname.includes('/blog/');
            // If we're already in the blog directory, we don't need to add 'blog/'
            // Otherwise, we need to fetch from 'blog/'
            const basePath = inBlogDir ? '' : 'blog/';
            
            // Update URL without full navigation
            if (history.pushState) {
                // If we're already in a blog post, just change the slug part
                if (inBlogDir) {
                    const newUrl = window.location.pathname.replace(/[^/]*$/, slug + '.html');
                    window.history.pushState({path: newUrl}, '', newUrl);
                } else {
                    // Create URL correctly based on the current path structure
                    // Make sure we don't get blog/blog/slug.html
                    const pathBase = window.location.pathname.includes('/blog.html') 
                        ? window.location.pathname.replace('blog.html', '')
                        : window.location.pathname.replace(/\\/[^\\/]*$/, '/');
                    const newUrl = window.location.origin + pathBase + 'blog/' + slug + '.html';
                    window.history.pushState({path: newUrl}, '', newUrl);
                }
            }
            
            // Fetch the post content with the correct path
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
            const blogPostMatch = path.match(/\\/blog\\/([\\w\\-]+)\\.html$/);
            if (blogPostMatch) {
                // We're on a specific post, load it
                loadBlogPost(blogPostMatch[1]);
                return;
            }
            
            // If we navigated away from a blog post, reload the page
            if (path.endsWith('/blog.html')) {
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
