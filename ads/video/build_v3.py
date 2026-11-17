#!/usr/bin/env python3
"""Shot-for-shot remake of swipe V3 (17 cuts, ~35.5s): long opening demo then rapid offer cuts.
Usage: python3 build_v3.py <voice_wav> <out_name> [atempo]"""
import subprocess, sys, os, json
from PIL import Image, ImageDraw, ImageFont

ROOT = '/home/user/Kengokuhebun/ads/video'; CL = f'{ROOT}/clips'; TMP = f'{ROOT}/_tmp'; OUT = f'{ROOT}/final'
os.makedirs(TMP, exist_ok=True); os.makedirs(OUT, exist_ok=True)
vo_in, name = sys.argv[1], sys.argv[2]; tempo = float(sys.argv[3]) if len(sys.argv) > 3 else 1.5
W, H = 1080, 1920
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
NAVY, GLOW = (29, 35, 64), (255, 211, 110)

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-1500:]); raise SystemExit('cmd failed')
    return r.stdout
def dur(p): return float(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{p}"').strip())

# V3 structure: 2 quick cuts, then one LONG ~18s demo take, then rapid cuts for offer section
# The long take uses multiple clips cross-dissolved; the rapid section matches V3's cuts
SHOTS = [
 (0.00, 0.70, 'S7_hero', 0.0, 0.7),      # flash hook
 (0.70, 1.43, 'S1_unbox', 0.0, 0.7),      # unbox flash
 # long demo section: 1.43-19.33 (~18s) - break into sub-shots from our clips
 (1.43, 5.43, 'S4_trace', 0.0, 4.0),      # tracing demo
 (5.43, 9.43, 'S5_dark', 0.0, 4.0),       # dark glow demo
 (9.43, 13.43, 'S4_trace', 0.0, 4.0),     # more tracing
 (13.43, 17.43, 'S6_house', 0.0, 4.0),    # house/living room
 (17.43, 19.33, 'S5_dark', 2.0, 3.9),     # dark glow close
 # rapid section from 19.33
 (19.33, 20.17, 'S2_markers', 0.0, 0.8),  # markers flash
 (20.17, 22.23, 'S3_flat', 0.0, 2.1),     # flat lay
 (22.23, 23.03, 'S7_hero', 0.5, 1.3),     # hero
 (23.03, 23.90, 'S1_unbox', 1.5, 2.4),    # unbox
 (23.90, 24.87, 'S5_dark', 0.5, 1.5),     # dark
 (24.87, 26.47, 'S4_trace', 1.0, 2.6),    # trace
 (26.47, 27.47, 'S2_markers', 1.0, 2.0),  # markers
 (27.47, 28.93, 'S6_house', 2.0, 3.5),    # house
 (28.93, 31.90, 'S7_hero', 0.5, 3.4),     # hero
 (31.90, 34.57, 'S5_dark', 0.0, 2.7),     # dark glow
 (34.57, 35.50, 'S7_hero', 3.0, 4.0),     # hero close
]
SW_LEN = 35.50

vo = f'{TMP}/{name}_vo.wav'
sh(f'ffmpeg -nostdin -loglevel error -y -i "{vo_in}" -af "atempo={tempo},loudnorm=I=-16:TP=-1.5" -ar 44100 {vo}')
L = dur(vo); body = L + 0.35; f = body / SW_LEN
print('VO', round(L, 1), 's | scale', round(f, 2))

parts = []
for i, (a, b, clip, si, so) in enumerate(SHOTS):
    need = (b - a) * f; have = max(so - si, 0.2)
    ratio = max(need / have, 1.0)
    p = f'{TMP}/{name}_s{i:02d}.mp4'
    sh(f'ffmpeg -nostdin -loglevel error -y -ss {si} -t {have} -i {CL}/r2_{clip}.mp4 -an '
       f'-vf "setpts={ratio}*PTS,tpad=stop_mode=clone:stop_duration=3,trim=duration={need},setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,format=yuv420p" '
       f'-c:v libx264 -preset fast -crf 19 {p}')
    parts.append(p)
open(f'{TMP}/{name}_list.txt', 'w').write('\n'.join(f"file '{p}'" for p in parts))
sh(f'ffmpeg -nostdin -loglevel error -y -f concat -safe 0 -i {TMP}/{name}_list.txt -c copy {TMP}/{name}_cut.mp4')

def ft(s): return ImageFont.truetype(FONT, s)
def pill(path, text, size, fg, bg, pad=34):
    f = ft(size); w = int(ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(text, font=f)) + pad * 2
    im = Image.new('RGBA', (w, size + pad), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, size + pad), radius=28, fill=bg); d.text((pad, pad // 2 - 4), text, font=f, fill=fg); im.save(path)
pill(f'{TMP}/top.png', 'The gift they will never forget', 54, (255, 255, 255), (29, 35, 64, 215))
pill(f'{TMP}/offer1.png', 'BLACK FRIDAY: BUY 2, GET 1 FREE', 52, (29, 35, 64), (255, 211, 110, 245))
pill(f'{TMP}/offer2.png', 'FREE TRACING BOOK · ENDS CYBER MONDAY', 34, (255, 255, 255), (214, 40, 57, 245))

sh(f'/root/.local/bin/whisper {vo} --model small.en --word_timestamps True --output_format json --output_dir {TMP} --language en')
j = json.load(open(f'{TMP}/{name}_vo.json')); words = [w for s in j['segments'] for w in s['words']]
HI = {'gift', 'free', 'light', 'reusable', 'friday', 'two', 'one', 'forget', 'love', 'cyber', 'monday', 'drawing', 'christmas', 'colorful', 'satisfying', 'patience', 'focus', 'wanted'}
ass = ['[Script Info]', 'ScriptType: v4.00+', f'PlayResX: {W}', f'PlayResY: {H}', '[V4+ Styles]',
       'Format: Name,Fontname,Fontsize,PrimaryColour,OutlineColour,BackColour,Bold,Outline,Shadow,Alignment,MarginL,MarginR,MarginV',
       'Style: Default,DejaVu Sans,74,&H00FFFFFF,&H00301E10,&H00000000,1,6,2,2,60,60,390',
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
t_off = next((w['start'] for k, w in enumerate(words) if w['word'].strip().lower().startswith('right') and k + 1 < len(words) and words[k + 1]['word'].strip().lower().startswith('now')), L * 0.60)
print('offer banner from', round(t_off, 1))

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

sh(f'ffmpeg -nostdin -loglevel error -y -i {TMP}/{name}_cut.mp4 -i {vo} -i {TMP}/top.png -i {TMP}/offer1.png -i {TMP}/offer2.png '
   f'-filter_complex "[0:v][2:v]overlay=(W-w)/2:120[a];[a][3:v]overlay=(W-w)/2:H-h-800:enable=\'gte(t,{t_off})\'[b];[b][4:v]overlay=(W-w)/2:H-h-705:enable=\'gte(t,{t_off + 0.3})\'[c];[c]ass={TMP}/{name}.ass[v]" '
   f'-map "[v]" -map 1:a -c:v libx264 -preset fast -crf 19 -c:a aac -b:a 192k -af "apad" -t {body} {TMP}/{name}_body.mp4')
sh(f'ffmpeg -nostdin -loglevel error -y -i {TMP}/{name}_end.mp4 -f lavfi -i anullsrc=r=44100:cl=stereo -t {END} -c:v copy -c:a aac {TMP}/{name}_end_a.mp4')
final = f'{OUT}/{name}.mp4'
sh(f'ffmpeg -nostdin -loglevel error -y -i {TMP}/{name}_body.mp4 -i {TMP}/{name}_end_a.mp4 -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -preset fast -crf 19 -c:a aac {final}')
print('built', final, round(dur(final), 1), 's')
