// R13: iOS Notes static native for the Ninu "installed, not another chore" story (see ads/ninu-r13-static-native-from-quilty.md).
// Writes one self-contained HTML per aspect ratio into creatives/r13-notes/ and renders each to creatives/png/R13-Notes-Native/.
// Usage: node build-r13-notes-native.js   (needs playwright + chromium)
// Every line of note text is lifted from the winning Ad C body (ads/ninu-r8-hook-only.md), lowercased the way a note is typed.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const OUT_HTML = path.join(__dirname, 'r13-notes');
const OUT_PNG = path.join(__dirname, 'png', 'R13-Notes-Native');

const TITLE = 'skipped my scalp oil again';
const LIST = ["baby up 3 times", "wet hands, in bed", "bottle's at the back of the shelf", "towel. cleanup. clean pillowcase", "10pm"];
const SUNDAY = "i'll start over sunday";
const WHY = ["i had the castor oil", "i had the rosemary", "i believe in the routine", "can't do it consistently"];

const ICON = {
  check: '<svg viewBox="0 0 24 24" width="1em" height="1em" fill="none" stroke="#FF9F0A" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9.2"/><path d="M8 12.4l2.8 2.8L16.2 9.6"/></svg>',
  share: '<svg viewBox="0 0 24 24" width="1em" height="1em" fill="none" stroke="#FF9F0A" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 15V3.5M8 7l4-4 4 4"/><path d="M6.5 10H5.2A1.2 1.2 0 0 0 4 11.2v8.1A1.2 1.2 0 0 0 5.2 20.5h13.6a1.2 1.2 0 0 0 1.2-1.2v-8.1a1.2 1.2 0 0 0-1.2-1.2h-1.3"/></svg>',
  more: '<svg viewBox="0 0 24 24" width="1em" height="1em" fill="none" stroke="#FF9F0A" stroke-width="1.8"><circle cx="12" cy="12" r="9.2"/><circle cx="8" cy="12" r="1" fill="#FF9F0A"/><circle cx="12" cy="12" r="1" fill="#FF9F0A"/><circle cx="16" cy="12" r="1" fill="#FF9F0A"/></svg>',
  back: '<svg viewBox="0 0 14 24" width="0.55em" height="1em" fill="none" stroke="#FF9F0A" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M11.5 2.5L3 12l8.5 9.5"/></svg>',
};

function status() {
  return `<div class="st"><span>10:52</span><span class="sti"><svg viewBox="0 0 60 24" width="1.9em" height="0.8em"><rect x="0" y="15" width="8" height="8" rx="2"/><rect x="13" y="10" width="8" height="13" rx="2"/><rect x="26" y="5" width="8" height="18" rx="2"/><rect x="39" y="0" width="8" height="23" rx="2" opacity=".3"/></svg><svg viewBox="0 0 64 26" width="2.2em" height="0.9em"><rect x="1" y="2" width="54" height="22" rx="6" fill="none" stroke="#000" stroke-width="2" opacity=".4"/><rect x="4" y="5" width="30" height="16" rx="3.5"/><rect x="57" y="9" width="4" height="8" rx="2" opacity=".4"/></svg></span></div>`;
}

function nav(compact) {
  return `<div class="nv${compact ? ' c' : ''}"><span class="bk">${ICON.back}<span>Notes</span></span><span class="ic">${ICON.check}${ICON.share}${ICON.more}</span></div>`;
}

function toolbar() {
  return `<div class="tb"><span>${ICON.check}</span><span><svg viewBox="0 0 24 24" width="1em" height="1em" fill="none" stroke="#FF9F0A" stroke-width="1.8" stroke-linecap="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18M9 5v14M15 5v14"/></svg></span><span><svg viewBox="0 0 24 24" width="1em" height="1em" fill="none" stroke="#FF9F0A" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="6.5" width="18" height="13" rx="2.4"/><circle cx="12" cy="13" r="3.4"/><path d="M8.5 6.5L9.6 4h4.8l1.1 2.5"/></svg></span><span><svg viewBox="0 0 24 24" width="1em" height="1em" fill="none" stroke="#FF9F0A" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M16 3.5l4.5 4.5L8.5 20 3.5 20.5 4 15.5z"/></svg></span><span class="cp"><svg viewBox="0 0 24 24" width="1em" height="1em" fill="none" stroke="#FF9F0A" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20l1-4L17 4l3 3L8 19z"/><path d="M14.5 6.5l3 3"/></svg></span></div>`;
}

function css(w, h, kind) {
  // sizes in px at the target canvas width of 1080
  const body = kind === 'wide' ? 46 : 50, title = kind === 'wide' ? 58 : 66, gap = kind === 'wide' ? 0.3 : 0.35;
  return `*{box-sizing:border-box;margin:0;padding:0}html,body{width:${w}px;height:${h}px;background:#fff}
.n{width:${w}px;height:${h}px;background:#fff;color:#000;font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;position:relative;overflow:hidden;-webkit-font-smoothing:antialiased}
.st{height:112px;display:flex;justify-content:space-between;align-items:flex-end;padding:0 64px 14px;font-weight:600;font-size:46px}.sti{display:flex;gap:16px;align-items:center;font-size:46px}.sti svg{fill:#000}
.nv{height:130px;display:flex;justify-content:space-between;align-items:center;padding:0 44px;color:#FF9F0A;font-size:50px}.nv.c{height:${kind === 'wide' ? 92 : 124}px;font-size:${kind === 'wide' ? 40 : 48}px}
.bk{display:flex;align-items:center;gap:14px}.ic{display:flex;gap:40px;font-size:1.0em}
.ts{text-align:center;color:#8E8E93;font-size:${kind === 'wide' ? 28 : 34}px;margin:${kind === 'wide' ? 8 : 18}px 0 ${kind === 'wide' ? 14 : 26}px}
.tx{padding:0 ${kind === 'wide' ? 56 : 64}px}.ti{font-weight:700;font-size:${title}px;line-height:1.15;letter-spacing:-.01em;margin-bottom:${kind === 'wide' ? 14 : 26}px}
.bd{font-size:${body}px;line-height:${1 + gap};white-space:pre-line;letter-spacing:-.005em}
.tb{position:absolute;left:0;right:0;bottom:0;height:200px;border-top:1px solid #d7d7da;display:flex;justify-content:flex-start;gap:96px;align-items:flex-start;padding:30px 64px 0;font-size:60px;background:#f9f9f9}.cp{margin-left:auto}`;
}

function html(w, h, kind, content) {
  const chrome = kind === 'tall' ? status() + nav(false) : nav(true);
  return `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=${w}"><title>R13 notes ${kind}</title><style>${css(w, h, kind)}</style></head><body><div class="n">${chrome}<div class="ts">Today 10:52 PM</div><div class="tx"><div class="ti">${TITLE}</div><div class="bd">${content}</div></div>${kind === 'tall' ? toolbar() : ''}</div></body></html>`;
}

const sq = html(1080, 1080, 'square', [...LIST, '', SUNDAY].join('\n'));
const tall = html(1080, 1920, 'tall', [...LIST, '', SUNDAY, '', ...WHY].join('\n'));
const wide = html(1080, 566, 'wide', LIST.slice(0, 3).join('\n'));

(async () => {
  fs.mkdirSync(OUT_HTML, { recursive: true }); fs.mkdirSync(OUT_PNG, { recursive: true });
  const jobs = [['notes-1x1', 1080, 1080, sq], ['notes-9x16', 1080, 1920, tall], ['notes-191', 1080, 566, wide]];
  const browser = await chromium.launch();
  for (const [name, w, h, markup] of jobs) {
    const f = path.join(OUT_HTML, name + '.html'); fs.writeFileSync(f, markup);
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    await page.goto('file://' + f); await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(OUT_PNG, name + '.png') });
    await page.close(); console.log('rendered', name, `${w}x${h}`);
  }
  await browser.close();
})();
