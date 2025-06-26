/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,njk,md,js}",
    "./.eleventy.js"
  ],
  darkMode: 'class',
  theme: {
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
          950: '#172554',
        }
      },
      typography: {
        DEFAULT: {
          css: {
            maxWidth: 'none',
            color: '#334155',
            a: {
              color: '#2563eb',
              '&:hover': {
                color: '#1d4ed8',
              },
            },
          },
        },
        invert: {
          css: {
            color: '#d1d5db', // gray-300
            a: {
              color: '#60a5fa', // blue-400
              '&:hover': {
                color: '#93bbfd', // blue-300
              },
            },
            strong: {
              color: '#e5e7eb', // gray-200
            },
            h1: {
              color: '#f3f4f6', // gray-100
            },
            h2: {
              color: '#f3f4f6', // gray-100
            },
            h3: {
              color: '#f3f4f6', // gray-100
            },
            h4: {
              color: '#f3f4f6', // gray-100
            },
            code: {
              color: '#e5e7eb', // gray-200
            },
            'blockquote p': {
              color: '#d1d5db', // gray-300
            },
          },
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', '"Helvetica Neue"', 'Arial', 'sans-serif'],
        mono: ['JetBrains Mono', 'Consolas', 'Monaco', '"Andale Mono"', '"Ubuntu Mono"', 'monospace'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ],
}