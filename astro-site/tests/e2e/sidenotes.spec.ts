import { test, expect } from 'playwright/test';
import AxeBuilder from '@axe-core/playwright';

// Sidenotes (Tufte/gwern-style margin notes, issue #272). Pilot post:
// 2025-10-29-post-quantum-cryptography-homelab has 5 GFM footnotes
// converted from inline citations — see rehype-sidenotes.mjs.
const PILOT_POST = '/posts/2025-10-29-post-quantum-cryptography-homelab/';

// 1280 is the CSS breakpoint itself (article.post-article's grid rule is
// `@media (min-width: 1280px)`) — worth checking in addition to a
// comfortably-wide 1440px, since off-by-one rail-width math would show up
// right at the boundary first.
const RAIL_WIDTHS = [1280, 1440];

for (const width of RAIL_WIDTHS) {
  test.describe(`sidenotes — margin rail at ${width}px`, () => {
    test.use({ viewport: { width, height: 1000 } });

    test('every sidenote is floated left of the prose column, in-viewport, and clear of the TOC', async ({
      page,
    }) => {
      await page.goto(PILOT_POST);

      const sidenotes = page.locator('aside.sidenote');
      const count = await sidenotes.count();
      expect(count).toBeGreaterThan(0);

      const prose = page.locator('.prose').first();
      const proseBox = await prose.boundingBox();
      expect(proseBox).not.toBeNull();

      const toc = page.locator('nav.toc').first();
      const tocBox = (await toc.count()) ? await toc.boundingBox() : null;

      for (let i = 0; i < count; i++) {
        const sidenote = sidenotes.nth(i);
        await expect(sidenote).toBeVisible();

        // Floated left with a negative margin — CSS technique check, not
        // just "is it visible": confirms the >=1280px rail rule actually
        // applied rather than the narrow-viewport in-flow fallback
        // rendering by luck.
        const float = await sidenote.evaluate((el) => getComputedStyle(el).float);
        expect(float, `sidenote #${i} should be float:left`).toBe('left');

        const noteBox = await sidenote.boundingBox();
        expect(noteBox, `sidenote #${i} should have a bounding box`).not.toBeNull();

        // In-viewport: never pulled off the left edge of the browser.
        expect(noteBox!.x, `sidenote #${i} should not be off-screen left`).toBeGreaterThanOrEqual(0);

        // Sits entirely to the LEFT of the prose column (in the margin),
        // not overlapping the reading column's text.
        expect(
          noteBox!.x + noteBox!.width,
          `sidenote #${i} should not overlap .prose`
        ).toBeLessThanOrEqual(proseBox!.x + 1);

        // TOC lives in the right rail (#299) — the two must never overlap.
        if (tocBox) {
          const overlaps =
            noteBox!.x < tocBox.x + tocBox.width &&
            noteBox!.x + noteBox!.width > tocBox.x &&
            noteBox!.y < tocBox.y + tocBox.height &&
            noteBox!.y + noteBox!.height > tocBox.y;
          expect(overlaps, `sidenote #${i} should not overlap nav.toc`).toBe(false);
        }
      }
    });
  });
}

test.describe('sidenotes — wide viewport (margin rail)', () => {
  test.use({ viewport: { width: 1440, height: 1000 } });

  test('sidenote-ref marker is visible inline in the prose, has no dangling aria-describedby, and precedes its note in DOM order', async ({
    page,
  }) => {
    await page.goto(PILOT_POST);

    const ref = page.locator('a.sidenote-ref').first();
    await expect(ref).toBeVisible();

    // GFM's aria-describedby points at the "Footnotes" <h2> this plugin
    // deletes along with the rest of the footnotes section — left in
    // place, that's a dangling ARIA reference (resolves to nothing).
    await expect(ref).not.toHaveAttribute('aria-describedby', /.+/);

    const targetId = await ref.getAttribute('href');
    expect(targetId).toMatch(/^#user-content-fn-/);
    const id = targetId!.slice(1);
    const noteById = page.locator(`aside.sidenote[id="${id}"]`);
    await expect(noteById).toHaveCount(1);

    // DOM order: the ref's paragraph must precede the note in document order.
    const order = await page.evaluate((noteId) => {
      const refEl = document.querySelector(`a.sidenote-ref[href="#${noteId}"]`);
      const noteEl = document.getElementById(noteId);
      if (!refEl || !noteEl) return null;
      // DOCUMENT_POSITION_FOLLOWING (4) means noteEl comes after refEl.
      return !!(refEl.compareDocumentPosition(noteEl) & Node.DOCUMENT_POSITION_FOLLOWING);
    }, id);
    expect(order).toBe(true);
  });

  test('clicking the sidenote-ref updates the URL hash to the matching note id', async ({ page }) => {
    await page.goto(PILOT_POST);
    const ref = page.locator('a.sidenote-ref').first();
    const href = await ref.getAttribute('href');
    await ref.click();
    await expect(page).toHaveURL(new RegExp(href!.slice(1) + '$'));
  });

  test('no GFM footnotes section remains on the pilot post', async ({ page }) => {
    await page.goto(PILOT_POST);
    await expect(page.locator('section[data-footnotes]')).toHaveCount(0);
  });
});

test.describe('sidenotes — narrow viewport (inline fallback)', () => {
  test.use({ viewport: { width: 375, height: 812 } });

  test('sidenote renders as an in-flow small-print block, not floated into a rail', async ({ page }) => {
    await page.goto(PILOT_POST);

    const sidenote = page.locator('aside.sidenote').first();
    await expect(sidenote).toBeVisible();

    const float = await sidenote.evaluate((el) => getComputedStyle(el).float);
    expect(float).toBe('none');

    // At this width the note should span close to the full viewport width
    // (in-flow block), not a narrow fixed-width margin column.
    const box = await sidenote.boundingBox();
    expect(box).not.toBeNull();
    expect(box!.width).toBeGreaterThan(280);
  });

  test('sidenote-ref marker is still visible and reachable at phone width', async ({ page }) => {
    await page.goto(PILOT_POST);
    await expect(page.locator('a.sidenote-ref').first()).toBeVisible();
  });
});

test.describe('sidenotes — accessibility', () => {
  test('axe: pilot post has no new violations at the wide-viewport (rail) layout', async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 1000 });
    await page.goto(PILOT_POST);
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'])
      .exclude('pre.astro-code span')
      // Pre-existing gap, unrelated to sidenotes: this post's "Threat Model
      // Checklist" uses GFM task-list syntax (`- [ ]`), which Astro's
      // default markdown pipeline renders as bare
      // `<input type="checkbox" disabled>` with no accessible label. Every
      // other page in the a11y suite happens not to use task lists, so
      // this was never caught before the sidenotes pilot picked this post
      // for its citation density. Tracked as a follow-up (needs a small
      // rehype pass adding aria-label to GFM task-list checkboxes) — out
      // of scope for the sidenotes plugin itself, excluded here (and ONLY
      // here / in a11y.spec.ts's page-specific exclusion — never applied
      // suite-wide) rather than silently left failing.
      .exclude('.task-list-item input[type="checkbox"]')
      .analyze();
    expect(results.violations, JSON.stringify(results.violations, null, 2)).toEqual([]);
  });

  test('axe: pilot post has no new violations at the narrow-viewport (inline) layout', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto(PILOT_POST);
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'])
      .exclude('pre.astro-code span')
      // See the wide-viewport test above for the task-list rationale.
      .exclude('.task-list-item input[type="checkbox"]')
      .analyze();
    expect(results.violations, JSON.stringify(results.violations, null, 2)).toEqual([]);
  });
});
