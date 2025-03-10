#!/usr/bin/env python3
import os
import re
import json
import shutil
from datetime import datetime
from bs4 import BeautifulSoup

# Configuration – adjust these paths if needed
MERGED_FILE = "merged_blog_posts.html"  # File containing new blog posts (if present)
BLOG_DIR = "blog"  # Directory to store individual blog post files
BLOG_LIST_JSON = "blog_list.json"  # JSON file listing all blog posts

# New header, nav, footer markup (using htmx)
NEW_HEADER = '<header hx-get="/includes/header.html" hx-trigger="load" hx-swap="outerHTML"></header>'
NEW_NAV = (
    '<nav hx-get="/includes/nav.html" hx-trigger="load" hx-swap="outerHTML"></nav>'
)
NEW_FOOTER = '<footer hx-get="/includes/footer.html" hx-trigger="load" hx-swap="outerHTML"></footer>'

# Template to wrap each blog post content consistently
TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <link rel="icon" href="../assets/images/favicon.ico" type="image/x-icon" />
  <link rel="stylesheet" href="../assets/css/style.css" />
  <script src="https://unpkg.com/htmx.org@1.9.2"></script>
</head>
<body>
  {header}
  {nav}
  <main class="container">
    {content}
  </main>
  {footer}
</body>
</html>
"""

# Regexes for markdown conversions
MD_LINK_REGEX = re.compile(r"\[([^\]]+)\]\(([^\)]+)\)")
BOLD_REGEX = re.compile(r"\*\*([^*]+)\*\*")
UNDERLINE_BOLD_REGEX = re.compile(r"__([^_]+)__")


def convert_markdown_links(text):
    """Convert markdown hyperlinks [text](url) to HTML <a> tags."""
    return MD_LINK_REGEX.sub(r'<a href="\2">\1</a>', text)


def convert_markdown_bold(text):
    """Convert markdown bold syntax (**text** or __text__) to HTML <strong> tags."""
    text = BOLD_REGEX.sub(r"<strong>\1</strong>", text)
    text = UNDERLINE_BOLD_REGEX.sub(r"<strong>\1</strong>", text)
    return text


def slugify(text):
    """Generate a slug from text: lower-case, dashes for spaces, remove non-alphanumerics."""
    text = text.lower().strip()
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"[^a-z0-9\-]", "", text)
    return text


def validate_date(date_str):
    """Return date_str if it's in YYYY-MM-DD format; otherwise, return 'unknown'."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        return "unknown"


def extract_metadata(soup):
    """
    Extract the title, date, and slug from the BeautifulSoup object.
    Fallbacks:
      - If the <title> tag is missing or equals "{title}", use the first <h2> in the inner article.
      - Clean up the title (collapse whitespace).
      - For date and slug, first look for an <em> in the first <p>.
      - If not found, try inner article attributes.
      - As a fallback for date, search for any <p> containing "Date:".
      - If slug is missing or "unknown", generate one from the title.
    """
    # Extract title
    title = ""
    title_tag = soup.find("title")
    if title_tag:
        title = " ".join(title_tag.get_text(strip=True).split())
    if not title or title == "{title}":
        inner_article = soup.find("article")
        if inner_article:
            h2 = inner_article.find("h2")
            if h2:
                title = " ".join(h2.get_text(strip=True).split())
    if not title:
        title = "Untitled"

    # Extract date and slug from first <em> within first <p>
    date = "unknown"
    slug = ""
    first_p = soup.find("p")
    if first_p:
        em_tag = first_p.find("em")
        if em_tag:
            em_text = em_tag.get_text(strip=True)
            parts = [p.strip() for p in em_text.split("|")]
            if len(parts) >= 2:
                date = validate_date(parts[0])
                slug = parts[1]
    # If still missing, check inner article attributes
    inner_article = soup.find("article")
    if inner_article:
        if inner_article.has_attr("data-date"):
            date = validate_date(inner_article["data-date"])
        if inner_article.has_attr("data-slug"):
            slug = inner_article["data-slug"]

    # Fallback: search for any <p> containing "Date:"
    if date == "unknown":
        for p in soup.find_all("p"):
            text = p.get_text()
            if "Date:" in text:
                potential_date = text.split("Date:")[-1].strip().split()[0]
                date = validate_date(potential_date)
                if date != "unknown":
                    break

    # If slug is still missing or equals "unknown", generate one from title
    if not slug or slug == "unknown":
        slug = slugify(title)

    return title, date, slug


def build_template(title, content_html):
    """Build the full HTML page using the standard template."""
    return TEMPLATE.format(
        title=title,
        header=NEW_HEADER,
        nav=NEW_NAV,
        content=content_html,
        footer=NEW_FOOTER,
    )


def process_merged_file():
    """
    Process the merged HTML file (if it exists):
      - Split it into individual posts.
      - Convert markdown hyperlinks and bold markdown to HTML.
      - Remove any vestigial header, nav, footer, or duplicate elements (any element with an hx-get attribute).
      - Extract metadata (title, date, slug) and rebuild the content using the template.
      - Ensure that the <title> tag in the new page matches the final title.
      - Save the post as BLOG_DIR/slug.html.
    """
    if not os.path.exists(MERGED_FILE):
        print(f"INFO: Merged file '{MERGED_FILE}' not found. Skipping this step.")
        return

    with open(MERGED_FILE, "r", encoding="utf-8") as f:
        merged_content = f.read()

    # Split posts based on the DOCTYPE marker
    posts_raw = re.split(r"(?=<!DOCTYPE html>)", merged_content)
    for post in posts_raw:
        post = post.strip()
        if not post:
            continue
        if not post.startswith("<!DOCTYPE html>"):
            post = "<!DOCTYPE html>\n" + post

        # Convert markdown links and bold syntax
        post = convert_markdown_links(post)
        post = convert_markdown_bold(post)

        soup = BeautifulSoup(post, "html.parser")

        # Remove vestigial elements by removing any element with an hx-get attribute
        for tag in soup.find_all(attrs={"hx-get": True}):
            tag.decompose()

        # Remove any old scripts referencing main.js
        for script in soup.find_all("script", src=True):
            if "main.js" in script["src"]:
                script.decompose()

        # Extract metadata from the current soup
        title, date, slug = extract_metadata(soup)

        # Ensure the <title> tag in the head matches the determined title.
        if soup.title:
            soup.title.string = title
        else:
            head = soup.head or soup.new_tag("head")
            new_title = soup.new_tag("title")
            new_title.string = title
            head.append(new_title)
            if not soup.head:
                soup.html.insert(0, head)

        # Extract the main content – use the inner <article> if available;
        # otherwise, use the entire body after removing any extraneous header/nav/footer.
        content_section = ""
        inner_article = soup.find("article")
        if inner_article:
            content_section = inner_article.decode_contents()
        else:
            # As fallback, remove any header, nav, footer from body and use the rest.
            for tag in soup.find_all(["header", "nav", "footer"]):
                tag.decompose()
            content_section = soup.body.decode_contents()

        # Build new full HTML using our template
        full_html = build_template(title, content_section)

        # Write the new HTML to a file named using the slug (ensuring consistency)
        output_filename = os.path.join(BLOG_DIR, slug + ".html")
        with open(output_filename, "w", encoding="utf-8") as out_f:
            out_f.write(full_html)
        print(
            f"Processed post: '{title}' | Date: {date} | Slug: '{slug}' => {output_filename}"
        )


def update_blog_list():
    """
    Scan all .html files in BLOG_DIR and update BLOG_LIST_JSON.
    Deduplicate entries by slug and sort them by date (descending).
    Create a backup of the existing BLOG_LIST_JSON before writing.
    """
    blog_entries = []
    for filename in os.listdir(BLOG_DIR):
        if filename.lower().endswith(".html"):
            filepath = os.path.join(BLOG_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            soup = BeautifulSoup(content, "html.parser")
            title, date, slug = extract_metadata(soup)
            blog_entries.append({"title": title, "date": date, "slug": slug})

    # Deduplicate entries by slug (latest occurrence wins)
    unique_entries = {}
    for entry in blog_entries:
        unique_entries[entry["slug"]] = entry
    final_entries = list(unique_entries.values())

    # Sort entries by date descending (if date valid; else treat as very old)
    def sort_key(entry):
        try:
            return datetime.strptime(entry["date"], "%Y-%m-%d")
        except Exception:
            return datetime.min

    final_entries.sort(key=sort_key, reverse=True)

    # Backup the current blog_list.json if it exists
    if os.path.exists(BLOG_LIST_JSON):
        shutil.copy(BLOG_LIST_JSON, BLOG_LIST_JSON + ".bak")
        print(f"Backup created: {BLOG_LIST_JSON}.bak")

    with open(BLOG_LIST_JSON, "w", encoding="utf-8") as f:
        json.dump(final_entries, f, indent=2)
    print(f"Updated {BLOG_LIST_JSON} with {len(final_entries)} entries.")


def main():
    if not os.path.exists(BLOG_DIR):
        os.makedirs(BLOG_DIR)
    process_merged_file()
    update_blog_list()


if __name__ == "__main__":
    main()
