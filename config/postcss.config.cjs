module.exports = {
  plugins: [
    // Using Tailwind v3.4.1
    require('tailwindcss')(
      process.env.GITHUB_ACTIONS ? './tailwind.config.cjs' : './config/tailwind.config.cjs'
    ),
    require('autoprefixer')
  ]
}