// Special script to check and fix imports for verification tests
// This script will identify any missing imports or initialization issues

// Import modules 
import { initSearch } from './src/js/components/search.js';
import { initThemeToggle } from './src/js/components/theme-toggle.js';
import { initCodeHighlight } from './src/js/components/code-highlight.js';
import { initStaticFallbacks } from './src/js/components/static-fallbacks.js';
import { initResourceHints } from './src/js/resource-hints.js';

// Main initialization function
export function initAll() {
  // Initialize all components
  if (typeof initSearch === 'function') initSearch();
  if (typeof initThemeToggle === 'function') initThemeToggle();
  if (typeof initCodeHighlight === 'function') initCodeHighlight();
  if (typeof initStaticFallbacks === 'function') initStaticFallbacks();
  if (typeof initResourceHints === 'function') initResourceHints();
}

// Export all the components
export {
  initSearch,
  initThemeToggle,
  initCodeHighlight,
  initStaticFallbacks,
  initResourceHints
};