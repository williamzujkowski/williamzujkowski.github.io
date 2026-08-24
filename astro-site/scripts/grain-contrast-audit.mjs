#!/usr/bin/env node
/**
 * Grain composited-contrast audit — ADVISORY ONLY (issue #283 item 2).
 *
 * Background: the zine "grain" texture (src/styles/zine.css, `.zine-grain`)
 * applies a procedural feTurbulence noise SVG as a `::before` pseudo-element
 * on chrome surfaces (masthead, footer — see BaseLayout.astro) via
 * `mix-blend-mode: soft-light` at `opacity: 0.5`. Token-based contrast audits
 * (run-remarque-audit.mjs, apca-audit.mjs) only reason about CSS custom
 * property values — they cannot see this per-pixel compositing effect. 4 of
 * 7 design-review voters flagged that grain over a surface could push real
 * text/border contrast below threshold in the worst themes, so this needs a
 * screenshot + pixel-sample check instead.
 *
 * Why sampling the background (not the text glyphs) is the right target:
 * `.zine-grain::before` is a `::before` pseudo-element, which paints BEFORE
 * an element's normal-flow children and BEFORE any `::after` in the
 * paint/stacking order (CSS §generated content: ::before is the first
 * child, ::after the last). Both `.site-masthead` and `.site-footer` have
 * only auto z-index content, so document order controls paint order:
 *   1. the surface's own background (transparent; body's --color-bg shows through)
 *   2. `.zine-grain::before` (the noise veil, inset:0 over the whole surface)
 *   3. real DOM children — including all text nodes and the wobble-rule's
 *      wavy border, which is itself a LATER `::after` on the same element
 *
 * So text glyphs and the wobble-rule border paint fully opaque ON TOP of
 * the grain veil — their resolved color is exactly the CSS token color
 * (verifiable via getComputedStyle, which we do below). What the grain
 * actually perturbs is the flat background immediately behind/around that
 * text: the real, composited luminance there wobbles up and down (uniformly
 * across the surface, because feTurbulence produces a homogeneous
 * high-frequency noise field) instead of sitting exactly at the token's
 * --color-bg value. That's the thing token audits cannot see, and the thing
 * this script measures directly from real rendered pixels.
 *
 * Method:
 *  1. Serve `dist/` with a throwaway static file server (no `astro preview`
 *     dependency — keeps this script self-contained and fast).
 *  2. For each theme scenario — default light, default dark, and the worst
 *     (lowest base fg/bg contrast) light + dark deck themes, computed live
 *     from src/data/theme-deck.json so this stays correct as themes are
 *     added/removed — force it via localStorage (same mechanism
 *     tests/e2e/theme-deck.spec.ts uses) and load the homepage.
 *  3. Resolve the *theoretical* (token) fg/border colors for a few real
 *     grained-surface targets via getComputedStyle (including the
 *     `::after` wobble-rule pseudo) — this is exact, browser-resolved OKLCH
 *     → sRGB, no reimplementation needed.
 *  4. Screenshot the viewport (masthead) and the footer (after scrolling it
 *     into view), decode the PNG via an in-page <canvas> (the browser's own
 *     PNG decoder — zero extra npm dependency), and sample a "clean strip"
 *     inside each grained surface: a band verified (by checking every real
 *     descendant element's bounding box) to contain no text/icons, so it's
 *     pure grain-over-background. Because the noise is spatially
 *     homogeneous, this strip's measured luminance range applies uniformly
 *     to the same surface's grain wherever it paints, including directly
 *     behind the real text/border sampled in step 3.
 *  5. Compute WCAG 2 contrast ratio between each target's token color and:
 *       - the token-only background (what today's audits already check)
 *       - the MEAN grain-perturbed background luminance (typical case)
 *       - the WORST grain-perturbed background luminance sampled (the
 *         strip extreme closest to the target's own luminance — i.e. the
 *         lowest contrast a reader could actually encounter)
 *     and flag anything whose grain-worst ratio drops below threshold.
 *  6. ADVISORY ONLY — always exits 0. This was a design-review "spot
 *     check" condition, not a hard gate (mirrors apca-audit.mjs's
 *     continue-on-error contract in .github/workflows).
 *
 * Thresholds (WCAG 2.1 relative-luminance contrast ratio):
 *   4.5:1 — normal/small text (nav links, footer text — all <18px here)
 *   3.0:1 — large text (nameplate title, ~36-68px) and non-text UI
 *           components / functional borders (WCAG 1.4.11; the wobble-rule
 *           bottom rule replaces the masthead's functional border)
 */
import { createServer } from 'node:http';
import { oklchToSrgb255, relLum255, contrastFromLum, TRANSFER_FN_SOURCE } from './lib/color.mjs';
import { readFile, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { extname, join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const here = dirname(fileURLToPath(import.meta.url));
const distDir = resolve(here, '../dist');
const themeDeckPath = resolve(here, '../src/data/theme-deck.json');

const PORT = 4319;

// ---------------------------------------------------------------------------
// OKLCH -> sRGB (0-255), same conversion apca-audit.mjs uses. Needed only to
// RANK deck themes by base fg/bg contrast so we can auto-pick the worst
// light/dark deck theme to test — the actual per-theme measurement below
// uses getComputedStyle (the browser's own OKLCH engine), not this.


function parseOklch(str) {
  const m = str.match(/oklch\(([\d.]+)\s+([\d.]+)\s+([\d.]+)\)/);
  if (!m) return null;
  return [parseFloat(m[1]), parseFloat(m[2]), parseFloat(m[3])];
}

function pickWorstDeckThemes(deckThemes) {
  const ranked = deckThemes.map((t) => {
    const bg = oklchToSrgb255(...parseOklch(t.tokens['--color-bg']));
    const fg = oklchToSrgb255(...parseOklch(t.tokens['--color-fg']));
    const ratio = contrastFromLum(relLum255(fg), relLum255(bg));
    return { slug: t.slug, isDark: t.isDark, ratio };
  });
  const worstLight = ranked.filter((t) => !t.isDark).sort((a, b) => a.ratio - b.ratio)[0];
  const worstDark = ranked.filter((t) => t.isDark).sort((a, b) => a.ratio - b.ratio)[0];
  return { worstLight, worstDark };
}

// ---------------------------------------------------------------------------
// Minimal static file server for dist/ (directory-per-route Astro output).
const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.avif': 'image/avif',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
  '.woff': 'font/woff',
  '.xml': 'application/xml; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
};

async function resolveDistFile(urlPath) {
  let p = decodeURIComponent(urlPath.split('?')[0].split('#')[0]);
  if (p.endsWith('/')) p += 'index.html';
  let full = join(distDir, p);
  if (existsSync(full)) {
    const st = await stat(full);
    if (st.isDirectory()) full = join(full, 'index.html');
    return full;
  }
  if (!extname(full)) {
    if (existsSync(full + '.html')) return full + '.html';
    const idx = join(full, 'index.html');
    if (existsSync(idx)) return idx;
  }
  return full; // let readFile throw -> 404
}

function startServer() {
  return new Promise((resolveP, reject) => {
    const server = createServer(async (req, res) => {
      try {
        const full = await resolveDistFile(req.url ?? '/');
        const data = await readFile(full);
        res.writeHead(200, { 'Content-Type': MIME[extname(full)] || 'application/octet-stream' });
        res.end(data);
      } catch {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not found');
      }
    });
    server.on('error', reject);
    server.listen(PORT, '127.0.0.1', () => resolveP(server));
  });
}

// ---------------------------------------------------------------------------
// Page-side helpers (run inside the browser via page.evaluate).

async function getComputedColors(page) {
  return page.evaluate(() => {
    function colorOf(sel) {
      const el = document.querySelector(sel);
      return el ? getComputedStyle(el).color : null;
    }
    function pseudoBgOf(sel, pseudo) {
      const el = document.querySelector(sel);
      return el ? getComputedStyle(el, pseudo).backgroundColor : null;
    }
    return {
      bg: getComputedStyle(document.body).backgroundColor,
      nameplateTitle: colorOf('.site-nameplate-title'),
      navLink: colorOf('.site-sections a:not([aria-current])'),
      footerText: colorOf('.site-footer > p:first-of-type'),
      footerLink: colorOf('.site-footer a'),
      wobbleBorder: pseudoBgOf('.site-masthead', '::after'),
    };
  });
}

// Find a horizontal band inside `containerSelector` that contains no visible
// descendant element (i.e. pure grain-over-background) — verified generically
// against real layout rather than hardcoded padding assumptions, so it stays
// correct across future markup edits. `bottomExclude` reserves px at the
// bottom of the container (e.g. to dodge the wobble-rule border band, which
// isn't a queryable DOM node).
async function findCleanStrip(page, containerSelector, bottomExclude = 0) {
  return page.evaluate(
    ({ containerSelector, bottomExclude }) => {
      const el = document.querySelector(containerSelector);
      if (!el) return null;
      const rect = el.getBoundingClientRect();
      const ranges = [];
      el.querySelectorAll('*').forEach((n) => {
        const r = n.getBoundingClientRect();
        if (r.width > 0 && r.height > 0) ranges.push([r.top, r.bottom]);
      });
      const stripHeight = 6;
      const top = Math.ceil(rect.top) + 1;
      const bottom = Math.floor(rect.bottom) - bottomExclude - stripHeight - 1;
      for (let y = top; y <= bottom; y++) {
        let clean = true;
        for (const [t, b] of ranges) {
          if (y < b + 1 && y + stripHeight > t - 1) {
            clean = false;
            break;
          }
        }
        if (clean) {
          return {
            x: Math.ceil(rect.left) + 6,
            y,
            width: Math.max(10, Math.floor(rect.width) - 12),
            height: stripHeight,
            fallback: false,
          };
        }
      }
      // Fallback: top edge of the container's own padding box.
      return {
        x: Math.ceil(rect.left) + 6,
        y: top,
        width: Math.max(10, Math.floor(rect.width) - 12),
        height: stripHeight,
        fallback: true,
      };
    },
    { containerSelector, bottomExclude }
  );
}

// Decode a PNG screenshot buffer via an in-page <canvas> (the browser's own
// PNG decoder — no image-decoding npm dependency needed) and return real
// composited luminance stats for each named rect.
async function samplePixelStats(page, pngBuffer, rects) {
  const base64 = pngBuffer.toString('base64');
  return page.evaluate(
    async ({ base64, rects }) => {
      const img = new Image();
      const loaded = new Promise((res, rej) => {
        img.onload = res;
        img.onerror = rej;
      });
      img.src = 'data:image/png;base64,' + base64;
      await loaded;
      const canvas = document.createElement('canvas');
      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;
      const ctx = canvas.getContext('2d', { willReadFrequently: true });
      ctx.drawImage(img, 0, 0);
      // Duplicated on purpose: this runs inside page.evaluate, where the
      // module scope is not available. It is pinned to lib/color.mjs's
      // TRANSFER_FN_SOURCE by tests/unit/color-drift.test.mjs, which fails
      // if the two ever disagree numerically (issue #506).
      function relLum(r, g, b) {
        const lin = [r, g, b].map((v) => {
          v /= 255;
          return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
        });
        return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2];
      }
      const out = {};
      for (const [key, rect] of Object.entries(rects)) {
        if (!rect) {
          out[key] = null;
          continue;
        }
        const x = Math.max(0, Math.min(canvas.width - 1, Math.round(rect.x)));
        const y = Math.max(0, Math.min(canvas.height - 1, Math.round(rect.y)));
        const w = Math.max(1, Math.min(canvas.width - x, Math.round(rect.width)));
        const h = Math.max(1, Math.min(canvas.height - y, Math.round(rect.height)));
        const data = ctx.getImageData(x, y, w, h).data;
        let min = Infinity;
        let max = -Infinity;
        let sum = 0;
        let n = 0;
        for (let i = 0; i < data.length; i += 4) {
          const l = relLum(data[i], data[i + 1], data[i + 2]);
          if (l < min) min = l;
          if (l > max) max = l;
          sum += l;
          n++;
        }
        out[key] = { min, max, mean: n ? sum / n : null, n };
      }
      return out;
    },
    { base64, rects }
  );
}

// getComputedStyle().color serialization varies by Chromium version: some
// resolve straight to rgb()/rgba(), others (CSS Color 4 aware) preserve the
// original color space and return e.g. `oklch(0.18 0.04 25)`. Handle both —
// reusing the same oklchToSrgb255 conversion apca-audit.mjs uses for the
// oklch() case.
function parseCssColor(str) {
  if (!str) return null;
  const oklchM = str.match(/oklch\(([\d.]+)\s+([\d.]+)\s+([\d.]+)/);
  if (oklchM) {
    const rgb = oklchToSrgb255(parseFloat(oklchM[1]), parseFloat(oklchM[2]), parseFloat(oklchM[3]));
    return { rgb, lum: relLum255(rgb) };
  }
  const rgbM = str.match(/rgba?\(([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)/);
  if (rgbM) {
    const rgb = [parseFloat(rgbM[1]), parseFloat(rgbM[2]), parseFloat(rgbM[3])];
    return { rgb, lum: relLum255(rgb) };
  }
  return null;
}

// ---------------------------------------------------------------------------

async function measureTheme(page, theme) {
  await page.addInitScript(
    ({ mode, deck }) => {
      try {
        if (deck) localStorage.setItem('themeDeck', `${deck}|${mode}`);
        else localStorage.setItem('theme', mode);
      } catch {
        /* storage blocked — theme falls back to CSS media query */
      }
    },
    { mode: theme.mode, deck: theme.deck }
  );
  await page.goto(`http://127.0.0.1:${PORT}/`, { waitUntil: 'load' });
  await page.waitForSelector('header.site-masthead.zine-grain');
  await page.waitForSelector('footer.site-footer.zine-grain');

  const colors = await getComputedColors(page);
  const bgTheoretical = parseCssColor(colors.bg);

  // ---- Masthead ----
  await page.evaluate(() => window.scrollTo(0, 0));
  const headerStrip = await findCleanStrip(page, 'header.site-masthead', 16);
  const headerShot = await page.screenshot();
  const headerStats = await samplePixelStats(page, headerShot, { strip: headerStrip });

  // ---- Footer ----
  await page.evaluate(() => {
    // behavior: 'instant' forces an immediate (non-animated) scroll,
    // bypassing global.css's `scroll-behavior: smooth` — 'auto' would
    // instead defer to that CSS property and animate over several frames,
    // leaving the very next screenshot taken before any scrolling occurred.
    document.querySelector('footer.site-footer')?.scrollIntoView({ block: 'end', behavior: 'instant' });
  });
  const footerStrip = await findCleanStrip(page, 'footer.site-footer', 0);
  const footerShot = await page.screenshot();
  const footerStats = await samplePixelStats(page, footerShot, { strip: footerStrip });

  const targets = [
    {
      surface: 'masthead',
      label: 'nameplate title (large text)',
      color: colors.nameplateTitle,
      threshold: 3.0,
      strip: headerStats.strip,
    },
    {
      surface: 'masthead',
      label: 'nav link (small text)',
      color: colors.navLink,
      threshold: 4.5,
      strip: headerStats.strip,
    },
    {
      surface: 'masthead',
      label: 'wobble-rule border (non-text)',
      color: colors.wobbleBorder,
      threshold: 3.0,
      strip: headerStats.strip,
    },
    {
      surface: 'footer',
      label: 'copyright text (small text)',
      color: colors.footerText,
      threshold: 4.5,
      strip: footerStats.strip,
    },
    {
      surface: 'footer',
      label: 'footer link (small text)',
      color: colors.footerLink,
      threshold: 4.5,
      strip: footerStats.strip,
    },
  ];

  const rows = targets.map((t) => {
    const fg = parseCssColor(t.color);
    if (!fg || !t.strip || !bgTheoretical) {
      return { ...t, error: 'missing color/strip data' };
    }
    const tokenRatio = contrastFromLum(fg.lum, bgTheoretical.lum);
    const meanRatio = contrastFromLum(fg.lum, t.strip.mean);
    // Worst-case: the sampled extreme (min or max luminance) closest to the
    // target's own luminance — i.e. the lowest contrast ratio grain could
    // actually produce right behind this text/border on this surface.
    const worstLum =
      Math.abs(t.strip.min - fg.lum) < Math.abs(t.strip.max - fg.lum) ? t.strip.min : t.strip.max;
    const worstRatio = contrastFromLum(fg.lum, worstLum);
    return {
      ...t,
      fgColor: t.color,
      tokenRatio,
      meanRatio,
      worstRatio,
      stripRange: [t.strip.min, t.strip.max],
      stripFallback: t.strip.fallback,
      pass: worstRatio >= t.threshold,
    };
  });

  return { colors, bgTheoretical, headerStrip, footerStrip, rows };
}

async function main() {
  if (!existsSync(distDir)) {
    console.error(
      `grain-contrast-audit: dist/ not found at ${distDir} — run \`pnpm build\` first.\n` +
      'This is a BROKEN run, not a clean one: an audit that samples zero pixels\n' +
      'must not be indistinguishable from one that found no problems (#511).\n' +
      'Contrast FINDINGS remain advisory; being unable to look does not.'
    );
    process.exit(1);
  }

  const deckThemes = JSON.parse(await readFile(themeDeckPath, 'utf8'));
  const { worstLight, worstDark } = pickWorstDeckThemes(deckThemes);

  const themes = [
    { name: 'default light', mode: 'light', deck: null },
    { name: 'default dark', mode: 'dark', deck: null },
    {
      name: `${worstLight.slug} (worst-base-contrast light deck, ${worstLight.ratio.toFixed(2)}:1)`,
      mode: 'light',
      deck: worstLight.slug,
    },
    {
      name: `${worstDark.slug} (worst-base-contrast dark deck, ${worstDark.ratio.toFixed(2)}:1)`,
      mode: 'dark',
      deck: worstDark.slug,
    },
  ];

  console.log('Grain composited-contrast audit — ADVISORY ONLY (issue #283 item 2)\n');
  console.log(
    `Serving ${distDir} at http://127.0.0.1:${PORT}, sampling real composited pixels via Chromium...\n`
  );

  const server = await startServer();
  const browser = await chromium.launch();
  let totalWarnings = 0;
  const allResults = [];

  try {
    for (const theme of themes) {
      const context = await browser.newContext({
        viewport: { width: 1440, height: 1000 },
        deviceScaleFactor: 1,
      });
      const page = await context.newPage();
      const result = await measureTheme(page, theme);
      allResults.push({ theme, result });
      await context.close();
    }
  } finally {
    await browser.close();
    server.close();
  }

  // Report
  for (const { theme, result } of allResults) {
    console.log(`\n=== ${theme.name} ===`);
    for (const row of result.rows) {
      if (row.error) {
        console.log(`  [ERROR ] ${row.surface.padEnd(9)} ${row.label.padEnd(30)} ${row.error}`);
        totalWarnings++;
        continue;
      }
      const status = row.pass ? 'OK    ' : 'REVIEW';
      if (!row.pass) totalWarnings++;
      console.log(
        `  [${status}] ${row.surface.padEnd(9)} ${row.label.padEnd(30)} ` +
          `token ${row.tokenRatio.toFixed(2).padStart(6)}:1  ` +
          `grain-mean ${row.meanRatio.toFixed(2).padStart(6)}:1  ` +
          `grain-worst ${row.worstRatio.toFixed(2).padStart(6)}:1  ` +
          `(target >=${row.threshold}:1)` +
          (row.stripFallback ? '  [clean-strip: fallback band]' : '')
      );
    }
  }

  console.log('\n--- Real-pixel grain luminance range sampled per surface ---');
  for (const { theme, result } of allResults) {
    const h = result.headerStrip;
    const f = result.footerStrip;
    const hStats = result.rows.find((r) => r.surface === 'masthead' && r.stripRange)?.stripRange;
    const fStats = result.rows.find((r) => r.surface === 'footer' && r.stripRange)?.stripRange;
    console.log(
      `  ${theme.name.padEnd(55)} masthead strip @(${h?.x},${h?.y}) L=[${hStats?.[0]?.toFixed(4)}, ${hStats?.[1]?.toFixed(4)}]  ` +
        `footer strip @(${f?.x},${f?.y}) L=[${fStats?.[0]?.toFixed(4)}, ${fStats?.[1]?.toFixed(4)}]`
    );
  }

  if (totalWarnings > 0) {
    console.log(
      `\n${totalWarnings} target(s) fall below their WCAG threshold under worst-case grain compositing.`
    );
    console.error('These are real WCAG failures in composited output. Fix the deck\n'
      + 'tokens (see DESIGN-DEVIATIONS.md) — this check is a gate now.');
  } else {
    console.log(
      '\nAll sampled targets stay at or above their WCAG threshold under worst-case grain compositing.'
    );
  }

  // This IS a gate now (issue #511). It was the only checker in the repo
  // measuring real composited pixels, and it was neutered twice — hardcoded
  // exit 0 here plus continue-on-error in a11y.yml — while reporting four
  // genuine WCAG failures in solarized-dark-higher-contrast on every green
  // run. Those are fixed; this keeps them fixed.
  process.exit(totalWarnings > 0 ? 1 : 0);
}

// A crash is a broken run. The findings this audit reports are advisory
// (pending the design decision on solarized-dark-higher-contrast), but an
// exception means it never measured anything — which previously exited 0
// and read as a pass.
main().catch((err) => {
  console.error(`grain-contrast-audit failed to run: ${err?.stack || err}`);
  process.exit(1);
});
