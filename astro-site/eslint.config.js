import js from '@eslint/js';
import eslintPluginAstro from 'eslint-plugin-astro';
import eslintPluginSvelte from 'eslint-plugin-svelte';
import globals from 'globals';
import tseslint from 'typescript-eslint';

// Why this file is longer than it was (issue #643):
//
// It used to be `...eslintPluginAstro.configs.recommended` and nothing else.
// That meant `pnpm lint` — which is inside the REQUIRED check-lint job —
// applied ten astro/* rules to 36 of 60 source files and no rules at all to
// the rest. Probed at the time: a .mjs file containing `var x = 1; if (x ==
// "1"){}` plus unreachable code returned zero findings, and a .svelte file
// returned "File ignored because no matching configuration was supplied".
// Zero of the three Svelte components and zero of the 21 .ts files were
// linted.
//
// The gate demonstrated it on itself: the one warning it emitted was an
// unused eslint-disable for `no-eval` — a suppression for a rule that was
// not configured, sitting directly above a live eval().

export default [
  { ignores: ['dist/', '.astro/', 'node_modules/', 'pagefind/'] },

  js.configs.recommended,
  ...tseslint.configs.recommended,
  ...eslintPluginAstro.configs.recommended,
  ...eslintPluginSvelte.configs.recommended,

  {
    languageOptions: {
      globals: { ...globals.browser, ...globals.node },
    },
    rules: {
      // set:html is used for JSON-LD structured data (trusted output from
      // JSON.stringify on our own schema objects, not user input).
      'astro/no-set-html-directive': 'warn',

      // skipComments: color-token-audit.mjs:88 explains its own blanking
      // routine and has to write a comment delimiter inside a comment. It
      // does that with a zero-width space, which is the correct trick and
      // not a stray invisible character in code.
      'no-irregular-whitespace': ['error', { skipComments: true }],
    },
  },

  // Svelte components use <script lang="ts">. Without pointing the svelte
  // parser at the TS parser for script blocks, every one of them fails with
  // "Parsing error: The keyword 'interface' is reserved" and NO rules run --
  // which looks like a clean file and is the same nothing as before.
  {
    files: ['**/*.svelte'],
    languageOptions: {
      parserOptions: { parser: tseslint.parser },
    },
  },

  // Node scripts: build tooling and audits, not browser code.
  {
    files: ['scripts/**/*.{js,mjs}', '*.config.{js,mjs}'],
    languageOptions: { globals: globals.node },
  },

  // Browser-side inline helpers live in .astro files; both environments apply
  // because the frontmatter is Node and the template body is browser.
  {
    files: ['**/*.astro'],
    rules: {
      // Astro components legitimately declare props that the template uses
      // via the frontmatter destructure; the parser does not always connect
      // the two, and astro/* rules already cover the real cases.
      'no-unused-vars': 'off',
      '@typescript-eslint/no-unused-vars': 'off',
    },
  },
];
