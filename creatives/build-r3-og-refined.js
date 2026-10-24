// R3 CPM refinement: OG Ad C control, larger text, 3 background colors.
// Same copy as the winning control (no hook change) — text size + color are the only variables.
// 9:16 only per user instruction.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const SIZE = [1080, 1920];
const OUT = path.join(__dirname, 'png', 'R3-OG-Refined-Colors');
fs.mkdirSync(OUT, { recursive: true });

const TEXT = `ok i actually do my scalp
oil EVERY night now 😭

and it's because of this
one little dispenser tool

i had the castor oil
i had good intentions
i just couldn't make
myself be consistent

the habit was always there
the routine just needed to
be easier than the reason
to quit`;

const VARIANTS = [
  {
    key: 'A__Orange-Large',
    gradient: 'linear-gradient(135deg, #ffb347 0%, #ff7a3d 25%, #ff4e4e 55%, #e5366b 80%, #c6327a 100%)',
  },
  {
    key: 'B__Purple-Large',
    // matches the reference: blue top-left easing through violet into magenta/pink bottom-right
    gradient: 'linear-gradient(135deg, #3E7BEA 0%, #6A5CEE 32%, #A855D1 62%, #D93FA8 85%, #E8399E 100%)',
  },
  {
    key: 'C__Green-Large',
    // matches the reference: sky blue at top easing through teal/green into gold at the bottom
    gradient: 'linear-gradient(165deg, #4FA8E0 0%, #2FB5A8 32%, #4FBF5C 60%, #9BC23F 82%, #D9B33C 100%)',
  },
];

function storyHTML(gradient) {
  const [w, h] = SIZE;
  const paragraphs = TEXT.split('\n\n').map(para => {
    const lines = para.split('\n').map(l => `<div>${l}</div>`).join('');
    return `<div class="para">${lines}</div>`;
  }).join('');

  return `<!doctype html>
<html><head><meta charset="utf-8"><style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width: ${w}px; height: ${h}px; overflow: hidden; }
  body {
    background: ${gradient};
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, sans-serif;
    display: flex; align-items: center; justify-content: center;
    text-align: center;
    padding: 60px 56px;
  }
  .wrap {
    color: #ffffff;
    font-size: 70px;
    font-weight: 700;
    line-height: 1.26;
    letter-spacing: -0.4px;
    text-shadow: 0 2px 12px rgba(0,0,0,0.1);
  }
  .para { margin-bottom: 28px; }
  .para:last-child { margin-bottom: 0; }
</style></head><body>
  <div class="wrap">${paragraphs}</div>
</body></html>`;
}

(async () => {
  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  });

  for (const v of VARIANTS) {
    const page = await browser.newPage({ viewport: { width: SIZE[0], height: SIZE[1] } });
    await page.setContent(storyHTML(v.gradient), { waitUntil: 'load' });
    const outPath = path.join(OUT, `OG-Refined-${v.key}__9x16.png`);
    await page.screenshot({ path: outPath });
    await page.close();
    console.log(`✓ ${outPath}`);
  }

  await browser.close();
})();
