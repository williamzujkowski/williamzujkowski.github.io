/** Text of a node, in document order, without margin-note text: a note sits
 * in the gutter at wide widths and is not part of the lead's line count. */
function text(node) {
  if (node.type === 'text') return node.value;
  const cls = node.properties?.className;
  if (Array.isArray(cls) && cls.includes('remarque-sidenote')) return '';
  return (node.children || []).map(text).join('');
}

// remarque-tokens/dropcap (0.33) sizes the cap in lines, and CSS cannot see
// text length or letter case, so the page builder says which cap a lead gets:
//   under ONE_LINE        a lead of one line: no cap.
//   ONE_LINE..SHORT_LEAD  two lines at the reading measure: a two-line cap.
//   SHORT_LEAD and over   the default three-line cap (no class).
// A three-line cap on a short lead hangs below the text. 190 is the
// threshold the 2026-10-28 drop-cap study measured and remarque documents
// ("roughly 100 to 190 characters"); the corpus has leads of 109, 165, 169
// and 180 characters that need the short cap.
export const ONE_LINE = 100;
export const SHORT_LEAD = 190;

/** Classify a lead paragraph for the drop cap.
 *
 * - `no-drop-cap` when the first letter or digit is lowercase or a digit
 *   ("npm provenance...", "gVisor adds...", "42 posts later"): the initial
 *   would split a name or read as a stray numeral. Also for a lead under
 *   ONE_LINE characters.
 * - `remarque-dropcap--short` for a lead under SHORT_LEAD characters.
 * - nothing otherwise: the default cap.
 */
export default function rehypeDropCap() {
  return (tree) => {
    const lead = tree.children.find((node) => node.type === 'element' && node.tagName === 'p');
    if (!lead) return;
    const body = text(lead).replace(/\s+/g, ' ').trim();
    // ::first-letter skips leading punctuation, so look at the first letter or digit.
    const first = body.match(/[\p{L}\p{N}]/u);
    if (!first) return;
    let cls;
    if (/[\p{Ll}\p{N}]/u.test(first[0]) || body.length < ONE_LINE) cls = 'no-drop-cap';
    else if (body.length < SHORT_LEAD) cls = 'remarque-dropcap--short';
    else return;
    const className = lead.properties.className || [];
    lead.properties.className = [...className, cls];
  };
}
