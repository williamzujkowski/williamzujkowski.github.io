---
layout: page
title: Style Guide
description: Visual design system and component library for williamzujkowski.github.io. Typography, colors, components, and patterns used throughout the site.
permalink: /style-guide/
eleventyNavigation:
  key: Style Guide
  parent: Resources
  order: 10
---

# Style Guide

This style guide documents the visual design system used throughout this website. It serves as a reference for maintaining consistency and as a showcase of available components.

## Colors

### Primary Palette

<div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
  <div>
    <div class="h-24 bg-primary-50 rounded-lg mb-2"></div>
    <p class="text-sm font-medium">Primary 50</p>
    <p class="text-xs text-gray-600 dark:text-gray-400">#eff6ff</p>
  </div>
  <div>
    <div class="h-24 bg-primary-100 rounded-lg mb-2"></div>
    <p class="text-sm font-medium">Primary 100</p>
    <p class="text-xs text-gray-600 dark:text-gray-400">#dbeafe</p>
  </div>
  <div>
    <div class="h-24 bg-primary-200 rounded-lg mb-2"></div>
    <p class="text-sm font-medium">Primary 200</p>
    <p class="text-xs text-gray-600 dark:text-gray-400">#bfdbfe</p>
  </div>
  <div>
    <div class="h-24 bg-primary-300 rounded-lg mb-2"></div>
    <p class="text-sm font-medium">Primary 300</p>
    <p class="text-xs text-gray-600 dark:text-gray-400">#93c5fd</p>
  </div>
  <div>
    <div class="h-24 bg-primary-400 rounded-lg mb-2"></div>
    <p class="text-sm font-medium">Primary 400</p>
    <p class="text-xs text-gray-600 dark:text-gray-400">#60a5fa</p>
  </div>
  <div>
    <div class="h-24 bg-primary-500 rounded-lg mb-2"></div>
    <p class="text-sm font-medium text-white">Primary 500</p>
    <p class="text-xs text-gray-600 dark:text-gray-400">#3b82f6</p>
  </div>
  <div>
    <div class="h-24 bg-primary-600 rounded-lg mb-2"></div>
    <p class="text-sm font-medium text-white">Primary 600</p>
    <p class="text-xs text-gray-600 dark:text-gray-400">#2563eb</p>
  </div>
  <div>
    <div class="h-24 bg-primary-700 rounded-lg mb-2"></div>
    <p class="text-sm font-medium text-white">Primary 700</p>
    <p class="text-xs text-gray-600 dark:text-gray-400">#1d4ed8</p>
  </div>
</div>

### Gray Scale

<div class="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
  <div>
    <div class="h-24 bg-gray-50 rounded-lg mb-2 border"></div>
    <p class="text-sm font-medium">Gray 50</p>
  </div>
  <div>
    <div class="h-24 bg-gray-100 rounded-lg mb-2"></div>
    <p class="text-sm font-medium">Gray 100</p>
  </div>
  <div>
    <div class="h-24 bg-gray-200 rounded-lg mb-2"></div>
    <p class="text-sm font-medium">Gray 200</p>
  </div>
  <div>
    <div class="h-24 bg-gray-300 rounded-lg mb-2"></div>
    <p class="text-sm font-medium">Gray 300</p>
  </div>
  <div>
    <div class="h-24 bg-gray-400 rounded-lg mb-2"></div>
    <p class="text-sm font-medium">Gray 400</p>
  </div>
  <div>
    <div class="h-24 bg-gray-500 rounded-lg mb-2"></div>
    <p class="text-sm font-medium text-white">Gray 500</p>
  </div>
  <div>
    <div class="h-24 bg-gray-600 rounded-lg mb-2"></div>
    <p class="text-sm font-medium text-white">Gray 600</p>
  </div>
  <div>
    <div class="h-24 bg-gray-700 rounded-lg mb-2"></div>
    <p class="text-sm font-medium text-white">Gray 700</p>
  </div>
  <div>
    <div class="h-24 bg-gray-800 rounded-lg mb-2"></div>
    <p class="text-sm font-medium text-white">Gray 800</p>
  </div>
  <div>
    <div class="h-24 bg-gray-900 rounded-lg mb-2"></div>
    <p class="text-sm font-medium text-white">Gray 900</p>
  </div>
</div>

### Semantic Colors

<div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
  <div>
    <div class="h-24 bg-green-500 rounded-lg mb-2"></div>
    <p class="text-sm font-medium text-white">Success</p>
    <p class="text-xs text-gray-600 dark:text-gray-400">Green 500</p>
  </div>
  <div>
    <div class="h-24 bg-blue-500 rounded-lg mb-2"></div>
    <p class="text-sm font-medium text-white">Info</p>
    <p class="text-xs text-gray-600 dark:text-gray-400">Blue 500</p>
  </div>
  <div>
    <div class="h-24 bg-yellow-500 rounded-lg mb-2"></div>
    <p class="text-sm font-medium">Warning</p>
    <p class="text-xs text-gray-600 dark:text-gray-400">Yellow 500</p>
  </div>
  <div>
    <div class="h-24 bg-red-500 rounded-lg mb-2"></div>
    <p class="text-sm font-medium text-white">Error</p>
    <p class="text-xs text-gray-600 dark:text-gray-400">Red 500</p>
  </div>
</div>

## Typography

### Font Family

<div class="space-y-4 mb-8">
  <div class="p-6 bg-gray-50 dark:bg-gray-800 rounded-lg">
    <p class="font-sans text-lg mb-2">Inter (Primary Font)</p>
    <p class="text-gray-600 dark:text-gray-400">ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyz<br>1234567890</p>
  </div>
  <div class="p-6 bg-gray-50 dark:bg-gray-800 rounded-lg">
    <p class="font-mono text-lg mb-2">Monospace (Code)</p>
    <p class="font-mono text-gray-600 dark:text-gray-400">ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyz<br>1234567890</p>
  </div>
</div>

### Headings

<div class="space-y-6 mb-8">
  <div>
    <h1 class="text-5xl font-bold text-gray-900 dark:text-gray-100">Heading 1</h1>
    <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">text-5xl font-bold</p>
  </div>
  <div>
    <h2 class="text-4xl font-bold text-gray-900 dark:text-gray-100">Heading 2</h2>
    <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">text-4xl font-bold</p>
  </div>
  <div>
    <h3 class="text-3xl font-bold text-gray-900 dark:text-gray-100">Heading 3</h3>
    <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">text-3xl font-bold</p>
  </div>
  <div>
    <h4 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">Heading 4</h4>
    <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">text-2xl font-semibold</p>
  </div>
  <div>
    <h5 class="text-xl font-semibold text-gray-900 dark:text-gray-100">Heading 5</h5>
    <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">text-xl font-semibold</p>
  </div>
  <div>
    <h6 class="text-lg font-semibold text-gray-900 dark:text-gray-100">Heading 6</h6>
    <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">text-lg font-semibold</p>
  </div>
</div>

### Body Text

<div class="space-y-4 mb-8">
  <div>
    <p class="text-lg text-gray-900 dark:text-gray-100">Large body text for emphasis and lead paragraphs.</p>
    <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">text-lg</p>
  </div>
  <div>
    <p class="text-base text-gray-900 dark:text-gray-100">Regular body text for general content and paragraphs.</p>
    <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">text-base (default)</p>
  </div>
  <div>
    <p class="text-sm text-gray-900 dark:text-gray-100">Small body text for captions and secondary information.</p>
    <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">text-sm</p>
  </div>
  <div>
    <p class="text-xs text-gray-900 dark:text-gray-100">Extra small text for labels and metadata.</p>
    <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">text-xs</p>
  </div>
</div>

## Components

### Buttons

<div class="space-y-4 mb-8">
  <div class="flex flex-wrap gap-4">
    <button class="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
      Primary Button
    </button>
    <button class="px-6 py-3 bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors">
      Secondary Button
    </button>
    <button class="px-6 py-3 border-2 border-primary-600 text-primary-600 dark:text-primary-400 rounded-lg hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors">
      Outline Button
    </button>
    <button class="px-6 py-3 text-primary-600 dark:text-primary-400 hover:underline transition-colors">
      Text Button
    </button>
  </div>
  <div class="flex flex-wrap gap-4">
    <button class="px-4 py-2 bg-primary-600 text-white text-sm rounded-lg hover:bg-primary-700 transition-colors">
      Small Button
    </button>
    <button class="px-8 py-4 bg-primary-600 text-white text-lg rounded-lg hover:bg-primary-700 transition-colors">
      Large Button
    </button>
  </div>
</div>

### Cards

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
  <div class="glass dark:glass-dark rounded-2xl p-6">
    <h3 class="text-xl font-semibold mb-2">Glass Card</h3>
    <p class="text-gray-600 dark:text-gray-400">This is a glass morphism card with backdrop blur effect.</p>
  </div>
  <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-6">
    <h3 class="text-xl font-semibold mb-2">Standard Card</h3>
    <p class="text-gray-600 dark:text-gray-400">This is a standard card with solid background.</p>
  </div>
</div>

### Badges & Tags

<div class="flex flex-wrap gap-2 mb-8">
  <span class="inline-flex items-center rounded-full bg-gray-100 dark:bg-gray-800 px-3 py-1 text-sm font-medium text-gray-700 dark:text-gray-300">
    Default
  </span>
  <span class="inline-flex items-center rounded-full bg-primary-100 dark:bg-primary-900/20 px-3 py-1 text-sm font-medium text-primary-700 dark:text-primary-300">
    Primary
  </span>
  <span class="inline-flex items-center rounded-full bg-green-100 dark:bg-green-900/20 px-3 py-1 text-sm font-medium text-green-700 dark:text-green-300">
    Success
  </span>
  <span class="inline-flex items-center rounded-full bg-yellow-100 dark:bg-yellow-900/20 px-3 py-1 text-sm font-medium text-yellow-700 dark:text-yellow-300">
    Warning
  </span>
  <span class="inline-flex items-center rounded-full bg-red-100 dark:bg-red-900/20 px-3 py-1 text-sm font-medium text-red-700 dark:text-red-300">
    Error
  </span>
</div>

### Alerts

<div class="space-y-4 mb-8">
  <div class="rounded-lg bg-blue-50 dark:bg-blue-900/20 p-4">
    <p class="text-blue-800 dark:text-blue-200">
      <strong>Info:</strong> This is an informational alert message.
    </p>
  </div>
  <div class="rounded-lg bg-green-50 dark:bg-green-900/20 p-4">
    <p class="text-green-800 dark:text-green-200">
      <strong>Success:</strong> This is a success alert message.
    </p>
  </div>
  <div class="rounded-lg bg-yellow-50 dark:bg-yellow-900/20 p-4">
    <p class="text-yellow-800 dark:text-yellow-200">
      <strong>Warning:</strong> This is a warning alert message.
    </p>
  </div>
  <div class="rounded-lg bg-red-50 dark:bg-red-900/20 p-4">
    <p class="text-red-800 dark:text-red-200">
      <strong>Error:</strong> This is an error alert message.
    </p>
  </div>
</div>

### Forms

<div class="max-w-md mb-8">
  <form class="space-y-4">
    <div>
      <label for="text-input" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
        Text Input
      </label>
      <input type="text" id="text-input" class="w-full px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors" placeholder="Enter text...">
    </div>
    <div>
      <label for="textarea" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
        Textarea
      </label>
      <textarea id="textarea" rows="3" class="w-full px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors" placeholder="Enter message..."></textarea>
    </div>
    <div>
      <label for="select" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
        Select
      </label>
      <select id="select" class="w-full px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors">
        <option>Option 1</option>
        <option>Option 2</option>
        <option>Option 3</option>
      </select>
    </div>
    <div class="flex items-center">
      <input type="checkbox" id="checkbox" class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded">
      <label for="checkbox" class="ml-2 text-sm text-gray-700 dark:text-gray-300">
        Checkbox option
      </label>
    </div>
  </form>
</div>

### Code Blocks

<div class="space-y-4 mb-8">
  <div>
    <p class="text-sm font-medium mb-2">Inline code:</p>
    <p>Use <code class="bg-gray-100 dark:bg-gray-800 px-1.5 py-0.5 rounded text-sm">inline code</code> for short snippets.</p>
  </div>
  <div>
    <p class="text-sm font-medium mb-2">Code block:</p>
    <pre class="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto"><code class="language-javascript">// JavaScript example
function greet(name) {
  return `Hello, ${name}!`;
}
console.log(greet('World'));</code></pre>
  </div>
</div>

### Tables

<div class="overflow-x-auto mb-8">
  <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
    <thead>
      <tr>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Name</th>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Type</th>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Description</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
      <tr>
        <td class="px-6 py-4 whitespace-nowrap text-sm">Primary</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm">Color</td>
        <td class="px-6 py-4 text-sm">Main brand color used for CTAs and links</td>
      </tr>
      <tr>
        <td class="px-6 py-4 whitespace-nowrap text-sm">Inter</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm">Font</td>
        <td class="px-6 py-4 text-sm">Primary typeface for all text content</td>
      </tr>
    </tbody>
  </table>
</div>

## Animations

### Fade In Up

<div class="space-y-4 mb-8">
  <div class="animate-fade-in-up bg-gray-100 dark:bg-gray-800 p-4 rounded-lg">
    <p>This element fades in and moves up</p>
  </div>
  <div class="animate-fade-in-up animation-delay-200 bg-gray-100 dark:bg-gray-800 p-4 rounded-lg">
    <p>This element has a 200ms delay</p>
  </div>
  <div class="animate-fade-in-up animation-delay-400 bg-gray-100 dark:bg-gray-800 p-4 rounded-lg">
    <p>This element has a 400ms delay</p>
  </div>
</div>

### Hover Effects

<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
  <div class="p-6 bg-gray-100 dark:bg-gray-800 rounded-lg hover:shadow-lg transition-shadow cursor-pointer">
    <p class="font-medium">Shadow on Hover</p>
  </div>
  <div class="p-6 bg-gray-100 dark:bg-gray-800 rounded-lg hover:scale-105 transition-transform cursor-pointer">
    <p class="font-medium">Scale on Hover</p>
  </div>
  <div class="p-6 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors cursor-pointer">
    <p class="font-medium">Color Change on Hover</p>
  </div>
</div>

## Special Effects

### Gradient Text

<div class="space-y-4 mb-8">
  <h2 class="text-4xl font-bold gradient-text">Gradient Text Effect</h2>
  <p class="text-gray-600 dark:text-gray-400">Used for special emphasis and branding</p>
</div>

### Glass Morphism

<div class="p-8 glass dark:glass-dark rounded-2xl mb-8">
  <h3 class="text-2xl font-bold mb-4">Glass Effect</h3>
  <p class="text-gray-700 dark:text-gray-300">This component uses backdrop blur and transparency for a modern glass effect.</p>
</div>

## Spacing

<div class="space-y-4 mb-8">
  <div class="bg-gray-100 dark:bg-gray-800 rounded">
    <div class="p-2 bg-primary-200 dark:bg-primary-800">p-2 (0.5rem)</div>
  </div>
  <div class="bg-gray-100 dark:bg-gray-800 rounded">
    <div class="p-4 bg-primary-200 dark:bg-primary-800">p-4 (1rem)</div>
  </div>
  <div class="bg-gray-100 dark:bg-gray-800 rounded">
    <div class="p-6 bg-primary-200 dark:bg-primary-800">p-6 (1.5rem)</div>
  </div>
  <div class="bg-gray-100 dark:bg-gray-800 rounded">
    <div class="p-8 bg-primary-200 dark:bg-primary-800">p-8 (2rem)</div>
  </div>
</div>

## Responsive Design

This site uses a mobile-first approach with the following breakpoints:

- **sm:** 640px and up
- **md:** 768px and up
- **lg:** 1024px and up
- **xl:** 1280px and up
- **2xl:** 1536px and up

Example usage: `text-base md:text-lg lg:text-xl`

## Accessibility

- All interactive elements have focus states
- Color contrast ratios meet WCAG AA standards
- Semantic HTML elements used throughout
- ARIA labels where appropriate
- Keyboard navigation support

## Dark Mode

The site supports automatic dark mode based on system preferences. Users can also manually toggle between light and dark themes using the moon/sun icon in the header.

Classes are applied conditionally using the `dark:` prefix in Tailwind CSS.