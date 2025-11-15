# Tailwind CSS Customization Guide

**Version:** 1.0.0  
**Last Updated:** 2024-01-24  
**Status:** Active  
**Category:** Guide

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Theme Customization](#theme-customization)
3. [Color Palette](#color-palette)
4. [Typography](#typography)
5. [Dark Mode](#dark-mode)
6. [Custom Components](#custom-components)
7. [Performance Optimization](#performance-optimization)
8. [Common Patterns](#common-patterns)

---

## Quick Start

### Modifying Tailwind Configuration

The main configuration file is `tailwind.config.js`:

```javascript
module.exports = {
  content: ['./src/**/*.{html,njk,md,js}'],
  darkMode: 'class',
  theme: {
    extend: {
      // Your customizations here
    }
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ]
}
```

### Development Workflow

1. Make changes to `tailwind.config.js`
2. CSS will automatically rebuild if using `npm run serve`
3. For manual rebuild: `npm run build:css`

---

## Theme Customization

### Extending vs Replacing

```javascript
theme: {
  // This REPLACES all Tailwind colors
  colors: {
    primary: '#0066cc',
  },
  
  extend: {
    // This ADDS to existing Tailwind colors
    colors: {
      primary: {
        50: '#e6f0ff',
        // ... more shades
      }
    }
  }
}
```

**Best Practice:** Always use `extend` unless you need to completely replace a theme value.

---

## Color Palette

### Current Primary Colors

```javascript
extend: {
  colors: {
    primary: {
      50: '#eff6ff',
      100: '#dbeafe',
      200: '#bfdbfe',
      300: '#93bbfd',
      400: '#60a5fa',
      500: '#3b82f6',
      600: '#2563eb',
      700: '#1d4ed8',
      800: '#1e40af',
      900: '#1e3a8a',
      950: '#172554'
    }
  }
}
```

### Adding Custom Colors

```javascript
extend: {
  colors: {
    brand: {
      twitter: '#1DA1F2',
      github: '#181717',
      linkedin: '#0A66C2'
    },
    accent: {
      warning: '#F59E0B',
      error: '#EF4444',
      success: '#10B981'
    }
  }
}
```

### Using Custom Colors

```html
<div class="bg-brand-twitter text-white">Twitter Blue</div>
<div class="border-accent-warning">Warning Border</div>
<p class="text-primary-600 dark:text-primary-400">Primary Text</p>
```

---

## Typography

### Customizing Prose Styles

The Typography plugin provides prose classes. Customize them:

```javascript
extend: {
  typography: (theme) => ({
    DEFAULT: {
      css: {
        color: theme('colors.gray.900'),
        a: {
          color: theme('colors.primary.600'),
          '&:hover': {
            color: theme('colors.primary.700'),
          },
        },
        'code::before': {
          content: '""',
        },
        'code::after': {
          content: '""',
        },
      },
    },
    invert: {
      css: {
        color: theme('colors.gray.100'),
        a: {
          color: theme('colors.primary.400'),
          '&:hover': {
            color: theme('colors.primary.300'),
          },
        },
      },
    },
  }),
}
```

### Custom Font Family

```javascript
extend: {
  fontFamily: {
    sans: ['Inter', ...defaultTheme.fontFamily.sans],
    mono: ['Fira Code', ...defaultTheme.fontFamily.mono],
    display: ['Playfair Display', 'serif'],
  }
}
```

Usage:
```html
<h1 class="font-display">Elegant Heading</h1>
<code class="font-mono">monospace code</code>
```

---

## Dark Mode

### Current Implementation

Dark mode uses class-based strategy with system preference detection:

```javascript
darkMode: 'class', // Enables .dark class on <html>
```

### Dark Mode Utilities

```html
<!-- Text that changes in dark mode -->
<p class="text-gray-900 dark:text-gray-100">Adaptive text</p>

<!-- Background that changes -->
<div class="bg-white dark:bg-gray-900">Adaptive background</div>

<!-- Complex dark mode styling -->
<button class="bg-primary-600 hover:bg-primary-700 
               dark:bg-primary-500 dark:hover:bg-primary-400">
  Button
</button>
```

### Custom Dark Mode Colors

```javascript
extend: {
  colors: {
    // Surface colors for dark mode
    surface: {
      light: '#ffffff',
      dark: '#1a1a1a',
    }
  }
}
```

---

## Custom Components

### Adding to CSS

In `src/assets/css/tailwind.css`:

```css
@layer components {
  /* Buttons */
  .btn {
    @apply px-4 py-2 rounded-lg font-medium transition-colors duration-200;
  }
  
  .btn-primary {
    @apply btn bg-primary-600 text-white hover:bg-primary-700 
           dark:bg-primary-500 dark:hover:bg-primary-400;
  }
  
  .btn-secondary {
    @apply btn bg-gray-200 text-gray-900 hover:bg-gray-300 
           dark:bg-gray-700 dark:text-gray-100 dark:hover:bg-gray-600;
  }
  
  /* Cards */
  .card {
    @apply rounded-lg border border-gray-200 dark:border-gray-700 
           bg-white dark:bg-gray-800 p-6 shadow-sm;
  }
  
  .card-hover {
    @apply card hover:shadow-lg transition-shadow duration-200;
  }
  
  /* Glass effect */
  .glass {
    @apply bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl;
  }
}

@layer utilities {
  /* Text gradient */
  .text-gradient {
    @apply bg-linear-to-r from-primary-600 to-primary-400 
           bg-clip-text text-transparent;
  }
  
  /* Glow effect */
  .glow {
    @apply shadow-lg shadow-primary-500/25;
  }
}
```

### Using Custom Components

```html
<button class="btn-primary">Primary Button</button>
<button class="btn-secondary">Secondary Button</button>

<div class="card-hover">
  <h3 class="text-gradient">Gradient Heading</h3>
  <p>Card content with hover effect</p>
</div>

<nav class="glass sticky top-0">
  Glass navigation bar
</nav>
```

---

## Performance Optimization

### 1. PurgeCSS Configuration

Tailwind automatically removes unused CSS in production:

```javascript
content: [
  './src/**/*.{html,njk,md,js}',
  './.eleventy.js', // If you use classes in config
],
```

### 2. Optimize for Production

```javascript
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
    ...(process.env.NODE_ENV === 'production' ? { 
      cssnano: {
        preset: 'default',
      }
    } : {})
  }
}
```

### 3. Selective Imports

For very large sites, consider selective plugin imports:

```javascript
// Only include what you need
plugins: [
  require('@tailwindcss/typography'),
  // require('@tailwindcss/forms'), // Commented if not using forms
]
```

---

## Common Patterns

### Responsive Design

```html
<!-- Mobile-first approach -->
<div class="text-sm md:text-base lg:text-lg xl:text-xl">
  Responsive text size
</div>

<!-- Hide/show at breakpoints -->
<nav class="hidden md:block">Desktop navigation</nav>
<button class="md:hidden">Mobile menu</button>

<!-- Grid layouts -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <!-- Grid items -->
</div>
```

### Animation Classes

```javascript
extend: {
  animation: {
    'fade-in': 'fadeIn 0.5s ease-in-out',
    'slide-up': 'slideUp 0.3s ease-out',
  },
  keyframes: {
    fadeIn: {
      '0%': { opacity: '0' },
      '100%': { opacity: '1' },
    },
    slideUp: {
      '0%': { transform: 'translateY(10px)', opacity: '0' },
      '100%': { transform: 'translateY(0)', opacity: '1' },
    },
  },
}
```

### State Variants

```html
<!-- Focus states -->
<input class="focus:ring-2 focus:ring-primary-500 focus:border-primary-500">

<!-- Group hover -->
<div class="group">
  <h3 class="group-hover:text-primary-600">Hover the parent</h3>
  <p class="group-hover:translate-x-1 transition-transform">I move!</p>
</div>

<!-- Peer states -->
<input type="checkbox" class="peer" id="toggle">
<label for="toggle" class="peer-checked:text-primary-600">
  Changes when checkbox is checked
</label>
```

### Container Queries

```html
<!-- Responsive container -->
<div class="container mx-auto px-4 sm:px-6 lg:px-8">
  <!-- Content with consistent padding -->
</div>

<!-- Max-width wrapper -->
<article class="max-w-prose mx-auto">
  <!-- Readable content width -->
</article>
```

---

## Best Practices

1. **Use Semantic Names**: Instead of `bg-blue-500`, create `bg-primary-500`
2. **Consistent Spacing**: Stick to Tailwind's spacing scale
3. **Avoid Arbitrary Values**: Use `p-4` not `p-[17px]`
4. **Component Extraction**: Repeat patterns → extract to @layer components
5. **Dark Mode First**: Design with both modes in mind
6. **Performance**: Keep an eye on CSS file size
7. **Accessibility**: Use focus states and proper contrast ratios

---

## Debugging Tips

### See All Generated CSS

```bash
# Generate full CSS for inspection
npx tailwindcss -i ./src/assets/css/tailwind.css -o ./debug.css
```

### Check Final Bundle Size

```bash
# After production build
ls -lh _site/assets/css/main.css
```

### Useful VS Code Extensions

- **Tailwind CSS IntelliSense**: Autocomplete and hover previews
- **Headwind**: Sorts Tailwind classes automatically

---

## Resources

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Tailwind UI Patterns](https://tailwindui.com/components) (paid)
- [Tailwind Play](https://play.tailwindcss.com/) - Online playground
- [Heroicons](https://heroicons.com/) - Icons by Tailwind team
- [Tailwind Color Generator](https://uicolors.app/create) - Generate color scales

---

## Related Documentation

- [Content Guide](CONTENT_GUIDE.md) - Using Tailwind in content
- [README.md](../../README.md) - Project overview
- [CLAUDE.md](../../CLAUDE.md) - AI assistance for Tailwind tasks