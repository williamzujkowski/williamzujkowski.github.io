import { test, expect } from 'playwright/test';

/**
 * WCAG 2.2.2 (Pause, Stop, Hide): automatic motion that lasts more than 5s
 * needs a pause control. The 404 doodle (6s) and the PizzaOps status pulse
 * (2.4s) both looped forever. Rather than add pause buttons to a gag and a
 * doodle, each is capped so its total runtime is at most 5s (#698).
 *
 * Reads the running animations from the page, so a duration or iteration
 * change anywhere in the cascade is caught, not just in the one rule.
 */

test.use({ reducedMotion: 'no-preference' });

for (const [path, selector] of [
  ['/404.html', '.lost-doodle .doodle-wander'],
  ['/pizza-ops/', '.po-health .po-dot'],
] as const) {
  test(`automatic motion on ${path} stops within 5s`, async ({ page }) => {
    await page.goto(path);
    const timings = await page.evaluate(
      () => document.getAnimations().map((a) => {
        const t = a.effect!.getComputedTiming();
        const target = (a.effect as KeyframeEffect).target as Element;
        return { name: (a as CSSAnimation).animationName, active: t.activeDuration, cls: target.getAttribute('class') };
      }),
    );
    // Not vacuous: the animation this test is about is actually running.
    const own = await page.locator(selector).first().evaluate((el) => el.getAnimations().length);
    expect(own, `${selector} animates`).toBeGreaterThan(0);
    for (const t of timings) {
      expect(Number(t.active), `${t.name} on .${t.cls}`).toBeLessThanOrEqual(5000);
    }
  });
}
