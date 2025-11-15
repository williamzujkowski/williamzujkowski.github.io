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
        // Body text - Figtree (clean, readable sans-serif)
        sans: ['Figtree', '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', '"Noto Sans"', 'Helvetica', 'Arial', 'sans-serif'],
        // Headings - Bricolage Grotesque (distinctive, strong)
        heading: ['"Bricolage Grotesque"', 'Figtree', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        // Code blocks - JetBrains Mono (technical, readable)
        mono: ['"JetBrains Mono"', '"Fira Code"', '"SF Mono"', 'Monaco', '"Cascadia Code"', '"Roboto Mono"', 'monospace'],
        // Quotes/serif - Newsreader (elegant, authoritative)
        serif: ['Newsreader', 'Georgia', 'Cambria', '"Times New Roman"', 'serif'],
      },
      fontWeight: {
        // Body text weights (Figtree)
        light: '300',      // Figtree Light
        normal: '400',     // Figtree Regular
        medium: '500',     // Figtree Medium
        // Heading weights (Bricolage Grotesque)
        semibold: '600',   // Bricolage Grotesque SemiBold
        bold: '700',       // Bricolage Grotesque Bold
        extrabold: '800',  // Bricolage Grotesque ExtraBold
      },
      animation: {
        'fade-in': 'fadeIn 0.6s ease-out',
        'fade-in-up': 'fadeInUp 0.8s ease-out',
        'slide-in-right': 'slideInRight 0.6s ease-out',
        'glow-pulse': 'glowPulse 2s ease-in-out infinite',
        'scan-line': 'scanLine 8s linear infinite',
        'matrix-rain': 'matrixRain 20s linear infinite',
        'glitch': 'glitch 0.5s ease-in-out infinite',
        'typing': 'typing 3.5s steps(40, end), blink-caret 0.75s step-end infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideInRight: {
          '0%': { opacity: '0', transform: 'translateX(-30px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        glowPulse: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(0, 255, 170, 0.4)' },
          '50%': { boxShadow: '0 0 40px rgba(0, 255, 170, 0.8)' },
        },
        scanLine: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100vh)' },
        },
        matrixRain: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100%)' },
        },
        glitch: {
          '0%, 100%': { transform: 'translate(0)' },
          '20%': { transform: 'translate(-2px, 2px)' },
          '40%': { transform: 'translate(-2px, -2px)' },
          '60%': { transform: 'translate(2px, 2px)' },
          '80%': { transform: 'translate(2px, -2px)' },
        },
        typing: {
          'from': { width: '0' },
          'to': { width: '100%' },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ],
}