#!/usr/bin/env python3
"""
Convert HTML blog posts to Hugo-compatible Markdown page bundles.

Usage:
    python convert_html_to_hugo.py -i source -o content/post [--author "Your Name"] [--categories "cat1,cat2"] [--tags "tag1,tag2"] [--verbose] [--dry-run]

Requirements:
    pip install beautifulsoup4 html2text
"""

import os
import re
import argparse
from bs4 import BeautifulSoup
import html2text
from datetime import datetime

def slugify(value):
    """Convert a string to a URL-friendly slug."""
    value = value.lower().strip()
    value = re.sub(r'[^a-z0-9]+', '-', value)
    value = re.sub(r'-+', '-', value)
    return value.strip('-')

def extract_cover_image(article):
    """
    Look for a cover image in the article.
    If found, remove it from the article so it isn’t duplicated in the body.
    Returns the src attribute if an image is found, otherwise None.
    """
    img_tag = article.find('img')
    if img_tag and img_tag.get('src'):
        src = img_tag['src']
        img_tag.decompose()  # remove image from content
        return src.strip()
    return None

def convert_html_to_markdown(html_content, input_filepath, extra_front_matter):
    """
    Convert HTML content into Hugo-compatible Markdown with YAML front matter.
    
    Process:
      - Parse HTML using BeautifulSoup.
      - Look for an inner <article> element with a data-date attribute.
      - Extract title from the first <h2> (or fallback to <title> from head).
      - Get the date from the data-date attribute (fallback to a paragraph or today's date).
      - Determine the slug from data-slug attribute or generate one from the title.
      - Use the first paragraph as a brief description.
      - Optionally detect a cover image.
      - Convert the remaining HTML to Markdown using html2text.
      - Construct YAML front matter including extra keys (author, categories, tags) if provided.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    # Try to find the inner article with a data-date attribute
    article = soup.find('article', attrs={'data-date': True})
    if article is None:
        if verbose:
            print(f"Warning: No <article> with data-date found in '{input_filepath}'. Using entire content.")
        article = soup

    # Extract title from the first <h2>
    title_tag = article.find('h2')
    if title_tag:
        title = title_tag.get_text(strip=True)
        title_tag.extract()  # remove the title so it's not duplicated
    else:
        # Fallback: use <title> from head if available, else use filename
        head_title = soup.find('title')
        title = head_title.get_text(strip=True) if head_title else os.path.splitext(os.path.basename(input_filepath))[0]

    # Escape any double quotes in title for YAML
    title = title.replace('"', '\\"')

    # Get date from data-date attribute; if missing, try to parse a paragraph or use today's date.
    date = article.get('data-date')
    if not date:
        date_paragraph = article.find('p')
        if date_paragraph and "Date:" in date_paragraph.get_text():
            date = date_paragraph.get_text().split("Date:")[-1].strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Get slug from data-slug attribute; if missing, generate from title.
    slug = article.get('data-slug')
    if not slug:
        slug = slugify(title)
    else:
        slug = slugify(slug)

    # Use the first paragraph as a description if available
    first_paragraph = article.find('p')
    description = first_paragraph.get_text(strip=True) if first_paragraph else ""
    description = description.replace('"', '\\"')

    # Optionally extract a cover image (first <img> in the article)
    cover_image = extract_cover_image(article)

    # Convert remaining article HTML to Markdown
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = False
    markdown_body = converter.handle(str(article)).strip()

    # Build YAML front matter
    front_matter_lines = [
        "---",
        f'title: "{title}"',
        f"date: {date}",
        f'slug: "{slug}"',
        f'description: "{description}"',
        'layout: "post"',
        "draft: false"
    ]
    if cover_image:
        front_matter_lines.append(f'image: "{cover_image}"')
    # Add extra front matter if provided
    for key, value in extra_front_matter.items():
        if value:  # Only add if not empty
            # For comma-separated lists, convert to YAML list format
            if key in ['categories', 'tags']:
                items = [item.strip() for item in value.split(',') if item.strip()]
                if items:
                    front_matter_lines.append(f'{key}:')
                    for item in items:
                        front_matter_lines.append(f'  - "{item}"')
            else:
                front_matter_lines.append(f'{key}: "{value}"')
    front_matter_lines.append("---\n")
    front_matter = "\n".join(front_matter_lines)

    output_markdown = front_matter + markdown_body
    return title, date, slug, output_markdown

def process_file(input_filepath, output_dir, extra_front_matter, dry_run=False):
    """
    Read an HTML file, convert its content, and write the output Markdown
    to a Hugo page bundle (a folder named by the slug with an index.md file).
    """
    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"Error reading {input_filepath}: {e}")
        return False

    title, date, slug, markdown_content = convert_html_to_markdown(html_content, input_filepath, extra_front_matter)

    # Create folder for post in the output directory
    post_folder = os.path.join(output_dir, slug)
    if not dry_run:
        os.makedirs(post_folder, exist_ok=True)
        output_filepath = os.path.join(post_folder, "index.md")
        try:
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            if verbose:
                print(f"Converted '{input_filepath}' -> '{output_filepath}'")
        except Exception as e:
            print(f"Error writing {output_filepath}: {e}")
            return False
    else:
        if verbose:
            print(f"[Dry-run] Would convert '{input_filepath}' into folder '{post_folder}'")
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Recursively convert HTML blog posts into Hugo page bundles with enhanced front matter."
    )
    parser.add_argument("-i", "--input", default="source", 
                        help="Input directory containing HTML files (default: source)")
    parser.add_argument("-o", "--output", default="content/post", 
                        help="Output directory for Markdown posts (default: content/post)")
    parser.add_argument("--author", default="", help="Author name to add to front matter")
    parser.add_argument("--categories", default="", help="Comma-separated list of categories")
    parser.add_argument("--tags", default="", help="Comma-separated list of tags")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--dry-run", action="store_true", help="Run without writing files")
    args = parser.parse_args()

    global verbose
    verbose = args.verbose

    input_dir = args.input
    output_dir = args.output

    # Extra front matter parameters to be added
    extra_front_matter = {
        "author": args.author,
        "categories": args.categories,
        "tags": args.tags
    }

    if verbose:
        print(f"Processing HTML files from '{input_dir}' to output directory '{output_dir}'.")
        if args.dry_run:
            print("Dry-run mode enabled: no files will be written.")
        if extra_front_matter["author"]:
            print(f"Author: {extra_front_matter['author']}")
        if extra_front_matter["categories"]:
            print(f"Categories: {extra_front_matter['categories']}")
        if extra_front_matter["tags"]:
            print(f"Tags: {extra_front_matter['tags']}")

    # Ensure output directory exists (unless dry-run)
    if not args.dry_run:
        os.makedirs(output_dir, exist_ok=True)

    processed_count = 0
    error_count = 0

    # Walk through input directory to process .html files
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".html"):
                input_filepath = os.path.join(root, file)
                if process_file(input_filepath, output_dir, extra_front_matter, dry_run=args.dry_run):
                    processed_count += 1
                else:
                    error_count += 1

    print("\nConversion complete!")
    print(f"Processed {processed_count} file(s).")
    if error_count:
        print(f"{error_count} file(s) encountered errors.")

if __name__ == "__main__":
    main()
