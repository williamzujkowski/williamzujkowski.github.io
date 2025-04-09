/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./_includes/**/*.{njk,md,js,css}",
    "./_layouts/**/*.{njk,md,js,css}",
    "./src/**/*.{njk,md,js,css}",
    "./src/_includes/**/*.{njk,md,js,css}",
    "./*.{njk,md,js,css}"
  ],
  darkMode: 'class', // Enable dark mode variant
  theme: {
    extend: {
      borderRadius: {
        'github': '6px',
      },
      // OKLCH color theme system
      // Base colors defined in OKLCH format for better color accuracy and accessibility
      colors: {
        // Primary color - GitHub green equivalent
        'primary': {
          DEFAULT: 'oklch(0.56 0.15 145)', // GitHub green
          50: 'oklch(0.92 0.05 145)',
          100: 'oklch(0.87 0.06 145)',
          200: 'oklch(0.82 0.08 145)',
          300: 'oklch(0.76 0.10 145)',
          400: 'oklch(0.66 0.12 145)',
          500: 'oklch(0.56 0.15 145)', // Base primary
          600: 'oklch(0.46 0.13 145)',
          700: 'oklch(0.36 0.11 145)',
          800: 'oklch(0.26 0.09 145)',
          900: 'oklch(0.16 0.07 145)',
          950: 'oklch(0.11 0.04 145)',
        },
        
        // Accent color - GitHub blue equivalent
        'accent': {
          DEFAULT: 'oklch(0.70 0.15 230)', // GitHub blue
          50: 'oklch(0.95 0.05 230)',
          100: 'oklch(0.92 0.07 230)',
          200: 'oklch(0.87 0.09 230)',
          300: 'oklch(0.82 0.11 230)',
          400: 'oklch(0.76 0.13 230)',
          500: 'oklch(0.70 0.15 230)', // Base accent
          600: 'oklch(0.60 0.13 230)',
          700: 'oklch(0.50 0.11 230)',
          800: 'oklch(0.40 0.09 230)',
          900: 'oklch(0.30 0.07 230)',
          950: 'oklch(0.20 0.05 230)',
        },
        
        // Alert/Status colors
        'success': 'oklch(0.56 0.15 145)', // Same as primary
        'warning': 'oklch(0.75 0.15 80)', // Yellow
        'danger': 'oklch(0.65 0.15 25)', // Red
        'info': 'oklch(0.70 0.15 230)', // Same as accent
        
        // UI Colors for dark theme
        'background': 'oklch(0.16 0.02 250)', // GitHub dark background
        'surface': 'oklch(0.20 0.02 250)', // GitHub dark surface
        'border': 'oklch(0.30 0.02 250)', // GitHub dark border
        'gray-light': 'oklch(0.25 0.02 250)', // GitHub dark container
        
        // Text Colors
        'text': 'oklch(0.93 0.02 250)', // Main text - bright for contrast
        'text-secondary': 'oklch(0.75 0.03 250)', // Secondary text
        'muted': 'oklch(0.65 0.02 250)', // Muted text
        
        // Legacy hover variants (will be migrated to theme variables)
        'primary-hover': 'oklch(0.62 0.16 145)', // Brighter primary for hover states
        'accent-hover': 'oklch(0.76 0.13 230)', // Brighter accent for hover states
        'secondary': 'oklch(0.75 0.03 250)' // Secondary text (same as text-secondary)
      },
      fontFamily: {
        'sans': ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Helvetica', 'Arial', 'sans-serif', 'Apple Color Emoji', 'Segoe UI Emoji'],
        'mono': ['SFMono-Regular', 'Consolas', 'Liberation Mono', 'Menlo', 'Courier', 'monospace'],
      },
      boxShadow: {
        'card': '0 0 0 1px var(--color-border)',
        'dropdown': '0 8px 24px rgba(1, 4, 9, 0.3)',
        'btn': '0 0 transparent',
        'btn-primary': '0 0 transparent',
        'md': '0 4px 6px -1px rgb(0 0 0 / 0.2), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
        'lg': '0 10px 15px -3px rgb(0 0 0 / 0.2), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
      },
      typography: {
        DEFAULT: {
          css: {
            maxWidth: '65ch',
            color: 'oklch(0.93 0.02 250)', // Text color
            a: {
              color: 'oklch(0.70 0.15 230)', // Accent color
              textDecoration: 'none',
              '&:hover': {
                color: 'oklch(0.76 0.13 230)', // Accent-400
                textDecoration: 'underline',
              },
            },
            strong: {
              color: 'oklch(0.98 0.005 250)', // White for maximum contrast
              fontWeight: '600',
            },
            h1: {
              color: 'oklch(0.98 0.005 250)', // White for maximum contrast
              fontWeight: '600',
            },
            h2: {
              color: 'oklch(0.98 0.005 250)', // White for maximum contrast
              fontWeight: '600',
            },
            h3: {
              color: 'oklch(0.98 0.005 250)', // White for maximum contrast
              fontWeight: '600',
            },
            h4: {
              color: 'oklch(0.98 0.005 250)', // White for maximum contrast
              fontWeight: '600',
            },
            code: {
              color: 'oklch(0.93 0.02 250)', // Text color
              backgroundColor: 'oklch(0.25 0.02 250)', // Gray-light
              borderRadius: '6px',
              padding: '0.2em 0.4em',
              border: '1px solid oklch(0.30 0.02 250)', // Border
            },
            blockquote: {
              color: 'oklch(0.75 0.03 250)', // Text-secondary
              borderLeftColor: 'oklch(0.30 0.02 250)', // Border
            },
            pre: {
              backgroundColor: 'oklch(0.25 0.02 250)', // Gray-light
            },
            thead: {
              color: 'oklch(0.98 0.005 250)', // White for maximum contrast
            },
            'ol > li::before': {
              color: 'oklch(0.75 0.03 250)', // Text-secondary
            },
            'ul > li::before': {
              backgroundColor: 'oklch(0.75 0.03 250)', // Text-secondary
            },
          },
        },
      },
      spacing: {
        '72': '18rem',
        '84': '21rem',
        '96': '24rem',
      },
      screens: {
        'xs': '475px',
      },
      transitionProperty: {
        'height': 'height',
        'spacing': 'margin, padding',
      },
      animation: {
        'spin-slow': 'spin 3s linear infinite',
        'bounce-slow': 'bounce 3s ease-in-out infinite',
        'fade-in': 'fadeIn 0.5s ease-out forwards',
        'slide-up': 'slideUp 0.6s ease-out forwards',
        'pulse-soft': 'pulseSoft 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 3s ease-in-out infinite',
      },
      backdropBlur: {
        'xs': '2px',
      },
      keyframes: {
        pulseSoft: {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0.8 },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
      },
      aspectRatio: {
        'auto': 'auto',
        'square': '1 / 1',
        'video': '16 / 9',
        'blog': '2 / 1',
        'portrait': '3 / 4',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/container-queries'),
    function({ addUtilities }) {
      const newUtilities = {
        '.bg-theme-primary-10': { backgroundColor: 'color-mix(in oklch, var(--color-primary), transparent 90%)' },
        '.bg-theme-primary-20': { backgroundColor: 'color-mix(in oklch, var(--color-primary), transparent 80%)' },
        '.bg-theme-primary-30': { backgroundColor: 'color-mix(in oklch, var(--color-primary), transparent 70%)' },
        '.bg-theme-accent-10': { backgroundColor: 'color-mix(in oklch, var(--color-accent), transparent 90%)' },
        '.bg-theme-accent-20': { backgroundColor: 'color-mix(in oklch, var(--color-accent), transparent 80%)' },
        '.bg-theme-accent-30': { backgroundColor: 'color-mix(in oklch, var(--color-accent), transparent 70%)' },
        '.text-theme-primary': { color: 'var(--color-primary)' },
        '.text-theme-accent': { color: 'var(--color-accent)' },
        '.text-theme-background': { color: 'var(--color-background)' },
        '.text-theme-surface': { color: 'var(--color-surface)' },
        '.text-theme-border': { color: 'var(--color-border)' },
        '.text-theme-text': { color: 'var(--color-text)' },
        '.text-theme-text-secondary': { color: 'var(--color-text-secondary)' },
        '.text-theme-muted': { color: 'var(--color-muted)' },
        '.border-theme-primary': { borderColor: 'var(--color-primary)' },
        '.border-theme-accent': { borderColor: 'var(--color-accent)' },
        '.border-theme-border': { borderColor: 'var(--color-border)' },
        '.bg-theme-primary': { backgroundColor: 'var(--color-primary)' },
        '.bg-theme-accent': { backgroundColor: 'var(--color-accent)' },
        '.bg-theme-background': { backgroundColor: 'var(--color-background)' },
        '.bg-theme-surface': { backgroundColor: 'var(--color-surface)' },
        '.bg-theme-gray-light': { backgroundColor: 'var(--color-gray-light)' },
        '.hover\\:bg-theme-primary:hover': { backgroundColor: 'var(--color-primary)' },
        '.hover\\:bg-theme-accent:hover': { backgroundColor: 'var(--color-accent)' },
        '.hover\\:text-theme-primary:hover': { color: 'var(--color-primary)' },
        '.hover\\:text-theme-accent:hover': { color: 'var(--color-accent)' },
        '.hover\\:text-accent-hover:hover': { color: 'oklch(0.76 0.13 230)' }, /* For legacy compatibility */
        '.hover\\:text-theme-success:hover': { color: 'var(--color-success)' },
        '.hover\\:text-theme-warning:hover': { color: 'var(--color-warning)' },
        '.hover\\:text-theme-danger:hover': { color: 'var(--color-danger)' },
        '.hover\\:text-theme-info:hover': { color: 'var(--color-info)' },
        '.hover\\:border-theme-primary:hover': { borderColor: 'var(--color-primary)' },
        '.hover\\:border-theme-accent:hover': { borderColor: 'var(--color-accent)' },
        '.hover\\:border-theme-success:hover': { borderColor: 'var(--color-success)' },
        '.hover\\:border-theme-warning:hover': { borderColor: 'var(--color-warning)' },
        '.hover\\:border-theme-danger:hover': { borderColor: 'var(--color-danger)' },
        '.hover\\:border-theme-info:hover': { borderColor: 'var(--color-info)' },
        '.ring-theme-accent': { '--tw-ring-color': 'var(--color-accent)' },
        '.border-theme-accent': { borderColor: 'var(--color-accent)' },
      }
      addUtilities(newUtilities)
    }
  ],
  corePlugins: {
    container: false, // Disable default container to use custom one below
  },
};