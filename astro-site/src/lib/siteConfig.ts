/** Centralized site metadata — single source of truth for author, URLs, and social links. */
export const SITE_CONFIG = {
  author: 'William Zujkowski',
  siteUrl: 'https://williamzujkowski.github.io',
  description:
    'Senior Information Security Engineer with 15+ years experience in cybersecurity, AI security, and Zero-Trust architectures.',
  rssDescription:
    'Senior Information Security Engineer sharing insights on cybersecurity, AI security, and homelab automation.',
  social: {
    github: 'https://github.com/williamzujkowski',
    linkedin: 'https://www.linkedin.com/in/williamzujkowski',
  },
} as const;

/**
 * Masthead sections, in nav order. The label is the section's one name: the
 * destination's <h1> and <title>, the breadcrumbs and their JSON-LD all use
 * it (issue #698 -- four of six labels used to name a different page than
 * the one they opened). tests/e2e/nav-labels.spec.ts holds them together.
 */
export const SECTIONS = [
  { label: 'Front', href: '/' },
  { label: 'Dispatches', href: '/posts/' },
  { label: 'About', href: '/about/' },
  { label: 'Uses', href: '/uses/' },
  { label: 'Workbench', href: '/projects/' },
  { label: 'Now', href: '/now/' },
] as const;
