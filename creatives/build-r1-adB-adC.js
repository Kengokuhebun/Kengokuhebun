// Renders Ad B (dark-mode Reddit post) and Ad C (IG-story confessional) at 3 ratios each.
// Matches reference image 11 (dark Reddit) and image 10 (orange-gradient story).
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const SIZES = { '1x1': [1080, 1080], '9x16': [1080, 1920], '191': [1200, 628] };
const OUT_B = path.join(__dirname, 'png', 'R1-AdB-Reddit-Dark');
const OUT_C = path.join(__dirname, 'png', 'R1-AdC-Story-Confessional');
fs.mkdirSync(OUT_B, { recursive: true });
fs.mkdirSync(OUT_C, { recursive: true });

// -------- Ad B: dark-mode Reddit --------
const AD_B = {
  sub: 'beyondthebump',
  avatarColor: '#ff6b4a',
  avatarLetter: 'b',
  time: '4h ago',
  user: 'u/mama_of_two_tired',
  title: 'Genuinely so tired of being told to just take more biotin.',
  body: `i have a full shelf of things to swallow. prenatals, biotin gummies, collagen powder, liquid iron, hair/skin/nails gummies. been taking most of these for months now and genuinely can't tell if any of it has done anything.

every appointment, every mom group, every 2am scroll, the answer is always something to swallow. and nobody has ever asked me about the actual oil routine i've been doing every single night.

am i the only one noticing this? feels like the whole conversation is just pills.`,
  up: '847',
  comments: '263',
  replies: [
    { user: 'u/third_trimester_tired', color: '#8a4fff', time: '3h', up: '218',
      text: 'literally. my doctor just keeps telling me "give it a year" and prescribing more supplements. my hair is falling out NOW.' },
    { user: 'u/labs_came_back_fine', color: '#2563eb', time: '2h', up: '142',
      text: 'oh my god the dropper comment unlocked something in my brain. half of mine ends up on my pillowcase too' },
    { user: 'u/shedding_season_vol2', color: '#46a758', time: '1h', up: '89',
      text: 'the biotin aisle at target is a whole scam at this point. i have a drawer full of untouched bottles.' },
    { user: 'u/four_months_in', color: '#d97706', time: '47m', up: '54',
      text: 'thank you for posting this. i\'ve literally been doing the same thing for weeks and feeling like a crazy person. not just you.' },
  ],
};

function redditDarkHTML(ratio, p) {
  const [w, h] = SIZES[ratio];
  const bodyParagraphs = p.body.split('\n\n');
  // 1.91:1 shows only the first paragraph (space-constrained)
  const bodyToRender = ratio === '191' ? bodyParagraphs.slice(0, 1) : bodyParagraphs;
  const bodyLines = bodyToRender.map(l => `<p>${l}</p>`).join('');
  const showBody = true;
  const titleSize = ratio === '191' ? 44 : (ratio === '1x1' ? 54 : 72);
  const bodySize = ratio === '191' ? 24 : (ratio === '1x1' ? 32 : 38);
  const showReplies = ratio === '9x16';
  const centerFor191 = ratio === '191' ? 'justify-content: center;' : '';
  const repliesHTML = showReplies ? `<div class="replies">${p.replies.map(r => `
    <div class="reply">
      <div class="reply-head">
        <span class="reply-avatar" style="background:${r.color}"></span>
        <span class="reply-user">${r.user}</span>
        <span class="reply-meta">· ${r.time} · ${r.up} upvotes</span>
      </div>
      <div class="reply-text">${r.text}</div>
    </div>
  `).join('')}</div>` : '';

  return `<!doctype html>
<html><head><meta charset="utf-8"><style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width: ${w}px; height: ${h}px; overflow: hidden; }
  body {
    background: #030303;
    color: #d7dadc;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, sans-serif;
    display: flex; flex-direction: column;
    padding: ${ratio === '191' ? '36px 60px' : '48px 44px'};
    ${centerFor191}
  }
  .top { display: flex; align-items: center; gap: 14px; margin-bottom: 16px; }
  .avatar {
    width: ${ratio === '191' ? '44px' : '56px'};
    height: ${ratio === '191' ? '44px' : '56px'};
    border-radius: 50%;
    background: ${p.avatarColor};
    color: #fff;
    font-weight: 700;
    font-size: ${ratio === '191' ? '24px' : '30px'};
    display: flex; align-items: center; justify-content: center;
  }
  .sub-line {
    display: flex; align-items: baseline; gap: 10px;
    font-size: ${ratio === '191' ? '24px' : '30px'};
    color: #ffffff;
    font-weight: 700;
  }
  .sub-line .dot { color: #818384; font-weight: 400; }
  .sub-line .time { color: #818384; font-weight: 400; font-size: ${ratio === '191' ? '22px' : '26px'}; }
  .user {
    color: #818384;
    font-size: ${ratio === '191' ? '22px' : '26px'};
    margin-left: ${ratio === '191' ? '58px' : '70px'};
    margin-top: -2px;
    margin-bottom: ${ratio === '191' ? '24px' : '36px'};
  }
  .menu-dots {
    margin-left: auto;
    color: #818384;
    font-size: 32px;
    letter-spacing: 3px;
  }
  .join {
    margin-left: auto;
    background: #0079d3;
    color: #fff;
    padding: ${ratio === '191' ? '8px 22px' : '10px 28px'};
    border-radius: 999px;
    font-weight: 700;
    font-size: ${ratio === '191' ? '22px' : '26px'};
  }
  .title {
    font-size: ${titleSize}px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.22;
    margin-bottom: ${ratio === '191' ? '18px' : '28px'};
    letter-spacing: -0.3px;
  }
  .body {
    font-size: ${bodySize}px;
    line-height: 1.48;
    color: #c8ced3;
    margin-bottom: ${ratio === '191' ? '20px' : '36px'};
  }
  .body p { margin-bottom: ${ratio === '9x16' ? '26px' : '18px'}; }
  .actions {
    display: flex; gap: 12px; align-items: center;
    flex-wrap: wrap;
    padding-bottom: ${ratio === '9x16' ? '24px' : '0'};
    border-bottom: ${ratio === '9x16' ? '1px solid #272729' : 'none'};
  }
  .replies { margin-top: 32px; display: flex; flex-direction: column; gap: 32px; }
  .reply { padding: 0 0 0 8px; border-left: 2px solid #272729; padding-left: 24px; }
  .reply-head { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; font-size: 28px; }
  .reply-avatar { width: 44px; height: 44px; border-radius: 50%; display: inline-block; }
  .reply-user { color: #ffffff; font-weight: 700; }
  .reply-meta { color: #818384; }
  .reply-text { color: #d7dadc; font-size: 34px; line-height: 1.45; }
  .pill {
    background: #1a1a1b;
    border: 1px solid #272729;
    color: #d7dadc;
    padding: ${ratio === '191' ? '12px 20px' : '16px 26px'};
    border-radius: 999px;
    font-size: ${ratio === '191' ? '24px' : '30px'};
    font-weight: 600;
    display: flex; align-items: center; gap: 10px;
  }
  .pill .arrow { color: #818384; font-size: ${ratio === '191' ? '24px' : '30px'}; }
  .pill .arrow.up { color: #d7dadc; }
  .pill .num { color: #d7dadc; }
  .save-row {
    display: flex; margin-left: auto; gap: 12px;
  }
</style></head><body>
  <div class="top">
    <div class="avatar">${p.avatarLetter}</div>
    <div>
      <div class="sub-line">
        <span>r/${p.sub}</span>
        <span class="dot">·</span>
        <span class="time">${p.time}</span>
      </div>
    </div>
    <div class="menu-dots">···</div>
  </div>
  <div class="user">${p.user}</div>
  <div class="title">${p.title}</div>
  <div class="body">${bodyLines}</div>
  <div class="actions">
    <div class="pill">
      <span class="arrow up">⬆</span>
      <span class="num">${p.up}</span>
      <span class="arrow">⬇</span>
    </div>
    <div class="pill">
      <span>💬</span>
      <span class="num">${p.comments}</span>
    </div>
    <div class="pill">
      <span>↗</span>
      <span>Share</span>
    </div>
  </div>
  ${repliesHTML}
</body></html>`;
}

// -------- Ad C: IG-story confessional (orange gradient) --------
const AD_C = {
  text: `ok i actually do my scalp
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
to quit`,
  text191: `ok i actually do my scalp
oil EVERY night now 😭

and it's because of this
one little dispenser tool`,
};

function storyHTML(ratio, p) {
  const [w, h] = SIZES[ratio];
  const sourceText = ratio === '191' ? p.text191 : p.text;
  const paragraphs = sourceText.split('\n\n').map(para => {
    const lines = para.split('\n').map(l => `<div>${l}</div>`).join('');
    return `<div class="para">${lines}</div>`;
  }).join('');

  const fontSize = ratio === '9x16' ? 62 : (ratio === '1x1' ? 54 : 56);
  const lineHeight = 1.28;
  const paraGap = ratio === '191' ? '14px' : '26px';

  return `<!doctype html>
<html><head><meta charset="utf-8"><style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width: ${w}px; height: ${h}px; overflow: hidden; }
  body {
    background: linear-gradient(135deg, #ffb347 0%, #ff7a3d 25%, #ff4e4e 55%, #e5366b 80%, #c6327a 100%);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, sans-serif;
    display: flex; align-items: center; justify-content: center;
    text-align: center;
    padding: ${ratio === '191' ? '40px 80px' : '60px 70px'};
  }
  .wrap {
    color: #ffffff;
    font-size: ${fontSize}px;
    font-weight: 600;
    line-height: ${lineHeight};
    letter-spacing: -0.3px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.08);
  }
  .para { margin-bottom: ${paraGap}; }
  .para:last-child { margin-bottom: 0; }
</style></head><body>
  <div class="wrap">${paragraphs}</div>
</body></html>`;
}

// -------- Render --------
(async () => {
  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  });

  const render = async (html, outPath, w, h) => {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    await page.setContent(html, { waitUntil: 'load' });
    await page.screenshot({ path: outPath, omitBackground: false });
    await page.close();
  };

  for (const ratio of Object.keys(SIZES)) {
    const [w, h] = SIZES[ratio];
    const bHTML = redditDarkHTML(ratio, AD_B);
    const cHTML = storyHTML(ratio, AD_C);
    const bOut = path.join(OUT_B, `AdB_Reddit-Dark__${ratio}.png`);
    const cOut = path.join(OUT_C, `AdC_Story-Confessional__${ratio}.png`);
    await render(bHTML, bOut, w, h);
    await render(cHTML, cOut, w, h);
    console.log(`✓ ${bOut}`);
    console.log(`✓ ${cOut}`);
  }

  await browser.close();
})();
