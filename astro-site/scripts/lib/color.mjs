/**
 * Colour maths shared by the design audits.
 *
 * `oklchToSrgb255` existed in two copies — apca-audit.mjs and
 * grain-contrast-audit.mjs — differing only by one comment line, with a
 * comment in the latter that NAMED the duplication rather than resolving it
 * ("same conversion apca-audit.mjs uses"). The WCAG transfer function
 * appeared twice more inside grain-contrast-audit.mjs alone (issue #506).
 *
 * One of those extra copies is legitimate and stays: grain-contrast-audit
 * injects a luminance function into the page via `page.evaluate`, where the
 * module scope is not available. It is now generated from
 * `TRANSFER_FN_SOURCE` below rather than hand-copied, so the browser-side
 * and node-side definitions cannot drift apart.
 */

/** OKLCH -> sRGB, clipped and gamma-encoded to 0-255. */
export function oklchToSrgb255(L, C, h) {
  const hr = (h * Math.PI) / 180;
  const a = C * Math.cos(hr);
  const b = C * Math.sin(hr);

  const l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3;
  const m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3;
  const s_ = (L - 0.0894841775 * a - 1.291485548 * b) ** 3;

  const lin = [
    +4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
    -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
    -0.0041960863 * l_ - 0.7034186147 * m_ + 1.707614701 * s_,
  ];

  // Linear -> sRGB (gamma encode), clip, scale to 0-255
  return lin.map((v) => {
    const clipped = Math.max(0, Math.min(1, v));
    const gamma =
      clipped <= 0.0031308 ? 12.92 * clipped : 1.055 * clipped ** (1 / 2.4) - 0.055;
    return Math.round(Math.max(0, Math.min(1, gamma)) * 255);
  });
}

/**
 * WCAG 2.x sRGB->linear transfer function, as source text.
 *
 * Kept as a string so the identical definition can be injected into a
 * `page.evaluate` body. Never edit one side without the other — that is the
 * whole reason this is a single constant.
 */
export const TRANSFER_FN_SOURCE =
  '(v) => (v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4)';

// eslint-disable-next-line no-eval
const transfer = eval(TRANSFER_FN_SOURCE);

/** WCAG relative luminance from an [r,g,b] triple in 0-255. */
export function relLum255([r, g, b]) {
  const [lr, lg, lb] = [r, g, b].map((c) => transfer(c / 255));
  return 0.2126 * lr + 0.7152 * lg + 0.0722 * lb;
}

/** WCAG contrast ratio between two relative luminances. */
export function contrastFromLum(l1, l2) {
  const [hi, lo] = l1 >= l2 ? [l1, l2] : [l2, l1];
  return (hi + 0.05) / (lo + 0.05);
}

/** Parse `oklch(L C H)` / `oklch(L% C H)` into [L, C, H], or null. */
export function parseOklch(value) {
  const m = /oklch\(\s*([\d.]+)(%?)\s+([\d.]+)\s+([\d.]+)/i.exec(value);
  if (!m) return null;
  const L = parseFloat(m[1]) / (m[2] === '%' ? 100 : 1);
  return [L, parseFloat(m[3]), parseFloat(m[4])];
}
