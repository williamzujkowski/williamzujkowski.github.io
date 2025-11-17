module.exports = {
  plugins: {
    'postcss-import': {},
    '@tailwindcss/postcss': {},
    ...(process.env.NODE_ENV === 'production' ? { cssnano: {} } : {})
  },
}