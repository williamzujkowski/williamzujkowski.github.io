Below is a sample **README.md** you can place in your GitHub repository for this website. Feel free to modify any sections to better fit your needs:

```markdown
# William Zujkowski's Personal Website

Welcome to the official repository of **William Zujkowski’s Personal Website**! This is a modern, lightweight static site featuring:

- **Dynamic Navigation** and **Dynamic Footer** generation (via small JavaScript scripts).
- A **Pizza Calculator** and **Coffee Calculator** for fun (and somewhat practical!) dev team usage.
- A **Blog** section loaded from external `blog_data.html`, with client-side sorting and filtering.
- **Mizu.js** for easy data fetching and templating, plus **Matcha CSS** for minimalist styling.

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Key Features](#key-features)  
3. [Setup & Usage](#setup--usage)  
4. [File Structure](#file-structure)  
5. [Customization](#customization)  
6. [Additional Notes](#additional-notes)

---

## Project Overview

This site demonstrates how to build a small, static personal site with dynamic behaviors, such as:

- Automatically generated **Nav** and **Footer** across pages, so any update to your site’s navigation or footer is done in one place.
- A **Blog** that pulls posts from an HTML file (`blog_data.html`), sorts them by date, and renders them on the fly.
- Fun tools like the **Pizza Calculator** and **Coffee Calculator** to figure out how many pizzas or cups of coffee your dev team needs.
- Hidden “Easter Eggs,” such as a Konami code unlock and a secret message toggler.

**No database** or heavy server-side logic is required; everything is front-end driven.

---

## Key Features

- **Mizu.js**: A micro library for reactive HTML attributes like `*mizu` and `%http`, letting us fetch content from external files (like `blog_data.html`) and insert it into the page.
- **Matcha CSS**: A small, utility-focused CSS library that keeps the site design simple, consistent, and responsive.
- **Dynamic Nav and Footer**: Implemented in `nav_gen.js` and `footer_gen.js`, so we can keep a single source of truth for navigation links and footer content.  
- **Blog**: Load `blog_data.html`, parse each `<article>` (which has a `data-date` attribute), reorder by date descending, and display.
- **Pizza & Coffee Calculators**: Tools that utilize local storage for “remembering” user inputs and feature some humorous touches (Konami code, secret Easter egg, etc.).

---

## Setup & Usage

1. **Clone the Repo**  
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   ```
2. **Open `index.html`** in your browser.  
   - No build step is needed because this is a static site.  
   - If you see no content for the blog or calculators, ensure you’re either running from a local web server or your browser allows local file requests.
3. **Navigation & Footer**  
   - Each page includes `<div id="dynamic-nav"></div>` and `<div id="dynamic-footer"></div>`.  
   - `nav_gen.js` automatically builds the nav links from a small array.  
   - `footer_gen.js` appends a consistent footer across pages.
4. **Blog**  
   - `blog_data.html` holds all your blog posts in `<article>` elements.  
   - `index.html` grabs the newest post, while `blog.html` shows them all (with an optional search box).
5. **Pizza / Coffee Calculators**  
   - `pizza.html` and `coffee.html` each have forms that store user inputs in local storage.  
   - They display comedic loading bars, console logs, and final reports.

---

## File Structure

A simplified look at the main files:

```
.
├── index.html            # Main page with dynamic nav/footer placeholders
├── blog.html             # Lists all blog posts, dynamic filtering
├── coffee.html           # Coffee Calculator
├── pizza.html            # Pizza Calculator
├── nav_gen.js            # Script that builds the <nav> dynamically
├── footer_gen.js         # Script that builds the <footer> dynamically
├── coffee_calc.js        # Logic for coffee calculator
├── pizza_calc.js         # Logic for pizza calculator
├── blog_data.html        # The blog content in HTML <article> tags
├── matcha.mizu.sh        # External link to Matcha CSS
├── mizu.sh               # External link to Mizu.js
└── README.md             # This file
```

> _Note_: The actual structure can differ. For any local dev server usage, place them in a typical web root or run a simple Python server:  
> ```bash
> python -m http.server
> ```

---

## Customization

1. **Navigation**  
   - Edit `nav_gen.js` to adjust the `pages` array if you add or remove pages.  
2. **Footer**  
   - Modify `footer_gen.js` to change or add more footer links, disclaimers, or a second row.  
3. **Blog Posts**  
   - To add a new blog entry, just insert another `<article data-date="YYYY-MM-DD" data-slug="some-slug">` block in `blog_data.html`.  
4. **Site Appearance**  
   - You can create a custom `.css` file or keep it all in `<style>` blocks. If you want to minify or bundle it, you can do so with a build tool.

---
