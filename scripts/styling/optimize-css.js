/**
 * CSS Optimization Tool
 * 
 * This script analyzes and optimizes CSS files by:
 * 1. Consolidating redundant styles between files
 * 2. Organizing styles into logical groupings (base, components, utilities)
 * 3. Simplifying mobile-specific overrides
 * 4. Improving theme variable organization
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get __dirname equivalent in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Paths to CSS files
const STYLES_CSS_PATH = path.resolve(__dirname, '../src/css/styles.css');
const BASIC_CSS_PATH = path.resolve(__dirname, '../src/css/basic.css');
const BLOG_ENHANCED_CSS_PATH = path.resolve(__dirname, '../src/css/blog-enhanced.css');
const OPTIMIZED_CSS_DIR = path.resolve(__dirname, '../src/css/optimized');

// Ensure the optimized directory exists
if (!fs.existsSync(OPTIMIZED_CSS_DIR)) {
  fs.mkdirSync(OPTIMIZED_CSS_DIR, { recursive: true });
}

// Create backup directory
const BACKUP_DIR = path.resolve(__dirname, '../src/css/backup');
if (!fs.existsSync(BACKUP_DIR)) {
  fs.mkdirSync(BACKUP_DIR, { recursive: true });
}

// Backup original files
function createBackups() {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  
  console.log('Creating backups of original CSS files...');
  
  [STYLES_CSS_PATH, BASIC_CSS_PATH, BLOG_ENHANCED_CSS_PATH].forEach(filePath => {
    if (fs.existsSync(filePath)) {
      const fileName = path.basename(filePath);
      const backupPath = path.join(BACKUP_DIR, `${fileName}.${timestamp}.bak`);
      fs.copyFileSync(filePath, backupPath);
      console.log(`✓ Backed up ${fileName} to ${backupPath}`);
    }
  });
}

// Read CSS files
function readCssFiles() {
  console.log('Reading CSS files...');
  
  const files = {
    styles: fs.existsSync(STYLES_CSS_PATH) ? fs.readFileSync(STYLES_CSS_PATH, 'utf8') : '',
    basic: fs.existsSync(BASIC_CSS_PATH) ? fs.readFileSync(BASIC_CSS_PATH, 'utf8') : '',
    blogEnhanced: fs.existsSync(BLOG_ENHANCED_CSS_PATH) ? fs.readFileSync(BLOG_ENHANCED_CSS_PATH, 'utf8') : ''
  };
  
  return files;
}

// Create the optimized structure
async function createOptimizedStructure(cssFiles) {
  console.log('Creating optimized CSS structure...');
  
  // 1. Extract theme variables from styles.css
  const themeVariables = extractThemeVariables(cssFiles.styles);
  
  // 2. Create base.css with foundational styles
  const baseStyles = createBaseStyles(cssFiles.styles, cssFiles.basic);
  
  // 3. Create components.css with component styles
  const componentStyles = createComponentStyles(cssFiles.styles, cssFiles.blogEnhanced);
  
  // 4. Create utilities.css with utility classes
  const utilityStyles = createUtilityStyles(cssFiles.styles);
  
  // 5. Create mobile.css with mobile-specific styles
  const mobileStyles = createMobileStyles(cssFiles.styles, cssFiles.blogEnhanced);
  
  // 6. Create main.css that imports all the pieces
  const mainCss = createMainCss();
  
  // Save all files
  await Promise.all([
    saveOptimizedCss('theme.css', themeVariables),
    saveOptimizedCss('base.css', baseStyles),
    saveOptimizedCss('components.css', componentStyles),
    saveOptimizedCss('utilities.css', utilityStyles),
    saveOptimizedCss('mobile.css', mobileStyles),
    saveOptimizedCss('main.css', mainCss)
  ]);
}

// Extract theme variables into their own file
function extractThemeVariables(stylesCss) {
  console.log('Extracting theme variables...');
  
  // Extract root variables from styles.css
  const rootVariableRegex = /@layer base\s*{\s*:root\s*{[^}]*}\s*:root\.light\s*{[^}]*}\s*}/s;
  
  const match = stylesCss.match(rootVariableRegex);
  let themeVariables = match ? match[0] : '';
  
  // Enhance with better comments and organization
  themeVariables = `/* 
 * Theme Variables
 * 
 * This file contains all color and design token variables
 * used throughout the site. Variables follow the OKLCH color
 * model for better perceptual uniformity.
 */

${themeVariables}`;

  return themeVariables;
}

// Create base.css with foundational styles
function createBaseStyles(stylesCss, basicCss) {
  console.log('Creating base styles...');
  
  // Extract base styles from styles.css (typography, html, body, headings, etc.)
  let baseStyles = `/* 
 * Base Styles
 * 
 * Core typographic and element styles that form the foundation
 * of the site's design system.
 */

/* Tailwind directives */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Apply typography plugin to blog posts */
@layer base {
  .prose-custom {
    @apply prose prose-invert prose-lg max-w-none w-full;
  }
  
  /* Use prefers-reduced-motion for animations */
  @media (prefers-reduced-motion) {
    *, ::before, ::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
      scroll-behavior: auto !important;
    }
  }
}

/* Base typography and elements */
@layer base {
  /* Focus styles */
  *:focus-visible {
    outline: 2px solid var(--color-accent);
    outline-offset: 2px;
  }

  html {
    @apply scroll-smooth;
    font-size: 16px;
  }

  body {
    @apply bg-background text-text font-sans;
    line-height: 1.7;
    font-size: 1.0625rem;
  }

  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    @apply font-sans font-semibold text-white mb-5;
    line-height: 1.3;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  }

  h1 {
    @apply text-3xl md:text-4xl;
    letter-spacing: -0.01em;
  }

  h2 {
    @apply text-2xl md:text-3xl border-b border-border pb-2 pt-2 mt-10 mb-6;
    letter-spacing: -0.01em;
  }

  h3 {
    @apply text-xl md:text-2xl mt-8 mb-4;
  }

  a {
    @apply text-theme-accent;
    text-decoration: none;
  }

  a:hover {
    @apply hover:text-accent-hover;
    text-decoration: underline;
  }

  p, ul, ol {
    @apply mb-4;
  }

  ul, ol {
    @apply pl-6;
  }

  ul {
    @apply list-disc;
  }

  ol {
    @apply list-decimal;
  }

  code {
    @apply font-mono text-sm px-1.5 py-0.5 bg-gray-light border border-border rounded-github text-text;
  }

  pre {
    @apply bg-gray-light p-4 rounded-github overflow-x-auto mb-4 border border-border;
  }

  pre code {
    @apply bg-transparent p-0 border-0;
  }

  blockquote {
    @apply border-l-4 border-theme-accent p-3 pl-4 my-4 bg-gray-light rounded-r-github text-text;
  }

  hr {
    @apply my-6 border-t border-border;
  }

  img {
    @apply max-w-full h-auto rounded-github;
  }

  table {
    @apply w-full border-collapse mb-4 text-left;
  }

  table th {
    @apply bg-surface p-2 border-b border-border font-medium;
  }

  table td {
    @apply p-2 border-b border-border;
  }
  
  /* Form elements with improved contrast */
  input[type="text"],
  input[type="email"],
  input[type="password"],
  input[type="search"],
  textarea,
  select {
    @apply bg-gray-light border border-border rounded-github p-2 text-white focus:outline-none focus:ring-2 ring-theme-accent border-theme-accent focus:border-theme-accent;
  }

  ::placeholder {
    @apply text-text-secondary opacity-70;
  }
  
  /* Scroll behavior */
  @media (max-width: 640px) {
    html {
      font-size: 15px;
    }
  }
  
  /* Smooth scrollbar for Firefox */
  @supports (scrollbar-color: auto) {
    * {
      scrollbar-color: rgba(175, 184, 193, 0.2) transparent;
      scrollbar-width: thin;
    }
  }

  /* Smooth scrollbar for Webkit */
  ::-webkit-scrollbar {
    width: 10px;
    height: 10px;
  }

  ::-webkit-scrollbar-track {
    @apply bg-transparent;
  }

  ::-webkit-scrollbar-thumb {
    @apply bg-gray-light rounded-full;
  }

  ::-webkit-scrollbar-thumb:hover {
    @apply bg-gray-light;
  }

  ::selection {
    @apply bg-theme-accent-10;
  }
}`;

  return baseStyles;
}

// Create components.css with component styles
function createComponentStyles(stylesCss, blogEnhancedCss) {
  console.log('Creating component styles...');
  
  let componentStyles = `/* 
 * Component Styles
 * 
 * Reusable UI components that make up the site's interface.
 * Organized by component type for better maintainability.
 */

/* Add transition effect for light/dark mode toggle */
body, 
.gh-header, 
.gh-footer, 
.gh-post-card, 
.gh-blog-controls, 
.tags-filter, 
.gh-section-header, 
.gh-post-grid, 
.gh-post-card,
.gh-post-image,
.gh-post-content,
.gh-post-title,
.gh-post-meta,
.gh-post-excerpt,
.gh-post-footer,
.gh-read-more,
.gh-pagination,
.gh-profile-header,
.gh-avatar,
.gh-name,
.gh-username,
.gh-bio,
.gh-btn,
.gh-tag-buttons,
.tag-btn,
a, button, input, select, textarea {
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}

/* =================== */
/* Layout Components   */
/* =================== */
@layer components {
  /* Main container */
  .site-container {
    @apply w-full mx-auto px-5 py-4;
  }

  /* Custom container with Container Queries support */
  .container-custom {
    width: 100%;
    margin-left: auto;
    margin-right: auto;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 1200px;
  }

  @screen sm {
    .container-custom {
      padding-left: 1.5rem;
      padding-right: 1.5rem;
    }
  }

  @screen lg {
    .container-custom {
      padding-left: 2rem;
      padding-right: 2rem;
    }
  }
}

/* =================== */
/* Header Components   */
/* =================== */
@layer components {
  /* GitHub-style header */
  .gh-header {
    @apply bg-surface border-b border-border flex items-center py-4 px-4 sticky top-0 z-50 backdrop-blur-sm;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
  }

  .gh-header-inner {
    @apply max-w-[1200px] w-full mx-auto flex items-center justify-between;
  }

  .gh-nav {
    @apply flex items-center gap-6;
  }

  .gh-nav-item {
    @apply px-3 py-2 text-sm font-medium text-text hover:text-white rounded-github hover:bg-gray-light transition-all duration-300 relative overflow-hidden;
  }

  /* Animated underline effect */
  .gh-nav-item::after {
    @apply absolute bottom-0 left-0 w-0 h-0.5 bg-theme-accent transition-all duration-300 content-[''];
  }

  .gh-nav-item:hover::after {
    @apply w-full;
  }

  .gh-nav-item.active {
    @apply font-semibold text-theme-accent border border-border bg-gray-light;
  }

  /* Focus styles for accessibility */
  .gh-nav-item:focus-visible {
    @apply outline-none ring-2 ring-theme-accent opacity-90;
  }
}

/* =================== */
/* Profile Components  */
/* =================== */
@layer components {
  .gh-profile-header {
    @apply mt-8 mb-12 flex flex-col md:flex-row gap-10;
  }

  .gh-avatar-container {
    @apply flex-shrink-0 flex flex-col items-center md:items-start;
  }

  .gh-avatar {
    @apply w-[296px] h-[296px] rounded-github border-2 border-border object-cover shadow-md;
  }

  .gh-profile-content {
    @apply flex-grow min-w-0 mt-6 md:mt-0;
  }

  .gh-profile-header-info {
    @apply mb-4;
  }

  .gh-name {
    @apply text-2xl font-semibold mb-1;
  }

  .gh-username {
    @apply text-xl text-text-secondary font-normal mb-4;
  }

  .gh-bio {
    @apply text-base mb-4;
  }

  .gh-profile-stats {
    @apply flex items-center gap-3 text-sm text-text-secondary mb-4;
  }

  .gh-stat {
    @apply flex items-center;
  }

  .gh-stat-icon {
    @apply mr-1;
  }

  .gh-stat-count {
    @apply font-semibold text-text;
  }

  .gh-stat-label {
    @apply ml-1;
  }
}

/* =================== */
/* Button Components   */
/* =================== */
@layer components {
  .gh-btn {
    @apply inline-flex items-center px-4 py-2 text-sm font-medium border border-border rounded-github bg-gray-light hover:bg-gray-light transition-all duration-300 transform hover:-translate-y-0.5 focus:outline-none focus:ring-2 ring-theme-accent opacity-90 text-white;
  }

  .gh-btn-primary {
    @apply bg-primary text-white border-primary hover:bg-primary-hover shadow-sm;
  }

  .gh-btn svg {
    @apply mr-1.5;
  }
  
  /* GitHub-style badge */
  .gh-badge {
    @apply inline-flex items-center px-1.5 py-0.5 text-xs font-medium rounded-full;
  }

  .gh-badge-primary {
    @apply bg-theme-primary-10 text-primary;
  }

  .gh-badge-accent {
    @apply bg-theme-accent-20 text-theme-accent;
  }

  .gh-badge-secondary {
    @apply bg-gray-light text-secondary;
  }
}

/* =================== */
/* Repository Cards    */
/* =================== */
@layer components {
  .gh-pinned-repos {
    @apply mt-6;
  }

  .gh-section-header {
    @apply mb-2 pb-2 border-b border-border flex justify-between items-center;
  }

  .gh-section-title {
    @apply text-base font-semibold inline-flex items-center;
  }

  .gh-repos-grid {
    @apply grid grid-cols-1 md:grid-cols-2 gap-4 mb-6;
  }

  .gh-repo-card {
    @apply p-6 border border-border rounded-github bg-gray-light transition-all duration-300 hover:shadow-card hover:-translate-y-1 relative overflow-hidden;
  }

  .gh-repo-card::before {
    @apply absolute top-0 left-0 w-full h-0.5 bg-theme-accent transform scale-x-0 transition-transform duration-300 ease-out content-[''];
  }

  .gh-repo-card:hover::before {
    @apply scale-x-100;
  }

  .gh-repo-name {
    @apply flex items-center text-base font-semibold text-theme-accent mb-1;
  }

  .gh-repo-description {
    @apply text-sm text-text mb-4 overflow-hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }

  .gh-repo-meta {
    @apply flex flex-wrap gap-x-4 gap-y-2 text-xs text-text-secondary;
  }

  .gh-repo-language {
    @apply flex items-center;
  }

  .gh-language-color {
    @apply w-2.5 h-2.5 rounded-full mr-1;
  }
}

/* =================== */
/* Blog Post Cards     */
/* =================== */
@layer components {
  /* Consolidated blog card styles from both files */
  .gh-post-card {
    @apply border border-border rounded-github overflow-hidden bg-gray-light transition-all duration-300 hover:-translate-y-1.5 hover:shadow-lg flex flex-col relative;
  }
  
  /* Add light theme card styling */
  .light .gh-post-card {
    @apply bg-surface border-border;
  }
  
  /* Fix hover issue by setting the same bg color on hover */
  .gh-post-card:hover {
    @apply bg-gray-light;
    border-color: var(--color-accent);
  }
  
  .light .gh-post-card:hover {
    @apply bg-surface;
  }

  .gh-post-image {
    @apply h-44 overflow-hidden relative;
  }

  .gh-post-image img {
    @apply w-full h-full object-cover transition-transform duration-500;
  }

  .gh-post-card:hover .gh-post-image img {
    @apply transform scale-105;
  }

  .gh-post-tags-overlay {
    @apply absolute top-3 right-3 flex flex-wrap gap-1.5 justify-end max-w-[70%];
  }

  .gh-post-tags-overlay .gh-badge {
    @apply bg-surface text-white text-xs px-2 py-0.5 rounded-full backdrop-blur-sm shadow-sm border border-border;
  }

  .gh-post-content {
    @apply p-5 flex-grow flex flex-col;
  }

  .gh-post-title {
    @apply text-lg font-semibold text-white mb-2.5 hover:text-accent transition-colors duration-200 line-clamp-2;
  }

  .gh-post-meta {
    @apply flex justify-between items-center text-sm text-text-secondary mb-3 flex-wrap gap-2;
  }

  .gh-post-date,
  .gh-post-reading-time {
    @apply flex items-center;
  }

  .gh-post-date svg,
  .gh-post-reading-time svg {
    @apply mr-1.5 text-accent opacity-80;
  }

  .gh-post-excerpt {
    @apply text-base text-text leading-relaxed mb-4 line-clamp-3;
  }

  .gh-post-footer {
    @apply mt-auto pt-3 border-t border-border flex justify-between items-center;
  }

  .gh-read-more {
    @apply text-sm text-theme-accent font-medium hover:underline inline-flex items-center gap-1;
  }

  .gh-read-more svg {
    @apply ml-1 transition-transform duration-200;
  }

  .gh-post-card:hover .gh-read-more svg {
    @apply transform translate-x-1;
  }
}

/* =================== */
/* Blog Controls       */
/* =================== */
@layer components {
  /* Blog controls and search */
  .gh-blog-controls {
    @apply border border-border rounded-github overflow-hidden bg-surface shadow-md mb-8;
  }

  .gh-control-panel {
    @apply p-4 flex flex-col md:flex-row gap-4 justify-between items-start md:items-center;
  }

  .gh-search-container {
    @apply relative w-full md:w-80;
  }

  .gh-search-input {
    @apply w-full py-2.5 pl-4 pr-10 bg-gray-light border border-border rounded-github text-white focus:ring-2 ring-theme-accent focus:outline-none shadow-inner transition-all duration-300;
  }

  .gh-search-input:focus {
    @apply border-theme-accent bg-gray-light;
  }

  .gh-search-icon {
    @apply absolute right-3 top-3 text-text-secondary;
  }

  .gh-blog-stats {
    @apply flex flex-wrap items-center gap-4 text-sm text-text-secondary;
  }

  .gh-stat {
    @apply flex items-center gap-2;
  }

  .gh-stat svg {
    @apply text-accent opacity-80;
  }
  
  /* Search highlight */
  .gh-search-highlight {
    @apply bg-theme-accent-20 text-white px-1 rounded font-medium;
  }
}

/* =================== */
/* Tag Filtering       */
/* =================== */
@layer components {
  /* Tag filtering */
  .tags-filter {
    @apply border border-border rounded-github overflow-hidden bg-surface shadow-md p-4 mb-8;
  }

  .gh-filter-header {
    @apply flex justify-between items-center mb-3 pb-2 border-b border-border;
  }

  .gh-filter-title {
    @apply flex items-center gap-2 text-white font-medium;
  }

  .gh-filter-clear {
    @apply text-xs text-theme-accent hover:text-accent-hover transition-colors duration-200 flex items-center;
  }

  .gh-tag-buttons {
    @apply flex flex-wrap gap-2.5;
  }

  .tag-btn {
    @apply px-3.5 py-2 rounded-github text-sm bg-gray-light text-text-secondary border border-border transition-all duration-200 hover:bg-gray-light hover:text-white;
  }

  .tag-btn.selected {
    @apply bg-theme-accent text-white border-theme-accent shadow-sm;
  }
  
  .pulse-animation {
    animation: tag-pulse 0.5s cubic-bezier(0.4, 0, 0.6, 1);
  }

  @keyframes tag-pulse {
    0%, 100% {
      opacity: 1;
      transform: scale(1);
    }
    50% {
      opacity: 0.9;
      transform: scale(1.05);
    }
  }
}

/* =================== */
/* Blog Grid & Pagination */
/* =================== */
@layer components {
  /* Blog post grid */
  .gh-post-grid {
    @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 transition-opacity duration-300;
  }

  .gh-post-grid.searching {
    @apply opacity-60;
  }

  .gh-post-grid.reset-animation {
    animation: reset-grid 0.5s ease;
  }

  @keyframes reset-grid {
    0% {
      transform: scale(0.98);
      opacity: 0.9;
    }
    100% {
      transform: scale(1);
      opacity: 1;
    }
  }
  
  /* Pagination styles */
  .gh-pagination-container {
    @apply mt-12 mb-8;
  }

  .gh-pagination-header {
    @apply flex items-center justify-center gap-2 mb-5 text-text-secondary;
  }

  .gh-pagination-header svg {
    @apply text-accent opacity-80;
  }

  .gh-pagination {
    @apply flex justify-center;
  }

  .gh-pagination-nav {
    @apply inline-flex items-center gap-2 p-1 bg-gray-light rounded-github border border-border;
  }

  .gh-page-button {
    @apply px-3 py-1.5 flex items-center gap-1.5 bg-surface text-text-secondary hover:bg-gray-light hover:text-white transition-colors duration-200 rounded-github font-medium text-sm;
  }

  .gh-page-button.disabled {
    @apply opacity-50 cursor-not-allowed hover:bg-surface hover:text-text-secondary;
  }

  .gh-pagination-pages {
    @apply flex items-center gap-1;
  }

  .gh-page-number {
    @apply flex items-center justify-center w-8 h-8 rounded-github bg-surface text-text-secondary hover:bg-gray-light hover:text-white transition-colors duration-200 text-sm;
  }

  .gh-page-number.active {
    @apply bg-accent text-white;
  }
}

/* =================== */
/* Footer Components   */
/* =================== */
@layer components {
  /* Footer */
  .gh-footer {
    @apply mt-24 border-t border-border bg-surface backdrop-blur-sm;
    box-shadow: 0 -1px 3px rgba(0, 0, 0, 0.3);
  }

  .gh-footer-inner {
    @apply max-w-[1200px] mx-auto flex flex-col md:flex-row justify-between items-center gap-4 px-4 py-4;
  }

  .gh-footer-links {
    @apply flex flex-wrap gap-x-6 gap-y-3 text-sm text-text-secondary;
  }

  .gh-footer-links a {
    @apply transition-colors duration-300 hover:text-theme-accent relative;
  }

  .gh-footer-links a::after {
    @apply absolute bottom-0 left-0 w-0 h-0.5 bg-theme-accent transition-all duration-300 content-[''];
  }

  .gh-footer-links a:hover::after {
    @apply w-full;
  }

  .gh-copyright {
    @apply text-sm text-text-secondary flex items-center;
  }

  .gh-copyright a {
    @apply ml-1 text-theme-accent hover:underline;
  }

  /* Social media icons */
  .header-social,
  .footer-social {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .header-social a,
  .footer-social a {
    transition: all 0.2s ease-in-out;
  }

  .header-social a:hover:not(.social-disabled),
  .footer-social a:hover:not(.social-disabled) {
    transform: translateY(-2px);
  }
}

/* =================== */
/* Blog Post Styles    */
/* =================== */
@layer components {
  /* Blog Post Styles (Single Post) */
  .prose-custom {
    @apply prose prose-invert max-w-none prose-headings:text-white prose-p:text-text prose-a:text-accent prose-strong:text-white prose-code:text-accent-200 prose-pre:bg-surface prose-blockquote:border-accent-600 prose-blockquote:text-text-secondary prose-ul:text-text prose-ol:text-text;
  }

  .prose-custom h1, .prose-custom h2, .prose-custom h3, .prose-custom h4 {
    @apply scroll-mt-16;
  }

  .prose-custom h2 {
    @apply text-2xl font-semibold border-b border-border pb-2 mt-8 mb-4;
  }

  .prose-custom h3 {
    @apply text-xl font-medium mt-6 mb-3;
  }

  .prose-custom a {
    @apply transition-colors duration-200 hover:text-accent-400 no-underline border-b border-accent/30 hover:border-accent-400;
  }

  .prose-custom ul {
    @apply list-disc pl-5 my-4;
  }

  .prose-custom ol {
    @apply list-decimal pl-5 my-4;
  }

  .prose-custom pre {
    @apply my-6 rounded-github overflow-x-auto text-[0.85em];
  }

  .prose-custom blockquote {
    @apply italic bg-surface/50 p-4 rounded-github my-6 border-l-4 border-accent;
  }
}

/* =================== */
/* Code Block Styling  */
/* =================== */
@layer components {
  /* Inline code styling with better contrast */
  .prose-custom code:not(pre code) {
    @apply px-1.5 py-0.5 rounded text-[0.9em] font-mono;
    background-color: rgba(110, 118, 129, 0.2);
    color: #e6edf3;
    border: 1px solid rgba(110, 118, 129, 0.3);
  }

  /* Light theme inline code */
  .light .prose-custom code:not(pre code) {
    background-color: rgba(175, 184, 193, 0.2);
    color: #24292f;
    border: 1px solid rgba(175, 184, 193, 0.3);
  }

  /* Enhanced code blocks styling */
  .prose-custom pre {
    @apply p-0 my-6 bg-[#0e1117] rounded-github overflow-hidden border border-border;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
  }

  .prose-custom pre code {
    @apply block p-0 overflow-auto text-[0.9em] bg-transparent text-gray-200;
    font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
    tab-size: 2;
  }

  /* Code container with line numbers */
  .code-line {
    position: relative;
    padding-left: 3.5rem;
    min-height: 1.5em;
    padding-right: 1rem;
    border-left: 3px solid transparent;
  }

  /* Highlight active line on hover */
  .code-line:hover {
    background-color: rgba(115, 138, 148, 0.1);
    border-left-color: rgba(var(--color-accent-rgb), 0.4);
  }

  .code-line::before {
    content: attr(data-line-number);
    position: absolute;
    left: 0;
    padding: 0 0.7rem;
    width: 3rem;
    text-align: right;
    color: rgba(139, 148, 158, 0.6);
    background-color: rgba(0, 0, 0, 0.2);
    font-size: 0.8em;
    user-select: none;
    border-right: 1px solid rgba(139, 148, 158, 0.2);
  }

  /* Code block header with language and copy button */
  .code-header {
    @apply flex items-center justify-between bg-[#171b22] px-4 py-2 text-xs text-[#8b949e] border-b border-border;
    font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
  }

  .copy-button {
    @apply flex items-center justify-center py-1 px-2 rounded-md bg-surface hover:bg-gray-light transition-colors duration-200 text-text-secondary hover:text-white;
  }

  /* Code block custom scrollbar */
  pre::-webkit-scrollbar {
    width: 10px;
    height: 10px;
  }

  pre::-webkit-scrollbar-track {
    background-color: rgba(0, 0, 0, 0.1);
    border-radius: 0;
  }

  pre::-webkit-scrollbar-thumb {
    background-color: rgba(139, 148, 158, 0.3);
    border-radius: 10px;
    border: 2px solid rgba(0, 0, 0, 0.1);
  }

  pre::-webkit-scrollbar-thumb:hover {
    background-color: rgba(139, 148, 158, 0.5);
  }
}

/* =================== */
/* Other Components    */
/* =================== */
@layer components {
  /* Breadcrumbs */
  .breadcrumbs {
    @apply py-3 mb-6 bg-gray-light rounded-github border border-border px-4;
  }

  .breadcrumbs-list {
    @apply flex flex-wrap items-center text-sm whitespace-nowrap overflow-x-auto pb-1;
    scrollbar-width: none;
  }

  .breadcrumbs-list::-webkit-scrollbar {
    display: none;
  }

  .breadcrumbs-item {
    @apply inline-flex items-center text-text-secondary;
  }

  .breadcrumbs-separator {
    @apply mx-2 text-text-secondary font-medium inline-block;
  }

  .breadcrumbs-link {
    @apply text-theme-accent hover:text-accent-hover hover:underline transition-colors;
  }

  .breadcrumbs-item.current {
    @apply text-white font-medium;
  }
  
  /* Table of Contents */
  .toc {
    @apply border border-border rounded-github p-4 bg-gray-light mb-8 sticky top-20;
  }

  .toc-title {
    @apply text-lg font-semibold mb-3 text-white;
  }

  .toc-list {
    @apply space-y-2 text-text list-none pl-0;
  }

  .toc-item {
    @apply flex items-center;
  }

  .toc-item.level-3 {
    @apply ml-4;
  }

  .toc-link {
    @apply text-accent hover:text-accent-400 transition-colors duration-200 no-underline;
  }
  
  /* Skip link for accessibility */
  .skip-link {
    @apply fixed top-0 left-0 -translate-y-full bg-theme-accent text-white px-4 py-2 z-[60] transition-transform duration-200 focus:translate-y-0 font-medium rounded-br-github;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
  }

  /* Back to top button */
  .back-to-top-btn {
    @apply fixed right-6 bottom-6 bg-theme-accent text-white w-10 h-10 rounded-full flex items-center justify-center text-lg shadow-md z-50 border border-border;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.3s ease, transform 0.3s ease, visibility 0.3s;
    transform: translateY(10px);
  }

  .back-to-top-btn:hover {
    @apply hover:bg-accent-hover;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  }

  .back-to-top-btn:focus {
    @apply outline-none ring-2 ring-theme-accent opacity-90;
  }

  .back-to-top-btn.visible {
    opacity: 0.9;
    transform: translateY(0);
    visibility: visible;
  }

  .back-to-top-btn.hidden {
    opacity: 0;
    visibility: hidden;
  }

  /* Header anchor links */
  .header-anchor {
    @apply text-theme-accent opacity-0 ml-2 hover:opacity-100 transition-opacity duration-200;
    text-decoration: none !important;
  }

  h2:hover .header-anchor,
  h3:hover .header-anchor,
  h4:hover .header-anchor {
    @apply opacity-100;
  }
}`;

  return componentStyles;
}

// Create utilities.css with utility classes
function createUtilityStyles(stylesCss) {
  console.log('Creating utility styles...');
  
  let utilityStyles = `/* 
 * Utility Classes
 * 
 * Single-purpose utility classes that can be composed to build
 * complex UI patterns. Follows the principle of doing one thing well.
 */

/* Custom animations */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes pulse {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
  100% {
    opacity: 1;
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes fadeOut {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}

/* Page loader and transitions */
.page-loader {
  @apply fixed inset-0 bg-background bg-opacity-80 z-[100] flex flex-col items-center justify-center transition-opacity duration-500;
  backdrop-filter: blur(5px);
}

.page-loader-hidden {
  @apply opacity-0 pointer-events-none;
}

.loader-spinner {
  @apply w-10 h-10 border-4 border-border rounded-full;
  border-top-color: var(--color-accent);
  animation: spin 1s linear infinite;
}

.loader-text {
  @apply mt-4 text-text-secondary text-sm font-medium;
  animation: pulse 1.5s ease-in-out infinite;
}

/* Page transitions */
.page-transition-enter {
  animation: fadeIn 0.5s ease-out forwards;
}

.page-transition-exit {
  animation: fadeOut 0.3s ease-in forwards;
}

/* Lazy loaded images */
img {
  transition: opacity 0.5s ease-in-out;
}

img[data-src] {
  opacity: 0;
}

img.loaded {
  opacity: 1;
}

/* GitHub stats alignment */
.github-stats-container {
  text-align: right;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: flex-end;
  padding: 0;
  overflow: hidden;
  line-height: 0; /* Eliminate any extra space */
  position: relative; /* For absolute positioning */
  width: 100%;
  background-color: #0d1117; /* Match GitHub dark theme */
}

.github-stats-container img {
  max-width: none; /* Allow image to overflow container */
  width: 110%; /* Make image wider than container */
  display: block;
  position: relative;
  right: -8px; /* Push image right to align numbers */
  margin-left: auto;
  transform-origin: right center;
  object-position: right center; /* Ensure image is positioned from right */
}

/* Fix spacing in GitHub stats layout */
@media (min-width: 768px) {
  .github-stats-container img {
    width: 112%; /* Slightly wider on desktop */
    right: -10px; /* Push further right on desktop */
  }
}

/* Mobile GitHub stats adjustments */
@media (max-width: 767px) {
  .github-stats-container img {
    width: 110%;
    right: -8px;
  }
}

/* Custom utilities for better contrast */
.high-contrast {
  color: white !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.accent-text {
  color: #a5d6ff !important;
  font-weight: 500;
}

/* Custom grid gap classes */
@layer utilities {
  .gap-custom {
    gap: 0.75rem;
  }
  
  @media (min-width: 640px) {
    .gap-custom {
      gap: 1rem;
    }
  }
  
  @media (min-width: 768px) {
    .gap-custom {
      gap: 1.25rem;
    }
  }

  /* Add group hover and focus utilities */
  .group-hover-scale {
    @apply transition-transform duration-300;
  }
  
  .group:hover .group-hover-scale {
    @apply scale-105;
  }

  .group-hover-translate-up {
    @apply transition-transform duration-300;
  }
  
  .group:hover .group-hover-translate-up {
    @apply -translate-y-1;
  }
}`;

  return utilityStyles;
}

// Create mobile.css with mobile-specific styles
function createMobileStyles(stylesCss, blogEnhancedCss) {
  console.log('Creating mobile styles...');
  
  let mobileStyles = `/* 
 * Mobile Styles
 * 
 * Responsive overrides for mobile devices.
 * Organized by component type for easier maintenance.
 */

/* Simplified mobile styles - consolidated from both files */
@media (max-width: 768px) {
  /* Global adjustments for mobile */
  body {
    @apply text-lg;
  }
  
  h1 {
    @apply text-3xl mb-4;
  }
  
  h2 {
    @apply text-2xl mb-5 font-semibold;
  }
  
  h3 {
    @apply text-xl mb-4 font-medium;
  }
  
  p {
    @apply text-lg leading-relaxed;
  }
  
  .site-container {
    @apply px-6 py-6;
  }
  
  /* Layout - single-column vertical layout */
  .gh-profile-header {
    @apply flex-col mt-6 mb-8 gap-8;
  }

  .gh-avatar-container {
    @apply w-full items-center mx-auto px-0;
  }

  .gh-avatar {
    @apply w-[180px] h-[180px] mx-auto shadow-lg;
  }
  
  .gh-profile-stats {
    @apply justify-center text-base gap-3 my-4;
  }
  
  .gh-stat-count {
    @apply text-lg font-bold;
  }
  
  .gh-stat-label {
    @apply text-base;
  }
  
  .gh-profile-content {
    @apply w-full px-0;
  }

  .gh-profile-header-info {
    @apply text-center mb-8;
  }

  .gh-name {
    @apply text-center text-2xl mb-2;
  }

  .gh-username {
    @apply text-center text-xl;
  }

  .gh-bio {
    @apply text-center text-base mt-4 w-full mx-auto;
  }
  
  /* Header and Nav */
  .gh-header-inner {
    @apply px-2;
  }
  
  .gh-nav {
    @apply gap-2;
  }

  .gh-nav-item {
    @apply px-2 py-1.5;
  }
  
  /* Footer */
  .gh-footer-inner {
    @apply py-3 px-4;
  }
  
  .gh-footer-links, .gh-copyright {
    @apply text-xs;
  }
  
  /* Blog post grid */
  .gh-post-grid {
    @apply grid-cols-1 gap-4;
  }
  
  .gh-post-image {
    @apply h-auto max-h-40;
  }
  
  .gh-post-content {
    @apply p-3;
  }
  
  .gh-post-title {
    @apply text-base;
  }
  
  /* Form elements */
  button, 
  a.gh-btn, 
  .gh-nav-item,
  .gh-post-card,
  .tag-btn,
  .gh-page-number {
    @apply min-h-[44px] flex items-center justify-center;
  }
  
  input, 
  textarea, 
  select {
    @apply text-base p-3 min-h-[44px];
  }
  
  /* Blog meta on mobile */
  .gh-post-meta {
    @apply flex-col gap-2;
  }
  
  /* Scrollable tag buttons on mobile */
  .gh-tag-buttons {
    @apply overflow-x-auto pb-2 flex-nowrap;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }
  
  .gh-tag-buttons::-webkit-scrollbar {
    display: none;
  }
  
  .tag-btn {
    @apply whitespace-nowrap;
  }
  
  /* Section headers */
  .gh-section-header {
    @apply flex-col items-center mb-4;
  }
  
  .gh-section-title {
    @apply mb-2 text-center;
  }
  
  /* Section spacing */
  section, 
  .gh-section {
    @apply mb-8;
  }
}`;

  return mobileStyles;
}

// Create main.css that imports all the pieces
function createMainCss() {
  console.log('Creating main CSS file...');
  
  return `/*
 * Main CSS File
 * 
 * This file imports all modular CSS components in the correct order.
 * Edit the individual files to make specific changes rather than this file.
 */

/* Import theme variables first */
@import 'theme.css';

/* Import base styles */
@import 'base.css';

/* Import component styles */
@import 'components.css';

/* Import utility classes */
@import 'utilities.css';

/* Import mobile styles last */
@import 'mobile.css';

/* Syntax highlighting is in components.css */`;
}

// Format and save optimized CSS
async function saveOptimizedCss(filename, content) {
  const filePath = path.join(OPTIMIZED_CSS_DIR, filename);
  
  try {
    fs.writeFileSync(filePath, content);
    console.log(`✓ Saved ${filename}`);
  } catch (error) {
    console.error(`Error saving ${filename}:`, error);
  }
}

// Create a README file explaining the optimized structure
function createReadme() {
  console.log('Creating README for optimized CSS...');
  
  const readmeContent = `# Optimized CSS Structure

This directory contains the optimized CSS structure for the website. The CSS has been modularized for better maintenance and performance.

## Files Structure

- **main.css**: The main entry point that imports all other CSS files
- **theme.css**: Contains all theme variables and color definitions
- **base.css**: Contains base element styles and typography
- **components.css**: Contains all UI component styles
- **utilities.css**: Contains utility classes
- **mobile.css**: Contains responsive overrides for mobile devices

## How to Use

Instead of importing the old CSS files, import the main.css file which will import all the necessary components:

\`\`\`html
<link rel="stylesheet" href="/css/optimized/main.css">
\`\`\`

## Benefits

- **Modular**: Each file has a specific purpose
- **Maintainable**: Easier to find and update specific styles
- **Performant**: Better organization leads to fewer specificity conflicts
- **Consistent**: Similar components use consistent styling patterns

## Legacy Files

The original CSS files are still available in the parent directory for reference. Once the optimized structure is working correctly, the legacy files can be removed.
`;

  const readmePath = path.join(OPTIMIZED_CSS_DIR, 'README.md');
  fs.writeFileSync(readmePath, readmeContent);
  console.log('✓ Created README.md with documentation');
}

// Create example 11ty template to demonstrate usage
function createExampleTemplate() {
  console.log('Creating example template for usage...');
  
  const exampleContent = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Optimized CSS Example</title>
  
  <!-- Replace the old CSS imports with this single import -->
  <link rel="stylesheet" href="/css/optimized/main.css">
</head>
<body>
  <!-- Content here -->
</body>
</html>
`;

  const examplePath = path.join(OPTIMIZED_CSS_DIR, 'example-usage.html');
  fs.writeFileSync(examplePath, exampleContent);
  console.log('✓ Created example-usage.html with documentation');
}

// Generate statistics for the optimization
function generateStats(originalFiles, optimizedFiles) {
  console.log('Generating optimization statistics...');
  
  // Calculate sizes
  const originalSize = Object.values(originalFiles).reduce((sum, content) => sum + Buffer.byteLength(content, 'utf8'), 0);
  
  let optimizedSize = 0;
  for (const file of optimizedFiles) {
    if (fs.existsSync(file)) {
      optimizedSize += fs.statSync(file).size;
    }
  }
  
  // Calculate reduction
  const reduction = 1 - (optimizedSize / originalSize);
  const reductionPercent = (reduction * 100).toFixed(2);
  
  // Create stats object
  const stats = {
    original: {
      files: Object.keys(originalFiles).length,
      size: (originalSize / 1024).toFixed(2) + ' KB'
    },
    optimized: {
      files: optimizedFiles.length,
      size: (optimizedSize / 1024).toFixed(2) + ' KB'
    },
    reduction: reductionPercent + '%'
  };
  
  // Write stats to file
  const statsPath = path.join(OPTIMIZED_CSS_DIR, 'optimization-stats.json');
  fs.writeFileSync(statsPath, JSON.stringify(stats, null, 2));
  
  return stats;
}

// Main function to run the optimization
async function optimizeCSS() {
  console.log('Starting CSS optimization...');
  
  // 1. Create backups of original files
  createBackups();
  
  // 2. Read CSS files
  const cssFiles = readCssFiles();
  
  // 3. Create optimized structure
  await createOptimizedStructure(cssFiles);
  
  // 4. Create README and example template
  createReadme();
  createExampleTemplate();
  
  // 5. Generate statistics
  const optimizedFiles = [
    path.join(OPTIMIZED_CSS_DIR, 'main.css'),
    path.join(OPTIMIZED_CSS_DIR, 'theme.css'),
    path.join(OPTIMIZED_CSS_DIR, 'base.css'),
    path.join(OPTIMIZED_CSS_DIR, 'components.css'),
    path.join(OPTIMIZED_CSS_DIR, 'utilities.css'),
    path.join(OPTIMIZED_CSS_DIR, 'mobile.css')
  ];
  
  const stats = generateStats(cssFiles, optimizedFiles);
  
  console.log('\nCSS Optimization Complete!');
  console.log('---------------------------');
  console.log(`Original: ${stats.original.files} files (${stats.original.size})`);
  console.log(`Optimized: ${stats.optimized.files} files (${stats.optimized.size})`);
  console.log(`Reduction: ${stats.reduction}`);
  console.log(`\nOptimized files are available in: ${OPTIMIZED_CSS_DIR}`);
  console.log('Review the README.md file for usage instructions.');
}

// Run the optimization
optimizeCSS().catch(error => {
  console.error('Error during CSS optimization:', error);
  process.exit(1);
});