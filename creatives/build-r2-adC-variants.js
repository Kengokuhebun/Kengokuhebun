// Renders the 4 new Ad C hook variants at 9:16 for the R2 hook test.
// Same orange gradient + font treatment as the Ad C control image.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const SIZE = [1080, 1920]; // 9:16 only
const OUT = path.join(__dirname, 'png', 'R2-AdC-Hook-Variants');
fs.mkdirSync(OUT, { recursive: true });

const CLOSE = `the habit was always there
the routine just needed to
be easier than the reason
to quit`;

const VARIANTS = [
  {
    key: 'B__Shelf-Confession',
    text: `i have THREE bottles
of scalp oil on my shelf
and they're all still
mostly full 😭

the only one i actually
use every night is since
i got this one dispenser

${CLOSE}`,
  },
  {
    key: 'C__Habit-Death-Moment',
    text: `6 weeks postpartum
i started my scalp
oil routine

by week 8 the bottle
was in the back of
my drawer 😭

got it back out when i
found this one little
dispenser tool

${CLOSE}`,
  },
  {
    key: 'D__Social-Compare',
    text: `every mom in my fb group
did her nightly oil for
6 months straight

i made it eleven nights 😭
then i found this one
little dispenser tool

${CLOSE}`,
  },
  {
    key: 'E__Dialogue-Sister',
    text: `my sister: "when was
the last time you
actually did your oil"

me: "five days ago" 😭
the real answer was
eighteen days ago

now it's a different
answer because of this
one little tool

${CLOSE}`,
  },
];

function storyHTML(text) {
  const [w, h] = SIZE;
  const paragraphs = text.split('\n\n').map(para => {
    const lines = para.split('\n').map(l => `<div>${l}</div>`).join('');
    return `<div class="para">${lines}</div>`;
  }).join('');

  return `<!doctype html>
<html><head><meta charset="utf-8"><style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width: ${w}px; height: ${h}px; overflow: hidden; }
  body {
    background: linear-gradient(135deg, #ffb347 0%, #ff7a3d 25%, #ff4e4e 55%, #e5366b 80%, #c6327a 100%);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, sans-serif;
    display: flex; align-items: center; justify-content: center;
    text-align: center;
    padding: 60px 70px;
  }
  .wrap {
    color: #ffffff;
    font-size: 58px;
    font-weight: 600;
    line-height: 1.28;
    letter-spacing: -0.3px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.08);
  }
  .para { margin-bottom: 26px; }
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
    await page.setContent(storyHTML(v.text), { waitUntil: 'load' });
    const outPath = path.join(OUT, `AdC-Hook-${v.key}__9x16.png`);
    await page.screenshot({ path: outPath });
    await page.close();
    console.log(`✓ ${outPath}`);
  }

  await browser.close();
})();
