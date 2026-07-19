import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';
import sanitizeHtml from 'sanitize-html';
import MarkdownIt from 'markdown-it';
import { SITE_CONFIG } from '@/lib/siteConfig';

const parser = new MarkdownIt();

// JSON Feed 1.1 — https://jsonfeed.org/version/1.1
// Mirrors feed.xml.ts: same post set, same full (non-truncated) content_html.
export async function GET(context: APIContext) {
  const posts = await getCollection('posts', ({ data }) => !data.draft);
  const sortedPosts = posts.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
  const siteUrl = (context.site?.toString() ?? SITE_CONFIG.siteUrl).replace(/\/$/, '');

  const items = sortedPosts.map((post) => {
    const url = `${siteUrl}/posts/${post.id}/`;
    const contentHtml = sanitizeHtml(parser.render(post.body ?? ''), {
      allowedTags: sanitizeHtml.defaults.allowedTags.concat(['img']),
    });

    return {
      id: url,
      url,
      title: post.data.title,
      content_html: contentHtml,
      summary: post.data.description ?? undefined,
      date_published: post.data.date.toISOString(),
      date_modified: post.data.lastUpdate?.toISOString(),
      author: { name: post.data.author ?? SITE_CONFIG.author },
      tags: post.data.tags?.filter((t: string) => t !== 'posts'),
    };
  });

  const feed = {
    version: 'https://jsonfeed.org/version/1.1',
    title: SITE_CONFIG.author,
    home_page_url: `${siteUrl}/`,
    feed_url: `${siteUrl}/feed.json`,
    description: SITE_CONFIG.rssDescription,
    author: { name: SITE_CONFIG.author },
    items,
  };

  return new Response(JSON.stringify(feed, null, 2), {
    headers: {
      'Content-Type': 'application/feed+json; charset=utf-8',
    },
  });
}
