import { smartQuotes } from './smart-quotes.mjs';

const CODE = new Set(['code', 'pre', 'kbd', 'samp', 'script', 'style']);
// `open("/etc/shadow", O_RDONLY)` in a diagram is code set in prose type —
// a call is spelled with straight quotes, so leave call-shaped text alone.
const CALL = /\w\(["']/;

/** Curl quotes in raw-HTML text that remark-smartypants never sees.
 * smartypants runs on the Markdown tree, so a post's hand-written
 * <figcaption>, .hand-note doodle caption or .flow/.arch diagram label kept
 * typewriter apostrophes (19 nodes across 17 posts, design review 2026-10).
 * Runs after rehype-raw; text smartypants already curled has nothing left
 * to change, so a second pass over it is a no-op.
 */
export default function rehypeSmartQuotes() {
  return (tree) => walk(tree, false);
}

function walk(node, inCode) {
  if (node.type === 'text') {
    if (!inCode && !CALL.test(node.value)) node.value = smartQuotes(node.value);
    return;
  }
  const code = inCode || (node.type === 'element' && CODE.has(node.tagName));
  for (const child of node.children || []) walk(child, code);
}
