import { getPublishedPosts } from '@/lib/posts';
import { countPostTags, postsByUTCYear } from './publication.mjs';

/**
 * Canonical site-wide stats derived at build time.
 * Single source of truth so no page duplicates counting logic.
 */
export async function getSiteStats() {
  const posts = await getPublishedPosts();
  const tagCount = countPostTags(posts).size;
  const yearCount = postsByUTCYear(posts).size;
  const latest = posts[0]?.data.date ?? new Date();
  const earliest = posts[posts.length - 1]?.data.date ?? new Date();
  const currentYear = new Date().getUTCFullYear();
  const earliestYear = earliest.getUTCFullYear();
  return {
    postCount: posts.length,
    tagCount,
    yearCount,
    latest,
    latestISO: latest.toISOString().split('T')[0],
    earliest,
    earliestYear,
    currentYear,
    volume: toRoman(currentYear),
    established: toRoman(earliestYear),
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

export function formatDate(d: Date): string {
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    timeZone: 'UTC', // dates are UTC-midnight; format in UTC so text matches <time datetime>
  });
}
