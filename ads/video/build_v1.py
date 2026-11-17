#!/usr/bin/env python3
"""Shot-for-shot remake of swipe V1 (23 cuts, ~47.6s): same beat order and pacing, our product, our offer.
Usage: python3 build_v1.py <voice_wav> <out_name> [atempo]"""
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

# V1 cut list from scene detection: 23 shots mapped to r2 clips
SHOTS = [
 (0.00, 1.07, 'S7_hero', 0.0, 1.1),    # hook: hero shot
 (1.07, 2.00, 'S1_unbox', 0.0, 0.9),    # hook cont: unboxing
 (2.00, 3.77, 'S1_unbox', 1.0, 2.8),    # "obsessed": unboxing
 (3.77, 6.00, 'S2_markers', 0.0, 2.2),  # product name: markers
 (6.00, 7.93, 'S3_flat', 0.0, 1.9),     # "sold out": flat lay
 (7.93, 10.23, 'S4_trace', 0.0, 2.3),   # "grab early": tracing
 (10.23, 12.83, 'S4_trace', 1.5, 4.0),  # "several": tracing cont
 (12.83, 14.73, 'S5_dark', 0.0, 1.9),   # "bright light": dark glow
 (14.73, 17.00, 'S5_dark', 1.5, 3.8),   # "colorful": glow cont
 (17.00, 18.67, 'S5_dark', 2.5, 4.0),   # "magic": glow
 (18.67, 20.70, 'S4_trace', 0.5, 2.5),  # "hours": drawing
 (20.70, 23.03, 'S6_house', 0.0, 2.3),  # "iPad": living room
 (23.03, 24.53, 'S4_trace', 2.0, 3.5),  # "patience": focus
 (24.53, 26.93, 'S5_dark', 0.5, 2.9),   # "creativity": glow
 (26.93, 29.00, 'S4_trace', 0.0, 2.1),  # "pen control": tracing
 (29.00, 31.97, 'S5_dark', 1.0, 4.0),   # "night light": dark glow
 (31.97, 34.17, 'S3_flat', 0.0, 2.2),   # "wipe clean": flat
 (34.17, 35.23, 'S2_markers', 1.0, 2.1),# "reusable": fresh markers
 (35.23, 39.57, 'S7_hero', 0.5, 4.0),   # "Black Friday": hero
 (39.57, 40.97, 'S1_unbox', 2.0, 3.4),  # "buy two": multiple
 (40.97, 42.67, 'S6_house', 1.5, 3.2),  # "Cyber Monday": house
 (42.67, 44.77, 'S7_hero', 1.0, 3.1),   # "selling fast": hero
 (44.77, 47.60, 'S7_hero', 2.5, 4.0),   # "tap below": hero close
]
SW_LEN = 47.60

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
pill(f'{TMP}/top.png', 'The gift kids actually want', 54, (255, 255, 255), (29, 35, 64, 215))
pill(f'{TMP}/offer1.png', 'BLACK FRIDAY: BUY 2, GET 1 FREE', 52, (29, 35, 64), (255, 211, 110, 245))
pill(f'{TMP}/offer2.png', 'FREE TRACING BOOK · ENDS CYBER MONDAY', 34, (255, 255, 255), (214, 40, 57, 245))

sh(f'/root/.local/bin/whisper {vo} --model small.en --word_timestamps True --output_format json --output_dir {TMP} --language en')
j = json.load(open(f'{TMP}/{name}_vo.json')); words = [w for s in j['segments'] for w in s['words']]
HI = {'gift', 'free', 'light', 'reusable', 'friday', 'two', 'one', 'magic', 'christmas', 'cyber', 'monday', 'drawing', 'obsessed', 'creativity', 'imagination', 'hours', 'fast', 'gone'}
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
t_off = next((w['start'] for k, w in enumerate(words) if w['word'].strip().lower().startswith('right') and k + 1 < len(words) and words[k + 1]['word'].strip().lower().startswith('now')), L * 0.70)
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
