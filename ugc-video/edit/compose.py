"""Assemble one Ninu green-screen UGC ad.  usage: python compose.py H1|H2|H3 [preview_seconds]"""
import json, re, subprocess, sys, difflib
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

HOOK = sys.argv[1]
PREVIEW = float(sys.argv[2]) if len(sys.argv) > 2 else None
W, H, FPS = 1080, 1920, 30
S = "/tmp/claude-0/-home-user/9a61313d-511d-510f-9a34-284a91bf6e72/scratchpad"
FONT = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
FONT_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
FONT_S = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
CREAM, ESPRESSO, GOLD, TERRA = (245, 239, 230), (36, 24, 18), (199, 154, 90), (184, 90, 62)

IMG = {
    "S1": f"{S}/../images/14.jpg", "S3": f"{S}/../images/12.jpg",
    "S5": f"{S}/r17/s5-laundry.jpg", "S6": f"{S}/r17/s6-collar.jpg", "S8": f"{S}/r17/s8-bed3am.jpg",
    **{k: f"{S}/ugc/stills/{k}.png" for k in ["B1", "B2a", "B2b", "B2c", "B2d", "B2e", "B3b", "B4", "B6"]},
}
HOOK_IMG = {"H1": "S1", "H2": "S3", "H3": "S8"}[HOOK]
HOOK_TEXT = {"H1": "Where my scalp oil was actually going",
             "H2": "Try the towel test tonight",
             "H3": "Since the baby, this was my one thing"}[HOOK]
CALLOUT = "For moms who keep skipping their scalp oil routine"

# ---------- script text and word timing alignment ----------
md = open("/home/user/Kengokuhebun/ugc-video/ninu-ugc-green-screen-scripts.md").read()
body_md = md[md.index("## The locked body"):md.index("Spoken length")]
ROWS = re.findall(r'\| \d+ \| [^|]+\| "([^"]+)"', body_md)
HOOKS = dict(re.findall(r'\| \*\*(H\d)\*\* \| \w+ \| "([^"]+)"', md))
WORDS = json.load(open(f"{S}/edit/words.json"))

def norm(w):
    w = w.lower().replace("’", "'")
    w = re.sub(r"[^a-z0-9$']", "", w)
    return {"ninus": "ninu", "ninu's": "ninu", "nino": "ninu", "10pm": "10", "60ml": "60", "boil": "oil"}.get(w, w)

def align(text, recog):
    """Give every script token a (start, end) from the recognised words."""
    toks = text.split()
    a = [norm(t) for t in toks]
    b = [norm(w["w"]) for w in recog]
    times = [None] * len(toks)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            times[blk.a + k] = (recog[blk.b + k]["s"], recog[blk.b + k]["e"])
    # fill gaps: share the time between the neighbouring known words evenly
    i = 0
    while i < len(toks):
        if times[i] is not None: i += 1; continue
        j = i
        while j < len(toks) and times[j] is None: j += 1
        s0 = times[i - 1][1] if i > 0 else 0.0
        s1 = times[j][0] if j < len(toks) else s0 + 0.35 * (j - i)
        step = max(s1 - s0, 0.2 * (j - i)) / (j - i)
        for k in range(i, j): times[k] = (s0 + step * (k - i), s0 + step * (k - i + 1))
        i = j
    return list(zip(toks, times))

hook_tokens = align(HOOKS[HOOK], WORDS[HOOK])
body_text = " ".join(ROWS)
body_tokens = align(body_text, WORDS["BODY"])
TH = hook_tokens[-1][1][1] + 0.3                       # hook length
BODY_END = body_tokens[-1][1][1] + 0.9
TOTAL = TH + BODY_END
FULL_TOTAL = TOTAL
if PREVIEW: TOTAL = min(TOTAL, PREVIEW)

# row start times (body time)
row_start, idx = [], 0
for r in ROWS:
    row_start.append(body_tokens[idx][1][0]); idx += len(r.split())
row_start.append(BODY_END)

def word_time(row, word, nth=1):
    """Body time of the nth token in a row that starts with `word`."""
    base = sum(len(r.split()) for r in ROWS[:row])
    seen = 0
    for k, tok in enumerate(ROWS[row].split()):
        if norm(tok).startswith(norm(word)):
            seen += 1
            if seen == nth: return body_tokens[base + k][1][0]
    raise KeyError((row, word))

# ---------- visual schedule (global time) ----------
B = lambda t: TH + t
sched = [(0, TH, ("img", HOOK_IMG))]
R = row_start
sched.append((B(R[0]), B(R[1]), ("img", "B1")))
items = [("B2a", "shampoo"), ("B2b", "vitamins"), ("B2c", "satin"), ("B2d", "$88"), ("B2e", "10pm")]
cuts = [R[1]] + [word_time(1, w) for _, w in items[1:]] + [R[2]]
for (k, _), a, b in zip(items, cuts[:-1], cuts[1:]):
    sched.append((B(a), B(b), ("img", k)))
sched.append((B(R[2]), B(word_time(3, "fingers")), ("full",)))
sched.append((B(word_time(3, "fingers")), B(word_time(3, "towel", 2)), ("img", "B3b")))
sched.append((B(word_time(3, "towel", 2)), B(R[4]), ("img", "S3")))
sched.append((B(R[4]), B(word_time(4, "it", 2)), ("img", "S5")))
sched.append((B(word_time(4, "it", 2)), B(R[5]), ("img", "S6")))
sched.append((B(R[5]), B(R[6]), ("product",)))
sched.append((B(R[6]), B(R[7]), ("img", "B4")))
sched.append((B(R[7]), B(R[8]), ("full",)))
sched.append((B(R[8]), B(R[9]), ("img", "B6")))
sched.append((B(R[9]), B(R[11]), ("kit",)))
sched.append((B(R[11]), B(R[12]) + 0.01, ("split",)))

labels = [
    (max(B(R[0]), TH + 0.3), B(R[1]), "3 wake-ups. Skipped."),
    *[(B(a), B(b), t) for (_, _), a, b, t in zip(items, cuts[:-1], cuts[1:],
        ["New shampoo", "Vitamins", "Satin pillowcase", "$88 supplement", "10pm reminder"])],
    (B(word_time(3, "part")), B(word_time(3, "fingers")), "Part: barely damp"),
    (B(word_time(3, "fingers")), B(word_time(3, "towel", 2)), "Fingers: slick"),
    (B(word_time(3, "towel", 2)), B(R[4]), "Towel: soaked"),
    (B(word_time(4, "it", 2)), B(R[5]), "It was the method."),
    (B(R[5]), B(R[6]), "One hand · 2 minutes"),
    (B(R[6]), B(R[7]), "Dry towel"),
    (B(R[7]), B(R[8]), "Week 1 · Nothing to restart"),
]

# ---------- helpers ----------
_font = {}
def font(path, size):
    if (path, size) not in _font: _font[(path, size)] = ImageFont.truetype(path, size)
    return _font[(path, size)]

_txt = {}
def text_img(text, size, fill=(255, 255, 255), stroke=0, stroke_fill=(0, 0, 0), path=FONT, maxw=980, pill=None, align="center"):
    key = (text, size, fill, stroke, pill, path, maxw, align)
    if key in _txt: return _txt[key]
    f = font(path, size)
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if f.getlength(t) + 2 * stroke > maxw and cur: lines.append(cur); cur = w
        else: cur = t
    lines.append(cur)
    lh = int(size * 1.18)
    tw = int(max(f.getlength(l) for l in lines)) + 2 * stroke
    padx, pady = (34, 18) if pill else (4, 4)
    im = Image.new("RGBA", (tw + 2 * padx, lh * len(lines) + 2 * pady), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if pill: d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=min(40, im.height // 2), fill=pill)
    for i, l in enumerate(lines):
        x = padx + stroke + ((tw - 2 * stroke - f.getlength(l)) / 2 if align == "center" else 0)
        d.text((x, pady + i * lh), l, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    arr = np.array(im)
    _txt[key] = arr
    return arr

def paste(dst, rgba, x, y, alpha=1.0):
    h, w = rgba.shape[:2]
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, dst.shape[1]), min(y + h, dst.shape[0])
    if x1 <= x0 or y1 <= y0: return
    src = rgba[y0 - y:y1 - y, x0 - x:x1 - x]
    a = (src[..., 3:4].astype(np.float32) / 255.0) * alpha
    reg = dst[y0:y1, x0:x1].astype(np.float32)
    dst[y0:y1, x0:x1] = (src[..., :3] * a + reg * (1 - a)).astype(np.uint8)

_imgs = {}
def cover(key, w=W, h=H):
    k = (key, w, h)
    if k not in _imgs:
        im = cv2.cvtColor(cv2.imread(IMG[key]), cv2.COLOR_BGR2RGB)
        s = max(w * 1.1 / im.shape[1], h * 1.1 / im.shape[0])     # 10% headroom for the zoom
        _imgs[k] = cv2.resize(im, (int(im.shape[1] * s + 0.5), int(im.shape[0] * s + 0.5)), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
    return _imgs[k]

def kenburns(key, p, w=W, h=H):
    big = cover(key, w, h)
    z = 1.0 + 0.07 * p                                            # slow push-in
    cw, ch = int(w * 1.1 / z), int(h * 1.1 / z)
    cx, cy = big.shape[1] // 2, big.shape[0] // 2
    crop = big[cy - ch // 2:cy - ch // 2 + ch, cx - cw // 2:cx - cw // 2 + cw]
    return cv2.resize(crop, (w, h), interpolation=cv2.INTER_LINEAR)

class Clip:
    def __init__(self, path):
        self.cap = cv2.VideoCapture(path); self.i = -1; self.frame = None
        self.n = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
    def get(self, i):
        i = max(0, min(i, self.n - 1))
        if i < self.i:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, i); self.i = i - 1
        while self.i < i:
            ok, f = self.cap.read()
            if not ok: break
            self.frame = f; self.i += 1
        return self.frame

V = f"{S}/ugc/video"
hook_v, hook_m = Clip(f"{V}/{HOOK}.mp4"), Clip(f"{S}/edit/mask_{HOOK}.mp4")
body_v, body_m = Clip(f"{V}/BODY.mp4"), Clip(f"{S}/edit/mask_BODY.mp4")
product = Clip(f"{S}/edit/assets/product-in-use.mp4")

def presenter(t):
    if t < TH: i = int(t * FPS); v, m = hook_v.get(i), hook_m.get(i)
    else: i = int((t - TH) * FPS); v, m = body_v.get(i), body_m.get(i)
    return cv2.cvtColor(v, cv2.COLOR_BGR2RGB), m[..., 0]

# ---------- kit card ----------
def build_kit():
    card = np.zeros((H, W, 3), np.uint8); card[:] = CREAM
    d_im = Image.open(f"{S}/edit/assets/product-reference.png").convert("RGBA")
    b_im = Image.open(f"{S}/edit/assets/oil-bottle-cutout.png").convert("RGBA")
    pil = Image.fromarray(card).convert("RGBA")
    d = ImageDraw.Draw(pil)
    d.text((W // 2, 150), "The Ninu Kit", font=font(FONT, 92), fill=ESPRESSO, anchor="mm")
    d.text((W // 2, 245), "Everything for the routine, in one box", font=font(FONT_S, 40), fill=(120, 96, 80), anchor="mm")
    def place(im, cx, top, hgt):
        s = hgt / im.height; im = im.resize((int(im.width * s), hgt), Image.LANCZOS)
        pil.alpha_composite(im, (int(cx - im.width / 2), top))
    d.rounded_rectangle([90, 310, 990, 890], radius=40, fill=(255, 252, 247))
    place(d_im, 360, 340, 520)
    place(b_im, 740, 350, 500)
    y = 925
    for t in ["Ninu dispenser with silicone tips", "60ml scalp oil", "Satin sleep bonnet"]:
        d.ellipse([110, y + 6, 150, y + 46], fill=GOLD)
        d.line([(120, y + 27), (128, y + 35), (141, y + 17)], fill=(255, 255, 255), width=5)
        d.text((172, y + 26), t, font=font(FONT_B, 44), fill=ESPRESSO, anchor="lm")
        y += 72
    return np.array(pil.convert("RGB"))
KIT = build_kit()
kit_lines = [  # appear at the spoken word (body row, word)
    ((9, "$49.99"), "$49.99", 64, TERRA),
    ((9, "free"), "Free US shipping", 46, ESPRESSO),
    ((9, "about"), "About $1.67 a night", 46, ESPRESSO),
    ((10, "ships"), "Ships in 6 to 12 days", 42, ESPRESSO),
    ((10, "30-day"), "30-day money-back guarantee", 42, ESPRESSO),
]
kit_lines = [(B(word_time(*k)), t, s, c) for k, t, s, c in kit_lines]

# ---------- captions ----------
def chunks(tokens, offset):
    out, cur = [], []
    for tok, (s, e) in tokens:
        cur.append((tok, s + offset, e + offset))
        if len(cur) == 3 or tok[-1] in ".,?" or len(" ".join(c[0] for c in cur)) > 18:
            out.append(cur); cur = []
    if cur: out.append(cur)
    res = []
    for i, c in enumerate(out):
        end = out[i + 1][0][1] if i + 1 < len(out) else c[-1][2] + 0.4
        res.append((c[0][1], min(end, c[-1][2] + 0.6), c))
    return res
CAPS = chunks(hook_tokens, 0) + chunks(body_tokens, TH)

def caption_img(chunk, t):
    f = font(FONT, 70); stroke = 7
    words = [w for w, _, _ in chunk]
    txt = " ".join(words)
    tw = int(f.getlength(txt)) + 2 * stroke + 8
    im = Image.new("RGBA", (tw, 100), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x = stroke + 4
    for w, s, e in chunk:
        col = GOLD if s <= t < e + 0.05 else (255, 255, 255)
        d.text((x, 6), w, font=f, fill=col, stroke_width=stroke, stroke_fill=(0, 0, 0))
        x += f.getlength(w + " ")
    return np.array(im)

# ---------- render ----------
PW = int(720 * 0.6); PH = int(1280 * 0.6)                 # corner presenter 432 x 768
PX, PY = 20, H - PH
EDGE = np.ones(PW, np.float32); EDGE[-70:] = np.linspace(1, 0, 70); EDGE[:12] = np.linspace(0.3, 1, 12)
def frame_at(t):
    seg = next((s for s in sched if s[0] <= t < s[1]), sched[-1])
    kind = seg[2]; p = (t - seg[0]) / max(seg[1] - seg[0], 1e-3)
    pv, pm = presenter(t)
    if kind[0] == "img": out = kenburns(kind[1], p)
    elif kind[0] == "product":
        out = cv2.resize(cv2.cvtColor(product.get(int(p * (product.n - 1))), cv2.COLOR_BGR2RGB), (W, H), interpolation=cv2.INTER_CUBIC)
    elif kind[0] == "kit":
        out = KIT.copy()
        for at, txt, sz, col in kit_lines:
            if t >= at:
                a = min(1.0, (t - at) / 0.25)
                im = text_img(txt, sz, fill=col, path=FONT if sz > 50 else FONT_B, maxw=560, align="left")
                yy = 1180 + [x[1] for x in kit_lines].index(txt) * 92
                paste(out, im, 500, yy, a)
    elif kind[0] == "split":
        out = np.zeros((H, W, 3), np.uint8)
        out[:, :W // 2] = kenburns("S8", p, W // 2, H)
        out[:, W // 2:] = kenburns("B4", p, W // 2, H)
        out[:, W // 2 - 3:W // 2 + 3] = 255
        paste(out, text_img("Sunday again", 50, fill=(255, 255, 255), pill=(0, 0, 0, 170)), 40, 300)
        paste(out, text_img("Tonight", 50, fill=ESPRESSO, pill=(245, 239, 230, 235)), W // 2 + 60, 300)
    else:  # full-screen presenter
        out = cv2.resize(pv, (W, H), interpolation=cv2.INTER_CUBIC)
    if kind[0] != "full":
        sm = cv2.resize(pv, (PW, PH), interpolation=cv2.INTER_AREA)
        mm = (cv2.resize(pm, (PW, PH), interpolation=cv2.INTER_AREA) * EDGE[None, :]).astype(np.uint8)
        paste(out, np.dstack([sm, mm]), PX, PY)
    # hook overlay + call-out
    if t < TH + 0.3:
        a = min(1.0, t / 0.2) * (1.0 if t < TH else max(0.0, (TH + 0.3 - t) / 0.3))
        hi = text_img(HOOK_TEXT, 76, fill=(255, 255, 255), stroke=0, pill=(36, 24, 18, 225), maxw=900)
        paste(out, hi, (W - hi.shape[1]) // 2, 170, a)
        ci = text_img(CALLOUT, 40, fill=ESPRESSO, pill=(245, 239, 230, 235), path=FONT_B, maxw=900)
        paste(out, ci, (W - ci.shape[1]) // 2, 170 + hi.shape[0] + 18, a)
    # beat labels
    for a0, a1, txt in labels:
        if a0 <= t < a1:
            li = text_img(txt, 56, fill=(255, 255, 255), pill=(36, 24, 18, 220), maxw=900)
            paste(out, li, (W - li.shape[1]) // 2, 210, min(1.0, (t - a0) / 0.15))
    # captions
    for c0, c1, ch in CAPS:
        if kind[0] == "kit": break
        if c0 <= t < c1:
            ci = caption_img(ch, t); paste(out, ci, (W - ci.shape[1]) // 2, 1000 if kind[0] != "kit" else 1180 - 260)
            break
    # end card CTA + label
    if t >= FULL_TOTAL - 2.2:
        cta = text_img("Tap Shop Now", 64, fill=(255, 255, 255), pill=(184, 90, 62, 240))
        paste(out, cta, 760 - cta.shape[1] // 2, 1560, min(1.0, (t - (FULL_TOTAL - 2.2)) / 0.2))
    dr = text_img("Dramatisation", 30, fill=(255, 255, 255), path=FONT_S, pill=(0, 0, 0, 120))
    paste(out, dr, W - dr.shape[1] - 24, H - dr.shape[0] - 28)
    return out

name = f"{S}/edit/out/ninu-ugc-{HOOK}" + ("-preview" if PREVIEW else "")
import os; os.makedirs(f"{S}/edit/out", exist_ok=True)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", f"{name}-v.mp4"], stdin=subprocess.PIPE)
nf = int(TOTAL * FPS)
for f in range(nf):
    enc.stdin.write(frame_at(f / FPS).tobytes())
    if f % 300 == 0: print(f"{HOOK} frame {f}/{nf}", flush=True)
enc.stdin.close(); enc.wait()
# audio: hook speech then body speech
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{V}/{HOOK}.mp4", "-i", f"{V}/BODY.mp4", "-i", f"{name}-v.mp4",
                "-filter_complex", f"[0:a]atrim=0:{TH:.3f},asetpts=PTS-STARTPTS[a0];[1:a]atrim=0:{BODY_END:.3f},asetpts=PTS-STARTPTS[a1];[a0][a1]concat=n=2:v=0:a=1,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
                "-map", "2:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", f"{name}.mp4"], check=True)
os.remove(f"{name}-v.mp4")
print("done", name, f"{TOTAL:.1f}s", "hook", f"{TH:.2f}", "rows", [round(x, 2) for x in R])
