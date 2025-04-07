# William Zujkowski's Personal Website

This is my personal website and blog, built with [11ty](https://www.11ty.dev/), a simpler static site generator. The site features a GitHub-style dark theme with responsive design, blog functionality, and dynamic content integration.

## Features

- GitHub-style dark theme with responsive design
- Blog with markdown support and tag filtering
- Configurable homepage with customizable sections
- Links page with categorized resources in a grid layout
- Rich link previews with metadata and screenshots using Microlink
- GitHub repository pinning and showcase
- arXiv research papers feed showing latest AI/ML and cybersecurity papers
- Social media integration
- RSS feed

## Development

To work on this site locally:

1. Clone the repository
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`
4. Visit `http://localhost:8080` in your browser

## Build

To build the site for production:

```
npm run build
```

The built site will be in the `_site` directory.

## Site Configuration

The majority of site configuration is managed through JSON files in the `src/_data` directory.

### Main Configuration (site.json)

The `site.json` file contains the primary configuration for the website:

```json
{
  "title": "Your Name",
  "description": "Personal website and technology blog",
  "url": "https://yourdomain.com",
  "author": "Your Name",
  "email": "your.email@example.com",
  "theme": "system",
  "seo": { ... },
  "homepage": { ... },
  "social_media": [ ... ],
  "navigation": [ ... ],
  "linkGroups": [ ... ],
  "links": [ ... ],
  "blog": { ... }
}
```

### Homepage Configuration

The homepage is highly customizable through the `homepage` section in `site.json`:

```json
"homepage": {
  "welcome_heading": "Welcome",
  "welcome_subtitle": "IT Engineer & Technology Enthusiast",
  "about_me_title": "About Me",
  "about_me_content": "Your bio text here...",
  "show_recent_posts": true,
  "recent_posts_count": 3,
  "show_activity_timeline": false,
  "show_github_pins": true,
  "show_github_repos_on_links": false,
  "show_arxiv_papers": true,
  "pinned_repositories": [ ... ],
  "skills": [ ... ],
  "interests": "Your interests text here..."
}
```

Toggle features on/off by changing the boolean values:
- `show_recent_posts`: Display recent blog posts
- `show_activity_timeline`: Show the blog post activity timeline
- `show_github_pins`: Display pinned GitHub repositories on homepage
- `show_github_repos_on_links`: Display GitHub repositories on links page
- `show_arxiv_papers`: Show the arXiv papers section

### Navigation

Site navigation is configured in the `navigation` array:

```json
"navigation": [
  { "name": "Home", "url": "/", "icon": "" },
  { "name": "Links", "url": "/links/", "icon": "" },
  { "name": "Blog", "url": "/blog/", "icon": "" }
]
```

Add, remove, or modify navigation items by editing this array.

### Social Media Links

Social media profiles are configured in the `social_media` array:

```json
"social_media": [
  {
    "name": "GitHub",
    "url": "https://github.com/yourusername",
    "icon": "<svg>...</svg>",
    "enabled": true,
    "display_on_home": false,
    "display_in_header": true,
    "display_in_footer": true
  },
  // Additional social profiles...
]
```

For each social profile, you can control:
- `enabled`: Whether the profile is active
- `display_on_home`: Show on homepage
- `display_in_header`: Show in site header
- `display_in_footer`: Show in site footer

### Links Page

The links page is organized by categories defined in `linkGroups` and populated from the `links` array:

```json
"linkGroups": [
  { "name": "Social", "icon": "🔗" },
  { "name": "Projects", "icon": "💻" },
  // Additional categories...
],
"links": [
  { 
    "name": "GitHub", 
    "url": "https://github.com/yourusername", 
    "group": "Social", 
    "icon": "GitHub" 
  },
  // Additional links...
]
```

Each link must have a `group` that corresponds to one of the defined `linkGroups`.

### Blog Configuration

Blog settings are managed in the `blog` section:

```json
"blog": {
  "postsPerPage": 5,
  "showDates": true,
  "dateFormat": "%B %d, %Y"
}
```

## Content Management

### Blog Posts

Blog posts are markdown files stored in the `src/posts` directory. Each post should include front matter at the top:

```markdown
---
title: Your Post Title
date: 2024-07-15
description: A brief description of your post
tags: ['tag1', 'tag2']
image: /assets/images/blog/your-post-image.jpg
---

Your post content here...
```

Required front matter:
- `title`: The post title
- `date`: Publication date (YYYY-MM-DD format)

Optional front matter:
- `description`: Brief summary of the post
- `tags`: Array of relevant tags
- `image`: Featured image path

### Adding Images

Store images in the `assets/images` directory:
- Blog post images: `assets/images/blog/`
- General site images: `assets/images/`

## GitHub Pins

To update the GitHub repository pins, edit the `homepage.pinned_repositories` array in `site.json` or run:

```
npm run build:github-pins
```

This fetches public repository information for the specified GitHub username.

## arXiv Integration

The site includes an integration with arXiv to fetch and display recent AI/ML and cybersecurity research papers. The integration:

1. Fetches papers from the arXiv API (cs.AI, cs.LG, and cs.CR categories)
2. Categorizes papers by AI/ML and Cybersecurity
3. Displays the most recent paper from each category on the homepage

To update the arXiv feed:

```
npm run build:arxiv
```

## Styling

The site uses Tailwind CSS for styling. Main CSS files:
- `src/css/styles.css`: Main stylesheet
- `tailwind.config.cjs`: Tailwind configuration

## Deployment

The site is configured for GitHub Pages deployment. When you push to the repository, GitHub Actions will automatically build and deploy the site.

## Microlink Integration

The site uses Microlink's open source tools to enhance link previews:

- During the build process, `build-link-previews.js` generates screenshots and extracts metadata for all external links
- This data is stored as JSON and used by the frontend to display rich link previews
- The validation script `validate-links.js` can be run periodically to check link health
- In case pre-generated data is unavailable, the site falls back to using the Microlink API in real-time

To generate or update link previews:

```
npm run build:links
```

To validate links and check for broken URLs:

```
npm run validate:links
```

The tooling uses:
- `metascraper` for metadata extraction
- `puppeteer` and `@browserless/goto` for screenshot generation
- Microlink's API as a fallback for real-time preview generation

## License

MIT
