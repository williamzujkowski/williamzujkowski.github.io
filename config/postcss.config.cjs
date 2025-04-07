module.exports = {
  plugins: [
    // Check if we're in GitHub Actions (file at root) or local dev (file in config/)
    require('tailwindcss')(process.env.GITHUB_ACTIONS ? './tailwind.config.cjs' : './config/tailwind.config.cjs'),
    require('autoprefixer')
  ]
}