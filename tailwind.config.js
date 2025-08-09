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
        // OKLCH-based colors for better perceptual uniformity
        background: {
          light: 'var(--clr-background-light)',
          dark: 'var(--clr-background-dark)',
        },
        text: {
          light: 'var(--clr-text-light)',
          dark: 'var(--clr-text-dark)',
        },
        link: {
          light: 'var(--clr-link-light)',
          dark: 'var(--clr-link-dark)',
        },
        primary: {
          50: 'var(--clr-primary-50)',
          100: 'var(--clr-primary-100)',
          200: 'var(--clr-primary-200)',
          300: 'var(--clr-primary-300)',
          400: 'var(--clr-primary-400)',
          500: 'var(--clr-primary-500)',
          600: 'var(--clr-primary-600)',
          700: 'var(--clr-primary-700)',
          800: 'var(--clr-primary-800)',
          900: 'var(--clr-primary-900)',
          950: 'var(--clr-primary-950)',
        }
      },
      fontSize: {
        // Responsive font sizes using clamp
        'xs': 'var(--font-size-xs)',
        'sm': 'var(--font-size-sm)',
        'base': 'var(--font-size-base)',
        'lg': 'var(--font-size-lg)',
        'xl': 'var(--font-size-xl)',
        '2xl': 'var(--font-size-2xl)',
        '3xl': 'var(--font-size-3xl)',
        '4xl': 'var(--font-size-4xl)',
        '5xl': 'var(--font-size-5xl)',
      },
      spacing: {
        // Mobile-friendly touch targets (minimum 44px)
        'touch': '44px',
        'touch-sm': '36px',
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