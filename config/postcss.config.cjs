module.exports = {
  plugins: [
    // In Tailwind v4, the PostCSS plugin is moved to @tailwindcss/postcss
    // This config supports both v3 and v4
    (process.env.USE_TAILWIND_V3 === 'true' ? 
      require('tailwindcss')(process.env.GITHUB_ACTIONS ? './tailwind.config.cjs' : './config/tailwind.config.cjs') :
      require('@tailwindcss/postcss')(process.env.GITHUB_ACTIONS ? './tailwind.config.cjs' : './config/tailwind.config.cjs')),
    require('autoprefixer')
  ]
}