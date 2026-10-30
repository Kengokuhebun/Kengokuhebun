"""R11 assembly for the v2 sung ad: cut shots to the new song's phrase boundaries, hook text card at frame 0,
karaoke captions from the sung word timestamps, end card, loudnorm, export 720x1280 H.264.

Usage: WORK=/path/to/workdir python3 build-r11-assemble.py
WORK needs clips/ (R9b shots), clips2/ (R11 shots), song2/take0.mp3 and song2/take0_ts.json.
Song time = take 0 minus LEAD seconds (the take has a 1.5s lead-in before the first sung word).
"""
import json
import os
import re
import subprocess

WORK = os.environ.get("WORK", ".")
OUT = os.environ.get("OUT", f"{WORK}/ninu-3d-sung-ad-v2.mp4")
W, H, FPS = 720, 1280, 24
LEAD = 1.5
END = 74.1
HOOK_END = 3.5  # the hook question is a static card until here; its words are left out of the karaoke captions

# (dir, file, start, end, source offset[, max source seconds]). Starts follow the song's phrase boundaries.
CUT = [
    ("clips2", "H1.mp4", 0.00, 3.40, 0.0),     # hook question: distress
    ("clips2", "H2.mp4", 3.40, 9.20, 0.0),     # "Hey mama, it's me." talking bottle (pattern interrupt)
    ("clips2", "BL1.mp4", 9.20, 10.70, 0.0),   # you blame the baby
    ("clips2", "BL2.mp4", 10.70, 12.60, 0.0),  # the shampoo
    ("clips2", "BL3.mp4", 12.60, 14.40, 0.0),  # yourself
    ("clips", "B1.mp4", 14.40, 17.40, 0.0),    # Sunday
    ("clips2", "R1.mp4", 17.40, 19.90, 0.0),   # nobody told you, mama
    ("clips2", "R2.mp4", 19.90, 22.00, 0.0),   # never reached your scalp
    ("clips2", "R3.mp4", 22.00, 26.20, 0.0),   # sat on your hair, soaked your towel
    ("clips2", "P1.mp4", 26.20, 29.90, 0.0),   # it wasn't you
    ("clips2", "P2.mp4", 29.90, 32.10, 0.0),   # it was the dropper
    ("clips2", "P3.mp4", 32.10, 34.35, 0.0),   # hair doesn't drink oil, skin does
    ("clips", "C1.mp4", 34.35, 37.30, 0.0),    # meet the one with hollow silicone tips
    ("clips", "D1.mp4", 37.30, 39.20, 0.0),    # press them to your scalp
    ("clips", "D2.mp4", 39.20, 41.30, 0.0),    # I release right there
    ("clips2", "D3c.mp4", 41.30, 43.20, 0.0),  # directly on the skin (retake, dispenser upright)
    ("clips", "E1.mp4", 43.20, 45.20, 0.0),    # the first night
    ("clips", "E2.mp4", 45.20, 53.00, 2.0),    # "oh" lands on the relief at about 2.5s into this cut
    ("clips2", "M1.mp4", 53.00, 58.40, 0.0, 4.7),   # hook callback: not doing anything? I was never getting there
    ("clips2", "K1.mp4", 58.40, 61.80, 0.0),   # Sunday can stay on the calendar
    ("clips2", "G2.mp4", 61.80, 68.80, 0.0),   # the kit, free shipping, guarantee
    ("clips", "F2.mp4", 68.80, 74.10, 7.5),    # make tonight the easy one
]
HOOK_TEXT = "WHY IS MY HAIR\\NOIL NOT DOING\\NANYTHING??"


def probe_dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


def seg_filter(i, path, d, ss, sl=None):
    g = min(probe_dur(path) - ss, sl or 1e9)
    f = f"[{i}:v]"
    if g > d + 0.04:
        f += f"trim={ss:.3f}:{ss + d:.3f},setpts=PTS-STARTPTS,"
    else:
        ratio = d / g
        f += f"trim={ss:.3f}:{ss + g:.3f},setpts={ratio:.4f}*(PTS-STARTPTS),"
        if ratio > 1.3:
            f += f"minterpolate=fps={FPS}:mi_mode=mci,"
    f += f"scale=-2:{H}:flags=lanczos,crop={W}:{H},fps={FPS},format=yuv420p,setsar=1[v{i}]"
    return f, g


def ass_time(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def words():
    raw = json.load(open(f"{WORK}/song2/take0_ts.json"))["data"]["data"]["alignedWords"]
    ws = [dict(w=re.sub(r"\[.*?\]", "", x["word"]).strip().upper(), s=x["startS"] - LEAD, e=x["endS"] - LEAD) for x in raw]
    ws = [x for x in ws if x["w"]]
    out = []
    for x in ws:
        if x["w"] == "NEE-NOO":
            x["w"] = "NINU"  # sung "Nee-noo", printed as the brand
        if x["w"] == "U." and out is not None:
            x["w"] = "US"
        elif x["w"] == "S." and out and out[-1]["w"] == "US":
            out[-1]["e"] = x["e"]
            continue
        out.append(x)
    return [x for x in out if x["s"] >= HOOK_END - 0.2]


def captions():
    chunks, cur = [], []
    for w in words():
        if cur and (len(cur) >= 3 or len(" ".join(x["w"] for x in cur + [w]).rstrip(".,:;")) > 16):
            chunks.append(cur); cur = []
        cur.append(w)
        if w["w"].endswith((".", ",", ":", "?", "!")):
            chunks.append(cur); cur = []
    if cur:
        chunks.append(cur)
    ev = []
    for i, ch in enumerate(chunks):
        s = max(ch[0]["s"], HOOK_END); e = ch[-1]["e"]
        if i + 1 < len(chunks) and chunks[i + 1][0]["s"] - e < 0.7:
            e = chunks[i + 1][0]["s"]
        else:
            e = min(e + 0.35, END)
        ev.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},Cap,,0,0,0,,{' '.join(x['w'] for x in ch).rstrip('.,:;')}")
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
Style: Hook,DejaVu Sans,66,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,8,0,2,40,40,230,1
Style: Brand,DejaVu Serif,74,&H00121824,&H00121824,&H00F5EFE6,&H00000000,-1,0,0,0,100,100,14,0,1,0,0,8,40,40,95,1
Style: Offer,DejaVu Sans,38,&H00121824,&H00121824,&H00F5EFE6,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,8,40,40,195,1
Style: Site,DejaVu Sans,34,&H0032729A,&H0032729A,&H00F5EFE6,&H00000000,-1,0,0,0,100,100,2,0,1,0,0,8,40,40,350,1
Style: Tag,DejaVu Sans,42,&H00E6EFF5,&H00E6EFF5,&H00121824,&H00000000,-1,0,0,0,100,100,4,0,1,5,0,2,40,40,120,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    ev = [f"Dialogue: 1,{ass_time(0)},{ass_time(HOOK_END)},Hook,,0,0,0,,{HOOK_TEXT}"] + captions()
    card, card_end = 64.5, 68.8  # offer card over the product scene only; a small brand tag carries the last shot
    ev.append(f"Dialogue: 2,{ass_time(card)},{ass_time(card_end)},Brand,,0,0,0,,{{\\fad(500,300)}}N I N U")
    ev.append(f"Dialogue: 2,{ass_time(card + 0.3)},{ass_time(card_end)},Offer,,0,0,0,,{{\\fad(500,300)}}The Ninu Kit  ·  $49.99\\NFree US shipping\\N30-day money-back guarantee")
    ev.append(f"Dialogue: 2,{ass_time(card + 0.6)},{ass_time(card_end)},Site,,0,0,0,,{{\\fad(500,300)}}tryninu.store")
    ev.append(f"Dialogue: 2,{ass_time(card_end)},{ass_time(END)},Tag,,0,0,0,,{{\\fad(400,0)}}N I N U  ·  tryninu.store")
    open(f"{WORK}/captions_v2.ass", "w", encoding="utf-8").write(head + "\n".join(ev) + "\n")


def main():
    ass()
    inputs, filters, labels = [], [], []
    for i, (d, src, a, b, ss, *sl) in enumerate(CUT):
        path = f"{WORK}/{d}/{src}"
        inputs += ["-i", path]
        f, g = seg_filter(i, path, b - a, ss, *sl)
        filters.append(f)
        labels.append(f"[v{i}]")
        print(f"{src:9s} avail {g:5.2f}s -> cut {b - a:5.2f}s ({a:.2f}-{b:.2f}){'  STRETCH x%.2f' % ((b - a) / g) if g < b - a else ''}")
    inputs += ["-i", f"{WORK}/song2/take0.mp3"]
    n = len(CUT)
    fc = (";".join(filters) + ";" + "".join(labels) + f"concat=n={n}:v=1:a=0[cat];[cat]subtitles={WORK}/captions_v2.ass[vout];"
          f"[{n}:a]atrim=start={LEAD},asetpts=PTS-STARTPTS,loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
    cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", fc, "-map", "[vout]", "-map", "[aout]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
           "-t", f"{END}", "-movflags", "+faststart", OUT]
    subprocess.run(cmd, check=True)
    print("wrote", OUT, f"{os.path.getsize(OUT) / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
