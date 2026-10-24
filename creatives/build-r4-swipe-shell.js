// R4 Ad 1 swipe reproduction — graphic shell (wordmark, badge, headline, bullets, button,
// warm terracotta/gold burst background). Product photo is a placeholder until the
// generated image comes back, then this script re-renders with the real asset.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const SIZES = { '9x16': [1080, 1920] };
const OUT = path.join(__dirname, 'png', 'R4-Ad1-Swipe-Reproduction');
fs.mkdirSync(OUT, { recursive: true });

// Swap this to the real generated product shot's local path/URL once available.
const PRODUCT_IMG = process.env.NINU_PRODUCT_IMG || null;

const COPY = {
  badge: '30-DAY GUARANTEE',
  headline: "Your messy oil routine's\nworst nightmare.",
  bullets: [
    'Precise, mess-free application.\nNo oil ending up on your pillow.',
    'Turns your nightly routine into\nsomething that actually takes two minutes.',
    'Targets your scalp, not your hair,\nso nothing goes to waste.',
  ],
  cta: 'SHOP NOW',
};

function shellHTML(ratio) {
  const [w, h] = SIZES[ratio];
  const bullets = COPY.bullets.map(b => {
    const lines = b.split('\n').map(l => `<span>${l}</span>`).join('<br>');
    return `<div class="bullet"><span class="check">✓</span><span class="btext">${lines}</span></div>`;
  }).join('');
  const headlineLines = COPY.headline.split('\n').map(l => `<div>${l}</div>`).join('');

  const productBlock = PRODUCT_IMG
    ? `<img class="product-img" src="${PRODUCT_IMG}" alt="The Ninu Dispenser">`
    : `<div class="product-placeholder">PRODUCT SHOT<br><span>swap in generated image</span></div>`;

  return `<!doctype html>
<html><head><meta charset="utf-8"><style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width: ${w}px; height: ${h}px; overflow: hidden; }
  body {
    position: relative;
    background: linear-gradient(155deg, #C98A52 0%, #B85A3E 42%, #8E3F27 100%);
    font-family: 'Georgia', 'Cormorant Garamond', serif;
    color: #F5EFE6;
    display: flex;
    flex-direction: column;
    padding: 64px 56px 72px;
  }
  /* Holographic ray burst, focal point lower-right behind the product */
  .rays {
    position: absolute;
    inset: 0;
    background: repeating-conic-gradient(
      from 0deg at 78% 82%,
      rgba(255,236,210,0.16) 0deg 4deg,
      rgba(255,255,255,0) 4deg 11deg
    );
    filter: blur(1px);
    mix-blend-mode: overlay;
    opacity: 0.9;
  }
  .glow {
    position: absolute;
    right: -10%;
    bottom: -8%;
    width: 760px;
    height: 760px;
    background: radial-gradient(circle, rgba(255,222,179,0.55) 0%, rgba(255,222,179,0) 68%);
    filter: blur(2px);
  }
  .vignette {
    position: absolute;
    inset: 0;
    background: linear-gradient(0deg, rgba(20,10,5,0.55) 0%, rgba(20,10,5,0) 28%);
  }

  .content { position: relative; z-index: 2; display: flex; flex-direction: column; height: 100%; }

  .wordmark {
    text-align: center;
    font-size: 30px;
    letter-spacing: 0.32em;
    font-weight: 500;
    margin-bottom: 36px;
    font-family: 'Cormorant Garamond', Georgia, serif;
  }

  .badge-row { display: flex; justify-content: center; margin-bottom: 26px; }
  .badge {
    background: #F5EFE6;
    color: #241812;
    font-family: -apple-system, 'Helvetica Neue', sans-serif;
    font-size: 19px;
    font-weight: 700;
    letter-spacing: 0.04em;
    padding: 12px 26px;
    border-radius: 999px;
  }

  .headline {
    font-size: 54px;
    font-weight: 600;
    line-height: 1.14;
    text-align: center;
    letter-spacing: -0.5px;
    margin-bottom: 48px;
    text-shadow: 0 2px 14px rgba(0,0,0,0.18);
  }

  .bullets { display: flex; flex-direction: column; gap: 26px; margin-bottom: auto; max-width: 560px; }
  .bullet { display: flex; align-items: flex-start; gap: 16px; }
  .check {
    flex-shrink: 0;
    width: 30px; height: 30px;
    border: 2px solid #F5EFE6;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
    font-family: -apple-system, sans-serif;
    margin-top: 2px;
  }
  .btext {
    font-family: -apple-system, 'Helvetica Neue', sans-serif;
    font-size: 23px;
    line-height: 1.38;
    font-weight: 500;
  }

  .bottom-row {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    margin-top: 40px;
  }
  .cta-btn {
    background: #241812;
    color: #F5EFE6;
    font-family: -apple-system, 'Helvetica Neue', sans-serif;
    font-size: 19px;
    font-weight: 700;
    letter-spacing: 0.08em;
    padding: 20px 38px;
    border-radius: 6px;
  }

  .product-zone { position: absolute; right: 0; bottom: 0; width: 56%; height: 58%; z-index: 1; }
  .product-img { width: 100%; height: 100%; object-fit: contain; object-position: bottom right; }
  .product-placeholder {
    width: 100%; height: 100%;
    border: 2px dashed rgba(245,239,230,0.6);
    border-radius: 14px;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    color: rgba(245,239,230,0.75);
    font-family: -apple-system, sans-serif;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-align: center;
  }
  .product-placeholder span { font-size: 13px; font-weight: 400; letter-spacing: 0.04em; margin-top: 8px; opacity: 0.8; }
</style></head><body>
  <div class="rays"></div>
  <div class="glow"></div>
  <div class="vignette"></div>
  <div class="product-zone">${productBlock}</div>

  <div class="content">
    <div class="wordmark">N I N U</div>
    <div class="badge-row"><div class="badge">${COPY.badge}</div></div>
    <div class="headline">${headlineLines}</div>
    <div class="bullets">${bullets}</div>
    <div class="bottom-row">
      <div class="cta-btn">${COPY.cta}</div>
    </div>
  </div>
</body></html>`;
}

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const ratio of Object.keys(SIZES)) {
    const [w, h] = SIZES[ratio];
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    await page.setContent(shellHTML(ratio), { waitUntil: 'load' });
    const outPath = path.join(OUT, `Ad1-Swipe-Reproduction__${ratio}.png`);
    await page.screenshot({ path: outPath });
    await page.close();
    console.log(`✓ ${outPath}`);
  }
  await browser.close();
})();
