#!/usr/bin/env python3
"""Assemble Glowling Black Friday videos (9:16, 1080x1920) from AI clips + ElevenLabs VO + captions + end card.
Usage: python3 build.py <A_gift|B_christmas|C_lastcall> [voice]"""
import subprocess, sys, os, json, re
from PIL import Image, ImageDraw, ImageFont

ROOT = '/home/user/Kengokuhebun/ads/video'
CL = f'{ROOT}/clips'; AU = f'{ROOT}/audio'; OUT = f'{ROOT}/final'; TMP = f'{ROOT}/_tmp'
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
name = sys.argv[1]; voice = sys.argv[2] if len(sys.argv) > 2 else 'Sarah'
W, H = 1080, 1920
NAVY, GLOW = (29, 35, 64), (255, 211, 110)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

# clip order per video (existing files in clips/)
PLAN = {
 'A_gift':      ['draw_white', 'kling_boy', 'night_glow', 'draw_white'],
 'B_christmas': ['kling_kitchen', 'draw_white', 'kling_boy', 'night_glow', 'draw_white'],
 'C_lastcall':  ['draw_white', 'night_glow'],
}
clips = [c for c in PLAN[name] if os.path.exists(f'{CL}/{c}.mp4')]

def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-1500:]); raise SystemExit('ffmpeg failed')
    return r.stdout

def dur(p): return float(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{p}"').strip())

vo = f'{AU}/{name}_{voice}.mp3'
vo_len = dur(vo)
END = 3.2                       # end card seconds
body_len = vo_len + 0.4         # body runs slightly past VO, then end card
seg = body_len / len(clips)

# 1) each body segment: square/16:9 clip centred over its own blurred, enlarged copy; muted; trimmed/slowed to fit
parts = []
for i, c in enumerate(clips):
    p = f'{TMP}/{name}_seg{i}.mp4'
    d = dur(f'{CL}/{c}.mp4')
    # slow the clip down if it is shorter than the segment (max 0.6x), else trim
    f = max(seg / d, 1.0) if seg > d else 1.0
    f = min(f, 1.7)
    sh(f'ffmpeg -nostdin -loglevel error -y -i "{CL}/{c}.mp4" -an -t {seg} '
       f'-filter_complex "[0:v]split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:5,eq=brightness=-0.08[bg];'
       f'[b]{"crop=iw:ih*0.80:0:ih*0.20," if c == "kling_kitchen" else ""}setpts={f}*PTS,scale={W}:-2:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-80,fps=30,format=yuv420p[v]" '
       f'-map "[v]" -t {seg} -c:v libx264 -preset fast -crf 20 "{p}"')
    parts.append(p)

# 2) end card (PIL)
img = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(img)
def ft(s): return ImageFont.truetype(FONT, s)
def center(y, text, size, fill):
    f = ft(size); w = d.textlength(text, font=f); d.text(((W - w) / 2, y), text, font=f, fill=fill)
center(300, 'BLACK FRIDAY', 120, GLOW)
center(470, 'BUY 2', 230, (255, 255, 255)); center(720, 'GET 1 FREE', 190, GLOW)
center(980, '+ FREE Glow Tracing Book', 64, (255, 255, 255))
center(1070, '+ FREE shipping', 64, (255, 255, 255))
d.rounded_rectangle((90, 1250, W - 90, 1420), radius=40, fill=GLOW)
center(1288, 'ENDS CYBER MONDAY', 78, NAVY)
d.rounded_rectangle((230, 1520, W - 230, 1680), radius=80, fill=(255, 255, 255))
center(1563, 'SHOP NOW', 84, NAVY)
center(1760, 'Only on our website', 46, (200, 205, 225))
img.save(f'{TMP}/endcard.png')
sh(f'ffmpeg -nostdin -loglevel error -y -loop 1 -i {TMP}/endcard.png -t {END} -vf "fps=30,format=yuv420p" -c:v libx264 -crf 20 {TMP}/{name}_end.mp4')

# 3) captions from Whisper word timings -> ASS, 3-4 word chunks
wj = f'{TMP}/{name}.json'
sh(f'/root/.local/bin/whisper "{vo}" --model small.en --word_timestamps True --output_format json --output_dir {TMP} --language en')
j = json.load(open(f'{TMP}/{name}_{voice}.json'))
words = [w for s in j['segments'] for w in s['words']]
ass = ['[Script Info]', 'ScriptType: v4.00+', f'PlayResX: {W}', f'PlayResY: {H}', '[V4+ Styles]',
       'Format: Name,Fontname,Fontsize,PrimaryColour,OutlineColour,BackColour,Bold,Outline,Shadow,Alignment,MarginL,MarginR,MarginV',
       'Style: Default,DejaVu Sans,78,&H00FFFFFF,&H00402318,&H00000000,1,6,2,2,60,60,330',
       '[Events]', 'Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text']
def t(x): h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60; return f'{h}:{m:02d}:{s:05.2f}'
i = 0
while i < len(words):
    chunk = words[i:i + 3]; i += 3
    txt = ' '.join(w['word'].strip() for w in chunk).upper()
    ass.append(f'Dialogue: 0,{t(chunk[0]["start"])},{t(chunk[-1]["end"] + 0.05)},Default,,0,0,0,,{txt}')
open(f'{TMP}/{name}.ass', 'w').write('\n'.join(ass))

# 4) concat body, burn captions, add VO; then append end card
open(f'{TMP}/{name}_list.txt', 'w').write('\n'.join(f"file '{p}'" for p in parts))
sh(f'ffmpeg -nostdin -loglevel error -y -f concat -safe 0 -i {TMP}/{name}_list.txt -i "{vo}" -vf "ass={TMP}/{name}.ass" '
   f'-map 0:v -map 1:a -c:v libx264 -preset fast -crf 20 -c:a aac -b:a 160k -shortest -af "apad=pad_dur=0.1" {TMP}/{name}_body.mp4')
open(f'{TMP}/{name}_list2.txt', 'w').write(f"file '{TMP}/{name}_body.mp4'\nfile '{TMP}/{name}_end.mp4'")
# end card has no audio: add silence so concat keeps audio stream
sh(f'ffmpeg -nostdin -loglevel error -y -i {TMP}/{name}_end.mp4 -f lavfi -i anullsrc=r=44100:cl=stereo -t {END} -c:v copy -c:a aac {TMP}/{name}_end_a.mp4')
sh(f'ffmpeg -nostdin -loglevel error -y -i {TMP}/{name}_body.mp4 -i {TMP}/{name}_end_a.mp4 '
   f'-filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -preset fast -crf 20 -c:a aac "{OUT}/Glowling_{name}_{voice}.mp4"')
print('built', f'{OUT}/Glowling_{name}_{voice}.mp4', round(dur(f"{OUT}/Glowling_{name}_{voice}.mp4"), 1), 's')
