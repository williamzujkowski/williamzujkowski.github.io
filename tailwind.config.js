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
        'cyber-black': '#0c0c16',
        'cyber-dark': '#1a1a2e',
        'cyber-light': '#e6e6fa',
        'cyber-muted': '#a8a8d2',
        'cyber-primary': '#00ffaa',
        'cyber-secondary': '#ff007f',
        'cyber-accent': '#7e00ff',
        'cyber-border': '#2a2a4a',
        'cyber-terminal': '#080812',
      },
      fontFamily: {
        'mono': ['IBM Plex Mono', 'monospace'],
      },
      boxShadow: {
        'neon': '0 0 5px rgba(0, 255, 170, 0.5), 0 0 10px rgba(0, 255, 170, 0.3)',
        'text': '0 0 2px rgba(230, 230, 250, 0.4)',
      },
      animation: {
        'background-gradient': 'backgroundGradient 15s ease infinite',
        'text-pulse': 'textPulse 4s infinite alternate',
        'blink': 'blink 1s step-end infinite',
      },
      keyframes: {
        backgroundGradient: {
          '0%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
          '100%': { backgroundPosition: '0% 50%' },
        },
        textPulse: {
          '0%': { textShadow: '0 0 5px rgba(0, 255, 170, 0.5)' },
          '100%': { textShadow: '0 0 15px rgba(0, 255, 170, 0.8), 0 0 25px rgba(0, 255, 170, 0.4)' },
        },
        blink: {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0 },
        },
      },
    },
  },
  plugins: [],
};
