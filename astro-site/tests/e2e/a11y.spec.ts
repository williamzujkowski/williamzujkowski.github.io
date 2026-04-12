import { test, expect } from 'playwright/test';
import AxeBuilder from '@axe-core/playwright';

// Key pages covering each layout archetype
const PAGES = [
  { path: '/', name: 'landing' },
  { path: '/about/', name: 'about' },
  { path: '/posts/', name: 'blog-index' },
  { path: '/uses/', name: 'uses-specimen' },
  { path: '/now/', name: 'now' },
  { path: '/projects/', name: 'projects' },
  { path: '/tags/', name: 'tags' },
  { path: '/posts/2026-02-09-building-nexus-agents-multi-model-orchestration/', name: 'blog-post' },
];

for (const { path, name } of PAGES) {
  test(`a11y: ${name} (${path}) — light`, async ({ page }) => {
    await page.goto(path);
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'])
      .analyze();
    expect(results.violations, JSON.stringify(results.violations, null, 2)).toEqual([]);
  });

  test(`a11y: ${name} (${path}) — dark`, async ({ page }) => {
    await page.emulateMedia({ colorScheme: 'dark' });
    await page.goto(path);
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'])
      .analyze();
    expect(results.violations, JSON.stringify(results.violations, null, 2)).toEqual([]);
  });
}
