import { visit } from 'unist-util-visit';

const OWN_HOSTS = new Set(['williamzujkowski.github.io']);

/**
 * Mark off-site links with rel="external" so remarque-tokens' opt-in
 * `.remarque-prose--external-marks` can draw its arrow (the old mark keyed
 * on the href in CSS). Runs after sanitize, which would otherwise be free to
 * drop or rewrite `rel`. Existing tokens (noopener, nofollow ...) are kept.
 * Links inside a margin note's ref anchor (`#`-hrefs) never match.
 */
export default function rehypeExternalRel() {
  return (tree) => {
    visit(tree, 'element', (node) => {
      if (node.tagName !== 'a') return;
      const href = node.properties?.href;
      if (typeof href !== 'string' || !/^https?:\/\//i.test(href)) return;
      let host;
      try {
        host = new URL(href).hostname;
      } catch {
        return;
      }
      if (OWN_HOSTS.has(host)) return;
      const rel = node.properties.rel;
      const tokens = Array.isArray(rel) ? [...rel] : typeof rel === 'string' ? rel.split(/\s+/).filter(Boolean) : [];
      if (!tokens.includes('external')) tokens.push('external');
      node.properties.rel = tokens;
    });
  };
}
