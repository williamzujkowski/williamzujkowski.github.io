/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./_includes/**/*.{njk,md,js}",
    "./_layouts/**/*.{njk,md,js}",
    "./src/**/*.{njk,md,js}",
    "./*.{njk,md,js}"
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#003366',
        'secondary': '#990000',
        'accent': '#006633',
        'background': '#ffffff',
        'text': '#333333',
        'muted': '#666666',
        'light': '#f5f5f5',
        'border': '#dddddd',
      },
      fontFamily: {
        'sans': ['Georgia', 'Times New Roman', 'serif'],
        'serif': ['Georgia', 'Times New Roman', 'serif'],
        'mono': ['Courier New', 'Courier', 'monospace'],
      },
      boxShadow: {
        'classic': '2px 2px 4px rgba(0, 0, 0, 0.2)',
      },
    },
  },
  plugins: [],
};