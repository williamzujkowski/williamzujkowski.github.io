import { test, expect } from 'playwright/test';

/**
 * Reading measure, counted in characters actually set per line (#698).
 *
 * `--content-reading` was documented as "40rem ≈ 71ch", which is the width
 * of the digit 0 (9px in Source Serif 4 at 17px), not of text: real lines
 * ran a median of 77 characters. Nothing checked it, so the wrong number
 * was ratified. This counts glyphs per rendered line of body paragraphs and
 * holds the median to the 60-75 editorial range.
 *
 * Three of the longest posts; the lead paragraph (drop cap) and each
 * paragraph's last, ragged line are left out.
 */

const POSTS = [
  '/posts/2024-08-02-quantum-computing-leap-forward/',
  '/posts/2024-05-14-ai-new-frontier-cybersecurity/',
  '/posts/2025-10-29-post-quantum-cryptography-homelab/',
];

test.use({ viewport: { width: 1280, height: 900 } });

for (const path of POSTS) {
  test(`median characters per line is 60-75 on ${path}`, async ({ page }) => {
    await page.goto(path);
    await page.evaluate(() => document.fonts.ready);
    const counts = await page.evaluate(() => {
      const out: number[] = [];
      const range = document.createRange();
      for (const p of [...document.querySelectorAll('.prose > p')].slice(1)) {
        const lines: { top: number; n: number }[] = [];
        const walker = document.createTreeWalker(p, NodeFilter.SHOW_TEXT);
        let node: Node | null;
        while ((node = walker.nextNode())) {
          if (node.parentElement?.closest('aside, sup')) continue; // sidenotes, refs
          const text = node.textContent ?? '';
          for (let i = 0; i < text.length; i++) {
            range.setStart(node, i);
            range.setEnd(node, i + 1);
            const rect = range.getClientRects()[0];
            if (!rect) continue;
            // Glyphs on one line can differ in top by a few px (inline code,
            // italics); a new line is a full line-height (~30px) down.
            const last = lines[lines.length - 1];
            if (last && Math.abs(rect.top - last.top) < 8) last.n++;
            else lines.push({ top: rect.top, n: 1 });
          }
        }
        lines.pop();
        out.push(...lines.map((l) => l.n));
      }
      return out;
    });
    expect(counts.length, 'enough full lines to take a median').toBeGreaterThan(100);
    const sorted = [...counts].sort((a, b) => a - b);
    const median = sorted[Math.floor(sorted.length / 2)];
    expect(median).toBeGreaterThanOrEqual(60);
    expect(median).toBeLessThanOrEqual(75);
  });
}
