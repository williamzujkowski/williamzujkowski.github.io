module.exports = {
  plugins: [
    // Using Tailwind v3.4.1
    require('tailwindcss')(
      process.env.GITHUB_ACTIONS ? './tailwind.config.cjs' : './config/tailwind.config.cjs'
    ),
    require('autoprefixer'),
    require('cssnano')({
      preset: ['default', {
        discardComments: {
          removeAll: true,
        },
        normalizeWhitespace: process.env.NODE_ENV === 'production',
        minifyFontValues: true,
        minifySelectors: true,
        reduceIdents: false // Preserve custom animations
      }]
    })
  ],
  // Add input and output paths
  input: './src/css/main.css',
  output: './_site/css/styles.css'
}