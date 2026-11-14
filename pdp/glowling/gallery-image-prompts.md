# Glowling: Gallery Image Prompts (Seedream 4.5 / 5.0 via KIE)

These recreate the competitor's five gallery shots (same job, layout and scene type) as Glowling images, plus three extra shots for the screen-time angle. Following the Master Document, generate a white-background master reference first, then attach it to every prompt.

**Global settings**
- Aspect ratio 1:1, 2048 × 2048. Photoreal, soft cinematic light, shallow depth of field.
- Brand palette (matches the PDP blocks): night navy `#1D2340`, glow yellow `#FFD36E`, warm cream `#FFF8EC`, accent neon pink `#FF5FA2` and teal `#3FE0C5`. The competitor uses brown; we use navy and cream so we don't look like a copy.
- Fonts on graphics: a rounded bold sans (e.g. Nunito ExtraBold) for headlines, regular for sub-lines.
- Text: Seedream 4.5 handles short headlines well. If small text comes out garbled, generate the image with `"text": "none"` and add the copy in Canva.
- **Product lock:** every image must show the same board: a clear rectangular acrylic panel (landscape, about 30 × 20 cm, rounded corners) standing upright in a white base with an X-shaped foot and a short centre support fin, a warm LED strip along the bottom edge, and white-barrel fluorescent markers with coloured caps. **If your supplier's board differs (e.g. a wooden base), change this description and the master reference to match what you actually ship.**
- Never show a brand logo other than Glowling, never add fake reviews or star ratings, and never write health claims (e.g. "eye-friendly", "safe light") on images.

---

## 0. Master reference (not in the gallery)
**Job:** gives Seedream an exact product to copy in every later image.
**Attach:** the clearest supplier photos of the board and markers.
```json
{
  "task": "product photograph for reference",
  "subject": "clear rectangular acrylic LED drawing board, landscape, approx 30x20cm, rounded corners, standing upright in a white plastic base with an X-shaped foot and a short centre support fin, warm white LED strip glowing along the bottom edge of the panel, panel completely blank; in front, 8 fluorescent marker pens with white barrels and caps in pink, orange, yellow, green, blue, purple, red, white, lying in a neat fan",
  "background": "pure seamless white #FFFFFF",
  "lighting": "even softbox studio light, subtle contact shadow",
  "camera": "front three-quarter view, 50mm, eye level with panel centre, everything in sharp focus",
  "style": "high-end ecommerce packshot, photoreal",
  "text": "none",
  "negative": "logos, text, hands, props, reflections of people, extra stands, distorted acrylic, duplicate markers"
}
```
Check it against the supplier photos (base shape, LED strip position, marker count) before you go on.

---

## 1. Hero lifestyle (recreates competitor image 1)
**Answers:** what is it, and will my child love it?
**Attach:** master reference.
```json
{
  "task": "lifestyle hero product photo",
  "scene": "a 5-year-old child in a knitted rust-coloured jumper sits at a warm wooden kids' desk in a cosy bedroom at dusk, focused and smiling slightly, drawing with a white fluorescent marker on the glowing Glowling LED board",
  "drawing_on_board": "a neon rocket ship with flames and five stars around it, lines glowing pink, orange, yellow and teal against the lit acrylic",
  "props": "wooden pencil cup holding the fluorescent markers on the left, a small stack of picture books and a soft teddy bear on the right, bookshelf softly out of focus behind",
  "lighting": "room lights dim and warm, the board's glow lighting the child's face from below and in front, golden hour light from a window edge",
  "camera": "straight-on at desk height, 50mm, child centred behind the board, f/2.8 background blur",
  "product_fidelity": "board, base and markers must match the reference image exactly",
  "text": "none",
  "negative": "screens, tablets, phones, logos, extra fingers, warped acrylic, text on board other than the drawing"
}
```

## 2. How it works + benefits infographic (recreates competitor image 2)
**Answers:** how does it work, and what do I get from it?
**Attach:** master reference.
```json
{
  "task": "ecommerce infographic",
  "layout": "top third: headline + three steps left-to-right joined by arrows, each with a thin-line icon in navy; middle: the Glowling board on a wooden coffee table in a softly blurred cream living room, glowing; bottom third: three benefit icons with labels",
  "headline": "How Glowling Works",
  "steps": [
    {"icon": "hand drawing with marker", "label": "1. DRAW", "sub": "Draw on the clear panel with the neon markers"},
    {"icon": "panel with light rays", "label": "2. GLOW", "sub": "Switch on and watch it light up"},
    {"icon": "hand wiping with cloth", "label": "3. WIPE & REPEAT", "sub": "A damp cloth clears it in seconds"}
  ],
  "drawing_on_board": "an Australian summer Christmas scene: a glowing Christmas tree, a smiling sun in a Santa hat, a koala with a present, the words 'Merry Christmas' in neon bubble letters",
  "benefits": [
    {"icon": "lightbulb", "label": "CREATES, NOT SCROLLS"},
    {"icon": "recycle arrows", "label": "ENDLESSLY REUSABLE"},
    {"icon": "plug", "label": "USB POWERED"}
  ],
  "palette": "cream #FFF8EC background, navy #1D2340 text and icons, glow yellow #FFD36E accents",
  "style": "clean modern infographic over photoreal product, generous margins",
  "negative": "brown colour scheme, competitor wording, health claims, logos other than Glowling, misspelt words"
}
```

## 3. Lifestyle collage + benefits panel (recreates competitor image 3)
**Answers:** what does it look like in real life, day and night?
**Attach:** master reference.
```json
{
  "task": "collage product graphic",
  "layout": "left two-thirds: one large top photo + two small photos side by side + one wide bottom photo, rounded corners, thin cream borders; right third: navy #1D2340 vertical panel with three round icons and labels; bottom-right corner: small cream box with the Glowling wordmark and the line 'Glow time, not screen time'",
  "photos": [
    "the glowing board on a bedroom desk at night, neon drawing of planets and stars",
    "a smiling girl about 6 drawing a neon rainbow on the board flat on a table, face lit by the glow",
    "two siblings laughing while drawing together on the same board",
    "a child asleep in bed, the board on the bedside table glowing softly with a moon and stars drawing"
  ],
  "panel_items": [
    {"icon": "sparkle", "label": "SPARKS CREATIVITY", "sub": "Drawing, letters and games"},
    {"icon": "recycle", "label": "WIPE & REUSE", "sub": "A fresh page every time"},
    {"icon": "moon", "label": "NIGHT LIGHT TOO", "sub": "A calm glow for bedtime"}
  ],
  "style": "warm, cosy, photoreal photos; crisp flat panel graphics",
  "negative": "fake reviews, star ratings, customer faces with names, tablets, phones, misspelt words"
}
```
*Change from the competitor:* their bottom-right "Sarah M. ★★★★★ Best gift ever" card is a stock face with an invented review. Swap in a real customer photo and review once you have one; until then use the tagline.

## 4. Four use cases grid (recreates competitor image 4)
**Answers:** what else can it do besides drawing?
**Attach:** master reference.
```json
{
  "task": "2x2 use-case grid",
  "layout": "four equal photo tiles with a navy label strip under each tile, line icon left of each label",
  "tiles": [
    {"photo": "a girl drawing a neon Christmas tree on the glowing board at a desk", "label": "CREATIVE DRAWING", "sub": "Neon art that glows"},
    {"photo": "a boy in pyjamas writing a spelling list on the board on his bed", "label": "LETTERS & NOTES", "sub": "Practise words, leave messages"},
    {"photo": "a child tracing a printed cartoon animal placed on the lit board", "label": "TRACING FUN", "sub": "Trace any picture"},
    {"photo": "a child asleep, board on the bedside table glowing with a moon and stars", "label": "NIGHT LIGHT", "sub": "A soft glow for bedtime"}
  ],
  "palette": "navy #1D2340 label strips, cream text, glow yellow icons",
  "negative": "copyrighted cartoon characters on the tracing page, misspelt words, logos"
}
```
Use an original animal on the tracing sheet, never a licensed character.

## 5. Size + features (recreates competitor image 5)
**Answers:** how big is it, and what are the key features?
**Attach:** master reference.
```json
{
  "task": "product dimensions graphic",
  "scene": "the glowing Glowling board on a wooden desk in a dim warm room, a desk lamp off to the left, the fluorescent markers fanned in front, a small plant behind",
  "drawing_on_board": "'Merry Christmas' in neon bubble letters with snowflakes, a tree and a snowman",
  "annotations": "white thin dimension arrow on the left side reading '20 cm' and along the bottom reading '30 cm'",
  "right_panel": "navy #1D2340 vertical strip with four round cream icons and labels: 'GLOWING LED', 'WIPE & REUSE', 'BUILDS FOCUS', 'GIFT READY'",
  "style": "photoreal product shot with clean flat graphics",
  "negative": "wrong dimensions, logos, misspelt words, competitor brown colour"
}
```
**Put your real board size in the dimension labels.** The 30 × 20 cm here is a placeholder.

---

## Extra shots for the screen-time angle (not in the competitor's gallery)

### 6. Glowling vs the tablet (comparison)
```json
{
  "task": "split comparison image",
  "layout": "vertical split; left half desaturated blue-grey, right half warm and glowing",
  "left": "a child slumped on a couch with a blank-faced stare at a tablet, room dark and cold, label 'SCREEN TIME' with three small ✖ lines: 'Autoplay', 'Ads', 'Meltdown when it's off'",
  "right": "the same child sitting up at a table, smiling, drawing a neon dinosaur on the glowing Glowling board, label 'GLOW TIME' with three ✔ lines: 'Creating', 'Calm', 'Off with no fight'",
  "palette": "right side cream, navy and glow yellow",
  "negative": "real app logos, real tablet brand logos, misspelt words"
}
```
Only keep "Off with no fight" if your customer reviews support it. Otherwise use "No apps".

### 7. Dinner-time scene (matches the PDP problem section)
```json
{
  "task": "lifestyle photo",
  "scene": "early evening kitchen, a parent cooking at the stove in soft focus in the background, a 4-year-old at the kitchen bench in the foreground happily drawing on the glowing Glowling board, steam from a pot, warm lights",
  "camera": "35mm, child and board sharp, parent blurred",
  "text": "headline top-left in navy: 'Dinner's on. They're busy.'",
  "negative": "tablets, phones, logos, extra fingers"
}
```

### 8. What's in the box + gift
```json
{
  "task": "flat lay",
  "scene": "top-down flat lay on cream linen: the Glowling board laid flat and glowing, the stand, 8 fluorescent markers in a neat row, the USB cable coiled, a gift box with a navy ribbon and a small tag reading 'For Posy, from Nan & Pop'",
  "annotations": "thin navy leader lines with labels: '1 × LED board', '8 × neon markers', '1 × stand', '1 × USB cable'",
  "text_top": "Everything in the box",
  "negative": "items you don't ship, logos, misspelt words"
}
```
Change the counts to match your supplier's actual box contents.

---

## Gallery order
1 Hero → 2 How it works → 6 vs the tablet → 4 Four uses → 3 Day & night collage → 5 Size & features → 7 Dinner-time → 8 What's in the box.
Images 6 and 7 carry the screen-time angle from the ads, so they sit high in the order. That way the page matches the ad that sent people there.
