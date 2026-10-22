import { test, expect } from 'playwright/test';
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

/**
 * Two defects that every other gate passed over, both found by the Oct 2026
 * design review:
 *
 * 1. Reflow (WCAG 1.4.10). A bare URL or long inline `code` span is one
 *    unbreakable word, and 26 of 100 posts scrolled the whole page sideways at
 *    320px. The only width assertion before this checked one page at 390px.
 * 2. Words glued to links. Astro 7's `compressHTML` deleted the line break
 *    between text and an inline `<a>` written on the next source line, so the
 *    footer on all 223 pages read "Terminal themes via<a…>". The page looked
 *    almost right, which is why nobody saw it.
 *
 * Both read the built `dist/`. An empty or missing build fails loudly rather
 * than passing over zero pages (see a11y.spec.ts for why that matters here).
 */

const DIST = join(process.cwd(), 'dist');
const posts = readdirSync(join(DIST, 'posts')).filter((d) =>
  statSync(join(DIST, 'posts', d)).isDirectory(),
);
const pages = ['/', '/posts/', '/tags/', '/about/', '/now/', '/uses/', '/projects/', '/404.html',
  ...posts.map((d) => `/posts/${d}/`)];

test('the build has the posts these checks iterate over', () => {
  expect(posts.length).toBeGreaterThanOrEqual(90);
});

test.describe('no horizontal page scroll at 320px', () => {
  test.use({ viewport: { width: 320, height: 800 } });
  for (const path of pages) {
    test(path, async ({ page }) => {
      const response = await page.goto(path);
      expect(response?.status()).toBe(200);
      const widths = await page.evaluate(() => ({
        scroll: document.documentElement.scrollWidth,
        viewport: innerWidth,
      }));
      expect(widths.scroll, `page is ${widths.scroll}px wide at a ${widths.viewport}px viewport`)
        .toBeLessThanOrEqual(widths.viewport);
    });
  }
});

function htmlFiles(dir: string): string[] {
  return readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    const p = join(dir, e.name);
    if (e.isDirectory()) return htmlFiles(p);
    return e.name.endsWith('.html') ? [p] : [];
  });
}

test('no word is glued to the start or end of a link', () => {
  const files = htmlFiles(DIST);
  expect(files.length).toBeGreaterThanOrEqual(100);
  const offenders: string[] = [];
  for (const file of files) {
    const html = readFileSync(file, 'utf8');
    // Footnote references legitimately sit flush against the word they mark.
    const before = [...html.matchAll(/(.{0,30}[A-Za-z0-9,.;:])<a\s(?![^>]*href="#user-content-fn)/g)];
    const after = [...html.matchAll(/<\/a>([A-Za-z0-9(].{0,30})/g)];
    for (const m of [...before, ...after]) {
      offenders.push(`${file.slice(DIST.length)}: …${m[0].replace(/href="[^"]*"/, 'href=…')}`);
    }
  }
  expect(offenders, offenders.slice(0, 20).join('\n')).toEqual([]);
});
