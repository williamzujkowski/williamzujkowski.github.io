import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseFrontmatter } from '@astrojs/markdown-remark';
import { postSchema } from '../../src/lib/post-schema.mjs';
import { publicationClock } from '../../src/lib/publication-clock.mjs';

// Run tests with the same PUBLICATION_AS_OF value as a local preview build.
// Parse real YAML (quoted dates, block tags and inline comments included).
const postsDir = fileURLToPath(new URL('../../../src/posts/', import.meta.url));
const cutoff = publicationClock().getTime();
export const sourcePosts = readdirSync(postsDir).filter((name) => name.endsWith('.md'))
  .map((name) => ({
    id: name.slice(0, -3),
    data: postSchema.parse(parseFrontmatter(readFileSync(join(postsDir, name), 'utf8')).frontmatter),
  }));
export const hiddenPosts = sourcePosts.filter((post) => post.data.draft || post.data.date.getTime() > cutoff);
export const expectedPosts = sourcePosts.filter((post) => !post.data.draft && post.data.date.getTime() <= cutoff)
  .sort((a, b) => b.data.date.getTime() - a.data.date.getTime()
    || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
