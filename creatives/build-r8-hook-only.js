// R8: hook-only creative. Same gradients as the R3 Orange/Purple winners, but the on-image
// text is cut from ~12 lines to the hook alone, set much larger (reference: single bold
// italic line on a gradient). Copy lives in ads/ninu-r8-hook-only.md.
//
// Hook test: A/B are the control hook (both colors). C and D are the two new hooks, Orange only
// so the hook is the single variable.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const SIZE = [1080, 1920];
const OUT = path.join(__dirname, 'png', 'R8-Hook-Only');
fs.mkdirSync(OUT, { recursive: true });

const ORANGE = 'linear-gradient(135deg, #ffb347 0%, #ff7a3d 25%, #ff4e4e 55%, #e5366b 80%, #c6327a 100%)';
const PURPLE = 'linear-gradient(135deg, #3E7BEA 0%, #6A5CEE 32%, #A855D1 62%, #D93FA8 85%, #E8399E 100%)';

const CONTROL = { lines: ['ok i actually', 'do my scalp oil', 'EVERY night', 'now 😭'], size: 122 };
const PAIN = { lines: ['baby up 3 times.', 'wet hands, in bed.', 'skipped my scalp', 'oil again 😭'], size: 105 };
const MECHANISM = { lines: ['i thought i was bad', 'at scalp oil.', 'i was just doing', 'it wrong 😭'], size: 101 };

const VARIANTS = [
  { key: 'A__Orange-HookOnly', gradient: ORANGE, ...CONTROL },
  { key: 'B__Purple-HookOnly', gradient: PURPLE, ...CONTROL },
  { key: 'C__Orange-Hook-Pain', gradient: ORANGE, ...PAIN },
  { key: 'D__Orange-Hook-Mechanism', gradient: ORANGE, ...MECHANISM },
];

function html(v) {
  const [w, h] = SIZE;
  return `<!doctype html>
<html><head><meta charset="utf-8"><style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width: ${w}px; height: ${h}px; overflow: hidden; }
  body {
    background: ${v.gradient};
    display: flex; align-items: center; justify-content: center;
    text-align: center; padding: 0 70px;
  }
  .hook {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    font-style: italic; font-weight: 800;
    font-size: ${v.size}px; line-height: 1.12; letter-spacing: -2px;
    color: #fff; white-space: nowrap;
    text-shadow: 0 3px 18px rgba(0,0,0,0.12);
  }
</style></head><body><div class="hook">${v.lines.map(l => `<div>${l}</div>`).join('')}</div></body></html>`;
}

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
  for (const v of VARIANTS) {
    const page = await browser.newPage({ viewport: { width: SIZE[0], height: SIZE[1] } });
    await page.setContent(html(v), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(400);
    const widest = await page.evaluate(() => Math.max(...[...document.querySelectorAll('.hook div')].map(d => { const r = document.createRange(); r.selectNodeContents(d); return r.getBoundingClientRect().width; })));
    if (widest > SIZE[0] - 140) console.warn(`! ${v.key}: widest line ${Math.round(widest)}px exceeds safe width`);
    const outPath = path.join(OUT, `R8-${v.key}__9x16.png`);
    await page.screenshot({ path: outPath });
    await page.close();
    console.log(`✓ ${outPath}`);
  }
  await browser.close();
})();
