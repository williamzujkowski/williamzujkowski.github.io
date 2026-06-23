import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { renderOgCard } from '../../og/card';

export async function getStaticPaths() {
  const posts = await getCollection('posts', ({ data }) => !data.draft);
  return posts.map((post) => ({ params: { slug: post.id }, props: { post } }));
}

export const GET: APIRoute = async ({ props }) => {
  const post = (props as { post: { data: { title: string; date: Date; tags?: string[] } } }).post;
  const date = new Date(post.data.date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    timeZone: 'UTC', // dates are UTC-midnight; format in UTC for consistency
  });
  const tag = post.data.tags?.[0];
  const subtitle = tag ? `${date} · ${tag}` : date;

  const png = await renderOgCard({ title: post.data.title, subtitle });

  return new Response(new Uint8Array(png), {
    headers: {
      'Content-Type': 'image/png',
      'Cache-Control': 'public, max-age=31536000, immutable',
    },
  });
};
