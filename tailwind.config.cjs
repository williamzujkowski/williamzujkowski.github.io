/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./_includes/**/*.{njk,md,js}",
    "./_layouts/**/*.{njk,md,js}",
    "./src/**/*.{njk,md,js}",
    "./src/_includes/**/*.{njk,md,js}",
    "./*.{njk,md,js}"
  ],
  darkMode: 'class', // Changed to 'class' for better manual toggle control
  theme: {
    extend: {
      colors: {
        'primary': {
          light: '#2563eb', // Modern royal blue
          dark: '#60a5fa',  // Bright blue for dark mode
        },
        'secondary': {
          light: '#e11d48', // Vibrant red
          dark: '#fb7185',  // Soft coral for dark mode
        },
        'accent': {
          light: '#0891b2', // Teal
          dark: '#22d3ee',  // Bright cyan for dark mode
        },
        'background': {
          light: '#ffffff',
          dark: '#0f172a',  // Deep slate blue for dark mode
        },
        'text': {
          light: '#1e293b', // Slate blue
          dark: '#f1f5f9',  // Slate white for dark mode
        },
        'muted': {
          light: '#64748b', // Slate gray
          dark: '#94a3b8',  // Lighter slate for dark mode
        },
        'light': {
          light: '#f8fafc', // Lightest slate
          dark: '#1e293b',  // Dark slate for dark mode
        },
        'border': {
          light: '#e2e8f0', // Soft slate border
          dark: '#334155',  // Medium slate for dark mode
        },
        'terminal': {
          bg: '#0e1016',    // Sleek dark terminal background
          text: '#a0aec0',  // Light slate terminal text (for responses)
          prompt: '#2563eb', // Royal blue for the prompt
          command: '#f8fafc', // Bright white for commands
        },
      },
      fontFamily: {
        'sans': ['Outfit', 'system-ui', '-apple-system', 'sans-serif'],
        'serif': ['Georgia', 'Times New Roman', 'serif'],
        'mono': ['JetBrains Mono', 'Fira Code', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
        'display': ['Plus Jakarta Sans', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'classic': '0 4px 10px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'classic-dark': '0 4px 10px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -1px rgba(0, 0, 0, 0.12)',
        'card': '0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05)',
        'card-dark': '0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.15)',
        'card-hover': '0 25px 35px -5px rgba(0, 0, 0, 0.15), 0 10px 15px -5px rgba(0, 0, 0, 0.08)',
        'terminal': '0 0 15px rgba(56, 189, 248, 0.15), 0 0 30px rgba(56, 189, 248, 0.1)',
      },
      animation: {
        'terminal-cursor': 'blink 1s step-end infinite',
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        blink: {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0 },
        },
        fadeIn: {
          '0%': { opacity: 0, transform: 'translateY(10px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'noise': "url(\"data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E\")",
      },
      typography: {
        DEFAULT: {
          css: {
            maxWidth: '65ch',
          },
        },
      },
    },
  },
  plugins: [],
};