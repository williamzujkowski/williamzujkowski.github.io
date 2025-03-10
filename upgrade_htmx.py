#!/usr/bin/env python3
import os

# Define the old and new htmx URLs
OLD_HTMX = "https://unpkg.com/htmx.org@1.9.2"
NEW_HTMX = "https://unpkg.com/htmx.org@2.0.4"

def update_htmx_in_file(filepath):
    """Open a file, replace old htmx URL with the new one, and write back if changes occur."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    if OLD_HTMX not in content:
        return

    new_content = content.replace(OLD_HTMX, NEW_HTMX)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated: {filepath}")
    except Exception as e:
        print(f"Error writing {filepath}: {e}")

def main(root_dir="."):
    """Recursively walk through the directory tree and update all HTML files."""
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(".html"):
                filepath = os.path.join(dirpath, filename)
                update_htmx_in_file(filepath)

if __name__ == "__main__":
    main()
