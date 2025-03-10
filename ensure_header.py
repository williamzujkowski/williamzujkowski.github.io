#!/usr/bin/env python3
import os
from bs4 import BeautifulSoup

# The header snippet to ensure exists in every HTML page.
REQUIRED_HEADER = '<header hx-get="/includes/header.html" hx-swap="outerHTML" hx-trigger="load"></header>'

def ensure_header_in_file(filepath):
    """Ensure the specified header snippet is present in the HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    soup = BeautifulSoup(content, 'html.parser')
    # Check if a header tag with the required hx-get attribute exists.
    existing_header = soup.find('header', attrs={'hx-get': '/includes/header.html'})
    if existing_header:
        # Header already exists; no update needed.
        return False

    # Find the <body> tag; if it exists, insert the header at the beginning.
    body = soup.body
    if body:
        new_header = BeautifulSoup(REQUIRED_HEADER, 'html.parser')
        body.insert(0, new_header)
    else:
        print(f"No <body> tag found in {filepath}, skipping.")
        return False

    # Write the updated HTML back to the file.
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return True
    except Exception as e:
        print(f"Error writing {filepath}: {e}")
        return False

def main(root_dir='.'):
    """Recursively update all HTML files in root_dir to ensure the required header exists."""
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.html'):
                filepath = os.path.join(dirpath, filename)
                if ensure_header_in_file(filepath):
                    print(f"Updated header in: {filepath}")

if __name__ == '__main__':
    main()
