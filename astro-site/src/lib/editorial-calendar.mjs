/**
 * Scheduling conflicts among posts that have not been published yet.
 *
 * A scheduled post is `draft: false` with a date after the cutoff. Two of them
 * on the same day, or within MIN_GAP_DAYS of each other or of the newest
 * published post, compete for the same readers and the same daily deploy.
 * Nothing else notices: the build happily publishes both.
 *
 * Published history is left alone. Four old posts carry a filename date that
 * differs from their frontmatter date, and the filename is the URL, so they
 * cannot be "fixed". The rules below apply only to posts still in the future,
 * where renaming the file is free.
 */

export const MIN_GAP_DAYS = 3;
const DAY_MS = 86_400_000;

/**
 * @param {readonly { file: string, date: Date, draft?: boolean }[]} posts
 * @param {Date} now Publication cutoff (same meaning as selectPublishedPosts).
 * @param {number} [minGapDays]
 * @returns {string[]} Human-readable conflicts; empty means the calendar is clean.
 */
export function calendarConflicts(posts, now, minGapDays = MIN_GAP_DAYS) {
  const cutoff = now.getTime();
  if (!Number.isFinite(cutoff)) throw new TypeError('Calendar cutoff must be a valid Date');
  const live = posts.filter((p) => !p.draft).sort((a, b) => a.date.getTime() - b.date.getTime());
  const scheduled = live.filter((p) => p.date.getTime() > cutoff);
  const problems = [];

  for (const post of scheduled) {
    const iso = post.date.toISOString().slice(0, 10);
    if (!post.file.startsWith(`${iso}-`)) {
      problems.push(`${post.file}: scheduled for ${iso} but the filename says otherwise`);
    }
  }

  // Each scheduled post against its predecessor, which may be a published one.
  for (let i = 1; i < live.length; i += 1) {
    const prev = live[i - 1];
    const next = live[i];
    if (next.date.getTime() <= cutoff) continue;
    const gap = (next.date.getTime() - prev.date.getTime()) / DAY_MS;
    if (gap < minGapDays) {
      problems.push(
        `${next.file}: ${gap === 0 ? 'same day as' : `${gap} day(s) after`} ${prev.file} (minimum ${minGapDays})`,
      );
    }
  }
  return problems;
}
