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
            color: 'var(--fg)',
            a: {
              color: 'var(--link)',
              textDecoration: 'underline',
              textDecorationColor: 'transparent',
              textUnderlineOffset: '2px',
              transition: 'all 150ms ease',
              '&:hover': {
                color: 'var(--link-hover)',
                textDecorationColor: 'currentColor',
              },
            },
            strong: {
              color: 'var(--fg)',
              fontWeight: '600',
            },
            'h1, h2, h3, h4, h5, h6': {
              color: 'var(--fg)',
              fontWeight: '600',
            },
            code: {
              color: 'var(--accent)',
              backgroundColor: 'var(--bg-secondary)',
              padding: '0.125rem 0.375rem',
              borderRadius: '0.25rem',
              fontWeight: '500',
            },
            'code::before': {
              content: '""',
            },
            'code::after': {
              content: '""',
            },
            pre: {
              backgroundColor: 'var(--bg-secondary)',
              border: '1px solid var(--border)',
              borderRadius: '0.75rem',
              color: 'var(--fg-secondary)',
            },
            'pre code': {
              backgroundColor: 'transparent',
              padding: '0',
              color: 'inherit',
            },
            blockquote: {
              color: 'var(--muted)',
              borderLeftColor: 'var(--border-secondary)',
              fontStyle: 'italic',
            },
            'blockquote p': {
              color: 'var(--muted)',
            },
            hr: {
              borderColor: 'var(--border)',
            },
            'ol, ul': {
              color: 'var(--fg-secondary)',
            },
            li: {
              color: 'var(--fg-secondary)',
            },
            p: {
              color: 'var(--fg-secondary)',
            },
            thead: {
              color: 'var(--fg)',
              borderBottomColor: 'var(--border-secondary)',
            },
            'tbody tr': {
              borderBottomColor: 'var(--border)',
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