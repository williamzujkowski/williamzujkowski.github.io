# Validate the complete published site

Build the exact revision being deployed, then run the manual Playwright suite:

```bash
cd astro-site
pnpm build
SITE_URL=https://williamzujkowski.github.io \
  SITE_REPORT=/tmp/website-live-report.json \
  SITE_ARTIFACTS=/tmp/website-live-artifacts \
  pnpm exec playwright test --config=playwright.live.config.ts
```

For a local rehearsal, start `pnpm preview` and use `SITE_URL=http://localhost:4321`.
Do not rebuild that `dist/` while the suite is using it. Keep draft-preview builds
in a separate checkout with separate Astro, Vite and dependency cache directories.

The suite enumerates every built HTML route, including hidden pages, tag listings
and `404.html`. Each route runs in desktop/light and mobile/dark Chromium. It checks
HTTP responses, headings, canonical paths, horizontal overflow, same-origin links
and fragments, images/stylesheets, JavaScript errors, failed same-origin requests,
and axe WCAG A/AA rules. It also checks feeds and sitemap consistency, draft
exclusion from those feeds, real search, repeated search opening, theme persistence
and reading paths with JavaScript disabled. JSON results and failure traces stay
outside the repository by default.

This is a deployment validation tool, not another recurring CI audit. The existing
E2E suite owns deterministic interaction regressions. Scheduled citation workflows
own external-link health; this suite does not crawl external websites. Passing axe
and Chromium checks does not replace manual assistive-technology testing or cover
every browser and viewport.
