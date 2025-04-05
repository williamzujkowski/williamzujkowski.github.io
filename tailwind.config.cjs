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
        'primary': {
          light: '#FFF824', // Yellow accent
          dark: '#FFF824',  // Same yellow for dark mode
        },
        'secondary': {
          light: '#151515', // Almost black
          dark: '#F3F3F3',  // Light gray for dark mode
        },
        'accent': {
          light: '#6200EA', // Purple accent
          dark: '#BB86FC',  // Light purple for dark mode
        },
        'background': {
          light: '#F3F3F3', // Light gray
          dark: '#151515',  // Almost black for dark mode 
        },
        'text': {
          light: '#151515', // Almost black
          dark: '#F3F3F3',  // Light gray for dark mode
        },
        'muted': {
          light: '#666666', // Medium gray
          dark: '#AAAAAA',  // Light medium gray for dark mode
        },
        'light': {
          light: '#FFFFFF', // White
          dark: '#242424',  // Dark gray for dark mode
        },
        'border': {
          light: '#DDDDDD', // Light border
          dark: '#333333',  // Dark border for dark mode
        },
        'terminal': {
          bg: '#151515',    // Black terminal background
          text: '#F3F3F3',  // Light gray terminal text
          prompt: '#FFF824', // Yellow for the prompt
          command: '#F3F3F3', // Light gray for commands
        },
      },
      fontFamily: {
        'sans': ['Inter', 'Helvetica', 'Arial', 'sans-serif'],
        'serif': ['Georgia', 'Times New Roman', 'serif'],
        'mono': ['JetBrains Mono', 'IBM Plex Mono', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
        'display': ['Inter', 'Helvetica', 'Arial', 'sans-serif'],
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