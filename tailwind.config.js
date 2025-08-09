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
        // USWDS-inspired primary colors with improved accessibility
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
          950: '#082f49',
        },
        // USWDS-inspired accent colors
        accent: {
          50: '#fdf4ff',
          100: '#fae8ff',
          200: '#f5d0fe',
          300: '#f0abfc',
          400: '#e879f9',
          500: '#d946ef',
          600: '#c026d3',
          700: '#a21caf',
          800: '#86198f',
          900: '#701a75',
          950: '#4a044e',
        },
        // USWDS-inspired success colors
        success: {
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0',
          300: '#86efac',
          400: '#4ade80',
          500: '#22c55e',
          600: '#16a34a',
          700: '#15803d',
          800: '#166534',
          900: '#14532d',
          950: '#052e16',
        },
        // USWDS-inspired warning colors
        warning: {
          50: '#fffbeb',
          100: '#fef3c7',
          200: '#fde68a',
          300: '#fcd34d',
          400: '#fbbf24',
          500: '#f59e0b',
          600: '#d97706',
          700: '#b45309',
          800: '#92400e',
          900: '#78350f',
          950: '#451a03',
        },
        // USWDS-inspired error colors
        error: {
          50: '#fef2f2',
          100: '#fee2e2',
          200: '#fecaca',
          300: '#fca5a5',
          400: '#f87171',
          500: '#ef4444',
          600: '#dc2626',
          700: '#b91c1c',
          800: '#991b1b',
          900: '#7f1d1d',
          950: '#450a0a',
        },
        // USWDS-inspired gray scale
        gray: {
          50: '#f9fafb',
          100: '#f3f4f6',
          200: '#e5e7eb',
          300: '#d1d5db',
          400: '#9ca3af',
          500: '#6b7280',
          600: '#4b5563',
          700: '#374151',
          800: '#1f2937',
          900: '#111827',
          950: '#030712',
        }
      },
      typography: {
        DEFAULT: {
          css: {
            maxWidth: '72ex', // USWDS-inspired measure
            color: '#1f2937',
            lineHeight: '1.5',
            fontSize: '1.0625rem', // 17px base like USWDS
            a: {
              color: '#0369a1',
              textDecoration: 'underline',
              textUnderlineOffset: '2px',
              '&:hover': {
                color: '#075985',
                textDecorationThickness: '2px',
              },
              '&:focus': {
                outline: '2px solid #0ea5e9',
                outlineOffset: '2px',
              },
            },
            h1: {
              fontSize: '2.5rem',
              lineHeight: '1.2',
              marginTop: '1.5em',
              marginBottom: '0.5em',
              fontWeight: '700',
            },
            h2: {
              fontSize: '2rem',
              lineHeight: '1.3',
              marginTop: '1.5em',
              marginBottom: '0.5em',
              fontWeight: '700',
            },
            h3: {
              fontSize: '1.5rem',
              lineHeight: '1.4',
              marginTop: '1.5em',
              marginBottom: '0.5em',
              fontWeight: '600',
            },
            h4: {
              fontSize: '1.25rem',
              lineHeight: '1.5',
              marginTop: '1.5em',
              marginBottom: '0.5em',
              fontWeight: '600',
            },
            'code': {
              fontSize: '0.875em',
              fontWeight: '500',
              backgroundColor: '#f3f4f6',
              padding: '0.125em 0.25em',
              borderRadius: '0.25rem',
            },
            'pre': {
              fontSize: '0.875em',
              lineHeight: '1.7',
              backgroundColor: '#1f2937',
              color: '#f3f4f6',
              padding: '1rem',
              borderRadius: '0.5rem',
            },
            'blockquote': {
              borderLeftWidth: '4px',
              borderLeftColor: '#0ea5e9',
              paddingLeft: '1rem',
              fontStyle: 'italic',
            },
          },
        },
        invert: {
          css: {
            color: '#e5e7eb',
            a: {
              color: '#38bdf8',
              '&:hover': {
                color: '#7dd3fc',
              },
              '&:focus': {
                outline: '2px solid #38bdf8',
              },
            },
            strong: {
              color: '#f3f4f6',
            },
            h1: {
              color: '#f9fafb',
            },
            h2: {
              color: '#f9fafb',
            },
            h3: {
              color: '#f9fafb',
            },
            h4: {
              color: '#f9fafb',
            },
            code: {
              color: '#f3f4f6',
              backgroundColor: '#374151',
            },
            'blockquote': {
              borderLeftColor: '#0ea5e9',
              color: '#d1d5db',
            },
          },
        },
      },
      fontFamily: {
        // USWDS-inspired font stacks
        sans: ['"Public Sans"', 'Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', '"Helvetica Neue"', 'Arial', 'sans-serif'],
        serif: ['Merriweather', 'Georgia', 'Cambria', '"Times New Roman"', 'Times', 'serif'],
        mono: ['"Roboto Mono"', 'JetBrains Mono', 'Consolas', 'Monaco', '"Andale Mono"', '"Ubuntu Mono"', 'monospace'],
      },
      fontSize: {
        // USWDS-inspired type scale
        'xs': ['0.75rem', { lineHeight: '1rem' }],
        'sm': ['0.875rem', { lineHeight: '1.25rem' }],
        'base': ['1.0625rem', { lineHeight: '1.5rem' }], // 17px base
        'lg': ['1.25rem', { lineHeight: '1.75rem' }],
        'xl': ['1.5rem', { lineHeight: '2rem' }],
        '2xl': ['2rem', { lineHeight: '2.5rem' }],
        '3xl': ['2.5rem', { lineHeight: '3rem' }],
        '4xl': ['3rem', { lineHeight: '3.5rem' }],
        '5xl': ['3.5rem', { lineHeight: '4rem' }],
      },
      spacing: {
        // USWDS-inspired spacing scale
        '0.5': '0.25rem',
        '1': '0.5rem',
        '2': '1rem',
        '3': '1.5rem',
        '4': '2rem',
        '5': '2.5rem',
        '6': '3rem',
        '7': '3.5rem',
        '8': '4rem',
        '9': '4.5rem',
        '10': '5rem',
        '12': '6rem',
        '15': '7.5rem',
        '18': '9rem',
        '20': '10rem',
      },
      borderRadius: {
        'none': '0',
        'sm': '0.125rem',
        DEFAULT: '0.25rem',
        'md': '0.375rem',
        'lg': '0.5rem',
        'xl': '0.75rem',
        '2xl': '1rem',
        '3xl': '1.5rem',
        'full': '9999px',
      },
      boxShadow: {
        'sm': '0 1px 2px 0 rgb(0 0 0 / 0.05)',
        DEFAULT: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
        'md': '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
        'lg': '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
        'xl': '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
        '2xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',
        'inner': 'inset 0 2px 4px 0 rgb(0 0 0 / 0.05)',
        'none': 'none',
      },
      animation: {
        'fade-in': 'fade-in 0.5s ease-out',
        'fade-in-up': 'fade-in-up 0.5s ease-out',
        'slide-in-right': 'slide-in-right 0.3s ease-out',
        'slide-in-left': 'slide-in-left 0.3s ease-out',
        'scale-in': 'scale-in 0.2s ease-out',
      },
      keyframes: {
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'fade-in-up': {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'slide-in-right': {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(0)' },
        },
        'slide-in-left': {
          '0%': { transform: 'translateX(100%)' },
          '100%': { transform: 'translateX(0)' },
        },
        'scale-in': {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ],
}