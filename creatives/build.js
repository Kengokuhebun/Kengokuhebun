// Generates HTML for Reddit + confessional creatives at 1:1, 9:16, 1.91:1, then renders PNGs.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const SIZES = { '1x1': [1080,1080], '9x16': [1080,1920], '191': [1080,565] };
const FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif";

const C3=[['u/pumpandpray','#d97706','24','same. thought it was just me'],['u/fourthtrimestergirl','#2563eb','19','saving this thread, thank you all'],['u/quietly_shedding','#e5533d','33','the hair tie count on my wrist says it all'],['u/kinkycurlyandtired','#8a4fff','27','the way i cackled at troll doll'],['u/lurker_turned_poster','#46a758','41','ok going to try this and report back']];
const reddit = [
 { key:'r1-ritual-upgrade', sub:'HaircareScience', color:'#0079d3', user:'u/oilyroots_nightly', time:'6h',
   title:'does anyone else feel like they\'re wasting half their scalp oil??', up:'340', com:'89',
   body:'i do my oiling ritual every night and lately i swear more of it ends up on my towel and pillowcase than on my scalp. am i just doing it wrong or is this normal',
   c1:['u/bunmom_of_2','#e5533d','62','omg yes, half of it just runs down my neck every time.'],
   c2:['u/tealwaterfall','#46a758','31','i part in like 30 sections and still feel like it\'s not reaching my scalp'] },
 { key:'r2-temple-rescue', sub:'beyondthebump', color:'#e5533d', user:'u/sleepdeprived_mama', time:'9h',
   title:'Is this normal?? (pic)', up:'512', com:'140',
   body:'5 months pp and my temples look like this now. i keep pulling my hair back and then immediately regretting it. is this just shedding or is it not coming back',
   c1:['u/thirdtrimestertired','#8a4fff','88','this happened to me too, it does grow back, hang in there ❤️'],
   c2:['u/nap_trap_nora','#0aa5a5','47','7 months in and mine is finally filling in. the baby hairs are a whole other story lol'] },
 { key:'r3-not-a-pill', sub:'HairLoss', color:'#7a3e9d', user:'u/done_with_supplements', time:'11h',
   title:'Genuinely so tired of being told to just take more biotin.', up:'890', com:'210',
   body:'biotin, prenatals, collagen, iron, the gummies, the shampoo. i\'ve tried all of it. every answer is "take more of X" and my hair is still coming out in the shower',
   c1:['u/labs_came_back_fine','#d97706','145','literally, my doctor just keeps telling me the same thing.'],
   c2:['u/shedding_season','#2563eb','73','the biotin aisle is a scam at this point, i\'ve got a whole drawer of it'] },
 { key:'r4-regrowth-companion', sub:'Naturalhair', color:'#b45309', user:'u/coilsandcoffee', time:'4h',
   title:'Anyone else\'s regrowth look like a Troll doll?? 😭', up:'670', com:'155',
   body:'the shedding finally slowed down but now my whole hairline is these little baby hairs standing straight up. edges, gel, brush, nothing lays them down',
   c1:['u/twist_out_tuesday','#e5533d','91','omg the struggle, mine won\'t lay down no matter what 😩'],
   c2:['u/edges_and_prayers','#46a758','58','at least they\'re growing?? i keep telling myself that lol'] },
 { key:'r5-root-cause', sub:'HaircareScience', color:'#0079d3', user:'u/curious_about_follicles', time:'2h',
   title:'TIL scalp buildup might be why my oiling wasn\'t working.', up:'1.2k', com:'340',
   body:'apparently oil just sits on top of product and sebum buildup instead of getting to the scalp. i\'ve been oiling for a year over a layer of gunk',
   c1:['u/wait_what_now','#8a4fff','210','wait this actually explains so much'],
   c2:['u/scalp_science_nerd','#0aa5a5','96','yep, this is why people exfoliate first. oil on a clogged scalp mostly just sits there'] },
];

function redditHTML(p, ratio){
  const [w,h] = SIZES[ratio];
  const avatar = c => `<span class="av" style="background:${c}"></span>`;
  const comment = (c) => `<div class="cmt"><div class="cm"><span class="av sm" style="background:${c[1]}"></span><b>${c[0]}</b><span class="g">· ${c[2]} upvotes</span></div><div class="ct">${c[3]}</div></div>`;
  const header = `<div class="hdr"><span class="back">‹</span><span class="sic" style="background:${p.color}">r/</span><b>r/${p.sub}</b><span class="join">Join</span></div>`;
  const status = `<div class="status"><span>9:41</span><span>●●● 5G ▮</span></div>`;
  const meta = `<div class="meta"><span class="sic s" style="background:${p.color}">r/</span><b>r/${p.sub}</b><span class="g">· ${p.user} · ${p.time}</span></div>`;
  const eng = `<div class="eng"><span>⬆ <b>${p.up}</b> ⬇</span><span>💬 <b>${p.com}</b></span><span>↗ Share</span></div>`;
  let content, extraCss='';
  if(ratio==='1x1'){
    content = `${header}<div class="post">${meta}<div class="title">${p.title}</div><div class="bodyt">${p.body}</div>${eng}${comment(p.c1)}${comment(p.c2)}</div>`;
  } else if(ratio==='9x16'){ extraCss='.post{zoom:1.3}';
    content = `${status}${header}<div class="post">${meta}<div class="title">${p.title}</div><div class="bodyt">${p.body}</div>${eng}${comment(p.c1)}${comment(p.c2)}${comment(C3[reddit.indexOf(p)])}<div class="more">View all ${p.com} comments</div></div><div class="nav"><span>⌂</span><span>◎</span><span>＋</span><span>💬</span><span>🔔</span></div>`;
  } else {
    content = `<div class="post wide">${meta}<div class="title">${p.title}</div>${eng}${comment(p.c1)}</div>`;
    extraCss = '.title{font-size:54px}.post.wide{padding:40px 50px;justify-content:center}';
  }
  return `<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0}body{width:${w}px;height:${h}px;background:#fff;font-family:${FONT};color:#1c1c1c;display:flex;flex-direction:column;overflow:hidden}
.status{height:60px;background:#fff;display:flex;justify-content:space-between;align-items:center;padding:0 44px;font-weight:600;font-size:26px}
.hdr{height:96px;display:flex;align-items:center;gap:18px;padding:0 36px;border-bottom:1px solid #e6e6e6;font-size:32px}
.back{font-size:56px;color:#555;margin-right:4px}.sic{width:54px;height:54px;border-radius:50%;color:#fff;font-weight:700;font-size:24px;display:flex;align-items:center;justify-content:center}
.sic.s{width:36px;height:36px;font-size:15px}.join{margin-left:auto;background:#0b0b0b;color:#fff;border-radius:30px;padding:10px 32px;font-weight:600;font-size:28px}
.post{flex:1;padding:36px 44px;display:flex;flex-direction:column;justify-content:flex-start}
.meta{display:flex;align-items:center;gap:12px;font-size:26px;margin-bottom:22px}.g{color:#7c7c7c}
.title{font-size:48px;font-weight:700;line-height:1.18;margin-bottom:24px}
.bodyt{font-size:33px;line-height:1.4;color:#333;margin-bottom:28px}
.eng{display:flex;gap:44px;font-size:30px;padding:20px 0;border-top:1px solid #e6e6e6;border-bottom:1px solid #e6e6e6;margin-bottom:26px;color:#444}
.cmt{background:#f7f8f9;border-radius:18px;padding:24px 28px;margin-bottom:18px}
.cm{display:flex;align-items:center;gap:12px;font-size:26px;margin-bottom:10px}.av.sm{width:38px;height:38px;border-radius:50%;display:inline-block}
.ct{font-size:32px;line-height:1.35}.more{color:#0079d3;font-size:28px;font-weight:600;padding:8px 4px}
.nav{height:120px;border-top:1px solid #e6e6e6;display:flex;justify-content:space-around;align-items:center;font-size:44px;color:#555;margin-top:auto}
${extraCss}</style></head><body>${content}</body></html>`;
}

const confess = [
 { key:'c1-ritual-upgrade', g:['#ff9a3c','#ff3d6e'], text:"not me realizing half my scalp oil has been ending up on my towel this whole time 💀 like i've been doing this ritual every night for MONTHS thinking it was working... turns out my fingers just weren't getting it where it needed to go. wish someone had told me sooner" },
 { key:'c2-temple-rescue', g:['#ffb347','#e8437a'], text:"ok so i just found out my hairline thinning is apparently the #1 most obsessed-over postpartum thing and no one talks about it 😭 staring in every mirror i pass like is it filling back in or am i imagining it" },
 { key:'c3-not-a-pill', g:['#ffcc33','#ff6a3d'], text:"the amount of money i've spent on biotin + prenatals + collagen powder trying to fix my postpartum hair 💸 pls someone explain why nobody mentioned the actual thing that would've helped first" },
 { key:'c4-regrowth-companion', g:['#ff8a5c','#c2337a'], text:"the regrowth phase really said 'here's some baby hairs that will NEVER lay flat' 😭 nobody warns you the shedding stopping doesn't mean it's over, it just gets weird in a whole new way" },
 { key:'c5-root-cause', g:['#ffa62b','#d6336c'], text:"wait so scalp buildup can literally block your follicles and nobody mentioned this once in like 8 months of postpartum hair loss research?? 🙃 feel like i wasted so much time" },
];
function confessHTML(p, ratio){
  const [w,h]=SIZES[ratio];
  const len = p.text.length;
  const fs = ratio==='9x16' ? Math.round(Math.min(86, 5200/Math.sqrt(len)*0.62)) : ratio==='1x1' ? Math.round(Math.min(72, 4300/Math.sqrt(len)*0.58)) : Math.round(Math.min(48, 3300/Math.sqrt(len)*0.42));
  const pad = ratio==='191' ? 40 : 80;
  return `<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0}body{width:${w}px;height:${h}px;overflow:hidden;font-family:${FONT};background:linear-gradient(155deg,${p.g[0]},${p.g[1]});display:flex;align-items:center;justify-content:center;padding:${pad}px}
.t{color:#fff;font-weight:900;font-size:${fs}px;line-height:1.16;text-align:center;letter-spacing:-.5px;-webkit-text-stroke:${Math.round(fs/9)}px #000;paint-order:stroke fill;text-shadow:0 4px 0 rgba(0,0,0,.25)}
</style></head><body><div class="t">${p.text}</div></body></html>`;
}

(async()=>{
  fs.mkdirSync('html',{recursive:true});
  const jobs=[];
  for(const [set,list,fn] of [['reddit',reddit,redditHTML],['confessional',confess,confessHTML]])
    for(const p of list) for(const r of Object.keys(SIZES)){
      const name=`${set}-${p.key}-${r}`; fs.writeFileSync(`html/${name}.html`, fn(p,r)); jobs.push([name,...SIZES[r]]);
    }
  fs.mkdirSync('png',{recursive:true});
  const ANG={'ritual-upgrade':'Angle1_Ritual-Upgrade','temple-rescue':'Angle2_Temple-Rescue','not-a-pill':'Angle3_Not-A-Pill','regrowth-companion':'Angle4_Regrowth-Companion','root-cause':'Angle5_Root-Cause'};
  const RAT={'1x1':'1x1-square','9x16':'9x16-story','191':'1.91x1-landscape'};
  const pngPath=n=>{const m=n.match(/^(reddit|confessional)-[rc]\d-(.+)-(1x1|9x16|191)$/);const d='png/'+ANG[m[2]];fs.mkdirSync(d,{recursive:true});return `${d}/${ANG[m[2]]}__${m[1]==='reddit'?'Reddit-Post':'Confessional-Text'}__${RAT[m[3]]}.png`;};
  const b=await chromium.launch();
  for(const [n,w,h] of jobs){
    const pg=await b.newPage({viewport:{width:w,height:h}});
    await pg.goto('file://'+path.resolve(`html/${n}.html`));
    await pg.screenshot({path:pngPath(n)});
    // overflow check
    const ov=await pg.evaluate(()=>document.documentElement.scrollHeight>innerHeight+1||document.documentElement.scrollWidth>innerWidth+1);
    console.log(n,w+'x'+h,ov?'OVERFLOW':'ok'); await pg.close();
  }
  await b.close();
})();
