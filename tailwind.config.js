/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./_includes/**/*.{njk,md,js}",
    "./_layouts/**/*.{njk,md,js}",
    "./src/**/*.{njk,md,js}",
    "./*.{njk,md,js}"
  ],
  darkMode: 'media', // or 'class' for manual toggle control
  theme: {
    extend: {
      colors: {
        'primary': {
          light: '#003366',
          dark: '#4d8bc9',
        },
        'secondary': {
          light: '#990000',
          dark: '#ff5c5c',
        },
        'accent': {
          light: '#006633',
          dark: '#00cc66', 
        },
        'background': {
          light: '#ffffff',
          dark: '#121212',
        },
        'text': {
          light: '#333333',
          dark: '#f5f5f5',
        },
        'muted': {
          light: '#666666',
          dark: '#a0a0a0',
        },
        'light': {
          light: '#f5f5f5',
          dark: '#282828',
        },
        'border': {
          light: '#dddddd',
          dark: '#444444',
        },
      },
      fontFamily: {
        'sans': ['Georgia', 'Times New Roman', 'serif'],
        'serif': ['Georgia', 'Times New Roman', 'serif'],
        'mono': ['Courier New', 'Courier', 'monospace'],
      },
      boxShadow: {
        'classic': '2px 2px 4px rgba(0, 0, 0, 0.2)',
        'classic-dark': '2px 2px 4px rgba(0, 0, 0, 0.4)',
      },
    },
  },
  plugins: [],
};