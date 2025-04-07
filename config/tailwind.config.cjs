/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./_includes/**/*.{njk,md,js}",
    "./_layouts/**/*.{njk,md,js}",
    "./src/**/*.{njk,md,js}",
    "./src/_includes/**/*.{njk,md,js}",
    "./*.{njk,md,js}"
  ],
  darkMode: 'class', // Enable dark mode variant
  theme: {
    extend: {
      borderRadius: {
        'github': '6px',
      },
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
        'md': '0 4px 6px -1px rgb(0 0 0 / 0.2), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
        'lg': '0 10px 15px -3px rgb(0 0 0 / 0.2), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
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
  ],
  corePlugins: {
    container: false, // Disable default container to use custom one below
  },
};