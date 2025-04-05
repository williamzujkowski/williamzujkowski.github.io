/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./_includes/**/*.{njk,md,js}",
    "./_layouts/**/*.{njk,md,js}",
    "./src/**/*.{njk,md,js}",
    "./src/_includes/**/*.{njk,md,js}",
    "./*.{njk,md,js}"
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // GitHub-inspired color scheme
        'primary': '#2da44e', // GitHub Green
        'primary-hover': '#2c974b',
        'secondary': '#6e7781', // GitHub secondary text
        'accent': '#0969da', // GitHub blue
        'accent-hover': '#0860C7',
        'background': '#ffffff', // White
        'surface': '#f6f8fa', // GitHub light gray background
        'border': '#d0d7de', // GitHub border color
        'text': '#24292f', // GitHub text color
        'text-secondary': '#57606a', // GitHub secondary text
        'gray-light': '#eaeef2', 
        'danger': '#cf222e', // GitHub red
        'warning': '#bf8700', // GitHub yellow
        'muted': '#6e7781', // Muted text
      },
      fontFamily: {
        'sans': ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Helvetica', 'Arial', 'sans-serif', 'Apple Color Emoji', 'Segoe UI Emoji'],
        'mono': ['SFMono-Regular', 'Consolas', 'Liberation Mono', 'Menlo', 'Courier', 'monospace'],
      },
      boxShadow: {
        'card': '0 1px 0 rgba(27, 31, 36, 0.04), 0 1px 3px rgba(27, 31, 36, 0.12)',
        'dropdown': '0 8px 24px rgba(140, 149, 159, 0.2)',
        'btn': '0 1px 0 rgba(27, 31, 36, 0.04)',
        'btn-primary': '0 1px 0 rgba(27, 31, 36, 0.1)',
      },
      borderRadius: {
        'github': '6px',
      },
      typography: {
        DEFAULT: {
          css: {
            maxWidth: '65ch',
            a: {
              color: '#0969da',
              textDecoration: 'none',
              '&:hover': {
                textDecoration: 'underline',
              },
            },
            code: {
              color: '#24292f',
              backgroundColor: '#f6f8fa',
              borderRadius: '6px',
              padding: '0.2em 0.4em',
              border: '1px solid #d0d7de',
            },
          },
        },
      },
    },
  },
  plugins: [],
};