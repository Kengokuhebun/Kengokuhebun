import sys, os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
TEXT = "Ends Cyber Monday"

def add_banner(src, dst, text=TEXT):
    im = Image.open(src).convert("RGB")
    W, H = im.size
    ft = ImageFont.truetype(os.path.join(HERE, "fonts", "Nunito.ttf"), int(W * 0.046))
    ft.set_variation_by_name("ExtraBold")
    d = ImageDraw.Draw(im)
    l, t, r, b = d.textbbox((0, 0), text, font=ft)
    tw, th = r - l, b - t
    padx, pady = int(W * 0.035), int(W * 0.022)
    pw, ph = tw + 2 * padx, th + 2 * pady
    x1 = int(W * 0.97) - pw
    y0 = int(W * 0.025)
    d.rounded_rectangle((x1, y0, x1 + pw, y0 + ph), radius=ph // 2, fill=(255, 255, 255))
    d.text((x1 + padx - l, y0 + pady - t), text, font=ft, fill=(20, 20, 20))
    im.save(dst, quality=95)

if __name__ == "__main__":
    add_banner(sys.argv[1], sys.argv[2], *(sys.argv[3:4]))
