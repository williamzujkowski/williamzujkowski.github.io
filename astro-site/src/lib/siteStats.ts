import { getCollection } from 'astro:content';
import { execSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

/**
 * Canonical site-wide stats derived at build time.
 * Single source of truth so no page duplicates counting logic.
 */
export async function getSiteStats() {
  const allPosts = await getCollection('posts', ({ data }) => !data.draft);
  const posts = allPosts.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
  const tagSet = new Set<string>();
  posts.forEach((p) =>
    (p.data.tags ?? []).filter((t: string) => t !== 'posts').forEach((t: string) => tagSet.add(t)),
  );
  const years = new Set<number>(posts.map((p) => p.data.date.getFullYear()));
  const latest = posts[0]?.data.date ?? new Date();
  const currentYear = new Date().getFullYear();
  return {
    postCount: posts.length,
    tagCount: tagSet.size,
    yearCount: years.size,
    latest,
    latestISO: latest.toISOString().split('T')[0],
    currentYear,
    volume: toRoman(currentYear),
  };
}

/** Roman-numeral formatter for masthead "Vol." markers. */
export function toRoman(n: number): string {
  const map: Array<[number, string]> = [
    [1000, 'M'], [900, 'CM'], [500, 'D'], [400, 'CD'],
    [100, 'C'], [90, 'XC'], [50, 'L'], [40, 'XL'],
    [10, 'X'], [9, 'IX'], [5, 'V'], [4, 'IV'], [1, 'I'],
  ];
  let out = '';
  let v = n;
  for (const [num, letter] of map) {
    while (v >= num) {
      out += letter;
      v -= num;
    }
  }
  return out;
}

/**
 * Git mtime for a source file, falls back to current date.
 * Use for pages like /now/ where "last updated" should be live.
 */
export function gitMtime(importMetaUrl: string): Date {
  try {
    const path = fileURLToPath(importMetaUrl);
    if (!existsSync(path)) return new Date();
    const iso = execSync(`git log -1 --format=%cI -- "${path}"`, {
      cwd: path.substring(0, path.lastIndexOf('/')),
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
    }).trim();
    if (!iso) return new Date();
    return new Date(iso);
  } catch {
    return new Date();
  }
}

export function formatDate(d: Date): string {
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}
