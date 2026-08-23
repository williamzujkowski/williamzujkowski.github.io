import sanitizeHtml from 'sanitize-html';
import MarkdownIt from 'markdown-it';
import footnote from 'markdown-it-footnote';

/**
 * Render a post body for syndication.
 *
 * Both feeds previously did this inline with a bare `new MarkdownIt()`, which
 * produced two defects (issue #499):
 *
 *   1. **Relative URLs.** Feed content is resolved against the READER's base
 *      URI, not the site's, so all 75 root-relative cross-links in the corpus
 *      were dead for every subscriber. markdown-it has no base-URL option and
 *      nothing rewrote them.
 *
 *   2. **Raw footnote syntax.** The site pipeline runs remark-gfm via Astro;
 *      this parser was stock, so `[^id]` markers rendered as literal text and
 *      the definitions became an orphan paragraph with no referents.
 *
 * Shared so the two feeds cannot drift apart again — they had already diverged
 * from the site's own rendering, which is how both defects survived.
 */
const parser = new MarkdownIt().use(footnote);

/** Absolutise root-relative href/src values against the site origin. */
export function absolutiseUrls(html: string, siteUrl: string): string {
  const base = siteUrl.replace(/\/$/, '');
  // Only `/path` — never `//host` (protocol-relative) and never `/` inside an
  // already-absolute URL, since the attribute value must START with the slash.
  return html.replace(
    /(\s(?:href|src)=)(["'])(\/(?!\/)[^"']*)\2/g,
    (_m, attr, quote, path) => `${attr}${quote}${base}${path}${quote}`,
  );
}

export function renderPostForFeed(body: string, siteUrl: string): string {
  const html = sanitizeHtml(parser.render(body ?? ''), {
    allowedTags: sanitizeHtml.defaults.allowedTags.concat(['img']),
    allowedAttributes: {
      ...sanitizeHtml.defaults.allowedAttributes,
      // Footnotes are only useful if the jump works. The default schema
      // strips id/class, which left a numbered marker linking to nothing.
      // Scoped to the elements the footnote plugin actually emits.
      a: [...(sanitizeHtml.defaults.allowedAttributes.a ?? []), 'id', 'class'],
      li: ['id', 'class'],
      sup: ['class'],
      section: ['class'],
      ol: ['class'],
      hr: ['class'],
      img: ['src', 'alt', 'title'],
    },
  });
  return absolutiseUrls(html, siteUrl);
}
