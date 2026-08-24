/**
 * Calculate reading time from text content.
 */
export function getReadingTime(body: string): number {
  const words = body.split(/\s+/).length;
  return Math.ceil(words / 225);
}

/**
 * Render a kebab-case tag slug as a human label.
 *
 * Existed in three copies (PostLayout, BroadsheetEntry, tags/[tag]), each a
 * bare `\b\w` title-case, which rendered `Ai`, `Llm`, `Ebpf`, `Devops`,
 * `Iot`, `Sbom`, `Siem`, `Mcp`, `Cve` and `Nvd` on the archive, every post
 * kicker and every tag page heading (issue #506).
 *
 * The map is exhaustive over the current 109-tag vocabulary; a tag not in it
 * falls through to title case, which is correct for ordinary words.
 */
const TAG_ACRONYMS: Record<string, string> = {
  ai: 'AI',
  cve: 'CVE',
  devops: 'DevOps',
  ebpf: 'eBPF',
  iot: 'IoT',
  llm: 'LLM',
  llms: 'LLMs',
  mcp: 'MCP',
  ml: 'ML',
  nvd: 'NVD',
  sbom: 'SBOM',
  siem: 'SIEM',
};

export function humanTag(slug: string): string {
  return slug
    .split('-')
    .map((word) => TAG_ACRONYMS[word.toLowerCase()] ?? word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}
