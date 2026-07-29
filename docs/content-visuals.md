# Content Visuals

Use native HTML patterns first. They inherit Remarque tokens, survive the theme deck,
and stay readable on phones. Mermaid still renders, but it is legacy for new posts.

## Decision Rule

| Reader question | Pattern |
|---|---|
| What happens next? A process, pipeline, or recovery path. | `.flow` |
| What's in this layer, tier, or zone? | `.arch` |
| What talks to what under failure or security policy? | Split into 2-3 focused `.flow` / `.arch` views, then add a caption. |
| Which option is better? A matrix or trade-off grid. | Markdown table |
| A genuine node graph that resists all of the above. | Leave as a fenced `mermaid` block for now. Legacy; being phased down. Consider a future vertical-D2 render. |

## `.flow`

Use `.flow` for ordered work: pipelines, backup paths, gates, fan-out/fan-in, and
pass/fail branches. Connectors are drawn by CSS between direct children. Do not add
arrow characters or connector markup.

Class contract:

```html
<div class="flow" aria-label="Short diagram purpose">
  <div class="flow-node">Step</div>
  <div class="flow-node is-gate">Decision / gate</div>
  <div class="flow-parallel">
    <div class="flow-node">Parallel step</div>
  </div>
  <div class="flow-branch">
    <div class="flow-leg" data-branch="Pass">
      <div class="flow-node is-good">Good result</div>
    </div>
    <div class="flow-leg" data-branch="Fail">
      <div class="flow-node is-bad">Bad result</div>
    </div>
  </div>
</div>
```

Allowed node variants: `.is-gate`, `.is-good`, `.is-bad`.

Raw HTML rules:

- Put the opening tag at column 0.
- Use no blank lines inside the block.
- Use 2-space indentation.
- Escape HTML-sensitive characters: `&` -> `&amp;`, `<` -> `&lt;`, `>` -> `&gt;`.
- Use `<b>` for the main label and `<i>` for the second line when needed.

Copy-paste example:

```html
<div class="flow" aria-label="Security scanning pipeline">
  <div class="flow-node">Git Push / PR</div>
  <div class="flow-node is-gate">Trigger Pipeline</div>
  <div class="flow-parallel">
    <div class="flow-node"><b>OSV</b><i>dependency scan</i></div>
    <div class="flow-node"><b>Grype</b><i>container scan</i></div>
    <div class="flow-node"><b>Trivy</b><i>filesystem scan</i></div>
  </div>
  <div class="flow-node">Upload SARIF</div>
  <div class="flow-node is-gate">Security Gate</div>
  <div class="flow-branch">
    <div class="flow-leg" data-branch="Pass"><div class="flow-node is-good">Deploy</div></div>
    <div class="flow-leg" data-branch="Critical"><div class="flow-node is-bad">Block &amp; Alert</div></div>
  </div>
</div>
```

## `.arch`

Use `.arch` for layered systems, trust zones, service tiers, and component
inventory by tier. It is not a dense topology graph. If the story depends on many
cross-links, split the view.

Class contract:

```html
<figure class="arch-fig">
<div class="arch is-stack" aria-label="Short diagram purpose">
  <section class="arch-tier" data-label="Tier label">
    <span class="arch-chip is-primary"><b>Main component</b><i>second line</i></span>
    <span class="arch-chip is-guard">Guardrail</span>
    <span class="arch-chip is-warn">Warning</span>
    <span class="arch-chip is-bad">Failure</span>
  </section>
</div>
<figcaption>One sentence explaining how to read the view.</figcaption>
</figure>
```

Allowed chip variants: `.is-primary`, `.is-guard`, `.is-warn`, `.is-bad`.
Chips may use `<b>` and `<i>` for a two-line label. `<figcaption>` is optional,
but use it when the interpretation is not obvious.

Use `.arch.is-stack` when tiers are ordered dependencies; it shows a down-cue
between tiers. Omit `.is-stack` for peer zones.

Raw HTML rules:

- Put the opening `<figure>` or `<div class="arch...">` tag at column 0.
- Use no blank lines inside the block.
- Use 2-space indentation.
- Escape HTML-sensitive characters: `&` -> `&amp;`, `<` -> `&lt;`, `>` -> `&gt;`.
- Set `aria-label` on the `.arch` when the diagram needs a text purpose.

Copy-paste example:

```html
<figure class="arch-fig">
<div class="arch is-stack" aria-label="Self-hosted vault architecture">
  <section class="arch-tier" data-label="Client Access"><span class="arch-chip">Web Vault</span><span class="arch-chip">Mobile Apps</span><span class="arch-chip">Browser Extensions</span></section>
  <section class="arch-tier" data-label="Ingress Protection"><span class="arch-chip is-guard">Firewall Rules</span><span class="arch-chip is-guard">TLS 1.3</span><span class="arch-chip is-guard">Fail2ban</span></section>
  <section class="arch-tier" data-label="Application Edge"><span class="arch-chip">Nginx Reverse Proxy</span></section>
  <section class="arch-tier" data-label="Vault Service"><span class="arch-chip is-primary">Vaultwarden</span></section>
  <section class="arch-tier" data-label="Data Store"><span class="arch-chip"><b>SQLite / PostgreSQL</b><i>encrypted at rest</i></span></section>
</div>
<figcaption>Clients enter through the protected edge; the vault service writes to a private database.</figcaption>
</figure>
```

## Splitting Dense Diagrams

Each view should answer one question and stay under about 8 items. If a zero-trust
VLAN diagram wants to show zones, flows, policy, exceptions, and failure behavior,
split it:

- Trust zones: one `.arch` without `.is-stack`.
- Allowed path or failure path: one `.flow`.
- Policy matrix: one Markdown table.

Tie the set together with a one-sentence caption. Do not make one heroic graph
that requires horizontal scrolling and a generous reader.

## Tables

Use plain Markdown tables for matrices, comparisons, scanner/tool choices, policy
rules, and measured results. The prose stylesheet handles table wrapping and
theme-token styling.

```markdown
| Option | Strength | Weakness | Use when |
|---|---|---|---|
| Grype | Fast container scans | Narrower coverage | Image risk is the question |
| Trivy | Broad scanner | Slower | One tool needs to cover several surfaces |
```

## Images

### Zine Doodles

Use zine doodles as hand-drawn spot illustrations for posts that would otherwise
open as pure text. Place them after the intro and before the next heading.

Placement pattern:

```html
<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/example.png'); width: min(240px, 62%); aspect-ratio: 340/328; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">short caption</p>
```

The drawing must carry the post's idea on its own: a specific visual metaphor,
not a stamped text label. The caption can add voice; it cannot rescue a vague
drawing.

Assets are alpha-masked pure-black PNGs, under 60 KB, recolored per theme by CSS
masking. Set `--doodle`, `width`, `aspect-ratio`, and margin per use. Keep the
doodle `aria-hidden="true"` because the adjacent prose carries the meaning.

### OG Social Cards

Do nothing. Per-post OG cards are generated at build time at `/og/<slug>.png`
from the post metadata. Do not add hero-image frontmatter.

## Shared Rules

- Use existing classes only. Do not invent one-off diagram classes in a post.
- Use `var(--color-*)` design tokens for authored visuals. Never hardcode
  `fill:#hex`, inline SVG colors, or theme-specific CSS.
- Keep all visual text at `0.8125rem` or larger. That is the USWDS 13px floor.
- Diagrams must reflow on mobile without horizontal scroll.
- Set an `aria-label` on diagrams when the purpose is not obvious.
- Add a `<figcaption>` when interpretation helps.
