/**
 * Example Interactions for williamzujkowski.github.io
 *
 * This module provides example responses and interactions to guide
 * LLM agents in understanding expected behavior and output formats.
 */

/**
 * Example responses for different types of requests
 */
export const exampleResponses = {
  /**
   * Example: Creating a new blog post
   */
  createBlogPost: {
    request: "Create a blog post about implementing rate limiting in Node.js APIs",
    response: `---
title: "Implementing Rate Limiting in Node.js APIs: A Comprehensive Guide"
date: 2024-01-15
tags: ["nodejs", "api", "security", "performance"]
excerpt: "Learn how to protect your Node.js APIs from abuse with effective rate limiting strategies"
topic: "api-security"
readingTime: "8 min read"
---

# Implementing Rate Limiting in Node.js APIs: A Comprehensive Guide

Rate limiting is a crucial security and performance feature for any production API. It prevents abuse, ensures fair resource usage, and protects your servers from being overwhelmed. In this guide, we'll explore different rate limiting strategies and implement them in Node.js.

## Why Rate Limiting Matters

Before diving into implementation, let's understand why rate limiting is essential:

1. **Prevents DoS attacks**: Limits the impact of malicious traffic
2. **Ensures fair usage**: Prevents single users from monopolizing resources
3. **Reduces server load**: Maintains performance for all users
4. **Controls costs**: Especially important for APIs that consume paid resources

## Basic Rate Limiting with Express

Let's start with a simple implementation using the popular \`express-rate-limit\` package:

\`\`\`javascript
const express = require('express');
const rateLimit = require('express-rate-limit');

const app = express();

// Create a limiter: 100 requests per 15 minutes
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.',
  standardHeaders: true, // Return rate limit info in headers
  legacyHeaders: false, // Disable X-RateLimit-* headers
});

// Apply rate limiting to all requests
app.use(limiter);

// API routes
app.get('/api/data', (req, res) => {
  res.json({ message: 'Data retrieved successfully' });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
\`\`\`

## Advanced Strategies

### Token Bucket Algorithm

For more sophisticated rate limiting, implement a token bucket algorithm:

\`\`\`javascript
class TokenBucket {
  constructor(capacity, refillRate) {
    this.capacity = capacity;
    this.tokens = capacity;
    this.refillRate = refillRate;
    this.lastRefill = Date.now();
  }

  consume(tokens = 1) {
    this.refill();

    if (this.tokens >= tokens) {
      this.tokens -= tokens;
      return true;
    }

    return false;
  }

  refill() {
    const now = Date.now();
    const timePassed = (now - this.lastRefill) / 1000;
    const tokensToAdd = timePassed * this.refillRate;

    this.tokens = Math.min(this.capacity, this.tokens + tokensToAdd);
    this.lastRefill = now;
  }
}

// Usage with Express middleware
const buckets = new Map();

function tokenBucketLimiter(capacity, refillRate) {
  return (req, res, next) => {
    const key = req.ip;

    if (!buckets.has(key)) {
      buckets.set(key, new TokenBucket(capacity, refillRate));
    }

    const bucket = buckets.get(key);

    if (bucket.consume()) {
      next();
    } else {
      res.status(429).json({
        error: 'Rate limit exceeded',
        retryAfter: Math.ceil((1 - bucket.tokens) / bucket.refillRate)
      });
    }
  };
}

app.use('/api', tokenBucketLimiter(10, 1)); // 10 tokens, 1 per second
\`\`\`

### Redis-Based Distributed Rate Limiting

For distributed systems, use Redis:

\`\`\`javascript
const Redis = require('ioredis');
const redis = new Redis();

async function redisRateLimiter(key, limit, window) {
  const current = await redis.incr(key);

  if (current === 1) {
    await redis.expire(key, window);
  }

  return current <= limit;
}

// Middleware
function createRedisLimiter(limit, window) {
  return async (req, res, next) => {
    const key = \`rate_limit:\${req.ip}:\${Date.now() / (window * 1000) | 0}\`;

    try {
      const allowed = await redisRateLimiter(key, limit, window);

      if (allowed) {
        next();
      } else {
        res.status(429).json({ error: 'Rate limit exceeded' });
      }
    } catch (error) {
      console.error('Redis error:', error);
      next(); // Fail open
    }
  };
}
\`\`\`

## Best Practices

1. **Use appropriate time windows**: Balance between security and user experience
2. **Implement different limits**: Vary limits based on endpoint sensitivity
3. **Provide clear feedback**: Include retry-after headers and informative messages
4. **Consider user tiers**: Implement different limits for authenticated users
5. **Monitor and adjust**: Track rate limit hits and adjust thresholds accordingly

## Conclusion

Rate limiting is essential for building robust APIs. Start with simple solutions and evolve based on your needs. Remember to balance security with user experience, and always provide clear feedback when limits are reached.

The implementations shown here provide a solid foundation, but consider your specific requirements and scale when choosing a strategy. For high-traffic applications, distributed solutions with Redis or dedicated rate limiting services might be more appropriate.`,
  },

  /**
   * Example: Refactoring code
   */
  refactorCode: {
    request: "Refactor this function to be more testable and maintainable",
    originalCode: `
function processUserData(userId) {
  const user = db.query('SELECT * FROM users WHERE id = ' + userId);
  if (user) {
    const age = new Date().getFullYear() - new Date(user.birthdate).getFullYear();
    if (age >= 18) {
      sendEmail(user.email, 'Welcome!');
      return { success: true, message: 'User processed' };
    }
  }
  return { success: false, message: 'Processing failed' };
}`,
    refactoredCode: `
/**
 * Processes user data with age verification
 * @param {Object} dependencies - Injected dependencies
 * @param {Function} dependencies.getUserById - Function to fetch user
 * @param {Function} dependencies.calculateAge - Function to calculate age
 * @param {Function} dependencies.sendEmail - Function to send emails
 * @param {string} userId - The user's ID
 * @returns {Promise<{success: boolean, message: string}>}
 */
async function processUserData({ getUserById, calculateAge, sendEmail }, userId) {
  try {
    // Validate input
    if (!userId || typeof userId !== 'string') {
      throw new TypeError('Invalid userId');
    }

    // Fetch user with proper parameterization
    const user = await getUserById(userId);

    if (!user) {
      return {
        success: false,
        message: 'User not found'
      };
    }

    // Calculate age using injected function
    const age = calculateAge(user.birthdate);

    if (age < 18) {
      return {
        success: false,
        message: 'User must be 18 or older'
      };
    }

    // Send welcome email
    await sendEmail(user.email, 'Welcome!', {
      name: user.name,
      userId: user.id
    });

    return {
      success: true,
      message: 'User processed successfully'
    };
  } catch (error) {
    console.error('Error processing user:', error);

    return {
      success: false,
      message: error.message || 'Processing failed'
    };
  }
}

// Helper functions (testable separately)
export function calculateAge(birthdate) {
  const today = new Date();
  const birth = new Date(birthdate);
  let age = today.getFullYear() - birth.getFullYear();
  const monthDiff = today.getMonth() - birth.getMonth();

  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--;
  }

  return age;
}

// Usage example
const dependencies = {
  getUserById: async (id) => await db.users.findById(id),
  calculateAge,
  sendEmail: emailService.send
};

const result = await processUserData(dependencies, userId);`,
  },

  /**
   * Example: Creating a component
   */
  createComponent: {
    request: "Create a search autocomplete component",
    response: {
      javascript: `
/**
 * Search Autocomplete Component
 * Provides real-time search suggestions with accessibility support
 */
export class SearchAutocomplete {
  constructor(element, options = {}) {
    this.element = element;
    this.input = element.querySelector('input[type="search"]');
    this.resultsContainer = element.querySelector('[role="listbox"]');

    this.options = {
      minChars: 2,
      debounceMs: 300,
      maxResults: 10,
      searchEndpoint: '/api/search',
      ...options
    };

    this.selectedIndex = -1;
    this.results = [];
    this.debounceTimer = null;

    this.init();
  }

  init() {
    if (!this.input || !this.resultsContainer) {
      console.error('SearchAutocomplete: Required elements not found');
      return;
    }

    this.bindEvents();
    this.setupAccessibility();
  }

  bindEvents() {
    this.input.addEventListener('input', this.handleInput.bind(this));
    this.input.addEventListener('keydown', this.handleKeydown.bind(this));
    this.input.addEventListener('blur', this.handleBlur.bind(this));

    this.resultsContainer.addEventListener('click', this.handleResultClick.bind(this));
  }

  setupAccessibility() {
    this.input.setAttribute('role', 'combobox');
    this.input.setAttribute('aria-autocomplete', 'list');
    this.input.setAttribute('aria-expanded', 'false');
    this.input.setAttribute('aria-controls', this.resultsContainer.id);

    this.resultsContainer.setAttribute('role', 'listbox');
  }

  handleInput(event) {
    const query = event.target.value.trim();

    clearTimeout(this.debounceTimer);

    if (query.length < this.options.minChars) {
      this.hideResults();
      return;
    }

    this.debounceTimer = setTimeout(() => {
      this.search(query);
    }, this.options.debounceMs);
  }

  async search(query) {
    try {
      this.showLoading();

      const response = await fetch(\`\${this.options.searchEndpoint}?q=\${encodeURIComponent(query)}\`);

      if (!response.ok) {
        throw new Error(\`Search failed: \${response.status}\`);
      }

      const data = await response.json();
      this.displayResults(data.results.slice(0, this.options.maxResults));

    } catch (error) {
      console.error('Search error:', error);
      this.showError();
    }
  }

  displayResults(results) {
    this.results = results;
    this.selectedIndex = -1;

    if (results.length === 0) {
      this.showNoResults();
      return;
    }

    const html = results.map((result, index) => \`
      <li
        role="option"
        id="result-\${index}"
        data-index="\${index}"
        aria-selected="false"
        class="search-autocomplete__result"
      >
        <span class="search-autocomplete__result-title">\${this.escapeHtml(result.title)}</span>
        <span class="search-autocomplete__result-meta">\${this.escapeHtml(result.category)}</span>
      </li>
    \`).join('');

    this.resultsContainer.innerHTML = html;
    this.showResults();
  }

  handleKeydown(event) {
    if (!this.resultsVisible) return;

    switch (event.key) {
      case 'ArrowDown':
        event.preventDefault();
        this.selectNext();
        break;

      case 'ArrowUp':
        event.preventDefault();
        this.selectPrevious();
        break;

      case 'Enter':
        event.preventDefault();
        this.selectCurrent();
        break;

      case 'Escape':
        this.hideResults();
        break;
    }
  }

  selectNext() {
    this.setSelectedIndex(
      this.selectedIndex < this.results.length - 1
        ? this.selectedIndex + 1
        : 0
    );
  }

  selectPrevious() {
    this.setSelectedIndex(
      this.selectedIndex > 0
        ? this.selectedIndex - 1
        : this.results.length - 1
    );
  }

  setSelectedIndex(index) {
    // Remove previous selection
    if (this.selectedIndex >= 0) {
      const prevElement = this.resultsContainer.querySelector(\`[data-index="\${this.selectedIndex}"]\`);
      if (prevElement) {
        prevElement.setAttribute('aria-selected', 'false');
        prevElement.classList.remove('is-selected');
      }
    }

    // Set new selection
    this.selectedIndex = index;

    if (index >= 0) {
      const element = this.resultsContainer.querySelector(\`[data-index="\${index}"]\`);
      if (element) {
        element.setAttribute('aria-selected', 'true');
        element.classList.add('is-selected');
        this.input.setAttribute('aria-activedescendant', element.id);

        // Ensure visible
        element.scrollIntoView({ block: 'nearest' });
      }
    }
  }

  selectCurrent() {
    if (this.selectedIndex >= 0 && this.results[this.selectedIndex]) {
      this.selectResult(this.results[this.selectedIndex]);
    }
  }

  handleResultClick(event) {
    const resultElement = event.target.closest('[data-index]');
    if (resultElement) {
      const index = parseInt(resultElement.dataset.index);
      if (this.results[index]) {
        this.selectResult(this.results[index]);
      }
    }
  }

  selectResult(result) {
    this.input.value = result.title;
    this.hideResults();

    // Emit custom event
    this.element.dispatchEvent(new CustomEvent('autocomplete:select', {
      detail: { result }
    }));

    // Navigate if URL provided
    if (result.url) {
      window.location.href = result.url;
    }
  }

  showResults() {
    this.resultsContainer.hidden = false;
    this.input.setAttribute('aria-expanded', 'true');
    this.resultsVisible = true;
  }

  hideResults() {
    this.resultsContainer.hidden = true;
    this.input.setAttribute('aria-expanded', 'false');
    this.input.removeAttribute('aria-activedescendant');
    this.resultsVisible = false;
    this.selectedIndex = -1;
  }

  showLoading() {
    this.resultsContainer.innerHTML = '<li class="search-autocomplete__loading">Searching...</li>';
    this.showResults();
  }

  showNoResults() {
    this.resultsContainer.innerHTML = '<li class="search-autocomplete__no-results">No results found</li>';
    this.showResults();
  }

  showError() {
    this.resultsContainer.innerHTML = '<li class="search-autocomplete__error">Search failed. Please try again.</li>';
    this.showResults();
  }

  handleBlur() {
    // Delay to allow click events
    setTimeout(() => {
      this.hideResults();
    }, 200);
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  destroy() {
    clearTimeout(this.debounceTimer);
    this.input.removeEventListener('input', this.handleInput);
    this.input.removeEventListener('keydown', this.handleKeydown);
    this.input.removeEventListener('blur', this.handleBlur);
    this.resultsContainer.removeEventListener('click', this.handleResultClick);
  }
}`,
      css: `
/* Search Autocomplete Component Styles */
.search-autocomplete {
  position: relative;
  width: 100%;
  max-width: 600px;
}

.search-autocomplete__input {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--font-size-base);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-md);
  background-color: var(--color-surface);
  color: var(--color-text);
  transition: border-color 0.2s ease;
}

.search-autocomplete__input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-alpha-20);
}

.search-autocomplete__results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: var(--spacing-xs);
  max-height: 400px;
  overflow-y: auto;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  z-index: 1000;
}

.search-autocomplete__results[hidden] {
  display: none;
}

.search-autocomplete__result {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-sm) var(--spacing-md);
  cursor: pointer;
  transition: background-color 0.1s ease;
}

.search-autocomplete__result:hover,
.search-autocomplete__result.is-selected {
  background-color: var(--color-primary-alpha-10);
}

.search-autocomplete__result-title {
  font-weight: 500;
  color: var(--color-text);
}

.search-autocomplete__result-meta {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.search-autocomplete__loading,
.search-autocomplete__no-results,
.search-autocomplete__error {
  padding: var(--spacing-md);
  text-align: center;
  color: var(--color-text-secondary);
}

.search-autocomplete__error {
  color: var(--color-error);
}

/* Dark theme support */
@media (prefers-color-scheme: dark) {
  .search-autocomplete__input {
    background-color: var(--color-surface-dark);
    border-color: var(--color-border-dark);
    color: var(--color-text-dark);
  }

  .search-autocomplete__results {
    background-color: var(--color-surface-dark);
    border-color: var(--color-border-dark);
  }
}`,
      usage: `
<!-- Nunjucks template usage -->
<div class="search-autocomplete" data-component="search-autocomplete">
  <label for="search-input" class="sr-only">Search the site</label>
  <input
    type="search"
    id="search-input"
    class="search-autocomplete__input"
    placeholder="Search posts, topics..."
    autocomplete="off"
  >
  <ul
    id="search-results"
    class="search-autocomplete__results"
    hidden
  ></ul>
</div>

<script type="module">
  import { SearchAutocomplete } from '/js/components/search-autocomplete.js';

  // Initialize on page load
  document.addEventListener('DOMContentLoaded', () => {
    const searchElement = document.querySelector('[data-component="search-autocomplete"]');

    if (searchElement) {
      const search = new SearchAutocomplete(searchElement, {
        searchEndpoint: '/api/blog/search',
        minChars: 3,
        debounceMs: 300
      });

      // Listen for selection events
      searchElement.addEventListener('autocomplete:select', (event) => {
        console.log('Selected:', event.detail.result);
      });
    }
  });
</script>`,
    },
  },
};

/**
 * Export example responses
 */
export default exampleResponses;
