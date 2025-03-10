#!/usr/bin/env python3
import os
import re
import json
import shutil
from datetime import datetime
from bs4 import BeautifulSoup

# Configuration – adjust these paths if needed
MERGED_FILE = "merged_blog_posts.html"  # File with new blog posts to split (if present)
BLOG_DIR = "blog"  # Directory to store individual blog post files
BLOG_LIST_JSON = "blog_list.json"  # JSON file listing all blog posts

# New header, nav, footer markup (using htmx)
NEW_HEADER = '<header hx-get="/includes/header.html" hx-trigger="load" hx-swap="outerHTML"></header>'
NEW_NAV = (
    '<nav hx-get="/includes/nav.html" hx-trigger="load" hx-swap="outerHTML"></nav>'
)
NEW_FOOTER = '<footer hx-get="/includes/footer.html" hx-trigger="load" hx-swap="outerHTML"></footer>'

# Regex to convert markdown hyperlinks [text](url) to HTML links.
MD_LINK_REGEX = re.compile(r"\[([^\]]+)\]\(([^\)]+)\)")


def convert_markdown_links(text):
    """Convert markdown hyperlinks [text](url) to HTML <a> tags."""
    return MD_LINK_REGEX.sub(r'<a href="\2">\1</a>', text)


def slugify(text):
    """Generate a slug from text: lower-case, dashes for spaces, remove non-alphanumerics."""
    text = text.lower().strip()
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"[^a-z0-9\-]", "", text)
    return text


def validate_date(date_str):
    """Return date_str if it's in YYYY-MM-DD format, else 'unknown'."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        return "unknown"


def extract_metadata(soup):
    """
    Extract title, date, and slug from the BeautifulSoup object.
    Fallbacks:
      - If <title> is missing or equals "{title}", use the first <h2> in the inner article.
      - Clean up the title by collapsing whitespace.
      - For date and slug, first try to extract from the first <em> in the first <p>.
      - If that fails, search for a <p> containing "Date:" and extract the date from it.
      - If slug is missing or equals "unknown", generate one from the title.
    """
    # Title extraction and cleanup
    title = ""
    title_tag = soup.find("title")
    if title_tag:
        title = title_tag.get_text(strip=True)
    title = " ".join(title.split())
    if not title or title == "{title}":
        inner_article = soup.find("article")
        if inner_article:
            h2 = inner_article.find("h2")
            if h2:
                title = " ".join(h2.get_text(strip=True).split())
    if not title:
        title = "Untitled"

    # Date and slug extraction from first <em> in the first <p>
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
    # If still missing date or slug, try the inner article attributes
    inner_article = soup.find("article")
    if inner_article:
        if inner_article.has_attr("data-date"):
            date = validate_date(inner_article["data-date"])
        if inner_article.has_attr("data-slug"):
            slug = inner_article["data-slug"]

    # As a fallback for date, search for any <p> that contains "Date:" (if still unknown)
    if date == "unknown":
        p_tags = soup.find_all("p")
        for p in p_tags:
            if "Date:" in p.get_text():
                text = p.get_text()
                # Extract text after "Date:" and remove extra whitespace
                potential_date = text.split("Date:")[-1].strip().split()[0]
                date = validate_date(potential_date)
                if date != "unknown":
                    break

    # If slug is still missing or equals "unknown", generate from title
    if not slug or slug == "unknown":
        slug = slugify(title)

    return title, date, slug


def process_merged_file():
    """
    Process the merged HTML file (if it exists):
      - Split it into individual blog posts.
      - Convert markdown hyperlinks to HTML.
      - Remove vestigial header/nav/footer placeholders and old scripts.
      - Insert the new header, nav, and footer (which load via htmx).
      - Extract metadata (title, date, slug) from each post.
      - Save each post as an individual file in BLOG_DIR.
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

        # Convert markdown hyperlinks to HTML
        post = convert_markdown_links(post)
        soup = BeautifulSoup(post, "html.parser")

        # Remove vestigial placeholders and old script references
        for vestige_id in [
            "header-placeholder",
            "nav-placeholder",
            "footer-placeholder",
        ]:
            for vestige in soup.find_all(id=vestige_id):
                vestige.decompose()
        for script in soup.find_all("script", src=True):
            if "main.js" in script["src"]:
                script.decompose()

        # Insert new header, nav, and footer if not already present
        body = soup.body
        if body:
            if not body.find("header", attrs={"hx-get": "/includes/header.html"}):
                new_header = BeautifulSoup(NEW_HEADER, "html.parser")
                body.insert(0, new_header)
            if not body.find("nav", attrs={"hx-get": "/includes/nav.html"}):
                new_nav = BeautifulSoup(NEW_NAV, "html.parser")
                header_elem = body.find(
                    "header", attrs={"hx-get": "/includes/header.html"}
                )
                if header_elem:
                    header_elem.insert_after(new_nav)
                else:
                    body.insert(0, new_nav)
            if not body.find("footer", attrs={"hx-get": "/includes/footer.html"}):
                new_footer = BeautifulSoup(NEW_FOOTER, "html.parser")
                body.append(new_footer)

        # Extract metadata
        title, date, slug = extract_metadata(soup)
        output_filename = os.path.join(BLOG_DIR, slug + ".html")
        with open(output_filename, "w", encoding="utf-8") as out_f:
            out_f.write(soup.prettify(formatter="html"))
        print(f"Processed post: '{title}' | Date: {date} | Slug: '{slug}'")


def update_blog_list():
    """
    Scan all .html files in BLOG_DIR and update BLOG_LIST_JSON.
    Deduplicate entries based on slug and sort them by date (descending).
    Create a backup of the existing BLOG_LIST_JSON if it exists.
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

    # Sort entries by date descending (if date is valid; else treat as very old)
    def sort_key(entry):
        try:
            return datetime.strptime(entry["date"], "%Y-%m-%d")
        except Exception:
            return datetime.min

    final_entries.sort(key=sort_key, reverse=True)

    # Backup current BLOG_LIST_JSON if exists
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
