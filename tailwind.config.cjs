/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./_includes/**/*.{njk,md,js}",
    "./_layouts/**/*.{njk,md,js}",
    "./src/**/*.{njk,md,js}",
    "./src/_includes/**/*.{njk,md,js}",
    "./*.{njk,md,js}"
  ],
  darkMode: 'media', // or 'class' for manual toggle control
  theme: {
    extend: {
      colors: {
        'primary': {
          light: '#0055a4', // Slightly brighter blue
          dark: '#5c9ce6',  // Brighter bluish for dark mode
        },
        'secondary': {
          light: '#d63031', // Modern red
          dark: '#ff7675',  // Softer red for dark mode
        },
        'accent': {
          light: '#00b894', // Modern teal
          dark: '#55efc4',  // Bright teal for dark mode
        },
        'background': {
          light: '#ffffff',
          dark: '#121212',  // Deep dark background for dark mode
        },
        'text': {
          light: '#2d3436', // Slightly softer black
          dark: '#f5f5f5',  // Off-white for dark mode
        },
        'muted': {
          light: '#636e72', // Slate gray
          dark: '#b2bec3',  // Lighter slate for dark mode
        },
        'light': {
          light: '#f8f9fa', // Almost white
          dark: '#2d3436',  // Dark gray for dark mode
        },
        'border': {
          light: '#dfe6e9', // Soft border color
          dark: '#4d5656',  // Medium gray for dark mode
        },
        'terminal': {
          bg: '#151515',    // Almost black terminal background
          text: '#00ff9d',  // Bright green for terminal text
          prompt: '#5ce1e6', // Bright teal for the prompt
          command: '#ffffff', // White for commands
        },
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        'serif': ['Georgia', 'Times New Roman', 'serif'],
        'mono': ['JetBrains Mono', 'Fira Code', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
        'display': ['Poppins', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'classic': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'classic-dark': '0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -1px rgba(0, 0, 0, 0.12)',
        'card': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'card-dark': '0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.15)',
        'card-hover': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        'terminal': '0 0 10px rgba(92, 225, 230, 0.15), 0 0 20px rgba(92, 225, 230, 0.1)',
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