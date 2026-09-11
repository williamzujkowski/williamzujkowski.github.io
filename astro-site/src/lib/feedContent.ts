import sanitizeHtml from 'sanitize-html';
import MarkdownIt from 'markdown-it';
import footnote from 'markdown-it-footnote';

// Both feeds share this renderer. Authored HTML must reach the sanitizer as
// markup; escaping it first exposes diagram source in feed readers (#581).
const parser = new MarkdownIt({ html: true }).use(footnote);

const feedPolicy: sanitizeHtml.IOptions = {
  allowedTags: sanitizeHtml.defaults.allowedTags.concat(['img']),
  allowedAttributes: {
    ...sanitizeHtml.defaults.allowedAttributes,
    // Keep the footnote plugin's jump targets and back references (#499).
    a: [...(sanitizeHtml.defaults.allowedAttributes.a ?? []), 'id', 'class'],
    li: ['id', 'class'],
    sup: ['class'],
    section: ['class'],
    ol: ['class'],
    hr: ['class'],
    img: ['src', 'alt', 'title'],
  },
  allowedClasses: {
    a: ['footnote-ref', 'footnote-backref'],
    li: ['footnote-item'],
    sup: ['footnote-ref'],
    section: ['footnotes'],
    ol: ['footnotes-list'],
    hr: ['footnotes-sep'],
  },
  // Discard the contents too; these elements have no feed fallback.
  nonTextTags: ['script', 'style', 'textarea', 'option', 'iframe', 'object', 'embed', 'svg', 'math', 'template'],
};

export function renderPostForFeed(body: string, siteUrl: string): string {
  const base = siteUrl.replace(/\/$/, '');
  const diagramNodes: boolean[] = [];
  const normalized = sanitizeHtml(parser.render(body ?? ''), {
    ...feedPolicy,
    allowedAttributes: {
      ...feedPolicy.allowedAttributes,
      div: ['data-feed-label', 'data-feed-doodle'],
      i: ['data-feed-detail'],
      span: ['data-feed-detail'],
    },
    // Remove the decorative subtree without changing the parser's tag name.
    exclusiveFilter: (frame) => frame.attribs['data-feed-doodle'] === 'true',
    onOpenTag: (_tagName, attribs) => {
      const classes = (attribs.class ?? '').split(/\s+/);
      diagramNodes.push(classes.some((name) => ['flow-node', 'arch-chip', 'seq-step'].includes(name)));
    },
    onCloseTag: () => { diagramNodes.pop(); },
    transformTags: {
      '*': (tagName, attribs) => {
        // Never rewrite text containing href/src, especially code examples.
        for (const name of ['href', 'src']) {
          if (/^\/(?!\/)/.test(attribs[name] ?? '')) attribs[name] = base + attribs[name];
        }
        delete attribs['data-feed-label'];
        delete attribs['data-feed-doodle'];
        delete attribs['data-feed-detail'];
        if ((tagName === 'i' || tagName === 'span') && diagramNodes.at(-2)) {
          attribs['data-feed-detail'] = 'true';
        }
        const classes = new Set((attribs.class ?? '').split(/\s+/));
        if (tagName === 'div' && classes.has('zine-doodle')) {
          return { tagName: 'div', attribs: { 'data-feed-doodle': 'true' } };
        }
        // CSS normally supplies these labels and makes chips separate blocks.
        // A temporary attribute lets the HTML parser escape labels without
        // transformTags.text replacing the element's own text or children.
        let label: string | undefined;
        if (tagName === 'section' && classes.has('arch-tier')) label = attribs['data-label'];
        if (tagName === 'div' && classes.has('flow-leg')) label = attribs['data-branch'];
        if (tagName === 'div' && classes.has('flow-parallel')) label = attribs['aria-label'] || 'Parallel steps';
        if (label) return { tagName: 'div', attribs: { 'data-feed-label': label } };
        if (tagName === 'span' && classes.has('arch-chip')) return { tagName: 'div', attribs: {} };
        return { tagName, attribs };
      },
    },
  });
  // This matches only our canonical, escaped sanitizer output, never raw HTML
  // or Markdown. Keep entity escaping intact while moving labels into text.
  const readable = normalized
    .replace(/<div data-feed-label="([^"]*)">/g, '<div><p><strong>$1</strong></p>')
    .replace(/<(i|span) data-feed-detail="true">/g, ' <$1>');
  return sanitizeHtml(readable, feedPolicy);
}
