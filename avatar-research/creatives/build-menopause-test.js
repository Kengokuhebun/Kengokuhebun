// Menopause avatar, 3-angle test creatives. Copy lives in avatar-research/05-menopause-3-angle-copy.md.
// C1: colour hook-only (same gradient + layout as the proven R8 Orange). C2, C3: ugly natives with a story-style caption.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const DIR = __dirname, OUT = path.join(DIR, 'final');
fs.mkdirSync(OUT, { recursive: true });
const ORANGE = 'linear-gradient(135deg, #ffb347 0%, #ff7a3d 25%, #ff4e4e 55%, #e5366b 80%, #c6327a 100%)';
const img = f => 'data:image/png;base64,' + fs.readFileSync(path.join(DIR, 'raw', f)).toString('base64');

const colour = (w, h, size) => `<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}html,body{width:${w}px;height:${h}px;overflow:hidden}
body{background:${ORANGE};display:flex;align-items:center;justify-content:center;text-align:center;padding:0 70px}
.hook{font-family:-apple-system,'Helvetica Neue',Roboto,Arial,sans-serif;font-style:italic;font-weight:800;font-size:${size}px;line-height:1.12;letter-spacing:-2px;color:#fff;white-space:nowrap;text-shadow:0 3px 18px rgba(0,0,0,.12)}
</style></head><body><div class="hook"><div>my hair was always</div><div>my best feature.</div><div>then menopause</div><div>happened 😭</div></div></body></html>`;

const native = (w, h, file, lines, top) => `<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}html,body{width:${w}px;height:${h}px;overflow:hidden;background:#000}
.bg{position:absolute;inset:-60px;background:url(${img(file)}) center/cover;filter:blur(40px) brightness(.55)}
.ph{position:absolute;left:0;width:${w}px;top:${(h - w * 1152 / 896) / 2}px;height:${w * 1152 / 896}px;background:url(${img(file)}) center/cover}
.cap{position:absolute;left:0;right:0;top:${top}px;display:flex;flex-direction:column;align-items:center;gap:0}
.cap span{font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-weight:500;font-size:46px;line-height:1.25;color:#fff;background:rgba(0,0,0,.62);padding:6px 18px;border-radius:10px;margin:-3px 0;text-align:center}
</style></head><body><div class="bg"></div><div class="ph"></div><div class="cap">${lines.map(l => `<span>${l}</span>`).join('')}</div></body></html>`;

const C2 = ['11:47pm. scalp itching again.', 'my derm says it’s all', 'in my head 🙃'];
const C3 = ['2 years since menopause.', 'all of this.', 'nothing changed 😩'];
const JOBS = [
  ['C1__Colour-Identity__4x5', 1080, 1350, colour(1080, 1350, 100)],
  ['C1__Colour-Identity__9x16', 1080, 1920, colour(1080, 1920, 108)],
  ['C2__Native-NightScalp__4x5', 1080, 1350, native(1080, 1350, 'A2-night-v2.png', C2, 120)],
  ['C2__Native-NightScalp__9x16', 1080, 1920, native(1080, 1920, 'A2-night-v2.png', C2, 330)],
  ['C3__Native-TriedEverything__4x5', 1080, 1350, native(1080, 1350, 'A3-counter-v1.png', C3, 70)],
  ['C3__Native-TriedEverything__9x16', 1080, 1920, native(1080, 1920, 'A3-counter-v1.png', C3, 300)],
];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
  for (const [name, w, h, html] of JOBS) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.setContent(html, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(OUT, name + '.png') }); await p.close();
    console.log('ok', name);
  }
  await b.close();
})();
