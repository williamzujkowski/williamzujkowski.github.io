/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./_includes/**/*.{njk,md,js}",
    "./_layouts/**/*.{njk,md,js}",
    "./src/**/*.{njk,md,js}",
    "./src/_includes/**/*.{njk,md,js}",
    "./*.{njk,md,js}"
  ],
  theme: {
    extend: {
      colors: {
        // GitHub-inspired dark mode color scheme with enhanced contrast
        'primary': '#2ea043', // GitHub Green (dark) - brightened
        'primary-hover': '#3fb950',
        'secondary': '#a3aab3', // Secondary text - brightened for better contrast
        'accent': '#79c0ff', // GitHub blue (dark) - brightened
        'accent-hover': '#a5d6ff',
        'background': '#0d1117', // GitHub dark background
        'surface': '#161b22', // GitHub dark surface
        'border': '#30363d', // GitHub dark border
        'text': '#e6edf3', // Text color - brightened for better contrast
        'text-secondary': '#a3aab3', // Secondary text - brightened
        'gray-light': '#21262d', 
        'danger': '#ff7b72', // GitHub red (dark) - brightened
        'warning': '#f0b83e', // GitHub yellow (dark) - brightened
        'muted': '#a3aab3', // Muted text - brightened
      },
      fontFamily: {
        'sans': ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Helvetica', 'Arial', 'sans-serif', 'Apple Color Emoji', 'Segoe UI Emoji'],
        'mono': ['SFMono-Regular', 'Consolas', 'Liberation Mono', 'Menlo', 'Courier', 'monospace'],
      },
      boxShadow: {
        'card': '0 0 0 1px #30363d',
        'dropdown': '0 8px 24px rgba(1, 4, 9, 0.3)',
        'btn': '0 0 transparent',
        'btn-primary': '0 0 transparent',
      },
      borderRadius: {
        'github': '6px',
      },
      typography: {
        DEFAULT: {
          css: {
            maxWidth: '65ch',
            color: '#e6edf3', // Brightened for better contrast
            a: {
              color: '#79c0ff', // Brightened for better contrast
              textDecoration: 'none',
              '&:hover': {
                textDecoration: 'underline',
              },
            },
            strong: {
              color: '#ffffff', // White for maximum contrast
              fontWeight: '600',
            },
            h1: {
              color: '#ffffff', // White for maximum contrast
              fontWeight: '600',
            },
            h2: {
              color: '#ffffff', // White for maximum contrast
              fontWeight: '600',
            },
            h3: {
              color: '#ffffff', // White for maximum contrast
              fontWeight: '600',
            },
            h4: {
              color: '#ffffff', // White for maximum contrast
              fontWeight: '600',
            },
            code: {
              color: '#e6edf3', // Brightened for better contrast
              backgroundColor: '#21262d', // Slightly lighter for better contrast
              borderRadius: '6px',
              padding: '0.2em 0.4em',
              border: '1px solid #30363d',
            },
            blockquote: {
              color: '#a3aab3', // Brightened for better contrast
              borderLeftColor: '#30363d',
            },
            pre: {
              backgroundColor: '#21262d', // Slightly lighter for better contrast
            },
            thead: {
              color: '#ffffff', // White for maximum contrast
            },
            'ol > li::before': {
              color: '#a3aab3', // Brightened for better contrast
            },
            'ul > li::before': {
              backgroundColor: '#a3aab3', // Brightened for better contrast
            },
          },
        },
      },
    },
  },
  plugins: [],
};