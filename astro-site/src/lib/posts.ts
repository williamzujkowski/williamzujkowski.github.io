import { getCollection } from 'astro:content';
import { selectPublishedPosts } from './publication.mjs';

/** The publication's non-draft posts, newest first with stable ID ties. */
export async function getPublishedPosts() {
  return selectPublishedPosts(await getCollection('posts'));
}
