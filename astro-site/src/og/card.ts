/**
 * Build-time OG/social card generator (#178).
 * satori (JSX-free object tree) -> SVG -> PNG via resvg. Matches the site's
 * brand: dark navy, blue top bar + corner brackets, bold title, footer.
 */
import satori from 'satori';
import { Resvg } from '@resvg/resvg-js';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const fontDir = resolve(process.cwd(), 'src/og/fonts');
const bold = readFileSync(resolve(fontDir, 'FreeSansBold.ttf'));
const regular = readFileSync(resolve(fontDir, 'FreeSans.ttf'));

const BG = '#1a1f2e';
const BLUE = '#3b82f6';
const TITLE = '#f8fafc';
const SUB = '#94a3b8';
const FOOT = '#64748b';

type Node = { type: string; props: { style: Record<string, unknown>; children?: unknown } };
function div(style: Record<string, unknown>, children?: unknown): Node {
  // satori requires an explicit display on every element.
  return { type: 'div', props: { style: { display: 'flex', ...style }, children } };
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
      div({ position: 'absolute', top: 0, left: 0, width: '1200px', height: '12px', backgroundColor: BLUE }),
      div({ flexDirection: 'row', alignItems: 'stretch', maxWidth: '1010px' }, [
        div({ width: '40px', borderLeft: `5px solid ${BLUE}`, borderTop: `5px solid ${BLUE}`, borderBottom: `5px solid ${BLUE}` }),
        div({ flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '50px 56px' }, [
          div({ fontFamily: 'FreeSansBold', fontSize: titleSize, color: TITLE, textAlign: 'center', lineHeight: 1.18 }, title),
          div({ fontSize: 28, color: SUB, marginTop: '26px', textAlign: 'center' }, subtitle),
        ]),
        div({ width: '40px', borderRight: `5px solid ${BLUE}`, borderTop: `5px solid ${BLUE}`, borderBottom: `5px solid ${BLUE}` }),
      ]),
      div({ position: 'absolute', bottom: '46px', fontSize: 26, color: FOOT }, 'williamzujkowski.github.io'),
    ]
  );

  const svg = await satori(tree as never, {
    width: 1200,
    height: 630,
    fonts: [
      { name: 'FreeSans', data: regular, weight: 400, style: 'normal' },
      { name: 'FreeSansBold', data: bold, weight: 700, style: 'normal' },
    ],
  });

  return Buffer.from(new Resvg(svg, { fitTo: { mode: 'width', value: 1200 } }).render().asPng());
}
