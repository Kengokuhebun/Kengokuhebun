// R8: hook-only creative. Same gradients as the R3 Orange/Purple winners, but the on-image
// text is cut from ~12 lines to the hook alone, set much larger (reference: single bold
// italic line on a gradient). Copy lives in ads/ninu-r8-hook-only.md.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const SIZE = [1080, 1920];
const OUT = path.join(__dirname, 'png', 'R8-Hook-Only');
fs.mkdirSync(OUT, { recursive: true });

const HOOK_LINES = ['ok i actually', 'do my scalp oil', 'EVERY night', 'now 😭'];

const VARIANTS = [
  {
    key: 'A__Orange-HookOnly',
    gradient: 'linear-gradient(135deg, #ffb347 0%, #ff7a3d 25%, #ff4e4e 55%, #e5366b 80%, #c6327a 100%)',
  },
  {
    key: 'B__Purple-HookOnly',
    gradient: 'linear-gradient(135deg, #3E7BEA 0%, #6A5CEE 32%, #A855D1 62%, #D93FA8 85%, #E8399E 100%)',
  },
];

function html(gradient) {
  const [w, h] = SIZE;
  return `<!doctype html>
<html><head><meta charset="utf-8"><style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width: ${w}px; height: ${h}px; overflow: hidden; }
  body {
    background: ${gradient};
    display: flex; align-items: center; justify-content: center;
    text-align: center; padding: 0 70px;
  }
  .hook {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    font-style: italic; font-weight: 800;
    font-size: 122px; line-height: 1.12; letter-spacing: -2px;
    color: #fff; white-space: nowrap;
    text-shadow: 0 3px 18px rgba(0,0,0,0.12);
  }
</style></head><body><div class="hook">${HOOK_LINES.map(l => `<div>${l}</div>`).join('')}</div></body></html>`;
}

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
  for (const v of VARIANTS) {
    const page = await browser.newPage({ viewport: { width: SIZE[0], height: SIZE[1] } });
    await page.setContent(html(v.gradient), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(400);
    const outPath = path.join(OUT, `R8-${v.key}__9x16.png`);
    await page.screenshot({ path: outPath });
    await page.close();
    console.log(`✓ ${outPath}`);
  }
  await browser.close();
})();
