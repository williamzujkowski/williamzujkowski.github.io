#!/usr/bin/env python3
import os
import sys
from bs4 import BeautifulSoup

# Directory containing blog post HTML files (update if needed)
BLOG_DIR = "blog"

# htmx script to include if not already present
HTMX_SCRIPT = '<script src="https://unpkg.com/htmx.org@1.9.2"></script>'

# New header, nav, footer markup to insert
NEW_HEADER = '<header hx-get="/includes/header.html" hx-trigger="load" hx-swap="outerHTML"></header>'
NEW_NAV = (
    '<nav hx-get="/includes/nav.html" hx-trigger="load" hx-swap="outerHTML"></nav>'
)
NEW_FOOTER = '<footer hx-get="/includes/footer.html" hx-trigger="load" hx-swap="outerHTML"></footer>'


def update_blog_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # --- Update head ---
    head = soup.head
    if head:
        # Remove any script that references main.js
        for script in head.find_all("script", src=True):
            if "main.js" in script["src"]:
                script.decompose()
        # Ensure htmx script is present; if not, add it at the end of head
        htmx_present = any(
            "htmx.org" in script["src"] for script in head.find_all("script", src=True)
        )
        if not htmx_present:
            new_script = BeautifulSoup(HTMX_SCRIPT, "html.parser")
            head.append(new_script)

    # --- Update body ---
    body = soup.body
    if not body:
        print(f"Warning: No <body> found in {filepath}. Skipping.")
        return

    # Remove vestigial elements (header-placeholder, nav-placeholder, footer-placeholder)
    for vestige_id in ["header-placeholder", "nav-placeholder", "footer-placeholder"]:
        vestige = body.find(id=vestige_id)
        if vestige:
            vestige.decompose()

    # Remove any extra inline scripts that reference main.js (if any remain)
    for script in body.find_all("script"):
        if script.string and "main.js" in script.string:
            script.decompose()

    # Check if the new header/nav/footer are already present (by checking for hx-get attributes)
    header_present = body.find("header", attrs={"hx-get": "/includes/header.html"})
    nav_present = body.find("nav", attrs={"hx-get": "/includes/nav.html"})
    footer_present = body.find("footer", attrs={"hx-get": "/includes/footer.html"})

    # If header not present, insert new header and nav before main element (if main exists)
    main_el = body.find("main", class_="container")
    if main_el:
        if not header_present:
            header_tag = BeautifulSoup(NEW_HEADER, "html.parser")
            main_el.insert_before(header_tag)
        if not nav_present:
            nav_tag = BeautifulSoup(NEW_NAV, "html.parser")
            main_el.insert_before(nav_tag)
        if not footer_present:
            footer_tag = BeautifulSoup(NEW_FOOTER, "html.parser")
            main_el.insert_after(footer_tag)
    else:
        # If no main element, simply prepend header/nav and append footer
        if not header_present:
            header_tag = BeautifulSoup(NEW_HEADER, "html.parser")
            body.insert(0, header_tag)
        if not nav_present:
            nav_tag = BeautifulSoup(NEW_NAV, "html.parser")
            # Insert after header if exists; otherwise at top
            if header_present:
                header_elem = body.find(
                    "header", attrs={"hx-get": "/includes/header.html"}
                )
                header_elem.insert_after(nav_tag)
            else:
                body.insert(0, nav_tag)
        if not footer_present:
            footer_tag = BeautifulSoup(NEW_FOOTER, "html.parser")
            body.append(footer_tag)

    # Write out the updated file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(soup.prettify(formatter="html")))
    print(f"Updated {filepath}")


def main():
    # Process all .html files in the blog directory
    if not os.path.isdir(BLOG_DIR):
        print(f"Error: Directory {BLOG_DIR} does not exist.")
        sys.exit(1)
    for filename in os.listdir(BLOG_DIR):
        if filename.lower().endswith(".html"):
            filepath = os.path.join(BLOG_DIR, filename)
            update_blog_file(filepath)


if __name__ == "__main__":
    main()
