#!/usr/bin/env python3
"""QC-fixed assembler for the V1-V5 remakes.
Fixes: native 24fps end to end (no 24->30 pulldown judder), no slow-mo stretching/frozen tails (each shot uses real
footage, least-reused window first, punch-in variation on repeats), caption overlap clamp, Reels/Stories safe zones,
audio true-peak limiter + stereo.
Usage: python3 build_fixed.py V1|V2|V3|V4|V5"""
import subprocess, sys, os, json, re
from PIL import Image, ImageDraw, ImageFont

ROOT = '/home/user/Kengokuhebun/ads/video'; CL = f'{ROOT}/clips'; TMP = f'{ROOT}/_tmp'; OUT = f'{ROOT}/final'
os.makedirs(TMP, exist_ok=True)
FPS = 24; W, H = 1080, 1920; CLIPF = 96
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
NAVY, GLOW, RED = (29, 35, 64), (255, 211, 110), (214, 40, 57)
SAFE_TOP = 280

CFG = {
 'V1': dict(src='build_v1.py', vo='audio/V1r_kitten2f.wav', tempo=1.5, top='The gift kids actually want',
            hi={'gift', 'free', 'light', 'reusable', 'friday', 'two', 'one', 'magic', 'christmas', 'cyber', 'monday', 'drawing', 'obsessed', 'creativity', 'imagination', 'hours', 'fast', 'gone'}),
 'V2': dict(src='build_v2.py', vo='audio/V2r_kitten2f.wav', tempo=1.3, top='The gift they will never forget',
            hi={'gift', 'free', 'light', 'reusable', 'friday', 'two', 'one', 'forget', 'love', 'cyber', 'monday', 'drawing', 'birthday'}),
 'V3': dict(src='build_v3.py', vo='audio/V3r_kitten2f.wav', tempo=1.5, top='The gift they will never forget',
            hi={'gift', 'free', 'light', 'reusable', 'friday', 'two', 'one', 'forget', 'love', 'cyber', 'monday', 'drawing', 'christmas', 'colorful', 'satisfying', 'patience', 'focus', 'wanted'}),
 'V4': dict(src=None, vo='audio/V4r_kitten2f.wav', tempo=1.5, top=None,
            hi={'last', 'free', 'chance', 'friday', 'two', 'one', 'cyber', 'monday', 'deal', 'gone', 'prices'}),
 'V5': dict(src='build_v5.py', vo='audio/V5r_kitten2f.wav', tempo=1.5, top='A gift that sparks creativity',
            hi={'gift', 'free', 'light', 'reusable', 'friday', 'two', 'one', 'forget', 'love', 'cyber', 'monday', 'drawing', 'birthday', 'creativity', 'sparks', 'creators', 'imagination', 'special'}),
}
v = sys.argv[1]; cfg = CFG[v]; name = f'{v}_fix'

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-1500:]); raise SystemExit('cmd failed: ' + c[:200])
    return r.stdout
def dur(p): return float(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{p}"').strip())

# ---- shot list (swipe cut structure -> clip names only; windows are chosen below)
if cfg['src']:
    s = open(f'{ROOT}/{cfg["src"]}').read()
    m = re.search(r'SHOTS\s*=\s*\[(.*?)\n\]', s, re.S)
    SHOTS = eval('[' + re.sub(r'#.*', '', m.group(1)) + ']')
    SW_LEN = float(re.search(r'SW_LEN\s*=\s*([0-9.]+)', s).group(1))
    slots = [(a, b, c) for a, b, c, _, _ in SHOTS]
else:
    SW_LEN = 14.4
    slots = [(0.0, 3.6, 'S5_dark'), (3.6, 7.2, 'S6_house'), (7.2, 10.8, 'S7_hero'), (10.8, 14.4, 'S5_dark')]

# ---- voice: tempo + loudness, then true-peak limit, fade tail, stereo
vo_raw = f'{TMP}/{name}_vo1.wav'; vo = f'{TMP}/{name}_vo.wav'
sh(f'ffmpeg -nostdin -loglevel error -y -i "{ROOT}/{cfg["vo"]}" -af "atempo={cfg["tempo"]},loudnorm=I=-17:TP=-2.5:LRA=7" -ar 44100 {vo_raw}')
L = dur(vo_raw)
sh(f'ffmpeg -nostdin -loglevel error -y -i {vo_raw} -af "alimiter=limit=0.80:attack=3:release=40,afade=t=out:st={L - 0.15:.3f}:d=0.15,pan=stereo|c0=c0|c1=c0" -ar 44100 {vo}')
body = L + 0.35
N = round(body * FPS)
print(v, 'VO', round(L, 2), 's | body', round(N / FPS, 2), 's =', N, 'frames')

# ---- frame-accurate shot allocation, least-reused real footage, punch-in on repeats
f = body / SW_LEN
edges = [round(b * f * FPS) for (_, b, _) in slots]; edges[-1] = N
used = {}; pieces = []; prev = 0
for (a, b, clip), e in zip(slots, edges):
    need = e - prev; prev = e
    n_pieces = 1 if need <= 78 else -(-need // 60)
    base, extra = divmod(need, n_pieces)
    for k in range(n_pieces):
        n = base + (1 if k < extra else 0)
        n = max(n, 3)
        cnt = used.setdefault(clip, [0] * CLIPF)
        best = None
        for sf in range(0, CLIPF - 1 - n + 1):
            cost = sum(cnt[sf:sf + n])
            if best is None or cost < best[0]: best = (cost, sf)
        sf = best[1]; kk = max(cnt[sf:sf + n])
        for i in range(sf, sf + n): cnt[i] += 1
        pieces.append((clip, sf, n, kk))

parts = []
ANCH = [0.5, 0.72, 0.28, 0.5]
for i, (clip, sf, n, kk) in enumerate(pieces):
    z = min(1.0 + 0.11 * kk, 1.36); sw = int(W * z) // 2 * 2; shh = int(H * z) // 2 * 2
    ax = int((sw - W) * ANCH[kk % 4]); ay = int((shh - H) * 0.45)
    p = f'{TMP}/{name}_s{i:03d}.mp4'
    sh(f'ffmpeg -nostdin -loglevel error -y -ss {sf / FPS:.4f} -i {CL}/r2_{clip}.mp4 -an -frames:v {n} '
       f'-vf "scale={sw}:{shh}:flags=lanczos,crop={W}:{H}:{ax}:{ay},fps={FPS},format=yuv420p" -c:v libx264 -preset fast -crf 17 -r {FPS} {p}')
    parts.append(p)
open(f'{TMP}/{name}_list.txt', 'w').write('\n'.join(f"file '{p}'" for p in parts))
sh(f'ffmpeg -nostdin -loglevel error -y -f concat -safe 0 -i {TMP}/{name}_list.txt -c copy {TMP}/{name}_cut.mp4')
print('shots', len(pieces), '| reused windows', sum(1 for p in pieces if p[3] > 0), '| cut', round(dur(f'{TMP}/{name}_cut.mp4'), 2), 's')

# ---- overlays
def ft(s): return ImageFont.truetype(FONT, s)
def pill(path, text, size, fg, bg, pad=34):
    fo = ft(size); w = int(ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(text, font=fo)) + pad * 2
    assert w <= W - 80, (text, w)
    im = Image.new('RGBA', (w, size + pad), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, size + pad), radius=28, fill=bg); d.text((pad, pad // 2 - 4), text, font=fo, fill=fg); im.save(path)
if cfg['top']: pill(f'{TMP}/{name}_top.png', cfg['top'], 54, (255, 255, 255), (29, 35, 64, 215))
else: pill(f'{TMP}/{name}_top.png', 'LAST CHANCE · ENDS CYBER MONDAY', 38, (255, 255, 255), (*RED, 235))
if v == 'V4': pill(f'{TMP}/{name}_o1.png', 'BUY 2, GET 1 FREE + FREE TRACING BOOK', 38, NAVY, (*GLOW, 245))
else:
    pill(f'{TMP}/{name}_o1.png', 'BLACK FRIDAY: BUY 2, GET 1 FREE', 46, NAVY, (*GLOW, 245))
    pill(f'{TMP}/{name}_o2.png', 'FREE TRACING BOOK · ENDS CYBER MONDAY', 32, (255, 255, 255), (*RED, 245))

# ---- captions (clamped so chunks never overlap)
sh(f'/root/.local/bin/whisper {vo} --model small.en --word_timestamps True --output_format json --output_dir {TMP} --language en')
words = [w for s_ in json.load(open(f'{TMP}/{name}_vo.json'))['segments'] for w in s_['words']]
FIX = {'lead': 'led', 'lid': 'led'}
chunks = [words[i:i + 3] for i in range(0, len(words), 3)]
ass = ['[Script Info]', 'ScriptType: v4.00+', f'PlayResX: {W}', f'PlayResY: {H}', '[V4+ Styles]',
       'Format: Name,Fontname,Fontsize,PrimaryColour,OutlineColour,BackColour,Bold,Outline,Shadow,Alignment,MarginL,MarginR,MarginV',
       'Style: Default,DejaVu Sans,72,&H00FFFFFF,&H00301E10,&H00000000,1,6,2,2,70,70,380',
       '[Events]', 'Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text']
def t(x): return f'{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}'
for ci, ch in enumerate(chunks):
    for w in ch: w['word'] = FIX.get(w['word'].strip().lower().strip('.,!?'), w['word'])
    st = ch[0]['start']; en = ch[-1]['end'] + 0.05
    if ci + 1 < len(chunks): en = min(en, chunks[ci + 1][0]['start'] - 0.01)
    en = max(en, st + 0.25)
    txt = ' '.join(('{\\c&H6ED3FF&}' + w['word'].strip().upper() + '{\\c&HFFFFFF&}') if w['word'].strip().lower().strip('.,!?') in cfg['hi'] else w['word'].strip().upper() for w in ch)
    ass.append(f'Dialogue: 0,{t(st)},{t(en)},Default,,0,0,0,,{txt}')
open(f'{TMP}/{name}.ass', 'w').write('\n'.join(ass))
t_off = 0.0 if v == 'V4' else next((w['start'] for k, w in enumerate(words) if w['word'].strip().lower().startswith('right') and k + 1 < len(words) and words[k + 1]['word'].strip().lower().startswith('now')), L * 0.6)
print('offer from', round(t_off, 1))

# ---- end card inside the Reels/Stories safe zone (content between y=280 and y=1560)
END = 2.6
img = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(img)
def center(y, s_, size, fill):
    fo = ft(size); w_ = d.textlength(s_, font=fo); d.text(((W - w_) / 2, y), s_, font=fo, fill=fill)
center(300, 'BLACK FRIDAY', 112, GLOW); center(440, 'BUY 2', 230, (255, 255, 255)); center(710, 'GET 1 FREE', 140, GLOW)
center(900, '+ FREE Glow Tracing Book', 62, (255, 255, 255)); center(985, '+ FREE shipping', 62, (255, 255, 255))
d.rounded_rectangle((90, 1090, W - 90, 1250), radius=40, fill=GLOW); center(1125, 'ENDS CYBER MONDAY', 62, NAVY)
d.rounded_rectangle((230, 1330, W - 230, 1490), radius=80, fill=(255, 255, 255)); center(1373, 'SHOP NOW', 84, NAVY)
center(1520, 'Only on our website', 44, (200, 205, 225)); img.save(f'{TMP}/{name}_end.png')
sh(f'ffmpeg -nostdin -loglevel error -y -loop 1 -i {TMP}/{name}_end.png -t {END} -vf "fps={FPS},format=yuv420p" -c:v libx264 -crf 17 -r {FPS} {TMP}/{name}_end.mp4')
sh(f'ffmpeg -nostdin -loglevel error -y -i {TMP}/{name}_end.mp4 -f lavfi -i anullsrc=r=44100:cl=stereo -t {END} -c:v copy -c:a aac -b:a 192k {TMP}/{name}_end_a.mp4')

# ---- compose body: banners (kept out of the top 280px and bottom 340px UI zones), captions, voice
P1, P2 = 1170, 1268
if v == 'V4':
    fc = (f'[0:v][2:v]overlay=(W-w)/2:{SAFE_TOP}[a];[a][3:v]overlay=(W-w)/2:{P1}[b];[b]ass={TMP}/{name}.ass[v]')
    ins = f'-i {TMP}/{name}_top.png -i {TMP}/{name}_o1.png'
else:
    fc = (f'[0:v][2:v]overlay=(W-w)/2:{SAFE_TOP}[a];[a][3:v]overlay=(W-w)/2:{P1}:enable=\'gte(t,{t_off})\'[b];'
          f'[b][4:v]overlay=(W-w)/2:{P2}:enable=\'gte(t,{t_off + 0.3})\'[c];[c]ass={TMP}/{name}.ass[v]')
    ins = f'-i {TMP}/{name}_top.png -i {TMP}/{name}_o1.png -i {TMP}/{name}_o2.png'
sh(f'ffmpeg -nostdin -loglevel error -y -i {TMP}/{name}_cut.mp4 -i {vo} {ins} -filter_complex "{fc}" '
   f'-map "[v]" -map 1:a -c:v libx264 -preset fast -crf 17 -r {FPS} -c:a aac -b:a 192k -ar 44100 -af apad -t {N / FPS:.4f} {TMP}/{name}_body.mp4')
final = f'{OUT}/{v}_remake_v2.mp4'
sh(f'ffmpeg -nostdin -loglevel error -y -i {TMP}/{name}_body.mp4 -i {TMP}/{name}_end_a.mp4 -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" '
   f'-map "[v]" -map "[a]" -c:v libx264 -preset fast -crf 17 -r {FPS} -c:a aac -b:a 192k -movflags +faststart {final}')
print('built', final, round(dur(final), 2), 's')
