#!/usr/bin/env python3
import os
import json
from bs4 import BeautifulSoup

# Directory where individual blog post files are located
BLOG_DIR = "blog"
# Output JSON file path (at the repository root)
OUTPUT_JSON = "blog_list.json"

def extract_metadata_from_file(filepath):
    """
    Parse an HTML file and extract blog post metadata.
    Expected metadata:
      - title: from <title> tag or the first <h2> inside the article
      - date: from the data-date attribute of the inner <article> or the first <p> containing "Date:"
      - slug: from the data-slug attribute of the inner <article>; if not present, use the filename (without extension)
    """
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    
    # Try to get title from the <title> tag first
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else ""
    
    # Look for the main article element inside the <main> or <article> container.
    # We assume that the individual blog post's content is wrapped in an inner <article> element.
    article = soup.find("article")
    if article:
        # If the inner article has data attributes, use them.
        data_date = article.get("data-date", "").strip()
        data_slug = article.get("data-slug", "").strip()
        # If there's an <h2> inside the article, use that as title if not already found.
        h2 = article.find("h2")
        if h2:
            title = h2.get_text(strip=True)
        # Fallback: try to extract date from a <p> that starts with "Date:" if data-date is not present.
        if not data_date:
            p_tags = article.find_all("p")
            for p in p_tags:
                if "Date:" in p.get_text():
                    # Extract text after "Date:" (this is a simple heuristic)
                    data_date = p.get_text().split("Date:")[-1].strip()
                    break
    else:
        # If no inner article found, fallback to empty strings.
        data_date = ""
        data_slug = ""
    
    # Use the filename (without extension) as fallback slug if none was found.
    filename_slug = os.path.splitext(os.path.basename(filepath))[0]
    slug = data_slug if data_slug else filename_slug
    
    return {
        "title": title,
        "date": data_date,
        "slug": slug
    }

def generate_blog_list():
    blog_posts = []
    # Loop through all files in the BLOG_DIR
    for filename in os.listdir(BLOG_DIR):
        if filename.endswith(".html"):
            filepath = os.path.join(BLOG_DIR, filename)
            metadata = extract_metadata_from_file(filepath)
            # Only add the post if it has a title and a date.
            if metadata["title"] and metadata["date"]:
                blog_posts.append(metadata)
            else:
                print(f"Warning: Skipping {filename} due to missing title or date.")
    
    # Sort the posts by date descending (newest first)
    # Note: This sorting assumes dates in a standard format (e.g. YYYY-MM-DD)
    blog_posts.sort(key=lambda post: post["date"], reverse=True)
    
    # Write out the JSON file
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(blog_posts, f, indent=2)
    print(f"Generated {OUTPUT_JSON} with {len(blog_posts)} posts.")

if __name__ == "__main__":
    generate_blog_list()
