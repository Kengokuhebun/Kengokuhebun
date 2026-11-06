# Scalp massager image for the gift block

Written 2026-11-06. Two ways to get a clean tile image of the free scalp massager.

## Option A: the cutout (ready now, 100% accurate to the item)

Files in this folder:
- `scalp-massager-tile-cream.png` is an 800 x 600 tile on the page's cream (#F1E7D8) with a soft contact shadow. It is ready to use.
- `scalp-massager-cutout.png` is the item on a transparent background.

Both come from the supplier photo you sent, which is 520 x 445. That is plenty for a tile shown at about 170 to 250 px wide, but it will look soft if shown larger.

To use it in the gift block:
1. Upload `scalp-massager-tile-cream.png` in Shopify: Settings, then Files. Copy the file URL.
2. In `pdp/ninu-pdp.html`, find the "Scalp massager" tile. Replace the whole `<svg ...>...</svg>` inside `<span class="ninu-g-i">` with:
   `<img src="PASTE_FILE_URL" alt="Scalp massager">`

## Option B: a generated hero image (higher resolution)

Use Nano Banana Pro (or Nano Banana 2), with the supplier photo attached as the reference image at high influence. Aspect ratio 4:3 (the tile crops to about 1:0.72), resolution 2k. Set the aspect ratio in the generator, not in the prompt.

```
A single speckled oatmeal-grey silicone scalp massager, centred on a smooth warm cream surface, the clean product tile of a premium gift block.

The massager from the attached reference image, reproduced with absolute fidelity to its exact shape, proportions, matte speckled stone-grey silicone finish, the looped handle with its round hole, and the cone-shaped bristles underneath. Do not change the number, length or colour of the bristles. Do not add any logo, text or brand mark.

Composition: a three-quarter side view as in the reference, centred, filling about 60 percent of the frame width, with generous clean margin on every side so it can be cropped to a wide tile.

Lighting: soft wrapping light from a large diffused source at forty-five degrees camera left, slightly above the object, about 5500K, with a white reflector card on the right for gentle fill. A faint, soft contact shadow directly beneath the bristles. No hard shadows, no visible lights or equipment.

Background: a seamless warm cream surface, hex F1E7D8, no props, no gradient banding, nothing else in the frame. No hands, no hair, no scalp, no water.

Camera and lens: Canon EOS R5 with a 100mm macro lens at f/8 for edge-to-edge sharpness.

Colour grade: warm, soft and natural, clean whites with a faint cream cast, matte finish. Premium but honest, a real product photograph and not a render.
```

### Check every result against the real item

- The handle loop and its round hole are there.
- The bristles are cone-shaped, about 10 to 12 visible, the same colour as the body or a touch warmer, and not longer or more numerous than the reference.
- The colour is a speckled grey, not pure white or beige.
- There is no text, logo or extra object.

Generators sometimes redraw small details. If any check fails, use Option A.

## Rules

- The image must match what ships. If the supplier changes the colour or shape, redo it from a photo of the item you actually receive.
- Replace it with your own photo of the item as soon as you have a sample.
