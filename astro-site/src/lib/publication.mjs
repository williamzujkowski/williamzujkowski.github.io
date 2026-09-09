/**
 * Pure publication metadata. Consumers pass the same newest-first, non-draft
 * post list to numbering and taxonomy helpers; nothing is cached between builds.
 */

/**
 * @template {{ id: string, data: { date: Date, draft?: boolean } }} T
 * @param {readonly T[]} posts
 * @returns {T[]}
 */
export function selectPublishedPosts(posts) {
  return posts.filter((post) => !post.data.draft).sort((a, b) =>
    b.data.date.getTime() - a.data.date.getTime()
      || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0),
  );
}

/** @param {{ tags?: readonly string[] }} data */
export function postTags(data) {
  return [...new Set((data.tags ?? []).filter((tag) => tag !== 'posts'))];
}

/** @param {readonly { data: { tags?: readonly string[] } }[]} posts */
export function countPostTags(posts) {
  /** @type {Map<string, number>} */
  const counts = new Map();
  for (const post of posts) {
    for (const tag of postTags(post.data)) counts.set(tag, (counts.get(tag) ?? 0) + 1);
  }
  return counts;
}

/** @param {readonly { id: string }[]} posts Newest first. */
export function postPieceNumbers(posts) {
  return new Map(posts.map((post, index) => [post.id, posts.length - index]));
}

/**
 * @template {{ data: { date: Date } }} T
 * @param {readonly T[]} posts Newest first.
 * @returns {Map<number, T[]>}
 */
export function postsByUTCYear(posts) {
  /** @type {Map<number, T[]>} */
  const years = new Map();
  for (const post of posts) {
    const year = post.data.date.getUTCFullYear();
    if (!years.has(year)) years.set(year, []);
    years.get(year).push(post);
  }
  return years;
}
