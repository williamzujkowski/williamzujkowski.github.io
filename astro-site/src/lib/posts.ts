import { getCollection } from 'astro:content';
import { countPostTags, kickerTag, selectPublishedPosts } from './publication.mjs';
import { publicationClock } from './publication-clock.mjs';

// Every consumer in this build uses the same cutoff, even across UTC midnight.
const publicationCutoff = publicationClock();

/** Eligible non-draft posts at the build cutoff, newest first with stable ID ties. */
export async function getPublishedPosts() {
  return selectPublishedPosts(await getCollection('posts'), publicationCutoff);
}

/** The kicker tag for a post, ranked against this build's published posts. */
export async function getKickerTag(data: { tags?: readonly string[] }) {
  return kickerTag(data, countPostTags(await getPublishedPosts()));
}
