# Components Documentation

This document provides details about the components used in the website, their functionality, dependencies, and usage patterns.

## Table of Contents

1. [Component Overview](#component-overview)
2. [Component Categories](#component-categories)
3. [Core Components](#core-components)
   - [Theme Toggle](#theme-toggle)
   - [Code Highlight](#code-highlight)
   - [Search](#search)
   - [Static Fallbacks](#static-fallbacks)
   - [Joke Generator](#joke-generator)
4. [Utility Components](#utility-components)
5. [Component Interactions](#component-interactions)
6. [Adding New Components](#adding-new-components)

## Component Overview

The website uses a component-based architecture to organize JavaScript functionality. Each component:

- Focuses on a specific functionality
- Manages its own initialization and lifecycle
- Is organized by priority (high, medium, low)
- Follows a consistent API pattern

## Component Categories

Components are divided into several categories based on their purpose:

1. **UI Components**: User interface elements with visual representation
2. **Functional Components**: Provide functionality without direct UI elements
3. **Layout Components**: Handle responsive design and layout adjustments
4. **Enhancement Components**: Progressive enhancements for better user experience

## Core Components

### Theme Toggle

**File**: `src/js/components/theme-toggle.js`

**Purpose**: Manages theme switching between light and dark modes.

**API**:

```javascript
import { initThemeToggle } from "./components/theme-toggle.js";

// Initialize the theme system
initThemeToggle();
```

**Features**:

- Toggles between light and dark themes
- Persists user preferences in local storage
- Respects system color scheme preferences
- Updates theme-related UI elements

**Dependencies**:

- `utils/storage.js` for local storage operations

**DOM Requirements**:

- Requires a `#theme-toggle` button in the DOM
- Applies theme classes to the root HTML element

**Usage Example**:

```html
<button id="theme-toggle" aria-label="Toggle theme">
  <!-- SVG icon here -->
</button>

<script>
  // Theme toggle will be initialized by main.js
</script>
```

### Code Highlight

**File**: `src/js/components/code-highlight.js`

**Purpose**: Enhances code blocks with syntax highlighting, line numbers, and copy functionality.

**API**:

```javascript
import { initCodeHighlight } from "./components/code-highlight.js";

// Initialize code highlighting
initCodeHighlight();
```

**Features**:

- Adds language identification to code blocks
- Inserts line numbers for better readability
- Provides copy-to-clipboard functionality
- Improves styling and accessibility

**Dependencies**:

- `utils/dom.js` for DOM manipulation utilities

**DOM Requirements**:

- Targets `<pre><code>` elements for enhancement
- Language detection via `language-*` classes

**Usage Example**:

```html
<pre><code class="language-javascript">
function example() {
  console.log("This will be enhanced");
}
</code></pre>
```

### Search

**File**: `src/js/components/search.js`

**Purpose**: Provides full-text search functionality for the website.

**API**:

```javascript
import { initSearch } from "./components/search.js";

// Initialize search functionality
initSearch();
```

**Features**:

- Indexes content for fast searching
- Provides real-time search results
- Supports keyboard navigation
- Highlights search terms in results

**Dependencies**:

- `utils/dom.js` for DOM manipulation
- `utils/storage.js` for caching search index

**DOM Requirements**:

- Requires a search input with `#search-input` ID
- Requires a results container with `#search-results` ID

**Usage Example**:

```html
<div class="search-container">
  <input type="text" id="search-input" placeholder="Search..." />
  <div id="search-results"></div>
</div>
```

### Static Fallbacks

**File**: `src/js/components/static-fallbacks.js`

**Purpose**: Provides fallback content when dynamic content cannot be loaded.

**API**:

```javascript
import { initStaticFallbacks } from "./components/static-fallbacks.js";

// Initialize static fallbacks
initStaticFallbacks();
```

**Features**:

- Detects failed content loading
- Substitutes static backup content
- Provides graceful degradation
- Logs errors for diagnostics

**Dependencies**:

- `utils/dom.js` for DOM manipulation

**DOM Requirements**:

- Looks for elements with `data-fallback` attributes

**Usage Example**:

```html
<div
  class="dynamic-content"
  data-source="/api/content"
  data-fallback="Static fallback content"
>
  Loading...
</div>
```

### Joke Generator

**File**: `src/js/components/joke-generator.js`

**Purpose**: Adds a fun element to the site with programming jokes.

**API**:

```javascript
import { initJokeGenerator } from "./components/joke-generator.js";

// Initialize joke generator
initJokeGenerator();
```

**Features**:

- Displays random programming jokes
- Allows users to request new jokes
- Stores previously seen jokes to avoid repetition

**Dependencies**:

- `utils/dom.js` for DOM manipulation
- `utils/storage.js` for tracking seen jokes

**DOM Requirements**:

- Requires a container with `#joke-container` ID
- Requires a button with `#new-joke-button` ID

**Usage Example**:

```html
<div class="joke-section">
  <div id="joke-container">
    <!-- Joke will be inserted here -->
  </div>
  <button id="new-joke-button">Get Another Joke</button>
</div>
```

## Utility Components

Beyond the core components, several utility components provide common functionality:

1. **URL Validator** (`url-validator.js`):

   - Validates external URLs for broken links
   - Provides a diagnostic report
   - Used primarily in development

2. **Analytics** (`utils/analytics.js`):

   - Tracks page views and user interactions
   - Respects user privacy settings
   - Supports multiple analytics platforms

3. **Site Configuration** (`utils/site-config.js`):
   - Loads and applies site-wide configuration
   - Handles feature flags and settings
   - Manages environment-specific configurations

## Component Interactions

Components interact through several patterns:

1. **Direct Imports**: Components can import and use functionality from other components
2. **DOM Events**: Components can communicate by dispatching and listening for events
3. **Shared State**: Some components share state through common utilities
4. **Indirect Interactions**: Components can affect the same DOM elements independently

Example of event-based communication:

```javascript
// Component A dispatches an event
document.dispatchEvent(
  new CustomEvent("theme-changed", {
    detail: { theme: "dark" },
  })
);

// Component B listens for the event
document.addEventListener("theme-changed", (event) => {
  const { theme } = event.detail;
  // Handle theme change
});
```

## Adding New Components

To add a new component:

1. Create a new file in `src/js/components/` following the naming convention
2. Follow the component pattern with an initialization function:

```javascript
/**
 * my-component.js - Description of component functionality
 *
 * This component provides [description of functionality].
 *
 * @module components/my-component
 */

import { $, $$ } from "../utils/dom.js";

/**
 * Initializes the component functionality
 *
 * @param {Object} options - Optional configuration options
 * @returns {void}
 */
export function initMyComponent(options = {}) {
  // Component initialization
  const container = $("#my-component");
  if (!container) return;

  // Setup event listeners
  container.addEventListener("click", handleClick);

  // Initialize state

  // Component-specific functions
  function handleClick(event) {
    // Handle click event
  }
}
```

3. Import and initialize the component in `main.js` at the appropriate priority level
4. Add any necessary HTML/CSS to support the component
5. Document the component in this file
