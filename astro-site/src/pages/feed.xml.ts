import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';
import sanitizeHtml from 'sanitize-html';
import MarkdownIt from 'markdown-it';
import { SITE_CONFIG } from '@/lib/siteConfig';
import { getValidImageUrl } from '@/lib/utils';

const parser = new MarkdownIt();

export async function GET(context: APIContext) {
  const posts = await getCollection('posts', ({ data }) => !data.draft);
  const sortedPosts = posts.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
  const siteUrl = context.site?.toString() ?? SITE_CONFIG.siteUrl;

  return rss({
    title: SITE_CONFIG.author,
    description: SITE_CONFIG.rssDescription,
    site: siteUrl,
    xmlns: {
      atom: 'http://www.w3.org/2005/Atom',
    },
    customData: `<atom:link href="${siteUrl}/feed.xml" rel="self" type="application/rss+xml"/>`,
    items: sortedPosts.map((post) => {
      const imageUrl = getValidImageUrl(post.data.image);
      const renderedContent = sanitizeHtml(parser.render(post.body ?? ''), {
        allowedTags: sanitizeHtml.defaults.allowedTags.concat(['img']),
      });
      // Prepend cover image to content if available
      const contentWithImage = imageUrl
        ? `<p><img src="${imageUrl}" alt="${post.data.title}" width="1200" height="630" /></p>${renderedContent}`
        : renderedContent;

      return {
        title: post.data.title,
        pubDate: post.data.date,
        description: post.data.description ?? '',
        link: `/posts/${post.id}/`,
        categories: post.data.tags?.filter((t: string) => t !== 'posts'),
        content: contentWithImage,
      };
    }),
  });
}
