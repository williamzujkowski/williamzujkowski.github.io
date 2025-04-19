# Data Flow Documentation

This document describes the data flow architecture used throughout the website. It provides an overview of how data is loaded, processed, and displayed across the system.

## Data Sources

The website uses multiple data sources to populate content:

1. **Static Files**: JSON files in the `src/_data/config` directory
2. **Generated Data**: Data generated at build time via Eleventy data files
3. **External APIs**: Data from external sources (e.g., GitHub, arXiv)
4. **Local Storage**: User preferences and cached data
5. **URL Parameters**: Dynamic configuration via query parameters

## Data Flow Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Data Sources   │────▶│  Data Processing│────▶│  Templates      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                        │                       │
        │                        │                       │
        ▼                        ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Client-side JS │◀───▶│  Browser Storage│     │  Rendered HTML  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Build-time Data Processing

At build time, data flows through the following stages:

1. **Collection**: Data is gathered from various sources
2. **Transformation**: Data is normalized and transformed
3. **Validation**: Data is validated against expected schemas
4. **Integration**: Multiple data sources are combined
5. **Templating**: Data is passed to templates for rendering

### Example: Blog Post Data Flow

```
src/_data/config/blog/*.json   src/posts/*.md
           │                        │
           ▼                        ▼
      ┌─────────────────────────────────────────┐
      │           Eleventy Data Cascade         │
      └─────────────────────────────────────────┘
                          │
                          ▼
      ┌─────────────────────────────────────────┐
      │              Template Rendering         │
      └─────────────────────────────────────────┘
                          │
                          ▼
                  Generated HTML
```

## Runtime Data Flow

At runtime, client-side JavaScript interacts with data in the following ways:

1. **Initialization**: Load configuration from global variables and/or local storage
2. **User Interactions**: Capture and process user-generated data
3. **Dynamic Content**: Load additional data as needed (lazy loading)
4. **State Management**: Maintain and update component state
5. **Persistence**: Save user preferences and application state

### Example: Theme System Data Flow

```
     User Preference        System Preference
           │                       │
           ▼                       ▼
  ┌─────────────────────────────────────┐
  │          Theme Detection            │
  └─────────────────────────────────────┘
                    │
                    ▼
  ┌─────────────────────────────────────┐
  │     Theme Toggle Component          │
  └─────────────────────────────────────┘
                    │
      ┌─────────────┴──────────────┐
      │                            │
      ▼                            ▼
┌──────────────┐           ┌──────────────┐
│ DOM Updates  │           │ Local Storage│
└──────────────┘           └──────────────┘
```

## Data Types and Structures

### Core Data Structures

1. **Site Configuration**:
   ```javascript
   {
     title: "Site Title",
     description: "Site description",
     url: "https://example.com",
     author: {
       name: "Author Name",
       email: "author@example.com"
     },
     // ...
   }
   ```

2. **Blog Post**:
   ```javascript
   {
     title: "Post Title",
     date: "2025-01-01",
     tags: ["tag1", "tag2"],
     description: "Post description",
     content: "...",
     eleventyNavigation: {
       key: "post-title",
       parent: "blog"
     }
   }
   ```

3. **Theme Configuration**:
   ```javascript
   {
     themes: {
       default: {
         name: "Dark Theme",
         colors: {
           // ...
         }
       },
       light: {
         name: "Light Theme",
         colors: {
           // ...
         }
       }
     },
     defaultTheme: "default"
   }
   ```

## External Data Sources

### GitHub Data

Repository and contribution data is fetched from GitHub and cached:

1. **GitHub API calls**: Fetch repository information and contribution data
2. **Transformation**: Convert to internal data structure
3. **Cache**: Store in JSON for build-time use
4. **Static Fallback**: Include static backup data for offline/error scenarios

### arXiv Feed

Recent academic papers are fetched from arXiv:

1. **arXiv API**: Fetch papers matching configured search criteria
2. **Processing**: Extract relevant information and format
3. **Integration**: Combine with site data
4. **Rendering**: Display in templates with appropriate styling

## Data Consolidation Pattern

To simplify data management, related data is consolidated into unified files:

```
src/_data/config/
├── blog.json        # Combined blog settings and image mapping
├── homepage.json    # All homepage configuration
├── links.json       # Link collections for different categories
└── theme.json       # Theme definitions and settings
```

This pattern:
1. Reduces the number of API calls at build time
2. Simplifies imports in JavaScript
3. Improves maintenance by grouping related data
4. Ensures consistent data structures

## Client-side Data Management

### Local Storage Schema

User preferences and cache data follows this structure:

```javascript
{
  "preferred-theme": "dark", // User's theme preference
  "search-cache": {          // Cached search index
    "version": "1.0.0",
    "created": "2025-01-01T00:00:00Z",
    "data": [...]
  },
  "link-cache": {            // Recently visited links
    "expires": "2025-01-01T00:00:00Z",
    "links": [...]
  }
}
```

### State Management

Components manage their own internal state using:

1. **Module scope variables**: For simple state needs
2. **DOM data attributes**: For state visible in HTML
3. **Custom events**: For cross-component communication

## Error Handling

Data flow includes error handling at multiple levels:

1. **Validation**: Schema validation for data files
2. **Fallbacks**: Static fallback data when dynamic sources fail
3. **Default Values**: Sensible defaults when expected data is missing
4. **Cache Expiration**: Time-based cache invalidation
5. **Error Logging**: Structured error logging for debugging

## Data Security

The following measures protect sensitive data:

1. **No sensitive data in client-side code**: API keys and credentials are never included in client-side code
2. **Data validation**: Input is validated before processing
3. **Content Security Policy**: Restricts data sources to trusted origins
4. **Local Storage limits**: Only non-sensitive data is stored in browser storage

## Data Optimization

Data is optimized for performance:

1. **Minification**: JSON is minified in production
2. **Compression**: Server compression reduces transfer size
3. **Lazy Loading**: Data is loaded only when needed
4. **Incremental Updates**: Only changed data is processed during development

## Future Enhancements

Planned improvements to the data architecture:

1. **Offline Support**: Service workers for offline data access
2. **Real-time Updates**: WebSocket integration for live data
3. **Improved Caching**: More sophisticated cache invalidation
4. **GraphQL**: Consider GraphQL for more efficient data fetching
5. **Data Visualization**: Enhanced visualization of complex data sets