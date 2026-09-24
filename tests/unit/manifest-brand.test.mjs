/**
 * The web app manifest and the layout's theme-color must agree.
 *
 * They drifted: the manifest shipped #4338ca (Tailwind indigo-600, a
 * pre-Remarque leftover) and #ffffff, while BaseLayout.astro six lines
 * away declared #f5ede4. An installed PWA painted a white splash with
 * indigo chrome.
 *
 * Nothing could catch it: color-token-audit.mjs roots at ../src and never
 * walks public/, and its regex requires a `property:` form, which
 * `"theme_color": "#4338ca"` is not.
 */

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '../../astro-site');

function lightThemeColor() {
  const layout = readFileSync(resolve(root, 'src/layouts/BaseLayout.astro'), 'utf8');
  const m = layout.match(
    /<meta name="theme-color" content="(#[0-9a-fA-F]{6})" media="\(prefers-color-scheme: light\)"/
  );
  assert.ok(m, 'the light-scheme theme-color meta was not found in BaseLayout.astro');
  return m[1];
}

test('manifest theme_color matches the light-scheme theme-color meta', () => {
  const manifest = JSON.parse(readFileSync(resolve(root, 'public/manifest.json'), 'utf8'));
  assert.equal(manifest.theme_color, lightThemeColor());
});

test('manifest background_color matches it too', () => {
  const manifest = JSON.parse(readFileSync(resolve(root, 'public/manifest.json'), 'utf8'));
  assert.equal(manifest.background_color, lightThemeColor());
});

test('the layout literal is a real hex, not an unresolved custom property', () => {
  // Negative control: if BaseLayout ever switched to var(--color-bg), the
  // regex above would stop matching and the two tests would fail loudly
  // rather than silently comparing nothing.
  assert.match(lightThemeColor(), /^#[0-9a-f]{6}$/i);
});
