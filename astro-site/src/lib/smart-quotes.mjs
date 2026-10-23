/**
 * Typographic quotes for strings that never pass through Markdown.
 *
 * remark-smartypants (astro.config.mjs) curls post BODIES, but titles and
 * descriptions are frontmatter strings: they rendered with typewriter
 * apostrophes in 30–60px display type on the front page, the archive,
 * related lists, feeds and OG cards (design review 2026-10). The post
 * schema runs both fields through this once, so every surface agrees.
 *
 * Rules, in order: an apostrophe inside or closing a word is ’; a double
 * quote opens after start/space/bracket/dash, otherwise closes; a leftover
 * single quote opens the same way, otherwise is ’. Backticked spans are
 * left alone — they are code, where a straight quote is the spelling.
 */
export function smartQuotes(text) {
  if (typeof text !== 'string' || !/["']/.test(text)) return text;
  return text
    .split(/(`[^`]*`)/)
    .map((part, i) => (i % 2 ? part : curl(part)))
    .join('');
}

function curl(s) {
  return s
    .replace(/(?<=\w)'(?=\w)/g, '’')
    .replace(/(?<=[\w.,!?])'(?=\s|$|[.,;:!?)])/g, '’')
    .replace(/(^|[\s([—–])"/g, '$1“')
    .replace(/"/g, '”')
    .replace(/(^|[\s([—])'/g, '$1‘')
    .replace(/'/g, '’');
}
