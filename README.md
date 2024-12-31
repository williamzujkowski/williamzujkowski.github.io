# William Zujkowski's Personal Website

Welcome to the official repository of **William Zujkowski’s Personal Website**! This site, also known as **grenlan.com**, is a modern, lightweight static site featuring:

-   **Dynamic Navigation** and **Dynamic Footer** generation (via small JavaScript scripts).
-   A fun (and somewhat practical!) **Pizza Calculator** to determine how many pizzas to order for your team.
-   A **Coffee Calculator** to determine how many cups of coffee to prepare for your team.
-   A **Blog** section loaded from an external `blog_data.html`, with client-side sorting and filtering, and a table of contents for each blog.
-   **Mizu.js** for easy data fetching and templating, plus **Matcha CSS** for minimalist styling.

---

## Table of Contents

1.  [Project Overview](#project-overview)
2.  [Key Features](#key-features)
3.  [Setup & Usage](#setup--usage)
4.  [File Structure](#file-structure)
5.  [Customization](#customization)
6.  [Additional Notes](#additional-notes)

---

## Project Overview

This site demonstrates how to build a small, static personal site with dynamic behaviors, such as:

-   Automatically generated **Nav** and **Footer** across pages. Any update to your site’s navigation or footer is done in one place (`main.js`).
-   A **Blog** that pulls posts from an HTML file (`blog_data.html`), sorts them by date, and renders them on the fly. The `blog.html` page displays all posts, while the `index.html` page shows the most recent post and a list of older posts.
-   Fun tools like the **Pizza Calculator** and the **Coffee Calculator** to figure out how many pizzas or cups of coffee your dev team needs. These tools utilize local storage to remember user inputs.
-   Hidden “Easter Eggs,” such as a Konami code unlock and a secret message toggler.

**No database** or heavy server-side logic is required; everything is front-end driven using JavaScript.

---

## Key Features

-   **Mizu.js**: A micro-library for reactive HTML attributes like `*mizu` and `%http`. This allows fetching content from external files (like `blog_data.html`) and inserting it into the page.
-   **Matcha CSS**: A small, utility-focused CSS library that keeps the site design simple, consistent, and responsive. It is used alongside normalize.css.
-   **Dynamic Nav and Footer**: Implemented in `main.js`. The navigation bar is built from an array of pages, and the footer content includes links to the site's GitHub repository, the author's LinkedIn profile, and the author's Steam profile.
-   **Blog**: Load `blog_data.html`, parse each `<article>` (which has `data-date` and `data-slug` attributes), reorder by date descending, and display. The `index.html` page shows the latest post, while `blog.html` shows them all (with optional filtering and a dynamically generated table of contents).
-   **Pizza & Coffee Calculators**: Tools that utilize local storage for “remembering” user inputs and feature some humorous touches (Konami code, secret Easter egg, etc.). The Pizza Calculator can also generate a downloadable report and has a feature to handle "enterprise" orders. The Coffee Calculator includes similar features.

---

## Setup & Usage

1.  **Clone the Repo**

    ```bash
    gh repo clone williamzujkowski/williamzujkowski.github.io
    ```

2.  **Open `index.html`** in your browser.

    -   No build step is needed because this is a static site.
    -   If you see no content for the blog or calculators, ensure you’re either running from a local web server or your browser allows local file requests.

3.  **Navigation & Footer**

    -   Each page includes `<div id="dynamic-nav"></div>` and `<div id="dynamic-footer"></div>`.
    -   `main.js` automatically builds the nav links from a small array and appends a consistent footer across pages.

4.  **Blog**

    -   `blog_data.html` holds all your blog posts in `<article>` elements.
    -   `index.html` grabs the newest post, while `blog.html` shows them all (with an optional search box and a table of contents).

5.  **Pizza / Coffee Calculators**

    -   `pizza.html` and `coffee.html` each have forms that store user inputs in local storage.
    -   They display humorous loading bars, console logs, and final reports.

---

## File Structure

A simplified look at the main files:
```
.
├── index.html            # Main page 
├── blog.html             # Lists all blog posts, dynamic  filtering, and table of contents
├── coffee.html           # Coffee Calculator page
├── pizza.html            # Pizza Calculator page
├── main.js               # Consolidated script 
├── blog_data.html        # The blog content in HTML <article> tags
├── matcha.mizu.sh        # External link to Matcha CSS
├── mizu.sh              # External link to Mizu.js
├── simpson_profile.png   # Profile image used on index.html
├── favicon.ico           # Favicon for the website
└── README.md             # This file
```

**Note**: For any local dev server usage, place them in a typical web root or run a simple Python server:
>
> ```bash
> python -m http.server
> ```

---

## Customization

1.  **Navigation**

    -   Edit `main.js` to adjust the `pages` array if you add or remove pages.

2.  **Footer**

    -   Modify `main.js` to change or add more footer links, disclaimers, or a second row.

3.  **Blog Posts**

    -   To add a new blog entry, insert another `<article data-date="YYYY-MM-DD" data-slug="some-slug">` block in `blog_data.html`.

4.  **Site Appearance**

    -   The site uses Matcha CSS along with some custom styles in `<style>` tags within each HTML file. You can further customize the appearance by modifying these styles or creating a separate CSS file.