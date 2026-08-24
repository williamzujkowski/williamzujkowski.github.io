<script lang="ts">
  /*
   * PizzaOps™ — enterprise-grade pizza provisioning control plane.
   *
   * This is a joke. The pizza math underneath is not. The geometry is real
   * (area = πr²), the slice arithmetic is real, and the 18-inch really does
   * beat two 12-inch pizzas on both area and price. Everything wrapped around
   * that arithmetic is deadpan SRE ceremony. Never break character.
   */
  import { onMount, onDestroy } from 'svelte';

  // ─── Provisioning target (the real inputs) ───
  let consumers = $state(8);
  let intensity = $state(0.7); // 0 = grazing, 1 = this is the whole meal
  let mealClass = $state<'main' | 'side'>('main');
  let teenagers = $state(false);
  let daypart = $state<'lunch' | 'dinner' | 'late'>('dinner');

  // ─── Real pizza arithmetic ───
  const SLICES_PER_PIZZA = 8;
  const BASE_SLICES = 2.8; // slices per consumer, office-lunch baseline

  const intensityAdj = $derived(1 + 0.4 * intensity); // 1.0 … 1.4
  const mealMult = $derived(mealClass === 'main' ? 1.35 : 1.0);
  const teenMult = $derived(teenagers ? 1.5 : 1.0);
  const daypartMult = $derived(daypart === 'late' ? 1.1 : 1.0);

  const perConsumer = $derived(BASE_SLICES * intensityAdj * mealMult * teenMult * daypartMult);
  const totalSlices = $derived(consumers * perConsumer);
  const units = $derived(consumers <= 0 ? 0 : Math.max(1, Math.ceil(totalSlices / SLICES_PER_PIZZA)));

  // ─── The geometry service (the 18-inch vindication) ───
  const area18 = Math.PI * 9 * 9; // one 18" pizza
  const area12x2 = 2 * Math.PI * 6 * 6; // two 12" pizzas
  const price18 = 24.99;
  const price12x2 = 2 * 14.99;
  const areaPerDollar18 = area18 / price18;
  const areaPerDollar12 = area12x2 / price12x2;
  const fmt = (n: number) => n.toFixed(0);

  // ─── Live observability (fake, and proud of it) ───
  let p99 = $state(41);
  let uptime = $state('99.97');
  let ticker: ReturnType<typeof setInterval> | undefined;

  onMount(() => {
    ticker = setInterval(() => {
      // p99 "latency" wobbles in a band that widens under heavier load.
      const load = Math.min(consumers, 40);
      const band = 6 + load * 0.4;
      p99 = Math.round(34 + (band / 2) + (Math.random() - 0.5) * band);
      // uptime creeps around three-nines, because of course it does.
      uptime = (99.9 + Math.random() * 0.09).toFixed(2);
    }, 1100);
  });
  onDestroy(() => clearInterval(ticker));

  // ─── Provisioning ceremony ───
  const CONSENSUS_STEPS = [
    'Achieving hunger consensus…',
    'Reconciling appetite state across nodes…',
    'Consulting the geometry service…',
    'Establishing consensus on pineapple (this may take a while)…',
    'Applying the teenager multiplier…',
    'Draining the breadstick queue…',
  ];

  let phase = $state<'idle' | 'provisioning' | 'committed'>('idle');
  let consensusLine = $state('');
  let stepTimers: ReturnType<typeof setTimeout>[] = [];

  const prefersReducedMotion = () =>
    typeof window !== 'undefined' &&
    window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;

  function provision() {
    stepTimers.forEach(clearTimeout);
    stepTimers = [];

    if (consumers <= 0) {
      // The loneliest possible outcome. Logged.
      phase = 'committed';
      return;
    }

    if (prefersReducedMotion()) {
      phase = 'committed';
      return;
    }

    phase = 'provisioning';
    const steps = CONSENSUS_STEPS.slice(0, 4 + (teenagers ? 1 : 0));
    steps.forEach((line, i) => {
      stepTimers.push(
        setTimeout(() => {
          consensusLine = line;
          if (i === steps.length - 1) {
            stepTimers.push(setTimeout(() => (phase = 'committed'), 480));
          }
        }, i * 460)
      );
    });
  }

  // Any change to the target invalidates the committed decision — you must
  // re-run consensus. This is a feature. It is, specifically, our feature.
  function invalidate() {
    // Cancel the pending ceremony too, not just the visible state. Every
    // input stays enabled during provisioning (only the Provision button is
    // disabled), so changing one mid-run left the queued timers alive and
    // ~500ms later the last one flipped phase back to 'committed' — publishing
    // a verdict computed from inputs that never ran consensus, which is the
    // exact invariant the comment above claims. Issue #500.
    stepTimers.forEach(clearTimeout);
    stepTimers = [];
    if (phase !== 'idle') {
      phase = 'idle';
      consensusLine = '';
    }
  }

  onDestroy(() => stepTimers.forEach(clearTimeout));

  const daypartNote = $derived(
    daypart === 'late' ? 'late-daypart surcharge applied (people eat more after 10pm; we have data)' : ''
  );

  const consensusLabel = $derived(
    teenagers ? '3/3 · 1 abstention (guess who)' : '3/3 estimators agree'
  );
  const confidenceLabel = $derived(
    intensity < 0.3 && mealClass === 'main'
      ? 'low · someone here is lying about how hungry they are'
      : 'high · dissent: none'
  );

  // ─── Static deadpan banks ───
  const statusComponents = [
    { name: 'Dough Provisioning API', state: 'operational', note: '' },
    { name: 'Topping Consensus Cluster', state: 'operational', note: '3/3 healthy' },
    { name: 'Oven Control Plane', state: 'operational', note: '' },
    { name: 'Anchovy Isolation Chamber', state: 'operational', note: 'permanently isolated, by design' },
    { name: 'Breadstick Queue', state: 'degraded', note: 'backpressure; auto-scaling' },
    { name: 'Deep Dish Latency Buffer', state: 'operational', note: 'elevated p99, expected' },
    { name: 'Thin Crust Compatibility Layer', state: 'deprecated', note: 'still in production' },
    { name: 'Leftover Cold Storage Subsystem', state: 'operational', note: 'underutilized' },
    { name: 'Pineapple Feature Flag', state: 'disabled', note: 'by policy' },
  ];

  const incidents = [
    { sev: 'SEV-1', text: 'Entire order consumed within four minutes of arrival. Capacity planning for next order under review.' },
    { sev: 'SEV-1', text: 'Box structural integrity failure in transit. Contents unaffected. Dignity affected.' },
    { sev: 'SEV-2', text: 'Pepperoni quorum lost; failed over to secondary topping. RCA pending.' },
    { sev: 'SEV-2', text: 'Doorbell rang twice: duplicate delivery-confirmation event. Idempotency key missing.' },
    { sev: 'SEV-3', text: 'One (1) breadstick missing from batch. Logged. Not escalated. Never forgotten.' },
    { sev: 'SEV-5', text: 'Someone asked for pineapple. Ticket opened. Ticket closed. No further comment.' },
  ];

  const changelog = [
    { v: 'v3.1', text: 'Added support for teenagers. Regretted immediately.' },
    { v: 'v3.0', text: 'Migrated hunger estimation to a consensus quorum. Latency up, arguments down.' },
    { v: 'v2.5', text: 'Introduced the Anchovy Isolation Chamber after a Q3 incident we do not discuss.' },
    { v: 'v2.2', text: 'Fixed a bug where "light eaters" were modeled honestly. Reverted to prior, more accurate skepticism.' },
    { v: 'v2.0', text: 'Introduced area-per-dollar optimization. The 18-inch has not lost since.' },
    { v: 'v1.0', text: 'Initial release. Promised a lot. Delivered pizza.' },
  ];

  const legalese = [
    'PizzaOps™ is a registered trademark of nothing in particular.',
    'Recommendations are advisory. Do not taunt the oven.',
    'Uptime figures exclude scheduled maintenance, unscheduled maintenance, and Tuesdays.',
    'SLA excludes acts of oven, acts of teenager, and pineapple.',
    'Leftover pizza is not a bug. Do not open a ticket.',
  ];
</script>

<div class="pizzaops">
  <!-- Title bar -->
  <div class="po-titlebar">
    <div class="po-lights" aria-hidden="true">
      <span class="po-light po-light--r"></span>
      <span class="po-light po-light--y"></span>
      <span class="po-light po-light--g"></span>
    </div>
    <span class="po-appname">PizzaOps™ · Control Plane</span>
    <span class="po-health" class:degraded={consumers <= 0}>
      <span class="po-dot"></span>
      {consumers <= 0 ? 'quorum lost' : 'all systems nominal'}
    </span>
  </div>

  <div class="po-body">
    <!-- LEFT: provisioning target -->
    <section class="po-panel" aria-label="Provisioning target">
      <h2 class="po-h">Provisioning target</h2>

      <div class="po-field">
        <label for="po-consumers">Consumers
          <span class="po-help" title="Human units to be fed. Non-human units are out of scope.">?</span>
        </label>
        <div class="po-stepper">
          <button type="button" onclick={() => { consumers = Math.max(0, consumers - 1); invalidate(); }} aria-label="Decrease consumers">−</button>
          <input id="po-consumers" type="number" min="0" max="500" bind:value={consumers} oninput={invalidate} />
          <button type="button" onclick={() => { consumers = Math.min(500, consumers + 1); invalidate(); }} aria-label="Increase consumers">+</button>
        </div>
      </div>

      <div class="po-field">
        <label for="po-intensity">Hunger intensity
          <span class="po-help" title="0.0 = grazing. 1.0 = this is the whole meal and everyone skipped lunch.">?</span>
          <span class="po-val">{intensity.toFixed(2)}</span>
        </label>
        <input id="po-intensity" type="range" min="0" max="1" step="0.05" bind:value={intensity} oninput={invalidate} />
      </div>

      <div class="po-field">
        <span class="po-label">Meal class
          <span class="po-help" title="Side act: 1.0× multiplier. Main event: 1.35×. Choose honestly.">?</span>
        </span>
        <div class="po-seg" role="radiogroup" aria-label="Meal class">
          <button type="button" class:active={mealClass === 'main'} role="radio" aria-checked={mealClass === 'main'} onclick={() => { mealClass = 'main'; invalidate(); }}>Main event</button>
          <button type="button" class:active={mealClass === 'side'} role="radio" aria-checked={mealClass === 'side'} onclick={() => { mealClass = 'side'; invalidate(); }}>Side act</button>
        </div>
      </div>

      <div class="po-field">
        <span class="po-label">Daypart
          <span class="po-help" title="Hunger increases nonlinearly after 11 PM. We do not know why. We have stopped asking.">?</span>
        </span>
        <div class="po-seg" role="radiogroup" aria-label="Daypart">
          <button type="button" class:active={daypart === 'lunch'} role="radio" aria-checked={daypart === 'lunch'} onclick={() => { daypart = 'lunch'; invalidate(); }}>Lunch</button>
          <button type="button" class:active={daypart === 'dinner'} role="radio" aria-checked={daypart === 'dinner'} onclick={() => { daypart = 'dinner'; invalidate(); }}>Dinner</button>
          <button type="button" class:active={daypart === 'late'} role="radio" aria-checked={daypart === 'late'} onclick={() => { daypart = 'late'; invalidate(); }}>Late</button>
        </div>
      </div>

      <label class="po-toggle">
        <input type="checkbox" bind:checked={teenagers} onchange={invalidate} />
        <span>Teenagers present
          <span class="po-help" title="Applies a mandatory 1.5× multiplier. This value is not configurable. We have seen things.">?</span>
        </span>
      </label>

      <button type="button" class="po-provision" onclick={provision} disabled={phase === 'provisioning'}>
        {phase === 'provisioning' ? 'Achieving consensus…' : 'Provision'}
      </button>
    </section>

    <!-- RIGHT: recommendation + observability -->
    <section class="po-panel po-panel--out" aria-live="polite">
      {#if phase === 'idle'}
        <div class="po-draft">
          <h2 class="po-h">Recommendation</h2>
          <p class="po-muted">Draft estimate: <strong>{units}</strong> {units === 1 ? 'unit' : 'units'}. Awaiting formal consensus.</p>
          <p class="po-muted po-tiny">No decision is binding until you Provision. This is deliberate.</p>
        </div>
      {:else if phase === 'provisioning'}
        <div class="po-consensus">
          <div class="po-spinner" aria-hidden="true"></div>
          <p class="po-console">{consensusLine || 'Achieving hunger consensus…'}</p>
        </div>
      {:else if consumers <= 0}
        <div class="po-empty">
          <h2 class="po-h">No target</h2>
          <p class="po-console">0 consumers detected. There is no one to feed.</p>
          <p class="po-muted">This is the loneliest possible outcome, and it has been logged.</p>
        </div>
      {:else}
        <div class="po-verdict">
          <p class="po-verdict-label">Provisioning decision</p>
          <p class="po-verdict-units"><strong>{units}</strong> {units === 1 ? 'unit' : 'units'} <span>· 18″</span></p>
          <dl class="po-metrics">
            <div><dt>Consensus</dt><dd>{consensusLabel}</dd></div>
            <div><dt>Confidence</dt><dd>{confidenceLabel}</dd></div>
            <div><dt>SLA</dt><dd>{perConsumer.toFixed(1)} slices / consumer</dd></div>
            <div><dt>Total demand</dt><dd>{Math.ceil(totalSlices)} slices</dd></div>
          </dl>
          {#if daypartNote}<p class="po-note">▸ {daypartNote}</p>{/if}
          <p class="po-note po-note--quiet">We always round up. A pizza cannot be provisioned in
            fractions. Neither, frankly, can dignity.</p>
          {#if teenagers}<p class="po-note po-note--quiet">▸ teenager multiplier engaged (1.5×, non-negotiable). We have seen things.</p>{/if}

          <div class="po-geo">
            <p class="po-geo-h">Geometry service · value analysis</p>
            <p>One 18″ pizza is <strong>{fmt(area18)} in²</strong> for ${price18.toFixed(2)}
              — that's <strong>{areaPerDollar18.toFixed(1)} in²/$</strong>.</p>
            <p>Two 12″ pizzas are <strong>{fmt(area12x2)} in²</strong> for ${price12x2.toFixed(2)}
              — only <strong>{areaPerDollar12.toFixed(1)} in²/$</strong>.</p>
            <p class="po-geo-verdict">The 18-inch wins on area-per-dollar. It always wins. This is
              not a matter of opinion; it is a matter of π.</p>
          </div>
        </div>
      {/if}

      <div class="po-obs" aria-hidden="true">
        <span><em>p99</em> {p99}ms</span>
        <span><em>uptime</em> {uptime}%</span>
        <span><em>blast radius</em> 1 kitchen</span>
      </div>
    </section>
  </div>

  <!-- Status page -->
  <section class="po-strip">
    <h2 class="po-h po-h--strip">System status</h2>
    <ul class="po-status">
      {#each statusComponents as c}
        <li class="po-status-row po-state--{c.state}">
          <span class="po-status-dot"></span>
          <span class="po-status-name">{c.name}</span>
          <span class="po-status-state">{c.state}{c.note ? ` · ${c.note}` : ''}</span>
        </li>
      {/each}
    </ul>
  </section>

  <div class="po-strip-grid">
    <section class="po-strip">
      <h2 class="po-h po-h--strip">Recent incidents</h2>
      <ul class="po-log">
        {#each incidents as i}
          <li><span class="po-sev po-sev--{i.sev.split('-')[1]}">{i.sev}</span> {i.text}</li>
        {/each}
      </ul>
    </section>

    <section class="po-strip">
      <h2 class="po-h po-h--strip">Changelog</h2>
      <ul class="po-log">
        {#each changelog as c}
          <li><span class="po-ver">{c.v}</span> {c.text}</li>
        {/each}
      </ul>
    </section>
  </div>

  <footer class="po-legal">
    {#each legalese as line}<span>{line}</span>{/each}
  </footer>
</div>

<style>
  /* Everything reads from the site's --color-* tokens, so PizzaOps inherits
     light / dark / every deck theme automatically. The register is
     "enterprise dashboard": mono type, tight rules, status dots. */
  .pizzaops {
    font-family: var(--font-mono, monospace);
    font-size: 0.9rem;
    line-height: 1.5;
    color: var(--color-fg);
    border: 1px solid var(--color-border-bold);
    border-radius: 0.5rem;
    overflow: hidden;
    background: var(--color-surface);
    box-shadow: 0 1px 0 var(--color-border), 0 8px 30px -18px var(--color-shadow);
    max-width: 62rem;
    margin: 0 auto;
  }

  .po-titlebar {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem 0.85rem;
    background: var(--color-bg-subtle);
    border-bottom: 1px solid var(--color-border-bold);
  }
  .po-lights { display: flex; gap: 0.4rem; }
  .po-light { width: 0.72rem; height: 0.72rem; border-radius: 50%; opacity: 0.85; }
  .po-light--r { background: var(--color-error); }
  .po-light--y { background: var(--color-accent-hover); }
  .po-light--g { background: var(--color-accent); }
  .po-appname { font-weight: 600; letter-spacing: 0.02em; }
  .po-health {
    margin-left: auto; display: inline-flex; align-items: center; gap: 0.4rem;
    font-size: 0.8125rem; color: var(--color-muted); text-transform: uppercase; letter-spacing: 0.04em;
  }
  .po-health .po-dot {
    width: 0.5rem; height: 0.5rem; border-radius: 50%;
    background: var(--color-accent);
    box-shadow: 0 0 0 0 var(--color-accent);
    animation: po-pulse 2.4s ease-out infinite;
  }
  .po-health.degraded { color: var(--color-error); }
  .po-health.degraded .po-dot { background: var(--color-error); animation: none; }
  @keyframes po-pulse {
    0% { box-shadow: 0 0 0 0 color-mix(in oklch, var(--color-accent) 60%, transparent); }
    70% { box-shadow: 0 0 0 6px transparent; }
    100% { box-shadow: 0 0 0 0 transparent; }
  }

  .po-body { display: grid; grid-template-columns: 1fr 1fr; gap: 0; }
  @media (max-width: 640px) { .po-body { grid-template-columns: 1fr; } }

  .po-panel { padding: 1.1rem 1.15rem; }
  .po-panel--out {
    border-left: 1px solid var(--color-border);
    background: var(--color-bg);
    display: flex; flex-direction: column;
  }
  @media (max-width: 640px) {
    .po-panel--out { border-left: none; border-top: 1px solid var(--color-border); }
  }

  .po-h {
    font-size: 0.8125rem; text-transform: uppercase; letter-spacing: 0.12em;
    color: var(--color-muted); margin: 0 0 0.9rem; font-weight: 600;
  }
  .po-h--strip { margin-bottom: 0.6rem; }

  .po-field { margin-bottom: 1rem; }
  .po-field label, .po-label {
    display: flex; align-items: center; gap: 0.4rem;
    font-size: 0.8125rem; color: var(--color-fg-muted); margin-bottom: 0.4rem;
  }
  .po-val { margin-left: auto; color: var(--color-accent); font-weight: 600; }

  .po-help {
    display: inline-grid; place-items: center;
    width: 1.25rem; height: 1.25rem; border-radius: 50%;
    border: 1px solid var(--color-border-bold); color: var(--color-muted);
    font-size: 0.8125rem; cursor: help; user-select: none; flex: none;
  }

  .po-stepper { display: flex; align-items: stretch; }
  .po-stepper button {
    width: 2.2rem; border: 1px solid var(--color-border-bold);
    background: var(--color-surface); color: var(--color-fg);
    cursor: pointer; font-size: 1.1rem; line-height: 1;
  }
  .po-stepper button:first-child { border-radius: 0.3rem 0 0 0.3rem; }
  .po-stepper button:last-child { border-radius: 0 0.3rem 0.3rem 0; }
  .po-stepper button:hover { background: var(--color-bg-subtle); }
  .po-stepper input {
    flex: 1; min-width: 0; text-align: center;
    border: 1px solid var(--color-border-bold); border-left: 0; border-right: 0;
    background: var(--color-bg); color: var(--color-fg);
    font-family: inherit; font-size: 1rem; padding: 0.4rem 0; -moz-appearance: textfield;
  }
  .po-stepper input::-webkit-outer-spin-button,
  .po-stepper input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }

  input[type='range'] { width: 100%; accent-color: var(--color-accent); }

  .po-seg { display: flex; gap: 0; }
  .po-seg button {
    flex: 1; padding: 0.45rem 0.3rem; font-family: inherit; font-size: 0.8125rem;
    border: 1px solid var(--color-border-bold); background: var(--color-surface);
    color: var(--color-fg-muted); cursor: pointer;
  }
  .po-seg button + button { border-left: 0; }
  .po-seg button:first-child { border-radius: 0.3rem 0 0 0.3rem; }
  .po-seg button:last-child { border-radius: 0 0.3rem 0.3rem 0; }
  .po-seg button.active {
    background: color-mix(in oklch, var(--color-accent) 16%, var(--color-surface));
    color: var(--color-fg); border-color: var(--color-accent);
    font-weight: 600; position: relative; z-index: 1;
  }

  .po-toggle { display: flex; align-items: center; gap: 0.55rem; font-size: 0.82rem; cursor: pointer; margin-bottom: 1.2rem; }
  .po-toggle input { accent-color: var(--color-accent); width: 1.05rem; height: 1.05rem; }

  .po-provision {
    width: 100%; padding: 0.7rem; font-family: inherit; font-size: 0.82rem;
    text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700;
    background: var(--color-accent); color: var(--color-bg);
    border: 0; border-radius: 0.35rem; cursor: pointer;
  }
  .po-provision:hover { background: var(--color-accent-hover); }
  .po-provision:disabled { opacity: 0.7; cursor: progress; }

  .po-muted { color: var(--color-muted); }
  .po-tiny { font-size: 0.8125rem; }
  .po-console { font-size: 0.85rem; color: var(--color-fg); }

  .po-consensus { display: flex; flex-direction: column; align-items: flex-start; gap: 0.9rem; padding-top: 0.5rem; }
  .po-spinner {
    width: 1.4rem; height: 1.4rem; border-radius: 50%;
    border: 2px solid var(--color-border-bold); border-top-color: var(--color-accent);
    animation: po-spin 0.8s linear infinite;
  }
  @keyframes po-spin { to { transform: rotate(360deg); } }
  @media (prefers-reduced-motion: reduce) {
    .po-spinner { animation: none; }
    .po-health .po-dot { animation: none; }
  }

  .po-verdict-label { font-size: 0.8125rem; text-transform: uppercase; letter-spacing: 0.14em; color: var(--color-accent); margin: 0; font-weight: 700; }
  .po-verdict-units { font-size: 2rem; margin: 0.2rem 0 0.9rem; font-weight: 400; }
  .po-verdict-units strong { font-weight: 700; }
  .po-verdict-units span { font-size: 1rem; color: var(--color-muted); }

  .po-metrics { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem 1rem; margin: 0 0 0.8rem; }
  .po-metrics dt { font-size: 0.8125rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--color-muted); }
  .po-metrics dd { margin: 0; font-size: 0.82rem; }

  .po-note { font-size: 0.8125rem; color: var(--color-fg-muted); margin: 0 0 0.8rem; }
  .po-note--quiet { color: var(--color-muted); font-style: italic; }

  .po-geo { border-top: 1px dashed var(--color-border-bold); padding-top: 0.8rem; font-size: 0.8125rem; }
  .po-geo p { margin: 0 0 0.35rem; }
  .po-geo-h { font-size: 0.8125rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--color-muted); }
  .po-geo-verdict { color: var(--color-fg-muted); font-style: italic; }

  .po-empty .po-console { color: var(--color-fg); }

  .po-obs {
    margin-top: auto; display: flex; flex-wrap: wrap; gap: 0.4rem 1.1rem;
    padding-top: 0.9rem; border-top: 1px solid var(--color-border);
    font-size: 0.8125rem; color: var(--color-muted); letter-spacing: 0.03em;
  }
  /* No opacity here. --color-muted is already the dimmest text token that
     clears 4.5:1 (it renders 4.81:1 on --color-bg), so dimming it further
     fails by construction — 0.7 composited it to 2.75:1, a real WCAG AA
     failure that shipped because /pizza-ops/ was not in the axe page list
     (issues #500, #508). The uppercase + letter-spacing treatment already
     distinguishes the label. */
  .po-obs em {
    font-style: normal;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-right: 0.25rem;
  }

  .po-strip { padding: 1rem 1.15rem; border-top: 1px solid var(--color-border); }
  .po-strip-grid { display: grid; grid-template-columns: 1fr 1fr; }
  .po-strip-grid .po-strip:last-child { border-left: 1px solid var(--color-border); }
  @media (max-width: 640px) {
    .po-strip-grid { grid-template-columns: 1fr; }
    .po-strip-grid .po-strip:last-child { border-left: none; }
  }

  .po-status { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.35rem; }
  .po-status-row { display: flex; align-items: center; gap: 0.55rem; font-size: 0.8125rem; }
  .po-status-dot { width: 0.5rem; height: 0.5rem; border-radius: 50%; background: var(--color-accent); flex: none; }
  .po-state--degraded .po-status-dot { background: var(--color-accent-hover); }
  .po-state--disabled .po-status-dot { background: var(--color-muted); }
  .po-state--deprecated .po-status-dot { background: var(--color-muted); }
  .po-status-name { color: var(--color-fg); }
  .po-status-state { margin-left: auto; color: var(--color-muted); font-size: 0.8125rem; text-transform: lowercase; }

  .po-log { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.5rem; font-size: 0.8125rem; }
  .po-log li { color: var(--color-fg-muted); }
  .po-sev, .po-ver {
    display: inline-block; font-size: 0.8125rem; font-weight: 700; letter-spacing: 0.04em;
    padding: 0.05rem 0.3rem; border-radius: 0.2rem; margin-right: 0.35rem;
    border: 1px solid var(--color-border-bold); color: var(--color-muted);
  }
  .po-sev--1 { color: var(--color-error); border-color: var(--color-error); }
  .po-sev--2 { color: var(--color-accent-hover); border-color: var(--color-accent-hover); }
  .po-ver { color: var(--color-accent); border-color: var(--color-accent); }

  .po-legal {
    display: flex; flex-wrap: wrap; gap: 0.3rem 1rem;
    padding: 0.8rem 1.15rem; border-top: 1px solid var(--color-border-bold);
    background: var(--color-bg-subtle); font-size: 0.8125rem; color: var(--color-muted);
  }
</style>
