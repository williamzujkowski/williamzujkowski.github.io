/**
 * Example responses for various types of requests
 *
 * These examples demonstrate high-quality AI responses for different
 * types of requests. They serve as few-shot learning examples for LLMs
 * to understand expected response patterns.
 */

export const exampleResponses = {
  /**
   * Example of a code generation response
   */
  codeGeneration: {
    request: "Create a theme toggle component that persists user preference",
    response: `
I'll create a theme toggle component that allows users to switch between light and dark themes and persists their preference across sessions using localStorage.

\`\`\`javascript
// theme-toggle.js
/**
 * Theme toggle component that persists user preferences
 *
 * @module theme-toggle
 */

// Constants for theme values and storage key
const THEMES = {
  LIGHT: 'light',
  DARK: 'dark'
};
const STORAGE_KEY = 'user-theme-preference';

/**
 * Initialize the theme system
 * @param {Object} options - Configuration options
 * @param {string} [options.defaultTheme='light'] - Default theme if no preference exists
 * @param {boolean} [options.respectSystemPreference=true] - Whether to respect system preference
 * @returns {Object} - API for controlling the theme
 */
export function initThemeToggle(options = {}) {
  const {
    defaultTheme = THEMES.LIGHT,
    respectSystemPreference = true
  } = options;

  // Get stored preference or use system preference/default
  const getInitialTheme = () => {
    const storedTheme = localStorage.getItem(STORAGE_KEY);

    if (storedTheme) {
      return storedTheme;
    }

    if (respectSystemPreference && window.matchMedia) {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      return prefersDark ? THEMES.DARK : THEMES.LIGHT;
    }

    return defaultTheme;
  };

  let currentTheme = getInitialTheme();

  // Apply theme to document
  const applyTheme = (theme) => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);
    currentTheme = theme;

    // Dispatch event for other components
    window.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
  };

  // Initialize theme
  applyTheme(currentTheme);

  // Setup listeners for theme toggle buttons
  const setupToggleListeners = () => {
    const toggleButtons = document.querySelectorAll('[data-theme-toggle]');

    toggleButtons.forEach(button => {
      button.addEventListener('click', () => {
        const newTheme = currentTheme === THEMES.LIGHT
          ? THEMES.DARK
          : THEMES.LIGHT;
        applyTheme(newTheme);
      });

      // Update button state
      updateToggleButtonState(button);
    });
  };

  // Update toggle button state based on current theme
  const updateToggleButtonState = (button) => {
    if (button.tagName === 'INPUT' && button.type === 'checkbox') {
      button.checked = currentTheme === THEMES.DARK;
    }

    // Set accessible attributes
    button.setAttribute('aria-pressed', currentTheme === THEMES.DARK);
    button.setAttribute('aria-label',
      currentTheme === THEMES.LIGHT ? 'Switch to dark theme' : 'Switch to light theme'
    );
  };

  // Setup system preference change listener
  if (respectSystemPreference && window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)')
      .addEventListener('change', (e) => {
        if (!localStorage.getItem(STORAGE_KEY)) {
          applyTheme(e.matches ? THEMES.DARK : THEMES.LIGHT);
        }
      });
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupToggleListeners);
  } else {
    setupToggleListeners();
  }

  // Return public API
  return {
    getTheme: () => currentTheme,
    setTheme: applyTheme,
    toggle: () => applyTheme(currentTheme === THEMES.LIGHT ? THEMES.DARK : THEMES.LIGHT),
    THEMES
  };
}

// Initialize the theme toggle with default options
const themeToggle = initThemeToggle();

// Export for external usage
export default themeToggle;
\`\`\`

You can use this component by adding a toggle button in your HTML:

\`\`\`html
<button data-theme-toggle aria-label="Toggle theme">
  Toggle theme
</button>
\`\`\`

Or with a checkbox:

\`\`\`html
<label for="theme-toggle">Toggle dark mode</label>
<input id="theme-toggle" type="checkbox" data-theme-toggle>
\`\`\`

This implementation:
- Persists user preference in localStorage
- Respects system preference when no user preference exists
- Provides an accessible interface with proper ARIA attributes
- Exports an API for programmatic theme control
- Updates all toggle buttons when theme changes
- Uses CSS custom properties via the data-theme attribute
`,
  },

  /**
   * Example of a code review response
   */
  codeReview: {
    request: "Review this error handling implementation",
    response: `
I've reviewed the error handling implementation. Here's my feedback:

## Strengths

1. **Structured error classes** - Creating custom error types (DatabaseError, ValidationError, etc.) helps classify errors by source and type.

2. **Context preservation** - The error wrapper preserves the original error as a cause, which is good for debugging.

3. **Standardized format** - Using a consistent error response format is good for API consumers.

## Areas for Improvement

1. **Uncaught promise rejections** - There's no global handler for uncaught promise rejections. Consider adding:

\`\`\`javascript
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  // Log to your error reporting service
});
\`\`\`

2. **Error codes** - I recommend adding numeric error codes that are stable across error message changes:

\`\`\`javascript
class ValidationError extends BaseError {
  constructor(message, validationErrors = [], cause = null) {
    super(message, { cause, code: 'E1001', validationErrors });
    this.validationErrors = validationErrors;
  }
}
\`\`\`

3. **Excessive catch blocks** - Some error handling is repetitive. Consider a higher-order function:

\`\`\`javascript
function withErrorHandling(fn, errorMapper) {
  return async (...args) => {
    try {
      return await fn(...args);
    } catch (error) {
      return errorMapper(error);
    }
  };
}
\`\`\`

4. **Missing security considerations** - Ensure sensitive information isn't leaked in error messages sent to clients.

5. **Inconsistent logging** - Some errors are logged, others aren't. Standardize your logging approach.

## Recommendations

1. Create an error handling middleware that centralizes all API error responses.
2. Add error serialization that removes sensitive data before logging or responding.
3. Implement structured logging with correlation IDs across requests.
4. Consider adding retry logic for transient errors (like network issues).

Overall, this is a solid foundation for error handling but could benefit from more consistency and security considerations.
`,
  },

  /**
   * Example of a refactoring response
   */
  refactoring: {
    request: "Refactor this code to be more maintainable",
    response: `
I'll refactor the provided code to improve maintainability. Here's my approach:

### Original Code Issues

The original code has several issues:
- Mixes business logic, data fetching, and UI updates
- Long functions with multiple responsibilities
- Lacks error handling
- Uses direct DOM manipulation throughout
- Hardcoded values and duplicated logic

### Refactored Solution

\`\`\`javascript
// data-service.js - Separating data concerns
/**
 * Service for handling API data operations
 */
class DataService {
  /**
   * Fetch user data from API
   * @param {string} userId - User ID to fetch
   * @returns {Promise<Object>} User data
   */
  static async fetchUserData(userId) {
    try {
      const response = await fetch(\`/api/users/\${userId}\`);

      if (!response.ok) {
        throw new Error(\`Failed to fetch user: \${response.status}\`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching user data:', error);
      throw error;
    }
  }

  /**
   * Fetch user activity data
   * @param {string} userId - User ID
   * @param {Object} options - Query options
   * @returns {Promise<Array>} Activity data
   */
  static async fetchUserActivity(userId, options = {}) {
    const { limit = 10, page = 1 } = options;

    try {
      const response = await fetch(
        \`/api/users/\${userId}/activity?limit=\${limit}&page=\${page}\`
      );

      if (!response.ok) {
        throw new Error(\`Failed to fetch activity: \${response.status}\`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching user activity:', error);
      throw error;
    }
  }
}

// ui-renderer.js - Separating UI concerns
/**
 * Handles rendering UI components
 */
class UserProfileRenderer {
  /**
   * Initialize the renderer with a container element
   * @param {HTMLElement} containerElement - Container for the profile
   */
  constructor(containerElement) {
    this.container = containerElement;
    this.elements = {
      userName: containerElement.querySelector('.user-name'),
      userBio: containerElement.querySelector('.user-bio'),
      activityList: containerElement.querySelector('.activity-list'),
      loadMoreBtn: containerElement.querySelector('.load-more-btn'),
      errorMessage: containerElement.querySelector('.error-message')
    };
  }

  /**
   * Render user profile data
   * @param {Object} userData - User profile data
   */
  renderUserProfile(userData) {
    if (!userData) return;

    this.elements.userName.textContent = userData.name;
    this.elements.userBio.textContent = userData.bio || 'No bio available';

    // Add additional user info rendering as needed
    this.container.classList.add('profile-loaded');
  }

  /**
   * Render user activity items
   * @param {Array} activities - Activity data
   * @param {boolean} append - Whether to append or replace content
   */
  renderUserActivity(activities, append = false) {
    if (!Array.isArray(activities)) return;

    const activityItems = activities.map(activity => {
      const item = document.createElement('li');
      item.className = 'activity-item';

      const date = new Date(activity.timestamp).toLocaleDateString();

      item.innerHTML = \`
        <span class="activity-type activity-type-\${activity.type}">
          \${activity.type}
        </span>
        <p class="activity-description">\${activity.description}</p>
        <span class="activity-date">\${date}</span>
      \`;

      return item;
    });

    if (!append) {
      this.elements.activityList.innerHTML = '';
    }

    activityItems.forEach(item => {
      this.elements.activityList.appendChild(item);
    });
  }

  /**
   * Show an error message
   * @param {string} message - Error message to display
   */
  showError(message) {
    this.elements.errorMessage.textContent = message;
    this.elements.errorMessage.classList.remove('hidden');
  }

  /**
   * Hide the error message
   */
  hideError() {
    this.elements.errorMessage.classList.add('hidden');
  }

  /**
   * Update load more button state
   * @param {boolean} hasMore - Whether more data is available
   * @param {boolean} isLoading - Whether data is currently loading
   */
  updateLoadMoreButton(hasMore, isLoading = false) {
    this.elements.loadMoreBtn.disabled = isLoading || !hasMore;
    this.elements.loadMoreBtn.textContent = isLoading
      ? 'Loading...'
      : 'Load More';

    this.elements.loadMoreBtn.classList.toggle('hidden', !hasMore);
  }
}

// profile-controller.js - Controller connecting data and UI
/**
 * Controller for managing user profile state and interactions
 */
class UserProfileController {
  /**
   * Initialize controller
   * @param {string} userId - User ID to display
   * @param {HTMLElement} containerElement - Profile container element
   */
  constructor(userId, containerElement) {
    this.userId = userId;
    this.renderer = new UserProfileRenderer(containerElement);
    this.activityPage = 1;
    this.activityLimit = 5;
    this.hasMoreActivities = true;
    this.isLoading = false;

    // Bind methods
    this.loadMoreActivities = this.loadMoreActivities.bind(this);

    // Initialize event listeners
    this.initEventListeners();
  }

  /**
   * Initialize event listeners
   */
  initEventListeners() {
    const loadMoreBtn = this.renderer.elements.loadMoreBtn;
    if (loadMoreBtn) {
      loadMoreBtn.addEventListener('click', this.loadMoreActivities);
    }
  }

  /**
   * Load user profile data
   */
  async loadUserProfile() {
    this.isLoading = true;

    try {
      this.renderer.hideError();

      // Load user data
      const userData = await DataService.fetchUserData(this.userId);
      this.renderer.renderUserProfile(userData);

      // Load initial activity data
      await this.loadMoreActivities(true);

    } catch (error) {
      this.renderer.showError('Failed to load user profile. Please try again.');
      console.error('Profile loading error:', error);
    } finally {
      this.isLoading = false;
    }
  }

  /**
   * Load more user activities
   * @param {boolean|Event} replaceExisting - Whether to replace existing items or event object
   */
  async loadMoreActivities(replaceExisting = false) {
    // Handle case when called from event handler
    if (replaceExisting instanceof Event) {
      replaceExisting = false;
    }

    if (this.isLoading || (!this.hasMoreActivities && !replaceExisting)) {
      return;
    }

    this.isLoading = true;
    this.renderer.updateLoadMoreButton(this.hasMoreActivities, true);

    try {
      // Reset page if replacing
      if (replaceExisting) {
        this.activityPage = 1;
      }

      const options = {
        limit: this.activityLimit,
        page: this.activityPage
      };

      const activities = await DataService.fetchUserActivity(this.userId, options);

      // Update state
      this.hasMoreActivities = activities.length >= this.activityLimit;
      this.activityPage++;

      // Update UI
      this.renderer.renderUserActivity(activities, !replaceExisting);

    } catch (error) {
      this.renderer.showError('Failed to load activities.');
      console.error('Activity loading error:', error);
    } finally {
      this.isLoading = false;
      this.renderer.updateLoadMoreButton(this.hasMoreActivities, false);
    }
  }
}

// Initialize profile
document.addEventListener('DOMContentLoaded', () => {
  const profileContainer = document.getElementById('user-profile');
  const userId = profileContainer.dataset.userId;

  if (userId) {
    const profileController = new UserProfileController(userId, profileContainer);
    profileController.loadUserProfile();
  }
});
\`\`\`

### Key Improvements

1. **Separation of Concerns**:
   - DataService: Handles API calls and data fetching
   - UserProfileRenderer: Manages UI updates
   - UserProfileController: Orchestrates data and UI

2. **Improved Error Handling**:
   - All API calls have proper try/catch blocks
   - Errors are displayed to users appropriately
   - Console logging for debugging

3. **More Maintainable Structure**:
   - Classes with single responsibilities
   - Methods that do one thing well
   - Clear interfaces between components

4. **Better State Management**:
   - State is contained within controller
   - UI is updated based on state changes
   - Loading states are properly tracked

5. **Code Reusability**:
   - Renderer can be reused for different profiles
   - DataService methods can be used elsewhere
   - Clear separation allows easier testing

This refactoring maintains all the original functionality while making the code more maintainable, testable, and extensible.
`,
  },
};
