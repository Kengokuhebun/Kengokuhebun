"""R12 assembly for the v3 sung ad (answer front-loaded, ~51s): cut the existing shots to the new song's word
timings, hook card held until the question is sung, karaoke captions, offer card, loudnorm, 720x1280 H.264.

Usage: WORK=/path/to/workdir python3 build-r12-assemble.py
WORK needs clips/ (R9b shots), clips2/ (R11 shots), song3/take0.mp3 and song3/take0_ts.json.
Song time = take 0 minus LEAD seconds (the take has a 2.3s lead-in before the first sung word).
"""
import json
import os
import re
import subprocess

WORK = os.environ.get("WORK", ".")
OUT = os.environ.get("OUT", f"{WORK}/ninu-3d-sung-ad-v3.mp4")
W, H, FPS = 720, 1280, 24
LEAD = 2.3

RAW = json.load(open(f"{WORK}/song3/take0_ts.json"))["data"]["data"]["alignedWords"]
WORDS = [dict(w=re.sub(r"\[.*?\]", "", x["word"]).strip(), s=x["startS"] - LEAD, e=x["endS"] - LEAD) for x in RAW]
WORDS = [x for x in WORDS if x["w"]]


def at(word, nth=1, before=0.0):
    """Start time of the nth occurrence of a sung word (exact text match), minus a small lead."""
    hits = [x for x in WORDS if x["w"] == word]
    return hits[nth - 1]["s"] - before


T_BECAUSE = at("Because,")
T_ITWASNT = [x for x in WORDS if x["w"] == "wasn't"][0]["s"] - 0.1   # the "It" before "wasn't"
T_DROPPER = [x for x in WORDS if x["w"] == "dropper."][0]["s"] - 0.45  # the "It was the" before "dropper."
T_SO = at("So")
T_PRESS = at("Press")
T_AND = [x for x in WORDS if x["w"] == "and"][0]["s"]
T_FIRST = at("first", 1, 0.25)       # "The" before "first"
T_FELT = at("felt", 1, 0.2)          # "I" before "felt"
T_NOT = at("Not")
T_NEENOO = at("Nee-noo", 1, 0.3)     # "The" before "Nee-noo"
T_MAKE = at("Make")
END = round(WORDS[-1]["e"] + 0.45, 2)
HOOK_END = round(T_BECAUSE - 0.15, 2)  # the question card stays until the question is sung

# (dir, file, start, end, source offset[, max source seconds])
CUT = [
    ("clips2", "H1.mp4", 0.0, T_BECAUSE, 0.0),           # hook question, held until it is sung
    ("clips2", "R2.mp4", T_BECAUSE, T_ITWASNT, 0.0),     # the answer: oil sits on the hair
    ("clips2", "P1.mp4", T_ITWASNT, T_DROPPER, 0.0),     # it wasn't you
    ("clips2", "P2.mp4", T_DROPPER, T_SO, 0.0),          # it was the dropper
    ("clips", "C1.mp4", T_SO, T_PRESS, 0.0),             # meet the one with hollow silicone tips
    ("clips", "D1.mp4", T_PRESS, T_AND, 0.0),            # press them to your scalp
    ("clips", "D2.mp4", T_AND, T_FIRST, 0.0),            # the oil releases right there
    ("clips", "E1.mp4", T_FIRST, T_FELT, 0.0),           # the first night, mama
    ("clips", "E2.mp4", T_FELT, T_NOT, 4.5),             # I felt it. Oh. (eyes open on the "Oh")
    ("clips2", "M1.mp4", T_NOT, T_NEENOO, 0.0, 4.7),     # hook callback
    ("clips2", "G2.mp4", T_NEENOO, T_MAKE - 0.45, 0.0),  # the kit, free shipping, guarantee
    ("clips", "F2.mp4", T_MAKE - 0.45, END, 7.5),        # make tonight the easy one
]


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
    out = []
    for x in WORDS:
        x = dict(x)
        x["w"] = x["w"].upper()
        if x["w"] == "NEE-NOO":
            x["w"] = "NINU"  # sung "Nee-noo", printed as the brand
        if x["w"] == "U.":
            x["w"] = "US"
        elif x["w"] == "S." and out and out[-1]["w"] == "US":
            out[-1]["e"] = x["e"]
            continue
        out.append(x)
    return [x for x in out if x["s"] >= HOOK_END - 0.1]


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
    ev = [f"Dialogue: 1,{ass_time(0)},{ass_time(HOOK_END)},Hook,,0,0,0,,WHY IS MY HAIR\\NOIL NOT DOING\\NANYTHING??"] + captions()
    card, card_end = T_NEENOO + 0.2, T_MAKE - 0.45
    ev.append(f"Dialogue: 2,{ass_time(card)},{ass_time(card_end)},Brand,,0,0,0,,{{\\fad(500,300)}}N I N U")
    ev.append(f"Dialogue: 2,{ass_time(card + 0.3)},{ass_time(card_end)},Offer,,0,0,0,,{{\\fad(500,300)}}The Ninu Kit  ·  $49.99\\NFree US shipping\\N30-day money-back guarantee")
    ev.append(f"Dialogue: 2,{ass_time(card + 0.6)},{ass_time(card_end)},Site,,0,0,0,,{{\\fad(500,300)}}tryninu.store")
    ev.append(f"Dialogue: 2,{ass_time(card_end)},{ass_time(END)},Tag,,0,0,0,,{{\\fad(400,0)}}N I N U  ·  tryninu.store")
    open(f"{WORK}/captions_v3.ass", "w", encoding="utf-8").write(head + "\n".join(ev) + "\n")


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
    inputs += ["-i", f"{WORK}/song3/take0.mp3"]
    n = len(CUT)
    fc = (";".join(filters) + ";" + "".join(labels) + f"concat=n={n}:v=1:a=0[cat];[cat]subtitles={WORK}/captions_v3.ass[vout];"
          f"[{n}:a]atrim=start={LEAD},asetpts=PTS-STARTPTS,loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
    cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", fc, "-map", "[vout]", "-map", "[aout]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
           "-t", f"{END}", "-movflags", "+faststart", OUT]
    subprocess.run(cmd, check=True)
    print("hook card until", HOOK_END, "| end", END, "| wrote", OUT, f"{os.path.getsize(OUT) / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
