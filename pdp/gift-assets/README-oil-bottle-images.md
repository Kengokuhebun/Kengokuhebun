# Updating the oil bottle in the page images

Written 2026-11-06. The bottle that ships is **MELAO Rosemary Essential Oil, 60ml / 2 fl oz**: an amber glass bottle with a black dropper cap and a green label (MELAO, a hair illustration, "Rosemary Essential Oil", 60ml/2fl.oz). The page images show a different bottle (a short brown bottle with a cream "Ninu Scalp Oil" label and no dropper).

## What I made

- `oil-bottle-tile-cream.png`: the real bottle on the page cream with a soft shadow, for small tiles and icons.
- `oil-bottle-cutout.png`: the real bottle on a transparent background.

The photo you sent is only 187 x 544 px. That is fine for an icon about 150 px tall, and too small for a gallery image. For the gallery, get a higher-resolution photo (from the supplier or your own, when the sample arrives).

## Which gallery images show the old bottle

(Numbers match `pdp/previews/gallery-contact-sheet.png`, the order of the slides on the page.)

| Slide | Problem | Action |
|---|---|---|
| 1 Hero | Old Ninu-labelled bottle, no dropper. Also says "EBOOK" | Replace the bottle (prompt below). Rewrite the caption when the gifts go live |
| 9 "Everything the routine needs. One kit." | Old bottle. Also "$39.99 value", "$24 value", "$14 value" labels | Replace the bottle. Remove the "value" labels (see below) |
| 3, 4, 7, 8 | Dispenser only, no bottle | No bottle change |

## Other things on the gallery that don't match the real product or your own copy

Not what you asked, but these are the same kind of mismatch and I found them while checking.

| Slide | What it says | Issue |
|---|---|---|
| 9 | "$39.99 value", "$24 value", "$14 value" | Value claims you can't back unless you sell those items at those prices |
| 10 | "Hair doesn't absorb oil. Skin does." | An absolute claim a knowledgeable reader can dispute. Replace with "Oil on your scalp, not on your hair" |
| 12 "The facts" | Shipping "Free US, 5 to 7 days" | The page and supplier say 6 to 12 days |
| 12 vs 7 | Weight "60g" on slide 12, "under 90 grams" on slide 7 | They contradict each other. Check the real weight |
| 12 | "Included: Dispenser + 60ml oil + bonnet + ebook" | Out of date once the gifts go live |
| 6 | "Glide, don't scrub" and "No massaging. No fingers" | I can't confirm how your dispenser is used (the guide says "press"). Check against the real product. Also conflicts with the massager gift on wash day |
| 5 | "Shedding is hormonal and runs its own timeline" | A health-adjacent statement. Safer to delete |

## The bottle on the product

The label says **Rosemary Essential Oil** and carries supplier hair claims ("scalp and hair care oil", "nourishing split hair and dry scalps"). Three things follow:

1. **Don't label the bottle "Ninu" in any image.** It would misrepresent what the customer receives.
2. **The page calls it "60ml scalp oil".** The bottle calls it rosemary essential oil. Name it on the page as **60ml rosemary oil**, and don't repeat the label's hair claims.
3. **Get the ingredient list.** "Essential oil" is normally diluted before skin contact. Ask the supplier whether the bottle is neat essential oil or blended with a carrier, and add a patch-test and nursing/pregnancy line on the page.

The MELAO name will be visible on the bottle in the photos, so a customer can search for it. That's accurate and honest, but it means they can compare prices. Decide whether you're comfortable with that.

## Prompts (edit the existing slide, don't redraw it)

Use Nano Banana Pro or Nano Banana 2 in edit mode. Attach **two images**: image 1 is the existing slide, image 2 is the bottle photo. Generate 4 variations and compare each to the real bottle.

### Slide 1 (hero)

```
Edit image 1. Replace only the small brown bottle on the right, the one with the cream label reading Ninu Scalp Oil, with the bottle from image 2: an amber glass dropper bottle with a black rubber dropper cap and a green label reading MELAO, ROSEMARY ESSENTIAL OIL, 60ml/2fl.oz. Reproduce the new bottle with absolute fidelity to its exact shape, proportions, label layout, label artwork and printed text.

Keep everything else in image 1 exactly as it is: the dispenser, the satin bonnet, the card, the headline, the caption, the background and the colours. Match the existing scene lighting for the new bottle: soft light from the left, a faint contact shadow on the surface. The bottle stands upright and is slightly smaller than the dispenser, as the original bottle was. No other changes.
```

### Slide 9 (flat lay)

```
Edit image 1. Replace only the bottle in the top-right panel (the cream label reading Ninu Scalp Oil) with the bottle from image 2: an amber glass dropper bottle with a black rubber dropper cap and a green label reading MELAO, ROSEMARY ESSENTIAL OIL, 60ml/2fl.oz. Reproduce it with absolute fidelity to its shape, proportions, label layout and printed text, photographed from directly above, lying on its side as a flat-lay item would, with the dropper cap on one side.

Keep the rest of image 1 exactly as it is, including the dispenser, the bonnet, the card, the layout and the lighting. No other changes.
```

### Check every result

- Black dropper cap present; amber glass; green label.
- Label text reads MELAO, ROSEMARY ESSENTIAL OIL, 60ml/2fl.oz. Small label text is the usual failure.
- No leftover "Ninu Scalp Oil" text.
- Everything else is unchanged.

If the text comes out garbled, don't use it. Fix it by pasting `oil-bottle-cutout.png` over the bottle in Canva or Figma at the right size, or use a higher-resolution photo of the real bottle.

## After the gifts are sourced

Slides 1, 9 and 12 should be redone from real photos of the real items: dispenser, bottle, bonnet, massager, pouch. I'll write those prompts when you have the photos.
