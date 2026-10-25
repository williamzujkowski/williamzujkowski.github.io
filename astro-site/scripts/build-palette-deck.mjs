#!/usr/bin/env node
/*
 * Builds the site's theme deck with remarque-deck (remarque-tokens 0.31+):
 * remarque's curated light/dark pairs, plus Kanagawa (Lotus/Wave), each
 * derived from @williamzujkowski/oklch-terminal-themes (pinned exactly in
 * devDependencies, so the colors are pinned too) and audited before it's
 * written. Replaces the frozen theme-deck.css, whose Python generator was
 * gone. Runs first in `pnpm dev` and `pnpm build`.
 *
 *   public/palettes/deck.css   every palette + picker swatches (incl. the
 *                              site's own palette, from global.css)
 *   public/palettes/deck.json  the manifest ThemeDeck.astro renders
 *   src/data/theme-deck-attribution.json
 *                              upstream sources for the About page credits
 *
 * public/palettes/ is gitignored; the attribution file is committed so
 * `astro check` can resolve its import before any build.
 */
import { execFileSync } from 'node:child_process';
import { readFileSync, rmSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const site = join(dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(import.meta.url);
const deckBin = join(dirname(require.resolve('remarque-tokens/package.json')), 'scripts', 'deck.mjs');
const outDir = join(site, 'public', 'palettes');

// Beyond the curated set: Kanagawa was in the old deck, and the dataset
// has both halves (it just doesn't link them as counterparts).
const EXTRA = ['kanagawa-lotus:kanagawa-wave=kanagawa'];

execFileSync('node', [deckBin, '--curated', ...EXTRA, '--default', join(site, 'src', 'styles', 'global.css'), '--out-dir', outDir], {
  cwd: site,
  stdio: ['ignore', 'ignore', 'inherit'],
});

const manifest = JSON.parse(readFileSync(join(outDir, 'deck.json'), 'utf8'));
// A CLI entry's label defaults to its name; give the extras real labels.
const LABELS = { kanagawa: 'Kanagawa' };
for (const p of manifest.palettes) if (LABELS[p.name]) p.label = LABELS[p.name];
writeFileSync(join(outDir, 'deck.json'), JSON.stringify(manifest, null, 2) + '\n');
// The site loads only deck.css; drop the per-palette copies remarque-deck
// also writes, so they don't ship in dist/.
for (const p of manifest.palettes) rmSync(join(outDir, p.css));
const dataset = (slug) => require(`@williamzujkowski/oklch-terminal-themes/themes/${slug}.json`);
const credits = manifest.palettes.flatMap((p) => [p.light, p.dark]).map((slug) => {
  const t = dataset(slug);
  return { slug, name: t.name, source: t.source, sourceUrl: t.sourceUrl };
});
writeFileSync(join(site, 'src', 'data', 'theme-deck-attribution.json'), JSON.stringify(credits, null, 2) + '\n');
console.error(`build-palette-deck: ${manifest.palettes.length} palettes, ${credits.length} credited themes`);
