#!/usr/bin/env python3
"""V4 remake: single-shot urgency format with countdown banners. ~10s body + end card.
Usage: python3 build_v4.py <voice_wav> <out_name> [atempo]"""
import subprocess, sys, os, json
from PIL import Image, ImageDraw, ImageFont

ROOT = '/home/user/Kengokuhebun/ads/video'; CL = f'{ROOT}/clips'; TMP = f'{ROOT}/_tmp'; OUT = f'{ROOT}/final'
os.makedirs(TMP, exist_ok=True); os.makedirs(OUT, exist_ok=True)
vo_in, name = sys.argv[1], sys.argv[2]; tempo = float(sys.argv[3]) if len(sys.argv) > 3 else 1.5
W, H = 1080, 1920
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
NAVY, GLOW = (29, 35, 64), (255, 211, 110)
RED = (214, 40, 57)

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-1500:]); raise SystemExit('cmd failed')
    return r.stdout
def dur(p): return float(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{p}"').strip())

vo = f'{TMP}/{name}_vo.wav'
sh(f'ffmpeg -nostdin -loglevel error -y -i "{vo_in}" -af "atempo={tempo},loudnorm=I=-16:TP=-1.5" -ar 44100 {vo}')
L = dur(vo); body = L + 0.35
print('VO', round(L, 1), 's | body', round(body, 1), 's')

# single continuous shot: S5_dark (4s) + S7_hero (4s) concatenated then slowed to fill body
clips = ['S5_dark', 'S7_hero', 'S5_dark']
parts = []
for i, c in enumerate(clips):
    p = f'{TMP}/{name}_raw{i}.mp4'
    sh(f'ffmpeg -nostdin -loglevel error -y -i {CL}/r2_{c}.mp4 -an '
       f'-vf "scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,format=yuv420p" '
       f'-c:v libx264 -preset fast -crf 19 {p}')
    parts.append(p)
open(f'{TMP}/{name}_rawlist.txt', 'w').write('\n'.join(f"file '{p}'" for p in parts))
sh(f'ffmpeg -nostdin -loglevel error -y -f concat -safe 0 -i {TMP}/{name}_rawlist.txt -c copy {TMP}/{name}_rawcat.mp4')
raw_len = dur(f'{TMP}/{name}_rawcat.mp4')
slow = max(body / raw_len, 1.0)
sh(f'ffmpeg -nostdin -loglevel error -y -i {TMP}/{name}_rawcat.mp4 '
   f'-vf "setpts={slow}*PTS,tpad=stop_mode=clone:stop_duration=5,trim=duration={body},setpts=PTS-STARTPTS,fps=30,format=yuv420p" '
   f'-c:v libx264 -preset fast -crf 19 -an {TMP}/{name}_cut.mp4')

# overlays: red urgency banner (persistent) + yellow offer banner (persistent)
def ft(s): return ImageFont.truetype(FONT, s)
def pill(path, text, size, fg, bg, pad=34):
    f = ft(size); w = int(ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(text, font=f)) + pad * 2
    im = Image.new('RGBA', (w, size + pad), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, size + pad), radius=28, fill=bg); d.text((pad, pad // 2 - 4), text, font=f, fill=fg); im.save(path)

pill(f'{TMP}/v4_red.png', 'LAST CHANCE · ENDS CYBER MONDAY', 46, (255, 255, 255), (*RED, 235))
pill(f'{TMP}/v4_offer.png', 'BUY 2, GET 1 FREE + FREE TRACING BOOK', 38, NAVY, (*GLOW, 245))

# captions
sh(f'/root/.local/bin/whisper {vo} --model small.en --word_timestamps True --output_format json --output_dir {TMP} --language en')
j = json.load(open(f'{TMP}/{name}_vo.json')); words = [w for s in j['segments'] for w in s['words']]
HI = {'last', 'free', 'chance', 'friday', 'two', 'one', 'cyber', 'monday', 'deal', 'gone', 'prices'}
ass = ['[Script Info]', 'ScriptType: v4.00+', f'PlayResX: {W}', f'PlayResY: {H}', '[V4+ Styles]',
       'Format: Name,Fontname,Fontsize,PrimaryColour,OutlineColour,BackColour,Bold,Outline,Shadow,Alignment,MarginL,MarginR,MarginV',
       'Style: Default,DejaVu Sans,78,&H00FFFFFF,&H00301E10,&H00000000,1,6,2,2,60,60,390',
       '[Events]', 'Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text']
def t(x): return f'{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}'
i = 0
while i < len(words):
    ch = words[i:i + 3]; i += 3
    FIX = {'lead': 'led', 'lid': 'led'}
    for w in ch: w['word'] = FIX.get(w['word'].strip().lower().strip('.,!'), w['word'])
    txt = ' '.join(('{\\c&H6ED3FF&}' + w['word'].strip().upper() + '{\\c&HFFFFFF&}') if w['word'].strip().lower().strip('.,!') in HI else w['word'].strip().upper() for w in ch)
    ass.append(f'Dialogue: 0,{t(ch[0]["start"])},{t(ch[-1]["end"] + 0.05)},Default,,0,0,0,,{txt}')
open(f'{TMP}/{name}.ass', 'w').write('\n'.join(ass))

# end card
END = 2.6
img = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(img)
def center(y, s, size, fill):
    fo = ft(size); w = d.textlength(s, font=fo); d.text(((W - w) / 2, y), s, font=fo, fill=fill)
center(330, 'BLACK FRIDAY', 112, GLOW); center(500, 'BUY 2', 230, (255, 255, 255)); center(760, 'GET 1 FREE', 140, GLOW)
center(1000, '+ FREE Glow Tracing Book', 62, (255, 255, 255)); center(1085, '+ FREE shipping', 62, (255, 255, 255))
d.rounded_rectangle((90, 1260, W - 90, 1420), radius=40, fill=GLOW); center(1295, 'ENDS CYBER MONDAY', 62, NAVY)
d.rounded_rectangle((230, 1520, W - 230, 1680), radius=80, fill=(255, 255, 255)); center(1563, 'SHOP NOW', 84, NAVY)
center(1770, 'Only on our website', 46, (200, 205, 225)); img.save(f'{TMP}/end.png')
sh(f'ffmpeg -nostdin -loglevel error -y -loop 1 -i {TMP}/end.png -t {END} -vf "fps=30,format=yuv420p" -c:v libx264 -crf 19 {TMP}/{name}_end.mp4')

# compose: banners + captions + voice
sh(f'ffmpeg -nostdin -loglevel error -y -i {TMP}/{name}_cut.mp4 -i {vo} -i {TMP}/v4_red.png -i {TMP}/v4_offer.png '
   f'-filter_complex "[0:v][2:v]overlay=(W-w)/2:100[a];[a][3:v]overlay=(W-w)/2:H-h-800[b];[b]ass={TMP}/{name}.ass[v]" '
   f'-map "[v]" -map 1:a -c:v libx264 -preset fast -crf 19 -c:a aac -b:a 192k -af "apad" -t {body} {TMP}/{name}_body.mp4')
sh(f'ffmpeg -nostdin -loglevel error -y -i {TMP}/{name}_end.mp4 -f lavfi -i anullsrc=r=44100:cl=stereo -t {END} -c:v copy -c:a aac {TMP}/{name}_end_a.mp4')
final = f'{OUT}/{name}.mp4'
sh(f'ffmpeg -nostdin -loglevel error -y -i {TMP}/{name}_body.mp4 -i {TMP}/{name}_end_a.mp4 -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -preset fast -crf 19 -c:a aac {final}')
print('built', final, round(dur(final), 1), 's')
