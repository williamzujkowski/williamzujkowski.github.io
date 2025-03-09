#!/usr/bin/env python3
import os
import re
import json
from bs4 import BeautifulSoup

# Configuration – adjust these paths if needed
INPUT_FILE = "merged_blog_posts.html"  # File containing all blog posts
BLOG_DIR = "blog"                      # Directory to save individual blog posts
BLOG_LIST_JSON = "blog_list.json"      # JSON file to store the blog list

def process_blog_posts():
    # Read the merged blog posts file
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Split the content into individual posts.
    # We assume each post begins with "<!DOCTYPE html>"
    posts_raw = re.split(r"(?=<!DOCTYPE html>)", content)
    blog_entries = []

    for post in posts_raw:
        post = post.strip()
        if not post:
            continue

        # Ensure the post starts with DOCTYPE (in case split removed it)
        if not post.startswith("<!DOCTYPE html>"):
            post = "<!DOCTYPE html>\n" + post

        # Parse the post with BeautifulSoup
        soup = BeautifulSoup(post, "html.parser")

        # Extract the title from the <title> tag
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else "Untitled"

        # Find the date and slug from the first <em> inside a <p>
        em_tag = None
        first_p = soup.find("p")
        if first_p:
            em_tag = first_p.find("em")
        if em_tag:
            em_text = em_tag.get_text(strip=True)
            # Expected format: "YYYY-MM-DD | slug"
            parts = [p.strip() for p in em_text.split("|")]
            if len(parts) >= 2:
                date = parts[0]
                slug = parts[1]
            else:
                date = "unknown"
                slug = "unknown"
        else:
            date = "unknown"
            slug = "unknown"

        # Define the output filename using the slug
        output_filename = os.path.join(BLOG_DIR, slug + ".html")
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(post)
        print(f"Processed blog post: {title} ({date}, slug: {slug})")

        # Append the entry to our blog list
        blog_entries.append({
            "title": title,
            "date": date,
            "slug": slug
        })

    # Sort the blog entries by date descending (assuming format YYYY-MM-DD)
    blog_entries.sort(key=lambda x: x["date"], reverse=True)

    # Write out the updated blog_list.json file
    with open(BLOG_LIST_JSON, "w", encoding="utf-8") as f:
        json.dump(blog_entries, f, indent=2)
    print(f"Updated blog list in {BLOG_LIST_JSON}")

def main():
    # Ensure the blog directory exists
    if not os.path.exists(BLOG_DIR):
        os.makedirs(BLOG_DIR)
    process_blog_posts()

if __name__ == "__main__":
    main()
