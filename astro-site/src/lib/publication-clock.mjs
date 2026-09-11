/**
 * Capture once per build in posts.ts. A local preview may supply an explicit UTC
 * timestamp; CI deployments always use the actual clock, never a preview date.
 * @param {Record<string, string | undefined>} [env]
 * @param {Date} [now]
 * @returns {Date}
 */
export function publicationClock(env = process.env, now = new Date()) {
  const override = env.PUBLICATION_AS_OF;
  if (override !== undefined) {
    if (env.CI || env.GITHUB_ACTIONS) {
      throw new Error('PUBLICATION_AS_OF is for local previews and must not be set in CI');
    }
    if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$/.test(override)) {
      throw new TypeError('PUBLICATION_AS_OF must be an explicit UTC ISO timestamp ending in Z');
    }
    const parsed = new Date(override);
    const canonical = override.includes('.') ? override : override.replace('Z', '.000Z');
    if (!Number.isFinite(parsed.getTime()) || parsed.toISOString() !== canonical) {
      throw new TypeError('PUBLICATION_AS_OF must be a valid UTC date and time');
    }
    return parsed;
  }
  if (!Number.isFinite(now.getTime())) throw new TypeError('Publication clock must be a valid Date');
  return new Date(now.getTime());
}
