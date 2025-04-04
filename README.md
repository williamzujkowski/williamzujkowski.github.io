# William Zujkowski's Personal Website

This is my personal website and blog, built with [11ty](https://www.11ty.dev/), a simpler static site generator.

## Features

- Responsive design with cyberpunk/terminal theme
- Dark/light theme based on system preferences
- Blog with markdown support
- Links page for projects and resources
- Contact page
- Social media integration
- RSS feed 
- arXiv research papers feed showing latest AI/ML and cybersecurity papers

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

## arXiv Integration

The site includes an integration with arXiv to fetch and display recent AI/ML and cybersecurity research papers. The integration:

1. Fetches papers from the arXiv API (cs.AI, cs.LG, and cs.CR categories)
2. Categorizes papers by AI/ML and Cybersecurity
3. Displays the most recent paper from each category on the homepage

To update the arXiv feed:

```
npm run build:arxiv
```

## License

MIT
