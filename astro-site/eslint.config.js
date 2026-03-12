import eslintPluginAstro from 'eslint-plugin-astro';

export default [
  ...eslintPluginAstro.configs.recommended,
  {
    rules: {
      // set:html is used for JSON-LD structured data (trusted output from
      // JSON.stringify on our own schema objects, not user input)
      'astro/no-set-html-directive': 'warn',
    },
  },
  {
    ignores: ['dist/', '.astro/', 'node_modules/'],
  },
];
