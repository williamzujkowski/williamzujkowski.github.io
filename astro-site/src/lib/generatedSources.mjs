import { resolveSources, collectHits, transformSourceMarginalia } from './rehype-source-marginalia.mjs';

/**
 * Generated "Sources" bibliography for inline-citing posts.
 *
 * A post that cites with ordinary inline links and has NO hand-written
 * `## Sources` list and NO GFM footnotes gets its margin notes from
 * src/data/citations.json (rehype-source-marginalia.mjs, "CITATION-FILE
 * FALLBACK"). This module lists the same citations at the end of the post, on
 * the page and in both feeds, so the notes are not the only place a source is
 * named.
 *
 * ONE function decides what is listed: generatedSourceItems(). It reuses the
 * plugin's own eligibility (resolveSources: http/https only, own-domain and
 * GitHub blob/commit/tree/compare links skipped, footnote and Sources-heading
 * posts excluded) and its own link walk (collectHits: first link per URL, one
 * entry per citation title, body paragraphs and list items only), and the same
 * `Title · Publisher · Year` parts with the same publisher elision. It does
 * NOT apply echo suppression: a note that only repeats its sentence is dropped
 * from the margin, but a bibliography lists every cited source.
 *
 * Order is first-link order in the body. The page appends the list after the
 * margin-note plugin has run, so the plugin never sees it as a hand-written
 * Sources list. The feeds append the same items as plain h2 + ul HTML.
 */

/** Marker for tooling (rendered-text gate, tests): class and data attribute on the wrapper. */
export const GENERATED_SOURCES_CLASS = 'generated-sources';
export const GENERATED_SOURCES_ATTR = 'dataGeneratedSources';

/**
 * @param {object} tree hast root of the post body
 * @param {Record<string, object>} citations src/data/citations.json
 * @returns {{ href: string, title: string, publisher: string | null, year: string | null }[]}
 */
export function generatedSourceItems(tree, citations) {
  const sources = resolveSources(tree, { citations });
  if (!sources || !sources.fallback) return [];
  return collectHits(tree, sources)
    .filter((h) => h.li.parts)
    .map((h) => ({ href: h.link.properties.href, ...h.li.parts }));
}

const el = (tagName, properties, children) => ({ type: 'element', tagName, properties, children });
const text = (value) => ({ type: 'text', value });

/** `<a href>Title</a> · Publisher · Year`, missing parts omitted. */
function itemNode(item) {
  const tail = [item.publisher, item.year].filter(Boolean).map((p) => ` · ${p}`).join('');
  return el('li', {}, [el('a', { href: item.href }, [text(item.title)]), ...(tail ? [text(tail)] : [])]);
}

/** The heading and list, as a hast fragment (what an older post's `## Sources` renders to). */
export function sourcesListNodes(items) {
  return [
    el('h2', { id: 'sources' }, [text('Sources')]),
    el('ul', {}, items.map(itemNode)),
  ];
}

/**
 * The page block: the same h2 + ul inside a marked wrapper. A <div>, not a
 * <section>: global.css gives `.prose section > h2` a different top margin.
 * data-pagefind-ignore keeps the search index as it was (titles already in
 * the body would otherwise be indexed twice).
 */
export function generatedSourcesBlock(items) {
  return el(
    'div',
    { className: [GENERATED_SOURCES_CLASS], [GENERATED_SOURCES_ATTR]: '', dataPagefindIgnore: '' },
    sourcesListNodes(items)
  );
}

/**
 * Margin notes, then the generated list, for one post. The list is computed
 * BEFORE the notes are inserted (the notes' refs would otherwise look like
 * footnotes to resolveSources) and appended AFTER them (so the margin-note
 * plugin never reads the list as a hand-written Sources heading). Posts
 * without `marginNotes: true` are untouched, as before.
 */
export function transformNotesAndSources(tree, options = {}) {
  const items = generatedSourceItems(tree, options.citations);
  transformSourceMarginalia(tree, options);
  if (items.length) tree.children.push(generatedSourcesBlock(items));
  return tree;
}

/** unified/rehype plugin factory: replaces rehypeSourceMarginalia in the pipeline. */
export default function rehypeSourceNotesAndList(options = {}) {
  return (tree, file) => {
    if (file?.data?.astro?.frontmatter?.marginNotes !== true) return;
    transformNotesAndSources(tree, options);
  };
}
