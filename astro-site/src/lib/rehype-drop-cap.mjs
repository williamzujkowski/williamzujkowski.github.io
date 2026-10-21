/** Text of a node, in document order. */
function text(node) {
  if (node.type === 'text') return node.value;
  return (node.children || []).map(text).join('');
}

/** Mark a lead paragraph that opens on a lowercase letter with .no-drop-cap.
 * global.css sets a drop cap on a post's first top-level <p> via
 * ::first-letter, which CSS cannot condition on letter case. A lead such as
 * "npm provenance..." or "gVisor adds..." would split a name in two, its
 * first letter set as a capital-sized initial.
 */
export default function rehypeDropCap() {
  return (tree) => {
    const lead = tree.children.find((node) => node.type === 'element' && node.tagName === 'p');
    if (!lead) return;
    // ::first-letter skips leading punctuation, so look at the first letter or digit.
    const first = text(lead).match(/[\p{L}\p{N}]/u);
    if (!first || !/\p{Ll}/u.test(first[0])) return;
    const className = lead.properties.className || [];
    lead.properties.className = [...className, 'no-drop-cap'];
  };
}
