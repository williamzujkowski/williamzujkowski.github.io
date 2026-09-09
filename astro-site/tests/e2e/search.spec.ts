import { test, expect, type Page } from 'playwright/test';
import AxeBuilder from '@axe-core/playwright';

async function openSearch(page: Page) {
  await page.goto('/');
  await page.getByRole('button', { name: 'Search site', exact: true }).click();
  await expect(page.getByRole('textbox', { name: 'Search site content' })).toBeFocused();
  return page.getByRole('textbox', { name: 'Search site content' });
}

// Real module loading and UI, with only the Pagefind boundary substituted.
// Deferred promises make races reproducible without relying on CPU speed.
async function mockIndex(page: Page, searchBody: string, initBody = '') {
  await page.route('**/pagefind/pagefind.js*', (route) => route.fulfill({
    contentType: 'text/javascript',
    body: `
      export async function init() { ${initBody} }
      const hit = (title) => ({ id: title, data: async () => ({
        id: title, url: '/about/#' + title, meta: { title }, excerpt: 'Matched text'
      }) });
      export async function search(query) { ${searchBody} }
    `,
  }));
}

test('search cannot accept a click before its island has hydrated', async ({ page }) => {
  let releaseModule!: () => void;
  const moduleGate = new Promise<void>((resolve) => { releaseModule = resolve; });
  await page.route('**/_astro/Search.*.js', async (route) => {
    await moduleGate;
    await route.continue();
  });
  const moduleRequested = page.waitForRequest(/\/_astro\/Search\.[^/]+\.js(?:\?|$)/);
  try {
    await page.goto('/', { waitUntil: 'domcontentloaded' });
    await moduleRequested;
    const trigger = page.getByRole('button', { name: 'Search site', exact: true });
    await expect(trigger).toBeVisible();
    await expect(trigger).toBeDisabled();
    await expect(page.getByRole('dialog')).toHaveCount(0);

    releaseModule();
    await expect(trigger).toBeEnabled();
    await trigger.click();
    await expect(page.getByRole('textbox', { name: 'Search site content' })).toBeFocused();
  } finally {
    releaseModule();
  }
});

test('repeated shortcuts preserve inert cleanup, external inert state and original focus', async ({ page }) => {
  await page.goto('/');
  await page.locator('footer').evaluate((el) => el.setAttribute('inert', ''));
  const trigger = page.getByRole('button', { name: 'Search site', exact: true });
  await trigger.click();
  await expect(page.getByRole('textbox')).toBeFocused();
  await page.keyboard.press('Control+k');
  await page.keyboard.press('Control+k');
  await page.keyboard.press('Escape');
  await expect(page.getByRole('dialog')).toHaveCount(0);
  await expect(page.locator('[data-search-inert]')).toHaveCount(0);
  await expect(page.locator('main')).not.toHaveAttribute('inert');
  await expect(page.locator('footer')).toHaveAttribute('inert', '');
  await expect(trigger).toBeFocused();
  await page.getByRole('link', { name: 'Dispatches', exact: true }).click();
  await expect(page).toHaveURL(/\/posts\/$/);
});

test('typing a new query cannot be overwritten by an older response', async ({ page }) => {
  await mockIndex(page, `
    if (query === 'older') {
      window.oldStarted = true;
      await new Promise(resolve => { window.releaseOld = resolve; });
    }
    return { results: [hit(query)] };
  `);
  const input = await openSearch(page);
  await input.fill('older');
  await page.waitForFunction(() => (window as any).oldStarted);
  await input.fill('newer');
  await expect(page.locator('.search-result-title')).toHaveText('newer');
  await page.evaluate(() => (window as any).releaseOld());
  await expect(page.getByRole('status')).toHaveText('Showing 1 of 1 results');
  await expect(page.locator('.search-result-title')).toHaveText('newer');
});

test('an old request failure cannot replace a newer successful search', async ({ page }) => {
  await mockIndex(page, `
    if (query === 'older') {
      window.oldStarted = true;
      await new Promise((_, reject) => { window.rejectOld = () => reject(new Error('Late failure')); });
    }
    return { results: [hit(query)] };
  `);
  const input = await openSearch(page);
  await input.fill('older');
  await page.waitForFunction(() => (window as any).oldStarted);
  await input.fill('newer');
  await expect(page.locator('.search-result-title')).toHaveText('newer');
  await page.evaluate(() => (window as any).rejectOld());
  await expect(page.getByRole('status')).toHaveText('Showing 1 of 1 results');
  await expect(page.getByRole('button', { name: 'Try again' })).toHaveCount(0);
});

for (const action of ['clear', 'shorten', 'close'] as const) {
  test(`${action} invalidates in-flight result hydration`, async ({ page }) => {
    await mockIndex(page, `return { results: [{ id: 'late', data: async () => {
      window.hydrationStarted = true;
      await new Promise(resolve => { window.releaseHydration = resolve; });
      return { id: 'late', url: '/about/', meta: { title: 'Late result' }, excerpt: '' };
    } }] };`);
    const input = await openSearch(page);
    await input.fill('security');
    await page.waitForFunction(() => (window as any).hydrationStarted);
    if (action === 'clear') await page.getByRole('button', { name: 'Clear', exact: true }).click();
    if (action === 'shorten') await input.fill('s');
    if (action === 'close') {
      await page.getByRole('button', { name: 'Close search' }).click();
      await page.getByRole('button', { name: 'Search site', exact: true }).click();
    }
    await page.evaluate(() => (window as any).releaseHydration());
    await expect(page.getByRole('status')).toHaveText('Type at least two characters to search.');
    await expect(page.locator('.search-result-link')).toHaveCount(0);
    await expect(input).toBeFocused();
  });
}

for (const failure of ['import', 'init', 'query', 'fragment'] as const) {
  test(`${failure} failures report an error and retry successfully`, async ({ page }) => {
    if (failure === 'import') {
      await mockIndex(page, `return { results: [hit(query)] };`);
      // The first request is missing; the next must use a fresh module URL.
      await page.route('**/pagefind/pagefind.js', (route) => route.fulfill({ status: 404, body: 'Missing' }), { times: 1 });
    } else {
      const failOnce = `if (!window.failedOnce) { window.failedOnce = true; throw new Error('Unavailable'); }`;
      await mockIndex(page,
        failure === 'fragment'
          ? `return { results: [{ id: query, data: async () => { ${failOnce} return (await hit(query).data()); } }] };`
          : `${failure === 'query' ? failOnce : ''} return { results: [hit(query)] };`,
        failure === 'init' ? failOnce : '');
    }
    const input = await openSearch(page);
    await input.fill('security');
    await expect(page.getByRole('status')).toHaveText('Search is unavailable. Please try again.');
    await expect(page.getByText('No results for')).toHaveCount(0);
    await expect(page.getByRole('link', { name: 'Browse all posts' })).toHaveAttribute('href', '/posts/');
    await page.getByRole('button', { name: 'Try again' }).click();
    await expect(input).toBeFocused();
    await expect(page.locator('.search-result-title')).toHaveText('security');
  });
}

test('every result is reachable and loading more moves focus to the first new result', async ({ page }) => {
  await mockIndex(page, `return { results: Array.from({length: 19}, (_, i) => hit('Result ' + (i + 1))) };`);
  const input = await openSearch(page);
  await input.fill('security');
  await expect(page.getByRole('status')).toHaveText('Showing 8 of 19 results');
  const more = page.getByRole('button', { name: 'Show more results' });
  await more.click();
  await expect(page.locator('.search-result-link').nth(8)).toBeFocused();
  await expect(page.getByRole('status')).toHaveText('Showing 16 of 19 results');
  await more.click();
  await expect(page.locator('.search-result-link').nth(16)).toBeFocused();
  await expect(page.locator('.search-result-link')).toHaveCount(19);
  await expect(more).toHaveCount(0);
  await page.keyboard.press('Tab');
  await page.keyboard.press('Tab');
  await page.keyboard.press('Tab');
  await expect(input).toBeFocused();
});

test('load-more failure preserves results and retries the missing batch', async ({ page }) => {
  await mockIndex(page, `return { results: Array.from({length: 10}, (_, i) => ({
    id: String(i), data: async () => {
      if (i === 8 && !window.failedOnce) { window.failedOnce = true; throw new Error('Fragment missing'); }
      return hit('Result ' + (i + 1)).data();
    }
  })) };`);
  const input = await openSearch(page);
  await input.fill('security');
  await page.getByRole('button', { name: 'Show more results' }).click();
  await expect(page.getByRole('status')).toHaveText('More results could not be loaded. Please try again.');
  await expect(page.locator('.search-result-link')).toHaveCount(8);
  await expect(page.getByRole('button', { name: 'Try again' })).toBeFocused();
  await page.getByRole('button', { name: 'Try again' }).click();
  await expect(page.locator('.search-result-link')).toHaveCount(10);
  await expect(page.locator('.search-result-link').nth(8)).toBeFocused();
});

test('focus stays in the dialog while another result batch is pending', async ({ page }) => {
  await mockIndex(page, `return { results: Array.from({length: 9}, (_, i) => ({
    id: String(i), data: async () => {
      if (i === 8) {
        window.moreStarted = true;
        await new Promise(resolve => { window.releaseMore = resolve; });
      }
      return hit('Result ' + (i + 1)).data();
    }
  })) };`);
  const input = await openSearch(page);
  await input.fill('security');
  const more = page.getByRole('button', { name: 'Show more results' });
  await more.click();
  await page.waitForFunction(() => (window as any).moreStarted);
  await expect(more).toBeFocused();
  await expect(more).toHaveAttribute('aria-disabled', 'true');
  await page.keyboard.press('Tab');
  await expect(input).toBeFocused();
  await page.evaluate(() => (window as any).releaseMore());
  await expect(page.locator('.search-result-link').nth(8)).toBeFocused();
});

test('mobile controls are visible, keyboard focus stays in the dialog, and axe passes', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });
  await mockIndex(page, 'return { results: [] };');
  const input = await openSearch(page);
  await input.fill('unmatched');
  await expect(page.getByRole('status')).toHaveText('No results for "unmatched"');
  await expect(page.getByRole('button', { name: 'Clear', exact: true })).toBeInViewport();
  await expect(page.getByRole('button', { name: 'Close search' })).toBeInViewport();
  await page.keyboard.press('Shift+Tab');
  await expect(page.getByRole('button', { name: 'Close search' })).toBeFocused();
  await page.keyboard.press('Tab');
  await expect(input).toBeFocused();
  const audit = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']).analyze();
  expect(audit.violations).toEqual([]);
});

test('production index includes articles and substantive pages, excludes listing and 404 pages', async ({ page }) => {
  await page.goto('/');
  const urls = await page.evaluate(async () => {
    const path = `${location.origin}/pagefind/pagefind.js`;
    const pagefind = await import(/* @vite-ignore */ path);
    await pagefind.init();
    // null returns every indexed document, avoiding assumptions about ranking.
    const response = await pagefind.search(null);
    const results = await Promise.all(response.results.map((r: any) => r.data()));
    return results.map((r: any) => new URL(r.url, location.origin).pathname) as string[];
  });
  expect(urls.length).toBeGreaterThan(80);
  for (const route of ['/about/', '/uses/', '/projects/', '/now/']) expect(urls).toContain(route);
  expect(urls.some((url) => /^\/posts\/.+\/$/.test(url))).toBe(true);
  // PizzaOps explicitly requests noindex and is intentionally discoverable
  // through its companion post only. Preserve that existing page policy.
  expect(urls.filter((url) => url === '/' || url === '/posts/' || url === '/pizza-ops/' || url.startsWith('/tags/') || url.includes('404'))).toEqual([]);
  // Check that the user-facing UI also works with the actual generated index.
  await page.getByRole('button', { name: 'Search site', exact: true }).click();
  await page.getByRole('textbox').fill('security');
  await expect(page.locator('.search-result-link').first()).toBeVisible();
  await expect(page.getByRole('status')).toHaveText(/Showing 8 of \d+ results/);
  await page.getByRole('button', { name: 'Show more results' }).click();
  await expect(page.locator('.search-result-link')).toHaveCount(16);
});

test('the real Pagefind module recovers after a transient missing script', async ({ page }) => {
  await page.route('**/pagefind/pagefind.js', (route) => route.fulfill({ status: 404, body: 'Temporarily missing' }), { times: 1 });
  const input = await openSearch(page);
  await input.fill('security');
  await expect(page.getByRole('status')).toHaveText('Search is unavailable. Please try again.');
  await page.getByRole('button', { name: 'Try again' }).click();
  await expect(page.locator('.search-result-link').first()).toBeVisible();
  await expect(page.getByRole('status')).toHaveText(/Showing 8 of \d+ results/);
});

test('structured data does not advertise an unsupported search URL', async ({ page }) => {
  await page.goto('/');
  const schemas = await page.locator('script[type="application/ld+json"]').allTextContents();
  expect(schemas.some((schema) => JSON.parse(schema)['@type'] === 'WebSite')).toBe(true);
  expect(schemas.join('')).not.toContain('SearchAction');
});
