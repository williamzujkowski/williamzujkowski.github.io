import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseFrontmatter } from '@astrojs/markdown-remark';
import { postSchema } from '../../src/lib/post-schema.mjs';

// Read the cutoff captured by the build. Taking a fresh clock reading here can
// disagree with a build that crossed UTC midnight between these imports.
const manifestPath = fileURLToPath(new URL('../../dist/publication-cutoff.json', import.meta.url));
if (!existsSync(manifestPath)) {
  throw new Error('dist/publication-cutoff.json is missing; run the production build before e2e tests');
}
const manifest = JSON.parse(readFileSync(manifestPath, 'utf8')) as { cutoff?: string };
if (typeof manifest.cutoff !== 'string') throw new Error('publication cutoff manifest is invalid');
const cutoffDate = new Date(manifest.cutoff);
if (!Number.isFinite(cutoffDate.getTime())) throw new Error('publication cutoff manifest has an invalid timestamp');

// Parse real YAML (quoted dates, block tags and inline comments included).
const postsDir = fileURLToPath(new URL('../../../src/posts/', import.meta.url));
const cutoff = cutoffDate.getTime();
export const sourcePosts = readdirSync(postsDir).filter((name) => name.endsWith('.md'))
  .map((name) => ({
    id: name.slice(0, -3),
    data: postSchema.parse(parseFrontmatter(readFileSync(join(postsDir, name), 'utf8')).frontmatter),
  }));
export const hiddenPosts = sourcePosts.filter((post) => post.data.draft || post.data.date.getTime() > cutoff);
export const expectedPosts = sourcePosts.filter((post) => !post.data.draft && post.data.date.getTime() <= cutoff)
  .sort((a, b) => b.data.date.getTime() - a.data.date.getTime()
    || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
