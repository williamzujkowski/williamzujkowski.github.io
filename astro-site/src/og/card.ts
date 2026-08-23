/**
 * Build-time OG/social card generator (#178; restyled to the zine maximal
 * aesthetic per #283 item 5 — "go maximal"). satori (JSX-free object tree)
 * -> SVG -> PNG via resvg.
 *
 * Visual layers (back to front), each doing one job so the maximal treatment
 * doesn't fight the title for attention:
 *   1. Flat navy background.
 *   2. Baked-alpha grain tile (paper texture; see assets/grain-tile.png).
 *   3. Solid top/bottom structural bars (brand continuity with the old card).
 *   4. A hand-wobbled frame drawn as real SVG <path> strokes (deterministic,
 *      generated once — see scripts note below — not re-randomized per build).
 *   5. Small corner tick marks where the wobble strokes don't quite meet.
 *   6. A Shantell Sans "Field Notes" kicker (hand-note voice, matches the
 *      site nameplate) — rotated, off to the side of the title.
 *   7. Title + subtitle: unchanged, still the dominant, highest-contrast
 *      element.
 *   8. Footer URL, with a small hand-drawn accent mark.
 */
import satori from 'satori';
import { Resvg } from '@resvg/resvg-js';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const fontDir = resolve(process.cwd(), 'src/og/fonts');
const assetDir = resolve(process.cwd(), 'src/og/assets');
const bold = readFileSync(resolve(fontDir, 'FreeSansBold.ttf'));
const regular = readFileSync(resolve(fontDir, 'FreeSans.ttf'));
const shantell = readFileSync(resolve(fontDir, 'ShantellSans.ttf'));
const grainTile = readFileSync(resolve(assetDir, 'grain-tile.png'));
const grainDataUri = `data:image/png;base64,${grainTile.toString('base64')}`;

// Social-card palette. These are literals on purpose: satori renders an
// object tree straight to SVG at build time with no CSS cascade and no
// :root, so var(--color-*) cannot resolve here. The colour-token audit does
// see these lines (issue #511) — the allow-raw-color markers are what
// exempts them, so the exemption is reviewed rather than structural. If this
// palette should track the site tokens, it has to be resolved in JS and
// passed in; it cannot be done with CSS custom properties.
const BG = '#1a1f2e'; // allow-raw-color: satori has no CSS cascade
const BLUE = '#3b82f6'; // allow-raw-color: satori has no CSS cascade
const AMBER = '#f0a828'; // allow-raw-color: satori has no CSS cascade
const TITLE = '#f8fafc'; // allow-raw-color: satori has no CSS cascade
const SUB = '#94a3b8'; // allow-raw-color: satori has no CSS cascade
const FOOT = '#64748b'; // allow-raw-color: satori has no CSS cascade

type Node = { type: string; props: Record<string, unknown> };
function div(style: Record<string, unknown>, children?: unknown): Node {
  // satori requires an explicit display on every element.
  return { type: 'div', props: { style: { display: 'flex', ...style }, children } };
}
function el(type: string, props: Record<string, unknown>, children?: unknown): Node {
  return { type, props: { ...props, children } };
}

// ---------------------------------------------------------------------
// Hand-wobble frame path data — deterministic (mulberry32, fixed seeds),
// generated once by a throwaway script using the same sine + jitter
// technique as src/styles/zine.css's --zine-rule-mask, extended around
// all four card edges. Regenerate by re-running that technique with the
// same seeds (1/2/3/4) if the card dimensions ever change; do not
// hand-edit these strings.
const FRAME_INSET = 34;
const FRAME_STROKE = 6.5;
const FRAME_TOP =
  'M 34.0 34.3 Q 42.0 36.7 46.0 37.9 Q 50.0 39.0 54.0 38.3 Q 58.0 37.6 62.0 35.5 Q 66.0 33.4 70.0 31.2 Q 74.0 28.9 78.0 29.4 Q 82.0 29.8 86.0 31.6 Q 90.0 33.4 94.0 35.1 Q 98.0 36.9 102.0 38.5 Q 106.0 40.1 110.0 38.7 Q 114.0 37.3 118.0 35.4 Q 122.0 33.4 126.0 31.3 Q 130.0 29.1 134.0 29.0 Q 138.0 29.0 142.0 30.2 Q 146.0 31.3 150.0 33.3 Q 154.0 35.3 158.0 37.1 Q 162.0 38.8 166.0 38.0 Q 170.0 37.2 174.0 35.7 Q 178.0 34.3 182.0 32.7 Q 186.0 31.1 190.0 29.8 Q 194.0 28.5 198.0 29.4 Q 202.0 30.3 206.0 32.2 Q 210.0 34.1 214.0 36.2 Q 218.0 38.3 222.0 38.6 Q 226.0 38.8 230.0 37.5 Q 234.0 36.3 238.0 33.6 Q 242.0 31.0 246.0 29.7 Q 250.0 28.4 254.0 29.5 Q 258.0 30.5 262.0 32.3 Q 266.0 34.1 270.0 36.2 Q 274.0 38.4 278.0 38.3 Q 282.0 38.3 286.0 37.7 Q 290.0 37.1 294.0 34.7 Q 298.0 32.3 302.0 31.1 Q 306.0 30.0 310.0 30.3 Q 314.0 30.7 318.0 31.5 Q 322.0 32.4 326.0 35.0 Q 330.0 37.6 334.0 37.9 Q 338.0 38.2 342.0 37.6 Q 346.0 37.0 350.0 35.2 Q 354.0 33.3 358.0 31.3 Q 362.0 29.3 366.0 28.9 Q 370.0 28.4 374.0 30.4 Q 378.0 32.4 382.0 34.3 Q 386.0 36.3 390.0 37.1 Q 394.0 38.0 398.0 37.8 Q 402.0 37.6 406.0 35.6 Q 410.0 33.5 414.0 32.2 Q 418.0 30.8 422.0 30.3 Q 426.0 29.8 430.0 30.1 Q 434.0 30.4 438.0 33.3 Q 442.0 36.2 446.0 37.5 Q 450.0 38.9 454.0 38.7 Q 458.0 38.4 462.0 36.8 Q 466.0 35.2 470.0 33.5 Q 474.0 31.8 478.0 30.9 Q 482.0 30.1 486.0 30.6 Q 490.0 31.1 494.0 32.8 Q 498.0 34.4 502.0 36.6 Q 506.0 38.7 510.0 39.2 Q 514.0 39.7 518.0 38.6 Q 522.0 37.5 526.0 34.5 Q 530.0 31.6 534.0 29.9 Q 538.0 28.3 542.0 29.4 Q 546.0 30.4 550.0 31.4 Q 554.0 32.5 558.0 35.2 Q 562.0 37.9 566.0 38.4 Q 570.0 39.0 574.0 38.7 Q 578.0 38.4 582.0 36.2 Q 586.0 33.9 590.0 31.5 Q 594.0 29.1 598.0 29.3 Q 602.0 29.6 606.0 31.2 Q 610.0 32.9 614.0 34.1 Q 618.0 35.3 622.0 37.6 Q 626.0 39.9 630.0 38.6 Q 634.0 37.4 638.0 35.8 Q 642.0 34.3 646.0 32.0 Q 650.0 29.7 654.0 29.3 Q 658.0 28.8 662.0 29.7 Q 666.0 30.6 670.0 33.0 Q 674.0 35.4 678.0 36.9 Q 682.0 38.4 686.0 38.6 Q 690.0 38.7 694.0 36.7 Q 698.0 34.7 702.0 33.4 Q 706.0 32.1 710.0 31.0 Q 714.0 29.8 718.0 29.8 Q 722.0 29.7 726.0 31.5 Q 730.0 33.3 734.0 35.3 Q 738.0 37.4 742.0 38.6 Q 746.0 39.8 750.0 38.0 Q 754.0 36.1 758.0 33.9 Q 762.0 31.6 766.0 30.7 Q 770.0 29.7 774.0 29.7 Q 778.0 29.7 782.0 31.1 Q 786.0 32.5 790.0 34.4 Q 794.0 36.2 798.0 37.2 Q 802.0 38.2 806.0 37.3 Q 810.0 36.5 814.0 34.8 Q 818.0 33.0 822.0 31.6 Q 826.0 30.2 830.0 29.9 Q 834.0 29.5 838.0 30.3 Q 842.0 31.1 846.0 33.6 Q 850.0 36.1 854.0 37.5 Q 858.0 38.9 862.0 38.2 Q 866.0 37.5 870.0 36.3 Q 874.0 35.2 878.0 32.6 Q 882.0 30.0 886.0 30.1 Q 890.0 30.1 894.0 31.0 Q 898.0 32.0 902.0 33.9 Q 906.0 35.9 910.0 36.6 Q 914.0 37.3 918.0 37.6 Q 922.0 37.9 926.0 36.3 Q 930.0 34.6 934.0 33.5 Q 938.0 32.5 942.0 30.6 Q 946.0 28.7 950.0 29.7 Q 954.0 30.7 958.0 32.7 Q 962.0 34.8 966.0 35.9 Q 970.0 36.9 974.0 37.7 Q 978.0 38.4 982.0 37.9 Q 986.0 37.4 990.0 35.2 Q 994.0 33.1 998.0 31.5 Q 1002.0 30.0 1006.0 29.5 Q 1010.0 29.0 1014.0 30.5 Q 1018.0 32.0 1022.0 34.1 Q 1026.0 36.3 1030.0 37.5 Q 1034.0 38.8 1038.0 38.2 Q 1042.0 37.5 1046.0 35.3 Q 1050.0 33.0 1054.0 31.8 Q 1058.0 30.7 1062.0 29.7 Q 1066.0 28.8 1070.0 30.8 Q 1074.0 32.8 1078.0 34.8 Q 1082.0 36.9 1086.0 38.0 Q 1090.0 39.1 1094.0 38.8 Q 1098.0 38.5 1102.0 36.2 Q 1106.0 34.0 1110.0 32.1 Q 1114.0 30.3 1118.0 29.4 Q 1122.0 28.6 1126.0 29.5 Q 1130.0 30.3 1134.0 32.4 Q 1138.0 34.6 1142.0 37.0 Q 1146.0 39.4 1150.0 39.5 Q 1154.0 39.7 1158.0 37.3 Q 1162.0 34.8 1164.0 34.2 L 1166.0 33.5';
const FRAME_BOTTOM =
  'M 34.0 596.5 Q 42.0 599.4 46.0 599.9 Q 50.0 600.5 54.0 599.6 Q 58.0 598.7 62.0 596.9 Q 66.0 595.2 70.0 593.4 Q 74.0 591.6 78.0 591.6 Q 82.0 591.6 86.0 593.1 Q 90.0 594.6 94.0 597.1 Q 98.0 599.6 102.0 599.9 Q 106.0 600.1 110.0 600.1 Q 114.0 600.1 118.0 597.4 Q 122.0 594.8 126.0 593.2 Q 130.0 591.7 134.0 591.8 Q 138.0 591.9 142.0 593.0 Q 146.0 594.1 150.0 595.7 Q 154.0 597.3 158.0 599.3 Q 162.0 601.2 166.0 600.5 Q 170.0 599.8 174.0 598.7 Q 178.0 597.6 182.0 594.6 Q 186.0 591.5 190.0 591.7 Q 194.0 591.9 198.0 592.0 Q 202.0 592.0 206.0 594.1 Q 210.0 596.3 214.0 598.0 Q 218.0 599.7 222.0 599.7 Q 226.0 599.6 230.0 599.1 Q 234.0 598.6 238.0 595.9 Q 242.0 593.3 246.0 592.3 Q 250.0 591.4 254.0 592.3 Q 258.0 593.3 262.0 594.3 Q 266.0 595.4 270.0 597.6 Q 274.0 599.7 278.0 600.2 Q 282.0 600.6 286.0 599.1 Q 290.0 597.6 294.0 596.0 Q 298.0 594.5 302.0 592.5 Q 306.0 590.5 310.0 590.5 Q 314.0 590.6 318.0 593.3 Q 322.0 595.9 326.0 597.8 Q 330.0 599.7 334.0 599.8 Q 338.0 599.9 342.0 600.2 Q 346.0 600.5 350.0 597.5 Q 354.0 594.5 358.0 593.7 Q 362.0 592.9 366.0 592.1 Q 370.0 591.2 374.0 592.2 Q 378.0 593.2 382.0 595.9 Q 386.0 598.5 390.0 599.2 Q 394.0 599.8 398.0 600.3 Q 402.0 600.7 406.0 599.1 Q 410.0 597.4 414.0 595.4 Q 418.0 593.3 422.0 592.1 Q 426.0 590.9 430.0 592.4 Q 434.0 594.0 438.0 595.0 Q 442.0 596.1 446.0 598.5 Q 450.0 600.9 454.0 601.3 Q 458.0 601.7 462.0 600.0 Q 466.0 598.3 470.0 596.0 Q 474.0 593.7 478.0 592.4 Q 482.0 591.1 486.0 591.1 Q 490.0 591.2 494.0 594.0 Q 498.0 596.8 502.0 598.7 Q 506.0 600.6 510.0 600.8 Q 514.0 601.0 518.0 599.6 Q 522.0 598.2 526.0 596.7 Q 530.0 595.3 534.0 593.8 Q 538.0 592.3 542.0 591.9 Q 546.0 591.5 550.0 593.0 Q 554.0 594.6 558.0 596.3 Q 562.0 598.0 566.0 600.0 Q 570.0 602.0 574.0 600.5 Q 578.0 599.0 582.0 597.2 Q 586.0 595.3 590.0 593.9 Q 594.0 592.5 598.0 592.3 Q 602.0 592.0 606.0 593.4 Q 610.0 594.8 614.0 596.4 Q 618.0 597.9 622.0 599.1 Q 626.0 600.2 630.0 600.3 Q 634.0 600.5 638.0 598.6 Q 642.0 596.8 646.0 594.9 Q 650.0 593.0 654.0 592.5 Q 658.0 592.0 662.0 592.1 Q 666.0 592.3 670.0 594.5 Q 674.0 596.6 678.0 598.3 Q 682.0 600.1 686.0 600.4 Q 690.0 600.7 694.0 598.6 Q 698.0 596.6 702.0 594.8 Q 706.0 593.0 710.0 592.4 Q 714.0 591.8 718.0 591.6 Q 722.0 591.5 726.0 594.0 Q 730.0 596.6 734.0 598.1 Q 738.0 599.6 742.0 600.2 Q 746.0 600.8 750.0 599.6 Q 754.0 598.3 758.0 596.8 Q 762.0 595.2 766.0 593.2 Q 770.0 591.3 774.0 592.0 Q 778.0 592.7 782.0 593.5 Q 786.0 594.4 790.0 596.3 Q 794.0 598.1 798.0 599.8 Q 802.0 601.5 806.0 599.9 Q 810.0 598.4 814.0 597.2 Q 818.0 596.0 822.0 594.2 Q 826.0 592.5 830.0 592.0 Q 834.0 591.5 838.0 592.5 Q 842.0 593.4 846.0 595.6 Q 850.0 597.7 854.0 599.4 Q 858.0 601.2 862.0 600.2 Q 866.0 599.3 870.0 597.6 Q 874.0 595.9 878.0 594.5 Q 882.0 593.1 886.0 592.6 Q 890.0 592.1 894.0 592.7 Q 898.0 593.3 902.0 594.7 Q 906.0 596.2 910.0 598.4 Q 914.0 600.6 918.0 601.1 Q 922.0 601.6 926.0 599.1 Q 930.0 596.6 934.0 595.1 Q 938.0 593.6 942.0 592.3 Q 946.0 591.1 950.0 591.9 Q 954.0 592.7 958.0 594.7 Q 962.0 596.8 966.0 598.2 Q 970.0 599.6 974.0 600.3 Q 978.0 601.0 982.0 599.3 Q 986.0 597.6 990.0 596.4 Q 994.0 595.2 998.0 593.2 Q 1002.0 591.2 1006.0 591.1 Q 1010.0 591.0 1014.0 593.0 Q 1018.0 595.1 1022.0 597.0 Q 1026.0 598.9 1030.0 600.0 Q 1034.0 601.1 1038.0 600.3 Q 1042.0 599.5 1046.0 597.3 Q 1050.0 595.0 1054.0 593.1 Q 1058.0 591.2 1062.0 591.7 Q 1066.0 592.1 1070.0 593.1 Q 1074.0 594.1 1078.0 596.1 Q 1082.0 598.1 1086.0 599.2 Q 1090.0 600.2 1094.0 599.8 Q 1098.0 599.4 1102.0 597.7 Q 1106.0 596.0 1110.0 594.6 Q 1114.0 593.3 1118.0 591.8 Q 1122.0 590.3 1126.0 592.2 Q 1130.0 594.0 1134.0 595.3 Q 1138.0 596.5 1142.0 598.8 Q 1146.0 601.1 1150.0 600.7 Q 1154.0 600.3 1158.0 598.7 Q 1162.0 597.2 1164.0 596.3 L 1166.0 595.5';
const FRAME_LEFT =
  'M 34.5 34.0 Q 36.8 42.0 37.8 46.0 Q 38.8 50.0 37.2 54.0 Q 35.6 58.0 34.3 62.0 Q 33.0 66.0 31.1 70.0 Q 29.3 74.0 29.4 78.0 Q 29.6 82.0 30.9 86.0 Q 32.2 90.0 34.3 94.0 Q 36.5 98.0 37.8 102.0 Q 39.1 106.0 37.9 110.0 Q 36.8 114.0 34.7 118.0 Q 32.5 122.0 31.4 126.0 Q 30.3 130.0 29.7 134.0 Q 29.1 138.0 30.8 142.0 Q 32.5 146.0 34.7 150.0 Q 36.9 154.0 37.7 158.0 Q 38.4 162.0 38.5 166.0 Q 38.6 170.0 36.3 174.0 Q 34.1 178.0 32.5 182.0 Q 30.9 186.0 30.0 190.0 Q 29.1 194.0 30.4 198.0 Q 31.7 202.0 33.4 206.0 Q 35.2 210.0 36.3 214.0 Q 37.3 218.0 38.4 222.0 Q 39.5 226.0 37.3 230.0 Q 35.2 234.0 33.8 238.0 Q 32.4 242.0 31.0 246.0 Q 29.7 250.0 29.8 254.0 Q 30.0 258.0 32.2 262.0 Q 34.5 266.0 35.8 270.0 Q 37.1 274.0 37.8 278.0 Q 38.6 282.0 37.9 286.0 Q 37.1 290.0 34.2 294.0 Q 31.3 298.0 29.8 302.0 Q 28.3 306.0 28.9 310.0 Q 29.5 314.0 31.6 318.0 Q 33.7 322.0 35.5 326.0 Q 37.3 330.0 38.3 334.0 Q 39.4 338.0 38.7 342.0 Q 38.1 346.0 35.9 350.0 Q 33.6 354.0 31.8 358.0 Q 30.0 362.0 29.1 366.0 Q 28.2 370.0 29.9 374.0 Q 31.6 378.0 33.9 382.0 Q 36.2 386.0 37.9 390.0 Q 39.6 394.0 38.8 398.0 Q 37.9 402.0 36.2 406.0 Q 34.5 410.0 32.5 414.0 Q 30.6 418.0 29.9 422.0 Q 29.2 426.0 30.4 430.0 Q 31.6 434.0 33.7 438.0 Q 35.9 442.0 37.3 446.0 Q 38.8 450.0 38.6 454.0 Q 38.4 458.0 37.2 462.0 Q 36.0 466.0 33.9 470.0 Q 31.9 474.0 30.4 478.0 Q 29.0 482.0 30.1 486.0 Q 31.2 490.0 33.0 494.0 Q 34.8 498.0 36.6 502.0 Q 38.3 506.0 38.8 510.0 Q 39.3 514.0 38.4 518.0 Q 37.6 522.0 35.3 526.0 Q 33.0 530.0 30.7 534.0 Q 28.4 538.0 28.5 542.0 Q 28.6 546.0 30.8 550.0 Q 33.0 554.0 35.4 558.0 Q 37.8 562.0 38.2 566.0 Q 38.7 570.0 38.1 574.0 Q 37.5 578.0 35.3 582.0 Q 33.0 586.0 31.4 590.0 Q 29.8 594.0 29.6 595.0 L 29.4 596.0';
const FRAME_RIGHT =
  'M 1166.9 34.0 Q 1169.4 42.0 1169.9 46.0 Q 1170.3 50.0 1169.0 54.0 Q 1167.7 58.0 1165.7 62.0 Q 1163.8 66.0 1162.6 70.0 Q 1161.4 74.0 1161.0 78.0 Q 1160.7 82.0 1163.3 86.0 Q 1166.0 90.0 1167.6 94.0 Q 1169.3 98.0 1170.4 102.0 Q 1171.4 106.0 1170.7 110.0 Q 1170.0 114.0 1167.6 118.0 Q 1165.2 122.0 1163.8 126.0 Q 1162.4 130.0 1162.2 134.0 Q 1162.0 138.0 1163.0 142.0 Q 1164.0 146.0 1166.3 150.0 Q 1168.6 154.0 1169.6 158.0 Q 1170.6 162.0 1170.4 166.0 Q 1170.1 170.0 1168.6 174.0 Q 1167.1 178.0 1165.3 182.0 Q 1163.5 186.0 1162.8 190.0 Q 1162.1 194.0 1162.5 198.0 Q 1162.9 202.0 1164.8 206.0 Q 1166.7 210.0 1168.9 214.0 Q 1171.1 218.0 1170.6 222.0 Q 1170.1 226.0 1169.1 230.0 Q 1168.2 234.0 1165.8 238.0 Q 1163.5 242.0 1162.1 246.0 Q 1160.7 250.0 1161.4 254.0 Q 1162.1 258.0 1163.5 262.0 Q 1164.9 266.0 1167.4 270.0 Q 1169.8 274.0 1170.4 278.0 Q 1171.0 282.0 1170.1 286.0 Q 1169.2 290.0 1166.3 294.0 Q 1163.5 298.0 1162.8 302.0 Q 1162.0 306.0 1161.7 310.0 Q 1161.4 314.0 1163.0 318.0 Q 1164.6 322.0 1166.8 326.0 Q 1169.1 330.0 1169.6 334.0 Q 1170.0 338.0 1169.9 342.0 Q 1169.7 346.0 1167.3 350.0 Q 1165.0 354.0 1163.5 358.0 Q 1162.0 362.0 1161.2 366.0 Q 1160.4 370.0 1162.7 374.0 Q 1164.9 378.0 1166.9 382.0 Q 1168.9 386.0 1170.3 390.0 Q 1171.7 394.0 1170.8 398.0 Q 1169.8 402.0 1167.8 406.0 Q 1165.9 410.0 1164.4 414.0 Q 1162.9 418.0 1162.0 422.0 Q 1161.0 426.0 1161.5 430.0 Q 1162.0 434.0 1164.8 438.0 Q 1167.7 442.0 1169.5 446.0 Q 1171.4 450.0 1170.5 454.0 Q 1169.6 458.0 1168.6 462.0 Q 1167.6 466.0 1165.9 470.0 Q 1164.3 474.0 1162.9 478.0 Q 1161.5 482.0 1161.9 486.0 Q 1162.3 490.0 1164.7 494.0 Q 1167.1 498.0 1168.2 502.0 Q 1169.3 506.0 1170.4 510.0 Q 1171.5 514.0 1169.9 518.0 Q 1168.3 522.0 1166.3 526.0 Q 1164.3 530.0 1163.1 534.0 Q 1161.8 538.0 1161.1 542.0 Q 1160.5 546.0 1162.4 550.0 Q 1164.4 554.0 1166.7 558.0 Q 1169.0 562.0 1170.3 566.0 Q 1171.6 570.0 1170.9 574.0 Q 1170.2 578.0 1167.4 582.0 Q 1164.5 586.0 1163.1 590.0 Q 1161.8 594.0 1161.6 595.0 L 1161.4 596.0';

// Corner tick marks — small hand-drawn "X" pins where the wobble strokes
// deliberately don't quite meet (a classic freehand-frame tell).
function cornerTick(cx: number, cy: number, rotate: number): Node {
  const r = 9;
  return el(
    'path',
    {
      d: `M ${cx - r} ${cy - r} L ${cx + r} ${cy + r} M ${cx + r} ${cy - r} L ${cx - r} ${cy + r}`,
      stroke: BLUE,
      'stroke-width': 3.4,
      'stroke-linecap': 'round',
      fill: 'none',
      transform: `rotate(${rotate} ${cx} ${cy})`,
    }
  );
}

function frameSvg(): Node {
  return el(
    'svg',
    {
      width: 1200,
      height: 630,
      viewBox: '0 0 1200 630',
      style: { position: 'absolute', top: 0, left: 0 },
    },
    [
      el('path', { d: FRAME_TOP, stroke: AMBER, 'stroke-width': FRAME_STROKE, 'stroke-linecap': 'round', fill: 'none' }),
      el('path', { d: FRAME_BOTTOM, stroke: AMBER, 'stroke-width': FRAME_STROKE, 'stroke-linecap': 'round', fill: 'none' }),
      el('path', { d: FRAME_LEFT, stroke: AMBER, 'stroke-width': FRAME_STROKE, 'stroke-linecap': 'round', fill: 'none' }),
      el('path', { d: FRAME_RIGHT, stroke: AMBER, 'stroke-width': FRAME_STROKE, 'stroke-linecap': 'round', fill: 'none' }),
      cornerTick(FRAME_INSET, FRAME_INSET, -8),
      cornerTick(1200 - FRAME_INSET, FRAME_INSET, 8),
      cornerTick(FRAME_INSET, 630 - FRAME_INSET, 8),
      cornerTick(1200 - FRAME_INSET, 630 - FRAME_INSET, -8),
    ]
  );
}

export async function renderOgCard({
  title,
  subtitle,
}: {
  title: string;
  subtitle: string;
}): Promise<Buffer> {
  const titleSize = title.length > 55 ? 46 : title.length > 35 ? 54 : 66;
  const tree = div(
    {
      flexDirection: 'column',
      width: '1200px',
      height: '630px',
      backgroundColor: BG,
      position: 'relative',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: 'FreeSans',
    },
    [
      // Grain: baked-alpha noise tile, composited straight (satori has no
      // mix-blend-mode) — alpha is kept low in the source PNG itself so it
      // reads as paper texture without touching text contrast.
      div({
        position: 'absolute',
        top: 0,
        left: 0,
        width: '1200px',
        height: '630px',
        backgroundImage: `url(${grainDataUri})`,
        backgroundRepeat: 'repeat',
        backgroundSize: '180px 180px',
      }),
      // Structural top/bottom bars — brand continuity with the original card.
      div({ position: 'absolute', top: 0, left: 0, width: '1200px', height: '12px', backgroundColor: BLUE }),
      div({ position: 'absolute', bottom: 0, left: 0, width: '1200px', height: '8px', backgroundColor: AMBER }),
      // Hand-wobble frame (native SVG, not CSS — see frameSvg()).
      frameSvg(),
      // Kicker: hand-note voice, matches the site nameplate ("Field Notes").
      div(
        {
          position: 'absolute',
          top: '66px',
          left: '78px',
          fontFamily: 'ShantellSans',
          fontSize: 30,
          color: AMBER,
          transform: 'rotate(-3deg)',
        },
        'Field Notes'
      ),
      div({ flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '50px 96px', maxWidth: '1010px' }, [
        div({ fontFamily: 'FreeSansBold', fontSize: titleSize, color: TITLE, textAlign: 'center', lineHeight: 1.18 }, title),
        div({ fontSize: 28, color: SUB, marginTop: '26px', textAlign: 'center' }, subtitle),
      ]),
      div({ position: 'absolute', bottom: '46px', flexDirection: 'row', alignItems: 'center' }, [
        // Plain ASCII only — the embedded font subsets (see fonts/README.md)
        // cover Latin + basic punctuation, not misc-symbol codepoints, and
        // satori fails silently (blank glyph) rather than erroring on a
        // missing character. Verified via cmap before committing to this.
        div({ fontFamily: 'ShantellSans', fontSize: 26, color: AMBER, marginRight: '10px' }, '*'),
        div({ fontSize: 26, color: FOOT }, 'williamzujkowski.github.io'),
      ]),
    ]
  );

  const svg = await satori(tree as never, {
    width: 1200,
    height: 630,
    fonts: [
      { name: 'FreeSans', data: regular, weight: 400, style: 'normal' },
      { name: 'FreeSansBold', data: bold, weight: 700, style: 'normal' },
      { name: 'ShantellSans', data: shantell, weight: 500, style: 'normal' },
    ],
  });

  return Buffer.from(new Resvg(svg, { fitTo: { mode: 'width', value: 1200 } }).render().asPng());
}
