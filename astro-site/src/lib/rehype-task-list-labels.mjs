import { visit } from 'unist-util-visit';

/** Inline task text, excluding nested tasks and decorative controls. */
function taskText(node) {
  if (node.type === 'text') return node.value;
  if (node.type !== 'element' || ['input', 'ul', 'ol'].includes(node.tagName)) return '';
  if (node.properties?.ariaHidden === true || node.properties?.ariaHidden === 'true') return '';
  if (node.tagName === 'img') return node.properties?.alt || '';
  if (node.tagName === 'br') return ' ';
  const text = (node.children || []).map(taskText).join('');
  return node.tagName === 'p' ? `${text} ` : text;
}

/** Give GFM's disabled checkboxes the text of their own task as a name.
 * Keep checked/disabled states and the visible prose unchanged. Explicit names
 * remain author-controlled; nested tasks receive their own independent names.
 */
export default function rehypeTaskListLabels() {
  return (tree) => {
    visit(tree, 'element', (node) => {
      if (node.tagName !== 'li' || !node.properties?.className?.includes('task-list-item')) return;
      // Tight lists put the input directly in <li>; loose lists wrap it in <p>.
      const children = node.children.flatMap((child) =>
        child.type === 'element' && child.tagName === 'p' ? child.children : [child]);
      const checkbox = children.find((child) => child.type === 'element'
        && child.tagName === 'input' && child.properties?.type === 'checkbox'
        && child.properties.disabled);
      if (!checkbox || checkbox.properties.ariaLabel || checkbox.properties.ariaLabelledBy
        || checkbox.properties.title) return;
      const label = node.children.map(taskText).join('').replace(/\s+/g, ' ').trim();
      if (label) checkbox.properties.ariaLabel = label;
    });
  };
}
