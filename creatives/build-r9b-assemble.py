"""R9b assembly: cut the generated shots to the song's phrase boundaries, burn karaoke-style
captions from the sung word timestamps, add the end card, mix the song, export 720x1280 H.264.

Usage: WORK=/path/to/workdir python3 build-r9b-assemble.py
WORK needs clips/*.mp4, song/track.mp3 and song/ts.json (kie.ai timestamped lyrics response).
"""
import json
import os
import re
import subprocess

WORK = os.environ.get("WORK", ".")
C = f"{WORK}/clips"
OUT = os.environ.get("OUT", f"{WORK}/ninu-3d-sung-ad.mp4")
W, H, FPS = 720, 1280, 24

# (file, start, end) in the final cut. Starts follow the song's phrase boundaries.
CUT = [
    ("test_s1_mini.mp4", 0.00, 8.22),    # hook, present
    ("test_s2_480.mp4", 8.22, 13.31),    # six months ago, past
    ("B1.mp4", 13.31, 18.16),
    ("B2.mp4", 18.16, 26.76),
    ("C1.mp4", 26.76, 32.76),
    ("D1.mp4", 32.76, 36.38),
    ("D2.mp4", 36.38, 40.23),
    ("D3.mp4", 40.23, 45.42),
    ("E1.mp4", 45.42, 49.52),
    ("E2.mp4", 49.52, 59.75),
    ("F1.mp4", 59.75, 64.62),
    ("F2.mp4", 64.62, 77.64),
    ("G1.mp4", 77.64, 85.00),
]


def probe_dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


def seg_filter(i, src, d):
    g = probe_dur(f"{C}/{src}")
    f = f"[{i}:v]"
    if g > d + 0.04:
        f += f"trim=0:{d:.3f},setpts=PTS-STARTPTS,"
    else:
        ratio = d / g
        f += f"setpts={ratio:.4f}*PTS,"
        if ratio > 1.3:
            f += f"minterpolate=fps={FPS}:mi_mode=mci,"
    f += f"scale=-2:{H}:flags=lanczos,crop={W}:{H},fps={FPS},format=yuv420p,setsar=1[v{i}]"
    return f, g


def ass_time(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def captions():
    words = json.load(open(f"{WORK}/song/ts.json"))["data"]["data"]["alignedWords"]
    words = [dict(w=re.sub(r"\[.*?\]", "", w["word"]).strip().upper(), s=w["startS"], e=w["endS"]) for w in words]
    words = [w for w in words if w["w"]]
    chunks, cur = [], []
    for w in words:
        if cur and (len(cur) >= 3 or len(" ".join(x["w"] for x in cur + [w]).rstrip(".,:;")) > 16):
            chunks.append(cur); cur = []
        cur.append(w)
        if w["w"].endswith((".", ",", ":", "?", "!")):
            chunks.append(cur); cur = []
    if cur:
        chunks.append(cur)
    ev = []
    for i, ch in enumerate(chunks):
        s = ch[0]["s"]; e = ch[-1]["e"]
        if i + 1 < len(chunks) and chunks[i + 1][0]["s"] - e < 0.7:
            e = chunks[i + 1][0]["s"]
        else:
            e = min(e + 0.35, 80.4)
        text = " ".join(x["w"] for x in ch).rstrip(".,:;")
        ev.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},Cap,,0,0,0,,{text}")
    return ev


def ass():
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,DejaVu Sans,60,&H001FD2FF,&H001FD2FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,6,0,2,40,40,420,1
Style: Brand,DejaVu Serif,74,&H00121824,&H00121824,&H00F5EFE6,&H00000000,-1,0,0,0,100,100,14,0,1,0,0,8,40,40,95,1
Style: Offer,DejaVu Sans,38,&H00121824,&H00121824,&H00F5EFE6,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,8,40,40,195,1
Style: Site,DejaVu Sans,34,&H0032729A,&H0032729A,&H00F5EFE6,&H00000000,-1,0,0,0,100,100,2,0,1,0,0,8,40,40,350,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    ev = captions()
    card = 77.9
    ev.append(f"Dialogue: 1,{ass_time(card)},{ass_time(85)},Brand,,0,0,0,,{{\\fad(500,0)}}N I N U")
    ev.append(f"Dialogue: 1,{ass_time(card + 0.3)},{ass_time(85)},Offer,,0,0,0,,{{\\fad(500,0)}}The Ninu Kit  ·  $49.99\\NFree US shipping\\N30-day money-back guarantee")
    ev.append(f"Dialogue: 1,{ass_time(card + 0.6)},{ass_time(85)},Site,,0,0,0,,{{\\fad(500,0)}}tryninu.store")
    open(f"{WORK}/captions.ass", "w", encoding="utf-8").write(head + "\n".join(ev) + "\n")


def main():
    ass()
    inputs, filters, labels = [], [], []
    for i, (src, a, b) in enumerate(CUT):
        inputs += ["-i", f"{C}/{src}"]
        f, g = seg_filter(i, src, b - a)
        filters.append(f)
        labels.append(f"[v{i}]")
        print(f"{src:18s} gen {g:5.2f}s -> cut {b - a:5.2f}s ({a:.2f}-{b:.2f})")
    inputs += ["-i", f"{WORK}/song/track.mp3"]
    n = len(CUT)
    fc = ";".join(filters) + ";" + "".join(labels) + f"concat=n={n}:v=1:a=0[cat];[cat]subtitles={WORK}/captions.ass[vout];[{n}:a]loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
    cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", fc, "-map", "[vout]", "-map", "[aout]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
           "-t", "85.0", "-movflags", "+faststart", OUT]
    subprocess.run(cmd, check=True)
    print("wrote", OUT, f"{os.path.getsize(OUT) / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
