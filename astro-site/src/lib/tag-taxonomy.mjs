/**
 * Retired tag slugs and the canonical tag each one became (issue #698).
 *
 * Post frontmatter was rewritten once to canonical tags; it stays the source
 * of truth. This map exists only to (a) emit a static redirect for every
 * retired /tags/<old>/ page and (b) reject a retired tag if one reappears in
 * frontmatter (post-schema.mjs). Nothing normalises tags at load time.
 *
 * `null` retires a tag with no apt parent (it was vague, not a topic); its
 * old page redirects to the tag index.
 *
 * Merges were made by judgement, not name: docker and container-security,
 * and networking and its one network-security post, stay distinct where at
 * least three posts are genuinely about the narrower topic.
 */
export const RETIRED_TAGS = Object.freeze({
  'alerting': 'monitoring',
  'apparmor': 'linux',
  'astro': 'web-development',
  'authentication': 'security',
  'backup': 'storage',
  'blockchain': 'cryptography',
  'breakthrough': null,
  'civic-tech': 'open-source',
  'cognitive-science': 'ai',
  'container-orchestration': 'container-security',
  'containers': 'container-security',
  'css': 'web-development',
  'cve': 'vulnerability-management',
  'dashboard': 'monitoring',
  'databases': 'storage',
  'defense-in-depth': 'security',
  'distributed-systems': 'architecture',
  'ebpf': 'linux',
  'eleventy': 'web-development',
  'filesystems': 'storage',
  'firmware': 'hardware',
  'fonts': 'design',
  'formal-verification': 'software-engineering',
  'frontend': 'web-development',
  'future-technology': null,
  'gaming': 'linux',
  'git': 'software-engineering',
  'github': 'open-source',
  'grafana': 'monitoring',
  'graylog': 'threat-detection',
  'hardening': 'security',
  'incident-response': 'threat-detection',
  'iot': 'hardware',
  'kernel': 'linux',
  'learning': 'professional-development',
  'lsm': 'linux',
  'monorepo': 'software-engineering',
  'music': 'projects',
  'network-security': 'networking',
  'nodejs': 'supply-chain',
  'npm': 'supply-chain',
  'nvd': 'vulnerability-management',
  'observability': 'monitoring',
  'ollama': 'llm',
  'open-data': 'open-source',
  'opencv': 'python',
  'optimization': 'monitoring',
  'orchestration': 'ai-agents',
  'oscal': 'compliance',
  'passwords': 'cryptography',
  'performance': 'monitoring',
  'playwright': 'web-development',
  'programming': 'software-engineering',
  'prometheus': 'monitoring',
  'proxmox': 'virtualization',
  'quantum-computing': 'computational-science',
  'reading': 'projects',
  'reliability': 'architecture',
  'rust': 'software-engineering',
  'sbom': 'supply-chain',
  'selinux': 'linux',
  'siem': 'threat-detection',
  'society': 'ethics',
  'svelte': 'web-development',
  'svg': 'web-development',
  'systems': 'architecture',
  'testing': 'software-engineering',
  'tooling': 'devops',
  'typography': 'design',
  'uefi': 'hardware',
  'wazuh': 'threat-detection',
  'zero-knowledge': 'cryptography',
  'zk-snark': 'cryptography',
});

/** Tag slugs become URL segments: lowercase kebab-case only. */
export const TAG_SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

/**
 * Throw unless every retired tag resolves in one step to a live slug.
 * A chain (a -> b where b is itself retired) would redirect to a redirect;
 * a self-map would loop.
 * @param {Readonly<Record<string, string | null>>} retired
 */
export function assertTagAliases(retired) {
  const problems = [];
  for (const [from, to] of Object.entries(retired)) {
    if (!TAG_SLUG.test(from)) problems.push(`retired tag "${from}" is not a slug`);
    if (to === null) continue;
    if (!TAG_SLUG.test(to)) problems.push(`"${from}" maps to non-slug "${to}"`);
    if (to === from) problems.push(`"${from}" maps to itself`);
    else if (Object.hasOwn(retired, to)) problems.push(`chain: "${from}" -> "${to}", which is also retired`);
  }
  if (problems.length > 0) throw new Error(`tag-taxonomy: ${problems.join('; ')}`);
}

/**
 * Astro `redirects` entries for every retired tag page. Static output turns
 * each into a meta-refresh page with rel=canonical to the target.
 * @param {Readonly<Record<string, string | null>>} [retired]
 * @returns {Record<string, string>}
 */
export function tagRedirects(retired = RETIRED_TAGS) {
  assertTagAliases(retired);
  return Object.fromEntries(Object.entries(retired).map(([from, to]) =>
    [`/tags/${from}/`, to === null ? '/tags/' : `/tags/${to}/`]));
}
