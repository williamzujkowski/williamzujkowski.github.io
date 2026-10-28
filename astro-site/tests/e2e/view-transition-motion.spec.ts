import { test, expect } from 'playwright/test';

// Cross-document view transitions (`@view-transition { navigation: auto }`)
// cross-fade the whole page. They must not run for visitors who ask for
// reduced motion (#661). `*` does not match view-transition pseudo-elements,
// so the universal reduced-motion reset can't be what stops them: the opt-in
// itself is gated on `prefers-reduced-motion: no-preference`, with an
// `animation: none` backstop on the pseudo-elements.
//
// Chromium fires `pageswap` with a ViewTransition only when one is about to
// run, so the event is the direct observation, in both directions: the
// no-preference case proves the opt-in is live and the test can see it.
async function navigatedWithTransition(page: import('playwright/test').Page) {
  await page.goto('/', { waitUntil: 'networkidle' });
  await page.evaluate(() => {
    addEventListener('pageswap', (e) => {
      sessionStorage.setItem('vt', String(Boolean((e as PageSwapEvent).viewTransition)));
    });
  });
  await page.getByRole('link', { name: 'About' }).first().click();
  await page.waitForURL('**/about/');
  return page.evaluate(() => sessionStorage.getItem('vt'));
}

interface PageSwapEvent extends Event {
  viewTransition: unknown;
}

test('navigation uses a view transition by default', async ({ browser }) => {
  const context = await browser.newContext({ reducedMotion: 'no-preference' });
  expect(await navigatedWithTransition(await context.newPage())).toBe('true');
  await context.close();
});

test('navigation starts no view transition under prefers-reduced-motion', async ({ browser }) => {
  const context = await browser.newContext({ reducedMotion: 'reduce' });
  expect(await navigatedWithTransition(await context.newPage())).toBe('false');
  await context.close();
});

test('the view-transition pseudo-elements carry animation: none under reduced motion', async ({ browser }) => {
  const context = await browser.newContext({ reducedMotion: 'reduce' });
  const page = await context.newPage();
  await page.goto('/');
  const rule = await page.evaluate(() => {
    const out: string[] = [];
    const walk = (rules: CSSRuleList) => {
      for (const r of Array.from(rules)) {
        if (r instanceof CSSMediaRule) {
          if (matchMedia(r.conditionText).matches) walk(r.cssRules);
        } else if (r.cssText.includes('::view-transition') && /animation[^;]*none/.test(r.cssText)) {
          out.push(r.cssText);
        }
      }
    };
    for (const sheet of Array.from(document.styleSheets)) {
      try { walk(sheet.cssRules); } catch { /* cross-origin sheet */ }
    }
    return out.join('\n');
  });
  expect(rule).toContain('::view-transition-group(*)');
  expect(rule).toContain('::view-transition-old(*)');
  expect(rule).toContain('::view-transition-new(*)');
  await context.close();
});
